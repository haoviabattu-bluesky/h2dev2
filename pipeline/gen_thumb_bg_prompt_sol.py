"""gen_thumb_bg_prompt_sol.py — nhờ GPT-5.6-sol VIẾT LẠI prompt ảnh nền thumbnail (tiếng Anh,
dán thẳng vào gpti2 qua gen_images.py) khi ảnh nền HIỆN TẠI sai nội dung/bố cục — khác hẳn
qc_thumbnail_sol.py (chấm chữ+ảnh ĐÃ RENDER), tool này SINH LẠI PROMPT trước khi render.

Bài học 2026-09-17 (kenko-chiebukuro ep01, 2 vòng sửa liên tiếp):
  vòng 1: ảnh chỉ có 1 món (natto) dù tiêu đề nói "5 thực phẩm" → phải sửa NỘI DUNG prompt.
  vòng 2: 5 món nổi rời rạc trên nền đen, không có bối cảnh thật → phải sửa BỐ CỤC/PHONG CÁCH.
  Cả 2 lần đều: đưa {title + summary + prompt cũ + phản hồi cụ thể} cho GPT-5.6-sol, nó viết lại
  1 đoạn prompt hoàn chỉnh, dán thẳng vào gen_images.py, KHÔNG cần Claude tự đoán prompt.

Ràng buộc khung ảnh (constraints) LẤY TỪ profile.json của lane (`thumbnail` + `thumbnail_qc`) —
MỖI LANE một bố cục khác nhau (vd kenko-chiebukuro: trái đen 62% cho chữ/phải ảnh thật; lane khác
có thể không dùng bố cục tách đôi này) — xem `_default_constraints()` bên dưới, hoặc tự khai
`thumbnail_qc.image_prompt_constraints` trong profile.json để ghi đè hẳn.

Dùng:
  py -3.13 gen_thumb_bg_prompt_sol.py --title-file listting.txt --profile kenko-chiebukuro \\
      --old-prompt thumb_bg_prompt.txt --feedback "ảnh chỉ có 1 món, tiêu đề nói 5 món" \\
      --write-to thumb_bg_prompt.txt
"""
import argparse
import json
import sys
from pathlib import Path

import sol_client

sys.stdout.reconfigure(encoding="utf-8")

PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles" / "profiles"

PROMPT_TMPL = """Bạn là chuyên gia viết PROMPT ảnh (tiếng Anh) cho model text-to-image "gpti2" (tương thích
OpenAI images API) để tạo ẢNH NỀN cho thumbnail YouTube.

Tiêu đề video: {title}

Mô tả/tóm tắt nội dung video: {summary}

PROMPT ĐANG DÙNG (cần sửa lại theo phản hồi bên dưới):
\"\"\"{old_prompt}\"\"\"

PHẢN HỒI CẦN SỬA (đọc kỹ, đây là yêu cầu bắt buộc phải sửa đúng):
{feedback}

RÀNG BUỘC KỸ THUẬT BẮT BUỘC CỦA KÊNH NÀY (giữ nguyên, không được bỏ):
{constraints}

OUTPUT: CHỈ trả về ĐÚNG 1 đoạn prompt tiếng Anh hoàn chỉnh (không giải thích, không đánh số, không
markdown code block), sẵn sàng dán thẳng vào gpti2 để generate ảnh.
"""

_GENERIC_CONSTRAINTS = """1. Ảnh tỉ lệ ngang 16:9.
2. real photograph, photorealistic, ultra-sharp, appetizing/eye-catching, no people (trừ khi nội
   dung kênh BẮT BUỘC có người), no text, no watermark, no logo, không vẽ chữ/số/ký tự bất kỳ
   ngôn ngữ nào trong ảnh (chữ sẽ overlay riêng sau).
3. Ánh sáng SÁNG RÕ, không tối, không moody, không ám màu điện ảnh nặng."""


