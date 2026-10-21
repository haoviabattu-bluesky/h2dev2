import json
from pathlib import Path
import pytest
import fetch_script as FS


@pytest.fixture(autouse=True)
def _chan_llm_that_khi_tach_suon(monkeypatch):
    """2026-10-17: phan_tich_nguon/ensure_locked nay gọi phan_tich_cau_truc (claude -p → Gemini). Test KHÔNG được gọi model
    thật — mặc định cả 2 đường ném lỗi (phan_tich_cau_truc trả None); test nào cần thì tự monkeypatch đè lên."""
    import claude_p_bridge, llm_client

    def _cam(*a, **k):
        raise RuntimeError("test: cấm gọi model thật")
    monkeypatch.setattr(claude_p_bridge, "ask", _cam)
    monkeypatch.setattr(llm_client, "chat", _cam)


class _FakeYDL:
    def __init__(self, opts): self.opts = opts
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def extract_info(self, url, download=False):
        return {"id": "abc123XYZ00", "title": "T", "description": "D\nline2",
                "thumbnail": "https://i.ytimg.com/vi/abc123XYZ00/maxresdefault.jpg", "duration": 1500}


def test_lay_meta_video(monkeypatch):
    import types, sys
    fake = types.SimpleNamespace(YoutubeDL=_FakeYDL)
    monkeypatch.setitem(sys.modules, "yt_dlp", fake)
    m = FS.lay_meta_video("https://www.youtube.com/watch?v=abc123XYZ00")
    assert m["video_id"] == "abc123XYZ00" and m["title"] == "T"
    assert m["description"].startswith("D") and m["thumbnail_url"].endswith(".jpg")
    assert m["duration_sec"] == 1500


def test_lay_meta_video_loi_khong_nem(monkeypatch):
    """Task 1b (2026-09-23): lay_meta_video giờ có fallback đọc HTML khi yt_dlp chết — test này
    phải mock LUÔN đường fallback (yt_tags._get) để không gọi mạng thật, giữ đúng kỳ vọng gốc
    của Task 1 (cả 2 đường đều thất bại → title rỗng, duration 0, KHÔNG ném exception)."""
    import types, sys
    import yt_tags
    class Boom(_FakeYDL):
        def extract_info(self, url, download=False): raise RuntimeError("net")
    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=Boom))
    def boom_get(*a, **kw): raise RuntimeError("net html")
    monkeypatch.setattr(yt_tags, "_get", boom_get)
    m = FS.lay_meta_video("abc123XYZ00")
    assert m["title"] == "" and m["duration_sec"] == 0
    # điểm vá số 1: thumbnail_url mặc định (maxresdefault suy từ video_id) phải CÒN dù cả 2 đường lỗi
    assert m["thumbnail_url"] == "https://i.ytimg.com/vi/abc123XYZ00/maxresdefault.jpg"


def test_lay_meta_video_yt_dlp_loi_fallback_html_thanh_cong(monkeypatch):
    """Task 1b: yt_dlp bị chặn bot (DownloadError giống bằng chứng thật 2026-09-23) nhưng fallback
    đọc HTML trang watch (yt_tags) vẫn lấy được title/description → không còn rỗng."""
    import types, sys
    import yt_tags
    class Boom(_FakeYDL):
        def extract_info(self, url, download=False):
            raise RuntimeError("Sign in to confirm you're not a bot")
    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=Boom))
    fake_html = "<html>...</html>"
    monkeypatch.setattr(yt_tags, "_get", lambda *a, **kw: fake_html)
    fake_data = {"videoDetails": {"title": "Tiêu đề thật", "shortDescription": "Mô tả thật",
                                   "lengthSeconds": "1234"}}
    monkeypatch.setattr(yt_tags, "_extract_json_var", lambda html, var: fake_data)
    m = FS.lay_meta_video("abc123XYZ00")
    assert m["title"] == "Tiêu đề thật"
    assert m["description"] == "Mô tả thật"
    assert m["duration_sec"] == 1234
    # thumbnail_url vẫn là maxresdefault suy từ video_id (yt_tags không có field ảnh bìa)
    assert m["thumbnail_url"] == "https://i.ytimg.com/vi/abc123XYZ00/maxresdefault.jpg"


def test_lay_meta_video_thumbnail_mac_dinh_truoc_try():
    """Task 1b điểm vá số 1 (đóng chốt riêng, không phụ thuộc mock nào): thumbnail_url mặc định
    phải suy ra được từ video_id kể cả khi module yt_dlp không hề tồn tại trong môi trường —
    chứng minh giá trị này nằm NGOÀI khối try/except, không phải sản phẩm phụ của 1 lần gọi mạng
    thành công nào."""
    import builtins
    orig = builtins.__import__
    def fake_import(name, *a, **kw):
        if name in ("yt_dlp", "yt_tags"):
            raise ImportError(f"{name} không có trong môi trường test này")
        return orig(name, *a, **kw)
    builtins.__import__ = fake_import
    try:
        m = FS.lay_meta_video("abc123XYZ00")
    finally:
        builtins.__import__ = orig
    assert m["thumbnail_url"] == "https://i.ytimg.com/vi/abc123XYZ00/maxresdefault.jpg"
    assert m["title"] == "" and m["duration_sec"] == 0


def test_lay_meta_video_cookie_file(monkeypatch, tmp_path):
    """Task 1b điểm vá số 2: YTDLP_COOKIES phải được gắn vào opts của yt_dlp.YoutubeDL, giống hệt
    cơ chế via_ytdlp_subs đã có (đo thật: đường transcript sống nhờ cookie, đường meta thì không)."""
    import types, sys
    captured = {}
    class _CapturingYDL(_FakeYDL):
        def __init__(self, opts):
            captured.update(opts)
            super().__init__(opts)
    monkeypatch.setenv("YTDLP_COOKIES", str(tmp_path / "cookies.txt"))
    monkeypatch.delenv("YTDLP_COOKIES_BROWSER", raising=False)
    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=_CapturingYDL))
    FS.lay_meta_video("abc123XYZ00")
    assert captured["cookiefile"] == str(tmp_path / "cookies.txt")


def test_lay_meta_video_cookie_browser(monkeypatch):
    """Task 1b điểm vá số 2, nhánh YTDLP_COOKIES_BROWSER (đọc cookie thẳng từ trình duyệt đang mở)."""
    import types, sys
    captured = {}
    class _CapturingYDL(_FakeYDL):
        def __init__(self, opts):
            captured.update(opts)
            super().__init__(opts)
    monkeypatch.delenv("YTDLP_COOKIES", raising=False)
    monkeypatch.setenv("YTDLP_COOKIES_BROWSER", "chrome")
    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=_CapturingYDL))
    FS.lay_meta_video("abc123XYZ00")
    assert captured["cookiesfrombrowser"] == ("chrome",)


def test_tai_anh_ghi_file(monkeypatch, tmp_path):
    import requests
    class FakeResponse:
        status_code = 200
        content = b"x" * 3000
    monkeypatch.setattr(requests, "get", lambda *a, **kw: FakeResponse())
    out_file = tmp_path / "t.jpg"
    result = FS.tai_anh("http://x/t.jpg", out_file)
    assert result is True
    assert out_file.exists()
    assert out_file.read_bytes() == b"x" * 3000


def test_tai_anh_that_bai_tra_false(monkeypatch, tmp_path):
    import requests
    # Case (a): status_code = 404
    class FakeResponse404:
        status_code = 404
        content = b"not found"
    monkeypatch.setattr(requests, "get", lambda *a, **kw: FakeResponse404())
    out_file = tmp_path / "t404.jpg"
    result = FS.tai_anh("http://x/t404.jpg", out_file)
    assert result is False
    assert not out_file.exists()

    # Case (b): requests.get ném RuntimeError
    def fake_get_boom(*a, **kw):
        raise RuntimeError("net")
    monkeypatch.setattr(requests, "get", fake_get_boom)
    out_file2 = tmp_path / "t_boom.jpg"
    result2 = FS.tai_anh("http://x/t_boom.jpg", out_file2)
    assert result2 is False
    assert not out_file2.exists()


