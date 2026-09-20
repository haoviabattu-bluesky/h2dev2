"""openspeaker_tts.py — client TTS ai33.pro / OpenSpeaker (proxy ElevenLabs/MiniMax giá rẻ).

Voice CHÍNH cho Satori JP (chất ElevenLabs). Gửi CẢ kịch bản 1 lần (≤1M chars), trả mp3 + SRT sẵn.

⚠️ PITFALL (đã dính): curl -F mangle UTF-8 CJK thành ?????  → BẮT BUỘC dùng requests, gửi text dạng
bytes UTF-8 trong multipart (files=) để giữ nguyên tiếng Nhật/Hàn. KHÔNG dùng curl cho text CJK.

Flow (verify thật 2026-09-07):
  POST /v3/text-to-speech (FormData) → {task_id}
  → poll GET /v1/task/{id} tới status=done VÀ metadata.transcript_status=completed
  → tải metadata.audio_url (mp3 44.1kHz) + srt_url (phụ đề timestamps chuẩn)

Giọng Satori JP: elevenlabs_7arouBAZXrSnH9IwDlWQ (Enishi - Deep Japanese Storyteller).
"""
import time

import requests

import keys

BASE = "https://api.openspeaker.ai"
# Key gói đã mua (cũng ở CLAUDE.md dự án). Header xi-api-key, KHÔNG Bearer.
# Đổi ở máy khác: khoá `openspeaker` trong keys.json CẠNH exe (hoặc biến AI33_API_KEY).
API_KEY = keys.get("openspeaker", env="AI33_API_KEY",
                   default="sk_vdplz671t7nq190rwxrwd52lj30z1giekav30rh0mkaqzleo")

# Giọng đã chấm cho Satori JP
VOICE_ENISHI = "elevenlabs_7arouBAZXrSnH9IwDlWQ"   # Deep Japanese Storyteller (CHÍNH)
VOICE_PAPAJI = "elevenlabs_rDiGqdvxRVKhplqZE31x"   # Deep Wise (dự phòng)
VOICE_AKIRA = "elevenlabs_JKne0OHHjFFwcwWzlGj0"    # Calm Deep (dự phòng)
VOICE_SENIOR = "minimax_209533299589242"           # Intellectual Senior (minimax)

POLL_INTERVAL = 5
POLL_TIMEOUT = 900     # kịch bản dài có thể lâu


class OpenSpeakerError(Exception):
    pass


def _headers():
    return {"xi-api-key": API_KEY}


def get_credits():
    r = requests.get(f"{BASE}/v1/credits", headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json()


def submit(text, voice_id, speed=0.95, with_transcript=True, file_name="satori"):
    """Gửi task. text dạng bytes UTF-8 trong multipart (CJK-safe). Trả task_id."""
    files = {
        "voice_id": (None, voice_id),
        "text": (None, text.encode("utf-8"), "text/plain; charset=utf-8"),
        "speed": (None, str(speed)),
        "with_transcript": (None, "true" if with_transcript else "false"),
        "file_name": (None, file_name),
    }
    r = requests.post(f"{BASE}/v3/text-to-speech", headers=_headers(), files=files, timeout=120)
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", "10"))
        time.sleep(wait)
        return submit(text, voice_id, speed, with_transcript, file_name)
    r.raise_for_status()
    j = r.json()
    tid = j.get("task_id") or (j.get("data") or {}).get("task_id")
    if not j.get("success", True) or not tid:
        raise OpenSpeakerError(f"submit lỗi: {str(j)[:300]}")
    return tid


def poll(task_id, need_transcript=True):
    """Chờ task xong. Trả (audio_url, srt_url). Đợi CẢ transcript nếu need_transcript."""
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL)
        r = requests.get(f"{BASE}/v1/task/{task_id}", headers=_headers(), timeout=60)
        if r.status_code >= 500:
            continue
        r.raise_for_status()
        j = r.json()
        status = j.get("status") or (j.get("data") or {}).get("status")
        meta = j.get("metadata") or (j.get("data") or {}).get("metadata") or {}
        if status == "failed":
            raise OpenSpeakerError(f"task failed (credit tự hoàn): {str(j)[:300]}")
        if status == "done":
            audio = meta.get("audio_url")
            tstat = meta.get("transcript_status")
            srt = meta.get("srt_url")
            if not need_transcript:
                if audio:
                    return audio, srt
            elif tstat == "completed" and audio:
                return audio, srt
            # audio có trước transcript → chờ tiếp
    raise OpenSpeakerError(f"quá {POLL_TIMEOUT}s task chưa xong")


