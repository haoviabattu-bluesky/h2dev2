"""hook_stage.py — HOOK đầu video, artifact thượng nguồn của mọi tập.

LUẬT DUY NHẤT (anh chốt 2026-10-21, thay luật 17/10): hook BÁM SÁT CẤU TRÚC hook của video gốc — gốc làm thế nào mình làm
thế ấy, được đổi một chút cho hợp/hay hơn (docs/HOOK_CAU_TRUC/00_CHUNG.md). KHÔNG còn luật viết hook nào khác: không phân loại
động cơ, không khuôn riêng lane, không đòi mở bằng thoại/cao trào/kịch tính/câu để ngỏ. Đổi tên họ, nghề, câu thoại theo hồ sơ
tập mình là đủ khác nội dung; giữ cấu trúc hook gốc không bị coi là trùng lặp.
Luồng: H1 bóc lời 0–150s + meta video gốc → H2 soi khung hình → H3 tách CẤU TRÚC hook gốc (phan_tich_cau_truc: cách mở,
nhịp, giây kết) → H4 viết N phương án cùng cấu trúc (brain_model) → check() tất định + Sol chấm bám cấu trúc → LOCK (sha256)
→ S2 viết thân NỐI từ hook. Hook là pure prose (TTS đọc mọi ký tự) — marker/visual nằm ở JSON riêng.
Repair mode (tập chưa đăng, có script.txt): nguồn = chính script.txt, không chạy S2, chỉ thêm hook đầu video.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_steps, profiles  # noqa: E402

HOOK_DIR = "hook"
MAX_PATCH_HOOK = 2
ROOT_DIR = Path(__file__).resolve().parent.parent
# Lời video gốc có mốc thời gian do TRENDING-RESEARCH tải sẵn (data/<kênh>/transcripts/<id>.json) — _nguon_tu_video_goc đọc trước.
TRENDING_DATA = Path(r"E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data")
# Cửa sổ lời gốc dùng để tách sườn hook (hook gốc Lane L dài tới ~105s).
GIAY_LOI_GOC = 150.0
# Sàn kỹ thuật độ dài hook (dưới mức này không dựng nổi 1 cảnh clip hook).
GIAY_SAN = 6.0
MAC_DINH = {
    # 2026-09-23: công tắc BẬT/TẮT hook THEO TỪNG KÊNH — mặc định TẮT, kênh phải tự khai `script.hook.enabled: true`.
    "enabled": False,
    # Ghim model VIẾT hook khác brain_model khi cần; rỗng = dùng brain_model. Lượt SỬA hook luôn dùng patch_model.
    "model": "",
    # Số phương án hook H4 viết (mặc định 2) — mọi phương án CÙNG một sườn, khác nhau ở cách thực thi.
    "so_ung_vien": 2,
    # 2026-10-21: độ dài hook = đúng giây kết hook của video gốc (chỉ kẹp sàn/trần kỹ thuật GIAY_SAN..GIAY_LOI_GOC).
    # `giay` [tối thiểu, tối đa] + `giay_mac_dinh` CHỈ dùng khi tập không có lời hook gốc. Field `huong_dan_cau_truc`
    # (khuôn hook riêng lane) đã BỎ 21/10 — profile còn khai thì bị bỏ qua.
    "giay": [15, 90],
    "giay_mac_dinh": 30,
    "tol": 0.25,
    # model ĐỌC CHỮ ở H1–H3 (phân tích lời video gốc). Phần NHÌN khung hình dùng Sol.
    "analysis_model": "claude-opus-5",
    # Chỉ cấm xin đăng ký/cảm ơn xem ở hook (CTA chỉ 1 lần ở cuối bài) — không còn luật cấm cách mở nào khác.
    "banned_openers": {
        "ja": ["チャンネル登録", "ご視聴"],
        "ko": ["구독"],
        "en": ["subscribe"]},
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


def so_ung_vien(prof):
    """Số phương án hook H4 viết (field `script.hook.so_ung_vien`, mặc định 2 — anh chốt 2026-09-30), kẹp 1..3."""
    return max(1, min(3, int(cau_hinh(prof).get("so_ung_vien") or 2)))


def _so_giay(x):
    """'64' / '60-65' / 64.0 → số giây (lấy mốc CUỐI của khoảng); không đọc được → None."""
    so = re.findall(r"\d+(?:\.\d+)?", str(x if x is not None else ""))
    return float(so[-1]) if so else None


def giay_hook(prof, src=None):
    """Độ dài hook (giây) = giây kết hook của video gốc (src.cau_truc_hook.giay_ket_hook) — gốc dài bao nhiêu làm bấy nhiêu,
    chỉ kẹp sàn/trần kỹ thuật [GIAY_SAN, GIAY_LOI_GOC]. Không có hook gốc → `script.hook.giay_mac_dinh` kẹp trong `giay`."""
    h = cau_hinh(prof)
    g = _so_giay(((src or {}).get("cau_truc_hook") or {}).get("giay_ket_hook"))
    if g:
        return max(GIAY_SAN, min(GIAY_LOI_GOC, g))
    lo, hi = (list(h.get("giay") or [15, 90]) + [90])[:2]
    return max(float(lo), min(float(hi), float(h.get("giay_mac_dinh") or 30)))


def so_chu_muc_tieu(prof, src=None):
    """Số chữ mục tiêu của hook = char_rate (chữ/phút) × giay_hook / 60."""
    return int(round(profiles.char_rate(prof) * giay_hook(prof, src) / 60.0))


def muc_cua_tap(d, prof):
    """Số chữ mục tiêu theo `hook/source.json` đã phân tích của tập (không có → mặc định lane). Không gọi mạng/LLM."""
    try:
        src = json.loads((Path(d) / HOOK_DIR / "source.json").read_text(encoding="utf-8"))
    except Exception:
        src = None
    return so_chu_muc_tieu(prof, src)


def cat_0_30s(segments, sec=30.0):
    return re.sub(r"\s+", " ", " ".join(s["text"] for s in segments if float(s.get("start", 0)) < sec)).strip()


def tach_candidates(text):
    parts = CAND_PAT.split(text)
    # split → [đầu, "1", body1, "2", body2, ...]
    return [parts[i].strip() for i in range(2, len(parts), 2) if parts[i].strip()]


def _sach(t):
    return re.sub(r"[\s、。「」！？…・ー－\-,.!?\"']", "", t)


def check(text, prof, ctx="", muc=None, cam_ho=None):
    """Phép đo tất định 0 LLM. Trả list việc phải sửa (rỗng = đạt). `muc` = số chữ mục tiêu của tập (theo giây hook gốc);
    vắng → mặc định lane. Chỉ đo kỹ thuật (độ dài ≈ gốc, marker, CTA, thoại tách câu cho TTS, số ngoài tư liệu) — không có
    luật cách viết hook nào ở đây (21/10: cách viết = bám cấu trúc hook gốc, Sol chấm)."""
    h = cau_hinh(prof)
    viec = []
    n = ai_steps.measure(text)["chars"]
    muc = int(muc or so_chu_muc_tieu(prof))
    lo, hi = int(muc * (1 - h["tol"])), int(muc * (1 + h["tol"]))
    if not (lo <= n <= hi):
        viec.append(f"độ dài {n} chữ ngoài {lo}–{hi} (≈ độ dài hook video gốc, char_rate {profiles.char_rate(prof):.0f})")
    for w in h["banned_openers"]:
        if w.lower() in text.lower():
            viec.append(f"hook không được xin đăng ký/cảm ơn xem (CTA chỉ ở cuối bài): 「{w}」")
    if ai_steps.MARKER_PAT.search(text):
        viec.append("hook chứa marker/ký hiệu — phải là pure prose")
    if cam_ho:
        # 2026-10-21 (Lane L ep23): hook tự do lấy lại họ 佐野 của ep04. cam_ho = kiem_hook_goc.ho_da_dung(tập).
        import kiem_hook_goc
        for x in kiem_hook_goc.ho_trung(text, cam_ho):
            viec.append(f"họ nhân vật đã dùng ở tập trước: {x} — đổi họ khác (lấy họ trong hồ sơ tập mình)")
    # 2026-09-26 (Lane M ep01): lane ĐA GIỌNG khai gate.dialogue_own_sentence — S3 (lean_script) bắt mọi「…」dính lời
    # dẫn, nhưng hook khoá ở đây KHÔNG bị kiểm luật đó → hook khoá chứa 「はい」とだけ答えた, S3 vừa đòi chép NGUYÊN VĂN
    # hook vừa đòi tách thoại → 2 patch đá nhau, ESCALATE. Cùng một luật phải kiểm ở cả hai cổng.
    if profiles.gate(prof).get("dialogue_own_sentence"):
        import cau_vai
        _cs = cau_vai.tach_cau(text)
        manh = [c["text"] for k, c in enumerate(_cs)
                if not cau_vai.la_thoai(c["text"]) and (
                    not re.search(r"[。！？!?」]$", c["text"].strip())
                    or (k and cau_vai.la_thoai(_cs[k - 1]["text"]) and _cs[k - 1]["para"] == c["para"]
                        and re.match(r"^[とっ、]", c["text"].strip())))]
        if manh:
            viec.append(f"THOẠI DÍNH LỜI DẪN (lane đa giọng): {len(manh)} chỗ, vd「{manh[0][:30]}」— mỗi「…」là 1 câu riêng, "
                        f"lời dẫn viết thành câu người kể riêng kết bằng 。")
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


def cau_truc_cua_tap(d):
    """cau_truc_hook đã tách của tập (hook/source.json) — None khi chưa có/không có nhịp."""
    try:
        ct = json.loads((Path(d) / HOOK_DIR / "source.json").read_text(encoding="utf-8")).get("cau_truc_hook") or {}
    except Exception:
        return None
    return ct if ct.get("nhip") else None


def khoa(d, text, mode="upstream", extra=None):
    import datetime as _dt
    d = Path(d)
    hd = d / HOOK_DIR
    hd.mkdir(exist_ok=True)
    # 2026-10-21 (anh chốt): không có cấu trúc hook gốc = CẤM khoá hook, kể cả khoá tay (Lane L ep23 bị khoá hook tự do).
    ct = cau_truc_cua_tap(d)
    if not ct:
        raise SystemExit(f"✗ KHÔNG khoá hook: {hd / 'source.json'} chưa có cấu trúc hook gốc (cau_truc_hook) — "
                         f"cấm hook viết tự do. Kiểm: py -3.13 -X utf8 {ROOT_DIR / 'pipeline' / 'kiem_hook_goc.py'} --tap {d}")
    extra = {"so_nhip_goc": len(ct["nhip"]), **(extra or {})}
    # 2026-10-11 (Lane L ep14): bản vá hook từng giữ nhãn「=== HOOK ===」ở đầu → S3 báo 'script không bắt đầu bằng
    # hook đã khoá' 2 lượt rồi ESCALATE. Bỏ nhãn ứng viên trước khi khoá.
    text = re.sub(r"^===\s*HOOK[^=\n]*===\s*", "", text.strip())
    text = text.strip() +("\n" if not text.endswith("\n") else "")
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
PROMPT_KHUNG = """Đây là lưới {n} khung hình lấy đều trong 30 giây đầu của một video YouTube kể chuyện.
Trả JSON: {{"so_shot_uoc": <số bố cục khác nhau>, "co_chu_tren_hinh": true/false, "co_nhan_vat": true/false,
"hinh_bam_loi": "manh|yeu|khong", "verdict": "manh|yeu|khong", "ly_do": "1 câu"}}
verdict = manh khi ≥3 bố cục khác nhau VÀ có nhân vật/vật thể gây chú ý; yeu khi 1–2 bố cục; khong khi chỉ ảnh nền/logo/chữ giới thiệu."""


def _nguon_tu_video_goc(d, proxy=None):
    """(2026-09-26, anh duyệt) Tập KHÔNG có `competitor.segments.json` (competitor.txt đưa vào dạng file sẵn) nhưng CÓ
    `video_goc.json` → tự tải lời có mốc thời gian (youtube-transcript-api, rồi phụ đề yt-dlp; KHÔNG whisper vì chỉ cần
    30 giây đầu) + meta, cache ở `hook/source_segments.json`. Trước bản vá: 4/6 tập gần nhất (L ep04–06, F ep05) ra
    phân tích hook RỖNG trong im lặng dù video_goc.json có đủ mã video. Không bao giờ ném — hỏng thì trả None."""
    d = Path(d)
    cache = d / HOOK_DIR / "source_segments.json"
    if cache.exists():
        try:
            j = json.loads(cache.read_text(encoding="utf-8"))
            return j if j.get("video_id") else None
        except Exception:
            pass
    try:
        vg = json.loads((d / "video_goc.json").read_text(encoding="utf-8")).get("video_goc") or {}
    except Exception:
        return None
    vid = (vg.get("id") or "").strip()
    if not vid:
        return None
    import fetch_script, kiem_hook_goc
    # Ưu tiên bản lời CÓ SẴN ở máy (TRENDING-RESEARCH / cache data\loi_goc — không mạng, không dính 429; đo thật
    # 2026-09-26: tải mạng video AjEK9D_JjxQ bị chặn IP ở cả 2 đường phụ đề). 2026-10-21: thêm đường whisper (không đụng
    # phụ đề) — lời gốc là ĐIỀU KIỆN BẮT BUỘC để viết hook (ensure_locked chặn cứng khi thiếu).
    segs, cach = kiem_hook_goc.tim_loi(vid, d, proxy=proxy)
    if not segs:
        print(f"  ! không có lời hook video gốc {vid}: {cach}")
        cach = ""
    try:
        m = fetch_script.lay_meta_video(vid, proxy=proxy)
    except Exception:
        m = {"title": vg.get("tieu_de", ""), "description": "", "thumbnail_url": ""}
    j = {"video_id": vid, "source": cach or "khong_co_loi", "title": m.get("title") or vg.get("tieu_de", ""),
         "description": m.get("description", ""), "thumbnail_url": m.get("thumbnail_url", ""),
         "segments": [{"start": float(s["start"]), "duration": float(s.get("duration", 0)), "text": s["text"]}
                      for s in segs if float(s.get("start", 0)) < GIAY_LOI_GOC]}
    (d / HOOK_DIR).mkdir(parents=True, exist_ok=True)
    if j["segments"]:   # KHÔNG cache bản rỗng lời — lần sau (hết 429) còn thử tải lại
        cache.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ nguồn hook lấy từ video_goc.json: {vid} · {len(j['segments'])} đoạn lời ({cach or 'không có lời'})")
    return j


def nguon_cua_tap(d):
    p = Path(d) / "competitor.segments.json"
    if not p.exists():
        return _nguon_tu_video_goc(d)
    try:
        j = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        # 2026-09-23: file có thể đang ghi dở (lần chạy trước bị ngắt) → JSON hỏng. phan_tich_nguon
        # KHÔNG BAO GIỜ được ném — coi như chưa có video nguồn, không phải lỗi chặn cả tập.
        print(f"  ! competitor.segments.json hỏng, coi như chưa có video nguồn: {type(e).__name__} {str(e)[:100]}")
        return None
    if isinstance(j, list):
        # 2026-10-15: lô Lane O tập 11–22 (TRENDING-RESEARCH) ghi competitor.segments.json dạng MẢNG trần
        # [{start, end, text}] (whisper), không có video_id/meta → bọc lại bằng video_goc.json của tập.
        try:
            vg = json.loads((Path(d) / "video_goc.json").read_text(encoding="utf-8")).get("video_goc") or {}
        except Exception:
            vg = {}
        if not (vg.get("id") or "").strip():
            return None
        j = {"video_id": vg["id"].strip(), "source": "competitor.segments.json (mảng whisper)",
             "title": vg.get("tieu_de", ""), "description": "", "thumbnail_url": "",
             "segments": [{"start": float(s["start"]),
                           "duration": float(s.get("duration", float(s.get("end", s["start"])) - float(s["start"]))),
                           "text": s["text"]} for s in j if s.get("text")]}
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
           "transcript_0_90s": "", "hook_4_nhip": {}, "hook_kind": "none", "score_0_12": 0, "video_hook_verdict": "khong_soi_duoc",
           "promise_match": {"verdict": "NA", "ly_do": "không có video nguồn"}}
    j = nguon_cua_tap(d)
    if j:
        vid = j["video_id"]
        src.update(video_id=vid, url=f"https://www.youtube.com/watch?v={vid}", title=j.get("title", ""),
                   description=j.get("description", ""), transcript_0_30s=cat_0_30s(j.get("segments") or []),
                   transcript_0_90s=cat_0_30s(j.get("segments") or [], 90.0),
                   transcript_hook=_loi_co_moc(j.get("segments") or []))
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
            # (c) 2026-09-26 anh duyệt: NHÌN khung hình = GPT-5.6-sol (sol_client, 3 đường dự phòng); lỗi thì rơi về
            # qc_visual._vision (thang Gemini cũ). Opus qua claude -p KHÔNG nhìn được ảnh (bridge tắt mọi tool).
            v = None
            try:
                import sol_client
                import qc_character as qcc
                txt, _u = sol_client.chat(PROMPT_KHUNG.format(n=6), grid, max_tokens=400, timeout=120)
                v = qcc._parse_json(txt)
                src["khung_hinh_model"] = "gpt-5.6-sol"
            except Exception as e:
                print(f"  ! Sol nhìn khung hình lỗi ({type(e).__name__} {str(e)[:80]}) → thử thang Gemini")
                try:
                    v = qc_visual._vision(PROMPT_KHUNG.format(n=6), grid)
                    src["khung_hinh_model"] = "qc_visual._vision"
                except Exception as e2:
                    print(f"  ! vision khung hình lỗi: {e2}")
            if isinstance(v, dict):
                src["video_hook_verdict"] = v.get("verdict", "khong_soi_duoc")
                src["khung_hinh"] = v
        # H1 cũ (4 nhịp A–E + promise) đã bỏ 17/10 — sườn hook gốc do phan_tich_cau_truc() tách ngay bên dưới.
    out_p.write_text(json.dumps(src, ensure_ascii=False, indent=2), encoding="utf-8")
    phan_tich_cau_truc(d, prof, src)
    return src


# ── H3 (anh chốt 2026-10-21): tách CẤU TRÚC hook video gốc — luật duy nhất "hook gốc thế nào mình làm thế ấy" ──
PROMPT_CAU_TRUC = """Bạn tách CẤU TRÚC HOOK của một video YouTube tiếng Nhật (video GỐC — tập mới sẽ viết hook bám sát cấu trúc này).
Chỉ MÔ TẢ hook gốc làm gì, theo thứ tự nào — không đánh giá, không xếp loại, không áp luật hook nào.
TIÊU ĐỀ GỐC: {title}
LỜI 0–150 GIÂY CỦA VIDEO GỐC (phụ đề tự động, có thể sai chính tả; [số] = giây):
{loi}