def test_crawl_transcripts_luu_segments_meta(monkeypatch, tmp_path):
    import channel_analyzer as CA
    monkeypatch.setattr(FS, "fetch_any", lambda vid, langs, proxy=None: (
        [{"start": 0.0, "duration": 10, "text": "A"}, {"start": 12.0, "duration": 10, "text": "B"},
         {"start": 40.0, "duration": 10, "text": "C"}], "api"))
    monkeypatch.setattr(FS, "lay_meta_video", lambda vid, proxy=None: {
        "video_id": vid, "title": "T", "description": "DESC", "thumbnail_url": "http://x/t.jpg", "duration_sec": 100})
    monkeypatch.setattr(FS, "tai_anh", lambda url, p, proxy=None: Path(p).write_bytes(b"x" * 3000) or True)
    rows = [{"id": "v1", "title": "T", "view_count": 500, "duration": 100}]
    out = CA.crawl_transcripts(rows, ["ja"], tmp_path)
    assert out[0]["description"] == "DESC" and out[0]["dau_0_30s"] == "A B"
    assert (tmp_path / "_raw/segments/v1.json").exists()
    assert (tmp_path / "_raw/meta/v1.json").exists()
    assert (tmp_path / "_raw/thumbs/01_500_v1.jpg").exists()


def test_video_prompt_co_khoi_hook():
    import channel_analyzer as CA
    for k in ("hook_0_30s", "hook_4_nhip", "hook_kind", "hook_score_0_12", "promise_match", "{description}", "{dau_0_30s}"):
        assert k in CA.VIDEO_PROMPT


# Task 3: hook_stage phép đo tất định
import hook_stage as HS

PROF = {"id": "x", "language": "ja", "voice": {"char_rate": 300.0}, "script": {}}


def test_so_chu_muc_tieu_va_cau_hinh():
    assert HS.so_chu_muc_tieu(PROF) == 150
    p2 = {**PROF, "script": {"hook": {"giay_mac_dinh": 24, "giay": [15, 90], "banned_openers": ["X"]}}}
    assert HS.so_chu_muc_tieu(p2) == 120 and HS.cau_hinh(p2)["banned_openers"] == ["X"]
    # 2026-10-21: độ dài = đúng giây kết hook của video gốc (không kẹp theo script.hook.giay), chỉ sàn 6s / trần 150s
    assert HS.so_chu_muc_tieu(p2, {"cau_truc_hook": {"giay_ket_hook": "60-64"}}) == 320
    assert HS.so_chu_muc_tieu(p2, {"cau_truc_hook": {"giay_ket_hook": 120}}) == 600
    assert HS.so_chu_muc_tieu(p2, {"cau_truc_hook": {"giay_ket_hook": 300}}) == 750
    assert HS.so_chu_muc_tieu(p2, {"cau_truc_hook": {"giay_ket_hook": 3}}) == 30
    # không có hook gốc → giay_mac_dinh kẹp trong script.hook.giay
    assert HS.so_chu_muc_tieu({**PROF, "script": {"hook": {"giay_mac_dinh": 5, "giay": [15, 90]}}}) == 75


def test_cat_0_30s():
    segs = [{"start": 0, "text": "あ"}, {"start": 29.9, "text": "い"}, {"start": 30.0, "text": "う"}]
    assert HS.cat_0_30s(segs) == "あ い"


def test_tach_candidates():
    t = "=== HOOK 1 ===\n一\n=== HOOK 2 ===\n二\n三\n=== HOOK 3 ===\n四"
    assert HS.tach_candidates(t) == ["一", "二\n三", "四"]


def test_check_bat_loi():
    ngan = "短い。"
    assert any("độ dài" in v for v in HS.check(ngan, PROF))
    cta = "チャンネル登録お願いします。" + "あ" * 140
    assert any("đăng ký" in v for v in HS.check(cta, PROF))
    # 2026-10-17: bỏ luật cấm chào hỏi/đòi neo cụ thể — mở kiểu nào là theo hook video gốc
    assert HS.check("皆さんは、何歳で結婚しましたか。" + "あ" * 135, PROF) == []
    assert any("độ dài" in v for v in HS.check("あ" * 150, PROF, muc=400))


def test_check_dat():
    ok = "「三年前に引っ越しました」と隣人は言った。五十年の友が消えていた。私はその理由を知らずにいた。多くの問題があった。しかし、それはすぐに明らかになった。家族の事情が複雑だった。誰もが苦しんでいた。これが人生なのだと感じた。時間は止まらない。結局、私たちは皆同じ道を歩いているのだ。"
    ok = ok[:139]
    assert HS.check(ok, PROF) == []


def test_bat_dau_va_ke_lai():
    hook = "「三年前に引っ越しました」隣人は言った。五十年の友が消えた。"
    script = hook + "\n\n私は箱を抱えたまま立ち尽くした。"
    assert HS.bat_dau_bang_hook(script, hook)
    assert not HS.bat_dau_bang_hook("晩秋の風が。" + script, hook)
    assert HS.ke_lai_hook(hook + "\n\n" + hook, hook) > 0.8
    assert HS.ke_lai_hook(script, hook) < 0.3


# Task 4: LOCK + promise snapshot + HOOK_STALE
def _tap(tmp_path, title="T1", ctx="[D1] x\n", thumb="A|B"):
    d = tmp_path
    (d / "title.txt").write_text(title, encoding="utf-8")
    (d / "series_ctx.txt").write_text(ctx, encoding="utf-8")
    (d / "thumb_text.txt").write_text(thumb, encoding="utf-8")
    return d


def test_khoa_va_stale(tmp_path):
    d = _tap(tmp_path)
    meta = HS.khoa(d, "hook文。", mode="upstream")
    assert (d / "hook/hook_locked.txt").read_text(encoding="utf-8") == "hook文。\n"
    assert meta["stale"] is False and len(meta["sha256"]) == 64 and meta["promise"]["title"] == "T1"
    assert HS.kiem_stale(d) == (False, [])
    (d / "title.txt").write_text("T2", encoding="utf-8")
    stale, ly_do = HS.kiem_stale(d)
    assert stale and any("title" in r for r in ly_do)


def test_stale_theo_promise_txt(tmp_path):
    d = _tap(tmp_path)
    (d / "hook").mkdir()
    (d / "hook/promise.txt").write_text("core_event: A\npayoff: B\n", encoding="utf-8")
    HS.khoa(d, "hook文。")
    (d / "series_ctx.txt").write_text("[D1] sửa chính tả\n", encoding="utf-8")   # ctx đổi nhưng promise.txt không
    assert HS.kiem_stale(d) == (False, [])
    (d / "hook/promise.txt").write_text("core_event: KHÁC\n", encoding="utf-8")
    assert HS.kiem_stale(d)[0]


def test_stale_hook_sua_tay(tmp_path):
    d = _tap(tmp_path)
    HS.khoa(d, "hook文。")
    (d / "hook/hook_locked.txt").write_text("đổi", encoding="utf-8")
    stale, ly_do = HS.kiem_stale(d)
    assert stale and any("hook_locked.txt" in r for r in ly_do)


def test_chua_co_lock(tmp_path):
    assert HS.kiem_stale(tmp_path) == (False, ["chưa có hook lock"])


