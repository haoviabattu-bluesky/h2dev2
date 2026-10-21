# -*- coding: utf-8 -*-
r"""chu_dao_cu.py — CHÈN CHỮ lên đạo cụ trong ẢNH HOOK TRƯỚC KHI SINH CLIP GROK (anh chốt 10/10/2026, mọi lane).

Ảnh AI (gpti2/ima2) vẽ giấy tờ/biển/màn hình TRƠN (chữ AI = chữ lạ, méo). Ở cảnh mà chữ trên đạo cụ là điểm nhấn (婚姻届,
退職届, 売家 看板, 通帳 số dư, tin nhắn LINE, biên bản có tên…) máy 1 chèn chữ bằng code vào ẢNH (`hook\img\NNN.png`),
rồi MỚI sinh clip Grok từ ảnh đã có chữ. Grok làm méo chữ trong clip = giới hạn của Grok, không phải lỗi khâu này (anh chốt).
Luật: docs/QUY_TAC_CHU_TREN_DAO_CU_HOOK.md

Khai ở `<tập>\hook\chu_tren_vat.json`:
  {"anh": [{"img": "028.png", "vat": [{"goc": [[x,y]×4 TRÁI-TRÊN, PHẢI-TRÊN, PHẢI-DƯỚI, TRÁI-DƯỚI, toạ độ 0–1 trên ảnh],
                                       "mau": "giay_to|bien|phong_bi|man_hinh|nhan", "tieu_de": "退職面談記録",
                                       "dong": ["氏名　菊池 美羽"], "dau": "施設長"?, "doc"?, "font"?, "mau_chu"?, "tron"?}]}],
   "bo_qua": {"028.png": "lý do không cần chữ"}}
Ảnh gốc trơn cất ở `hook\img\_goc\` (chạy lại luôn đi từ bản gốc); ảnh soi trước|sau ở `hook\chu\`. Prompt Grok của ảnh
đã chèn (grok_jobs.csv) tự đổi "no text" → giữ nguyên chữ in sẵn + máy quay gần như đứng yên.

  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập> --nhap        # ảnh nghi có chữ
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập> --tim 028     # dò mặt phẳng
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập> [--chi 028]   # chèn + soi
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập> --kiem        # cổng
"""
import argparse
import csv
import io
import json
import re
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
FONT_DIR = [HERE / "the_ten_mau" / "fonts", Path(r"C:\Users\admin\.claude\skills\motion_graphics\assets\fonts")]
FONTS = {"SM": "ShipporiMinchoB1-ExtraBold.ttf", "NJ": "NotoSansJP.ttf", "MR": "MPLUSRounded1c-Black.ttf"}
# đạo cụ hay mang chữ trọng tâm (lời hook + ky_vong) → --nhap/--kiem hỏi "cảnh này có cần chữ không"
TU_KHOA = re.compile(r"(?<![-\w])(?:document|form|certificate|notice|letter|envelope|signboard|for sale|placard|passbook|"
                     r"bank book|contract|screen|smartphone|monitor|message|report|record sheet|name tag|nameplate|"
                     r"receipt|invoice|label|poster)s?\b|届|書類|記録|契約|通帳|残高|請求|通知|診断書|看板|売家|貸家|売り物件|張り紙|貼り紙|手紙|封筒|遺言|名札|"
                     r"画面|LINE|メッセージ|メール|領収|明細|辞令|退職|離婚|婚姻|表彰|賞状|"
                     r"giấy|biên bản|hợp đồng|phong bì|lá thư|bức thư|biển|bảng|màn hình|tin nhắn|sổ tiết kiệm|hoá đơn|đơn ")   # KHÔNG re.I: "LINE" (ứng dụng) ≠ "line"; (?<![-\w]) bỏ "off-screen"/"on-screen name card"
W_CANVAS = 1600


# ───────────────────────────── dựng tờ chữ phẳng ─────────────────────────────
def _font(ten, size, dam="Bold"):
    f = next((d / FONTS[ten] for d in FONT_DIR if (d / FONTS[ten]).exists()), None)
    if not f:
        raise SystemExit(f"✗ thiếu font {FONTS[ten]}")
    ft = ImageFont.truetype(str(f), max(8, int(size)))
    if ten == "NJ":
        try:
            ft.set_variation_by_name(dam)
        except Exception:
            pass
    return ft


