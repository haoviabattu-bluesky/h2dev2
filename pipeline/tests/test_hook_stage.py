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


def test_phan_tich_nguon(monkeypatch, tmp_path):
    d = tmp_path
    (d / "competitor.segments.json").write_text(json.dumps({
        "video_id": "vid1", "title": "T", "description": "D", "thumbnail_url": "http://x/t.jpg",
        "segments": [{"start": 0, "duration": 5, "text": "「三年前に引っ越しました」"}, {"start": 31, "duration": 5, "text": "後半"}]}),
        encoding="utf-8")
    import llm_client, qc_visual
    monkeypatch.setattr(llm_client, "chat", lambda prompt, **k: type("R", (), {"text": json.dumps({
        "hook_4_nhip": {"event": "隣人が告げる", "contradiction": "50年の友", "stake": None, "open_loop": "理由は?"},
        "hook_kind": "B", "score_0_12": 9,
        "promise_match": {"title": "PASS", "thumb": "NA", "description": "PASS", "verdict": "PASS", "ly_do": "ok"}})})())
    monkeypatch.setattr(HS, "khung_hinh_0_30s", lambda vid, out, n=6, proxy=None: None)
    monkeypatch.setattr(FS, "tai_anh", lambda url, p, proxy=None: False)
    src = HS.phan_tich_nguon(d, PROF)
    assert src["transcript_0_30s"] == "「三年前に引っ越しました」"
    assert src["hook_kind"] == "B" and src["video_hook_verdict"] == "khong_soi_duoc"
    assert json.loads((d / "hook/source.json").read_text(encoding="utf-8"))["score_0_12"] == 9


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