def test_phan_tich_nguon(monkeypatch, tmp_path):
    """2026-10-21: H1–H3 = lời 0–150s + khung hình + CẤU TRÚC hook gốc (phan_tich_cau_truc) ghi vào hook/source.json."""
    d = tmp_path
    (d / "competitor.segments.json").write_text(json.dumps({
        "video_id": "vid1", "title": "T", "description": "D", "thumbnail_url": "http://x/t.jpg",
        "segments": [{"start": 0, "duration": 5, "text": "「三年前に引っ越しました」"}, {"start": 31, "duration": 5, "text": "後半"},
                     {"start": 120, "duration": 5, "text": "百二十秒"}, {"start": 160, "duration": 5, "text": "ngoài cửa sổ"}]}),
        encoding="utf-8")
    import claude_p_bridge
    goi = {}

    def fake_ask(prompt, **k):
        goi["prompt"] = prompt
        return type("R", (), {"text": json.dumps({
            "mo_dau": "câu thoại", "giay_ket_hook": 64,
            "nhip": [{"tu": 0, "den": 5, "vai_tro": "câu sốc", "cach_lam": "thoại", "cau_goc": "三年前", "dich": "3 năm trước"}],
            "giu_chan_bang": "câu hỏi"})})()
    monkeypatch.setattr(claude_p_bridge, "ask", fake_ask)
    monkeypatch.setattr(HS, "khung_hinh_0_30s", lambda vid, out, n=6, proxy=None: None)
    monkeypatch.setattr(FS, "tai_anh", lambda url, p, proxy=None: False)
    src = HS.phan_tich_nguon(d, PROF)
    assert src["transcript_0_30s"] == "「三年前に引っ越しました」"
    assert "百二十秒" in src["transcript_hook"] and "ngoài cửa sổ" not in src["transcript_hook"]
    assert "百二十秒" in goi["prompt"]
    luu = json.loads((d / "hook/source.json").read_text(encoding="utf-8"))
    assert luu["cau_truc_hook"]["mo_dau"] == "câu thoại" and src["video_hook_verdict"] == "khong_soi_duoc"
    # 2026-10-21: prompt tách cấu trúc KHÔNG còn phân loại động cơ / khuôn lane
    assert "CAO_TRAO" not in goi["prompt"] and "khuon_lane" not in goi["prompt"]
    assert HS.so_chu_muc_tieu(PROF, luu) == 320   # 300 chữ/phút × 64s
    assert "CẤU TRÚC HOOK VIDEO GỐC" in HS.khoi_suon(d, luu) and "câu sốc" in HS.khoi_suon(d, luu)
    assert "động cơ" not in HS.khoi_suon(d, luu)


@pytest.mark.cong_hook_goc
def test_phan_tich_cau_truc_json_hong_tra_none(tmp_path, monkeypatch):
    import claude_p_bridge
    monkeypatch.setattr(claude_p_bridge, "ask", lambda prompt, **k: type("R", (), {"text": "không phải json"})())
    assert HS.phan_tich_cau_truc(tmp_path, PROF, {"transcript_hook": "[0]あ"}) is None
    with pytest.raises(SystemExit):          # 21/10: nhánh viết hook tự do đã bỏ
        HS.khoi_suon(tmp_path, {})


# 2026-10-21 (Lane L ep23 佐野稔): không có hook gốc → cấm viết/khoá hook; họ nhân vật tập trước bị chặn.
@pytest.mark.cong_hook_goc
def test_ensure_locked_khong_hook_goc_thi_chan(monkeypatch, tmp_path):
    d = _tap(tmp_path)
    monkeypatch.setattr(HS, "phan_tich_nguon", lambda *a, **k: {"video_id": "kKzleVgzGso", "transcript_0_30s": "", "title": ""})
    def _cam(*a, **k):
        raise AssertionError("không được viết hook khi thiếu hook gốc")
    monkeypatch.setattr(ai_steps, "_writer_chat", _cam)
    with pytest.raises(SystemExit) as e:
        HS.ensure_locked(d, PROF)
    assert "KHÔNG CÓ CẤU TRÚC HOOK GỐC" in str(e.value)
    assert json.loads((d / "hook/hook_qc.json").read_text(encoding="utf-8"))["state"] == "NO_HOOK_GOC"
    assert not (d / "hook/hook_lock.json").exists()


@pytest.mark.cong_hook_goc
def test_khoa_tay_khong_co_cau_truc_bi_chan(tmp_path):
    d = _tap(tmp_path)
    with pytest.raises(SystemExit):
        HS.khoa(d, "hook文。", extra={"source": "may1_tay"})
    (d / "hook").mkdir(exist_ok=True)
    (d / "hook/source.json").write_text(json.dumps({"cau_truc_hook": {"nhip": [{"tu": 0}, {"tu": 5}]}}), encoding="utf-8")
    assert HS.khoa(d, "hook文。")["so_nhip_goc"] == 2


def test_check_chan_ho_tap_truoc(tmp_path):
    import kiem_hook_goc as K
    sd = tmp_path / "lane"
    for ep, ten in (("ep04-a", "佐野 健二"), ("ep05-b", "さくら"), ("ep06-c", "さくら"), ("ep07-d", "さくら")):
        (sd / ep).mkdir(parents=True)
        (sd / ep / "characters.json").write_text(json.dumps({"characters": [{"name": ten}]}, ensure_ascii=False),
                                                 encoding="utf-8")
    (sd / "ep23-x").mkdir()
    cam = K.ho_da_dung(sd / "ep23-x")
    assert cam == {"佐野": ["ep04"]}          # さくら toàn kana + vai cố định → không cấm
    v = HS.check("佐野稔、五十一歳。", PROF, muc=len("佐野稔五十一歳"), cam_ho=cam)
    assert any("佐野" in x for x in v)
    assert not any("họ" in x for x in HS.check("川西稔、五十一歳。", PROF, muc=len("川西稔五十一歳"), cam_ho=cam))


def test_danh_gia_loi_goc():
    import kiem_hook_goc as K
    assert not K.danh_gia([])[0]
    assert not K.danh_gia([{"start": 40, "duration": 3, "text": "あ"}] * 6)[0]          # bắt đầu muộn
    assert K.danh_gia([{"start": i * 6.0, "duration": 5, "text": "あ"} for i in range(8)])[0]
    assert K.id_video(None, "xem https://www.youtube.com/watch?v=kKzleVgzGso nhé") == "kKzleVgzGso"


def test_cau_truc_cu_17_10_van_doc_duoc(tmp_path):
    """source.json tách theo luật 17/10 (còn dong_co_chinh/khuon_lane) vẫn dùng được; khối cấu trúc bỏ 2 trường đó."""
    ct = {"dong_co_chinh": "CAO_TRAO", "khuon_lane": "O-B", "mo_dau": "thoai", "giay_ket_hook": 20,
          "nhip": [{"tu": 0, "den": 5, "vai_tro": "mở", "cach_lam": "thoại"}]}
    k = HS.khoi_suon(tmp_path, {"cau_truc_hook": ct})
    assert "CAO_TRAO" not in k and "O-B" not in k and "mở" in k
    assert HS.phan_tich_cau_truc(tmp_path, PROF, {"cau_truc_hook": ct}) is ct


def test_prompt_viet_khong_con_luat_hook_cu():
    assert "LUẬT DUY NHẤT (anh chốt 2026-10-21)" in HS.PROMPT_VIET
    for cu in ("ĐỘNG CƠ CHÍNH", "HƯỚNG DẪN CẤU TRÚC HOOK CỦA LANE", "{huong_dan}", "KHÔNG được thêm/bớt/đảo nhịp"):
        assert cu not in HS.PROMPT_VIET
    assert not hasattr(HS, "doc_huong_dan") and "huong_dan_cau_truc" not in HS.MAC_DINH


def test_phan_tich_nguon_khong_co_nguon(tmp_path):
    src = HS.phan_tich_nguon(tmp_path, PROF)
    assert src["video_id"] is None and src["video_hook_verdict"] == "khong_soi_duoc"


# Vá sau review Task 5 (2026-09-23): V1 nguon_cua_tap không ném khi JSON hỏng, V2 bọc lay_meta_video/
# tai_anh, V3 mkdir(parents=True), V4 khung_hinh_0_30s thử lại đổi player_client.

def test_nguon_cua_tap_json_hong_khong_nem(tmp_path):
    (tmp_path / "competitor.segments.json").write_text("{broken", encoding="utf-8")
    assert HS.nguon_cua_tap(tmp_path) is None


