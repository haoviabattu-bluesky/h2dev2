"""thumbnail_text.py — overlay chữ tiêu đề TO lên ảnh nền thành thumbnail kiểu kênh Satori/Hàn
(bắt chước simbot2: chữ bold nhiều dòng phủ ~80%, keyword đổi màu trắng/vàng/đỏ, viền đen dày +
bóng đổ, banner đỏ dưới cùng). Dùng PIL vì gpti2 KHÔNG render chữ Nhật/Hàn chuẩn.

Config text (mỗi dòng `MÀU|nội dung`, dòng cuối `BANNER|...`):
  WHITE|もし ある日突然
  YELLOW|あなたが亡くなったら…
  RED|銀行預金は本当に
  RED|家族が引き出せるのか？
  BANNER|銀行員の息子が明かした\"口座凍結\"の真実

Dùng:
  py -3.13 thumbnail_text.py --bg bg.png --text thumb_text.txt --out thumb_final.png
  (bg nên là ảnh nền MỀM/mờ để chữ nổi; tool tự làm tối + phủ gradient nhẹ)
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

W, H = 1280, 720
FONT_BOLD = r"C:\Windows\Fonts\YuGothB.ttc"     # Yu Gothic Bold (đậm, hợp Nhật)
FONT_BANNER = r"C:\Windows\Fonts\YuGothB.ttc"
COLORS = {"WHITE": (255, 255, 255), "YELLOW": (255, 225, 0), "RED": (255, 78, 66),
          "CYAN": (90, 220, 255), "GREEN": (120, 240, 130), "ORANGE": (255, 149, 0)}
REVERSE_COLORS = {v: k for k, v in COLORS.items()}   # chỉ để LABEL dòng khi báo lỗi FACE OVERLAP
STROKE = (15, 15, 15)          # viền đen
BANNER_BG = (200, 20, 20)      # đỏ banner

# Gom bbox tuyệt đối (đã bù viền/bóng đổ) của TỪNG DÒNG main text đã vẽ, để hard gate chống-đè-mặt
# kiểm tra SAU khi vẽ xong toàn bộ main text — xem draw_line() và gate trong main(). BANNER không
# gọi draw_line() (banner tự vẽ riêng ở cuối main()) nên tự động được MIỄN gate.
_TEXT_BBOXES = []   # list[(nhãn, left, top, right, bottom)]
STROKE_W = 2                   # viền cố định, đúng 2px (không scale theo cỡ chữ). 2026-09-17:
                                # từng thử tách "mập" (BOLD_GROW, thân chữ phình riêng bằng cách vẽ
                                # 2 lớp stroke chồng nhau) khỏi viền — nhưng ở size lớn, glyph CJK
                                # phức tạp bị 2 lớp stroke chồng đè GÃY NÉT (user báo "chữ vẽ lỗi").
                                # Quay lại v3: MỘT lớp stroke_width=STROKE_W duy nhất, chỉ giảm từ
                                # 5px (v3) xuống 2px cho viền mỏng hơn.


def _shrink_photo(img, scale, side):
    """Thu nhỏ TOÀN BỘ khung ảnh (kể cả chủ thể sắc nét) rồi ghim về mép ĐỐI DIỆN với chữ, phần
    còn lại lấp ĐEN THUẦN. Dùng khi chữ cần thêm đất mà chủ thể đã chiếm diện tích lớn — khác
    `side_width`/`keep_sharp` (chỉ đổi RANH GIỚI mờ/nét, không đổi KÍCH THƯỚC chủ thể). User yêu
    cầu 2026-09-17: 'ảnh đang chiếm hơi lớn, cho ảnh nhỏ lại tý' — ảnh nhỏ lại THẬT (không phải
    chữ lấn thêm vào ảnh) để chủ thể vẫn còn NGUYÊN VẸN, chỉ bé hơn và lùi sát mép kia."""
    if scale >= 1.0 or side not in ("left", "right"):
        return img
    nw, nh = int(W * scale), int(H * scale)
    small = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    px = W - nw if side == "left" else 0     # chữ bên trái → ảnh ghim mép PHẢI, và ngược lại
    py = (H - nh) // 2
    canvas.paste(small, (px, py))
    return canvas


def load_bg(path, side="center", keep_sharp=0.44, fit_height=False, subject_side="right",
            photo_scale=1.0, flat=False):
    """side=left/right → CHỈ làm mờ nửa bên CHỮ, giữ nửa bên MẶT thật nét.
    (B7Q chấm 'face slightly out of focus' ở MỌI thumbnail vì bản cũ làm mờ CẢ khung.)

    `fit_height=True` (ảnh chân dung DỌC, ví dụ 1024x1536): cover-crop cũ ép khung ngang
    1280x720 lên ảnh dọc thì KHÔNG CÒN BIÊN NGANG để đẩy mặt sang một bên (mặt luôn ở giữa
    khung dù --side là gì — đã dính thật ở ep05, mặt+chữ đè nhau ngay giữa khung). Chế độ
    này scale theo CHIỀU CAO (giữ mặt nét đủ khổ dọc), ghim khối mặt về `subject_side`
    (mặc định phải), rồi LẤP phần khung còn trống bằng chính ảnh đó phóng to làm nền mờ —
    có chỗ trống thật để chữ đứng riêng bên trái, không tranh chỗ với mặt.

    `flat=True`: ảnh nền đã được PROMPT dựng sẵn đúng bố cục (vd nửa trái đen thuần, nửa
    phải là ảnh thật đầy đủ bối cảnh) — bỏ qua HOÀN TOÀN blend mờ/tối + vignette + co ảnh
    82% (`_shrink_photo`/`_darken_edges`), chỉ crop đúng khung 16:9 rồi dùng nguyên vẹn.
    Bài học 2026-09-17 (kenko-chiebukuro ep01, lần 2): dải blend Gaussian 60px ở biên vẫn
    làm mờ mép ảnh thật, và `_shrink_photo` co ảnh còn 82% rồi ghim giữa theo chiều dọc đẻ
    ra viền đen trên/dưới ("thọt lõm") dù ảnh gốc đã cao kín khung — cả hai bước này vốn
    thiết kế cho ảnh THÂN VIDEO cắt tạm làm nền (chủ thể to hết cỡ cần thu bớt + làm mờ giả
    thành 'vùng chữ'), không hợp với ảnh nền RIÊNG đã tự chừa chỗ chữ ngay từ prompt."""
    img = Image.open(path).convert("RGB")
    if flat:
        scale = max(W / img.width, H / img.height)
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
        x = (img.width - W) // 2
        y = (img.height - H) // 2
        return img.crop((x, y, x + W, y + H))
    if fit_height:
        vscale = H / img.height
        sharp_w = max(1, int(img.width * vscale))
        sharp = img.resize((sharp_w, H), Image.LANCZOS)
        bscale = max(W / img.width, H / img.height)
        bg = img.resize((int(img.width * bscale), int(img.height * bscale)), Image.LANCZOS)
        bx, by = (bg.width - W) // 2, (bg.height - H) // 2
        bg = bg.crop((bx, by, bx + W, by + H))
        canvas = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(30))).enhance(0.5)
        if sharp_w >= W:
            sx = (sharp_w - W) // 2 if subject_side == "center" else \
                 (sharp_w - W if subject_side == "right" else 0)
            img = sharp.crop((sx, 0, sx + W, H))
        else:
            px = W - sharp_w if subject_side == "right" else \
                 (W - sharp_w) // 2 if subject_side == "center" else 0
            canvas.paste(sharp, (px, 0))
            img = canvas
        return _shrink_photo(_darken_edges(img), photo_scale, side)
    # crop phủ 16:9 1280x720
    scale = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    x = (img.width - W) // 2
    y = (img.height - H) // 2
    img = img.crop((x, y, x + W, y + H))
    # Vùng chữ (soft) tối/mờ thêm ~20% theo yêu cầu 2026-09-17 (bên chữ đang hơi nhiều chi tiết
    # nền cạnh tranh với chữ) — blur 4→6, brightness 0.62→0.50 (~20% tối hơn), TÁCH BIỆT khỏi vùng
    # chủ thể sắc nét (giữ nguyên 1.08 sáng rõ ở nhánh dưới).
    soft = ImageEnhance.Brightness(img.filter(ImageFilter.GaussianBlur(6))).enhance(0.50)
    if side in ("left", "right"):
        mask = Image.new("L", (W, H), 0)
        cut = int(W * keep_sharp)
        d = ImageDraw.Draw(mask)
        d.rectangle([0, 0, cut, H] if side == "left" else [W - cut, 0, W, H], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(60))   # chuyển tiếp mềm, không lộ đường cắt
        # Vùng SẮC NÉT (ảnh chính) từng bị hạ sáng 0.9 (dịu bớt cho đỡ chói cạnh chữ) — user chê
        # "ảnh bên phải tối quá, yêu cầu sáng rõ nhìn chi tiết như thật" (2026-09-17) → bỏ hạ sáng,
        # tăng nhẹ lên 1.08 để chủ thể nổi bật, rõ chi tiết thay vì dịu/tối.
        img = Image.composite(soft, ImageEnhance.Brightness(img).enhance(1.08), mask)
    else:
        img = soft
    return _shrink_photo(_darken_edges(img), photo_scale, side)


def _darken_edges(img, strength=35):
    # gradient tối 2 mép trên/dưới (giảm 90→35 mặc định: user chê ảnh chính tối, vignette cũ ăn
    # cả vào chủ thể ở mép trên/dưới khung — 2026-09-17)
    ov = Image.new("L", (1, H), 0)
    for i in range(H):
        t = abs(i - H / 2) / (H / 2)
        ov.putpixel((0, i), int(strength * t))
    ov = ov.resize((W, H))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(dark, img, ov)
    return img


def parse_text(path):
    """Tag hỗ trợ hậu tố `:<scale>` để đánh dấu dòng HOOK cần to hơn hẳn phần còn lại — vd
    `RED:1.25|「死ぬな、` — scale nhân với cỡ chữ nền chung (mặc định 1.0, mọi dòng bằng nhau
    như trước nếu không ghi). 2026-09-17: user chỉ ra phân cấp phẳng (mọi dòng cùng cỡ) làm mắt
    không biết bắt vào đâu trước — câu hook (thường màu đỏ) nên NỔI nhất, không chỉ nhờ màu."""
    lines, banner = [], None
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.rstrip("\n")
        if not ln.strip() or "|" not in ln:
            continue
        tag, txt = ln.split("|", 1)
        tag = tag.strip().upper()
        if tag == "BANNER":
            banner = txt
        else:
            color_key, scale = (tag.split(":", 1) + ["1.0"])[:2] if ":" in tag else (tag, "1.0")
            try:
                scale = float(scale)
            except ValueError:
                scale = 1.0
            lines.append((COLORS.get(color_key, COLORS["WHITE"]), txt, scale))
    return lines, banner


CAM_DAU_HANG = "、。！？」』…"     # không được đứng ĐẦU hàng
CAM_CUOI_HANG = "「『"            # không được đứng CUỐI hàng


def _la_katakana(c):
    """Katakana + dấu kéo dài ー + dấu chấm giữa ・ — coi là cùng một cụm từ, không cắt rời."""
    return "゠" <= c <= "ヿ" or c == "ｰ"


def _cat_giua_katakana(tren, duoi):
    return bool(tren and duoi and _la_katakana(tren[-1]) and _la_katakana(duoi[0]))


def _duoc_cat(text, i):
    """Có được ngắt dòng NGAY TRƯỚC ký tự thứ i không (禁則処理)."""
    if i <= 0 or i >= len(text):
        return False
    if text[i] in CAM_DAU_HANG:                 # 、。」… không được mở hàng
        return False
    if text[i - 1] in CAM_CUOI_HANG:            # 「『 không được đóng hàng
        return False
    if _la_katakana(text[i - 1]) and _la_katakana(text[i]):
        return False                            # giữa một cụm katakana = giữa MỘT TỪ
    return True


def wrap_cjk(draw, text, font, max_w):
    """Ngắt dòng CÂN ĐỐI cho tiếng Nhật (không có dấu cách nên không ngắt theo từ được).

    Ngắt tham lam (nhồi đầy hàng trên rồi tràn) đẻ ra hàng mồ côi 1 ký tự — đo thật:
    「物理学者が認め / た」. Nhìn như lỗi hiển thị, và ở thumbnail thì đó là mất khách. Nên chia
    thành N hàng DÀI GẦN BẰNG NHAU, rồi **HÚT từng ranh giới về vị trí ngắt HỢP LỆ gần nhất**.

    ⚠️ Hút, chứ không phải "nắn sau khi đã chia". Bản trước sửa vi phạm bằng cách đẩy ký tự qua
    lại giữa hai hàng liền kề trong một vòng lặp — với cụm katakana dài thì mỗi vòng lại đẻ ra vi
    phạm mới ở ranh giới kế tiếp, kết quả vỡ vụn thành 「消え/た/パ/イロット/が」. Chọn đúng điểm
    cắt ngay từ đầu thì không có gì phải nắn.

    Ba luật cấm: dấu đóng câu không mở hàng · dấu mở ngoặc không đóng hàng · **không cắt giữa cụm
    katakana** (パイロット là một từ; cắt ra 「パイ/ロット」 người Nhật đọc vấp ngay — QC vision
    bắt đúng lỗi này). Chữ Hán và hiragana cắt giữa vẫn đọc được nên không cấm.
    """
    if draw.textlength(text, font=font) <= max_w:
        return [text]
    n = 2
    while n <= 6:
        rows, truoc = [], 0
        for k in range(1, n):
            muc = round(len(text) * k / n)
            cat = None
            for lech in range(0, 5):            # hút ra hai phía, gần nhất thắng
                for j in (muc - lech, muc + lech):
                    if j > truoc and _duoc_cat(text, j):
                        cat = j
                        break
                if cat:
                    break
            if cat is None:
                continue                        # không có chỗ hợp lệ ⇒ bỏ ranh giới này
            rows.append(text[truoc:cat])
            truoc = cat
        rows.append(text[truoc:])
        rows = [r for r in rows if r]
        if rows and all(draw.textlength(r, font=font) <= max_w for r in rows):
            return rows
        n += 1
    return [text]


LINE_LEAD = 1.18   # hệ số giãn dòng — dùng THỐNG NHẤT giữa fit_font và lúc vẽ thật.
                   # 1.08 (bản trước) từng ổn khi viền chỉ scale theo size, nhưng sau khi thêm
                   # BOLD_GROW (thân chữ phình thêm px CỐ ĐỊNH mỗi phía, không co giãn theo size)
                   # thì 2 dòng liền kề ở size lớn CHẠM/ĐÈ LÊN NHAU thật (đo thật 2026-09-17,
                   # simbot2-04 bản cũ 2 dòng đỏ "尊厳奪う"/"冷酷な実態" dính vào nhau) — nới lên
                   # 1.18 để chừa đúng phần BOLD_GROW+STROKE_W bulge mà không mất hết chỗ tăng cỡ chữ.


def fit_font(draw, lines, max_w, max_h=None, max_size=160, wrap=False):
    """Cỡ chữ LỚN NHẤT còn vừa khung — tối đa hoá cả BỀ NGANG lẫn CHIỀU CAO, không chỉ dừng ở
    một trần cố định thấp. `wrap=False`: mỗi dòng phải vừa 1 hàng ngang; `wrap=True`: cho ngắt
    dòng để giữ cỡ to với câu dài.

    Bài học (2026-09-17, ep1 lần đầu): bản cũ chỉ kiểm BỀ NGANG của dòng dài nhất và dừng ngay ở
    max_size=92 nếu đã vừa — không bao giờ thử to hơn dù còn thừa cả khung ngang lẫn khung dọc
    (khoảng trống ~200px giữa khối chữ và banner). Nay kiểm CẢ 3 dòng riêng theo bề ngang VÀ tổng
    chiều cao khối so với `max_h`, bắt đầu từ `max_size` cao rồi giảm dần — chữ sẽ to hết cỡ mà
    khung cho phép theo đúng yêu cầu "chữ to hết khung bên trái"."""
    # `lines` = (color, text, scale) — scale khác 1.0 đánh dấu dòng HOOK cần TO HƠN base size
    # theo tỉ lệ riêng (xem parse_text). `size` tìm được ở đây là size NỀN (scale=1.0); dòng có
    # scale>1 dùng int(size*scale) khi build font thật — cả 2 nhánh dưới đều kiểm khung ở đúng
    # size THẬT của từng dòng (không phải size nền) để không tràn khung.
    if not wrap:
        size = max_size
        while size > 30:
            ok_w = True
            total_h = 0
            for _, t, scale in lines:
                sz = max(20, int(size * scale))
                f = ImageFont.truetype(FONT_BOLD, sz)
                pad = 2 * STROKE_W   # cộng bù viền
                if draw.textlength(t, font=f) + pad > max_w:
                    ok_w = False
                    break
                total_h += int(sz * LINE_LEAD)
            if ok_w and (max_h is None or total_h <= max_h):
                return size
            size -= 2
        return 30
    for size in range(max_size, 29, -2):
        total_h = 0
        for _, t, scale in lines:
            sz = max(20, int(size * scale))
            f = ImageFont.truetype(FONT_BOLD, sz)
            total_h += len(wrap_cjk(draw, t, f, max_w)) * int(sz * LINE_LEAD)
        if max_h is None or total_h <= max_h:
            return size
    return 30


def fit_banner_font(draw, text, box_w, max_size=110):
    """Cỡ chữ banner LỚN NHẤT còn vừa bề ngang khung dưới — tách khỏi tỉ lệ cố định theo cỡ chữ
    tiêu đề (bản cũ `size*0.74` luôn để thừa lề hai bên dù tiêu đề đã to), để banner cũng
    "cho hết dòng khung dưới" như tiêu đề, không phụ thuộc cỡ chữ tiêu đề bao nhiêu."""
    size = max_size
    while size > 28:
        f = ImageFont.truetype(FONT_BANNER, size)
        if draw.textlength(text, font=f) <= box_w:
            return size
        size -= 2
    return 28


def _ink_bbox_raster(font, text):
    """Bù lề bằng `draw.textbbox()` VẪN SAI cho dấu mở ngoặc 「 — đo được thật (2026-09-17):
    `textbbox(anchor='la')` của riêng glyph「 trả về (0, y0, 112, y1) ở cỡ 112px — đúng NGUYÊN
    bề rộng 1 em (hộp thiết kế/advance của font), KHÔNG PHẢI hộp mực thật; mực thật (nét vẽ
    nhìn thấy) của「 nằm lệch hẳn sang phải trong hộp đó, đo pixel thật lệch tới ~70px. Dùng
    `textbbox` để bù lề trái do đó vẫn để dòng bắt đầu bằng「 thụt sâu vào trong.

    Fix: KHÔNG tin `textbbox`, vẽ thật ra 1 canvas nháp rồi dùng `Image.getbbox()` (quét pixel
    thật, không phải metrics khai báo của font) để lấy đúng mép mực nhìn thấy.
    Trả về (left, top, right, bottom) tính từ điểm neo pen ở (pad, 10) trên canvas nháp — trừ
    lại (pad, 10) trước khi dùng."""
    asc, desc = font.getmetrics()
    pad = font.size
    w = int(font.getlength(text)) + pad * 2 + 20
    h = asc + desc + 20
    tmp = Image.new("L", (max(w, 10), max(h, 10)), 0)
    ImageDraw.Draw(tmp).text((pad, 10), text, font=font, fill=255, anchor="la")
    box = tmp.getbbox()
    if box is None:
        return 0, 0, 0, 0
    return box[0] - pad, box[1] - 10, box[2] - pad, box[3] - 10


def ink_x(draw, cx, text, font, ax):
    """Trả về pixel-x thật để vẽ sao cho MỰC (ink) của dòng chữ bám sát `cx`, thay vì bám theo
    hộp advance-width mặc định của font (xem `_ink_bbox_raster` — lý do KHÔNG dùng textbbox)."""
    if ax not in ("l", "r"):
        return cx
    left, _, right, _ = _ink_bbox_raster(font, text)
    return cx - left if ax == "l" else cx - right


def draw_line(draw, cx, y, text, font, color, ax="m"):
    """MỘT lớp stroke_width=STROKE_W duy nhất (v3) — bản 2 lớp (silhouette to + lõi trong, để tách
    "mập" khỏi "viền") làm glyph CJK phức tạp GÃY NÉT ở size lớn, đã bỏ (2026-09-17)."""
    x = ink_x(draw, cx, text, font, ax)
    anchor = ax + "a"
    # bóng đổ
    draw.text((x + 4, y + 5), text, font=font, fill=(0, 0, 0), anchor=anchor)
    # ĐỎ viền đen trên nền tối = chìm nghỉm (B7Q bắt: "red text lacks brightness").
    # Chữ đỏ phải viền TRẮNG mới nổi; trắng/vàng thì viền đen như cũ.
    r, g, b = color
    outline = (255, 255, 255) if (r > 200 and g < 120 and b < 120) else STROKE
    draw.text((x, y), text, font=font, fill=color, anchor=anchor,
              stroke_width=STROKE_W, stroke_fill=outline)

    # Thu bbox tuyệt đối cho hard gate chống-đè-mặt (gate chạy ở main(), draw_line CHỈ thu thập,
    # không tự raise). left/top/right/bottom ở đây là offset TƯƠNG ĐỐI so với pen (x,y) đo bằng
    # _ink_bbox_raster() — với anchor "la" (ax="l", trường hợp DUY NHẤT lane satori dùng: chữ luôn
    # neo trái) phép cộng thẳng x+left/x+right là CHÍNH XÁC (cùng kiểu anchor "la" ở cả lúc đo lẫn
    # lúc vẽ thật, nên chỉ là tịnh tiến theo pen — đã verify thực nghiệm). Cộng thêm STROKE_W+4 mỗi
    # phía để bù viền (stroke_width vẽ đè ra ngoài glyph) và bóng đổ (lệch (+4,+5)).
    left, top, right, bottom = _ink_bbox_raster(font, text)
    pad = STROKE_W + 4
    label = REVERSE_COLORS.get(color, str(color))
    _TEXT_BBOXES.append((label, x + left - pad, y + top - pad, x + right + pad, y + bottom + pad))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", required=True, help="ảnh nền (nên mềm/mờ)")
    ap.add_argument("--text", required=True, help="file config MÀU|nội dung")
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=float, default=0.035, help="lề trên (tỉ lệ H)")
    ap.add_argument("--side", choices=["center", "left", "right"], default="center",
                    help="dồn chữ sang 1 bên để CHỪA CHỖ CHO MẶT (nền chủ thể lệch bên kia)")
    ap.add_argument("--side-width", type=float, default=0.60,
                    help="bề rộng vùng chữ khi --side left/right (tỉ lệ W) — chữ TO hơn thì tăng số này")
    ap.add_argument("--fit-height", action="store_true",
                    help="ảnh chân dung DỌC: scale theo chiều cao, ghim mặt về --subject-side, "
                         "lấp chỗ trống bằng nền mờ (dùng khi cover-crop cũ làm mặt luôn ở giữa)")
    ap.add_argument("--subject-side", choices=["left", "center", "right"], default="right",
                    help="mặt ghim về bên nào khi --fit-height (đi cùng --side đối diện cho chữ)")
    ap.add_argument("--max-size", type=int, default=160, help="trần cỡ chữ (px)")
    ap.add_argument("--wrap", action="store_true",
                    help="cho phép ngắt xuống hàng để GIỮ CỠ CHỮ TO (ngách đòi chữ phủ 30-50%% khung)")
    ap.add_argument("--fit-each", action="store_true",
                    help="SENIOR TYPOGRAPHY (lane satori, user khoá 2026-09-17): fit TỪNG DÒNG độc lập "
                         "theo bề ngang cột (dòng ngắn được to hơn dòng dài, không để dòng dài nhất "
                         "ép cả khối), rồi xếp khối SÁT nhau — không dàn đều khoảng dư xuống hết "
                         "chiều cao. `MÀU:scale|` lúc này là hệ số GHÌM (≤1) dòng cần nhỏ hơn mức fit.")
    ap.add_argument("--gap-max", type=float, default=0.25,
                    help="--fit-each: trần khoảng dư chèn giữa các dòng, tỉ lệ theo chiều cao dòng")
    ap.add_argument("--per-line-fit", action=argparse.BooleanOptionalAction, default=True,
                    help="MẶC ĐỊNH BẬT (2026-09-18): một side-width CHUNG cho cả khối làm dòng NGẮN "
                         "(vd WHITE) bị dòng DÀI (vd RED) kéo nhỏ theo dù dòng ngắn còn thừa chỗ. Mỗi "
                         "dòng tự có TRẦN CHIỀU NGANG riêng = khoảng cách margin→zone.x (đọc từ "
                         "face.json) nếu dải y của dòng đó giao với dải y của zone, hoặc margin→(W-"
                         "margin) [full khung] nếu không giao (chỗ đó không có mặt). Chỉ áp dụng khi "
                         "--side left (side duy nhất lane satori dùng) — side khác rơi về hành vi "
                         "--fit-each cũ (một max_w chung). Tắt bằng --no-per-line-fit.")
    ap.add_argument("--photo-scale", type=float, default=1.0,
                    help="thu nhỏ TOÀN BỘ ảnh nền (kể cả chủ thể) rồi ghim về mép đối diện chữ, "
                         "phần trống lấp đen — dùng khi ảnh chính chiếm diện tích quá lớn (<1.0)")
    ap.add_argument("--flat-bg", action="store_true",
                    help="ảnh nền đã tự chừa đúng bố cục (nửa chữ đen thuần + nửa ảnh thật) ngay "
                         "từ prompt — bỏ qua blend mờ/tối + vignette + co ảnh, dùng nguyên vẹn")
    args = ap.parse_args()

    # vùng MỜ phải khớp đúng vùng CHỮ (side_width) — trước đây keep_sharp=0.44 cố định độc lập với
    # side_width, chữ to ra là lấn vào vùng SẮC NÉT lởm chởm phía sau chữ. Nay khoá theo nhau + thêm
    # đệm nhỏ để dải chuyển mờ (gaussian 60px) không lộ ranh giới ngay dưới chữ.
    keep_sharp = min(0.85, args.side_width + 0.04) if args.side in ("left", "right") else 0.44
    img = load_bg(args.bg, args.side, keep_sharp=keep_sharp, fit_height=args.fit_height,
                 subject_side=args.subject_side, photo_scale=args.photo_scale, flat=args.flat_bg)
    draw = ImageDraw.Draw(img)
    lines, banner = parse_text(args.text)

    margin = int(W * 0.045)

    # Đọc face.json SỚM (trước khi tính layout) — --per-line-fit cần zone.x để quyết định trần
    # chiều ngang từng dòng, và hard gate ở cuối cũng cần y hệt zone này. Đọc MỘT LẦN, dùng lại cho
    # cả hai chỗ để không lệch dữ liệu. KHÔNG mặc định, KHÔNG bỏ qua nếu thiếu — bắt buộc chạy
    # face_box.py trước (xem lỗi bên dưới).
    face_json_path = Path(args.bg).parent / "face.json"
    if not face_json_path.exists():
        print(f"LỖI: THIẾU face.json, chạy face_box.py trước ({face_json_path})")
        sys.exit(1)
    face_data = json.loads(face_json_path.read_text(encoding="utf-8"))
    if "zone" not in face_data:
        print(f"LỖI: face.json ({face_json_path}) thiếu khoá 'zone', chạy lại face_box.py")
        sys.exit(1)
    zone = face_data["zone"]
    zx, zy, zw, zh = zone["x"], zone["y"], zone["w"], zone["h"]
    zx0, zy0, zx1, zy1 = zx, zy, zx + zw, zy + zh

    # Chữ căn giữa + ảnh chân dung mặt ở giữa = chữ đè lên mặt, mất cả hai (B7Q bắt được ở ep08).
    # --side left/right thu hẹp vùng chữ về một bên, nhường nửa kia cho khuôn mặt.
    # Neo SÁT MÉP (trái/phải) thay vì CĂN GIỮA cột — bài học 2026-09-17 (ep1): căn giữa cột để hờ
    # khoảng trống đều 2 bên mỗi dòng NGẮN, nhìn "chữ trôi giữa khung" thay vì bám sát mép khung như
    # thumbnail kênh mẫu; neo mép còn giúp dòng dài nhất không đẩy tâm dòng lấn thêm vào vùng ảnh.
    if args.side == "center":
        max_w = W - 2 * margin
        cx, ax = W // 2, "m"
    elif args.side == "left":
        max_w = int(W * args.side_width) - margin
        cx, ax = margin, "l"
    else:
        max_w = int(W * args.side_width) - margin
        cx, ax = W - margin, "r"
    top_y = int(H * args.top)

    # Banner tính TRƯỚC để tiêu đề biết chính xác còn bao nhiêu chỗ mà lấp cho hết, thay vì
    # đoán một tỉ lệ khung cố định (bài học ep1: 0.55*H để hờ ~200px trống giữa chữ và banner).
    bfont = bh = by0 = None
    if banner:
        box_w = (W - 2 * margin) - 48   # trừ đệm trong cho banner khỏi dính sát viền
        bsize = fit_banner_font(draw, banner, box_w, max_size=110)
        bfont = ImageFont.truetype(FONT_BANNER, bsize)
        # Ôm SÁT chữ banner — trước dùng hệ số cố định *1.55 luôn dư một khoảng lớn quanh chữ dù
        # banner đã to hết bề ngang (user chốt 2026-09-17: "ô đỏ chỉ cần to hơn chữ vài px thôi").
        # Đo MỰC THẬT bằng raster (không dùng textbbox — xem _ink_bbox_raster) rồi cộng đệm.
        # BUG THẬT đã vá 2026-09-17: hệ số *0.87 (bản trước, nhường đất cho ảnh nhân vật) co hộp
        # NHỎ HƠN cả chiều cao mực đo được — chữ (đặc biệt nét đuôi Hiragana như した/けた) tràn
        # ra ngoài viền đỏ, đo thật trên test_v3-opus. Bỏ hệ số co, tăng đệm 16→40px (đối xứng
        # trên/dưới quanh tâm chữ, vì vẽ bằng anchor="mm") — hộp giờ LUÔN ≥ chiều cao mực thật.
        _, bbox_top, _, bbox_bot = _ink_bbox_raster(bfont, banner)
        bh = int((bbox_bot - bbox_top) + 40)
        by0 = H - bh - int(H * 0.03)

    gap = int(H * 0.02)
    max_h = (by0 - gap - top_y) if banner else (int(H * 0.9) - top_y)
    base_size = fit_font(draw, lines, max_w, max_h, args.max_size, args.wrap)

    # Gộp trước thành DANH SÁCH HÀNG THẬT (sau khi ngắt dòng) rồi mới vẽ — cần biết TỔNG SỐ HÀNG
    # để rải đều xuống hết `max_h`. Bài học (2026-09-17, ep1): cỡ chữ bị CHIỀU NGANG ép nhỏ (ép bởi
    # `max_w` của cột chữ, không phải `max_h`) nên khối chữ vẽ xong chỉ chiếm 449/623px chiều cao —
    # 174px trống phía dưới, nhìn thừa hẳn khoảng trắng so với thumbnail kênh mẫu (chữ phủ ĐẦY khung,
    # không có mép trống). Cỡ chữ vẫn giữ nguyên (đã tối đa theo bề ngang cột), nhưng dãn KHOẢNG CÁCH
    # dòng ra để cả khối chữ chiếm ĐỦ `max_h`, không co cụm ở phần trên rồi bỏ trống phần dưới.
    # Mỗi dòng dùng font size RIÊNG = base_size*scale (xem parse_text) — dòng hook (scale>1) to hơn
    # hẳn phần còn lại thay vì đồng loạt 1 cỡ (user chốt 2026-09-17: mắt cần biết bắt vào đâu trước).
    rows = []   # (color, hang, font, line_h)
    row_caps = []   # song song với rows, CHỈ có ý nghĩa khi per-line-fit thật sự chạy (side=left)
    per_line_active = args.per_line_fit and args.side == "left"
    even_rows = None
    if per_line_active:
        # 3 DÒNG TO GẦN BẰNG NHAU (2026-09-18 lần 5 — thay HẲN cơ chế băng tỉ lệ 0.22/0.44/0.34 +
        # mọi hệ số `:scale` riêng từng dòng). Cỡ CHUNG = MIN của 3 cỡ tối đa riêng (mỗi dòng fit
        # theo ĐÚNG trần ngang của nó, bỏ qua scale ghim trong thumb_text.txt) — đây là cỡ LỚN NHẤT
        # mà CẢ 3 dòng đều vừa trần của mình. Dòng nào còn dư trần (max riêng > cỡ chung) được nới
        # thêm tối đa 12%, không hơn — giữ 3 dòng nhìn gần bằng nhau thay vì phân cấp bậc thang.
        if len(lines) != 3:
            print(f"LỖI: per-line-fit (3 dòng đều) yêu cầu ĐÚNG 3 dòng main, có {len(lines)}")
            sys.exit(1)

        cap_zone_w = max(1, zx - margin)          # DÒNG 1 (WHITE) + DÒNG 2 (YELLOW)
        cap3_w = max(1, int(0.88 * W) - margin)   # DÒNG 3 (RED) — được đè vai/áo
        caps = [cap_zone_w, cap_zone_w, cap3_w]

        own_max = [fit_font(draw, [(c, t, 1.0)], cap_w, None, args.max_size)
                   for (c, t, _), cap_w in zip(lines, caps)]
        common_size = min(own_max)
        sizes = [max(20, min(m, int(common_size * 1.12))) for m in own_max]

        fonts = [ImageFont.truetype(FONT_BOLD, sz) for sz in sizes]
        lhs = [int(sz * LINE_LEAD) for sz in sizes]

        TOP = int(H * 0.03)
        BOT = by0 if banner else int(H * 0.9)
        available = max(1, BOT - TOP)
        total_text_h = sum(lhs)
        n = len(lines)
        gap_v = max(0.0, (available - total_text_h) / (n + 1))   # rải đều, kể cả mép trên/dưới

        even_rows = []   # (color, text, font, lh, y_start, cap_w)
        y_cursor = TOP + gap_v
        for (color, text, _), f, lh, cap_w in zip(lines, fonts, lhs, caps):
            even_rows.append((color, text, f, lh, int(round(y_cursor)), cap_w))
            y_cursor += lh + gap_v

        base_size = "/".join(str(sz) for sz in sizes)
    elif args.fit_each:
        # Mỗi dòng tự to hết bề ngang cột (trần --max-size), nhân hệ số ghìm scale (≤1). Nếu tổng
        # chiều cao vượt max_h thì co CẢ khối theo cùng tỉ lệ (giữ tương quan giữa các dòng).
        sizes = [int(fit_font(draw, [(c, t, 1.0)], max_w, None, args.max_size) * min(scale, 1.0))
                 for c, t, scale in lines]
        total = sum(int(s * LINE_LEAD) for s in sizes)
        if total > max_h:
            k = max_h / total
            sizes = [max(20, int(s * k)) for s in sizes]
        for (color, text, _), sz in zip(lines, sizes):
            f = ImageFont.truetype(FONT_BOLD, sz)
            rows.append((color, text, f, int(sz * LINE_LEAD)))
        base_size = "/".join(str(s) for s in sizes)
    else:
        for color, text, scale in lines:
            sz = max(20, int(base_size * scale))
            f = ImageFont.truetype(FONT_BOLD, sz)
            lh = int(sz * LINE_LEAD)
            for hang in (wrap_cjk(draw, text, f, max_w) if args.wrap else [text]):
                rows.append((color, hang, f, lh))

    total_natural = sum(lh for *_, lh in rows)
    extra_per_row = max(0, max_h - total_natural) // len(rows) if rows else 0
    if (args.fit_each or per_line_active) and rows:
        # khối SÁT nhau: khoảng dư chèn giữa dòng bị trần theo chiều cao dòng, phần còn lại bỏ trống
        # phía dưới (sát banner) thay vì kéo giãn 3 dòng ra thành 3 mảnh rời.
        extra_per_row = min(extra_per_row, int(args.gap_max * min(lh for *_, lh in rows)))

    y = top_y
    _TEXT_BBOXES.clear()
    for i, (color, hang, f, lh) in enumerate(rows):
        draw_line(draw, cx, y, hang, f, color, ax)
        y += lh + extra_per_row

    if even_rows is not None:
        # Vẽ 3 dòng RẢI ĐỀU — mỗi dòng ở đúng y_start đã tính ở trên (khoảng cách đều nhau, kể cả
        # mép trên/dưới), KHÔNG dùng extra_per_row/gap_max.
        for color, text, f, lh, y_start, cap_w in even_rows:
            draw_line(draw, cx, y_start, text, f, color, ax)
        for (color, text, f, lh, y_start, cap_w), (label, l, t, r, b) in \
                zip(even_rows, _TEXT_BBOXES):
            boundary = margin + cap_w
            khe = boundary - r
            print(f"{label} | y={y_start} | size={f.size} | bbox=({l},{t},{r},{b}) | "
                  f"trần={cap_w} | khe={khe}px")

    # === HARD GATE chống chữ đè vùng cấm (face + thân/tay) — chạy SAU main text, TRƯỚC banner và
    # TRƯỚC img.save(). zx/zy/zw/zh (zone) đã đọc từ face.json ở ĐẦU main() — dùng lại nguyên vẹn,
    # KHÔNG đọc lại. Dùng khoá "zone", KHÔNG dùng hộp mặt thuần x/y/w/h. BANNER không gọi
    # draw_line() nên không nằm trong _TEXT_BBOXES — tự động được MIỄN gate. Với chế độ "3 dòng
    # đều", DÒNG 3 (RED, index cuối) cũng được MIỄN gate theo yêu cầu ("được đè vai/áo") — chỉ
    # DÒNG 1+2 (WHITE/YELLOW) bị kiểm.
    gate_bboxes = _TEXT_BBOXES[:2] if even_rows is not None else _TEXT_BBOXES
    violations = []
    min_gap = None
    for label, l, t, r, b in gate_bboxes:
        ox0, ox1 = max(l, zx0), min(r, zx1)
        oy0, oy1 = max(t, zy0), min(b, zy1)
        if ox1 > ox0 and oy1 > oy0:
            violations.append((label, l, t, r, b, ox1 - ox0))
        else:
            gap = (zx0 - r) if r <= zx0 else (l - zx1)
            if min_gap is None or gap < min_gap:
                min_gap = gap

    if violations:
        for label, l, t, r, b, lan in violations:
            print(f"FACE OVERLAP | dòng={label} | bbox=({l},{t},{r},{b}) | "
                  f"zone=({zx},{zy},{zw},{zh}) | side-width={args.side_width} | lấn {lan}px")
        sys.exit(1)

    print(f"FACE GATE PASS | side-width={args.side_width} | khe hẹp nhất={min_gap}px")

    # banner đỏ dưới cùng — chữ đã tính TO HẾT BỀ NGANG khung ở fit_banner_font phía trên
    if banner:
        draw.rounded_rectangle([margin - 6, by0, W - margin + 6, by0 + bh], radius=14,
                               fill=BANNER_BG, outline=(255, 255, 255), width=4)
        draw.text((W // 2, by0 + bh // 2), banner, font=bfont, fill=(255, 255, 255),
                  anchor="mm", stroke_width=2, stroke_fill=(90, 0, 0))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out, quality=95)
    print(f"✓ Thumbnail: {args.out} ({W}x{H}, font nền {base_size}px, chữ {args.side})")


if __name__ == "__main__":
    main()
