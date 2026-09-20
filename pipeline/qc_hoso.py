# -*- coding: utf-8 -*-
"""qc_hoso.py — CỔNG B0: NGHIỆM THU HỒ SƠ ĐỀ TÀI do dự án research giao sang.

Chạy TRƯỚC khi sản xuất, trên thư mục bàn giao (`_READY/<nn>-<slug>/`) hoặc trên thư mục tập.

    py -3.13 qc_hoso.py --folder "E:\\...\\SPACE_RESEARCH\\output\\_READY\\01-valentich" \
                        --profile toshi-densetsu-jp

VÌ SAO CẦN CỔNG NÀY — bài học đắt nhất của hợp đồng hai bên
------------------------------------------------------------------------------------------------
Dự án đã CÓ hợp đồng bằng chữ từ đầu (`docs/KHUON_HO_SO_DE_TAI.md`), và hồ sơ đầu tiên vẫn sai 6
chỗ. Sai không phải vì bên kia ẩu — mà vì **không có gì kiểm hợp đồng đó**, nên mọi sai lệch chỉ
lộ ra sau khi đã tiêu tiền:

  · tiêu đề 47 ký tự  → chỉ biết ở B10, tức là sau khi đã trả tiền giọng đọc + dựng xong video
  · competitor 8,5'   → không ai biết, kịch bản 28' cứ thế viết theo nhịp video ngắn
  · 20 từ khoá không hàng → biết sau 24 phút tải về 0 file dùng được
  · tư liệu nói nửa chừng → biết ở B3F, sau khi đã đốt một lượt sinh kịch bản

Tệ hơn: **khuôn của CHÍNH DỰ ÁN NÀY dạy sai một chỗ.** `KHUON_HO_SO_DE_TAI.md` ghi mẫu
"TIÊU ĐỀ ĐÃ CHỐT (không đổi):" — bên research làm ĐÚNG mẫu, và mẫu đó chặn luôn quyền chỉnh tiêu
đề của bên làm video. Hợp đồng bằng chữ mà không có cổng thì lỗi của chính hợp đồng cũng không ai
phát hiện.

Nguyên tắc: **cổng phải chạy chính đoạn code mà khâu sản xuất sẽ chạy.** Phần kiểm kho tư liệu ở
đây gọi thẳng `stock_cut.nap_kho()` + `suc_chua()` — đúng hai hàm B5/B8 dùng — nên "kho đủ" ở B0
có nghĩa đúng là "B8 dựng được", không phải một phép đếm gần đúng viết riêng cho cổng.

Mọi ngưỡng lấy từ profile (khối `research` + `script.gate` + `body`). Lane nào không khai
`research` thì lane đó không nhận hàng nghiên cứu — cổng báo và thoát êm.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def _ensure_std():
    """xem publish_kit.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
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

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Ngưỡng mặc định khi profile không khai — cố ý RỘNG, để cổng không tự bịa ra luật riêng.
MAC_DINH = {
    "files_required": ["series_ctx.txt", "competitor.txt", "stock_queries.txt"],
    "competitor_ratio": [0.85, 1.30],   # nhân với script.target_minutes
    "title_options_min": 1,
    "source_coverage_min": 0.90,
    "stock_queries_min": 12,
    "stock_by_chapter": False,
    "deliver_stock": False,
    "deliver_evidence": False,
    "evidence_min": 0,
    "evidence_dir": "stock",
    "blocks_required": [],
}


def _ra(kq, sev, ma, noi, goi_y=""):
    kq.append({"sev": sev, "ma": ma, "noi": noi, "goi_y": goi_y})


# ------------------------------------------------------------------ tiêu đề
# Bên research có thể viết "TIÊU ĐỀ ĐÃ CHỐT", "TIÊU ĐỀ — 3 PHƯƠNG ÁN", hoặc đánh số ①②③.
# Bóc mọi dòng nằm dưới tiêu mục cho tới dòng trống đầu tiên, rồi gọt phần chú thích đuôi.
_DAU_MUC = re.compile(r"^\s*[①②③④⑤\d]+[\.\)、]?\s*")
_CHU_THICH_DUOI = re.compile(r"[（(][^）)]*ký tự[^）)]*[）)]\s*$")


