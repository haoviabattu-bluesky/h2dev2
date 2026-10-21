"""claude_p_bridge.py — gọi `claude -p` headless để SINH VĂN BẢN cho ĐÚNG 1 prompt, dùng làm
"não viết" thay Gemini cho những bước THỰC SỰ SÁNG TẠO (PASS 0 bóc khung + PASS 1 viết bản nháp của
B3) khi profile khai `script.engine = "claude_p"`.

KHÁC `brain_steps.py` (satori): ở satori, `claude -p` là 1 AGENT ĐẦY ĐỦ — tự đọc file, tự ghi
script.txt/characters.json/img_prompts.txt, tự gọi qc_script.py, tự sửa lặp tới khi đạt, chạy trong
CHÍNH thư mục dự án (`--add-dir`). Ở ĐÂY, `claude -p` chỉ TRẢ CHỮ cho 1 PROMPT — `--tools ""` tắt hết
tool (không đọc/ghi file gì, không Bash, không WebSearch) — y hệt cách `llm_client.chat()` đang được
dùng trong `ai_steps.py` (nhận 1 chuỗi prompt đã có sẵn đủ ngữ cảnh, trả 1 chuỗi văn bản). Nhờ vậy
CẮM THẲNG vào chỗ đang gọi `chat(...)` mà KHÔNG phải sửa gì xung quanh — gate/nén/QC/retry
(`trim_chunked`, `check()`, `qc_script.py`, `qc_facts.py`, `--tries`) vẫn nguyên vẹn, vẫn Gemini,
đúng tinh thần "Claude viết — Gemini chấm độc lập" (đã áp dụng cho satori: `qc_script.py` bên đó
CŨNG là Gemini, không phải Claude tự chấm bài mình).

Trả về CÙNG kiểu `llm_client.ChatResult` (`.text/.provider/.model/.elapsed/.chars`) để nơi gọi không
cần đổi 1 dòng nào khác ngoài chỗ chọn nhánh chat() vs ask().
"""
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from llm_client import ChatResult, LLMError, SENT_END, _bo_tieu_de_cuoi


_CLAUDE_CACHE = {}


def brain_model_of(prof):
    """Model `claude -p` của lane: `profile.script.brain_model` (vd "claude-fable-5-1", "opus") →
    env BRAIN_MODEL → "opus". Field-driven (hàng rào #2): Lane G chọn Fable 5.1 viết kịch bản
    (anh chốt 2026-09-20), lane khác không khai thì giữ opus như cũ."""
    return ((prof.get("script", {}) or {}).get("brain_model") or os.environ.get("BRAIN_MODEL") or "opus")


def patch_model_of(prof):
    """Model cho S4 (patch tại chỗ theo Sol/máy, lean_script.patch): `profile.script.patch_model`, không khai
    thì = brain_model. Tách khỏi S2 để Fable chỉ VIẾT (S2), còn sửa là việc của model khác — A/B replay 9 lượt
    patch thật Lane F/G 2026-09-22: Opus 5 ngang Fable (Sol PASS 7/9, số câu đổi ngoài phạm vi Sol trích tương
    đương), anh chốt đổi S4 sang Opus để giảm tải quota Fable."""
    return ((prof.get("script", {}) or {}).get("patch_model") or brain_model_of(prof))


def prompt_model_of(prof):
    """Model viết PROMPT ẢNH (B5W, prompt_doan.py): `profile.image.prompt_model`, không khai = claude-opus-5.
    Anh chốt 2026-09-26: B5W không cần Fable — chuyển Opus để dành hạn mức Fable (tính riêng) cho viết kịch bản S2
    và kịch bản quay hook (hook_storyboard, vẫn brain_model = Fable)."""
    return ((prof.get("image", {}) or {}).get("prompt_model") or "claude-opus-5")


