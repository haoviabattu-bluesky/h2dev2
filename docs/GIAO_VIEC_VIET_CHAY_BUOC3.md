# GIAO VIỆC — viết `pipeline/chay_buoc3.py` (bộ điều phối bước 3, lane `satori-jp-obaa`)

File này tự chứa. Đọc hết rồi làm theo đúng thứ tự, không cần hỏi ai, không cần đọc lịch sử chat.
Mọi lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev\pipeline`, luôn dùng `py -3.13`.

## 0. BỨC TRANH — vì sao có việc này

Dự án chia video thành 3 bước: **bước 1** (một AI khác, viết kịch bản + prompt ảnh, không đụng
tới), **bước 2** (người vẽ ảnh qua Google Flow, không đụng tới), **bước 3** — việc của bạn — nhận
ảnh đã vẽ, ghép thành video, chấm chất lượng, giao hàng, ghi kết quả vào trang tính.

Bước 3 trước đây do một agent khác (đọc file text, tự gõ lệnh) đảm nhiệm, nhưng hay **hiểu sai chỉ
thị phức tạp** (đo thật: agent đó trả lời RỖNG 2/2 lần với đúng dạng việc "đọc log rồi viết báo cáo
có cấu trúc"). Việc của bạn là viết một **script tất định** thay thế nó: mọi quyết định (chạy tiếp
hay dừng, thử lại mấy lần) nằm CỨNG trong code, không dựa vào một AI "hiểu" chỉ thị rồi tự quyết.
Sau khi có script, một script khác/cron sẽ tự gọi nó định kỳ — bạn không cần lo phần đó.

## 1. ⛔ CẤM TUYỆT ĐỐI

1. **Không đụng lane nào khác** ngoài `satori-jp-obaa`. Không sửa code chung (`llm_client.py`,
   `qc_visual.py`, `qc_character.py`...) theo cách chỉ đúng cho lane này — nếu phải sửa file dùng
   chung, sửa theo hướng ĐỌC TỪ PROFILE, cấm viết `if profile_id == "satori-jp-obaa"` bất cứ đâu.
2. **Không tự vẽ ảnh khi thiếu** (không gọi `gen_images.py`/`gpti2_gen.py`/`sinh_anh_canh.py` để
   "vẽ bù" khi đếm thấy thiếu ảnh). Thiếu ảnh = DỪNG, báo cáo, chờ máy 2 vẽ thêm — vẽ bù là đốt
   ~8.000đ cho đúng thứ máy 2 đang vẽ miễn phí.
3. **Không xoá dòng/cột/dữ liệu trong Google Sheet.** Chỉ được ghi đúng ô đã quy định (mục 5).
4. **Không sửa `script.txt`, `voice.mp3`, `voice.srt`, `img_doan.txt`, `characters.json`** — đó là
   sản phẩm bước 1 đã nghiệm thu. Thấy sai thì ghi vào báo cáo, không tự sửa.
5. **Không `taskkill`/kill Chrome theo tên.** Bước 3 không cần Chrome, không nên đụng tới.
6. **Không đăng `review-vi.mp4`/`final_vi.mp4`** — đó là bản duyệt tiếng Việt, không phải bản đăng.
7. **Không thêm cờ `--burn-sub`** khi gọi `render_engine.py`.

## 2. VIỆC 0 — SỬA BUG THẬT đã tìm thấy (làm TRƯỚC, mọi việc sau phụ thuộc vào đây)

**Triệu chứng:** `ghi_cot_video.py::thu_muc_tap()` và `quet_dong_can_anh.py::slug_tu_dia()` đều tìm
thư mục tập bằng glob cứng `ep{stt:02d}-*` trong `slug_dir` của lane. Đúng cho Lane A
(`toshi-densetsu-jp/ep02-walton`), nhưng **lane satori đặt tên thư mục làm việc kiểu
`simbot2-{stt:02d}-<videoID>`**, không đổi tên. Trong `assets/satori_jp/` còn sót 8 thư mục nháp
cũ từ series bỏ dở (`ep06-nenkin-kai`, `ep08-nanajuu`, `ep09-oyakoukou`, `ep10-saigo`,
`ep11-saikon`, `ep12-yokin`, `ep13-ginkou`, `ep14-kaimono`) — vô tình khớp đúng glob đó, khiến hai
hàm trên trả về **thư mục SAI** cho STT 6, 8, 9, 10, 11, 12, 13, 14. Verify: `py -3.13 -c` gọi
`ghi_cot_video.lane_theo_tab('Lopezzapa68')` rồi `thu_muc_tap(prof, 11)` → trả về `ep11-saikon`
(sai) thay vì thư mục thật `simbot2-11-DXXwIxhcfF0`.

**Vì sao chưa gây hậu quả tới giờ:** thư mục đích tương ứng dưới `CHANEL\Lopezzapa68\` không tồn
tại nên hai hàm tự dừng an toàn ("chưa có thư mục giao hàng"), không ghi sai. Nhưng vì vậy suy ra
**`ghi_cot_video.py` CHƯA TỪNG chạy thành công cho lane này** — cột G của tập 04/06/07 hiện tại
được ghi tay, không qua tool.

**Cách sửa (bắt buộc, không hardcode theo lane):** thêm field mới vào profile, đọc nó ở cả hai hàm:

- Thêm vào `profiles/profiles/satori-jp-obaa.json`: `"folder_pattern": "simbot2-{nn:02d}-*"`.
- Thêm vào `profiles/profiles/toshi-densetsu-jp.json` và `irogatatarukioku.json` (nếu chưa có):
  `"folder_pattern": "ep{nn:02d}-*"` (giữ hành vi cũ, không đổi gì cho 2 lane đó).
- Sửa `ghi_cot_video.thu_muc_tap(prof, stt)`: thay dòng
  `m = sorted(p for p in goc.glob(f"ep{stt:02d}-*") if p.is_dir())`
  bằng đọc `mau = prof.get("folder_pattern", "ep{nn:02d}-*")` rồi
  `m = sorted(p for p in goc.glob(mau.format(nn=stt)) if p.is_dir())`.
- Sửa tương tự `quet_dong_can_anh.slug_tu_dia(stt, tab)` — hàm này đang gọi `thu_muc_lane(tab)` trả
  về đường dẫn thư mục, cần đọc thêm field `folder_pattern` từ CHÍNH profile mà `thu_muc_lane` đã
  tìm ra (sửa `thu_muc_lane` trả về cả `prof` thay vì chỉ đường dẫn, hoặc load lại profile theo tab).
- **Kiểm bằng chính lệnh đã dùng để phát hiện bug**, phải đổi kết quả từ sai sang đúng:
  ```
  py -3.13 -c "import sys; sys.path.insert(0, r'E:\CLAUDE\YOUTUBE\h2dev\pipeline'); import ghi_cot_video as g; p=g.lane_theo_tab('Lopezzapa68'); print(g.thu_muc_tap(p, 11))"
  ```
  Phải in ra `...\assets\satori_jp\simbot2-11-DXXwIxhcfF0`, KHÔNG phải `ep11-saikon`.
- Chạy thêm cho STT 6: phải in ra `simbot2-06-sYRr33eHYSM`, không phải `ep06-nenkin-kai`.
- **Không xoá 8 thư mục nháp cũ** — không phải việc của bạn, để nguyên đó.

## 3. Tạo file `pipeline/chay_buoc3.py`

### 3.1 Chữ ký dòng lệnh

```
py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong <STT>
py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong <STT> --thu     (chỉ kiểm tra, không chạy gì)
```

Chỉ nhận **một STT mỗi lần chạy** (đúng luật dự án: không tự chạy dải/tất cả khi không được chỉ
định — xem `docs/DANH_BA_LANE.md`). Bên gọi nó (cron/script khác) muốn làm nhiều dòng thì tự lặp.

### 3.2 Các bước, ĐÚNG THỨ TỰ, tái dùng tool có sẵn — KHÔNG viết lại logic đã có

Với mỗi bước, script phải **in ra** tên bước + kết quả (đạt/lỗi) + thời gian bước đó chạy hết bao
lâu, giống định dạng `render_engine.py` đang làm (nó đã có sẵn thói quen này — bắt chước, đừng bịa
định dạng khác). Toàn bộ đường dẫn tra từ profile, KHÔNG gõ cứng số Lopezzapa68/satori-jp-obaa vào
trong logic của một bước (chỉ dùng làm mặc định của `--tab`).

```
BƯỚC A — Xác định dòng có sẵn sàng không.
  Đọc trang tính (dùng chung cơ chế đọc của quet_dong_can_anh.py, KHÔNG tự viết lại việc gọi
  Google Sheets API). Điều kiện sẵn sàng: cột STATUS-IMG bắt đầu bằng "Img done" (không phân biệt
  hoa/thường) VÀ cột VIDEO còn trống. Không thoả điều kiện → DỪNG NGAY, in rõ lý do, KHÔNG coi là
  lỗi (exit 0) — đây là trạng thái bình thường khi máy 2 chưa vẽ xong.

