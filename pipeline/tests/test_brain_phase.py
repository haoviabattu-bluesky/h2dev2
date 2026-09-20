# -*- coding: utf-8 -*-
"""Test tach 2 pha cua brain_steps.creative_prompt (P0 2026-09-18) — thuan chuoi, KHONG goi claude."""
from pathlib import Path
import brain_steps as B


def _mk(tmp_path):
    (tmp_path / "competitor.txt").write_text("x" * 100, encoding="utf-8")
    return tmp_path


def test_phase_script_chi_co_b3(tmp_path):
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30, phase="script")
    assert "1) B3" in p and "70/30" in p
    assert "img_doan.txt" not in p and "thumb_text.txt" not in p and "TIEU_DE_MO_TA" not in p
    assert "BRAIN_DONE" in p


def test_phase_assets_khong_sua_script(tmp_path):
    (tmp_path / "script.txt").write_text("s" * 200, encoding="utf-8")
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30, phase="assets")
    assert "KHÔNG sửa script.txt" in p or "KHONG sua script.txt" in p
    assert "img_doan.txt" in p and "TIEU_DE_MO_TA" in p and "thumb_text.txt" in p
    assert "1) B3: viết `script.txt`" not in p


def test_phase_all_giu_nguyen(tmp_path):
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30)
    assert "1) B3" in p and "img_doan.txt" in p and "TIEU_DE_MO_TA" in p


def test_assets_skip_theo_profile(tmp_path):
    """Lane khai `assets.skip` (satori 2026-09-19: tiêu đề/thumbnail do dự án khác lo) → đề bài pha
    assets KHÔNG còn khối việc đó, và danh sách file bắt buộc cũng bỏ chúng."""
    import profiles
    assert profiles.assets_need({"assets": {"skip": ["TIEU_DE_MO_TA.txt", "thumb_text.txt"]}}) == [
        "characters.json", "img_prompts.txt", "img_doan.txt"]
    assert profiles.assets_need({}) == profiles.ASSETS_MAC_DINH

    (tmp_path / "script.txt").write_text("s" * 200, encoding="utf-8")
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30, phase="assets")
    than = "\n".join(ln for ln in p.split("\n") if not ln.startswith("- LANE NÀY KHÔNG LÀM"))
    assert "TIEU_DE_MO_TA" not in than and "thumb_text.txt" not in than
    assert "img_prompts.txt" in than and "img_doan.txt" in than     # việc vẫn phải làm
    assert "LANE NÀY KHÔNG LÀM" in p