def test_phan_tich_nguon_lay_meta_nem_van_ghi_file(monkeypatch, tmp_path):
    """V2: fetch_script.lay_meta_video ném RuntimeError, sidecar thiếu title → vẫn ghi source.json,
    vẫn trả dict, không ném ra ngoài."""
    d = tmp_path
    (d / "competitor.segments.json").write_text(json.dumps({
        "video_id": "vid2", "title": "", "description": "", "thumbnail_url": None,
        "segments": [{"start": 0, "duration": 5, "text": "テスト"}]}), encoding="utf-8")
    import fetch_script

    def boom(vid, proxy=None):
        raise RuntimeError("mạng lỗi giả lập")
    monkeypatch.setattr(fetch_script, "lay_meta_video", boom)
    monkeypatch.setattr(HS, "khung_hinh_0_30s", lambda vid, out, n=6, proxy=None: None)
    src = HS.phan_tich_nguon(d, PROF)
    assert (d / "hook/source.json").exists()
    assert src["video_hook_verdict"] == "khong_soi_duoc"
    assert src["title"] == ""  # không lấy được meta, đi tiếp với chuỗi rỗng


def test_phan_tich_nguon_segments_hong_van_ghi_file(tmp_path):
    """V1: competitor.segments.json hỏng → phan_tich_nguon vẫn ghi source.json với video_id=None."""
    d = tmp_path
    (d / "competitor.segments.json").write_text("{broken", encoding="utf-8")
    src = HS.phan_tich_nguon(d, PROF)
    assert (d / "hook/source.json").exists()
    assert src["video_id"] is None


class _FakeYDLKhungHinh:
    """Fake yt_dlp.YoutubeDL: client 'android' ném DownloadError-giả (mô phỏng lượt thử ĐẦU vẫn có
    thể fail vì lý do khác video), client 'web' thì 'tải' thành công (ghi ra .webm để mô phỏng
    format video-only). Ghi lại danh sách client đã thử vào `da_thu`.
    Vá lần 2 (2026-09-23): KHUNG_HINH_THU đổi thứ tự 'android' lên ĐẦU (đã verify tải thật trên
    video thật) — test này đổi client fail từ 'web'→'android' để vẫn khoá được HÀNH VI THỬ LẠI
    (không phải chỉ khoá tên client đầu tiên), đồng thời chốt thứ tự thử mới ở da_thu."""
    da_thu = []

    def __init__(self, opts):
        self.opts = opts

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def download(self, urls):
        client = self.opts["extractor_args"]["youtube"]["player_client"][0]
        _FakeYDLKhungHinh.da_thu.append(client)
        if client == "android":
            raise RuntimeError("Requested format is not available")
        out = Path(self.opts["outtmpl"].replace("%(ext)s", "webm"))
        out.write_bytes(b"0" * 20_000)


def test_khung_hinh_0_30s_thu_lai_doi_client(monkeypatch, tmp_path):
    import types, sys
    import qc_visual
    _FakeYDLKhungHinh.da_thu = []
    fake_yt_dlp = types.SimpleNamespace(YoutubeDL=_FakeYDLKhungHinh,
                                         utils=types.SimpleNamespace(download_range_func=lambda *a, **k: None))
    monkeypatch.setitem(sys.modules, "yt_dlp", fake_yt_dlp)
    monkeypatch.setitem(sys.modules, "yt_dlp.utils", fake_yt_dlp.utils)
    monkeypatch.setattr(HS.time, "sleep", lambda s: None)
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(tmp_path / "ffmpeg_gia" / "ffmpeg.exe"))
    # shim PATH đã có test riêng (test_ffmpeg_tren_path_*) — ở đây tắt hẳn để không đụng ổ đĩa
    # thật/PATH thật của máy chạy test.
    monkeypatch.setattr(HS, "_ffmpeg_tren_path", lambda: None)

    def fake_frame(mp4, t, out):
        from PIL import Image
        Image.new("RGB", (20, 20), "white").save(out)
        return True
    monkeypatch.setattr(qc_visual, "_frame", fake_frame)

    out = HS.khung_hinh_0_30s("vidX", tmp_path / "frames", n=2)
    assert out is not None and Path(out).exists() and Path(out).stat().st_size > 2000
    # Vá lần 2: thứ tự thử mới android → web (android đứng đầu, đã verify tải thật).
    assert _FakeYDLKhungHinh.da_thu == ["android", "web"]


def test_khung_hinh_0_30s_ca_3_lan_deu_nem_tra_none(monkeypatch, tmp_path):
    import types, sys
    import qc_visual

    class LuonLoi(_FakeYDLKhungHinh):
        def download(self, urls):
            raise RuntimeError("Requested format is not available")
    fake_yt_dlp = types.SimpleNamespace(YoutubeDL=LuonLoi,
                                         utils=types.SimpleNamespace(download_range_func=lambda *a, **k: None))
    monkeypatch.setitem(sys.modules, "yt_dlp", fake_yt_dlp)
    monkeypatch.setitem(sys.modules, "yt_dlp.utils", fake_yt_dlp.utils)
    monkeypatch.setattr(HS.time, "sleep", lambda s: None)
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(tmp_path / "ffmpeg_gia" / "ffmpeg.exe"))
    monkeypatch.setattr(HS, "_ffmpeg_tren_path", lambda: None)

    out = HS.khung_hinh_0_30s("vidY", tmp_path / "frames2", n=2)
    assert out is None


# ── _ffmpeg_tren_path: shim PATH cho yt_dlp download_ranges (vá lần 2, 2026-09-23) ──────────

def test_ffmpeg_tren_path_tao_shim(monkeypatch, tmp_path):
    """Tạo được ffmpeg.exe (hoặc 'ffmpeg' ngoài Windows) trong thư mục shim và prepend vào PATH."""
    import sys
    import qc_visual
    nguon = tmp_path / "nguon" / "ffmpeg-win-x86_64-v7.1.exe"
    nguon.parent.mkdir(parents=True, exist_ok=True)
    nguon.write_bytes(b"gia lap binary ffmpeg")
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(nguon))
    monkeypatch.setattr(HS.tempfile, "gettempdir", lambda: str(tmp_path))
    monkeypatch.delenv("PATH", raising=False)
    monkeypatch.setenv("PATH", str(tmp_path / "path_cu"))

    thu_muc = HS._ffmpeg_tren_path()
    assert thu_muc is not None
    ten_file = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    dich = thu_muc / ten_file
    assert dich.exists() and dich.read_bytes() == b"gia lap binary ffmpeg"
    assert str(thu_muc) in HS.os.environ["PATH"].split(HS.os.pathsep)


def test_ffmpeg_tren_path_idempotent(monkeypatch, tmp_path):
    """Gọi 2 lần: không tạo lại file, không nhân đôi PATH, không ném."""
    import qc_visual
    nguon = tmp_path / "nguon" / "ffmpeg.exe"
    nguon.parent.mkdir(parents=True, exist_ok=True)
    nguon.write_bytes(b"binary that")
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(nguon))
    monkeypatch.setattr(HS.tempfile, "gettempdir", lambda: str(tmp_path))
    monkeypatch.setenv("PATH", str(tmp_path / "path_cu"))

    thu_muc1 = HS._ffmpeg_tren_path()
    thu_muc2 = HS._ffmpeg_tren_path()
    assert thu_muc1 == thu_muc2
    assert HS.os.environ["PATH"].split(HS.os.pathsep).count(str(thu_muc1)) == 1


def test_ffmpeg_tren_path_loi_khong_nem(monkeypatch, tmp_path):
    """os.link VÀ shutil.copy2 cùng ném → trả None, không lan lỗi ra ngoài."""
    import qc_visual
    nguon = tmp_path / "nguon" / "ffmpeg.exe"
    nguon.parent.mkdir(parents=True, exist_ok=True)
    nguon.write_bytes(b"binary that")
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(nguon))
    monkeypatch.setattr(HS.tempfile, "gettempdir", lambda: str(tmp_path))

    def boom_link(*a, **k):
        raise OSError("khong hardlink duoc")

    def boom_copy(*a, **k):
        raise OSError("khong copy duoc")
    monkeypatch.setattr(HS.os, "link", boom_link)
    monkeypatch.setattr(HS.shutil, "copy2", boom_copy)

    assert HS._ffmpeg_tren_path() is None


