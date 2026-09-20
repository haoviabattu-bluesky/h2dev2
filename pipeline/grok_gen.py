"""grok_gen.py — text->image qua Grok Imagine (xAI) trên proxy ramclouds.

LÝ DO TỒN TẠI (verify 2026-09-08): gpti2/imgstudio (gpt-image-2 nền Azure) CHẶN MỌI mô tả người
dưới 18 tuổi — kể cả cảnh lành mạnh, kể cả silhouette không thấy mặt (từ "child/kid/baby/infant/
students/little girl/số tuổi" là bị content_policy_violation). Grok Imagine cho phép ảnh trẻ em lành
mạnh (đã test: bé chơi đồ chơi, em bé quấn tã, bé gái ở mộ, mẹ ôm con ốm trong bão tuyết — đều OK).
→ Dùng module này CHỈ cho cảnh có trẻ em/em bé; cảnh khác vẫn dùng gpti2_gen (nét hơn, 2560x1440).

Chốt kỹ thuật (verify 2026-09-08 qua ramclouds):
- model = "grok-imagine-image-2.0" (KHÔNG phải grok-2-image — model đó 403/không có channel).
- BẮT BUỘC response_format="b64_json": URL kết quả Grok trỏ host bị chặn từ máy VN (WinError 10061),
  chỉ b64 mới lấy được ảnh.
- size WHITELIST: "1280x720" (16:9 landscape) OK, "768x1152" (2:3 portrait, mặc định) OK.
  "1920x1080"/"1344x768"/"aspect_ratio" → 400 "aspect_ratio 不受支持". → chỉ dùng 2 size này.
- Key ramclouds có quyền Grok (group khác key gpt-image-2 thường). 403 "no access"/"no available
  channel" = key/group không có Grok.
"""
import io
import json
import base64
import urllib.request
import urllib.error

from PIL import Image

import keys

BASE_URL = "https://ramclouds.me"
MODEL = "grok-imagine-image-2.0"
# Key ramclouds CÓ quyền Grok (user cấp 2026-09-08). Key gpt-image-2 thường KHÔNG gọi được Grok.
# Đổi ở máy khác: khoá `grok` trong keys.json CẠNH exe.
API_KEY = keys.get("grok", env="GROK_API_KEY",
                   default="sk-ue0LE9lhUveoGFrt3Ah2SFJb82nPD9FVoe7jiihO3n6RnMeJ")

SIZE_LANDSCAPE = "1280x720"   # 16:9 — size landscape DUY NHẤT đã verify chạy
SIZE_PORTRAIT = "768x1152"    # 2:3 — mặc định của Grok
TIMEOUT = 180
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


class GrokError(Exception):
    def __init__(self, message, http_code=502):
        super().__init__(message)
        self.http_code = http_code


def _size_for(orientation, size=""):
    if size:
        return size
    return SIZE_LANDSCAPE if orientation == "landscape" else SIZE_PORTRAIT


def generate(prompt, orientation="landscape", size="", api_key=""):
    """Text->image PNG bytes qua Grok Imagine. Dùng cho cảnh có TRẺ EM (gpti2 chặn)."""
    key = api_key or API_KEY
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "n": 1,
        "size": _size_for(orientation, size), "response_format": "b64_json",
    }).encode()
    req = urllib.request.Request(
        BASE_URL + "/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {key}", "User-Agent": _UA,
                 "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", "replace")
        raise GrokError(f"Grok HTTP {e.code}: {body_txt[:220]}", http_code=e.code) from None
    except urllib.error.URLError as e:
        raise GrokError(f"Grok network: {getattr(e, 'reason', e)}") from None
    try:
        it = resp["data"][0]
    except (KeyError, IndexError, TypeError):
        raise GrokError(f"Grok response lạ: {str(resp)[:200]}")
    if not it.get("b64_json"):
        raise GrokError(f"Grok không trả b64_json (keys={list(it)}). Phải gửi response_format=b64_json.")
    raw = base64.b64decode(it["b64_json"])
    out = io.BytesIO()
    Image.open(io.BytesIO(raw)).convert("RGB").save(out, format="PNG")  # strip metadata C2PA
    return out.getvalue()


if __name__ == "__main__":
    img = generate("A happy toddler playing with wooden blocks, wholesome family photo, photorealistic",
                   orientation="landscape")
    open("_grok_smoke.png", "wb").write(img)
    print("OK", len(img) // 1024, "KB -> _grok_smoke.png")
