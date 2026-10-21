# -*- coding: utf-8 -*-
"""Test nút đăng ký: font JP, vị trí click, không crop, alpha thật, ghép 3 độ phân giải, cache.

Chạy:  py -3.12 -m pytest tests -q      (≈ 2-3 phút: render thật 3 overlay vào cache tạm)
"""
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import so_config  # noqa: E402
import so_compose  # noqa: E402
import so_ffmpeg as ff  # noqa: E402
import so_fonts  # noqa: E402
import so_layout as ly  # noqa: E402
import subscribe_overlay as so  # noqa: E402

FF = ff.ffmpeg_exe()


@pytest.fixture(scope="session")
def cache(tmp_path_factory):
    return str(tmp_path_factory.mktemp("sub_cache"))


def _video(path, w, h, dur=12, fps=30):
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"testsrc2=s={w}x{h}:r={fps}:d={dur}",
                    "-f", "lavfi", "-i", f"sine=frequency=440:sample_rate=48000:duration={dur}",
                    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                    str(path)], check=True)
    return path


def _frame(path, t, out):
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", str(out)], check=True)
    return Image.open(out).convert("RGB")


def test_font_ja_that_su_co_glyph():
    p, _ = so_fonts.find_font(["チャンネル登録", "登録済み"])
    assert so_fonts.covers(p, "チャンネル登録済み")


def test_con_tro_click_dung_nut_va_chuong():
    cfg = so_config.load_config()
    fp, idx = so_fonts.find_font([cfg["subscribe_text"], cfg["subscribed_text"]])
    L = ly.build_layout(fp, [cfg["subscribe_text"], cfg["subscribed_text"]], 576, 1, True, idx)
    tl = cfg["timeline"]
    (x1, y1), _, _ = ly.state(tl["click1"], cfg, L)["cursor"]
    assert L.pill_x < x1 < L.pill_x + L.pill_full and abs(y1 - L.cy) < ly.PILL_H / 2
    (x2, y2), _, _ = ly.state(tl["click2"], cfg, L)["cursor"]
    bx, by = L.bell_c
    assert (x2 - bx) ** 2 + (y2 - by) ** 2 < (ly.BELL_D / 2) ** 2
    assert ly.state(tl["click1"] + tl["press"] / 2, cfg, L)["pill_press"] < 0.93
    angles = [ly.state(tl["click2"] + k * 0.01, cfg, L)["bell_angle"] for k in range(0, 91)]
    assert min(angles) <= -9.9 and max(angles) >= 9.9


def test_chu_cam_on_sau_chuong_va_avatar():
    cfg = so_config.load_config()
    assert cfg["thanks_text"] == "ありがとうございます" and cfg["avatar_file"]
    texts = [cfg["subscribe_text"], cfg["subscribed_text"], cfg["thanks_text"]]
    fp, idx = so_fonts.find_font(texts)
    L = ly.build_layout(fp, texts, 730, 1, True, idx, avatar=True)
    th = cfg["timeline"]["thanks"]
    assert ly.state(cfg["timeline"]["click2"] + 0.1, cfg, L)["mix2"] == 0      # đang reo: chưa đổi chữ
    assert ly.state(th + 0.3, cfg, L)["mix2"] == 1                             # sau ting: đã là lời cảm ơn
    assert L.icon_x > L.avatar_c[0] + ly.AVATAR_D / 2                          # avatar nằm bên trái logo
    off = so_config.load_config(overrides={"thanks_text": "", "enable_avatar": False})
    assert off["thanks_text"] == "" and off["avatar_file"] is None


def test_timeline_sai_thu_tu_bi_chan():
    with pytest.raises(ValueError):
        so_config.load_config(overrides={"timeline": {"click1": 3.5}})


def test_vi_tri_1080p_bottom_center():
    cfg = so_config.load_config()
    meta = {"card_box": [33, 41, 576, 137]}
    x, y = so_compose.placement(cfg, meta, 1920, 1080)
    assert x + 33 == (1920 - 576) // 2
    gap = 1080 - (y + 41 + 137)  # khoảng từ đáy thẻ tới mép dưới video
    assert 25 <= gap <= 60, gap  # anh chốt: gần mép dưới nhưng không sát
    x2, y2 = so_compose.placement({**cfg, "has_subtitles": True}, meta, 1920, 1080)
    assert y2 < y  # có phụ đề → nút cao lên


