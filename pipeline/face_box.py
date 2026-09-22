"""face_box.py — detect vùng mặt LỚN NHẤT trên ảnh nền thumbnail, trong ĐÚNG hệ toạ độ 1280x720
mà renderer (thumbnail_text.py) thật sự vẽ chữ lên — ảnh nền gốc do ima2/gpti2 sinh ra KHÔNG phải
1280x720 (vd 1536x1024), nên bắt buộc chạy qua `load_bg()` của chính renderer trước khi detect,
không tự viết lại công thức resize/crop (khác coordinate system là toạ độ face lệch khỏi toạ độ
chữ thật). Ngoài hộp mặt thuần, còn xuất "zone" = cột nhân vật mở rộng xuống hết chiều cao khung
(thân + tay cũng phải tránh, Haar chỉ thấy đầu) để renderer sau này dùng làm vùng cấm chữ đè lên.

Dùng:
  py -3.13 face_box.py <đường_dẫn_bg.png> [--pad 0.35]
      [--side center|left|right] [--side-width 0.60] [--fit-height]
      [--subject-side left|center|right] [--photo-scale 1.0] [--flat-bg]
  (các flag layout phía trên PHẢI khớp đúng lệnh render thật đã/sẽ dùng cho ảnh này, để load_bg()
  cho ra đúng cùng một khung 1280x720 — mặc định trùng mặc định của thumbnail_text.py)
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thumbnail_text import load_bg, W as TW, H as TH  # noqa: E402  (dùng ĐÚNG hệ toạ độ renderer)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bg", help="đường dẫn ảnh nền gốc (bất kỳ kích thước)")
    ap.add_argument("--pad", type=float, default=0.35,
                    help="pad DỌC (trên/dưới), tỉ lệ theo w của box mặt — chừa tóc/trán/cằm/cổ")
    ap.add_argument("--pad-x", type=float, default=0.10,
                    help="pad NGANG (trái/phải), tỉ lệ theo w của box mặt — CHỈ chừa vừa đủ mép mặt "
                         "(sửa 2026-09-18: pad ngang dùng chung 0.35 với pad dọc từng đẩy zone.x ra "
                         "xa hơn mép mặt thật rất nhiều, ăn oan chỗ trống lẽ ra chữ dùng được)")
    ap.add_argument("--side", choices=["center", "left", "right"], default="center",
                    help="PHẢI khớp --side dùng khi render thật (ảnh hưởng khung/độ nét)")
    ap.add_argument("--side-width", type=float, default=0.60)
    ap.add_argument("--fit-height", action="store_true")
    ap.add_argument("--subject-side", choices=["left", "center", "right"], default="right")
    ap.add_argument("--photo-scale", type=float, default=1.0)
    ap.add_argument("--flat-bg", action="store_true")
    ap.add_argument("--allow-no-face", action="store_true",
                    help="lane khong dung mat nguoi lam nen (profile.thumbnail.require_face=false, "
                         "vd ngach ke tai lieu Lane A) — khong detect duoc mat thi KHONG loi, tu suy "
                         "zone cam-chu tu --side/--side-width/--subject-side thay vi hop mat that.")
    args = ap.parse_args()

    bg_path = Path(args.bg)
    if not bg_path.exists():
        print(f"LỖI: không tìm thấy ảnh nền: {bg_path}")
        sys.exit(1)

    # y hệt công thức main() của thumbnail_text.py — không tự bịa keep_sharp riêng.
    keep_sharp = min(0.85, args.side_width + 0.04) if args.side in ("left", "right") else 0.44

    try:
        pil_img = load_bg(str(bg_path), args.side, keep_sharp=keep_sharp,
                          fit_height=args.fit_height, subject_side=args.subject_side,
                          photo_scale=args.photo_scale, flat=args.flat_bg)
    except Exception as e:
        print(f"LỖI: load_bg() thất bại trên {bg_path}: {e}")
        sys.exit(1)

    # load_bg() LUÔN trả về đúng khung TWxTH (1280x720) — đây chính là hệ toạ độ chữ thật sẽ vẽ.
    rgb = np.array(pil_img.convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray)

    if len(faces) == 0:
        if not args.allow_no_face:
            print(f"LỖI: KHÔNG detect được khuôn mặt nào trong {bg_path} "
                  f"(sau khi load_bg -> {TW}x{TH})")
            sys.exit(1)
        # Lane KHÔNG dùng mặt người (vd Lane A: "No text, no watermark, no recognizable real
        # person's face" ngay trong prompt sinh nền) — không có mặt để detect là ĐÚNG THIẾT KẾ,
        # không phải lỗi. Suy zone-cấm-chữ từ CHÍNH công thức bố cục side/side-width mà
        # thumbnail_text.py dùng để cắt cột chữ (xem max_w ở đó) — vùng CÒN LẠI (phần dành cho chủ
        # thể) là zone cấm chữ đè lên, full chiều cao vì không biết chủ thể cao thấp thế nào khi
        # không detect được mặt.
        if args.side == "left":
            zx = int(round(TW * args.side_width))
            zw = TW - zx
        elif args.side == "right":
            zx = 0
            zw = int(round(TW * (1 - args.side_width)))
        else:
            zx = zw = 0   # side=center: không có cột chủ thể cố định → không giới hạn thêm
        zy, zh = 0, TH
        x = y = w = h = 0
        face_json = bg_path.parent / "face.json"
        face_json.write_text(
            '{"x": %d, "y": %d, "w": %d, "h": %d, "src": "%s", "no_face": true, '
            '"zone": {"x": %d, "y": %d, "w": %d, "h": %d}}'
            % (x, y, w, h, bg_path.name, zx, zy, zw, zh),
            encoding="utf-8",
        )
        print(f"KHÔNG có mặt (--allow-no-face) → zone suy từ side={args.side} "
              f"side-width={args.side_width}: x={zx} y={zy} w={zw} h={zh}")
        return

    # chọn face có diện tích LỚN NHẤT
    fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])

    pad_x = args.pad_x * fw
    pad_y = args.pad * fw
    x0 = int(round(fx - pad_x))
    y0 = int(round(fy - pad_y))
    x1 = int(round(fx + fw + pad_x))
    y1 = int(round(fy + fh + pad_y))

    # clamp thật sự vào đúng khung renderer [0,TW]x[0,TH]
    x0 = max(0, min(TW, x0))
    y0 = max(0, min(TH, y0))
    x1 = max(0, min(TW, x1))
    y1 = max(0, min(TH, y1))

    x, y, w, h = x0, y0, x1 - x0, y1 - y0

    # ZONE (sửa 2026-09-18 lần 2, định nghĩa trước đó vẫn SAI): chỉ cấm đè MẮT/MŨI/MIỆNG — đè lên
    # TÓC/ĐỈNH ĐẦU/TRÁN là CHẤP NHẬN ĐƯỢC (lần trước zone.y=0 ăn hết tóc/trán, ép chữ nhỏ không cần
    # thiết). zone.x/zone.w vẫn giữ nguyên hộp mặt đã pad 0.35 ở trên. zone.y giờ bắt đầu từ khoảng
    # chân mày (cắt bớt 25% chiều cao hộp mặt PADDED — hộp pad đã bao gồm phần tóc/trán thêm vào),
    # zone đáy vẫn = đáy hộp mặt PADDED + 0.15*h (chừa thêm cằm/cổ).
    zx, zw = x, w
    zy = int(round(y + 0.25 * h))
    zbottom = int(round(y + h + 0.15 * h))
    zy = max(0, min(TH, zy))
    zbottom = max(0, min(TH, zbottom))
    zbottom = max(zy, zbottom)
    zh = zbottom - zy

    out_dir = bg_path.parent
    face_json = out_dir / "face.json"
    face_json.write_text(
        '{"x": %d, "y": %d, "w": %d, "h": %d, "src": "%s", '
        '"zone": {"x": %d, "y": %d, "w": %d, "h": %d}}'
        % (x, y, w, h, bg_path.name, zx, zy, zw, zh),
        encoding="utf-8",
    )

    debug_img = bgr.copy()
    cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 0, 255), 3)          # đỏ = hộp mặt
    cv2.rectangle(debug_img, (zx, zy), (zx + zw, zy + zh), (0, 200, 0), 3)    # xanh lá = zone
    debug_path = out_dir / "face_debug.png"
    cv2.imwrite(str(debug_path), debug_img)

    print(f"FACE x={x} y={y} w={w} h={h}")
    print(f"ZONE x={zx} y={zy} w={zw} h={zh}")


if __name__ == "__main__":
    main()
