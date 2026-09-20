# -*- coding: utf-8 -*-
"""tts_chia.py — đọc kịch bản DÀI bằng ai33/OpenSpeaker theo NHIỀU PHẦN rồi nối lại.

Vì sao cần (đo thật STT13 2026-09-19): với một số kịch bản ~8.500 chữ, server ai33 trả audio CỤT
(2 lần liên tiếp đều đúng 16:05 cho bản phụ đề khai 29:32 — lỗi TẤT ĐỊNH, chạy lại không cứu) mà
KHÔNG báo lỗi gì. Ghép bản đó vào video = chết tiếng từ phút 18, phụ đề lệch 808 giây; chỉ
`qc_audio.py` mới phát hiện, tức đã tốn nguyên một lượt TTS.

Cách làm: cắt kịch bản tại ranh giới ĐOẠN thành N phần gần đều, đọc từng phần, KIỂM từng phần
(độ dài mp3 phải ≥95% mốc cuối SRT mà server khai), rồi nối audio bằng ffmpeg và dịch mốc SRT của
các phần sau theo độ dài thực của phần trước. Đây là nối FILE ÂM THANH của cùng một bản đọc,
không phải dựng video.

  py -3.13 tts_chia.py --script <slug>/script.txt --out <slug>/voice.mp3 --profile satori-jp-obaa --phan 2
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg

sys.stdout.reconfigure(encoding="utf-8")
FF = imageio_ffmpeg.get_ffmpeg_exe()

import openspeaker_tts as osp
import tts as T


def srt_giay_cuoi(srt):
    moc = re.findall(r"(\d\d):(\d\d):(\d\d),(\d+)\s*-->", srt or "")
    if not moc:
        return 0.0
    h, m, s, ms = moc[-1]
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def _fmt(t):
    h, r = divmod(t, 3600)
    m, r = divmod(r, 60)
    s = int(r)
    return "%02d:%02d:%02d,%03d" % (int(h), int(m), s, int(round((r - s) * 1000)))


def srt_doi_moc(srt, offset, so_bat_dau):
    """Dịch mọi mốc thời gian thêm `offset` giây, đánh số lại từ `so_bat_dau`. Trả (srt, số_tiếp)."""
    ra, n = [], so_bat_dau
    for khoi in re.split(r"\n\s*\n", (srt or "").strip()):
        m = re.search(r"(\d\d):(\d\d):(\d\d),(\d+)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d+)", khoi)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000 + offset
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000 + offset
        loi = [d for d in khoi.splitlines()[1:] if d.strip() and "-->" not in d]
        ra.append("%d\n%s --> %s\n%s" % (n, _fmt(a), _fmt(b), "\n".join(loi)))
        n += 1
    return "\n\n".join(ra) + "\n", n


def chia_doan(text, so_phan):
    """Cắt tại ranh giới đoạn văn thành `so_phan` phần gần đều theo SỐ KÝ TỰ."""
    doan = [d.strip() for d in re.split(r"\n\s*\n", text) if d.strip()]
    if len(doan) < so_phan * 2:
        raise SystemExit("✗ kịch bản quá ít đoạn (%d) để chia %d phần" % (len(doan), so_phan))
    muc = len(text) / so_phan
    phan, cur, n = [], [], 0
    for d in doan:
        cur.append(d)
        n += len(d)
        if n >= muc and len(phan) < so_phan - 1:
            phan.append("\n\n".join(cur))
            cur, n = [], 0
    if cur:
        phan.append("\n\n".join(cur))
    return phan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", default="")
    ap.add_argument("--voice", default="")
    ap.add_argument("--speed", type=float, default=None)
    ap.add_argument("--fx", default="")
    ap.add_argument("--phan", type=int, default=2, help="số phần cắt (mặc định 2)")
    a = ap.parse_args()

    voice, fx, speed = a.voice, a.fx, a.speed
    if a.profile:
        import profiles
        prof = profiles.load(a.profile)
        v, f, sp = profiles.voice_conf(prof)
        voice = voice or v
        fx = fx or f
        speed = sp if speed is None else speed
    speed = T.SPEED_MAC_DINH if speed is None else speed
    fx = T.normalize_fx(fx or "none")
    vid = T.resolve_voice(voice or "enishi")

    text = T.clean(Path(a.script).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    phan = chia_doan(text, a.phan)
    print("[tts_chia] voice=%s fx=%s speed=%s · %d phần: %s ký tự"
          % (vid, fx, speed, len(phan), " + ".join(str(len(p)) for p in phan)))

    T.kiem_credit(osp, text)      # cổng credit: thiếu là dừng, không để server trả audio cụt
    tmp = Path(tempfile.mkdtemp(prefix="tts_chia_"))
    files, srts = [], []
    for i, p in enumerate(phan, 1):
        audio, srt = osp.synthesize(p, voice_id=vid, speed=speed, with_transcript=True,
                                    file_name="%s_p%d" % (out.stem, i))
        f = tmp / ("p%d.mp3" % i)
        f.write_bytes(audio)
        dur = T.mp3_seconds(f)
        can = srt_giay_cuoi(srt)
        print("  ✓ phần %d/%d: %.1f′ (phụ đề khai %.1f′)" % (i, len(phan), dur / 60, can / 60))
        if can and dur < can * 0.95:
            raise SystemExit("✗ phần %d VẪN cụt (%.1f′ < %.1f′) — chia nhỏ hơn (--phan %d) hoặc xử lý tay."
                             % (i, dur / 60, can / 60, a.phan + 1))
        files.append(f)
        srts.append(srt)

    lst = tmp / "list.txt"
    lst.write_text("\n".join("file '%s'" % f.as_posix() for f in files), encoding="utf-8")
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)],
                   check=True, capture_output=True)
    T.apply_age(out, fx)
    T.chuan_muc(out)
    dur = T.mp3_seconds(out)
    print("✓ Voice: %s (dài %d:%02d) [ai33/%s · %d phần]" % (out, dur // 60, dur % 60, vid, len(phan)))

    gop, n, offset = [], 1, 0.0
    for f, s in zip(files, srts):
        doan_srt, n = srt_doi_moc(s, offset, n)
        gop.append(doan_srt)
        offset += T.mp3_seconds(f)
    srt_path = out.with_suffix(".srt")
    srt_path.write_text("\n".join(gop), encoding="utf-8")
    print("✓ Phụ đề (server sync, đã dịch mốc): %s" % srt_path)
    tong = srt_giay_cuoi(srt_path.read_text(encoding="utf-8"))
    if dur < tong * 0.95:
        raise SystemExit("✗ bản nối vẫn ngắn hơn phụ đề (%.1f′ < %.1f′)" % (dur / 60, tong / 60))


if __name__ == "__main__":
    main()