def _vua(draw, text, ten, max_w, max_h, start, dam="Bold"):
    s = int(start)
    while s > 8:
        ft = _font(ten, s, dam)
        x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=ft)
        if x1 - x0 <= max_w and y1 - y0 <= max_h:
            return ft
        s = int(s * 0.92)
    return _font(ten, 8, dam)


def _mau(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def _doc_chu(draw, cx, top, text, ft, fill, buoc):
    """Chữ dọc 1 cột (PIL không có vertical): xếp từng ký tự, ー/～ xoay bằng ký tự dọc tương đương."""
    y = top
    for ch in text:
        ch = {"ー": "︱", "～": "︴", "、": "︑", "。": "︒", "（": "︵", "）": "︶", "「": "﹁", "」": "﹂"}.get(ch, ch)
        x0, y0, x1, y1 = draw.textbbox((0, 0), ch, font=ft)
        draw.text((cx - (x1 - x0) / 2 - x0, y - y0), ch, font=ft, fill=fill)
        y += buoc


def _dau(draw, cx, cy, r, text, mau="#c62828"):
    """Con dấu tròn đỏ 印 (1–3 chữ dọc)."""
    c = _mau(mau, 235)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=max(3, int(r * 0.12)))
    t = text[:3]
    ft = _font("SM", r * 1.5 / max(1, len(t)))
    _doc_chu(draw, cx, cy - r * 0.75, t, ft, c, r * 1.5 / max(1, len(t)))


def dung_to_chu(v, ti_le):
    """Trả RGBA W_CANVAS × W_CANVAS*ti_le: nền trong suốt, chữ/nét = mực."""
    w = W_CANVAS
    h = int(w * ti_le)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    mau = v.get("mau", "giay_to")
    ink = _mau(v.get("mau_chu") or {"bien": "#c62828", "man_hinh": "#111111"}.get(mau, "#1d1d1d"))
    tieu = str(v.get("tieu_de") or "")
    dong = [str(x) for x in v.get("dong") or []]
    m = int(w * 0.08)
    if mau == "giay_to":
        ft = _vua(dr, tieu, v.get("font") or "SM", w - 2 * m, h * 0.1, w * 0.085)
        x0, y0, x1, y1 = dr.textbbox((0, 0), tieu, font=ft)
        y = int(h * 0.07)
        dr.text(((w - (x1 - x0)) / 2 - x0, y - y0), tieu, font=ft, fill=ink)
        y += (y1 - y0) + int(h * 0.03)
        dr.line([(m, y), (w - m, y)], fill=ink, width=max(2, int(w * 0.004)))
        y += int(h * 0.04)
        if dong:
            fl = _vua(dr, max(dong, key=len), "NJ", w - 2 * m, h * 0.06, w * 0.055, "Medium")
            buoc = int(fl.size * 1.9)
            for t in dong:
                dr.text((m, y), t, font=fl, fill=ink)
                dr.line([(m, y + buoc * 0.82), (w - m, y + buoc * 0.82)], fill=ink[:3] + (90,), width=2)
                y += buoc
        if v.get("dau"):
            _dau(dr, w - m - w * 0.08, h - m - w * 0.08, w * 0.075, v["dau"])
    elif mau == "phong_bi" or v.get("doc"):
        t = tieu or "".join(dong)
        buoc = min(h * 0.7 / max(1, len(t)), w * 0.45)
        ft = _font(v.get("font") or "SM", buoc * 0.92)
        _doc_chu(dr, w / 2, (h - buoc * len(t)) / 2, t, ft, ink, buoc)
        for k, t2 in enumerate(dong if tieu else []):
            b2 = min(h * 0.35 / max(1, len(t2)), w * 0.1)
            _doc_chu(dr, m + b2 * (0.6 + 1.3 * k), h - m - b2 * len(t2), t2, _font("SM", b2 * 0.9), ink, b2)
    elif mau == "man_hinh":
        y = m
        if tieu:
            fh = _vua(dr, tieu, "NJ", w - 2 * m, h * 0.07, w * 0.06)
            dr.rectangle([0, 0, w, y + fh.size * 1.6], fill=(36, 41, 46, 235))
            dr.text((m, y * 0.6), tieu, font=fh, fill=(255, 255, 255, 255))
            y += int(fh.size * 2.2)
        fl = _vua(dr, max(dong or [" "], key=len).lstrip(">"), "NJ", w * 0.7, h * 0.08, w * 0.058, "Medium")
        for t in dong:
            phai = t.startswith(">")
            t = t.lstrip(">").strip()
            x0, y0, x1, y1 = dr.textbbox((0, 0), t, font=fl)
            bw, bh = (x1 - x0) + fl.size, (y1 - y0) + fl.size * 0.9
            bx = w - m - bw if phai else m
            dr.rounded_rectangle([bx, y, bx + bw, y + bh], radius=int(fl.size * 0.6),
                                 fill=(141, 224, 138, 245) if phai else (255, 255, 255, 245))
            dr.text((bx + fl.size / 2 - x0, y + fl.size * 0.45 - y0), t, font=fl, fill=ink)
            y += int(bh + fl.size * 0.6)
    else:   # bien / nhan / tu_do: chữ to căn giữa, chia đều chiều cao
        cac = [tieu] + dong if tieu else dong
        hang = h * (0.8 if mau == "bien" else 0.55) / max(1, len(cac))
        ten = v.get("font") or ("NJ" if mau == "bien" else "SM")
        y = (h - hang * len(cac)) / 2
        for k, t in enumerate(cac):
            ft = _vua(dr, t, ten, w - 2 * m, hang * 0.86, hang * (0.9 if k == 0 else 0.7), "Black")
            x0, y0, x1, y1 = dr.textbbox((0, 0), t, font=ft)
            dr.text(((w - (x1 - x0)) / 2 - x0, y + (hang - (y1 - y0)) / 2 - y0), t, font=ft, fill=ink)
            y += hang
    return np.array(im)


