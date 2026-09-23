# -*- coding: utf-8 -*-
"""Cong PHU CHU cua tts.py — chan ban doc bi server NUOT MAT mot cau.

Vi sao co bai test nay: do that 2026-09-23 tren hook ep05-bermuda-triangle, 4 luot TTS cung mot
doan text thi 3 luot nuot tron mot cau, moi luot mot cau khac nhau. Cong DO DAI cu (so mp3 voi SRT)
khong bat duoc vi ca hai deu do cung server sinh ra nen khop nhau trong cai sai.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tts  # noqa: E402


def _srt(*cau):
    khoi = []
    for i, c in enumerate(cau, 1):
        khoi.append(f"{i}\n00:00:0{i-1},000 --> 00:00:0{i},000\n{c}\n")
    return "\n".join(khoi)


GOC = "こんにちは、皆さん。今日はいい天気です。そして明日も晴れるでしょう。"


def test_doc_du_thi_phu_100_phan_tram():
    srt = _srt("こんにちは、皆さん。", "今日はいい天気です。", "そして明日も晴れるでしょう。")
    ti_le, doc, goc = tts.kiem_phu_chu(GOC, srt)
    assert doc == goc
    assert ti_le == 1.0


def test_nuot_cau_CUOI_thi_ti_le_tut_duoi_nguong():
    srt = _srt("こんにちは、皆さん。", "今日はいい天気です。")
    ti_le, _, _ = tts.kiem_phu_chu(GOC, srt)
    assert ti_le < tts.PHU_CHU_TOI_THIEU


def test_nuot_cau_GIUA_cung_bi_bat():
    """Luot 2 cua lan do that nuot cau AP CUOI chu khong phai cau cuoi."""
    srt = _srt("こんにちは、皆さん。", "そして明日も晴れるでしょう。")
    ti_le, _, _ = tts.kiem_phu_chu(GOC, srt)
    assert ti_le < tts.PHU_CHU_TOI_THIEU


def test_dau_cau_va_xuong_dong_khong_lam_lech_ti_le():
    """SRT ngat dong giua cau (server hay lam) van phai ra 100%."""
    srt = ("1\n00:00:00,000 --> 00:00:02,000\nこんにちは、\n皆さん。\n\n"
           "2\n00:00:02,000 --> 00:00:04,000\n今日は\nいい天気です。\n\n"
           "3\n00:00:04,000 --> 00:00:06,000\nそして明日も晴れるでしょう。\n")
    ti_le, _, _ = tts.kiem_phu_chu(GOC, srt)
    assert ti_le == 1.0


def test_srt_rong_thi_ti_le_0_khong_no_loi():
    ti_le, doc, goc = tts.kiem_phu_chu(GOC, "")
    assert doc == 0 and goc > 0 and ti_le == 0.0


def test_kich_ban_rong_khong_chia_cho_0():
    ti_le, _, _ = tts.kiem_phu_chu("", "")
    assert ti_le == 1.0
