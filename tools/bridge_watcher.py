#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bridge_watcher.py — ĐIỀU PHỐI TỰ ĐỘNG LANE A (toshi-densetsu-jp)
================================================================
Vòng lặp cần tự động hoá:
    DeepSeek (agent bước 3) ghi câu hỏi vào CLAUDE-DEEPSEEK.TXT
        →  watcher phát hiện
        →  gọi `claude -p` (Claude Code print mode, máy 1 — người giám sát pipeline)
        →  Claude đọc báo cáo + runbook + dữ liệu thật, TỰ QUYẾT, ghi trả lời vào
           CUỐI cùng file giao việc (khối "CLAUDE → DEEPSEEK TRẢ LỜI")
        →  watcher xác minh, log, thoát. KHÔNG cần người ngồi trả lời.

AN TOÀN (ràng buộc cứng):
- Chỉ ĐỌC file giao việc + gọi claude -p. KHÔNG đụng assets/, pipeline/, cột H.
- claude -p chạy với --allowedTools "Read,Write,Edit" (KHÔNG Bash) → không chạy lệnh,
  không --force-qc, không tự ý make_video. Chỉ đọc + ghi trả lời vào file giao việc.
- KHÔNG sửa nội dung cũ của file — chỉ THÊM khối trả lời vào cuối.
- Idempotent: có marker trả lời hoặc hash đã xử lý → bỏ qua. Retry tối đa 2 lần.

Cách dùng:
    py -3.13 bridge_watcher.py --once        # quét 1 lần (cho Task Scheduler)
    py -3.13 bridge_watcher.py --watch 180   # vòng lặp 180s
    py -3.13 bridge_watcher.py --test        # tự kiểm tra logic phát hiện
Env: AI_H2DEV_ROOT (mặc định E:\\CLAUDE\\YOUTUBE\\h2dev)
     FILE_GIAO_VIEC   (mặc định CLAUDE-DEEPSEEK.TXT)
     CLAUDE_MODEL     (mặc định sonnet)
