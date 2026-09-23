# -*- coding: utf-8 -*-
"""ai_steps.strip_markers phải bỏ DÒNG TIÊU ĐỀ ở đầu bản thảo (2026-09-23).

Bẫy thật: 6/8 tập lane kenko-chiebukuro có dòng 「タイトル：…」 đứng đầu script.txt; script.txt đi
thẳng vào TTS nên giọng đọc to chữ 「タイトル」 ở giây 0,3 — ep01–04 đã ra tới người xem như vậy.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_steps  # noqa: E402


def test_bo_dong_tieu_de_dau_ban_thao():
    t = "タイトル：気づかないうちに進む「筋肉の減少」5つのサイン\n\n朝ベッドから起き上がるとき"
    assert ai_steps.strip_markers(t).startswith("朝ベッドから")


def test_bo_ca_dau_hai_cham_nua_rong_va_bien_the():
    for dau in ("タイトル:", "題名：", "表題:", "Title:", "TITLE ："):
        assert ai_steps.strip_markers(f"{dau}あるタイトル\n本文です。") == "本文です。"


def test_khong_dung_toi_chu_タイトル_nam_giua_bai():
    """Chỉ DÒNG ĐẦU mới bị bỏ — chữ 「タイトル」 trong thân bài là lời đọc thật, giữ nguyên."""
    t = "本文です。\n新聞のタイトル：見出しを読んだ。"
    assert "新聞のタイトル：見出しを読んだ。" in ai_steps.strip_markers(t)


def test_khong_dung_toi_ban_thao_binh_thuong():
    t = "「お母さん、腕が細くなった」。訪ねてきた娘さんの、ひと言でした。"
    assert ai_steps.strip_markers(t) == t
