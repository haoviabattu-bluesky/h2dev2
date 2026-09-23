# Test Task 8 (2026-09-23): _pass1_prompt(hook_locked=) + extract_beats Beat 0.
# Toàn bộ test OFFLINE — monkeypatch ai_steps._writer_chat, không gọi LLM thật.
import json
from pathlib import Path

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


# 2026-09-23 (Việc 2, vá review cuối): qc_final.kiem_hook() giờ có ngã rẽ hook_stage.is_enabled(prof)
# — profile giả trong các test bên dưới PHẢI khai `script.hook.enabled: True` tường minh, khớp
# đúng thiết kế mới (mặc định TẮT theo từng kênh). Không đổi tên test/không đổi hành vi đang kiểm,
# chỉ thêm field còn thiếu để test tiếp tục đúng ý đồ gốc (mọi phép kiểm hook vẫn chạy khi ĐÃ bật).
PROF_HOOK_ON = {"id": "x", "script": {"hook": {"enabled": True}}}


def test_qc_final_kiem_hook(tmp_path):
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    (tmp_path / "script.txt").write_text("khác。", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    assert any("hook_lock" in x["msg"] for x in ra)
    HS.khoa(tmp_path, "hook。")
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    assert any("không bắt đầu" in x["msg"] for x in ra)
    (tmp_path / "script.txt").write_text("hook。thân。", encoding="utf-8")
    # 2026-09-23 (vá review cuối, Việc 1b): kiem_hook() nay CŨNG đòi final_with_hook.mp4 +
    # hook/render_info.json ở mọi chế độ (kể cả upstream) — tập "sạch hoàn toàn" phải có đủ 2 thứ
    # này mới còn ra == [] như trước bản vá.
    (tmp_path / "final_with_hook.mp4").write_bytes(b"x")
    (tmp_path / "hook" / "render_info.json").write_text("{}", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    assert ra == []


def test_qc_final_kiem_hook_tat_bo_qua_het(tmp_path):
    """Việc 2: profile KHÔNG khai script.hook.enabled (mặc định False) → kiem_hook bỏ qua HẲN,
    kể cả khi tập chưa hề có hook_lock.json (trước đây sẽ báo 'cao' — luật mới chỉ áp cho kênh đã bật)."""
    import qc_final as F
    ra = []
    F.kiem_hook(tmp_path, {"id": "x", "script": {}}, ra)
    assert ra == []


def test_qc_hoso_kiem_hook(tmp_path):
    import qc_hoso as H
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {}}
    # Việc 3a: hook_heading giờ là trường profile.research — test phải khai rs["hook_heading"]
    # tường minh để giữ đúng hành vi kiểm tra gốc (mặc định rỗng = không kiểm gì cả).
    rs = dict(H.MAC_DINH)
    rs["hook_heading"] = "HOOK 30 GIÂY ĐẦU"
    kq = []
    H.kiem_hook_ho_so(kq, "TIÊU ĐỀ\n① a\n", prof, rs)
    assert any(x["ma"] == "hook_thieu" for x in kq)
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK 30 GIÂY ĐẦU:\nそれは不思議だった。\n\nKHUNG N CHƯƠNG:", prof, rs)
    assert any(x["ma"] == "hook_noi_suong" for x in kq)
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK 30 GIÂY ĐẦU:\n1978年10月21日、セスナが消えた。\n\nKHUNG N CHƯƠNG:", prof, rs)
    assert kq == []


def test_qc_hoso_kiem_hook_khong_khai_thi_bo_qua(tmp_path):
    """Việc 3a: rs không khai hook_heading (mặc định "" trong MAC_DINH) → bỏ qua HẲN, kể cả hồ sơ
    hoàn toàn không có tiêu mục hook nào — không kênh nào bị ảnh hưởng nếu chưa khai."""
    import qc_hoso as H
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {}}
    kq = []
    H.kiem_hook_ho_so(kq, "TIÊU ĐỀ\n① a\n", prof, dict(H.MAC_DINH))
    assert kq == []