"""
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

H2DEV = Path(os.environ.get("AI_H2DEV_ROOT", r"E:\CLAUDE\YOUTUBE\h2dev"))
FILE_GIAO_VIEC = Path(os.environ.get("FILE_GIAO_VIEC", str(H2DEV / "CLAUDE-DEEPSEEK.TXT")))
if not os.path.isabs(str(FILE_GIAO_VIEC)):
    FILE_GIAO_VIEC = H2DEV / FILE_GIAO_VIEC
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "sonnet")
CLAUDE_TIMEOUT = int(os.environ.get("CLAUDE_TIMEOUT", "900"))
TOOLS = H2DEV / "tools"
LOG_FILE = TOOLS / "bridge_watcher.log"
STATE_FILE = TOOLS / "bridge_state.json"
BACKUP_DIR = TOOLS / "_backup_giao_viec"
LOCK_FILE = TOOLS / "bridge_watcher.lock"

MARKER_HOI = ("Câu hỏi cho Claude", "CÂU HỎI CHO CLAUDE",
              "Cau hoi cho Claude", "CAU HOI CHO CLAUDE",
              "chờ Claude trả lời", "CHỜ CLAUDE TRẢ LỜI")
MARKER_TRA_LOI = "CLAUDE → DEEPSEEK TRẢ LỜI"
RETRY_MAX = 2

BASH = os.environ.get("BASH") or r"C:\Program Files\Git\bin\bash.exe"

# Telegram topic toshi (DeepSeek agent bước 3) — tự động báo sau khi Claude trả lời
TOSHI_ENV = Path(os.environ.get("TOSHI_ENV",
                                r"C:\Users\admin\AppData\Local\hermes\profiles\toshi\.env"))
TOSHI_CHAT_ID = os.environ.get("TOSHI_CHAT_ID", "1037124408")
TOSHI_THREAD_ID = os.environ.get("TOSHI_THREAD_ID", "555548")


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    line = f"{now_ts()} {msg}"
    print(line, flush=True)
    TOOLS.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def md5_file(path):
    h = hashlib.md5()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def read_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(st):
    TOOLS.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, STATE_FILE)


def co_cau_hoi(text):
    return any(m in text for m in MARKER_HOI)


def da_tra_loi(text):
    # Footer chuẩn do chính watcher/Claude viết khi trả lời — không bị false positive
    # khi worker THAM CHIẾU lại marker cũ trong nội dung báo cáo mới.
    return "Trả lời tự động bởi bridge watcher" in text


def tinh_so_lieu_qc():
    """Watcher TỰ tính số liệu từ qc_canh.json/state.json (không để worker tự suy diễn).
    Trả chuỗi 'SỐ LIỆU MÁY TÍNH' để nhúng vào prompt, hoặc '' nếu không tìm thấy tập."""
    try:
        txt = FILE_GIAO_VIEC.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    slugs = re.findall(r"ep\d+[\w-]*", txt)
    for slug in slugs:
        td = H2DEV / "assets" / "toshi-densetsu-jp" / slug
        qf = td / "qc_canh.json"
        if not qf.exists():
            continue
        ds = json.loads(qf.read_text(encoding="utf-8"))
        cham = [x for x in ds if x.get("muc") is not None]
        lac = [x for x in cham if x.get("muc") == 0]
        ha = [x for x in ds if x.get("loi_ha_tang")]
        ty = len(lac) / max(len(cham), 1)
        sf = td / "state.json"
        st = json.loads(sf.read_text(encoding="utf-8")).get("B8Q", {}) if sf.exists() else {}
        bang_chung_lac = [x for x in lac if x.get("bangchung")]
        buf = [
            "=== SỐ LIỆU DO WATCHER TỰ TÍNH (đáng tin hơn tự đọc — đừng kết luận trái ngược) ===",
            f"Tập: {slug}",
            f"qc_canh.json: tổng {len(ds)} · chấm được {len(cham)} · "
            f"LẠC (muc==0) {len(lac)} ({ty:.1%}) · lỗi hạ tầng (loi_ha_tang) {len(ha)}",
            f"state.json B8Q: canh {st.get('canh')} · lac {st.get('lac')} · ty_le_lac {st.get('ty_le_lac')} · infra {st.get('infra')}",
            f"Trong {len(lac)} cảnh lạc có {len(bang_chung_lac)} cảnh là ẢNH BẰNG CHỨNG "
            f"({', '.join(sorted({x['file'] for x in bang_chung_lac})) or 'không'}).",
            "CẢNH LẠC THẬT (muc==0 — CÓ 'ta', chấm được nhưng lạc):",
        ]
        for x in sorted(lac, key=lambda c: c["t0"])[:20]:
            buf.append(f"  {x['t0']:>7.1f}s {x['file'][:34]:34s} | {str(x.get('ta'))[:42]}")
        buf.append("CẢNH HẠ TẦNG (loi_ha_tang — KHÔNG chấm được):")
        for x in ha[:20]:
            buf.append(f"  {x['t0']:>7.1f}s {x['file'][:34]:34s} | {str(x.get('loi_ha_tang'))[:42]}")
        buf.append("LƯU Ý CẤU TRÚC: trong qc_canh.json KHÔNG có field 'lac' — cảnh lạc = field "
                   "'muc' == 0. 'xau' = hình xấu kỹ thuật. 'bangchung': true = ảnh bằng chứng "
                   "(evidence.json ghim cố định, không bị cam-file-lac cấm).")
        return "\n".join(buf)
    return ""


def prompt_tra_loi(file_path):
    so_lieu = tinh_so_lieu_qc()
    du_lieu = ("\n" + so_lieu + "\n") if so_lieu else ("\n(KHÔNG tìm thấy qc_canh.json cho tập "
                "trong file giao việc — bạn phải tự đọc và tự tính, cẩn thận field 'muc'.)\n")
    return (
        "Bạn là Claude — máy 1 (agent giám sát pipeline) của lane toshi-densetsu-jp trong dự án h2dev.\n"
        "\n"
        "Đọc theo thứ tự:\n"
        f"1. {file_path} — báo cáo của DeepSeek (agent bước 3) + mục 'Câu hỏi cho Claude' cần bạn trả lời.\n"
        "2. E:/CLAUDE/YOUTUBE/h2dev/docs/GIAO_VIEC_BUOC3_AGENT.md — runbook bước 3 (đặc biệt §5.2 B8Q rớt, §8 checklist xong việc).\n"
        "3. E:/CLAUDE/YOUTUBE/h2dev/docs/SOP_TOSHI_DENSETSU_JP.md — SOP lane A (mục §8a B8Q).\n"
        + du_lieu +
        "\n"
        "NHIỆM VỤ: trả lời ĐẦY ĐỦ từng câu hỏi trong mục 'Câu hỏi cho Claude'. Bạn có toàn quyền quyết định "
        "kỹ thuật trong phạm vi runbook. Mỗi câu trả lời gồm: quyết định rõ ràng + lý do dựa trên số liệu "
        "thật + lệnh tiếp theo cụ thể cho DeepSeek (kèm điều kiện/ràng buộc nếu có). Nếu quyết định vượt hạn "
        "mức runbook thì phải nói rõ vì sao vượt và ràng buộc chặt (ví dụ: chỉ 1 lượt cuối, rớt nữa thì dừng).\n"
        "SỐ LIỆU MÁY TÍNH ở trên là do watcher tính trực tiếp từ file — dùng nó làm nền tảng. Bạn có thể đọc "
        "lại file để kiểm chứng chi tiết, nhưng KHÔNG được kết luận trái ngược số liệu máy tính mà không nêu "
        "rõ bằng chứng.\n"
        "\n"
        "YÊU CẦU GHI FILE: dùng công cụ Edit/Write THÊM vào CUỐI file giao việc một khối có dạng:\n"
        "================================================================================\n"
        "CLAUDE → DEEPSEEK TRẢ LỜI (2026-09-13 HH:MM)\n"
        "================================================================================\n"
        "<toàn văn câu trả lời của bạn>\n"
        "\n"
        "(Trả lời tự động bởi bridge watcher — claude -p print mode)\n"
        "================================================================================\n"
        "\n"
        "LUẬT CỨNG:\n"
        "- KHÔNG sửa/xoá/thay đổi bất kỳ nội dung nào khác của file (báo cáo DeepSeek phía trên giữ nguyên).\n"
        "- KHÔNG sửa file nào khác ngoài file giao việc. KHÔNG chạy lệnh. KHÔNG --force-qc.\n"
        "- KHÔNG tự ý chạy make_video.py hay bất kỳ lệnh ghép nào — bạn chỉ TRẢ LỜI và ghi vào file.\n"
        "- KHÔNG bịa số liệu — mọi con số phải tra từ file thật trên đĩa.\n"
        "Khi xong, trả lời ngắn gọn một dòng cuối: ĐÃ TRẢ LỜI <n> CÂU HỎI"
    )


def run_claude(prompt):
    cmd = ("claude -p " + shlex.quote(prompt) +
           f" --model {shlex.quote(CLAUDE_MODEL)} --output-format json "
           "--max-turns 30 --allowedTools 'Read,Write,Edit' --no-session-persistence")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    try:
        r = subprocess.run([BASH, "-lc", cmd], cwd=str(H2DEV), env=env,
                           capture_output=True, text=True, timeout=CLAUDE_TIMEOUT)
        return r.returncode, (r.stdout or "") + "\n" + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT sau {CLAUDE_TIMEOUT}s"
    except Exception as e:
        return -1, f"EXCEPTION: {e}"


def backup_truoc_khi_ghi(path):
    """Backup bản gốc để verify sau — watcher KHÔNG tự sửa file, chỉ để truy vết."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = BACKUP_DIR / f"{Path(path).stem}_{stamp}.bak"
    dst.write_bytes(Path(path).read_bytes())
    return dst


