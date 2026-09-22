# GIAO VIỆC — cháy phụ đề tiếng Nhật còn thiếu ở 3 tập đầu Lane D (irogatatarukioku)

> File tự chứa — không cần đọc lịch sử chat. Việc này thuộc **Bước 3** (render/ghép video bằng
> ffmpeg), Claude Code không tự chạy — giao cho Hermes/DeepSeek hoặc agent bước 3 bất kỳ.

## Phát hiện (đã verify bằng ảnh thật, không phải suy đoán)

Kiểm 11 tập trong `E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\` — trích khung hình tại đúng mốc giữa
1 câu thoại (đọc từ `phude.srt`) cho từng tập:

| Tập | Phụ đề Nhật cháy trong `final.mp4`? |
|---|---|
| ep01-ushijima-mitsuru | ❌ KHÔNG |
| ep02-kuribayashi-iwojima | ❌ KHÔNG |
| ep03-nakagawa-peleliu | ❌ KHÔNG |
| ep04-aruga-yamato → ep11-ando-226incident (8 tập) | ✅ CÓ |

Cả 11 tập đều đã có sẵn `phude.srt` chính xác trong đúng thư mục CHANEL của tập đó (đã đối chiếu
byte-for-byte khớp 100% với `voice_paced.srt` gốc ở bước 1 — không cần sinh lại phụ đề, chỉ cần
CHÁY nó vào 3 video còn thiếu).

## Việc cần làm: CHÁY `phude.srt` vào `final.mp4` cho ĐÚNG 3 tập ep01/ep02/ep03

Dùng đúng style đã áp dụng nhất quán cho ep04-11 (lấy từ `pipeline/assemble.py --burn-sub`, font
Meiryo, cỡ 18, viền đen, đáy khung — xem dòng lệnh dưới). **Không đổi style khác** để 11 tập nhìn
đồng nhất.

Với mỗi tập trong `{ep01-ushijima-mitsuru, ep02-kuribayashi-iwojima, ep03-nakagawa-peleliu}`:

```
EP=E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\<ten-tap>

REM 1) Backup bản gốc (an toàn — lỡ ffmpeg lỗi giữa chừng vẫn còn bản cũ)
copy "%EP%\final.mp4" "%EP%\final_no_sub_backup.mp4"

REM 2) Copy srt ra thư mục làm việc tạm rồi cd vào đó (libass cần đường dẫn tương đối/không dấu
REM    cách phức tạp — lệnh dưới giả định chạy trong PowerShell/CMD tại đúng %EP%)
copy "%EP%\phude.srt" "%EP%\subs.srt"

REM 3) Cháy phụ đề — filter GIỐNG HỆT assemble.py để đồng nhất 11 tập
ffmpeg -y -i "%EP%\final_no_sub_backup.mp4" -vf "subtitles=subs.srt:force_style='FontName=Meiryo,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,MarginV=45,Alignment=2'" -c:v libx264 -crf 18 -preset medium -c:a copy "%EP%\final.mp4"

REM 4) Dọn file tạm
del "%EP%\subs.srt"
```

(Lệnh trên viết kiểu Windows CMD cho dễ đọc — đổi sang cú pháp shell đang dùng nếu chạy Bash/
PowerShell, ý nghĩa các bước giữ nguyên.)

## Nghiệm thu sau khi cháy (bắt buộc, đừng chỉ tin log ffmpeg thoát mã 0)

Trích 1 khung hình ở đúng mốc giữa câu thoại bên dưới cho từng tập, xem có CHỮ NHẬT hiện rõ ở đáy
khung không (không phải chỉ "video chạy được"):

| Tập | Giây | Câu thoại phải thấy |
|---|---|---|
| ep01-ushijima-mitsuru | 456 | 慎重に稜線を進んでいく様子が写真に残されている。 |
| ep02-kuribayashi-iwojima | 378 | いう一文も残されている。 |
| ep03-nakagawa-peleliu | 389 | 軽戦車、重機関銃、迫撃砲を配備している。 |

```
ffmpeg -y -ss <giây> -i "%EP%\final.mp4" -frames:v 1 -update 1 check.jpg
```

Thấy đúng câu trên hiện ở đáy khung, chữ trắng viền đen → ĐẠT. Xoá `final_no_sub_backup.mp4` sau
khi đã xác nhận (giữ lại phòng khi cần đối chiếu thì giữ thêm vài ngày cũng được, không bắt buộc
xoá ngay).

## Phạm vi — KHÔNG động vào các file khác

- Chỉ sửa `final.mp4` của đúng 3 tập trên. **KHÔNG đụng `final_vi_phude.mp4`** (bản phụ đề Việt để
  chủ dự án soi nội dung — khác mục đích, không phải bản đăng).
- **KHÔNG sửa `thumbnail.png`/`TIEU_DE_MO_TA.txt`/`tomtat.txt`** — không liên quan việc này.
- 8 tập ep04-11 đã ĐÚNG sẵn — không cần chạy lại.

Xong thì báo lại kết quả nghiệm thu 3 tập (ảnh check.jpg hoặc mô tả đã thấy chữ) — không cần ghi gì
thêm vào Google Sheet (cột G đã trỏ đúng thư mục CHANEL này từ trước, file được thay tại chỗ).
