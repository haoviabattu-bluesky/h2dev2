"""Cổng SỐ HỌC cho script.txt — chạy được từ dòng lệnh (KHÔNG tốn LLM, chạy tức thì).

Vì sao có file này: `ai_steps.check()` là hàm Python thuần, chỉ gọi được khi import. Bộ não Claude
(brain_steps) viết kịch bản trong tiến trình riêng, KHÔNG import được, nên trước đây nó chỉ được
NGHE ngưỡng bằng lời rồi đoán — đo thật lần chạy 2026-09-10: 0.86 phẩy/câu (cần 2.5–6.0), hội thoại
30% (tối đa 15%). Không ai đếm tay được dấu phẩy trên 9.000 chữ Nhật; phải có lệnh đo.

  py -3.13 gate_check.py --profile satori-jp-obaa --script <đường dẫn script.txt> [--minutes 30]

exit 0 = ĐẠT · exit 1 = còn lệch (in từng dòng vấn đề + số đo thật để biết sửa hướng nào).
"""
import argparse
import sys
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    _ensure_std()
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--minutes", type=float, default=0)
    a = ap.parse_args()

    import ai_steps
    import profiles

    prof = profiles.load(a.profile)
    text = Path(a.script).read_text(encoding="utf-8")
    bad, m = ai_steps.check(prof, text, a.minutes or None)

    g = profiles.gate(prof)
    print(f"ĐO ĐƯỢC: {m['chars']:,} chữ · {m['minutes']}' · {m['comma_per_sentence']} phẩy/câu "
          f"(cần {g['comma_per_sentence'][0]}–{g['comma_per_sentence'][1]}) · "
          f"{m['chars_per_breath']} chữ/nhịp thở "
          f"(cần {g['chars_per_breath'][0]}–{g['chars_per_breath'][1]}) · "
          f"hội thoại {m['dialogue_ratio']:.0%} (tối đa {g['dialogue_ratio_max']:.0%})")
    if not bad:
        print("=== CỔNG SỐ HỌC: ĐẠT ===")
        return 0
    print(f"=== CỔNG SỐ HỌC: {len(bad)} VẤN ĐỀ ===")
    for b in bad:
        print(f"   ✗ {b}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
