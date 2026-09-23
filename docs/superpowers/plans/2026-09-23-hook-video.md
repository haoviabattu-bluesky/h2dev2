# Hook 20–30s Đầu Video — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mọi tập của mọi lane có `hook/hook_locked.txt` (20–30s, rút từ video nguồn qua 3 phép kiểm) được khoá TRƯỚC S2, S2 viết thân nối từ hook, `extract_beats` coi hook là Beat 0, HOOK_STALE chặn khi promise đổi; tập chưa đăng có repair mode chỉ thêm hook đầu video.

**Architecture:** Module mới `pipeline/hook_stage.py` (H1–H4: bóc hook nguồn → viết 3 hook → cổng tất định + Sol → LOCK + STALE) và `pipeline/hook_storyboard.py` (4–7 shot + flow prompts + jobs.csv cho Grok). `lean_script.run()` gọi `hook_stage.ensure_locked()` giữa S1Q và S2; `ai_steps._pass1_prompt`/`extract_beats` nhận `hook_locked`; các cổng hiện có (`do_tat_dinh`, Sol, `make_video.kiem_lock`, `qc_final`, `qc_hoso`) thêm phép kiểm hook. Bước 3 (TTS hook repair, sinh clip, ghép) nhận spec ffmpeg trong `docs/GIAO_VIEC_BUOC3_AGENT.md` — Claude Code không tự chạy render.

**Tech Stack:** Python 3.13 (`py -3.13`), pytest 9 (chạy từ `E:\CLAUDE\YOUTUBE\h2dev\pipeline`: `py -3.13 -m pytest tests -q`), yt_dlp, requests, Pillow, imageio_ffmpeg (`imageio_ffmpeg.get_ffmpeg_exe()`), `llm_client.chat` (Gemini), `sol_client.chat` (GPT-5.6-sol, nhận `image_path`), `claude_p_bridge.ask` (Fable viết / Opus vá), `qc_visual._vision` (Gemini vision JSON).

## Global Constraints

- Đường dẫn trong mọi báo cáo/lệnh = tuyệt đối (`E:\CLAUDE\YOUTUBE\h2dev\...`).
- **Hook là pure prose** giống `script.txt`: không `[HOOK]`, không marker, không heading — TTS đọc mọi ký tự.
- Độ dài hook = `round(profiles.char_rate(prof) * script.hook.ratio_30s)` chữ (mặc định `ratio_30s=0.5` ≈ 30 giây), dung sai `script.hook.tol=0.15`. Đếm bằng `ai_steps.measure(text)["chars"]`.
- Phân vai model (anh chốt 2026-09-22): viết hook = `claude_p_bridge.brain_model_of(prof)` đúng 1 lần; vá = `claude_p_bridge.patch_model_of(prof)`; Sol chỉ chấm. Luật lean `FIX×3 = PASS` áp cho hook (MAX_PATCH_HOOK = 2, lượt 3 vẫn FIX → coi PASS, ghi log).
- Khác biệt lane CHỈ qua field profile `script.hook.*`; **cấm `if profile_id ==`**. Lane không khai → mặc định; không có cách tắt hook.
- Không sửa `script.txt` sau LOCK (NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS). Repair mode không đụng `script.txt` · `voice.mp3` · `img/` · `final.mp4`.
- Claude Code không chạy render/ghép video (trừ lane `toshi-densetsu-jp`). Task 13 chỉ viết spec cho agent bước 3.
- Không xoá dữ liệu Google Sheet. Không `taskkill chrome`.
- Mỗi test chạy được offline: mọi lệnh mạng/LLM/ffmpeg đều `monkeypatch`.
- Commit chỉ khi anh cho phép; message kết thúc bằng `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## File Structure

| File | Trách nhiệm |
|---|---|
| Create `pipeline/hook_stage.py` | H0–H4 + STALE + repair mode + CLI. Không biết gì về S2. |
| Create `pipeline/hook_storyboard.py` | Từ `hook_locked.txt` + `characters.json` → `hook_storyboard.json`, `flow_prompts/`, `grok_jobs.csv`. |
| Create `pipeline/tests/test_hook_stage.py`, `pipeline/tests/test_hook_storyboard.py`, `pipeline/tests/test_hook_wiring.py` | Test tất định + wiring (monkeypatch LLM). |
| Modify `pipeline/fetch_script.py` | `lay_meta_video()`; sidecar `.segments.json` thêm `title/description/thumbnail_url`; tải `competitor_thumb.jpg`. |
| Modify `pipeline/channel_analyzer.py` | K1 lưu `_raw/segments/<id>.json`, `_raw/meta/<id>.json`, `_raw/thumbs/`; K2 prompt thêm khối hook có cấu trúc. |
| Modify `pipeline/qc_script_sol.py` | `HOOK_TMPL` + `run_hook()`; `{hook_block}` trong 3 lens. |
| Modify `pipeline/ai_steps.py` | `_pass1_prompt(hook_locked=)`, `extract_beats(hook_locked=)` Beat 0. |
| Modify `pipeline/lean_script.py` | gọi `hook_stage.ensure_locked`; `viet(hook)`; `do_tat_dinh(hook)`; `PRESERVE`; `sol_qc(hook)`. |
| Modify `pipeline/qc_script.py` | `mo_dau(..., warn_no_marker=False)` hết ĐẠT giả. |
| Modify `pipeline/make_video.py` | `Job.kiem_lock()` thêm `hook_stage.kiem_stale`. |
| Modify `pipeline/qc_final.py` | `kiem_hook()`. |
| Modify `pipeline/qc_hoso.py` | `kiem_hook_ho_so()`. |
| Modify docs: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`, `docs/GIAO_VIEC_BUOC3_AGENT.md`, `CLAUDE.md`, `docs/SOP_*.md` | 1 mục hook / 1 dòng trỏ. |

Thư mục tập sau khi xong: `assets/<lane>/epNN-<slug>/hook/{source.json, frames/, source_thumb.jpg, hook_candidates.txt, hook_qc.json, hook_locked.txt, hook_lock.json, promise.txt(tuỳ chọn), hook_storyboard.json, flow_prompts/shot_NN.txt, grok_jobs.csv}`.

---

### Task 1: `fetch_script.lay_meta_video()` + sidecar có title/description/thumbnail

**Files:**
- Modify: `pipeline/fetch_script.py:254-277` (thêm hàm sau `video_minutes`), `pipeline/fetch_script.py:318-329` (sidecar)
- Test: `pipeline/tests/test_hook_stage.py` (mục fetch)

**Interfaces:**
- Produces: `fetch_script.lay_meta_video(url_or_id, proxy=None) -> dict` với khoá `video_id, title, description, thumbnail_url, duration_sec` (rỗng/0 khi lỗi, không ném). `fetch_script.tai_anh(url, out_path, proxy=None) -> bool`.
- Sidecar `<out>.segments.json` thêm 3 khoá `title, description, thumbnail_url`; file `competitor_thumb.jpg` cạnh `competitor.txt` khi tải được.

- [ ] **Step 1: Viết test thất bại**

```python
# pipeline/tests/test_hook_stage.py
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
```

- [ ] **Step 2: Chạy test, xác nhận FAIL**

Run: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_hook_stage.py -q`
Expected: FAIL `AttributeError: module 'fetch_script' has no attribute 'lay_meta_video'`

- [ ] **Step 3: Cài đặt**

Thêm sau `video_minutes()` trong `pipeline/fetch_script.py`:

```python
def lay_meta_video(url_or_id, timeout=25, proxy=None):
    """Title / mô tả / thumbnail / thời lượng của video nguồn (H1–H3 của hook_stage). Không ném — lỗi trả rỗng.
    KHÔNG extract_flat: mô tả chỉ có ở lượt đọc trang watch đầy đủ (~1–2 s/video)."""
    vid = video_id(url_or_id)
    out = {"video_id": vid, "title": "", "description": "", "thumbnail_url": "", "duration_sec": 0}
    try:
        import yt_dlp
        opts = {"quiet": True, "no_warnings": True, "skip_download": True, "noprogress": True,
                "socket_timeout": timeout}
        if proxy:
            opts["proxy"] = proxy
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False) or {}
        out["title"] = info.get("title") or ""
        out["description"] = info.get("description") or ""
        out["thumbnail_url"] = info.get("thumbnail") or f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
        out["duration_sec"] = int(info.get("duration") or 0)
    except Exception as e:
        print(f"  ! không đọc được meta video {vid} ({type(e).__name__} {e})")
    return out


def tai_anh(url, out_path, proxy=None, timeout=30):
    """Tải 1 ảnh (thumbnail nguồn). Trả True khi file > 2 KB."""
    try:
        import requests
        r = requests.get(url, timeout=timeout, proxies={"http": proxy, "https": proxy} if proxy else None)
        if r.status_code == 200 and len(r.content) > 2000:
            Path(out_path).write_bytes(r.content)
            return True
    except Exception as e:
        print(f"  ! không tải được {url} ({type(e).__name__})")
    return False
```

Sửa khối sidecar trong `main()` (dòng `side.write_text(...)`):

```python
    meta = lay_meta_video(vid, proxy=args.proxy or None)
    side = out.with_name(out.stem + ".segments.json")
    side.write_text(json.dumps({"video_id": vid, "source": used, "video_duration_sec": dur_sec,
                                "title": meta["title"], "description": meta["description"],
                                "thumbnail_url": meta["thumbnail_url"],
                                "segments": [{"start": float(s["start"]), "duration": float(s.get("duration", 0)),
                                              "text": s["text"]} for s in segs]},
                               ensure_ascii=False), encoding="utf-8")
    if meta["thumbnail_url"]:
        tai_anh(meta["thumbnail_url"], out.with_name(out.stem + "_thumb.jpg"), proxy=args.proxy or None)
```

- [ ] **Step 4: Chạy test, xác nhận PASS**

Run: `py -3.13 -m pytest tests/test_hook_stage.py -q` → Expected: `2 passed`

- [ ] **Step 5: Commit (nếu anh cho phép)**

```bash
git add pipeline/fetch_script.py pipeline/tests/test_hook_stage.py
git commit -m "feat(hook): fetch_script lưu title/description/thumbnail nguồn vào sidecar

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: K1 lưu segments/meta/thumbs; K2 prompt hook có cấu trúc

**Files:**
- Modify: `pipeline/channel_analyzer.py:100-121` (`crawl_transcripts`), `:125-140` (`VIDEO_PROMPT`), `:186-195` (`analyze_one_video`)
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces:**
- Consumes: `fetch_script.lay_meta_video`, `fetch_script.tai_anh` (Task 1).
- Produces: `out_dir/_raw/segments/<id>.json` (`[{"start","duration","text"}]`), `out_dir/_raw/meta/<id>.json` (dict Task 1), `out_dir/_raw/thumbs/<rank02>_<view>_<id>.jpg`; row transcript thêm `description`, `dau_0_30s` (chuỗi 30 giây đầu theo mốc `start<30`). `VIDEO_ANALYSIS/<id>.json` thêm khoá `hook_0_30s, hook_4_nhip{event,contradiction,stake,open_loop}, hook_kind(A|B|C|D|E), hook_score_0_12, promise_match{title,description,verdict,ly_do}`.

- [ ] **Step 1: Test thất bại**

```python
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
```

- [ ] **Step 2: Chạy → FAIL** (`KeyError: 'description'` / assert prompt)

- [ ] **Step 3: Cài đặt**

`crawl_transcripts` thay thân vòng `for r in rows`:

```python
    (out_dir / "_raw" / "segments").mkdir(parents=True, exist_ok=True)
    (out_dir / "_raw" / "meta").mkdir(parents=True, exist_ok=True)
    (out_dir / "_raw" / "thumbs").mkdir(parents=True, exist_ok=True)
    for rank, r in enumerate(rows, 1):
        try:
            segs, used = fetch_script.fetch_any(r["id"], langs, proxy=proxy)
            text = re.sub(r"\s+", " ", " ".join(s["text"] for s in segs)).strip()
            dau = re.sub(r"\s+", " ", " ".join(s["text"] for s in segs if float(s.get("start", 0)) < 30)).strip()
            meta = fetch_script.lay_meta_video(r["id"], proxy=proxy)
            (out_dir / "_raw" / "segments" / f"{r['id']}.json").write_text(
                json.dumps([{"start": float(s.get("start", 0)), "duration": float(s.get("duration", 0)),
                             "text": s["text"]} for s in segs], ensure_ascii=False), encoding="utf-8")
            (out_dir / "_raw" / "meta" / f"{r['id']}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                                                        encoding="utf-8")
            if meta.get("thumbnail_url"):
                fetch_script.tai_anh(meta["thumbnail_url"],
                                     out_dir / "_raw" / "thumbs" / f"{rank:02d}_{r.get('view_count', 0)}_{r['id']}.jpg",
                                     proxy=proxy)
            out.append({**r, "transcript": text, "description": meta.get("description", ""), "dau_0_30s": dau})
            print(f"  ✓ {r['id']} [{used}]: {len(text):,} ký tự — {r['title'][:50]}")
        except SystemExit as e:
            print(f"  ✗ {r['id']} bỏ qua: {e}")
```