def _claude_version(path):
    """Trả tuple version của 1 binary claude (vd (2,1,278)); lỗi → (0,)."""
    try:
        r = subprocess.run([path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, timeout=20)
        m = re.search(r"(\d+)\.(\d+)\.(\d+)", r.stdout or "")
        return tuple(int(x) for x in m.groups()) if m else (0,)
    except Exception:
        return (0,)


def find_claude():
    """Tìm `claude` CLI — ưu tiên bản MỚI NHẤT trên máy, không phải bản đầu tiên trên PATH.

    Bài học 2026-09-20 (Lane G): máy có 3 bản — npm trên PATH 2.1.145, ~/.local/bin 2.1.12, và bản
    native trong extension VSCode 2.1.278. Bản npm cũ (a) KHÔNG gọi được Fable 5.1 ("version 2.1.251
    or newer is required"), (b) alias `opus` của nó trỏ về **Opus 4.7** trong khi bản 2.1.278 trỏ về
    Opus 5 — tức lane E chạy "não Claude Opus" lâu nay thực ra là 4.7 mà không ai biết. Chọn theo
    version thật (`--version`) thay vì thứ tự PATH; ép bản cụ thể bằng env `CLAUDE_CLI=<đường dẫn>`.
    Kết quả cache trong tiến trình (mỗi `--version` ~0,5s)."""
    if "path" in _CLAUDE_CACHE:
        return _CLAUDE_CACHE["path"]
    forced = os.environ.get("CLAUDE_CLI", "").strip()
    if forced and Path(forced).exists():
        _CLAUDE_CACHE["path"] = forced
        return forced
    cands = []
    for name in ("claude", "claude.cmd", "claude.exe"):
        p = shutil.which(name)
        if p:
            cands.append(p)
    for c in (Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd",
              Path.home() / "AppData" / "Roaming" / "npm" / "claude.cmd",
              Path.home() / ".local" / "bin" / "claude.exe"):
        if c.exists():
            cands.append(str(c))
    # bản native đi kèm extension VSCode (anthropic.claude-code-<ver>-win32-x64/resources/native-binary/claude.exe)
    cands += [str(x) for x in (Path.home() / ".vscode" / "extensions").glob(
        "anthropic.claude-code-*/resources/native-binary/claude.exe")]
    cands = list(dict.fromkeys(cands))
    if not cands:
        _CLAUDE_CACHE["path"] = ""
        return ""
    best = max(cands, key=_claude_version)
    _CLAUDE_CACHE["path"] = best
    return best


def ask(prompt, system=None, model=None, timeout=1800, min_chars=0, require_sentence_end=False, max_chars=0):
    """Gọi `claude -p` KHÔNG tool (`--tools ""`), trả `ChatResult`. Ném `LLMError` nếu hỏng/thiếu
    chữ/cắt giữa câu — CÙNG tiêu chí `llm_client._reject_reason()` áp cho Gemini, để hai nhánh so
    được công bằng và nơi gọi (vd `write_script`'s "bản nháp ngắn → viết lại 1 lần") xử lý y hệt."""
    claude = find_claude()
    if not claude:
        raise LLMError("không tìm thấy `claude` CLI trên máy này — cần Claude Code đã cài + đăng nhập")
    # Thứ tự: tham số → env BRAIN_MODEL → "opus". Lane khai `script.brain_model` trong profile thì nơi
    # gọi truyền vào đây (ai_steps._writer_chat / make_video B3S) — xem brain_model_of().
    model = model or os.environ.get("BRAIN_MODEL", "opus")
    cmd = [claude, "-p", "--tools", "", "--output-format", "text", "--model", model,
           "--no-session-persistence"]
    if system:
        cmd += ["--system-prompt", system]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, input=prompt, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout,
                           # 2026-10-03 (Lane F ep09 B5W): câu trả lời dài vượt trần output mặc định → CLI tự "continue"
                           # và `--output-format text` chỉ in KHÚC CUỐI (bắt đầu từ dòng 400/444) → "trả quá ngắn". Nâng trần.
                           env={"CLAUDE_CODE_MAX_OUTPUT_TOKENS": "64000", **os.environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        raise LLMError(f"claude -p quá thời gian ({timeout}s)") from None
    except Exception as e:
        raise LLMError(f"gọi claude -p thất bại: {type(e).__name__} {e}") from None
    elapsed = time.time() - t0
    if r.returncode != 0:
        # stderr có thể chỉ là cảnh báo settings (đo thật 20/09: rule allow có wildcard che mất lỗi thật) → kèm cả đuôi stdout
        raise LLMError(f"claude -p thoát mã {r.returncode}: stderr={(r.stderr or '')[-200:]!r} stdout={(r.stdout or '')[-300:]!r}")
    text = (r.stdout or "").strip()
    # Bản CLI cũ trả LỜI BÁO LỖI dạng text với exit 0 (đo thật 2.1.145 + model fable): coi là lỗi.
    if re.match(r"^(API Error:|There's an issue with the selected model)", text):
        raise LLMError(f"claude -p ({claude}) từ chối model {model}: {text[:160]}")
    n = len(text.replace("\n", "").replace(" ", "").replace("　", ""))
    if min_chars and n < min_chars:
        raise LLMError(f"claude -p trả quá ngắn {n} < {min_chars} chữ (elapsed={elapsed:.0f}s)")
    # Lượt SỬA TẠI CHỖ (B3S/B3R FIX) mà trả dài vượt trần = model VIẾT THÊM thay vì sửa (đo thật Lane G ep01:
    # 6.962 → 8.063 chữ, +16%, thoại 39→45%) → từ chối, nơi gọi giữ bản gốc.
    if max_chars and n > max_chars:
        raise LLMError(f"claude -p trả quá dài {n:,} > trần {max_chars:,} chữ — sửa tại chỗ mà viết thêm (elapsed={elapsed:.0f}s)")
    if require_sentence_end:
        than = _bo_tieu_de_cuoi(text)
        if than and than[-1] not in SENT_END:
            raise LLMError(f"claude -p cắt giữa câu (kết bằng {than[-12:]!r})")
    return ChatResult(text=text, provider="claude-cli", model=model, elapsed=elapsed)