# ── Vá lần 4 (2026-09-23): BỎ side effect lúc import, thay bằng gọi lười + tự xoá memo yt_dlp ──
# Trước đó (vá lần 3) FFMPEG_SHIM = _ffmpeg_tren_path() chạy ngay lúc `import hook_stage` — blast
# radius quá rộng (ghi đĩa thật ~87MB + sửa PATH cả tiến trình chỉ vì import, kể cả lúc pytest
# collect). Controller đã đo thật: memo dò-ffmpeg của yt_dlp nằm ở 2 dict CẤP CLASS trong
# `FFmpegPostProcessor` (_version_cache/_features_cache, khoá tên trần 'ffmpeg'/'ffprobe') và XOÁ
# ĐƯỢC — nên _ffmpeg_tren_path() giờ tự xoá memo đó nếu module yt_dlp.postprocessor.ffmpeg đã nằm
# trong sys.modules, và không cần chạy sớm hơn mọi lệnh gọi yt_dlp nữa (gọi muộn ở đầu
# phan_tich_nguon() vẫn ăn).

def test_import_hook_stage_khong_tao_shim_khong_sua_path():
    """V2: import hook_stage KHÔNG được có side effect nào — không tạo shim, không sửa PATH. Kiểm
    bằng tiến trình CON (không đụng PATH/biến toàn cục của chính tiến trình pytest đang chạy):
    import xong, FFMPEG_SHIM phải là None."""
    import subprocess, sys as _sys
    thu_muc_pipeline = str(Path(__file__).resolve().parent.parent)
    ma = ("import sys; sys.path.insert(0, r'%s'); import hook_stage; "
          "print(hook_stage.FFMPEG_SHIM)") % thu_muc_pipeline
    kq = subprocess.run([_sys.executable, "-c", ma], capture_output=True, text=True, timeout=30)
    assert kq.returncode == 0, f"tiến trình con lỗi: {kq.stderr}"
    assert kq.stdout.strip() == "None"


class _FakeFFmpegPP:
    """Mô phỏng yt_dlp.postprocessor.ffmpeg.FFmpegPostProcessor — chỉ 2 dict memo cấp CLASS mà
    _ffmpeg_tren_path() phải xoá đúng 2 khoá, giữ nguyên khoá None."""
    _version_cache = {None: None, "ffmpeg": False, "ffprobe": False}
    _features_cache = {"ffmpeg": {"setts": True}}


def _module_gia_yt_dlp_ffmpeg(cls):
    import types
    mod = types.SimpleNamespace(FFmpegPostProcessor=cls)
    return mod


def test_ffmpeg_tren_path_xoa_memo_yt_dlp_da_nap(monkeypatch, tmp_path):
    """V1: nếu yt_dlp.postprocessor.ffmpeg ĐÃ nằm trong sys.modules (giả lập bằng monkeypatch),
    _ffmpeg_tren_path() phải pop đúng 2 khoá 'ffmpeg'/'ffprobe' khỏi _version_cache, giữ khoá None,
    và clear() _features_cache."""
    import sys as _sys
    import qc_visual
    nguon = tmp_path / "nguon" / "ffmpeg.exe"
    nguon.parent.mkdir(parents=True, exist_ok=True)
    nguon.write_bytes(b"binary that")
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(nguon))
    monkeypatch.setattr(HS.tempfile, "gettempdir", lambda: str(tmp_path))
    monkeypatch.setenv("PATH", str(tmp_path / "path_cu"))

    cls = type("FFmpegPostProcessor", (), {
        "_version_cache": dict(_FakeFFmpegPP._version_cache),
        "_features_cache": dict(_FakeFFmpegPP._features_cache)})
    monkeypatch.setitem(_sys.modules, "yt_dlp.postprocessor.ffmpeg", _module_gia_yt_dlp_ffmpeg(cls))

    thu_muc = HS._ffmpeg_tren_path()
    assert thu_muc is not None
    assert "ffmpeg" not in cls._version_cache and "ffprobe" not in cls._version_cache
    assert cls._version_cache[None] is None
    assert cls._features_cache == {}


def test_ffmpeg_tren_path_loi_xoa_memo_khong_lam_nga(monkeypatch, tmp_path):
    """Module yt_dlp giả có _version_cache ném lỗi khi truy cập (mô phỏng API nội bộ đã đổi) —
    _ffmpeg_tren_path() vẫn phải trả về thư mục shim bình thường, không ném."""
    import sys as _sys
    import qc_visual
    nguon = tmp_path / "nguon" / "ffmpeg.exe"
    nguon.parent.mkdir(parents=True, exist_ok=True)
    nguon.write_bytes(b"binary that")
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(nguon))
    monkeypatch.setattr(HS.tempfile, "gettempdir", lambda: str(tmp_path))
    monkeypatch.setenv("PATH", str(tmp_path / "path_cu"))

    class _VersionCacheNem:
        def pop(self, *a, **k):
            raise RuntimeError("API noi bo da doi")

    class FFmpegPostProcessorHong:
        _version_cache = _VersionCacheNem()
        _features_cache = {}
    monkeypatch.setitem(_sys.modules, "yt_dlp.postprocessor.ffmpeg",
                         _module_gia_yt_dlp_ffmpeg(FFmpegPostProcessorHong))

    thu_muc = HS._ffmpeg_tren_path()
    assert thu_muc is not None
    ten_file = "ffmpeg.exe" if _sys.platform == "win32" else "ffmpeg"
    assert (thu_muc / ten_file).exists()


class _CapturingYDLKhungHinh(_FakeYDLKhungHinh):
    """Như _FakeYDLKhungHinh (client 'android' fail, 'web' 'tải' được) nhưng lưu lại `opts` của
    LƯỢT GỌI ĐẦU TIÊN — dùng để soi ffmpeg_location/cookiefile mà khung_hinh_0_30s() thật sự
    truyền cho yt_dlp, không đoán qua hành vi bên ngoài."""
    opts_da_goi = []

    def __init__(self, opts):
        super().__init__(opts)
        _CapturingYDLKhungHinh.opts_da_goi.append(opts)


def test_khung_hinh_0_30s_ffmpeg_location_va_cookie(monkeypatch, tmp_path):
    """V2: ffmpeg_location truyền cho yt_dlp phải là ĐÚNG thư mục shim (HS.FFMPEG_SHIM hoặc thư
    mục mà _ffmpeg_tren_path() trả về trong lượt gọi này), KHÔNG phải thư mục imageio_ffmpeg; và
    _ap_cookies() phải được gọi (cookiefile xuất hiện trong opts khi có YTDLP_COOKIES)."""
    import types, sys
    import qc_visual
    _FakeYDLKhungHinh.da_thu = []
    _CapturingYDLKhungHinh.opts_da_goi = []
    fake_yt_dlp = types.SimpleNamespace(YoutubeDL=_CapturingYDLKhungHinh,
                                         utils=types.SimpleNamespace(download_range_func=lambda *a, **k: None))
    monkeypatch.setitem(sys.modules, "yt_dlp", fake_yt_dlp)
    monkeypatch.setitem(sys.modules, "yt_dlp.utils", fake_yt_dlp.utils)
    monkeypatch.setattr(HS.time, "sleep", lambda s: None)
    monkeypatch.setattr(qc_visual, "_ff", lambda: str(tmp_path / "ffmpeg_gia" / "ffmpeg.exe"))

    thu_muc_shim = tmp_path / "shim_gia"
    monkeypatch.setattr(HS, "_ffmpeg_tren_path", lambda: thu_muc_shim)

    cookie_file = tmp_path / "cookie.txt"
    cookie_file.write_text("gia lap cookie", encoding="utf-8")
    monkeypatch.setenv("YTDLP_COOKIES", str(cookie_file))

    def fake_frame(mp4, t, out):
        from PIL import Image
        Image.new("RGB", (20, 20), "white").save(out)
        return True
    monkeypatch.setattr(qc_visual, "_frame", fake_frame)

    out = HS.khung_hinh_0_30s("vidZ", tmp_path / "frames3", n=2)
    assert out is not None and Path(out).exists()
    assert _CapturingYDLKhungHinh.opts_da_goi, "khung_hinh_0_30s không gọi tới yt_dlp.YoutubeDL"
    opts0 = _CapturingYDLKhungHinh.opts_da_goi[0]
    if thu_muc_shim is not None:
        assert opts0["ffmpeg_location"] == str(thu_muc_shim)
    else:
        pytest.skip("_ffmpeg_tren_path() trả None trong test này — không kiểm được nhánh shim")
    assert opts0.get("cookiefile") == str(cookie_file)


