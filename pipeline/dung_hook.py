# -*- coding: utf-8 -*-
r"""DUNG CLIP HOOK cho lane satori (script chay lai duoc — viet 2026-09-24 tai tap 5).

Doc `hook_timeline.json` roi dung `hook_final.mp4`. Chay lai bao nhieu lan cung ra ket qua nhu nhau.

    py -3.13 dung_hook.py --hook-dir <tap>\hook                 # uu tien clip Grok, thieu clip nao thi lay ANH TINH cua shot do
    py -3.13 dung_hook.py --hook-dir <tap>\hook --chi-anh       # ep dung anh tinh het (dung khi Grok het luot sinh)
    py -3.13 dung_hook.py --hook-dir <tap>\hook --than <final.mp4> --noi   # dung xong NOI luon vao dau than video

BANG CANH lay tu hook_timeline.json (moc cat lay tu hook_voice.srt DA NAN theo hook_locked.txt,
khong chia deu — xem skill narration_audio_pacing_qc).

BON THU PHAI KHOP voi than video (docs/QUY_TAC_VIDEO_HOOK.md §2) — script nay tu ep:
  1. do phan giai 1920x1080   2. 30 fps   3. yuv420p + bt709   4. muc tieng do tu CHINH than video
Lane satori KHONG chay phu de vao hinh → script nay khong ve chu. Phu de di kem file .srt rieng,
va khi noi hook vao dau thi PHAI dich moc cua phude.srt (tham so --noi lam luon viec do).
"""
import argparse, json, re, subprocess, shutil
from pathlib import Path

D = None   # dat trong main() theo --hook-dir
W, H, FPS = 1920, 1080, 30


def ffmpeg_bin():
    for p in Path(r"E:\CLAUDE\YOUTUBE\h2dev\pipeline\dist").glob("*/_internal/imageio_ffmpeg/binaries/ffmpeg-win-*.exe"):
        return str(p)
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    raise SystemExit("khong tim thay ffmpeg")


FF = ffmpeg_bin()


def chay(args):
    r = subprocess.run([FF, "-hide_banner", "-v", "error", "-y"] + args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"ffmpeg loi: {r.stderr[-800:]}")