def test_qc_hoso_kiem_hook_tieu_muc_khac_va_noi_dung_cung_dong(tmp_path):
    """Việc 3: (a) tên tiêu mục tuỳ khai qua hook_heading (không ghim cứng 'HOOK 30 GIÂY ĐẦU'),
    (b) nội dung viết NGAY SAU dấu hai chấm trên CÙNG một dòng cũng phải nhận được, không chỉ khi
    xuống dòng."""
    import qc_hoso as H
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {}}
    rs = dict(H.MAC_DINH)
    rs["hook_heading"] = "HOOK — MÔ TẢ ẢNH CHÍNH"
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK — MÔ TẢ ẢNH CHÍNH: 1978年10月21日、セスナが消えた。\n\nKHUNG N CHƯƠNG:", prof, rs)
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
    """V1: hook_lock.json hỏng → qc_final.kiem_hook không ném, báo lỗi 'thiếu hook' như chưa khoá.
    (Việc 2: profile phải khai script.hook.enabled=True, xem PROF_HOOK_ON ở trên.)"""
    import qc_final as F
    (tmp_path / "hook").mkdir()
    (tmp_path / "hook" / "hook_lock.json").write_text("{broken", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    assert any("hook_lock" in x["msg"] for x in ra)


def test_qc_final_kiem_hook_title_mat_sau_khoa(tmp_path):
    """V5: lúc khoá CÓ title.txt, sau đó title.txt bị xoá (t rỗng) → phải ra lỗi 'title.txt đã
    mất', không được để phép kiểm title-drift biến mất im lặng.
    (Việc 2: profile phải khai script.hook.enabled=True, xem PROF_HOOK_ON ở trên.)"""
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    (tmp_path / "script.txt").write_text("hook。thân。", encoding="utf-8")
    HS.khoa(tmp_path, "hook。")
    (tmp_path / "title.txt").unlink()
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    assert any("title.txt đã mất" in x["msg"] for x in ra)


# ---------------------------------------------------------------------------
# Việc 2 (vá review cuối, 2026-09-23): công tắc script.hook.enabled theo từng kênh.
# ---------------------------------------------------------------------------

def test_is_enabled_mac_dinh_tat():
    import hook_stage as HS
    assert HS.is_enabled({"id": "x", "script": {}}) is False
    assert HS.is_enabled({"id": "x"}) is False   # không khai cả khối `script`
    assert HS.is_enabled({"id": "x", "script": {"hook": {"enabled": True}}}) is True


def test_lean_script_run_khong_goi_ensure_locked_khi_tat(monkeypatch, tmp_path):
    """Kênh KHÔNG khai script.hook.enabled → lean_script.run() không được đụng tới
    hook_stage.ensure_locked/doc_hook (chạy y hệt luồng trước khi có tính năng hook) — kiểm bằng
    monkeypatch ném AssertionError nếu ensure_locked bị gọi (KHÔNG kiểm bằng capsys: test này dừng
    ở S2 trước khi chạm đoạn code in cảnh báo trong do_tat_dinh — xem 2 test capsys ngay bên dưới,
    test_do_tat_dinh_khong_in_canh_bao_khi_hook_tat/test_do_tat_dinh_in_canh_bao_khi_hook_bat, mới
    là chỗ chứng minh hành vi in/không-in bằng capsys thật sự)."""
    import lean_script as L, hook_stage as HS
    import gate_common

    def _cam_ensure(*a, **k):
        raise AssertionError("KHÔNG được gọi ensure_locked khi script.hook.enabled=False")
    monkeypatch.setattr(HS, "ensure_locked", _cam_ensure)

    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {"gate": {}},
            "narrator": {}}

    class FakeJob:
        p = prof
        dir = tmp_path
        slug = "ep_test"
        minutes = 1
        state = {}
    job = FakeJob()

    monkeypatch.setattr(L, "s1q_ho_so", lambda d, prof, competitor, ctx: [])
    monkeypatch.setattr(L, "_title", lambda d: "T")
    monkeypatch.setattr(L, "viet", lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("test chỉ cần kiểm khối H1-H4, không cần S2 chạy thật")))
    # S2 sẽ ném ngay sau khối H1-H4 (không mock viet()) — đủ để chứng minh khối H1-H4 đã chạy xong
    # (không gọi ensure_locked) TRƯỚC KHI test dừng lại ở S2; bọc bằng pytest.raises.
    with pytest.raises(AssertionError, match="test chỉ cần kiểm khối H1-H4"):
        L.run(job, force=False)