# ---------------------------------------------------------------------------
# Task 6 (2026-09-23): Sol lens `hook` + khối "NỐI TỪ HOOK" cho 3 lens cũ.
# run_hook() chấm 3 ứng viên hook 20-30s, chọn 1, trả PASS/FIX (không REMAKE — hook
# chỉ ~150 chữ, sửa tại chỗ luôn đủ). NOI_TU_HOOK là khối chèn được vào 3 lens cũ qua
# tham số hook_block của run() để khi chấm TOÀN VĂN, sol soi thêm việc thân bài có nối
# đúng với hook đã khoá không (không lặp/không reset/không phá promise).
# ---------------------------------------------------------------------------

def test_run_hook_parse(monkeypatch):
    import qc_script_sol as Q, sol_client
    monkeypatch.setattr(sol_client, "chat", lambda *a, **k: ("KẾT QUẢ: FIX\nCHỌN: 2\nLÝ DO: x\n1. TITLE_MATCH: PASS", {}))
    v, chon, txt = Q.run_hook("=== HOOK 1 ===\na\n=== HOOK 2 ===\nb", "T", "A|B", "core_event: X")
    assert v == "FIX" and chon == 2 and "CHỌN" in txt


def test_lens_cu_co_hook_block():
    import qc_script_sol as Q
    for t in Q.LENS_TMPL.values():
        assert "{hook_block}" in t
    assert "NỐI TỪ HOOK" in Q.NOI_TU_HOOK


# ---------------------------------------------------------------------------
# Task 7 (2026-09-23): viết 3 hook + Sol chọn/vá + ensure_locked() orchestrator.
# ---------------------------------------------------------------------------
import ai_steps


def test_ensure_locked_fix_roi_pass(monkeypatch, tmp_path):
    d = _tap(tmp_path, title="【漫画】63歳で年金を繰り上げた男…本当の後悔")
    (d / "competitor.txt").write_text("x" * 3000, encoding="utf-8")
    monkeypatch.setattr(HS, "phan_tich_nguon", lambda d, prof, proxy=None, force=False: {"video_id": None, "hook_4_nhip": {},
                                                                                        "hook_kind": "none", "score_0_12": 0,
                                                                                        "video_hook_verdict": "khong_soi_duoc",
                                                                                        "transcript_0_30s": "", "title": "",
                                                                                        "promise_match": {}})
    # NOTE (2026-09-23, khác brief — xem báo cáo Task 7 §"chỉnh gì so với brief"): chuỗi "good"
    # nguyên văn trong brief chỉ có 99 chữ, LUÔN NGOÀI khoảng 127–172 mà chính so_chu_muc_tieu(PROF)
    # (muc=150, tol=15%) đòi hỏi → check() sẽ luôn trượt "độ dài" cho CẢ 3 ứng viên, hop rỗng, và
    # đường "cả 3 trượt → vá 1 lần → BLOCK" chạy thay vì đường "1/3 qua → Sol chọn/vá/PASS" mà test
    # này đặt tên và đang muốn kiểm. Nối thêm 2 câu cùng mạch truyện để "good" rơi đúng khoảng hợp lệ
    # (143 chữ, đã verify HS.check(good, PROF) == []), giữ nguyên nội dung/văn phong câu gốc.
    good = ("「三年前に引っ越しましたよ」隣人はそう言った。五十年の友が、黙って消えていた。私は箱を抱えたまま、"
            "何をしたのか分からなかった。理由を知ったのは、ずっと後のことだった。それは私の一言から始まっていた。"
            "あの日交わした約束を、私は忘れていたのだ。友の家族にも誰にも、本当のことは言えなかった。")
    cands = f"=== HOOK 1 ===\n短い。\n=== HOOK 2 ===\n{good}\n=== HOOK 3 ===\nこんにちは。{good}"
    monkeypatch.setattr(ai_steps, "_writer_chat", lambda prof, prompt, **k: type("R", (), {"text": cands, "model": "m", "provider": "p", "elapsed": 1})())
    import qc_script_sol as Q
    calls = {"n": 0}
    def fake_run_hook(c, title, thumb, promise, profile_id=None, out=None, **kw):
        calls["n"] += 1
        return ("FIX" if calls["n"] == 1 else "PASS"), 2, f"KẾT QUẢ: {'FIX' if calls['n']==1 else 'PASS'}\nCHỌN: 2\nVIỆC PHẢI SỬA:\n1. x"
    monkeypatch.setattr(Q, "run_hook", fake_run_hook)
    monkeypatch.setattr(HS, "patch_hook", lambda prof, text, viec: text)
    hook = HS.ensure_locked(d, PROF, ctx="", title="T")
    assert hook == good.strip() and (d / "hook/hook_lock.json").exists()
    qc = json.loads((d / "hook/hook_qc.json").read_text(encoding="utf-8"))
    assert qc["sol_rounds"] == 2 and qc["state"] == "PASS"


def test_ensure_locked_tai_dung_lock(tmp_path, monkeypatch):
    d = _tap(tmp_path)
    HS.khoa(d, "đã khoá。")
    # V4 hermetic (vá review, 2026-09-23): test gốc không monkeypatch gì — nếu nhánh
    # tái-dùng-khoá (`doc_lock(d)` có + không stale → return sớm) hỏng và rơi xuống nhánh viết
    # mới, test sẽ ÂM THẦM gọi LLM/mạng THẬT thay vì fail sạch. Chặn cả 2 cửa ra ngoài (model
    # VIẾT + Sol) bằng hàm ném lỗi, để test vừa CHỨNG MINH nhánh tái dùng khoá vừa KÍN offline.
    def _cam(*a, **k):
        raise AssertionError("khong duoc goi LLM khi da co lock")
    monkeypatch.setattr(ai_steps, "_writer_chat", _cam)
    import qc_script_sol as Q
    monkeypatch.setattr(Q, "run_hook", _cam)
    assert HS.ensure_locked(d, PROF) == "đã khoá。"


def test_ensure_locked_block_khi_check_khong_qua(monkeypatch, tmp_path):
    d = _tap(tmp_path)
    monkeypatch.setattr(HS, "phan_tich_nguon", lambda *a, **k: {"video_id": None, "hook_4_nhip": {}, "hook_kind": "none",
                                                                "score_0_12": 0, "video_hook_verdict": "khong_soi_duoc",
                                                                "transcript_0_30s": "", "title": "", "promise_match": {}})
    monkeypatch.setattr(ai_steps, "_writer_chat", lambda prof, prompt, **k: type("R", (), {"text": "=== HOOK 1 ===\n短。\n=== HOOK 2 ===\n短。\n=== HOOK 3 ===\n短。"})())
    monkeypatch.setattr(HS, "patch_hook", lambda prof, text, viec: text)
    with pytest.raises(SystemExit):
        HS.ensure_locked(d, PROF)


# ---------------------------------------------------------------------------
# Vá sau review Task 7 (2026-09-23): V1 patch_hook ném không được mất trắng,
# V2 NO_CANDIDATES vẫn ghi dấu vết, V3 state PASS vs PASS_LEAN, V4 3 test luật quan trọng.
# ---------------------------------------------------------------------------

def _cands_fix_x3(d, monkeypatch):
    """Dựng chung: 1 ứng viên hợp lệ (qua check tất định) để Sol luôn có cái để chọn/FIX."""
    (d / "competitor.txt").write_text("x" * 3000, encoding="utf-8")
    monkeypatch.setattr(HS, "phan_tich_nguon", lambda d, prof, proxy=None, force=False: {
        "video_id": None, "hook_4_nhip": {}, "hook_kind": "none", "score_0_12": 0,
        "video_hook_verdict": "khong_soi_duoc", "transcript_0_30s": "", "title": "", "promise_match": {}})
    good = ("「三年前に引っ越しましたよ」隣人はそう言った。五十年の友が、黙って消えていた。私は箱を抱えたまま、"
            "何をしたのか分からなかった。理由を知ったのは、ずっと後のことだった。それは私の一言から始まっていた。"
            "あの日交わした約束を、私は忘れていたのだ。友の家族にも誰にも、本当のことは言えなかった。")
    cands = f"=== HOOK 1 ===\n短い。\n=== HOOK 2 ===\n{good}\n=== HOOK 3 ===\nこんにちは。{good}"
    monkeypatch.setattr(ai_steps, "_writer_chat",
                        lambda prof, prompt, **k: type("R", (), {"text": cands, "model": "m", "provider": "p", "elapsed": 1})())
    return good


