"""sol_client.py — gọi GPT-5.6-sol để làm QC ĐỘC LẬP thumbnail (đọc chữ tiếng Nhật + ảnh, chấm
PASS/FIX/REMAKE), viết PROMPT ảnh cho gpti2 khi ảnh nền cần sửa nội dung, VÀ (2026-09-20) chấm
kịch bản độc lập ở luồng lean (qc_script_sol.py — dùng CHUNG client này).

BA ĐƯỜNG, tự động fallback theo thứ tự (verify thật 2026-09-17 cho #1/#2; #3 verify 2026-09-22):
  1. CHÍNH: proxy 9router LOCAL (`http://localhost:20128/v1`, model `cx/gpt-5.6-sol` — CÓ prefix
     `cx/`), non-stream, chỉ chạy được trên máy đã bật 9router ở cổng 20128.
  2. DỰ PHÒNG 1: proxy ns24.io (`https://api.ns24.io/v1`, model `gpt-5.6-sol` — KHÔNG prefix), dùng
     khi #1 lỗi (9router tắt/máy khác/connection refused/timeout/HTTP khác 200). ns24 đã dùng sẵn
     trong dự án cho Gemini (`llm_client.py`) — key này CHÍNH LÀ key `ns24` mặc định ở đó.
     ⚠️ ns24/ramclouds BẮT BUỘC `stream:true` (gọi non-stream trả HTTP 200 + SSE rỗng, mất trắng nội
     dung mà không báo lỗi — bài học thật đã ghi ở `llm_client.py`) + BẮT BUỘC User-Agent (thiếu bị
     Cloudflare chặn 403 code 1010). Cả 2 điều đã áp dụng ở nhánh dự phòng bên dưới.
  3. DỰ PHÒNG 2: proxy hhtechapi.net (`https://hhtechapi.net/v1`, model `gpt-5.6-sol` — KHÔNG
     prefix), dùng khi CẢ #1 lẫn #2 đều lỗi. New-API gateway khác hẳn ns24/9router (đề phòng cả 2
     cùng hết quota/cùng bị chặn một lúc — quan sát thật 2026-09-21: Fable ở 9router hết quota cùng
     lúc dính nhiều nơi). Non-stream chuẩn OpenAI, ĐÃ verify multimodal (đọc đúng chữ Nhật trên
     thumbnail_final.png thật) + text thường, không cần User-Agent riêng. Key mượn từ dự án khác
     (memory `hhtechapi-portal`), đăng ký RIÊNG không liên quan ns24/9router — hỏng đồng thời cả 3
     khó xảy ra hơn hỏng đồng thời 2.

Vì sao "độc lập" (áp dụng cho CẢ 3 đường): mọi bước sinh/chấm ảnh khác trong pipeline (qc_visual.py)
đều dùng Gemini qua ramclouds — cùng 1 nhà cung cấp/1 lối tư duy chấm điểm thì lỗi hệ thống của
Gemini sẽ lọt qua cả 2 lớp. GPT-5.6-sol là model KHÁC HẲN — dùng làm lớp chấm THỨ HAI cho khâu
thumbnail (khâu duy nhất người xem thấy TRƯỚC KHI bấm play, đáng đầu tư 1 lớp QC riêng) và cho kịch
bản (lean flow, "lời cuối" trước khoá). Proxy nào đưa tới model đó không quan trọng — chỉ là đường
dây, không đổi bản chất "model thứ 2"; càng nhiều đường dây độc lập càng giảm rủi ro CẢ 2 cùng hết
quota một lúc (đã xảy ra thật với Fable ở claude -p, xem memory `opus-s4-patch-ab-test`).
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

# Dự phòng 2 — hhtechapi.net (New-API gateway khác hẳn ns24/9router, key riêng không chung tài
# khoản với 2 đường trên — xem docstring module). Verify thật 2026-09-22: text + multimodal OK,
# non-stream, không cần User-Agent riêng.
BACKUP2_BASE_URL = keys.get("sol_backup2_base_url", env="SOL_BACKUP2_BASE_URL",
                             default="https://hhtechapi.net/v1")
BACKUP2_API_KEY = keys.get("sol_backup2", env="SOL_BACKUP2_API_KEY",
                            default="sk-d4108f8b284a42b48df72bf4")
BACKUP2_MODEL = keys.get("sol_backup2_model", env="SOL_BACKUP2_MODEL", default="gpt-5.6-sol")

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


def _chat_backup2(text, image_path, max_tokens, timeout):
    """hhtechapi.net — non-stream chuẩn OpenAI, không cần User-Agent riêng (verify 2026-09-22)."""
    payload = {"model": BACKUP2_MODEL, "messages": [{"role": "user", "content": _content(text, image_path)}],
               "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {BACKUP2_API_KEY}", "Content-Type": "application/json"}
    r = httpx.post(f"{BACKUP2_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"sol backup2(hhtechapi) HTTP {r.status_code}: {r.text[:500]}")
    data = r.json()
    return data["choices"][0]["message"]["content"], data.get("usage", {})


# 9router LÀ ĐƯỜNG ĐẦU TIÊN Ở CẢ HAI MÁY (anh chốt 2026-09-26).
#
# ⚠️ ĐỌC TRƯỚC KHI ĐỊNH "TỐI ƯU" CHỖ NÀY: sáng 26/09 đã có một bản thêm phép TỰ DÒ (gõ cổng 20128,
# không thấy thì bỏ qua 9router) với lý do "máy 2 không có 9router". Lý do đó SAI — máy 2 vẫn dùng
# 9router từ trước tới nay. Phép tự dò đó chỉ chực tắt nhầm đường chính ở máy 2 mà không ai hay,
# nên đã gỡ bỏ. Muốn tắt thì đặt tay `SOL_DUNG_9ROUTER=0`, không để máy tự đoán hộ.
def _co_9router():
    """Có đưa 9router vào hàng không. Mặc định CÓ; chỉ `SOL_DUNG_9ROUTER=0` mới bỏ."""
    ep = str(keys.get("sol_dung_9router", env="SOL_DUNG_9ROUTER", default="")).strip().lower()
    return ep not in ("0", "false", "no")


def chat(text, image_path=None, max_tokens=2000, timeout=180):
    """Gửi 1 lượt chat (kèm ảnh nếu có) tới GPT-5.6-sol.

    Thứ tự: 9router → ns24 → hhtechapi (bỏ 9router bằng `SOL_DUNG_9ROUTER=0`).
    LỖI GÌ CŨNG chuyển đường (connection refused/timeout/HTTP khác 200) — người gọi không cần biết
    đang đi đường nào. Chỉ ném lỗi khi MỌI đường đều hỏng."""
    duong = ([("9router", _chat_primary)] if _co_9router() else []) + \
            [("ns24", _chat_backup), ("hhtechapi", _chat_backup2)]
    loi = []
    for i, (ten, ham) in enumerate(duong):
        try:
            return ham(text, image_path, max_tokens, timeout)
        except Exception as e:
            loi.append(f"{ten}: {e}")
            con = duong[i + 1][0] if i + 1 < len(duong) else None
            print(f"  ! sol {ten} lỗi: {type(e).__name__} {e}"
                  + (f" → thử {con}…" if con else ""), file=sys.stderr)
    raise RuntimeError("sol_client: MỌI đường đều lỗi.\n  " + "\n  ".join(loi))


def selftest():
    """`py -3.13 sol_client.py` — kiểm từng đường độc lập.

    9router chỉ được kiểm khi máy này thật sự có nó (máy 1); ở máy 2 nó không nằm trong đường chạy
    nên báo hỏng ở đây chỉ gây hoang mang."""
    sys.stdout.reconfigure(encoding="utf-8")
    bo = ([("9router", _chat_primary, BASE_URL, MODEL)] if _co_9router() else []) + \
         [("ns24", _chat_backup, BACKUP_BASE_URL, BACKUP_MODEL),
          ("hhtechapi", _chat_backup2, BACKUP2_BASE_URL, BACKUP2_MODEL)]
    if not _co_9router():
        print(f"(9router bị tắt tay bằng SOL_DUNG_9ROUTER=0 — bỏ qua {BASE_URL})")
    song = 0
    for ten, ham, base, model in bo:
        try:
            content, _usage = ham("Reply with exactly: OK", None, 10, 30)
            print(f"✓ {ten:10s} {base} model={model} → {content!r}")
            song += 1
        except Exception as e:
            print(f"✗ {ten:10s} {base}: {type(e).__name__} {e}")
    if song == 0:
        print("  → KHÔNG còn đường nào sống: mọi bước gọi sol sẽ hỏng.")
    elif song < len(bo):
        print(f"  ({song}/{len(bo)} đường sống — chat() vẫn chạy, chỉ hỏng khi về 0)")
    sys.exit(0 if song else 1)


if __name__ == "__main__":
    selftest()
