# -*- coding: utf-8 -*-
"""
H2DEV LESSON GRABBER — bắt trọn 1 bài học (audio) từ player mona-cloud rồi transcribe tiếng Việt.

CÁCH DÙNG:
  1) Mở Chrome profile dự án (đã login) kèm CDP:
     "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" ^
       --user-data-dir=E:\\CLAUDE\\YOUTUBE\\h2dev\\chrome_profile --profile-directory=Default ^
       --remote-debugging-port=9345 --disk-cache-size=1 --media-cache-size=1 ^
       https://h2dev.vn/learn/study/1
  2) py -3.13 learn_grab.py "<needle tên bài trong sidebar>" "<phần slug>" "<tên_output>"

CƠ CHẾ (đã trải nghiệm, xem docs/CAPTURE_NOTES):
  - Điều hướng bằng CLICK sidebar (SPA), KHÔNG goto — chỉ cách này Playwright mới với được iframe OOPIF.
  - Móc SourceBuffer.appendBuffer trong MỌI frame (add_init_script) để lấy đúng media player nạp
    (bỏ qua token/CORS/cache — không tải trực tiếp được vì segment khoá theo phiên, mở thẳng link 500/403).
  - Phát 16x, ĐỌC CHUNK DẦN (drain) trong lúc phát; dừng trước khi hết để tránh autoplay-next đóng iframe.
  - Media là fMP4; player hay re-init giữa chừng -> tách theo ranh giới 'ftyp', decode từng phần rồi ghép.
"""
import sys, time, base64, os, struct, subprocess
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9345"
HOOK = r"""
(() => { try {
  // SILENCER: ép muted ngay khi play (chạy trước script player) + quét định kỳ + bắt sự kiện play
  if (!window.__silenced) { window.__silenced = true;
    const op = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function(){ try{this.muted=true;this.volume=0;}catch(e){} return op.apply(this, arguments); };
    const force = () => { try{ document.querySelectorAll('video,audio').forEach(v=>{v.muted=true;v.volume=0;}); }catch(e){} };
    setInterval(force, 300); force();
    document.addEventListener('play', e=>{ try{e.target.muted=true;e.target.volume=0;}catch(_){} }, true);
  }
  if (window.__mseHooked) return; window.__mseHooked = true; window.__mseChunks = [];
  const origAdd = MediaSource.prototype.addSourceBuffer;
  MediaSource.prototype.addSourceBuffer = function(mime){
    const sb = origAdd.call(this, mime);
    try { const oa = sb.appendBuffer.bind(sb);
      sb.appendBuffer = function(data){
        try { const u8 = data instanceof ArrayBuffer ? new Uint8Array(data)
              : (data && data.buffer ? new Uint8Array(data.buffer, data.byteOffset||0, data.byteLength) : null);
          if (u8 && u8.length){ let bin=""; for(let i=0;i<u8.length;i+=0x8000) bin+=String.fromCharCode.apply(null,u8.subarray(i,i+0x8000));
            window.__mseChunks.push({mime:mime, b64:btoa(bin)}); } } catch(e){}
        return oa(data); };
    } catch(e){} return sb; };
} catch(e){} })();
"""

