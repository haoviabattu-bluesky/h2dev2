"""Test yt_stock.py — cổng giấy phép CC BY + credits. KHÔNG gọi mạng (monkeypatch hết)."""
import json
import sys
import types
from pathlib import Path

import pytest

import yt_stock as YS


def _info(lic, **kw):
    d = {"id": "abc123", "url": "https://www.youtube.com/watch?v=abc123", "title": "Navy 1945",
         "channel": "US National Archives", "channel_url": "", "duration_s": 600, "license": lic}
    d.update(kw)
    return d


# ------------------------------------------------------------------ cổng giấy phép (lý do tồn tại)


def test_la_cc_by_chi_nhan_dung_chuoi():
    assert YS.la_cc_by(_info(YS.LICENSE_CC_BY))
    # None = Giấy phép YouTube tiêu chuẩn (verify thật: yP0Ias0Jcek)
    assert not YS.la_cc_by(_info(None))
    assert not YS.la_cc_by(_info("Creative Commons"))
    assert not YS.la_cc_by(_info("Standard YouTube License"))


@pytest.mark.parametrize("lic", [None, "", "Standard YouTube License", "CC BY", "creative commons attribution license (reuse allowed)"])
def test_tai_tu_choi_khi_khong_phai_cc_by(monkeypatch, tmp_path, lic):
    """Giấy phép sai ⇒ NÉM trước khi tải byte nào: _tai_doan không được gọi, không có manifest."""
    monkeypatch.setattr(YS, "lay_thong_tin", lambda vid, proxy=None: _info(lic))
    def khong_duoc_goi(*a, **kw):
        raise AssertionError("đã tải dù giấy phép không phải CC BY")
    monkeypatch.setattr(YS, "_tai_doan", khong_duoc_goi)
    with pytest.raises(YS.KhongDuocPhep):
        YS.tai("abc123", [(10.0, 20.0)], tmp_path)
    assert not (tmp_path / "manifest.jsonl").exists()
    assert not list(tmp_path.glob("yt_*.mp4"))


def test_tai_tu_choi_khi_khong_ghi_noi_nguon(monkeypatch, tmp_path):
    """CC BY nhưng thiếu tên kênh ⇒ không dựng được credit ⇒ vẫn từ chối (CC BY buộc ghi nguồn)."""
    monkeypatch.setattr(YS, "lay_thong_tin", lambda vid, proxy=None: _info(YS.LICENSE_CC_BY, channel=""))
    monkeypatch.setattr(YS, "_tai_doan", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("đã tải")))
    with pytest.raises(YS.KhongDuocPhep):
        YS.tai("abc123", [(10.0, 20.0)], tmp_path)