`VIDEO_PROMPT`: thêm sau dòng `LƯỢT XEM: {view_count}`:

```
MÔ TẢ (description gốc, rút gọn): {description}
ĐOẠN ĐẦU 0–30 GIÂY (nguyên văn theo mốc giây): {dau_0_30s}
```

và trong JSON output thêm ngay sau `"hook_type"`:

```
  "hook_0_30s": "chép lại nguyên văn 30 giây đầu (ngôn ngữ gốc), không tóm tắt",
  "hook_4_nhip": {{"event": "sự kiện cụ thể ở 0–5s hoặc null", "contradiction": "mâu thuẫn ở 5–12s hoặc null",
                   "stake": "cảm xúc/mất mát 12–20s hoặc null", "open_loop": "câu hỏi để ngỏ 20–30s hoặc null"}},
  "hook_kind": "A biến cố bất thường | B câu nói sốc | C mâu thuẫn | D hậu quả chưa rõ nguyên nhân | E hé reveal | none",
  "hook_score_0_12": 0,
  "promise_match": {{"title": "PASS|FAIL", "description": "PASS|FAIL|NA", "verdict": "PASS|FAIL", "ly_do": "1 câu"}},
```

`analyze_one_video`: `.format(..., description=(row.get("description") or "")[:1500], dau_0_30s=row.get("dau_0_30s") or row["transcript"][:300])`. Cache cũ không có khoá mới vẫn đọc được (`.get`).

- [ ] **Step 4: Chạy → PASS** `py -3.13 -m pytest tests/test_hook_stage.py -q`

- [ ] **Step 5: Chạy thật 1 kênh nhỏ để nghiệm thu P0** (mạng, ~2 phút):
`py -3.13 channel_analyzer.py --channel-url https://www.youtube.com/@simbot2 --out-dir ..\docs\channel_dna\simbot2 --n-candidates 4 --n-select 4`
Expected: `docs\channel_dna\simbot2\_raw\thumbs\` có 4 jpg, `_raw\meta\` 4 json có `description` khác rỗng.

- [ ] **Step 6: Commit** `feat(hook): K1 lưu segments/meta/thumbnail, K2 bóc hook 0–30s có cấu trúc`

---

### Task 3: `hook_stage.py` — phép đo tất định

**Files:**
- Create: `pipeline/hook_stage.py`
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces (Produces):**
```python
HOOK_DIR = "hook"
MAX_PATCH_HOOK = 2
def cau_hinh(prof) -> dict            # {"ratio_30s":0.5,"tol":0.15,"banned_openers":[...],"neo_ratio":0.4}
def so_chu_muc_tieu(prof) -> int      # round(char_rate * ratio_30s)
def cat_0_30s(segments, sec=30.0) -> str
def tach_candidates(text) -> list[str]        # "=== HOOK n ===" blocks
def check(text, prof, ctx="") -> list[str]    # [] = đạt; mỗi phần tử là 1 việc phải sửa
def bat_dau_bang_hook(script, hook) -> bool
def ke_lai_hook(script, hook, cua_so=600) -> float   # 0..1 tỉ lệ bigram hook xuất hiện lại ngay sau hook
```

- [ ] **Step 1: Test thất bại**

```python
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
    ok = "「三年前に引っ越しましたよ」隣人はそう言った。" + "五十年の友が消えていた。" * 4 + "理由は後で知った。"
    ok = ok[:150]
    assert HS.check(ok, PROF) == []


def test_bat_dau_va_ke_lai():
    hook = "「三年前に引っ越しました」隣人は言った。五十年の友が消えた。"
    script = hook + "\n\n私は箱を抱えたまま立ち尽くした。"
    assert HS.bat_dau_bang_hook(script, hook)
    assert not HS.bat_dau_bang_hook("晩秋の風が。" + script, hook)
    assert HS.ke_lai_hook(hook + "\n\n" + hook, hook) > 0.8
    assert HS.ke_lai_hook(script, hook) < 0.3
```

- [ ] **Step 2: Chạy → FAIL** `ModuleNotFoundError: hook_stage`

- [ ] **Step 3: Cài đặt `pipeline/hook_stage.py` (phần 1)**

```python
"""hook_stage.py — HOOK 20–30 GIÂY ĐẦU, artifact thượng nguồn của mọi tập (anh chốt 2026-09-23).

Luồng: S0 hồ sơ → H1 bóc 0–30s + title/mô tả/thumb video nguồn → H2 soi khung hình → H3 khớp promise nguồn
→ viết 3 hook cho tập mình (brain_model) → check() tất định + Sol lens hook → LOCK (sha256 + promise snapshot)
→ S2 viết thân NỐI từ hook. Hook là pure prose (TTS đọc mọi ký tự) — marker/visual nằm ở JSON riêng.
Repair mode (tập chưa đăng, có script.txt): nguồn = chính script.txt, không chạy S2, chỉ thêm hook đầu video.
"""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_steps, profiles  # noqa: E402

HOOK_DIR = "hook"
MAX_PATCH_HOOK = 2
MAC_DINH = {
    "ratio_30s": 0.5, "tol": 0.15, "neo_ratio": 0.4,
    "banned_openers": {
        "ja": ["こんにちは", "こんばんは", "皆さん", "みなさん", "チャンネル登録", "ご視聴", "私の名前は", "俺の名前は",
               "と申します", "今回は", "今日のテーマ"],
        "ko": ["안녕하세요", "여러분", "구독", "오늘은"],
        "en": ["hello", "hi everyone", "welcome", "subscribe", "in this video", "my name is"]},
}
NEO = re.compile(r"[0-9０-９〇一二三四五六七八九十百千万億]+[年月日歳円人回分秒時km]|「[^」]{2,}」|[ァ-ヴー]{3,}|[A-Z][a-z]+")
CAND_PAT = re.compile(r"^===\s*HOOK\s*(\d+)\s*===\s*$", re.M)


def cau_hinh(prof):
    h = dict(MAC_DINH)
    lang = prof.get("language", "ja")
    h["banned_openers"] = list(MAC_DINH["banned_openers"].get(lang, MAC_DINH["banned_openers"]["ja"]))
    h.update((prof.get("script", {}) or {}).get("hook") or {})
    return h


def so_chu_muc_tieu(prof):
    return int(round(profiles.char_rate(prof) * float(cau_hinh(prof)["ratio_30s"])))


def cat_0_30s(segments, sec=30.0):
    return re.sub(r"\s+", " ", " ".join(s["text"] for s in segments if float(s.get("start", 0)) < sec)).strip()


def tach_candidates(text):
    parts = CAND_PAT.split(text)
    # split → [đầu, "1", body1, "2", body2, ...]
    return [parts[i].strip() for i in range(2, len(parts), 2) if parts[i].strip()]


def _sach(t):
    return re.sub(r"[\s、。「」！？…・ー－\-,.!?\"']", "", t)


def check(text, prof, ctx=""):
    """Phép đo tất định 0 LLM. Trả list việc phải sửa (rỗng = đạt)."""
    h = cau_hinh(prof)
    viec = []
    n = ai_steps.measure(text)["chars"]
    muc = so_chu_muc_tieu(prof)
    lo, hi = int(muc * (1 - h["tol"])), int(muc * (1 + h["tol"]))
    if not (lo <= n <= hi):
        viec.append(f"độ dài {n} chữ ngoài {lo}–{hi} (≈30 giây với char_rate {profiles.char_rate(prof):.0f})")
    dau = text[:max(40, int(len(text) * 0.5))]
    for w in h["banned_openers"]:
        if w.lower() in dau.lower():
            viec.append(f"chào hỏi/giới thiệu bị cấm trong hook: 「{w}」")
    if not NEO.search(text[:max(40, int(len(text) * h["neo_ratio"]))]):
        viec.append(f"{int(h['neo_ratio']*100)}% đầu hook không có neo cụ thể (số/thoại「」/tên riêng) — đang nói suông")
    if ai_steps.MARKER_PAT.search(text):
        viec.append("hook chứa marker/ký hiệu — phải là pure prose")
    if ctx:
        from lean_script import _so_lieu_ngoai_tu_lieu
        for x in _so_lieu_ngoai_tu_lieu(text, ctx):
            viec.append(f"số ngoài tư liệu: {x}")
    return viec


def bat_dau_bang_hook(script, hook):
    return _sach(script).startswith(_sach(hook))


def _bigrams(t):
    t = _sach(t)
    return {t[i:i + 2] for i in range(len(t) - 1)}


def ke_lai_hook(script, hook, cua_so=600):
    """Tỉ lệ bigram của hook xuất hiện lại trong `cua_so` ký tự NGAY SAU hook (0..1). >0.5 = thân kể lại hook."""
    s = _sach(script)
    h = _sach(hook)
    if s.startswith(h):
        s = s[len(h):]
    doan = s[:cua_so]
    bh = _bigrams(hook)
    if not bh:
        return 0.0
    bd = {doan[i:i + 2] for i in range(len(doan) - 1)}
    return len(bh & bd) / len(bh)
```

Lưu ý: `lean_script._so_lieu_ngoai_tu_lieu(text, ctx, exempt_units=())` đã có (dòng 201) — import trong hàm để tránh vòng import (`lean_script` sẽ import `hook_stage`).

- [ ] **Step 4: Chạy → PASS** (7 test mới)

- [ ] **Step 5: Commit** `feat(hook): hook_stage phép đo tất định`

---

### Task 4: LOCK + promise snapshot + HOOK_STALE

**Files:**
- Modify: `pipeline/hook_stage.py`
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces (Produces):**
```python
def promise_snapshot(d: Path) -> dict   # {"title","thumb_text","promise_sha256"|"ctx_sha256","script_sha256"|None}
def khoa(d: Path, text: str, mode="upstream", extra=None) -> dict   # ghi hook/hook_locked.txt + hook/hook_lock.json
def doc_lock(d: Path) -> dict | None
def kiem_stale(d: Path) -> tuple[bool, list[str]]   # (stale, lý_do); không có lock → (False, ["chưa có hook lock"])
```
Quy ước promise: `title.txt` dòng 1 · `thumb_text.txt` toàn văn · nếu có `hook/promise.txt` (6 dòng `core_event/payoff/reveal/timeline_start/...` do Claude Code viết ở S1) thì hash file đó, KHÔNG thì hash `series_ctx.txt` (repair: hash `script.txt`).

- [ ] **Step 1: Test thất bại**

```python
def _tap(tmp_path, title="T1", ctx="[D1] x\n", thumb="A|B"):
    d = tmp_path
    (d / "title.txt").write_text(title, encoding="utf-8")
    (d / "series_ctx.txt").write_text(ctx, encoding="utf-8")
    (d / "thumb_text.txt").write_text(thumb, encoding="utf-8")
    return d


def test_khoa_va_stale(tmp_path):
    d = _tap(tmp_path)
    meta = HS.khoa(d, "hook文。", mode="upstream")
    assert (d / "hook/hook_locked.txt").read_text(encoding="utf-8") == "hook文。"
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
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt (thêm vào `hook_stage.py`)**

```python
def _sha_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _sha_file(p):
    return _sha_text(Path(p).read_text(encoding="utf-8")) if Path(p).exists() else None


def _title(d):
    for name in ("title.txt", "listting.txt"):
        f = d / name
        if f.exists():
            for l in f.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    return l.strip()
    return ""


def promise_snapshot(d, mode="upstream"):
    d = Path(d)
    snap = {"title": _title(d),
            "thumb_text": (d / "thumb_text.txt").read_text(encoding="utf-8").strip() if (d / "thumb_text.txt").exists() else ""}
    pr = d / HOOK_DIR / "promise.txt"
    if pr.exists():
        snap["promise_sha256"] = _sha_file(pr)
    elif mode == "repair":
        snap["script_sha256"] = _sha_file(d / "script.txt")
    else:
        snap["ctx_sha256"] = _sha_file(d / "series_ctx.txt")
    return snap


def khoa(d, text, mode="upstream", extra=None):
    import datetime as _dt
    d = Path(d)
    hd = d / HOOK_DIR
    hd.mkdir(exist_ok=True)
    text = text.strip() + ("\n" if not text.endswith("\n") else "")
    (hd / "hook_locked.txt").write_text(text, encoding="utf-8")
    meta = {"state": "LOCKED", "mode": mode, "at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sha256": _sha_text(text), "chars": ai_steps.measure(text)["chars"],
            "promise": promise_snapshot(d, mode), "stale": False, "source": "hook_locked.txt", **(extra or {})}
    (hd / "hook_lock.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def doc_lock(d):
    p = Path(d) / HOOK_DIR / "hook_lock.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def doc_hook(d):
    p = Path(d) / HOOK_DIR / "hook_locked.txt"
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""


def kiem_stale(d):
    d = Path(d)
    m = doc_lock(d)
    if not m:
        return False, ["chưa có hook lock"]
    ly_do = []
    if _sha_file(d / HOOK_DIR / "hook_locked.txt") != m.get("sha256"):
        ly_do.append("hook_locked.txt bị sửa tay sau khi khoá")
    now = promise_snapshot(d, m.get("mode", "upstream"))
    for k, v in (m.get("promise") or {}).items():
        if now.get(k) != v:
            ly_do.append(f"promise '{k}' đã đổi sau khi khoá hook → HOOK_STALE, chạy lại H1–H4")
    if ly_do:
        m["stale"] = True
        (d / HOOK_DIR / "hook_lock.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    return bool(ly_do), ly_do
```