# ───────────────────────────── dò mặt phẳng + bám ─────────────────────────────
def tim_mat_phang(f, n=8):
    """Ứng viên tứ giác sáng/phẳng (giấy, biển, màn hình) trên khung đầu: [(diện tích, 4 góc px)]."""
    H, W = f.shape[:2]
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    ra = []
    cands = []
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    for thr in (0, 1, 130, 170, 200, 225):
        if thr == 0:     # mép (giấy có bóng lá/bóng tay vẫn ra viền)
            b = cv2.dilate(cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 40, 120), np.ones((3, 3), np.uint8))
        elif thr == 1:   # ít màu (giấy trắng/xám kể cả chỗ bị bóng râm)
            b = ((hsv[:, :, 1] < 40) & (hsv[:, :, 2] > 110)).astype(np.uint8) * 255
        else:
            _, b = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)
        b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
        cs, _ = cv2.findContours(b, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cands += cs
    for c in cands:
        a = cv2.contourArea(c)
        if a < 0.012 * W * H or a > 0.8 * W * H:
            continue
        hull = cv2.convexHull(c)
        p = None
        for eps in (0.02, 0.03, 0.045, 0.06):   # bao lồi rồi rút về 4 đỉnh: mép bị bóng/lá che vẫn ra tứ giác
            x = cv2.approxPolyDP(hull, eps * cv2.arcLength(hull, True), True)
            if len(x) == 4:
                p = x
                break
        if p is None or not 0.82 < cv2.contourArea(p) / max(a, 1) < 1.25:
            continue
        q = _xep_goc(p.reshape(4, 2).astype(np.float32))
        if min(np.linalg.norm(q[i] - q[(i + 1) % 4]) for i in range(4)) < 0.03 * W:   # tứ giác suy biến (2 đỉnh trùng)
            continue
        if any(np.abs(q - r[1]).max() < 0.02 * W for r in ra):
            continue
        ra.append((a, q))
    ra.sort(key=lambda r: -r[0])
    return ra[:n]


def _xep_goc(q):
    """Xếp 4 điểm theo TRÁI-TRÊN, PHẢI-TRÊN, PHẢI-DƯỚI, TRÁI-DƯỚI."""
    s = q.sum(1)
    d = np.diff(q, axis=1).ravel()
    return np.array([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]], np.float32)


