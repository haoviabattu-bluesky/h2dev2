# -*- coding: utf-8 -*-
"""soi_kho.py — CHẤM KHO TƯ LIỆU: clip có ĐÚNG là thứ từ khoá đã hứa không?

    py -3.13 soi_kho.py --stock <thư mục kho> [--n 0]

Ghi kết quả vào `soi_kho.json` trong chính thư mục kho, và cập nhật cột `hop` cho từng file.

VÌ SAO CẦN — CHỖ HỎNG NẰM TRƯỚC KHÂU GHÉP
------------------------------------------------------------------------------------------------
Chuỗi làm hình là: **từ khoá → clip → câu**. Đã nối xong khâu *clip → câu* (`khop_hinh.py`), nhưng
khâu *từ khoá → clip* thì chưa ai kiểm. Pexels là kho ảnh ĐỜI THƯỜNG: tìm thứ nó không có thì nó
vẫn trả về thứ gì đó, mình vẫn tải, vẫn ghi sổ, rồi ghép vào đúng câu — **khớp hoàn hảo với một
clip sai**.

Đo thật tập 3 (xem bằng mắt, 3 mẫu):
   `area 51 sign nevada`          → bến xe buýt thành phố ban ngày
   `national laboratory building` → chung cư cũ vùng nhiệt đới, có cây cọ
   `warehouse industrial facility`→ kho vận có xe tải  ✓ (đúng)

Nên phải chấm cả kho TRƯỚC khi quyết định sinh ảnh AI: biết chính xác bao nhiêu phần trăm kho dùng
được thì mới biết cần vẽ thêm bao nhiêu, thay vì đoán.

CHẤM THẾ NÀO
  Mỗi clip lấy 1 khung ở giữa, hỏi model vision đúng một câu: "ảnh này có thể hiện <từ khoá> không"
  và trả về mức 0–2 (0 = lạc hẳn · 1 = tạm, liên quan xa · 2 = đúng). Ảnh tĩnh thì chấm thẳng.
  Kèm mô tả ngắn để người đọc tự đối chiếu, không phải tin số suông.
"""
import argparse
import base64
import itertools
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
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

from assemble import FF

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
STILL_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def khung_giua(p: Path, tmp: Path) -> Path | None:
    """1 khung ở GIỮA clip — đầu/đuôi hay là thẻ tiêu đề hoặc cảnh chuyển."""
    out = tmp / (p.stem + ".jpg")
    r = subprocess.run([FF, "-i", str(p)], capture_output=True, text=True).stderr
    import re
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", r)
    giay = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 4.0
    subprocess.run([FF, "-y", "-ss", f"{giay/2:.2f}", "-i", str(p), "-vframes", "1",
                    "-vf", "scale=640:-2", str(out)], capture_output=True)
    return out if out.exists() else None


