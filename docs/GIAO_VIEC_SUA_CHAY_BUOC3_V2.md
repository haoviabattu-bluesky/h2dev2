# GIAO VIỆC — vá 3 lỗi trong `pipeline/chay_buoc3.py` (bản V2, sau khi kiểm tra)

File này tự chứa. Đọc hết rồi làm theo đúng thứ tự, không cần hỏi ai, không cần đọc lịch sử chat.
Mọi lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev\pipeline`, luôn dùng `py -3.13`.

**Bối cảnh:** bạn (hoặc phiên trước của bạn) đã viết `pipeline/chay_buoc3.py` theo
`docs/GIAO_VIEC_VIET_CHAY_BUOC3.md` và nộp `docs/BAO_CAO_HOAN_THANH_CHAY_BUOC3.md`. Người giao việc
đã đọc code thật (không chỉ tin báo cáo) và tìm ra 3 điểm cần sửa trước khi được dùng cho cron tự
động. Phần lớn code ĐÃ ĐÚNG (8 bước, cấm tuyệt đối, định dạng báo cáo, ghi cột H — giữ nguyên,
đừng viết lại từ đầu). Đây là bản VÁ, không phải viết lại.

## ⛔ CẤM — nhắc lại nguyên vẹn từ hồ sơ gốc

Không đụng lane nào khác ngoài `satori-jp-obaa`. Không tự vẽ ảnh khi thiếu. Không xoá dòng/cột/dữ
liệu Google Sheet. Không sửa `script.txt`/`voice.*`/`img_doan.txt`/`characters.json`. Không
`taskkill` Chrome. Không đăng `review-vi.mp4`/`final_vi.mp4`. Không thêm `--burn-sub`.

---

## VÁ 1 (QUAN TRỌNG NHẤT) — BƯỚC A không sẵn sàng đang GHI RÁC

**Lỗi:** trong `main()`, nhánh "dòng chưa sẵn sàng" (khoảng dòng 207-220 hiện tại — số dòng có thể
lệch nếu code đã đổi, tìm theo đoạn `if not san_sang:`) vẫn gọi `viet_bao_cao()` +
`ghi_cot_h()` như một lần chạy thật. "Chưa tới lượt" là trạng thái BÌNH THƯỜNG (máy 2 chưa vẽ xong,
hoặc tập đã giao rồi) — không phải sự kiện cần lưu vết. Nếu một cron gọi `chay_buoc3.py` định kỳ
cho một dải STT, MỌI dòng chưa tới lượt sẽ nhận thêm một dòng cột H + một file báo cáo MỖI LẦN cron
chạy — cột H phình rác, `BAO_CAO_BUOC3/` đầy file rỗng vô nghĩa.

**Cách sửa:** trong nhánh `if not san_sang:`, XOÁ hai dòng gọi `viet_bao_cao()` và `ghi_cot_h()`
(chỉ giữ lại cho nhánh `--thu`). Nhánh không-sẵn-sàng khi chạy THẬT (không `--thu`) chỉ cần:
```python
log(f"=== {a.tab} · STT {a.dong} ===")
log(f"  BƯỚC A: {ly_do}")
return 0
```
Không ghi báo cáo, không ghi cột H. Giữ nguyên toàn bộ phần còn lại của hàm (BƯỚC B trở đi vẫn ghi
báo cáo + cột H bình thường khi có việc thật để báo).

## VÁ 2 — chưa biết đọc dấu hiệu "TẠM DỪNG" ở cột H

**Lỗi:** một dòng có thể đang bị NGƯỜI giữ lại thủ công vì lý do khác (ví dụ: đang sửa lỗi neo ảnh
ở một script riêng, chưa liên quan tới bước 3). Người giữ ghi một ghi chú vào cột H, nhưng
`chay_buoc3.py` không đọc cột H trước khi chạy — nó sẽ vô tư chạy đè lên đúng lúc không nên.

**Cách sửa:** trong BƯỚC A, sau khi đọc `status_img, video, de_tai`, đọc THÊM giá trị cột H của
đúng dòng đó (dùng lại cơ chế đọc đã có trong `doc_trang_tinh()` — sửa hàm này để trả về thêm cột H,
hoặc đọc thêm một ô riêng, tuỳ bạn, miễn không tự viết lại kết nối Google Sheets từ đầu). Nếu cột H
chứa chuỗi con **"TẠM DỪNG"** (không phân biệt hoa/thường) → coi như KHÔNG sẵn sàng, xử lý CÙNG
NHÁNH với VÁ 1 (chỉ log, không ghi báo cáo/cột H, tránh đè lên chính ghi chú giữ lại đó):
```python
ly_do = f"cột GHI CHÚ (H) có dấu 'TẠM DỪNG' — người khác đang giữ dòng này: '{cot_h[:80]}'"
```
Quy ước cho về sau: bất kỳ ai muốn giữ một dòng lại thủ công thì ghi vào cột H một cụm bắt đầu bằng
đúng chữ "TẠM DỪNG" — quy ước này áp dụng từ giờ, ghi lại trong docstring đầu file.

**Kiểm bằng dữ liệu THẬT (không phải mô phỏng):** dòng 11 và 19 của tab `Lopezzapa68` VỪA được ghi
dấu này thật (cột H, nối vào ghi chú cũ). Chạy:
```
py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 11 --thu
py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 19 --thu
```
Cả hai PHẢI báo "không sẵn sàng" vì lý do TẠM DỪNG (không phải vì thiếu ảnh — hai dòng này ĐANG
"Img done" đầy đủ, nên nếu vẫn báo sẵn sàng nghĩa là vá chưa ăn). Trước khi vá, hai lệnh trên báo
"mọi thứ sẵn sàng" — dán cả hai lần chạy (trước/sau vá) vào báo cáo hoàn thành.

## VÁ 3 — BƯỚC E xếp lỗi nội dung thật vào lỗi hạ tầng

**Lỗi:** `sinh_img_doan.py` có hai loại lỗi khác hẳn nhau, nhưng code hiện tại xếp chung một loại
(retry 3 lần hạ tầng):
- `"khong xep vua"` — lỗi NỘI DUNG THẬT (kịch bản quá ngắn so với số ảnh cần gán). Retry vô ích,
  script không tự đổi, thử 3 lần vẫn y hệt lần 1 — chỉ tốn thêm 2 lần gọi LLM vô ích.
- Lỗi khác (`"loi LLM"`, exception mạng/API) — mới thật sự là lỗi hạ tầng, đáng retry.

**Cách sửa:** trong khối BƯỚC E, sau khi `chay_lenh(...)` trả về `ok=False`, kiểm thêm:
```python
if not ok:
    if "khong xep vua" in lines.lower() or "khong xếp vừa" in lines.lower():
        raise DungViNguyenNhan(f"sinh img_doan.txt: kịch bản quá ngắn so với số ảnh — "
                                f"trích: {lines[-300:]}")
    raise DungViNguyenNhan(f"sinh img_doan.txt thất bại sau {lan} lần — trích: {lines[-300:]}")
