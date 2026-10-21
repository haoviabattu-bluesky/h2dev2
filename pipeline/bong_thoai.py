# -*- coding: utf-8 -*-
r"""bong_thoai.py — hộp lời kể + BÓNG THOẠI có đuôi chỉ về người nói, chữ dọc 縦書き (Lane K, 2026-09-24).

Vì sao (docs/PHUONG_AN_LANE_K_DA_GIONG_BONG_THOAI.md §C5): kênh mẫu 千種テンカ hiện MỌI câu lên hình — lời kể
trong hộp chữ nhật trắng chữ dọc, lời thoại + câu nội tâm trong bóng tròn trắng có ĐUÔI chỉ vào miệng người nói
(khung gốc docs/channel_dna/yakkyoku-sukatto/_raw/video/khung/sheet_v1.png). AI vẽ chữ hay sai → ảnh cấm chữ,
máy vẽ bóng thoại sau. Khác tate_text.py (Lane F): hộp đặt ở CHỖ TRỐNG không đè mặt ai, bóng có đuôi theo người nói.

Ba việc:
  do_mat(slug, prof)   ảnh có @CAST → model thị giác (sol_client) trả hộp mặt + điểm miệng từng nhân vật
                       → img_faces.json (chạy 1 lần, resume được). Chạy ở MÁY 2 (ảnh vẽ ở đó), trước B8.
  render_cue(...)      1 câu → PNG RGBA 1920×1080 trong suốt (hộp hoặc bóng + chữ dọc).
  build_track(...)     mọi câu (voice_roles.json) × dòng thời gian ảnh (assemble) → 1 track .mov alpha,
                       assemble overlay đúng 1 filter như --tate.

Dùng thử offline (0đ ngoài vision):
  py -3.13 bong_thoai.py --faces <tập>          (chỉ chạy do_mat)
  py -3.13 bong_thoai.py --demo <ảnh.png> --text 「…」 --faces-json <img_faces.json> --speaker shu --out x.png
"""
import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cau_vai     # noqa: E402
import tate_text   # noqa: E402  (load_font + FF dùng chung)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NHO = set("ゃゅょぁぃぅぇぉっャュョァィゥェォッヮゎ")        # chữ nhỏ: lệch lên-phải trong ô dọc
DAU = set("、。，．")                                         # dấu câu: góc trên-phải ô
XOAY = set("ー―〜～…‥（）()「」『』")                        # xoay 90° khi viết dọc
TRO_TU = set("はがをにでともへやねよかのて")                  # ngắt cột sau trợ từ nếu tiện


# ---------------------------------------------------------------- 1) định vị mặt
def _cast_cua_anh(slug):
    """img_prompts.txt → {"001.png": [ids]} cho dòng @CAST."""
    pf = Path(slug) / "img_prompts.txt"
    out = {}
    if not pf.exists():
        return out
    lines = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
    for i, l in enumerate(lines, 1):
        m = re.match(r"^\s*@cast:([A-Za-z0-9_,\-]+)\s", l, re.I)
        if m:
            out[f"{i:03d}.png"] = [x for x in m.group(1).split(",") if x]
    return out


def _json(txt):
    t = re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", t, re.S)
    return json.loads(m.group(0)) if m else None


def _anh_luoi(anh):
    """Ảnh 1920×1080 kẻ lưới 10% có ghi số → file tạm. Đo thật ep01 (2026-09-24): hỏi toạ độ 0–1 trên ảnh
    trần, model lệch tới ~20% chiều ngang (005.png: mặt cô part trả ở 0,58–0,70, thật ở 0,72–0,86 → hộp
    lời kể đè mặt); có lưới để 'đọc' thì 3/3 ảnh thử khớp mặt thật."""
    im = Image.open(anh).convert("RGB").resize((1920, 1080))
    d = ImageDraw.Draw(im)
    font = tate_text.load_font("ms gothic", 28)
    for k in range(1, 10):
        x, y = k * 192, k * 108
        d.line([(x, 0), (x, 1080)], fill=(255, 0, 0), width=2)
        d.text((x + 4, 4), str(k * 10), fill=(255, 0, 0), font=font)
        d.line([(0, y), (1920, y)], fill=(0, 0, 255), width=2)
        d.text((4, y + 4), str(k * 10), fill=(0, 0, 255), font=font)
    fd, f = tempfile.mkstemp(suffix=".jpg", prefix="luoi_")
    import os
    os.close(fd)
    f = Path(f)
    im.save(f, quality=90)
    return f


