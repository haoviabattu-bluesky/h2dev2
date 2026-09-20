# -*- coding: utf-8 -*-
"""Test B3S trong flow B (brain_channel.check_b3s) — mock sol + mock Claude, KHONG goi mang/LLM.
Thu tu anh chot 2026-09-18: PASS di tiep · FIX -> Claude sua -> sol cham lai 1 lan (FIX nhe van qua)
· REMAKE -> Claude tu cham: PASS di tiep / khong sua duoc -> dung + ESCALATION."""
import brain_channel as BC
import qc_script_sol

PROF_SOL = {"id": "satori-jp-obaa", "script": {"sol_qc": True}}
PROF_KHONG = {"id": "kenko-chiebukuro", "script": {}}


def _mk(tmp_path):
    (tmp_path / "script.txt").write_text("昔の話です。" * 50, encoding="utf-8")
    (tmp_path / "dan_y.txt").write_text("老後の話\n", encoding="utf-8")
    return tmp_path


def _mock_sol(monkeypatch, verdicts):
    """sol tra lan luot cac verdict; ghi ra file --out nhu that."""
    goi = []

    def run(script_text, title, profile_id=None, out=None):
        v = verdicts[len(goi)]
        goi.append((title, out))
        if out:
            from pathlib import Path
            Path(out).write_text(f"KẾT QUẢ: {v}\n1. ...", encoding="utf-8")
        return v, f"KẾT QUẢ: {v}"
    monkeypatch.setattr(qc_script_sol, "run", run)
    return goi


def _mock_claude(monkeypatch, tmp_path, viet_verdict=None, doi_script=True):
    """Claude headless: doi script (neu doi_script) va ghi B3S_claude_verdict.txt (neu viet_verdict)."""
    import brain_steps
    goi = []

    def run_creative(slug_dir, profile_id, minutes, on_line=None, permission_mode="x",
                     budget_usd=0.0, phase="all", extra_prompt="", **kw):
        goi.append(extra_prompt)
        if doi_script:
            (tmp_path / "script.txt").write_text("直した話です。" * 50, encoding="utf-8")
        if viet_verdict is not None:
            (tmp_path / "logs").mkdir(exist_ok=True)
            (tmp_path / "logs" / "B3S_claude_verdict.txt").write_text(viet_verdict, encoding="utf-8")
        return True, "BRAIN_DONE"
    monkeypatch.setattr(brain_steps, "run_creative", run_creative)
    # cong so sau sua: coi nhu dat (khong goi ai_steps) · B3Q hoi quy: coi nhu dat (khong goi LLM)
    monkeypatch.setattr(BC, "check_gate", lambda *a, **k: [])
    monkeypatch.setattr(BC, "check_b3q", lambda *a, **k: (True, []))
    return goi


def test_lane_khong_bat_sol_bo_qua(tmp_path, monkeypatch):
    goi = _mock_sol(monkeypatch, ["REMAKE"])
    ok, v = BC.check_b3s(PROF_KHONG, _mk(tmp_path), {"title": ""}, 30)
    assert ok and v == "SKIPPED" and goi == []


def test_pass_di_tiep_khong_goi_claude(tmp_path, monkeypatch):
    goi = _mock_sol(monkeypatch, ["PASS"])
    claude = _mock_claude(monkeypatch, tmp_path)
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": "T"}, 30)
    assert ok and v == "PASS" and len(goi) == 1 and claude == []
    assert goi[0][0] == "T" and str(goi[0][1]).endswith("B3S_sol_001.txt")


def test_fix_claude_sua_sol_cham_lai_1_lan_fix_nhe_van_qua(tmp_path, monkeypatch):
    goi = _mock_sol(monkeypatch, ["FIX", "FIX"])
    claude = _mock_claude(monkeypatch, tmp_path)
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert ok and v == "FIX"
    assert len(goi) == 2 and len(claude) == 1          # sol dung 2 lan, Claude sua dung 1 lan
    assert "SAI" in claude[0] and "B3S_sol_001.txt" in claude[0]
    assert "直した" in (tmp_path / "script.txt").read_text(encoding="utf-8")


def test_fix_roi_remake_claude_tu_cham_pass(tmp_path, monkeypatch):
    goi = _mock_sol(monkeypatch, ["FIX", "REMAKE"])
    claude = _mock_claude(monkeypatch, tmp_path, viet_verdict="PASS\nđã cắt tình tiết gãy")
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert ok and v == "PASS_CLAUDE" and len(goi) == 2 and len(claude) == 2
    assert "B3S_sol_002.txt" in claude[1]