- [ ] **Step 4: Chạy → PASS**

- [ ] **Step 5: Commit** `feat(hook): LOCK + promise snapshot + HOOK_STALE`

---

### Task 5: H1–H3 — bóc hook video nguồn (`phan_tich_nguon`)

**Files:**
- Modify: `pipeline/hook_stage.py`
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces:**
- Consumes: `fetch_script.lay_meta_video`, `fetch_script.tai_anh`, `llm_client.chat(prompt, task="short", ...)` → `.text`, `qc_visual._vision(prompt, img_path)` → dict, `qc_visual._ff()` (đường dẫn ffmpeg).
- Produces:
```python
def nguon_cua_tap(d, mode) -> dict | None   # {"video_id","segments"} từ competitor.segments.json; None nếu không có
def khung_hinh_0_30s(video_id, out_dir, n=6, proxy=None) -> Path | None   # tải 30s đầu, ghép lưới n khung → out_dir/contact.jpg
def phan_tich_nguon(d, prof, proxy=None, force=False) -> dict   # ghi hook/source.json, trả dict
```
`source.json`: `{"video_id","url","title","description","thumb_path","transcript_0_30s","hook_4_nhip":{...},"hook_kind","score_0_12","video_hook_verdict":"manh|yeu|khong|khong_soi_duoc","promise_match":{"title","thumb","description","verdict","ly_do"}}`.

- [ ] **Step 1: Test thất bại**

```python
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
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt (thêm vào `hook_stage.py`)**

```python
PROMPT_NGUON = """Bạn phân tích 30 GIÂY ĐẦU của một video YouTube (video NGUỒN mà tập mới sẽ nhân bản 70/30).
TIÊU ĐỀ NGUỒN: {title}
MÔ TẢ NGUỒN (rút gọn): {description}
CHỮ TRÊN THUMBNAIL NGUỒN (nếu đọc được): {thumb_text}
LỜI 0–30 GIÂY (nguyên văn): {t30}

Trả ĐÚNG 1 JSON (không bọc ```):
{{"hook_4_nhip": {{"event": "sự kiện cụ thể ở 0–5s hoặc null", "contradiction": "vì sao bất thường, 5–12s hoặc null",
                  "stake": "mất mát/cảm xúc 12–20s hoặc null", "open_loop": "câu hỏi để ngỏ 20–30s hoặc null"}},
 "hook_kind": "A|B|C|D|E|none  (A biến cố bất thường · B câu nói sốc · C mâu thuẫn · D hậu quả chưa rõ nguyên nhân · E hé reveal 20–40%)",
 "score_0_12": 0,
 "promise_match": {{"title": "PASS|FAIL", "thumb": "PASS|FAIL|NA", "description": "PASS|FAIL|NA", "verdict": "PASS|FAIL",
                    "ly_do": "1 câu: hook nguồn có bán CÙNG lời hứa với tiêu đề/thumbnail không"}}}}
Chấm score_0_12 = tổng 6 tiêu chí 0–2: liên quan title · liên quan thumbnail · có bất thường · có câu hỏi mở · có cảm xúc · dựng hình được."""

PROMPT_KHUNG = """Đây là lưới {n} khung hình lấy đều trong 30 giây đầu của một video YouTube kể chuyện.
Trả JSON: {{"so_shot_uoc": <số bố cục khác nhau>, "co_chu_tren_hinh": true/false, "co_nhan_vat": true/false,
"hinh_bam_loi": "manh|yeu|khong", "verdict": "manh|yeu|khong", "ly_do": "1 câu"}}
verdict = manh khi ≥3 bố cục khác nhau VÀ có nhân vật/vật thể gây chú ý; yeu khi 1–2 bố cục; khong khi chỉ ảnh nền/logo/chữ giới thiệu."""


def nguon_cua_tap(d):
    p = Path(d) / "competitor.segments.json"
    if not p.exists():
        return None
    j = json.loads(p.read_text(encoding="utf-8"))
    return j if j.get("video_id") else None


