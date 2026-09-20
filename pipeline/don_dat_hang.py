# -*- coding: utf-8 -*-
"""don_dat_hang.py — sinh ĐƠN ĐẶT HÀNG gửi dự án nghiên cứu, cho MỘT lane.

    py -3.13 don_dat_hang.py --profile toshi-densetsu-jp
    py -3.13 don_dat_hang.py --profile <lane> --out "E:\\...\\SPACE_RESEARCH"

VÌ SAO CẦN — chỗ hở của quy trình giao việc bản đầu
------------------------------------------------------------------------------------------------
`docs/GIAO_VIEC_SPACE_RESEARCH.md` nói "hợp đồng nằm ở `profile.research`". Đúng với BÊN MÌNH,
nhưng bắt dự án bên kia mở JSON của h2dev ra đọc là sai hướng: hai dự án tách vai chính là để bên
đó không phải biết ruột gan bên này. Và một lane mới thì chính bên này cũng chưa chắc đã khai đủ
khối `research` — không có gì nhắc.

Nên: h2dev **tự xuất ra một file duy nhất, tự chứa**, đặt thẳng vào thư mục dự án nghiên cứu. Bên
đó chỉ cần đọc đúng file đó là làm được, không mở dự án này lần nào.

Đơn sinh RA TỪ PROFILE, không gõ tay. Ngưỡng trong đơn và ngưỡng cổng B0 (`qc_hoso.py`) đọc **cùng
một khối JSON**, nên không thể lệch nhau — lỗi kinh điển của hợp đồng viết tay là bản gửi đi một
đằng, bản đem ra chấm một nẻo.
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path


def _ensure_std():
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_std()
sys.path.insert(0, str(Path(__file__).resolve().parent))

MAC_DINH_RA = Path("E:/CLAUDE/YOUTUBE/SPACE_RESEARCH")


def dong(v, mac_dinh="—"):
    return mac_dinh if v in (None, "", [], {}) else v


def dung_don(prof: dict) -> str:
    rs = prof.get("research") or {}
    sc = prof.get("script") or {}
    gate = sc.get("gate") or {}
    body = prof.get("body") or {}
    voice = prof.get("voice") or {}
    nar = prof.get("narrator") or {}

    phut = float(sc.get("target_minutes") or 0)
    rate = float(voice.get("char_rate") or 0)
    cuts = body.get("cuts_per_min") or [12, 16]
    canh = int(phut * (sum(cuts) / 2)) if phut else 0
    lo_r, hi_r = (rs.get("competitor_ratio") or [0.85, 1.30])[:2]
    tlo, thi = (gate.get("title_len") or [1, 100])[:2]
    moc = gate.get("chapter_markers") or []
    stock = bool(rs.get("deliver_stock"))
    evid = bool(rs.get("deliver_evidence"))
    la_clip = (body.get("mode") == "stock_clips")

    t = []
    A = t.append
    A(f"# ĐƠN ĐẶT HÀNG NGHIÊN CỨU — lane `{prof.get('id')}`")
    A("")
    A(f"> Sinh tự động bởi `h2dev/pipeline/don_dat_hang.py` ngày {date.today():%Y-%m-%d}.")
    A("> **File này tự chứa** — không cần mở dự án h2dev để bắt đầu.")
    A("> Mọi ngưỡng dưới đây lấy thẳng từ profile của lane, và **cổng nghiệm thu chấm bằng đúng")
    A(">  những con số này** (`h2dev/pipeline/qc_hoso.py`). Không có bản thứ hai để tranh cãi.")
    A("")
    A("---")
    A("")
    A("## 1. KHÁCH HÀNG CỦA ĐƠN NÀY")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| Lane | `{prof.get('id')}` |")
    A(f"| Thị trường · ngôn ngữ | {dong(prof.get('market'))} · {dong(prof.get('language'))} |")
    A(f"| Ngách | {dong(prof.get('niche'))} |")
    A(f"| Kênh tham chiếu | {dong(prof.get('competitor'))} |")
    A(f"| Người dẫn | {dong(nar.get('persona'))} |")
    A(f"| Độ dài video mục tiêu | **{phut:.0f} phút** |")
    A(f"| Thân video | {'CLIP STOCK' if la_clip else 'ẢNH AI'} |")
    A("")
    if not rs:
        A("> ⚠️ **Lane này CHƯA khai khối `research` trong profile.** Đơn đặt hàng chỉ là bản")
        A("> rỗng. Bên h2dev phải khai hợp đồng trước rồi sinh lại đơn — đừng bắt đầu nghiên cứu")
        A("> theo bản này.")
        A("")
    A("---")
    A("")
    A("## 2. GIAO GÌ — mỗi đề tài một thư mục")
    A("")
    A("```")
    A("output/_READY/<nn>-<slug>/")
    thu_muc_anh = rs.get("evidence_dir") or "stock"
    for f in rs.get("files_required") or []:
        ghi = {"series_ctx.txt": "  ← TƯ LIỆU SỰ THẬT (file chính)",
               "competitor.txt": "  ← KHUNG NHỊP (transcript video dài của kênh cùng định dạng)",
               "stock_queries.txt": "  ← từ khoá tiếng Anh, CHIA THEO CHƯƠNG",
               "evidence.json": "  ← ảnh dẫn nguồn, CHỈ Public Domain"}.get(f, "")
        A(f"    {f:<20}{ghi}")
    if evid:
        A(f"    {thu_muc_anh}/")
        A(f"        *.jpg *.png            ← file ẢNH THẬT, tên khớp đúng field `file` trong "
          f"evidence.json")
    if stock:
        A("    stock/")
        A("        manifest.jsonl    ← SỔ GIẤY PHÉP, mỗi file một dòng")
        A("        *.mp4 *.jpg")
    A("```")
    A("")
    A("⚠️ `competitor.txt` và `series_ctx.txt` **khác vai trò, đừng gộp**. File đầu dạy NHỊP và")
    A("thứ tự dẫn dắt — có thể là đề tài hoàn toàn khác. File sau mới là nội dung.")
    A("")
    A("---")
    A("")
    A("## 3. NGƯỠNG NGHIỆM THU — cổng chấm đúng bảng này")
    A("")
    A("| Mục | Ngưỡng | Trượt thì sao |")
    A("|---|---|---|")
    if phut and rate:
        A(f"| `competitor.txt` độ dài | **{phut*lo_r:.0f}–{phut*hi_r:.0f} phút** "
          f"(≈{phut*lo_r*rate:,.0f}–{phut*hi_r*rate:,.0f} chữ, char-rate {rate:g}/phút) | "
          f"dạy sai nhịp ⇒ mất mốc chương, không cổng nào sau đó bắt được |")
    A(f"| Tiêu đề | **{rs.get('title_options_min', 1)} phương án**, mỗi phương án "
      f"**{tlo}–{thi} ký tự** (đếm CẢ khối tag 【】) | lệch dải ⇒ view thấp hơn 2,4 lần |")
    A("| | ❌ **Cấm ghi \"ĐÃ CHỐT / không đổi\"** — quyền chốt tiêu đề thuộc bên làm video "
      "(còn phải khớp thumbnail) | |")
    if moc:
        A(f"| Khung chương | đủ {len(moc)} mốc: {' '.join(moc)} | pipeline không tự nghĩ ra khung |")
    hook = gate.get("require_japan_hook_chapter")
    if hook:
        A(f"| Chương {hook} | **bắt buộc móc về {dong(prof.get('market'))}** | công thức kênh |")
    if rs.get("blocks_required"):
        A(f"| Khối bắt buộc trong tư liệu | {' · '.join('「'+b+'」' for b in rs['blocks_required'])} "
          f"| thiếu khối ⇒ chương đó không có nguyên liệu ⇒ model tự bịa |")
    A(f"| Độ phủ nguồn | ≥ **{float(rs.get('source_coverage_min', 0.9)):.0%}** số khối dữ kiện "
      f"có 〔出典: URL — 原文: \"…\"〕 | khối không nguồn = không truy ngược được khi bị khiếu nại |")
    A(f"| `stock_queries.txt` | ≥ **{rs.get('stock_queries_min', 12)} từ khoá**"
      + (f", chia thành **{len(moc) or 5} nhóm `# 第N章`**" if rs.get("stock_by_chapter") else "")
      + " | danh sách phẳng dồn hết vào chương 1, đếm TỔNG vẫn thấy \"đủ\" |")
    if stock and canh:
        A(f"| `stock/` | kho phải **gánh được ≥{canh} cảnh** "
          f"(video {phut:.0f}′ × {sum(cuts)/2:.0f} cảnh/phút, trần dùng lại "
          f"{body.get('reuse_max', 6)} lần/clip) | kho mỏng = lặp hình thấy rõ |")
    if evid:
        A(f"| `evidence.json` | ≥ **{rs.get('evidence_min', 8)} mục**, mỗi mục đủ "
          f"`file · caption · source · license`, giấy phép **chỉ "
          f"{body.get('evidence_license_policy', 'pd').upper()}** | ảnh cháy màn hình sai giấy "
          f"phép là rủi ro thật |")
    A("")
    A("---")
    A("")
    A("## 4. LUẬT SỐ 1 KHI VIẾT TƯ LIỆU")
    A("")
    A("> **Tư liệu thiếu chỗ nào, mô hình sẽ tự điền chỗ đó.**")
    A("")
    A("Ở chế độ này mô hình **bị cấm tự nghĩ ra tên người, năm, địa danh, số liệu** — nó chỉ được")
    A("dùng thứ có trong tư liệu. Nên im lặng không phải là an toàn, im lặng là lời mời sáng tác.")
    A("")
    A("Bốn luật rút ra từ lỗi đã dính thật:")
    A("")
    A("1. **Ghi ĐỦ hoặc ghi thẳng là KHÔNG CÓ.** Hồ sơ viết \"bộ phim công chiếu chưa đầy một năm")
    A("   trước\" mà không ghi năm, không ghi đạo diễn ⇒ model tự điền năm và tên đạo diễn. Nếu")
    A("   nguồn không có thì viết hẳn ra: `公開年と監督名は資料になし。書くな。`")
    A("2. **Số đo ghi SẴN CẢ HAI ĐƠN VỊ**: `約125海里（約232km）`. Để một phép đổi đơn vị hở ra là")
    A("   model tự bấm máy — lần này ra đúng, lần trước ra `埼玉県` bịa.")
    A("3. **Số dạng khoảng phải chốt**: `3〜4倍` → thêm dòng \"= 3倍 hoặc 4倍, không viết số khác\".")
    A("4. **Kèm phía phản bác, có nguyên văn.** Khung chương có chương phản bác mà tư liệu không")
    A("   cấp dữ kiện phản bác nào thì model nghiêng hẳn một chiều — vừa dở vừa dễ bị gắn cờ.")
    A("")
    if stock:
        A("---")
        A("")
        A("## 5. KHO HÌNH — ràng buộc kỹ thuật")
        A("")
        A(f"- **Nguồn dùng**: `{body.get('stock_sources', 'nasa,pexels')}`")
        A(f"- **Giấy phép b-roll** (`{body.get('license_policy', 'permissive')}`): nhận Public")
        A("  Domain / CC0 / CC BY / Pexels-Pixabay-Unsplash. **LOẠI mọi thứ có `-SA`, `-NC`,")
        A("  `-ND`** — SA kéo cả video 30 phút vào ràng buộc chia sẻ tương tự, NC cấm kiếm tiền,")
        A("  ND cấm cắt ghép. Lọc ngay lúc TÌM, đừng tải về rồi mới loại.")
        A("- **Chiều cao ≥720px · độ sáng trung bình ≥20/255.** Đo thật: một clip nguyệt thực")
        A("  độ sáng 14,0 lọt vào video, trên màn hình nhìn như khung đen.")
        A("- **Ưu tiên clip dài ≥20 giây.** Bên dựng cắt bỏ **6s đầu + 9s đuôi** mỗi clip để né")
        A("  thẻ thương hiệu (clip NASA gắn logo + \"GODDARD SPACE FLIGHT CENTER\" ở hai đầu).")
        A("  Clip 10 giây thì cắt xong không còn gì.")
        A("- **B-roll không được mang CHỮ của câu chuyện khác.** Đã dính: một cảnh rơi vào biểu đồ")
        A("  El Niño của NOAA có dòng chữ tiếng Anh, chạy giữa đoạn kể về đá vũ trụ. Loại sẵn")
        A("  title chứa: chart, diagram, graph, map of, screenshot, poster, logo, certificate.")
        A("- ⛔ **Xếp hạng độ phân giải NASA phải là** `{\"large\":0,\"medium\":1,\"small\":2,")
        A("  \"mobile\":3}`. NASA `~mobile` là **320×180**, phóng lên 1920×1080 là upscale 6 lần.")
        A("  Đo thật: 73% thời lượng một video dựng từ clip 320×180, chủ dự án xem xong nhận xét")
        A("  \"ảnh cũ mờ\". Nỗi lo `~orig` 5,4 GB đã được chặn ở tầng khác (trần 250 MB + sàn tốc")
        A("  độ + trần 90s mỗi file) — đừng né bằng cách chọn bản bé nhất.")
        A("- **`manifest.jsonl` là nguồn chân lý bản quyền.** File nào không có dòng trong đó thì")
        A("  bên dựng BỎ HẲN (không đoán bản quyền) ⇒ đừng chép file vào thư mục bằng tay.")
        A("")
    A("---")
    A("")
    A("## 6. NHỊP GIAO HÀNG — cột `TÌNH TRẠNG` trên trang tính")
    A("")
    A("| Chặng | Hình ảnh | Cột TÌNH TRẠNG |")
    A("|---|---|---|")
    A("| Sàng lọc nhiều đề tài ứng viên | **CHỈ DÒ API đếm kết quả — không tải file nào** | (trống) |")
    A("| Đã chốt 1 đề tài, viết hồ sơ | — | `DOING` |")
    A("| Hồ sơ xong | **TẢI** kho hình + ảnh dẫn nguồn | `DOING` |")
    A("| Tự chấm đủ bảng mục 3 | — | ghi **`DONE-READY`** |")
    A("")
    A("**Cấm tải ở chặng sàng lọc**: chặng đó có nhiều ứng viên, 9 đề tài bị loại vẫn để lại")
    A("~1,8 GB mỗi cái nằm chết trên ổ.")
    A("")
    A("⚠️ **`DONE-READY` mang nghĩa NẶNG: \"hồ sơ + kho hình đã sẵn sàng, cắm vào dựng được ngay\"**")
    A("— không còn là \"đã viết xong hồ sơ\". Vì nó là **thứ duy nhất báo bên kia đã ghi XONG**.")
    A("Đã dính thật: bên h2dev chạy cổng lúc đây còn tải dở, thư mục có 9 file `.mp4` mà nạp được")
    A("**1** (8 file viết dở, ffprobe đọc không ra, bị loại lặng lẽ) — cổng in ra một con số hoàn")
    A("toàn sai mà nhìn y hệt kết luận thật. **Ghi cờ sau khi mọi thứ đã nằm trên ổ.**")
    A("")
    A("---")
    A("")
    A("## 7. CỔNG CHẤM — chạy thử trước khi ghi DONE-READY")
    A("")
    A("Bên h2dev chạy lệnh này ngay khi thấy cờ. Nếu chạy được ở đây thì cứ tự chạy trước:")
    A("")
    A("```")
    A(f"py -3.13 E:\\CLAUDE\\YOUTUBE\\h2dev\\pipeline\\qc_hoso.py \\")
    A(f"        --folder \"<...>\\output\\_READY\\<nn>-<slug>\" --profile {prof.get('id')}")
    A("```")
    A("")
    A("Trượt thì hồ sơ bị **trả lại kèm danh sách**, không ai sửa hộ — sửa hộ thì tập sau sai y hệt.")
    A("")
    A("---")
    A("")
    A("## 8. NẾU ĐÂY LÀ LANE THỨ HAI TRỞ ĐI")
    A("")
    A("`CLAUDE.md` của dự án nghiên cứu hiện viết cho **một kênh duy nhất** — số liệu ngách, khung")
    A("chương, giọng văn đều đóng cứng theo kênh đó. Thêm lane mới thì **đừng sửa đè**, mà thêm")
    A("một mục lane riêng + một bảng router ở đầu file, giống cách h2dev đã làm:")
    A("")
    A("> Ngưỡng của lane này KHÔNG được chép từ lane kia. Mọi con số phải đo lại từ kênh tham")
    A("> chiếu của chính lane này. Bài học đã trả giá: chép ngưỡng \"しかし mỗi ≤90 giây\" từ một")
    A("> tài liệu sang, đo lại kênh thật thì khoảng cách thực là 200–560 giây.")
    A("")
    return "\n".join(t) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--out", default=str(MAC_DINH_RA),
                    help="thư mục dự án nghiên cứu (mặc định SPACE_RESEARCH)")
    a = ap.parse_args()

    import profiles
    prof = profiles.load(a.profile)
    ra = Path(a.out)
    if not ra.exists():
        raise SystemExit(f"✗ không thấy thư mục dự án nghiên cứu: {ra}")
    f = ra / f"DON_DAT_HANG_{prof.get('id')}.md"
    f.write_text(dung_don(prof), encoding="utf-8")
    if not prof.get("research"):
        print(f"⚠️ profile '{a.profile}' CHƯA khai khối `research` — đơn đang RỖNG NGƯỠNG. "
              f"Khai hợp đồng trong profile rồi sinh lại, đừng gửi bản này.")
    print("\n" + "─" * 78)
    print("ĐƯA ĐƯỜNG DẪN NÀY CHO CHAT CỦA DỰ ÁN NGHIÊN CỨU:")
    print(f"\n{f}\n")
    print("─" * 78)


if __name__ == "__main__":
    main()