def boc_tieu_de(text: str) -> list[str]:
    ra, dang_doc = [], False
    for dong in text.splitlines():
        if re.match(r"^\s*TIÊU ĐỀ", dong):
            dang_doc = True
            continue
        if dang_doc:
            if not dong.strip():
                break
            if dong.strip().startswith(("→", "->", "＊", "*", "#")):
                continue          # dòng ghi chú của bên kia, không phải phương án
            t = _CHU_THICH_DUOI.sub("", _DAU_MUC.sub("", dong)).strip()
            if t:
                ra.append(t)
    return ra


def kiem_tieu_de(kq, ctx_text, rs, gate):
    ds = boc_tieu_de(ctx_text)
    lo, hi = (gate.get("title_len") or [1, 100])[:2]
    can = int(rs["title_options_min"])
    if not ds:
        _ra(kq, "nang", "tieu_de_khong_thay",
            "không tìm thấy dòng tiêu đề nào dưới tiêu mục 'TIÊU ĐỀ'",
            "hồ sơ phải có tiêu mục TIÊU ĐỀ, mỗi phương án một dòng")
        return
    hop = [t for t in ds if lo <= len(t) <= hi and len(t) <= 100]
    for t in ds:
        if len(t) > 100:
            _ra(kq, "nang", "tieu_de_qua_100", f"{len(t)} ký tự (YouTube cắt ở 100): {t[:40]}…")
    if not hop:
        _ra(kq, "nang", "tieu_de_ngoai_dai",
            f"{len(ds)} phương án, KHÔNG cái nào nằm trong dải {lo}–{hi} ký tự "
            f"(đo được: {[len(t) for t in ds]})",
            "đo thật kênh đối thủ: lệch dải này thì view thấp hơn 2,4 lần")
    elif len(hop) < can:
        _ra(kq, "nhe", "tieu_de_it_phuong_an",
            f"chỉ {len(hop)}/{can} phương án hợp lệ trong dải {lo}–{hi}")
    if re.search(r"TIÊU ĐỀ ĐÃ CHỐT|không đổi", ctx_text):
        _ra(kq, "nhe", "tieu_de_khoa_cung",
            "hồ sơ ghi 'ĐÃ CHỐT / không đổi'",
            "quyền chốt tiêu đề thuộc bên làm video vì còn phải khớp thumbnail — "
            "xin bên research đưa phương án, đừng khoá")
    return ds, hop


# ------------------------------------------------------------------ khung kể
def kiem_competitor(kq, folder: Path, prof, rs):
    f = folder / "competitor.txt"
    if not f.exists():
        return
    chars = len(re.sub(r"\s", "", f.read_text(encoding="utf-8", errors="replace")))
    rate = float((prof.get("voice") or {}).get("char_rate") or 0)
    muc_tieu = float((prof.get("script") or {}).get("target_minutes") or 0)
    if not rate or not muc_tieu:
        return
    phut = chars / rate
    lo, hi = [muc_tieu * r for r in rs["competitor_ratio"]]
    if lo <= phut <= hi:
        return
    # Lane có KHUNG NHỊP CHUNG đủ dài thì bản ngắn không còn là lỗi chặn: make_video sẽ mượn
    # khung chung, còn bản ngắn cùng đề tài vẫn có ích làm tham khảo nội dung. Nhịp là thuộc
    # tính của ĐỊNH DẠNG KÊNH, không phải của đề tài — bắt tìm lại bản dài cho từng tập là đặt
    # ra một việc vừa khó vừa vô ích (đề tài hiếm thì chỉ có bản 8–10 phút mà thôi).
    chung = ROOT / prof.get("slug_dir", "assets") / "_khung_nhip.txt"
    co_chung = chung.exists() and \
        len(re.sub(r"\s", "", chung.read_text(encoding="utf-8", errors="replace"))) / rate >= lo
    _ra(kq, "nhe" if co_chung else "nang", "khung_ke_lech_do_dai",
        f"competitor.txt ≈ {phut:.1f}′ ({chars:,} chữ) — cần {lo:.0f}–{hi:.0f}′ "
        f"cho video mục tiêu {muc_tieu:.0f}′"
        + (f" · lane CÓ khung nhịp chung ({chung.name}) nên không chặn" if co_chung else ""),
        "file này dạy NHỊP. Đưa bản ngắn thì model dựng nhịp video ngắn rồi kéo dài ra "
        "— mất mốc chương, mất nhịp lật. Bản cùng đề tài nhưng ngắn để ở "
        "competitor_cung_de_tai.txt")


