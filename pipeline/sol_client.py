"""sol_client.py — gọi GPT-5.6-sol để làm QC ĐỘC LẬP thumbnail (đọc chữ tiếng Nhật + ảnh, chấm
PASS/FIX/REMAKE) và viết PROMPT ảnh cho gpti2 khi ảnh nền cần sửa nội dung.

HAI ĐƯỜNG, tự động fallback (verify thật 2026-09-17):
  1. CHÍNH: proxy 9router LOCAL (`http://localhost:20128/v1`, model `cx/gpt-5.6-sol` — CÓ prefix
     `cx/`), non-stream, chỉ chạy được trên máy đã bật 9router ở cổng 20128.
  2. DỰ PHÒNG: proxy ns24.io (`https://api.ns24.io/v1`, model `gpt-5.6-sol` — KHÔNG prefix), dùng
     khi #1 lỗi (9router tắt/máy khác/connection refused/timeout/HTTP khác 200). ns24 đã dùng sẵn
     trong dự án cho Gemini (`llm_client.py`) — key này CHÍNH LÀ key `ns24` mặc định ở đó.
     ⚠️ ns24/ramclouds BẮT BUỘC `stream:true` (gọi non-stream trả HTTP 200 + SSE rỗng, mất trắng nội
     dung mà không báo lỗi — bài học thật đã ghi ở `llm_client.py`) + BẮT BUỘC User-Agent (thiếu bị
     Cloudflare chặn 403 code 1010). Cả 2 điều đã áp dụng ở nhánh dự phòng bên dưới.

Vì sao "độc lập" (áp dụng cho CẢ 2 đường): mọi bước sinh/chấm ảnh khác trong pipeline (qc_visual.py)
đều dùng Gemini qua ramclouds — cùng 1 nhà cung cấp/1 lối tư duy chấm điểm thì lỗi hệ thống của
Gemini sẽ lọt qua cả 2 lớp. GPT-5.6-sol là model KHÁC HẲN — dùng làm lớp chấm THỨ HAI cho khâu
thumbnail (khâu duy nhất người xem thấy TRƯỚC KHI bấm play, đáng đầu tư 1 lớp QC riêng). Proxy nào
đưa tới model đó không quan trọng — chỉ là đường dây, không đổi bản chất "model thứ 2".
"""
import base64
import json
import sys

import httpx

import keys

BASE_URL = keys.get("sol_base_url", env="SOL_BASE_URL", default="http://localhost:20128/v1")
API_KEY = keys.get("sol", env="SOL_API_KEY",
                    default="sk-f8cb1a67a6a3f23b-7vhgv7-844b67c4")
MODEL = keys.get("sol_model", env="SOL_MODEL", default="cx/gpt-5.6-sol")

# Dự phòng ns24 — key mặc định TRÙNG với key `ns24` mặc định trong llm_client.py (cùng 1 proxy,
# dùng chung tài khoản). Model KHÔNG có prefix `cx/` (khác 9router).
BACKUP_BASE_URL = keys.get("sol_backup_base_url", env="SOL_BACKUP_BASE_URL",
                            default="https://api.ns24.io/v1")
BACKUP_API_KEY = keys.get("sol_backup", env="SOL_BACKUP_API_KEY",
                           default="sk-up-0ef5398f1893e50f6a8d9055c7b9e7cb4f847dac7601d09f")
BACKUP_MODEL = keys.get("sol_backup_model", env="SOL_BACKUP_MODEL", default="gpt-5.6-sol")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def _content(text, image_path):
    content = [{"type": "text", "text": text}]
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = str(image_path).rsplit(".", 1)[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"}})
    return content


def _chat_primary(text, image_path, max_tokens, timeout):
    payload = {"model": MODEL, "messages": [{"role": "user", "content": _content(text, image_path)}],
               "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    r = httpx.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"sol primary HTTP {r.status_code}: {r.text[:500]}")
    data = r.json()
    return data["choices"][0]["message"]["content"], data.get("usage", {})


def _chat_backup(text, image_path, max_tokens, timeout):
    """ns24 dự phòng — LUÔN stream:true + User-Agent (xem docstring module: thiếu 1 trong 2 là
    mất trắng nội dung câm lặng hoặc bị Cloudflare chặn 403, không phải lỗi code/key)."""
    payload = {"model": BACKUP_MODEL,
               "messages": [{"role": "user", "content": _content(text, image_path)}],
               "max_tokens": max_tokens, "stream": True}
    headers = {"Authorization": f"Bearer {BACKUP_API_KEY}", "Content-Type": "application/json",
               "User-Agent": UA}
    text_out, usage = "", {}
    with httpx.stream("POST", f"{BACKUP_BASE_URL}/chat/completions", headers=headers,
                       json=payload, timeout=timeout) as r:
        if r.status_code != 200:
            raise RuntimeError(f"sol backup(ns24) HTTP {r.status_code}: {r.read()[:500]}")
        for line in r.iter_lines():
            if not line or not line.startswith("data:"):
                continue
            chunk = line[5:].strip()
            if chunk == "[DONE]":
                break
            obj = json.loads(chunk)
            choice = (obj.get("choices") or [{}])[0]
            text_out += (choice.get("delta") or {}).get("content", "")
            if obj.get("usage"):
                usage = obj["usage"]
    if not text_out.strip():
        raise RuntimeError("sol backup(ns24): SSE rỗng — mất trắng nội dung (xem cảnh báo #1 "
                            "llm_client.py, dù HTTP 200)")
    return text_out, usage


def chat(text, image_path=None, max_tokens=2000, timeout=180):
    """Gửi 1 lượt chat (kèm ảnh nếu có) tới GPT-5.6-sol. Thử proxy CHÍNH (9router local) trước,
    LỖI GÌ CŨNG (connection refused/timeout/HTTP khác 200) tự chuyển sang proxy DỰ PHÒNG (ns24)
    — không cần người gọi biết đang dùng đường nào. Chỉ ném lỗi khi CẢ HAI đều hỏng."""
    try:
        content, usage = _chat_primary(text, image_path, max_tokens, timeout)
        return content, usage
    except Exception as e_primary:
        print(f"  ! sol primary (9router) lỗi: {type(e_primary).__name__} {e_primary} "
              f"→ thử dự phòng ns24…", file=sys.stderr)
        try:
            return _chat_backup(text, image_path, max_tokens, timeout)
        except Exception as e_backup:
            raise RuntimeError(
                f"sol_client: CẢ HAI đường đều lỗi.\n  primary(9router): {e_primary}\n"
                f"  backup(ns24): {e_backup}") from e_backup


def selftest():
    """`py -3.13 sol_client.py` — kiểm cả 2 đường (chính + dự phòng) độc lập."""
    sys.stdout.reconfigure(encoding="utf-8")
    ok = True
    try:
        content, usage = _chat_primary("Reply with exactly: OK", None, 10, 30)
        print(f"✓ CHÍNH  {BASE_URL} model={MODEL} → {content!r}")
    except Exception as e:
        ok = False
        print(f"✗ CHÍNH  {BASE_URL}: {type(e).__name__} {e}")
    try:
        content, usage = _chat_backup("Reply with exactly: OK", None, 10, 30)
        print(f"✓ DỰ PHÒNG {BACKUP_BASE_URL} model={BACKUP_MODEL} → {content!r}")
    except Exception as e:
        ok = False
        print(f"✗ DỰ PHÒNG {BACKUP_BASE_URL}: {type(e).__name__} {e}")
    if not ok:
        print("  (còn ít nhất 1 đường sống thì chat() vẫn hoạt động — chỉ FAIL khi cả 2 đều hỏng)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    selftest()