def test_remake_khong_sua_duoc_dung_va_escalation(tmp_path, monkeypatch):
    goi = _mock_sol(monkeypatch, ["REMAKE"])
    claude = _mock_claude(monkeypatch, tmp_path, viet_verdict=BC.KHONG_SUA_DUOC + "\nkhung truyện gãy")
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert not ok and v == "REMAKE" and len(goi) == 1 and len(claude) == 1
    rep = (tmp_path / "ESCALATION_REPORT.md").read_text(encoding="utf-8")
    assert BC.KHONG_SUA_DUOC in rep and "B3S" in rep


def test_remake_claude_khong_ghi_ket_luan_coi_nhu_khong_sua_duoc(tmp_path, monkeypatch):
    _mock_sol(monkeypatch, ["REMAKE"])
    _mock_claude(monkeypatch, tmp_path, viet_verdict=None)
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert not ok and (tmp_path / "ESCALATION_REPORT.md").exists()


def test_sol_loi_ha_tang_khong_chan(tmp_path, monkeypatch):
    def run(*a, **k):
        raise RuntimeError("9router down")
    monkeypatch.setattr(qc_script_sol, "run", run)
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert ok and v == "INFRA"


def test_resume_script_khong_doi_bo_qua_sol(tmp_path, monkeypatch):
    goi = _mock_sol(monkeypatch, ["PASS", "REMAKE"])
    _mock_claude(monkeypatch, tmp_path)
    d = _mk(tmp_path)
    ok, v = BC.check_b3s(PROF_SOL, d, {"title": ""}, 30)
    assert ok and v == "PASS" and (d / "logs" / "B3S_latest.json").exists()
    ok2, v2 = BC.check_b3s(PROF_SOL, d, {"title": ""}, 30)      # chạy lại, script chưa đổi
    assert ok2 and v2 == "PASS" and len(goi) == 1               # sol KHÔNG bị gọi lần 2
    (d / "script.txt").write_text("別の話。" * 60, encoding="utf-8")
    ok3, v3 = BC.check_b3s(PROF_SOL, d, {"title": ""}, 30)      # script đổi → chấm lại
    assert len(goi) == 2


def test_brief_noi_ro_nguon_tieu_de(tmp_path, monkeypatch):
    _mock_sol(monkeypatch, ["FIX", "PASS"])
    claude = _mock_claude(monkeypatch, tmp_path)
    BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert "dan_y.txt" in claude[0]


def _mock_qc_script(monkeypatch, tmp_path, returncode, lines):
    """Giả lập subprocess qc_script.py: in `lines`, thoát `returncode`."""
    import subprocess

    class P:
        def __init__(self, *a, **k):
            self.stdout = iter([l + "\n" for l in lines]); self.returncode = returncode
        def wait(self): pass
    monkeypatch.setattr(subprocess, "Popen", P)
    (tmp_path / "script.txt").write_text("話。" * 50, encoding="utf-8")  # không competitor.txt → bỏ qua tầng 0


def test_b3q_dat_thi_dong_x_khong_chan(tmp_path, monkeypatch):
    _mock_qc_script(monkeypatch, tmp_path, 0, ["=== QC NỘI DUNG: DAT ===",
                                              "   ✗ trùng ý: thủ pháp kết cấu vòng có chủ đích"])
    dat, loi = BC.check_b3q(PROF_SOL, tmp_path, bo_cham_claude=True)
    assert dat and loi == []


def test_b3q_sua_thi_dong_x_van_chan(tmp_path, monkeypatch):
    _mock_qc_script(monkeypatch, tmp_path, 1, ["=== QC NỘI DUNG: SUA ===",
                                              "   ✗ mâu thuẫn @đoạn 3: 74 tuổi ↔ 78 tuổi"])
    dat, loi = BC.check_b3q(PROF_SOL, tmp_path, bo_cham_claude=True)
    assert not dat and len(loi) == 1 and "mâu thuẫn" in loi[0]


def test_sua_theo_sol_xong_phai_chay_lai_b3q(tmp_path, monkeypatch):
    """Sửa theo sol có thể làm gãy 伏線 / sinh câu dịch sát (đo thật STT10) → phải hồi quy B3Q."""
    _mock_sol(monkeypatch, ["FIX", "FIX"])
    claude = _mock_claude(monkeypatch, tmp_path)
    goi_b3q = []

    def fake_b3q(prof, d, on_line=None, bo_cham_claude=False):
        goi_b3q.append(1)
        return (False, ["✗ 伏線 gieo không trả:千円札"]) if len(goi_b3q) == 1 else (True, [])
    monkeypatch.setattr(BC, "check_b3q", fake_b3q)
    ok, v = BC.check_b3s(PROF_SOL, _mk(tmp_path), {"title": ""}, 30)
    assert ok and v == "FIX"
    assert len(goi_b3q) == 1                      # B3Q hồi quy được gọi sau lượt sửa
    assert len(claude) == 2                       # sửa theo sol + sửa hồi quy B3Q
    assert "伏線" in claude[1] and "RỚT LẠI cổng B3Q" in claude[1]
