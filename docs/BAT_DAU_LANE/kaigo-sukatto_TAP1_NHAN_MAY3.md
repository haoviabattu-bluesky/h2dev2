# NHẬN BÀN GIAO MÁY 3 → LÀM TIẾP — LANE O `kaigo-sukatto` · TẬP 1 `ep01-jaa-yamemasu`

> Viết 2026-09-30 bởi tab Lane O sau khi chạy xong bước B (viết + khoá) của `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kaigo-sukatto_TAP1.md`.
> Dùng khi anh báo "anh sửa xong kịch bản lane O tập 1" hoặc ô D2 tab `Lane-O` = `Đã sửa kịch bản`.
> Tab mới: đọc HẾT file này, mở đầu báo cáo bằng `@lane:kaigo-sukatto`, làm liền một mạch từ mục 2 tới mục 7, KHÔNG hỏi lại
> (trừ điểm DỪNG ở mục 8). KHÔNG đọc lại SOP/COMMENT_INSIGHT/profile — cần gì thì file này đã trỏ đúng mục.
> Mọi lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev`.

## 0. ĐANG Ở ĐÂU
| Mục | Giá trị |
|---|---|
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\` |
| Bản đã gửi máy 3 | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\Lane-O\ep01-jaa-yamemasu\script.txt` (anh sửa thẳng file này) |
| Sheet | tab `Lane-O` dòng 2 (D2 = trạng thái, C2 = thư mục tập) |
| Tiêu đề | 【漫画】「じゃあ、辞めます」が口ぐせの介護士が、人手不足の施設で3回目に言った結果… (Nhân viên chăm sóc có câu cửa miệng "Vậy tôi nghỉ" — kết quả khi nói lần thứ 3 ở cơ sở thiếu người) |
| Log bước B | `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\run_B3G.log` |
| Bản khoá (trước khi anh sửa) | 5.334 chữ ≈ 16,8' · thoại 11% · sha `9e039e89e6…` · hook 177 chữ · khoá 30/09 21:22 |
| Vai trong bản khoá (anh có thể đổi) | 宇佐見航 (Usami Wataru) 38t = `shu` · 牧野 (Makino) = 主任 nữ · 竹内 (Takeuchi) = パート nữ · 片山美緒 (Katayama Mio) 22t = nhân viên mới · 石黒誠 (Ishiguro Makoto) 45t = người thế chỗ · 小田切 (Odagiri) = 施設長 · 富田さん (bà/ông Tomita) = cụ ở unit |
| Việc còn lại | nhận bản sửa → soi → cast + giọng → prompt ảnh → hình + clip hook → giao máy 2 |

## 1. KIỂM TRẠNG THÁI TRƯỚC
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --trang-thai --profile kaigo-sukatto
```
- D2 vẫn `Chờ kiểm tra kịch bản` → nhắc anh đổi D2, DỪNG. Chỉ khi anh bảo "cứ nhận" mới thêm `--force` ở mục 2.
- Kiểm không có `make_video` nào của `kaigo-sukatto` đang chạy (cấm 2 tiến trình cùng slug):
  `powershell -NoProfile -c "Get-CimInstance Win32_Process -Filter \"Name like 'py%'\" | ?{$_.CommandLine -match 'kaigo-sukatto'} | Select ProcessId,CommandLine"`

## 2. NHẬN BẢN SỬA (0 LLM, không sửa 1 chữ)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --nhan --profile kaigo-sukatto --slug ep01-jaa-yamemasu
```
- Kết quả đo ở `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\NHAN_MAY3.md`.
- **CHẶN** (ngắn <70% ngân sách, hoặc số liệu ngoài `series_ctx.txt`) → báo anh 1 dòng lý do, DỪNG, không sửa hộ.
- **Kiểm hook 30 giây:** so `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\hook\hook_locked.txt` với đoạn đầu `script.txt`.
  Lệch ranh giới → khoá lại tay theo lệnh ở `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` §2. Tuyệt đối không sửa `script.txt`.

## 3. SOI 1 LƯỢT BẢN NHẬN (chỉ BÁO, không sửa) — luật `SOP_LANE_O.md` §5
Đọc `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\script.txt`, ghi nhận xét vào báo cáo:
1. Hậu quả đến từ CƠ CHẾ (chọn ユニットリーダー (trưởng unit), không níu, phỏng vấn nơi khác hỏng) — không mắng, không trả thù, không hả hê.
2. 「じゃあ、辞めます」 (Vậy tôi nghỉ) đúng 3 lần, mức cược tăng (ca đêm → エルダー/委員会 (kèm người mới/uỷ ban) → chọn trưởng unit);
   câu CUỐI lặp câu cửa miệng với nghĩa đổi, KHÔNG phải 「あの店でその言葉を聞く人はもういない」 (ở tiệm đó không còn ai nghe câu ấy).
