# -*- coding: utf-8 -*-
r"""tts_voicevox.py — lồng tiếng ĐA GIỌNG bằng VOICEVOX engine local (lane khai `voice.provider = "voicevox"`).

Vì sao có file này (2026-09-24, docs/PHUONG_AN_LANE_K_DA_GIONG_BONG_THOAI.md §C3): kênh mẫu của Lane K
(千種テンカ) đọc mỗi vai bằng một giọng VOICEVOX khác nhau — đo thật 4 video: người kể 玄野武宏, nhân vật chính
黒沢冴白, 事務さん 波音リツ + vai phụ đổi theo tập (docs/channel_dna/yakkyoku-sukatto/GIONG_VAI.md).
tts.py chỉ đọc MỘT giọng cho cả bài nên không dùng được.

Cách làm: cắt script theo cau_vai.tach_cau() → mỗi câu lấy id vai từ vai.txt (gan_vai.py, máy 1) → giọng
của vai (characters.json / profile voice.narrator) → POST /audio_query + /synthesis → nối, chèn nghỉ →
voice.mp3 + voice.srt (MỐC ĐO TỪ ĐỘ DÀI THẬT từng câu, chữ = nguyên văn script, không qua STT) +
voice_roles.json (cue → vai, cho bóng thoại) + credits_giong.txt (khối ▼素材 phải ghi trong mô tả).

Engine: E:\CLAUDE\YOUTUBE\VOICEVOX_ENGINE\0.25.2\run.exe --port 50021 (máy 2 phải cài y hệt, miễn phí).

Nhánh ai33 (voice.provider = "ai33", Lane L `shakai_no_naze` 2026-09-24): cùng luồng vai.txt → câu → nối, nhưng mỗi
câu là 1 task OpenSpeaker với `voice_id` của vai (profile voice.narrator / characters.json[].voice = {voice_id, speed?}).
Có cổng credit trước khi gửi + cổng nuốt chữ theo từng câu; không sinh credits_giong.txt (không có điều khoản ghi công).

Dùng:
  py -3.13 tts_voicevox.py --script <tập>\script.txt --profile yakkyoku-sukatto --out <tập>\voice.mp3
      [--vai <tập>\vai.txt] [--chars <tập>\characters.json]
  (script có thể là hook\hook_locked.txt: câu được dò theo chữ trong vai.txt của cả tập)
"""
import argparse
import io
import json
import re
import subprocess
import sys
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cau_vai    # noqa: E402
import profiles   # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ENGINE = "http://127.0.0.1:50021"
CAI_DAT = (r"VOICEVOX engine chưa chạy ở :50021. Máy 1: E:\CLAUDE\YOUTUBE\VOICEVOX_ENGINE\0.25.2\run.exe --host 127.0.0.1 "
           r"--port 50021 · Máy khác: tải voicevox_engine-windows-cpu-0.25.2.vvpp từ "
           r"https://github.com/VOICEVOX/voicevox_engine/releases/tag/0.25.2 (file zip, giải nén) rồi chạy run.exe như trên.")


def _tim_file(start: Path, name):
    """vai.txt / characters.json nằm ở thư mục tập; script có thể ở tập\\hook\\ → dò lên tối đa 2 cấp."""
    for d in (start, start.parent, start.parent.parent):
        if (d / name).exists():
            return d / name
    return None


def _style_map():
    try:
        sp = requests.get(f"{ENGINE}/speakers", timeout=20).json()
    except Exception:
        raise SystemExit("✗ " + CAI_DAT)
    return {(s["name"], st["name"]): st["id"] for s in sp for st in s["styles"]}


def giong_cua_vai(prof, chars_path):
    """id vai → {speaker, style, speed?}. Người kể = profile voice.narrator; vai khác = characters.json[].voice."""
    v = prof.get("voice", {}) or {}
    ban = {cau_vai.KE: dict(v.get("narrator") or {})}
    if chars_path and Path(chars_path).exists():
        for c in json.loads(Path(chars_path).read_text(encoding="utf-8")).get("characters", []):
            if c.get("voice"):
                ban[c["id"]] = dict(c["voice"])
    if not (ban[cau_vai.KE].get("speaker") or ban[cau_vai.KE].get("voice_id")):
        raise SystemExit("✗ profile thiếu voice.narrator.speaker / voice_id (giọng người kể)")
    return ban


