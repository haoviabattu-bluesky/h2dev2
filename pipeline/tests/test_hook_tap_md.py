# -*- coding: utf-8 -*-
"""HOOK_TAP.md — file hook text máy 1 gửi cho dự án tiêu đề + máy 2 (anh chốt 2026-09-24). 0 LLM, 0 mạng."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hook_tap_md as H  # noqa: E402


def _prof(monkeypatch, **kw):
    p = {"id": "x", "language": "ja", "voice": {"char_rate": 300.0},
         "script": {"gate": {"list_item_count": 5}, "hook": {"enabled": True}},
         "goi_dang": {"enabled": True, **kw}}
    monkeypatch.setattr(H.profiles, "load", lambda pid: p)
    monkeypatch.setattr(H.profiles, "gate", lambda pr: pr["script"]["gate"])
    return p


def _tap(tmp, hook="", script="", promise="", timeline=None, vi_srt="", n_anh=0):
    d = tmp / "ep01-x"
    (d / "hook").mkdir(parents=True, exist_ok=True)
    (d / "script.txt").write_text(script, encoding="utf-8")
    if hook:
        (d / "hook" / "hook_locked.txt").write_text(hook, encoding="utf-8")
    if promise:
        (d / "promise.txt").write_text(promise, encoding="utf-8")
    if timeline:
        (d / "hook" / "hook_timeline.json").write_text(json.dumps(timeline, ensure_ascii=False),
                                                      encoding="utf-8")
    if vi_srt:
        (d / "hook" / "hook_vi.srt").write_text(vi_srt, encoding="utf-8")
    if n_anh:
        (d / "hook" / "img").mkdir(exist_ok=True)
        for i in range(1, n_anh + 1):
            (d / "hook" / "img" / f"{i:03d}.png").write_bytes(b"x")
    return d


TL = {"cau_ket_hook": "お伝えしたいことがあります",
      "shots": [{"n": 1, "t0": 0.0, "t1": 6.4, "voice": "六十八歳の私は気づかなかった。",
                 "ky_vong": "Bà mẹ rót trà, thấy mặt"},
                {"n": 2, "t0": 6.4, "t1": 11.1, "voice": "段差でふらついた。",
                 "ky_vong": "Bà bước xuống bậc, loạng choạng"}]}
VI = ("1\n00:00:00,100 --> 00:00:06,000\nTôi 68 tuổi, chẳng nhận ra gì.\n\n"
      "2\n00:00:06,500 --> 00:00:11,000\nLoạng choạng ở bậc thềm.\n")
SC = "六十八歳の私は気づかなかった。段差でふらついた。" + "あ" * 300


# ───────────────────────────────── cổng nghiệm thu
def test_tap_chua_co_hook_thi_cong_khong_doi(tmp_path, monkeypatch):
    """Tập chưa có hook không phải việc của cổng này — đừng chặn oan tập cũ."""
    d = _tap(tmp_path, script=SC)
    assert H.kiem(d) == []


def test_thieu_file_thi_chan(tmp_path, monkeypatch):
    d = _tap(tmp_path, hook="あ" * 50, script=SC)
    loi = H.kiem(d)
    assert any("thiếu" in x and "HOOK_TAP.md" in x for x in loi)


def test_con_cho_chua_viet_thi_chan(tmp_path, monkeypatch):
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私は気づかなかった。", script=SC, timeline=TL)
    H.sinh(d, "x")
    loi = H.kiem(d)
    assert any("chưa viết" in x for x in loi), loi


def test_viet_xong_thi_qua(tmp_path, monkeypatch):
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私は気づかなかった。", script=SC, timeline=TL)
    f, _ = H.sinh(d, "x")
    txt = f.read_text(encoding="utf-8")
    # giả lập người viết xong: bỏ hết dấu còn chờ
    import re
    f.write_text(re.sub(r"<<CẦN NGƯỜI:[^>]*>>", "đã viết", txt), encoding="utf-8")
    assert H.kiem(d) == []


def test_dong_huong_dan_khong_bi_dem_la_cho_can_viet(tmp_path, monkeypatch):
    """Dòng dặn ở đầu file từng bị đếm là 'chỗ cần viết' (báo 5 chỗ trong khi chỉ có 4)."""
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私は気づかなかった。", script=SC, timeline=TL, promise="lời hứa")
    f, _ = H.sinh(d, "x")
    dong_quote = [l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith(">")]
    assert dong_quote, "phải có khối hướng dẫn"
    assert all(H.CAN_NGUOI not in l for l in dong_quote)


# ───────────────────────────────── phần TẤT ĐỊNH máy rút
def test_bang_moc_giay_ghep_du_jp_vi_hinh(tmp_path, monkeypatch):
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私は気づかなかった。", script=SC, timeline=TL, vi_srt=VI)
    f, _ = H.sinh(d, "x")
    t = f.read_text(encoding="utf-8")
    assert "0.0–6.4" in t and "六十八歳の私は気づかなかった。" in t
    assert "Tôi 68 tuổi" in t                     # cột Việt lấy từ hook_vi.srt
    assert "Bà mẹ rót trà" in t                   # cột hình lấy từ ky_vong


def test_tu_khoa_chi_lay_cum_CO_trong_script(tmp_path, monkeypatch):
    """Cụm hook không có trong script thì KHÔNG được liệt kê — đó chính là luật G2."""
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私。そして納豆の秘密。", script="六十八歳の私" + "あ" * 200, timeline=TL)
    f, _ = H.sinh(d, "x")
    muc3 = f.read_text(encoding="utf-8").split("## 3")[1].split("## 4")[0]
    assert "六十八歳" in muc3
    assert "納豆" not in muc3, "cụm không có trong script mà vẫn liệt kê = chỉ đường sai cho bên viết tiêu đề"


def test_tu_khoa_khong_lay_tu_than_bai(tmp_path, monkeypatch):
    """Bản đầu quét cả script[:4000] → lọt kanji chung chung của thân bài, làm danh sách mất tác dụng."""
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="段差でふらついた。", script="段差でふらついた。判断 体重 水分 病気 理由" + "あ" * 200,
             timeline=TL)
    f, _ = H.sinh(d, "x")
    muc3 = f.read_text(encoding="utf-8").split("## 3")[1].split("## 4")[0]
    assert "段差" in muc3
    assert "判断" not in muc3 and "体重" not in muc3


def test_lane_danh_sach_tu_viet_dong_cam_lo_muc_1(tmp_path, monkeypatch):
    _prof(monkeypatch, list_mode=True)
    d = _tap(tmp_path, hook="六十八歳の私。", script=SC, timeline=TL)
    f, _ = H.sinh(d, "x")
    assert "Tên mục số 1" in f.read_text(encoding="utf-8")


def test_lane_khong_phai_danh_sach_thi_khong_co_dong_do(tmp_path, monkeypatch):
    _prof(monkeypatch, list_mode=False)
    d = _tap(tmp_path, hook="六十八歳の私。", script=SC, timeline=TL)
    f, _ = H.sinh(d, "x")
    assert "Tên mục số 1" not in f.read_text(encoding="utf-8")


def test_liet_ke_anh_hook(tmp_path, monkeypatch):
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私。", script=SC, timeline=TL, n_anh=3)
    t = H.sinh(d, "x")[0].read_text(encoding="utf-8")
    assert t.count("hook\\img\\") >= 3 or t.count("hook/img/") >= 3


# ───────────────────────────────── không phá phần người đã viết
def test_khong_ghi_de_file_da_co(tmp_path, monkeypatch):
    """Phần viết tay trong HOOK_TAP.md không sinh lại được — mất là phải viết từ đầu."""
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私。", script=SC, timeline=TL)
    (d / H.TEN).write_text("# bản người viết tay\nnội dung quý", encoding="utf-8")
    f, canh = H.sinh(d, "x")
    assert "nội dung quý" in f.read_text(encoding="utf-8")
    assert any("giữ nguyên" in c for c in canh)


def test_ghi_de_khi_duoc_yeu_cau_tuong_minh(tmp_path, monkeypatch):
    _prof(monkeypatch)
    d = _tap(tmp_path, hook="六十八歳の私。", script=SC, timeline=TL)
    (d / H.TEN).write_text("cũ", encoding="utf-8")
    f, _ = H.sinh(d, "x", ghi_de=True)
    assert "HOOK TẬP" in f.read_text(encoding="utf-8")


def test_chua_co_hook_locked_thi_khong_sinh(tmp_path, monkeypatch):
    _prof(monkeypatch)
    d = _tap(tmp_path, script=SC)
    f, canh = H.sinh(d, "x")
    assert not f.exists() and any("hook_locked" in c for c in canh)
