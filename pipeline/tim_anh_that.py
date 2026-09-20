# -*- coding: utf-8 -*-
"""tim_anh_that.py — tìm CLIP/ẢNH THẬT MIỄN PHÍ thay cho vẽ AI, cho các đoạn B5K đã gán CU_THE.

    py -3.13 tim_anh_that.py --slug <thư mục tập>

Chạy SAU B5K (cần `khop_hinh.json`), TRƯỚC khi ra đơn ảnh (`sinh_anh_canh.py --chi-don`).

VÌ SAO CÓ FILE NÀY (anh chốt 2026-09-16, sau khi nghiên cứu ep05-bermuda-triangle +
ep06-mandela-effect)
------------------------------------------------------------------------------------------------
`khop_hinh.py` (B5K) gán nhãn CU_THE THUẦN BẰNG NGỮ NGHĨA — "câu này có nói tới một vật/nơi/thiết
bị XÁC ĐỊNH không" — mà KHÔNG HỀ thử tìm xem thứ đó có tìm được thật hay không. Một câu nói tới
"cargo ship at sea" hay "night sky stars milky way" hoàn toàn ĐỦ CỤ THỂ để bị gán CU_THE, dù kho
ảnh miễn phí có hàng nghìn clip đúng y hệt. Đo thật: lấy 43 từ khoá CU_THE duy nhất của 2 tập
trên, tìm thật trên Pexels rồi cho gemini-3.8-flash (qua ramclouds) xem 5 tiêu đề mỗi từ khoá và
chấm độ khớp — 63% SỐ ĐOẠN có kết quả khớp tốt. Nghĩa là gần 2/3 lượng ảnh AI đang vẽ ra (và tốn
lượt vẽ của máy 2, nơi có trần ~310 ảnh/2 giờ) là để thay cho thứ vốn ĐÃ CÓ SẴN miễn phí.

CƠ CHẾ — VÌ SAO KHÔNG CẦN SỬA `stock_cut.py`
------------------------------------------------------------------------------------------------
`stock_cut.chia_theo_cau()` (đọc `khop_hinh.json`) đã lấy field `query` của MỌI đoạn — kể cả đoạn
CU_THE — làm tập từ khoá ĐƯỢC PHÉP cho đúng khung giờ đó khi `chon_nguon()` chọn clip thường. Vấn
đề chỉ là: chưa từng có file nào trong `stock/` được TẢI VỀ đúng bằng từ khoá CU_THE đó (kho chỉ
có các từ khoá cố định trong `stock_queries.txt`, viết trước khi có kịch bản), nên `chon_nguon()`
luôn thấy khung giờ đó "cạn clip đúng chương" và phải mượn bừa. File này bịt đúng lỗ hổng: TẢI
THẬT một file khớp đúng `query` của đoạn CU_THE, gắn `query` ĐÚNG NHƯ VẬY vào manifest.jsonl — từ
đó `chon_nguon()` tự nhiên chọn đúng file này cho đúng khung giờ, không cần sửa gì ở `stock_cut.py`.
Chỉ cần thêm MỘT việc: đổi `loai` của đoạn đó từ `CU_THE` sang `CU_THE_DA_TIM_DUOC` để `sinh_anh_canh.py`
(lọc đúng `loai == "CU_THE"`) không vẽ AI cho đoạn này nữa.

⚠️ CHẤM ĐỘ KHỚP BẮT BUỘC BẰNG gemini-3.8-flash (qua ramclouds), KHÔNG PHẢI CLAUDE TỰ ĐỌC/TỰ QUYẾT
------------------------------------------------------------------------------------------------
Anh chốt rõ 2026-09-16. Lý do kỹ thuật trùng với mọi cổng khác của lane này (`soi_kho.py`,
`qc_canh.py`): Claude không "nhìn" được frame ảnh thật trong ngữ cảnh này, và giữ nguyên tắc "máy
đo, không phải Claude tự khai" — vision model độc lập chấm, code tự ép luật, không tin cảm giác.
Dùng LẠI ĐÚNG hàm `soi_kho.cham()` (đã học bài học thang chấm hỏng: bắt tả CHỦ THỂ trước, `co_chu_de`
sau, `muc` tính từ đó — không hỏi thẳng "có khớp không" vì mọi thứ sẽ dồn vào một bậc giữa).

⚠️ MỘT FILE VẬT LÝ CÓ THỂ PHỤC VỤ NHIỀU TỪ KHOÁ — ĐỪNG CHẶN, HÃY NHÂN BẢN
------------------------------------------------------------------------------------------------
`manifest.jsonl` chỉ giữ được MỘT `query` cho mỗi TÊN FILE (`doc_manifest()` là dict theo tên file,
dòng ghi sau đè dòng trước). Pexels rất hay trả về CÙNG một video cho hai từ khoá gần nghĩa (vd
"toy store shelf" và "toy store shelf colorful"), và đôi khi trùng luôn với một file kho ĐÃ TẢI
SẴN TỪ TRƯỚC (do hồ sơ nghiên cứu hoặc B5 tải, gắn NHÃN KHÁC). Bản đầu của file này CHẶN LUÔN mọi
ứng viên trùng ID với bất kỳ file nào đã có trong manifest — tưởng là an toàn, nhưng thực ra chặn
nhầm cả trường hợp TỐT (ứng viên đúng là file kho đã có sẵn, vừa được vision xác nhận khớp thêm
một ý nghĩa nữa) → chạy thật ra kết quả 0/23, tệ hơn không làm gì. Sửa đúng: KHÔNG chặn ứng viên
ở khâu chấm; nếu lúc LƯU phát hiện trùng TÊN FILE ĐÍCH, tạo một BẢN SAO vật lý mang tên khác
(thêm hậu tố) rồi ghi DÒNG MANIFEST MỚI cho bản sao đó — dòng gốc không bị đụng, tốn thêm vài MB
đĩa nhưng không có cách nào ít rủi ro hơn với schema hiện tại (mỗi file 1 query).

GIỚI HẠN CỦA LƯỢT NÀY (nói rõ, đừng ngộ nhận đã làm hết)
------------------------------------------------------------------------------------------------
Chỉ tìm qua PEXELS (nguồn đã verify mạnh nhất cho b-roll đời thường/lịch sử gần, xem
`docs/laneA_from_research` + `Huong_dan_nguon_anh_video_mien_phi_cho_YouTube.docx`). Tài liệu đó
còn khuyến nghị Pixabay/Unsplash/Mixkit/Coverr/Wikimedia/Library of Congress — CHƯA viết thêm vào
`stock_sources.py` ở lượt này (mỗi nguồn cần tự kiểm API + giấy phép riêng, không làm vội). Việc
mở rộng nguồn là bước SAU, độc lập với file này — file này giải quyết đúng phần lớn nhất (63%)
bằng đúng nguồn đã có sẵn và đã verify.
"""
import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent

