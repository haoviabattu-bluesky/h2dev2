# -*- coding: utf-8 -*-
"""G7 — channel_analyzer phải ĐỌC chữ thumbnail từ ẢNH, không suy luận (chốt 2026-09-23).

Không gọi mạng: `sol_client` được thay bằng bản giả trong từng test.
"""
import json
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import channel_analyzer as C  # noqa: E402


@pytest.fixture
def gia(monkeypatch):
    """Cắm sol_client GIẢ vào sys.modules rồi GỠ RA khi test xong.

    Bài học 2026-09-23: bản đầu ghi thẳng `sys.modules["sol_client"] = <giả>` và không gỡ — module
    giả sống tiếp sang các test sau trong cùng tiến trình và làm hỏng test_hook_stage::
    test_run_hook_parse (chỉ hỏng khi chạy CẢ BỘ, chạy riêng vẫn xanh — đúng kiểu lỗi khó truy nhất).
    monkeypatch.setitem tự khôi phục trạng thái cũ.
    """
    def cam(tra=None, no=None):
        m = types.ModuleType("sol_client")

        def chat(text, image_path=None, max_tokens=2000, timeout=180):
            if no:
                raise no
            return json.dumps(tra, ensure_ascii=False)
        m.chat = chat
        monkeypatch.setitem(sys.modules, "sol_client", m)
        return m
    return cam


def test_prompt_cam_suy_luan_chu_thumbnail():
    assert "CẤM suy luận" in C.DNA_PROMPT
    assert "## Promise" in C.DNA_PROMPT          # mục "lời hứa của video" bắt buộc
    for k in ("loi_hua_video", "cap_khop", "thumbnail"):
        assert k in C.VIDEO_PROMPT


def test_thumb_block_thieu_anh_thi_noi_ro_de_trong(tmp_path):
    t = C._thumb_block({"id": "x"})
    assert "CHƯA ĐỌC ĐƯỢC ẢNH" in t and "KHÔNG suy luận" in t


def test_doc_chu_thumbnail_tra_dong_chu(tmp_path, gia):
    gia({"dong_chu": ["彼は地球の人間ではない", "UFOは宇宙人じゃない"], "bo_cuc": "2 băng chữ", "doc_duoc": True})
    anh = tmp_path / "a.jpg"
    anh.write_bytes(b"x")
    d = C.doc_chu_thumbnail(anh)
    assert d["dong_chu"][0] == "彼は地球の人間ではない"


def test_loi_doc_anh_khong_lam_gay_ca_luot_phan_tich(tmp_path, gia):
    """Hỏng mạng/model trả rác chỉ mất phần thumbnail của MỘT video — cùng chính sách với bước tags."""
    gia(no=RuntimeError("503 upstream"))
    anh = tmp_path / "a.jpg"
    anh.write_bytes(b"x")
    assert C.doc_chu_thumbnail(anh) is None


def test_cache_khong_goi_lai_lan_hai(tmp_path, monkeypatch):
    goi = {"n": 0}
    m = types.ModuleType("sol_client")

    def chat(text, image_path=None, max_tokens=2000, timeout=180):
        goi["n"] += 1
        return json.dumps({"dong_chu": ["A"], "bo_cuc": "x"}, ensure_ascii=False)
    m.chat = chat
    monkeypatch.setitem(sys.modules, "sol_client", m)
    (tmp_path / "_raw" / "thumbs").mkdir(parents=True)
    (tmp_path / "_raw" / "thumbs" / "01_100_vid1.jpg").write_bytes(b"x")
    rows = [{"id": "vid1"}]
    C.gan_chu_thumbnail(rows, tmp_path)
    C.gan_chu_thumbnail([{"id": "vid1"}], tmp_path)
    assert goi["n"] == 1, "lượt thứ hai phải đọc cache, không gọi lại (mỗi lượt gọi là tiền)"


def test_thieu_anh_thi_bo_qua_khong_nem(tmp_path, gia):
    gia({"dong_chu": [], "bo_cuc": ""})
    (tmp_path / "_raw" / "thumbs").mkdir(parents=True)
    rows = C.gan_chu_thumbnail([{"id": "khong_co_anh"}], tmp_path)
    assert "thumb_text" not in rows[0]
