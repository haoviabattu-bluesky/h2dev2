#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pipeline_one_shot.py — CHẠY 1 MẠCH: pre-check ảnh (fail fast) → download nếu thiếu/hỏng → render → báo cáo.

Tái cấu trúc 2026-09-13 sau bài học "2 tiếng / 1 video" (làm tay chỉ 30 phút):
  - Pre-check ảnh TRƯỚC render: phát hiện PNG giả (JPEG đội lốt), truncated, 0-byte trong
    ~20-30 giây — thay vì để render chạy xong mới TimeoutError (mất cả lượt).
  - Download ảnh CHỈ KHI thiếu/hỏng — bỏ thói quen tải lại 300 ảnh mỗi lượt (~16 phút).
  - Render xuyên B8..B11 bằng make_video — GIỮ NGUYÊN toàn bộ QC nội tại (B8Q chấm từng cảnh,
    B10 nghiệm thu toàn tập, ngưỡng lạc). Script này KHÔNG cắt bất kỳ bước kiểm tra nào,
    KHÔNG tự sửa lỗi nội dung, KHÔNG hạ ngưỡng — chỉ phát hiện SỚM và báo cáo 1 lệnh.
  - Báo cáo 1 lệnh: state.json render + qc_canh.json + final.mp4.

Dùng (session điều khiển — desktop không giới hạn 25 phút):
  env -u PYTHONPATH py -3.13 -X utf8 tools/pipeline_one_shot.py --profile toshi-densetsu-jp --slug ep02-walton

Cờ:
  --from B8              bước bắt đầu (mặc định B8)
  --skip-precheck        bỏ pre-check ảnh
  --no-download          không download dù thiếu ảnh
  --detach               chạy make_video qua render_detach + poll log (dùng khi session bị giới hạn)
  --toi-da-lac 0.03      ngưỡng lạc tối đa cho báo cáo (chỉ để ĐÁNH GIÁ, không sửa render)

Exit: 0 = ĐẠT (B11 xong + lạc ≤ ngưỡng) · 1 = render rớt (đọc báo cáo) · 2 = pre-check lỗi (ảnh hỏng).
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

H2DEV = Path(r"E:\CLAUDE\YOUTUBE\h2dev")


def pycmd(*args):
    return ["py", "-3.13", "-X", "utf8", *args]


def precheck_images(slug_dir: Path, expected: int) -> list:
    """Mở từng ảnh bằng PIL: format đúng extension, verify() không truncated, size > 0.
    Trả về danh sách lỗi [(path, lý do)]. KHÔNG tự sửa — fail fast để báo người điều khiển."""
    try:
        from PIL import Image
    except ImportError:
        return [(str(slug_dir / "img_ai"), "thiếu PIL — chạy: py -3.13 -m pip install pillow")]

    img_ai = slug_dir / "img_ai"
    if not img_ai.is_dir():
        return [(str(img_ai), "thư mục img_ai không tồn tại")]

    files = sorted(img_ai.glob("*.png"))
    if len(files) < expected:
        return [(str(img_ai), f"thiếu ảnh: có {len(files)}/{expected} PNG — cần download-result trước")]

    loi = []
    for f in files:
        if f.stat().st_size == 0:
            loi.append((str(f), "0 byte"))
            continue
        try:
            with Image.open(f) as im:
                fmt = im.format
                im.verify()
            # verify() làm hỏng handle → mở lại để chắc chắn đọc được full file
            with Image.open(f) as im:
                im.load()
            if fmt != "PNG":
                loi.append((str(f), f"PNG giả: format thật là {fmt}"))
        except Exception as e:
            loi.append((str(f), f"hỏng: {e}"))
    return loi


def count_img_ai(slug_dir: Path) -> int:
    img_ai = slug_dir / "img_ai"
    return len(list(img_ai.glob("*.png"))) if img_ai.is_dir() else 0


