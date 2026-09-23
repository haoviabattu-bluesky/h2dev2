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


# Test Task 9 (2026-09-23): wire H1-H4 vào lean_script.py — do_tat_dinh() kiểm bắt-đầu-bằng-hook + kể-lại-hook,
# PRESERVE khoá đoạn mở đầu. Test OFFLINE: monkeypatch mọi thứ chạm LLM/mạng.
def test_do_tat_dinh_hook(monkeypatch):
    import lean_script as L, ai_steps
    monkeypatch.setattr(ai_steps, "check", lambda prof, text, minutes=None, tol=0.12: ([], {"chars": 100, "minutes": 1, "comma_per_sentence": 1, "chars_per_breath": 8, "dialogue_ratio": 0.1, "markers": []}))
    monkeypatch.setattr(ai_steps, "_go_cat_neu_ja", lambda prof, t: t)
    import profiles
    monkeypatch.setattr(profiles, "target_chars", lambda prof, minutes=None, speed=None: 100)
    hook = "「三年前に引っ越しました」隣人は言った。"
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {"gate": {}}}
    _, m, vf, vl, warn = L.do_tat_dinh(prof, "晩秋の風。\n\n" + hook, "", "", 1, hook=hook)
    assert any(v.startswith("HOOK:") for v in vl)
    _, m, vf, vl, warn = L.do_tat_dinh(prof, hook + "\n\n" + hook + "隣人はそう言った。", "", "", 1, hook=hook)
    assert not any(v.startswith("HOOK:") for v in vl) and any("kể lại hook" in w for w in warn)


def test_preserve_co_hook():
    import lean_script as L
    assert "hook" in L.PRESERVE.lower()


# Test Task 10 (2026-09-23): mo_dau hết ĐẠT giả (warn_no_marker) + qc_final.kiem_hook + qc_hoso.kiem_hook_ho_so.
# Toàn bộ test OFFLINE — không mạng, không LLM.
def test_mo_dau_warn_no_marker():
    import qc_script as Q
    assert Q.mo_dau("không marker", {}) == []
    r = Q.mo_dau("không marker", {}, warn_no_marker=True)
    assert r and r[0]["kind"] == "mo_dau_khong_do"


def test_qc_final_kiem_hook(tmp_path):
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    (tmp_path / "script.txt").write_text("khác。", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert any("hook_lock" in x["msg"] for x in ra)
    HS.khoa(tmp_path, "hook。")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert any("không bắt đầu" in x["msg"] for x in ra)
    (tmp_path / "script.txt").write_text("hook。thân。", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert ra == []


def test_qc_hoso_kiem_hook(tmp_path):
    import qc_hoso as H
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {}}
    kq = []
    H.kiem_hook_ho_so(kq, "TIÊU ĐỀ\n① a\n", prof)
    assert any(x["ma"] == "hook_thieu" for x in kq)
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK 30 GIÂY ĐẦU:\nそれは不思議だった。\n\nKHUNG N CHƯƠNG:", prof)
    assert any(x["ma"] == "hook_noi_suong" for x in kq)
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK 30 GIÂY ĐẦU:\n1978年10月21日、セスナが消えた。\n\nKHUNG N CHƯƠNG:", prof)
    assert kq == []
