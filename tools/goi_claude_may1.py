#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""goi_claude_may1.py — gọi claude -p thực thi 3 việc máy 1 (dùng 1 lần, qua terminal)."""
import os
import shlex
import subprocess
import sys
from pathlib import Path

H2DEV = Path(r"E:\CLAUDE\YOUTUBE\h2dev")
BASH = r"C:\Program Files\Git\bin\bash.exe"

PROMPT = """Bạn là Claude — máy 1 (agent giám sát pipeline) của lane toshi-densetsu-jp, thực thi kế hoạch sửa đã được chính bạn phê duyệt (trả lời 10:13) và chủ dự án đã duyệt + bổ sung quy tắc gpti2.

BỐI CẢNH: Tập ep02-walton (STT 2). B8Q lượt 5 rớt: 17 lạc (3.69% > 3%) + 5 lỗi hạ tầng (4 do file PNG mang đuôi .png nhưng thật là JPEG). final.mp4 466 cảnh OK. Chuẩn bị lượt 6 (CUỐI TUYỆT ĐỐI).

LÀM 3 VIỆC THEO THỨ TỰ. BACKUP mọi file trước khi sửa: copy vào E:/CLAUDE/YOUTUBE/h2dev/tools/_backup_giao_viec/ (hậu tố _truoc_sua_HHMMSS).

VIỆC 1 — Sửa vị trí 3 ảnh bằng chứng (evidence.json):
- File: E:/CLAUDE/YOUTUBE/h2dev/assets/toshi-densetsu-jp/ep02-walton/evidence.json (KHÔNG tồn tại img_meta.json — file đó chỉ được tạo khi ra đơn máy 2).
- Entry gồm: file, caption, source, url, license, accessed, chapter, note — vị trí ghim xác định bằng "chapter". Đọc pipeline/stock_cut.py để hiểu cách chapter được dùng trước khi sửa.
- Sửa chapter (và note nếu cần) cho: ev04_polygraph_administration.jpg (dời về đoạn chương 3 nói kiểm tra polygraph của Walton ~941-1000s), ev06_tono_iwate.png (đoạn nói 神隠し so với vụ Walton), ev08_fire_lookout_tower_generic.jpg (đoạn nói Gentry Tower / Mike Rogers). Ghi rõ chapter cũ → mới trong báo cáo.
- GIỮ NGUYÊN caption/source/url/license — chỉ sửa chapter/note nếu cần.

VIỆC 2 — Vẽ ảnh bù bằng GPTI2 (quy tắc mới chủ dự án):
- QUY TẮC: số ảnh cần vẽ < 20% tổng (~60/300) → ĐƯỢC phép gọi gpti2 TRỰC TIẾP (KHÔNG ra đơn máy 2 — máy 2 mất thời gian).
- a) Ước tính trước: cd /e/CLAUDE/YOUTUBE/h2dev && env -u PYTHONPATH py -3.13 -X utf8 pipeline/sinh_anh_canh.py --slug ep02-walton --theo-qc --uoc-tinh (đọc pipeline/sinh_anh_canh.py --help nếu lỗi; --slug có thể cần đường dẫn đầy đủ thư mục tập).
- b) Nếu số ảnh < 20%: chạy lại KHÔNG có --uoc-tinh (vẽ thật bằng gpti2, giữ --quality mặc định). Nếu ≥ 20%: DỪNG, báo số liệu, không tự ý vẽ.
- TUYỆT ĐỐI KHÔNG --chi-don (ra đơn máy 2). KHÔNG vẽ ảnh không cần thiết.

VIỆC 3 — Re-convert 4 file PNG giả thành PNG thật:
- 4 file: E:/CLAUDE/YOUTUBE/h2dev/assets/toshi-densetsu-jp/ep02-walton/img_ai/006.png, 021.png, 096.png, 124.png (đã xác nhận format=JPEG dù đuôi .png).
- Dùng Python + Pillow: đọc từng file rồi lưu lại đúng PNG (đè cùng path, backup trước). Giữ nguyên nội dung.

SAU KHI XONG CẢ 3 — GHI ĐƠN MỚI CHO DEEPSEEK (ghi ĐÈ toàn bộ E:/CLAUDE/YOUTUBE/h2dev/CLAUDE-DEEPSEEK.TXT):
- Header: 'DEEPSEEK → CLAUDE (đơn lúc HH:MM)'
- Mục 'ĐƠN CHO DEEPSEEK:' (ĐÚNG chữ này — monitor dùng làm tín hiệu) gồm:
  1) 3 việc đã xong (tóm tắt: evidence chapter cũ → mới; số ảnh gpti2 đã vẽ + tiền; 4 PNG đã re-convert)
  2) Lệnh cho DeepSeek: 'env -u PYTHONPATH py -3.13 -X utf8 tools/render_detach.py --slug ep02-walton --from B8' (lượt 6 CUỐI TUYỆT ĐỐI — ngưỡng: lạc ≤ 3% VÀ 0 lỗi hạ tầng, không hạ ngưỡng)
  3) Yêu cầu: tải lại img_ai (drive_handoff download-result) trước khi ghép; báo cáo kèm số đo thời gian khi xong.
- KHÔNG ghi cột H/F trang tính. KHÔNG thêm footer '(Trả lời tự động...' — đây là ĐƠN, không phải trả lời câu hỏi.

LUẬT CỨNG: không sửa script.txt/voice.mp3/voice.srt/khop_hinh.json/qc_facts.json/qc_canh.json/scenes.json; không --force-qc; không xoá dữ liệu; MỌI thay đổi phải backup trước.
Khi xong trả lời 1 dòng cuối: HOÀN TẤT 3 VIỆC + ĐÃ GHI ĐƠN (hoặc nêu rõ lỗi nếu dừng giữa chừng)."""


def main():
    cmd = ("claude -p " + shlex.quote(PROMPT) +
           " --model sonnet --output-format json --max-turns 45 "
           "--allowedTools 'Read,Write,Edit,Bash' --no-session-persistence")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    r = subprocess.run([BASH, "-lc", cmd], cwd=str(H2DEV), env=env,
                       capture_output=True, text=True, timeout=1800)
    print(r.stdout[-3000:])
    print("STDERR:", r.stderr[-1000:], file=sys.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()