# ------------------------------------------------------------------ tư liệu
def kiem_tu_lieu(kq, folder: Path, rs, gate):
    ctx = folder / "series_ctx.txt"
    if not ctx.exists():
        return
    text = ctx.read_text(encoding="utf-8", errors="replace")

    for khoi in rs["blocks_required"]:
        if khoi not in text:
            _ra(kq, "nang", "thieu_khoi_bat_buoc", f"tư liệu không có khối 「{khoi}」",
                "thiếu khối này thì chương tương ứng không có nguyên liệu, model tự bịa vào")

    moc = gate.get("chapter_markers") or []
    thieu = [m for m in moc if m not in text]
    if thieu:
        _ra(kq, "nang", "khung_chuong_khong_du",
            f"khung chương thiếu: {' '.join(thieu)}",
            "khung N chương phải ghi đủ trong hồ sơ, pipeline không tự nghĩ ra")

    try:
        import qc_facts
        _, co, tong = qc_facts.tu_lieu_thieu_nguon(text)
    except Exception as e:                      # cổng hỏng thì phải NÓI, không im lặng cho qua
        _ra(kq, "nhe", "khong_do_duoc_nguon", f"không đo được độ phủ nguồn: {e}")
        return
    if tong:
        ty = co / tong
        if ty < rs["source_coverage_min"]:
            _ra(kq, "nang", "tu_lieu_thieu_nguon",
                f"chỉ {co}/{tong} khối dữ kiện có 〔出典〕 ({ty:.0%}, "
                f"cần ≥{rs['source_coverage_min']:.0%})",
                "khối không nguồn = không truy ngược được khi bị khiếu nại")
        else:
            print(f"  · độ phủ nguồn tư liệu: {co}/{tong} ({ty:.0%})")


# ------------------------------------------------------------------ từ khoá hình
def kiem_stock_queries(kq, folder: Path, rs, gate):
    f = folder / "stock_queries.txt"
    if not f.exists():
        return
    dong = f.read_text(encoding="utf-8", errors="replace").splitlines()
    tu = [d.strip() for d in dong if d.strip() and not d.strip().startswith("#")]
    nhom = [d for d in dong if d.strip().startswith("#") and len(d.strip()) > 3]
    if len(tu) < rs["stock_queries_min"]:
        _ra(kq, "nang", "it_tu_khoa_hinh",
            f"{len(tu)} từ khoá, cần ≥{rs['stock_queries_min']}")
    if rs["stock_by_chapter"]:
        can = len(gate.get("chapter_markers") or []) or 5
        if len(nhom) < can:
            _ra(kq, "nang", "tu_khoa_khong_chia_chuong",
                f"chỉ {len(nhom)} nhóm '#', cần {can} (một nhóm mỗi chương)",
                "danh sách phẳng có thể dồn hết vào chương 1 mà chương 4 trống — "
                "đếm TỔNG vẫn thấy đủ, chỉ khi dựng mới lộ")


