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


# Patch review Task 9 (2026-09-23), Minor V4: nhánh hook="" (tập cũ / lane chưa bật hook) PHẢI hành xử y hệt
# luồng trước khi có tính năng hook — không sinh việc "HOOK:" nào, không có cảnh báo hook trong `warn` (sau V3
# đã chuyển sang print thay vì warn.append), các giá trị trả về khác chạy trót lọt bình thường.
def test_do_tat_dinh_khong_hook(monkeypatch):
    import lean_script as L, ai_steps
    monkeypatch.setattr(ai_steps, "check", lambda prof, text, minutes=None, tol=0.12: ([], {"chars": 100, "minutes": 1, "comma_per_sentence": 1, "chars_per_breath": 8, "dialogue_ratio": 0.1, "markers": []}))
    monkeypatch.setattr(ai_steps, "_go_cat_neu_ja", lambda prof, t: t)
    import profiles
    monkeypatch.setattr(profiles, "target_chars", lambda prof, minutes=None, speed=None: 100)
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {"gate": {}}}
    text, m, vf, vl, warn = L.do_tat_dinh(prof, "晩秋の風。隣人はそう言った。", "", "", 1, hook="")
    assert not any(v.startswith("HOOK: ") for v in vl)
    # sau V3: cảnh báo "chưa có hook đã khoá" chuyển sang print(), KHÔNG còn nằm trong warn[] (ghi vào do.json/
    # ESCALATION_REPORT) — không assert bằng substring "hook" chung chung vì mo_dau_khong_do (Task 10, không
    # liên quan V3) hợp lệ nhắc tới hook_stage trong nội dung của nó.
    assert not any("chưa có hook đã khoá" in w for w in warn)
    assert isinstance(text, str) and text
    assert isinstance(m, dict) and "chars" in m


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


# ---------------------------------------------------------------------------
# Vá review dọn hook (6 điểm Minor, 2026-09-23).
# ---------------------------------------------------------------------------

def test_writer_chat_khong_claude_p_loc_max_chars(monkeypatch):
    """V4: profile KHÔNG khai script.engine="claude_p" mà vẫn gọi _writer_chat kèm max_chars
    (đúng như hook_stage.viet_candidates/hook_storyboard.sinh đang làm) không được TypeError —
    llm_client.chat() không có tham số này, _writer_chat phải tự lọc bỏ trước khi gọi."""
    captured = {}

    def fake_chat(prompt, **kwargs):
        captured.update(kwargs)
        return type("R", (), {"text": "ok"})()
    monkeypatch.setattr(ai_steps, "chat", fake_chat)
    prof = {"id": "x", "script": {}}  # không khai engine → rơi vào nhánh chat() thường
    r = ai_steps._writer_chat(prof, "prompt", task="short", max_chars=500, min_chars=10)
    assert r.text == "ok"
    assert "max_chars" not in captured
    assert captured.get("min_chars") == 10


def test_qc_final_kiem_hook_lock_hong_khong_nem(tmp_path):
    """V1: hook_lock.json hỏng → qc_final.kiem_hook không ném, báo lỗi 'thiếu hook' như chưa khoá."""
    import qc_final as F
    (tmp_path / "hook").mkdir()
    (tmp_path / "hook" / "hook_lock.json").write_text("{broken", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert any("hook_lock" in x["msg"] for x in ra)


def test_qc_final_kiem_hook_title_mat_sau_khoa(tmp_path):
    """V5: lúc khoá CÓ title.txt, sau đó title.txt bị xoá (t rỗng) → phải ra lỗi 'title.txt đã
    mất', không được để phép kiểm title-drift biến mất im lặng."""
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    (tmp_path / "script.txt").write_text("hook。thân。", encoding="utf-8")
    HS.khoa(tmp_path, "hook。")
    (tmp_path / "title.txt").unlink()
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert any("title.txt đã mất" in x["msg"] for x in ra)
