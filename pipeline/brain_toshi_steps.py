# -*- coding: utf-8 -*-
"""brain_toshi_steps.py — BỘ NÃO Claude cho Lane A (toshi-densetsu-jp), TÁCH HẲN khỏi
brain_steps.py của Satori (memory `hai-tool-exe-tach-han`: cấm gộp 2 nhánh não).

Khác biệt cốt lõi so với Satori bắt buộc phải tách file riêng thay vì tổng quát hoá chung:
Satori được đổi tên/ngày/số tự do (hư cấu 70/30). Lane A CẤM TUYỆT ĐỐI — mọi tên/ngày/số CHỈ được
lấy từ `series_ctx.txt`, sai là B3F chặn cứng. Khung "70/30 giữ nhịp gốc" của Satori vì vậy không
áp dụng được cho Lane A; NHỊP ở đây bám đúng 4 cổng thật của Lane A (chương/đảo chiều しかし/mốc sự
thật/câu lá chắn — xem docs/SOP_TOSHI_DENSETSU_JP.md §0).

    py -3.13 brain_toshi.py --slug ep08-fatima-akita --profile toshi-densetsu-jp
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def find_claude():
    import shutil
    for name in ("claude", "claude.cmd", "claude.exe"):
        p = shutil.which(name)
        if p:
            return p
    for c in (Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd",
              Path.home() / "AppData" / "Roaming" / "npm" / "claude.cmd"):
        if c.exists():
            return str(c)
    return None


def creative_prompt(slug_dir, profile_id, minutes, out_name, extra_prompt=""):
    """Đề bài NHỊP A→A.5→B→B.5 cho `claude -p`. Viết `out_name` (KHÔNG đè `script.txt` gốc — bản
    não-ramcloud vẫn giữ nguyên để so sánh)."""
    import profiles
    S = Path(slug_dir)
    prof = profiles.load(profile_id)
    target = int(profiles.target_chars(prof, minutes))
    g = profiles.gate(prof)
    chuong = g.get("chapter_markers") or ["第1章", "第2章", "第3章", "第4章", "第5章"]
    hook_lo, hook_hi = (g.get("hook_chars") or [650, 1150])[:2]

    gate_note = (
        f"\n⛔ CỔNG THẬT của lane này (đo bằng máy sau khi viết xong — KHÔNG phải khung 70/30 của "
        f"lane khác, đừng áp nhầm):"
        f"\n   · độ dài ~{target:,} chữ (không dấu cách) ±12%"
        f"\n   · đủ {len(chuong)} chương đánh dấu đúng nhãn: {', '.join(chuong)}"
        f"\n   · đảo chiều しかし/だが/ところが ≥{g.get('reversal_per_min', 0.5)}/phút VÀ khoảng cách "
        f"giữa 2 lần đảo chiều liên tiếp KHÔNG vượt {g.get('reversal_max_gap_sec', 300)} giây"
        f"\n   · mốc năm/số có đơn vị ≥{g.get('fact_anchor_per_min', 0.8)}/phút"
        f"\n   · mẫu câu lá chắn kiểu 〜という説がある ≥{g.get('hedge_min_per_10min', 2.0)}/10 phút"
        f"\n   · mở đầu (hook) dài {hook_lo}-{hook_hi} chữ, ≥{g.get('hook_anchor_per_1000', 18.0)} "
        f"neo dữ kiện (số + danh từ riêng katakana)/1000 chữ — mở đầu RỖNG (nói suông không dữ kiện) "
        f"là lỗi thật đã dính ở tập 3, ĐỪNG lặp lại"
        f"\n   · chương {g.get('require_japan_hook_chapter', 4)} PHẢI móc về Nhật Bản"
    )

    return "\n".join([
        "⚠️ CHẾ ĐỘ TỰ ĐỘNG (HEADLESS) — KHÔNG có người trả lời bạn. TUYỆT ĐỐI KHÔNG hỏi xác nhận, "
        "KHÔNG dừng giữa chừng xin ý kiến, KHÔNG dùng skill brainstorming/hỏi-đáp. Tự quyết và làm "
        "một mạch tới khi tạo xong file được giao.",
        "",
        f"Bạn viết B3 (kịch bản) cho 1 tập Lane A (都市伝説/vũ trụ/bí ẩn, kể tài liệu ngôi 3, tiếng "
        f"Nhật). Thư mục tập: {S}. Profile: {profile_id}. Mục tiêu: {minutes} phút.",
        "",
        f"Trong thư mục đã có `competitor.txt` (KHUNG KỂ — dạy nhịp/thứ tự dẫn dắt, KHÔNG phải nguồn "
        f"dữ kiện) và `series_ctx.txt` (TƯ LIỆU GỐC — mọi tên/ngày/số liệu PHẢI lấy đúng từ đây, CẤM "
        f"BỊA THÊM, CẤM đổi số liệu/tên/ngày để né trùng — khác hẳn lane hư cấu khác được phép đổi).",
        "Đọc docs/SOP_TOSHI_DENSETSU_JP.md mục §2-§4b (B2/B3/B3Q/B3F) trước khi viết.",
        gate_note,
        "",
        "LÀM ĐÚNG THEO NHỊP SAU, KHÔNG NHẢY CÓC:",
        "",
        f"NHỊP A — viết `{S / 'dan_y_claude.txt'}` (outline, CHƯA phải prose): liệt kê đúng "
        f"{len(chuong)} mục (1 mục/chương) + 1 mục hook mở đầu. Mỗi mục ghi: (a) nội dung chính kể "
        f"gì, (b) mốc dữ kiện cụ thể (tên/ngày/số) sẽ dùng, KÈM trích dẫn đúng câu/dòng trong "
        f"`series_ctx.txt` làm nguồn — không trích được thì KHÔNG được đưa mốc đó vào outline.",
        "",
        "NHỊP A.5 — TỰ KIỂM NGAY TRÊN OUTLINE (rẻ, làm TRƯỚC khi viết hết prose đắt):"
        f"\n   Đếm bằng số, không cảm tính, trả lời ĐÚNG/SAI cho từng câu:"
        f"\n   1. Outline có ĐỦ {len(chuong)} chương + 1 hook, không thiếu không thừa?"
        f"\n   2. MỖI chương có ≥1 mốc dữ kiện trích được nguồn trong series_ctx.txt (không phải suy "
        f"diễn/đoán)?"
        f"\n   3. Mục hook đã phác được ≥1 mốc dữ kiện đặc trưng chưa (tránh hook rỗng chỉ có câu hỏi "
        f"tu từ kiểu 'vì sao suốt bao năm...' không kèm dữ kiện nào)?"
        f"\n   4. Đã phác sơ bộ vị trí các câu đảo chiều しかし (mỗi chương ít nhất 1 chỗ dự kiến quay "
        f"đầu lập luận) chưa?"
        f"\n   THIẾU BẤT KỲ CÂU NÀO Ở TRÊN → sửa lại `dan_y_claude.txt` NGAY rồi tự hỏi lại 4 câu trên "
        f"cho tới khi cả 4 đều ĐÚNG. Đừng viết hết prose rồi mới phát hiện thiếu — sửa outline vài "
        f"dòng luôn rẻ hơn viết lại toàn bộ prose dài.",
        "",
        f"NHỊP B — viết `{S / out_name}` (voiceover-ready, thuần prose, KHÔNG bracket/heading/nhãn "
        f"chương lộ liễu kiểu markdown — nhãn 第◯章 viết THẲNG vào câu văn kể như lời dẫn tự nhiên) "
        f"bám sát outline vừa chốt. Giọng: {(prof.get('narrator', {}) or {}).get('persona', 'người dẫn tài liệu nam, trầm, điềm tĩnh')}.",
        "",
        "NHỊP B.5 — TỰ SOÁT 1 LƯỢT TRƯỚC KHI DỪNG (bộ lọc rẻ, KHÔNG thay thế cổng máy sẽ chạy sau "
        "bởi tiến trình khác — bạn không tự tuyên bố 'đạt', chỉ tự sửa lỗi rõ ràng tự nhìn thấy):"
        "\n   Đọc lại toàn bộ script vừa viết, tự hỏi và tự sửa nếu có:"
        "\n   - Tên người/địa danh/số liệu có NHẤT QUÁN xuyên suốt các chương không (lỗi thật đã "
        "dính: đặt 1 địa điểm ở 2 nơi khác nhau giữa 2 chương)?"
        "\n   - Có câu nào nói suông không chứa dữ kiện nào không (đặc biệt đoạn mở đầu)?"
        "\n   - Có đoạn nào lặp ý đã nói ở chương trước không?"
        "\n   Sửa xong thì DỪNG. In dòng `BRAIN_TOSHI_DONE` ra CÂU TRẢ LỜI CỦA BẠN (terminal), "
        "TUYỆT ĐỐI KHÔNG ghi chữ đó vào bất kỳ file nào — kể cả cuối script.txt (đã dính thật lần "
        "đầu chạy công cụ này: dòng `BRAIN_TOSHI_DONE` bị viết thẳng vào cuối kịch bản, lọt vào cả "
        "bản ghi giọng).",
        extra_prompt,
    ])


def run_creative(slug_dir, profile_id, minutes, out_name="script_claude.txt", on_line=None,
                  permission_mode="bypassPermissions", budget_usd=0.0, timeout=2400,
                  extra_prompt=""):
    """Gọi `claude -p` headless viết B3 cho Lane A. Trả (ok, dòng_cuối). Xem brain_steps.run_creative
    (Satori) — cùng cơ chế subprocess, KHÁC nội dung đề bài (tài liệu thật, không hư cấu)."""
    claude = find_claude()
    if not claude:
        msg = "✗ Không tìm thấy `claude` CLI trên máy này."
        (on_line or print)(msg)
        return False, msg
    prompt = creative_prompt(slug_dir, profile_id, minutes, out_name, extra_prompt)
    autonomy = ("Bạn đang chạy KHÔNG người giám sát (headless -p). Không bao giờ hỏi câu hỏi làm rõ, "
                "không chờ xác nhận, không đề xuất phương án rồi dừng. Tự quyết và thực thi liền mạch "
                "tới khi hoàn thành nhiệm vụ được giao.")
    PROJECT_ROOT = HERE.parent
    cmd = [claude, "-p", "--permission-mode", permission_mode,
           "--model", os.environ.get("BRAIN_MODEL", "opus"),
           "--append-system-prompt", autonomy,
           "--add-dir", str(PROJECT_ROOT), "--output-format", "stream-json", "--verbose"]
    if budget_usd and budget_usd > 0:
        cmd += ["--max-budget-usd", str(budget_usd)]
    emit = on_line or (lambda s: print(s, flush=True))
    emit(f"🧠 Claude (não Lane A) bắt đầu viết — {Path(slug_dir).name} · profile {profile_id} · {minutes}'")
    try:
        p = subprocess.Popen(cmd, cwd=str(PROJECT_ROOT), stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                             encoding="utf-8", errors="replace", bufsize=1,
                             env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        p.stdin.write(prompt)
        p.stdin.close()
    except Exception as e:
        emit(f"✗ Không chạy được claude: {type(e).__name__} {e}")
        return False, str(e)
    last = ""
    try:
        for raw in p.stdout:
            line = raw.rstrip("\n")
            if line:
                last = line
                emit("  " + line)
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        emit("✗ Claude quá thời gian → dừng.")
        return False, "timeout"
    out_f = Path(slug_dir) / out_name
    ok = (p.returncode == 0) and out_f.exists() and out_f.stat().st_size > 200
    if not ok:
        emit(f"✗ Claude chưa tạo {out_name} hợp lệ.")
        return False, f"thiếu {out_name}"
    return ok, last