# ------------------------------------------------------------------ kho hình đã giao
def kiem_kho_hinh(kq, folder: Path, prof, rs):
    if not rs["deliver_stock"]:
        return
    stock = folder / "stock"
    if not stock.exists():
        _ra(kq, "nang", "khong_co_kho_hinh", "thiếu thư mục stock/",
            "hồ sơ đã bật deliver_stock — kho hình là một phần của bàn giao")
        return
    try:
        import stock_cut
    except Exception as e:
        _ra(kq, "nhe", "khong_nap_duoc_kho", f"không nạp được stock_cut: {e}")
        return
    body = prof.get("body") or {}
    chinh_sach = body.get("license_policy") or "permissive"
    vids, stills = stock_cut.nap_kho(stock, chinh_sach=chinh_sach,
                                     cam_tieu_de=body.get("title_blocklist") or ())
    reuse = int(body.get("reuse_max") or 6)
    chua = stock_cut.suc_chua(vids, stills, reuse)
    cuts = body.get("cuts_per_min") or [12, 16]
    phut = float((prof.get("script") or {}).get("target_minutes") or 0)
    can = int(phut * (sum(cuts) / 2))
    print(f"  · kho hình: {len(vids)} clip + {len(stills)} ảnh · gánh được {chua} cảnh "
          f"(cần ~{can})")
    if chua < can:
        _ra(kq, "nang", "kho_hinh_khong_du",
            f"kho gánh được {chua} cảnh, video cần ~{can}",
            "dựng bằng kho mỏng là lặp hình thấy rõ — bổ sung từ khoá rồi tải thêm")
    if not vids:
        _ra(kq, "nang", "kho_toan_anh_tinh",
            "không có clip VIDEO nào (chỉ ảnh tĩnh)",
            "lane này thân video là clip; toàn ảnh tĩnh là sai định dạng kênh")


# ------------------------------------------------------------------ ảnh bằng chứng
def kiem_bang_chung(kq, folder: Path, prof, rs):
    if not rs["deliver_evidence"]:
        return
    f = folder / "evidence.json"
    if not f.exists():
        _ra(kq, "nang", "khong_co_bang_chung", "thiếu evidence.json")
        return
    try:
        ds = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        _ra(kq, "nang", "bang_chung_hong", f"evidence.json không đọc được: {e}")
        return
    if len(ds) < rs["evidence_min"]:
        _ra(kq, "nang", "it_bang_chung", f"{len(ds)} mục, cần ≥{rs['evidence_min']}")
    try:
        import stock_cut
        hop = stock_cut.hop_chinh_sach
    except Exception:
        hop = None
    can_truong = ("file", "caption", "source", "license")
    for i, m in enumerate(ds, 1):
        thieu = [t for t in can_truong if not str(m.get(t) or "").strip()]
        if thieu:
            _ra(kq, "nang", "bang_chung_thieu_truong",
                f"mục {i} thiếu: {', '.join(thieu)}")
        # Ảnh cháy màn hình siết chặt hơn thân video: CHỈ Public Domain.
        pol = (prof.get("body") or {}).get("evidence_license_policy") or "pd"
        if hop and m.get("license") and not hop(m["license"], pol):
            _ra(kq, "nang", "bang_chung_sai_giay_phep",
                f"mục {i} giấy phép '{m['license']}' ngoài chính sách '{pol}'",
                "ảnh dẫn nguồn phải là tư liệu gốc PD, không nhận CC BY / Pexels")
        p = None
        thu_muc_anh = rs.get("evidence_dir") or "stock"
        for c in ((folder / thu_muc_anh / str(m.get("file") or "")), (folder / str(m.get("file") or ""))):
            if m.get("file") and c.exists():
                p = c
                break
        if m.get("file") and p is None:
            _ra(kq, "nang", "bang_chung_thieu_file", f"mục {i}: không thấy file {m['file']}")
            continue
        # Độ phân giải ảnh dẫn nguồn: cảnh báo, KHÔNG chặn.
        # Ảnh bằng chứng thường là tấm DUY NHẤT tồn tại (bản đồ tuyến bay trên Wikipedia chỉ có
        # 551×561 — không có bản lớn hơn vì đó chính là ảnh gốc). Chặn cứng ở đây là ép bên
        # nghiên cứu bỏ đúng tấm quan trọng nhất. Khâu dựng đã xử lý: ảnh nhỏ hơn khung được đặt
        # nguyên tấm vào giữa trên nền mờ (`fit="blur"`) thay vì phóng cho lấp khung.
        if p and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"):
            try:
                from PIL import Image
                w0, h0 = Image.open(p).size
                if w0 < 1280 or h0 < 720:
                    _ra(kq, "nhe", "bang_chung_do_phan_giai_thap",
                        f"mục {i} ({m['file']}) chỉ {w0}×{h0}",
                        "ưu tiên ≥1280×720. Nếu nguồn chỉ có bản này thì giữ — khâu dựng sẽ đặt "
                        "nguyên tấm trên nền mờ thay vì phóng to")
            except Exception:
                pass