# Vá review (2026-09-23): do_tat_dinh() chỉ được in "(warn) chưa có hook đã khoá" khi ĐỒNG THỜI
# (a) hook_stage.is_enabled(prof) True VÀ (b) hook="" (tập chưa chạy hook_stage). Trước đây dòng
# print chạy VÔ ĐIỀU KIỆN mỗi khi hook rỗng — vì công tắc mặc định TẮT cho cả 6 kênh đang sản xuất,
# dòng này in ra ở MỌI tập của MỌI kênh. Hai test dưới đây gọi THẲNG do_tat_dinh() (không đi vòng
# qua lean_script.run() — không cần thiết cho mục đích này) và kiểm capsys thật sự.
_CHECK_OK = lambda prof, text, minutes=None, tol=0.12: (
    [], {"chars": 100, "minutes": 1, "comma_per_sentence": 1, "chars_per_breath": 8,
         "dialogue_ratio": 0.1, "markers": []})


def test_do_tat_dinh_khong_in_canh_bao_khi_hook_tat(monkeypatch, capsys):
    """Công tắc script.hook.enabled TẮT (hoặc không khai — mặc định của 6 kênh đang sản xuất) +
    hook="" → do_tat_dinh() phải im lặng tuyệt đối, không in dòng 'chưa có hook đã khoá' (đúng cam
    kết 'hook="" hành xử y hệt trước khi có tính năng hook')."""
    import lean_script as L, ai_steps, profiles
    monkeypatch.setattr(ai_steps, "check", _CHECK_OK)
    monkeypatch.setattr(ai_steps, "_go_cat_neu_ja", lambda prof, t: t)
    monkeypatch.setattr(profiles, "target_chars", lambda prof, minutes=None, speed=None: 100)
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {"gate": {}}}  # không khai hook → is_enabled=False
    capsys.readouterr()  # xả sạch mọi output trước đó
    L.do_tat_dinh(prof, "晩秋の風。隣人はそう言った。", "", "", 1, hook="")
    out = capsys.readouterr().out
    assert "chưa có hook đã khoá" not in out


def test_do_tat_dinh_in_canh_bao_khi_hook_bat(monkeypatch, capsys):
    """Đối chứng: script.hook.enabled=True nhưng tập CHƯA có hook đã khoá (hook="") → PHẢI in
    dòng nhắc 'chưa có hook đã khoá' để người vận hành biết chạy `hook_stage.py --mode repair`."""
    import lean_script as L, ai_steps, profiles
    monkeypatch.setattr(ai_steps, "check", _CHECK_OK)
    monkeypatch.setattr(ai_steps, "_go_cat_neu_ja", lambda prof, t: t)
    monkeypatch.setattr(profiles, "target_chars", lambda prof, minutes=None, speed=None: 100)
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300},
            "script": {"gate": {}, "hook": {"enabled": True}}}
    capsys.readouterr()
    L.do_tat_dinh(prof, "晩秋の風。隣人はそう言った。", "", "", 1, hook="")
    out = capsys.readouterr().out
    assert "chưa có hook đã khoá" in out


def test_job_kiem_lock_bo_qua_hook_khi_tat(tmp_path, monkeypatch):
    """Việc 2: Job.kiem_lock() không được đụng hook_stage.kiem_stale khi kênh chưa khai
    script.hook.enabled — dùng self giả (duck-typing, kiem_lock chỉ đọc self.dir/self.p)."""
    import make_video, hook_stage, gate_common
    (tmp_path / "script.txt").write_text("nội dung。", encoding="utf-8")
    gate_common.ghi_lock(tmp_path, "PASS")

    def _cam(*a, **k):
        raise AssertionError("KHÔNG được gọi kiem_stale khi script.hook.enabled=False")
    monkeypatch.setattr(hook_stage, "kiem_stale", _cam)

    fake = type("FakeJob", (), {})()
    fake.dir = tmp_path
    fake.p = {"id": "x", "script": {}}
    make_video.Job.kiem_lock(fake, "B4")   # không được ném, không gọi kiem_stale


def test_job_kiem_lock_kiem_hook_khi_bat(tmp_path, monkeypatch):
    """Đối chứng: cùng thiết lập trên nhưng script.hook.enabled=True → kiem_stale PHẢI được gọi."""
    import make_video, hook_stage, gate_common
    (tmp_path / "script.txt").write_text("nội dung。", encoding="utf-8")
    gate_common.ghi_lock(tmp_path, "PASS")

    calls = {"n": 0}
    def _dem(d):
        calls["n"] += 1
        return False, []
    monkeypatch.setattr(hook_stage, "kiem_stale", _dem)

    fake = type("FakeJob", (), {})()
    fake.dir = tmp_path
    fake.p = {"id": "x", "script": {"hook": {"enabled": True}}}
    make_video.Job.kiem_lock(fake, "B4")
    assert calls["n"] == 1


