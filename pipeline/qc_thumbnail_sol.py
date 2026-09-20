"""qc_thumbnail_sol.py — QC ĐỘC LẬP thumbnail bằng GPT-5.6-sol (khác hẳn Gemini/ramclouds đang
dùng ở mọi cổng QC khác của pipeline — xem sol_client.py để biết TẠI SAO cần model thứ 2).

Chấm 6 mục: chữ tiếng Nhật (typo/ngắt dòng sai) · khớp thumbnail↔title · lỗi ảnh AI · bố cục/khả
năng đọc · sức hút · claim/độ chính xác (mục claim CÓ THỂ tuỳ biến theo lane qua --profile, xem
`thumbnail_qc.claim_focus` trong profile.json — mỗi ngách có rủi ro claim khác nhau, sức khỏe khác
truyền thuyết đô thị khác lịch sử chiến tranh).

Trả về PASS / FIX / REMAKE — quy trình dùng đúng như đã verify thật 2026-09-17 (kenko-chiebukuro
ep01, 3 vòng QC liên tiếp): FIX thì đọc mục "CẦN SỬA", sửa ĐÚNG chỗ đó, gửi lại chấm tiếp, lặp
tối đa 3 vòng — KHÔNG tự ý đổi tiêu đề video, KHÔNG đổi nội dung/claim chỉ để né QC.

Dùng:
  py -3.13 qc_thumbnail_sol.py --thumb thumbnail.png --title "..." --summary summary.txt
  py -3.13 qc_thumbnail_sol.py --thumb thumbnail.png --title-file listting.txt --profile kenko-chiebukuro
  (--title-file: dòng ĐẦU của file là tiêu đề, xem quy ước listting.txt của dự án)
"""
import argparse
import json
import re
import sys
from pathlib import Path

import sol_client

sys.stdout.reconfigure(encoding="utf-8")

PROMPT_TMPL = """Bạn là QC cuối cùng cho thumbnail YouTube tiếng Nhật.

INPUT:
- Thumbnail: (ảnh đính kèm)
- Tiêu đề video: {title}
- Nội dung/tóm tắt video nếu có: {summary}

Hãy kiểm tra thumbnail dựa trên TIÊU ĐỀ và NỘI DUNG video.

MỤC TIÊU:
Phát hiện lỗi trước khi thumbnail được đăng lên YouTube.
Không thiết kế lại thumbnail nếu không cần thiết.
Chỉ báo những vấn đề thực sự đáng sửa.

HÃY KIỂM TRA:

1. CHỮ TIẾNG NHẬT
- Đọc chính xác toàn bộ chữ xuất hiện trên thumbnail.
- Có typo, sai Kanji/Kana, mất ký tự hoặc ký tự render lỗi không?
- Câu có tự nhiên với người Nhật không?
- Có cụm từ khó hiểu, sai ngữ pháp hoặc mang nghĩa khác dự định không?
- Có từ nào bị xuống dòng/tách dòng sai làm thay đổi hoặc khó hiểu nghĩa không?

2. THUMBNAIL ↔ TITLE
- Nội dung chữ trên thumbnail có đúng chủ đề của title không?
- Có mâu thuẫn với title không?
- Thumbnail có khiến người xem hiểu sai nội dung video không?
- Hình ảnh minh họa có phù hợp với title không?
- Có chi tiết quan trọng nào trong ảnh không khớp với nội dung không?

3. HÌNH ẢNH
- Có vật thể bị lỗi AI, biến dạng, dư/thiếu chi tiết bất thường không?
- Hình ảnh chính có dễ nhận biết khi thumbnail thu nhỏ không?
- Hình có truyền tải đúng chủ đề video không?
- Có chi tiết gây hiểu nhầm không?

4. BỐ CỤC & KHẢ NĂNG ĐỌC
- Chữ có quá nhiều không?
- Chữ có đủ lớn để đọc trên điện thoại không?
- Có chữ bị sát mép, cắt, che hoặc chồng lên hình không?
- Màu chữ và background có đủ tương phản không?
- Viền chữ/stroke có quá dày làm Kanji bị bệt hoặc mất nét không?
- Thứ tự thị giác có rõ ràng không?
- Người xem có thể hiểu thông điệp chính trong khoảng 1–2 giây không?

5. SỨC HÚT / CLICKABILITY
- Thumbnail có tạo tò mò phù hợp với title không?
- Có phần chữ nào thừa hoặc lặp lại title mà không mang thêm giá trị không?
- Có thể rút ngắn chữ để mạnh và dễ đọc hơn không?
- Hình ảnh có đủ nổi bật khi đứng cạnh các thumbnail khác không?

6. CLAIM / ĐỘ CHÍNH XÁC
{claim_focus}
Nếu có, chỉ rõ chính xác câu cần sửa.

QUY TẮC ĐÁNH GIÁ:
Không chấm điểm chung chung.
Phân loại kết quả cuối cùng thành:

PASS = Có thể dùng ngay, không có lỗi đáng kể.
FIX = Có lỗi đáng sửa trước khi đăng.
REMAKE = Có vấn đề lớn về nội dung/hình ảnh/bố cục, nên làm lại.

OUTPUT BẮT BUỘC:

KẾT QUẢ: [PASS / FIX / REMAKE]

CHỮ ĐỌC ĐƯỢC TRÊN THUMBNAIL:
[chép nguyên văn tiếng Nhật theo từng dòng]

LỖI PHÁT HIỆN:
- [lỗi 1]
- [lỗi 2]
Nếu không có lỗi, ghi: Không phát hiện lỗi đáng kể.

CẦN SỬA:
- [nêu chính xác phần cần sửa → đề xuất thay bằng gì]
Chỉ đề xuất những thay đổi thực sự cần thiết.

KẾT LUẬN:
[2–4 câu ngắn: thumbnail có khớp title không, vấn đề quan trọng nhất là gì và có thể đăng ngay hay cần sửa.]
"""