def bot_token_toshi():
    """Đọc TELEGRAM_BOT_TOKEN từ .env của profile toshi — KHÔNG in giá trị ra."""
    try:
        for line in TOSHI_ENV.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("TELEGRAM_BOT_TOKEN="):
                t = s.split("=", 1)[1].strip().strip('"').strip("'")
                if t and not t.startswith("${"):
                    return t
    except Exception:
        pass
    return ""


def tom_tat_tra_loi(text):
    """Trích tóm tắt quyết định từ KHỐI TRẢ LỜI THẬT (neo vào footer — worker có thể
    tham chiếu lại marker cũ trong nội dung, đừng tìm bằng find() đơn thuần)."""
    f = text.rfind("(Trả lời tự động bởi bridge watcher")
    if f == -1:
        return ""
    m = text.rfind(MARKER_TRA_LOI, 0, f)  # marker NGAY TRƯỚC footer = khối cuối cùng
    if m == -1:
        return ""
    body = text[m:f]
    for line in body.splitlines():
        if "QUYẾT ĐỊNH" in line.upper():
            return re.sub(r"\s+", " ", line).strip()[:300]
    return re.sub(r"\s+", " ", body).strip()[:400]


def gui_topic_toshi(noi_dung):
    """Gửi tin nhắn vào topic Telegram toshi (DeepSeek) qua Bot API. Trả (ok, chi_tiet)."""
    tok = bot_token_toshi()
    if not tok:
        return False, f"không đọc được TELEGRAM_BOT_TOKEN từ {TOSHI_ENV}"
    url = f"https://api.telegram.org/bot{tok}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TOSHI_CHAT_ID,
        "message_thread_id": TOSHI_THREAD_ID,
        "text": noi_dung,
        "disable_web_page_preview": "true",
    }).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
            return (r.status == 200 and '"ok":true' in body), body[:150]
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def bao_deepseek_topic(text_giao_viec):
    """Báo DeepSeek: Claude đã trả lời. Chỉ gửi 1 lần cho mỗi bản trả lời (state hash)."""
    st = read_state()
    cur = md5_file(FILE_GIAO_VIEC)
    if st.get("da_gui_topic_hash") == cur:
        return None  # bản trả lời này đã báo rồi
    tom = tom_tat_tra_loi(text_giao_viec)
    if not tom:
        return None
    noi_dung = (
        "📬 [BRIDGE] Claude đã trả lời câu hỏi của bạn.\n"
        f"Đọc đầy đủ: {FILE_GIAO_VIEC} (khối `{MARKER_TRA_LOI}`).\n\n"
        f"Tóm tắt quyết định: {tom}\n\n"
        "→ Vào đọc file và tiếp tục công việc bước 3. Sau khi xong, ghi đè file bằng "
        "báo cáo mới (kèm mục 'Câu hỏi cho Claude' nếu còn vướng mắc cần Claude xử lý)."
    )
    ok, chi_tiet = gui_topic_toshi(noi_dung)
    if ok:
        st["da_gui_topic_hash"] = cur
        save_state(st)
        log(f"📨 Đã báo topic toshi (thread {TOSHI_THREAD_ID}) — DeepSeek đọc file tiếp tục")
    else:
        log(f"⚠️ Gửi topic toshi LỖI: {chi_tiet} — sẽ thử lại lần quét sau")
    return ok