def khung_hinh_0_30s(video_id, out_dir, n=6, proxy=None):
    """Tải 30 giây đầu (yt_dlp download_sections) → n khung → 1 ảnh lưới contact.jpg. Lỗi trả None."""
    import qc_visual
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    mp4 = out_dir / "src_0_30s.mp4"
    try:
        import yt_dlp
        from yt_dlp.utils import download_range_func
        opts = {"quiet": True, "no_warnings": True, "noprogress": True, "format": "best[height<=480]",
                "download_ranges": download_range_func(None, [(0, 30)]), "force_keyframes_at_cuts": True,
                "outtmpl": str(mp4), "ffmpeg_location": str(Path(qc_visual._ff()).parent)}
        if proxy:
            opts["proxy"] = proxy
        with yt_dlp.YoutubeDL(opts) as y:
            y.download([f"https://www.youtube.com/watch?v={video_id}"])
        if not mp4.exists():
            return None
        frames = []
        for i in range(n):
            f = out_dir / f"f{i+1:02d}.jpg"
            if qc_visual._frame(mp4, 1.0 + i * (28.0 / max(n - 1, 1)), f):
                frames.append(f)
        if not frames:
            return None
        from PIL import Image
        ims = [Image.open(f).convert("RGB").resize((480, 270)) for f in frames]
        cols = 3
        rows = (len(ims) + cols - 1) // cols
        grid = Image.new("RGB", (480 * cols, 270 * rows), "black")
        for i, im in enumerate(ims):
            grid.paste(im, ((i % cols) * 480, (i // cols) * 270))
        out = out_dir / "contact.jpg"
        grid.save(out, quality=85)
        return out
    except Exception as e:
        print(f"  ! không soi được khung hình nguồn {video_id}: {type(e).__name__} {str(e)[:100]}")
        return None


def phan_tich_nguon(d, prof, proxy=None, force=False):
    import fetch_script, llm_client, qc_visual
    d = Path(d); hd = d / HOOK_DIR; hd.mkdir(exist_ok=True)
    out_p = hd / "source.json"
    if out_p.exists() and not force:
        return json.loads(out_p.read_text(encoding="utf-8"))
    src = {"video_id": None, "url": None, "title": "", "description": "", "thumb_path": None, "transcript_0_30s": "",
           "hook_4_nhip": {}, "hook_kind": "none", "score_0_12": 0, "video_hook_verdict": "khong_soi_duoc",
           "promise_match": {"verdict": "NA", "ly_do": "không có video nguồn"}}
    j = nguon_cua_tap(d)
    if j:
        vid = j["video_id"]
        src.update(video_id=vid, url=f"https://www.youtube.com/watch?v={vid}", title=j.get("title", ""),
                   description=j.get("description", ""), transcript_0_30s=cat_0_30s(j.get("segments") or []))
        if not src["title"]:
            m = fetch_script.lay_meta_video(vid, proxy=proxy)
            src.update(title=m["title"], description=m["description"])
            j["thumbnail_url"] = j.get("thumbnail_url") or m["thumbnail_url"]
        if j.get("thumbnail_url") and fetch_script.tai_anh(j["thumbnail_url"], hd / "source_thumb.jpg", proxy=proxy):
            src["thumb_path"] = str(hd / "source_thumb.jpg")
        # H2 — khung hình
        grid = khung_hinh_0_30s(vid, hd / "frames", proxy=proxy)
        if grid:
            try:
                v = qc_visual._vision(PROMPT_KHUNG.format(n=6), grid)
                src["video_hook_verdict"] = v.get("verdict", "khong_soi_duoc")
                src["khung_hinh"] = v
            except Exception as e:
                print(f"  ! vision khung hình lỗi: {e}")
        # H1 + H3 — 4 nhịp + promise
        if src["transcript_0_30s"]:
            r = llm_client.chat(PROMPT_NGUON.format(title=src["title"], description=src["description"][:800],
                                                    thumb_text="(chưa đọc)", t30=src["transcript_0_30s"]),
                                task="short", max_tokens=1500, temperature=0.2, verbose=False)
            try:
                a = json.loads(re.sub(r"^```[a-z]*\n?|\n?```$", "", r.text.strip()))
                src.update(hook_4_nhip=a.get("hook_4_nhip") or {}, hook_kind=a.get("hook_kind", "none"),
                           score_0_12=int(a.get("score_0_12") or 0), promise_match=a.get("promise_match") or {})
            except Exception as e:
                print(f"  ! JSON phân tích nguồn hỏng: {e}")
    out_p.write_text(json.dumps(src, ensure_ascii=False, indent=2), encoding="utf-8")
    return src
```

- [ ] **Step 4: Chạy → PASS**

- [ ] **Step 5: Chạy thật 1 tập có `competitor.segments.json`** (mạng): `py -3.13 -c "import hook_stage as H, profiles as P; print(H.phan_tich_nguon(r'E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\ep14-kaimono', P.load('satori-jp-obaa'), force=True)['score_0_12'])"`
Expected: in số ≥0; có `assets\satori_jp\ep14-kaimono\hook\frames\contact.jpg` và `source.json`.

- [ ] **Step 6: Commit** `feat(hook): H1–H3 bóc hook video nguồn (transcript 0–30s, khung hình, promise)`

---

### Task 6: Sol lens `hook` + khối "NỐI TỪ HOOK" cho 3 lens cũ

**Files:**
- Modify: `pipeline/qc_script_sol.py` (thêm `HOOK_TMPL`, `run_hook`, `NOI_TU_HOOK`, tham số `hook_block` trong `run`; 3 template thêm `{hook_block}` trước dòng `QUY TẮC ĐÁNH GIÁ`/`MỨC ĐỘ`)
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces (Produces):**
```python
def run_hook(candidates_text, title, thumb_text, promise_text, profile_id=None, out=None) -> (verdict, chon:int, text)
   # verdict PASS|FIX ; chon = 1..3 ; parse "CHỌN: n" và "KẾT QUẢ: PASS|FIX"
def run(script_text, title, profile_id=None, out=None, extra_note="", hook_block="")  # tương thích cũ
NOI_TU_HOOK = "..."   # đoạn chèn vào extra_note khi có hook
```

- [ ] **Step 1: Test thất bại**

```python
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
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt**

Thêm vào `qc_script_sol.py` (trước `LENS_TMPL`):

```python
NOI_TU_HOOK = """
7. NỐI TỪ HOOK (đoạn mở đầu đã KHOÁ trước khi viết thân — nguyên văn dưới đây):
{hook}
   - Thân bài có KỂ LẠI thông tin hook vừa nói không (lặp sự kiện/câu thoại)? Có RESET câu chuyện (tả thời tiết,
     giới thiệu kênh, mở lại từ đầu) ngay sau hook không?
   - Câu hỏi/lời hứa hook mở ra có được TRẢ đúng chỗ trong thân không? Có phá promise của hook không?
   - Lỗi ở mục này = SAI (không phải chưa hay)."""

HOOK_TMPL = """Bạn là biên tập viên chấm HOOK 20–30 GIÂY ĐẦU của video YouTube kể chuyện tiếng Nhật. Có 3 ứng viên;
hãy chọn 1 và chấm. Đây là LƯỢT DUY NHẤT.

TIÊU ĐỀ (promise): {title}
CHỮ THUMBNAIL (promise): {thumb_text}
LỜI HỨA/SỰ THẬT CỦA TẬP (core_event · payoff · reveal · timeline — hook KHÔNG được bịa ngoài đây, KHÔNG spoil reveal):
{promise_text}

3 ỨNG VIÊN:
{candidates}

Chấm TỪNG ứng viên theo checklist (mỗi ô PASS/FAIL):
TITLE_MATCH · THUMB_MATCH · STORY_TRUTH (sự kiện có trong lời hứa/sự thật ở trên) · NO_FAKE_DRAMA · NO_SPOILER ·
OPEN_LOOP (câu cuối để ngỏ) · EMOTIONAL_STAKE · KHONG_CAN_SETUP (hiểu được ngay) · SU_KIEN_0_5S (3–5 giây đầu đã có
sự kiện) · KHONG_CHAO_HOI · KHONG_CAU_THUA · DU_4_NHIP (event → contradiction → stake → open loop) ·
RETENTION ("tắt title/thumb, chỉ nghe 30s: có muốn biết chuyện gì tiếp không?").

OUTPUT BẮT BUỘC:
KẾT QUẢ: [PASS / FIX]   (PASS = ứng viên được chọn không FAIL ô nào; FIX = ứng viên tốt nhất còn FAIL ≤3 ô, sửa tại chỗ được)
CHỌN: [1 / 2 / 3]
LÝ DO CHỌN: [1–2 câu]
CHECKLIST ỨNG VIÊN ĐƯỢC CHỌN: [mỗi ô 1 dòng: TÊN_Ô: PASS/FAIL — lý do ngắn]
VIỆC PHẢI SỬA (nếu FIX): [đánh số; mỗi việc: trích câu tiếng Nhật | nghĩa Việt → sửa thành gì, ngắn]
"""


def run_hook(candidates_text, title, thumb_text, promise_text, profile_id=None, out=None):
    prompt = HOOK_TMPL.format(title=title or "(chưa chốt)", thumb_text=thumb_text or "(chưa có)",
                              promise_text=promise_text or "(không có — dùng tư liệu tập)", candidates=candidates_text)
    text, usage = sol_client.chat(prompt, max_tokens=3000, timeout=240)
    m = re.search(r"CHỌN\s*[:：]\s*([123])", text)
    chon = int(m.group(1)) if m else 1
    verdict = "PASS" if re.search(r"KẾT QUẢ\s*[:：]\s*PASS", text, re.I) else "FIX"
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return verdict, chon, text
```

Sửa `run()`:

```python
def run(script_text, title, profile_id=None, out=None, extra_note="", hook_block=""):
    ...
    prompt = LENS_TMPL[lens].format(title=title, domain_focus=domain_focus, script=script_text, hook_block=hook_block)
```

Trong 3 template (`PROMPT_TMPL`, `STORY_TMPL`, `PLAIN_TMPL`) chèn dòng `{hook_block}` ngay trước `QUY TẮC ĐÁNH GIÁ` (medical/story) và trước `MỨC ĐỘ —` (plain). Mọi nơi gọi `run()` cũ không truyền `hook_block` → chuỗi rỗng, prompt không đổi.

- [ ] **Step 4: Chạy → PASS**; chạy cả `tests/test_brain_b3s.py` để chắc `run()` cũ không gãy.

- [ ] **Step 5: Commit** `feat(hook): Sol lens hook + mục NỐI TỪ HOOK`

---

### Task 7: Viết 3 hook + chọn + vá + `ensure_locked()` orchestrator

**Files:**
- Modify: `pipeline/hook_stage.py`
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces:**
- Consumes: `ai_steps._writer_chat(prof, prompt, system=, task="short", min_chars=, max_chars=)` → `.text`; `claude_p_bridge.ask(prompt, model=claude_p_bridge.patch_model_of(prof), ...)`; `qc_script_sol.run_hook`; Task 3–5.
- Produces:
```python
def viet_candidates(d, prof, src, title, ctx, mode="upstream") -> str   # ghi hook/hook_candidates.txt, trả text
def patch_hook(prof, text, viec) -> str
def ensure_locked(d, prof, ctx="", title="", mode="upstream", force=False, proxy=None) -> str  # trả hook text; ném SystemExit khi BLOCK
```

- [ ] **Step 1: Test thất bại**

```python
def test_ensure_locked_fix_roi_pass(monkeypatch, tmp_path):
    d = _tap(tmp_path, title="【漫画】63歳で年金を繰り上げた男…本当の後悔")
    (d / "competitor.txt").write_text("x" * 3000, encoding="utf-8")
    monkeypatch.setattr(HS, "phan_tich_nguon", lambda d, prof, proxy=None, force=False: {"video_id": None, "hook_4_nhip": {},
                                                                                        "hook_kind": "none", "score_0_12": 0,
                                                                                        "video_hook_verdict": "khong_soi_duoc",
                                                                                        "transcript_0_30s": "", "title": "",
                                                                                        "promise_match": {}})
    good = ("「三年前に引っ越しましたよ」隣人はそう言った。五十年の友が、黙って消えていた。私は箱を抱えたまま、"
            "何をしたのか分からなかった。理由を知ったのは、ずっと後のことだった。それは私の一言から始まっていた。")
    good = good[:150]
    cands = f"=== HOOK 1 ===\n短い。\n=== HOOK 2 ===\n{good}\n=== HOOK 3 ===\nこんにちは。{good}"
    monkeypatch.setattr(ai_steps, "_writer_chat", lambda prof, prompt, **k: type("R", (), {"text": cands, "model": "m", "provider": "p", "elapsed": 1})())
    import qc_script_sol as Q
    calls = {"n": 0}
    def fake_run_hook(c, title, thumb, promise, profile_id=None, out=None):
        calls["n"] += 1
        return ("FIX" if calls["n"] == 1 else "PASS"), 2, f"KẾT QUẢ: {'FIX' if calls['n']==1 else 'PASS'}\nCHỌN: 2\nVIỆC PHẢI SỬA:\n1. x"
    monkeypatch.setattr(Q, "run_hook", fake_run_hook)
    monkeypatch.setattr(HS, "patch_hook", lambda prof, text, viec: text)
    hook = HS.ensure_locked(d, PROF, ctx="", title="T")
    assert hook == good.strip() and (d / "hook/hook_lock.json").exists()
    qc = json.loads((d / "hook/hook_qc.json").read_text(encoding="utf-8"))
    assert qc["sol_rounds"] == 2 and qc["state"] == "PASS"


def test_ensure_locked_tai_dung_lock(tmp_path):
    d = _tap(tmp_path)
    HS.khoa(d, "đã khoá。")
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
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt (thêm vào `hook_stage.py`)**

```python
PROMPT_VIET = """NHIỆM VỤ: viết 3 ỨNG VIÊN HOOK 20–30 giây cho phần MỞ ĐẦU của một video YouTube kể chuyện ({lang}).
Hook = nội dung ĐẦU TIÊN người xem nghe. Nó phải giữ chân người vừa click tiêu đề/thumbnail.

TIÊU ĐỀ (lời hứa): {title}
CHỮ THUMBNAIL (lời hứa): {thumb_text}
HOOK CỦA VIDEO NGUỒN (đã phân tích — MƯỢN LOẠI hook và VỊ TRÍ giây 0, KHÔNG chép sự kiện/câu thoại/tên):
  loại: {hook_kind} · điểm nguồn: {score}/12 · hình nguồn: {video_verdict}
  4 nhịp nguồn: {nhip}
{khoi_nguon_yeu}
HỒ SƠ / LỜI HỨA CỦA TẬP MÌNH (sự kiện, payoff, reveal — hook chỉ được dùng thứ có ở đây, hé reveal tối đa 20–40%):
{promise}
{khoi_repair}
LUẬT VIẾT (SOP hook):
- Đúng {muc} chữ (±{tol}%; không tính xuống dòng). Pure prose, không marker, không ngoặc vuông, không tiêu đề.
- 4 nhịp theo thứ tự: 0–5s SỰ KIỆN cụ thể (câu thoại「」/con số/hành động) → 5–12s VÌ SAO BẤT THƯỜNG → 12–20s MẤT MÁT/CẢM XÚC
  → 20–30s CÂU HỎI ĐỂ NGỎ rồi DỪNG (không giải thích).
- CẤM: chào hỏi, giới thiệu kênh, xin đăng ký, tả thời tiết/mùa/phong cảnh mở màn, tên-tuổi-nghề người kể, câu triết lý
  suông, tóm tắt cả video, spoil reveal, phóng đại khác bản chất, dữ kiện không có trong hồ sơ.
- Câu ngắn, có chỗ nghỉ, dễ nghe (khán giả lớn tuổi). Ngôi kể/văn thể: {narrator}.
- Mỗi ứng viên chọn 1 loại khác nhau trong A biến cố bất thường · B câu nói sốc · C mâu thuẫn · D hậu quả chưa rõ
  nguyên nhân · E hé reveal.

OUTPUT ĐÚNG KHUÔN, không giải thích thêm:
=== HOOK 1 ===
<hook>
=== HOOK 2 ===
<hook>
=== HOOK 3 ===
<hook>"""

KHOI_NGUON_YEU = ("⚠️ Video nguồn hook YẾU/KHÔNG có hook (verdict {v}) → KHÔNG bắt chước mở đầu nguồn; tự dựng hook từ "
                  "CLIMAX/REVEAL của tập mình (anh chốt 2026-09-23).")
KHOI_REPAIR = ("CHẾ ĐỘ REPAIR: kịch bản tập đã có sẵn và KHÔNG được sửa. Hook sẽ được ghép TRƯỚC đoạn 1 hiện có (dưới đây). "
               "Câu cuối hook phải là CÂU CẦU NỐI để đoạn 1 nghe như setup, không như bắt đầu lại:\nĐOẠN 1 HIỆN CÓ: {doan1}")


def _promise_text(d, ctx, mode):
    d = Path(d)
    pr = d / HOOK_DIR / "promise.txt"
    if pr.exists():
        return pr.read_text(encoding="utf-8").strip()
    if mode == "repair":
        return (d / "script.txt").read_text(encoding="utf-8")[:6000]
    return (ctx or "").strip()[:6000] or "(không có tư liệu — hook chỉ dùng chi tiết hư cấu hợp persona)"


def viet_candidates(d, prof, src, title, ctx, mode="upstream"):
    d = Path(d)
    thumb = (d / "thumb_text.txt").read_text(encoding="utf-8").strip() if (d / "thumb_text.txt").exists() else ""
    n = prof.get("narrator", {}) or {}
    yeu = src.get("video_hook_verdict") in ("yeu", "khong") or int(src.get("score_0_12") or 0) < 6
    doan1 = ""
    if mode == "repair":
        doan1 = next((p.strip() for p in (d / "script.txt").read_text(encoding="utf-8").split("\n\n") if p.strip()), "")
    muc = so_chu_muc_tieu(prof)
    prompt = PROMPT_VIET.format(
        lang=ai_steps.LANG_NAME.get(prof.get("language", "ja"), "Japanese"), title=title or _title(d) or "(chưa chốt)",
        thumb_text=thumb or "(chưa có)", hook_kind=src.get("hook_kind", "none"), score=src.get("score_0_12", 0),
        video_verdict=src.get("video_hook_verdict", "?"), nhip=json.dumps(src.get("hook_4_nhip") or {}, ensure_ascii=False),
        khoi_nguon_yeu=KHOI_NGUON_YEU.format(v=src.get("video_hook_verdict")) if yeu else "",
        promise=_promise_text(d, ctx, mode), khoi_repair=KHOI_REPAIR.format(doan1=doan1) if mode == "repair" else "",
        muc=muc, tol=int(cau_hinh(prof)["tol"] * 100),
        narrator=f"{n.get('persona','')} · {n.get('point_of_view','')} · {n.get('register','')}")
    r = ai_steps._writer_chat(prof, prompt, system=ai_steps._skill_text(prof, "script"), task="short",
                              min_chars=muc * 2, max_chars=muc * 6)
    (d / HOOK_DIR).mkdir(exist_ok=True)
    (d / HOOK_DIR / "hook_candidates.txt").write_text(r.text, encoding="utf-8")
    return r.text


def patch_hook(prof, text, viec):
    import claude_p_bridge
    ds = "\n".join(f"- {v}" for v in viec)
    prompt = (f"SỬA TẠI CHỖ đoạn hook 20–30 giây dưới đây đúng các điểm sau, mọi thứ khác giữ nguyên từng chữ; "
              f"pure prose, không marker, giữ 4 nhịp và câu cuối để ngỏ.\nCÁC ĐIỂM PHẢI SỬA:\n{ds}\n\n"
              f"OUTPUT: chỉ đoạn hook sau khi sửa, không lời dẫn.\n\n=== HOOK ===\n{text}")
    r = claude_p_bridge.ask(prompt, model=claude_p_bridge.patch_model_of(prof), timeout=600,
                            min_chars=int(len(text) * 0.6), max_chars=int(len(text) * 1.6), require_sentence_end=True)
    return ai_steps.normalize_paragraphs(ai_steps.strip_markers(r.text)).strip()


def _viec_tu_sol(text):
    m = re.search(r"VIỆC PHẢI SỬA[^\n]*\n(.*)", text, re.S)
    return [l.strip() for l in (m.group(1) if m else "").splitlines() if re.match(r"^\s*\d+[.)]", l)]


def ensure_locked(d, prof, ctx="", title="", mode="upstream", force=False, proxy=None):
    """H1–H4. Trả hook text đã khoá. SystemExit khi không khoá được (BLOCK)."""
    import qc_script_sol
    d = Path(d); hd = d / HOOK_DIR; hd.mkdir(exist_ok=True)
    if not force and doc_lock(d):
        stale, ly_do = kiem_stale(d)
        if not stale:
            print(f"[H4] dùng hook đã khoá ({doc_lock(d)['chars']} chữ)")
            return doc_hook(d)
        print("[H4] HOOK_STALE: " + " · ".join(ly_do) + " → chạy lại H1–H4")
    src = phan_tich_nguon(d, prof, proxy=proxy, force=force)
    print(f"[H1-H3] nguồn {src.get('video_id') or '(không có)'} · loại {src.get('hook_kind')} · {src.get('score_0_12')}/12 · "
          f"hình {src.get('video_hook_verdict')} · promise nguồn {(src.get('promise_match') or {}).get('verdict', 'NA')}")
    title = title or _title(d)
    cands_text = viet_candidates(d, prof, src, title, ctx, mode)
    cands = tach_candidates(cands_text)
    if len(cands) < 1:
        raise SystemExit("✗ H2': model không trả ứng viên hook theo khuôn === HOOK n ===")
    thumb = (d / "thumb_text.txt").read_text(encoding="utf-8").strip() if (d / "thumb_text.txt").exists() else ""
    promise = _promise_text(d, ctx, mode)
    qc = {"candidates": len(cands), "check": {}, "sol_rounds": 0, "patches": 0, "log": []}
    # tất định trước, Sol chỉ thấy ứng viên qua máy
    hop = []
    for i, c in enumerate(cands, 1):
        v = check(c, prof, ctx)
        qc["check"][str(i)] = v
        if not v:
            hop.append((i, c))
    if not hop:
        # thử vá ứng viên ít lỗi nhất 1 lần
        i, c = min(enumerate(cands, 1), key=lambda t: len(qc["check"][str(t[0])]))
        c2 = patch_hook(prof, c, qc["check"][str(i)])
        qc["patches"] += 1
        if check(c2, prof, ctx):
            (hd / "hook_qc.json").write_text(json.dumps({**qc, "state": "BLOCK"}, ensure_ascii=False, indent=2), encoding="utf-8")
            raise SystemExit(f"✗ H3': cả 3 ứng viên trượt phép đo tất định: {qc['check']}")
        hop = [(i, c2)]
    cands_hop = "\n".join(f"=== HOOK {i} ===\n{c}" for i, c in hop)
    text = None
    for vong in range(1, MAX_PATCH_HOOK + 2):
        verdict, chon, rep = qc_script_sol.run_hook(cands_hop, title, thumb, promise, profile_id=prof["id"],
                                                    out=str(hd / f"hook_sol_report_{vong}.txt"))
        qc["sol_rounds"] = vong
        chosen = dict(hop).get(chon) or hop[0][1]
        if verdict == "PASS":
            text = chosen; qc["log"].append(f"sol{vong} PASS chọn {chon}"); break
        viec = _viec_tu_sol(rep) or ["theo báo cáo Sol"]
        if vong > MAX_PATCH_HOOK:
            text = chosen; qc["log"].append(f"sol{vong} FIX×{vong} → coi như PASS (luật lean)"); break
        new = patch_hook(prof, chosen, viec)
        qc["patches"] += 1
        if check(new, prof, ctx):
            qc["log"].append(f"patch{vong} trượt tất định, giữ bản trước")
            new = chosen
        hop = [(chon, new)]
        cands_hop = f"=== HOOK {chon} ===\n{new}"
    qc["state"] = "PASS"
    (hd / "hook_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = khoa(d, text, mode=mode, extra={"sol_rounds": qc["sol_rounds"], "patches": qc["patches"],
                                          "source_video_id": src.get("video_id")})
    print(f"[H4] HOOK_LOCKED {meta['chars']} chữ · sol {qc['sol_rounds']} vòng · vá {qc['patches']}")
    return text
```

- [ ] **Step 4: Chạy → PASS**

- [ ] **Step 5: Commit** `feat(hook): viết 3 hook, Sol chọn, vá ≤2, LOCK`

---

### Task 8: `_pass1_prompt(hook_locked)` + `extract_beats` Beat 0

**Files:**
- Modify: `pipeline/ai_steps.py:294-360` (`_pass1_prompt`), `:891-918` (`extract_beats`)
- Test: `pipeline/tests/test_hook_wiring.py`

**Interfaces (Produces):**
```python
HOOK_LOCK_BLOCK = "..."   # format(hook=)
def _pass1_prompt(prof, competitor, minutes, series_ctx, ask_chars=0, comment_insight=None, budget_block=None, hook_locked="")
def extract_beats(prof, competitor, n=10, hook_locked="")   # trả text; nếu hook_locked: dòng đầu là JSON beat0 + "N00. [HOOK — ĐÃ KHOÁ] ..."
```

- [ ] **Step 1: Test thất bại**

```python
# pipeline/tests/test_hook_wiring.py
import json, pytest
import ai_steps

PROF = {"id": "x", "language": "ja", "voice": {"char_rate": 300.0}, "script": {}, "narrator": {}}


def test_pass1_prompt_co_khoi_hook():
    p = ai_steps._pass1_prompt(PROF, "KHUNG", 20, "", budget_block="2) ...", hook_locked="HOOK文。")
    assert "PHẦN MỞ ĐẦU ĐÃ KHOÁ" in p and "HOOK文。" in p
    assert p.index("PHẦN MỞ ĐẦU ĐÃ KHOÁ") < p.index("KHUNG SỰ KIỆN CẦN ĐI THEO")
    assert "PHẦN MỞ ĐẦU ĐÃ KHOÁ" not in ai_steps._pass1_prompt(PROF, "KHUNG", 20, "", budget_block="2)")


def test_extract_beats_beat0(monkeypatch):
    monkeypatch.setattr(ai_steps, "_writer_chat", lambda prof, ask, **k: type("R", (), {"text": "N01. a\nN02. b", "provider": "p", "model": "m", "elapsed": 0})())
    out = ai_steps.extract_beats(PROF, "transcript", hook_locked="HOOK文。")
    first, rest = out.split("\n", 1)
    assert json.loads(first)["beat0"]["locked"] is True
    assert rest.startswith("N00. [HOOK — ĐÃ KHOÁ] HOOK文。") and "N01. a" in rest
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt**

Thêm hằng (gần `LANG_NAME`):

```python
HOOK_LOCK_BLOCK = (
    "PHẦN MỞ ĐẦU ĐÃ KHOÁ — chép NGUYÊN VĂN làm đoạn ĐẦU TIÊN của bản kể, không đổi một chữ, không thêm gì phía trước:\n"
    "{hook}\n"
    "Viết phần còn lại NỐI TỰ NHIÊN từ câu cuối của đoạn trên: KHÔNG kể lại thông tin đoạn trên vừa nói, KHÔNG mở lại câu "
    "chuyện từ đầu (không tả thời tiết/mùa/giới thiệu kênh), KHÔNG giới thiệu tên-tuổi-nghề người kể trước khi câu chuyện "
    "cần đến; câu hỏi mà đoạn trên để ngỏ phải được TRẢ ở đúng chỗ khung sự kiện quy định, không trả ngay lập tức.")
```

`_pass1_prompt(..., hook_locked="")`: ngay trước `parts += ["", "KHUNG SỰ KIỆN CẦN ĐI THEO:", competitor]` thêm:

```python
    if hook_locked:
        parts += ["", HOOK_LOCK_BLOCK.format(hook=hook_locked.strip())]
```

`extract_beats(prof, competitor, n=10, hook_locked="")`: thêm vào `rules` (sau dòng "Trả ĐÚNG {n} nhịp") khi có hook:

```python
    if hook_locked:
        rules.insert(2, "N00 = HOOK đã khoá (cho sẵn, KHÔNG viết lại). N01 là SETUP nối từ N00: không mô tả lại sự kiện N00; "
                        "nếu transcript mở bằng đúng sự kiện đó thì N01 bắt đầu từ SAU nó.\nN00 (tham khảo, không chép vào output): "
                        + hook_locked.strip())
```

và sau khi có `beats`:

```python
    if hook_locked:
        import hashlib
        head = json.dumps({"beat0": {"beat_type": "hook", "locked": True, "source": "hook_locked.txt",
                                     "sha256": hashlib.sha256(hook_locked.strip().encode("utf-8")).hexdigest()}}, ensure_ascii=False)
        beats = head + "\n" + "N00. [HOOK — ĐÃ KHOÁ] " + hook_locked.strip().replace("\n", " ") + "\n" + beats
    return beats
```

(`json` đã import ở đầu `ai_steps.py`; nếu chưa thì thêm.) Dòng JSON đầu + `N00.` cũng nằm trong "KHUNG SỰ KIỆN" đưa cho PASS 1 — đúng ý Beat 0 đã khoá; `strip_markers` KHÔNG áp lên khung nên `[HOOK — ĐÃ KHOÁ]` không bị xoá.

- [ ] **Step 4: Chạy → PASS**

- [ ] **Step 5: Commit** `feat(hook): S2 prompt khối hook khoá + extract_beats Beat 0`

---

### Task 9: Wire vào `lean_script.py`

**Files:**
- Modify: `pipeline/lean_script.py` — `viet()` (111), `do_tat_dinh()` (364), `PRESERVE` (453), `sol_qc()` (505), `run()` (530–575)
- Test: `pipeline/tests/test_hook_wiring.py`

**Interfaces:**
- Consumes: `hook_stage.ensure_locked`, `hook_stage.doc_hook`, `hook_stage.bat_dau_bang_hook`, `hook_stage.ke_lai_hook`, `qc_script_sol.NOI_TU_HOOK`, `ai_steps` Task 8.
- Produces: `viet(prof, competitor, ctx, minutes, ns, log, hook="")`; `do_tat_dinh(prof, text, ctx, competitor, minutes, hook="")` — thêm `viec_len` `"HOOK: script không bắt đầu bằng đoạn mở đầu đã khoá — chép lại nguyên văn hook làm đoạn đầu"` và warn `"thân kể lại hook (NN%)"` khi `ke_lai_hook > 0.5`; `sol_qc(prof, text, title, out, ns, m, hook="")`.

- [ ] **Step 1: Test thất bại**

```python
def test_do_tat_dinh_hook(monkeypatch):
    import lean_script as L, ai_steps
    monkeypatch.setattr(ai_steps, "check", lambda prof, text, minutes=None, tol=0.12: ([], {"chars": 100, "minutes": 1, "comma_per_sentence": 1, "chars_per_breath": 8, "dialogue_ratio": 0.1, "markers": []}))
    monkeypatch.setattr(ai_steps, "_go_cat_neu_ja", lambda prof, t: t)
    import profiles
    monkeypatch.setattr(profiles, "target_chars", lambda prof, minutes=None, speed=None: 100)
    hook = "「三年前に引っ越しました」隣人は言った。"
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {"gate": {}}}
    _, m, vf, vl, warn = L.do_tat_dinh(prof, "晩秋の風。\n\n" + hook, "", "", 1, hook=hook)
    assert any(v.startswith("HOOK:") for v in vl)
    _, m, vf, vl, warn = L.do_tat_dinh(prof, hook + "\n\n" + hook + "隣人はそう言った。", "", "", 1, hook=hook)
    assert not any(v.startswith("HOOK:") for v in vl) and any("kể lại hook" in w for w in warn)


def test_preserve_co_hook():
    import lean_script as L
    assert "hook" in L.PRESERVE.lower()
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt**

`import hook_stage` cạnh các import đầu file. `viet()`:

```python
def viet(prof, competitor: str, ctx: str, minutes: float, ns, log: list, hook: str = ""):
    ...
        source = ai_steps.extract_beats(prof, competitor, hook_locked=hook)
    ...
    prompt = ai_steps._pass1_prompt(prof, source, minutes, ctx_prompt, budget_block=budget_block(ns), hook_locked=hook)
```

`do_tat_dinh(prof, text, ctx, competitor, minutes, hook="")` — sau `warn += _bam_goc(...)`:

```python
    if hook:
        if not hook_stage.bat_dau_bang_hook(text, hook):
            viec_len.append("HOOK: script không bắt đầu bằng đoạn mở đầu đã khoá — chép lại NGUYÊN VĂN hook làm đoạn đầu, "
                            "xoá mọi đoạn đứng trước nó")
        kl = hook_stage.ke_lai_hook(text, hook)
        if kl > 0.5:
            warn.append(f"thân kể lại hook ({kl:.0%} bigram hook xuất hiện lại ngay sau hook) — nối tiếp, đừng nhắc lại")
    if not hook:
        warn.append("chưa có hook đã khoá (tập cũ?) — cổng mở đầu do hook_stage đảm nhận, chạy `hook_stage.py --mode repair`")
```

`PRESERVE`: thêm `"· ĐOẠN MỞ ĐẦU ĐÃ KHOÁ (hook, đoạn đầu tiên) — giữ nguyên từng chữ, không thêm gì phía trước "` trước `KHÔNG thêm tình tiết`.

`sol_qc(prof, text, title, out, ns, m, hook="")`: `return qc_script_sol.run(text, title, profile_id=prof["id"], out=str(out), extra_note=note, hook_block=(qc_script_sol.NOI_TU_HOOK.format(hook=hook) if hook else ""))`.

`run()`: sau `print(f"[S1Q] ✓ hồ sơ đủ ...")` và trước `# ---- S2`:

```python
    # ---- H1–H4 (hook thượng nguồn, anh chốt 2026-09-23) — chỉ khi S2 sắp VIẾT MỚI; tập đã có script + lock → repair mode riêng
    sf = d / "script.txt"
    co_lock = (d / gate_common.LOCK_NAME).exists()
    se_viet_moi = force or not (sf.exists() and ((job.state.get("B3") or {}).get("flow") == "lean" or co_lock))
    if se_viet_moi:
        hook = hook_stage.ensure_locked(d, prof, ctx=ctx, title=_title(d), mode="upstream", force=force)
        bench["hook_sol_rounds"] = (hook_stage.doc_lock(d) or {}).get("sol_rounds", 0)
    else:
        hook = hook_stage.doc_hook(d)
        if not hook:
            print("[H4] ⚠️ tập đã có script.txt mà chưa có hook — dùng `py -3.13 hook_stage.py --profile … --slug … --mode repair`")
```

Xoá 2 dòng `sf = ...`/`co_lock = ...` cũ ngay dưới `# ---- S2` (đã khai ở trên). Trong nhánh viết mới: `text = viet(prof, competitor, ctx, minutes, ns, log, hook=hook)`. `do_va_ghi`: `do_tat_dinh(prof, text, ctx, competitor, minutes, hook=hook)`. Mọi chỗ gọi `sol_qc(...)` thêm `hook=hook`.

- [ ] **Step 4: Chạy → PASS**; chạy trọn `py -3.13 -m pytest tests -q` (không gãy test cũ).

- [ ] **Step 5: Commit** `feat(hook): lean flow H1–H4 trước S2, S3 kiểm bắt đầu bằng hook, Sol mục nối từ hook`

---

### Task 10: Vá `mo_dau` ĐẠT giả · `Job.kiem_lock` STALE · `qc_final.kiem_hook` · `qc_hoso.kiem_hook_ho_so`

**Files:**
- Modify: `pipeline/qc_script.py:101-148`, `pipeline/make_video.py` (`Job.kiem_lock`), `pipeline/qc_final.py` (`kiem`), `pipeline/qc_hoso.py` (`main` + hàm mới)
- Test: `pipeline/tests/test_hook_wiring.py`

**Interfaces (Produces):**
- `qc_script.mo_dau(text, gate, marker="第1章", warn_no_marker=False)` → khi không có marker và `warn_no_marker=True` trả `[{"kind":"mo_dau_khong_do","sev":"thap","msg":...}]`.
- `qc_final.kiem_hook(S, prof, ra)`: thiếu `hook/hook_lock.json` → `cao`; stale → `cao`; mode upstream mà `script.txt` không bắt đầu bằng hook → `cao`; mode repair mà thiếu `hook/hook_final.mp4` → `cao`; `promise.title != title.txt` → `cao`.
- `qc_hoso.kiem_hook_ho_so(kq, ctx_text, prof)`: thiếu tiêu mục `HOOK 30 GIÂY ĐẦU:` → `nang`; nội dung không có neo (regex `hook_stage.NEO`) → `nang`; dài > 2×`so_chu_muc_tieu` → `nhe`.

- [ ] **Step 1: Test thất bại**

```python
def test_mo_dau_warn_no_marker():
    import qc_script as Q
    assert Q.mo_dau("không marker", {}) == []
    r = Q.mo_dau("không marker", {}, warn_no_marker=True)
    assert r and r[0]["kind"] == "mo_dau_khong_do"


def test_qc_final_kiem_hook(tmp_path):
    import qc_final as F, hook_stage as HS
    (tmp_path / "title.txt").write_text("T", encoding="utf-8")
    (tmp_path / "script.txt").write_text("khác。", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert any("hook_lock" in x["msg"] for x in ra)
    HS.khoa(tmp_path, "hook。")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert any("không bắt đầu" in x["msg"] for x in ra)
    (tmp_path / "script.txt").write_text("hook。thân。", encoding="utf-8")
    ra = []
    F.kiem_hook(tmp_path, {"id": "x"}, ra)
    assert ra == []


def test_qc_hoso_kiem_hook(tmp_path):
    import qc_hoso as H
    prof = {"id": "x", "language": "ja", "voice": {"char_rate": 300}, "script": {}}
    kq = []
    H.kiem_hook_ho_so(kq, "TIÊU ĐỀ\n① a\n", prof)
    assert any(x["ma"] == "hook_thieu" for x in kq)
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK 30 GIÂY ĐẦU:\nそれは不思議だった。\n\nKHUNG N CHƯƠNG:", prof)
    assert any(x["ma"] == "hook_noi_suong" for x in kq)
    kq = []
    H.kiem_hook_ho_so(kq, "HOOK 30 GIÂY ĐẦU:\n1978年10月21日、セスナが消えた。\n\nKHUNG N CHƯƠNG:", prof)
    assert kq == []
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt**

`qc_script.mo_dau`:

```python
def mo_dau(text, gate, marker="第1章", warn_no_marker=False):
    ...
    if not pos:
        if warn_no_marker:
            return [{"kind": "mo_dau_khong_do", "sev": "thap",
                     "msg": "lane không có marker chương/mục → cổng mở đầu KHÔNG đo được ở đây (trước 2026-09-23 là ĐẠT giả); "
                            "mở đầu do hook_stage kiểm"}]
        return []
```

`lean_script.do_tat_dinh` gọi `qc_script.mechanical(text, lang, g)` — `mechanical` gọi `mo_dau(text, gate)`; thêm tham số xuyên: `def mechanical(text, lang="ja", gate=None, warn_no_marker=False)` → `mo_dau(text, gate or {}, warn_no_marker=warn_no_marker)`; lean truyền `warn_no_marker=True` và map `"mo_dau_khong_do"` vào danh sách warn (dòng 443).

`make_video.Job.kiem_lock(self, buoc)` — sau `print(f"[{buoc}] lock: {msg}")`:

```python
        import hook_stage
        stale, ly_do = hook_stage.kiem_stale(self.dir)
        if stale:
            raise SystemExit(f"✗ {buoc}: HOOK_STALE — " + " · ".join(ly_do))
        if ly_do:   # ["chưa có hook lock"]
            print(f"[{buoc}] ⚠️ {ly_do[0]} — tập cũ: chạy hook_stage.py --mode repair trước khi giao")
```

`qc_final.kiem_hook`:

```python
def kiem_hook(S: Path, prof, ra):
    """Mọi tập phải có hook khoá (anh chốt 2026-09-23). upstream: script bắt đầu bằng hook; repair: có hook_final.mp4."""
    import hook_stage
    m = hook_stage.doc_lock(S)
    if not m:
        _loi(ra, "hook", "cao", "thiếu hook/hook_lock.json — tập chưa có hook 20–30s", "chạy hook_stage.py (--mode repair nếu tập đã có script)")
        return
    stale, ly_do = hook_stage.kiem_stale(S)
    if stale:
        _loi(ra, "hook", "cao", "HOOK_STALE: " + " · ".join(ly_do), "chạy lại H1–H4 (hook_stage.py --force)")
    hook = hook_stage.doc_hook(S)
    if m.get("mode") == "repair":
        if not (S / "hook" / "hook_final.mp4").exists():
            _loi(ra, "hook", "cao", "repair mode nhưng chưa có hook/hook_final.mp4", "bước 3 dựng hook_final.mp4 rồi final_with_hook.mp4")
    else:
        sc = (S / "script.txt").read_text(encoding="utf-8") if (S / "script.txt").exists() else ""
        if not hook_stage.bat_dau_bang_hook(sc, hook):
            _loi(ra, "hook", "cao", "script.txt không bắt đầu bằng hook đã khoá", "S3 phải bắt lỗi này — kiểm lại lean_script")
    t = hook_stage._title(S)
    if t and (m.get("promise") or {}).get("title") not in ("", t):
        _loi(ra, "hook", "cao", f"title.txt ≠ title lúc khoá hook ({(m.get('promise') or {}).get('title')!r})", "HOOK_STALE — khoá lại")
```

Gọi trong `kiem()` sau `kiem_du_kien(S, ra)`: `kiem_hook(S, prof, ra)`.

`qc_hoso.kiem_hook_ho_so`:

```python
def kiem_hook_ho_so(kq, ctx_text, prof):
    """Trường 'HOOK 30 GIÂY ĐẦU:' của hồ sơ (docs/KHUON_HO_SO_DE_TAI.md) — trước 2026-09-23 không ai kiểm."""
    import hook_stage
    m = re.search(r"HOOK 30 GIÂY ĐẦU\s*[:：]\s*\n(.*?)(?=\n\s*\n|\n[A-ZĐ][A-ZĐ ]{3,}[:：]|\Z)", ctx_text, re.S)
    if not m or not m.group(1).strip():
        _ra(kq, "nang", "hook_thieu", "hồ sơ không có tiêu mục 'HOOK 30 GIÂY ĐẦU:' hoặc để trống",
            "bên research phải viết 1–2 câu hook: sự kiện cụ thể, neo NGÀY/NƠI/NGƯỜI, không kết luận suông")
        return
    h = m.group(1).strip()
    if not hook_stage.NEO.search(h):
        _ra(kq, "nang", "hook_noi_suong", f"hook hồ sơ không có neo cụ thể (số/tên/thoại): {h[:60]}…",
            "thêm mốc ngày/nơi/người hoặc câu thoại")
    if len(h) > 2 * hook_stage.so_chu_muc_tieu(prof):
        _ra(kq, "nhe", "hook_qua_dai", f"hook hồ sơ {len(h)} ký tự — dài hơn 2×30 giây đọc")
```

Gọi trong `main()` ngay sau `kiem_tieu_de(kq, text, rs, gate)`: `kiem_hook_ho_so(kq, text, prof)`.

- [ ] **Step 4: Chạy → PASS**; chạy trọn bộ test.

- [ ] **Step 5: Commit** `feat(hook): cổng hook ở B10/B0, STALE chặn pha asset, mo_dau hết ĐẠT giả`

---

### Task 11: `hook_storyboard.py` — 4–7 shot + flow prompts + jobs.csv Grok

**Files:**
- Create: `pipeline/hook_storyboard.py`
- Test: `pipeline/tests/test_hook_storyboard.py`

**Interfaces:**
- Consumes: `hook_stage.doc_hook/doc_lock`, `characters.json` (khoá `world`, `characters[].name/role/...`), `ai_steps._writer_chat`, `profiles.char_rate`.
- Produces:
```python
def validate(sb: dict, hook: str, char_rate: float) -> list[str]   # [] = hợp lệ
def sinh(d, prof, force=False) -> dict     # ghi hook/hook_storyboard.json, hook/flow_prompts/shot_NN.txt, hook/grok_jobs.csv
```
Schema `hook_storyboard.json`: `{"hook_sha256", "duration_target_s", "shots":[{"n","t0","t1","voice","visual","shot_type","ref_image","flow_prompt","continuity"}]}`. `grok_jobs.csv` cột `id,image,prompt,duration,resolution,aspect` (đúng `E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py --jobs`), `image` = `hook/img/shot_NN.png` (máy 2 vẽ), `duration` ∈ {6,10,15} làm tròn lên từ `t1-t0`.

- [ ] **Step 1: Test thất bại**

```python
# pipeline/tests/test_hook_storyboard.py
import json
import hook_storyboard as SB

HOOK = "「三年前に引っ越しました」隣人は言った。五十年の友が消えた。私は箱を抱えたまま立ち尽くした。理由は後で知った。"


def _sb(n=5, total=25.0):
    step = total / n
    voice_parts = ["「三年前に引っ越しました」隣人は言った。", "五十年の友が消えた。", "私は箱を抱えたまま立ち尽くした。", "理由は後で知った。", "理由は後で知った。"][:n]
    return {"shots": [{"n": i + 1, "t0": round(i * step, 1), "t1": round((i + 1) * step, 1), "voice": voice_parts[i % len(voice_parts)],
                       "visual": "v", "shot_type": "close-up", "ref_image": "REF", "flow_prompt": "p", "continuity": "c"} for i in range(n)]}


def test_validate_ok():
    assert SB.validate(_sb(), HOOK, 300.0) == []


def test_validate_bat_loi():
    assert any("4–7" in e for e in SB.validate(_sb(3), HOOK, 300.0))
    assert any("20–30" in e for e in SB.validate(_sb(5, 45.0), HOOK, 300.0))
    bad = _sb(); bad["shots"][0]["voice"] = "文なし"
    assert any("voice" in e for e in SB.validate(bad, HOOK, 300.0))
    bad = _sb(); bad["shots"][2]["t0"] = 99
    assert any("liên tục" in e for e in SB.validate(bad, HOOK, 300.0))


def test_jobs_csv(tmp_path):
    (tmp_path / "hook").mkdir()
    sb = _sb()
    SB.ghi_flow_prompts_va_jobs(tmp_path, sb)
    rows = (tmp_path / "hook/grok_jobs.csv").read_text(encoding="utf-8-sig").splitlines()
    assert rows[0] == "id,image,prompt,duration,resolution,aspect" and len(rows) == 6
    assert rows[1].split(",")[3] == "6"
    assert (tmp_path / "hook/flow_prompts/shot_01.txt").exists()
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt `pipeline/hook_storyboard.py`**

```python
"""hook_storyboard.py — chia hook đã khoá thành 4–7 shot (SOP §11–13), xuất prompt Google Flow/Grok từng shot + jobs.csv.
Claude Code (bước 1) chạy sau HOOK_LOCKED; máy 2/agent bước 3 vẽ ảnh shot + sinh clip + ghép (docs/GIAO_VIEC_BUOC3_AGENT.md)."""
import argparse, csv, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_steps, hook_stage, profiles  # noqa: E402

PROMPT = """Chia đoạn HOOK dưới đây thành 4–7 SHOT cho 20–30 giây đầu video (kể chuyện, ảnh AI → clip 6/10/15s).
HOOK (đã khoá, không đổi chữ): {hook}
Tốc độ đọc: {cr:.0f} chữ/phút → tổng ≈ {tong:.0f} giây.
THẾ GIỚI / NHÂN VẬT (characters.json — giữ continuity, nhân vật chính mặt khoá REF):
{chars}
Luật: mỗi shot 3–6 s, 1 ý, 1 hành động, 1 điểm nhấn; shot mới phải THÊM thông tin (reveal/reaction/detail/memory/contrast);
ưu tiên close-up ở cảm xúc (mắt, tay, vật, cửa, giấy); motion nhỏ (push-in, rack focus, tay siết, cửa mở); hình bám đúng
câu voice của shot; KHÔNG spoil reveal bằng hình; không text trên hình. `voice` mỗi shot = đoạn con NGUYÊN VĂN của HOOK,
ghép lại đúng thứ tự phải ra đủ HOOK. `flow_prompt` tiếng Anh, 11 mục: SUBJECT / AGE-FACE-CLOTHING / LOCATION / ACTION /
EMOTION / CAMERA / LIGHTING / MOVEMENT / DURATION / CONTINUITY / NEGATIVE (no text, no subtitles, no distorted hands).
Trả ĐÚNG 1 JSON: {{"shots": [{{"n":1,"t0":0.0,"t1":4.0,"voice":"...","visual":"1 câu tiếng Việt","shot_type":"close-up|medium|wide|reaction|detail|establishing|memory","ref_image":"REF|REF2|none","flow_prompt":"...","continuity":"..."}}]}}"""


def validate(sb, hook, char_rate):
    loi = []
    shots = sb.get("shots") or []
    if not 4 <= len(shots) <= 7:
        loi.append(f"cần 4–7 shot, có {len(shots)}")
    if shots:
        tong = shots[-1]["t1"] - shots[0]["t0"]
        if not 18 <= tong <= 32:
            loi.append(f"tổng {tong:.1f}s ngoài 20–30s (dung sai ±2)")
        for i, s in enumerate(shots):
            if s["t1"] - s["t0"] < 2.5 or s["t1"] - s["t0"] > 6.5:
                loi.append(f"shot {s['n']} dài {s['t1']-s['t0']:.1f}s ngoài 3–6s")
            if i and abs(s["t0"] - shots[i - 1]["t1"]) > 0.05:
                loi.append(f"shot {s['n']} không liên tục với shot trước")
            if hook_stage._sach(s.get("voice", "")) and hook_stage._sach(s["voice"]) not in hook_stage._sach(hook):
                loi.append(f"shot {s['n']} voice không phải đoạn nguyên văn của hook")
        ghep = hook_stage._sach("".join(s.get("voice", "") for s in shots))
        if ghep != hook_stage._sach(hook):
            loi.append("ghép voice các shot ≠ hook (thiếu/thừa/lặp câu)")
    return loi


def ghi_flow_prompts_va_jobs(d, sb):
    d = Path(d); fp = d / "hook" / "flow_prompts"; fp.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in sb["shots"]:
        (fp / f"shot_{s['n']:02d}.txt").write_text(s.get("flow_prompt", ""), encoding="utf-8")
        dur = s["t1"] - s["t0"]
        rows.append({"id": f"shot_{s['n']:02d}", "image": f"hook/img/shot_{s['n']:02d}.png", "prompt": s.get("flow_prompt", ""),
                     "duration": 6 if dur <= 6 else 10 if dur <= 10 else 15, "resolution": "720p", "aspect": "16:9"})
    with (d / "hook" / "grok_jobs.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "image", "prompt", "duration", "resolution", "aspect"])
        w.writeheader(); w.writerows(rows)


def sinh(d, prof, force=False):
    d = Path(d)
    hook = hook_stage.doc_hook(d)
    lock = hook_stage.doc_lock(d)
    if not hook or not lock:
        raise SystemExit("✗ chưa có hook khoá — chạy hook_stage.py trước")
    out = d / "hook" / "hook_storyboard.json"
    if out.exists() and not force:
        sb = json.loads(out.read_text(encoding="utf-8"))
        if sb.get("hook_sha256") == lock["sha256"]:
            return sb
    cr = profiles.char_rate(prof)
    chars = (d / "characters.json").read_text(encoding="utf-8")[:4000] if (d / "characters.json").exists() else "(chưa có characters.json — mô tả nhân vật theo hook)"
    prompt = PROMPT.format(hook=hook, cr=cr, tong=ai_steps.measure(hook)["chars"] / cr * 60, chars=chars)
    sb = None
    for lan in range(3):
        r = ai_steps._writer_chat(prof, prompt, task="short", max_chars=20000)
        try:
            sb = json.loads(re.sub(r"^```[a-z]*\n?|\n?```$", "", r.text.strip()))
        except Exception as e:
            print(f"  ! JSON storyboard hỏng lần {lan+1}: {e}"); continue
        loi = validate(sb, hook, cr)
        if not loi:
            break
        print(f"  ! storyboard lần {lan+1}: " + " · ".join(loi))
        prompt = prompt + "\n\nLẦN TRƯỚC SAI: " + " · ".join(loi) + " — sửa đúng."
    else:
        raise SystemExit("✗ storyboard không hợp lệ sau 3 lần — người xem hook/hook_storyboard.err.json")
    sb["hook_sha256"] = lock["sha256"]
    sb["duration_target_s"] = round(sb["shots"][-1]["t1"], 1)
    out.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")
    ghi_flow_prompts_va_jobs(d, sb)
    print(f"[STORYBOARD] {len(sb['shots'])} shot · {sb['duration_target_s']}s → {out}")
    return sb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True); ap.add_argument("--slug", required=True); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    prof = profiles.load(a.profile)
    d = Path(__file__).resolve().parent.parent / (prof.get("slug_dir") or "assets/out") / a.slug
    sinh(d, prof, force=a.force)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Chạy → PASS**

- [ ] **Step 5: Commit** `feat(hook): storyboard 4–7 shot + flow prompts + grok jobs.csv`

---

### Task 12: Repair mode + CLI `hook_stage.py`

**Files:**
- Modify: `pipeline/hook_stage.py` (thêm `main()`)
- Test: `pipeline/tests/test_hook_stage.py`

**Interfaces (Produces):** CLI
```
py -3.13 hook_stage.py --profile <lane> --slug <tập> [--mode upstream|repair] [--force] [--only source] [--proxy ...]
```
`--mode repair`: bắt buộc có `script.txt`; `ensure_locked(..., mode="repair")` (Task 7 đã xử lý `KHOI_REPAIR`, promise = script); sau lock gọi `hook_storyboard.sinh()`; in 3 dòng: đường dẫn `hook_locked.txt`, `hook_storyboard.json`, `grok_jobs.csv`. `--only source` chỉ chạy `phan_tich_nguon` (nghiệm thu H1–H3).

- [ ] **Step 1: Test thất bại**

```python
def test_cli_repair_yeu_cau_script(tmp_path, monkeypatch, capsys):
    import profiles
    monkeypatch.setattr(profiles, "load", lambda pid: {**PROF, "slug_dir": str(tmp_path.relative_to(tmp_path.parent.parent)) if False else "assets/_t"})
    monkeypatch.setattr(HS, "ROOT", tmp_path)
    (tmp_path / "assets/_t/ep").mkdir(parents=True)
    with pytest.raises(SystemExit) as e:
        HS.main(["--profile", "x", "--slug", "ep", "--mode", "repair"])
    assert "script.txt" in str(e.value)
```

- [ ] **Step 2: Chạy → FAIL**

- [ ] **Step 3: Cài đặt (cuối `hook_stage.py`)**

```python
ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    ap = argparse.ArgumentParser(description="H1–H4 hook 20–30s (upstream) hoặc repair mode cho tập đã có script")
    ap.add_argument("--profile", required=True); ap.add_argument("--slug", required=True)
    ap.add_argument("--mode", default="upstream", choices=["upstream", "repair"])
    ap.add_argument("--force", action="store_true"); ap.add_argument("--only", default="", choices=["", "source"])
    ap.add_argument("--proxy", default="")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    d = ROOT / (prof.get("slug_dir") or "assets/out") / a.slug
    if not d.exists():
        raise SystemExit(f"✗ không thấy thư mục tập {d}")
    if a.mode == "repair" and not (d / "script.txt").exists():
        raise SystemExit(f"✗ repair mode cần {d / 'script.txt'} đã có")
    if a.only == "source":
        src = phan_tich_nguon(d, prof, proxy=a.proxy or None, force=a.force)
        print(json.dumps({k: src[k] for k in ("video_id", "hook_kind", "score_0_12", "video_hook_verdict", "promise_match")},
                         ensure_ascii=False, indent=1))
        return
    ctx = (d / "series_ctx.txt").read_text(encoding="utf-8") if (d / "series_ctx.txt").exists() else ""
    ensure_locked(d, prof, ctx=ctx, title=_title(d), mode=a.mode, force=a.force, proxy=a.proxy or None)
    import hook_storyboard
    hook_storyboard.sinh(d, prof, force=a.force)
    for f in ("hook_locked.txt", "hook_storyboard.json", "grok_jobs.csv"):
        print(f"  → {d / HOOK_DIR / f}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Chạy → PASS**; chạy trọn bộ `py -3.13 -m pytest tests -q`.

- [ ] **Step 5: Commit** `feat(hook): repair mode + CLI`

---

### Task 13: Spec bước 3 — TTS hook (repair), clip Grok, `hook_final.mp4`, `final_with_hook.mp4`

**Files:**
- Modify: `docs/GIAO_VIEC_BUOC3_AGENT.md` (thêm `## 9. HOOK 20–30S ĐẦU VIDEO` trước checklist §8) 
- Không code compositor (luật Claude Code chỉ bước 1). Agent bước 3 code `pipeline/ghep_hook.py` theo spec dưới, có test đếm khung.

- [ ] **Step 1: Viết mục 9 vào `docs/GIAO_VIEC_BUOC3_AGENT.md`** với nội dung:

```markdown
## 9. HOOK 20–30S ĐẦU VIDEO (mọi lane, từ 2026-09-23)

Đầu vào (bước 1 đã để sẵn trong `<tập>\hook\`): `hook_locked.txt` · `hook_lock.json` (`mode` upstream|repair) ·
`hook_storyboard.json` · `flow_prompts\shot_NN.txt` · `grok_jobs.csv`. Thiếu bất kỳ file nào → DỪNG, báo lane.

9.1 Ảnh shot: vẽ `hook\img\shot_NN.png` (1280×720, 16:9) theo `flow_prompts\shot_NN.txt`; `ref_image=REF/REF2` → REF-LOCK
    bằng master trong `_ref\` (ima2 `--ref`), giống quy trình ảnh thân video. 4–7 ảnh.
9.2 Clip: `python E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py --jobs <tập>\hook\grok_jobs.csv --out <tập>\hook\clips --gap 5`
    (profile Grok port 9334; lỗi 429/403 xem skill grok_video.md). Fallback khi Grok chết: dùng ảnh tĩnh + `--zoom 1.0`
    qua `ghep_anh_co_chuyen_canh.py` với timeline = t0/t1 của storyboard (V3 trong docs/PHUONG_AN_HOOK_VIDEO.md).
9.3 Voice hook:
    - upstream: KHÔNG làm gì — hook nằm trong `voice.mp3` chung (là đoạn đầu). Lấy mốc kết thúc hook = cue SRT cuối cùng có
      text thuộc hook (`voice_paced.srt`), gọi `T_hook`.
    - repair: `py -3.13 tts.py --script <tập>\hook\hook_locked.txt --out <tập>\hook\hook_voice.mp3 --profile <lane>`
      (cùng voice/speed/fx của profile) → `hook_voice.mp3` + `.srt`; `T_hook` = thời lượng mp3.
9.4 Dựng `hook\hook_final.mp4` (FF = imageio_ffmpeg.get_ffmpeg_exe(), 1920×1080 30fps h264 yuv420p, giống final.mp4):
    - Với mỗi shot n: cắt clip `clips\shot_NN.mp4` đúng `t1-t0` giây (`-ss 0 -t <dur>`), scale/pad 1920×1080.
      Clip ngắn hơn `dur` → `tpad=stop_mode=clone:stop_duration=<thiếu>`.
    - Nối theo concat demuxer; giữa shot dùng crossfade 12 khung (xfade `offset` = tổng trước − 0.4) — công thức trong
      skill video-chuyen-canh (xfade trả d−1 khung: cấp d+1 rồi `-frames:v`).
    - Tổng khung phải = round(T_hook × 30) ± 15; thừa → cắt shot cuối; thiếu → clone khung cuối.
    - Âm: repair → `hook_voice.mp3`; upstream → không ghép tiếng (tiếng nằm trong thân). Nhạc nền hook: cùng BGM thân
      nhưng −6 dB, fade-in 1 s; SFX không bắt buộc (không whoosh trailer).
9.5 Ghép vào thân:
    - upstream: `final.mp4` đã chứa đoạn hook bằng ảnh tĩnh ở 0–T_hook → THAY đoạn đó: `final_with_hook.mp4` =
      `hook_final.mp4` (video) + `final.mp4` từ `T_hook` (video) với audio LẤY NGUYÊN của `final.mp4` từ 0 (không cắt tiếng),
      chuyển cảnh mờ-vào 10 khung tại mốc T_hook.
    - repair: `final_with_hook.mp4` = `hook_final.mp4` (có tiếng) + crossfade 17 khung + `final.mp4` nguyên vẹn.
    - Xuất CẠNH `final.mp4`, KHÔNG ghi đè. Phụ đề: repair → nối `hook_voice.srt` + dịch mọi mốc `voice_paced.srt` thêm
      T_hook + 17/30 s → `final_with_hook.srt`.
9.6 Nghiệm thu: đếm khung `final_with_hook.mp4` = khung(hook_final) + khung(final từ T_hook) − khung chuyển cảnh;
    `qc_visual.kiem_tieng_ghep` không báo mất tiếng; xem tay 30 s đầu: 4–7 bố cục, không chữ AI, mặt nhân vật khớp REF;
    ghi `hook\render_info.json` {T_hook, frames, mode}. Cột G sheet trỏ tới `final_with_hook.mp4`.
```

- [ ] **Step 2: Kiểm tài liệu**: `grep -n "## 9. HOOK" E:\CLAUDE\YOUTUBE\h2dev\docs\GIAO_VIEC_BUOC3_AGENT.md` → 1 dòng.

- [ ] **Step 3: Commit** `docs(hook): spec bước 3 dựng hook_final + final_with_hook`

---

### Task 14: Tài liệu + field profile

**Files:**
- Modify: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` (thêm `### 2b. H1–H4 HOOK — bắt buộc trước S2` sau §2), `CLAUDE.md` (2 dòng), `docs/SOP_SATORI_JP.md`, `docs/SOP_TOSHI_DENSETSU_JP.md`, `docs/SOP_LANE_D.md`, `docs/SOP_LANE_E.md`, `docs/SOP_LANE_F.md`, `docs/SOP_LANE_G.md` (mỗi file 1 dòng), `docs/BAT_DAU_LANE/*.md` (1 dòng), `docs/PHUONG_AN_HOOK_VIDEO.md` (đổi trạng thái → "ĐÃ DUYỆT, plan: docs/superpowers/plans/2026-09-23-hook-video.md").

- [ ] **Step 1: §2b trong QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md**

```markdown
### 2b. H1–H4 HOOK 20–30 GIÂY — bắt buộc TRƯỚC S2 (anh chốt 2026-09-23, mọi lane)
`lean_script.run()` tự gọi `hook_stage.ensure_locked()` sau S1Q. Cần thêm trong thư mục tập:
| File | Bắt buộc | Ghi chú |
|---|---|---|
| `competitor.segments.json` | lane nhân bản 1 video | `fetch_script.py` sinh kèm `competitor.txt` (có title/description/thumbnail nguồn) |
| `hook/promise.txt` | khuyến nghị | 4–6 dòng `core_event:/payoff:/reveal:/timeline_start:` — HOOK_STALE so theo file này thay vì hash cả `series_ctx.txt` |
| `thumb_text.txt` | nếu đã có | Sol chấm THUMB_MATCH |
Sinh ra: `hook/source.json` (H1–H3) · `hook_candidates.txt` · `hook_qc.json` · `hook_locked.txt` + `hook_lock.json` (H4) ·
`hook_storyboard.json` + `flow_prompts/` + `grok_jobs.csv` (chạy `py -3.13 hook_storyboard.py --profile <lane> --slug <tập>` sau LOCK).
Lớp 3 (Claude Code) đọc `hook_locked.txt` 2 phút trước khi S2 chạy tiếp: kiểm 4 nhịp + khớp title. Sửa hook = sửa TRƯỚC S2;
sau khi script đã LOCK mà đổi title/thumb/promise → HOOK_STALE chặn ở pha asset, chạy `hook_stage.py --force` rồi S2 lại.
Field profile (tuỳ chọn, mặc định trong `hook_stage.MAC_DINH`): `script.hook = {"ratio_30s":0.5,"tol":0.15,"neo_ratio":0.4,"banned_openers":[...]}`.
Tập đã có script (chưa đăng): `py -3.13 hook_stage.py --profile <lane> --slug <tập> --mode repair` — không đụng script/voice/img;
bước 3 dựng `hook_final.mp4` + `final_with_hook.mp4` theo `docs/GIAO_VIEC_BUOC3_AGENT.md` §9.
```

- [ ] **Step 2: `CLAUDE.md`** — trong mục "📝⭐ QUY TRÌNH TẠO KỊCH BẢN CHUẨN MỌI LANE" thêm 1 dòng:
`**HOOK 20–30s bắt buộc mọi tập (2026-09-23):** khoá TRƯỚC S2 bằng `pipeline/hook_stage.py`, đọc `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b; phương án gốc `docs/PHUONG_AN_HOOK_VIDEO.md`.`
Trong mục "🎞️ CHUYỂN CẢNH" thêm 1 dòng: `Ngoại lệ hook: 20–30s đầu là CLIP sinh sẵn (Grok/Veo) theo storyboard — không phải zoom/pan giả trên ảnh, không vi phạm luật ảnh tĩnh.`

- [ ] **Step 3: Mỗi SOP lane + BAT_DAU_LANE** thêm 1 dòng đầu mục quy trình: `⚠️ Hook 20–30s bắt buộc trước S2 — xem QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md §2b.`

- [ ] **Step 4: Kiểm** `grep -ln "§2b" docs/SOP_*.md docs/BAT_DAU_LANE/*.md CLAUDE.md | wc -l` ≥ 10.

- [ ] **Step 5: Commit** `docs(hook): §2b quy trình + router CLAUDE.md + SOP mỗi lane`

---

### Task 15: Pilot (sau khi mọi test PASS) — 1 tập mới + 1 repair

Chỉ chạy khi Task 1–14 xong và `py -3.13 -m pytest tests -q` toàn PASS. Đây là bước "test thử cho 1 video" anh yêu cầu.

- [ ] **Step 1: Test hồi quy promise trên tập thật** (không tốn LLM viết): `py -3.13 hook_stage.py --profile teinengo-tanoshimi --slug ep09-toshokan --only source`
Expected: in `promise_match` của nguồn; ghi nhận `score_0_12`.

- [ ] **Step 2: Tập mới Lane G** — tạo hồ sơ S1 tập kế tiếp theo `docs/BAT_DAU_LANE/teinengo-tanoshimi.md` (competitor.txt + `competitor.segments.json` bằng `fetch_script.py`, series_ctx.txt, title.txt, `hook/promise.txt`), rồi:
`py -3.13 make_video.py --profile teinengo-tanoshimi --slug <epNN-slug> --den B3`
Expected trong log: `[H1-H3] …`, `[H4] HOOK_LOCKED …`, `[S2] Fable viết …`, S3 KHÔNG có việc `HOOK:`, Sol PASS/FIX với mục 7 "NỐI TỪ HOOK" không SAI, `script.lock.json` state PASS. Lớp 3: đọc `hook/hook_locked.txt` + 3 đoạn đầu `script.txt`, xác nhận không reset/kể lại.
Sau đó: `py -3.13 hook_storyboard.py --profile teinengo-tanoshimi --slug <epNN-slug>` → 4–7 shot, `grok_jobs.csv`.

- [ ] **Step 3: Repair satori ep14** (tập 30s thời tiết): `py -3.13 hook_stage.py --profile satori-jp-obaa --slug ep14-kaimono --mode repair`
Expected: `hook/hook_locked.txt` mở bằng sự kiện (lời xì xào/quầy), câu cuối là câu cầu nối vào đoạn "晩秋の…"; `hook_lock.json.mode=repair`; storyboard + jobs.csv. Giao bước 3 theo §9 → `final_with_hook.mp4`; anh xem 30 s đầu (retention test tay).

- [ ] **Step 4: Ghi số đo vào `docs/PHUONG_AN_HOOK_VIDEO.md` §8** (thời gian máy, số vòng Sol, số vá, chi phí) và chốt "áp dụng toàn bộ" hay chỉnh ngưỡng.

---

## Self-review

- **Spec coverage:** Q1 (nguồn yếu → tự dựng từ climax) = `KHOI_NGUON_YEU` Task 7 · Q2 (hook trước S2, Beat 0, prompt khoá, STALE, repair là fallback) = Task 4/7/8/9/12 · Q3 (tập chưa đăng: giữ script/ảnh, ghép clip hook đầu) = Task 12/13 · 3 phép kiểm H1–H3 = Task 2/5 · Sol lens + nối từ hook = Task 6/9 · cổng B0/B10/STALE pha asset/mo_dau ĐẠT giả = Task 10 · thu thập mô tả/thumbnail nguồn = Task 1/2 · storyboard/flow prompts/Grok = Task 11/13 · tài liệu = Task 14 · pilot 1 video sau khi code xong = Task 15. Chưa làm (cố ý, YAGNI): cột HOOK trên sheet (ghi tay vào cột H như quy trình lean §5), K3 chọn video mẫu cho Lane A/D (A/D dùng `HOOK 30 GIÂY ĐẦU` của hồ sơ qua `hook/promise.txt` + Task 10 `qc_hoso`).
- **Placeholder scan:** không còn TBD/"tương tự Task N"; mọi prompt LLM viết đủ.
- **Type consistency:** `hook_stage.check(text, prof, ctx="") -> list[str]`; `ensure_locked(d, prof, ctx="", title="", mode="upstream", force=False, proxy=None) -> str`; `kiem_stale(d) -> (bool, list[str])`; `qc_script_sol.run_hook(...) -> (verdict, chon, text)` và `run(..., hook_block="")`; `ai_steps._pass1_prompt(..., hook_locked="")`, `extract_beats(prof, competitor, n=10, hook_locked="")`; `lean_script.viet(..., hook="")`, `do_tat_dinh(..., hook="")`, `sol_qc(..., hook="")` — dùng thống nhất ở Task 7/9/10/12.
