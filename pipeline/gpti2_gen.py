"""gpti2_gen.py — client gpt-image-2 text->image TỰ CHỨA cho pipeline WW2.

Rút gọn từ d:/CLAUDE/RAMCLOUD/gpti2_client.py (đã kiểm chứng bằng tiền thật), BỎ phụ thuộc
gpti2_pool + gpti2_img_fit (chỉ cần cho edit/upload). Chỉ giữ text->image generation qua đơn
BẤT ĐỒNG BỘ /v1/images/jobs + poll + download (bài học: sync bị Cloudflare cắt ~100s).

Bài học đã ghim (skill gpti2.md):
- Size ngang 2560x1440 (gpti2 KHÔNG có 2048x1152). quality mặc định "low" = "Tiêu chuẩn" rẻ.
- Tải ảnh kết quả TUYỆT ĐỐI KHÔNG gửi Authorization (link R2 ký sẵn → gửi Bearer là ra XML lỗi).
- Poll dính 502/503 KHÔNG có nghĩa job hỏng → hỏi tiếp, bỏ cuộc là mất tiền. 402 = hết tiền (dừng key).
- Job "upstream" là lỗi TẠM, hoàn tiền 100% → retry PHẢI đổi Idempotency-Key.
- 3 key RPM riêng (20/phút) → luân phiên để tăng throughput.
"""
import io
import json
import threading
import time
import uuid
import urllib.request
import urllib.error

from PIL import Image

import keys

BASE_URL = "https://gpti2.store"

# Còn 1 key sống (10/10: 2 key cũ cạn tiền) — thêm key thì thêm dòng, tự luân phiên.
# Đổi key ở máy khác: sửa `gpti2` trong keys.json CẠNH exe (nhận cả danh sách), KHÔNG build lại.
_DEFAULT_KEYS = [
    "sk--GUch2kmDgSCGJ2uvFFCb652ULRqyvzTOMT1iP8GlZQ",  # nap lai 100.000d 15/10
    "sk-YGVr-OzozR6zawnFNDG5DCn_PDiAbNZkj9LVOHaOFcA",
]
API_KEYS = keys.get_list("gpti2", env="GPTI2_API_KEYS", default=_DEFAULT_KEYS)
_key_lock = threading.Lock()
_key_i = [0]

SIZE_LANDSCAPE = "2560x1440"   # 16:9 cho video YouTube
SIZE_PORTRAIT = "1536x2048"
QUALITY_DEFAULT = "low"        # "low"=Tiêu chuẩn (rẻ) · "medium"=Tốt · "high" tránh dùng (mờ + đắt)

SUBMIT_TIMEOUT = 120
POLL_INTERVAL = 7
POLL_TIMEOUT = int(__import__("os").environ.get("GPTI2_POLL_TIMEOUT", "420"))  # gpti2 nghẽn (30/09: low 414s) → nới qua env
MAX_ATTEMPTS = 5
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


class Gpti2Error(Exception):
    def __init__(self, message, http_code=502):
        super().__init__(message)
        self.http_code = http_code


class QuotaExhaustedError(Gpti2Error):
    """402 — hết tiền trong key. KHÔNG retry."""
    def __init__(self, message):
        super().__init__(message, http_code=402)


class _Transient(Exception):
    def __init__(self, message, retry_after=0.0):
        super().__init__(message)
        self.retry_after = retry_after


# Key da bao 402 (het tien) trong phien nay. Round-robin tran KHONG tu tranh key chet
# -> 1 key can tien la moi anh roi vao no deu hong (skill gpti2 da canh bao). Loai han ra.
_DEAD_KEYS = set()


def mark_key_dead(key):
    with _key_lock:
        _DEAD_KEYS.add(key)
    alive = len(API_KEYS) - len(_DEAD_KEYS)
    print(f"  ! key ...{key[-6:]} het tien -> loai, con {alive}/{len(API_KEYS)} key", flush=True)


def _pick_key(explicit=""):
    if explicit:
        return explicit
    with _key_lock:
        live = [k for k in API_KEYS if k not in _DEAD_KEYS]
        if not live:
            raise QuotaExhaustedError("TAT CA key gpti2 deu het tien.")
        i = _key_i[0]
        _key_i[0] += 1
    return live[i % len(live)]


def _size_for(orientation, size=""):
    if size:
        return size
    return SIZE_LANDSCAPE if orientation == "landscape" else SIZE_PORTRAIT


def _headers(api_key, idem=""):
    h = {"Authorization": f"Bearer {api_key}", "User-Agent": _UA}
    if idem:
        h["Idempotency-Key"] = idem
    return h