def _download(url, retry=3):
    """Tải file, KIỂM Content-Length. Đo thật STT13 2026-09-19: server trả mp3 ĐỨT GIỮA CHỪNG
    (16:05 thay vì 29:32, 23MB thay vì ~38MB) mà requests KHÔNG báo lỗi gì — ghép vào là video
    chết tiếng từ phút 18, phụ đề lệch 808s. Chỉ QC nghe (qc_audio.py) mới bắt được, tức là
    đã tốn cả lượt TTS. Nay kiểm ngay lúc tải: thiếu byte → tải lại, hết lượt → ném lỗi."""
    loi = ""
    for lan in range(1, retry + 1):
        r = requests.get(url, timeout=240)
        r.raise_for_status()
        data = r.content
        can = r.headers.get("Content-Length")
        if can and can.isdigit() and len(data) < int(can):
            loi = f"tải thiếu {len(data):,}/{int(can):,} byte"
            print(f"  ! tải file lần {lan}: {loi} → thử lại", flush=True)
            continue
        return data
    raise OpenSpeakerError(f"tải file hỏng sau {retry} lần ({loi}) — {url[:80]}")


def synthesize(text, voice_id=VOICE_ENISHI, speed=0.95, with_transcript=True, file_name="satori"):
    """Trả (audio_bytes_mp3, srt_text|None). Gửi cả kịch bản 1 lần."""
    tid = submit(text, voice_id, speed, with_transcript, file_name)
    audio_url, srt_url = poll(tid, need_transcript=with_transcript)
    audio = _download(audio_url)
    srt = None
    if with_transcript and srt_url:
        srt = _download(srt_url).decode("utf-8", "replace")
    return audio, srt


# ---- Suno music (BGM) — endpoint bóc từ bundle ai33: POST /v1s/task/music-generation (JSON) ----
MUSIC_POLL_TIMEOUT = 600     # Suno lâu hơn TTS (~1-3 phút/bài)


def _music_audio_url(meta):
    """Suno done → lấy 1 audio URL từ metadata (nhiều biến thể field)."""
    for k in ("audio_url", "stream_url"):
        if meta.get(k):
            return meta[k]
    for k in ("stream_urls", "audio_urls", "clips"):
        v = meta.get(k)
        if isinstance(v, list) and v:
            if isinstance(v[0], str):
                return v[0]
            if isinstance(v[0], dict):
                return v[0].get("audio_url") or v[0].get("stream_url") or v[0].get("url")
    return None


def generate_music(prompt, instrumental=True, create_mode="simple", tags="", title="", timeout=MUSIC_POLL_TIMEOUT):
    """Sinh nhạc Suno (mặc định INSTRUMENTAL cho BGM). Trả bytes mp3 của bài đầu tiên."""
    payload = {"create_mode": create_mode, "make_instrumental": bool(instrumental)}
    if create_mode == "simple":
        payload["gpt_description_prompt"] = prompt
    else:
        payload["title"] = title or "bgm"
        payload["tags"] = tags or prompt
    r = requests.post(f"{BASE}/v1s/task/music-generation", headers={**_headers(),
                      "Content-Type": "application/json"}, json=payload, timeout=120)
    r.raise_for_status()
    j = r.json()
    tid = j.get("task_id") or (j.get("data") or {}).get("task_id") or j.get("id")
    if not tid:
        raise OpenSpeakerError(f"music submit lỗi: {str(j)[:300]}")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        time.sleep(8)
        tr = requests.get(f"{BASE}/v1/task/{tid}", headers=_headers(), timeout=60)
        if tr.status_code >= 500:
            continue
        tr.raise_for_status()
        tj = tr.json()
        status = tj.get("status") or (tj.get("data") or {}).get("status")
        meta = tj.get("metadata") or (tj.get("data") or {}).get("metadata") or {}
        if status == "failed":
            raise OpenSpeakerError(f"music task failed: {str(tj)[:300]}")
        if status == "done":
            url = _music_audio_url(meta)
            if url:
                return _download(url)
            # audio có thể chưa gắn — chờ thêm 1 vòng
    raise OpenSpeakerError(f"music quá {timeout}s chưa xong")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Credits:", get_credits())