SO_UNG_VIEN = 5       # ứng viên tải/thử mỗi từ khoá (đủ để có cơ hội trúng, không tải hết cả 5)
DUNG_TOI_DA = 3        # trong SO_UNG_VIEN đó, tải thật + chấm tối đa bấy nhiêu — trúng sớm thì dừng
NGHI_GIUA_TU_KHOA = 0.3
MAX_BYTES_UNG_VIEN = 60 * 1024 * 1024   # 60 MB — ứng viên chỉ để CHẤM, không cần bản gốc quá to
TIMEOUT_TAI = (10, 20)                    # (nối, đọc) giây — mỗi CHUNK phải về trong 20s


def _tai_va_luu_frame(url: str, tmp: Path, ten: str):
    """Tải 1 file về `tmp`, cắt khung giữa để chấm. Trả (đường_dẫn_file_goc, đường_dẫn_frame).

    ⚠️ Đã dính TREO THẬT 2026-09-16: `requests.get(..., timeout=TIMEOUT)` chỉ áp cho lúc NỐI +
    byte đầu tiên — một kết nối tụt tốc độ giữa chừng (còn sống, chỉ rất chậm) không bị timeout
    cắt, và vòng `for chunk in r.iter_content()` treo vô thời hạn không có gì bắt được. Nay
    timeout là CẶP (nối, đọc-mỗi-lần) nên mỗi khối chunk cũng bị giới hạn, và có trần dung lượng
    kèm mốc thời gian tổng để bỏ giữa chừng thay vì chờ mãi.

    `ten` PHẢI DUY NHẤT GIỮA MỌI LẦN GỌI TRONG CẢ LƯỢT CHẠY (không chỉ trong một từ khoá) — đã
    dính thật: đặt tên chỉ theo chỉ số ứng viên (`cv_0.mp4`) khiến hai từ khoá KHÁC NHAU cùng ghi
    đè lên một tên file tạm, rồi từ khoá sau xoá mất file mà từ khoá trước đang tham chiếu tới,
    vỡ ở bước di chuyển cuối cùng (`FileNotFoundError`)."""
    import time as _time
    import requests
    from stock_sources import UA
    ext = ".mp4" if url.lower().split("?")[0].endswith(".mp4") else Path(url).suffix or ".jpg"
    dest = tmp / f"{ten}{ext}"
    t0 = _time.time()
    got = 0
    with requests.get(url, headers=UA, timeout=TIMEOUT_TAI, stream=True) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_content(1 << 16):
                got += len(chunk)
                if got > MAX_BYTES_UNG_VIEN:
                    raise IOError(f"ứng viên > {MAX_BYTES_UNG_VIEN // 1024 // 1024} MB, bỏ")
                if _time.time() - t0 > 60:
                    raise IOError("tải ứng viên quá 60s, bỏ")
                f.write(chunk)
    if ext == ".mp4":
        import soi_kho
        frame = soi_kho.khung_giua(dest, tmp)
        return dest, frame
    return dest, dest   # ảnh tĩnh: chấm thẳng