def test_tai_cc_by_ghi_manifest_dung_schema(monkeypatch, tmp_path):
    monkeypatch.setattr(YS, "lay_thong_tin", lambda vid, proxy=None: _info(YS.LICENSE_CC_BY))

    def fake_tai_doan(vid, a, b, tho, proxy=None, **kw):
        f = Path(str(tho) + ".webm")
        f.write_bytes(b"x" * 20_000)
        return f

    def fake_chuan_hoa(src, dest, crop_bottom=0.0, fps=30):
        Path(dest).write_bytes(b"y" * 30_000)

    monkeypatch.setattr(YS, "_tai_doan", fake_tai_doan)
    monkeypatch.setattr(YS, "_chuan_hoa", fake_chuan_hoa)
    recs = YS.tai("abc123", [(120.0, 128.0), (300.0, 306.0)], tmp_path,
                  chapter=2, crop_bottom=0.17, query="navy 1945")
    assert [r["file"] for r in recs] == ["yt_abc123_01.mp4", "yt_abc123_02.mp4"]
    lines = [json.loads(l) for l in (tmp_path / "manifest.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == 2
    r = lines[0]
    for k in ("src", "id", "url", "title", "duration_s", "license", "credit", "query", "chapter"):
        assert k in r, f"manifest thiếu field {k} (schema stock_cut đang đọc)"
    assert r["src"] == "youtube_cc" and r["license"] == YS.LICENSE_CC_BY
    assert "US National Archives" in r["credit"] and r["url"] in r["credit"]
    assert r["duration_s"] == 8.0 and r["chapter"] == "2"
    # file tạm phải dọn sạch, không để rác trong kho stock
    assert not list(tmp_path.glob(".tmp_yt_*"))


def test_tai_bo_qua_doan_hong_van_giu_doan_tot(monkeypatch, tmp_path):
    monkeypatch.setattr(YS, "lay_thong_tin", lambda vid, proxy=None: _info(YS.LICENSE_CC_BY))
    monkeypatch.setattr(YS, "_tai_doan", lambda vid, a, b, tho, proxy=None, **kw:
                        None if a == 120.0 else Path(str(tho) + ".mp4"))
    monkeypatch.setattr(YS, "_chuan_hoa", lambda src, dest, crop_bottom=0.0, fps=30:
                        Path(dest).write_bytes(b"z" * 12_000))
    recs = YS.tai("abc123", [(120.0, 128.0), (300.0, 306.0)], tmp_path)
    assert [r["file"] for r in recs] == ["yt_abc123_02.mp4"]


# ------------------------------------------------------------------ tìm


def test_tim_kiem_lai_tung_video_va_danh_dau(monkeypatch):
    fake = types.SimpleNamespace(YoutubeDL=None)

    class _YDL:
        def __init__(self, opts): self.opts = opts
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def extract_info(self, url, download=False):
            # extract_flat: KHÔNG có license → đây chính là lý do phải tra lần hai
            return {"entries": [{"id": "ok1", "title": "A"}, {"id": "no1", "title": "B"}]}

    fake.YoutubeDL = _YDL
    monkeypatch.setitem(sys.modules, "yt_dlp", fake)
    monkeypatch.setattr(YS, "lay_thong_tin", lambda vid, proxy=None:
                        _info(YS.LICENSE_CC_BY if vid == "ok1" else None, id=vid))
    kq = YS.tim("navy 1945", n=2, nghi=0)
    assert [r["ok"] for r in kq] == [True, False]
    assert "KHÔNG tải" in kq[1]["ly_do"]


def test_doc_ranges():
    assert YS.doc_ranges("120-128,300-306") == [(120.0, 128.0), (300.0, 306.0)]
    assert YS.doc_ranges("2:00-2:08") == [(120.0, 128.0)]
    for xau in ("", "120", "128-120", "a-b"):
        with pytest.raises(ValueError):
            YS.doc_ranges(xau)


# ------------------------------------------------------------------ credits (lỗi ghi sai nguồn)


def _kho(tmp_path):
    tap = tmp_path / "ep05"
    stock = tap / "stock"
    stock.mkdir(parents=True)
    recs = [
        {"file": "pexels_1.mp4", "src": "pexels", "title": "sunset over ocean 1",
         "credit": "Manav .", "license": "Pexels License"},
        {"file": "ev01.jpg", "src": "evidence", "credit": "https://commons.wikimedia.org/wiki/File:TBM.jpg",
         "license": "Public domain", "caption": "アヴェンジャー雷撃機（1945年撮影）"},
    ]
    (stock / "manifest.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    return tap, stock


def test_viet_credits_lay_nguon_tu_manifest_khong_muon_cua_canh_cu(tmp_path):
    """Lỗi thật ep05: cảnh bằng chứng ev01 mang title/credit của clip Pexels nó thay thế."""
    tap, _ = _kho(tmp_path)
    scenes = [
        {"i": 0, "file": "pexels_1.mp4", "title": "sunset over ocean 1", "credit": "Manav .",
         "license": "Pexels License"},
        # scene ghi SAI (di sản của bug cũ) — credits.txt phải sửa lại theo manifest
        {"i": 1, "file": "ev01.jpg", "title": "sunset over ocean 1", "credit": "Manav .",
         "license": "Public domain", "bangchung": True},
    ]
    (tap / "scenes.json").write_text(json.dumps(scenes, ensure_ascii=False), encoding="utf-8")
    kq = YS.viet_credits(tap)
    txt = (tap / "credits.txt").read_text(encoding="utf-8")
    assert kq["n_nguon"] == 2 and not kq["thieu_manifest"]
    dong_ev = [l for l in txt.splitlines() if "ev01.jpg" in l][0]
    assert "Manav" not in dong_ev and "sunset" not in dong_ev
    assert "アヴェンジャー" in dong_ev and "commons.wikimedia.org" in dong_ev
    assert "[Public domain]" in dong_ev


def test_viet_credits_bao_file_ngoai_so(tmp_path):
    tap, _ = _kho(tmp_path)
    scenes = [{"i": 0, "file": "la_hoac.mp4", "title": "?", "credit": "", "license": "?"},
              {"i": 1, "file": "001.png", "anh_ai": True, "title": "AI生成イメージ — x",
               "credit": "AI生成イメージ", "license": "ai-generated"}]
    (tap / "scenes.json").write_text(json.dumps(scenes, ensure_ascii=False), encoding="utf-8")
    kq = YS.viet_credits(tap)
    assert kq["thieu_manifest"] == ["la_hoac.mp4"]      # ảnh AI không bị tính là thiếu sổ


# ------------------------------------------------------------------ vá stock_cut.gan_bang_chung


def test_gan_bang_chung_khong_muon_title_cua_canh_bi_thay(tmp_path):
    import stock_cut
    stock = tmp_path / "stock"
    stock.mkdir()
    (stock / "ev01.jpg").write_bytes(b"i" * 100)
    (stock / "manifest.jsonl").write_text(json.dumps(
        {"file": "ev01.jpg", "src": "evidence", "license": "Public domain",
         "credit": "https://commons.wikimedia.org/wiki/File:TBM.jpg",
         "caption": "アヴェンジャー雷撃機"}, ensure_ascii=False) + "\n", encoding="utf-8")
    ke_hoach = [{"i": 0, "t0": 10.0, "dur": 5.0, "kieu": "video", "file": "pexels_1.mp4",
                 "vao": 0.0, "license": "Pexels License", "credit": "Manav .",
                 "title": "sunset over ocean 1"}]
    stock_cut.gan_bang_chung(ke_hoach, [{"at": 11.0, "file": "ev01.jpg", "sec": 3.0,
                                         "caption": "アヴェンジャー雷撃機"}], stock, chinh_sach="pd")
    c = ke_hoach[0]
    assert c["bangchung"] and c["file"] == "ev01.jpg"
    assert c["title"] == "アヴェンジャー雷撃機"          # KHÔNG phải "sunset over ocean 1"
    assert c["credit"].startswith("https://commons.wikimedia.org")   # KHÔNG phải "Manav ."
    assert c["license"] == "Public domain"


def test_viet_credits_lui_ve_caption_trong_evidence_json(tmp_path):
    """Manifest src='commons' không có title lẫn caption → lấy caption từ evidence.json của tập,
    KHÔNG tụt xuống tên file, và tuyệt đối không mượn title của scene (đó là title đã bị gán nhầm)."""
    tap = tmp_path / "ep01"
    stock = tap / "stock"
    stock.mkdir(parents=True)
    (stock / "manifest.jsonl").write_text(json.dumps(
        {"file": "ev03c.jpg", "src": "commons", "license": "Public domain",
         "credit": "Senior Airman Timothy Tweet"}, ensure_ascii=False) + "\n", encoding="utf-8")
    (tap / "evidence.json").write_text(json.dumps(
        [{"file": "ev03c.jpg", "caption": "セスナ182 同型機の参考写真"}], ensure_ascii=False), encoding="utf-8")
    (tap / "scenes.json").write_text(json.dumps(
        [{"i": 0, "file": "ev03c.jpg", "title": "canadian snowbirds jet on runway 28924896",
          "credit": "Pexels ai đó", "license": "Public domain", "bangchung": True}],
        ensure_ascii=False), encoding="utf-8")
    YS.viet_credits(tap)
    dong = (tap / "credits.txt").read_text(encoding="utf-8").splitlines()[-1]
    assert "セスナ182" in dong and "snowbirds" not in dong and "ev03c.jpg —" not in dong
    assert "Timothy Tweet" in dong


def test_thu_client_doi_thu_tu_va_format_mac_dinh():
    """--clients đổi được thứ tự player_client; client lạ vẫn có format mặc định để thử."""
    assert YS._thu_client("") == YS.TAI_THU
    t = YS._thu_client("tv_embedded,android")
    assert [c for c, _ in t] == ["tv_embedded", "android"]
    assert t[0][1] == YS.FMT_MAC_DINH and t[1][1] == dict(YS.TAI_THU)["android"]


def test_viet_credits_gop_ca_tu_lieu_cua_hook(tmp_path):
    """Tư liệu dùng trong hook 20–30s đầu KHÔNG nằm trong scenes.json — vẫn phải có trong credits,
    nếu không là thiếu ghi nguồn cho CC BY (vi phạm giấy phép)."""
    tap, stock = _kho(tmp_path)
    (stock / "manifest.jsonl").open("a", encoding="utf-8").write(json.dumps(
        {"file": "yt_abc_01.mp4", "src": "youtube_cc", "title": "STORY OF NAVAL AVIATION",
         "credit": "PublicResourceOrg · https://www.youtube.com/watch?v=abc",
         "license": YS.LICENSE_CC_BY}, ensure_ascii=False) + "\n")
    (tap / "scenes.json").write_text(json.dumps(
        [{"i": 0, "file": "pexels_1.mp4", "title": "sunset over ocean 1", "credit": "Manav .",
          "license": "Pexels License"}], ensure_ascii=False), encoding="utf-8")
    (tap / "hook").mkdir()
    (tap / "hook" / "hook_shots.json").write_text(json.dumps(
        [{"file": "yt_abc_01.mp4", "n": 2}], ensure_ascii=False), encoding="utf-8")
    kq = YS.viet_credits(tap)
    txt = (tap / "credits.txt").read_text(encoding="utf-8")
    assert kq["n_nguon"] == 2 and "STORY OF NAVAL AVIATION" in txt
    assert "PublicResourceOrg" in txt and "(2 cảnh · yt_abc_01.mp4)" in txt


def test_viet_credits_credit_xuong_dong_khong_lam_vo_dong(tmp_path):
    """Credit của Commons có thể chứa xuống dòng → phải ép về 1 dòng, kẻo dòng nguồn vỡ làm đôi."""
    tap, stock = _kho(tmp_path)
    (stock / "manifest.jsonl").open("a", encoding="utf-8").write(json.dumps(
        {"file": "map.png", "src": "commons", "title": "Flight 19 raster map",
         "credit": "NASA, Landsat image\n\nModified by Marikanto", "license": "Public domain"},
        ensure_ascii=False) + "\n")
    (tap / "scenes.json").write_text(json.dumps([{"i": 0, "file": "map.png"}], ensure_ascii=False),
                                     encoding="utf-8")
    YS.viet_credits(tap)
    dong = [l for l in (tap / "credits.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(dong) == 2                      # tiêu đề + đúng 1 dòng nguồn
    assert "Modified by Marikanto" in dong[1] and dong[1].startswith("- ")
