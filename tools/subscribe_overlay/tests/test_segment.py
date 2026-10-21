# -*- coding: utf-8 -*-
"""Test mode "segment": chỉ encode lại GOP có nút, phần còn lại phải giữ NGUYÊN TỪNG KHUNG (md5).

Chạy:  py -3.12 -m pytest tests/test_segment.py -q
"""
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import so_ffmpeg as ff  # noqa: E402
import so_segment  # noqa: E402
import subscribe_overlay as so  # noqa: E402

FF = ff.ffmpeg_exe()


@pytest.fixture(scope="module")
def cache(tmp_path_factory):
    return str(tmp_path_factory.mktemp("seg_cache"))


@pytest.fixture(scope="module")
def src(tmp_path_factory):
    """Giống tập h2dev: h264 yuvj420p (pc), keyframe THƯA (-g 250 ≈ 8,3s ở 30fps)."""
    p = tmp_path_factory.mktemp("seg_src") / "in.mp4"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=1280x720:r=30:d=40",
                    "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=40",
                    "-c:v", "libx264", "-preset", "ultrafast", "-g", "250", "-sc_threshold", "0",
                    "-pix_fmt", "yuvj420p", "-color_range", "pc", "-c:a", "aac", "-shortest", str(p)], check=True)
    return p


def _md5s(path) -> list[tuple[float, str]]:
    p = subprocess.run([FF, "-loglevel", "error", "-i", str(path), "-map", "0:v", "-f", "framemd5", "-"],
                       capture_output=True, check=True)
    rows, tb = [], None
    for ln in p.stdout.decode().splitlines():
        if ln.startswith("#tb"):
            num, den = ln.split(":")[1].strip().split("/")
            tb = int(num) / int(den)
        if ln.startswith("#"):
            continue
        c = [x.strip() for x in ln.split(",")]
        rows.append((int(c[2]), c[5]))
    return [(pts * tb, h) for pts, h in rows]


def _pixel(path, t, xy, tmp):
    out = tmp / f"f_{Path(path).stem}_{t}.png"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", str(out)], check=True)
    return Image.open(out).convert("RGB").getpixel(xy)


def test_plan_windows_gop_va_gop_chung():
    kf = [0.0, 8.33, 16.67, 25.0, 33.33]
    assert so_segment.plan_windows(kf, [10.0], 6.0) == [(8.33, 16.67, [10.0])]
    assert so_segment.plan_windows(kf, [10.0, 13.0], 2.0) == [(8.33, 16.67, [10.0, 13.0])]  # cùng GOP → gộp
    assert so_segment.plan_windows(kf, [34.0], 6.0) == [(33.33, None, [34.0])]              # tới hết video


def test_segment_giu_nguyen_khung_ngoai_doan(tmp_path, src, cache):
    out = tmp_path / "out.mp4"
    r = so.apply_to_video(src, out, overrides={"start_times": [10, -9], "min_gap": 5, "cache_dir": cache,
                                               "enable_sound": True})
    assert r["mode"] == "segment", r["warnings"]
    assert r["starts"] == [10.0, 31.0]
    assert r["reencoded_seconds"] < 25                         # không encode lại cả 40s
    assert r["output"]["pix_fmt"] == "yuvj420p" and r["output"]["color_range"] == "pc"
    assert abs(r["duration_delta"]) < 0.05
    a, b = _md5s(src), _md5s(out)
    assert len(a) == len(b) == 1200                            # số khung bằng nhau
    wins = [(w0, 40.0 if w1 is None else w1) for w0, w1 in r["windows"]]
    ngoai = [i for i, (t, _) in enumerate(a) if not any(w0 - 0.02 <= t < w1 - 0.02 for w0, w1 in wins)]
    assert len(ngoai) > 400
    lech = [i for i in ngoai if a[i][1] != b[i][1]]
    assert not lech, f"{len(lech)} khung ngoài đoạn bị đổi, vd khung {lech[:5]}"
    cx, cy, cw, ch = __import__("json").loads(Path(r["overlay"]).with_suffix(".json").read_text(encoding="utf-8"))["card_box"]
    px, py = r["x"] + cx + 8, r["y"] + cy + ch // 2
    for t, co in ((5.0, False), (13.0, True), (20.0, False), (34.0, True)):
        v = _pixel(out, t, (px, py), tmp_path)
        assert (min(v) > 235) == co, (t, v)                    # nút hiện ĐÚNG mốc


def test_segment_cat_lech_roi_ve_full(tmp_path, src, cache, monkeypatch):
    monkeypatch.setattr(so_segment, "CUT_BACKOFF", -0.5)       # giả lập bẫy làm tròn: cắt sang GOP sau
    out = tmp_path / "out.mp4"
    r = so.apply_to_video(src, out, overrides={"start_times": [10], "cache_dir": cache})
    assert r["mode"] == "full"
    assert any("segment hỏng" in w for w in r["warnings"])
    assert abs(r["duration_delta"]) < 0.05