def test_qc_final_kiem_hook_dung_prof_that_khong_chi_dict_id(tmp_path):
    """profile đầy đủ hơn {"id": "x"} — is_enabled đọc script.hook.enabled đúng vị trí lồng nhau."""
    import qc_final as F
    prof = {"id": "x", "language": "ja", "script": {"hook": {"enabled": False}}}
    ra = []
    F.kiem_hook(tmp_path, prof, ra)
    assert ra == []   # tắt → bỏ qua hẳn, dù thư mục rỗng hoàn toàn (không hook_lock.json)


# ---------------------------------------------------------------------------
# Vá review cuối (2026-09-23), Việc 1+2: nối hook_storyboard.sinh() vào Job.b5w_write_prompts()
# (khâu ghi tài sản của bước 1), thay vì chỉ chạy khi gọi tay hook_stage.py. Toàn bộ test dùng
# self giả (duck-typing, giống test_job_kiem_lock_* ở trên) — không dựng Job thật.
# ---------------------------------------------------------------------------

def test_b5w_write_prompts_goi_ca_ghi_prompt_va_hook_storyboard():
    """b5w_write_prompts() phải gọi CẢ 2 theo ĐÚNG THỨ TỰ: thân ghi tài sản (_b5w_ghi_prompt)
    TRƯỚC, rồi mới _sinh_hook_storyboard_neu_can() — vì hàm sau cần characters.json đã có (do thân
    ghi tài sản, hoặc do lớp 1 ghi trước đó, để lại trên đĩa)."""
    import make_video
    goi = []
    fake = type("FakeJob", (), {})()
    fake._b5w_ghi_prompt = lambda sheet="": goi.append(("ghi_prompt", sheet))
    fake._sinh_hook_storyboard_neu_can = lambda: goi.append(("hook_storyboard",))
    make_video.Job.b5w_write_prompts(fake, sheet="S")
    assert goi == [("ghi_prompt", "S"), ("hook_storyboard",)]


def test_sinh_hook_storyboard_neu_can_bo_qua_khi_tat(monkeypatch, tmp_path):
    """Kênh KHÔNG bật script.hook.enabled → không được gọi hook_storyboard.sinh() (giữ log sạch
    cho ~90% tập chưa dùng tính năng này)."""
    import make_video, hook_stage, hook_storyboard
    monkeypatch.setattr(hook_stage, "is_enabled", lambda p: False)
    monkeypatch.setattr(hook_stage, "doc_lock", lambda d: {"sha256": "x"})  # dù có lock cũng phải bỏ qua
    calls = []
    monkeypatch.setattr(hook_storyboard, "sinh", lambda *a, **k: calls.append(1))
    fake = type("FakeJob", (), {})()
    fake.dir = tmp_path; fake.p = {"id": "x", "script": {}}; fake.slug = "ep01"
    make_video.Job._sinh_hook_storyboard_neu_can(fake)
    assert calls == []


def test_sinh_hook_storyboard_neu_can_bo_qua_khi_chua_khoa_hook(monkeypatch, tmp_path):
    """Kênh bật hook nhưng tập CHƯA khoá hook (hook_stage.doc_lock trả None, vd tập cũ trước khi
    có tính năng) → không được gọi hook_storyboard.sinh() (sinh() sẽ tự raise nếu bị gọi thiếu
    hook, nhưng ở đây phải chặn TRƯỚC khi gọi, không dựa vào chính sinh() tự chặn)."""
    import make_video, hook_stage, hook_storyboard
    monkeypatch.setattr(hook_stage, "is_enabled", lambda p: True)
    monkeypatch.setattr(hook_stage, "doc_lock", lambda d: None)
    calls = []
    monkeypatch.setattr(hook_storyboard, "sinh", lambda *a, **k: calls.append(1))
    fake = type("FakeJob", (), {})()
    fake.dir = tmp_path; fake.p = {"id": "x", "script": {"hook": {"enabled": True}}}; fake.slug = "ep01"
    make_video.Job._sinh_hook_storyboard_neu_can(fake)
    assert calls == []


