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