def _hoi_anh(anh, ids, chars):
    import sol_client
    ds = "\n".join(f"- {i}: {chars.get(i, {}).get('look', '')}" for i in ids)
    q = ("Ảnh minh hoạ manga, đã kẻ lưới: vạch ĐỎ dọc ghi % chiều ngang (10..90), vạch XANH ngang ghi % chiều dọc. "
         "Các nhân vật có thể xuất hiện (id: ngoại hình):\n" + ds +
         "\nVới MỖI người nhìn thấy MẶT trong ảnh: nếu khớp một id ở trên thì ghi id đó, không khớp thì id = \"khac\". "
         "Trả hộp MẶT (gồm cả tóc) và điểm MIỆNG theo % (0–100), đọc theo lưới cho chính xác. "
         "Trả ĐÚNG 1 JSON, không giải thích: {\"nguoi\":[{\"id\":\"...\",\"mat\":[x1,y1,x2,y2],\"mieng\":[x,y]}]}")
    luoi = _anh_luoi(anh)
    try:
        r = sol_client.chat(q, image_path=str(luoi), max_tokens=700)
    finally:
        luoi.unlink(missing_ok=True)
    r = r[0] if isinstance(r, tuple) else r
    j = _json(r if isinstance(r, str) else getattr(r, "text", str(r)))
    for p in (j or {}).get("nguoi") or []:          # % → 0–1 (định dạng img_faces.json giữ nguyên)
        for k in ("mat", "mieng"):
            if isinstance(p.get(k), list):
                p[k] = [max(0.0, min(1.0, float(v) / 100)) for v in p[k]]
    return j


def do_mat(slug, workers=6):
    d = Path(slug)
    out_f = d / "img_faces.json"
    kq = json.loads(out_f.read_text(encoding="utf-8")) if out_f.exists() else {}
    chars = {c["id"]: c for c in json.loads((d / "characters.json").read_text(encoding="utf-8")).get("characters", [])}
    cast = _cast_cua_anh(d)
    # Đo MỌI ảnh, không chỉ ảnh @CAST: ảnh "cảnh vật" vẫn có người qua đường/bệnh nhân (ep01 giây 300: hộp
    # lời kể đè cô y tá vì ảnh đó không khoá mặt nên chưa từng được đo) → id "khac".
    tat_ca = {p.name: cast.get(p.name, []) for p in sorted((d / "img").glob("[0-9][0-9][0-9].png"))}
    viec = [(n, ids) for n, ids in tat_ca.items() if n not in kq]
    print(f"[bong_thoai] định vị mặt: {len(viec)} ảnh cần hỏi · {len(kq)} đã có")

    def _mot(x):
        n, ids = x
        for _ in range(2):
            try:
                j = _hoi_anh(d / "img" / n, ids, chars)
                if j and isinstance(j.get("nguoi"), list):
                    return n, j["nguoi"]
            except Exception as e:
                print(f"  ! {n}: {type(e).__name__} {str(e)[:80]}")
        return n, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for n, ng in ex.map(_mot, viec):
            if ng is not None:
                kq[n] = ng
    out_f.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    thieu = [n for n, _ in viec if n not in kq]
    print(f"[bong_thoai] ✓ img_faces.json {len(kq)} ảnh" + (f" · ⚠️ {len(thieu)} ảnh không định vị được: {thieu[:8]}" if thieu else ""))
    return kq


def do_mat_ds(viec, chars, out_f, workers=6):
    """Định vị mặt cho 1 danh sách ảnh bất kỳ (vd ảnh hook): viec = {khoá: (đường_dẫn_ảnh, [ids])} → ghi out_f.
    Dùng cho đoạn hook (ghep_hook_noi_truoc.py) — ảnh hook không nằm trong img/ + img_prompts.txt của thân."""
    out_f = Path(out_f)
    kq = json.loads(out_f.read_text(encoding="utf-8")) if out_f.exists() else {}
    lam = [(k, p, ids) for k, (p, ids) in viec.items() if k not in kq and Path(p).exists()]

    def _mot(x):
        k, p, ids = x
        for _ in range(2):
            try:
                j = _hoi_anh(p, ids, chars)
                if j and isinstance(j.get("nguoi"), list):
                    return k, j["nguoi"]
            except Exception as e:
                print(f"  ! {k}: {type(e).__name__} {str(e)[:80]}")
        return k, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for k, ng in ex.map(_mot, lam):
            if ng is not None:
                kq[k] = ng
    out_f.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    return kq