def _default_constraints(profile):
    """Suy ràng buộc khung ảnh từ profile.thumbnail (side/side_width/art_style) — mỗi lane bố
    cục khác nhau nên KHÔNG hardcode 1 khung chung cho mọi kênh."""
    th = (profile or {}).get("thumbnail") or {}
    art = th.get("art_style", "")
    if th.get("dedicated_bg") and th.get("side_width"):
        pct = round(th["side_width"] * 100)
        return _GENERIC_CONSTRAINTS + f"""
4. VÙNG BÊN TRÁI (khoảng {pct-3}-{pct}% chiều ngang tính từ mép trái) PHẢI là nền ĐEN THUẦN,
   không có bất kỳ vật thể/chi tiết/ánh sáng nào lấn vào — đây là chỗ dành riêng để overlay chữ
   to, không được vi phạm.
5. VÙNG BÊN PHẢI (phần còn lại, sát mép phải) phải là MỘT BỨC ẢNH CÓ ĐẦY ĐỦ BỐI CẢNH THẬT (không
   phải vật thể cắt rời nổi trên nền đen studio) — có chiều sâu, có môi trường xung quanh thật.
   Phong cách/chủ thể tham khảo: {art or "(theo đúng chủ đề video)"}."""
    return _GENERIC_CONSTRAINTS + (f"\n4. Phong cách: {art}" if art else "")


def load_profile(profile_id):
    if not profile_id:
        return {}
    p = PROFILES_DIR / f"{profile_id}.json"
    if not p.exists():
        print(f"  ! khong thay profile {p}, dung constraints mac dinh")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def build_constraints(profile_id):
    profile = load_profile(profile_id)
    override = (profile.get("thumbnail_qc") or {}).get("image_prompt_constraints")
    if override:
        return override.strip()
    return _default_constraints(profile)


def run(title, summary, old_prompt, feedback, profile_id=None):
    constraints = build_constraints(profile_id)
    prompt = PROMPT_TMPL.format(title=title, summary=summary or "(không có)",
                                old_prompt=old_prompt.strip(), feedback=feedback.strip(),
                                constraints=constraints)
    text, usage = sol_client.chat(prompt, max_tokens=1200)
    print(f"[usage={json.dumps(usage)}]", file=sys.stderr)
    return text.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title")
    ap.add_argument("--title-file", help="dòng ĐẦU của file là tiêu đề")
    ap.add_argument("--summary")
    ap.add_argument("--summary-file")
    ap.add_argument("--old-prompt", required=True, help="chuỗi HOẶC đường dẫn file prompt cũ")
    ap.add_argument("--feedback", required=True, help="chuỗi HOẶC đường dẫn file phản hồi/lỗi cần sửa")
    ap.add_argument("--profile", help="id lane — lấy ràng buộc bố cục riêng từ profile.json")
    ap.add_argument("--write-to", help="ghi thẳng prompt mới vào file này (vd thumb_bg_prompt.txt)")
    args = ap.parse_args()

    title = args.title
    if args.title_file:
        lines = Path(args.title_file).read_text(encoding="utf-8").splitlines()
        title = next((l.strip() for l in lines if l.strip()), "")
    if not title:
        ap.error("cần --title hoặc --title-file")

    summary = args.summary
    if args.summary_file:
        summary = Path(args.summary_file).read_text(encoding="utf-8")

    old_prompt = args.old_prompt
    if Path(args.old_prompt).exists():
        old_prompt = Path(args.old_prompt).read_text(encoding="utf-8")

    feedback = args.feedback
    if Path(args.feedback).exists():
        feedback = Path(args.feedback).read_text(encoding="utf-8")

    new_prompt = run(title, summary, old_prompt, feedback, profile_id=args.profile)
    print(new_prompt)
    if args.write_to:
        Path(args.write_to).write_text(new_prompt + "\n", encoding="utf-8")
        print(f"\n✓ đã ghi vào {args.write_to}", file=sys.stderr)


if __name__ == "__main__":
    main()
