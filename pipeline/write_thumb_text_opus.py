"""write_thumb_text_opus.py — viết CHỮ OVERLAY thumbnail bằng quy trình 2 lượt Opus ĐỘC LẬP,
THAY THẾ `ai_steps.write_thumb_text()` (1 lượt Gemini/ramclouds, không có vòng QC nào).

Quy trình đã verify thật 2026-09-17 (satori ep01, so sánh trực tiếp với bản 1-lượt cũ):
  Title + tóm tắt → Opus VIẾT 3 phương án chữ khác góc độ → Opus CONTEXT MỚI (subprocess `claude -p`
  riêng, không thấy lý do của lượt viết) QC tiếng Nhật + đối chiếu sự thật, chọn bản PASS mạnh nhất
  → ghi ra file. Lượt QC bắt được lỗi thật mà lượt viết không tự thấy (PA3 gán nhầm trách nhiệm hỏi
  chuyện lương hưu cho người kể — lỗi LOGIC câu chuyện, không phải lỗi văn phạm).

Vì sao 2 SUBPROCESS riêng chứ không phải 1 lượt "tự phê bình": mỗi lần gọi `claude -p` là 1 phiên
HEADLESS MỚI HOÀN TOÀN (claude_p_bridge.ask), không mang theo lý do/thiên kiến của lượt viết — cùng
nguyên tắc "2 model độc lập" đã áp dụng cho QC ảnh (xem sol_client.py/qc_thumbnail_sol.py), chỉ khác
ở đây CẢ HAI lượt đều là Opus (đo thật: Opus viết + QC tiếng Nhật tốt hơn hẳn GPT-5.6-sol).

QC ẢNH CUỐI (sau khi render thumbnail thật) VẪN dùng `qc_thumbnail_sol.py` (GPT-5.6-sol, có vision)
— tool này chỉ thay bước VIẾT CHỮ, không thay bước chấm ảnh đã ghép.

Dùng:
  py -3.13 write_thumb_text_opus.py --profile satori-jp-obaa \\
      --title-file listting.txt --summary-file tomtat.txt --out thumb_text.txt
"""
import argparse
import json
import re
import sys
from pathlib import Path

import claude_p_bridge

sys.stdout.reconfigure(encoding="utf-8")

PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles" / "profiles"

WRITE_TMPL = """Bạn đang viết CHỮ PHỦ LÊN THUMBNAIL YouTube tiếng Nhật cho 1 video kể chuyện.

{title_block}

TÓM TẮT/NỘI DUNG THẬT (chữ thumbnail PHẢI khớp đúng, KHÔNG được bịa thêm tình tiết không có ở đây):
{summary}

{claim_focus}

QUY CÁCH KỸ THUẬT (bố cục cố định của kênh, không đổi):
- Mỗi dòng dạng `MÀU|nội dung`, dòng cuối `BANNER|nội dung` (banner luôn có, là câu chốt cảm xúc).
- Màu cho phép: {palette}.
- {n_lines} dòng chữ chính, MỖI DÒNG CỰC NGẮN (lý tưởng ≤8 ký tự tiếng Nhật, tối đa 10) — dòng dài
  làm cỡ chữ tự thu nhỏ đáng kể (đã đo thật: 1 dòng dài kéo cỡ chữ từ 120px xuống còn 78px).
- Dòng BANNER được dài hơn (tự co giãn riêng, không bị giới hạn 8-10 ký tự).
- Các dòng chữ chính ĐỌC LIỀN phải thành 1 câu/mạch ý CÓ NGỮ PHÁP, không phải cụm từ ghép rời rạc.

YÊU CẦU: Viết 3 PHƯƠNG ÁN KHÁC NHAU (khác góc tiếp cận/nhịp điệu, không phải chỉ đổi vài từ của
nhau). Mỗi phương án PHẢI đúng sự thật, tiếng Nhật tự nhiên có đủ trợ từ/ngữ pháp, tạo tò mò hợp
tiêu đề, KHÔNG suy diễn/gán trách nhiệm sai người, KHÔNG gợi ý tình tiết không có trong tóm tắt.

OUTPUT: đúng 3 khối, đặt tên PHƯƠNG ÁN 1/2/3, mỗi khối đúng format `MÀU|nội dung` (không giải
thích dài dòng ngoài format này, có thể ghi 1 dòng ghi chú ngắn cuối mỗi phương án nếu cần)."""

