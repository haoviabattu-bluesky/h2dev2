# Thẻ viết VIRAL_LAB (2026-10-05): field script.the_viet → chèn vào prompt hook (viet_candidates) + S2 (khoi_them).
# OFFLINE: thẻ giả trong tmp_path, monkeypatch _writer_chat — không đọc thẻ thật, không gọi LLM.
import ai_steps
import hook_stage as HS
import lean_script as L

PROF = {"id": "x", "language": "ja", "voice": {"char_rate": 300.0}, "script": {}}
THE = "# THẺ\n## PHẦN 1 — LUẬT CỦA ANH\n- luật A\n## PHẦN 2 — THỊ TRƯỜNG\n- số B\n"


def _tap(d):
    (d / "title.txt").write_text("T1", encoding="utf-8")
    (d / "series_ctx.txt").write_text("[D1] x\n", encoding="utf-8")
    (d / "thumb_text.txt").write_text("A|B", encoding="utf-8")
    return d


def _prompt_hook(monkeypatch, d, prof):
    got = {}
    monkeypatch.setattr(HS.ai_steps, "_writer_chat",
                        lambda prof, prompt, **k: (got.update(p=prompt) or type("R", (), {"text": "x"})()))
    HS.viet_candidates(d, prof, {}, "T", "")
    return got["p"]


def test_doc_the_viet_vang_field_va_file_thieu(tmp_path, capsys):
    assert ai_steps.doc_the_viet(PROF) == ""
    assert ai_steps.doc_the_viet({"script": {"the_viet": str(tmp_path / "khong_co.md")}}) == ""
    assert "thẻ viết không có" in capsys.readouterr().out


def test_doc_the_viet_cat_tran(tmp_path):
    f = tmp_path / "the.md"
    f.write_text("あ" * 20000, encoding="utf-8")
    assert len(ai_steps.doc_the_viet({"script": {"the_viet": str(f)}})) == ai_steps.THE_VIET_MAX


def test_hook_vang_field_prompt_giu_nguyen(monkeypatch, tmp_path):
    d = _tap(tmp_path)
    a = _prompt_hook(monkeypatch, d, {**PROF, "script": {}})
    b = _prompt_hook(monkeypatch, d, {**PROF, "script": {"the_viet": ""}})
    c = _prompt_hook(monkeypatch, d, {**PROF, "script": {"the_viet": str(tmp_path / "khong_co.md")}})
    assert a == b == c and "THẺ VIẾT" not in a


def test_hook_co_the_dung_truoc_luat_viet(monkeypatch, tmp_path):
    d = _tap(tmp_path)
    f = tmp_path / "the.md"; f.write_text(THE, encoding="utf-8")
    # 2026-10-17 (anh duyệt): luật hook DUY NHẤT = bám sườn + động cơ chính hook video gốc → thẻ viết KHÔNG còn vào prompt hook
    # (chỉ còn ở S2 thân bài).
    p = _prompt_hook(monkeypatch, d, {**PROF, "script": {"the_viet": str(f), "hook": {}}})
    assert "PHẦN 1 — LUẬT CỦA ANH" not in p and "LUẬT DUY NHẤT" in p


def test_s2_khoi_them(tmp_path):
    assert L.khoi_them({**PROF, "script": {"cung_cam_xuc": False}}) == ""
    f = tmp_path / "the.md"; f.write_text(THE, encoding="utf-8")
    them = L.khoi_them({**PROF, "script": {"the_viet": str(f)}})
    assert them.index(L.CUNG_CAM_XUC) < them.index("PHẦN 1 — LUẬT CỦA ANH")
    assert L.khoi_them({**PROF, "script": {}}) == L.CUNG_CAM_XUC


def test_expanduser(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path)); monkeypatch.setenv("USERPROFILE", str(tmp_path))
    (tmp_path / "t.md").write_text(THE, encoding="utf-8")
    assert "PHẦN 1" in ai_steps.doc_the_viet({"script": {"the_viet": "~/t.md"}})