def test_ensure_locked_fix_x3_coi_nhu_pass(monkeypatch, tmp_path):
    """V4.1: run_hook luôn trả FIX cả 3 vòng → vẫn khoá được, sol_rounds==3, state==PASS_LEAN,
    log có dòng coi-như-PASS (luật lean FIX×3)."""
    d = _tap(tmp_path, title="【漫画】63歳で年金を繰り上げた男…本当の後悔")
    good = _cands_fix_x3(d, monkeypatch)
    import qc_script_sol as Q
    monkeypatch.setattr(Q, "run_hook", lambda c, title, thumb, promise, profile_id=None, out=None, **kw:
                        ("FIX", 2, "KẾT QUẢ: FIX\nCHỌN: 2\nVIỆC PHẢI SỬA:\n1. x"))
    monkeypatch.setattr(HS, "patch_hook", lambda prof, text, viec: text)  # vá không đổi gì, vẫn hợp lệ
    hook = HS.ensure_locked(d, PROF, ctx="", title="T")
    assert hook == good.strip()
    qc = json.loads((d / "hook/hook_qc.json").read_text(encoding="utf-8"))
    assert qc["sol_rounds"] == 3 and qc["state"] == "PASS_LEAN"
    assert any("coi như PASS" in l or "coi nhu PASS" in l for l in qc["log"])


def test_ensure_locked_ban_va_truot_giu_ban_truoc(monkeypatch, tmp_path):
    """V4.2: patch_hook trả về 1 chuỗi CHẮC CHẮN trượt check() (quá ngắn) → hook khoá phải là bản
    TRƯỚC khi vá (chosen), log có ghi nhận việc giữ bản trước."""
    d = _tap(tmp_path, title="【漫画】63歳で年金を繰り上げた男…本当の後悔")
    good = _cands_fix_x3(d, monkeypatch)
    import qc_script_sol as Q
    calls = {"n": 0}
    def fake_run_hook(c, title, thumb, promise, profile_id=None, out=None, **kw):
        calls["n"] += 1
        return ("FIX" if calls["n"] == 1 else "PASS"), 2, "KẾT QUẢ: FIX\nCHỌN: 2\nVIỆC PHẢI SỬA:\n1. x"
    monkeypatch.setattr(Q, "run_hook", fake_run_hook)
    # bản vá trả về "短。" — chắc chắn trượt check() (quá ngắn so với muc±tol)
    monkeypatch.setattr(HS, "patch_hook", lambda prof, text, viec: "短。")
    hook = HS.ensure_locked(d, PROF, ctx="", title="T")
    assert hook == good.strip()  # giữ nguyên bản trước, KHÔNG phải "短。"
    qc = json.loads((d / "hook/hook_qc.json").read_text(encoding="utf-8"))
    assert any("trượt tất định, giữ bản trước" in l for l in qc["log"])


def test_ensure_locked_patch_hook_nem_khong_lam_sap(monkeypatch, tmp_path):
    """V1/V4.3: patch_hook ném RuntimeError ngay trong vòng Sol → ensure_locked KHÔNG ném ra
    ngoài, vẫn khoá được bản `chosen`, hook_qc.json vẫn được ghi, log có nêu lỗi vá."""
    d = _tap(tmp_path, title="【漫画】63歳で年金を繰り上げた男…本当の後悔")
    good = _cands_fix_x3(d, monkeypatch)
    import qc_script_sol as Q
    monkeypatch.setattr(Q, "run_hook", lambda c, title, thumb, promise, profile_id=None, out=None, **kw:
                        ("FIX", 2, "KẾT QUẢ: FIX\nCHỌN: 2\nVIỆC PHẢI SỬA:\n1. x"))
    def _no(prof, text, viec):
        raise RuntimeError("claude -p quá thời gian (600s)")
    monkeypatch.setattr(HS, "patch_hook", _no)
    hook = HS.ensure_locked(d, PROF, ctx="", title="T")  # không được ném ra ngoài
    assert hook == good.strip()
    qc = json.loads((d / "hook/hook_qc.json").read_text(encoding="utf-8"))
    # V3 (vá review dọn hook, 2026-09-23): patch_hook ném → PASS_PATCH_ERROR, KHÔNG còn PASS_LEAN
    # (PASS_LEAN giờ chỉ dành riêng cho nhánh FIX×3 coi-như-PASS theo luật lean).
    assert qc["state"] == "PASS_PATCH_ERROR"
    assert any("lỗi" in l and "RuntimeError" in l for l in qc["log"])


# ---------------------------------------------------------------------------
# Task 12 (2026-09-23): repair mode + CLI main()
# ---------------------------------------------------------------------------

def test_cli_repair_yeu_cau_script(tmp_path, monkeypatch, capsys):
    """--mode repair mà tập chưa có script.txt → SystemExit nhắc rõ thiếu script.txt.
    (Viết lại sạch từ brief — brief gốc có biểu thức rác `... if False else ...` không có ý
    nghĩa, ở đây chỉ cần profiles.load trả về slug_dir cố định "assets/_t".)"""
    import profiles
    monkeypatch.setattr(profiles, "load", lambda pid: {**PROF, "slug_dir": "assets/_t"})
    monkeypatch.setattr(HS, "ROOT", tmp_path)
    (tmp_path / "assets/_t/ep").mkdir(parents=True)
    with pytest.raises(SystemExit) as e:
        HS.main(["--profile", "x", "--slug", "ep", "--mode", "repair"])
    assert "script.txt" in str(e.value)


def test_cli_only_source_khong_goi_ensure_locked(tmp_path, monkeypatch, capsys):
    """--only source: chỉ chạy phan_tich_nguon rồi in JSON tóm tắt, KHÔNG động tới ensure_locked
    (mock ensure_locked ném AssertionError để chứng minh nó không được gọi tới)."""
    import profiles
    monkeypatch.setattr(profiles, "load", lambda pid: {**PROF, "slug_dir": "assets/_t"})
    monkeypatch.setattr(HS, "ROOT", tmp_path)
    (tmp_path / "assets/_t/ep").mkdir(parents=True)

    def _khong_duoc_goi(*a, **kw):
        raise AssertionError("--only source KHÔNG được gọi ensure_locked")
    monkeypatch.setattr(HS, "ensure_locked", _khong_duoc_goi)

    fake_src = {"video_id": "abc123XYZ00", "hook_kind": "curiosity_gap", "score_0_12": 10,
                "video_hook_verdict": "PASS", "cau_truc_hook": {"dong_co_chinh": "TO_MO"}, "trash": "khong duoc in ra"}
    monkeypatch.setattr(HS, "phan_tich_nguon", lambda d, prof, proxy=None, force=False: fake_src)

    HS.main(["--profile", "x", "--slug", "ep", "--mode", "upstream", "--only", "source"])
    out = json.loads(capsys.readouterr().out)
    assert out == {"video_id": "abc123XYZ00", "hook_kind": "curiosity_gap", "score_0_12": 10,
                   "video_hook_verdict": "PASS", "cau_truc_hook": {"dong_co_chinh": "TO_MO"}}


def test_cli_thu_muc_tap_khong_ton_tai(tmp_path, monkeypatch):
    """Thư mục tập không tồn tại → SystemExit nhắc rõ đường dẫn thư mục đó."""
    import profiles
    monkeypatch.setattr(profiles, "load", lambda pid: {**PROF, "slug_dir": "assets/_t"})
    monkeypatch.setattr(HS, "ROOT", tmp_path)
    with pytest.raises(SystemExit) as e:
        HS.main(["--profile", "x", "--slug", "ep_khong_co"])
    msg = str(e.value)
    assert str(tmp_path / "assets/_t/ep_khong_co") in msg