Trả ĐÚNG 1 JSON (không bọc ```):
{{"mo_dau": "1 câu tiếng Việt: giây 0 gốc mở bằng gì (vd câu thoại, tả cảnh, câu hỏi người dẫn, số liệu, người kể ngôi 1…)",
 "giay_ket_hook": <số giây hook gốc kết thúc và bắt đầu kể tuyến tính>,
 "nhip": [{{"tu": 0, "den": 5, "vai_tro": "vai trò nhịp (tiếng Việt)", "cach_lam": "gốc làm cụ thể thế nào (tiếng Việt)",
           "cau_goc": "trích ngắn tiếng Nhật", "dich": "nghĩa tiếng Việt"}}],
 "giu_chan_bang": "1 câu tiếng Việt: hook gốc giữ người xem bằng gì"}}
Nhịp = từng bước của hook theo đúng thứ tự (bao nhiêu nhịp tuỳ gốc), CHỈ tới giây kết hook."""


def _loi_co_moc(segments, sec=GIAY_LOI_GOC):
    """Lời gốc kèm mốc giây thưa (mỗi ~10s một mốc) cho prompt tách sườn — đủ để model biết nhịp rơi vào giây nào."""
    out, moc = [], -99.0
    for s in segments or []:
        t = float(s.get("start", 0))
        if t >= sec:
            break
        txt = re.sub(r"\s+", " ", str(s.get("text", ""))).strip()
        if not txt:
            continue
        if t - moc >= 10:
            out.append(f"[{int(t)}]{txt}")
            moc = t
        else:
            out.append(txt)
    return " ".join(out).strip()


def _loi_hook_goc(d, src):
    """Lời 0–150s video gốc (ưu tiên bản có mốc giây). Bản source.json cũ chỉ lưu 0–90s → đọc lại segments ở file local
    (competitor.segments.json / hook/source_segments.json), KHÔNG gọi mạng; không có thì dùng bản chữ đang có."""
    if src.get("transcript_hook"):
        return src["transcript_hook"]
    for p in (Path(d) / "competitor.segments.json", Path(d) / HOOK_DIR / "source_segments.json"):
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
            segs = j if isinstance(j, list) else (j.get("segments") or [])
            t = _loi_co_moc(segs)
            if t:
                return t
        except Exception:
            continue
    return src.get("transcript_0_90s") or src.get("transcript_0_30s") or ""


def phan_tich_cau_truc(d, prof, src, force=False):
    """H3: tách cấu trúc hook gốc → src['cau_truc_hook'] (ghi lại hook/source.json). Đã có thì dùng lại (trừ force; bản
    17/10 còn trường dong_co_chinh/khuon_lane thì khoi_suon() bỏ qua 2 trường đó). Không có lời gốc → None (ensure_locked chặn tập, cấm viết tự do).
    Lỗi model/JSON → None + cảnh báo, không ném."""
    if src.get("cau_truc_hook") and not force:
        return src["cau_truc_hook"]
    import kiem_hook_goc
    ct = kiem_hook_goc.doc_hook_goc_json(d, src.get("video_id") or "")
    if ct:   # 2026-10-21: TRENDING-RESEARCH giao sẵn cấu trúc hook gốc (hook_goc.json) → dùng luôn, không cần tải lời/LLM
        src["cau_truc_hook"], src["cau_truc_nguon"] = ct, "hook_goc.json"
        p = Path(d) / HOOK_DIR / "source.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(src, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[H3] cấu trúc hook gốc từ hook_goc.json: {len(ct['nhip'])} nhịp · kết ~{ct.get('giay_ket_hook')}s")
        return ct
    loi = _loi_hook_goc(d, src)
    if not loi:
        return None
    q = PROMPT_CAU_TRUC.format(title=src.get("title") or "(không rõ)", loi=loi[:5000])
    model_ptich = cau_hinh(prof).get("analysis_model") or "claude-opus-5"
    try:
        import claude_p_bridge
        r = claude_p_bridge.ask(q, model=model_ptich, timeout=600, min_chars=50)
    except Exception as e:
        print(f"  ! {model_ptich} tách sườn hook gốc lỗi ({type(e).__name__} {str(e)[:80]}) → Gemini")
        try:
            import llm_client
            r = llm_client.chat(q, task="short", max_tokens=2500, temperature=0.2, verbose=False)
        except Exception as e2:
            print(f"  ! Gemini tách sườn hook gốc cũng lỗi ({type(e2).__name__} {str(e2)[:80]}) → viết không có cấu trúc gốc")
            return None
    try:
        t = r.text.strip()
        mj = re.search(r"\{.*\}", t, re.S)
        ct = json.loads(mj.group(0) if mj else t)
        if not ct.get("nhip"):
            raise ValueError(f"thiếu nhip: {str(ct)[:120]}")
    except Exception as e:
        print(f"  ! JSON sườn hook gốc hỏng: {type(e).__name__} {str(e)[:120]}")
        return None
    src["cau_truc_hook"] = ct
    p = Path(d) / HOOK_DIR / "source.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(src, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[H3] cấu trúc hook gốc: mở {ct.get('mo_dau')} · {len(ct['nhip'])} nhịp · kết ~{ct.get('giay_ket_hook')}s")
    return ct


def khoi_suon(d, src):
    """Khối CẤU TRÚC HOOK GỐC chèn vào prompt viết + prompt Sol chấm."""
    ct = (src or {}).get("cau_truc_hook")
    if not ct:
        # 2026-10-21: nhánh "viết hook tự do" đã BỎ — ensure_locked chặn trước khi tới đây.
        raise SystemExit("✗ KHÔNG CÓ CẤU TRÚC HOOK GỐC — cấm viết hook tự do")
    nhip = "\n".join(
        f"  {i}. {n.get('tu', '?')}–{n.get('den', '?')}s · {n.get('vai_tro', '')} · {n.get('cach_lam', '')}"
        + (f" · gốc:「{n['cau_goc']}」({n.get('dich', '')})" if n.get("cau_goc") else "")
        for i, n in enumerate(ct.get("nhip") or [], 1))
    loi = _loi_hook_goc(d, src)
    return (f"CẤU TRÚC HOOK VIDEO GỐC CỦA TẬP NÀY (máy đã tách — BÁM SÁT):\n"
            f"- cách mở giây 0: {ct.get('mo_dau', '')}\n"
            f"- hook gốc kết ở ~{ct.get('giay_ket_hook', '?')} giây · giữ chân bằng: {ct.get('giu_chan_bang', '')}\n"
            f"- các nhịp theo thứ tự:\n{nhip}\n"
            + (f"LỜI HOOK VIDEO GỐC (nguyên văn — để bám cấu trúc; câu chữ phải đổi theo hồ sơ tập mình):\n{loi[:3000]}"
               if loi else ""))


PROMPT_VIET = """NHIỆM VỤ: viết {n} PHƯƠNG ÁN HOOK cho phần MỞ ĐẦU một video YouTube kể chuyện ({lang}).

LUẬT DUY NHẤT (anh chốt 2026-10-21): hook BÁM SÁT CẤU TRÚC hook của video gốc — gốc làm thế nào mình làm thế ấy.
- Giữ như gốc: cách mở giây 0 · các nhịp theo thứ tự + vai trò từng nhịp · độ dài ≈ hook gốc ({muc} chữ ±{tol}%).
- ĐƯỢC thay đổi một chút cho hợp tập mình hơn / hay hơn (gộp, tách, chỉnh một nhịp; đổi cách nói), nhưng tổng thể nghe
  ra vẫn đúng cấu trúc hook gốc.
- Đổi tên họ, tuổi, công việc/ngành nghề, câu thoại, chi tiết theo HỒ SƠ tập mình — không chép nguyên câu của gốc.
  Giữ cấu trúc hook gốc là ĐƯỢC PHÉP (không bị coi là trùng lặp nội dung).
- Ngoài điều trên KHÔNG có luật hook nào khác: không bắt mở bằng thoại, không bắt cao trào/kịch tính, không bắt câu để
  ngỏ, không khuôn nào của kênh — gốc có thì có, gốc không có thì không.
- Người/sự kiện/số phải khớp HỒ SƠ tập mình (để hook không vênh với thân bài).
- {n} phương án CÙNG một cấu trúc, khác nhau ở cách thực thi (chi tiết, câu chữ).

{suon}

HỒ SƠ / LỜI HỨA CỦA TẬP MÌNH (sự kiện, payoff, reveal — hook chỉ dùng thứ có ở đây):
{promise}
{khoi_repair}
KỸ THUẬT (cho TTS):
- Pure prose, không marker, không ngoặc vuông, không tiêu đề. Mỗi câu một dòng, mỗi「…」một dòng, không dòng trống trong hook.
- Không xin đăng ký/cảm ơn xem ở hook. Ngôi kể/văn thể: {narrator}.

OUTPUT ĐÚNG KHUÔN ({n} khối), không giải thích thêm:
{khuon}"""

KHOI_REPAIR = ("CHẾ ĐỘ REPAIR: kịch bản tập đã có sẵn và KHÔNG được sửa. Hook sẽ được ghép TRƯỚC đoạn 1 hiện có (dưới đây). "
               "Câu cuối hook phải là CÂU CẦU NỐI để đoạn 1 nghe như setup, không như bắt đầu lại:\nĐOẠN 1 HIỆN CÓ: {doan1}")

KHOI_THE_TEN = """THẺ TÊN ĐỘNG (luật dựng hình, docs/QUY_TAC_THE_TEN_NHAN_VAT_HOOK.md): tên + tuổi + nghề nhân vật chính hiện bằng
motion graphics lúc họ xuất hiện lần đầu. Lời hook ĐƯỢC đọc tên-tuổi(-nghề) bằng 1 câu ngắn ĐÚNG nhịp sườn có nhân vật
xuất hiện/giới thiệu — KHÔNG thêm nhịp mới chỉ để đọc tên, không đọc cả lý lịch dài."""


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
    n = prof.get("narrator", {}) or {}
    doan1 = ""
    if mode == "repair":
        doan1 = next((p.strip() for p in (d / "script.txt").read_text(encoding="utf-8").split("\n\n") if p.strip()), "")
    muc = so_chu_muc_tieu(prof, src)
    so = so_ung_vien(prof)
    prompt = PROMPT_VIET.format(
        lang=ai_steps.LANG_NAME.get(prof.get("language", "ja"), "Japanese"), n=so,
        khuon="\n".join(f"=== HOOK {i} ===\n<hook>" for i in range(1, so + 1)),
        suon=khoi_suon(d, src), promise=_promise_text(d, ctx, mode),
        khoi_repair=KHOI_REPAIR.format(doan1=doan1) if mode == "repair" else "",
        muc=muc, tol=int(cau_hinh(prof)["tol"] * 100),
        narrator=f"{n.get('persona','')} · {n.get('point_of_view','')} · {n.get('register','')}")
    import the_ten_hook
    if the_ten_hook.is_enabled(prof):
        prompt = prompt.replace("KỸ THUẬT (cho TTS):", KHOI_THE_TEN + "\n\nKỸ THUẬT (cho TTS):", 1)
    kwargs_viet = {"system": ai_steps._skill_text(prof, "script"), "task": "short",
                   "min_chars": muc * 2, "max_chars": muc * 6}
    model_hook = cau_hinh(prof).get("model") or ""
    if model_hook:
        if (prof.get("script", {}) or {}).get("engine") != "claude_p":
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
    prompt = (f"SỬA TẠI CHỖ đoạn hook dưới đây đúng các điểm sau, mọi thứ khác giữ nguyên từng chữ; pure prose, không "
              f"marker, GIỮ cấu trúc hook gốc (cách mở, thứ tự + vai trò từng nhịp).\n"
              f"CÁC ĐIỂM PHẢI SỬA:\n{ds}\n\n"
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
    phan_tich_cau_truc(d, prof, src)   # source.json cũ (trước 17/10) chưa có sườn → tách bổ sung, không tải lại video
    if not (src.get("cau_truc_hook") or {}).get("nhip") and not force and not _loi_hook_goc(d, src):
        # source.json từ lượt trước lưu bản RỖNG lời (dính 429) → tìm lời lại 1 lần (có thể đã có ở TRENDING/cache).
        src = phan_tich_nguon(d, prof, proxy=proxy, force=True)
    ct = src.get("cau_truc_hook") or {}
    if not ct.get("nhip"):
        # 2026-10-21 (anh chốt, Lane L ep23 佐野稔): không có cấu trúc hook gốc = KHÔNG viết hook, KHÔNG dựng tập.
        (hd / "hook_qc.json").write_text(json.dumps({"state": "NO_HOOK_GOC", "video_id": src.get("video_id")},
                                                    ensure_ascii=False, indent=2), encoding="utf-8")
        raise SystemExit(f"✗ H3: KHÔNG CÓ CẤU TRÚC HOOK GỐC (video {src.get('video_id') or 'không có'}) — CẤM viết hook tự do, "
                         f"tập DỪNG. Gỡ: có lời 0–150s video gốc (TRENDING-RESEARCH transcripts / competitor.segments.json) "
                         f"rồi chạy lại; kiểm: py -3.13 -X utf8 {ROOT_DIR / 'pipeline' / 'kiem_hook_goc.py'} --tap {d}")
    import kiem_hook_goc
    cam_ho = kiem_hook_goc.ho_da_dung(d)
    muc = so_chu_muc_tieu(prof, src)
    print(f"[H1-H3] nguồn {src.get('video_id')} · {len(ct['nhip'])} nhịp gốc · "
          f"mục tiêu {muc} chữ (~{giay_hook(prof, src):.0f}s) · cấm {len(cam_ho)} họ tập trước")
    title = title or _title(d)
    cands_text = viet_candidates(d, prof, src, title, ctx, mode)
    cands = tach_candidates(cands_text)[:so_ung_vien(prof)]
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
        v = check(c, prof, ctx, muc, cam_ho)
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
            raise SystemExit(f"✗ H3': mọi ứng viên trượt phép đo tất định, vá cứu cũng lỗi: {qc['check']}") from e
        qc["patches"] += 1
        if check(c2, prof, ctx, muc, cam_ho):
            (hd / "hook_qc.json").write_text(json.dumps({**qc, "state": "BLOCK"}, ensure_ascii=False, indent=2), encoding="utf-8")
            raise SystemExit(f"✗ H3': mọi ứng viên trượt phép đo tất định: {qc['check']}")
        hop = [(i, c2)]
    cands_hop = "\n".join(f"=== HOOK {i} ===\n{c}" for i, c in hop)
    text = None
    for vong in range(1, MAX_PATCH_HOOK + 2):
        verdict, chon, rep = qc_script_sol.run_hook(cands_hop, title, thumb, promise, profile_id=prof["id"],
                                                    so=len(hop), khop_tieu_de=False, suon=khoi_suon(d, src),
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
        if check(new, prof, ctx, muc, cam_ho):
            qc["log"].append(f"patch{vong} trượt tất định, giữ bản trước")
            new = chosen
        hop = [(chon, new)]
        cands_hop = f"=== HOOK {chon} ===\n{new}"
    qc.setdefault("state", "PASS")
    (hd / "hook_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = khoa(d, text, mode=mode, extra={"sol_rounds": qc["sol_rounds"], "patches": qc["patches"],
                                          "source_video_id": src.get("video_id"),
                                          "so_nhip_goc": len(ct.get("nhip") or [])})
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
    ap = argparse.ArgumentParser(description="H1–H4 hook bám sát cấu trúc hook video gốc (upstream) hoặc repair mode cho tập đã có script")
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
        print(json.dumps({k: src.get(k) for k in ("video_id", "hook_kind", "score_0_12", "video_hook_verdict", "cau_truc_hook")},
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