def _peak_db(path, start, dur):
    p = subprocess.run([FF, "-hide_banner", "-ss", str(start), "-t", str(dur), "-i", str(path), "-vn",
                        "-af", "volumedetect", "-f", "null", "-"], capture_output=True)
    import re
    return float(re.search(r"max_volume: (-?[\d.]+|-inf) dB", p.stderr.decode()).group(1).replace("-inf", "-999"))


def test_am_thanh_giu_stereo_va_dung_thoi_diem(tmp_path, cache):
    src = tmp_path / "silent.mp4"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=gray:s=1280x720:r=30:d=12",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "12", "-c:v", "libx264",
                    "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", str(src)], check=True)
    out = tmp_path / "snd.mp4"
    r = so.apply_to_video(src, out, overrides={"start_time": 3.0, "cache_dir": cache, "enable_sound": True})
    assert r["sound"] and r["output"]["audio_layout"] == "stereo" and r["output"]["audio_rate"] == 44100
    assert abs(r["duration_delta"]) < 0.05
    assert _peak_db(out, 0.5, 2.0) < -60              # trước khi nút hiện: vẫn im lặng
    assert _peak_db(out, 3 + 3.3, 0.6) > -25          # click chuông + tiếng chuông


@pytest.mark.parametrize("w,h", [(1920, 1080), (1280, 720), (1080, 1920)])
def test_ghep_that(tmp_path, cache, w, h):
    src = _video(tmp_path / "in.mp4", w, h)
    out = tmp_path / "out.mp4"
    r = so.apply_to_video(src, out, overrides={"start_time": 3.0, "cache_dir": cache})
    i, o = r["input"], r["output"]
    assert (o["w"], o["h"], o["fps"]) == (i["w"], i["h"], i["fps"])
    assert abs(r["duration_delta"]) < 0.05 and o["has_audio"]
    meta = so_config.load_config()  # noqa: F841 — bảo đảm config hợp lệ
    ov_meta = __import__("json").loads(Path(r["overlay"]).with_suffix(".json").read_text(encoding="utf-8"))
    assert ov_meta["border_alpha_max"] == 0  # không hình nào chạm mép canvas
    cx, cy, cw, ch = ov_meta["card_box"]
    px, py = r["x"] + cx + 8, r["y"] + cy + ch // 2  # mép trái thẻ trắng
    before = _frame(src, 5.5, tmp_path / "a.png").getpixel((px, py))
    after = _frame(out, 5.5, tmp_path / "b.png").getpixel((px, py))
    assert min(after) > 235, f"thẻ trắng không hiện: {after}"
    assert before != after
    early_in = _frame(src, 1.0, tmp_path / "c.png").getpixel((px, py))
    early_out = _frame(out, 1.0, tmp_path / "d.png").getpixel((px, py))
    assert max(abs(a - b) for a, b in zip(early_in, early_out)) < 12  # trước start: video giữ nguyên
    # gọi lần 2 → phải lấy cache, không render lại
    r2 = so.apply_to_video(src, tmp_path / "out2.mp4", overrides={"start_time": 3.0, "cache_dir": cache})
    assert r2["overlay_cached"] is True


def test_moc_chen_2_lan():
    cfg = so_config.load_config()
    assert cfg["start_times"] == [180, -120]
    assert so_compose.resolve_starts(cfg, 1320)[0] == [180.0, 1200.0]   # tập 22 phút: phút 3 + còn 2 phút
    assert so_compose.resolve_starts(cfg, 330)[0] == [180.0]            # 2 mốc chồng nhau → giữ 1
    assert len(so_compose.resolve_starts(cfg, 60)[0]) == 1              # video ngắn vẫn có 1 lần
    assert so_config.load_config(overrides={"start_time": 3.0})["start_times"] is None


def test_ghep_2_lan_1_lan_encode(tmp_path, cache):
    src = _video(tmp_path / "in.mp4", 1280, 720, dur=40)
    out = tmp_path / "out.mp4"
    r = so.apply_to_video(src, out, overrides={"start_times": [5, -12], "min_gap": 5, "cache_dir": cache, "enable_sound": True})
    assert r["starts"] == [5.0, 28.0] and abs(r["duration_delta"]) < 0.05
    cx, cy, cw, ch = __import__("json").loads(Path(r["overlay"]).with_suffix(".json").read_text(encoding="utf-8"))["card_box"]
    px, py = r["x"] + cx + 8, r["y"] + cy + ch // 2
    for t, co in ((8.0, True), (18.0, False), (31.0, True)):
        v = _frame(out, t, tmp_path / f"f{t}.png").getpixel((px, py))
        assert (min(v) > 235) == co, (t, v)
