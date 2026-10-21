# -*- coding: utf-8 -*-
"""so_lieu_dong.py — nháp số liệu động + nghiệm thu --kiem (anh chốt 2026-10-06; 2026-10-07 chuyển sang máy 2).

Giữ chốt 2 điều: (1) chỉ lấy số trong SỐ ĐƯỢC PHÉP mà script thật sự đọc, nguồn lấy theo tổ chức
được nêu ngay trong câu/câu trước (ep03 từng gán nhầm 2024年 của GPTW sang マイナビ khi chỉ tìm theo số);
(2) --kiem bắt bản nháp chưa duyệt và cau_chua không có trong script.
"""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import so_lieu_dong as sld  # noqa: E402

CTX = """SỐ ĐƯỢC PHÉP: 2024年 · 44.5% · 13,824人 · 11.9% · 5社に1社
[D1] マイナビ「正社員の静かな退職に関する調査2025年（2024年実績）」で、正社員の44.5%が…
[D2] 同調査で、得られたものが「ある」…
[D4] Great Place To Work® Institute Japanの2024年12月調査（13,824人）で、上司層はわずか11.9%…
[D5] エン・ジャパンの調査で、5社に1社が…
"""
SCRIPT = ("マイナビが調べた。それをしていると答えた人が、44.5%だった。"
          "「Great Place To Work Institute Japanが、2024年の暮れに、13,824人に聞いた調査がある。」"
          "上司の側で同じ意見なのは、わずか11.9%。そう答えた会社が、5社に1社。")


def test_so_duoc_phep_va_don_vi():
    assert sld._so_duoc_phep(CTX) == ["2024年", "44.5%", "13,824人", "11.9%", "5社に1社"]
    assert sld._don_vi("44.5%") == ("44.5", "%")
    assert sld._don_vi("13,824人") == ("13,824", "人")
    assert sld._don_vi("5社に1社") == ("5社に1社", "")


def test_nguon_theo_to_chuc_trong_cau_khong_theo_so_dau_tien():
    nguon = sld._cac_nguon(CTX)
    cau = sld._cau(SCRIPT)
    k = next(i for i, c in enumerate(cau) if "2024年" in c)
    dn, ten = sld._nguon(nguon, "2024年", "".join(cau[max(0, k - 3): k + 1]))
    assert dn == "D4" and ten.startswith("Great Place")


def test_dong_dong_dieu_tra_muon_ten_truoc():
    nguon = dict((dn, ten) for dn, ten, _ in sld._cac_nguon(CTX))
    assert nguon["D2"] == nguon["D1"] == "マイナビ"


def _tap(tmp_path, trang_thai):
    (tmp_path / "script.txt").write_text(SCRIPT, encoding="utf-8")
    (tmp_path / sld.TEN).write_text(json.dumps({"trang_thai": trang_thai, "so": [
        {"cau_chua": "わずか11.9%", "so": "11.9", "don_vi": "%", "nhan": ""}]}, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def test_kiem_bat_ban_nhap(tmp_path):
    assert any("chưa" in x for x in sld.kiem(_tap(tmp_path, sld.NHAP)))


def test_kiem_qua_ban_da_duyet(tmp_path):
    assert sld.kiem(_tap(tmp_path, sld.DA_DUYET)) == []


def test_kiem_bat_cau_khong_co_trong_script(tmp_path):
    tap = _tap(tmp_path, sld.DA_DUYET)
    d = json.loads((tap / sld.TEN).read_text(encoding="utf-8"))
    d["so"][0]["cau_chua"] = "câu không tồn tại"
    (tap / sld.TEN).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    assert any("không có trong script" in x for x in sld.kiem(tap))
