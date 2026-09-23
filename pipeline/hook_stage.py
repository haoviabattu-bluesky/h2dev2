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
# 2026-09-23 (Việc 1, nối kho hook vào PROMPT_VIET): kho nằm ở DỰ ÁN KHÁC
# (E:\CLAUDE\YOUTUBE\HOOK_LIBRARY, dự án nghiên cứu — không thuộc h2dev) — khai hằng cấp module
# để test thay được (monkeypatch HS.HOOK_LIBRARY_PATH) và để doc_kho_hook() không hardcode đường dẫn
# rải rác nhiều chỗ. Thiếu file này KHÔNG được làm gãy dây chuyền viết hook ở đây (xem doc_kho_hook).
HOOK_LIBRARY_PATH = Path(r"E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\patterns.json")
MAC_DINH = {
    # 2026-09-23 (Việc 2, vá review cuối): công tắc BẬT/TẮT tính năng hook THEO TỪNG KÊNH — mặc
    # định TẮT, kênh nào muốn dùng phải tự khai `script.hook.enabled: true` trong profile. Trước
    # đây tính năng tự áp dụng cho MỌI kênh chỉ cần `script.flow == "lean"` — tập kế tiếp của cả 6
    # kênh sẽ cùng lúc là "tập thật đầu tiên" chạy tính năng mới, không bật dần được.
    "enabled": False,
    # 2026-09-23 (Việc thêm field script.hook.model): hook do model VIẾT viết (viet_candidates →
    # ai_steps._writer_chat → mặc định lấy `script.brain_model` của kênh — đúng nguyên tắc "model
    # viết kịch bản thì viết luôn hook"). Trường NÀY chỉ để GHIM model viết HOOK khác với model viết
    # THÂN kịch bản khi kênh cần — rỗng ("") = im lặng dùng brain_model như trước, không đổi hành vi
    # cũ. Lý do có trường: A/B thật cùng hồ sơ teinengo-tanoshimi, chỉ đổi model viết hook — Opus
    # viết: cả 3 phương án vượt trần độ dài (259/232/221 chữ, trần 185) → phải vá cứu (2 vòng chấm +
    # 2 lượt vá); Fable viết: cả 3 qua cổng máy ngay lần đầu (1 vòng chấm, 0 lượt vá, hook cuối 158
    # chữ). Trường này KHÔNG đụng brain_model/patch_model của kênh — mọi lượt SỬA hook (patch_hook,
    # tức S4) vẫn dùng patch_model như luật chung, không đọc trường này.
    "model": "",
    # 2026-09-23 (Việc 1): id kiểu hook (patterns) + id thiết bị khoá hook (closer) tra trong kho
    # HOOK_LIBRARY_PATH. Mặc định rỗng = KHÔNG chèn khối kho vào PROMPT_VIET, hành vi y hệt trước
    # khi có tính năng này (xem doc_kho_hook + viet_candidates).
    "patterns": [], "closer": "",
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


def is_enabled(prof):
    """2026-09-23 (Việc 2): True chỉ khi profile khai `script.hook.enabled: true` tường minh.
    Đây là NGÃ RẼ DUY NHẤT giữa kênh đã bật/chưa bật hook — mọi nơi gọi (lean_script.run,
    make_video.Job.kiem_lock, qc_final.kiem_hook) đều phải qua đúng hàm này, không tự suy luận
    theo tên/`id` kênh (xem CLAUDE.md hàng rào #2: khác biệt lane chỉ đi qua field profile)."""
    return bool(cau_hinh(prof).get("enabled"))


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
        # 2026-09-23 (Việc 3b, vá review cuối): trước đây gọi KHÔNG truyền exempt_units, trong khi
        # lean_script.py (đo thân bài) truyền sc.get("fact_exempt_units") — 2 cổng CÙNG một hàm mà
        # dùng 2 luật khác nhau. Lane teinengo-real khai fact_exempt_units=["万円","円"] vì số tiền
        # của nhân vật là hư cấu; hook lấy con số tiền làm điểm neo (đúng khuyến khích của chính
        # PROMPT_VIET) mà không được miễn thì bị đánh trượt cả 3 ứng viên oan.
        from lean_script import _so_lieu_ngoai_tu_lieu
        exempt = tuple((prof.get("script", {}) or {}).get("fact_exempt_units") or ())
        for x in _so_lieu_ngoai_tu_lieu(text, ctx, exempt):
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
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        # 2026-09-23 (vá review dọn hook, V1): hook_lock.json ghi dở/hỏng (tiến trình bị ngắt giữa
        # chừng) không được ném thẳng JSONDecodeError vào qc_final.kiem_hook (cổng B10) hay
        # Job.kiem_lock — coi như CHƯA KHOÁ (None), cùng kiểu vá đã làm cho nguon_cua_tap.
        print(f"  ! hook_lock.json hỏng, coi như chưa khoá hook: {type(e).__name__} {str(e)[:100]}")
        return None


def doc_hook(d):
    p = Path(d) / HOOK_DIR / "hook_locked.txt"
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""


def kiem_stale(d):
    """2026-09-23 (Việc 1, vá review cuối): thứ tự pipeline thật là hook khoá TRƯỚC — còn
    `thumb_text.txt` (B7) và `title.txt` (B9) mãi sau này mới được ghi. Lúc `promise_snapshot()`
    chụp lúc khoá, hai trường này là chuỗi rỗng; lần đầu chúng được ghi thật thì trước đây bị coi
    là 'đã đổi' → HOOK_STALE ngay giữa vận hành bình thường (make_video.Job.kiem_lock dừng ở B4/
    B5W, qc_final.kiem_hook báo `cao` ở B10) cho một tập hoàn toàn không có vấn đề gì.
    Sửa: coi "chưa có giá trị (rỗng/None) → có giá trị" là LẦN GHI ĐẦU TIÊN, không phải thay đổi —
    in 1 dòng thông báo rồi RE-BASELINE lại đúng trường đó trong hook_lock.json, đi tiếp bình
    thường. Chỉ khi một trường ĐANG có giá trị A đổi sang giá trị B (cả hai đều khác rỗng/None)
    mới coi là lỗi thời thật.
    ⚠️ Kẽ hở đã cân nhắc (không sửa ở đây, ghi lại để không quên): (1) tổng quát hoá từ "chuỗi
    rỗng" sang "falsy" (None lẫn "") — áp dụng luôn cho ctx_sha256/script_sha256/promise_sha256
    (giá trị khởi tạo có thể là None khi file nguồn chưa tồn tại lúc khoá); (2) một khi đã
    re-baseline, hook_lock.json không còn giữ dấu vết "giá trị gốc lúc khoá là rỗng" — nếu B7/B9
    ghi đè bằng nội dung SAI ngay lần đầu, cổng này sẽ coi lần ghi sai đó là baseline mới và không
    còn cách nào phát hiện qua so sánh promise nữa (chỉ còn phép kiểm khác, vd B10 title-drift, bắt
    được nếu có sửa TIẾP sau đó); (3) không thread-safe giữa 2 tiến trình gọi đồng thời — không mới
    so với phần còn lại của file, không xử lý thêm ở đây."""
    d = Path(d)
    m = doc_lock(d)
    if not m:
        return False, ["chưa có hook lock"]
    ly_do = []
    if _sha_file(d / HOOK_DIR / "hook_locked.txt") != m.get("sha256"):
        ly_do.append("hook_locked.txt bị sửa tay sau khi khoá")
    now = promise_snapshot(d, m.get("mode", "upstream"))
    promise = dict(m.get("promise") or {})
    re_baseline = False
    for k, v in promise.items():
        nv = now.get(k)
        if nv == v:
            continue
        if not v and nv:
            print(f"  [hook] promise '{k}' vừa được ghi LẦN ĐẦU sau khi khoá hook ({nv!r}) — "
                  f"cập nhật lại baseline, KHÔNG coi là lỗi thời")
            m["promise"][k] = nv
            re_baseline = True
            continue
        ly_do.append(f"promise '{k}' đã đổi sau khi khoá hook → HOOK_STALE, chạy lại H1–H4")
    if ly_do or re_baseline:
        m["stale"] = bool(ly_do)
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

    ⚠️ VÁ LẦN 3 (2026-09-23, đo thật):
    4. yt_dlp NHỚ kết quả dò ffmpeg trong CÙNG một tiến trình — `FFmpegPostProcessor().available`
       chỉ dò PATH một lần rồi cache; gọi `_ffmpeg_tren_path()` BÊN TRONG `khung_hinh_0_30s()` là
       QUÁ MUỘN nếu trước đó cùng tiến trình đã có lượt gọi yt_dlp khác (vd
       `fetch_script.lay_meta_video()` chạy ngay trước trong `phan_tich_nguon`) — lượt đó đã dò
       ffmpeg và ghi nhận "không có", sửa PATH sau đó KHÔNG cứu được nữa.

    ⚠️ VÁ LẦN 4 (2026-09-23, đo thật — SỬA LẠI cách xử lý mục 4 ở trên, đọc kỹ trước khi đụng vào):
    Chỗ NHỚ ở mục 4 không phải "không xoá được" — nó nằm CỤ THỂ ở 2 dict cấp CLASS trong
    `yt_dlp/postprocessor/ffmpeg.py`: `FFmpegPostProcessor._version_cache` (khoá là tên trần
    `'ffmpeg'`/`'ffprobe'` khi không truyền `ffmpeg_location`) và `_features_cache`. Đo thật trong
    1 tiến trình: (1) trước shim → `available=False`, cache `{None: None, 'ffmpeg': False}`; (2)
    sau khi tạo shim + sửa PATH nhưng CHƯA xoá memo → vẫn `False` (đúng như mục 4 mô tả); (3) sau
    khi `_version_cache.pop('ffmpeg', None)` + `.pop('ffprobe', None)` + `_features_cache.clear()`
    (giữ lại khoá `None: None`) → `available=True`. ⇒ memo XOÁ ĐƯỢC, nên KHÔNG cần side effect lúc
    import nữa (blast radius quá rộng: `import hook_stage` sẽ ghi đĩa thật ~87MB + sửa PATH của cả
    tiến trình dù người gọi chỉ cần `kiem_stale()`, kể cả mỗi lần pytest collect test) — hàm này
    giờ CHỈ chạy khi thật sự cần (đầu `phan_tich_nguon()`, và lặp lại idempotent trong
    `khung_hinh_0_30s()`), và tự xoá memo của `yt_dlp.postprocessor.ffmpeg` NẾU module đó đã nằm
    trong `sys.modules` (nghĩa là đã có lượt dò trước đó trong tiến trình) — gọi muộn vẫn ăn.
    Đây là API NỘI BỘ của yt_dlp (tên field có thể đổi ở bản sau) nên bọc try/except RIÊNG, lỗi chỉ
    in cảnh báo, không ném — không xoá được memo thì tệ nhất là quay lại tình trạng cũ (dò 1 lần rồi
    kẹt), không làm hỏng luồng chính.
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
    global FFMPEG_SHIM
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
        # V1 (vá lần 4, 2026-09-23): nếu yt_dlp.postprocessor.ffmpeg ĐÃ được nạp trong tiến trình
        # này (đã có lượt dò trước đó, vd fetch_script.lay_meta_video chạy trước), xoá memo cấp
        # CLASS của nó để lượt dò TIẾP THEO thấy PATH mới — xem mục 4 docstring ở trên. API nội bộ
        # nên bọc try/except riêng, lỗi chỉ cảnh báo, không ném.
        mod = sys.modules.get("yt_dlp.postprocessor.ffmpeg")
        if mod is not None:
            try:
                pp = mod.FFmpegPostProcessor
                pp._version_cache.pop("ffmpeg", None)
                pp._version_cache.pop("ffprobe", None)
                pp._features_cache.clear()
            except Exception as e:
                print(f"  ! không xoá được memo ffmpeg của yt_dlp (API nội bộ có thể đã đổi): "
                      f"{type(e).__name__} {str(e)[:100]}")
        FFMPEG_SHIM = thu_muc
        return thu_muc
    except Exception as e:
        print(f"  ! không tạo được ffmpeg shim trên PATH (tải khung hình 0-30s có thể fail): "
              f"{type(e).__name__} {str(e)[:100]}")
        return None


# V2 (vá lần 4, 2026-09-23): KHÔNG gọi _ffmpeg_tren_path() lúc import nữa — chỉ khai biến để các
# hàm khác tham chiếu được. Gọi lúc import nghĩa là `import hook_stage` một mình đã ghi đĩa thật
# (hardlink/copy binary ~87MB vào %TEMP%) và sửa os.environ["PATH"] của cả tiến trình, kể cả khi
# người gọi chỉ cần kiem_stale() và không bao giờ chạm yt_dlp — kể cả mỗi lần pytest thu thập test.
# Từ vá lần 4: memo dò-ffmpeg của yt_dlp XOÁ ĐƯỢC (xem V1 trong _ffmpeg_tren_path), nên gọi MUỘN ở
# đầu phan_tich_nguon() vẫn ăn, không cần chạy sớm hơn mọi lệnh gọi yt_dlp như trước.
FFMPEG_SHIM = None


def khung_hinh_0_30s(video_id, out_dir, n=6, proxy=None):
    """Tải 30 giây đầu (yt_dlp download_sections) → n khung → 1 ảnh lưới contact.jpg. Lỗi trả None."""
    import qc_visual
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    try:
        # Đã có clip từ lần chạy trước thì dùng lại, khỏi tải lại (không cache phức tạp hơn 1 glob).
        clip = next((f for f in sorted(out_dir.glob("src_0_30s.*")) if f.stat().st_size > 10_000), None)
        if not clip:
            # vá lần 3 (2026-09-23), chú thích sửa lại ở vá lần 4 (2026-09-23, vá review cuối) cho
            # khớp code thật: từ vá lần 4, `_ffmpeg_tren_path()` KHÔNG còn chạy lúc import module
            # nữa (xem FFMPEG_SHIM/V2 ở trên) — gọi Ở ĐÂY, ngay trước khi cần, mới là nơi shim thật
            # sự được tạo lần đầu. Idempotent nên gọi lại nhiều lần (kể cả khi thư mục shim đã có từ
            # trước) không hại gì; memo dò-ffmpeg của yt_dlp cũng tự xoá được (V1) nên gọi MUỘN vẫn ăn.
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
        # V6 (vá review dọn hook, 2026-09-23): lời gọi chỉ-đọc-cache KHÔNG được đụng tới
        # yt_dlp/PATH — trước đây _ffmpeg_tren_path() (tạo shim, ghi đĩa, sửa PATH tiến trình)
        # chạy TRƯỚC cả nhánh cache này nên vẫn "đụng" dù chẳng cần tải gì cả.
        return json.loads(out_p.read_text(encoding="utf-8"))
    # V2 (vá lần 4, 2026-09-23): gọi LƯỜI ở đây — TRƯỚC fetch_script.lay_meta_video() bên dưới —
    # thay vì lúc import module (xem FFMPEG_SHIM/docstring _ffmpeg_tren_path). Idempotent, và từ vá
    # lần 4 hàm này tự xoá memo yt_dlp nếu module đã lỡ được nạp trước đó trong cùng tiến trình.
    # V6 (vá review dọn hook, 2026-09-23): CHUYỂN XUỐNG SAU nhánh cache ở trên — vẫn giữ TRƯỚC lần
    # gọi fetch_script.lay_meta_video() đầu tiên bên dưới (đây là lý do tồn tại của hàm), chỉ đổi
    # thứ tự so với nhánh short-circuit cache.
    _ffmpeg_tren_path()
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


# ── Việc 1 (2026-09-23): nối KHO KIỂU HOOK (dự án khác) vào PROMPT_VIET ──────────
KHOI_KHO_HOOK_TIEU = ("KHO KIỂU HOOK ĐÃ ĐO ĐƯỢC ĐANG ĂN Ở CHÍNH NGÁCH NÀY (chọn 1 kiểu cho MỖI phương án, bám "
                      "đúng khuôn của nó; mục \"tránh\" là điều CẤM):\n")


def doc_kho_hook(ids, closer_id=""):
    """Đọc kho HOOK_LIBRARY_PATH (dự án nghiên cứu KHÁC, E:\\CLAUDE\\YOUTUBE\\HOOK_LIBRARY — không
    thuộc h2dev) → trả 1 chuỗi đã định dạng sẵn, chèn thẳng vào PROMPT_VIET. Với mỗi id trong
    `ids` (khớp `patterns[].id` trong kho): in `id · name · kind`, `mechanism`, `template`, `avoid`.
    Nếu có `closer_id` (khớp `closers[].id`): thêm `mechanism` + `template` của thiết bị khoá đó.

    Kho không tồn tại / JSON hỏng → in CẢNH BÁO tiếng Việt rồi trả chuỗi RỖNG, KHÔNG NÉM — kho nằm
    ở dự án khác, thiếu/hỏng kho không được phép làm gãy dây chuyền viết hook ở đây (cùng triết lý
    với `phan_tich_nguon`/`nguon_cua_tap` trong file này).

    NGOẠI LỆ (2026-09-23): kho ĐỌC ĐƯỢC mà KHÔNG id nào của kênh khớp thì DỪNG HẲN (SystemExit).
    Đó là lỗi khai profile (gõ "H2" thay "H22"), không phải sự cố hạ tầng — im lặng trả rỗng thì
    hook vẫn viết ra bình thường và cả lane chạy như thể chưa bật kho, cảnh báo chỉ hiện thoáng ở
    console rồi mất. Khớp được MỘT PHẦN thì vẫn chạy, chỉ cảnh báo id hỏng."""
    ids = list(ids or [])
    if not ids and not closer_id:
        return ""
    try:
        kho = json.loads(HOOK_LIBRARY_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ! không đọc được kho hook {HOOK_LIBRARY_PATH}: {type(e).__name__} {str(e)[:100]}")
        return ""
    pats = {p.get("id"): p for p in kho.get("patterns") or []}
    closers = {c.get("id"): c for c in kho.get("closers") or []}
    khoi = []
    for pid in ids:
        p = pats.get(pid)
        if not p:
            print(f"  ! kiểu hook {pid!r} không có trong kho hook, bỏ qua")
            continue
        khoi.append(f"- {p.get('id')} · {p.get('name')} · kind {p.get('kind')}\n"
                    f"  mechanism: {p.get('mechanism', '')}\n"
                    f"  template: {p.get('template', '')}\n"
                    f"  tránh: {p.get('avoid', '(không ghi)')}")
    phan_closer = ""
    if closer_id:
        c = closers.get(closer_id)
        if c:
            phan_closer = (f"\nTHIẾT BỊ KHOÁ HOOK (câu chuyển 30–90s biến mở đầu thành câu hỏi cả video): "
                          f"{c.get('id')} · {c.get('name')}\n  mechanism: {c.get('mechanism', '')}\n"
                          f"  template: {c.get('template', '')}")
        else:
            print(f"  ! thiết bị khoá hook {closer_id!r} không có trong kho hook, bỏ qua")
    if ids and not khoi:
        raise SystemExit(f"LỖI KHAI PROFILE: không kiểu hook nào trong {ids} có trong kho "
                         f"{HOOK_LIBRARY_PATH}. Sửa script.hook.patterns trong profile "
                         f"(id đúng dạng H01..H23), hoặc để rỗng nếu không muốn dùng kho.")
    return ("\n".join(khoi) + phan_closer).strip()


# ── Task 7 (2026-09-23): viết 3 hook + Sol chọn/vá + ensure_locked() orchestrator ──
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
    # Việc 1 (2026-09-23): chèn khối KHO KIỂU HOOK ngay TRƯỚC "LUẬT VIẾT (SOP hook):" — bằng
    # str.replace() thay vì thêm placeholder cấp-dòng vào PROMPT_VIET, để khi `patterns` rỗng (mặc
    # định) prompt GIỮ NGUYÊN VĂN như trước khi có tính năng này, không thêm dòng trống nào.
    h = cau_hinh(prof)
    kho = doc_kho_hook(h.get("patterns") or [], h.get("closer") or "")
    if kho:
        prompt = prompt.replace("LUẬT VIẾT (SOP hook):", KHOI_KHO_HOOK_TIEU + kho + "\n\nLUẬT VIẾT (SOP hook):", 1)
    # script.hook.model (2026-09-23): ghim model VIẾT hook khác brain_model khi kênh cần (xem chú
    # thích MAC_DINH["model"]). Rỗng ("", mặc định) → KHÔNG truyền `model`, y hệt hành vi cũ:
    # _writer_chat tự setdefault bằng claude_p_bridge.brain_model_of(prof) ở nhánh engine=claude_p;
    # ở nhánh Gemini (llm_client.chat) `model` chỉ có tác dụng khi đi kèm `provider` — lane không
    # khai `provider` thì đây vẫn là no-op an toàn giống trước, không phải cách chọn model đầy đủ
    # cho nhánh đó (xem báo cáo task, mục kiểm chữ ký 2 nhánh).
    kwargs_viet = {"system": ai_steps._skill_text(prof, "script"), "task": "short",
                   "min_chars": muc * 2, "max_chars": muc * 6}
    model_hook = cau_hinh(prof).get("model") or ""
    if model_hook:
        if (prof.get("script", {}) or {}).get("engine") != "claude_p":
            # 2026-09-23 (vá review cuối, Việc 4): kênh khai script.hook.model mà KHÔNG dùng
            # engine="claude_p" thì tham số này bị bỏ qua LẶNG LẼ (nhánh Gemini/llm_client.chat()
            # chỉ dùng `model` khi đi kèm `provider`, xem chú thích ngay trên) — người khai tưởng
            # đã ghim đúng model mà thật ra không đổi gì. In cảnh báo để không ai tưởng nhầm.
            print(f"  ! script.hook.model={model_hook!r} bị BỎ QUA — kênh không khai script.engine="
                  f"\"claude_p\" (đang ở nhánh Gemini, model chỉ có tác dụng khi đi kèm `provider`)")
        kwargs_viet["model"] = model_hook
    r = ai_steps._writer_chat(prof, prompt, **kwargs_viet)
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
        # V2 (vá review, 2026-09-23): model bỏ khuôn === HOOK n === là kiểu thất bại HAY GẶP NHẤT
        # trong sản xuất — trước đây raise thẳng, không để lại dấu vết gì. Ghi hook_qc.json trước
        # khi raise, kèm số ký tự thô model trả về để người đọc sau dò được đang thiếu khuôn hay
        # model trả rỗng.
        (hd / "hook_qc.json").write_text(json.dumps(
            {"candidates": 0, "state": "NO_CANDIDATES", "raw_chars": len(cands_text)},
            ensure_ascii=False, indent=2), encoding="utf-8")
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
        try:
            c2 = patch_hook(prof, c, qc["check"][str(i)])
        except Exception as e:
            # V1 (vá review, 2026-09-23): patch_hook ném (LLMError khi bản trả về quá ngắn/cắt giữa
            # câu, hoặc lỗi khác) — đây là lượt vá "cứu" duy nhất trước Sol, không có `chosen` nào để
            # giữ. Vẫn phải ghi hook_qc.json state=BLOCK (kèm lý do patch cứu thất bại) TRƯỚC khi
            # raise, kẻo mất luôn dấu vết vì sao BLOCK.
            qc["log"].append(f"patch cứu thất bại: {type(e).__name__}: {e}")
            (hd / "hook_qc.json").write_text(json.dumps({**qc, "state": "BLOCK"}, ensure_ascii=False, indent=2), encoding="utf-8")
            raise SystemExit(f"✗ H3': cả 3 ứng viên trượt phép đo tất định, vá cứu cũng lỗi: {qc['check']}") from e
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
            # V3 (vá review, 2026-09-23): PASS THẬT do Sol chấm, phân biệt với PASS_LEAN (chốt theo
            # luật FIX×3) — hook_lock.json không đổi, chỉ hook_qc.json.
            text = chosen; qc["log"].append(f"sol{vong} PASS chọn {chon}"); qc["state"] = "PASS"; break
        viec = _viec_tu_sol(rep) or ["theo báo cáo Sol"]
        if vong > MAX_PATCH_HOOK:
            text = chosen; qc["log"].append(f"sol{vong} FIX×{vong} → coi như PASS (luật lean)"); qc["state"] = "PASS_LEAN"; break
        try:
            new = patch_hook(prof, chosen, viec)
        except Exception as e:
            # V1 (vá review, 2026-09-23): patch_hook ném NGAY TRONG vòng Sol — lúc này đang giữ
            # `chosen`, một ứng viên ĐÃ qua check() (hoặc bản trước đã hợp lệ). Ném ở đây trước sẽ
            # làm ensure_locked chết TRƯỚC khi ghi hook_qc.json/khoá → mất cả hook đang có lẫn dấu
            # vết. Giữ nguyên `chosen`, ghi log, chốt luôn (không lặp thêm vì model sửa vừa thất bại).
            # V3 (vá review dọn hook, 2026-09-23): trước đây cũng gán "PASS_LEAN" như nhánh FIX×3 ở
            # trên — 2 nghĩa khác hẳn nhau (luật lean cho qua vs model sửa ném lỗi) bị gộp chung 1
            # state, người đọc hook_qc.json không phân biệt được tập khoẻ mạnh với tập có sự cố.
            # Đổi riêng cho nhánh NÀY (patch ném) thành PASS_PATCH_ERROR; nhánh FIX×3 giữ PASS_LEAN.
            qc["log"].append(f"patch{vong} lỗi ({type(e).__name__}: {e}) → giữ bản trước")
            text = chosen; qc["state"] = "PASS_PATCH_ERROR"; break
        qc["patches"] += 1
        if check(new, prof, ctx):
            qc["log"].append(f"patch{vong} trượt tất định, giữ bản trước")
            new = chosen
        hop = [(chon, new)]
        cands_hop = f"=== HOOK {chon} ===\n{new}"
    qc.setdefault("state", "PASS")
    (hd / "hook_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = khoa(d, text, mode=mode, extra={"sol_rounds": qc["sol_rounds"], "patches": qc["patches"],
                                          "source_video_id": src.get("video_id")})
    print(f"[H4] HOOK_LOCKED {meta['chars']} chữ · sol {qc['sol_rounds']} vòng · vá {qc['patches']}")
    return text


# ---------------------------------------------------------------------------
# CLI (Task 12, 2026-09-23) — cửa vào dòng lệnh cho hook_stage.
# `--mode upstream`: tập mới, thực ra lean_script đã tự gọi ensure_locked rồi — CLI ở đây để
#   chạy tay/khắc phục khi cần chạy lại riêng lẻ.
# `--mode repair`: tập ĐÃ có script.txt (script/ảnh/video cũ giữ nguyên), chỉ viết thêm hook rồi
#   ghép vào đầu video — ensure_locked(mode="repair") (Task 7) tự lấy script.txt làm nguồn promise.
# Sau khi khoá hook xong, gọi luôn hook_storyboard.sinh() (Task 11) để ra storyboard + prompt Flow
# + jobs.csv, rồi in đường dẫn TUYỆT ĐỐI cho người vận hành copy chạy tiếp.
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    ap = argparse.ArgumentParser(description="H1–H4 hook 20–30s (upstream) hoặc repair mode cho tập đã có script")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--mode", default="upstream", choices=["upstream", "repair"])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default="", choices=["", "source"])
    ap.add_argument("--proxy", default="")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    d = ROOT / (prof.get("slug_dir") or "assets/out") / a.slug
    if not d.exists():
        raise SystemExit(f"✗ không thấy thư mục tập {d}")
    if a.mode == "repair" and not (d / "script.txt").exists():
        raise SystemExit(f"✗ repair mode cần {d / 'script.txt'} đã có")
    # 2026-09-23 (Việc 2, vá review cuối): kênh chưa khai script.hook.enabled=true vẫn được phép
    # CHẠY TAY CLI này (người vận hành cố ý gọi để bật thử/khắc phục) — chỉ nhắc 1 dòng, không chặn.
    # In ra STDERR (không phải print thường/stdout) — `--only source` in JSON THUẦN ra stdout để
    # người vận hành/script khác parse được, dòng nhắc lẫn vào đó sẽ làm hỏng `json.loads()`.
    if not is_enabled(prof):
        print(f"[hook] ⚠️ profile '{a.profile}' chưa khai script.hook.enabled=true — "
              f"chạy tay theo yêu cầu, KHÔNG tự động trong pipeline lean_script cho tới khi bật",
              file=sys.stderr)
    if a.only == "source":
        src = phan_tich_nguon(d, prof, proxy=a.proxy or None, force=a.force)
        print(json.dumps({k: src[k] for k in ("video_id", "hook_kind", "score_0_12", "video_hook_verdict", "promise_match")},
                         ensure_ascii=False, indent=1))
        return
    ctx = (d / "series_ctx.txt").read_text(encoding="utf-8") if (d / "series_ctx.txt").exists() else ""
    ensure_locked(d, prof, ctx=ctx, title=_title(d), mode=a.mode, force=a.force, proxy=a.proxy or None)
    import hook_storyboard  # lazy: tránh vòng phụ thuộc module, chỉ cần khi thật sự chạy CLI
    hook_storyboard.sinh(d, prof, force=a.force)
    for f in ("hook_locked.txt", "hook_storyboard.json", "grok_jobs.csv"):
        print(f"  → {d / HOOK_DIR / f}")


if __name__ == "__main__":
    main()