def _raise_http(e):
    body = e.read().decode("utf-8", "replace")
    try:
        err = json.loads(body).get("error") or {}
        msg, code = err.get("message") or body[:300], err.get("code", "")
    except Exception:
        msg, code = body[:300], ""
    if e.code == 402 or code == "insufficient_balance":
        raise QuotaExhaustedError(f"Het tien trong key gpti2: {msg}") from None
    if e.code == 429:
        try:
            wait = float(e.headers.get("Retry-After") or 0)
        except (TypeError, ValueError):
            wait = 0.0
        raise _Transient(f"429 rate limit: {msg}", retry_after=wait or 10.0) from None
    if e.code == 503 or code == "server_draining":
        raise _Transient(f"503 server draining: {msg}", retry_after=15.0) from None
    if e.code == 401:
        raise Gpti2Error(f"Key gpti2 khong hop le: {msg}", http_code=401) from None
    raise Gpti2Error(f"HTTP {e.code}: {msg}") from None


def _request(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        _raise_http(e)
    except urllib.error.URLError as e:
        raise _Transient(f"Network: {getattr(e, 'reason', e)}", retry_after=5.0) from None


def _submit_generate(prompt, orientation, api_key, idem, quality, size="", model=""):
    payload = {"prompt": prompt, "size": _size_for(orientation, size),
               "quality": quality, "n": 1}
    if model:   # server default co the OFFLINE (model_unavailable 2026-09-20) -> cho phep chi dinh model dang phuc vu
        payload["model"] = model
    req = urllib.request.Request(
        BASE_URL + "/v1/images/jobs", data=json.dumps(payload).encode(),
        headers={**_headers(api_key, idem), "Content-Type": "application/json"}, method="POST")
    resp = _request(req, SUBMIT_TIMEOUT)
    job_id = resp.get("id")
    if not job_id:
        raise Gpti2Error(f"Response la, khong co id: {str(resp)[:200]}")
    return job_id


def _poll(job_id, api_key):
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL)
        req = urllib.request.Request(BASE_URL + f"/v1/images/jobs/{job_id}",
                                     headers=_headers(api_key))
        try:
            job = _request(req, 60)
        except (_Transient, Gpti2Error):
            continue   # don van chay — hoi tiep
        status = job.get("status")
        if status == "succeeded":
            data = job.get("data") or []
            url = data[0].get("url") if data else None
            if not url:
                raise Gpti2Error(f"Don xong nhung khong co url: {str(job)[:200]}")
            return url
        if status == "failed":
            err = job.get("error") or {}
            raise _Transient(f"Don loi ({err.get('code', '?')}): {err.get('message', '?')}")
    raise Gpti2Error(f"Qua {POLL_TIMEOUT}s don chua xong — gpti2 nghen.")


def _download_png(url):
    # KHONG gui Authorization (link R2 ky san). Re-save Pillow xoa chunk C2PA.
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            raw = r.read()
    except urllib.error.URLError as e:
        raise Gpti2Error(f"Tai anh that bai: {getattr(e, 'reason', e)}") from None
    out = io.BytesIO()
    Image.open(io.BytesIO(raw)).convert("RGB").save(out, format="PNG")
    return out.getvalue()


def generate(prompt, orientation="landscape", quality=QUALITY_DEFAULT,
             size="", api_key="", model=""):
    """Text->image PNG bytes. Luan phien key; retry loi TAM voi Idempotency-Key moi."""
    last = None
    for _ in range(MAX_ATTEMPTS):
        key = _pick_key(api_key)
        try:
            job_id = _submit_generate(prompt, orientation, key, uuid.uuid4().hex, quality, size, model)
            return _download_png(_poll(job_id, key))
        except QuotaExhaustedError as e:
            if api_key:          # nguoi goi chi dinh key cu the -> khong tu doi
                raise
            mark_key_dead(key)
            last = e
        except _Transient as e:
            last = e
            if e.retry_after:
                time.sleep(min(e.retry_after, 15))
    raise Gpti2Error(f"gpti2 that bai sau {MAX_ATTEMPTS} lan: {last}")


def get_balance(api_key):
    req = urllib.request.Request(BASE_URL + "/v1/balance", headers=_headers(api_key))
    return _request(req, 30)


if __name__ == "__main__":
    # smoke test: kiem so du 3 key
    for k in API_KEYS:
        try:
            b = get_balance(k)
            print(k[:16], "->", b.get("balance_vnd") or b)
        except Exception as e:
            print(k[:16], "ERR", e)