def chong(f, to, Hm, che=True, tron="nhan", ref_lab=None, gain=1.0):
    """Chồng tờ chữ RGBA (to) lên khung f theo ma trận Hm (tờ → khung)."""
    Hh, Ww = f.shape[:2]
    bgr = cv2.cvtColor(to, cv2.COLOR_RGBA2BGRA)
    w = cv2.warpPerspective(bgr, Hm, (Ww, Hh), flags=cv2.INTER_AREA if np.linalg.det(Hm[:2, :2]) < 1 else cv2.INTER_LINEAR)
    a = cv2.GaussianBlur(w[:, :, 3].astype(np.float32) / 255.0, (0, 0), 0.6) * float(gain)
    if che and ref_lab is not None:   # chỉ in lên chỗ còn là MẶT GIẤY (tay/vật che → không đè)
        lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32)
        dL = np.maximum(0, ref_lab[0] - lab[:, :, 0]) / 55.0
        dC = np.hypot(lab[:, :, 1] - ref_lab[1], lab[:, :, 2] - ref_lab[2]) / 22.0
        giay = np.clip(1.6 - np.hypot(dL, dC), 0, 1)
        a *= cv2.GaussianBlur(giay, (0, 0), 1.5)
    ink = w[:, :, :3].astype(np.float32)
    base = f.astype(np.float32)
    a3 = a[:, :, None]
    if tron == "phu":
        out = base * (1 - a3) + ink * a3
    else:   # multiply: mực ăn theo bóng/ánh sáng của giấy
        out = base * (1 - a3 + a3 * ink / 255.0)
    return np.clip(out, 0, 255).astype(np.uint8)


def _ref_lab(f, q):
    m = np.zeros(f.shape[:2], np.uint8)
    c = q.mean(0)
    cv2.fillConvexPoly(m, ((q - c) * 0.8 + c).astype(np.int32), 255)
    lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB)[m > 0].astype(np.float32)
    return np.median(lab, 0)


