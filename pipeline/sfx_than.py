# -*- coding: utf-8 -*-
r"""sfx_than.py — HIỆU ỨNG ÂM THANH cho THÂN video (không chỉ hook), lane khai `assemble.sfx.enabled`.

Vì sao (anh chốt 2026-09-24 sau khi xem Lane L ep01): video chỉ có giọng + hook có SFX thì nghe "trống"; phải có
tiếng động đúng lúc (điện thoại reo, cửa mở, giấy trượt, tiếng chuông nhẹ khi đưa số liệu…) cho chuyên nghiệp.

Chia việc đúng luật 2 máy:
  MÁY 1 (cần hiểu nội dung)  `--plan`  : model SỬA (script.patch_model) đọc câu + mốc giây (voice_roles.json) và CHỌN
                                         khoảnh khắc + loại tiếng trong KHO của lane → `sfx_plan.txt` (dòng `câu|khoá`).
                                         Máy kiểm: khoá thuộc kho, câu tồn tại, bỏ câu trong hook, giãn cách ≥ min_gap_s.
  MÁY 1 hoặc 2 (cơ học)     `--kho`   : sinh các file trong kho qua ai33 `/v1/task/sound-effect` (duration AUTO —
                                         memory sfx-ai33-mac-dinh-auto) vào `assets/<lane>/_sfx/<khoá>.mp3`, có rồi thì bỏ qua.
  MÁY 2 (cơ học, B8)         `--tron`  : trộn SFX vào tiếng `final.mp4` tại mốc câu (+lệch), video giữ nguyên (-c:v copy).

Profile:
  "assemble": {"sfx": {"enabled": true, "vol": 0.35, "min_gap_s": 18, "max_n": 40,
                        "bank": {"phone_ring": "an office desk phone ringing twice", ...}}}

Dùng:
  py -3.13 sfx_than.py --profile shakai_no_naze --slug <thư mục tập> --plan
  py -3.13 sfx_than.py --profile shakai_no_naze --slug <thư mục tập> --kho
  py -3.13 sfx_than.py --profile shakai_no_naze --slug <thư mục tập> --tron
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import profiles  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def cfg_of(prof):
    return ((prof.get("assemble") or {}).get("sfx") or {})


def kho_dir(prof):
    return ROOT / prof.get("slug_dir", f"assets/{prof['id']}") / "_sfx"


def _hook_end(d: Path):
    tl = d / "hook" / "hook_timeline.json"
    if tl.exists():
        try:
            return float(json.loads(tl.read_text(encoding="utf-8")).get("hook_voice_end_s") or 0)
        except Exception:
            return 0.0
    return 0.0


# ---------------------------------------------------------------- --plan (máy 1)
def _prompt(cues, bank, cfg):
    ds = "\n".join(f"{c['i']}|{c['start']:.0f}s|{c['vai']}|{c['text']}" for c in cues)
    kho = "\n".join(f"- {k}: {v}" for k, v in bank.items())
    return (
        "あなたは日本の漫画解説動画の音響演出担当です。下の台本（番号|開始秒|話者|文）に、効果音を付ける場所を選んでください。\n"
        f"使える効果音（キー: 内容）:\n{kho}\n\n"
        "ルール:\n"
        "1. 文の中で実際に音がする出来事（電話が鳴る、ドアが開く、紙を置く、雨、足音、缶を置く等）には、その出来事の文に対応する効果音。\n"
        "2. 統計の数字や調査結果を初めて示す文には data_reveal（1つの数字に1回だけ）。\n"
        "3. 大きな転換（時は遡る、季節が変わる、一年後、回想から現在へ）には scene_whoosh。\n"
        "4. 緊張が最高潮になる瞬間には tension_hit（全体で最大4回）。温かい結末や和解には warm_chime（最大2回）。\n"
        f"5. 合計 {cfg.get('min_n', 18)}〜{cfg.get('max_n', 40)} 個。同じ効果音を連続させない。音のない心理描写には付けない。\n"
        "6. 一覧にない効果音は使わない。\n\n"
        "出力形式（厳守）: 1行に1つ `番号|キー` のみ。説明・空行・マークダウン禁止。番号順。\n\n"
        f"台本:\n{ds}")


def plan(prof, d: Path):
    import claude_p_bridge
    cfg = cfg_of(prof)
    bank = cfg.get("bank") or {}
    if not bank:
        raise SystemExit("✗ assemble.sfx.bank trống")
    # Máy 1 CHƯA có voice_roles.json (lồng tiếng là việc máy 2) → câu lấy từ script.txt + vai.txt (cùng luật cắt
    # cau_vai nên số câu = chỉ số cue trong voice_roles.json máy 2 sinh ra); mốc giây ƯỚC theo char_rate chỉ để giãn cách.
    import cau_vai
    cau = cau_vai.tach_cau((d / "script.txt").read_text(encoding="utf-8"))
    vai = {r["i"]: r["id"] for r in cau_vai.doc_vai(d / "vai.txt")} if (d / "vai.txt").exists() else {}
    cps = profiles.char_rate(prof) / 60.0
    t, cues = 0.0, []
    for c in cau:
        cues.append({"i": c["i"], "start": t, "vai": vai.get(c["i"], "?"), "text": c["text"], "para": c["para"]})
        t += len(cau_vai._chuan(c["text"])) / cps + 0.4
    # hook (đoạn 1 khi script mở bằng hook) đã có SFX riêng trong hook_timeline.json → bỏ
    # 2026-09-25 (ep02): hook viết mỗi câu 1 dòng → trải nhiều "đoạn" (cau_vai: mỗi dòng = 1 đoạn), bỏ para==1 là SÓT
    # câu hook 2..n → tiếng thân chồng tiếng hook. Bỏ theo SỐ CÂU của hook_locked.txt (script mở bằng hook).
    hl = d / "hook" / "hook_locked.txt"
    n_hook = len(cau_vai.tach_cau(hl.read_text(encoding="utf-8"))) if hl.exists() else 0
    than = [c for c in cues if c["i"] > n_hook]
    r = claude_p_bridge.ask(_prompt(than, bank, cfg), model=claude_p_bridge.patch_model_of(prof), timeout=1500,
                            min_chars=20)
    (d / "logs").mkdir(exist_ok=True)
    (d / "logs" / "sfx_plan_raw.txt").write_text(r.text, encoding="utf-8")
    by = {c["i"]: c for c in than}
    gap = float(cfg.get("min_gap_s", 18))
    out, bo, last = [], [], -1e9
    for ln in r.text.splitlines():
        m = re.match(r"^\s*(\d+)\s*\|\s*([a-z_0-9]+)\s*$", ln.strip())
        if not m:
            continue
        i, k = int(m.group(1)), m.group(2)
        if k not in bank or i not in by:
            bo.append(f"{i}|{k} (khoá/câu lạ)")
            continue
        if by[i]["start"] - last < gap:
            bo.append(f"{i}|{k} (sát cái trước {by[i]['start'] - last:.0f}s)")
            continue
        out.append((i, k))
        last = by[i]["start"]
    out = out[: int(cfg.get("max_n", 40))]
    (d / "sfx_plan.txt").write_text("".join(f"{i}|{k}|{by[i]['text']}\n" for i, k in out), encoding="utf-8")
    print(f"[sfx_than] ✓ sfx_plan.txt {len(out)} tiếng" + (f" · bỏ {len(bo)}: {bo[:6]}" if bo else ""))
    return out


# ---------------------------------------------------------------- --kho (sinh file tiếng)
def kho(prof):
    import openspeaker_tts as osp
    import requests
    cfg = cfg_of(prof)
    kd = kho_dir(prof)
    kd.mkdir(parents=True, exist_ok=True)
    H = {"xi-api-key": osp.API_KEY}
    for k, txt in (cfg.get("bank") or {}).items():
        f = kd / f"{k}.mp3"
        if f.exists():
            continue
        r = requests.post(f"{osp.BASE}/v1/task/sound-effect", headers=H,
                          json={"text": txt, "prompt_influence": 0.3, "loop": False}, timeout=60).json()
        tid = r.get("task_id") or (r.get("data") or {}).get("task_id")
        if not tid:
            raise SystemExit(f"✗ sound-effect {k}: {str(r)[:200]}")
        for _ in range(80):
            time.sleep(3)
            t = requests.get(f"{osp.BASE}/v1/task/{tid}", headers=H, timeout=30).json()
            dd = t.get("data") if isinstance(t.get("data"), dict) else t
            if dd.get("status") == "done":
                f.write_bytes(requests.get((dd.get("metadata") or {}).get("audio_url"), timeout=60).content)
                print(f"  ✓ {k}.mp3")
                break
            if dd.get("status") in ("failed", "error"):
                raise SystemExit(f"✗ sound-effect {k} lỗi: {str(dd)[:200]}")
        else:
            raise SystemExit(f"✗ sound-effect {k}: quá giờ")
    print(f"[sfx_than] ✓ kho {kd} ({len(list(kd.glob('*.mp3')))} file)")


# ---------------------------------------------------------------- --tron (máy 2, cơ học)
def tron(prof, d: Path, video=None):
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    cfg = cfg_of(prof)
    pf = d / "sfx_plan.txt"
    if not pf.exists():
        raise SystemExit(f"✗ thiếu {pf} — máy 1 chạy sfx_than.py --plan trước khi giao")
    cues = {c["i"]: c for c in json.loads((d / "voice_roles.json").read_text(encoding="utf-8"))}
    kd = kho_dir(prof)
    viec = []
    for ln in pf.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        i, k, *_ = ln.split("|")
        f = kd / f"{k}.mp3"
        if not f.exists():
            raise SystemExit(f"✗ thiếu {f} — chạy sfx_than.py --kho")
        viec.append((cues[int(i)]["start"] + float(cfg.get("lech_s", 0.15)), f))
    video = Path(video) if video else d / "final.mp4"
    tmp = video.with_suffix(".sfx.mp4")
    vol = float(cfg.get("vol", 0.35))
    ins, fc, mix = ["-i", str(video)], ["[0:a]aresample=48000[a0]"], ["[a0]"]
    dinh = {}

    def _gain(f):
        # File ai33 lệch nhau rất xa (đo thật kho Lane L: đỉnh −35 → 0 dBFS) → đưa đỉnh về −3 dBFS rồi mới nhân vol,
        # không thì tiếng này mất hút, tiếng kia át giọng. Trần +24 dB để khỏi kéo cả tiếng xì nền lên.
        if f not in dinh:
            err = subprocess.run([FF, "-i", str(f), "-af", "volumedetect", "-f", "null", "-"], capture_output=True,
                                 text=True, encoding="utf-8", errors="replace").stderr
            m = re.search(r"max_volume:\s*(-?[\d.]+)", err)
            dinh[f] = min(24.0, -3.0 - float(m.group(1))) if m else 0.0
        return vol * (10 ** (dinh[f] / 20))

    for j, (t, f) in enumerate(viec, 1):
        ins += ["-i", str(f)]
        ms = int(t * 1000)
        fc.append(f"[{j}:a]aresample=48000,volume={_gain(f):.4f},adelay={ms}|{ms}[s{j}]")
        mix.append(f"[s{j}]")
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[aout]")
    subprocess.run([FF, "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(video)
    print(f"[sfx_than] ✓ trộn {len(viec)} tiếng vào {video.name} (vol {vol})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true")
    g.add_argument("--kho", action="store_true")
    g.add_argument("--tron", action="store_true")
    ap.add_argument("--video", default="")
    a = ap.parse_args()
    prof = profiles.load(a.profile)
    d = Path(a.slug).resolve()
    if a.plan:
        plan(prof, d)
    elif a.kho:
        kho(prof)
    else:
        tron(prof, d, a.video or None)


if __name__ == "__main__":
    main()
