"""hook_stage.py — HOOK 20–30 GIÂY ĐẦU, artifact thượng nguồn của mọi tập (anh chốt 2026-09-23).

Luồng: S0 hồ sơ → H1 bóc 0–30s + title/mô tả/thumb video nguồn → H2 soi khung hình → H3 khớp promise nguồn
→ viết 3 hook cho tập mình (brain_model) → check() tất định + Sol lens hook → LOCK (sha256 + promise snapshot)
→ S2 viết thân NỐI từ hook. Hook là pure prose (TTS đọc mọi ký tự) — marker/visual nằm ở JSON riêng.
Repair mode (tập chưa đăng, có script.txt): nguồn = chính script.txt, không chạy S2, chỉ thêm hook đầu video.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
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


# Task 4: LOCK + promise snapshot + HOOK_STALE
def _sha_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _sha_file(p):
    return _sha_text(Path(p).read_text(encoding="utf-8")) if Path(p).exists() else None


def _title(d):
    for name in ("title.txt", "listting.txt"):
        f = Path(d) / name
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


# ── H1–H3: bóc hook video NGUỒN (phan_tich_nguon, Task 5, 2026-09-23) ──────────
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
    try:
        j = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        # 2026-09-23: file có thể đang ghi dở (lần chạy trước bị ngắt) → JSON hỏng. phan_tich_nguon
        # KHÔNG BAO GIỜ được ném — coi như chưa có video nguồn, không phải lỗi chặn cả tập.
        print(f"  ! competitor.segments.json hỏng, coi như chưa có video nguồn: {type(e).__name__} {str(e)[:100]}")
        return None
    return j if j.get("video_id") else None


# 2026-09-23 (Task 5 V4, vá lần 2): "Requested format is not available" là lỗi TẠM THỜI phía
# YouTube khi 1 player_client cụ thể bị nghi bot/rate-limit — cùng nguyên nhân đã vá ở
# fetch_script.via_whisper. Chuỗi (player_client, format) thử lần lượt, dừng ngay khi tải được;
# chỉ cần KHUNG HÌNH nên video-only (bv*) là đủ, khỏi cần luồng tiếng.
# Thứ tự ĐÃ ĐO THẬT trên video thật (vá lần 2, 2026-09-23): client 'android' + format
# 'bv*[height<=480]/b[height<=480]/b' tải được ngay (t2_android.mp4, 2.898.375 byte); client
# 'web' trả "Requested format is not available" cho CHÍNH video đó → 'android' phải đứng ĐẦU.
KHUNG_HINH_THU = (
    ("android", "bv*[height<=480]/b[height<=480]/b"),
    ("web", "bv*[height<=480]+ba/b[height<=480]"),
    ("ios", "bv*[height<=720]/best"),
)


def _ffmpeg_tren_path():
    """Tạo shim `ffmpeg.exe` rồi prepend vào PATH — vá lỗi yt_dlp download_ranges thiếu ffmpeg.

    Gốc rễ đã ĐO THẬT (vá lần 2, 2026-09-23, đừng dò lại):
    1. yt_dlp ở chế độ tải-MỘT-PHẦN (download_ranges) tự kiểm ffmpeg bằng một
       `FFmpegPostProcessor()` KHÔNG NHẬN THAM SỐ → nó BỎ QUA HOÀN TOÀN `ffmpeg_location` và chỉ
       dò biến môi trường PATH. Truyền ffmpeg_location kiểu thư mục hay kiểu file đều vô ích cho
       phép kiểm này (đã thử cả hai, đều fail) — ffmpeg_location vẫn giữ lại vì có ích cho bước
       ghép/cắt khác của yt_dlp, chỉ riêng phép kiểm "có ffmpeg không" là lờ nó đi.
    2. Máy không có ffmpeg trên PATH; bản dùng chung của dự án là bundle imageio_ffmpeg,
       qc_visual._ff() trả về đường dẫn kiểu
       `...\\site-packages\\imageio_ffmpeg\\binaries\\ffmpeg-win-x86_64-v7.1.exe` — TÊN FILE
       không phải `ffmpeg.exe`, nên dù có thêm đúng thư mục đó vào PATH thì yt_dlp vẫn không
       nhận ra (nó dò đúng tên `ffmpeg`/`ffmpeg.exe`).
    3. Cách vá đã verify chạy thật: tạo 1 thư mục tạm chứa file ĐÚNG TÊN `ffmpeg.exe` (Windows)
       / `ffmpeg` (nền tảng khác) — hardlink (os.link, cùng ổ C: nên hardlink được) tới binary
       thật của imageio, lỗi thì fallback shutil.copy2 — rồi PREPEND thư mục đó vào
       os.environ["PATH"]. Sau khi vá: FFmpegPostProcessor().available == True, basename ==
       'ffmpeg', tải video-only client 'android' → OK (xem KHUNG_HINH_THU ở trên).

    ⚠️ VÁ LẦN 3 (2026-09-23, đo thật, đọc kỹ trước khi "dọn code cho gọn"):
    4. yt_dlp NHỚ kết quả dò ffmpeg trong CÙNG một tiến trình — `FFmpegPostProcessor().available`
       chỉ dò PATH một lần rồi cache; gọi `_ffmpeg_tren_path()` BÊN TRONG `khung_hinh_0_30s()` là
       QUÁ MUỘN nếu trước đó cùng tiến trình đã có lượt gọi yt_dlp khác (vd
       `fetch_script.lay_meta_video()` chạy ngay trước trong `phan_tich_nguon`) — lượt đó đã dò
       ffmpeg và ghi nhận "không có", sửa PATH sau đó KHÔNG cứu được nữa (đã đo thật: sau khi gọi
       `_ffmpeg_tren_path()` xong, `FFmpegPostProcessor().available` vẫn `False` nếu trước đó đã
       có 1 lượt dò thất bại). ⇒ PATH BẮT BUỘC phải có shim từ TRƯỚC KHI BẤT CỨ THỨ GÌ trong tiến
       trình dò yt_dlp lần đầu — vì vậy có biến module-level `FFMPEG_SHIM = _ffmpeg_tren_path()`
       chạy ngay lúc `import hook_stage`, sớm hơn mọi lệnh gọi yt_dlp trong toàn bộ luồng H1-H3.
       Lời gọi lại trong `khung_hinh_0_30s()` vẫn giữ nguyên (idempotent, vô hại) chỉ để cứu
       trường hợp thư mục shim bị xoá giữa phiên chạy dài.
    5. `ffmpeg_location` truyền vào yt_dlp KHÔNG được trỏ vào thư mục imageio_ffmpeg (nơi chứa
       `ffmpeg-win-x86_64-v7.1.exe`) — đọc `yt_dlp/postprocessor/ffmpeg.py::_determine_executables`
       thì khi `ffmpeg_location` là một THƯ MỤC, yt_dlp tự dựng đường dẫn `<thư mục>/ffmpeg` và
       `<thư mục>/ffprobe`; thư mục imageio không có file tên đúng như vậy nên không khớp — và
       tham số này ĐÈ LUÔN kết quả dò theo PATH (dù PATH đã có shim đúng, `ffmpeg_location` sai
       vẫn làm yt_dlp kết luận "không có ffmpeg", lỗi thật đã gặp: "m3u8 download detected but
       ffmpeg could not be found"). ⇒ `ffmpeg_location` phải trỏ ĐÚNG vào thư mục shim
       (`FFMPEG_SHIM`, thư mục có file tên `ffmpeg.exe`), không phải thư mục imageio.

    Idempotent (gọi nhiều lần không tạo lại file/không nhân đôi PATH). Lỗi bất kỳ (không tạo
    được hardlink/copy, không mkdir được...) → in cảnh báo tiếng Việt, trả None, KHÔNG NÉM —
    thiếu ffmpeg chỉ nên làm 1 lượt tải thất bại (rơi vào nhánh log lỗi có sẵn), không được chặn
    cứng cả tập.
    """
    ten_file = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    thu_muc = Path(tempfile.gettempdir()) / "h2dev_ffmpeg_shim"
    dich = thu_muc / ten_file
    try:
        thu_muc.mkdir(parents=True, exist_ok=True)
        if not dich.exists():
            import qc_visual
            nguon = qc_visual._ff()
            try:
                os.link(nguon, dich)
            except Exception:
                shutil.copy2(nguon, dich)
        path_hien_tai = os.environ.get("PATH", "")
        if str(thu_muc) not in path_hien_tai.split(os.pathsep):
            os.environ["PATH"] = str(thu_muc) + os.pathsep + path_hien_tai
        return thu_muc
    except Exception as e:
        print(f"  ! không tạo được ffmpeg shim trên PATH (tải khung hình 0-30s có thể fail): "
              f"{type(e).__name__} {str(e)[:100]}")
        return None


# Vá lần 3 (2026-09-23): PHẢI chạy NGAY LÚC IMPORT module, trước bất kỳ lệnh gọi yt_dlp nào khác
# trong tiến trình (kể cả fetch_script.lay_meta_video chạy trước trong phan_tich_nguon) — xem lý
# do đầy đủ ở mục 4 trong docstring _ffmpeg_tren_path ngay trên. Trả None (không ném) nếu môi
# trường không tạo được shim — mọi chỗ dùng FFMPEG_SHIM đều tự rơi về hành vi cũ khi gặp None.
FFMPEG_SHIM = _ffmpeg_tren_path()


def khung_hinh_0_30s(video_id, out_dir, n=6, proxy=None):
    """Tải 30 giây đầu (yt_dlp download_sections) → n khung → 1 ảnh lưới contact.jpg. Lỗi trả None."""
    import qc_visual
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    try:
        # Đã có clip từ lần chạy trước thì dùng lại, khỏi tải lại (không cache phức tạp hơn 1 glob).
        clip = next((f for f in sorted(out_dir.glob("src_0_30s.*")) if f.stat().st_size > 10_000), None)
        if not clip:
            # vá lần 3 (2026-09-23): gọi lại đây chỉ để cứu trường hợp thư mục shim (FFMPEG_SHIM,
            # đã tạo LÚC IMPORT module — xem mục 4 docstring _ffmpeg_tren_path) bị xoá giữa phiên
            # chạy dài; idempotent nên gọi lại không hại gì. Việc PATH có shim TỪ TRƯỚC lúc import
            # mới là điều kiện quyết định (yt_dlp nhớ kết quả dò trong cùng tiến trình).
            shim = _ffmpeg_tren_path()
            import yt_dlp
            from yt_dlp.utils import download_range_func
            outtmpl = str(out_dir / "src_0_30s.%(ext)s")
            # vá lần 3, mục 5: ffmpeg_location PHẢI là thư mục SHIM (có file tên đúng `ffmpeg.exe`),
            # KHÔNG phải thư mục imageio_ffmpeg (chỉ có tên `ffmpeg-win-x86_64-v7.1.exe`, yt_dlp tự
            # dựng `<thư mục>/ffmpeg` rồi không thấy → đè luôn kết quả dò PATH). Không tạo được shim
            # (shim=None) thì rơi về hành vi cũ (thư mục imageio) để không mất hẳn khả năng chạy.
            base_opts = {"quiet": True, "no_warnings": True, "noprogress": True,
                         "download_ranges": download_range_func(None, [(0, 30)]), "force_keyframes_at_cuts": True,
                         "outtmpl": outtmpl,
                         "ffmpeg_location": str(shim) if shim else str(Path(qc_visual._ff()).parent)}
            if proxy:
                base_opts["proxy"] = proxy
            # cùng cookie với lay_meta_video (fetch_script._ap_cookies) — request này cũng là gọi
            # thẳng YouTube nên ăn đòn chặn bot y hệt; bỏ sót ở vá lần 2, bổ sung ở vá lần 3.
            import fetch_script
            fetch_script._ap_cookies(base_opts)
            err = ""
            for i, (client, fmt) in enumerate(KHUNG_HINH_THU):
                opts = dict(base_opts, format=fmt, extractor_args={"youtube": {"player_client": [client]}})
                try:
                    with yt_dlp.YoutubeDL(opts) as y:
                        y.download([f"https://www.youtube.com/watch?v={video_id}"])
                    err = ""
                    break
                except Exception as e:
                    err = f"{type(e).__name__}: {e}"
                    if i < len(KHUNG_HINH_THU) - 1:
                        time.sleep(3)
            # format video-only có thể ra .webm chứ không phải .mp4 → không giả định đuôi file.
            clip = next((f for f in sorted(out_dir.glob("src_0_30s.*")) if f.stat().st_size > 10_000), None)
            if not clip:
                if err:
                    print(f"  ! không soi được khung hình nguồn {video_id}: {err[:150]}")
                return None
        frames = []
        for i in range(n):
            f = out_dir / f"f{i+1:02d}.jpg"
            if qc_visual._frame(clip, 1.0 + i * (28.0 / max(n - 1, 1)), f):
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
    d = Path(d); hd = d / HOOK_DIR; hd.mkdir(parents=True, exist_ok=True)
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
        # 2026-09-23 (Task 5 V2): lay_meta_video/tai_anh hợp đồng "không ném" nhưng vẫn là lời gọi
        # mạng ngoài tầm kiểm soát → bọc để 1 lỗi mạng không kéo sập cả phan_tich_nguon.
        try:
            if not src["title"]:
                m = fetch_script.lay_meta_video(vid, proxy=proxy)
                src.update(title=m["title"], description=m["description"])
                j["thumbnail_url"] = j.get("thumbnail_url") or m["thumbnail_url"]
            if j.get("thumbnail_url") and fetch_script.tai_anh(j["thumbnail_url"], hd / "source_thumb.jpg", proxy=proxy):
                src["thumb_path"] = str(hd / "source_thumb.jpg")
        except Exception as e:
            print(f"  ! lấy meta/thumbnail nguồn lỗi, đi tiếp với dữ liệu đang có: {type(e).__name__} {str(e)[:100]}")
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