BƯỚC B — Tìm thư mục tập trên đĩa.
  Dùng ĐÚNG cơ chế đã sửa ở VIỆC 0 (glob theo `folder_pattern` của profile). KHÔNG glob cứng
  "ep{stt:02d}-*" trong file mới này — gọi hàm đã sửa trong `ghi_cot_video.py`/`quet_dong_can_anh.py`
  qua import, đừng chép lại.
  Không tìm thấy đúng 1 thư mục (0 hoặc >1) → DỪNG, báo lỗi rõ ràng, KHÔNG đoán.

BƯỚC C — Tải ảnh về (nếu chưa có đủ).
  py -3.13 drive_handoff.py download-result <slug> "<thư mục tập>\img"
  Đây là lệnh có sẵn thu_lai()/retry — KHÔNG tự viết retry chồng lên, chỉ chạy 1 lần, nếu lỗi thì
  coi là lỗi hạ tầng (xem mục 3.4).

BƯỚC D — Đếm ảnh đủ chưa (RÀO CỨNG, KHÔNG ĐƯỢC BỎ QUA).
  Đếm số .png trong <thư mục tập>\img, so với số dòng khác rỗng trong img_prompts.txt.
  Thiếu → DỪNG HẲN (không retry, không tự vẽ bù — xem CẤM #2), viết báo cáo nói rõ thiếu bao nhiêu
  tấm, KHÔNG đi tiếp các bước sau.

BƯỚC E — Sinh `img_doan.txt` nếu chưa có.
  Chỉ chạy khi file <thư mục tập>\img_doan.txt CHƯA TỒN TẠI (tool tự phát hiện điều này, ĐỪNG
  duplicate logic — cứ gọi thẳng, nó tự bỏ qua nếu đã có):
  py -3.13 sinh_img_doan.py --slug "<thư mục tập>"
  Lỗi ở bước này → lỗi hạ tầng (xem 3.4), KHÔNG dừng hẳn ngay, cho retry.

BƯỚC F — Ghép video.
  py -3.13 render_engine.py --slug "<thư mục tập>" --profile satori-jp-obaa --quality low --workers 8
  Đây là lệnh DUY NHẤT có chính sách retry ĐẶC BIỆT — xem 3.4 mục "rớt cổng nội dung".

BƯỚC G — Giao hàng.
  py -3.13 giao_hang.py --slug "<thư mục tập>" --profile satori-jp-obaa
  (không cần truyền --ep/--ten, tool tự suy ra từ tên thư mục + trang tính theo docstring của nó
  — đọc docstring trước khi giả định tham số nào bắt buộc).

BƯỚC H — Ghi cột VIDEO (G).
  py -3.13 ghi_cot_video.py --tab <tab> --dong <STT>
  Tool này TỰ kiểm tra đã giao đủ 3 file chưa trước khi ghi — KHÔNG tự kiểm tra lại việc đó trong
  chay_buoc3.py (tránh 2 nơi cùng một luật, lệch nhau sau này). Nếu nó thoát khác 0 → coi là lỗi
  hạ tầng/cần người xem, KHÔNG thử ghi bằng cách khác (vd gọi thẳng Google Sheets API) để né rào.
```

### 3.3 KHÔNG ĐƯỢC làm khi viết bước trên

- KHÔNG tự gọi Google Sheets API trực tiếp ở bất cứ đâu trong file mới — mọi thao tác đọc/ghi
  trang tính đều đi qua `quet_dong_can_anh.py`/`ghi_cot_video.py` đã có rào chắn sẵn.
- KHÔNG parse output in ra màn hình của các tool trên bằng regex để lấy dữ liệu quan trọng (dễ vỡ
  khi tool đổi câu chữ) — ưu tiên `import <tool> as x; x.ham_can_dung(...)` khi tool có hàm gọi
  được, chỉ dùng `subprocess.run` + đọc mã thoát khi tool đó CHỦ Ý là chạy độc lập (như
  `render_engine.py`, `giao_hang.py` — không có hàm nào để import gọi thẳng).

### 3.4 Chính sách retry/dừng — ĐÚNG BA LOẠI, KHÔNG GỘP CHUNG

| Loại | Ví dụ | Xử lý |
|---|---|---|
| **A. Lỗi hạ tầng tạm thời** (mạng, API 503/timeout, tiến trình con thoát bất thường không rõ lý do nội dung) | `drive_handoff.py`/`sinh_img_doan.py` thoát khác 0, thông báo không khớp bất kỳ mẫu ở loại B/C | Thử lại **tối đa 3 lần**, nghỉ giữa các lần **10s → 30s → 90s**. Hết 3 lần vẫn lỗi → coi như loại C (dừng hẳn, báo cáo). |
| **B. Rớt cổng NỘI DUNG (chỉ áp dụng cho BƯỚC F)** | `render_engine.py` thoát khác 0 vì B4Q/B5Q/B8Q không đạt (không phải vì thiếu file) | Chạy lại `render_engine.py` (nó tự resume, bỏ qua bước đã xong) **tối đa 2 lần thêm** (tổng 3 lần). Vẫn rớt sau lần 3 → dừng hẳn, báo cáo kèm chi tiết bước nào rớt và bằng chứng (trích log). |
| **C. Lỗi cần người quyết — KHÔNG BAO GIỜ TỰ RETRY** | Thiếu ảnh (BƯỚC D) · tìm 0 hoặc >1 thư mục (BƯỚC B) · `ghi_cot_video.py` báo "chưa có thư mục giao hàng"/"đã có giá trị" | Dừng ngay lập tức, viết báo cáo, KHÔNG thử lại dưới bất kỳ hình thức nào. |

Với mọi lần retry (loại A, B): PHẢI in ra log "thử lại lần N/M sau Xs" — báo cáo cuối phải liệt kê
đủ số lần thử, không chỉ kết quả cuối.

## 4. Báo cáo VẬN HÀNH — mỗi lần chạy ghi MỘT file, KHÔNG đè lên lần chạy khác

Đường dẫn: `E:\CLAUDE\YOUTUBE\h2dev\BAO_CAO_BUOC3\<tab>_dong<STT>_<yyyymmdd_HHMM>.txt`
(tạo thư mục `BAO_CAO_BUOC3\` nếu chưa có). Giữ lịch sử — KHÔNG ghi đè file cũ, mỗi lần chạy một
file mới có mốc giờ trong tên, để còn tra lại được lần chạy trước nếu có tranh cãi.

Mẫu bắt buộc (điền số thật, không được để trống mục nào — thiếu số liệu thì ghi rõ "không đo được"
và lý do, không được bỏ trống im lặng):

```
================================================================================
BÁO CÁO BƯỚC 3 — chay_buoc3.py
Tab: <tab> · STT: <n> · Slug: <tên thư mục> · Bắt đầu: <hh:mm dd/mm> · Kết thúc: <hh:mm> (X phút)
Kết quả: ĐẠT / DỪNG Ở BƯỚC <tên bước> / LỖI HẠ TẦNG SAU 3 LẦN THỬ
================================================================================

MỤC 1 — TỪNG BƯỚC ĐÃ CHẠY (thứ tự thật, không phải danh sách lý thuyết)
  A. <tên bước>: OK/LỖI/BỎ QUA (X,X phút) — <1 dòng kết quả cụ thể, có số>
  ... (liệt kê đủ, kể cả bước bị bỏ qua vì đã có sẵn)

MỤC 2 — SỐ LIỆU ĐO ĐƯỢC
  - Số ảnh: <n>/<m prompt>
  - B8Q: <điểm/tỉ lệ nếu có>
  - Số lần thử lại: bước <X> thử N/M lần
  - Thư mục giao hàng: <đường dẫn>

MỤC 3 — DỪNG Ở ĐÂU / CẦN GÌ (chỉ có nếu không ĐẠT)
  - Bước dừng: <tên>
  - Lý do (trích nguyên văn thông báo lỗi, không diễn giải lại)
  - Đề xuất: chạy lại được không, hay cần người quyết việc gì

MỤC 4 — ĐƯỜNG DẪN GIAO HÀNG (chỉ có nếu ĐẠT)
  <đường dẫn CHANEL\...>
```

**Ghi cột H** (KHÔNG đè nội dung cũ nếu có, nối thêm bằng " | "):
```
py -3.13 ghi_don_buoc3.py ...   ← CHƯA CÓ SẴN CHO LANE NÀY, dùng tạm cách sau:
```
Vì lane satori CHƯA có tool ghi cột H riêng (khác Lane A đã có `ghi_don_buoc3.py`), file mới này
PHẢI tự ghi cột H bằng MCP `gsheets` với ĐÚNG một dòng nội dung:
`chay_buoc3.py chạy <hh:mm>: <ĐẠT/DỪNG> — xem <đường dẫn file báo cáo>`
— và áp đúng 2 rào đã có trong `ghi_cot_video.py` (đọc lại tiêu đề cột thật trước khi ghi, không
ghi đè ô đã có nội dung KHÁC của người khác — nối vào sau bằng " | " thay vì xoá). Copy nguyên rào
đó từ `ghi_cot_video.py`, đừng viết version yếu hơn.

## 5. Test BẮT BUỘC trước khi báo hoàn thành — KHÔNG được bỏ qua

1. Chạy `py -3.13 -c "..."` kiểm VIỆC 0 như đã nêu ở mục 2 (2 lệnh, cho STT 6 và 11) — dán kết quả
   thật vào báo cáo hoàn thành (mục 6), không được nói suông "đã sửa".
2. Chạy `chay_buoc3.py --tab Lopezzapa68 --dong 4 --thu` (tập 04 đã giao hàng xong từ trước) —
   PHẢI dừng ở BƯỚC A với lý do "cột VIDEO đã có giá trị", KHÔNG được chạy tiếp bất cứ bước nào
   (đây là phép thử an toàn nhất — không tốn tiền, không phá dữ liệu, nhưng buộc code phải đọc
   đúng trạng thái thật trên trang tính).
3. Chạy `chay_buoc3.py --tab Lopezzapa68 --dong 999 --thu` (dòng không tồn tại) — phải báo lỗi rõ
   ràng, KHÔNG crash không rõ nguyên nhân (traceback trần).
4. **KHÔNG được tự ý chạy thật cho STT 11 hoặc 19** (đang có vấn đề khác đang xử lý ở lane này,
   xem `CLAUDE-DEEPSEEK-satori.TXT` nếu tò mò tại sao — không phải việc của bạn, tránh đụng vào).
5. Ghi lại THỜI GIAN thật của mỗi bước test (yêu cầu chuẩn của dự án: mọi báo cáo test phải kèm số
   đo thời gian, không được nói suông "đã test xong").

## 6. BÁO CÁO HOÀN THÀNH VIỆC VIẾT CODE (khác báo cáo vận hành ở mục 4)

Khi xong toàn bộ (VIỆC 0 + `chay_buoc3.py` + test mục 5), ghi **một file duy nhất**, ghi đè được
nếu chạy lại:

`E:\CLAUDE\YOUTUBE\h2dev\docs\BAO_CAO_HOAN_THANH_CHAY_BUOC3.md`

Đúng khuôn sau, điền số thật — người kiểm (Claude) chỉ đọc file này để nghiệm thu, KHÔNG tự dò lại
toàn bộ code nếu file này đủ chi tiết và trung thực, nên bỏ sót/nói vống ở đây sẽ khiến việc kiểm
tra sai kết luận:

```markdown
# BÁO CÁO HOÀN THÀNH — chay_buoc3.py

Ngày làm: <ngày> · Model thực hiện: <tên model> · Thời gian làm: <tổng phút>

## 1. Đã sửa gì (VIỆC 0)
- File: <đường dẫn>, dòng: <số dòng hoặc mô tả vị trí>
- Trước/sau (trích đoạn code, không cần cả file)
- Kết quả 2 lệnh kiểm (mục 2 của hồ sơ giao việc) — DÁN NGUYÊN VĂN output thật

## 2. File mới đã tạo
- `pipeline/chay_buoc3.py` — <số dòng>, tóm tắt cấu trúc (tên hàm chính + việc mỗi hàm làm)

## 3. Kết quả 3 test bắt buộc (mục 5)
- Test 1 (VIỆC 0): <PASS/FAIL> — <output thật>
- Test 2 (--dong 4 --thu): <PASS/FAIL> — <output thật>, thời gian chạy: <X giây>
- Test 3 (--dong 999 --thu): <PASS/FAIL> — <output thật>

## 4. Quyết định thiết kế đáng chú ý
(chỗ nào hồ sơ giao việc không nói rõ, bạn tự quyết — ghi lại quyết định + vì sao, để người kiểm
biết chỗ nào cần soi kỹ hơn)

## 5. Rủi ro / việc CHƯA làm
(thành thật liệt kê — vd "chưa test đường chạy thật với STT có ảnh đủ vì sợ tốn tiền TTS thật")

## 6. Câu hỏi cho người giao việc (nếu có)
```

## 7. Tài liệu nên đọc trước khi viết (không bắt buộc đọc hết, nhưng đừng đoán nếu lệch)

- `E:\CLAUDE\YOUTUBE\h2dev\CLAUDE.md` — quy tắc chung dự án, đặc biệt mục "QUY TRÌNH 3 BƯỚC"
- `pipeline/render_engine.py` — xem cách nó tự in tiến độ + resume, bắt chước phong cách
- `pipeline/ghi_cot_video.py`, `pipeline/quet_dong_can_anh.py` — 2 file cần sửa ở VIỆC 0
- `pipeline/giao_hang.py`, `pipeline/drive_handoff.py`, `pipeline/sinh_img_doan.py` — đọc docstring
  đầu file để biết tham số bắt buộc
- `profiles/profiles/satori-jp-obaa.json` — nơi thêm field `folder_pattern`
- `docs/GIAO_DEEPSEEK_3TAP.md` — ví dụ thật về luật retry/dừng dự án đã dùng trước đây (tham khảo
  giọng văn báo cáo, KHÔNG copy nguyên lệnh trong đó — lệnh đó dành cho người, không phải script)
