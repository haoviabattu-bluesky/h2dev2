"""fetch_script.py — bóc transcript (kịch bản/voiceover) video đối thủ để nhân bản 70/30.

BA ĐƯỜNG, tự động tụt xuống khi đường trên hỏng (đo thật 2026-09-08: YouTube chặn 429 endpoint
phụ đề `/api/timedtext` theo IP — chặn CẢ khi gọi từ trong trình duyệt thật, nên đường 1+2 có thể
chết cùng lúc; đường 3 KHÔNG đụng phụ đề nên vẫn chạy):

  1. `youtube-transcript-api`  — nhanh nhất (~2s), cần YouTube cho phép IP.
  2. `yt-dlp` tải file phụ đề  — vẫn là endpoint timedtext, chỉ khác cách gọi.
  3. `yt-dlp` tải TIẾNG + `faster-whisper` nghe lại — chậm (vài phút) nhưng KHÔNG bao giờ bị chặn,
     và chạy được cả với video KHÔNG có phụ đề.

Dùng:
  py -3.13 fetch_script.py "<url hoặc video_id>"                  # in ra + lưu .txt
  py -3.13 fetch_script.py "<url>" --out competitor.txt --lang ko,ja,en
  py -3.13 fetch_script.py "<url>" --method whisper               # ép nghe lại bằng whisper
  py -3.13 fetch_script.py "<url>" --raw                          # kèm timestamp
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import paths

sys.stdout.reconfigure(encoding="utf-8")


def video_id(s):
    s = s.strip()
    m = re.search(r"(?:v=|/shorts/|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    raise SystemExit(f"Không nhận ra video id từ: {s}")


# ---------------------------------------------------------------- đường 1: API
def via_api(vid, langs, proxy=None):
    """proxy: 1 URL HTTP(S), vd 'http://user:pass@host:port' — dùng khi IP bị 429 kéo dài.
    Bản youtube_transcript_api CŨ (pre-GenericProxyConfig) không nhận tham số này → tự bỏ qua
    proxy cho đường 1, KHÔNG chết cả hàm (đường 2/3 vẫn dùng được proxy bình thường)."""
    from youtube_transcript_api import YouTubeTranscriptApi
    if proxy:
        try:
            from youtube_transcript_api.proxies import GenericProxyConfig
            api = YouTubeTranscriptApi(proxy_config=GenericProxyConfig(http_url=proxy, https_url=proxy))
        except (ImportError, TypeError):
            print("  ! youtube_transcript_api bản cũ không hỗ trợ proxy_config — bỏ qua proxy ở đường 1")
            api = YouTubeTranscriptApi()
    else:
        api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(vid, languages=langs)
        return [{"text": s.text, "start": s.start, "duration": s.duration} for s in fetched]
    except AttributeError:
        return YouTubeTranscriptApi.get_transcript(vid, languages=langs)


# ------------------------------------------------------------- đường 2: yt-dlp
def _ts(v):
    h, m, s = v.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s.replace(",", "."))


def parse_vtt(txt):
    """VTT → [{text,start,duration}].

    ⚠️ Phụ đề TỰ ĐỘNG của YouTube là kiểu CUỘN (roll-up): cue sau chép lại các dòng của cue trước
    rồi thêm 1 dòng mới. Bỏ trùng theo CẢ KHỐI là không đủ — text ra bị nhân 3 (đo thật
    l0p1EnDcXYM: 37.998 ký tự cho video 27 phút). Phải bỏ trùng theo TỪNG DÒNG."""
    segs, seen = [], []
    for block in re.split(r"\n\s*\n", txt):
        m = re.search(r"(\d+:\d\d:\d\d[.,]\d+)\s*-->\s*(\d+:\d\d:\d\d[.,]\d+)", block)
        if not m:
            continue
        raw = [re.sub(r"<[^>]+>", "", l).strip()          # bỏ tag <c>, <00:00:01.000>
               for l in block.splitlines() if "-->" not in l and not l.strip().isdigit()]
        fresh = [l for l in raw if l and l not in seen]    # chỉ giữ dòng CHƯA từng xuất hiện
        seen = (seen + raw)[-6:]                           # nhớ vài dòng gần nhất là đủ
        body = re.sub(r"\s+", " ", " ".join(fresh)).strip()
        if not body:
            continue
        a, b = _ts(m.group(1)), _ts(m.group(2))
        segs.append({"text": body, "start": a, "duration": max(0.1, b - a)})
    return segs


def via_ytdlp_subs(vid, langs, workdir, tries=4, proxy=None):
    """Tải auto-subs (ASR) THẲNG — vài giây, KHÔNG whisper. 429 timedtext là TẠM → retry backoff.
    Cookies YouTube (env YTDLP_COOKIES=path hoặc YTDLP_COOKIES_BROWSER=chrome) giảm hẳn 429.
    proxy: 1 URL HTTP(S) — yt-dlp tự dùng cho MỌI request của đường này (kể cả lúc retry)."""
    import os
    pats = ",".join(dict.fromkeys([f"{l}.*" for l in langs] + ["en.*"]))
    # Gọi yt_dlp bằng API Python, KHÔNG `sys.executable -m yt_dlp`: khi đóng .exe thì
    # sys.executable là chính exe, `-m` không chạy được (bẫy #23 skill tao_tool_exe).
    opts = {"quiet": True, "no_warnings": True, "noprogress": True, "skip_download": True, "writesubtitles": True,
            "writeautomaticsub": True, "subtitleslangs": pats.split(","), "subtitlesformat": "vtt",
            "retries": 5, "sleep_interval_requests": 1, "ignore_no_formats_error": True,
            "outtmpl": str(workdir / "s.%(ext)s")}
    if proxy:
        opts["proxy"] = proxy
    if os.environ.get("YTDLP_COOKIES"):
        opts["cookiefile"] = os.environ["YTDLP_COOKIES"]
    elif os.environ.get("YTDLP_COOKIES_BROWSER"):
        opts["cookiesfrombrowser"] = (os.environ["YTDLP_COOKIES_BROWSER"],)
    files = []
    for i in range(tries):
        try:
            import yt_dlp
            with yt_dlp.YoutubeDL(opts) as y:
                y.download([f"https://www.youtube.com/watch?v={vid}"])
        except Exception:
            pass                       # 429/không có phụ đề → thử lại hoặc tụt xuống whisper
        files = sorted(workdir.glob("s.*.vtt"))
        if files:
            break
        if i < tries - 1:
            wait = 20 * (i + 1)   # 20s,40s,60s — 429 timedtext thường tự hết
            print(f"  … yt-dlp subs trống (nghi 429), chờ {wait}s rồi thử lại [{i+2}/{tries}]")
            time.sleep(wait)
    if not files:
        raise RuntimeError("yt-dlp không tải được file phụ đề nào (429 timedtext kéo dài → cần proxy/cookies)")
    # ưu tiên đúng thứ tự ngôn ngữ người dùng xin
    for l in langs:
        for f in files:
            if f.name.split(".")[1].startswith(l):
                return parse_vtt(f.read_text(encoding="utf-8", errors="replace"))
    return parse_vtt(files[0].read_text(encoding="utf-8", errors="replace"))


# ------------------------------------------------------------ đường 3: whisper
def via_whisper(vid, langs, workdir, model_size="base", proxy=None):
    """Tải TIẾNG rồi nghe lại. KHÔNG đụng phụ đề nên không dính 429 (đường an toàn nhất khi bị
    chặn kéo dài — kể cả không có proxy). proxy vẫn truyền xuống nếu có, phòng khi audio format
    cũng bị chặn theo IP."""
    # Kiểm TRƯỚC khi tải: bản .exe cố tình KHÔNG kèm faster-whisper (kéo theo ctranslate2 nặng vài
    # trăm MB). Không kiểm sớm thì tải xong ~30MB audio mới báo thiếu module — vừa mất thời gian
    # vừa để lộ ModuleNotFoundError làm người dùng tưởng tool hỏng.
    try:
        import faster_whisper                                    # noqa: F401
    except Exception:
        raise RuntimeError(
            "bản này không kèm faster-whisper nên không nghe lại được. "
            "Cách xử lý: mở video, bấm '...' → 'Hiển thị bản chép lời', copy rồi dán vào "
            "competitor.txt trong thư mục tập" +
            ("" if getattr(sys, "frozen", False) else " (hoặc: pip install faster-whisper)"))
    print("  … tải audio (yt-dlp)")
    base_opts = {"quiet": True, "no_warnings": True, "noprogress": True,
                "format": "bestaudio/best",
                "outtmpl": str(workdir / "a.%(ext)s"),
                "postprocessors": [{"key": "FFmpegExtractAudio",
                                    "preferredcodec": "mp3",
                                    "preferredquality": "5"}]}
    # Bẫy frozen: postprocessor này gọi ffmpeg trên PATH. Máy khách thường KHÔNG có ffmpeg, còn bản
    # bundle của imageio_ffmpeg nằm trong _internal nên yt-dlp không tự thấy → phải chỉ đường tay.
    try:
        import imageio_ffmpeg
        base_opts["ffmpeg_location"] = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    if proxy:
        base_opts["proxy"] = proxy
    import yt_dlp
    err = ""
    # "Requested format is not available" đo thật (2026-09-09, video vU5PWT2zLDs) KHÔNG tái hiện
    # lại được ngay sau đó — thử tay bằng cùng opts, cùng video là chạy được → lỗi TẠM THỜI phía
    # YouTube lúc đó (server trả về danh sách format rút gọn khi có nghi ngờ bot/rate-limit), chứ
    # không phải video thật sự thiếu audio. `via_ytdlp_subs` đã có thử lại cho lỗi 429 tương tự,
    # nhánh này trước đó KHÔNG có — bước cuối cùng (không còn đường nào khác) mà hỏng ngay lần đầu
    # là dừng cả video. Thử lại 3 lần, lần sau đổi `player_client` (web → android → ios): nguyên
    # nhân phổ biến nhất của lỗi này trong 2026 là 1 client cụ thể bị YouTube tạm chặn khi các
    # client khác vẫn phục vụ bình thường — đổi client hay tự khỏi mà không cần đợi.
    for lan_thu, client in enumerate((None, "android", "ios"), 1):
        opts = dict(base_opts)
        if client:
            opts["extractor_args"] = {"youtube": {"player_client": [client]}}
        try:
            with yt_dlp.YoutubeDL(opts) as y:
                y.download([f"https://www.youtube.com/watch?v={vid}"])
            err = ""
            break
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            if lan_thu < 3:
                cho = 8 * lan_thu
                print(f"  … tải audio lỗi ({err.splitlines()[0][:100]}), thử lại "
                     f"[{lan_thu+1}/3, client={client or 'web'}] sau {cho}s")
                time.sleep(cho)
    mp3 = next(iter(sorted(workdir.glob("a.*"))), None)
    if not mp3:
        raise RuntimeError(f"yt-dlp không tải được audio sau 3 lần thử: {err[-300:]}\n"
                          "→ Nếu vẫn lỗi: mở video, bấm '...' → 'Hiển thị bản chép lời', copy rồi "
                          "dán vào competitor.txt trong thư mục tập, chạy lại (bước này tự bỏ qua "
                          "khi competitor.txt đã có sẵn).")
    import os
    th = max(4, min(16, (os.cpu_count() or 8)))
    # Model nằm SẴN cạnh exe (models/faster-whisper-<size>) thì dùng luôn. Nếu để faster-whisper tự
    # lo, nó tải ~142MB từ HuggingFace ở LẦN CHẠY ĐẦU — máy khách mạng chậm/bị chặn HF là gãy giữa
    # bài, mà lúc đó đã tải xong audio rồi. Bundle sẵn thì bước này chạy offline hoàn toàn.
    local = paths.res(f"models/faster-whisper-{model_size}")
    target = str(local) if (local / "model.bin").exists() else model_size
    print(f"  … nghe lại bằng faster-whisper ({model_size}, lang={langs[0]}, {th} luồng"
          f"{', model bản địa' if target != model_size else ', tải từ HuggingFace nếu chưa có'})")
    from faster_whisper import WhisperModel
    # Bản nghe này CHỈ để PASS 0 rút ra ~10 nhịp chức năng — mọi tên/số/câu chữ đều bị vứt đi.
    # Nên KHÔNG cần độ chính xác từng chữ: `base` + greedy đủ dùng và nhanh hơn `small`+beam5 nhiều.
    m = WhisperModel(target, device="cpu", compute_type="int8",
                     cpu_threads=th, num_workers=2)
    it, _ = m.transcribe(str(mp3), language=langs[0], vad_filter=True,
                         beam_size=1,                      # greedy: nhanh gần gấp đôi beam=5
                         condition_on_previous_text=False)  # tránh vòng lặp lải nhải + nhanh hơn
    return [{"text": s.text.strip(), "start": s.start, "duration": s.end - s.start}
            for s in it if s.text.strip()]


# ----------------------------------------------------------------------- chạy
def fetch_any(vid, langs, method="auto", whisper_model="small", proxy=None):
    """Trả (segs, tên_đường_đã_dùng). Tự tụt xuống đường dưới khi đường trên hỏng.

    proxy: 1 URL HTTP(S) truyền xuống CẢ 3 đường (vd IP bị YouTube 429 kéo dài, đổi IP qua proxy
    thường nhanh hơn chờ 429 tự hết). Không có proxy vẫn chạy bình thường — đường 3 (whisper)
    không đụng timedtext nên vốn đã KHÔNG dính 429, là lưới an toàn cuối kể cả không có proxy."""
    order = {"auto": ["api", "ytdlp", "whisper"], "api": ["api"],
             "ytdlp": ["ytdlp"], "whisper": ["whisper"]}[method]
    work = Path(tempfile.mkdtemp(prefix="fetch_"))
    errs = []
    try:
        for name in order:
            try:
                if name == "api":
                    segs = via_api(vid, langs, proxy=proxy)
                elif name == "ytdlp":
                    segs = via_ytdlp_subs(vid, langs, work, proxy=proxy)
                else:
                    segs = via_whisper(vid, langs, work, whisper_model, proxy=proxy)
                if segs:
                    return segs, name
                errs.append(f"{name}: rỗng")
            except Exception as e:
                errs.append(f"{name}: {type(e).__name__} {str(e).splitlines()[0][:120]}")
                print(f"  ✗ {errs[-1]} → thử đường tiếp")
        raise SystemExit("Không bóc được transcript.\n  " + "\n  ".join(errs) +
                         "\n→ Cách cuối: tự dán kịch bản đối thủ vào file competitor.txt.")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def video_minutes(url_or_id, timeout=25, proxy=None):
    """Thời lượng video nguồn, tính bằng PHÚT (float). Không lấy được thì trả 0.

    Dùng để bản clone dài BẰNG video gốc. Ép cứng một con số cho cả kênh là sai: cùng một kênh
    có video 28 phút lẫn 44 phút, ép hết về 30 thì bài ngắn bị kéo lê còn bài dài bị cắt cụt.

    `extract_flat` nên chỉ đọc metadata, không tải gì — đo thật ~0,5s.
    """
    try:
        import yt_dlp
        vid = video_id(url_or_id)
        opts = {"quiet": True, "no_warnings": True, "skip_download": True,
                "extract_flat": True, "noprogress": True, "socket_timeout": timeout}
        if proxy:
            opts["proxy"] = proxy
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
        sec = (info or {}).get("duration") or 0
        return round(sec / 60.0, 1) if sec else 0.0
    except Exception as e:
        print(f"  ! không đọc được thời lượng video gốc ({type(e).__name__} {e})")
        return 0.0


def _fix_dash_id(argv):
    """ID YouTube được phép BẮT ĐẦU bằng '-' (bộ chữ base64url), vd `-Gt6QYEFS38`.

    argparse thấy token mở đầu bằng '-' là coi như một tham số → `fetch_script.py -Gt6QYEFS38`
    chết với "the following arguments are required: url", còn `--competitor -Gt6QYEFS38` chết với
    "expected one argument". Đây KHÔNG phải lỗi gõ: khoảng 1/64 video có id như vậy, tức là cứ vài
    chục video quét từ kênh là gặp một cái. Đổi sớm thành URL đầy đủ cho argparse khỏi nhầm.
    """
    out = []
    for a in argv:
        if re.fullmatch(r"-[A-Za-z0-9_-]{10}", a):
            out.append("https://www.youtube.com/watch?v=" + a)
        else:
            out.append(a)
    return out


def main():
    sys.argv[1:] = _fix_dash_id(sys.argv[1:])
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="URL hoặc video_id YouTube đối thủ")
    ap.add_argument("--out", default="", help="file lưu (mặc định: <id>_transcript.txt)")
    ap.add_argument("--lang", default="en", help="ngôn ngữ ưu tiên, cách nhau bằng dấu phẩy (ko,ja,en)")
    ap.add_argument("--raw", action="store_true", help="giữ timestamp mỗi dòng")
    ap.add_argument("--method", default="auto", choices=["auto", "api", "ytdlp", "whisper"])
    ap.add_argument("--whisper-model", default="base", help="tiny/base/small/medium (càng to càng chậm)")
    ap.add_argument("--proxy", default="", help="proxy HTTP(S) dùng cho cả 3 đường khi IP bị 429 kéo dài, vd http://user:pass@host:port")
    args = ap.parse_args()

    vid = video_id(args.url)
    langs = [x.strip() for x in args.lang.split(",") if x.strip()]
    segs, used = fetch_any(vid, langs, args.method, args.whisper_model, proxy=args.proxy or None)

    if args.raw:
        text = "\n".join(f"[{int(s['start'])//60:02d}:{int(s['start'])%60:02d}] {s['text']}" for s in segs)
    else:
        text = re.sub(r"\s+", " ", " ".join(s["text"].replace("\n", " ").strip() for s in segs)).strip()

    out = Path(args.out) if args.out else Path(f"{vid}_transcript.txt")
    out.write_text(text, encoding="utf-8")
    # Sidecar cho cong B2Q (qc_transcript.py): moc thoi gian tung doan + thoi luong video. Ghi KEM,
    # khong doi dinh dang competitor.txt (moi tool khac van doc .txt nhu cu).
    try:
        dur_sec = round(video_minutes(vid, proxy=args.proxy or None) * 60, 1)
    except Exception:
        dur_sec = 0.0
    side = out.with_name(out.stem + ".segments.json")
    side.write_text(json.dumps({"video_id": vid, "source": used, "video_duration_sec": dur_sec,
                                "segments": [{"start": float(s["start"]), "duration": float(s.get("duration", 0)),
                                              "text": s["text"]} for s in segs]},
                               ensure_ascii=False), encoding="utf-8")
    print(f"✓ {vid} [{used}]: {len(segs)} đoạn, {len(text):,} ký tự → {out}  (+{side.name})")
    print("─" * 60)
    print(text[:800] + (" ..." if len(text) > 800 else ""))


if __name__ == "__main__":
    main()
