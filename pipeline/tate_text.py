# -*- coding: utf-8 -*-
r"""tate_text.py — dựng track chữ DỌC (縦書き) kiểu kênh mẫu Lane F/teinengo-real: mỗi câu narration
hiện trong 1 hộp trắng chữ nhật bo góc, câu thoại「」hiện trong 1 bóng thoại hình ellipse — cả hai
xếp CHỮ TỪ TRÊN XUỐNG, CỘT TỪ PHẢI SANG TRÁI (tategaki), đặt vào 1/3 khung hình (mặc định bên TRÁI,
khớp `style_suffix` đã dặn Fable chừa trống — xem prompt_doan.py::_tate_note).

VÌ SAO CÓ FILE NÀY (anh duyệt Q2(A) 2026-09-21, docs/PHUONG_AN_LANE_F_BUOC2_3.md §1/C4)
- Khung hình THẬT kênh mẫu (docs/laneF_visual_ref/) KHÔNG cháy phụ đề ngang ở đáy — chữ nằm dọc
  trong hộp, đây là "chữ ký" hình ảnh của định dạng【漫画】, không phải phụ đề thường.
- ffmpeg `drawtext` KHÔNG vẽ được chữ dọc tiếng Nhật đúng kiểu → tự dựng bằng Pillow (xếp CHỮ
  TỪNG KÝ TỰ theo cột, không dùng raqm 'ttb' vì font Windows không khai đủ OpenType 'vert').
- Mỗi cue render 1 clip video (ảnh tĩnh giữ đúng thời lượng cue, cùng kỹ thuật variable-duration
  concat mà assemble.py đã dùng cho ảnh nền) rồi NỐI thành 1 track trong suốt → assemble.py chỉ cần
  overlay TRACK NÀY lên video nền bằng 1 filter `overlay` DUY NHẤT (không chèn hàng trăm filter
  `enable=between()` vào filter_complex vốn đã lớn).

GIỚI HẠN ĐÃ BIẾT (v1, chấp nhận cho lượt đầu — ghi rõ để không tưởng nhầm là lỗi):
- Chỉ xoay riêng dấu trường âm 'ー'; ngoặc/dấu câu khác KHÔNG tự xoay theo chuẩn in ấn tategaki.
- Số Ả Rập nhiều chữ số xếp mỗi chữ số 1 hàng (tategumi suuji đúng kiểu KHÔNG viết ngang theo cụm).
- Cue quá dài so với hộp (> max_cols × max_chars_per_col ký tự) bị CẮT + thêm '…' — hiếm gặp vì
  cue đã là 1 câu ngắn (srt_from_script.py), nhưng vẫn có thể xảy ra.

Dùng độc lập (test offline, 0đ):
  py -3.13 tate_text.py --srt test.srt --out tate_track.mov --w 1920 --h 1080 --side left
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
FF = imageio_ffmpeg.get_ffmpeg_exe()

CHOONPU = "ー"
MIN_CUE_SEC = 0.6          # cue ngắn hơn mức này gộp vào cue TRƯỚC (tránh chữ nháy quá nhanh)

# ---------------------------------------------------------------- font resolver
_FONT_DIRS = [Path(r"C:\Windows\Fonts")]
_CANDIDATES = {
    "yu mincho":  [("yumin.ttf", 0), ("YuMincho.ttf", 0), ("YuMincho.ttc", 0), ("yumin.ttc", 0)],
    "yu gothic":  [("YuGothM.ttc", 0), ("yugothm.ttc", 0), ("YuGothR.ttc", 0)],
    # Lane N 2026-09-30: anh chê chữ Lane M (Yu Gothic Medium) nhạt → bản Bold, thiếu thì rơi về Medium.
    "yu gothic bold": [("YuGothB.ttc", 0), ("yugothb.ttc", 0), ("YuGothM.ttc", 0)],
    "ms gothic":  [("msgothic.ttc", 0)],
    "ms mincho":  [("msmincho.ttc", 0)],
    "meiryo":     [("meiryo.ttc", 0), ("Meiryo.ttc", 0)],
}
_FALLBACK_CHAIN = ["ms gothic", "yu gothic", "meiryo", "ms mincho"]
_warned = set()


def load_font(name, size):
    """Tra font theo TÊN (khớp voice/sub_font kiểu 'Yu Gothic'), có fallback theo máy — máy 2 có
    thể thiếu Yu Mincho (đã xác nhận trên máy 1 lúc viết file này) → dò sang MS Gothic/Meiryo."""
    key = (name or "").strip().lower()
    order = ([key] if key in _CANDIDATES else []) + [k for k in _FALLBACK_CHAIN if k != key]
    for k in order:
        for fname, idx in _CANDIDATES.get(k, []):
            for d in _FONT_DIRS:
                p = d / fname
                if p.exists():
                    try:
                        f = ImageFont.truetype(str(p), size, index=idx)
                        if k != key and key not in _warned:
                            print(f"  (tate_text: không có font '{name}' → dùng '{k}' thay)")
                            _warned.add(key)
                        return f
                    except OSError:
                        continue
    raise SystemExit(f"✗ tate_text: không tìm được font tiếng Nhật nào trên máy này (thử: {name!r} + fallback)")


# ---------------------------------------------------------------- cue parsing (khớp assemble.parse_srt_cues)
def parse_cues(srt_path):
    txt = Path(srt_path).read_text(encoding="utf-8")
    out = []
    for blk in re.split(r"\n\s*\n", txt.strip()):
        L = blk.splitlines()
        tl = next((x for x in L if "-->" in x), None)
        if not tl:
            continue
        m = re.match(r"\s*(\d\d):(\d\d):(\d\d)[,.](\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d\d\d)", tl)
        if not m:
            continue
        h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
        t0 = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000
        t1 = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000
        text = "".join(L[L.index(tl) + 1:]).strip()
        if text:
            out.append({"start": t0, "end": max(t1, t0 + 0.1), "text": text})
    return out


def merge_short(cues, min_dur=MIN_CUE_SEC):
    """Cue < min_dur gộp NGƯỢC vào cue trước (nối chữ, kéo dài mốc end) — cue đầu tiên nếu ngắn
    thì gộp XUÔI vào cue sau (không có cue trước để gộp)."""
    if not cues:
        return []
    out = [dict(cues[0])]
    for c in cues[1:]:
        if c["end"] - c["start"] < min_dur and out:
            out[-1]["text"] = (out[-1]["text"] + c["text"])
            out[-1]["end"] = c["end"]
        else:
            out.append(dict(c))
    if out and out[0]["end"] - out[0]["start"] < min_dur and len(out) > 1:
        out[1]["text"] = out[0]["text"] + out[1]["text"]
        out[1]["start"] = out[0]["start"]
        out = out[1:]
    return out


# ---------------------------------------------------------------- render 1 cue → PNG RGBA
def _columns(text, max_chars_per_col, max_cols):
    """Ký tự KHÔNG kể 「」bên ngoài (khung bóng thoại tự ngụ ý hội thoại). Cắt quá tay + '…'."""
    t = text.strip()
    is_dialogue = t.startswith("「")
    if is_dialogue:
        t = t.strip("「」")
    chars = list(t)
    cap = max_chars_per_col * max_cols
    if len(chars) > cap:
        chars = chars[:max(1, cap - 1)] + ["…"]
    cols = [chars[i:i + max_chars_per_col] for i in range(0, len(chars), max_chars_per_col)] or [[]]
    return cols, is_dialogue


def render_cue_image(text, W, H, side, font_narration, font_dialogue, font_size,
                      max_chars_per_col, max_cols):
    cols, is_dialogue = _columns(text, max_chars_per_col, max_cols)
    font = load_font(font_dialogue if is_dialogue else font_narration, font_size)
    cell = int(font_size * 1.15)                    # ô vuông cho mỗi ký tự (đơn giản hoá, xem docstring)
    n_cols = len(cols)
    n_rows = max((len(c) for c in cols), default=1)
    pad = int(font_size * 0.6)
    box_w = n_cols * cell + pad * 2
    box_h = n_rows * cell + pad * 2

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    third = W / 3
    margin = int(W * 0.02)
    if side == "left":
        box_x1 = min(third - margin, W - box_w - margin)
        box_x0 = box_x1 - box_w
    else:
        box_x0 = max(2 * third + margin, margin)
        box_x1 = box_x0 + box_w
    box_y0 = (H - box_h) / 2
    box_y1 = box_y0 + box_h

    if is_dialogue:
        d.ellipse([box_x0, box_y0, box_x1, box_y1], fill=(255, 255, 255, 235),
                  outline=(30, 30, 30, 255), width=3)
    else:
        r = int(font_size * 0.25)
        d.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=r,
                            fill=(255, 255, 255, 235), outline=(30, 30, 30, 255), width=3)

    # cột 1 = chữ ĐẦU câu → đặt bên PHẢI trong hộp (tategaki: cột mới mọc sang TRÁI)
    for ci, col in enumerate(cols):
        cx = box_x1 - pad - cell * ci - cell / 2
        for ri, ch in enumerate(col):
            cy = box_y0 + pad + cell * ri + cell / 2
            if ch == CHOONPU:
                tmp = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
                td = ImageDraw.Draw(tmp)
                bb = td.textbbox((0, 0), ch, font=font)
                tw, th = bb[2] - bb[0], bb[3] - bb[1]
                td.text((cell / 2 - tw / 2 - bb[0], cell / 2 - th / 2 - bb[1]), ch,
                        font=font, fill=(20, 20, 20, 255))
                tmp = tmp.rotate(90, expand=False)
                img.alpha_composite(tmp, (int(cx - cell / 2), int(cy - cell / 2)))
                continue
            bb = d.textbbox((0, 0), ch, font=font)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), ch, font=font, fill=(20, 20, 20, 255))
    return img


# ---------------------------------------------------------------- build track (concat variable-duration)
def build_track(srt_path, out_path, W, H, fps=30, side="left", font_narration="Yu Mincho",
                font_dialogue="Yu Gothic", font_size=42, max_chars_per_col=14, max_cols=2,
                total_dur=None, tmp_dir=None):
    cues = merge_short(parse_cues(srt_path))
    if not cues:
        raise SystemExit(f"✗ tate_text: {srt_path} không đọc được cue nào.")
    if total_dur and cues[-1]["end"] < total_dur:
        cues[-1]["end"] = total_dur          # kéo cue cuối phủ hết audio, tránh hụt track
    tmp = Path(tmp_dir) if tmp_dir else Path(tempfile.mkdtemp(prefix="tate_"))
    tmp.mkdir(parents=True, exist_ok=True)
    clip_paths = []
    for i, c in enumerate(cues):
        dur = max(0.15, c["end"] - c["start"])
        img = render_cue_image(c["text"], W, H, side, font_narration, font_dialogue, font_size,
                               max_chars_per_col, max_cols)
        png = tmp / f"tt_{i:05d}.png"
        img.save(png)
        clip = tmp / f"tt_{i:05d}.mov"
        subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-i", str(png), "-t", f"{dur:.3f}",
                        "-pix_fmt", "yuva420p", "-c:v", "qtrle", "-r", str(fps), str(clip)],
                       check=True)
        clip_paths.append(clip)
    listf = tmp / "tt_list.txt"
    listf.write_text("\n".join(f"file '{p.resolve().as_posix()}'" for p in clip_paths), encoding="utf-8")
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listf),
                    "-c", "copy", str(out)], check=True)
    print(f"[tate_text] {len(cues)} cue → {out} ({sum(c['end']-c['start'] for c in cues):.1f}s)")
    return out, cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--side", default="left", choices=["left", "right"])
    ap.add_argument("--font-narration", default="Yu Mincho")
    ap.add_argument("--font-dialogue", default="Yu Gothic")
    ap.add_argument("--size", type=int, default=42)
    ap.add_argument("--max-chars-per-col", type=int, default=14)
    ap.add_argument("--max-cols", type=int, default=2)
    ap.add_argument("--total-dur", type=float, default=0)
    a = ap.parse_args()
    build_track(a.srt, a.out, a.w, a.h, a.fps, a.side, a.font_narration, a.font_dialogue,
               a.size, a.max_chars_per_col, a.max_cols, total_dur=a.total_dur or None)


if __name__ == "__main__":
    main()