QC_TMPL = """Bạn là người QC ĐỘC LẬP (chưa từng thấy quá trình viết trước đó) cho chữ phủ thumbnail
YouTube tiếng Nhật của 1 video kể chuyện.

{title_block}

SỰ THẬT CÂU CHUYỆN (dùng để đối chiếu — chữ thumbnail KHÔNG được sai lệch hoặc bịa thêm so với đây):
{summary}

{claim_focus}

3 PHƯƠNG ÁN CẦN CHẤM:

{candidates}

CHẤM TỪNG PHƯƠNG ÁN theo:
1. Tiếng Nhật có tự nhiên không (đủ ngữ pháp/trợ từ, không phải cụm từ ghép rời rạc)?
2. Có khớp đúng sự thật câu chuyện không, có bịa/suy diễn/gán sai trách nhiệm không?
3. Độ dài mỗi dòng chính có đủ ngắn để giữ cỡ chữ to không (lý tưởng ≤8 ký tự/dòng)?
4. Có tạo được tò mò/cảm xúc hợp với tiêu đề không?

OUTPUT BẮT BUỘC — ĐÚNG CẤU TRÚC SAU (để máy đọc lại được):

CHẤM:
PHƯƠNG ÁN 1: PASS/FIX/REMAKE — <1 câu lý do>
PHƯƠNG ÁN 2: PASS/FIX/REMAKE — <1 câu lý do>
PHƯƠNG ÁN 3: PASS/FIX/REMAKE — <1 câu lý do>

CHỌN: <số phương án được chọn, hoặc "KHÔNG CÓ" nếu cả 3 đều REMAKE>

BẢN CHỐT:
MÀU|nội dung
MÀU|nội dung
...
BANNER|nội dung
(BẢN CHỐT là phương án được chọn, ĐÃ SỬA nếu QC thấy cần — nếu phương án được chọn không cần sửa gì
thì chép y nguyên. Nếu CHỌN="KHÔNG CÓ" vẫn phải điền BẢN CHỐT là bản ít lỗi nhất kèm sửa tối thiểu.)

BẢN DỊCH (tiếng Việt):
MÀU|nghĩa tiếng Việt của ĐÚNG dòng tiếng Nhật cùng vị trí ở BẢN CHỐT
MÀU|...
BANNER|...
(Dịch NGHĨA cho người không biết tiếng Nhật hiểu được nội dung đang nói gì — không cần dịch sát
từng chữ, ưu tiên dịch cho RÕ NGHĨA. Người đọc bản dịch này KHÔNG xem được ảnh, nên đừng viết kiểu
"như hình trên" — chỉ dịch đúng nghĩa câu chữ.)"""

DEFAULT_CLAIM_FOCUS = ("RÀNG BUỘC SỰ THẬT: Không bịa chi tiết không có trong tóm tắt. Không suy "
                       "diễn động cơ/trách nhiệm cho nhân vật nếu tóm tắt không nói rõ.")


def load_lane_config(profile_id):
    if not profile_id:
        return {}, DEFAULT_CLAIM_FOCUS
    p = PROFILES_DIR / f"{profile_id}.json"
    if not p.exists():
        print(f"  ! khong thay profile {p}, dung mac dinh", file=sys.stderr)
        return {}, DEFAULT_CLAIM_FOCUS
    prof = json.loads(p.read_text(encoding="utf-8"))
    th = prof.get("thumbnail", {}) or {}
    claim_focus = (prof.get("thumbnail_qc") or {}).get("claim_focus") or DEFAULT_CLAIM_FOCUS
    return th, claim_focus


def parse_block(text, header):
    """Bóc khối `<header>:` ra danh sách dòng MÀU|nội dung (kể cả BANNER) — dừng ở dòng trống
    đầu tiên SAU khi đã bắt được ≥1 dòng, để không nuốt luôn khối kế tiếp (vd BẢN CHỐT rồi tới
    BẢN DỊCH liền sau trong cùng response)."""
    m = re.search(rf"{header}\s*[:：]\s*\n(.+)", text, re.DOTALL)
    body = m.group(1) if m else text
    lines = []
    for ln in body.splitlines():
        ln = ln.strip().strip("`")
        if "|" in ln and not ln.lower().startswith(("phương án", "```")):
            lines.append(ln)
        elif lines and not ln:
            break
    return lines