```
(Tức là: dù lỗi loại nào, cuối cùng vẫn dừng hẳn — điểm khác là THÔNG BÁO phải nói rõ đây là lỗi
nội dung không thể sửa bằng cách thử lại, để người đọc báo cáo không thắc mắc "sao thử 3 lần vẫn
vậy". Nếu muốn tối ưu hơn: kiểm chuỗi này NGAY sau lần thử đầu tiên, dừng sớm không cần đợi đủ 3
lần — tự quyết, ghi lại quyết định ở mục 4 báo cáo.)

## VÁ 4 (nhỏ, tuỳ chọn — không bắt buộc, làm nếu còn thời gian)

BƯỚC C (`drive_handoff.py download-result`) đang được `chay_lenh(..., retry_toi_da=3)` — trong khi
`drive_handoff.py` đã tự retry bên trong nó rồi. Đổi thành `retry_toi_da=1` (gọi đúng 1 lần từ phía
`chay_buoc3.py`, để `drive_handoff.py` tự lo phần retry của chính nó). Không bắt buộc vì không gây
hại, chỉ hơi phí thời gian khi drive thật sự lỗi — bỏ qua nếu ưu tiên thời gian.

---

## TEST BẮT BUỘC sau khi vá — không được bỏ qua

1. Lệnh ở VÁ 2 (STT 11 và 19, có `--thu`) — dán output THẬT trước/sau vá.
2. Lặp lại nguyên 3 test đã làm ở bản trước (mục 5 hồ sơ gốc — STT 6 giờ đã có VIDEO nên đổi test
   này sang **STT 4** để giữ đúng tinh thần "dòng đã giao xong phải dừng ở BƯỚC A":
   ```
   py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 4 --thu
   py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 999 --thu
   ```
   Cả hai: PHẢI **không ghi gì vào cột H, không tạo file báo cáo mới** — vì đây chính là phép thử
   VÁ 1. Kiểm bằng cách so `ls BAO_CAO_BUOC3/` trước và sau khi chạy — số file phải KHÔNG đổi.
3. Đọc lại cột H của dòng 4 trên trang tính TRƯỚC và SAU khi chạy test — phải giống hệt nhau (chưa
   sửa VÁ 1 thì cột H dòng 4 sẽ có thêm dòng mới mỗi lần chạy test, đó chính là triệu chứng lỗi).

## BÁO CÁO — nối vào CUỐI file cũ, không xoá phần trước

Mở `docs/BAO_CAO_HOAN_THANH_CHAY_BUOC3.md`, thêm vào cuối (không xoá nội dung đã có):

```markdown
## PHẦN 2 — BẢN VÁ V2 (ngày <...>)

### Đã sửa
1. VÁ 1 (spam báo cáo khi chưa sẵn sàng): <mô tả + trích đoạn code trước/sau>
2. VÁ 2 (đọc "TẠM DỪNG" ở cột H): <mô tả + trích đoạn code trước/sau>
3. VÁ 3 (phân loại lỗi BƯỚC E): <mô tả + trích đoạn code trước/sau>
4. VÁ 4 (nếu có làm): <mô tả>

### Test — dán NGUYÊN VĂN output thật
- STT 11 --thu (trước vá / sau vá): ...
- STT 19 --thu (trước vá / sau vá): ...
- STT 4 --thu, STT 999 --thu: ...
- Số file trong BAO_CAO_BUOC3/ trước/sau: ...
- Cột H dòng 4 trước/sau: ...

### Câu hỏi (nếu có)
```

## Tài liệu liên quan (đọc nếu cần đối chiếu, không bắt buộc đọc lại từ đầu)

- `pipeline/chay_buoc3.py` — file đang vá
- `docs/GIAO_VIEC_VIET_CHAY_BUOC3.md` — hồ sơ gốc (luật nền vẫn áp dụng)
- `docs/BAO_CAO_HOAN_THANH_CHAY_BUOC3.md` — báo cáo lần trước, nối tiếp chứ không viết đè
