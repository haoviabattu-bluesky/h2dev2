# -*- coding: utf-8 -*-
"""stock_cut.py — dựng THÂN VIDEO bằng CLIP STOCK cắt nhanh, thay cho loạt ảnh AI.

Dùng cho ngách kể tài liệu (Lane A: 都市伝説/宇宙/ミステリー). Đo thật trên kênh mẫu
今夜も都市伝説: thân video **không có ảnh AI nào** — toàn clip tư liệu, cắt **12–16 lần/phút**
(mỗi cảnh 3,7–5,0 giây), tái dùng chéo giữa các video. Video 26 phút ≈ 340–410 cảnh nhưng chỉ
cần 80–120 file gốc.

  py -3.13 stock_cut.py --profile toshi-densetsu-jp --slug <thư mục tập> --plan-only
  py -3.13 stock_cut.py --profile toshi-densetsu-jp --slug <thư mục tập>

Ba điều file này làm mà ghép tay không làm nổi:
  1. **Cắt rơi đúng ranh giới câu**: mốc cắt hút về cue SRT gần nhất (±1s). Cắt tuỳ tiện giữa
     câu làm hình và lời lệch pha, nghe như xem hai video chồng lên nhau.
  2. **Không lặp hình lộ liễu**: mỗi file có trần số lần dùng, cấm dùng lại trong N cảnh gần
     nhau, và mỗi lần dùng lại phải lấy ĐOẠN KHÁC bên trong file (chọn điểm vào xa các điểm đã
     dùng nhất) — nếu không, người xem nhận ra ngay là một clip 20 giây quay vòng.
  3. **Sổ nguồn + ẢNH BẰNG CHỨNG có chú thích**: đây là chỗ thắng kênh mẫu. Hai comment nhiều
     like nhất của họ đều đòi tấm ảnh mà video đã hứa mà không có ("đưa ảnh ra đây" 86👍).
     `--evidence` ghim ảnh NASA/Wikimedia thật vào đúng giây, kèm dòng chú thích nguồn cháy
     lên hình. `credits.txt` xuất ra để dán vào phần mô tả video.

Yêu cầu: kho clip tải sẵn bằng `stockfetch.py` (kèm `manifest.jsonl` ghi giấy phép từng file).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

def _ensure_std():
    """xem publish_kit.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed.

    Gọi `sys.stdout.reconfigure()` thẳng ở CẤP MODULE là AttributeError câm lúc import khi đóng
    exe dạng --windowed (skill tao_tool_exe.md #30-35). Dùng chung một khuôn với các file khác.
    """
    import os
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

from assemble import FF, build_silent_concat, media_seconds, parse_srt_cues, render_clip

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
STILL_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}

# Bỏ bao nhiêu giây ĐẦU và ĐUÔI mỗi clip nguồn.
#
# ⚠️ 0,4s là KHÔNG ĐỦ. Clip NASA gắn **thẻ thương hiệu** (logo NASA + "GODDARD SPACE FLIGHT CENTER"
# + www.nasa.gov/goddard) ở CUỐI clip — đo thật: một cảnh rơi vào giây 115,8 của clip dài 119,9s và
# lên hình nguyên tấm thẻ đó giữa video kể về đa vũ trụ. Logo của đài khác nằm trong video mình là
# thứ tệ hơn cả nhoè: nó vừa lạc đề vừa trông như ăn cắp.
# Đuôi cắt dày hơn đầu vì thẻ kết thường dài hơn thẻ mở.
BIEN_DAU = 6.0
BIEN_DUOI = 9.0
BIEN_AN_TOAN = 0.4          # mức tối thiểu, dùng cho clip quá ngắn (giữ tên cũ cho code khác)
# Hút mốc cắt về ranh giới câu trong khoảng này. Rộng hơn 1,2s là nhịp cắt vỡ (cảnh 3s hoặc 7s).
HUT_VE_CUE = 1.2


# ----------------------------------------------------------------- kho tư liệu
# ----------------------------------------------------- chính sách giấy phép
# Không phải "có giấy phép" là dùng thoải mái. **CC BY-SA buộc tác phẩm phái sinh cũng phải mở
# theo SA** — nhét một tấm SA vào video 30 phút là kéo cả video vào ràng buộc đó. NC cấm dùng
# thương mại (mà YouTube bật kiếm tiền chính là thương mại), ND cấm sửa đổi (cắt/ghép/chèn phụ đề
# đều là sửa đổi). Vì vậy mặc định chỉ nhận PD + CC BY.
#   pd         — chỉ Public Domain / CC0: an toàn tuyệt đối, dùng cho ẢNH BẰNG CHỨNG cháy màn hình
#   permissive — PD + CC BY (mặc định): phải ghi nguồn, credits.txt đã lo
#   all        — nhận hết những gì có trong manifest (tự chịu trách nhiệm)
_SA_NC_ND = re.compile(r"\b(SA|NC|ND)\b", re.I)
_PD = re.compile(r"public\s*domain|\bCC0\b|\bPDM\b", re.I)
# Giấy phép "kho ảnh miễn phí" (Pexels/Pixabay/Unsplash): cho dùng thương mại, cho sửa đổi,
# KHÔNG bắt ghi nguồn ⇒ rộng hơn cả CC BY, nên nằm trong `permissive`. Phải khai tường minh vì
# chuỗi giấy phép của chúng không chứa "CC BY" lẫn "public domain" — thiếu dòng này thì tải về
# bao nhiêu clip Pexels cũng bị stock_cut loại sạch mà KHÔNG báo lỗi (chỉ thấy kho "hụt hàng").
# Vẫn KHÔNG được coi là `pd`: ảnh bằng chứng cháy màn hình phải là tư liệu gốc PD, không phải
# ảnh dàn dựng của kho stock.
_KHO_MIEN_PHI = re.compile(r"\bpexels\b|\bpixabay\b|\bunsplash\b", re.I)


def hop_chinh_sach(lic, chinh_sach="permissive"):
    lic = str(lic or "")
    if chinh_sach == "all":
        return True
    if _PD.search(lic):
        return True
    if chinh_sach == "pd":
        return False
    if _KHO_MIEN_PHI.search(lic):
        return True
    return bool(re.search(r"\bCC\s*BY\b", lic, re.I)) and not _SA_NC_ND.search(lic)


def doc_manifest(stock_dir: Path) -> dict:
    """{tên file: bản ghi giấy phép}. Thiếu sổ ⇒ file đó KHÔNG dùng (không đoán bản quyền)."""
    man = {}
    f = stock_dir / "manifest.jsonl"
    if not f.exists():
        return man
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if rec.get("file"):
            man[rec["file"]] = rec
    return man


def probe_kich_thuoc(path: Path, cache: dict):
    """(rộng, cao) của file — nhớ vào cache để khỏi gọi ffmpeg lại mỗi lần dựng."""
    key = "wh::" + path.name
    if key in cache:
        return tuple(cache[key])
    wh = (0, 0)
    try:
        r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True).stderr
        m = re.search(r"(\d{2,5})x(\d{2,5})", r)
        if m:
            wh = (int(m.group(1)), int(m.group(2)))
    except Exception:
        pass
    cache[key] = list(wh)
    return wh


def probe_do_sang(path: Path, cache: dict, la_anh=False):
    """Độ sáng trung bình (0–255) — lọc clip TỐI ĐEN mà vẫn là nội dung thật.

    B8Q báo "KHUNG ĐEN ở 964s". Soi ra không phải lỗi dựng: đó là clip **nguyệt thực**, mặt trăng
    chìm hẳn trong bóng. Nội dung thật, nhưng 4,6 giây gần như đen giữa video thì vẫn là hỏng mắt.
    Đo thật 11 clip trong kho: hai clip tối nhất 13,6 và 14,0 · clip kế tiếp đã 27,5 · sáng nhất
    128,5 → có một khoảng trống rõ ràng, đặt ngưỡng 20 là an toàn. Kênh này vốn tông tối nên KHÔNG
    được siết cao hơn, kẻo mất luôn mấy clip tinh vân đẹp.
    """
    key = "luma::" + path.name
    if key in cache:
        return cache[key]
    val = 255.0
    try:
        from PIL import Image
        import numpy as np
        if la_anh:
            val = float(np.asarray(Image.open(path).convert("L")).mean())
        else:
            dur = probe_seconds(path, cache)
            tmp = Path(tempfile.mkdtemp(prefix="luma_"))
            vals = []
            for k in range(3):
                f = tmp / f"{k}.png"
                subprocess.run([FF, "-y", "-ss", f"{dur * (k + 1) / 4:.2f}", "-i", str(path),
                                "-vframes", "1", str(f)], capture_output=True)
                if f.exists():
                    vals.append(float(np.asarray(Image.open(f).convert("L")).mean()))
            shutil.rmtree(tmp, ignore_errors=True)
            if vals:
                val = sum(vals) / len(vals)
    except Exception:
        pass
    cache[key] = round(val, 1)
    return cache[key]


def probe_seconds(path: Path, cache: dict) -> float:
    key = path.name
    if key in cache:
        return cache[key]
    try:
        d = media_seconds(path)
    except Exception:
        d = 0.0
    cache[key] = d
    return d


# Tư liệu NASA có RẤT NHIỀU video "chương trình" (bản tin tuần, livestream khoa học, họp báo,
# giới thiệu sứ mệnh) — toàn người nói chuyện + đồ hoạ + CHỮ TIẾNG ANH cháy sẵn. Đo thật ở tập 1:
# một cảnh rơi vào biểu đồ El Niño của NOAA có dòng "to produce a forecast for the next 9 months"
# nằm chình ình giữa video kể về đa vũ trụ. B-roll được phép không minh hoạ lời, nhưng KHÔNG được
# mang chữ của một câu chuyện khác.
CAM_TIEU_DE = [
    r"this week @?\s*nasa", r"science live", r"what'?s up", r"mission overview", r"talks? with",
    r"briefing", r"press conference", r"news release", r"\bep\.?\s*\d", r"episode",
    r"live stream", r"livestream", r"town hall", r"interview", r"q&a", r"webinar",
]


def bi_cam_tieu_de(tieu_de, them=()):
    t = str(tieu_de or "")
    for m in list(CAM_TIEU_DE) + list(them or []):
        if re.search(m, t, re.I):
            return m
    return ""


def nap_kho(stock_dir: Path, cho_phep_thieu_so=False, chinh_sach="permissive", cam_tieu_de=(),
            cao_toi_thieu=720, sang_toi_thieu=20.0):
    """Trả (videos, stills) — mỗi phần tử {path, dur, license, credit, title}.

    Lọc theo `chinh_sach` giấy phép (xem hop_chinh_sach): mặc định BỎ CC BY-SA/NC/ND.
    """
    man = doc_manifest(stock_dir)
    # DANH SÁCH CẤM do `soi_kho.py` chấm bằng mắt model. Mọi bộ lọc khác ở đây đều đo KỸ THUẬT
    # (giấy phép, độ nét, độ sáng, tiêu đề) — không cái nào biết được clip mang NỘI DUNG gì, nên
    # biển "Welcome to Las Vegas" và phụ nữ gõ máy tính văn phòng lọt qua sạch sẽ rồi nằm giữa
    # đoạn kể chuyện căn cứ quân sự. Chấm nội dung là việc chỉ vision làm được; chấm một lần rồi
    # ghi ra file, mỗi lần dựng đọc lại, khỏi trả tiền lại.
    cam_noi_dung, soi_f = set(), stock_dir / "soi_kho.json"
    if soi_f.exists():
        try:
            cam_noi_dung = {x["file"] for x in json.loads(soi_f.read_text(encoding="utf-8"))
                            if x.get("muc") == 0}
        except Exception as e:
            print(f"  ! đọc soi_kho.json lỗi ({type(e).__name__}) → không cấm được file nào")
    cache_f = stock_dir / "_probe.json"
    cache = json.loads(cache_f.read_text(encoding="utf-8")) if cache_f.exists() else {}
    vids, stills, bo_giay_phep, bo_tieu_de, bo_do_net, bo_toi = [], [], [], [], [], []
    bo_noi_dung = []
    for p in sorted(stock_dir.iterdir()):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if p.name in cam_noi_dung:
            bo_noi_dung.append(p.name)
            continue
        rec = man.get(p.name)
        if rec is None and not cho_phep_thieu_so:
            if ext in VIDEO_EXT or ext in STILL_EXT:
                print(f"  ⤫ {p.name} không có trong manifest.jsonl → bỏ (không rõ giấy phép)")
            continue
        rec = rec or {}
        if rec and not hop_chinh_sach(rec.get("license"), chinh_sach):
            bo_giay_phep.append((p.name, rec.get("license")))
            continue
        vi_pham = bi_cam_tieu_de(rec.get("title"), cam_tieu_de)
        if vi_pham:
            bo_tieu_de.append((rec.get("title", p.name)[:44], vi_pham))
            continue
        item = {"path": p, "license": rec.get("license", "?"), "credit": rec.get("credit", ""),
                "title": rec.get("title", p.stem), "src": rec.get("src", "?"),
                # TỪ KHOÁ đã tải file này về — là sợi dây DUY NHẤT nối clip với NỘI DUNG.
                # Thiếu nó thì khâu chọn hình chỉ còn biết "file nào ít dùng nhất", tức là
                # chọn ngẫu nhiên (xem `chia_theo_chuong`).
                "query": (rec.get("query") or "").strip().lower()}
        if ext in VIDEO_EXT:
            d = probe_seconds(p, cache)
            if d < 2.0:
                print(f"  ⤫ {p.name} chỉ {d:.1f}s → bỏ")
                continue
            # Khung ra là 1920×1080. Clip 320×180 phóng lên là upscale 6× — nhoè không cứu được,
            # kể cả bằng AI. Thà thiếu tư liệu còn hơn dựng 73% thời lượng bằng ảnh nhoè.
            w, h = probe_kich_thuoc(p, cache)
            if h and h < cao_toi_thieu:
                bo_do_net.append((p.name, f"{w}x{h}"))
                continue
            lum = probe_do_sang(p, cache)
            if lum < sang_toi_thieu:
                bo_toi.append((p.name, lum))
                continue
            vids.append({**item, "dur": d, "wh": (w, h), "luma": lum})
        elif ext in STILL_EXT:
            w, h = probe_kich_thuoc(p, cache)
            if h and h < cao_toi_thieu * 0.75:      # ảnh tĩnh nới hơn: Ken Burns crop vào giữa
                bo_do_net.append((p.name, f"{w}x{h}"))
                continue
            lum = probe_do_sang(p, cache, la_anh=True)
            if lum < sang_toi_thieu:
                bo_toi.append((p.name, lum))
                continue
            stills.append({**item, "dur": 0.0, "wh": (w, h), "luma": lum})
    cache_f.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    if bo_giay_phep:
        print(f"  ⓘ bỏ {len(bo_giay_phep)} file vì giấy phép ngoài chính sách '{chinh_sach}' "
              f"(vd {bo_giay_phep[0][0][:34]} — {bo_giay_phep[0][1]})")
    if bo_toi:
        print(f"  ⓘ bỏ {len(bo_toi)} file vì QUÁ TỐI (độ sáng <{sang_toi_thieu}): "
              + " · ".join(f"{n[:30]} {v}" for n, v in bo_toi[:3]))
    if bo_do_net:
        print(f"  ⓘ bỏ {len(bo_do_net)} file vì ĐỘ PHÂN GIẢI THẤP (<{cao_toi_thieu}p): "
              + " · ".join(f"{n[:28]} {k}" for n, k in bo_do_net[:3]))
    if bo_tieu_de:
        print(f"  ⓘ bỏ {len(bo_tieu_de)} file dạng CHƯƠNG TRÌNH (người nói/đồ hoạ/chữ tiếng Anh): "
              + " · ".join(f"{t}" for t, _ in bo_tieu_de[:3]))
    if bo_noi_dung:
        print(f"  🚫 bỏ {len(bo_noi_dung)} file vì NỘI DUNG LẠC ĐỀ TÀI (soi_kho.json chấm 0): "
              + " · ".join(n[:28] for n in bo_noi_dung[:3]))
    elif not soi_f.exists():
        print("  ⚠️ kho CHƯA được soi nội dung (thiếu soi_kho.json) → clip lạc đề tài vẫn lọt "
              "vào video. Chạy: py -3.13 soi_kho.py --stock <kho>")
    return vids, stills


# ----------------------------------------------------------------- lập kế hoạch cảnh
def moc_cat(audio_len, cues, lo, hi, rnd):
    """Danh sách (bắt đầu, dài) phủ kín audio, mỗi cảnh lo..hi giây, mốc hút về ranh giới câu."""
    starts = [c[0] if isinstance(c, (tuple, list)) else c for c in cues]
    out, t = [], 0.0
    while t < audio_len - 0.4:
        muon = rnd.uniform(lo, hi)
        moc = t + muon
        if starts:
            gan = min(starts, key=lambda s: abs(s - moc))
            # Chỉ hút khi vẫn giữ được cảnh trong khoảng cho phép — nếu không thì nhịp cắt vỡ.
            if abs(gan - moc) <= HUT_VE_CUE and lo * 0.75 <= gan - t <= hi * 1.25:
                moc = gan
        moc = min(moc, audio_len)
        if moc - t < 1.5:            # cảnh cụt ⇒ nhập vào cảnh trước
            if out:
                out[-1] = (out[-1][0], audio_len - out[-1][0])
                break
        out.append((t, moc - t))
        t = moc
    if out and abs((out[-1][0] + out[-1][1]) - audio_len) > 0.05:
        out[-1] = (out[-1][0], audio_len - out[-1][0])
    return out


def tran_dung(item, kieu, reuse_max):
    """Trần số lần dùng của MỘT file — theo sức chứa thật, không cào bằng.

    Ảnh tĩnh và clip ngắn: dùng lại nhiều lần là lộ ngay. Nhưng clip tư liệu NASA dài 20–44 phút
    chứa hàng trăm đoạn 4 giây hoàn toàn khác nhau — ép nó cùng trần với clip 40 giây là tự bắt
    mình tải thêm hàng chục file vô ích. Cứ ~15 giây nguồn đổi lấy 1 lần dùng, trần trên 4×.
    """
    if kieu != "video":
        return reuse_max
    return max(reuse_max, min(reuse_max * 4, int(item["dur"] // 15)))


def suc_chua(vids, stills, reuse_max):
    """Tổng số cảnh kho này gánh được mà chưa phải lặp quá trần."""
    return (sum(tran_dung(v, "video", reuse_max) for v in vids)
            + sum(tran_dung(s, "still", reuse_max) for s in stills))


def doc_tu_khoa_theo_chuong(f: Path) -> list[list[str]]:
    """`stock_queries.txt` chia theo chương → [[từ khoá chương 1], [chương 2], …].

    File có dạng:
        # 第1章 — 1989年の告発
        desert military base fence
        ...
        # 第2章 — …
    Dòng `#` KHÔNG phải chú thích suông mà là RANH GIỚI CHƯƠNG. Không có dòng `#` nào có nghĩa
    hồ sơ còn dùng khuôn cũ (danh sách phẳng) ⇒ trả rỗng, khâu chọn hình lùi về như trước.
    """
    if not f.exists():
        return []
    nhom, hien = [], None
    for d in f.read_text(encoding="utf-8", errors="replace").splitlines():
        d = d.strip()
        if not d:
            continue
        if d.startswith("#"):
            if re.search(r"第\s*\d+\s*章|chương\s*\d+", d, re.I):
                hien = []
                nhom.append(hien)
            continue
        if hien is not None:
            hien.append(d.lower())
    return [n for n in nhom if n]


def doc_khop_hinh(f: Path):
    """`khop_hinh.json` → [(t0, t1, query)] đã sắp theo thời gian. Không có file ⇒ rỗng."""
    if not f.exists():
        return []
    try:
        ds = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return []
    return [(float(x["t0"]), float(x["t1"]), str(x.get("query") or "").lower())
            for x in ds if x.get("query")]


def chia_theo_cau(canh, khop):
    """Từ khoá hình cho TỪNG CẢNH, lấy theo đoạn lời đang đọc lúc đó.

    Mịn hơn `chia_theo_chuong` một bậc: chương gom 5 phút vào 5–7 từ khoá, còn đây gom ~15 giây
    vào ĐÚNG MỘT từ khoá — tức là hình bám theo câu chứ không bám theo chương.
    Cảnh rơi ra ngoài mọi đoạn (đầu/cuối video) trả rỗng ⇒ gọi tầng dưới lo.
    """
    ra = []
    for t0, dur in canh:
        giua = t0 + dur / 2
        q = next((q for a, b, q in khop if a <= giua < b), "")
        ra.append({q} if q else set())
    return ra


def chia_theo_chuong(canh, moc_chuong, nhom_tu_khoa):
    """Với mỗi cảnh, trả TẬP TỪ KHOÁ được phép dùng (rỗng = cho dùng tất).

    ⚠️ ĐÂY LÀ CHỖ HỎNG NẶNG NHẤT TỪNG CÓ. `chon_nguon` vốn chọn clip theo "ít dùng nhất + ngẫu
    nhiên", KHÔNG hề đối chiếu clip với lời đang đọc. Kết quả xem thật ở tập 3: đoạn kể về người
    đàn ông tự xưng Dennis năm 1989 thì trên hình là **một phụ nữ mặc áo hồng ngồi gõ laptop**;
    một chỗ khác đang kể vụ mất tích thì hiện **máy bay Emirates**. Người xem không cần biết
    thuật toán nào cũng thấy ngay hình một đằng lời một nẻo.
    Kho chia theo tập chỉ chữa được một nửa (clip đúng ĐỀ TÀI); nửa còn lại là clip phải đúng
    **CHƯƠNG** — mà dữ liệu để làm việc đó đã có sẵn: `stock_queries.txt` từ nay chia theo chương,
    và `manifest.jsonl` ghi mỗi file tải về theo từ khoá nào.
    """
    if not moc_chuong or not nhom_tu_khoa:
        return [set() for _ in canh]
    bien = [m[0] for m in moc_chuong]
    ra = []
    for t0, _ in canh:
        k = max(0, sum(1 for b in bien if b <= t0) - 1)   # mốc[0] là phần dẫn nhập
        # Chương 1 ứng với nhóm từ khoá 1; phần dẫn nhập (trước 第1章) dùng chung nhóm 1.
        idx = min(max(k - 1, 0), len(nhom_tu_khoa) - 1) if k > 0 else 0
        ra.append(set(nhom_tu_khoa[idx]))
    return ra


def chon_nguon(canh, vids, stills, reuse_max, cach_nhau, rnd, cho_phep=None):
    """Gán file nguồn cho từng cảnh. Trả list bản ghi cảnh đã đủ thông tin để render."""
    pool = [{"it": v, "kieu": "video", "dung": 0, "diem": []} for v in vids] + \
           [{"it": s, "kieu": "still", "dung": 0, "diem": []} for s in stills]
    if not pool:
        raise SystemExit("Kho tư liệu rỗng — chạy stockfetch.py trước.")
    lan_cuoi = {id(p): -10 ** 6 for p in pool}
    ke_hoach = []
    for i, (t0, dur) in enumerate(canh):
        # Ứng viên: chưa chạm trần dùng lại, đủ dài, và đã cách xa lần dùng trước.
        hop_chuong = (cho_phep[i] if cho_phep and i < len(cho_phep) else set())

        def hop_le(p, gan=cach_nhau, theo_chuong=True):
            if p["kieu"] == "video" and p["it"]["dur"] < dur + 2 * BIEN_AN_TOAN:
                return False
            if theo_chuong and hop_chuong and p["it"].get("query") not in hop_chuong:
                return False
            return (p["dung"] < tran_dung(p["it"], p["kieu"], reuse_max)
                    and (i - lan_cuoi[id(p)]) >= gan)
        # THỨ TỰ NHƯỜNG BƯỚC có chủ ý: nới khoảng-cách-dùng-lại TRƯỚC, bỏ ràng buộc chương SAU.
        # Hình lặp lại sau vài cảnh chỉ hơi nhàm; hình lạc đề thì người xem thấy ngay là sai.
        # Nên thà dùng lại clip đúng chương còn hơn bốc một clip đúng "chưa dùng" mà lạc nội dung.
        ung = [p for p in pool if hop_le(p)]
        if not ung:
            for gan in (cach_nhau // 2, 3, 1):
                ung = [p for p in pool if hop_le(p, gan)]
                if ung:
                    break
        if not ung and hop_chuong:                    # chương này cạn clip ⇒ mới mượn cả kho
            for gan in (cach_nhau, cach_nhau // 2, 3, 1):
                ung = [p for p in pool if hop_le(p, gan, theo_chuong=False)]
                if ung:
                    break
        if not ung:                                   # kho quá nhỏ ⇒ bỏ trần dùng lại
            ung = [p for p in pool
                   if p["kieu"] == "still" or p["it"]["dur"] >= dur + 2 * BIEN_AN_TOAN]
        if not ung:
            raise SystemExit(f"Không file nào đủ dài cho cảnh {dur:.1f}s — kho tư liệu quá ngắn.")
        p = min(ung, key=lambda x: (x["dung"], rnd.random()))
        vao = 0.0
        if p["kieu"] == "video":
            # Clip đủ dài thì cắt biên dày (né thẻ thương hiệu ở đầu/đuôi); clip ngắn thì đành
            # dùng biên tối thiểu, còn hơn bỏ hẳn file.
            if p["it"]["dur"] >= BIEN_DAU + BIEN_DUOI + dur + 1:
                dau, tran = BIEN_DAU, p["it"]["dur"] - BIEN_DUOI - dur
            else:
                dau, tran = BIEN_AN_TOAN, p["it"]["dur"] - dur - BIEN_AN_TOAN
            if tran <= dau:
                vao = max(0.0, min(dau, p["it"]["dur"] - dur))
            elif not p["diem"]:
                vao = rnd.uniform(dau, tran)
            else:
                # Lần dùng lại: lấy đoạn XA NHẤT các đoạn đã dùng, để hai lần xuất hiện của
                # cùng một file trông như hai cảnh khác nhau.
                ungvien = [dau + (tran - dau) * k / 8 for k in range(9)]
                vao = max(ungvien, key=lambda v: min(abs(v - d) for d in p["diem"]))
        p["diem"].append(vao)
        p["dung"] += 1
        lan_cuoi[id(p)] = i
        ke_hoach.append({"i": i, "t0": round(t0, 3), "dur": round(dur, 3), "kieu": p["kieu"],
                         "file": p["it"]["path"].name, "vao": round(vao, 3),
                         "license": p["it"]["license"], "credit": p["it"]["credit"],
                         "title": p["it"]["title"]})
    return ke_hoach, pool


# ----------------------------------------------------------------- ảnh bằng chứng
def _giay(v):
    """'12:34' / '12:34.5' / 754 → giây."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if ":" in s:
        parts = [float(x) for x in s.split(":")]
        return sum(p * 60 ** (len(parts) - 1 - k) for k, p in enumerate(parts))
    return float(s)


def _luma_tai(path: Path, t: float, cache: dict):
    """Độ sáng của ĐÚNG một khung hình tại giây t."""
    key = f"lumat::{path.name}::{t:.1f}"
    if key in cache:
        return cache[key]
    val = 255.0
    try:
        from PIL import Image
        import numpy as np
        tmp = Path(tempfile.mkdtemp(prefix="lm_"))
        f = tmp / "f.png"
        subprocess.run([FF, "-y", "-ss", f"{t:.2f}", "-i", str(path), "-vframes", "1", str(f)],
                       capture_output=True)
        if f.exists():
            val = float(np.asarray(Image.open(f).convert("L")).mean())
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass
    cache[key] = val
    return val


def nan_doan_toi(ke_hoach, stock_dir: Path, cache: dict, nguong=20.0, luong=8):
    """Nắn lại ĐIỂM VÀO của những cảnh rơi trúng đoạn tối đen bên trong clip.

    ⚠️ Bộ lọc `min_luma` ở `nap_kho()` đo ĐỘ SÁNG TRUNG BÌNH CẢ CLIP (3 khung mẫu) — nó loại clip
    tối từ đầu đến cuối, nhưng KHÔNG cứu được clip sáng-tối lẫn lộn. Đo thật ở tập 2:
    `pexels_34296917.mp4` trung bình 21,9 (qua cửa), nhưng đoạn ở giây 10,3 chỉ còn **6–8** — B8Q
    báo "KHUNG ĐEN ở 505s", mà cắt khung ra xem thì cảnh liền sau lại sáng trưng 184.
    Nói cách khác: **qua cửa ở mức clip không có nghĩa là qua ở mức ĐOẠN ĐƯỢC CẮT.**

    Nên: soi chính đoạn sẽ dùng, tối quá thì dời điểm vào sang chỗ sáng nhất trong cùng clip.
    Chỉ soi clip có nguy cơ (trung bình < 70) để khỏi tốn thêm mấy trăm lần gọi ffmpeg.
    """
    nghi = [c for c in ke_hoach
            if c["kieu"] == "video" and not c.get("bangchung")
            and probe_do_sang(stock_dir / c["file"], cache) < 70.0]
    if not nghi:
        return 0
    da_nan = 0

    def xu_ly(c):
        p = stock_dir / c["file"]
        giua = c["vao"] + c["dur"] / 2
        if _luma_tai(p, giua, cache) >= nguong:
            return None
        dur_clip = probe_seconds(p, cache)
        dau = BIEN_AN_TOAN
        tran = max(dau, dur_clip - c["dur"] - BIEN_AN_TOAN)
        ung = [dau + (tran - dau) * k / 6 for k in range(7)]
        diem = [(_luma_tai(p, v + c["dur"] / 2, cache), v) for v in ung]
        sang, v = max(diem)
        return (c, sang, v)

    with cf.ThreadPoolExecutor(max_workers=luong) as ex:
        for kq in ex.map(xu_ly, nghi):
            if not kq:
                continue
            c, sang, v = kq
            if sang >= nguong:
                c["vao"] = v
                da_nan += 1
            else:
                c["_van_toi"] = round(sang, 1)
    con = [c for c in ke_hoach if c.get("_van_toi")]
    print(f"  ⓘ nắn {da_nan} cảnh rơi vào đoạn tối trong clip"
          + (f" · còn {len(con)} cảnh không tìm được đoạn sáng" if con else ""))
    return da_nan


def gan_at_theo_chuong(evid, prof, script_path: Path, srt_path, tong_giay: float):
    """Suy ra mốc giây cho ảnh bằng chứng CHỈ khai `chapter`, không khai `at`.

    Vì sao cần: hồ sơ do dự án nghiên cứu giao được viết **trước khi có kịch bản**, nên bên đó
    không thể biết tấm ảnh sẽ rơi vào giây thứ mấy — nhưng biết chắc nó thuộc **chương nào**.
    Bắt họ khai `at` là bắt khai một thứ chưa tồn tại; bản đầu của hàm này đòi `e["at"]` nên
    `KeyError: 'at'` làm chết cả B8 sau khi đã dựng xong kế hoạch cảnh.

    Mốc chương đọc từ CHÍNH LỜI ĐỌC (dùng lại `publish_kit._chuong_theo_marker`), không chia đều
    theo thời gian — chia đều thì ảnh ghim lệch khỏi đoạn đang nói tới nó. Nhiều ảnh cùng một
    chương thì rải đều BÊN TRONG chương đó, để hai tấm không chồng lên nhau.
    """
    thieu = [e for e in evid if "at" not in e and e.get("chapter")]
    if not thieu:
        return
    try:
        # ⚠️ PHẢI dùng storyboard.parse_cues, KHÔNG dùng `cues` của file này.
        # `assemble.parse_srt_cues()` trả **(giây, lời)** 2 phần tử, còn
        # `publish_kit._chuong_theo_marker()` đọc `c[2]` là lời (3 phần tử: đầu, cuối, lời).
        # Truyền nhầm loại thì nó ném `IndexError: tuple index out of range`, bị `except` nuốt
        # thành "không đọc được mốc chương" — và 8 ảnh bằng chứng biến mất khỏi video mà B8 vẫn
        # báo dựng xong. Đã dính thật một lần. Hai hàm parse cùng tên gọi khác hình dạng là bẫy.
        import publish_kit, storyboard
        script = script_path.read_text(encoding="utf-8") if script_path.exists() else ""
        cues3 = storyboard.parse_cues(Path(srt_path)) if srt_path and Path(srt_path).exists() else []
        moc = publish_kit._chuong_theo_marker(prof, script, cues3)
    except Exception as e:
        moc = []
        print(f"  ! không đọc được mốc chương ({type(e).__name__}: {e})")
    if not moc:
        print("  ! không xác định được mốc chương ⇒ bỏ qua ảnh bằng chứng khai theo chương")
        return
    # moc[0] luôn là phần dẫn nhập (0:00); 第N章 nằm ở moc[N].
    bien = [m[0] for m in moc] + [tong_giay]
    theo_ch = {}
    for e in thieu:
        theo_ch.setdefault(int(e["chapter"]), []).append(e)
    for ch, ds in theo_ch.items():
        if ch >= len(bien) - 1:
            print(f"  ! chương {ch} nằm ngoài {len(moc)} mốc đọc được → bỏ qua {len(ds)} ảnh")
            continue
        t0, t1 = bien[ch], bien[ch + 1]
        for i, e in enumerate(ds, 1):
            e["at"] = round(t0 + (t1 - t0) * i / (len(ds) + 1), 1)
            e["_tu_chuong"] = ch


def gan_bang_chung(ke_hoach, evid, stock_dir: Path, chinh_sach="pd"):
    """Ghim file cụ thể + chú thích vào các cảnh quanh mốc thời gian đã chỉ định.

    Ảnh bằng chứng đi kèm dòng chú thích CHÁY LÊN HÌNH và là thứ mình chủ động khoe ra, nên mặc
    định siết chặt hơn cả thân video: **chỉ Public Domain**. Một tấm CC BY-SA đặt ở đúng chỗ mình
    đang nói "đây là bằng chứng" là mời người ta soi giấy phép của cả video.
    """
    man = doc_manifest(stock_dir)
    for e in evid:
        if "at" not in e:
            print(f"  ! bằng chứng {e.get('file')} không có `at` lẫn `chapter` dùng được → bỏ qua")
            continue
        at = _giay(e["at"])
        sec = float(e.get("sec", 6.0))
        f = e["file"]
        p = (stock_dir / f) if not Path(f).is_absolute() else Path(f)
        if not p.exists():
            print(f"  ! bằng chứng thiếu file: {p} → bỏ qua")
            continue
        lic = (man.get(p.name) or {}).get("license")
        if lic is None:
            print(f"  ! bằng chứng {p.name} không có trong manifest (không rõ giấy phép) → bỏ qua")
            continue
        if not hop_chinh_sach(lic, chinh_sach):
            print(f"  ! bằng chứng {p.name} giấy phép '{lic}' ngoài chính sách '{chinh_sach}' "
                  f"→ bỏ qua (ảnh bằng chứng nên dùng Public Domain)")
            continue
        het = at + sec
        chon = [c for c in ke_hoach if c["t0"] + c["dur"] > at and c["t0"] < het]
        if not chon:
            print(f"  ! không có cảnh nào ở mốc {e['at']} → bỏ qua")
            continue
        for c in chon:
            c.update({"kieu": "still" if p.suffix.lower() in STILL_EXT else "video",
                      "file": p.name, "vao": 0.0, "bangchung": True,
                      "caption": e.get("caption", ""), "license": e.get("license", c["license"]),
                      "credit": e.get("credit", c["credit"])})
        print(f"  ⭐ bằng chứng {e['at']} ({sec:.0f}s): {p.name} — {len(chon)} cảnh")
    return ke_hoach


NHAN_ANH_AI = "イメージ（再現）"


def gan_anh_ai(ke_hoach, thu_muc: Path, nhan=NHAN_ANH_AI):
    """Thay clip stock bằng ẢNH TỰ VẼ ở những đoạn lời mà kho stock không có gì đúng.

    VÌ SAO PHẢI CÓ TẦNG NÀY
    --------------------------------------------------------------------------------------------
    Chuỗi làm hình là **từ khoá → clip → câu**. `khop_hinh.py` đã nối chuẩn khâu *clip → câu*, nên
    giờ mỗi cảnh đúng là clip của đoạn lời đang đọc. Nhưng khâu *từ khoá → clip* thì hỏng ở chỗ
    không code nào chữa được: Pexels là kho ảnh ĐỜI THƯỜNG, tìm thứ nó không có thì nó vẫn trả về
    thứ gì đó. Soi cả kho tập 3 bằng vision (`soi_kho.py`): **103/248 file dùng được (42%)**, và
    9 từ khoá sai 8/8 — `area 51 sign nevada` ra phố Las Vegas, `japan military base fence gate`
    ra cổng torii đền thờ, `polygraph test machine` / `stealth aircraft hangar` không có tấm nào
    đúng. Khớp hoàn hảo một clip sai thì người xem vẫn thấy sai.
    Chỗ nào kho không có thì VẼ — chỉ vẽ đúng những đoạn `khop_hinh` đánh dấu `CU_THE` (có vật/nơi
    xác định), còn đoạn `KHONG_KHI` (sa mạc, trời đêm, đường vắng) thì stock vốn thừa sức.

    NHÃN 「イメージ」 LÀ BẮT BUỘC, KHÔNG PHẢI TRANG TRÍ
      Ảnh vẽ ra trông như ảnh chụp thật, mà nội dung là **lời khai chính tập này bác bỏ** (hầm
      ngầm chứa 9 đĩa bay). Phim tài liệu thật luôn dán chữ "hình dựng lại" lên cảnh dàn dựng;
      bỏ nhãn là đúng thứ chính sách "nội dung không trung thực" 2026 của YouTube nhắm tới.
      Dán cho MỌI ảnh AI chứ không chọn lọc từng cảnh: nhất quán thì người xem hiểu ngay quy ước.

    `img_meta*.json` là NGUỒN CHÂN LÝ — nó ghi ảnh thứ i thuộc đoạn lời (t0,t1) nào. Không đi tính
    lại "từ khoá nào hỏng" lúc dựng: tính hai lần ở hai chỗ là hai kết quả khác nhau.
    """
    meta_f = next((thu_muc / t for t in ("img_meta.json", "img_meta_test.json")
                   if (thu_muc / t).exists()), None)
    if not meta_f:
        print(f"  ! {thu_muc} không có img_meta*.json → bỏ qua tầng ảnh tự vẽ")
        return 0
    ds = json.loads(meta_f.read_text(encoding="utf-8"))
    # GHÉP THEO TÊN FILE khi bản ghi có khai `file`.
    #
    # ⚠️ Cách cũ là `zip(bản_ghi, sorted(ảnh))` — chỉ đúng khi thư mục có ĐỦ và ĐÚNG số ảnh.
    # Thiếu một tấm ở giữa là mọi tấm phía sau **tụt một bậc**: ảnh của đoạn 12 rơi vào đoạn 11,
    # và không có gì báo lỗi — video vẫn dựng, vẫn đủ cảnh, chỉ là sai hết từ chỗ đó trở đi.
    # Rủi ro này thành thật khi ảnh do MÁY KHÁC vẽ rồi gửi sang: thiếu vài tấm là chuyện bình
    # thường. Có `file` thì tấm nào thiếu chỉ bỏ đúng tấm đó.
    thieu = []
    if ds and ds[0].get("file"):
        khoi = {}
        for rec in ds:
            p = thu_muc / rec["file"]
            if not p.exists():
                thieu.append(rec["file"])
                continue
            khoi.setdefault((float(rec["t0"]), float(rec["t1"])),
                            [rec.get("query", ""), []])[1].append(p)
        khoi = {k: v for k, v in khoi.items() if v[1]}
        if thieu:
            print(f"  ! thiếu {len(thieu)} ảnh đã đặt ({', '.join(thieu[:6])}…) → bỏ đúng những "
                  f"tấm đó, các tấm còn lại KHÔNG bị lệch đoạn")
    else:
        anh = sorted(p for p in thu_muc.iterdir() if p.suffix.lower() in STILL_EXT)
        if len(anh) != len(ds):
            print(f"  ! {meta_f.name} khai {len(ds)} ảnh nhưng thư mục có {len(anh)} → lấy phần "
                  f"chung (bản ghi cũ không có trường `file`, ghép theo thứ tự tên)")
            ds, anh = ds[:min(len(ds), len(anh))], anh[:min(len(ds), len(anh))]
        khoi = {}
        for rec, p in zip(ds, anh):
            khoi.setdefault((float(rec["t0"]), float(rec["t1"])), [rec.get("query", ""), []])[1].append(p)
    n, bo = 0, 0
    for (t0, t1), (q, ps) in sorted(khoi.items()):
        chon = [c for c in ke_hoach
                if not c.get("bangchung") and t0 <= c["t0"] + c["dur"] / 2 < t1]
        if not chon:
            bo += len(ps)
            continue
        for j, c in enumerate(chon):
            p = ps[j % len(ps)]
            c.update({"kieu": "still", "file": p.name, "goc": str(thu_muc), "vao": 0.0,
                      "anh_ai": True, "caption": nhan, "license": "ai-generated",
                      "credit": "AI生成イメージ", "title": f"AI生成イメージ — {q}"})
        n += len(chon)
    print(f"  🎨 ảnh tự vẽ: {len(khoi)} đoạn lời · {n} cảnh dùng ảnh (nhãn 「{nhan}」)"
          + (f" · {bo} ảnh không có cảnh tương ứng" if bo else ""))
    return n


# ----------------------------------------------------------------- render
FONT_CAPTION = ("C:/Windows/Fonts/meiryo.ttc", "C:/Windows/Fonts/YuGothB.ttc",
                "C:/Windows/Fonts/YuGothR.ttc", "C:/Windows/Fonts/msgothic.ttc")


def anh_caption(text, W, H, ra: Path):
    """Vẽ dải chú thích nguồn ra PNG trong suốt (PIL), để ffmpeg chỉ việc `overlay`.

    Vì sao KHÔNG dùng drawtext: đường dẫn Windows trong chuỗi filter mang dấu ':' của ổ đĩa, mà
    ':' cũng là dấu ngăn tham số của ffmpeg. Mọi kiểu escape thử qua đều ra
    "Error parsing a filter description" (exit -22) và nó giết CẢ lượt render 409 cảnh chỉ vì một
    dòng chữ. Vẽ sẵn ảnh rồi overlay là đường thẳng: không escape, không phụ thuộc fontconfig,
    lại chỉnh được kiểu chữ cho giống phần còn lại của kênh.
    """
    from PIL import Image, ImageDraw, ImageFont
    duong = next((f for f in FONT_CAPTION if Path(f).exists()), None)
    if not duong:
        raise SystemExit("Không có font Nhật (meiryo/YuGoth/msgothic) để vẽ chú thích nguồn.")
    co = max(20, H // 34)
    font = ImageFont.truetype(duong, co)
    dem = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    rong_toi_da = int(W * 0.94)
    while co > 14 and dem.textlength(text, font=font) > rong_toi_da:
        co -= 2
        font = ImageFont.truetype(duong, co)
    tw = int(dem.textlength(text, font=font))
    pad = int(co * 0.55)
    img = Image.new("RGBA", (tw + 2 * pad, int(co * 1.9)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=int(co * 0.35),
                        fill=(0, 0, 0, 165))
    d.text((pad, img.height // 2), text, font=font, fill=(255, 255, 255, 255), anchor="lm")
    img.save(ra)
    return ra


def phu_caption(video: Path, cap_png: Path, H, threads=2):
    """Chồng dải chú thích lên video cảnh (in-place)."""
    tam = video.with_suffix(".cap.mp4")
    subprocess.run([FF, "-y", "-i", str(video), "-i", str(cap_png),
                    "-filter_complex", f"[0:v][1:v]overlay=(W-w)/2:{H // 14}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-threads", str(threads), str(tam)],
                   check=True, capture_output=True)
    tam.replace(video)


def render_canh(c, stock_dir: Path, out: Path, W, H, fps, tmp: Path, threads=2, zoom_profile=None):
    # Cảnh có thể lấy file từ thư mục KHÁC kho stock (ảnh tự vẽ) — `goc` ghi rõ ở từng cảnh thay
    # vì bắt render tự đoán, để `scenes.json` đọc lại vẫn dựng đúng.
    src = Path(c["goc"]) / c["file"] if c.get("goc") else stock_dir / c["file"]
    cap = (c.get("caption") or "").strip()
    if c["kieu"] == "still":
        # Ảnh tĩnh: Ken Burns nhẹ để không "chết hình" giữa loạt clip đang chuyển động.
        #
        # ẢNH BẰNG CHỨNG nhỏ hơn khung hoặc lệch tỉ lệ ⇒ dùng `blur` thay vì `cover`.
        # Lý do: bản đồ tuyến bay gốc trên Wikipedia chỉ 551×561 — không có bản lớn hơn, vì đó
        # CHÍNH LÀ tấm ảnh nguồn. `cover` sẽ phóng nó 3,5 lần cho lấp khung 1920×1080, vừa nhoè
        # vừa cắt mất rìa bản đồ, mà rìa bản đồ chính là thứ cần đọc. `blur` đặt nguyên tấm vào
        # giữa khung trên nền là chính nó phóng to làm mờ: không nhoè, không mất chữ, và trông
        # như dụng ý dàn dựng chứ không như lỗi.
        # Chỉ áp cho ẢNH BẰNG CHỨNG. B-roll thường vẫn `cover` — b-roll đã qua bộ lọc ≥720p, mà
        # để letterbox tràn lan thì video mất cảm giác liền mạch.
        fit = "cover"
        if c.get("bangchung"):
            try:
                from PIL import Image as _I
                w0, h0 = _I.open(src).size
                if w0 < W or h0 < H or not (1.55 <= w0 / max(h0, 1) <= 2.05):
                    fit = "blur"
            except Exception:
                pass
        zoom = (1.10 if fit == "cover" else 1.03) if zoom_profile is None else zoom_profile
        render_clip(src, c["dur"], W, H, fps, zoom,
                    zoom_in=(c["i"] % 2 == 0), out=out, threads=threads, fit=fit)
    else:
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={fps},setsar=1,format=yuv420p")
        subprocess.run([FF, "-y", "-ss", f"{c['vao']:.3f}", "-i", str(src),
                        "-t", f"{c['dur']:.3f}", "-vf", vf, "-an", "-r", str(fps),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                        "-threads", str(threads), str(out)],
                       check=True, capture_output=True)
    if cap:
        png = anh_caption(cap, W, H, tmp / f"cap{c['i']:05d}.png")
        phu_caption(out, png, H, threads)


def viet_credits(ke_hoach, ra: Path):
    dung = {}
    for c in ke_hoach:
        d = dung.setdefault(c["file"], {"n": 0, "license": c["license"], "credit": c["credit"],
                                        "title": c["title"]})
        d["n"] += 1
    dong = ["【出典 / Sources】", ""]
    for f, d in sorted(dung.items(), key=lambda x: -x[1]["n"]):
        dong.append(f"- {d['title'][:70]} — {d['credit'] or '—'} [{d['license']}] "
                    f"({d['n']} cảnh · {f})")
    ra.write_text("\n".join(dong) + "\n", encoding="utf-8")
    return len(dung)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="", help="id profile → lấy body.* và assemble.*")
    ap.add_argument("--slug", default="", help="thư mục tập (có voice.mp3/voice.srt), tự suy ra out")
    ap.add_argument("--stock", default="", help="kho tư liệu (mặc định theo profile.body.stock_dir)")
    ap.add_argument("--audio", default="")
    ap.add_argument("--srt", default="")
    ap.add_argument("--khong-chay-phu-de", action="store_true",
                    help="VẪN đọc .srt để hút mốc cắt, nhưng KHÔNG cháy chữ vào hình")
    ap.add_argument("--out", default="")
    ap.add_argument("--evidence", default="", help="JSON list [{at,file,caption,sec}]")
    ap.add_argument("--bgm", default="")
    ap.add_argument("--bgm-volume", type=float, default=0.10)
    ap.add_argument("--font", default="Meiryo")
    ap.add_argument("--sub-size", type=int, default=18, help="cỡ chữ phụ đề cháy (ASS FontSize)")
    ap.add_argument("--sub-margin", type=int, default=45, help="lề đáy phụ đề (ASS MarginV)")
    ap.add_argument("--sub-outline", type=int, default=2, help="độ dày viền chữ phụ đề")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--sec-min", type=float, default=0.0)
    ap.add_argument("--sec-max", type=float, default=0.0)
    ap.add_argument("--reuse-max", type=int, default=0)
    ap.add_argument("--gap", type=int, default=25, help="tối thiểu bao nhiêu cảnh mới được lặp file")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--plan-only", action="store_true", help="chỉ lập kế hoạch + credits, KHÔNG render")
    ap.add_argument("--min-height", type=int, default=0,
                    help="bỏ clip thấp hơn N pixel chiều cao (mặc định 720 — chống nhoè do upscale)")
    ap.add_argument("--license-policy", default="", choices=["", "pd", "permissive", "all"],
                    help="lọc giấy phép: pd (chỉ Public Domain) · permissive (PD+CC BY, mặc định, "
                         "BỎ SA/NC/ND) · all. Mặc định theo profile.body.license_policy")
    ap.add_argument("--anh-ai", default="",
                    help="thư mục ảnh tự vẽ (có img_meta*.json). Để trống = tự dò img_ai/ rồi "
                         "img_test/ trong thư mục tập")
    ap.add_argument("--khong-anh-ai", action="store_true", help="bỏ hẳn tầng ảnh tự vẽ")
    ap.add_argument("--toi-da-giay", type=float, default=0.0,
                    help="CHỈ dựng N giây đầu để xem thử. Ghi scenes_test.json/credits_test.txt, "
                         "KHÔNG đụng vào bản thật")
    ap.add_argument("--jobs", type=int, default=0)
    ap.add_argument("--clip-threads", type=int, default=2)
    args = ap.parse_args()

    body = {}
    prof = {}
    if args.profile:
        import profiles
        prof = profiles.load(args.profile)
        p = prof
        body = prof.get("body", {}) or {}
        if (body.get("mode") or "ai_images") != "stock_clips":
            print(f"  ! profile '{args.profile}' có body.mode={body.get('mode')} — file này dựng "
                  f"stock_clips, chạy tiếp theo yêu cầu.")
    slug = Path(args.slug) if args.slug else None
    audio = Path(args.audio) if args.audio else None
    srt = Path(args.srt) if args.srt else None
    if slug:
        audio = audio or (slug / "voice_paced.wav" if (slug / "voice_paced.wav").exists()
                          else slug / "voice.mp3")
        srt = srt or (slug / "voice_paced.srt" if (slug / "voice_paced.srt").exists()
                      else slug / "voice.srt")
    if not audio or not audio.exists():
        raise SystemExit("Cần --audio (hoặc --slug có voice.mp3)")
    out = Path(args.out) if args.out else (slug / "final.mp4" if slug else Path("final.mp4"))

    stock_dir = Path(args.stock or body.get("stock_dir") or "assets/stock")
    if not stock_dir.is_absolute():
        from paths import OUT_ROOT
        cand = Path(OUT_ROOT) / stock_dir
        stock_dir = cand if cand.exists() else stock_dir
    if not stock_dir.exists():
        raise SystemExit(f"Không thấy kho tư liệu: {stock_dir} (chạy stockfetch.py trước)")

    sec = body.get("seconds_per_scene") or [3.7, 5.0]
    lo = args.sec_min or float(sec[0])
    hi = args.sec_max or float(sec[1])
    reuse_max = args.reuse_max or int(body.get("reuse_max") or 6)
    rnd = random.Random(args.seed or None)

    chinh_sach = args.license_policy or body.get("license_policy") or "permissive"
    print(f"[kho] {stock_dir} · giấy phép: {chinh_sach}")
    vids, stills = nap_kho(stock_dir, chinh_sach=chinh_sach,
                           cam_tieu_de=body.get("title_blocklist") or (),
                           cao_toi_thieu=int(args.min_height or body.get("min_height") or 720),
                           sang_toi_thieu=float(body.get("min_luma") or 20.0))
    print(f"  → {len(vids)} clip + {len(stills)} ảnh dùng được")

    audio_len = media_seconds(audio)
    cues = parse_srt_cues(srt) if srt and srt.exists() else []
    canh = moc_cat(audio_len, cues, lo, hi, rnd)
    if args.toi_da_giay:
        # Cắt NGAY tại đây chứ không cắt ở khâu ghép cuối: mọi tầng chọn hình phía sau đều chạy
        # theo chỉ số cảnh, cắt sau là lệch bảng.
        gh = float(args.toi_da_giay)
        canh = [(t0, min(d, gh - t0)) for t0, d in canh if t0 < gh - 0.5]
        audio_len = canh[-1][0] + canh[-1][1] if canh else audio_len
        print(f"  ✂️ BẢN XEM THỬ: chỉ dựng {audio_len/60:.1f} phút đầu ({len(canh)} cảnh)")
    # Chọn clip THEO CHƯƠNG: mốc chương đọc từ chính lời đọc, từ khoá đọc từ stock_queries.txt.
    moc_ch, nhom_tk = [], []
    if slug:
        try:
            import publish_kit, storyboard
            sc_f = slug / "script.txt"
            cues3 = storyboard.parse_cues(srt) if srt and srt.exists() else []
            if sc_f.exists() and cues3:
                moc_ch = publish_kit._chuong_theo_marker(
                    prof, sc_f.read_text(encoding="utf-8"), cues3)
        except Exception as e:
            print(f"  ! không đọc được mốc chương ({type(e).__name__}: {e})")
        nhom_tk = doc_tu_khoa_theo_chuong(slug / "stock_queries.txt")
    cho_phep = chia_theo_chuong(canh, moc_ch, nhom_tk)
    # Khớp theo CÂU (mịn nhất) đè lên khớp theo chương. Cảnh nào không có đoạn lời tương ứng thì
    # giữ nguyên tập từ khoá của chương — hai tầng chứ không phải thay thế.
    khop = doc_khop_hinh(slug / "khop_hinh.json") if slug else []
    if khop:
        theo_cau = chia_theo_cau(canh, khop)
        co = sum(1 for x in theo_cau if x)
        cho_phep = [c if c else ch for c, ch in zip(theo_cau, cho_phep)]
        print(f"[chọn hình] bám CÂU: {co}/{len(canh)} cảnh có từ khoá riêng theo lời "
              f"({len(khop)} đoạn lời đã khớp)")
    if nhom_tk and moc_ch:
        print(f"[chọn hình] bám chương: {len(moc_ch)} mốc · {len(nhom_tk)} nhóm từ khoá "
              f"({'/'.join(str(len(n)) for n in nhom_tk)} từ khoá mỗi chương)")
    else:
        print("  ⚠️ KHÔNG bám chương được (thiếu mốc chương hoặc stock_queries chưa chia theo "
              "chương) → clip chọn NGẪU NHIÊN trong kho, hình dễ lạc lời")
    ke_hoach, pool = chon_nguon(canh, vids, stills, reuse_max, args.gap, rnd, cho_phep)
    # Dùng chung sổ đo `_probe.json` với nap_kho: mỗi khung đã soi thì tập sau khỏi soi lại.
    _cf = stock_dir / "_probe.json"
    _cache = json.loads(_cf.read_text(encoding="utf-8")) if _cf.exists() else {}
    nan_doan_toi(ke_hoach, stock_dir, _cache, nguong=float(body.get("min_luma") or 20.0))
    _cf.write_text(json.dumps(_cache, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.evidence:
        ev = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
        gan_at_theo_chuong(ev, prof, (slug / "script.txt") if slug else Path("script.txt"),
                           srt, audio_len)
        gan_bang_chung(ke_hoach, ev, stock_dir,
                       chinh_sach=body.get("evidence_license_policy") or "pd")
    # Ảnh tự vẽ đặt SAU bằng chứng: ảnh bằng chứng là tư liệu thật, không được thay bằng hình vẽ
    # (`gan_anh_ai` bỏ qua cảnh có `bangchung`).
    if not args.khong_anh_ai:
        thu_muc_ai = Path(args.anh_ai) if args.anh_ai else next(
            (slug / t for t in ("img_ai", "img_test") if slug and (slug / t).is_dir()), None)
        if thu_muc_ai:
            gan_anh_ai(ke_hoach, thu_muc_ai, body.get("ai_image_label") or NHAN_ANH_AI)

    nph = len(ke_hoach) / (audio_len / 60)
    print(f"[kế hoạch] {len(ke_hoach)} cảnh / {audio_len/60:.1f} phút = {nph:.1f} cắt/phút "
          f"(mục tiêu {body.get('cuts_per_min') or [12, 16]}) · dài TB "
          f"{audio_len/len(ke_hoach):.1f}s · {len({c['file'] for c in ke_hoach})} file khác nhau")
    ra_dir = out.parent
    ra_dir.mkdir(parents=True, exist_ok=True)
    # Bản xem thử ghi ra TÊN KHÁC. Đã một lần chạy `--plan-only` đè mất `scenes.json` thật rồi đo
    # nhầm trên bản đè — sổ của bản thật và sổ của bản nháp không được dùng chung một tên.
    hau = "_test" if args.toi_da_giay else ""
    (ra_dir / f"scenes{hau}.json").write_text(json.dumps(ke_hoach, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
    n_file = viet_credits(ke_hoach, ra_dir / f"credits{hau}.txt")
    print(f"  → scenes{hau}.json + credits{hau}.txt ({n_file} nguồn)")
    if args.plan_only:
        for c in ke_hoach[:8]:
            print(f"   {c['t0']:7.1f}s +{c['dur']:.1f}s  {c['kieu']:5s} {c['file'][:44]}")
        return 0

    # `render_canh()` từng HARDCODE zoom 1.10/1.03 cho ảnh tĩnh, bỏ qua hẳn `profile.assemble.zoom`
    # — kênh khai zoom=1.0 (muốn ảnh đứng yên) vẫn bị Ken Burns áp lên do code không đọc field này.
    # Đã vá 2026-09-21 (bài học "rung giật" của Lane A): zoom=1.0 (hoặc field vắng nếu không dùng
    # profile) ⇒ giữ đúng mức nhẹ cũ 1.10/1.03; profile khai zoom khác 1.0 (kể cả 1.0 tường minh)
    # thì DÙNG ĐÚNG con số đó cho mọi ảnh tĩnh, không phân biệt cover/blur nữa.
    asm = (prof.get("assemble", {}) or {}) if args.profile else {}
    zoom_still = asm.get("zoom") if "zoom" in asm else None
    W, H = (int(x) for x in args.size.split("x"))
    jobs = args.jobs or max(2, (__import__("os").cpu_count() or 4) // 3)
    tmp = Path(tempfile.mkdtemp(prefix="stock_"))
    clips = [tmp / f"s{i:05d}.mp4" for i in range(len(ke_hoach))]
    t0 = time.time()
    done, lock = [0], threading.Lock()

    def _one(i):
        render_canh(ke_hoach[i], stock_dir, clips[i], W, H, args.fps, tmp, args.clip_threads,
                    zoom_profile=zoom_still)
        with lock:
            done[0] += 1
            if done[0] % 10 == 0 or done[0] == len(ke_hoach):
                print(f"  cảnh {done[0]}/{len(ke_hoach)}", end="\r", flush=True)

    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        list(ex.map(_one, range(len(ke_hoach))))
    print(f"\n  → {len(ke_hoach)} cảnh trong {time.time()-t0:.0f}s ({jobs} luồng)")

    # Chuyển cảnh: mặc định cũ CẮT THẲNG 100% (transition="cut") giữa 350-450 cảnh/tập ~4,35s mỗi
    # cảnh — nhịp cắt dày đặc này là thứ anh gọi "rung giật" (không phải camera rung, mà nhịp edit
    # dồn dập không có gì đệm giữa 2 cảnh). "mix" (2026-09-21) gọi ĐÚNG skill `video-chuyen-canh`
    # (`them_chuyen_canh_vao_clip.py`, vendor vào pipeline/) — hoạt động trên chuỗi clip ĐÃ RENDER
    # SẴN (từng mảnh encode riêng rồi concat demuxer, KHÔNG dựng 1 filter_complex khổng lồ cho
    # 400+ input — an toàn ở quy mô này, xem docstring của script). "fade" (dip-to-black đơn giản,
    # có sẵn trong `build_silent_concat`) giữ làm phương án dự phòng nhẹ hơn nếu "mix" gặp sự cố.
    transition = asm.get("transition", "cut") if args.profile else "cut"
    silent = tmp / "silent.mp4"
    if transition == "mix":
        them_ccc = Path(__file__).resolve().parent / "them_chuyen_canh_vao_clip.py"
        ratio = str(asm.get("mix_ratio", 0.6))
        mix = str(asm.get("mix_blend", "0.55,0.35,0.10,0"))
        # KHÔNG truyền --srt/--audio ở đây — chữ cháy + mux tiếng vẫn để nguyên bước mux cuối của
        # chính stock_cut.py (đã tune đúng sub_size/margin/outline riêng của lane này); script này
        # chỉ lo phần chuyển cảnh, trả về video CÂM chưa phụ đề.
        cmd = [sys.executable, str(them_ccc), "--clips"] + [str(c) for c in clips] + [
            "--out", str(silent), "--ratio", ratio, "--mix", mix,
            "--jobs", str(jobs), "--threads", str(args.clip_threads)]
        subprocess.run(cmd, check=True)
    else:
        fade_each = float(asm.get("fade_each", 0.15)) if transition == "fade" else 0.0
        build_silent_concat(clips, silent, tmp, fade_each=fade_each, fps=args.fps)

    # Mux 1 lần: phụ đề cháy + giọng + nhạc nền.
    inputs = ["-i", str(silent.resolve()), "-i", str(audio.resolve())]
    if args.bgm:
        inputs += ["-stream_loop", "-1", "-i", str(Path(args.bgm).resolve())]
    fc, vmap, amap = [], "0:v", "1:a"
    # ⚠️ FILE .srt Ở ĐÂY PHỤC VỤ HAI VIỆC KHÁC HẲN NHAU:
    #   1. hút mốc cắt về ranh giới câu (`moc_cat`) — LUÔN cần, bỏ là hình lệch pha với lời;
    #   2. cháy chữ vào hình — có thể KHÔNG muốn.
    # Bản đầu gộp làm một: `--slug` là tự dò ra voice.srt rồi vừa hút mốc vừa cháy chữ. Nên tắt
    # phụ đề ở make_video (không truyền --srt) **không có tác dụng** — stock_cut vẫn tự tìm thấy
    # file, video vẫn ra chữ cháy, mà log không hề khác. Phải tách bằng cờ riêng.
    chay_sub = bool(srt and srt.exists() and not args.khong_chay_phu_de)
    # Ghi lại ĐÃ CHÁY CHỮ HAY CHƯA, để cổng B10 khỏi phải ĐOÁN từ điểm ảnh.
    # Đo ngược bằng pixel là không đáng tin: phép đo cũ đếm điểm sáng ở đáy khung, mà cảnh vũ trụ
    # có dải chân trời sáng cũng cho đúng con số ấy — tập 1 bị báo "vẫn thấy chữ 5/6 mốc" trong khi
    # cắt khung ra nhìn thì sạch trơn. Thứ tất định thì đừng đi suy đoán.
    (ra_dir / f"render_info{hau}.json").write_text(
        json.dumps({"burned_subs": chay_sub, "srt": srt.name if srt else None},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    if chay_sub:
        shutil.copy(srt, tmp / "subs.srt")
        # Cỡ chữ phụ đề LÀ MỘT THAM SỐ NGÁCH, không phải hằng số. Đo thật 2026-09-10 trên khung
        # hình kênh mẫu: 2-3 dòng, mỗi dòng cao 7,4-8,1% chiều cao khung, khối chữ 17-27%, mép
        # dưới cách đáy 4,3%. Mặc định cũ (18/45) ra 1 dòng cao 4,3%, đáy cách 16,5% — bằng NỬA
        # cỡ chữ của họ. Khớp lại bằng FontSize=32 + MarginV=7 (đo: 7,6% · 18,7% · 4,5%).
        style = (f"FontName={args.font},FontSize={args.sub_size},PrimaryColour=&H00FFFFFF,"
                 f"OutlineColour=&H00000000,BorderStyle=1,Outline={args.sub_outline},Shadow=1,"
                 f"MarginV={args.sub_margin},Alignment=2")
        fc.append(f"[0:v]subtitles=subs.srt:force_style='{style}'[v]")
        vmap = "[v]"
    if args.bgm:
        fc.append(f"[1:a]volume=1.0[na];[2:a]volume={args.bgm_volume}[bg];"
                  f"[na][bg]amix=inputs=2:duration=first:dropout_transition=3[a]")
        amap = "[a]"
    cmd = [FF, "-y"] + inputs
    if fc:
        cmd += ["-filter_complex", ";".join(fc)]
    cmd += ["-map", vmap, "-map", amap, "-c:a", "aac", "-b:a", "192k",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-shortest", str(out.resolve())]
    subprocess.run(cmd, check=True, capture_output=True, cwd=str(tmp))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✓ Video: {out} ({len(ke_hoach)} cảnh · {nph:.1f} cắt/phút)")
    print(f"  TỔNG: {(time.time()-t0)/60:.1f} phút")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