def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def split_and_decode(mp4_path, wav_out):
    d = open(mp4_path, "rb").read()
    bounds, i = [], 0
    while i + 8 <= len(d):
        size = struct.unpack('>I', d[i:i+4])[0]; typ = d[i+4:i+8]
        if size == 1: size = struct.unpack('>Q', d[i+8:i+16])[0]
        if size < 8 or i+size > len(d): break
        if typ == b'ftyp': bounds.append(i)
        i += size
    bounds.append(len(d))
    ff = ffmpeg(); parts = []
    base = os.path.splitext(mp4_path)[0]
    for k in range(len(bounds)-1):
        seg = d[bounds[k]:bounds[k+1]]
        pf = f"{base}_p{k}.mp4"; open(pf, "wb").write(seg)
        wf = f"{base}_p{k}.wav"
        r = subprocess.run([ff, "-y", "-i", pf, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wf],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(wf): parts.append(wf)
    lst = f"{base}_concat.txt"
    open(lst, "w").write("\n".join(f"file '{os.path.basename(p)}'" for p in parts))
    subprocess.run([ff, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", wav_out], cwd=os.path.dirname(mp4_path) or ".", capture_output=True)
    return wav_out

def grab(needle, slug_hint, out_mp4):
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        ctx = b.contexts[0]
        ctx.add_init_script(HOOK)
        page = ctx.pages[0]; page.bring_to_front()
        # Must be on the study shell already (Chrome launched at /learn/study/1). NEVER goto here — a full
        # navigation poisons the OOPIF so content_frame() stops working. Only SPA sidebar clicks.
        if "/learn/study/" not in page.url:
            page.goto("https://h2dev.vn/learn/study/1", wait_until="commit", timeout=60000); time.sleep(10)

        def sidebar_click(txt):
            page.evaluate("""(needle)=>{const els=[...document.querySelectorAll('*')].filter(e=>e.children.length===0&&e.tagName!=='SCRIPT'&&e.tagName!=='STYLE'&&(e.textContent||'').includes(needle)); if(!els.length)return; let n=els[0]; for(let i=0;i<10&&n;i++){const c=n.className?n.className.toString():''; if(c.includes('cursor-pointer'))break; n=n.parentElement;} (n||els[0]).click();}""", txt)

        # NOTE: relaunch Chrome before each grab so the tab is fresh. Do NOT click-away-then-back — that
        # loads another lesson's init segment into __mseChunks; combined with the reset below it drops the
        # target's init (ftyp/moov) -> undecodable mp4. On a fresh tab, sidebar_click(needle) mounts a clean
        # player and __mseChunks captures the init first.
        sidebar_click(needle)
        for _ in range(20):
            time.sleep(1)
            if slug_hint in page.url: break
        if slug_hint not in page.url:
            print("NAV FAILED", page.url[:90]); return None
        time.sleep(3)
        fr = None
        for _ in range(25):
            el = page.query_selector("iframe[src*='mona-cloud']")
            if el:
                f = el.content_frame()
                if f:
                    try:
                        if f.query_selector("video"): fr = f; break
                    except Exception: pass
            try: page.evaluate("""()=>{const c=[...document.querySelectorAll('div,button,span')].find(e=>(e.className||'').toString().includes('rounded-full')&&e.offsetWidth>30&&e.offsetWidth<130); if(c)c.click();}""")
            except Exception: pass
            time.sleep(2)
        if not fr: print("NO CONTENT FRAME"); return None
        print("frame ok", flush=True)
        # Do NOT reset __mseChunks: the init segment (ftyp/moov) is appended on mount BEFORE this point;
        # clearing it makes the mp4 undecodable. On a fresh tab __mseChunks holds only this lesson's data.
        fr.evaluate("""()=>{const v=document.querySelector('video'); if(v){v.muted=true;v.currentTime=0;v.playbackRate=8;v.play().catch(()=>{});}}""")
        buckets = {}; read_idx = [0]
        def drain():
            try: total = fr.evaluate("()=>window.__mseChunks?window.__mseChunks.length:0")
            except Exception: return
            while read_idx[0] < total:
                hi = min(read_idx[0]+15, total)
                try: rows = fr.evaluate("""({a,b})=>window.__mseChunks.slice(a,b)""", {"a": read_idx[0], "b": hi})
                except Exception: return
                for c in rows: buckets.setdefault(c["mime"], bytearray()).extend(base64.b64decode(c["b64"]))
                read_idx[0] = hi
        last_ch = -1; stall = 0; last_cur = -1; cur_stall = 0
        for _ in range(600):
            try: info = fr.evaluate("""()=>{const v=document.querySelector('video'); if(!v)return null; v.muted=true;v.playbackRate=8; if(v.paused&&v.currentTime<v.duration-8)v.play().catch(()=>{}); return {dur:v.duration,cur:v.currentTime,ch:(window.__mseChunks?window.__mseChunks.length:0)};}""")
            except Exception: info = None
            if info and info.get("dur"):
                print(f"t={info['cur']:.0f}/{info['dur']:.0f} ch={info['ch']}", flush=True)
                drain()
                # normal end
                if info["cur"] >= info["dur"] - 12:
                    try: fr.evaluate("()=>{const v=document.querySelector('video'); if(v)v.pause();}")
                    except Exception: pass
                    time.sleep(1); drain(); break
                # stall detection: chunks stopped growing while near the end -> done
                if info["ch"] == last_ch:
                    stall += 1
                else:
                    stall = 0; last_ch = info["ch"]
                # cur-stall: playhead stuck (near end, player won't advance past buffered end)
                if abs(info["cur"] - last_cur) < 0.5:
                    cur_stall += 1
                else:
                    cur_stall = 0; last_cur = info["cur"]
                near = info["cur"] >= info["dur"] * 0.8
                if near and (stall >= 3 or cur_stall >= 3):
                    print("stall near end -> done", flush=True)
                    time.sleep(1); drain(); break
            time.sleep(2)
        # save audio bucket (what we transcribe)
        audio = None
        for mime, data in buckets.items():
            tag = "audio" if "audio" in mime else ("video" if "video" in mime else "mux")
            fn = f"{os.path.splitext(out_mp4)[0]}_{tag}.mp4"; open(fn, "wb").write(data)
            if tag == "audio": audio = fn
            print("saved", mime, fn, len(data), flush=True)
        return audio

if __name__ == "__main__":
    needle, slug_hint, out = sys.argv[1], sys.argv[2], sys.argv[3]
    a = grab(needle, slug_hint, out)
    if a:
        wav = os.path.splitext(out)[0] + ".wav"
        split_and_decode(a, wav)
        print("WAV:", wav, os.path.getsize(wav) if os.path.exists(wav) else "FAIL")