# ------------------------------------------------------------------ hàng còn đang về
NGUOI_TA_CON_GHI = 120          # giây


def kiem_con_dang_ghi(kq, folder: Path):
    """Cảnh báo nếu bên kia CÒN ĐANG GHI vào thư mục — đã dính thật ngay lần chạy đầu.

    Chạy cổng lúc 16:51 trong khi SPACE_RESEARCH đang tải dở: thư mục có 9 file .mp4 nhưng
    `nap_kho()` chỉ nạp được **1** — 8 file kia còn viết dở nên ffprobe đọc không ra, bị lặng lẽ
    loại. Cổng in "kho gánh được 6 cảnh / cần 392" — một con số HOÀN TOÀN SAI mà nhìn rất giống
    một kết luận thật. Chạy lại sau 2 phút: 9/9 clip nạp bình thường.

    Đây là lý do cờ DONE-READY trên trang tính phải là thứ mở cổng, không phải "thấy có thư mục
    thì vào lấy": bên kia ghi cờ SAU KHI mọi thứ đã nằm trên ổ.
    """
    import time
    moi = 0.0
    for p in folder.rglob("*"):
        if p.is_file():
            moi = max(moi, p.stat().st_mtime)
    tuoi = time.time() - moi
    if 0 <= tuoi < NGUOI_TA_CON_GHI:
        _ra(kq, "nhe", "ho_so_vua_moi_ghi",
            f"file mới nhất chỉ vừa ghi {tuoi:.0f} giây trước",
            "bên research có thể đang tải dở ⇒ mọi con số dưới đây có thể sai. "
            "Đợi cờ DONE-READY trên trang tính rồi chạy lại")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True, help="thư mục hồ sơ bàn giao (_READY/<nn>-<slug>)")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--json", help="ghi kết quả ra file")
    a = ap.parse_args()

    import profiles
    prof = profiles.load(a.profile)
    folder = Path(a.folder)
    if not folder.exists():
        raise SystemExit(f"✗ không thấy thư mục {folder}")

    rs = dict(MAC_DINH)
    rs.update(prof.get("research") or {})
    if not prof.get("research"):
        print(f"ⓘ profile '{a.profile}' không khai khối `research` ⇒ lane này không nhận hàng "
              f"nghiên cứu từ ngoài. Bỏ qua cổng B0.")
        return
    gate = (prof.get("script") or {}).get("gate") or {}

    print(f"=== B0 NGHIỆM THU HỒ SƠ · {folder.name} · profile {a.profile} ===")
    kq = []
    kiem_con_dang_ghi(kq, folder)
    for ten in rs["files_required"]:
        if not (folder / ten).exists():
            _ra(kq, "nang", "thieu_file", f"thiếu {ten}")

    ctx = folder / "series_ctx.txt"
    if ctx.exists():
        text = ctx.read_text(encoding="utf-8", errors="replace")
        kiem_tieu_de(kq, text, rs, gate)
    kiem_competitor(kq, folder, prof, rs)
    kiem_tu_lieu(kq, folder, rs, gate)
    kiem_stock_queries(kq, folder, rs, gate)
    kiem_kho_hinh(kq, folder, prof, rs)
    kiem_bang_chung(kq, folder, prof, rs)

    nang = [x for x in kq if x["sev"] == "nang"]
    print(f"\n=== B0: {len(kq)} phát hiện ({len(nang)} nặng) ===")
    for x in kq:
        print(f"   [{x['sev']:4s}] {x['ma']}: {x['noi']}")
        if x["goi_y"]:
            print(f"          → {x['goi_y']}")
    if a.json:
        Path(a.json).write_text(json.dumps({"phat_hien": kq, "nang": len(nang)},
                                           ensure_ascii=False, indent=1), encoding="utf-8")
    if nang:
        raise SystemExit("✗ B0: hồ sơ CHƯA nhận được — trả lại bên research kèm danh sách trên.")
    print("✓ B0 ĐẠT — hồ sơ nhận được, sản xuất được ngay.")


if __name__ == "__main__":
    main()