def _tong_hop(text, style_id, speed, pre, post):
    q = requests.post(f"{ENGINE}/audio_query", params={"text": text, "speaker": style_id}, timeout=120)
    q.raise_for_status()
    aq = q.json()
    aq["speedScale"] = speed
    aq["prePhonemeLength"] = pre
    aq["postPhonemeLength"] = post
    w = requests.post(f"{ENGINE}/synthesis", params={"speaker": style_id}, json=aq, timeout=300)
    w.raise_for_status()
    with wave.open(io.BytesIO(w.content)) as wf:
        sr = wf.getframerate()
        pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    return pcm, sr


AI33_SR = 44100


def ap_fx(pcm, fx, sr=AI33_SR):
    """Áp chuỗi bộ lọc ffmpeg (characters.json voice.fx, vd giọng QUÁT NẠT) lên 1 câu PCM int16 mono. Không fx → trả nguyên."""
    if not fx:
        return pcm
    import imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "pipe:0",
                        "-af", fx, "-f", "s16le", "-ar", str(sr), "-ac", "1", "pipe:1"], input=pcm.tobytes(), capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"✗ voice.fx lỗi: {r.stderr.decode('utf-8', 'ignore')[:200]}")
    return np.frombuffer(r.stdout, dtype=np.int16)


def _doi_sr(pcm, sr_vao, sr_ra):
    """Đổi tần số mẫu 1 câu PCM int16 mono (ghép câu ai33 44,1 kHz vào bài VOICEVOX 24 kHz)."""
    import imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "s16le", "-ar", str(sr_vao), "-ac", "1",
                        "-i", "pipe:0", "-f", "s16le", "-ar", str(sr_ra), "-ac", "1", "pipe:1"],
                       input=pcm.tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.int16)


def _tong_hop_ai33(text, voice_id, speed, n_thu=3):
    """1 câu → PCM int16 mono 44,1 kHz qua ai33 (OpenSpeaker). Lane L (2026-09-24): kênh mẫu đọc đa giọng bằng TTS
    thương mại (đo: KHÔNG phải VOICEVOX), gần nhất họ giọng MiniMax. Cắt lặng đầu/cuối server tự chèn (dài ngắn
    thất thường giữa các câu) để khoảng nghỉ giữa câu do profile quyết định như nhánh VOICEVOX.
    Cổng nuốt chữ theo câu: tiếng < 35% độ dài kỳ vọng (≈5,5 chữ/giây) → đọc lại, hết lượt → DỪNG."""
    import openspeaker_tts as osp
    import imageio_ffmpeg
    n = len(cau_vai._chuan(text))
    loi = ""
    for lan in range(1, n_thu + 1):
        try:
            mp3, _ = osp.synthesize(text, voice_id, speed=speed, with_transcript=False, file_name="da_giong")
        except Exception as e:
            loi = f"{type(e).__name__}: {e}"
            continue
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", "pipe:0", "-ac", "1",
                              "-ar", str(AI33_SR), "-f", "s16le", "pipe:1"], input=mp3, capture_output=True,
                             check=True).stdout
        pcm = np.frombuffer(raw, dtype=np.int16)
        tren = np.flatnonzero(np.abs(pcm) > 400)
        if len(tren):
            dem = int(0.03 * AI33_SR)
            pcm = pcm[max(0, tren[0] - dem): tren[-1] + dem]
        dur = len(pcm) / AI33_SR
        if dur >= 0.35 * n / 5.5 and dur >= 0.3:
            return pcm, AI33_SR
        loi = f"chỉ {dur:.2f}s cho {n} chữ (nghi nuốt chữ)"
    raise SystemExit(f"✗ ai33 đọc hỏng câu sau {n_thu} lượt ({loi}): {text[:40]}")


def _ts(s):
    h, r = divmod(s, 3600)
    m, r = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(r):02d},{int(round((r - int(r)) * 1000)) % 1000:03d}"