def xu_ly_mot_lan(force=False):
    """Quét 1 lần. Trả (code, thông điệp). code: 0 = không việc/đã xong, 1 = đã trả lời, 2 = lỗi."""
    if not FILE_GIAO_VIEC.exists():
        return 0, "không có file giao việc"
    try:
        text = FILE_GIAO_VIEC.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return 2, f"KHÔNG ĐỌC ĐƯỢC file giao việc: {e}"

    if da_tra_loi(text):
        # Đã có trả lời của Claude — nếu chưa báo DeepSeek thì báo (1 lần/bản trả lời)
        bao_deepseek_topic(text)
        return 0, "đã có trả lời của Claude — (đã/đang báo DeepSeek qua topic toshi)"
    if not co_cau_hoi(text):
        return 0, "file không chứa câu hỏi chờ — không phải việc của watcher"

    st = read_state()
    cur = md5_file(FILE_GIAO_VIEC)
    if not force and st.get("da_xu_ly_hash") == cur:
        return 0, "file chưa đổi từ lần xử lý trước — bỏ qua"

    log(f"PHÁT HIỆN câu hỏi chờ trong {FILE_GIAO_VIEC.name} — đánh thức Claude...")
    backup = backup_truoc_khi_ghi(FILE_GIAO_VIEC)
    ok = False
    for i in range(1, RETRY_MAX + 2):
        rc, out = run_claude(prompt_tra_loi(str(FILE_GIAO_VIEC)))
        sau = FILE_GIAO_VIEC.read_text(encoding="utf-8", errors="replace")
        if da_tra_loi(sau):
            ok = True
            log(f"✓ Claude ĐÃ TRẢ LỜI (lần {i}, rc={rc}) — marker xuất hiện trong file")
            break
        log(f"  lần {i}: claude thoát rc={rc} nhưng chưa ghi marker — {(out or '')[:300]}")
        time.sleep(5)
    st["da_xu_ly_hash"] = md5_file(FILE_GIAO_VIEC)
    st["lan_tra_loi_cuoi"] = now_ts()
    save_state(st)
    if ok:
        bao_deepseek_topic(FILE_GIAO_VIEC.read_text(encoding="utf-8", errors="replace"))
        return 1, f"✓ Claude đã trả lời câu hỏi → {FILE_GIAO_VIEC.name} (backup: {backup.name})"
    return 2, (f"✗ Claude KHÔNG ghi được trả lời sau {RETRY_MAX + 1} lần — xem {LOG_FILE.name}. "
               f"Backup: {backup.name}")


