# -*- coding: utf-8 -*-
"""
BATCH driver: nghe TOÀN BỘ khoá h2dev theo thứ tự ưu tiên module.
Với mỗi bài chưa có transcript: grab audio (learn_grab) -> split/decode WAV -> faster-whisper -> lưu
transcript vào docs/transcripts/<slug>.txt. Bỏ qua bài đã có transcript. Ghi log tiến độ ra stdout.

CHẠY: Chrome đã mở sẵn ở /learn/study/1 (xem learn_grab header). Rồi:
  py -3.13 tools\learn_all.py [start_index]
"""
import sys, os, json, time, traceback
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import learn_grab
from faster_whisper import WhisperModel

ROOT = r"E:\CLAUDE\YOUTUBE\h2dev"
CATALOG = os.path.join(ROOT, "docs", "catalog.json")
TDIR = os.path.join(ROOT, "docs", "transcripts")
WORK = os.path.join(ROOT, "tools", "_grab_work")   # nơi để wav/mp4 tạm
os.makedirs(TDIR, exist_ok=True)
os.makedirs(WORK, exist_ok=True)

# thứ tự ưu tiên module (Module 4 để cuối vì 88 video)
PRIO = [
    "Bắt đầu tại đây", "Module 1", "Xử lý & Kháng lỗi", "Module 2",
    "Hướng dẫn quy trình dùng Claude AI", "Module 3", "Module 5",
    "Module 6", "Module 7", "Module 8", "VIP - Module 4",
]
def prio(mod):
    for i, p in enumerate(PRIO):
        if mod.startswith(p): return i
    return 99

def safe_slug(slug):
    return slug[:80]

def main():
    cat = json.load(open(CATALOG, encoding="utf-8"))
    # gắn thứ tự gốc trong từng module để giữ 01,02,...
    items = list(enumerate(cat))
    items.sort(key=lambda x: (prio(x[1]["module"]), x[0]))
    order = [c for _, c in items]

    print("Loading whisper model...", flush=True)
    model = WhisperModel("small", device="cpu", compute_type="int8")

    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    total = len(order)
    for idx in range(start, total):
        c = order[idx]
        slug = c["slug"]; name = c["name"]
        tpath = os.path.join(TDIR, safe_slug(slug) + ".txt")
        if os.path.exists(tpath) and os.path.getsize(tpath) > 800:
            print(f"[{idx+1}/{total}] SKIP (done): {name[:60]}", flush=True)
            continue
        print(f"[{idx+1}/{total}] GRAB: {name[:70]}", flush=True)
        try:
            expected = int(c.get("time_s") or 0)
            outmp4 = os.path.join(WORK, f"les_{idx}")
            wav = outmp4 + ".wav"
            # grab with coverage-check + up to 2 retries (short capture = re-mount didn't take)
            ok = False
            for attempt in range(3):
                audio = learn_grab.grab(name, slug, outmp4)
                if not audio:
                    print(f"   grab fail (nav/frame) attempt {attempt+1}", flush=True)
                    time.sleep(2); continue
                learn_grab.split_and_decode(audio, wav)
                if not os.path.exists(wav):
                    print("   no wav", flush=True); continue
                import wave as _w
                try:
                    ww = _w.open(wav); dur = ww.getnframes()/ww.getframerate(); ww.close()
                except Exception:
                    dur = 0
                need = max(30, expected * 0.6) if expected else 30
                print(f"   wav {dur:.0f}s / expected {expected}s (need>{need:.0f})", flush=True)
                if dur >= need:
                    ok = True; break
                print(f"   SHORT capture, retry {attempt+1}", flush=True)
                time.sleep(2)
            if not ok:
                print("   GIVE UP (short/failed).", flush=True); continue
            # transcribe
            segs, info = model.transcribe(wav, language="vi", vad_filter=True,
                                          vad_parameters=dict(min_silence_duration_ms=500))
            lines = [f"[{int(s.start//60):02d}:{int(s.start%60):02d}] {s.text.strip()}" for s in segs]
            open(tpath, "w", encoding="utf-8").write("\n".join(lines))
            print(f"   OK transcript {len(lines)} lines -> {os.path.basename(tpath)}", flush=True)
            # dọn file tạm nặng để đỡ đầy ổ
            for ext in ("_audio.mp4", "_video.mp4", ".wav"):
                try: os.remove(outmp4 + ext)
                except Exception: pass
            for f in os.listdir(WORK):
                if f.startswith(f"les_{idx}_") or f.startswith(f"les_{idx}."):
                    try: os.remove(os.path.join(WORK, f))
                    except Exception: pass
        except Exception as e:
            print("   ERROR:", repr(e)[:200], flush=True)
            traceback.print_exc()
            time.sleep(3)
    print("BATCH DONE", flush=True)

if __name__ == "__main__":
    main()