def tim_mot_tu_khoa(query: str, tmp: Path, ten_tien_to: str) -> dict | None:
    """Thử tìm 1 file THẬT khớp `query`. Trả record sẵn sàng ghi manifest, hoặc None nếu không có
    ứng viên nào chấm `muc == 2` (đúng hẳn — theo đúng luật của `soi_kho.cham`, không hạ tiêu
    chuẩn xuống `muc == 1` vì đó là mức 'nền trung tính', không phải 'đúng chủ đề').

    KHÔNG chặn ứng viên vì trùng ID với file khác — xem lý do ở docstring đầu file (mục "MỘT FILE
    VẬT LÝ..."). Việc chống ghi-đè-tên-file xử lý ở `main()`, lúc LƯU, không phải ở đây."""
    import soi_kho
    import stockfetch
    stockfetch._load_dotenv()
    from stock_sources import pexels

    try:
        ung_vien = pexels(query, SO_UNG_VIEN)
    except Exception as e:
        print(f"    ! Pexels lỗi cho '{query}': {type(e).__name__} {e}")
        return None
    for i, it in enumerate(ung_vien[:DUNG_TOI_DA]):
        try:
            goc, frame = _tai_va_luu_frame(it["url"], tmp, f"{ten_tien_to}_{i}")
        except Exception as e:
            print(f"    ! tải ứng viên #{i} lỗi: {type(e).__name__} {e}")
            continue
        if not frame or not frame.exists():
            continue
        try:
            d = soi_kho.cham(frame, query)
        except Exception as e:
            print(f"    ! chấm gemini-3.8-flash lỗi: {type(e).__name__} {e}")
            continue
        print(f"    ứng viên #{i} muc={d.get('muc')} thay='{d.get('thay', '')}'")
        if d.get("muc") == 2:
            return {**it, "query": query, "_file_tam": goc}
        goc.unlink(missing_ok=True)
        if frame != goc:
            frame.unlink(missing_ok=True)
    return None


