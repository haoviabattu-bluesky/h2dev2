# PROMPT BÀN GIAO — mang kiến trúc "Claude làm bộ não" sang dự án khác

Copy nguyên khối dưới đây dán vào chat của dự án khác. Hai bản: **ngắn** (dùng khi dự án kia chỉ cần
áp dụng) và **đầy đủ** (khi dựng tool mới từ đầu).

---

## BẢN NGẮN — dán là chạy

```
Dự án này cần một tool mà phần "nghĩ/viết" do chính Claude làm (gọi `claude -p` headless từ code),
còn phần cơ học do Python lo. Trước khi code, ĐỌC SKILL:

    C:\Users\admin\.claude\skills\claude_headless_agent_tool.md

Skill đó có 12 pitfall đã dính thật + checklist. Ba điều quan trọng nhất, đừng bỏ qua:

1. PHÂN VAI (§4 — pitfall đắt nhất): Claude VIẾT, MÁY ĐO và NẮN.
   Claude KHÔNG đếm được ký tự/số lượng khi đang sinh chữ. Mọi ràng buộc ĐO ĐƯỢC (độ dài, tỉ lệ,
   mật độ) phải có (a) script đo chạy được, (b) script nắn bằng máy, (c) LỆNH GỌI NẰM TRONG PROMPT.
   Đã đo thật: dặn kỹ 4 vòng đều thất bại (nháp ra gấp 2-2,5 lần mục tiêu, Claude tự cắt 26-35 phút
   rồi cạn ngân sách); giao cho máy thì xong trong 2,4-4,7 phút, 0 quota.

2. Công cụ máy phải ở TRONG luồng của model, không phải tầng sau. Đã dính: viết xong script nắn
   nhưng đặt nó chạy sau khi bộ não kết thúc ⇒ bộ não vẫn tự vật lộn, máy không được gọi lần nào.

3. Ràng buộc số lượng nào buộc model tự giữ → đổi sang thứ ĐẾM ĐƯỢC (dòng đánh số) rồi bắt nó chạy
   `grep -c` xác nhận. "Viết 64 đoạn" → ra 104 đoạn; "viết dàn ý 64 dòng rồi grep -c" → đúng 64.

Code tham khảo chạy thật: E:\CLAUDE\YOUTUBE\h2dev\pipeline\{brain_steps.py, gate_check.py,
fix_gate.py, brain_channel.py} và runbook E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_CLONE_BRAIN.md
```

---

## BẢN ĐẦY ĐỦ — khi dựng tool mới từ đầu