def do_dai(f):
    """Thoi luong THAT doc tu ffmpeg, khong tin so trong ke hoach."""
    r = subprocess.run([FF, "-hide_banner", "-i", str(f)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", r.stderr)
    if not m:
        raise SystemExit(f"khong doc duoc thoi luong: {f}")
    h, p_, s_, cs = (int(x) for x in m.groups())
    return h * 3600 + p_ * 60 + s_ + cs / 100


def do_loudness(f):
    r = subprocess.run([FF, "-hide_banner", "-i", str(f), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+) LUFS", r.stderr)
    return float(m.group(1)) if m else None


def seg_tu_clip(clip, ra, dai):
    """Clip Grok: 1280x720@24fps -> phong len 1920x1080@30fps, cat dung do dai can."""
    chay(["-i", str(clip), "-t", f"{dai:.3f}", "-an",
          "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p",
          "-c:v", "libx264", "-preset", "medium", "-crf", "18",
          "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
          "-video_track_timescale", "15360", str(ra)])


def seg_tu_anh(img, ra, dai):
    """Anh tinh TUYET DOI khong zoom/pan (luat du an 2026-09-21)."""
    chay(["-loop", "1", "-i", str(img), "-t", f"{dai:.3f}", "-an",
          "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
          "-c:v", "libx264", "-preset", "medium", "-crf", "18",
          "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
          "-video_track_timescale", "15360", str(ra)])


def dich_srt(src, ra, offset_s, srt_hook=None):
    """Chen hook vao dau => MOI moc cua phu de than video phai lui +offset. Khong lam = lech ca video."""
    def doi(m):
        t = [int(x) for x in m.groups()]
        giay = t[0] * 3600 + t[1] * 60 + t[2] + t[3] / 1000 + offset_s
        h, con = divmod(giay, 3600); p, s = divmod(con, 60)
        return f"{int(h):02d}:{int(p):02d}:{int(s):02d},{round((s % 1) * 1000):03d}"
    khoi_than = re.split(r"\n\s*\n", Path(src).read_text(encoding="utf-8").strip())
    ra_khoi = []
    if srt_hook:
        ra_khoi += re.split(r"\n\s*\n", Path(srt_hook).read_text(encoding="utf-8").strip())
    n0 = len(ra_khoi)
    for k in khoi_than:
        d = k.split("\n")
        if len(d) < 3:
            continue
        d[1] = re.sub(r"(\d+):(\d+):(\d+),(\d+)", doi, d[1])
        ra_khoi.append("\n".join(d[1:]))
    # danh so lai tu 1
    sach = []
    for i, k in enumerate(ra_khoi, 1):
        dong = [x for x in k.split("\n") if x.strip()]
        if not re.match(r"^\d+$", dong[0]):
            dong = [str(i)] + dong
        else:
            dong[0] = str(i)
        sach.append("\n".join(dong))
    Path(ra).write_text("\n\n".join(sach) + "\n", encoding="utf-8")
    return len(sach), n0


def main():
    global D
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook-dir", required=True, help="thu muc hook/ cua tap (chua hook_timeline.json)")
    ap.add_argument("--chi-anh", action="store_true", help="ep dung anh tinh, bo qua clip Grok")
    ap.add_argument("--than", default="", help="final.mp4 cua than video (de do muc tieng + noi)")
    ap.add_argument("--noi", action="store_true", help="noi hook vao dau than video + dich phu de")
    ap.add_argument("--phude", default="", help="phude.srt cua than video (mac dinh: canh --than)")
    a = ap.parse_args()
    D = Path(a.hook_dir).resolve()

    tl = json.loads((D / "hook_timeline.json").read_text(encoding="utf-8"))
    seg_dir = D / "_seg"; seg_dir.mkdir(exist_ok=True)
    ds = []
    for s in tl["shots"]:
        clip = D / s["clip"]
        ra = seg_dir / f"seg_{s['n']:02d}.mp4"
        nguon = "anh tinh"
        if clip.exists() and not a.chi_anh:
            seg_tu_clip(clip, ra, s["dung_s"]); nguon = "clip Grok"
        else:
            seg_tu_anh(D / s["img"], ra, s["dung_s"])
        print(f"  shot {s['n']}: {s['dung_s']:.2f}s · {nguon}")
        ds.append(ra)

    lst = seg_dir / "list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in ds), encoding="utf-8")
    noi = seg_dir / "noi.mp4"
    chay(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(noi)])

    hook = D / "hook_final.mp4"
    chay(["-i", str(noi), "-i", str(D / "hook_voice.mp3"),
          "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
          "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-shortest", str(hook)])
    print(f"✓ {hook}")

    lu_hook = do_loudness(hook)
    print(f"  muc tieng hook: {lu_hook} LUFS")
    if a.than:
        lu_than = do_loudness(a.than)
        print(f"  muc tieng than: {lu_than} LUFS · lech {abs(lu_hook - lu_than):.2f} LU"
              f" → {'DAT' if abs(lu_hook - lu_than) <= 0.2 else 'TRUOT (phai nan lai)'}")

    if a.noi:
        if not a.than:
            raise SystemExit("--noi can --than <final.mp4>")
        than = Path(a.than)
        nl = D / "_noi.txt"
        nl.write_text(f"file '{hook.as_posix()}'\nfile '{than.as_posix()}'\n", encoding="utf-8")
        ra_mp4 = than.parent / "final_with_hook.mp4"
        chay(["-f", "concat", "-safe", "0", "-i", str(nl), "-c", "copy", str(ra_mp4)])
        print(f"✓ {ra_mp4}")
        sub = Path(a.phude) if a.phude else (than.parent / "phude.srt")
        if sub.exists():
            dt = do_dai(hook)
            n, nh = dich_srt(sub, than.parent / "phude_hook.srt", dt, D / "hook_voice.srt")
            print(f"✓ {than.parent / 'phude_hook.srt'} — {nh} dong hook + than da lui +{dt:.2f}s (tong {n})")


if __name__ == "__main__":
    main()
