# -*- coding: utf-8 -*-
r"""block_gioi_thieu.py — "BLOCK GIỚI THIỆU NHÂN VẬT" trong HOOK: FREEZE-FRAME + CHỮ GÕ HỒ SƠ (anh chốt 12/10/2026, mẫu Lane O ep10).

Anh nói "block giới thiệu" = KIỂU NÀY (khác thẻ tên động the_ten_hook.py):
  cảnh nhân vật LỘ MẶT LẦN ĐẦU (clip Grok) → ĐÓNG BĂNG khung hình ngay trong video (chớp trắng 0,18s, ảnh bớt màu) →
  dải tối bên TRÁI, MẶT bên PHẢI → gõ theo cụm: 「Họ Tên｜NN歳」 rồi từng dòng 「nhãn｜nội dung」 (仕事/経験/性格/過去/本音…) →
  dòng cuối giữ ≥3s cho người lớn tuổi đọc → hết block, clip chạy tiếp. KHÔNG đọc thành lời (chỉ 1 câu VO ngắn ở shot trước),
  KHÔNG dựng thẻ/profile card riêng, 9–14s/người, chỉ nhạc nền (luật 12 — không tiếng gõ phím).
  Trước freeze: KHÔNG lộ rõ mặt nhân vật đó (chỉ gáy/tay/dáng) — viết vào prompt ảnh các shot trước.
Chữ cháy thẳng vào clip → hook_timeline có shot LẶNG (freeze:true, lang_s, không `cau`); máy 2 chỉ ghép (cau_vai.lang_hook,
nhớ `dong_goi_may2.py --bundle`). Thay cho thẻ tên của người đó → the_ten.json tự ghi `bo_qua`.

Dữ liệu tập: `<tập>\hook\block_gioi_thieu.json`
  {"block": [{"id": "kitami", "sau_shot": 7, "t": null, "ten": "北見 翔太", "tuoi": "26歳", "dur_s": 10,
              "dong": [["仕事", "介護職員（転職直後）"], ["性格", "冗談で責任をかわす"]]}]}
  sau_shot = số shot (n) có clip lộ mặt; t = giây lấy khung (null = khung cuối; khung cuối nhắm mắt/mờ → đặt t).
Ra: `<tập>\hook\clip\clip_NN.mp4` (NN = số shot block, máy cấp số mới > mọi shot cũ) + `hook\qc\block_<id>_soi.jpg`.

  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập> --nhap    # nháp từ characters.json
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập>           # chèn shot + render
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập> --chi kitami
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập> --kiem    # cổng
Chạy SAU khi đủ clip Grok (cần clip shot sau_shot). Luật + ảnh mẫu: docs\QUY_TAC_BLOCK_GIOI_THIEU_NHAN_VAT.md
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
FF = imageio_ffmpeg.get_ffmpeg_exe()
FONT_DIR = [Path(r"C:\Users\admin\.claude\skills\motion_graphics\assets\fonts"), HERE / "the_ten_mau" / "fonts"]
W, HH, FPS = 1920, 1080, 30
MAC_DINH = {"mau": "#14806f", "mau_phu": "#e9c46a", "dur_s": 11.0, "giu_cuoi_s": 3.0}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cau_hinh(prof):
    c = dict(MAC_DINH)
    hk = ((prof.get("script") or {}).get("hook") or {})
    tt = hk.get("the_ten") or {}
    c.update({k: tt[k] for k in ("mau", "mau_phu") if tt.get(k)})   # cùng màu nhận diện lane với thẻ tên
    c.update(hk.get("block_gioi_thieu") or {})
    return c


def font(ten, sz):
    for d in FONT_DIR:
        if (d / ten).exists():
            return ImageFont.truetype(str(d / ten), sz)
    raise SystemExit(f"✗ thiếu font {ten}")


def _doc(p, mac=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return mac


# ───────────────────────────── vẽ ─────────────────────────────
def lich(b):
    t = 0.45
    ev = [("ten", t, b["ten"], 0.07)]
    t += len(b["ten"]) * 0.07 + 0.25
    ev.append(("tuoi", t, b.get("tuoi", ""), 0.0))
    t += 0.55
    for nhan, gt in b["dong"]:
        ev.append(("dong", t, (nhan, gt), 0.05))
        t += (len(gt) / 2) * 0.10 + 0.55
    return ev, t


def ve(nen, b, t, ev, F, acc, acc2):
    a = min(1.0, t / 0.3)
    im = ImageEnhance.Color(nen).enhance(1 - 0.45 * a)
    im = ImageEnhance.Brightness(im).enhance(1 - 0.12 * a)
    ov = Image.new("RGBA", (W, HH), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x in range(0, 1100):
        al = int(215 * a * (1 - max(0, x - 760) / 340)) if x > 760 else int(215 * a)
        d.line([(x, 0), (x, HH)], fill=(8, 14, 20, al))
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    if t < 0.18:   # chớp trắng lúc đóng băng (che luôn chỗ nhảy hình khi lấy khung `t`)
        im = Image.alpha_composite(im, Image.new("RGBA", (W, HH), (255, 255, 255, int(170 * (1 - t / 0.18)))))
    d = ImageDraw.Draw(im)
    x0, y = 96, int(b.get("y0", 200))
    if a > 0:
        d.rectangle([x0 - 34, y - 6, x0 - 24, y + int(110 * a)], fill=acc2 + (255,))
    con_tro, y_dong = None, y + 150
    for k, (loai, st, gt, cps) in enumerate(ev):
        if t < st:
            break
        if loai == "ten":
            n = min(len(gt), int((t - st) / cps) + 1)
            d.text((x0, y), gt[:n], font=F["ten"], fill=(255, 255, 255, 255))
            con_tro = (x0 + d.textlength(gt[:n], font=F["ten"]) + 8, y + 10, 64) if n < len(gt) else None
        elif loai == "tuoi" and gt:
            wx = d.textlength(b["ten"], font=F["ten"])
            d.text((x0 + wx + 28, y + 26), "｜" + gt, font=F["tuoi"], fill=acc2 + (255,))
        elif loai == "dong":
            nhan, val = gt
            lw = d.textlength(nhan, font=F["nhan"])
            d.rounded_rectangle([x0, y_dong + 4, x0 + lw + 28, y_dong + 62], radius=10, fill=acc + (255,))
            d.text((x0 + 14, y_dong + 8), nhan, font=F["nhan"], fill=(255, 255, 255, 255))
            kk = min(len(val), (int((t - st) / 0.10) + 1) * 2)
            vx = x0 + lw + 50
            d.text((vx, y_dong + 2), val[:kk], font=F["gt"], fill=(255, 255, 255, 255))
            if kk < len(val) or k == len(ev) - 1:
                con_tro = (vx + d.textlength(val[:kk], font=F["gt"]) + 6, y_dong + 8, 52)
            else:
                con_tro = None
            y_dong += 96
    if con_tro and int(t * 2.4) % 2 == 0:
        cx, cy, ch = con_tro
        d.rectangle([cx, cy, cx + 6, cy + ch], fill=acc2 + (255,))
    return im.convert("RGB")


def render(prof, hd, b, n_block):
    c = cau_hinh(prof)
    acc, acc2 = _rgb(b.get("mau") or c["mau"]), _rgb(b.get("mau_phu") or c["mau_phu"])
    clip = hd / "clip" / f"clip_{int(b['sau_shot']):02d}.mp4"
    if not clip.exists():
        raise SystemExit(f"✗ chưa có {clip} (clip lộ mặt của {b['id']}) — chạy Grok trước")
    png = hd / "clip" / f"_block_{b['id']}.png"
    vt = ["-ss", str(b["t"])] if b.get("t") is not None else ["-sseof", "-0.15"]
    subprocess.run([FF, "-y", "-loglevel", "error", *vt, "-i", str(clip), "-frames:v", "1", "-vf", f"scale={W}:{HH}", str(png)],
                   check=True)
    nen = Image.open(png).convert("RGB").resize((W, HH))
    ev, t_xong = lich(b)
    dur = max(float(b.get("dur_s") or c["dur_s"]), t_xong + float(c["giu_cuoi_s"]))
    F = {"ten": font("MPLUSRounded1c-Black.ttf", 96), "tuoi": font("MPLUSRounded1c-Black.ttf", 64),
         "nhan": font("MPLUSRounded1c-ExtraBold.ttf", 40), "gt": font("MPLUSRounded1c-ExtraBold.ttf", 52)}
    for nhan, gt in b["dong"]:   # chữ lấn sang nửa mặt (phải) → báo, không tự cắt chữ của anh
        if 96 + ImageDraw.Draw(nen).textlength(nhan, font=F["nhan"]) + 50 + ImageDraw.Draw(nen).textlength(gt, font=F["gt"]) > 1180:
            print(f"  ⚠ {b['id']}: dòng 「{nhan}｜{gt}」 dài, lấn gần mặt — rút gọn chữ hoặc chấp nhận")
    out = hd / "clip" / f"clip_{n_block:02d}.mp4"
    p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HH}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(out)],
                         stdin=subprocess.PIPE)
    for i in range(int(round(dur * FPS))):
        p.stdin.write(ve(nen, b, i / FPS, ev, F, acc, acc2).tobytes())
    p.stdin.close()
    p.wait()
    (hd / "qc").mkdir(exist_ok=True)
    snap = hd / "qc" / f"block_{b['id']}_soi.jpg"
    ve(nen, b, dur - 0.5, ev, F, acc, acc2).save(snap, quality=85)
    print(f"  ✓ {b['id']}: {out.name} · {dur:.1f}s (gõ xong {t_xong:.1f}s) · soi {snap}")
    return out, dur


# ───────────────────────────── timeline ─────────────────────────────
def chen_timeline(hd, b, dur):
    """Chèn (hoặc cập nhật) shot block NGAY SAU shot sau_shot. Số shot mới = max+1 (không đổi tên clip/ảnh cũ)."""
    tlp = hd / "hook_timeline.json"
    tl = _doc(tlp, {})
    shots = tl["shots"]
    cu = next((s for s in shots if s.get("block") == b["id"]), None)
    if cu is None:
        n = max(int(s["n"]) for s in shots) + 1
        i = next(i for i, s in enumerate(shots) if int(s["n"]) == int(b["sau_shot"]))
        cu = {"n": n, "clip": f"clip/clip_{n:02d}.mp4", "cast": b["id"], "freeze": True, "block": b["id"]}
        shots.insert(i + 1, cu)
    cu.update(lang_s=round(dur, 2), ky_vong=f"BLOCK GIỚI THIỆU {b['ten']} — đóng băng khung lộ mặt, gõ chữ hồ sơ (không đọc).")
    tlp.write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    return int(cu["n"])


def ghi_bo_qua_the_ten(hd, ids):
    p = hd / "the_ten.json"
    d = _doc(p, {"the": [], "bo_qua": {}, "cho_phep_cau": []})
    d["the"] = [t for t in d.get("the") or [] if t.get("id") not in ids]
    for i in ids:
        d.setdefault("bo_qua", {})[i] = "thay bằng BLOCK GIỚI THIỆU (freeze-frame + chữ gõ) — pipeline\\block_gioi_thieu.py"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def nhap(d, force=False):
    hd = d / "hook"
    p = hd / "block_gioi_thieu.json"
    if p.exists() and not force:
        raise SystemExit(f"✗ đã có {p} — sửa tay hoặc --force")
    chars = (_doc(d / "characters.json", {}) or {}).get("characters") or []
    shots = (_doc(hd / "hook_timeline.json", {}) or {}).get("shots") or []
    bl = []
    for c in chars:
        sh = [s for s in shots if "cau" in s and c["id"] in str(s.get("cast") or "").split(",")]
        if not sh or not c.get("ref"):
            continue
        ten = re.sub(r"[（(].*?[）)]", "", c.get("name") or "").strip()
        vai = re.split(r"[（(—]", str(c.get("vai") or ""))[0].strip()
        bl.append({"id": c["id"], "sau_shot": sh[0]["n"], "t": None, "ten": ten, "tuoi": f"{c['age']}歳" if c.get("age") else "",
                   "dur_s": 11, "dong": [["仕事", vai[:16]], ["性格", "<<SỬA>>"]]})
    p.write_text(json.dumps({"_doc": "BLOCK GIỚI THIỆU — docs/QUY_TAC_BLOCK_GIOI_THIEU_NHAN_VAT.md. ten 'Họ Tên' cách 1 dấu cách; "
                                     "sau_shot = shot LỘ MẶT LẦN ĐẦU (ảnh shot đó: mặt bên PHẢI, nửa trái trống); dong 3–5 dòng ≤16 chữ; "
                                     "bỏ người không cần block.", "block": bl}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ nháp {p} ({len(bl)} người) — sửa dòng hồ sơ, xoá người không cần, rồi chạy render")


def kiem(d):
    hd = d / "hook"
    cfg = _doc(hd / "block_gioi_thieu.json")
    if not cfg:
        print("· không có block_gioi_thieu.json — tập không dùng block")
        return 0
    shots = {s.get("block"): s for s in (_doc(hd / "hook_timeline.json", {}) or {}).get("shots", []) if s.get("block")}
    loi = []
    for b in cfg["block"]:
        s = shots.get(b["id"])
        if not s:
            loi.append(f"{b['id']}: chưa chèn shot block vào hook_timeline.json")
        elif not (hd / s["clip"]).exists():
            loi.append(f"{b['id']}: thiếu {s['clip']}")
        if any("<<" in x for row in b["dong"] for x in row):
            loi.append(f"{b['id']}: còn chỗ <<SỬA>>")
    for x in loi:
        print("✗ " + x)
    print("✓ block giới thiệu đạt" if not loi else f"✗ {len(loi)} lỗi")
    return 1 if loi else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True, help="tên thư mục tập hoặc đường dẫn")
    ap.add_argument("--nhap", action="store_true")
    ap.add_argument("--kiem", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--chi", nargs="*", default=[])
    a = ap.parse_args()
    import profiles
    prof = profiles.load(a.profile) if hasattr(profiles, "load") else profiles.get(a.profile)
    d = Path(a.slug)
    if not d.is_absolute() and not d.exists():
        d = ROOT / prof["slug_dir"] / a.slug
    if a.nhap:
        return nhap(d, a.force)
    if a.kiem:
        sys.exit(kiem(d))
    hd = d / "hook"
    cfg = _doc(hd / "block_gioi_thieu.json")
    if not cfg:
        raise SystemExit("✗ chưa có hook\\block_gioi_thieu.json — chạy --nhap")
    ids = []
    for b in cfg["block"]:
        if a.chi and b["id"] not in a.chi:
            continue
        tl = _doc(hd / "hook_timeline.json", {})
        cu = next((s for s in tl["shots"] if s.get("block") == b["id"]), None)
        n = int(cu["n"]) if cu else max(int(s["n"]) for s in tl["shots"]) + 1
        _, dur = render(prof, hd, b, n)
        chen_timeline(hd, b, dur)
        ids.append(b["id"])
    ghi_bo_qua_the_ten(hd, ids)
    print(f"✓ {len(ids)} block · timeline + the_ten.json bo_qua đã cập nhật → dựng clip xem thử (xem_thu_hook_giong.py); "
          f"giao máy 2 nhớ --bundle")


if __name__ == "__main__":
    main()