# ---------------------------------------------------------------------------
# Vá review dọn hook (6 điểm Minor, 2026-09-23) — V1 doc_lock hỏng không nổ,
# V6 cache short-circuit không đụng ffmpeg shim.
# ---------------------------------------------------------------------------

def test_doc_lock_hong_tra_none_khong_nem(tmp_path):
    """V1: hook_lock.json ghi dở/hỏng → doc_lock coi như CHƯA KHOÁ (None), không ném
    JSONDecodeError; kiem_stale vẫn hành xử y hệt trường hợp 'chưa có lock'."""
    hd = tmp_path / "hook"; hd.mkdir()
    (hd / "hook_lock.json").write_text("{broken", encoding="utf-8")
    assert HS.doc_lock(tmp_path) is None
    assert HS.kiem_stale(tmp_path) == (False, ["chưa có hook lock"])


def test_phan_tich_nguon_cache_khong_goi_ffmpeg_shim(monkeypatch, tmp_path):
    """V6: nhánh dùng lại hook/source.json (cache, force=False) KHÔNG được gọi _ffmpeg_tren_path
    (đọc cache không cần đụng yt_dlp/PATH)."""
    hd = tmp_path / "hook"; hd.mkdir()
    cached = {"video_id": "vidX", "hook_kind": "B"}
    (hd / "source.json").write_text(json.dumps(cached), encoding="utf-8")

    def _boom():
        raise AssertionError("cache short-circuit KHÔNG được gọi _ffmpeg_tren_path")
    monkeypatch.setattr(HS, "_ffmpeg_tren_path", _boom)
    src = HS.phan_tich_nguon(tmp_path, PROF)
    assert src == cached


# ---------------------------------------------------------------------------
# Vá review cuối (2026-09-23) — Việc 1: promise rỗng→có giá trị LẦN ĐẦU không phải HOOK_STALE.
# ---------------------------------------------------------------------------

def test_kiem_stale_rebaseline_lan_dau_khong_phai_loi_thoi(tmp_path):
    """Thứ tự pipeline thật: hook khoá TRƯỚC khi title.txt (B9)/thumb_text.txt (B7) tồn tại.
    Lần đầu 2 trường này được ghi (rỗng → có giá trị) không được coi là lỗi thời — chỉ re-baseline
    lại promise trong hook_lock.json. Sửa TIẾP một trường ĐANG có giá trị mới thật sự là lỗi thời."""
    d = tmp_path
    (d / "series_ctx.txt").write_text("[D1] x\n", encoding="utf-8")
    # LÚC KHOÁ: cố ý KHÔNG có title.txt lẫn thumb_text.txt (đúng thứ tự thật của pipeline).
    meta = HS.khoa(d, "hook文。", mode="upstream")
    assert meta["promise"]["title"] == "" and meta["promise"]["thumb_text"] == ""
    assert HS.kiem_stale(d) == (False, [])

    # B7 ghi thumb_text.txt LẦN ĐẦU → không lỗi thời, và lock phải được cập nhật lại (re-baseline).
    (d / "thumb_text.txt").write_text("A|B", encoding="utf-8")
    assert HS.kiem_stale(d) == (False, [])
    assert HS.doc_lock(d)["promise"]["thumb_text"] == "A|B"

    # B9 ghi title.txt LẦN ĐẦU → vẫn không lỗi thời.
    (d / "title.txt").write_text("T1", encoding="utf-8")
    assert HS.kiem_stale(d) == (False, [])
    assert HS.doc_lock(d)["promise"]["title"] == "T1"

    # Sửa title.txt sang nội dung KHÁC (từ "T1" đã có giá trị → "T2") → giờ MỚI là lỗi thời thật.
    (d / "title.txt").write_text("T2", encoding="utf-8")
    stale, ly_do = HS.kiem_stale(d)
    assert stale is True and any("title" in r for r in ly_do)


# ---------------------------------------------------------------------------
# Vá review cuối (2026-09-23) — Việc 3b: check() phải đọc fact_exempt_units từ profile, giống
# hệt luật lean_script.py dùng cho thân bài — tránh 2 luật khác nhau cho cùng khái niệm.
# ---------------------------------------------------------------------------

def test_check_doc_fact_exempt_units_tu_profile():
    ctx = "[D1] 何もない\n"
    hook = "「八十万円あったのに」と彼は言った。それからどうなったのか。" + "あ" * 40
    prof_khong_khai = {**PROF, "script": {}}
    assert any("số ngoài tư liệu" in v for v in HS.check(hook, prof_khong_khai, ctx))
    prof_mien = {**PROF, "script": {"fact_exempt_units": ["万円"]}}
    assert not any("số ngoài tư liệu" in v for v in HS.check(hook, prof_mien, ctx))


# ---------------------------------------------------------------------------
# script.hook.model (2026-09-23) — ghim model VIẾT hook khác brain_model khi kênh cần.
# ---------------------------------------------------------------------------

def test_viet_candidates_khai_model_truyen_xuong_writer_chat(monkeypatch, tmp_path):
    """Profile khai script.hook.model → viet_candidates gọi _writer_chat KÈM model đó."""
    d = _tap(tmp_path)
    prof = {**PROF, "script": {"hook": {"model": "claude-fable-5-1"}}}
    goi = {}
    def fake(prof, prompt, **k):
        goi.update(k)
        return type("R", (), {"text": "x", "model": "m", "provider": "p", "elapsed": 1})()
    monkeypatch.setattr(HS.ai_steps, "_writer_chat", fake)
    HS.viet_candidates(d, prof, {}, "T", "")
    assert goi.get("model") == "claude-fable-5-1"


def test_viet_candidates_khong_khai_model_khong_truyen(monkeypatch, tmp_path):
    """Không khai (hoặc rỗng) → giữ hành vi cũ: KHÔNG kèm `model` trong lời gọi _writer_chat,
    để _writer_chat tự setdefault bằng brain_model_of(prof) (nhánh engine=claude_p)."""
    d = _tap(tmp_path)
    prof = {**PROF, "script": {}}  # không có khối hook
    goi = {"da_goi": False}
    def fake(prof, prompt, **k):
        goi["da_goi"] = True
        goi.update(k)
        return type("R", (), {"text": "x", "model": "m", "provider": "p", "elapsed": 1})()
    monkeypatch.setattr(HS.ai_steps, "_writer_chat", fake)
    HS.viet_candidates(d, prof, {}, "T", "")
    assert goi["da_goi"] is True
    assert "model" not in goi

    # Khai hook nhưng model rỗng → cũng không truyền.
    prof2 = {**PROF, "script": {"hook": {"model": ""}}}
    goi2 = {}
    monkeypatch.setattr(HS.ai_steps, "_writer_chat", lambda prof, prompt, **k: (goi2.update(k) or type("R", (), {"text": "x"})()))
    HS.viet_candidates(d, prof2, {}, "T", "")
    assert "model" not in goi2



def test_hook_goc_json_trending_dung_thang(tmp_path):
    import kiem_hook_goc as K
    ct = {"mo_dau": "thoại", "giay_ket_hook": 20,
          "nhip": [{"tu": 0, "den": 5, "vai_tro": "mở", "cau_goc": "あ"}, {"tu": 5, "den": 20, "vai_tro": "bối cảnh", "cau_goc": "い"}]}
    (tmp_path / "hook_goc.json").write_text(json.dumps({"video_id": "kKzleVgzGso", **ct}, ensure_ascii=False), encoding="utf-8")
    assert K.doc_hook_goc_json(tmp_path, "kKzleVgzGso")["giay_ket_hook"] == 20
    assert K.doc_hook_goc_json(tmp_path, "khacMaVideo") is None
    assert K.kiem_nguon(tmp_path, tai_mang=False)["ok"]
    assert HS.phan_tich_cau_truc(tmp_path, PROF, {"video_id": "kKzleVgzGso"})["nhip"][1]["cau_goc"] == "い"