# ---------------------------------------------------------------- 2) xếp chữ dọc
def chia_cot(text, max_chu, max_cot):
    """Cắt chuỗi thành cột ≤ max_chu, ưu tiên ngắt sau dấu câu/trợ từ trong 4 ký tự cuối cột;
    không để dấu câu hay chữ nhỏ đứng đầu cột. Quá tải → thu thêm cột (người gọi tự giảm cỡ chữ)."""
    t = list(text.strip())
    cols, i = [], 0
    while i < len(t):
        j = min(i + max_chu, len(t))
        if j < len(t):
            best = None
            for k in range(j, max(i + max_chu - 4, i + 1) - 1, -1):
                if t[k - 1] in DAU or t[k - 1] in "！？!?":
                    best = k
                    break
                if best is None and t[k - 1] in TRO_TU and k < len(t) and t[k] not in TRO_TU:
                    best = k
            j = best or j
            while j < len(t) and (t[j] in DAU or t[j] in NHO or t[j] in "ー」』！？") and j - i < max_chu + 1:
                j += 1
        cols.append(t[i:j])
        i = j
    return cols


def _ve_chu_doc(img, cols, x_phai, y_tren, font, cell, fill=(20, 20, 20, 255), vien=0):
    """fill = 1 màu, HOẶC danh sách màu theo từng cột/từng chữ (cùng dáng `cols`) — thumbnail Lane K tô đỏ vài cụm
    (YT-TITLE-RESEARCH thumbnail_engine/dialogue_split.py dùng lại hàm này, không chép code).
    vien = số px viền CÙNG MÀU chữ quanh nét (assemble.bubble.stroke_chu, Lane N 2026-09-30: chữ đậm hơn Lane M);
    0 = như cũ."""
    d = ImageDraw.Draw(img)
    for ci, col in enumerate(cols):
        cx = x_phai - cell * ci - cell / 2
        for ri, ch in enumerate(col):
            mau = fill[ci][ri] if isinstance(fill, list) else fill
            cy = y_tren + cell * ri + cell / 2
            if ch in XOAY:
                tmp = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
                td = ImageDraw.Draw(tmp)
                bb = td.textbbox((0, 0), ch, font=font)
                td.text((cell / 2 - (bb[2] - bb[0]) / 2 - bb[0], cell / 2 - (bb[3] - bb[1]) / 2 - bb[1]), ch,
                        font=font, fill=mau, stroke_width=vien, stroke_fill=mau)
                tmp = tmp.rotate(-90)
                img.alpha_composite(tmp, (int(cx - cell / 2), int(cy - cell / 2)))
                continue
            bb = d.textbbox((0, 0), ch, font=font)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            dx, dy = 0, 0
            if ch in DAU:
                dx, dy = cell * 0.30, -cell * 0.30
            elif ch in NHO:
                dx, dy = cell * 0.10, -cell * 0.08
            d.text((cx - tw / 2 - bb[0] + dx, cy - th / 2 - bb[1] + dy), ch, font=font, fill=mau,
                   stroke_width=vien, stroke_fill=mau)


# ---------------------------------------------------------------- 3) đặt khung
def _cham(a, b, pad=0):
    return not (a[2] + pad < b[0] or a[0] - pad > b[2] or a[3] + pad < b[1] or a[1] - pad > b[3])


def _dat(W, H, bw, bh, mats, dich=None):
    """Tìm chỗ đặt hộp bw×bh không đè hộp mặt nào; có `dich` (miệng người nói) thì gần miệng nhất nhưng
    cách ≥ 180px để đuôi không cụt; không có thì ưu tiên nửa phải trên (giống khung gốc)."""
    le = 30
    tot = None
    for x in range(le, W - bw - le + 1, 24):
        for y in range(le, H - bh - le + 1, 24):
            box = [x, y, x + bw, y + bh]
            if any(_cham(box, m, 18) for m in mats):
                continue
            cx, cy = x + bw / 2, y + bh / 2
            if dich:
                kc = math.hypot(cx - dich[0], cy - dich[1])
                if kc < 180:
                    continue
                diem = kc + 0.15 * y
            else:
                diem = abs(cx - W * 0.72) + 0.5 * abs(y - H * 0.08)
            if tot is None or diem < tot[0]:
                tot = (diem, box)
    return tot[1] if tot else None