def normalize_img_ai(slug_dir: Path) -> int:
    """Chuẩn hoá kho ảnh: mọi file *.png có format thật KHÁC PNG (JPEG đội lốt) được
    convert sang PNG thật, GIỮ NGUYÊN pixel (không đổi màu/kích thước). Chạy SAU render
    (không chạy song song — tránh race đọc/ghi file). Trả về số ảnh đã convert."""
    from PIL import Image
    img_ai = slug_dir / "img_ai"
    dem = 0
    for f in sorted(img_ai.glob("*.png")):
        try:
            with Image.open(f) as im:
                if im.format == "PNG":
                    continue
                pix = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and "transparency" in im.info else "RGB")
                # ghi qua file tạm rồi thay thế — tránh file hỏng nếu save lỗi giữa chừng
                tmp = f.with_suffix(".png.tmp")
                pix.save(tmp, "PNG")
                tmp.replace(f)
                dem += 1
        except Exception as e:
            print(f"  ⚠️ bỏ qua {f.name}: {e}")
    return dem


def download_result(profile: str, slug: str, slug_dir: Path) -> tuple:
    """Gọi drive_handoff download-result. Trả về (rc, output)."""
    t0 = time.time()
    r = subprocess.run(
        pycmd("pipeline/drive_handoff.py", "download-result", slug, str(slug_dir / "img_ai")),
        cwd=str(H2DEV), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr)[-1500:], time.time() - t0


