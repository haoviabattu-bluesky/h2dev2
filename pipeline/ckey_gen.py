"""ckey_gen.py — client ảnh qua ckey.vn (cổng OpenAI https://api.xah.io/v1), thay/dự phòng gpti2.

Đo thật 2026-09-30 (E:\\CLAUDE\\GPT_API\\ckey_test):
- Model dungcsnd113/gpt-image-2: 52đ/ảnh CỐ ĐỊNH — không phụ thuộc quality, không phụ thuộc số ảnh ref.
- Ảnh tham chiếu gửi trong /images/generations qua `images: [data-url,...]` — đã chạy đúng 32 ref/lần.
  BẪY: `image: [mảng]` bị BỎ QUA im lặng; /images/edits trả 404.
- 16:9 tối đa 1672x941 (xin 2560x1440 cũng chỉ ra cỡ đó) → ở đây phóng về đúng cỡ gpti2 để khâu sau không đổi.
- Cảnh trẻ em KHÔNG bị chặn (khác gpti2/Azure) — nhưng route @GROK vẫn giữ nguyên, chưa đổi.
- 1 ảnh mất ~40-120s, gọi đồng bộ (không có job/poll).
Key: `ckey` trong keys.json (sk-..., tạo trên web ckey.vn/llm-api), hoặc biến môi trường CKEY_API_KEY.
"""
import base64
import io
import json
import os
import time
import urllib.error
import urllib.request

from PIL import Image

import keys
from gpti2_gen import QuotaExhaustedError as _Gpti2Quota

BASE_URL = keys.get("ckey_base_url", env="CKEY_BASE_URL", default="https://api.xah.io/v1")
MODEL = keys.get("ckey_model", env="CKEY_MODEL", default="dungcsnd113/gpt-image-2")
API_KEY = keys.get("ckey", env="CKEY_API_KEY", default="")   # key thật nằm ở keys.json (không commit — repo public)

PRICE_VND = 52                     # cố định/ảnh (2026-09-30), kể cả có ref
TARGET = {"landscape": (2560, 1440), "portrait": (1536, 2048)}   # = cỡ gpti2_gen đang ra
REQ_SIZE = {"landscape": "2560x1440", "portrait": "1536x2048"}
REF_MAX_SIDE = 768                 # thu ref về 768px JPEG: nhẹ payload, vẫn giữ mặt tốt
TIMEOUT = int(os.environ.get("CKEY_TIMEOUT", "420"))
MAX_ATTEMPTS = 4


class QuotaExhaustedError(_Gpti2Quota):
    """Hết số dư / key sai — KHÔNG retry. Kế thừa lỗi gpti2 để gen_images bắt chung một chỗ."""


def _ref_data_url(data):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.thumbnail((REF_MAX_SIDE, REF_MAX_SIDE))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _fit(raw, orientation):
    """Phóng/cắt về đúng cỡ gpti2 (2560x1440 / 1536x2048), trả PNG bytes."""
    tw, th = TARGET[orientation]
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    out = io.BytesIO()
    im.save(out, "PNG")
    return out.getvalue()


def _post(payload):
    req = urllib.request.Request(
        BASE_URL + "/images/generations", data=json.dumps(payload).encode(), method="POST",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())


def generate(prompt, orientation="landscape", refs=None, model=""):
    """Sinh 1 ảnh. `refs` = list (bytes, name) như gpti2_edit — KHÔNG giới hạn 8 ảnh.
    Trả PNG bytes đúng cỡ gpti2."""
    payload = {"model": model or MODEL, "prompt": prompt, "n": 1, "size": REQ_SIZE[orientation]}
    if refs:
        payload["images"] = [_ref_data_url(b) for b, _ in refs]   # PHẢI là `images`, không phải `image: []`
    last = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            j = _post(payload)
            d = (j.get("data") or [{}])[0]
            if d.get("b64_json"):
                raw = base64.b64decode(d["b64_json"])
            elif d.get("url"):
                raw = urllib.request.urlopen(d["url"], timeout=120).read()
            else:
                raise RuntimeError(f"ckey không trả ảnh: {json.dumps(j)[:200]}")
            return _fit(raw, orientation)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            low = body.lower()
            if e.code in (401, 402) or "balance" in low or "insufficient" in low or "số dư" in low:
                raise QuotaExhaustedError(f"ckey HTTP {e.code}: {body}")
            if e.code in (400, 404) and "safety" not in low and "moderation" not in low:
                raise RuntimeError(f"ckey HTTP {e.code}: {body}")     # lỗi request — retry vô ích
            last = f"HTTP {e.code}: {body}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError) as e:
            last = f"{type(e).__name__}: {e}"
        if attempt < MAX_ATTEMPTS:
            time.sleep(5 * attempt)
    raise RuntimeError(f"ckey lỗi sau {MAX_ATTEMPTS} lần: {last}")