def run_test():
    fails = []
    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name, flush=True)
        if not cond:
            fails.append(name)

    check("detect câu hỏi", co_cau_hoi("... Câu hỏi cho Claude: 1. abc"))
    check("detect CÂU HỎI hoa", co_cau_hoi("... CÂU HỎI CHO CLAUDE"))
    check("không nhận nhầm", not co_cau_hoi("báo cáo thường, không có câu hỏi"))
    check("detect đã trả lời", da_tra_loi("...\nCLAUDE → DEEPSEEK TRẢ LỜI (2026-09-13 07:00)\n...\n(Trả lời tự động bởi bridge watcher — claude -p print mode)"))
    check("không nhận nhầm trả lời", not da_tra_loi("CLAUDE đang chờ DEEPSEEK trả lời"))
    check("không nhận nhầm khi worker THAM CHIẾU marker cũ",
          not da_tra_loi("(CLAUDE → DEEPSEEK TRẢ LỜI 2026-09-13 07:47 — cho phép lượt 4)"))

    # mô phỏng chuỗi: file có câu hỏi → chưa trả lời → sau khi xử lý có marker
    tmp = Path(tempfile.mkdtemp(prefix="bridge_test_"))
    f = tmp / "test.txt"
    f.write_text("DEEPSEEK → CLAUDE\nCâu hỏi cho Claude:\n1. test?", encoding="utf-8")
    check("file mẫu có câu hỏi", co_cau_hoi(f.read_text(encoding="utf-8")))
    f.write_text(f.read_text(encoding="utf-8") + "\nCLAUDE → DEEPSEEK TRẢ LỜI (test)\n"
                 "(Trả lời tự động bởi bridge watcher — claude -p print mode)\n", encoding="utf-8")
    check("sau trả lời: có marker", da_tra_loi(f.read_text(encoding="utf-8")))
    check("nội dung cũ giữ nguyên", f.read_text(encoding="utf-8").startswith("DEEPSEEK → CLAUDE"))

    print("=" * 50)
    if fails:
        print(f"FAILED {len(fails)}: {fails}")
        return 1
    print("ALL TESTS PASSED")
    return 0


def _lock():
    """Chống 2 instance chạy đè (Task Scheduler mỗi 3 phút + watcher đang chạy lâu)."""
    TOOLS.mkdir(parents=True, exist_ok=True)
    try:
        if LOCK_FILE.exists():
            age = time.time() - LOCK_FILE.stat().st_mtime
            if age < 600:  # lock còn mới (< 10 phút) → instance khác đang chạy
                return False
        LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")
        return True
    except Exception:
        return True


def _unlock():
    try:
        LOCK_FILE.unlink()
    except Exception:
        pass


def main():
    args = sys.argv[1:]
    TOOLS.mkdir(parents=True, exist_ok=True)
    if "--test" in args:
        sys.exit(run_test())
    if "--watch" in args:
        secs = 180
        try:
            secs = int(args[args.index("--watch") + 1])
        except (ValueError, IndexError):
            pass
        log(f"START watch {FILE_GIAO_VIEC.name} mỗi {secs}s")
        while True:
            try:
                code, msg = xu_ly_mot_lan()
                if code:
                    log(msg)
            except Exception as e:
                log(f"LỖI vòng lặp: {e}")
            time.sleep(secs)
    # --once (mặc định)
    if not _lock():
        return 0  # instance khác đang chạy
    try:
        code, msg = xu_ly_mot_lan(force="--force" in args)
        if msg:
            print(msg, flush=True)
        return 0 if code in (0, 1) else 2
    finally:
        _unlock()


if __name__ == "__main__":
    sys.exit(main())