def run(title, summary, profile_id=None, n_lines=4, retries=1):
    th, claim_focus = load_lane_config(profile_id)
    palette = ", ".join(th.get("palette") or ["WHITE", "YELLOW", "RED"])
    n_lines = n_lines or (len(((th.get("template") or {}).get("tiers")) or []) or 3)
    # Ở B7 THẬT trong pipeline chưa có tiêu đề chốt (title.txt/publish_kit sinh ở B9, SAU B7) —
    # tool phải tự chạy được chỉ với script/tóm tắt, giống hệt ai_steps.write_thumb_text() cũ.
    title_block = (f"TIÊU ĐỀ VIDEO (đã chốt, KHÔNG được đổi):\n{title}" if title else
                   "(CHƯA có tiêu đề chốt — tự nhận diện góc hook mạnh nhất từ nội dung dưới đây.)")

    for attempt in range(1, retries + 2):
        write_prompt = WRITE_TMPL.format(title_block=title_block, summary=summary,
                                         claim_focus=claim_focus, palette=palette, n_lines=n_lines)
        print(f"[lượt {attempt}] Opus viết 3 phương án…", file=sys.stderr)
        r1 = claude_p_bridge.ask(write_prompt, model="opus", min_chars=60)
        print(r1.text, file=sys.stderr)

        qc_prompt = QC_TMPL.format(title_block=title_block, summary=summary,
                                   claim_focus=claim_focus, candidates=r1.text)
        print(f"[lượt {attempt}] Opus (context MỚI) QC 3 phương án…", file=sys.stderr)
        r2 = claude_p_bridge.ask(qc_prompt, model="opus", min_chars=60)
        print(r2.text, file=sys.stderr)

        chon = re.search(r"CHỌN\s*[:：]\s*(.+)", r2.text)
        chon_txt = chon.group(1).strip() if chon else "?"
        final_lines = parse_block(r2.text, "BẢN CHỐT")
        vi_lines = parse_block(r2.text, r"BẢN DỊCH \(tiếng Việt\)")
        if final_lines:
            print(f"[chọn={chon_txt}] → {len(final_lines)} dòng "
                  f"(+ {len(vi_lines)} dòng dịch)", file=sys.stderr)
            return final_lines, vi_lines
        print(f"  ! không bóc được BẢN CHỐT ở lượt {attempt}, thử lại…", file=sys.stderr)
    raise RuntimeError("write_thumb_text_opus: hết lượt thử mà vẫn không có BẢN CHỐT hợp lệ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title")
    ap.add_argument("--title-file", help="dòng ĐẦU của file là tiêu đề")
    ap.add_argument("--summary")
    ap.add_argument("--summary-file")
    ap.add_argument("--script-file", help="dùng script.txt đầy đủ thay vì tóm tắt (cắt 6000 ký tự)")
    ap.add_argument("--profile", help="id lane — lấy palette + claim_focus từ profile.json")
    ap.add_argument("--n-lines", type=int, default=0, help="số dòng chữ chính (0 = tự suy từ profile)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    title = args.title
    if args.title_file:
        lines = Path(args.title_file).read_text(encoding="utf-8").splitlines()
        title = next((l.strip() for l in lines if l.strip()), "")
    # title RỖNG là hợp lệ (đúng thời điểm B7 thật, xem run()) — không ép buộc như trước.

    if args.script_file:
        summary = Path(args.script_file).read_text(encoding="utf-8")[:6000]
    else:
        summary = args.summary
        if args.summary_file:
            summary = Path(args.summary_file).read_text(encoding="utf-8")
    if not summary:
        ap.error("cần --summary, --summary-file hoặc --script-file")

    final_lines, vi_lines = run(title, summary, profile_id=args.profile, n_lines=args.n_lines)
    out_path = Path(args.out)
    out_text = "\n".join(final_lines) + "\n"
    out_path.write_text(out_text, encoding="utf-8")
    print(out_text)
    print(f"✓ đã ghi {out_path}", file=sys.stderr)

    # File dịch tiếng Việt CẠNH thumb_text.txt — user không đọc được tiếng Nhật, cần hiểu thumbnail
    # đang nói gì mà không phải hỏi lại mỗi lần (đúng quy ước "_vi" đã dùng cho voice_vi.srt/
    # tomtat_vi.txt trong dự án). Vẫn ghi file dù rỗng — báo rõ thiếu thay vì im lặng bỏ qua.
    vi_path = out_path.with_name(out_path.stem + "_vi" + out_path.suffix)
    if vi_lines:
        vi_path.write_text("\n".join(vi_lines) + "\n", encoding="utf-8")
        print(f"✓ đã ghi {vi_path} (bản dịch tiếng Việt)", file=sys.stderr)
    else:
        print(f"  ! Opus không trả BẢN DỊCH hợp lệ — {vi_path} CHƯA được ghi", file=sys.stderr)


if __name__ == "__main__":
    main()
