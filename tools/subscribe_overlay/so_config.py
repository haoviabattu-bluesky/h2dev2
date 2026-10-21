# -*- coding: utf-8 -*-
"""Cấu hình nút đăng ký: mặc định + đọc subscribe_config.json + ghi đè CLI + khoá cache.

Mọi mốc thời gian animation nằm trong "timeline" (giây, tính từ lúc overlay bắt đầu hiện).
Khối này cố ý dùng CÙNG tên key với block `assemble.subscribe` sẽ thêm vào profile h2dev,
để sau này profile chỉ cần dán nguyên dict vào `load_config(overrides=...)`.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = HERE / "subscribe_config.json"

# Đổi số này mỗi khi sửa code vẽ → mọi cache cũ tự hết hiệu lực (khoá hash đổi).
RENDER_VERSION = 2  # v2 (2026-09-30): avatar kênh + chữ cảm ơn sau khi bấm chuông

# (nút đỏ, sau khi đăng ký, lời cảm ơn sau khi bấm chuông)
LANG_TEXTS = {
    "ja": ("チャンネル登録", "登録済み", "ありがとうございます"),
    "en": ("SUBSCRIBE", "SUBSCRIBED", "THANK YOU!"),
    "vi": ("ĐĂNG KÝ", "ĐÃ ĐĂNG KÝ", "CẢM ƠN BẠN!"),
}

POSITIONS = ("bottom_center", "bottom_left", "bottom_right", "center")

DEFAULTS: dict = {
    "enabled": True,
    "start_time": 12.0,          # giây trong video; số âm = tính từ CUỐI video (-10 = 10s trước khi hết)
    "start_times": None,         # nhiều lần hiện, vd [180, -120]; có thì THẮNG start_time
    "min_gap": 30.0,             # 2 lần hiện phải cách nhau ≥ duration + min_gap giây
    "sub_click_style": "1_click_that",
    "bell_style": "1_ting",      # chuông riêng từng lane — xem so_bells.BELLS
    "duration": 6.0,
    "position": "bottom_center",
    "overlay_width_ratio": 0.38,           # bề rộng khung nút / bề rộng video (video ngang) — có avatar nên rộng hơn
    "overlay_width_ratio_vertical": 0.80,  # video dọc 9:16 hẹp → cần tỉ lệ lớn hơn
    "bottom_margin_ratio": 0.035,          # anh chốt 2026-09-30: gần mép dưới nhưng không sát (1080p ≈ 38px)
    "bottom_margin_ratio_vertical": 0.24,  # Shorts: tránh vùng tiêu đề/nút YouTube phủ ở đáy
    "side_margin_ratio": 0.05,
    "has_subtitles": False,       # True → đẩy nút lên trên vùng phụ đề
    "subtitle_safe_ratio": 0.30,  # vùng đáy dành cho phụ đề (đo kênh kenko: phụ đề cháy chiếm y 810-890/1080)
    "language": "ja",
    "subscribe_text": None,       # None → lấy theo language
    "subscribed_text": None,
    "thanks_text": None,          # chữ thay 登録済み sau khi bấm chuông; "" = tắt bước cảm ơn
    "avatar_path": "assets/avatar_mau.png",  # avatar kênh bên trái logo; tương đối = tính từ thư mục tool
    "enable_avatar": True,
    "enable_cursor": True,
    "enable_bell": True,
    "enable_card": True,          # thẻ nền trắng bo góc phía sau (dễ đọc trên nền video rối)
    "enable_sound": False,
    "sound_volume": 0.6,
    "sound_gains": {"pop": 0.35, "click": 0.55, "bell": 0.8},  # nhân thêm theo từng âm
    "fade_in": 0.3,
    "fade_out": 0.5,
    "timeline": {
        "cursor_in": 1.3,      # con trỏ bắt đầu hiện
        "cursor_move1": 1.5,   # bắt đầu di tới nút
        "click1": 1.8,         # click nút đăng ký
        "press": 0.25,         # thời gian nút lún 100% → press_scale → 100%
        "switch": 2.1,         # đổi sang 登録済み
        "cursor_move2": 3.0,   # di sang chuông
        "click2": 3.3,         # click chuông
        "ring": 0.9,           # thời gian chuông rung
        "cursor_out": 3.9,     # con trỏ rời đi + mờ dần
        "thanks": 4.1,         # đổi 登録済み → ありがとうございます (sau tiếng "ting")
    },
    "press_scale": 0.92,
    "bell_angles": [0, -10, 10, -8, 8, -4, 4, 0],
    "style": {
        "red": "#FF0000",
        "subscribe_text_color": "#FFFFFF",
        "subscribed_bg": "#ECECEC",
        "subscribed_text_color": "#3A3A3A",
        "thanks_text_color": "#E00000",
        "bell_color": "#3A3A3A",
        "card_bg": "#FFFFFF",
        "shadow_opacity": 0.22,
    },
    "font_path": None,            # None → find_font() tự dò
    "supersample": 4,             # vẽ ở 4x rồi LANCZOS xuống → chữ/viền sắc
    "fps": None,                  # None → theo video; --generate-overlay mặc định 30
    "overlay_format": "webm",     # webm (VP9 alpha) | mov (ProRes 4444) | png (chuỗi PNG RGBA)
    "cache_dir": None,            # None → env SUBSCRIBE_CACHE_DIR → <tool>/cache/subscribe
    "compose_mode": "segment",    # segment = chỉ encode lại GOP có nút (nhanh ~4x) | full = encode lại cả video
    "video_encoder": "auto",      # auto (dò NVENC thật) | libx264 | h264_nvenc — chỉ dùng cho mode full
    "video_crf": 18,
    "video_preset": "medium",
}

# Key ảnh hưởng tới HÌNH của overlay → đưa vào hash cache. Vị trí/start/âm/encoder KHÔNG ảnh hưởng.
_RENDER_KEYS = ("duration", "language", "subscribe_text", "subscribed_text", "thanks_text", "enable_avatar", "enable_cursor",
                "enable_bell", "enable_card", "fade_in", "fade_out", "timeline", "press_scale",
                "bell_angles", "style", "supersample", "overlay_format")


def _deep_merge(base: dict, extra: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        elif v is not None or k not in out:
            out[k] = v
    return out


def load_config(path: str | os.PathLike | None = None, overrides: dict | None = None) -> dict:
    cfg = copy.deepcopy(DEFAULTS)
    p = Path(path) if path else DEFAULT_CONFIG_PATH
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        cfg = _deep_merge(cfg, {k: v for k, v in data.items() if not k.startswith("_")})
    elif path:
        raise FileNotFoundError(f"Không thấy file config: {p}")
    if overrides and overrides.get("start_time") is not None and "start_times" not in overrides:
        overrides = {**overrides, "start_times": None}  # gọi kèm start_time đơn → bỏ danh sách trong file
    cfg = _deep_merge(cfg, overrides or {})
    if overrides and "start_times" in overrides and overrides["start_times"] is None:
        cfg["start_times"] = None
    lang = str(cfg["language"]).lower()
    if lang not in LANG_TEXTS and not (cfg.get("subscribe_text") and cfg.get("subscribed_text")):
        raise ValueError(f"language '{lang}' chưa hỗ trợ (có: {', '.join(LANG_TEXTS)}) — hoặc tự ghi subscribe_text/subscribed_text")
    cfg["language"] = lang
    sub, subd, thx = LANG_TEXTS.get(lang, (None, None, ""))
    cfg["subscribe_text"] = cfg.get("subscribe_text") or sub
    cfg["subscribed_text"] = cfg.get("subscribed_text") or subd
    if cfg.get("thanks_text") is None:
        cfg["thanks_text"] = thx
    cfg["avatar_file"] = str(resolve_avatar(cfg)) if cfg["enable_avatar"] else None
    validate(cfg)
    return cfg


def resolve_avatar(cfg: dict) -> Path | None:
    """Đường dẫn avatar kênh. Tương đối → thử thư mục tool rồi thư mục đang chạy. Khai mà thiếu file → lỗi."""
    raw = cfg.get("avatar_path")
    if not raw:
        return None
    p = Path(raw)
    for cand in ([p] if p.is_absolute() else [HERE / p, Path.cwd() / p]):
        if cand.is_file():
            return cand.resolve()
    raise FileNotFoundError(f"Không thấy avatar kênh: {raw} (ghi avatar_path đúng, hoặc enable_avatar=false)")


def validate(cfg: dict) -> None:
    tl, d = cfg["timeline"], float(cfg["duration"])
    order = ["cursor_in", "cursor_move1", "click1", "switch", "cursor_move2", "click2"]
    vals = [float(tl[k]) for k in order]
    if vals != sorted(vals):
        raise ValueError(f"timeline phải tăng dần theo thứ tự {order}: {vals}")
    if tl["click1"] + tl["press"] > tl["switch"] + 1e-6:
        raise ValueError("click1 + press phải ≤ switch (nút lún xong mới đổi chữ)")
    if tl["click2"] + tl["ring"] > d - cfg["fade_out"] + 1e-6:
        raise ValueError("chuông phải rung xong trước khi fade out (click2 + ring ≤ duration - fade_out)")
    if cfg["thanks_text"] and not (tl["click2"] < tl["thanks"] <= d - cfg["fade_out"] - 0.5):
        raise ValueError("thanks phải sau click2 và còn ≥0.5s để đọc trước khi fade out")
    if cfg["fade_in"] + cfg["fade_out"] >= d:
        raise ValueError("fade_in + fade_out phải nhỏ hơn duration")
    if cfg["position"] not in POSITIONS:
        raise ValueError(f"position phải là một trong {POSITIONS}")
    if cfg["overlay_format"] not in ("webm", "mov", "png"):
        raise ValueError("overlay_format phải là webm | mov | png")


def overlay_width_px(cfg: dict, vw: int, vh: int) -> int:
    ratio = cfg["overlay_width_ratio_vertical"] if vh > vw else cfg["overlay_width_ratio"]
    return int(round(vw * float(ratio) / 2)) * 2


def size_label(vw: int, vh: int) -> str:
    short = min(vw, vh)
    named = {720: "720p", 1080: "1080p", 1440: "1440p", 2160: "4k"}.get(short, f"{short}p")
    return f"vertical_{named}" if vh > vw else named


def cache_dir(cfg: dict) -> Path:
    d = cfg.get("cache_dir") or os.environ.get("SUBSCRIBE_CACHE_DIR") or (HERE / "cache" / "subscribe")
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    return p


def cache_key(cfg: dict, width_px: int, vertical: bool, fps: str, font_path: str) -> str:
    payload = {k: cfg[k] for k in _RENDER_KEYS}
    fp = Path(font_path)
    payload.update(v=RENDER_VERSION, width_px=width_px, vertical=vertical, fps=fps,
                   font=fp.name, font_size=fp.stat().st_size if fp.exists() else 0)
    if cfg.get("avatar_file"):  # băm NỘI DUNG ảnh: thay ảnh cùng tên vẫn render lại
        payload["avatar_sha"] = hashlib.sha256(Path(cfg["avatar_file"]).read_bytes()).hexdigest()
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
