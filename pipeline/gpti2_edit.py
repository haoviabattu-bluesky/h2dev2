"""gpti2_edit.py — KHOA NHAT QUAN NHAN VAT bang ANH THAM CHIEU (image->image) qua gpti2.

Khac gpti2_gen.py (text->image, khong seed, moi anh mot khuon mat): module nay gui kem 1-3 ANH
NGUON (anh master cua nhan vat) vao /v1/images/jobs/edits, nen model giu duoc khuon mat/trang phuc.

Bai hoc da ghim (skill gpti2.md):
- Endpoint BAT DONG BO /v1/images/jobs/edits + poll (sync bi Cloudflare cat ~100s).
- quality: DO THAT 2026-09-07 tren khoa mat nhan vat -> "low" giu mat NGANG "medium" (50d vs 350d)
  => dung "low". Bai hoc "phai dung medium" trong skill gpti2.md la cho task GIU NGUYEN CHU TREN THE
  (content-lock text), KHONG ap cho khoa mat. "high" van tranh (ve lai -> mo + sai chi tiet).
- Anh nguon <= 8 MiB/anh. WebP lossless exact=True giu tung bit; qua nguong moi ha chat.
- Tai anh ket qua TUYET DOI KHONG gui Authorization (link R2 ky san).
- Poll dinh 502/503 KHONG phai job hong -> hoi tiep. 402 = het tien -> dung key.
- Retry loi TAM phai doi Idempotency-Key.
- Phu phi edit: +60d moi ANH NGUON, cong vao gia size x quality.
"""
import io
import time
import uuid

import requests
from PIL import Image

import gpti2_gen
from gpti2_gen import (BASE_URL, Gpti2Error, QuotaExhaustedError, _pick_key, _size_for,
                       _UA, mark_key_dead)

MAX_UPLOAD_BYTES = 8 * 1024 * 1024      # 8 MiB dung nghia; 8.388.609 byte -> HTTP 413
MAX_REFERENCE_IMAGES = 8                # GET /v1/pricing -> max_reference_images: 8 (KHONG phai 3)
QUALITY_DEFAULT = "low"                 # DO THAT 2026-09-07: low giu mat y het medium ma re gap 4
SUBMIT_TIMEOUT = 120
POLL_INTERVAL = 7
POLL_TIMEOUT = 420
MAX_ATTEMPTS = 5
_EDIT_SURCHARGE_PER_SOURCE = 60


def fit_for_upload(data):
    """Ep anh xuong <= 8 MiB. Tra ve (bytes, mime, ext).
    Thu tu: giu nguyen -> WebP lossless exact=True (giu tung bit, ke ca duoi alpha) ->
    WebP lossy q95/q80 -> thu nho canh dai ve 2048 (model bao hoa ~2048px)."""
    if len(data) <= MAX_UPLOAD_BYTES:
        return data, "image/png", "png"
    im = Image.open(io.BytesIO(data))
    for kw in ({"lossless": True, "exact": True}, {"quality": 95}, {"quality": 80}):
        buf = io.BytesIO()
        im.save(buf, format="WEBP", **kw)
        if buf.tell() <= MAX_UPLOAD_BYTES:
            return buf.getvalue(), "image/webp", "webp"
    im.thumbnail((2048, 2048), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=85)
    if buf.tell() > MAX_UPLOAD_BYTES:
        raise Gpti2Error(f"Anh nguon van {buf.tell()} byte > 8 MiB sau khi nen.")
    return buf.getvalue(), "image/webp", "webp"