def cham(anh: Path, tu_khoa: str):
    """Chấm MỘT file kho so với từ khoá đã dùng để tải nó về.

    ⚠️ THANG CHẤM ĐẦU TIÊN CỦA FILE NÀY ĐÃ HỎNG — ĐỪNG QUAY LẠI KIỂU ĐÓ.
    Bản cũ hỏi thẳng "ảnh này có thể hiện từ khoá không" kèm 3 bậc tả bằng tính từ ("đúng" /
    "liên quan xa" / "lạc hẳn"). Kết quả lưu trong `soi_kho.json` của tập 3: **243/248 file rơi
    vào đúng một bậc giữa**, 5 file bậc 0, 0 file bậc 2. Một thang mà mọi thứ ra cùng một bậc thì
    không đo gì cả — và tệ hơn, nó trông y hệt một kết quả thật, nên con số "42% kho dùng được"
    rút ra từ đó đã bị đem đi báo cáo.
    Cách chữa giống hệt `qc_canh.py`: bắt model **tả trước, kết luận sau**, rồi tự mình ép luật ở
    phía code chứ không tin model giữ luật. Hỏi cảm giác thì model chọn bậc an toàn; bắt nó chỉ
    vào thứ nó nhìn thấy thì nó buộc phải phân biệt.
    """
    import qc_character as qcc
    hoi = ("Bạn đang kiểm tra tư liệu hình cho một video TÀI LIỆU tiếng Nhật (đề tài quân sự, bí "
           "mật, điều tra).\n"
           f'Từ khoá đã dùng để tải hình này về là: "{tu_khoa}".\n\n'
           "BƯỚC 1 — `thay`: tả CHỦ THỂ CHÍNH trong ảnh, tối đa 8 từ tiếng Việt. Tả thứ thật sự "
           "nhìn thấy, đừng tả thứ bạn đoán từ từ khoá.\n"
           "BƯỚC 2 — `co_chu_de`: chủ thể chính vừa tả có ĐÚNG là thứ mà từ khoá gọi tên không? "
           "(true/false). Từ khoá nói 'area 51 sign' mà ảnh là biển 'Welcome to Las Vegas' → "
           "false. Từ khoá nói 'university campus' mà ảnh là một khuôn viên đại học bất kỳ → "
           "true.\n"
           "BƯỚC 3 — `muc`:\n"
           "· 2 = `co_chu_de` true.\n"
           "· 1 = `co_chu_de` false, nhưng ảnh là cảnh nền trung tính hợp tông phim tài liệu "
           "(bầu trời, sa mạc, đường vắng, mây, biển, đêm tối, tư liệu cũ) — vẫn chèn làm nền "
           "được.\n"
           "· 0 = `co_chu_de` false VÀ ảnh mang không khí đi ngược đề tài: du lịch, sinh hoạt đời "
           "thường, văn phòng hiện đại, trẻ em, thể thao, quảng cáo, thiên nhiên vui tươi, người "
           "lạ làm việc riêng.\n"
           "LUẬT CỨNG: `co_chu_de` false thì TUYỆT ĐỐI KHÔNG được chấm 2.\n\n"
           "`chu_la` = trong ảnh có chữ/biển hiệu/logo/thương hiệu ĐỌC ĐƯỢC mà không phải tiếng "
           "Nhật không (tên sòng bạc, tên hãng bay, biển quảng cáo, chữ Trung/Hàn…).\n\n"
           'Trả DUY NHẤT JSON: {"thay":"<…>","co_chu_de":true|false,"muc":0|1|2,'
           '"chu_la":true|false}')
    b64 = base64.b64encode(anh.read_bytes()).decode()
    d = qcc._parse_json(qcc._chat("gemini-3.8-flash", hoi, b64))
    if d.get("muc") == 2 and not d.get("co_chu_de"):
        d["muc"] = 1
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stock", required=True)
    ap.add_argument("--n", type=int, default=0, help="chỉ chấm N file đầu (0 = tất cả)")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--lam-lai", action="store_true",
                    help="chấm lại TOÀN BỘ kho (mặc định chỉ chấm file mới). ⚠️ xoá luôn lệnh "
                         "cấm mà qc_canh.py đã ghi thêm qua các vòng dựng")
    a = ap.parse_args()

    kho = Path(a.stock)
    man = {}
    f = kho / "manifest.jsonl"
    for l in f.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            if r.get("file") and r.get("query"):
                man[r["file"]] = r["query"]
    ds = [(kho / k, q) for k, q in man.items()
          if (kho / k).exists() and (kho / k).suffix.lower() in VIDEO_EXT | STILL_EXT]
    # CHẠY BÙ: file đã chấm rồi thì thôi. B5 gọi lại file này sau mỗi lượt tải, mà kho tập 3 có
    # 248 file — chấm lại toàn bộ mỗi lần là trả tiền cho thứ đã biết câu trả lời. Quan trọng hơn:
    # danh sách cấm do QC bản dựng ghi thêm (`qc_canh --cam-file-lac`) cũng nằm trong file này,
    # chấm đè lên là XOÁ MẤT lệnh cấm đã học được qua nhiều vòng.
    cu, f_ra = [], kho / "soi_kho.json"
    if f_ra.exists() and not a.lam_lai:
        try:
            cu = json.loads(f_ra.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! soi_kho.json hỏng ({type(e).__name__}) → chấm lại từ đầu")
    da_co = {x["file"] for x in cu}
    bo_qua = sum(1 for p, _ in ds if p.name in da_co)
    ds = [(p, q) for p, q in ds if p.name not in da_co]
    if a.n:
        ds = ds[:a.n]
    print(f"chấm {len(ds)} file mới"
          + (f" (bỏ qua {bo_qua} file đã chấm · muốn chấm lại tất: --lam-lai)" if bo_qua else ""))
    if not ds:
        print("  → kho không có file mới, giữ nguyên soi_kho.json")
        return
    tmp = Path(tempfile.mkdtemp(prefix="soikho_"))

    def mot(x):
        p, q = x
        try:
            anh = p if p.suffix.lower() in STILL_EXT else khung_giua(p, tmp)
            if not anh:
                return {"file": p.name, "query": q, "muc": None, "ta": "không lấy được khung"}
            kq = cham(anh, q)
            return {"file": p.name, "query": q, "muc": kq.get("muc"),
                    "co_chu_de": kq.get("co_chu_de"), "chu_la": kq.get("chu_la"),
                    "ta": kq.get("thay", "")}
        except Exception as e:
            return {"file": p.name, "query": q, "muc": None, "ta": f"lỗi: {type(e).__name__}"}

    ra = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for i, kq in enumerate(ex.map(mot, ds), 1):
            ra.append(kq)
            if i % 20 == 0:
                print(f"  {i}/{len(ds)}")
    ra = cu + ra
    f_ra.write_text(json.dumps(ra, ensure_ascii=False, indent=1), encoding="utf-8")
    import collections
    c = collections.Counter(x["muc"] for x in ra)
    n = sum(c[m] for m in (0, 1, 2)) or 1
    print(f"\nKẾT QUẢ: đúng(2)={c.get(2,0)} ({c.get(2,0)/n*100:.0f}%) · "
          f"tạm(1)={c.get(1,0)} ({c.get(1,0)/n*100:.0f}%) · "
          f"LẠC(0)={c.get(0,0)} ({c.get(0,0)/n*100:.0f}%) · không chấm được={c.get(None,0)}")
    chu = [x for x in ra if x.get("chu_la")]
    print(f"  có chữ/logo lạ: {len(chu)} file")
    xau = sorted((x for x in ra if x["muc"] == 0), key=lambda x: x["query"])
    if xau:
        print(f"\n{len(xau)} FILE BỊ CẤM (nap_kho sẽ bỏ qua từ nay):")
        for q, g in itertools.groupby(xau, key=lambda x: x["query"]):
            g = list(g)
            print(f"  {len(g):3d}× \"{q}\" → {g[0]['ta'][:44]}")
    print(f"→ {kho / 'soi_kho.json'}")


if __name__ == "__main__":
    main()
