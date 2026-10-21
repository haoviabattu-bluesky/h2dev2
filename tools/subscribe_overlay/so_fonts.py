# -*- coding: utf-8 -*-
"""find_font(): dò font đậm có ĐỦ glyph cho chữ cần vẽ — không cứng đường dẫn 1 máy.

Kiểm glyph THẬT (vẽ thử từng ký tự, so với glyph .notdef "ô vuông"), vì font mở được
chưa chắc có chữ Nhật/tiếng Việt → render ra ô vuông mà không báo lỗi gì.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Ưu tiên: Noto Sans JP → Yu Gothic → Meiryo → BIZ UD → MS Gothic → font Unicode chung.
CANDIDATES = [
    ("NotoSansJP-Bold.ttf", 0), ("NotoSansJP-Bold.otf", 0), ("NotoSansCJKjp-Bold.otf", 0),
    ("NotoSansCJK-Bold.ttc", 0), ("NotoSansJP-Black.ttf", 0),
    ("YuGothB.ttc", 0), ("meiryob.ttc", 0), ("BIZ-UDGothicB.ttc", 0),
    ("NotoSansJP-VariableFont_wght.ttf", 0), ("NotoSansJP-Regular.ttf", 0),
    ("YuGothM.ttc", 0), ("meiryo.ttc", 0), ("msgothic.ttc", 0),
    ("NotoSans-Bold.ttf", 0), ("segoeuib.ttf", 0), ("arialbd.ttf", 0),
    ("DejaVuSans-Bold.ttf", 0), ("arialuni.ttf", 0),
]


def font_dirs() -> list[Path]:
    dirs = []
    if sys.platform.startswith("win"):
        windir = os.environ.get("WINDIR", r"C:\Windows")
        dirs.append(Path(windir) / "Fonts")
        if os.environ.get("LOCALAPPDATA"):
            dirs.append(Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts")
    dirs += [Path.home() / ".fonts", Path("/usr/share/fonts"), Path("/usr/local/share/fonts"),
             Path("/System/Library/Fonts"), Path("/Library/Fonts")]
    return [d for d in dirs if d.is_dir()]


def _find_file(name: str, dirs: list[Path]) -> Path | None:
    for d in dirs:
        p = d / name
        if p.is_file():
            return p
    low = name.lower()
    for d in dirs:  # Linux/mac: font nằm trong thư mục con, tên hoa-thường lệch
        for p in d.rglob("*"):
            if p.name.lower() == low:
                return p
    return None


def _glyph(font: ImageFont.FreeTypeFont, ch: str) -> bytes:
    im = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(im).text((8, 8), ch, font=font, fill=255)
    return im.tobytes()


def covers(font_path: str | Path, text: str, index: int = 0) -> bool:
    """True nếu font có glyph thật cho MỌI ký tự (không tính khoảng trắng) của text."""
    try:
        font = ImageFont.truetype(str(font_path), 64, index=index)
    except OSError:
        return False
    notdef = _glyph(font, "\U0010FFFD")  # ký tự vùng riêng tư cuối cùng — font nào cũng thiếu
    blank = bytes(96 * 96)
    for ch in set(text):
        if ch.isspace():
            continue
        g = _glyph(font, ch)
        if g == notdef or g == blank:
            return False
    return True


def find_font(texts: list[str], preferred: str | None = None) -> tuple[str, int]:
    """Trả (đường_dẫn, index_ttc) của font đầu tiên vẽ được TẤT CẢ texts. Không có → SystemExit."""
    need = "".join(texts)
    if preferred:
        if not Path(preferred).is_file():
            raise SystemExit(f"[LỖI] font_path trong config không tồn tại: {preferred}")
        if not covers(preferred, need):
            raise SystemExit(f"[LỖI] font {preferred} thiếu glyph cho: {need!r}")
        return str(preferred), 0
    dirs = font_dirs()
    tried = []
    for name, idx in CANDIDATES:
        p = _find_file(name, dirs)
        if not p:
            continue
        tried.append(p.name)
        if covers(p, need, idx):
            return str(p), idx
    raise SystemExit(f"[LỖI] Không tìm được font có đủ glyph cho {need!r}. Đã thử: {tried or 'không có font nào'}."
                     " Cài Noto Sans JP (miễn phí) hoặc ghi font_path trong subscribe_config.json.")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    for lang, pair in {"ja": ("チャンネル登録", "登録済み"), "vi": ("ĐĂNG KÝ", "ĐÃ ĐĂNG KÝ"),
                       "en": ("SUBSCRIBE", "SUBSCRIBED")}.items():
        print(lang, find_font(list(pair)))