def test_sinh_hook_storyboard_neu_can_goi_dung_tham_so_khi_bat_va_da_khoa(monkeypatch):
    """Đối chứng: BẬT + ĐÃ khoá hook → phải gọi hook_storyboard.sinh(self.dir, self.p) đúng 1 lần."""
    import make_video, hook_stage, hook_storyboard
    monkeypatch.setattr(hook_stage, "is_enabled", lambda p: True)
    monkeypatch.setattr(hook_stage, "doc_lock", lambda d: {"sha256": "x"})
    calls = []
    monkeypatch.setattr(hook_storyboard, "sinh", lambda d, p: calls.append((d, p)))
    fake = type("FakeJob", (), {})()
    fake.dir = "GIA_DIR"; fake.p = {"id": "x", "script": {"hook": {"enabled": True}}}; fake.slug = "ep01"
    make_video.Job._sinh_hook_storyboard_neu_can(fake)
    assert calls == [("GIA_DIR", fake.p)]


def test_sinh_hook_storyboard_neu_can_loi_khong_lam_hong_b5w(monkeypatch, capsys):
    """Lỗi khi sinh storyboard (kể cả SystemExit — hook_storyboard.sinh dùng SystemExit cho lỗi
    nghiệp vụ) KHÔNG được văng ra ngoài, chỉ in cảnh báo kèm lệnh chạy tay để vá sau."""
    import make_video, hook_stage, hook_storyboard
    monkeypatch.setattr(hook_stage, "is_enabled", lambda p: True)
    monkeypatch.setattr(hook_stage, "doc_lock", lambda d: {"sha256": "x"})

    def _boom(d, p):
        raise SystemExit("✗ storyboard không hợp lệ sau 3 lần")
    monkeypatch.setattr(hook_storyboard, "sinh", _boom)
    fake = type("FakeJob", (), {})()
    fake.dir = "GIA_DIR"; fake.p = {"id": "lane-x", "script": {"hook": {"enabled": True}}}; fake.slug = "ep01"
    make_video.Job._sinh_hook_storyboard_neu_can(fake)   # không được ném ra ngoài
    out = capsys.readouterr().out
    assert "hook_storyboard.py --profile lane-x --slug ep01" in out


# ---------------------------------------------------------------------------
# Vá review cuối (2026-09-23), Việc vaB2: nối HOOK vào khâu giao hàng (giao_hang.py/qc_final.py)
# và khâu đóng gói máy 2 (dong_goi_may2.py/drive_handoff.py) — trước bản vá này 3 chỗ đều không
# biết `final_with_hook.mp4`/thư mục `hook/` tồn tại.
# ---------------------------------------------------------------------------

def test_chon_video_nguon_uu_tien_final_with_hook(tmp_path):
    """Việc 1a: tập có final_with_hook.mp4 ≥ 1 MB → giao_hang.py phải chọn ĐÚNG file đó làm nguồn chép
    (đích vẫn tên final.mp4 — không đổi quy ước tên file, chỉ đổi nguồn)."""
    import giao_hang as G
    (tmp_path / "final.mp4").write_bytes(b"khong hook")
    # File giả ≥ 1 MB (1.000.000 byte)
    (tmp_path / "final_with_hook.mp4").write_bytes(b"x" * 2_000_000)
    mp4, co_hook = G.chon_video_nguon(tmp_path)
    assert co_hook is True
    assert mp4 == tmp_path / "final_with_hook.mp4"
    assert mp4.stat().st_size == 2_000_000


def test_chon_video_nguon_khong_co_hook_giu_nguyen_final(tmp_path):
    """Đối chứng: tập KHÔNG có final_with_hook.mp4 → hành xử y hệt trước khi có tính năng hook."""
    import giao_hang as G
    (tmp_path / "final.mp4").write_bytes(b"khong hook")
    mp4, co_hook = G.chon_video_nguon(tmp_path)
    assert co_hook is False
    assert mp4 == tmp_path / "final.mp4"