def _ten_dich_duy_nhat(stock: Path, rec: dict, ext: str) -> Path:
    """Tên file đích trong `stock/`, KHÔNG BAO GIỜ trùng tên đang có (kể cả từ trước lượt chạy
    này) — trùng tên vật lý ép ta phải ghi đè hoặc bỏ dòng manifest, cả hai đều xoá mất thông tin
    của bên đang giữ tên đó trước. Thêm hậu tố `_b`, `_c`, … cho tới khi trống chỗ."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", f"{rec['src']}_{rec['id']}")[:60]
    dich = stock / f"{safe}{ext}"
    hau_to = iter("bcdefghijk")
    while dich.exists():
        dich = stock / f"{safe}_{next(hau_to)}{ext}"
    return dich


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--thu", action="store_true", help="chỉ thử + báo cáo, KHÔNG tải/KHÔNG sửa khop_hinh.json")
    a = ap.parse_args()

    slug = Path(a.slug)
    if not slug.is_absolute():
        slug = ROOT / "assets" / a.slug
    kh_f = slug / "khop_hinh.json"
    if not kh_f.exists():
        raise SystemExit(f"✗ không thấy {kh_f} — chạy B5K (khop_hinh.py) trước.")
    stock = slug / "stock"
    stock.mkdir(exist_ok=True)

    kh = json.loads(kh_f.read_text(encoding="utf-8"))
    doan_cu_the = [d for d in kh if d.get("loai") == "CU_THE" and d.get("query")]
    tu_khoa_doc_nhat = sorted({d["query"].strip() for d in doan_cu_the})
    print(f"=== {slug.name}: {len(doan_cu_the)} đoạn CU_THE · {len(tu_khoa_doc_nhat)} từ khoá "
          f"duy nhất ===")

    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="tim_anh_that_"))
    tim_duoc, khong_tim_duoc = {}, []
    man_f = stock / "manifest.jsonl"

    for i, q in enumerate(tu_khoa_doc_nhat, 1):
        print(f"[{i}/{len(tu_khoa_doc_nhat)}] {q}")
        rec = tim_mot_tu_khoa(q, tmp, ten_tien_to=f"q{i}")
        if rec:
            tim_duoc[q] = rec
            print(f"  ✓ tìm được thật: {rec.get('title', '')[:60]}")
        else:
            khong_tim_duoc.append(q)
            print("  · không có ứng viên nào chấm đúng — giữ CU_THE, để B5A vẽ AI")
        time.sleep(NGHI_GIUA_TU_KHOA)

    so_doan_giam = sum(1 for d in doan_cu_the if d["query"].strip() in tim_duoc)
    print(f"\n=== KẾT QUẢ: {len(tim_duoc)}/{len(tu_khoa_doc_nhat)} từ khoá tìm được thật "
          f"→ {so_doan_giam}/{len(doan_cu_the)} đoạn CHUYỂN sang dùng clip/ảnh thật ===")
    print(f"    còn lại {len(doan_cu_the) - so_doan_giam} đoạn vẫn cần vẽ AI (B5A)")

    if a.thu:
        print("\n(--thu) chưa tải file nào, chưa sửa khop_hinh.json. Bỏ --thu để áp dụng thật.")
        for _, r in tim_duoc.items():
            r["_file_tam"].unlink(missing_ok=True)
        return 0

    # --- sao lưu TRƯỚC khi sửa — cả 2 file bị đổi trong lượt chạy này ----------------------
    truoc = slug / "_truoc_khi_sua"
    truoc.mkdir(exist_ok=True)
    ts = time.strftime("%H%M%S")
    (truoc / f"khop_hinh.truoc_tim_anh_that_{ts}.json").write_text(
        kh_f.read_text(encoding="utf-8"), encoding="utf-8")
    if man_f.exists():
        (truoc / f"manifest.truoc_tim_anh_that_{ts}.jsonl").write_text(
            man_f.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"  (đã sao lưu vào {truoc}/*_{ts}.*)")

    # --- ghi file thật vào stock/ + manifest.jsonl -----------------------------------------
    dung = {"src", "id", "url", "title", "license", "credit", "query"}
    with man_f.open("a", encoding="utf-8") as mf:
        for q, rec in tim_duoc.items():
            tmp_file = rec.pop("_file_tam")
            dich = _ten_dich_duy_nhat(stock, rec, tmp_file.suffix)
            # `Path.replace()` = os.replace(), KHÔNG di chuyển được XUYÊN Ổ ĐĨA trên Windows (thư
            # mục tạm ở C:, thư mục tập ở E:) — đã dính thật. `shutil.move()` tự copy+xoá khi
            # khác ổ đĩa.
            shutil.move(str(tmp_file), str(dich))
            ghi = {k: rec[k] for k in dung if k in rec}
            ghi.update({"file": dich.name, "bytes": dich.stat().st_size})
            mf.write(json.dumps(ghi, ensure_ascii=False) + "\n")
            mf.flush()
            print(f"  ✓ lưu {dich.name} ({ghi['bytes']//1024} KB) query='{q}'")

    # --- đổi loai để B5A không vẽ AI cho các đoạn đã tìm được thật -------------------------
    doi = 0
    for d in kh:
        if d.get("loai") == "CU_THE" and d.get("query", "").strip() in tim_duoc:
            d["loai"] = "CU_THE_DA_TIM_DUOC"
            doi += 1
    kh_f.write_text(json.dumps(kh, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n✓ đã đổi {doi} đoạn trong khop_hinh.json (CU_THE → CU_THE_DA_TIM_DUOC)")

    bao_cao = slug / "tim_anh_that.json"
    bao_cao.write_text(json.dumps({
        "at": time.strftime("%Y-%m-%d %H:%M"),
        "tu_khoa_tim_duoc": {q: {"title": r.get("title"), "credit": r.get("credit"),
                                 "license": r.get("license")} for q, r in tim_duoc.items()},
        "tu_khoa_khong_tim_duoc": khong_tim_duoc,
        "doan_cu_the_truoc": len(doan_cu_the),
        "doan_cu_the_sau": len(doan_cu_the) - so_doan_giam,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ ghi báo cáo {bao_cao}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
