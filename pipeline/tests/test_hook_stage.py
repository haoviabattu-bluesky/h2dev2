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
    import types, sys
    class Boom(_FakeYDL):
        def extract_info(self, url, download=False): raise RuntimeError("net")
    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=Boom))
    m = FS.lay_meta_video("abc123XYZ00")
    assert m["title"] == "" and m["duration_sec"] == 0


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
