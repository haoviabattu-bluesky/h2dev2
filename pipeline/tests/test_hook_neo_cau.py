# -*- coding: utf-8 -*-
"""Giữ chốt ghep_hook_noi_truoc.neo_lai_theo_cau (Lane L 2026-09-25): máy 1 ghi mốc hook theo SỐ CÂU, máy 2 tính lại
giây từ voice_roles.json của giọng thân (ai33 không tất định) + cắt hook_voice.* từ giọng thân."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ghep_hook_noi_truoc as g   # noqa: E402

ROLES = [{"i": 1, "start": 0.0, "end": 1.5, "vai": "a", "text": "一"},
         {"i": 2, "start": 2.0, "end": 4.0, "vai": "ke", "text": "二"},
         {"i": 3, "start": 4.4, "end": 6.0, "vai": "ke", "text": "三"},
         {"i": 4, "start": 6.6, "end": 9.0, "vai": "ke", "text": "四"}]


@pytest.fixture
def tap(tmp_path):
    (tmp_path / "hook").mkdir()
    (tmp_path / "voice_roles.json").write_text(json.dumps(ROLES), encoding="utf-8")
    subprocess.run([g.FF, "-y", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=300:duration=10",
                    str(tmp_path / "voice.mp3")], check=True)
    (tmp_path / "voice.srt").write_text("".join(f"{r['i']}\n{g._tc(r['start'])} --> {g._tc(r['end'])}\n{r['text']}\n\n"
                                                for r in ROLES), encoding="utf-8")
    return tmp_path


def _tl(tap, shots, sfx=()):
    (tap / "hook" / "hook_timeline.json").write_text(json.dumps({"shots": shots, "sfx": list(sfx)}), encoding="utf-8")


def test_tinh_lai_moc_theo_cau(tap):
    _tl(tap, [{"n": 1, "cau": [1, 2], "clip": "clip/c1.mp4"}, {"n": 2, "cau": [3, 3], "clip": "clip/c2.mp4"}],
        [{"file": "sfx/x.mp3", "cau": 3, "lech": 0.1, "vol": 0.5}])
    assert g.neo_lai_theo_cau(tap)
    tl = json.loads((tap / "hook" / "hook_timeline.json").read_text(encoding="utf-8"))
    s = tl["shots"]
    assert s[0]["t0"] == 0.0 and s[0]["t1"] == 4.2          # giữa khoảng lặng câu 2 → 3
    assert s[1]["t0"] == 4.2 and s[1]["t1"] == 6.3          # giữa câu 3 → 4
    assert tl["sfx"][0]["t"] == 4.5 and tl["hook_voice_end_s"] == 6.3
    roles_h = json.loads((tap / "hook" / "hook_voice_roles.json").read_text(encoding="utf-8"))
    assert [r["i"] for r in roles_h] == [1, 2, 3]
    assert len(g._doc_cue(tap / "hook" / "hook_voice.srt")) == 3
    import re
    err = subprocess.run([g.FF, "-i", str(tap / "hook" / "hook_voice.mp3")], capture_output=True, text=True).stderr
    h, m, sec = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    assert abs(float(sec) - 6.3) < 0.1                       # cắt đúng T từ giọng thân


def test_timeline_giay_cu_khong_dung(tap):
    _tl(tap, [{"n": 1, "t0": 0.0, "t1": 3.0, "clip": "clip/c1.mp4"}])
    assert g.neo_lai_theo_cau(tap) is False
    assert not (tap / "hook" / "hook_voice.mp3").exists()


def test_cau_khong_noi_tiep_thi_dung(tap):
    _tl(tap, [{"n": 1, "cau": [1, 1], "clip": "a"}, {"n": 2, "cau": [3, 3], "clip": "b"}])
    with pytest.raises(SystemExit):
        g.neo_lai_theo_cau(tap)