def chay(script, out, prof, vai_path=None, chars_path=None, workers=3):
    script, out = Path(script), Path(out)
    provider = ((prof.get("voice") or {}).get("provider") or "voicevox")
    ai33 = provider == "ai33"
    if not ai33:
        try:
            requests.get(f"{ENGINE}/version", timeout=5).raise_for_status()
        except Exception:
            raise SystemExit("✗ " + CAI_DAT)
    vai_path = Path(vai_path) if vai_path else _tim_file(script.parent, "vai.txt")
    chars_path = Path(chars_path) if chars_path else _tim_file(script.parent, "characters.json")
    if not vai_path or not vai_path.exists():
        raise SystemExit("✗ thiếu vai.txt (máy 1 chạy gan_vai.py sau khi khoá kịch bản)")
    v = prof.get("voice", {}) or {}
    speed = float(v.get("speed", 1.0) or 1.0)
    pre, post = float(v.get("pre_s", 0.05)), float(v.get("post_s", 0.05))
    nghi_cau, nghi_doan = float(v.get("pause_sentence_ms", 350)) / 1000, float(v.get("pause_para_ms", 700)) / 1000

    text = script.read_text(encoding="utf-8")
    yomi = _tim_file(script.parent, "yomi.txt")
    cau = cau_vai.tach_cau(text)
    theo_khoi = len({c["khoi"] for c in cau}) > 1
    ids = cau_vai.khop_vai(cau, cau_vai.doc_vai(vai_path))
    doan_them = cau_vai.doan_hook(script.parent, cau)
    nghi_the = cau_vai.nghi_the_ten(script.parent, cau)   # 11/10: thẻ tên thân bài → nghỉ thêm cho kịp đọc
    lang = cau_vai.lang_hook(script.parent, cau)   # 12/10: shot hook LẶNG (lang_s) / giữ hình (nghi_sau_s) → chèn lặng
    if chars_path and Path(chars_path).exists():   # 22/10: giọng vai phải hợp tuổi theo kho chung (cụ bà ≠ giọng trẻ)
        import kho_giong
        kho_giong.chan(prof, chars_path)
    ban = giong_cua_vai(prof, chars_path)
    thieu = sorted({i for i in ids if i not in ban})
    if thieu:
        raise SystemExit(f"✗ vai.txt có vai không khai giọng trong characters.json: {thieu}")

    if ai33:
        def _sid(g):
            if not g.get("voice_id"):
                raise SystemExit(f"✗ provider ai33: giọng thiếu voice_id: {g}")
            return g["voice_id"]
    else:
        smap = _style_map()

        def _sid(g):
            # 2026-10-05 Lane O ep04: lane VOICEVOX cho phép VAI LẺ đọc bằng ai33 (characters.json voice.voice_id),
            # vd giám đốc hách dịch = Masafumi + fx punch (VOICEVOX không có giọng quát đủ uy) → trả voice_id (str).
            if g.get("voice_id"):
                if not v.get("ai33_cho_vai"):
                    raise SystemExit(f"✗ lane VOICEVOX chưa bật voice.ai33_cho_vai mà vai khai voice_id ai33: {g.get('voice_id')}")
                return g["voice_id"]
            k = (g["speaker"], g.get("style") or "ノーマル")
            if k not in smap:
                raise SystemExit(f"✗ engine không có giọng {k} — kiểm tên speaker/style")
            return smap[k]

    viec = []
    for c, vid in zip(cau, ids):
        g = ban[vid]
        doc = cau_vai.bo_ngoac(c["text"]).replace("「", "").replace("」", "").replace("『", "").replace("』", "")
        if yomi:
            import tts as _tts
            doc, _ = _tts.ap_yomi(doc, yomi)
        viec.append((doc, _sid(g), float(g.get("speed", speed)), g.get("fx")))
    tag = "ai33" if ai33 else "voicevox"
    print(f"[{tag}] {len(cau)} câu · {len(set(ids))} vai · {len({x[1] for x in viec})} giọng · speed {speed}")

    if ai33:
        import openspeaker_tts as _osp
        import tts as _tts
        _tts.kiem_credit(_osp, "".join(x[0] for x in viec))      # thiếu credit → DỪNG trước khi gửi câu nào
        workers = max(workers, int((prof.get("voice") or {}).get("workers", 8)))
        with ThreadPoolExecutor(max_workers=workers) as ex:
            kq = list(ex.map(lambda x: (ap_fx(_tong_hop_ai33(x[0], x[1], x[2])[0], x[3]), AI33_SR), viec))
    else:
        lai = [x for x in viec if isinstance(x[1], str)]          # câu của vai lẻ ai33 (voice_id)
        if lai:
            import openspeaker_tts as _osp
            import tts as _tts
            _tts.kiem_credit(_osp, "".join(x[0] for x in lai))

        def _mot(x):
            if isinstance(x[1], str):
                return ap_fx(_tong_hop_ai33(x[0], x[1], x[2])[0], x[3]), AI33_SR
            return _tong_hop(x[0], x[1], x[2], pre, post)
        with ThreadPoolExecutor(max_workers=workers) as ex:
            kq = list(ex.map(_mot, viec))
        sr_vv = next((s for (_, s), x in zip(kq, viec) if not isinstance(x[1], str)), AI33_SR)
        kq = [(_doi_sr(p, s, sr_vv), sr_vv) if s != sr_vv else (p, s) for p, s in kq]
    sr = kq[0][1]
    khuc, cues, t = [], [], 0.0
    if lang.get(0):   # shot hook lặng mở đầu (vd motion gõ ngày/địa điểm, không lời) → lặng trước câu 1
        khuc.append(np.zeros(int(lang[0] * sr), dtype=np.int16))
        t += lang[0]
    for k, ((pcm, _), c, vid) in enumerate(zip(kq, cau, ids)):
        dur = len(pcm) / sr
        # 2026-10-03 Lane O ep02: câu 1–2 chữ (vd 「は、」 tách sau ngoặc) đọc đúng chỉ ~0,28s → sàn 0,15s + phải có tiếng thật
        so_chu = len(re.sub(r"[\s、。，．,.!?！？・…ー「」『』（）()]", "", viec[k][0]))
        san = 0.15 if so_chu <= 2 else 0.3
        if dur < san or (so_chu <= 2 and int(np.abs(pcm).max(initial=0)) < 1000):
            raise SystemExit(f"✗ câu {c['i']} chỉ ra {dur:.2f}s tiếng — engine đọc hỏng: {c['text'][:30]}")
        cues.append({"i": c["i"], "start": round(t, 3), "end": round(t + dur, 3), "vai": vid,
                     "para": c["para"], "text": c["text"]})
        khuc.append(pcm)
        t += dur
        if k < len(cau) - 1:
            # nghỉ đoạn theo KHỐI dòng trống (cảnh), không theo từng dòng: kịch bản viết mỗi câu một dòng (04/10)
            # nên theo dòng thì câu nào cũng nghỉ đoạn → video dài thêm vài phút.
            # Script cũ không có dòng trống nào (cả bài 1 khối, vd N ep03 bản anh) → giữ cách cũ theo dòng.
            # Mảnh câu (xuống dòng giữa câu, 「…」 còn tiếp cùng dòng) → khe ngắn; sàn câu/đoạn + nghỉ đoạn trong hook
            # (hook_timeline `nghi_doan_sau`) — 1 luật chung với clip hook xem thử: cau_vai.khe_nghi (06/10).
            gap = cau_vai.khe_nghi(c, cau[k + 1], nghi_cau, nghi_doan, "khoi" if theo_khoi else "para", doan_them)
            gap = max(gap, nghi_the.get(c["i"], 0.0))
            gap += lang.get(c["i"], 0.0)
            khuc.append(np.zeros(int(gap * sr), dtype=np.int16))
            t += gap
    wav_path = out.with_suffix(".wav")
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(np.concatenate(khuc).tobytes())
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-i", str(wav_path), "-ar", "44100",
                    "-b:a", "192k", str(out)], check=True)
    wav_path.unlink(missing_ok=True)
    import tts as _tts
    _tts.chuan_muc(out)

    srt = out.with_suffix(".srt")
    srt.write_text("".join(f"{n}\n{_ts(c['start'])} --> {_ts(c['end'])}\n{c['text']}\n\n"
                           for n, c in enumerate(cues, 1)), encoding="utf-8")
    (out.parent / f"{out.stem}_roles.json").write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")
    # cổng phủ chữ (cùng tinh thần tts.kiem_phu_chu): tổng chữ cue = tổng chữ script
    a, b = len(cau_vai._chuan(text)), sum(len(cau_vai._chuan(c["text"])) for c in cues)
    if b < a * 0.99:
        raise SystemExit(f"✗ SRT chỉ phủ {b}/{a} chữ script — thiếu câu")
    if ai33:       # ai33 không có điều khoản ghi công như VOICEVOX → không sinh credits_giong.txt
        dung = sorted({ban[i]["voice_id"] for i in ids})
    else:
        dung = sorted({(ban[i].get("voice_id") or ban[i]["speaker"]) for i in ids})
        vv = sorted({ban[i]["speaker"] for i in ids if not ban[i].get("voice_id")})   # vai ai33 không ghi công VOICEVOX
        (out.parent / "credits_giong.txt").write_text("▼ 素材\n音声：" + "／".join(f"VOICEVOX:{s}" for s in vv) + "\n",
                                                       encoding="utf-8")
    print(f"[{tag}] ✓ {out.name} {t/60:.2f}' · {len(cues)} cue · giọng: {', '.join(dung)}")
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--vai", default="")
    ap.add_argument("--chars", default="")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    chay(a.script, a.out, profiles.load(a.profile), a.vai or None, a.chars or None, a.workers)


if __name__ == "__main__":
    main()