def test_chon_video_nguon_hook_nho_hon_1mb_fallback(tmp_path, capsys):
    """Việc 1b: tập có final_with_hook.mp4 nhưng nhỏ hơn 1 MB (ghi dở) → chọn final.mp4 + in cảnh báo."""
    import giao_hang as G
    (tmp_path / "final.mp4").write_bytes(b"x" * 500_000)  # 500 KB
    (tmp_path / "final_with_hook.mp4").write_bytes(b"y" * 500_000)  # 500 KB, dưới ngưỡng

    capsys.readouterr()
    mp4, co_hook = G.chon_video_nguon(tmp_path)

    assert co_hook is False
    assert mp4 == tmp_path / "final.mp4"
    out = capsys.readouterr().out
    assert "⚠️" in out and "final_with_hook.mp4" in out and "500000" in out


def test_chon_video_nguon_hook_dung_1mb_chon_hook(tmp_path):
    """Biên giới: final_with_hook.mp4 ĐÚNG 1 MB → vẫn chọn nó (≥ 1 MB)."""
    import giao_hang as G
    (tmp_path / "final.mp4").write_bytes(b"x")
    (tmp_path / "final_with_hook.mp4").write_bytes(b"z" * 1_000_000)

    mp4, co_hook = G.chon_video_nguon(tmp_path)
    assert co_hook is True
    assert mp4 == tmp_path / "final_with_hook.mp4"