3. Mỗi lần có 1 người tốt cụ thể gánh thay (主任 (chủ nhiệm) nữ 40s lo mẹ già; パート (bán thời gian) nữ 50s ăn trưa đứng).
4. Cụ già/người nhà không vô lý; tối đa ヒヤリハット (suýt sự cố); số quy định chỉ [D1]–[D4]; không 日曜当番/神田さん/trận bóng/đèn tiệm.
5. Lượt thoại nào cũng rõ ai nói.
6. Bản khoá kết bằng lời mời 高評価とチャンネル登録 (bấm thích và đăng ký kênh) dù kênh chưa có — anh giữ thì thôi, chỉ nhắc trong báo cáo.
Có vi phạm nặng (vd cụ bị ngã, câu kết chép gốc) → báo anh, DỪNG trước mục 4. Vi phạm nhẹ → ghi vào báo cáo, làm tiếp.

## 4. CAST + GIỌNG
Viết tay `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\characters.json` sau khi đọc kịch bản (lấy TÊN thật trong kịch bản):
- MỌI vai có thoại hoặc ≥2 cảnh = `{id,name,vai,age,gender,look,ref:true,voice:{speaker,style}}`.
- `shu` = nhân vật chính (nam cuối 30, 9 năm ở cơ sở) + `"kuchiguse": "「じゃあ、辞めます」"`.
- ユニットリーダー/主任 nữ 40s · パート nữ 50s · người thế chỗ (中途の介護福祉士 (nhân viên chăm sóc có chứng chỉ vào giữa chừng) 40s) · 施設長 (giám đốc cơ sở) · 1 cụ + người nhà nếu có thoại.
- Giọng lấy từ `voice.fixed_cast` / `voice.cast_bank` trong `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\kaigo-sukatto.json`.
  Bà cụ chưa có giọng → chọn 1 giọng VOICEVOX nữ trầm, ghi rõ trong báo cáo.
- `look` khác nhau rõ: màu đồng phục chăm sóc/áo polo, tóc, kính. KHÔNG áo blouse trắng (trừ y tá). Cụ già sạch sẽ, đàng hoàng.
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\gan_vai.py --profile kaigo-sukatto --slug E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu
```

## 5. PROMPT ẢNH THÂN (CHỈ `--only`)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --only B5W
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --only B5P
```
Kiểm `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\img_prompts.txt`: cảnh có người phải có dòng `@CAST:`;
không cảnh ngã/thương tích/trói/tắm lộ thân.

## 6. HOOK — máy 1 làm trọn hình (theo hook ANH SỬA)
```bat
:: 6a. storyboard (dựng từ hook_locked.txt mới)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_storyboard.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --force
:: 6b. master vai: make_video.Job(...).masters_from_bible()  ·  ảnh hook: pipeline\gen_images.py --cast-root <thư mục tập> --quality low   (chạy nền)
:: 6c. QC ảnh:  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\qc_hook_clip.py --hook E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\hook --anh N
:: 6d. clip Grok 6 giây (chạy nền):
set GROK_SHEET_ID=1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\hook_lane_g\grok_1tk.py E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\hook 14
:: 6e. QC clip: qc_hook_clip.py --clip N (FAIL → chỉnh prompt clip, chạy lại ĐÚNG clip đó) · SFX: tools\hook_lane_g\sfx.py
:: 6f. HOOK_TAP.md → viết hết <<CẦN NGƯỜI>> → chạy lại thêm --kiem
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu --profile kaigo-sukatto
```
- Xem clip Grok BẰNG MẮT (Grok từng trả clip lạc đề — gặp là làm lại clip đó).
- Xong kiểm 0 Chrome GPM còn sống: `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | ? CommandLine -match 'GPMLogin'` — chỉ đóng đúng PID của GPM, CẤM kill Chrome chung.

## 7. GIAO MÁY 2 (tự ghi D2 = `Done`, H2 = `cần ảnh (N ảnh, ~Xđ)`)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --job kaigo-sukatto ep01-jaa-yamemasu
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --bundle --profile-list kaigo-sukatto
```
- Đọc lại `_BANGIAO.txt` trong `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\Lane-O\ep01-jaa-yamemasu\`.
- KHÔNG gọi dự án TITLE (kênh chưa có, `title_auto=false`) → báo anh còn thiếu tiêu đề cuối/thumbnail.

## 8. ĐIỂM DỪNG / BẪY
- DỪNG: D2 chưa đổi · `--nhan` CHẶN · vi phạm nặng §3 · ảnh/clip hook làm theo hook CŨ cần xoá (xoá tay thì hỏi anh; còn lại tạo mới).
- Máy 1 CẤM `--den B4` / `--den B5Q` / `--from B4` (tốn tiền thật; code chặn cứng `chan_buoc2_may1`).
- Cổng `review_may3.cong()` chặn B5W/dong_goi khi chưa `received` hoặc script đổi sau khi nhận → chạy lại `--nhan`, không đi cửa sau.
- Không sửa tay `script.txt` — mọi sửa qua `viec_tay.txt` → Opus, hoặc anh sửa ở `jobs\`.
- Ảnh / Grok chạy bằng Bash `run_in_background`, báo giờ dự kiến rồi dừng lượt; cấm `tail` log định kỳ.
- Báo cáo: chữ Nhật kèm dịch Việt; đường dẫn tuyệt đối; dòng cuối nói tool nào đang chạy + dự kiến xong.
