# -*- coding: utf-8 -*-
"""qc_canh.py — SOI TỪNG CẢNH của bản đã dựng: hình có ăn với lời đang đọc không?

    py -3.13 qc_canh.py --video <mp4> --scenes <scenes.json> --srt <voice.srt> [--vi <voice.vi.srt>]

Ghi `qc_canh.json` cạnh video + in bảng tổng kết.

KHÁC GÌ `qc_visual.qc_video()` — VÀ VÌ SAO PHẢI CÓ CẢ HAI
------------------------------------------------------------------------------------------------
`qc_video()` lấy **8 mốc** rải đều rồi hỏi hình có ăn lời không. Nó trả lời được câu "video này có
hỏng toàn tập không", KHÔNG trả lời được câu "cảnh nào hỏng". Tập 3 đã qua B8Q sạch rồi vẫn bị chủ
dự án xem ra hình một đằng lời một nẻo — vì 8 mốc trong 400 cảnh là 2%, và xác suất 8 mốc đều rơi
vào cảnh đúng trong một video hỏng 40% là ~1,7%… mà nó đã rơi trúng thật.
File này soi **100% số cảnh**. Đắt hơn, nhưng đây là thứ người xem thật sự nhìn thấy.

Và rubric ở đây là rubric PHIM TÀI LIỆU, không phải rubric chuyện kể ngôi thứ nhất của
`qc_video()` (bên đó cho phép "quay bà đang kể trong lúc bà nói về con cái" — lane này không có
người kể xuất hiện trên hình, chấp nhận kiểu đó là tự bịt mắt mình).

BA THỨ HỎI CÙNG LÚC, VÌ CÙNG MỘT KHUNG HÌNH ĐÃ TRẢ TIỀN RỒI
  · `muc`     0/1/2 — hình có thuộc về khoảnh khắc này của câu chuyện không.
  · `chu_la`  khung có chữ/logo/thương hiệu lạ không (đã dính thật: máy bay Emirates, biển
              AIR NEW ZEALAND, biểu đồ NOAA tiếng Anh lọt vào b-roll tài liệu tiếng Nhật).
  · `xau`     hình vỡ/nhoè/tối/khung đen — chất lượng kỹ thuật.
"""
import argparse
import base64
import collections
import json
import os
import re
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


def doc_srt(f: Path):
    """[(t0, t1, lời)] — đọc thẳng, không phụ thuộc module khác."""
    ra = []
    for khoi in re.split(r"\n\s*\n", f.read_text(encoding="utf-8").strip()):
        d = [x for x in khoi.splitlines() if x.strip()]
        if len(d) < 2 or "-->" not in d[1]:
            continue
        a, b = d[1].split("-->")

        def _s(x):
            h, m, s = x.strip().replace(",", ".").split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
        ra.append((_s(a), _s(b), " ".join(d[2:]).strip()))
    return ra


def loi_trong(cues, t0, t1):
    """Lời đọc PHỦ LÊN khoảng cảnh. Cảnh 4,3 giây thường nằm gọn trong 1–2 cue."""
    x = [c[2] for c in cues if c[0] < t1 and c[1] > t0]
    return " ".join(x).strip()


def khung(video: Path, t: float, ra: Path, ff: str):
    subprocess.run([ff, "-y", "-ss", f"{t:.2f}", "-i", str(video), "-vframes", "1",
                    "-vf", "scale=640:-2", str(ra)], capture_output=True)
    if not ra.exists():
        return None
    # Tăng sáng nếu frame tối để tránh hallucination "màn hình xám trơn" của Gemini.
    # Frame tối (mean luma < 50/255) khiến model không nhận ra nội dung dù ảnh thật sự có.
    try:
        from PIL import Image, ImageEnhance
        import numpy as np
        img = Image.open(ra).convert("RGB")
        luma = np.array(img).mean()
        if luma < 50:
            img = ImageEnhance.Brightness(img).enhance(3.0)
            img.save(ra)
    except Exception:
        pass  # nếu PIL/numpy thiếu thì bỏ qua, vẫn gửi frame gốc
    return ra


SCHEMA = ('{"khop_voi":"<từ/cụm trong câu mà hình cho thấy, hoặc \\"\\" nếu không có>",'
          '"muc":0|1|2,"chu_la":true|false,"xau":true|false,'
          '"ta":"<mô tả hình, tối đa 10 từ tiếng Việt>"}')


