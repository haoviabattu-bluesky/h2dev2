# -*- coding: utf-8 -*-
"""Giữ chốt sfx_than.py (Lane L 2026-09-24): trộn hiệu ứng âm thanh thân video — video giữ nguyên, độ dài giữ nguyên,
thiếu kế hoạch/thiếu file tiếng thì DỪNG; tách thoại dài thành nhiều bóng (bong_thoai.tach_loi_ke ca_thoai)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bong_thoai   # noqa: E402
import sfx_than     # noqa: E402

import imageio_ffmpeg  # noqa: E402
FF = imageio_ffmpeg.get_ffmpeg_exe()


def _dur(p):
    err = subprocess.run([FF, "-i", str(p)], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


@pytest.fixture
def tap(tmp_path):
    subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=gray:s=320x180:d=4", "-f", "lavfi", "-i",
                    "sine=frequency=200:duration=4", "-shortest", "-c:v", "libx264", "-c:a", "aac",
                    str(tmp_path / "final.mp4")], check=True)
    (tmp_path / "_sfx").mkdir()
    subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=900:duration=0.5",
                    str(tmp_path / "_sfx" / "ding.mp3")], check=True)
    (tmp_path / "voice_roles.json").write_text(json.dumps([{"i": 1, "start": 0.0, "end": 1.0}, {"i": 2, "start": 2.0,
                                                                                                "end": 3.0}]))
    return tmp_path


def _prof(tmp):
    return {"id": "t", "slug_dir": str(tmp), "assemble": {"sfx": {"enabled": True, "vol": 0.3, "bank": {"ding": "x"}}}}


def test_tron_giu_do_dai(tap):
    (tap / "sfx_plan.txt").write_text("2|ding|câu hai\n", encoding="utf-8")
    d0 = _dur(tap / "final.mp4")
    sfx_than.tron(_prof(tap), tap)
    assert abs(_dur(tap / "final.mp4") - d0) < 0.1


def test_thieu_ke_hoach_thi_dung(tap):
    with pytest.raises(SystemExit):
        sfx_than.tron(_prof(tap), tap)


def test_thieu_file_tieng_thi_dung(tap):
    (tap / "sfx_plan.txt").write_text("1|khong_co|x\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        sfx_than.tron(_prof(tap), tap)


def test_tach_thoai_dai_thanh_nhieu_bong():
    c = {"vai": "mori", "start": 0.0, "end": 12.0,
         "text": "「さくら、正直に言う。会社は、佐伯が一人で抱えている管理の仕事を、分ける相手が欲しかった。課長代理は、そのための椅子だ。」"}
    assert len(bong_thoai.tach_loi_ke(c, 30)) == 1                       # mặc định: thoại không tách
    parts = bong_thoai.tach_loi_ke(c, 30, ca_thoai=True)
    assert len(parts) >= 2 and all("「" not in p["text"] for p in parts)
    assert parts[0]["start"] == 0.0 and abs(parts[-1]["end"] - 12.0) < 1e-6
