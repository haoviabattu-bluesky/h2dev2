"""llm_client.py — gọi LLM qua proxy OpenAI-compatible (ramclouds / ns24) THAY CHO Claude Code.

Vì sao code như dưới đây (mọi luật đều rút từ test thật 2026-09-07, xem
`docs/REPORT_RAMCLOUDS_HERMES.md` + `docs/AB_SCRIPT_MODELS.md`):

1. **LUÔN `stream:true`** — gọi non-stream thì claude-opus-5/deepseek-v4-pro/MiniMax-M3/kimi-k3 trả
   HTTP 200 + SSE RỖNG (`choices:[]`, `completion_tokens:0`) = MẤT TRẮNG nội dung, không báo lỗi.
2. **LUÔN có User-Agent** — thiếu là Cloudflare chặn 403 code 1010 (không phải lỗi key).
3. **Lỗi upstream có thể về dưới dạng NỘI DUNG**: `[Codex error: Our servers are currently overloaded]`
   với `finish_reason=stop`. Phải quét chuỗi, không tin status code.
4. **Stream có thể hết mà không có `finish_reason`** → văn bị cắt giữa câu. Phải kiểm ký tự cuối.
5. **Model đắt ≠ tốt**: claude-opus-5 (lane Postman) TỪ CHỐI viết truyện; ramclouds:gpt-5.6-sol hỏi lại
   bằng tiếng Việt 3/3 lần; grok-4.6 lặp vô hạn; deepseek-v4-pro cụt ở 200 token.
   → chuỗi fallback dưới đây chỉ gồm model ĐÃ VERIFY viết được.

Dùng:
  from llm_client import chat
  r = chat(prompt, system=skill_text, task="script")     # r.text, r.model, r.elapsed
  py -3.13 llm_client.py --ping              # kiểm 2 provider còn sống
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

PROVIDERS = {
    "ramclouds": {"base": "https://ramclouds.me",
                  "env": "RAMCLOUDS_API_KEY",
                  "default": "sk-ue0LE9lhUveoGFrt3Ah2SFJb82nPD9FVoe7jiihO3n6RnMeJ"},
    "ns24": {"base": "https://api.ns24.io",
             "env": "NS24_API_KEY",
             "default": "sk-up-0ef5398f1893e50f6a8d9055c7b9e7cb4f847dac7601d09f"},
}

# Mắt xích CUỐI của mọi chuỗi (thêm 2026-09-26): GPT-5.6-sol qua `sol_client`.
#
# VÌ SAO PHẢI CÓ (đo thật 2026-09-26): cả 3 mắt xích cũ đều là gemini-3.8-flash hoặc gpt-5.6-luna,
# mà `ramclouds:gpt-5.6-luna` hôm nay trả HTTP 503 → chuỗi thực chất chỉ còn ĐÚNG MỘT model
# (gemini-3.8-flash) ở 2 proxy. Gemini hỏng (hết quota / chặn chính sách nội dung / proxy sập) là
# TOÀN BỘ bước LLM của pipeline chết, không còn gì đỡ.
#
# VÌ SAO GỌI QUA `sol_client` CHỨ KHÔNG THÊM 1 DÒNG (provider, model) NHƯ CÁC MẮT XÍCH KHÁC:
# sol_client đã có sẵn đường tới cùng model đó ở nhiều proxy (ns24 stream+UA → hhtechapi
# non-stream; 9router đã TẮT vì máy 2 không có nó) với ĐÚNG cách gọi của từng proxy. Đo thật
# 2026-09-26: hhtechapi khi gọi stream trả HTTP 200 + SSE RỖNG, tức nó KHÔNG dùng được bằng bộ gọi
# stream của file này. Nhét thẳng vào PROVIDERS/CHAINS sẽ phải chép lại logic đó lần thứ hai và
# chắc chắn lệch dần.
#
# ⚠️ Đây là LƯỚI CUỐI, không phải model viết văn: bản ghi 2026-09-07 (docstring #5) cho thấy sol
# hỏi lại bằng tiếng Việt khi được giao VIẾT truyện. Đặt cuối chuỗi nên chỉ chạm tới khi gemini đã
# chết hẳn; nếu nó né việc thật thì `BAD_CONTENT` bắt được và chuỗi kết thúc đúng như cũ.
SOL_TAIL = ("sol", "gpt-5.6-sol")

# Chuỗi fallback theo việc — chỉ model ĐÃ VERIFY. Đừng thêm model chưa test vào đây.
CHAINS = {
    # viết/nén kịch bản dài: gemini-3.8-flash ramclouds (văn hay nhất, Nhật hoá 8/9)
    "script": [("ramclouds", "gemini-3.8-flash"),
               ("ns24", "gemini-3.8-flash"),
               SOL_TAIL],
    # việc ngắn/máy móc (prompt ảnh, chữ thumbnail, tóm tắt, cổng QC trả JSON): cùng model, rẻ, nhanh
    "short": [("ramclouds", "gemini-3.8-flash"),
              ("ns24", "gemini-3.8-flash"),
              ("ns24", "deepseek-v4.1-flash"),   # rẻ, KHÔNG phải gemini — xem ghi chú BAC_RE dưới
              SOL_TAIL],
    # tổng hợp DNA kênh (nhiều transcript gộp 1 lượt, pipeline/channel_analyzer.py) — TÁCH RIÊNG
    # khỏi "script" dù cùng model: đổi tham số viết-sáng-tạo sau này không vô tình ảnh hưởng bước
    # phân tích kênh (2 việc khác bản chất dù dùng chung model đã verify).
    "analysis": [("ramclouds", "gemini-3.8-flash"),
                 ("ns24", "gemini-3.8-flash"),
                 ("ns24", "deepseek-v4.1-flash"),
                 SOL_TAIL],
}

# BẬC RẺ `ns24:deepseek-v4.1-flash` (thêm 2026-09-26) — vì sao đúng model này, đúng nhà này:
#   · Đo thật cùng lúc 15 model ở 3 proxy: nó trả JSON đúng khuôn, viết được tiếng Nhật, và là bậc
#     NHANH NHẤT (dưới 1 giây cho việc ngắn).
#   · CÙNG TÊN MODEL nhưng ở RAMCLOUDS thì hỏng với ảnh — nên đừng đổi `ns24` thành `ramclouds` ở
#     dòng trên cho "gọn"; hai nhà chạy hai bản khác nhau.
#   · KHÔNG đưa vào chuỗi "script": phép thử chỉ chứng minh nó viết nổi HAI CÂU tiếng Nhật, không
#     chứng minh nổi bài kể 10.000 chữ. Việc viết vẫn gemini → sol.
# Tránh dùng làm bậc dự phòng (đã đo, đừng thử lại): `grok-4.5`/`grok-4.6` ở ramclouds treo 250
# giây rồi 503; `qwen3.8-flash` đọc ảnh sai tuổi tới 40 năm; `glm-5.3-flash` và `kimi-k3` là model
# SUY NGHĨ TRƯỚC — phần suy nghĩ ăn hết `max_tokens` nên hạn nhỏ là trả RỖNG mà HTTP vẫn 200.

# Nội dung TRẢ VỀ nhưng thực chất là lỗi/né việc → coi như FAIL, đổi model.
BAD_CONTENT = (
    "[codex error", "servers are currently overloaded", "rate limit",
    "bạn muốn tôi xử lý", "bạn muốn tôi", "how would you like me to",
    "i can't take", "i cannot take", "業務の範囲外", "お引き受けできません",
    # Google chặn theo CHÍNH SÁCH NỘI DUNG — trả về như NỘI DUNG BÌNH THƯỜNG (HTTP 200), không phải
    # lỗi. Không liệt kê ở đây thì coi như output hợp lệ ⇒ KHÔNG đổi model, cả chuỗi fallback đứng
    # yên. Đo thật 2026-09-11: cổng QC nội dung B3Q chết vì câu này trên một kịch bản kể chuyện
    # viện dưỡng lão — mà ngách satori thì tập nào cũng có tang ma/bệnh tật, nên sẽ dính liên tục.
    # Model kế trong chuỗi (deepseek/sol) không vướng chính sách này nên chỉ cần cho nó đổi là qua.
    "prompt could not be submitted", "prohibited use policy", "contains sensitive words",
    "blocked by the safety", "safety_ratings", "i'm not able to help with that",
)
SENT_END = "。．.!?！？」』）\"'”"

# DÒNG TIÊU ĐỀ CHƯƠNG vốn KHÔNG có dấu chấm — đó là tiêu đề, không phải câu bị cắt.
# Kịch bản Lane A chia 5 chương 第◯章, còn bước "chỉnh khúc" (ai_steps.trim_chunked) cắt bản nháp
# theo ranh giới đoạn, nên một khúc hoàn toàn có thể KẾT THÚC ngay tại dòng tiêu đề chương kế tiếp.
# Model trả lại đúng như vậy → phép kiểm "kết bằng dấu câu" tưởng là stream đứt giữa chừng và loại
# sạch. Đã dính thật ở ep02-walton 2026-09-12: khúc 2 kết bằng '第4章 神隠し', **cả 6 lượt / 3 model
# đều bị loại cùng một lý do** rồi chết cả lượt chạy — dấu hiệu nhận ra báo động giả: lỗi giống hệt
# nhau ở mọi model thì cái sai nằm ở phép kiểm, không nằm ở model.
# Chỉ bỏ qua dòng CUỐI khi nó khớp đúng khuôn tiêu đề chương (ngắn, mở đầu bằng 第◯章) — cố ý hẹp,
# để văn xuôi thật sự bị cắt giữa chừng vẫn bị bắt như cũ.
TIEU_DE_CHUONG = re.compile(r"^第[0-9０-９一二三四五六七八九十百]+章.{0,40}$")


def _bo_tieu_de_cuoi(text: str) -> str:
    """Bỏ dòng tiêu đề chương ở cuối (nếu có) trước khi kiểm 'kết bằng dấu câu'."""
    d = text.rstrip().splitlines()
    while d and (not d[-1].strip() or TIEU_DE_CHUONG.match(d[-1].strip())):
        d.pop()
    return "\n".join(d)


@dataclass
class ChatResult:
    text: str
    provider: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)
    finish: str = ""
    elapsed: float = 0.0
    attempts: list = field(default_factory=list)

    @property
    def chars(self):
        return len(self.text.replace("\n", "").replace(" ", "").replace("\u3000", ""))


class LLMError(RuntimeError):
    pass


# ---------------------------------------------------------------- key
def load_key(provider):
    """Ưu tiên: biến môi trường → keys.json/keys.txt CẠNH EXE → mặc định trong code.

    (đổi key ở máy khác chỉ cần sửa keys.json, không build lại exe)

    Phần tra file nằm trong `keys.py` — dùng CHUNG với key ảnh (gpti2/Grok) và key TTS. Trước đây
    mỗi bên có bộ đọc riêng, dẫn tới `keys.json` chỉ ăn cho key LLM còn key ảnh vẫn phải build lại.
    """
    import keys
    conf = PROVIDERS[provider]
    return keys.get(provider, env=conf["env"], default=conf["default"])


# ---------------------------------------------------------------- 1 lần gọi
def _stream_once(provider, model, messages, max_tokens, temperature, timeout, on_chunk):
    conf = PROVIDERS[provider]
    body = json.dumps({"model": model, "messages": messages, "max_tokens": max_tokens,
                       "temperature": temperature, "stream": True,
                       "stream_options": {"include_usage": True}},
                      ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        conf["base"] + "/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + load_key(provider), "User-Agent": UA,
                 "Content-Type": "application/json", "Accept": "text/event-stream"})
    parts, usage, finish, t0 = [], None, "", time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            try:
                obj = json.loads(payload)
            except Exception:
                continue
            if obj.get("usage"):
                usage = obj["usage"]
            for ch in obj.get("choices") or []:
                piece = (ch.get("delta") or {}).get("content")
                if piece:
                    parts.append(piece)
                    if on_chunk:
                        on_chunk(piece)
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
    return "".join(parts), usage or {}, finish, time.time() - t0


def _sol_once(model, messages, max_tokens, timeout):
    """Mắt xích cuối — GPT-5.6-sol qua `sol_client` (tự đi ns24 → hhtechapi).

    sol_client chỉ nhận MỘT khối text nên `system` được gộp vào đầu prompt; nó không phát từng
    mẩu nên `on_chunk` không áp dụng ở nhánh này (người gọi vẫn nhận đủ text ở cuối).
    Trả cùng bộ 4 giá trị như `_stream_once` để phần dưới không phải biết đây là nhánh khác.
    """
    import sol_client
    hoi = "\n\n".join(m["content"] for m in messages if isinstance(m.get("content"), str))
    t0 = time.time()
    # `model` chỉ để ghi nhật ký: mỗi proxy trong sol_client khai tên model riêng của nó
    # (`cx/gpt-5.6-sol` ở 9router, `gpt-5.6-sol` ở ns24/hhtechapi) nên chat() không nhận tham số này.
    text, usage = sol_client.chat(hoi, image_path=None, max_tokens=max_tokens,
                                  timeout=min(timeout, 300))
    return text, usage or {}, "stop", time.time() - t0


def _reject_reason(text, finish, min_chars, require_sentence_end):
    """Trả lý do FAIL, hoặc None nếu output dùng được."""
    if not text.strip():
        return "rỗng (proxy trả SSE không có content)"
    low = text[:600].lower()
    for bad in BAD_CONTENT:
        if bad in low:
            return f"model né việc/lỗi upstream trả trong nội dung: {text[:90]!r}"
    n = len(text.replace("\n", "").replace(" ", "").replace("\u3000", ""))
    if min_chars and n < min_chars:
        return f"quá ngắn {n} < {min_chars} chữ (finish={finish or 'None'})"
    if require_sentence_end:
        than = _bo_tieu_de_cuoi(text)
        if than and than[-1] not in SENT_END:
            return f"cắt giữa câu (finish={finish or 'None'}, kết bằng {than[-12:]!r})"
    return None


# ---------------------------------------------------------------- API chính
def chat(prompt, system=None, task="short", model=None, provider=None,
         max_tokens=32000, temperature=0.9, timeout=1800, on_chunk=None,
         min_chars=0, require_sentence_end=False, tries_per_model=2, verbose=True):
    """Gọi LLM, tự retry + tự đổi model khi output FAIL. Ném LLMError nếu hết chuỗi fallback."""
    chain = [(provider, model)] if (provider and model) else list(CHAINS.get(task, CHAINS["short"]))
    messages = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": prompt}]
    attempts = []
    for prov, mod in chain:
        for k in range(1, tries_per_model + 1):
            tag = f"{prov}:{mod} (lần {k})"
            try:
                if prov == "sol":
                    text, usage, finish, el = _sol_once(mod, messages, max_tokens, timeout)
                else:
                    text, usage, finish, el = _stream_once(prov, mod, messages, max_tokens,
                                                           temperature, timeout, on_chunk)
            except urllib.error.HTTPError as e:
                detail = e.read()[:160].decode("utf-8", "replace")
                msg = f"HTTP {e.code} {detail}"
                if "1010" in detail:
                    msg = "Cloudflare chặn 1010 — thiếu/sai User-Agent"
                attempts.append(f"{tag}: {msg}")
                if verbose:
                    print(f"  ✗ {tag}: {msg}")
                time.sleep(5)
                continue
            except Exception as e:
                attempts.append(f"{tag}: {type(e).__name__} {str(e)[:90]}")
                if verbose:
                    print(f"  ✗ {tag}: {type(e).__name__} {str(e)[:90]}")
                time.sleep(5)
                continue
            why = _reject_reason(text, finish, min_chars, require_sentence_end)
            if why:
                attempts.append(f"{tag}: {why}")
                if verbose:
                    print(f"  ✗ {tag}: {why}")
                time.sleep(3)
                continue
            n = len(text.replace("\n", "").replace(" ", "").replace("\u3000", ""))
            if verbose:
                print(f"  ✓ {tag}: {n:,} chữ · {el:.0f}s · out_tok={usage.get('completion_tokens')}")
            attempts.append(f"{tag}: OK {n} chữ {el:.0f}s")
            return ChatResult(text=text, provider=prov, model=mod, usage=usage,
                              finish=finish, elapsed=el, attempts=attempts)
    raise LLMError("Hết chuỗi fallback, không model nào cho output dùng được:\n  - " +
                   "\n  - ".join(attempts))


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ping", action="store_true", help="kiểm 2 provider + model chính còn sống")
    ap.add_argument("--ask", default="", help="gửi 1 prompt thử")
    ap.add_argument("--task", default="short", choices=list(CHAINS))
    args = ap.parse_args()
    if args.ping:
        for prov, mod in [("ramclouds", "gemini-3.8-flash"), ("ns24", "gemini-3.8-flash"),
                          ("ns24", "deepseek-v4.1-flash"), SOL_TAIL]:
            t0 = time.time()
            try:
                r = chat("Reply with exactly: ok", provider=prov, model=mod,
                         max_tokens=64, temperature=0, tries_per_model=1, verbose=False)
                print(f"{prov:10s} {mod:18s} OK   {time.time()-t0:5.1f}s  {r.text.strip()[:20]!r}")
            except LLMError as e:
                print(f"{prov:10s} {mod:18s} FAIL {time.time()-t0:5.1f}s  {str(e)[:110]}")
        return
    if args.ask:
        r = chat(args.ask, task=args.task)
        print(f"\n--- {r.provider}:{r.model} · {r.chars} chữ · {r.elapsed:.0f}s\n{r.text[:1200]}")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
