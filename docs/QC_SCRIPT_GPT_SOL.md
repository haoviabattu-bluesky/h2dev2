# QC kịch bản độc lập — HẠ TẦNG DÙNG CHUNG (GPT-5.6-sol qua 9router)

Áp dụng cho **mọi lane** của dự án, cùng mô hình với `docs/QC_THUMBNAIL_GPT_SOL.md` (model thứ 2
khác hãng chấm lại thứ mà QC nội bộ cùng hãng với người viết có thể bỏ sót). Xây + verify thật
2026-09-18 trên `kenko-chiebukuro/ep01-tento-kossetsu` + `ep02-sarukopenia-sign` — cả 2 tập đã
**PASS B3Q/B3F nội bộ và ĐÃ GIAO HÀNG THẬT** trước khi lớp này phát hiện lỗi an toàn thật (xem mục
"Vì sao cần lớp này" bên dưới).

## Kiến trúc 2 lớp QC kịch bản (thứ tự chạy: B3Q → B3F → B3S → B4)

| Lớp | Bước | File | Model | Bắt lỗi gì |
|---|---|---|---|---|
| 1 (nội bộ, có sẵn) | B3Q | `pipeline/qc_script.py` | Gemini | Mâu thuẫn nhân vật/mốc thời gian, 伏線, cảnh trùng, SỐ HỌC, bám gốc đối thủ 70/30 |
| 1 (nội bộ, có sẵn) | B3F | `pipeline/qc_facts.py` | **Không LLM — regex thuần** | Chi tiết BỊA (năm/địa danh/tổ chức không có trong `series_ctx.txt`), thiếu trích dẫn nguồn |
| 2 (MỚI, độc lập) | **B3S** | `pipeline/qc_script_sol.py` | **GPT-5.6-sol** (9router, khác hãng hoàn toàn với Gemini/Claude đang viết+B3Q) | 6 lăng kính TỔNG QUÁT (không khoá cứng 1 chủ đề): chuẩn tham chiếu đúng đối tượng, an toàn vật lý, nhân quả/chẩn đoán quá mức, triệu chứng khẩn cấp, ngôn ngữ tuyệt đối hoá, logic-ngữ pháp |

Lớp 1 rẻ, nhanh, bắt lỗi ĐỊNH LƯỢNG/CƠ HỌC. Lớp 2 đắt/chậm hơn nhưng là lớp DUY NHẤT bắt được lỗi
KHÁI NIỆM/AN TOÀN — **không thay thế lớp 1**, luôn chạy SAU khi lớp 1 đã sạch.

## Vì sao cần lớp 2 (bằng chứng thật, không phải phòng xa)

