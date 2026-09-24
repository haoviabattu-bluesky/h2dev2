# -*- coding: utf-8 -*-
"""Giữ chốt Lane L (2026-09-24): đa giọng qua ai33 (không VOICEVOX), bóng thoại không đuôi, profiles.da_giong."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bong_thoai      # noqa: E402
import profiles        # noqa: E402
import tts_voicevox    # noqa: E402

KB = "その日、人事部の空気は凍りついていた。\n「えっ、どういうことですか？」\n「来年の新卒採用は、半分に減らす」"


def _mp3_tone(sec):
    import imageio_ffmpeg
    return subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "lavfi", "-i",
                           f"sine=frequency=300:duration={sec}", "-f", "mp3", "pipe:1"],
                          capture_output=True, check=True).stdout


def test_da_giong_theo_provider():
    assert profiles.da_giong({"voice": {"provider": "voicevox"}})
    assert profiles.da_giong({"voice": {"provider": "ai33"}})
    assert not profiles.da_giong({"voice": {"id": "elevenlabs_x"}})


@pytest.fixture
def tap(tmp_path):
    (tmp_path / "script.txt").write_text(KB, encoding="utf-8")
    (tmp_path / "vai.txt").write_text("1|ke|その日、人事部の空気は凍りついていた。\n2|sakura|「えっ、どういうことですか？」\n"
                                      "3|bucho|「来年の新卒採用は、半分に減らす」\n", encoding="utf-8")
    (tmp_path / "characters.json").write_text(json.dumps({"characters": [
        {"id": "sakura", "ref": True, "voice": {"voice_id": "minimax_S"}},
        {"id": "bucho", "ref": True, "voice": {"voice_id": "minimax_B"}}]}), encoding="utf-8")
    return tmp_path


PROF = {"id": "t", "voice": {"provider": "ai33", "narrator": {"voice_id": "minimax_N"}, "speed": 1.0,
                             "pause_sentence_ms": 300, "pause_para_ms": 600}}


def test_ai33_moi_cau_dung_giong_cua_vai(tap, monkeypatch):
    import openspeaker_tts
    import tts
    goi = []

    def fake(text, voice_id, speed=1.0, with_transcript=False, file_name=""):
        goi.append((text, voice_id))
        return _mp3_tone(max(1.0, len(text) / 6)), None
    monkeypatch.setattr(openspeaker_tts, "synthesize", fake)
    monkeypatch.setattr(tts, "kiem_credit", lambda osp, text: None)
    monkeypatch.setattr(tts, "chuan_muc", lambda p: None)
    tts_voicevox.chay(tap / "script.txt", tap / "voice.mp3", PROF)
    assert sorted(v for _, v in goi) == ["minimax_B", "minimax_N", "minimax_S"]
    assert dict(goi)["えっ、どういうことですか？"] == "minimax_S"          # thoại gửi TTS không kèm 「」
    roles = json.loads((tap / "voice_roles.json").read_text(encoding="utf-8"))
    assert [r["vai"] for r in roles] == ["ke", "sakura", "bucho"]
    assert not (tap / "credits_giong.txt").exists()                   # ai33 không có khối VOICEVOX:


def test_ai33_cau_bi_nuot_thi_dung(tap, monkeypatch):
    import openspeaker_tts
    import tts
    monkeypatch.setattr(openspeaker_tts, "synthesize", lambda *a, **k: (_mp3_tone(0.2), None))
    monkeypatch.setattr(tts, "kiem_credit", lambda osp, text: None)
    with pytest.raises(SystemExit):
        tts_voicevox.chay(tap / "script.txt", tap / "voice.mp3", PROF)


def test_bong_khong_duoi_khong_ve_ra_ngoai_hop():
    W, H = 640, 360
    a = bong_thoai.render_cue("「どういうことですか？」", False, W, H, [], mieng=(100, 300), size=24, duoi=False)
    b = bong_thoai.render_cue("「どういうことですか？」", False, W, H, [], mieng=(100, 300), size=24, duoi=True)
    # có đuôi thì phủ thêm điểm ảnh ngoài hộp bóng; không đuôi thì ít hơn hẳn
    assert sum(1 for p in a.getdata() if p[3]) < sum(1 for p in b.getdata() if p[3])