def _submit_edit(images, prompt, size, quality, api_key, idem):
    """images = [(bytes, filename), ...] 1-8 anh; ANH DAU la anh duoc uu tien giu."""
    field = "image" if len(images) == 1 else "image[]"
    files = []
    for raw, filename in images:
        fitted, mime, ext = fit_for_upload(raw)
        stem = filename.rsplit(".", 1)[0]
        files.append((field, (f"{stem}.{ext}", fitted, mime)))
    try:
        r = requests.post(
            f"{BASE_URL}/v1/images/jobs/edits",
            headers={"Authorization": f"Bearer {api_key}", "User-Agent": _UA,
                     "Idempotency-Key": idem},
            files=files, data={"prompt": prompt, "size": size, "quality": quality},
            timeout=SUBMIT_TIMEOUT)
    except requests.RequestException as e:
        raise Gpti2Error(f"Submit edit loi mang: {e}") from None
    if r.status_code in (401, 402):
        raise QuotaExhaustedError(f"Het tien / sai key gpti2 (HTTP {r.status_code}): {r.text[:200]}")
    if r.status_code >= 400:
        raise Gpti2Error(f"Submit edit HTTP {r.status_code}: {r.text[:250]}")
    try:
        return r.json()["id"]
    except (ValueError, KeyError):
        raise Gpti2Error(f"Submit edit tra ve du lieu la: {r.text[:200]}") from None


def _poll_edit(job_id, api_key):
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        time.sleep(POLL_INTERVAL)
        try:
            g = requests.get(f"{BASE_URL}/v1/images/jobs/{job_id}",
                             headers={"Authorization": f"Bearer {api_key}", "User-Agent": _UA},
                             timeout=60)
        except requests.RequestException:
            continue                      # loi mang tam -> hoi tiep, bo cuoc la mat tien
        if g.status_code != 200:
            continue                      # 502/503 tam thoi
        try:
            j = g.json()
        except ValueError:
            continue
        if j.get("status") == "succeeded":
            url = (j.get("data") or [{}])[0].get("url")
            if not url:
                raise Gpti2Error(f"Job xong nhung khong co url: {str(j)[:200]}")
            img = requests.get(url, headers={"User-Agent": _UA}, timeout=240)  # KHONG Authorization
            img.raise_for_status()
            out = io.BytesIO()
            Image.open(io.BytesIO(img.content)).convert("RGB").save(out, format="PNG")
            return out.getvalue()         # re-save Pillow: xoa chunk C2PA danh dau AI
        if j.get("status") == "failed":
            raise Gpti2Error(f"Job that bai: {str(j.get('error'))[:200]}")
    raise Gpti2Error(f"Qua {POLL_TIMEOUT}s job edit chua xong.")


def edit(prompt, images, orientation="landscape", quality=QUALITY_DEFAULT, size="", api_key=""):
    """images = [(bytes, filename), ...] 1-8 anh nguon (anh dau = anh master nhan vat).
    Tra ve PNG bytes. 1 key DUY NHAT cho ca submit lan poll (job gan voi key tao no)."""
    if not 1 <= len(images) <= MAX_REFERENCE_IMAGES:
        raise ValueError(f"gpti2 edit nhan 1-{MAX_REFERENCE_IMAGES} anh nguon.")
    last = None
    for _ in range(MAX_ATTEMPTS):
        key = _pick_key(api_key)
        try:
            job_id = _submit_edit(images, prompt, _size_for(orientation, size), quality,
                                  key, uuid.uuid4().hex)   # Idem MOI moi lan -> khong tinh tien trung
            return _poll_edit(job_id, key)
        except QuotaExhaustedError as e:
            if api_key:
                raise
            mark_key_dead(key)   # doi sang key con tien thay vi hong ca loat anh
            last = e
        except Gpti2Error as e:
            last = e
            time.sleep(5)
    raise Gpti2Error(f"gpti2 edit that bai sau {MAX_ATTEMPTS} lan: {last}")


def edit_from_paths(prompt, paths, **kw):
    from pathlib import Path
    imgs = [(Path(p).read_bytes(), Path(p).name) for p in paths]
    return edit(prompt, imgs, **kw)


def estimate_price_vnd(orientation="landscape", quality=QUALITY_DEFAULT, n_sources=1, size=""):
    # GET /v1/pricing la nguon chan ly; bang duoi chi cache 2 size du an dung.
    table = {("2560x1440", "low"): 50, ("2560x1440", "medium"): 350, ("2560x1440", "high"): 1400,
             ("1536x2048", "low"): 50, ("1536x2048", "medium"): 430}
    return table.get((_size_for(orientation, size), quality), 0) \
        + _EDIT_SURCHARGE_PER_SOURCE * n_sources