Cả `ep01` và `ep02` (lane `kenko-chiebukuro`) đều đã PASS B3Q + B3F và **đã giao hàng thật** ở
`CHANEL\kenko-chiebukuro\` trước khi test B3S. Khi GPT-5.6-sol đọc lại (model khác hãng, không liên
quan gì tới chuỗi Gemini viết PASS2 → Gemini QC B3Q):
- `ep02`: dùng nhầm chuẩn châu Âu EWGSOP2 cho video hướng người Nhật (đáng lẽ AWGS 2019), và nghiêm
  trọng hơn — 1 câu chuyện minh hoạ mô tả triệu chứng **ĐỘT NGỘT** đúng khuôn dấu hiệu đột quỵ/TIA
  nhưng bị kể như suy giảm do tuổi già bình thường, mâu thuẫn thẳng với đoạn cảnh báo đột quỵ mà
  chính kịch bản đó đã có.
- `ep01`: round 1 chấm thẳng REMAKE — cảnh báo tương tác thuốc quá nhẹ/sai phạm vi, hướng dẫn hành
  động thiếu điều kiện an toàn, tiêu đề hứa hẹn vượt xa nội dung thật.

**Lý do gốc rễ:** QC cùng hãng với người viết (Gemini QC văn Gemini/Claude viết) = kiểm tra bằng
ĐÚNG "họ suy luận" đã tạo ra nội dung đó → không thấy được điểm mù của chính nó. Lỗi có cấu trúc,
lặp lại ở cả 2 tập độc lập — không phải xui rủi.

## Tool: `pipeline/qc_script_sol.py`

```
py -3.13 qc_script_sol.py --script script.txt --title-file listting.txt --profile <lane-id>
py -3.13 qc_script_sol.py --script script.txt --title "..." --out qc_sol_report.txt
```
(`--title-file`: dòng ĐẦU của file là tiêu đề, đúng quy ước `listting.txt` của dự án.)

Chấm theo 6 lăng kính ở trên, ép đọc kỹ 1 lượt liệt kê HẾT (không giữ lại lỗi "chờ vòng sau") → trả
**PASS / FIX / REMAKE** (exit code 0/2/3, dùng được trong script khác). Output đầy đủ in stdout,
`--out file.txt` lưu lại.

## REMAKE KHÔNG có nghĩa "viết lại từ đầu" — 4 chiến lược sửa nhẹ tay

Xem đầy đủ ở memory dự án `remake-khong-phai-viet-lai` — tóm tắt: REMAKE báo hiệu lỗi nằm ở khung
sườn (luận đề/thứ hạng/cấu trúc an toàn/phạm vi cảnh báo), không phải câu chữ, nhưng vẫn sửa được
bằng Edit tại chỗ theo đúng 4 chiến lược tương ứng, đo thật đã đưa `ep01` từ REMAKE (4 vòng liền) về
FIX:
1. **Sai luận đề** (tiêu đề hứa hẹn vượt nội dung thật) → làm mềm câu chữ tiêu đề/mở bài, GIỮ NGUYÊN
   chủ đề video.
2. **Sai thứ hạng** (đếm ngược ngụ ý đã so sánh khoa học) → GIỮ NGUYÊN định dạng nếu là mô-típ kênh,
   chỉ thêm 1 câu đính chính "thứ tự chỉ là cách trình bày".
3. **Thiếu cấu trúc an toàn** → Claude tự viết thẳng từ kiến thức an toàn công cộng chuẩn (không cần
   tra cứu riêng như số liệu nghiên cứu); khuyến nghị không cách nào viết an toàn được thì cắt bỏ.
4. **Cảnh báo sai phạm vi** → nếu mối nguy CÓ THẬT thì sửa lại đúng phạm vi (không loại bỏ); chỉ loại
   bỏ khi cảnh báo không có căn cứ thật.

## Chính sách dừng vòng lặp — KHÔNG đợi PASS tuyệt đối

B3S áp chuẩn học thuật nghiêm ngặt nên **không bao giờ tự chấm PASS tuyệt đối** cho văn phổ thông
(đo thật `ep01`: sau khi hết lỗi an toàn, verdict vẫn dừng ở FIX 3 vòng liền, cùng loại góp ý "có thể
hedging thêm"). Đuổi theo PASS là vòng lặp vô ích — cùng nguyên tắc chung `cong-llm-phai-dat-duoc`
(tách SAI khỏi CHƯA HAY, chỉ chặn ở cái sai) đã có trong memory dự án.

## Nối vào pipeline: bước **B3S** trong `make_video.py`

`Job.b3s_sol()` — chạy sau B3F, trước B4 (giọng đọc), CHỈ khi lane khai `profile.script.sol_qc =
true`:
1. Chạy B3S đúng 1 lần trên bản đã qua B3Q/B3F.
2. **PASS/FIX** → gọi `claude_p_bridge.ask()` (headless `claude -p`, timeout 1500s) sửa **đúng 1
   lần** nếu FIX, chấm lại **đúng 1 lần**, rồi LUÔN chạy tiếp B4 tự động — không chặn.
3. **REMAKE** (kể cả sau khi đã thử sửa) → **CHẶN HẲN pipeline trước B4** (giống B3F chặn khi thiếu
   tư liệu nguồn). Cần Claude đọc tay quyết định lại phạm vi/tiêu đề, máy không tự quyết được.

**Vì sao KHÔNG lặp headless nhiều lần tự động**: mỗi vòng sửa tay cần ĐỌC báo cáo rồi viết brief
riêng theo đúng lỗi còn lại — đó là phần PHÁN ĐOÁN mà máy chạy mù không làm được; `claude -p`
viết-lại-toàn-bộ nhiều lần còn dễ tự sinh lỗi mới (đã dính thật: dấu phẩy cắt cụm động từ ghép, lỗi
sai nghĩa `リスクを支える`, từ bịa `鼓道`). Máy tự động chỉ nên thử 1 lần, phần còn lại nhường cho
Claude đọc tay khi pipeline báo dừng — **kể cả sau khi máy báo PASS/FIX, Claude vẫn nên đọc lướt lại
báo cáo 1 lần khi rảnh**, vì máy chạy mù vẫn có thể tự sinh lỗi mới không bị bắt lại (bằng chứng: lỗi
`鼓道` chỉ bị phát hiện nhờ Claude đọc tay sau khi B3S đã báo FIX xong).

## Nối vào flow B (não Claude, `brain_channel.make_video_one`) — thêm 2026-09-18, lane satori

Cùng công tắc `profile.script.sol_qc`, nhưng chính sách do anh chốt gọn hơn lane E (`check_b3s()`):

```
B3Q gemini (≤3 vòng sửa tại chỗ)  ← tầng 2 Claude chấm TẮT khi có sol (cùng model chấm nhau = vô nghĩa)
→ B3S sol chấm (logs/B3S_sol_001.txt)
   PASS   → assets
   FIX    → Claude (claude -p, pha script) sửa tại chỗ CHỈ mục ghi SAI → sol chấm lại 1 lần
            (logs/B3S_sol_002.txt) → PASS/FIX-nhẹ đều qua; REMAKE → nhánh dưới
   REMAKE → Claude kiểm từng lỗi sol nêu, xoá/sửa cái SAI thật, TỰ chấm lại, ghi
            logs/B3S_claude_verdict.txt dòng đầu `PASS` (lỗi nhẹ vẫn PASS) hoặc
            `SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC` → dừng + ESCALATION_REPORT.md