def read_state(slug_dir: Path) -> dict:
    sf = slug_dir / "state.json"
    if not sf.exists():
        return {}
    try:
        return json.loads(sf.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_qc_canh(slug_dir: Path) -> dict:
    """qc_canh.json mới nhất: tổng cảnh, lạc (muc==0), % lạc."""
    qf = slug_dir / "qc_canh.json"
    if not qf.exists():
        return {"co": False}
    try:
        d = json.loads(qf.read_text(encoding="utf-8"))
        if not isinstance(d, list) or not d:
            return {"co": False}
        tong = len(d)
        lac = sum(1 for x in d if isinstance(x, dict) and x.get("muc") == 0)
        return {"co": True, "tong": tong, "lac": lac,
                "ty_le_lac": round(lac / tong, 4), "cap_nhat": datetime.fromtimestamp(qf.stat().st_mtime).strftime("%H:%M")}
    except Exception:
        return {"co": False}


def final_mp4(slug_dir: Path) -> dict:
    f = slug_dir / "final.mp4"
    if not f.exists():
        return {"co": False}
    return {"co": True, "mb": round(f.stat().st_size / 1048576, 1),
            "xong_luc": datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M")}


def run_render(profile: str, slug: str, tu_buoc: str, detach: bool):
    if detach:
        r = subprocess.run(
            pycmd("tools/render_detach.py", "--slug", slug, "--from", tu_buoc),
            cwd=str(H2DEV), capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(r.stdout + r.stderr)
        # render_detach in: RENDER_DETACHED pid=... log=...
        return None  # process tách rời — người gọi tự poll
    return subprocess.run(
        pycmd("pipeline/make_video.py", "--profile", profile, "--slug", slug, "--from", tu_buoc),
        cwd=str(H2DEV), text=True, encoding="utf-8", errors="replace")


def bao_cao(slug_dir: Path, profile: str, slug: str, toi_da_lac: float) -> int:
    state = read_state(slug_dir)
    qc = read_qc_canh(slug_dir)
    final = final_mp4(slug_dir)

    print("\n" + "=" * 62)
    print("BÁO CÁO 1 LỆNH — pipeline_one_shot")
    print("=" * 62)
    steps = ["B8", "B8Q", "B9", "B10", "B11"]
    for s in steps:
        st = state.get(s)
        print(f"  {s}: {'✅ ' + st['at'] if st else '⏳ chưa chạy'} "
              + (f"({st.get('ty_le_lac', '')})" if st and 'ty_le_lac' in st else ""))
    if qc.get("co"):
        danh_gia = "ĐẠT" if qc["ty_le_lac"] <= toi_da_lac else "RỚT"
        print(f"  QC cảnh ({qc['cap_nhat']}): {qc['tong']} cảnh · lạc {qc['lac']} ({qc['ty_le_lac']:.1%}) → {danh_gia} (ngưỡng {toi_da_lac:.0%})")
    if final.get("co"):
        print(f"  final.mp4: {final['mb']} MB (xong {final['xong_luc']})")
    else:
        print("  final.mp4: ⛔ CHƯA CÓ")
    print("=" * 62)

    b11 = state.get("B11")
    ok = bool(b11) and final.get("co") and (not qc.get("co") or qc["ty_le_lac"] <= toi_da_lac)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="toshi-densetsu-jp")
    ap.add_argument("--slug", default="ep02-walton")
    ap.add_argument("--from", dest="tu_buoc", default="B8")
    ap.add_argument("--skip-precheck", action="store_true")
    ap.add_argument("--no-download", action="store_true")
    ap.add_argument("--detach", action="store_true")
    ap.add_argument("--chuan-hoa-png", action="store_true",
                    help="sau render: convert mọi PNG giả (JPEG đội lốt) → PNG thật, giữ nguyên pixel")
    ap.add_argument("--toi-da-lac", type=float, default=0.03)
    args = ap.parse_args()

    slug_dir = H2DEV / "assets" / args.profile / args.slug
    t0 = time.time()

    # ── 1. Pre-check ảnh (fail fast) ──────────────────────────────
    if args.skip_precheck:
        print("[pre-check] bỏ qua (--skip-precheck)")
    else:
        expected = 300
        loi = precheck_images(slug_dir, expected)
        if loi:
            if not args.no_download:
                print(f"[pre-check] {len(loi)} ảnh lỗi → thử download-result để tự phục hồi:")
                rc, out, dt = download_result(args.profile, args.slug, slug_dir)
                print(f"  download-result rc={rc} ({dt:.0f}s): {out[-300:]}")
                loi = precheck_images(slug_dir, expected)  # chạy lại sau download
            if loi:
                print(f"[pre-check] ❌ {len(loi)} ảnh hỏng (không tự sửa):")
                for p, ly in loi[:15]:
                    print(f"  - {p}: {ly}")
                if len(loi) > 15:
                    print(f"  ... và {len(loi) - 15} ảnh nữa")
                print("[pre-check] Xử lý: xoá file hỏng rồi download-result, hoặc nhờ Claude máy 1 vẽ lại.")
                sys.exit(2)
        print(f"[pre-check] ✅ {count_img_ai(slug_dir)} ảnh PNG hợp lệ ({time.time()-t0:.0f}s)")

    # ── 2. Render ──────────────────────────────────────────────────
    print(f"[render] make_video --from {args.tu_buoc}" + (" (DETACH)" if args.detach else ""))
    r = run_render(args.profile, args.slug, args.tu_buoc, args.detach)
    if args.detach:
        # render_detach đã in RENDER_DETACHED — script thoát, người gọi poll log riêng
        return

    # ── 3. Báo cáo ────────────────────────────────────────────────
    if r.returncode != 0:
        print(f"[render] make_video thoát mã {r.returncode} — xem log để biết bước rớt.")
        rc = bao_cao(slug_dir, args.profile, args.slug, args.toi_da_lac)
        sys.exit(rc if rc else 1)

    # ── 4. Chuẩn hoá PNG (chỉ sau render — tránh race) ────────────
    if args.chuan_hoa_png:
        print("[chuẩn hoá] quét PNG giả trong img_ai…")
        n = normalize_img_ai(slug_dir)
        if n:
            print(f"[chuẩn hoá] ✅ convert {n} ảnh JPEG-đội-lốt → PNG thật (pixel giữ nguyên)")
            loi = precheck_images(slug_dir, 300)
            if loi:
                print(f"[chuẩn hoá] ❌ vẫn còn {len(loi)} ảnh lỗi sau convert:")
                for p, ly in loi[:10]:
                    print(f"  - {p}: {ly}")
                sys.exit(2)
            print("[chuẩn hoá] ✅ pre-check lại: toàn bộ PNG hợp lệ")
        else:
            print("[chuẩn hoá] không có ảnh nào cần convert (đã sạch)")

    rc = bao_cao(slug_dir, args.profile, args.slug, args.toi_da_lac)
    print(f"[xong] tổng thời gian {time.time()-t0:.0f}s")
    sys.exit(rc)


if __name__ == "__main__":
    main()
