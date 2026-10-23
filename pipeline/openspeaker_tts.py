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
import os
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


# ================= HAI KHOÁ CHẠY ĐAN XEN (anh chốt 2026-09-27) =================
# VÌ SAO: ai33 chặn theo TÀI KHOẢN — "You have too many tasks in queue (10/10)"
# (bạn đang có quá nhiều tác vụ trong hàng đợi). Đo thật 2026-09-27: ép khoá 1 đầy hàng đợi rồi
# bắn khoá 2 TỪ CHÍNH MÁY NÀY, cùng lúc, cùng mạng → khoá 1 bị chặn 199 lần trong khi khoá 2 qua
# 5/5. Tức là mỗi tài khoản có 10 chỗ RIÊNG, không dính nhau. Thêm khoá của CÙNG tài khoản thì vô
# ích (trần tính theo tài khoản, không theo khoá).
#
# Giọng clone DÙNG CHUNG ĐƯỢC giữa hai tài khoản: đo thật cùng ngày — khoá 2 (0 giọng clone trong
# danh sách của nó) vẫn đọc được `clone_2658912` của khoá 1, task `done`, ra mp3 0,84 giây nghe
# được. Lý do: clone nằm ở tầng MiniMax (`metadata.v3.provider = minimax`), ai33 chỉ chuyển tiếp id.
# ⚠️ Đây là điều QUAN SÁT ĐƯỢC ở ngày đó, không phải cam kết của nhà cung cấp — nếu sau này họ khoá
# clone theo tài khoản thì khoá 2 sẽ hỏng ở đúng chỗ này, và lỗi sẽ hiện ra lúc poll chứ không phải
# lúc gửi (lúc gửi vẫn HTTP 200).
API_KEYS = [k for k in [
    API_KEY,
    keys.get("openspeaker2", env="AI33_API_KEY_2",
             default="sk_v4zaxfe0tb5vew0d9ff4e8uxqevnyy6e3zlozlpcrejrckbt"),
] if k]

_luot = 0                 # con trỏ xoay vòng, để hai khoá đi ĐAN XEN chứ không dồn vào khoá đầu
_khoa_cua_task = {}       # task_id → khoá đã gửi nó (poll PHẢI hỏi đúng khoá đó)
_khoa_chet = set()        # khoá hết tiền / sai key — bỏ ra khỏi vòng xoay trong phiên này


def _headers(key=None):
    return {"xi-api-key": key or API_KEY}


def _khoa_kha_dung():
    ds = [k for k in API_KEYS if k not in _khoa_chet]
    return ds or list(API_KEYS)      # chết hết thì vẫn thử lại, còn hơn đứng im


def _khoa_tiep():
    """Khoá kế tiếp theo vòng xoay (đan xen đều hai tài khoản)."""
    global _luot
    ds = _khoa_kha_dung()
    k = ds[_luot % len(ds)]
    _luot += 1
    return k


def get_credits(key=None):
    """Số dư. Không truyền `key` = TỔNG của cả pool (đúng nghĩa 'còn tiêu được bao nhiêu'),
    kèm `per_key` để nhìn từng tài khoản. Truyền `key` = số dư đúng tài khoản đó."""
    if key:
        r = requests.get(f"{BASE}/v1/credits", headers=_headers(key), timeout=30)
        r.raise_for_status()
        return r.json()
    tong, chi_tiet = 0, []
    for k in API_KEYS:
        try:
            c = int(requests.get(f"{BASE}/v1/credits", headers=_headers(k),
                                 timeout=30).json().get("credits", 0))
        except Exception:
            c = -1
        chi_tiet.append(c)
        if c > 0:
            tong += c
    return {"success": True, "credits": tong, "per_key": chi_tiet, "n_keys": len(API_KEYS)}


def submit(text, voice_id, speed=0.95, with_transcript=True, file_name="satori"):
    """Gửi task. text dạng bytes UTF-8 trong multipart (CJK-safe). Trả task_id."""
    files = {
        "voice_id": (None, voice_id),
        "text": (None, text.encode("utf-8"), "text/plain; charset=utf-8"),
        "speed": (None, str(speed)),
        "with_transcript": (None, "true" if with_transcript else "false"),
        "file_name": (None, file_name),
    }
    # Bị chặn ở khoá này thì ĐỔI NGAY sang khoá kia, KHÔNG nằm chờ — đó là toàn bộ lợi ích của
    # việc có 2 tài khoản. Chỉ khi MỌI khoá đều đang bị chặn mới ngủ một nhịp rồi vòng lại.
    # (Bản cũ gọi đệ quy chính nó không giới hạn số lần + ngủ cứng 10 giây; hàng đợi đầy lâu là
    # đệ quy chồng hàng trăm tầng, chờ hàng giờ rồi mới gãy. Nay là vòng lặp có trần.)
    so_khoa = len(_khoa_kha_dung())
    cho = 0
    for lan in range(so_khoa * 40):
        khoa = _khoa_tiep()
        r = requests.post(f"{BASE}/v3/text-to-speech", headers=_headers(khoa),
                          files=files, timeout=120)
        if r.status_code == 429:
            cho += 1
            if cho >= so_khoa:          # đã thử hết lượt các khoá mà khoá nào cũng chặn
                time.sleep(int(r.headers.get("Retry-After", "5")))
                cho = 0
            continue
        if r.status_code in (401, 402, 403):
            _khoa_chet.add(khoa)
            print(f"  ! khoá ai33 ...{khoa[-6:]} bị từ chối (HTTP {r.status_code}) → bỏ khỏi vòng xoay",
                  flush=True)
            if not [k for k in API_KEYS if k not in _khoa_chet]:
                raise OpenSpeakerError(f"MỌI khoá ai33 đều bị từ chối: {r.text[:200]}")
            continue
        r.raise_for_status()
        j = r.json()
        tid = j.get("task_id") or (j.get("data") or {}).get("task_id")
        if not j.get("success", True) or not tid:
            raise OpenSpeakerError(f"submit lỗi: {str(j)[:300]}")
        _khoa_cua_task[tid] = khoa      # poll PHẢI hỏi đúng khoá đã gửi, task thuộc tài khoản đó
        return tid
    raise OpenSpeakerError(f"gửi TTS thất bại: {so_khoa} khoá đều kẹt hàng đợi quá lâu")


def poll(task_id, need_transcript=True):
    """Chờ task xong. Trả (audio_url, srt_url). Đợi CẢ transcript nếu need_transcript."""
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL)
        r = requests.get(f"{BASE}/v1/task/{task_id}",
                         headers=_headers(_khoa_cua_task.get(task_id)), timeout=60)
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
    """Sinh nhạc Suno (mặc định INSTRUMENTAL cho BGM). Trả bytes mp3 của bài đầu tiên.
    ⛔ KHOÁ từ 2026-10-23 (anh chốt): nhạc Suno qua ai33 không có chứng từ giấy phép → dễ bị claim.
    Dùng Thư viện âm thanh YouTube: pipeline/bgm_audio_library.py + pipeline/nhac_hook_tu_thu_vien.py
    (luật docs/QUY_TAC_NHAC_NEN.md). Chỉ mở lại khi anh cho phép: env H2DEV_CHO_PHEP_SUNO=1."""
    if os.environ.get("H2DEV_CHO_PHEP_SUNO") != "1":
        raise RuntimeError("Suno đã CẤM từ 2026-10-23 — dùng pipeline/nhac_hook_tu_thu_vien.py (hook) / "
                           "pipeline/bgm_audio_library.py (bài lane). Luật: docs/QUY_TAC_NHAC_NEN.md")
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