```
Tôi muốn dựng một tool kiểu "Claude làm bộ não": code Python điều phối, còn khâu sáng tạo/viết thì
spawn `claude -p` (headless CLI) để chính Claude làm. Máy đích đã cài + đăng nhập Claude Code nên
KHÔNG cần ANTHROPIC_API_KEY (ăn quota gói MAX/Pro, không phải hoá đơn thẻ).

BẮT BUỘC đọc trước: C:\Users\admin\.claude\skills\claude_headless_agent_tool.md
(12 pitfall đã dính thật + checklist + code mẫu). Áp dụng đủ, đặc biệt:

A. KỸ THUẬT GỌI
   - Đề bài dài PHẢI qua STDIN, không qua argv (qua argv thì Claude báo "không có yêu cầu").
   - `--append-system-prompt` cấm hỏi lại + đề bài cũng cấm hỏi lại (2 lớp) — headless không có ai trả lời.
   - `--permission-mode bypassPermissions` nếu Claude cần tự chạy script/QC. `acceptEdits` vẫn HỎI
     khi gọi Bash ⇒ chạy nền sẽ đứng im vô hạn.
   - GHIM `--model` (không ghim thì chạy model mặc định của CLI; `/model` của phiên cha KHÔNG truyền xuống).
   - Verify bằng FILE TỒN TẠI THẬT, không tin exit code.
   - Mọi đường dẫn nhúng trong prompt phải TUYỆT ĐỐI (Path(__file__).with_name(...)).

B. PHÂN VAI (quan trọng nhất)
   - Liệt kê ràng buộc của sản phẩm, chia làm 2 nhóm:
       * ĐO ĐƯỢC bằng code (độ dài, số lượng, tỉ lệ, mật độ) → MÁY lo.
       * PHẢI HIỂU mới làm được (logic, mạch truyện, đúng/sai nội dung) → CLAUDE lo.
   - Với nhóm ĐO ĐƯỢC, viết 2 script: `<x>_check.py` (đo, in số, exit 0/1) và `<x>_fix.py` (nắn).
   - NHÚNG LỆNH GỌI 2 SCRIPT ĐÓ VÀO PROMPT, kèm câu: "việc của bạn là viết cho hay, việc đếm là của
     máy — đừng tranh việc của máy, TUYỆT ĐỐI không tự viết lại để chỉnh số".

C. KHI NHỜ LLM RẺ SỬA CƠ HỌC
   - Luôn có CHỐT BẤT BIẾN: bỏ đúng những ký tự được phép đổi, phần còn lại phải giống hệt bản cũ;
     lệch một chữ là BỎ, giữ bản cũ (chặn LLM lén viết lại nội dung).
   - Ngưỡng hai đầu thì nhắm GIỮA DẢI, điều kiện nhận phải kiểm cả 2 chiều (sửa quá tay là thủng
     trần bên kia).
   - Chỉ nhận bản mới khi SỐ LỖI GIẢM; hoà thì lấy bản gần mục tiêu hơn.

D. CỔNG / NGƯỠNG
   - Ghi ngưỡng bằng SỐ + CẢ HAI ĐẦU DẢI vào prompt, kèm câu "đây là TOÀN BỘ cổng chặn, đừng đọc
     source dò thêm" (không ghi thì model đi đọc source cổng QC để đoán luật, tốn 4-5 phút/lượt).
   - Nêu rõ thứ nào KHÔNG phải cổng chặn.

E. ĐO THỜI GIAN NGAY TỪ ĐẦU
   - Orchestrator in `⏱ x.x phút` mỗi bước + tổng; driver in mốc `+phút` trước mọi dòng callback.
   - Không có đồng hồ thì không chẩn đoán được: 6,7 phút im lặng có thể là "đang sinh 16.000 ký tự"
     (trần cứng) hoặc "đang sleep vô ích" (cắt được ngay) — nhìn log không có giờ thì giống hệt nhau.

F. VERIFY
   - Test cả ca ĐẠT lẫn ca RỚT. (Đã dính: hàm cổng trả về tuple `(danh_sách_lỗi, số_đo)` — tuple 2
     phần tử LUÔN truthy nên `if loi:` chặn cả sản phẩm ĐẠT SẠCH; verify trước đó chỉ dùng 2 ca RỚT
     nên không lộ.)
   - Đừng sửa theo phỏng đoán: nghi provider ảnh viết sai chữ Hán → gen thử 6 ảnh (360đ) thì hoá ra
     viết ĐÚNG hoàn toàn. Sửa mù đã suýt phá mất mấy cảnh đắt giá nhất.

Code tham khảo chạy thật (đọc được luôn):
   E:\CLAUDE\YOUTUBE\h2dev\pipeline\brain_steps.py     — dựng prompt + spawn claude -p
   E:\CLAUDE\YOUTUBE\h2dev\pipeline\brain_channel.py   — orchestrator + hàng rào + vòng nắn
   E:\CLAUDE\YOUTUBE\h2dev\pipeline\gate_check.py      — cổng ĐO (mẫu ngắn, 60 dòng)
   E:\CLAUDE\YOUTUBE\h2dev\pipeline\fix_gate.py        — cổng NẮN + chốt bất biến
   E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_CLONE_BRAIN.md     — runbook + bảng 13 lỗi đã vá + số đo thật
```

---

## Dự án kia cần đổi gì cho khớp ngách của họ

| Thứ | Ở đây (video YouTube) | Dự án khác đổi thành |
|---|---|---|
| Ràng buộc ĐO ĐƯỢC | độ dài script, dấu phẩy/câu, nhịp thở, tỉ lệ hội thoại | bất kỳ số nào kiểm được bằng code |
| `gate_check.py` | đọc ngưỡng từ `profile.script.gate` | đọc từ config của họ |
| `fix_gate.py` | nén khúc · thêm/bớt nhịp · hạ hội thoại | 1-3 phép biến đổi cơ học của họ |
| Thứ ĐẾM ĐƯỢC | dàn ý 64 dòng đánh số | mục lục/danh sách/bảng có số thứ tự |
| Cổng NỘI DUNG | `qc_script.py` (logic + sao chép 70/30) | tiêu chí đúng/sai của họ |
