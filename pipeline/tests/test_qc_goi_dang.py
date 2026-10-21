# -*- coding: utf-8 -*-
"""Test offline cổng GÓI ĐĂNG (qc_goi_dang.py) — 0 LLM, 0 mạng.

Mỗi test dựng một thư mục tập GIẢ trong tmp_path rồi gọi thẳng từng phép kiểm, nên chạy được ở
máy không có voice/ảnh/credential. Profile được monkeypatch để KHÔNG phụ thuộc profiles/*.json thật
(đổi ngưỡng lane thật không được làm gãy test này).
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qc_goi_dang as G  # noqa: E402


# ───────────────────────────────────────────── hạ tầng dựng tập giả
def prof(**kw):
    p = {"id": "x", "language": "ja", "voice": {"char_rate": 300.0},
         "script": {"gate": {}}, "goi_dang": {"enabled": True}}
    p["goi_dang"].update(kw)
    return p


def tap(tmp, script="", title="", thumb=(), mo_ta="", promise="", ten="ep01-x"):
    d = tmp / ten
    d.mkdir(parents=True, exist_ok=True)
    (d / "script.txt").write_text(script, encoding="utf-8")
    if promise:
        (d / "promise.txt").write_text(promise, encoding="utf-8")
    if title:
        (d / "title.txt").write_text(title, encoding="utf-8")
    if thumb:
        (d / "thumb_text.txt").write_text("\n".join(thumb), encoding="utf-8")
    if title or mo_ta:
        (d / "TIEU_DE_MO_TA.txt").write_text(f"{title}\n\n{mo_ta}\n", encoding="utf-8")
    return d


def moc(d, p, script):
    return G.Moc(d, p, script)


# ───────────────────────────────────────────── chuẩn hoá & grep chữ số ↔ chữ Hán
def test_kanji_va_chu_so_quy_ve_mot():
    assert G.norm("76秒") == G.norm("七十六秒")
    assert G.norm("五つの話") == G.norm("5つの話")
    assert G.norm("二十一万二千円") == G.norm("212000円")   # bẫy kanji_to_int đã vá 2026-09-21


def test_norm_bo_dau_cau_va_toan_rong():
    assert G.norm("「本当の、理由」") == G.norm("本当の理由")
    assert G.norm("１２３") == "123"


# ───────────────────────────────────────────── tách vế tiêu đề
def test_tach_ve_bo_duoi_co_dinh_va_ve_qua_ngan():
    ve = G.tach_ve_tieu_de("【アッツ島】霧の中に消えた男｜守備隊2600名｜実際の写真をAIフルカラー復元",
                           bo_qua=["実際の写真をAIフルカラー復元"])
    assert "実際の写真をAIフルカラー復元" not in "".join(ve)
    assert any("霧の中に消えた男" in v for v in ve)
    assert any("2600" in G.norm(v) for v in ve)


def test_tach_ve_khong_tra_ve_trung_nhau():
    ve = G.tach_ve_tieu_de("定年後の暮らし…定年後の暮らし")
    assert len(ve) == 1


# ───────────────────────────────────────────── G2 grep + phủ định
def test_g2_bat_ve_khong_co_trong_script(tmp_path):
    p = prof()
    sc = "ある日、彼は静かに立ち上がった。" * 20
    d = tap(tmp_path, script=sc, title="元看護婦が遺した四文字の言葉")
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "元看護婦が遺した四文字の言葉", [])
    assert any("KHÔNG có trong lời đọc" in x for x in chan)


def test_g2_chu_han_trong_script_van_grep_duoc(tmp_path):
    """Bẫy thật toshi ep10: tiêu đề ghi 76秒, script viết 七十六秒 → cổng cũ báo thiếu oan."""
    p = prof()
    sc = "その映像は七十六秒の沈黙で終わる。" + "記録は続いた。" * 30
    d = tap(tmp_path, script=sc, title="76秒の沈黙")
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "76秒の沈黙", [])
    assert not any("KHÔNG có trong lời đọc" in x for x in chan)


def test_g2_bat_ve_bi_script_phu_dinh(tmp_path):
    """Bẫy thật tano ep06: thumbnail hứa 「1円も使わず」 mà script nói ngược."""
    p = prof()
    sc = "1円も使わずに過ごせるわけではない。" + "実際には交通費がかかる。" * 20
    d = tap(tmp_path, script=sc)
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "", ["1円も使わず"])
    assert any("PHỦ ĐỊNH" in x for x in chan)


def test_g2_ve_co_cho_khang_dinh_khac_thi_khong_chan(tmp_path):
    p = prof()
    sc = "1円も使わずに過ごせるわけではない。だが工夫すれば1円も使わず一日を楽しめる。" + "あ" * 200
    d = tap(tmp_path, script=sc)
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "", ["1円も使わず"])
    assert not any("PHỦ ĐỊNH" in x for x in chan)


def test_g2_ve_loi_xuat_hien_qua_muon_thi_chan(tmp_path):
    p = prof(promise_giu_duoc_max_s=90)
    # char_rate 300 chữ/phút = 5 chữ/giây → 900 ký tự ≈ giây 180
    sc = "あ" * 900 + "図書館で見つけた宝物の話をしよう"
    d = tap(tmp_path, script=sc)
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "図書館で見つけた宝物", [])
    assert any("LÕI" in x for x in chan)


# ───────────────────────────────────────────── G3 thứ tự
def test_g3_chan_cau_mo_dau_chao_hoi(tmp_path):
    # 2026-10-17: luật hook duy nhất = bám sườn hook gốc → chỉ còn cấm xin đăng ký/cảm ơn xem ở câu mở.
    p = prof()
    sc = "こんにちは、皆さん。今日もご視聴ありがとうございます。" + "しかし実は違った。" * 10
    d = tap(tmp_path, script=sc)
    chan, _ = G.g3_thu_tu(d, G.cau_hinh(p), moc(d, p, sc), p, "", sc)
    assert any("ご視聴" in x for x in chan) and not any("こんにちは" in x for x in chan)


def test_g3_chan_doc_to_chu_tieu_de(tmp_path):
    """Bẫy thật kenko ep01–04: TTS đọc to chữ 「タイトル」 ở giây 0,3."""
    p = prof()
    sc = "タイトル。高齢者が転ぶ本当の理由。" + "しかし原因は別にあった。" * 10
    d = tap(tmp_path, script=sc)
    chan, _ = G.g3_thu_tu(d, G.cau_hinh(p), moc(d, p, sc), p, "", sc)
    assert any("タイトル" in x for x in chan)


def test_g3_chan_cau_mau_thuan_qua_tre(tmp_path):
    p = prof(contradiction_max_s=25)
    sc = "あ" * 600 + "しかし、それは違った。"      # 600 chữ ≈ giây 120
    d = tap(tmp_path, script=sc)
    # 2026-10-17: hook bám sườn hook gốc → mâu thuẫn muộn chỉ CẢNH BÁO, không chặn
    chan, canh = G.g3_thu_tu(d, G.cau_hinh(p), moc(d, p, sc), p, "", sc)
    assert any("câu mâu thuẫn" in x and "> 25" in x for x in canh) and not any("mâu thuẫn" in x for x in chan)


def test_g3_thieu_cau_nghi_thuc_chi_canh_bao(tmp_path):
    """Nguyên tắc 5 — iro 0/11 tập có 「この写真をカラー化してみる」."""
    p = prof(ritual=["この写真をカラー化してみる"])
    sc = "しかし、この一枚は違う。" + "あ" * 100
    d = tap(tmp_path, script=sc)
    chan, canh = G.g3_thu_tu(d, G.cau_hinh(p), moc(d, p, sc), p, "", sc)
    assert any("nghi thức" in x for x in canh) and not any("nghi thức" in x for x in chan)


# ───────────────────────────────────────────── G4 danh sách
def test_g4_chan_doc_truoc_danh_sach(tmp_path):
    """Bẫy thật kenko 8/8 tập đọc trước cả 5 mục."""
    p = prof(list_mode=True, list_preview_ban_s=120)
    p["script"]["gate"]["list_item_count"] = 5
    sc = "第5位から第1位まで一気に紹介します。" + "あ" * 3000
    d = tap(tmp_path, script=sc)
    chan, _ = G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, [])
    assert any("đã nêu" in x for x in chan)


def test_g4_dem_muc_khop_gate(tmp_path):
    p = prof(list_mode=True)
    p["script"]["gate"]["list_item_count"] = 5
    sc = "あ" * 1200 + "第5位。" + "い" * 300 + "第4位。" + "う" * 300 + "第3位。"
    d = tap(tmp_path, script=sc)
    chan, _ = G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, [])
    assert any("≠ gate.list_item_count = 5" in x for x in chan)


def test_g4_muc_1_phai_o_cuoi(tmp_path):
    p = prof(list_mode=True, list_order="countdown")
    sc = "あ" * 1200 + "第1位。" + "い" * 300 + "第2位。"
    d = tap(tmp_path, script=sc)
    chan, _ = G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, [])
    assert any("mục 1 phải để cuối" in x for x in chan)


def test_g4_chan_cau_tu_thao_dem_nguoc(tmp_path):
    p = prof(list_mode=True)
    sc = "あ" * 1200 + "この順位は重要度を示すものではありません。"
    d = tap(tmp_path, script=sc)
    chan, _ = G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, [])
    assert any("tự tháo đếm ngược" in x for x in chan)


def test_g4_thumbnail_lo_muc_1(tmp_path):
    p = prof(list_mode=True, thumb_item_rank=1)
    sc = "あ" * 1200
    d = tap(tmp_path, script=sc)
    chan, _ = G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, ["この食品"])
    assert any("mục GIỮA" in x for x in chan)


def test_g4_tat_khi_lane_khong_phai_video_danh_sach(tmp_path):
    p = prof(list_mode=False)
    sc = "第1位。" * 5
    d = tap(tmp_path, script=sc)
    assert G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, []) == ([], [])


# ───────────────────────────────────────────── G5 tiêu đề
def test_g5_chan_chu_rao():
    chan, _ = G.g5_tieu_de(G.cau_hinh(prof()), "60代が気をつけたい習慣かもしれない5選")
    assert any("RÀO" in x for x in chan)


def test_g5_chan_chu_so_dung_mot_minh():
    chan, _ = G.g5_tieu_de(G.cau_hinh(prof()), "定年後の衝撃の末路とは")
    assert any("chữ sợ" in x and "một mình" in x for x in chan)


def test_g5_chu_so_co_con_so_chi_la_canh_bao():
    chan, canh = G.g5_tieu_de(G.cau_hinh(prof()), "退職金2500万円を失った男の末路とは")
    assert not any("chữ sợ" in x for x in chan)
    assert any("chữ sợ" in x for x in canh)


def test_g5_chan_tieu_de_khong_treo_an_so():
    chan, _ = G.g5_tieu_de(G.cau_hinh(prof()), "私は昨日スーパーで牛肉を買って家に帰りました")
    assert any("ẩn số" in x for x in chan)


def test_g5_do_dai_loi_bo_duoi_co_dinh():
    c = G.cau_hinh(prof(title_core_len=[10, 20],
                        title_suffix_ignore=["｜実際の写真をAIフルカラー復元"]))
    chan, _ = G.g5_tieu_de(c, "霧の中に消えた男とは｜実際の写真をAIフルカラー復元")
    assert not any("lõi tiêu đề" in x for x in chan)


# ───────────────────────────────────────────── G6 thumbnail
def test_g6_hai_thumbnail_khong_co_dang_tai_thi_chan(tmp_path):
    d = tap(tmp_path, script="あ")
    (d / "thumbnail_final.png").write_bytes(b"x")
    (d / "thumb_final.png").write_bytes(b"x")
    chan, _ = G.g6_thumbnail(d, G.cau_hinh(prof()), [])
    assert any("KHÔNG có DANG-TAI.txt" in x for x in chan)


def test_g6_dang_tai_chot_dung_mot_file_thi_qua(tmp_path):
    d = tap(tmp_path, script="あ")
    (d / "thumbnail_final.png").write_bytes(b"x")
    (d / "thumb_final.png").write_bytes(b"x")
    (d / "DANG-TAI.txt").write_text("ảnh bìa: thumbnail_final.png", encoding="utf-8")
    chan, canh = G.g6_thumbnail(d, G.cau_hinh(prof()), [])
    assert chan == []
    assert any("đang đăng thumbnail_final.png" in x for x in canh)


# ───────────────────────────────────────────── G8 không chép nhau
def test_g8_bat_hai_tap_cung_lane_chep_cau_cua_nhau(tmp_path):
    p = prof(chep_nhau_max=0.5, chep_nhau_cua_so=300)
    chung = "定年後の朝は静かだ。俺は коfee を淹れながら窓の外を見ていた。あの日のことを思い出す。" * 6
    d1 = tap(tmp_path, script=chung, ten="ep01-a")
    tap(tmp_path, script=chung, ten="ep02-b")
    chan, _ = G.g8_khong_chep_nhau(d1, G.cau_hinh(p), p, chung, "")
    assert any("ep02-b" in x for x in chan)


def test_g8_hai_tap_khac_nhau_thi_khong_bao(tmp_path):
    p = prof(chep_nhau_max=0.5, chep_nhau_cua_so=300)
    a = "定年後の朝は静かだ。" * 15
    b = "図書館の階段を上がると古い紙の匂いがした。" * 15
    d1 = tap(tmp_path, script=a, ten="ep01-a")
    tap(tmp_path, script=b, ten="ep02-b")
    assert G.g8_khong_chep_nhau(d1, G.cau_hinh(p), p, a, "")[0] == []


# ───────────────────────────────────────────── G1 + tổng thể
def test_g1_thieu_promise_thi_chan(tmp_path):
    p = prof()
    sc = "あ" * 200
    d = tap(tmp_path, script=sc)
    chan, _, _ = G.g1_mot_loi_hua(d, G.cau_hinh(p), moc(d, p, sc), "t", [], "")
    assert any("THIẾU promise.txt" in x for x in chan)


def test_g1_loi_hua_noi_qua_muon_thi_chan(tmp_path):
    p = prof(promise_window_s=45)
    loi = "図書館は定年後で一番贅沢な場所だ"
    sc = "あ" * 900 + loi                              # ≈ giây 180
    d = tap(tmp_path, script=sc, promise=loi, title=loi, thumb=[loi], mo_ta=loi)
    chan, _, _ = G.g1_mot_loi_hua(d, G.cau_hinh(p), moc(d, p, sc), loi, [loi], loi)
    # cổng chỉ ra tới giây bao nhiêu mới đủ, để người sửa biết phải kéo câu nào lên hook
    assert any("45s đầu" in x and "phải tới giây" in x for x in chan)


def test_g1_tieu_de_khong_noi_lai_loi_hua(tmp_path):
    p = prof()
    loi = "図書館は定年後で一番贅沢な場所だ"
    sc = loi + "あ" * 100
    d = tap(tmp_path, script=sc, promise=loi)
    chan, _, _ = G.g1_mot_loi_hua(d, G.cau_hinh(p), moc(d, p, sc), "今日は天気の話をします", [], "")
    assert any("tiêu đề KHÔNG nói lại lời hứa" in x for x in chan)


def test_lane_chua_bat_thi_khong_chan_gi(tmp_path, monkeypatch):
    """Hàng rào bật dần: `goi_dang.enabled` chưa bật → mọi phát hiện hạ xuống cảnh báo."""
    p = prof()
    p["goi_dang"]["enabled"] = False
    monkeypatch.setattr(G.profiles, "load", lambda pid: p)
    d = tap(tmp_path, script="こんにちは、皆さん。" + "あ" * 300, title="天気の話")
    kq = G.kiem(d, "x")
    assert kq["blocking_issues"] == []
    assert kq["status"] == "WARN"
    assert any("sẽ CHẶN khi bật" in w for w in kq["warnings"])


def test_bat_len_thi_chan_that(tmp_path, monkeypatch):
    p = prof()
    monkeypatch.setattr(G.profiles, "load", lambda pid: p)
    d = tap(tmp_path, script="こんにちは、皆さん。" + "あ" * 300, title="天気の話")
    kq = G.kiem(d, "x")
    assert kq["status"] == "FAIL" and kq["blocking_issues"]


def test_khong_co_script_thi_skip(tmp_path, monkeypatch):
    monkeypatch.setattr(G.profiles, "load", lambda pid: prof())
    d = tmp_path / "ep99"
    d.mkdir()
    assert G.kiem(d, "x")["status"] == "SKIPPED"


# ───────────────────────────────────────────── Moc (mốc giây)
def test_moc_dung_srt_that_khi_co(tmp_path):
    p = prof()
    d = tmp_path / "ep01"
    d.mkdir()
    (d / "voice.srt").write_text(
        "1\n00:00:00,000 --> 00:00:05,000\nこんばんは\n\n"
        "2\n00:01:00,000 --> 00:01:05,000\n本当の理由はこれだ\n", encoding="utf-8")
    m = G.Moc(d, p, "こんばんは本当の理由はこれだ")
    assert "voice.srt" in m.nguon()
    assert m.tim("本当の理由")[0] == pytest.approx(60.0)


def test_moc_khong_co_srt_thi_suy_tu_char_rate(tmp_path):
    p = prof()
    d = tmp_path / "ep01"
    d.mkdir()
    sc = "あ" * 300 + "本当の理由"
    m = G.Moc(d, p, sc)                                 # 300 chữ/phút = 5 chữ/giây
    assert m.tim("本当の理由")[0] == pytest.approx(60.0, abs=1.0)


# ───────────────────────────────────────────── G2 hai bậc (chặn vs cảnh báo)
def test_g2_dien_dat_khac_nhung_cung_y_thi_chi_canh_bao(tmp_path):
    """Thumbnail rút gọn ý của script → CẢNH BÁO, không chặn (nếu chặn thì 56/56 tập đều đỏ)."""
    p = prof(ve_phu_canh=0.6)
    sc = "四十年間、看護師として働いてきた私が命がけで教えたことがある。" * 6
    d = tap(tmp_path, script=sc)
    # thumbnail đảo trật tự + rút chữ: không còn là chuỗi con, nhưng mọi chữ đều lấy từ script
    chan, canh = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "", ["看護師として四十年間働いてきた"])
    assert chan == []
    assert any("cùng ý" in x for x in canh)


def test_g2_y_hoan_toan_khac_thi_van_chan(tmp_path):
    p = prof(ve_phu_canh=0.6)
    sc = "図書館の階段を上がると古い紙の匂いがした。" * 10
    d = tap(tmp_path, script=sc)
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "", ["元看護婦が遺した四文字の言葉"])
    assert any("KHÔNG có trong lời đọc" in x for x in chan)


def test_g4_thumb_rank_khai_theo_tung_tap(tmp_path):
    """thumb_rank.txt trong thư mục tập ĐÈ giá trị dự phòng của profile (mỗi tập một hạng khác)."""
    p = prof(list_mode=True, thumb_item_rank=3)
    sc = "あ" * 1200
    d = tap(tmp_path, script=sc)
    (d / "thumb_rank.txt").write_text("1", encoding="utf-8")
    chan, _ = G.g4_danh_sach(d, G.cau_hinh(p), moc(d, p, sc), p, sc, ["この食品"])
    assert any("mục GIỮA" in x for x in chan)


def test_tach_ve_ngat_o_ba_cham_ascii():
    """Tiêu đề thật của toshi/tano dùng '...' ASCII, không phải 「…」."""
    ve = G.tach_ve_tieu_de("テスラの死から61年後...米海軍が撮った76秒の映像")
    assert len(ve) == 2


def test_g5_lane_treo_an_so_bang_con_so_thi_khong_bao():
    """Lane iro: 9/9 tiêu đề kênh mẫu có SỐ và 0/9 có từ hỏi — cờ này tránh báo oan cả lane."""
    c = G.cau_hinh(prof(title_an_so_chap_nhan_so=True))
    chan, _ = G.g5_tieu_de(c, "【アッツ島】守備隊2600名が迎えた19日間")
    assert not any("ẩn số" in x for x in chan)
    c2 = G.cau_hinh(prof(title_an_so_chap_nhan_so=False))
    assert any("ẩn số" in x for x in G.g5_tieu_de(c2, "【アッツ島】守備隊2600名が迎えた19日間")[0])


def test_tach_ve_bo_N_chon_khoi_ve():
    """「5選」 là quy ước đặt tên, số N do G4 đếm mục thật — G2 không phạt lần thứ hai."""
    ve = G.tach_ve_tieu_de("定年後に歩きたい「通行料0円の道」5選")
    assert not any("選" in v for v in ve)
    assert any("通行料0円の道" in v for v in ve)


# ───────────────────────────────────────────── goi_dang_ok.txt (đã đọc tay)
def test_g2_ve_da_doc_tay_thi_ha_xuong_canh_bao(tmp_path):
    p = prof()
    sc = "図書館の階段を上がると古い紙の匂いがした。" * 10
    d = tap(tmp_path, script=sc)
    (d / "goi_dang_ok.txt").write_text(
        "# đã đối chiếu tay 2026-09-23\n元看護婦が遺した四文字の言葉 | script nói cùng ý ở giây 264\n",
        encoding="utf-8")
    chan, canh = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "", ["元看護婦が遺した四文字の言葉"])
    assert chan == []
    assert any("ĐÃ ĐỌC TAY" in x and "giây 264" in x for x in canh)


def test_mien_khong_anh_huong_ve_khac(tmp_path):
    p = prof()
    sc = "図書館の階段を上がると古い紙の匂いがした。" * 10
    d = tap(tmp_path, script=sc)
    (d / "goi_dang_ok.txt").write_text("元看護婦が遺した四文字の言葉 | lý do\n", encoding="utf-8")
    chan, _ = G.g2_loi_hua_giu_duoc(d, G.cau_hinh(p), moc(d, p, sc), "", ["まったく別の約束をした男"])
    assert any("KHÔNG có trong lời đọc" in x for x in chan)


# ═══════════════════════════════ CỔNG THƯỢNG NGUỒN: chặn TRƯỚC KHI VIẾT (anh chốt 2026-09-24)
def _prof_day(hook=None, **kw):
    """Profile đủ điều kiện: hook bật + goi_dang bật + visual_kind video sinh + sfx."""
    p = prof(**kw)
    p["script"]["hook"] = {"enabled": True, "visual": "video_grok",
                           "visual_kind": "video_sinh", "sfx": False, "nhac_nen": True, **(hook or {})}
    p["script"]["the_viet"] = "~/.claude/skills/youtube-kich-ban/market/THE_VIET_STORY.md"
    return p


def test_cong_chan_khi_chua_khai_the_viet(tmp_path):
    """05/10/2026 anh chốt thẻ viết bật mọi lane, cả lane tạo sau — quên khai thì S1L chặn."""
    p = _prof_day()
    del p["script"]["the_viet"]
    d = tap(tmp_path, script="あ" * 100, promise="một câu")
    assert any("script.the_viet" in x for x in G.cong_truoc_khi_viet(d, p))


def test_cong_chan_khi_lane_chua_bat_hook(tmp_path):
    """Luật 'hook bắt buộc mọi tập' chốt 23/09 nhưng 3/6 lane chưa ai bật — đó là lý do có cổng này."""
    p = prof()                                   # goi_dang bật, hook KHÔNG khai
    d = tap(tmp_path, script="あ" * 100, promise="một câu")
    loi = G.cong_truoc_khi_viet(d, p)
    assert any("script.hook.enabled" in x for x in loi)


def test_cong_chan_khi_lane_chua_khai_goi_dang(tmp_path):
    p = _prof_day()
    p["goi_dang"]["enabled"] = False
    d = tap(tmp_path, script="あ" * 100, promise="một câu")
    assert any("goi_dang.enabled" in x for x in G.cong_truoc_khi_viet(d, p))


def test_cong_chan_khi_thieu_promise(tmp_path):
    d = tap(tmp_path, script="あ" * 100)          # không có promise.txt
    loi = G.cong_truoc_khi_viet(d, _prof_day())
    assert any("promise.txt" in x for x in loi)


def test_cong_chan_khi_promise_nhieu_dong(tmp_path):
    d = tap(tmp_path, script="あ" * 100, promise="câu một\ncâu hai")
    assert any("nhiều dòng" in x for x in G.cong_truoc_khi_viet(d, _prof_day()))


def test_cong_cho_qua_khi_du_ba_dieu_kien(tmp_path):
    d = tap(tmp_path, script="あ" * 100, promise="図書館は定年後で一番贅沢な場所だ")
    assert G.cong_truoc_khi_viet(d, _prof_day()) == []


def test_cong_doc_duoc_promise_o_thu_muc_hook_ban_cu(tmp_path):
    d = tap(tmp_path, script="あ" * 100)
    (d / "hook").mkdir()
    (d / "hook" / "promise.txt").write_text("một câu", encoding="utf-8")
    assert G.cong_truoc_khi_viet(d, _prof_day()) == []


# ─────────────── khối luật nhồi vào PROMPT của model VIẾT
def test_khoi_luat_rong_khi_lane_chua_bat(tmp_path):
    p = prof()
    p["goi_dang"]["enabled"] = False
    d = tap(tmp_path, script="あ", promise="x")
    assert G.khoi_luat_cho_prompt(d, p) == "", "lane chưa bật thì prompt phải y hệt trước, không đổi hành vi"


def test_khoi_luat_mang_loi_hua_va_moc_giay(tmp_path):
    p = _prof_day(promise_window_s=45, contradiction_max_s=12, title_core_max_s=36)
    d = tap(tmp_path, script="あ", promise="図書館は定年後で一番贅沢な場所だ")
    t = G.khoi_luat_cho_prompt(d, p)
    assert "図書館は定年後で一番贅沢な場所だ" in t
    assert "45 GIÂY ĐẦU" in t and "HOOK ĐÃ KHOÁ" in t and "12 giây đầu" not in t
    assert "タイトル" in t                        # cấm đọc to chữ tiêu đề
    assert "PHỦ ĐỊNH" in t                       # G2 nói trước cho model


def test_khoi_luat_khong_ep_cau_nghi_thuc(tmp_path):
    p = _prof_day(ritual=["この写真をカラー化してみる"], ritual_max_s=160)
    d = tap(tmp_path, script="あ", promise="x")
    t = G.khoi_luat_cho_prompt(d, p)
    assert "この写真をカラー化してみる" not in t   # 17/10: câu nghi thức không còn ép vào mở đầu


def test_khoi_luat_them_phan_danh_sach_chi_khi_list_mode(tmp_path):
    d = tap(tmp_path, script="あ", promise="x")
    assert "CẤM đọc trước danh sách" not in G.khoi_luat_cho_prompt(d, _prof_day(list_mode=False))
    t = G.khoi_luat_cho_prompt(d, _prof_day(list_mode=True, list_order="countdown"))
    assert "CẤM đọc trước danh sách" in t and "mục số 1 để CUỐI" in t


def test_khoi_luat_im_lang_ve_thu_tu_khi_list_order_auto(tmp_path):
    """Lane tano khai `auto` (kênh mẫu dùng cả 2 kiểu) — cổng G4 bỏ qua phép kiểm thứ tự, nên prompt
    cũng KHÔNG được dặn một kiểu: dặn là dạy model sai một nửa số tập mà cổng không bắt được."""
    d = tap(tmp_path, script="あ", promise="x")
    t = G.khoi_luat_cho_prompt(d, _prof_day(list_mode=True, list_order="auto"))
    assert "CẤM đọc trước danh sách" in t
    assert "mục số 1" not in t.lower()


# ─────────────── luật 2026-09-24: hook = VIDEO SINH + BẮT BUỘC có SFX
def test_cong_chan_khi_hook_khong_phai_video_sinh(tmp_path):
    """Mặc định mọi lane: hook là video sinh Flow/Grok, không còn là video ghép từ ảnh render."""
    d = tap(tmp_path, script="あ" * 100, promise="một câu")
    p = _prof_day(hook={"visual_kind": "anh_tinh"})
    loi = G.cong_truoc_khi_viet(d, p)
    assert any("video_sinh" in x for x in loi)


def test_cong_cho_qua_anh_tinh_khi_co_visual_exception(tmp_path):
    """Ngoại lệ chính danh (toshi/iro bán sự thật có hồ sơ) — nhưng phải khai LÝ DO, không im lặng."""
    d = tap(tmp_path, script="あ" * 100, promise="một câu")
    p = _prof_day(hook={"visual_kind": "anh_tinh",
                        "visual_exception": "kênh bán sự thật có hồ sơ, clip AI phá credits.txt"})
    assert G.cong_truoc_khi_viet(d, p) == []


def test_cong_chan_khi_chua_khai_nhac_nen_hoac_con_sfx_vat_the(tmp_path):
    """01/10/2026: cấm SFX đồ vật; hook phải khai nhac_nen."""
    d = tap(tmp_path, script="あ" * 100, promise="một câu")
    assert any("nhac_nen" in x for x in G.cong_truoc_khi_viet(d, _prof_day(hook={"nhac_nen": False})))
    assert any("CẤM hiệu ứng âm thanh đồ vật" in x for x in G.cong_truoc_khi_viet(d, _prof_day(hook={"sfx": True})))


def test_khoi_luat_dan_dung_hinh_chi_cho_lane_video_sinh(tmp_path):
    """Lane có ngoại lệ ảnh tĩnh KHÔNG được nhận lời dặn 'dựng thành clip' — dặn sai là model viết
    cảnh không có tư liệu thật để dựng."""
    d = tap(tmp_path, script="あ", promise="x")
    assert "VIDEO SINH" in G.khoi_luat_cho_prompt(d, _prof_day())
    p_anh = _prof_day(hook={"visual_kind": "anh_tinh", "visual_exception": "lý do"})
    assert "VIDEO SINH" not in G.khoi_luat_cho_prompt(d, p_anh)


def test_khoi_luat_dan_chi_nhac_nen_khong_tieng_vat_the(tmp_path):
    d = tap(tmp_path, script="あ", promise="x")
    kl = G.khoi_luat_cho_prompt(d, _prof_day())
    assert "NHẠC NỀN" in kl and "KHÔNG có tiếng đồ vật" in kl and "HIỆU ỨNG ÂM THANH" not in kl


def test_moi_lane_that_deu_qua_cong(tmp_path):
    """Nghiệm thu trên profile THẬT: cả 6 lane phải qua được cổng (chỉ thiếu promise.txt là bình
    thường vì đó là file của TỪNG TẬP). Test này bắt được lúc ai đó thêm lane mới mà quên khai field."""
    import profiles as P
    # 05/10/2026: lane A/D/E đã bỏ 29/09; 17/10 bỏ Satori → danh sách = 8 lane đang chạy (router CLAUDE.md)
    for pid in ("teinengo-real", "teinengo-tanoshimi", "teinengo-fuufu", "yakkyoku-sukatto",
                "shakai_no_naze", "teinengo-anaba", "senior_korekara", "kaigo-sukatto"):
        d = tap(tmp_path, script="あ", promise="x", ten=f"ep-{pid}")
        loi = G.cong_truoc_khi_viet(d, P.load(pid))
        assert loi == [], f"{pid}: {loi}"