def cham(anh: Path, loi: str):
    """Chấm MỘT khung hình so với lời đang đọc.

    ⚠️ THANG CHẤM PHẢI BẮT MODEL CHỈ RA BẰNG CHỨNG, KHÔNG HỎI CẢM GIÁC.
    Bản đầu hỏi thẳng "hình có thuộc về khoảnh khắc này không" với 3 bậc mô tả bằng tính từ
    ("đúng" / "chung chung" / "khác hẳn") → 140/141 cảnh rơi vào bậc giữa, kể cả 24 cảnh ảnh TỰ VẼ
    từ chính câu đó. Một thang mà mọi thứ đều ra cùng một bậc thì không đo gì cả — y hệt lần đầu
    làm `soi_kho.py` (0/248 cảnh được chấm bậc cao nhất).
    Cách chữa: bắt model điền `khop_voi` — TỪ NÀO trong câu ứng với thứ nhìn thấy trên hình — rồi
    mới cho chấm. Không nêu được từ nào thì cấm chấm bậc 2. Bắt chỉ vào bằng chứng thì model buộc
    phải phân biệt, thay vì chọn bậc giữa cho an toàn.
    """
    import qc_character as qcc
    hoi = ("Đây là một khung hình của video TÀI LIỆU tiếng Nhật. Trong lúc khung hình này hiện "
           "trên màn, người dẫn đang đọc câu dưới đây.\n\n"
           f"LỜI ĐANG ĐỌC: {loi[:400]}\n\n"
           "BƯỚC 1 — `khop_voi`: trong câu trên, có từ/cụm nào chỉ một NƠI CHỐN, VẬT THỂ, CƠ SỞ, "
           "THIẾT BỊ, TÀI LIỆU, HÀNH ĐỘNG hay KHUNG CẢNH mà bạn ĐANG NHÌN THẤY trên hình không? "
           "Có thì chép đúng cụm đó ra (tiếng Nhật, nguyên văn). Không có thì để chuỗi rỗng.\n"
           "Tính là thấy kể cả khi hình là hình minh hoạ/dựng lại, miễn nó thể hiện đúng thứ đó "
           "(vd câu nói 'hầm ngầm' mà hình là một hầm ngầm → khớp; câu nói 'sa mạc Nevada' mà "
           "hình là sa mạc khô cằn có núi → khớp).\n\n"
           "BƯỚC 2 — `muc`:\n"
           "· 2 = `khop_voi` KHÔNG rỗng — hình cho thấy đúng thứ câu đang nói tới.\n"
           "· 1 = `khop_voi` rỗng, nhưng hình là cảnh nền trung tính hợp tông (bầu trời, sa mạc, "
           "đường vắng, mây, tư liệu mờ) — đặt vào không ai thấy sai.\n"
           "· 0 = hình cho thấy một nơi/vật/bối cảnh ĐI NGƯỢC với câu: sinh hoạt đời thường, "
           "du lịch, văn phòng hiện đại, trẻ em, thể thao, quảng cáo, thiên nhiên vui tươi… "
           "trong lúc lời đang kể chuyện quân sự/bí mật/điều tra.\n"
           "LUẬT CỨNG: `khop_voi` rỗng thì TUYỆT ĐỐI KHÔNG được chấm 2.\n"
           "Lane này KHÔNG có người dẫn xuất hiện trên hình — cảnh người lạ sinh hoạt đời thường "
           "là 0, không phải 1.\n\n"
           "chu_la = trong khung có chữ/biển hiệu/logo/thương hiệu ngoài tiếng Nhật ĐỌC ĐƯỢC "
           "không (nhãn 「イメージ」 của chính mình thì KHÔNG tính; chữ mờ không đọc ra cũng không "
           "tính).\n"
           "xau = hình vỡ, nhoè nặng, tối đen, hay lỗi kỹ thuật thấy rõ.\n\n"
           f"Trả DUY NHẤT JSON: {SCHEMA}")
    b64 = base64.b64encode(anh.read_bytes()).decode()
    d = qcc._parse_json(qcc._chat("gemini-3.8-flash", hoi, b64))
    # Nếu model vẫn hallucinate "xám trơn" dù đã tăng sáng trong khung(), thử tăng thêm 5× rồi hỏi lại.
    # Chỉ retry đúng 1 lần — nếu lần 2 vẫn "xám" thì tin kết quả lần 2 (không loop vô tận).
    _HAL = {"xám trơn", "màn hình", "màu xám", "không có nội dung"}
    if any(kw in (d.get("ta") or "") for kw in _HAL):
        try:
            from PIL import Image, ImageEnhance
            img = Image.open(anh).convert("RGB")
            img = ImageEnhance.Brightness(img).enhance(5.0)
            img.save(anh)
            b64 = base64.b64encode(anh.read_bytes()).decode()
            d = qcc._parse_json(qcc._chat("gemini-3.8-flash", hoi, b64))
        except Exception:
            pass
    # Ép luật cứng ở PHÍA MÌNH chứ không tin model tự giữ: nêu không được từ nào mà vẫn chấm 2 thì
    # hạ xuống 1. Luật viết trong prompt là lời nhắc, không phải hàng rào.
    if d.get("muc") == 2 and not (d.get("khop_voi") or "").strip():
        d["muc"] = 1
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--scenes", default="", help="scenes*.json (mặc định cạnh video)")
    ap.add_argument("--srt", default="", help="phụ đề gốc để lấy lời đang đọc")
    ap.add_argument("--vi", default="", help="phụ đề Việt — chỉ để IN ra cho người đọc báo cáo")
    ap.add_argument("--cam-file-lac", default="",
                    help="thư mục kho: ghi vào soi_kho.json lệnh cấm những file ĐÃ CHỨNG MINH là "
                         "lạc trên bản dựng (lạc ≥1 lần và chưa từng đúng)")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--n", type=int, default=0, help="chỉ chấm N cảnh đầu (0 = tất cả)")
    a = ap.parse_args()

    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    video = Path(a.video)
    thu_muc = video.parent
    sc_f = Path(a.scenes) if a.scenes else thu_muc / "scenes.json"
    ke_hoach = json.loads(sc_f.read_text(encoding="utf-8"))
    srt_f = Path(a.srt) if a.srt else next(
        (thu_muc / t for t in ("voice_paced.srt", "voice.srt") if (thu_muc / t).exists()), None)
    cues = doc_srt(srt_f) if srt_f else []
    cues_vi = doc_srt(Path(a.vi)) if a.vi and Path(a.vi).exists() else []
    if a.n:
        ke_hoach = ke_hoach[:a.n]
    print(f"soi {len(ke_hoach)} cảnh · {video.name} · lời từ {srt_f.name if srt_f else '—'}")
    tmp = Path(tempfile.mkdtemp(prefix="qccanh_"))

    def mot(i):
        c = ke_hoach[i]
        t0, dur = float(c["t0"]), float(c["dur"])
        giua = t0 + dur / 2
        base = {"i": i, "t0": round(t0, 1), "file": c.get("file", ""),
                "anh_ai": bool(c.get("anh_ai")), "bangchung": bool(c.get("bangchung")),
                "query": c.get("query", "")}
        loi = loi_trong(cues, t0, t0 + dur)
        base["loi"] = loi[:80]
        if cues_vi:
            base["loi_vi"] = loi_trong(cues_vi, t0, t0 + dur)[:90]
        if not loi:
            return {**base, "muc": None, "ta": "không có lời ở mốc này"}
        f = khung(video, giua, tmp / f"f{i:05d}.jpg", ff)
        if not f:
            return {**base, "muc": None, "ta": "không trích được khung"}
        try:
            d = cham(f, loi)
        except Exception as e:
            return {**base, "muc": None, "loi_ha_tang": f"{type(e).__name__}: {e}"}
        return {**base, "muc": d.get("muc"), "khop_voi": d.get("khop_voi", ""),
                "chu_la": d.get("chu_la"), "xau": d.get("xau"), "ta": d.get("ta", "")}

    ra = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for n, kq in enumerate(ex.map(mot, range(len(ke_hoach))), 1):
            ra.append(kq)
            if n % 20 == 0:
                print(f"  {n}/{len(ke_hoach)}", end="\r", flush=True)
    (thu_muc / "qc_canh.json").write_text(json.dumps(ra, ensure_ascii=False, indent=1),
                                          encoding="utf-8")

    # ⚠️ Lỗi HẠ TẦNG phải đếm riêng. Gộp nó vào "không có lỗi nội dung" là đúng cái bẫy 503 đã
    # dính ở dự án thẻ: 62/62 ảnh không hề được chấm mà báo cáo vẫn ghi "QC FAIL: 0".
    ha_tang = [x for x in ra if x.get("loi_ha_tang")]
    cham_duoc = [x for x in ra if x.get("muc") is not None]
    c = collections.Counter(x["muc"] for x in cham_duoc)
    n = len(cham_duoc) or 1
    print(f"\n{'='*74}\nCHẤM ĐƯỢC {len(cham_duoc)}/{len(ra)} cảnh"
          + (f"  ·  ⚠️ {len(ha_tang)} cảnh LỖI HẠ TẦNG (không tính là đạt)" if ha_tang else ""))
    print(f"  đúng (2) : {c.get(2,0):3d}  ({c.get(2,0)/n*100:.0f}%)")
    print(f"  tạm  (1) : {c.get(1,0):3d}  ({c.get(1,0)/n*100:.0f}%)")
    print(f"  LẠC  (0) : {c.get(0,0):3d}  ({c.get(0,0)/n*100:.0f}%)")
    for ten, loc in (("ảnh tự vẽ", lambda x: x["anh_ai"]),
                     ("ảnh bằng chứng", lambda x: x["bangchung"]),
                     ("clip stock", lambda x: not x["anh_ai"] and not x["bangchung"])):
        g = [x for x in cham_duoc if loc(x)]
        if g:
            cc = collections.Counter(x["muc"] for x in g)
            print(f"    · {ten:16s} {len(g):3d} cảnh → đúng {cc.get(2,0)} · tạm {cc.get(1,0)} "
                  f"· LẠC {cc.get(0,0)}")
    chu = [x for x in ra if x.get("chu_la")]
    xau = [x for x in ra if x.get("xau")]
    print(f"  chữ/logo lạ: {len(chu)} cảnh  ·  hình xấu/lỗi: {len(xau)} cảnh")
    lac = sorted([x for x in cham_duoc if x["muc"] == 0], key=lambda x: x["t0"])
    if lac:
        print(f"\n{len(lac)} CẢNH LẠC — sửa theo danh sách này:")
        for x in lac[:40]:
            print(f"  {x['t0']:7.1f}s  {x['file'][:34]:34s} │ {x['ta'][:30]:30s} │ "
                  f"{(x.get('loi_vi') or x['loi'])[:52]}")
    if a.cam_file_lac:
        cam_them(Path(a.cam_file_lac), cham_duoc)
    print(f"\n→ {thu_muc / 'qc_canh.json'}")
    return 1 if (c.get(0, 0) or ha_tang) else 0


