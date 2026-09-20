"""storyboard.py — dựng STORYBOARD từ voice.srt để ảnh KHỚP LỜI tuyệt đối.

Vì sao cần (skill youtube-image-prompts §ĐỒNG BỘ, đã dính lỗi thật ở nenkin-fujinkai):
`assemble.py` chia ảnh ĐỀU theo cue SRT — ảnh thứ i luôn được chiếu đúng lúc đọc khối cue thứ i,
`bounds[i] = round(i*M/N)`. Nó KHÔNG biết ảnh nào thuộc câu nào. Nếu prompt được viết theo cảm hứng
(dồn ảnh vào cao trào, ít ảnh cho đoạn mở đầu dài) thì ảnh TRÔI TRỄ so với lời ở khúc giữa video
(đo thật: phút 8:30 vẫn chiếu màn hình LINE trong khi lời đã sang cảnh khác).

Cách chắc chắn: chia cue thành N khối GIỐNG HỆT assemble, lấy LỜI của từng khối, rồi viết prompt #i
bám đúng lời khối #i. Ảnh nào cũng khớp đoạn mà assemble sẽ chiếu nó.

Dùng:
  py -3.13 storyboard.py --srt <slug>/voice.srt --n 120          # xem thử các khối
  (trong tool: ai_steps.write_img_prompts(..., srt=<file>) sẽ tự dùng)
"""
import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CUE = re.compile(r"(\d\d):(\d\d):(\d\d)[,.](\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d\d\d)(.*?)(?=\n\s*\n|\Z)",
                 re.DOTALL)


def parse_cues(srt_path):
    """[(start_sec, end_sec, text)] theo đúng thứ tự trong file."""
    txt = Path(srt_path).read_text(encoding="utf-8", errors="replace")
    out = []
    for m in CUE.finditer(txt):
        a = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 1000
        b = int(m[5]) * 3600 + int(m[6]) * 60 + int(m[7]) + int(m[8]) / 1000
        body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m[9])).strip()
        if body:
            out.append((a, b, body))
    return out


def blocks(cues, n):
    """Chia n khối GIỐNG assemble.sync_durations: bounds[i] = round(i*M/n).

    Trả [(idx, t_start, t_end, text_gộp)] — mỗi phần tử ứng với ĐÚNG 1 ảnh."""
    M = len(cues)
    if not M:
        return []
    n = max(1, min(n, M))
    bd = [round(i * M / n) for i in range(n + 1)]
    bd[-1] = M
    out = []
    for i in range(n):
        lo, hi = bd[i], max(bd[i] + 1, bd[i + 1])
        part = cues[lo:hi]
        if not part:
            continue
        out.append((len(out) + 1, part[0][0], part[-1][1], "".join(c[2] for c in part)))
    return out


def fmt(t):
    return f"{int(t)//60:02d}:{int(t)%60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    cues = parse_cues(args.srt)
    bl = blocks(cues, args.n)
    lines = [f"[{i:03d}] {fmt(a)}-{fmt(b)} ({len(t)} chữ) {t}" for i, a, b, t in bl]
    print(f"{len(cues)} cue → {len(bl)} khối (mỗi khối = 1 ảnh)")
    print("\n".join(lines[:8] + (["…"] if len(lines) > 8 else [])))
    if args.out:
        Path(args.out).write_text("\n".join(lines), encoding="utf-8")
        print(f"→ {args.out}")


if __name__ == "__main__":
    main()
