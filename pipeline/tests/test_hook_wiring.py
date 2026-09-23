# Test Task 8 (2026-09-23): _pass1_prompt(hook_locked=) + extract_beats Beat 0.
# Toàn bộ test OFFLINE — monkeypatch ai_steps._writer_chat, không gọi LLM thật.
import json
import pytest
import ai_steps

PROF = {"id": "x", "language": "ja", "voice": {"char_rate": 300.0}, "script": {}, "narrator": {}}


def test_pass1_prompt_co_khoi_hook():
    p = ai_steps._pass1_prompt(PROF, "KHUNG", 20, "", budget_block="2) ...", hook_locked="HOOK文。")
    assert "PHẦN MỞ ĐẦU ĐÃ KHOÁ" in p and "HOOK文。" in p
    assert p.index("PHẦN MỞ ĐẦU ĐÃ KHOÁ") < p.index("KHUNG SỰ KIỆN CẦN ĐI THEO")
    assert "PHẦN MỞ ĐẦU ĐÃ KHOÁ" not in ai_steps._pass1_prompt(PROF, "KHUNG", 20, "", budget_block="2)")


def test_extract_beats_beat0(monkeypatch):
    monkeypatch.setattr(ai_steps, "_writer_chat", lambda prof, ask, **k: type("R", (), {"text": "N01. a\nN02. b", "provider": "p", "model": "m", "elapsed": 0})())
    out = ai_steps.extract_beats(PROF, "transcript", hook_locked="HOOK文。")
    first, rest = out.split("\n", 1)
    assert json.loads(first)["beat0"]["locked"] is True
    assert rest.startswith("N00. [HOOK — ĐÃ KHOÁ] HOOK文。") and "N01. a" in rest
