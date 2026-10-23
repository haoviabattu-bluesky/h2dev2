r"""NHẠC NỀN HOOK TỪ THƯ VIỆN ÂM THANH YOUTUBE — thay bước sinh Suno `tao_nhac_hook.py` (anh chốt 2026-10-23: CẤM Suno).

Cắt 1 đoạn LIỀN (không lặp) dài ≥ hook từ bài nhạc riêng của lane (`assets\_bgm_kenh\<lane>\piano_nen.mp3`, tải bằng
bgm_audio_library.py), fade-in 2s + fade-out 1,5s, chuẩn hoá −16 LUFS (y quy cách cũ QUY_TAC_HOOK_DAI_VA_NHAC_NEN §2)
→ `<tập>\hook\sfx\99_nhac_piano.mp3` + `99_nhac_piano.nguon.json` (chứng từ). hook_timeline.json giữ "nen" trỏ file này.
Cùng bài với thân video → hook và thân 1 màu nhạc (máy 2 ghep_hook_noi_truoc.py cũng phát bài lane suốt hook + thân).

  py -3.13 -X utf8 pipeline\nhac_hook_tu_thu_vien.py --tap <thư mục tập> --lane teinengo-real --giay 45
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NGUON = [ROOT / "assets" / "_bgm_kenh",                                                                     # repo
         Path(r"E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\buoc2_3_tool\assets\_bgm_kenh"),          # máy 1 (Syncthing)
         Path(r"E:\CLAUDE\YOUTUBE\FlowHandoff_local\shared\buoc2_3_tool\assets\_bgm_kenh")]                # máy 2


def bai_lane(lane):
    for d in NGUON:
        if (d / lane / "piano_nen.mp3").exists() and (d / lane / "nguon.json").exists():
            return d / lane
    raise SystemExit(f"✗ lane {lane} chưa có nhạc Thư viện âm thanh (piano_nen.mp3 + nguon.json) ở {[str(d) for d in NGUON]}.\n"
                     f"  Tải: py -3.13 -X utf8 pipeline\\bgm_audio_library.py --only {lane}  (thêm lane vào DICH nếu chưa có). "
                     "KHÔNG sinh Suno.")


def do(f, af=""):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", (af + "," if af else "") + "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float([x for x in r.splitlines() if x.strip().startswith("I:")][-1].split()[1])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--tap", required=True, help="thư mục tập (có thư mục hook\\)")
    ap.add_argument("--lane", required=True, help="mã lane = id profile, vd teinengo-real")
    ap.add_argument("--giay", type=float, required=True, help="độ dài hook (giây) — đoạn cắt = giay + 2")
    ap.add_argument("--tu", type=float, default=0.0, help="giây bắt đầu cắt trong bài lane (mặc định 0)")
    a = ap.parse_args()
    d = bai_lane(a.lane)
    src = d / "piano_nen.mp3"
    dai = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                               capture_output=True, text=True).stdout)
    can = a.giay + 2
    if a.tu + can > dai:
        raise SystemExit(f"✗ bài lane dài {dai:.0f}s < cần {a.tu + can:.0f}s — luật: 1 đoạn liền, không lặp. Giảm --tu hoặc tải bài dài hơn")
    out = Path(a.tap) / "hook" / "sfx" / "99_nhac_piano.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)
    af = f"atrim={a.tu}:{a.tu + can},asetpts=PTS-STARTPTS,afade=t=in:d=2,afade=t=out:st={can - 1.5}:d=1.5"
    bu = -16 - do(src, af)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), "-af", f"{af},volume={bu:.2f}dB",
                    "-ar", "48000", "-b:a", "192k", str(out)], check=True)
    meta = json.loads((d / "nguon.json").read_text(encoding="utf-8"))
    meta.update({"cat_tu": a.tu, "cat_giay": can, "tu_file": str(src)})
    out.with_suffix(".nguon.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {out}  ({can:.1f}s, {do(out):.1f} LUFS) · bài: {', '.join(b['title'] for b in meta['bai'])}")


if __name__ == "__main__":
    main()