DEFAULT_CLAIM_FOCUS = """Đặc biệt kiểm tra nếu video thuộc sức khỏe, lịch sử, khoa học hoặc sự kiện có thật:
- Thumbnail có biến thông tin chưa chắc chắn thành sự thật tuyệt đối không?
- Có câu trích dẫn được trình bày như lời nói thật nhưng nội dung không chứng minh được không?
- Có claim quá tuyệt đối (dạng "chắc chắn", "100%", "không bao giờ", "chữa khỏi") không?"""


def load_claim_focus(profile_id):
    """Đọc `thumbnail_qc.claim_focus` trong profiles/profiles/<id>.json nếu có — MỖI LANE tự
    khai rủi ro claim riêng của ngách mình (sức khỏe khác truyền thuyết khác lịch sử chiến
    tranh). Không khai thì dùng mặc định chung ở trên."""
    if not profile_id:
        return DEFAULT_CLAIM_FOCUS
    p = Path(__file__).resolve().parent.parent / "profiles" / "profiles" / f"{profile_id}.json"
    if not p.exists():
        print(f"  ! khong thay profile {p}, dung claim_focus mac dinh")
        return DEFAULT_CLAIM_FOCUS
    prof = json.loads(p.read_text(encoding="utf-8"))
    focus = (prof.get("thumbnail_qc") or {}).get("claim_focus")
    return focus.strip() if focus else DEFAULT_CLAIM_FOCUS


def parse_verdict(text):
    m = re.search(r"KẾT QUẢ\s*[:：]\s*(PASS|FIX|REMAKE)", text, re.IGNORECASE)
    return m.group(1).upper() if m else "UNKNOWN"


def run(thumb, title, summary, profile_id=None, out=None):
    claim_focus = load_claim_focus(profile_id)
    prompt = PROMPT_TMPL.format(title=title, summary=summary or "(không có)",
                                claim_focus=claim_focus)
    text, usage = sol_client.chat(prompt, image_path=thumb, max_tokens=2000)
    verdict = parse_verdict(text)
    print(text)
    print(f"\n[verdict={verdict}] usage={json.dumps(usage)}", file=sys.stderr)
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return verdict, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thumb", required=True, help="đường dẫn ảnh thumbnail (.png/.jpg)")
    ap.add_argument("--title", help="tiêu đề video (chuỗi trực tiếp)")
    ap.add_argument("--title-file", help="file mà DÒNG ĐẦU là tiêu đề (quy ước listting.txt)")
    ap.add_argument("--summary", help="tóm tắt/mô tả video (chuỗi trực tiếp)")
    ap.add_argument("--summary-file", help="file chứa mô tả đầy đủ")
    ap.add_argument("--profile", help="id lane (profiles/profiles/<id>.json) — lấy claim_focus riêng")
    ap.add_argument("--out", help="lưu output thô ra file")
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

    verdict, _ = run(args.thumb, title, summary, profile_id=args.profile, out=args.out)
    sys.exit(0 if verdict == "PASS" else 2 if verdict == "FIX" else 3)


if __name__ == "__main__":
    main()
