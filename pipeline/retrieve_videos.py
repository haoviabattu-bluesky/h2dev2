"""retrieve_videos.py — K3 (đặt tên riêng K1/K2/K3, KHÔNG dùng B1/B2/B3 — B3 ở MỌI lane trong
make_video.py đã có nghĩa khác: "viết kịch bản" của 1 TẬP; đây là việc khác hẳn, cấp KÊNH): chọn N
video liên quan nhất 1 chủ đề mới, từ VIDEO_ANALYSIS/*.json đã có (sinh bởi channel_analyzer.py -
K1+K2). Thuần Python, KHÔNG gọi LLM, KHÔNG cần Claude/API key.

So khớp SUBSTRING (không tokenize/embedding): topics[] của mỗi video là cụm từ khoá ngắn do Gemini
sinh sẵn, so trực tiếp với chuỗi --topic là đủ dùng ở quy mô <50 video/kênh — tiếng Nhật không có
khoảng trắng giữa từ nên tokenize đúng cần mecab/fugashi, dự án này không có dependency đó ở đâu
khác nên cố tình không thêm.

Dùng:
  py -3.13 retrieve_videos.py --dna-dir docs/channel_dna/<slug>/ --topic "UFO và chính phủ che giấu" --top-n 8
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def load_videos(dna_dir):
    va_dir = dna_dir / "VIDEO_ANALYSIS"
    if not va_dir.exists():
        raise SystemExit(f"Chưa có {va_dir} — chạy channel_analyzer.py cho kênh này trước.")
    out = []
    for f in sorted(va_dir.glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  ✗ bỏ qua {f.name}: {type(e).__name__} {e}")
    if not out:
        raise SystemExit(f"{va_dir} rỗng hoặc mọi file lỗi — chạy lại channel_analyzer.py.")
    return out


def score(video, topic):
    topics = video.get("topics") or []
    title = video.get("title") or ""
    s = 0
    for t in topics:
        t = t.strip()
        if not t:
            continue
        if t in topic:
            s += 1
        if t in title:
            s += 1
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dna-dir", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--top-n", type=int, default=8)
    args = ap.parse_args()

    dna_dir = Path(args.dna_dir)
    videos = load_videos(dna_dir)
    ranked = sorted(videos, key=lambda v: score(v, args.topic), reverse=True)
    top_scores = [score(v, args.topic) for v in ranked[:args.top_n]]

    if max(top_scores or [0]) == 0:
        print("⚠ Không video nào khớp từ khoá chủ đề — trả về top view_count làm dự phòng.")
        ranked = sorted(videos, key=lambda v: v.get("view_count", 0), reverse=True)

    picked = ranked[:args.top_n]
    out_dir = dna_dir / "_retrieved"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{int(time.time())}.json"
    result = [{"video_id": v["video_id"], "title": v.get("title", ""),
              "score": score(v, args.topic), "topics": v.get("topics", [])} for v in picked]
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Top {len(picked)}/{len(videos)} video liên quan chủ đề: {args.topic!r}")
    for r in result:
        print(f"  [{r['score']:2d}] {r['video_id']}  {r['title'][:70]}")
    print(f"\n→ Đã ghi {out_path}")


if __name__ == "__main__":
    main()