def _than(m, H):
    """Hộp mặt → vùng THÂN NGƯỜI ước lượng (vision chỉ trả mặt): rộng thêm 35% mỗi bên, kéo xuống đáy khung."""
    w = m[2] - m[0]
    return [m[0] - 0.35 * w, m[1], m[2] + 0.35 * w, H]


def _giao(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


def _dat_mep(W, H, bw, bh, mats, le=24):
    """Hộp lời kể SÁT MÉP (anh chốt 2026-09-24 sau khi xem ep01: hộp giữa khung che mặt): ưu tiên mép PHẢI,
    mép phải có người (thân ước lượng từ mặt) thì sang mép TRÁI; hai mép đều có người → mép nào đè thân ít hơn.
    Mặt thì tuyệt đối không đè: trượt hộp xuống dần tới chỗ hết đè mặt."""
    thans = [_than(m, H) for m in mats]
    ung = []
    for uu, x in enumerate((W - bw - le, le)):              # 0 = phải, 1 = trái
        for y in range(le, H - bh - le + 1, 12):
            box = [x, y, x + bw, y + bh]
            if any(_cham(box, m, 18) for m in mats):
                continue
            ung.append((sum(_giao(box, t) for t in thans), uu, y, box))
            break
    if not ung:
        return None
    return min(ung)                                   # (diện tích đè thân, 0 phải/1 trái, y, hộp)


def render_cue(text, la_loi_ke, W, H, mats, mieng=None, font_name="Yu Gothic", size=40, max_chu=11, max_cot=3, duoi=True,
               dang="bo_goc", vien=0):
    """→ ảnh RGBA. la_loi_ke: hộp chữ nhật; ngược lại: bóng tròn + đuôi (mieng=None → đuôi chỉ ra mép gần nhất).
    duoi=False (assemble.bubble.tail=false, Lane L 2026-09-24): bóng oval KHÔNG đuôi như kênh mẫu 社会のウラガワ,
    vẫn đặt gần miệng người nói.
    dang="elip" (assemble.bubble.shape_thoai, Lane N 2026-09-30): bóng thoại ELIP có ĐUÔI chỉ về người nói
    (dang="bo_goc" = hình chữ nhật bo góc của Lane K, mặc định). vien = viền chữ (px) cho chữ đậm hơn."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chu = cau_vai.bo_ngoac(text)
    for sz in (size, int(size * 0.88), int(size * 0.78)):
        font = tate_text.load_font(font_name, sz)
        cell = int(sz * 1.18)
        cols = chia_cot(chu, max_chu, max_cot)
        if len(cols) <= max_cot + 1:
            break
    pad = int(sz * (0.55 if la_loi_ke else 0.9))
    bw = len(cols) * cell + pad * 2
    bh = max(len(c) for c in cols) * cell + pad * 2
    oval = (not la_loi_ke) and (not duoi or dang == "elip")
    if oval and dang == "elip":
        # Lane N (2026-09-30, đo demo): 2 cột × 10 chữ → elip cao 1000px hẹp như chiếc lá, không đặt được gần người
        # nói → chọn số chữ/cột cho khối chữ gần VUÔNG (cao/rộng ≈ 1,15) để elip tròn trịa.
        tot = None
        for mc in range(max(4, max_chu), 3, -1):
            cc = chia_cot(chu, mc, 99)
            tl = (max(len(c) for c in cc)) / len(cc)
            if len(cc) <= max_cot + 3 and (tot is None or abs(tl - 1.15) < tot[0]):
                tot = (abs(tl - 1.15), cc)
        if tot:
            cols = tot[1]
    if oval:
        # Lane L ep01 (2026-09-24): bóng oval không đuôi — elip NGOẠI TIẾP khối chữ (×√2 mỗi chiều), không phải
        # hình viên thuốc: câu dài 7 cột thì góc khối chữ lòi ra ngoài đường cong (đo thật giây 700).
        tw, th = len(cols) * cell, max(len(c) for c in cols) * cell
        bw, bh = int(tw * 1.42) + 20, int(th * 1.42) + 20
    if la_loi_ke:
        # Hộp cao quá không lọt khe giữa mặt và mép (ep01 005.png cỡ 64: cả 2 mép đều vướng mặt → rơi vào
        # góc trên phải đè mặt) → thử thêm dáng hộp THẤP hơn (cột ngắn, nhiều cột). Chọn: không đè mặt,
        # đè thân ít nhất, rồi dáng gốc trước, mép phải trước.
        tot = None
        for dang, mc in enumerate(dict.fromkeys((max_chu, max(5, round(max_chu * 0.72)), max(4, round(max_chu * 0.5))))):
            cc = chia_cot(chu, mc, 99)
            w_, h_ = len(cc) * cell + pad * 2, max(len(c) for c in cc) * cell + pad * 2
            if w_ > W * 0.45:
                continue
            kq = _dat_mep(W, H, w_, h_, mats)
            if kq and (tot is None or (kq[0], dang, kq[1]) < tot[0]):
                tot = ((kq[0], dang, kq[1]), kq[3], cc)
        box = None
        if tot:
            _, box, cols = tot
            bw, bh = box[2] - box[0], box[3] - box[1]
    else:
        box = _dat(W, H, bw, bh, mats, mieng)
    if box is None:                                    # hết chỗ trống → sát góc trên phải, chấp nhận đè
        box = [W - bw - 24, 24, W - 24, 24 + bh]
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    den, trang = (25, 25, 25, 255), (255, 255, 255, 245)
    if la_loi_ke:
        d.rectangle([x0, y0, x1, y1], fill=trang, outline=den, width=3)
    elif oval:
        if duoi:                                       # elip CÓ đuôi (Lane N): đuôi vẽ trước, elip đè lên gốc đuôi
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            tx, ty = mieng if mieng else ((W + 60 if cx > W / 2 else -60), cy)
            goc = math.atan2(ty - cy, tx - cx)
            a_, b_ = bw / 2, bh / 2                    # điểm trên viền elip theo hướng `goc`
            r = a_ * b_ / math.hypot(b_ * math.cos(goc), a_ * math.sin(goc)) - 4
            bx, by = cx + math.cos(goc) * r, cy + math.sin(goc) * r
            dai = min(math.hypot(tx - bx, ty - by) * 0.62, max(110, sz * 3.2))   # đuôi ngắn gọn, không vắt ngang khung
            ex, ey = bx + math.cos(goc) * dai, by + math.sin(goc) * dai
            vg = goc + math.pi / 2
            rong = max(16, int(sz * 0.5))
            de = [(bx + math.cos(vg) * rong, by + math.sin(vg) * rong), (bx - math.cos(vg) * rong, by - math.sin(vg) * rong)]
            d.polygon([de[0], (ex, ey), de[1]], fill=den)
            d.ellipse([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=den)
            vao = [(de[0][0] + (bx - de[0][0]) * 0.28, de[0][1] + (by - de[0][1]) * 0.28),
                   (ex - math.cos(goc) * 6, ey - math.sin(goc) * 6),
                   (de[1][0] + (bx - de[1][0]) * 0.28, de[1][1] + (by - de[1][1]) * 0.28)]
            d.polygon(vao, fill=trang)
            d.ellipse([x0, y0, x1, y1], fill=trang)
        else:
            d.ellipse([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=den)
            d.ellipse([x0, y0, x1, y1], fill=trang)
        _ve_chu_doc(img, cols, x1 - (bw - tw) / 2, y0 + (bh - th) / 2, font, cell, vien=vien)
        return img
    else:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if mieng:
            tx, ty = mieng
        else:                                          # người nói ngoài khung → đuôi ra mép gần nhất
            tx, ty = (W + 60 if cx > W / 2 else -60), cy
        goc = math.atan2(ty - cy, tx - cx)
        # gốc đuôi nằm trên viền bóng, mũi đuôi dừng cách miệng 30%
        r = min(bw, bh) / 2 - 6
        bx, by = cx + math.cos(goc) * r, cy + math.sin(goc) * r
        ex, ey = bx + (tx - bx) * 0.62, by + (ty - by) * 0.62
        vg = goc + math.pi / 2
        rong = max(16, int(sz * 0.5))
        de = [(bx + math.cos(vg) * rong, by + math.sin(vg) * rong), (bx - math.cos(vg) * rong, by - math.sin(vg) * rong)]
        bo = int(min(bw, bh) * 0.45)
        d.polygon([de[0], (ex, ey), de[1]], fill=den)
        d.rounded_rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], radius=bo + 3, fill=den)
        d.rounded_rectangle([x0, y0, x1, y1], radius=bo, fill=trang)
        vao = [(de[0][0] + (bx - de[0][0]) * 0.28, de[0][1] + (by - de[0][1]) * 0.28),
               (ex - math.cos(goc) * 6, ey - math.sin(goc) * 6),
               (de[1][0] + (bx - de[1][0]) * 0.28, de[1][1] + (by - de[1][1]) * 0.28)]
        d.polygon(vao, fill=trang)
        # lấp lại phần đuôi lấn vào trong bóng
        d.rounded_rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], radius=max(1, bo - 4), fill=trang)
    _ve_chu_doc(img, cols, x1 - pad, y0 + pad, font, cell, vien=vien)
    return img


def _mats_px(faces, W, H):
    return [[f["mat"][0] * W, f["mat"][1] * H, f["mat"][2] * W, f["mat"][3] * H] for f in (faces or []) if f.get("mat")]


def _mieng_cua(faces, vai, W, H):
    for f in faces or []:
        if f.get("id") == vai and f.get("mieng"):
            return (f["mieng"][0] * W, f["mieng"][1] * H)
    return None


# ---------------------------------------------------------------- 4) dựng track
def tach_loi_ke(c, lim, ca_thoai=False):
    """1 cue lời kể dài > lim chữ → n phần gần bằng nhau, cắt ở dấu 、。 (không có thì sau trợ từ) gần điểm chia
    nhất; thời gian chia theo tỉ lệ số chữ. Thoại「」mặc định không tách; ca_thoai=True (assemble.bubble.
    thoai_split_chars, Lane L ep01 2026-09-24) thì thoại dài cũng tách thành nhiều bóng nối tiếp — không thì
    câu thoại 70 chữ bị ép nhỏ còn 78% cỡ chữ (đo thật: bóng của 森 giây 150 chữ ~37px)."""
    t = cau_vai.bo_ngoac(c["text"]) if (ca_thoai and c.get("vai") != cau_vai.KE) else c["text"]
    if (c.get("vai") != cau_vai.KE and not ca_thoai) or len(t) <= lim:
        return [c]
    n = math.ceil(len(t) / lim)
    cat, dau = [], 0
    for k in range(1, n):
        muc = round(len(t) * k / n)
        tot = None
        for j in range(max(dau + 4, muc - 8), min(len(t) - 3, muc + 9)):
            diem = abs(j - muc) + (0 if t[j - 1] in DAU else 3 if t[j - 1] in TRO_TU else 99)
            if t[j] in DAU or t[j] in NHO or t[j] in "ー」』！？":
                continue
            if tot is None or diem < tot[0]:
                tot = (diem, j)
        j = tot[1] if tot else muc
        cat.append(j)
        dau = j
    moc = [0] + cat + [len(t)]
    ra, dai = [], c["end"] - c["start"]
    for a, b in zip(moc, moc[1:]):
        x = dict(c)
        x["text"] = t[a:b]
        x["start"] = c["start"] + dai * a / len(t)
        x["end"] = c["start"] + dai * b / len(t)
        ra.append(x)
    return ra



def build_track(roles_json, timeline, faces_json, out_path, W=1920, H=1080, fps=30, cfg=None, total_dur=None, tmp_dir=None):
    """timeline: list (tên_ảnh, t_start, t_end) — đúng dòng thời gian assemble dùng (anchor_durations)."""
    cfg = cfg or {}
    cues = json.loads(Path(roles_json).read_text(encoding="utf-8"))
    faces = json.loads(Path(faces_json).read_text(encoding="utf-8")) if faces_json and Path(faces_json).exists() else {}
    tmp = Path(tmp_dir) if tmp_dir else Path(tempfile.mkdtemp(prefix="bt_"))
    tmp.mkdir(parents=True, exist_ok=True)

    def _anh_luc(t):
        for n, a, b in timeline:
            if a <= t < b:
                return n
        return timeline[-1][0] if timeline else None

    # Lời kể dài → tách thành nhiều hộp nối tiếp (anh chốt 2026-09-24): mỗi hộp gọn ≤ `ke_split_chars` chữ,
    # thời gian chia theo số chữ (≈ nhịp đọc) — câu 8s hai nửa đều nhau thì mỗi nửa ~4s.
    lim = int(cfg.get("ke_split_chars", 0) or 0)
    if lim:
        cues = [p for c in cues for p in tach_loi_ke(c, lim)]
    lim_t = int(cfg.get("thoai_split_chars", 0) or 0)
    if lim_t:
        cues = [p for c in cues for p in (tach_loi_ke(c, lim_t, ca_thoai=True) if c.get("vai") != cau_vai.KE else [c])]
    # đoạn trống giữa các câu vẫn phải có khung (clip trong suốt) để track khớp thời gian
    doan, t = [], 0.0
    for c in cues:
        if c["start"] > t + 0.01:
            doan.append((None, c["start"] - t))
        doan.append((c, c["end"] - c["start"]))
        t = c["end"]
    if total_dur and total_dur > t + 0.01:
        doan.append((None, total_dur - t))
    trong = tmp / "trong.png"
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(trong)
    clips = []
    for k, (c, dur) in enumerate(doan):
        if c is None:
            png = trong
        else:
            n = _anh_luc((c["start"] + c["end"]) / 2)
            fs = faces.get(n) or []
            ke = c.get("vai") == cau_vai.KE
            co = cfg.get("font_size_ke" if ke else "font_size_thoai") or cfg.get("font_size", 40)
            img = render_cue(c["text"], ke, W, H, _mats_px(fs, W, H), None if ke else _mieng_cua(fs, c["vai"], W, H),
                             cfg.get("font", "Yu Gothic"), int(co),
                             int(cfg.get("max_chars_per_col_ke" if ke else "max_chars_per_col", 0)
                                 or cfg.get("max_chars_per_col", 11)), int(cfg.get("max_cols", 3)),
                             duoi=bool(cfg.get("tail", True)), dang=cfg.get("shape_thoai", "bo_goc"),
                             vien=int(cfg.get("stroke_chu", 0) or 0))
            png = tmp / f"bt_{k:05d}.png"
            img.save(png)
        clip = tmp / f"bt_{k:05d}.mov"
        subprocess.run([tate_text.FF, "-y", "-loglevel", "error", "-loop", "1", "-i", str(png), "-t", f"{max(dur, 0.04):.3f}",
                        "-pix_fmt", "argb", "-c:v", "qtrle", "-r", str(fps), str(clip)], check=True)
        clips.append(clip)
    lst = tmp / "bt_list.txt"
    lst.write_text("\n".join(f"file '{p.resolve().as_posix()}'" for p in clips), encoding="utf-8")
    subprocess.run([tate_text.FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out_path)], check=True)
    n_ke = sum(1 for c in cues if c.get("vai") == cau_vai.KE)
    print(f"[bong_thoai] {len(cues)} câu ({n_ke} hộp lời kể · {len(cues) - n_ke} bóng thoại) → {out_path}")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--faces", default="", help="thư mục tập: chạy định vị mặt → img_faces.json")
    ap.add_argument("--demo", default="", help="ảnh nền để vẽ thử 1 câu")
    ap.add_argument("--text", default="")
    ap.add_argument("--faces-json", default="")
    ap.add_argument("--speaker", default="ke")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    if a.faces:
        do_mat(a.faces)
    if a.demo:
        W, H = 1920, 1080
        nen = Image.open(a.demo).convert("RGBA").resize((W, H))
        fs = (json.loads(Path(a.faces_json).read_text(encoding="utf-8")).get(Path(a.demo).name) if a.faces_json else []) or []
        ke = a.speaker == cau_vai.KE
        lop = render_cue(a.text, ke, W, H, _mats_px(fs, W, H), None if ke else _mieng_cua(fs, a.speaker, W, H))
        nen.alpha_composite(lop)
        nen.convert("RGB").save(a.out)
        print("→", a.out)


if __name__ == "__main__":
    main()
