# -*- coding: utf-8 -*-
r"""Cổng chống chạy lại K1+K2 cho kênh máy 2 đã nghiên cứu (anh chốt 2026-09-24). 0 LLM, 0 mạng.

Nguồn: `FlowHandoff_local\shared\YEU_CAU_MAY1_2026-09-24_dung_chay_lai_k1k2.md`.
Điểm mấu chốt đã đo thật: gói `results\laneK_from_research\` KHÔNG có `CHANNEL_DNA.md` /
`VIDEO_ANALYSIS` — nên cổng phải phân biệt "máy 2 có đụng vào kênh" với "máy 2 giao bản DÙNG ĐƯỢC".
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import channel_analyzer as C  # noqa: E402

CID = "UCEBA1RFfkXQtqgiDVLh4bcw"
URL = f"https://www.youtube.com/channel/{CID}"


def _ban_du(goc, slug="rougo-no-goro", cid=CID, n=8):
    """Bản máy 2 giao theo kênh truyền CHUẨN: có CHANNEL_DNA.md + VIDEO_ANALYSIS + run_log.txt."""
    d = goc / "channel_dna" / slug
    (d / "VIDEO_ANALYSIS").mkdir(parents=True)
    (d / "CHANNEL_DNA.md").write_text("## Audience\n…", encoding="utf-8")
    (d / "run_log.txt").write_text(f"[B1] Crawl catalog https://www.youtube.com/channel/{cid} ...",
                                   encoding="utf-8")
    for i in range(n):
        (d / "VIDEO_ANALYSIS" / f"v{i}.json").write_text("{}", encoding="utf-8")
    return d


def _ban_thieu(goc, ten="laneK_from_research", cid=CID):
    """Bản máy 2 giao theo kênh truyền hồ sơ ngách: CHỈ có phiếu việc + data/, thiếu DNA."""
    d = goc / ten
    (d / "data").mkdir(parents=True)
    (d / "data" / "channel.json").write_text(
        json.dumps({"meta": {"channel_id": cid, "name": "千種テンカ"}, "videos": []},
                   ensure_ascii=False), encoding="utf-8")
    (d / "GIAO_VIEC_LANE_K_2026-09-24.md").write_text("# phiếu việc", encoding="utf-8")
    return d


# ───────────────────────────────── nhận diện kênh
def test_rut_dinh_danh_tu_url_id_va_handle():
    assert C._dinh_danh(URL) == (CID, None)
    assert C._dinh_danh("https://www.youtube.com/@iyaku_labo") == (None, "iyaku_labo")
    assert C._dinh_danh("") == (None, None)


def test_url_khong_doc_duoc_thi_khong_chan(tmp_path):
    """Không rút được định danh thì KHÔNG được chặn — thà chạy lại còn hơn khoá nhầm."""
    assert C.ban_cua_may2("https://example.com/abc", goc=tmp_path) == []


# ───────────────────────────────── phân biệt "có đụng" vs "dùng được"
def test_chan_khi_may2_giao_ban_DUNG_DUOC(tmp_path, capsys):
    _ban_du(tmp_path)
    assert C.ban_cua_may2(URL, goc=tmp_path)[0]["co_dna"] is True
    C.ban_cua_may2(URL, goc=tmp_path)


def test_KHONG_chan_khi_ban_may2_thieu_dna(tmp_path):
    """Đo thật Lane K: gói giao thiếu CHANNEL_DNA.md/VIDEO_ANALYSIS → K3 không chạy được, nên cổng
    phải CHO chạy, chỉ cảnh báo. Chặn ở đây là khoá máy 1 khỏi thứ nó buộc phải có."""
    _ban_thieu(tmp_path)
    ban = C.ban_cua_may2(URL, goc=tmp_path)
    assert len(ban) == 1 and ban[0]["co_dna"] is False and ban[0]["n_video_analysis"] == 0


def test_ban_co_dna_ma_thieu_video_analysis_van_cho_chay(tmp_path):
    """K3 `retrieve_videos.py` cần VIDEO_ANALYSIS/*.json — có mỗi CHANNEL_DNA.md là chưa đủ dùng."""
    d = _ban_du(tmp_path, n=0)
    assert (d / "CHANNEL_DNA.md").is_file()
    ban = C.ban_cua_may2(URL, goc=tmp_path)
    assert ban[0]["co_dna"] and ban[0]["n_video_analysis"] == 0


# ───────────────────────────────── hành vi cổng
def test_cong_chan_tra_False_va_in_duong_dan_ban_cu(tmp_path, capsys):
    _ban_du(tmp_path)
    assert C.cong_chong_trung(URL, goc=tmp_path) is False
    out = capsys.readouterr().out
    assert "DỪNG" in out and "rougo-no-goro" in out and "--force" in out


def test_force_thi_van_chay_nhung_canh_bao_ton_quota(tmp_path, capsys):
    _ban_du(tmp_path)
    assert C.cong_chong_trung(URL, force=True, goc=tmp_path) is True
    assert "quota" in capsys.readouterr().out.lower()


def test_ban_thieu_thi_cho_chay_va_chi_duong_xin_bo_sung(tmp_path, capsys):
    _ban_thieu(tmp_path)
    assert C.cong_chong_trung(URL, goc=tmp_path) is True
    out = capsys.readouterr().out
    assert "THIẾU" in out and "YEU_CAU_MAY2" in out


def test_kenh_may1_tu_tim_thi_im_lang_cho_chay(tmp_path, capsys):
    """Ngoại lệ hợp lý trong chính yêu cầu của máy 2: kênh máy 1 tự tìm thì chạy bình thường."""
    _ban_du(tmp_path, cid="UCxxxxxxxxxxxxxxxxxxxxxx")
    assert C.cong_chong_trung(URL, goc=tmp_path) is True
    assert capsys.readouterr().out.strip() == ""
