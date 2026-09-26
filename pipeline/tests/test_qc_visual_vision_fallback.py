# -*- coding: utf-8 -*-
"""Giữ chốt qc_visual._vision (2026-09-25, sự cố máy 2): ramclouds có thể ĐỨNG IM vô hạn (không lỗi,
không timeout ở tầng urllib) — _vision phải ép thời gian bằng thread rồi rơi sang sol_client (cloud,
khác hẳn 9router chỉ chạy máy 1), KHÔNG được treo vô hạn theo bên bị treo."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qc_visual  # noqa: E402


@pytest.fixture
def anh(tmp_path):
    f = tmp_path / "001.png"
    f.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 32)
    return f


def test_ramclouds_dung_yen_thi_roi_sang_sol_client(anh, monkeypatch):
    """Mô phỏng đúng sự cố máy 2: qcc._chat KHÔNG bao giờ trả (giả treo mạng), _vision phải bỏ
    cuộc sau _VISION_TIMEOUT_S rồi dùng sol_client — không được chờ hết đời."""
    monkeypatch.setattr(qc_visual, "_VISION_TIMEOUT_S", 0.3)

    def _dung_yen(model, prompt, b64):
        time.sleep(30)
        return '{"ok": true}'
    monkeypatch.setattr(qc_visual.qcc, "_chat", _dung_yen)

    goi = {}
    def _sol_chat(prompt, image_path, max_tokens=300, timeout=90):
        goi["called"] = True
        return '{"matches_prompt": true}', {}
    import sol_client
    monkeypatch.setattr(sol_client, "chat", _sol_chat)

    t0 = time.time()
    ra = qc_visual._vision("hỏi gì đó", anh)
    dt = time.time() - t0
    assert ra == {"matches_prompt": True}
    assert goi.get("called")
    assert dt < 5, f"phải rơi sang dự phòng nhanh, đo được {dt:.1f}s"


def test_ca_hai_deu_hong_thi_QcError(anh, monkeypatch):
    monkeypatch.setattr(qc_visual, "_VISION_TIMEOUT_S", 0.2)

    def _loi(model, prompt, b64):
        raise RuntimeError("HTTP 503")
    monkeypatch.setattr(qc_visual.qcc, "_chat", _loi)

    import sol_client
    def _sol_loi(prompt, image_path, max_tokens=300, timeout=90):
        raise RuntimeError("sol: CẢ BA đường đều lỗi")
    monkeypatch.setattr(sol_client, "chat", _sol_loi)

    with pytest.raises(qc_visual.QcError) as e:
        qc_visual._vision("hỏi gì đó", anh)
    assert "ramclouds" in str(e.value) and "sol_client" in str(e.value)


def test_ramclouds_binh_thuong_khong_can_du_phong(anh, monkeypatch):
    """Đường vui: ramclouds trả nhanh → không gọi sol_client (khỏi tốn tiền/thời gian oan)."""
    def _ok(model, prompt, b64):
        return '{"matches_prompt": true}'
    monkeypatch.setattr(qc_visual.qcc, "_chat", _ok)

    import sol_client
    def _khong_duoc_goi(*a, **k):
        raise AssertionError("không được gọi sol_client khi ramclouds đã ổn")
    monkeypatch.setattr(sol_client, "chat", _khong_duoc_goi)

    ra = qc_visual._vision("hỏi gì đó", anh)
    assert ra == {"matches_prompt": True}