```
Sol lỗi hạ tầng → đi tiếp nhưng log ghi rõ "KHÔNG phải đã soi". Lens theo `script_qc.lens`
(`story` cho lane kể chuyện — 6 lăng kính: mâu thuẫn dữ kiện · số học & tiền không quy đổi 1:10 won ·
dấu vết Hàn · logic hành vi · tuyệt đối hoá · nhịp đọc; `medical` = mặc định cũ). Test:
`pipeline/tests/test_brain_b3s.py` (mock sol + mock Claude, 7 case).

## Bật cho lane nào — khai trong `profiles/profiles/<id>.json`

```json
"script": {
  "sol_qc": true
}
```
Không khai → `b3s_sol()` tự bỏ qua êm, không phải lỗi. Chỉ bật cho ngách có rủi ro an toàn thật (y
tế, tài chính, pháp lý...) — B3S tốn thêm thời gian/tiền, không cần cho mọi lane.

Tuỳ chọn thêm `profile.script_qc.domain_focus` (đoạn text CHÈN vào cuối prompt của
`qc_script_sol.py`, mỗi ngách rủi ro khác nhau — mirror đúng field `thumbnail_qc.claim_focus` đã có
cho QC thumbnail). Không khai thì dùng `DEFAULT_DOMAIN_FOCUS` (rủi ro sức khoẻ người già) trong
`qc_script_sol.py`.

Ví dụ đã bật thật: `profiles/profiles/kenko-chiebukuro.json` → `script.sol_qc = true`.

## Bẫy đã dính thật khi chạy headless (`claude -p`) nhiều lần liên tiếp

Gọi `claude_p_bridge.ask()` nhiều lần liên tiếp trong cùng phiên (vd đang test tay nhiều vòng) khiến
mỗi lần MỞ THÊM 1 tiến trình `claude.exe` dùng CHUNG 1 tài khoản OAuth Max với các tab Claude Code
khác đang mở song song — càng gọi liên tiếp càng chậm dần rồi timeout (đo thật: 462s → timeout 600s
→ 896s → timeout 900s+). Không phải lỗi nội dung/code. Cách xử lý:
- Khi đang có Claude tương tác sẵn (không phải chạy tự động không người): **để Claude tự sửa trực
  tiếp bằng Edit thay vì gọi thêm `claude -p`** — nhanh hơn hẳn, không tranh chấp.
- Khi chạy tự động không người (`b3s_sol()` trong pipeline): chỉ gọi headless **đúng 1 lần** (đã
  thiết kế sẵn ở trên), không lặp nhiều lần liên tiếp.
- Nếu vẫn cần gọi nhiều lần headless (vd test tay), chạy TUẦN TỰ (không song song 2 lệnh cùng lúc) và
  chấp nhận timeout tăng dần — không phải máy hỏng.

## Ví dụ đã verify thật

`kenko-chiebukuro/ep01-tento-kossetsu` + `ep02-sarukopenia-sign` (2026-09-18) — chi tiết quá trình
sửa từng vòng xem lịch sử chat, kết quả cuối: cả 2 tập verdict B3S = FIX (không REMAKE), sẵn sàng cho
B4. `docs/SOP_LANE_E.md` §4b giữ phần khai báo riêng của lane này (cờ `sol_qc`, chưa khai
`domain_focus` riêng).
