import json
from pathlib import Path
import pytest
import fetch_script as FS


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
    p2 = {**PROF, "script": {"hook": {"ratio_30s": 0.4, "banned_openers": ["X"]}}}
    assert HS.so_chu_muc_tieu(p2) == 120 and HS.cau_hinh(p2)["banned_openers"] == ["X"]


def test_cat_0_30s():
    segs = [{"start": 0, "text": "あ"}, {"start": 29.9, "text": "い"}, {"start": 30.0, "text": "う"}]
    assert HS.cat_0_30s(segs) == "あ い"


def test_tach_candidates():
    t = "=== HOOK 1 ===\n一\n=== HOOK 2 ===\n二\n三\n=== HOOK 3 ===\n四"
    assert HS.tach_candidates(t) == ["一", "二\n三", "四"]


def test_check_bat_loi():
    ngan = "短い。"
    assert any("độ dài" in v for v in HS.check(ngan, PROF))
    chao = "こんにちは。" + "あ" * 150
    assert any("chào hỏi" in v for v in HS.check(chao, PROF))
    khong_neo = "そのとき私は何も知らなかった。" * 8
    assert any("neo" in v for v in HS.check(khong_neo[:160], PROF))


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
