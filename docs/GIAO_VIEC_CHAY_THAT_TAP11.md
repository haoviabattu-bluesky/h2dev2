# GIAO VIỆC — gỡ TẠM DỪNG + chạy thật `chay_buoc3.py` cho tập 11

File tự chứa, làm theo đúng thứ tự, không cần hỏi ai. Lệnh chạy tại
`E:\CLAUDE\YOUTUBE\h2dev\pipeline`, dùng `py -3.13`.

**Bối cảnh:** người giao việc đã xem báo cáo phương án B (đo neo ảnh + kiểm nội dung tay), chấp
nhận kết quả (1 cụm ~3 ảnh lệch vị trí trong 121 — do bước 1 viết `img_prompts.txt` lệch thứ tự
thời gian ở đúng cụm đó, không sửa được bằng đổi số trong `img_doan.txt` vì ảnh hiển thị theo thứ
tự tên file cố định; xem `docs/BAO_CAO_HOAN_THANH_PHUONG_AN_B.md` nếu cần đối chiếu). Quyết định:
**chạy thật, không sửa thêm.**

## ⛔ CẤM

Không xoá dòng/cột/dữ liệu Google Sheet. Không sửa `script.txt`/`voice.*`/`img_prompts.txt`. Không
`taskkill` Chrome. Không Ctrl+C giữa chừng trừ khi thấy log hiện B5 (gen ảnh) đang CHẠY THẬT — điều
đó không nên xảy ra vì ảnh đã đủ 121/121, thấy vậy là dấu hiệu đếm ảnh sai, dừng ngay và báo lại.

## VIỆC 1 — gỡ khoá cột H (⚠️ đọc kỹ, có một bẫy)

Ô H12 (tab `Lopezzapa68`, dòng 12 = STT 11, spreadsheet ID
`1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`) hiện có:
```
Deepseek trả lời Claude 22:56: vào kiểm tra câu trả lời tại E:\CLAUDE\YOUTUBE\h2dev\CLAUDE-DEEPSEEK-satori.TXT | TẠM DỪNG — chờ sửa neo ảnh, KHÔNG chạy bước 3
```

**Bẫy:** `chay_buoc3.py` kiểm khoá bằng `"TẠM DỪNG" in cot_h.upper()` — CHỈ TÌM CHUỖI CON. Nếu bạn
chỉ NỐI THÊM chữ (kiểu "HẾT TẠM DỪNG — ...") thì chuỗi con "TẠM DỪNG" VẪN CÒN trong ô, dòng vẫn bị
coi là khoá! Phải **XOÁ HẲN** đúng cụm `| TẠM DỪNG — chờ sửa neo ảnh, KHÔNG chạy bước 3` ra khỏi
nội dung ô, giữ nguyên phần còn lại. Đọc giá trị ô thật trước, dùng `.replace()` trên chuỗi Python,
rồi ghi đè lại NGUYÊN GIÁ TRỊ MỚI (không phải nối thêm) — dùng cơ chế `svc()` sẵn có trong
`ghi_cot_video.py`/`quet_dong_can_anh.py`, đừng viết lại kết nối Google Sheets từ đầu:

```python
import sys; sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\h2dev\pipeline")
import ghi_cot_video as gcv
SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
s = gcv.svc(doc_thoi=True)
cur = s.values().get(spreadsheetId=SHEET_ID, range="Lopezzapa68!H12").execute()["values"][0][0]
moi = cur.replace(" | TẠM DỪNG — chờ sửa neo ảnh, KHÔNG chạy bước 3", "")
assert "TẠM DỪNG" not in moi.upper(), "chưa xoá hết, kiểm lại chuỗi khớp chính xác"
gcv.svc(doc_thoi=False).values().update(
    spreadsheetId=SHEET_ID, range="Lopezzapa68!H12",
    valueInputOption="USER_ENTERED", body={"values": [[moi]]}).execute()
print("H12 sau khi go khoa:", moi)
```
In ra giá trị H12 sau khi sửa, dán vào báo cáo (mục dưới) — để xác nhận đã gỡ đúng, không xoá nhầm
phần "Deepseek trả lời Claude...".

## VIỆC 2 — xác nhận `chay_buoc3.py --thu` thấy sẵn sàng (kiểm trước khi chạy thật)

```
py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 11 --thu
```
Phải in ra "mọi thứ sẵn sàng" (không còn báo TẠM DỪNG). Nếu vẫn báo khoá → VIỆC 1 chưa xong, quay
lại sửa, ĐỪNG chạy thật khi còn báo khoá.

## VIỆC 3 — chạy thật

```
py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 11
```
Không tốn tiền giọng (voice.mp3 đã có, `render_engine.py` tự bỏ qua bước TTS). Sẽ mất thật
khoảng 20-30 phút cho các bước ghép + QC video. Để nó chạy hết, không ngắt giữa chừng trừ trường
hợp đã nêu ở mục CẤM.

## BÁO CÁO — file MỚI, không nối vào các báo cáo trước (việc khác)

`E:\CLAUDE\YOUTUBE\h2dev\docs\BAO_CAO_HOAN_THANH_CHAY_THAT_TAP11.md`:

```markdown
# BÁO CÁO — chạy thật tập 11 qua chay_buoc3.py

Ngày: <...> · Model: <...> · Thời gian: <tổng phút>

## 1. Gỡ khoá cột H
Giá trị H12 SAU khi gỡ (dán nguyên văn) — xác nhận không còn "TẠM DỪNG" và không mất nội dung cũ

## 2. Kết quả --thu (trước khi chạy thật)
Dán nguyên văn output

## 3. Kết quả chạy thật (dán TOÀN BỘ log chay_buoc3.py in ra, không tóm tắt)
- Đường dẫn báo cáo BAO_CAO_BUOC3\... mà chay_buoc3.py tự ghi
- Điểm B8Q (so với 3,1/5 của bản cũ không neo)
- Đường dẫn giao hàng cuối (nếu ĐẠT), hoặc bước nào dừng + lý do (nếu không ĐẠT)
- Giá trị cột G và H12 SAU khi chạy xong (đọc lại từ sheet, dán nguyên văn)

## 4. Câu hỏi (nếu có)
```

Nếu bước 3 KHÔNG đạt (dừng ở bước nào đó): dừng lại, KHÔNG tự thử sửa hay chạy lại quá 1 lần, báo
cáo trung thực rồi chờ người giao việc quyết — như mọi lần trước.