def cam_them(kho: Path, cham_duoc):
    """Đưa file đã chứng minh là lạc vào danh sách cấm của kho (`soi_kho.json`).

    `soi_kho.py` chấm file so với TỪ KHOÁ đã tải nó về — nên một clip "phụ nữ gõ máy tính văn
    phòng" tải bằng từ khoá `1980s office typewriter desk` được chấm ĐÚNG, hoàn toàn hợp lý, rồi
    vẫn rơi vào giữa đoạn kể vụ bắt giữ năm 1990. Cái sai nằm ở TỪ KHOÁ, mà `soi_kho` không có
    cách nào biết. Chỉ bản dựng thật mới lộ ra.
    Nên chốt vòng phản hồi: thứ QC bản dựng đã bắt tận tay thì cấm luôn ở kho, lần dựng sau không
    bốc lại. Cấm dè dặt — **lạc ít nhất một lần VÀ chưa từng được chấm đúng lần nào** — để không
    loại oan clip chỉ bị đặt nhầm chỗ.
    """
    f = kho / "soi_kho.json"
    ds = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    da_cam = {x["file"] for x in ds if x.get("muc") == 0}
    diem = collections.defaultdict(set)
    for x in cham_duoc:
        if x["file"] and not x["anh_ai"] and not x["bangchung"]:
            diem[x["file"]].add(x["muc"])
    moi = sorted(fn for fn, d in diem.items() if 0 in d and 2 not in d and fn not in da_cam)
    if not moi:
        print("\n  (không có file nào mới đủ điều kiện cấm)")
        return
    ta = {x["file"]: x.get("ta", "") for x in cham_duoc if x["muc"] == 0}
    ds += [{"file": fn, "query": "", "muc": 0, "co_chu_de": False,
            "ta": f"[QC bản dựng] {ta.get(fn, '')}"[:70]} for fn in moi]
    f.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  🚫 CẤM THÊM {len(moi)} file (tổng cấm {len(da_cam)+len(moi)}) → {f.name}")
    for fn in moi:
        print(f"     {fn[:38]:38s} {ta.get(fn, '')[:34]}")


if __name__ == "__main__":
    raise SystemExit(main())
