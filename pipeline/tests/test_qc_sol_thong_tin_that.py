# -*- coding: utf-8 -*-
"""Mục THÔNG TIN THẬT trong lời dặn Sol (anh duyệt 2026-10-07) — mock sol, KHONG goi mang."""
import qc_script_sol as Q
import sol_client


def _bat_prompt(monkeypatch, profile):
    seen = {}
    monkeypatch.setattr(Q, "_load_profile", lambda pid: profile)
    monkeypatch.setattr(sol_client, "chat", lambda prompt, **k: (seen.update(p=prompt) or "KẾT QUẢ: PASS", {}))
    return seen


def test_mac_dinh_bat_ca_3_lens(monkeypatch):
    for lens in Q.LENS_TMPL:
        seen = _bat_prompt(monkeypatch, {"script_qc": {"lens": lens}})
        v, _ = Q.run("本文。", "T", profile_id="x")
        assert v == "PASS"
        assert "KIỂM TRA THÔNG TIN THẬT" in seen["p"] and "Dễ gây hiểu nhầm" in seen["p"]
        assert "{ghi_vao}" not in seen["p"]
        assert Q.GHI_VAO[lens] in seen["p"]


def test_plain_ghi_chung_danh_sach_diem(monkeypatch):
    seen = _bat_prompt(monkeypatch, {"script_qc": {"lens": "plain"}})
    Q.run("本文。", "T", profile_id="x")
    assert "CHUNG danh sách ĐIỂM KHÔNG HỢP LÝ" in seen["p"]


def test_tat_bang_profile(monkeypatch):
    seen = _bat_prompt(monkeypatch, {"script_qc": {"lens": "plain", "thong_tin_that": False}})
    Q.run("本文。", "T", profile_id="x")
    assert "THÔNG TIN THẬT" not in seen["p"]


def test_dung_sau_noi_tu_hook(monkeypatch):
    seen = _bat_prompt(monkeypatch, {"script_qc": {"lens": "story"}})
    Q.run("本文。", "T", profile_id="x", hook_block=Q.NOI_TU_HOOK.format(hook="フック。"))
    p = seen["p"]
    assert p.index("NỐI TỪ HOOK") < p.index("KIỂM TRA THÔNG TIN THẬT") < p.index("=== KỊCH BẢN ===")