def _ti_le(q):
    w = (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2
    h = (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2
    return float(h / max(w, 1))


# ───────────────────────────── tập ─────────────────────────────

# ───────────────────────────── tập ─────────────────────────────
def _ten_anh(x):
    """'28' / '028' / '028.png' / 'clip_28' → '028.png'."""
    m = re.search(r"(\d+)", str(x))
    if not m:
        raise SystemExit(f"✗ không hiểu tên ảnh '{x}'")
    return f"{int(m.group(1)):03d}.png"


def _jobs(hd):
    """grok_jobs.csv → [(id clip, tên ảnh, prompt)] (nguồn chuẩn ảnh ↔ clip TRƯỚC khi có hook_timeline.json)."""
    f = hd / "grok_jobs.csv"
    if not f.exists():
        return []
    rows = list(csv.DictReader(io.StringIO(f.read_text(encoding="utf-8-sig"))))
    return [(r.get("id", ""), Path(r.get("image", "")).name, r.get("prompt", "")) for r in rows if r.get("image")]


def ung_vien(hd):
    """Ảnh nghi có đạo cụ mang chữ: từ khoá trong prompt Grok + lời/kỳ vọng của shot trong hook_timeline.json (nếu đã có)."""
    txt = {}
    for _, img, pr in _jobs(hd):
        txt.setdefault(img, []).append(pr)
    tl = hd / "hook_timeline.json"
    if tl.exists():
        d = json.loads(tl.read_text(encoding="utf-8"))
        for s in (d.get("shots") if isinstance(d, dict) else d) or []:
            if s.get("img"):
                txt.setdefault(Path(s["img"]).name, []).append(f"{s.get('voice', '')} {s.get('ky_vong', '')}")
    ra = []
    for img, ts in sorted(txt.items()):
        t = " ".join(ts)
        m = sorted({x.lower() for x in TU_KHOA.findall(t)})
        if m:
            ra.append((img, m, t))
    return ra


def _goc_anh(hd, img):
    p = hd / "img" / img
    g = hd / "img" / "_goc" / img
    if not g.exists():
        if not p.exists():
            raise SystemExit(f"✗ chưa có ảnh {p}")
        g.parent.mkdir(exist_ok=True)
        shutil.copy2(p, g)
    return p, g


def nhap(d, force=False):
    hd = Path(d) / "hook"
    p = hd / "chu_tren_vat.json"
    if p.exists() and not force:
        raise SystemExit(f"✗ đã có {p} — sửa tay hoặc --force")
    uv = ung_vien(hd)
    p.write_text(json.dumps({"_doc": "docs/QUY_TAC_CHU_TREN_DAO_CU_HOOK.md — mỗi ảnh nghi có chữ: khai 'anh' (vat + goc từ --tim) "
                                     "hoặc giữ ở bo_qua với lý do thật (xoá chữ '(CHƯA QUYẾT)').",
                             "anh": [], "bo_qua": {img: f"(CHƯA QUYẾT) {', '.join(k)}" for img, k, _ in uv}},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ {p}: {len(uv)} ảnh nghi có đạo cụ mang chữ — chữ là điểm nhấn → khai 'anh'; phông nền → bo_qua kèm lý do")
    for img, k, t in uv:
        print(f"   · {img}: {', '.join(k)} | {t[:110]}")


def tim(d, x):
    hd = Path(d) / "hook"
    img = _ten_anh(x)
    _, g = _goc_anh(hd, img)
    f = cv2.imread(str(g))
    H, W = f.shape[:2]
    ve = f.copy()
    kq = tim_mat_phang(f)
    for k, (a, q) in enumerate(kq):
        cv2.polylines(ve, [q.astype(np.int32)], True, (0, 0, 255), max(3, W // 400))
        cv2.putText(ve, str(k), tuple(int(t) for t in q.mean(0)), cv2.FONT_HERSHEY_SIMPLEX, W / 800, (0, 0, 255), max(3, W // 300))
        print(f"  [{k}] goc = {json.dumps([[round(float(a_) / W, 4), round(float(b_) / H, 4)] for a_, b_ in q])}")
    (hd / "chu").mkdir(exist_ok=True)
    p = hd / "chu" / f"{img[:-4]}_tim.jpg"
    cv2.imwrite(str(p), cv2.resize(ve, (1280, int(1280 * H / W))), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"✓ {p} — xem ảnh, chép 'goc' tứ giác đúng vào chu_tren_vat.json (dò sai → tự đo 4 góc trên ảnh này, toạ độ 0–1)")


def _tron(v):
    return v.get("tron") or ("phu" if v.get("mau") in ("bien", "man_hinh") else "nhan")


def lam_anh(hd, a):
    img = _ten_anh(a["img"])
    p, g = _goc_anh(hd, img)
    im = cv2.imread(str(g))
    H, W = im.shape[:2]
    goc = im.copy()
    for v in a["vat"]:
        q = np.array([[x * W, y * H] for x, y in v["goc"]], np.float32)
        to = dung_to_chu(v, float(v.get("ti_le") or _ti_le(q)))
        h, w = to.shape[:2]
        Hq = cv2.getPerspectiveTransform(np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32), q)
        im = chong(im, to, Hq, che=v.get("che", True), tron=_tron(v), ref_lab=_ref_lab(goc, q))
    cv2.imwrite(str(p), im)
    (hd / "chu").mkdir(exist_ok=True)
    sp = hd / "chu" / f"{img[:-4]}_soi.jpg"
    def nho(x):
        return cv2.resize(x, (960, int(960 * H / W)))
    cv2.imwrite(str(sp), np.hstack([nho(goc), nho(im)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
    (hd / "chu" / f"{img[:-4]}.spec").write_text(_van(a), encoding="utf-8")   # dấu vân khai báo đã chèn
    sua_prompt_grok(hd, img, a)
    print(f"  ✓ {p} ({len(a['vat'])} vật) · soi trước|sau {sp}")


GIU_CHU = ("KEEP TEXT: the {vat} already carries printed Japanese text — keep every character exactly as in the source image, "
           "sharp and unchanged; do not add, remove, animate or re-letter any text. Camera nearly static, only a very slow "
           "push-in; hands must not cover the text.")


def sua_prompt_grok(hd, img, a):
    """Prompt Grok của ảnh đã chèn chữ: bỏ 'no text' (Grok sẽ xoá/làm nhoè chữ có sẵn) + dặn giữ nguyên chữ."""
    f = hd / "grok_jobs.csv"
    if not f.exists():
        return
    rows = list(csv.DictReader(io.StringIO(f.read_text(encoding="utf-8-sig"))))
    if not rows:
        return
    ten = {"giay_to": "document", "bien": "sign", "phong_bi": "envelope", "man_hinh": "screen", "nhan": "label"}
    vat = ", ".join(sorted({ten.get(v.get("mau", "giay_to"), "prop") for v in a["vat"]}))
    doi = 0
    for r in rows:
        if Path(r.get("image", "")).name != img or "KEEP TEXT:" in r.get("prompt", ""):
            continue
        r["prompt"] = re.sub(r"\bno text,\s*", "no extra text, ", r["prompt"]).rstrip() + " " + GIU_CHU.format(vat=vat)
        doi += 1
    if doi:
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
        f.write_text(out.getvalue(), encoding="utf-8-sig")
        print(f"    · grok_jobs.csv: sửa prompt {doi} clip của {img} (giữ nguyên chữ, máy quay gần đứng yên)")


def _van(a):
    import hashlib
    return hashlib.sha256(json.dumps(a, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def lam(d, chi=None):
    hd = Path(d) / "hook"
    cfg = json.loads((hd / "chu_tren_vat.json").read_text(encoding="utf-8"))
    for a in cfg.get("anh") or []:
        if chi and _ten_anh(a["img"]) not in {_ten_anh(x) for x in chi}:
            continue
        lam_anh(hd, a)


def kiem(d, sau_grok=False):
    """Trước Grok: mọi ảnh nghi có chữ đã quyết + ảnh khai đã chèn. Sau Grok (duyet_hook): clip của ảnh có chữ phải sinh
    SAU khi chèn (sinh từ ảnh trơn = phải sinh lại). Chữ bị Grok làm méo trong clip KHÔNG xét (giới hạn của Grok)."""
    hd = Path(d) / "hook"
    p = hd / "chu_tren_vat.json"
    if not p.exists():
        uv = ung_vien(hd)
        return [f"chưa có {p} — {len(uv)} ảnh nghi có đạo cụ mang chữ (chạy --nhap)"] if uv else []
    cfg = json.loads(p.read_text(encoding="utf-8"))
    loi = []
    khai = {_ten_anh(a["img"]): a for a in cfg.get("anh") or []}
    co = set(khai)
    bo = cfg.get("bo_qua") or {}
    for k, ly in bo.items():
        if str(ly).startswith("(CHƯA QUYẾT)"):
            loi.append(f"ảnh {k} chưa quyết có chèn chữ không: {ly}")
    for img, k, _ in ung_vien(hd):
        if img not in co and img not in bo:
            loi.append(f"ảnh {img} nghi có đạo cụ mang chữ ({', '.join(k)}) — khai 'anh' hoặc bo_qua")
    clip_cua = {}
    for cid, img, _ in _jobs(hd):
        clip_cua.setdefault(img, []).append(hd / "clip" / f"{cid}.mp4")
    for img in co:
        pi, g = hd / "img" / img, hd / "img" / "_goc" / img
        vf = hd / "chu" / f"{img[:-4]}.spec"
        if not g.exists() or not vf.exists() or vf.read_text(encoding="utf-8") != _van(khai[img]):
            loi.append(f"ảnh {img}: chưa chèn chữ / khai báo đã đổi sau lần chèn → chạy lại chu_dao_cu.py")
            continue
        if sau_grok:
            for c in clip_cua.get(img, []):
                if c.exists() and c.stat().st_mtime < pi.stat().st_mtime:
                    loi.append(f"{c.name} sinh từ ảnh {img} CHƯA có chữ → sinh lại clip Grok từ ảnh đã chèn")
    return loi


def cong(prof, d, buoc, sau_grok=True):
    loi = kiem(d, sau_grok)
    if loi:
        raise SystemExit(f"✗ {buoc}: CHỮ TRÊN ĐẠO CỤ hook chưa xong (docs/QUY_TAC_CHU_TREN_DAO_CU_HOOK.md):\n  - " + "\n  - ".join(loi)
                         + f"\n  → py -3.13 -X utf8 {HERE / 'chu_dao_cu.py'} --profile {prof.get('id', '<lane>')} --slug {Path(d).name}")


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    import profiles
    import review_may3
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--nhap", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--tim", metavar="ANH")
    ap.add_argument("--kiem", action="store_true")
    ap.add_argument("--chi", nargs="*")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    d = review_may3.thu_muc_tap(prof, a.slug)
    if a.nhap:
        nhap(d, a.force)
    elif a.tim is not None:
        tim(d, a.tim)
    elif a.kiem:
        loi = kiem(d, sau_grok=True)
        print("✓ chữ trên đạo cụ đạt" if not loi else "✗ " + "\n✗ ".join(loi))
        sys.exit(1 if loi else 0)
    else:
        lam(d, a.chi)


if __name__ == "__main__":
    main()