def test_qc_final_kiem_hook_thieu_final_with_hook(tmp_path):
    """Việc 1b: kênh bật + tập đã khoá hook (upstream, script.txt đã bắt đầu đúng bằng hook) nhưng
    THIẾU final_with_hook.mp4 → phải ra phát hiện mức 'cao' (không được lọt B10 với 0 phát hiện,
    đúng đúng sự cố có thật mô tả trong yêu cầu vá)."""
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    HS.khoa(tmp_path, "hook。")
    (tmp_path / "script.txt").write_text("hook。thân。", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    cao = [x for x in ra if x["sev"] == "cao"]
    assert cao and any("final_with_hook.mp4" in x["msg"] for x in cao)


def test_qc_final_kiem_hook_repair_cung_doi_final_with_hook(tmp_path):
    """Việc 1b: áp dụng cho CẢ hai chế độ — repair có đủ hook/hook_final.mp4 (phép kiểm cũ ĐẠT) mà
    vẫn thiếu final_with_hook.mp4 + hook/render_info.json thì vẫn phải bị bắt (trước bản vá chỉ
    nhánh upstream mới có 2 phép kiểm mới này)."""
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    HS.khoa(tmp_path, "hook。", mode="repair")
    (tmp_path / "hook" / "hook_final.mp4").write_bytes(b"x")
    ra = []
    F.kiem_hook(tmp_path, PROF_HOOK_ON, ra)
    cao = [x for x in ra if x["sev"] == "cao"]
    assert any("final_with_hook.mp4" in x["msg"] for x in cao)
    assert any("render_info.json" in x["msg"] for x in cao)


def test_qc_final_kiem_hook_tat_van_bo_qua_du_thieu_final_with_hook(tmp_path):
    """Đối chứng cho phép kiểm mới: kênh TẮT hook (script.hook.enabled vắng/False) → kiem_hook()
    vẫn phải im lặng tuyệt đối dù thư mục tập không có gì (đã có test_qc_final_kiem_hook_tat_bo_qua_het
    kiểm ý này ở mức tổng quát; test này khẳng định lại RÕ cho đúng câu chữ yêu cầu vá 'kênh tắt →
    không phát hiện gì')."""
    import qc_final as F
    ra = []
    F.kiem_hook(tmp_path, {"id": "x", "script": {}}, ra)
    assert ra == []


def _tap_co_hook_day_du(tap: Path) -> None:
    """Dựng 1 thư mục `hook/` đầy đủ file (giống bước 1 thật để lại) — dùng chung cho các test
    đóng gói máy 2 bên dưới."""
    hook = tap / "hook"
    (hook / "flow_prompts").mkdir(parents=True)
    (hook / "hook_locked.txt").write_text("hook。", encoding="utf-8")
    (hook / "hook_lock.json").write_text("{}", encoding="utf-8")
    (hook / "hook_storyboard.json").write_text("{}", encoding="utf-8")
    (hook / "grok_jobs.csv").write_text("shot,prompt\n1,a\n", encoding="utf-8")
    (hook / "flow_prompts" / "shot_01.txt").write_text("prompt 1", encoding="utf-8")
    (hook / "flow_prompts" / "shot_02.txt").write_text("prompt 2", encoding="utf-8")


def test_dong_goi_hook_gop_du_file_khi_tap_co_hook(tmp_path):
    """Việc 2: tập CÓ thư mục hook/ → dong_goi_may2._dong_goi_hook() phải copy đủ 4 file gốc +
    toàn bộ flow_prompts/ sang gói giao, và đối chiếu khớp kích thước (luật 'vận chuyển phải tự
    chứng minh')."""
    import dong_goi_may2 as D
    job_dir = tmp_path / "job"
    dst = tmp_path / "goi"
    job_dir.mkdir()
    dst.mkdir()
    _tap_co_hook_day_du(job_dir)

    n = D._dong_goi_hook(job_dir, dst)
    assert n == 6  # 4 file gốc + 2 file trong flow_prompts/
    for ten in D.HOOK_FILES_GOC:
        d = dst / "hook" / ten
        assert d.exists()
        assert d.read_bytes() == (job_dir / "hook" / ten).read_bytes()
    assert (dst / "hook" / "flow_prompts" / "shot_01.txt").exists()
    assert (dst / "hook" / "flow_prompts" / "shot_02.txt").exists()


def test_dong_goi_hook_khong_co_hook_thi_khong_tao_gi_khong_loi(tmp_path):
    """Đối chứng: tập KHÔNG có hook/ → gói giao giữ nguyên như cũ, không tạo thư mục hook/ rỗng,
    không báo lỗi gì."""
    import dong_goi_may2 as D
    job_dir = tmp_path / "job"
    dst = tmp_path / "goi"
    job_dir.mkdir()
    dst.mkdir()
    (job_dir / "script.txt").write_text("nội dung", encoding="utf-8")   # tập bình thường, không hook

    n = D._dong_goi_hook(job_dir, dst)
    assert n == 0
    assert not (dst / "hook").exists()


def test_dong_goi_hook_thieu_file_sau_copy_thi_bao_loi(tmp_path, monkeypatch):
    """Tự kiểm: nếu 1 file bị hỏng/không khớp kích thước ngay sau khi copy (mô phỏng lỗi đĩa nửa
    chừng) thì phải SystemExit — không được lặng lẽ báo '✓ đóng gói' như đã đủ."""
    import dong_goi_may2 as D
    job_dir = tmp_path / "job"
    dst = tmp_path / "goi"
    job_dir.mkdir()
    dst.mkdir()
    _tap_co_hook_day_du(job_dir)

    goc = D.shutil.copy2

    def _copy2_hong(src, dst_path):
        goc(src, dst_path)
        if Path(dst_path).name == "hook_lock.json":
            Path(dst_path).write_bytes(b"")   # giả lập copy hỏng: rỗng, khác kích thước nguồn
    monkeypatch.setattr(D.shutil, "copy2", _copy2_hong)

    with pytest.raises(SystemExit, match="hook_lock.json"):
        D._dong_goi_hook(job_dir, dst)


def test_kiem_hook_trong_goi_bao_dat_khi_du(capsys):
    """Việc 2 (drive_handoff.py): phép tự kiểm hook trong doi_chieu/doi_chieu_local — đủ file thì
    in dòng khẳng định rõ ràng, không lẫn vào danh sách thiếu chung."""
    import drive_handoff as DH
    duoi = {"script.txt", "hook/hook_locked.txt", "hook/grok_jobs.csv"}
    DH._kiem_hook_trong_goi(duoi, thieu=[])
    out = capsys.readouterr().out
    assert "hook/" in out and "2" in out
    assert "THIẾU" not in out.upper() and "THIEU" not in out


def test_kiem_hook_trong_goi_bao_thieu_khi_thieu(capsys):
    import drive_handoff as DH
    duoi = {"script.txt", "hook/hook_locked.txt", "hook/grok_jobs.csv"}
    thieu = ["hook/grok_jobs.csv"]
    DH._kiem_hook_trong_goi(duoi, thieu)
    out = capsys.readouterr().out
    assert "hook/grok_jobs.csv" in out
    assert "THIẾU" in out.upper()


def test_kiem_hook_trong_goi_khong_co_hook_thi_im_lang(capsys):
    """Tập không có hook/ ở nguồn → không in gì cả (giữ log sạch cho ~90% tập chưa dùng hook)."""
    import drive_handoff as DH
    duoi = {"script.txt", "img_prompts.txt"}
    DH._kiem_hook_trong_goi(duoi, thieu=[])
    out = capsys.readouterr().out
    assert out == ""
