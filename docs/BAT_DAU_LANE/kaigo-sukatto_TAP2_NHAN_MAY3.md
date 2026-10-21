# NHẬN BÀN GIAO MÁY 3 → LÀM TIẾP — LANE O `kaigo-sukatto` · TẬP 2 `ep02-shigoto-dekirunde`

> Viết 2026-10-01 bởi tab Lane O sau khi chạy xong bước B (viết + khoá) của `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kaigo-sukatto_TAP2.md`.
> Dùng khi anh báo "anh sửa xong kịch bản lane O tập 2" hoặc ô D3 tab `Lane-O` = `Đã sửa kịch bản`.
> Tab mới: đọc HẾT file này, mở đầu báo cáo bằng `@lane:kaigo-sukatto`, làm liền một mạch từ mục 2 tới mục 7, KHÔNG hỏi lại
> (trừ điểm DỪNG ở mục 8). KHÔNG đọc lại SOP/COMMENT_INSIGHT/profile — cần gì thì file này đã trỏ đúng mục.
> Mọi lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev`.

## 0. ĐANG Ở ĐÂU
| Mục | Giá trị |
|---|---|
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\` |
| Bản đã gửi máy 3 | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\Lane-O\ep02-shigoto-dekirunde\script.txt` (anh sửa thẳng file này) |
| Sheet | tab `Lane-O` dòng 3 (D3 = trạng thái, C3 = thư mục tập) |
| Tiêu đề | 【漫画】「自分、仕事できるんで」が口ぐせの中途介護士が行き着く先… (Nhân viên chăm sóc chuyển việc suốt ngày nói "Tôi làm giỏi mà" — kết cục) |
| Log bước B | `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\run_B3G.log` |
| Bản khoá (trước khi anh sửa) | 5.035 chữ ≈ 15,9' · thoại 16% · sha `415e521449…` · hook 179 chữ · khoá 01/10 07:09 (1 patch) |
| Vai trong bản khoá (anh có thể đổi) | 根岸達也 (Negishi Tatsuya) 38t = `shu` · 浅井 (Asai) = 施設長 nữ 50s (người phỏng vấn) · 竹中 (Takenaka) = 主任 nam 40s (người phỏng vấn) · 早瀬 (Hayase) = ユニットリーダー nữ 40s (cơ sở cũ) · 小野寺 (Onodera) = 先輩 介護福祉士 nữ ~50s · 平田 (Hirata) = 後輩 năm 2, nam · 川村 (Kawamura) = 介護助手 · 戸川 (Togawa) = 介護福祉士 nam 40s, vào giữa chừng · 三好 (Miyoshi) = 施設長 cơ sở cũ · 佐伯さん (Saeki) = cụ nữ ~90t + 娘 (con gái) |
| Việc còn lại | nhận bản sửa → soi → cast + giọng → prompt ảnh → hình + clip hook → giao máy 2 |

## 1. KIỂM TRẠNG THÁI TRƯỚC
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --trang-thai --profile kaigo-sukatto
```
- D3 vẫn `Chờ kiểm tra kịch bản` → nhắc anh đổi D3, DỪNG. Chỉ khi anh bảo "cứ nhận" mới thêm `--force` ở mục 2.
- Kiểm không có `make_video` nào của `kaigo-sukatto` đang chạy (cấm 2 tiến trình cùng slug):
  `powershell -NoProfile -c "Get-CimInstance Win32_Process -Filter \"Name like 'py%'\" | ?{$_.CommandLine -match 'kaigo-sukatto'} | Select ProcessId,CommandLine"`

## 2. NHẬN BẢN SỬA (0 LLM, không sửa 1 chữ)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --nhan --profile kaigo-sukatto --slug ep02-shigoto-dekirunde
```
- Kết quả đo ở `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\NHAN_MAY3.md`.
- **CHẶN** (ngắn <70% ngân sách, hoặc số liệu ngoài `series_ctx.txt`) → báo anh 1 dòng lý do, DỪNG, không sửa hộ.
- **Kiểm hook 30 giây:** so `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\hook\hook_locked.txt` với đoạn đầu `script.txt`.
  Lệch ranh giới → khoá lại tay theo lệnh ở `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` §2. Tuyệt đối không sửa `script.txt`.

## 3. SOI 1 LƯỢT BẢN NHẬN (chỉ BÁO, không sửa) — luật `SOP_LANE_O.md` §5 + mục 3 của `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kaigo-sukatto_TAP2.md`
Đọc `E:\CLAUDE\YOUTUBE\h2devssets\O-kaigo-sukatto\ep02-shigoto-dekirunde\script.txt`, ghi nhận xét vào báo cáo:
1. Hậu quả đến từ CƠ CHẾ (bị rút 入浴介助 (hỗ trợ tắm)/kèm người mới, phần của anh luôn bị kiểm lại, phỏng vấn trượt vì tự khai) — không mắng, không hả hê.
2. 「自分、仕事できるんで」 (Tôi làm giỏi mà) 3 lần CHÍNH mức cược tăng, mỗi lần 1 người gánh: 早瀬 xếp lại ca, con ăn cà ri nguội một mình → 小野寺 kiểm lại mỗi ngày, ăn cơm hộp đứng → 平田 ở lại sau giờ học với 小野寺. Câu phụ 「前の施設ではこうでした」 (Ở cơ sở cũ làm thế này) xuất hiện 1 lần ở chỗ mới. Câu CUỐI lặp câu cửa miệng: bản khoá kết 「あの休憩室で『自分、仕事できるんで』と口にする人は、もう誰もいない」 (Ở phòng nghỉ ấy không còn ai nói câu đó) — NGHĨA CHƯA ĐỔI RÕ và dáng câu gần câu kết bị cấm của tập 1 (「あの店でその言葉を聞く人はもういない」) → anh cân nhắc.
3. Số mâu thuẫn: khai 「ミスはほぼゼロ」 (lỗi gần như bằng 0) vs 週に三回か四回 (3–4 lần/tuần) bị kiểm lại ✓.
4. Cụ già: chỉ ヒヤリハット (phanh xe lăn chưa khoá, cụ định đứng dậy, không ngã) ✓; không có 転倒/怪我/骨折 (ngã/thương tích/gãy xương). Người nhà không vô lý ✓. Số quy định chỉ [D1] 3:1, [D2] 週2回, [D3] 国家資格 ✓.
5. Không chép gốc: không cà vạt xanh, than 10 phút, 取り寄せ, câu 「半分だけ正しかった」, 「聞けば誰かが教えてくれる」 ✓ (đã grep = 0). NHƯNG câu đạo lý dòng áp chót (「仕事は…預けても大丈夫だという安心のほうへ集まっていく。できる人とは、自分で名乗るものではない」 — việc dồn về nơi có sự yên tâm) có cùng ý với câu kết gốc 「仕事が集まっていたのは信頼できる人のところだった」 → mượn ý, không mượn chữ; anh quyết giữ hay viết lại.
6. Cấu trúc: 7 chặng theo mục lục phỏng vấn ✓ (面接の朝 → 辞めた理由 → 仕事ぶり → 後輩 → 最後の質問 → chỗ mới → SAU ĐÓ). Có nhịp thương cảm với anh (物流倉庫, "代わりはいくらでもいる" (ai cũng thay được)) ✓. Tên cơ sở cũ けやきの里 (Làng Keyaki) hư cấu — anh kiểm lại xem trùng cơ sở thật không.
7. Lượt thoại: các câu của 浅井/竹中 đều rõ ai nói; dòng 「俺は信頼されている」 là nội tâm (không thoại).
8. Bản khoá kết bằng lời mời 高評価とチャンネル登録 (bấm thích và đăng ký kênh) dù kênh chưa có — anh giữ thì thôi, chỉ nhắc.
Có vi phạm nặng (vd cụ bị ngã, câu kết chép gốc) → báo anh, DỪNG trước mục 4. Vi phạm nhẹ → ghi vào báo cáo, làm tiếp.

## 4. CAST + GIỌNG
Viết tay `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\characters.json` sau khi đọc kịch bản (lấy TÊN thật trong kịch bản):
- MỌI vai có thoại hoặc ≥2 cảnh = `{id,name,vai,age,gender,look,ref:true,voice:{speaker,style}}`.
- `shu` = 根岸達也 (nam 38t, 中途, 6 năm ở cơ sở cũ) + `"kuchiguse": "「自分、仕事できるんで」"`.
- 早瀬 (ユニットリーダー nữ 40s) · 小野寺 (先輩 介護福祉士 nữ ~50s) · 平田 (後輩 năm 2, nam) · 川村 (介護助手) · 戸川 (介護福祉士 nam 40s) · 浅井 (施設長 nữ 50s) + 竹中 (主任 nam 40s) · 三好 (施設長 cơ sở cũ) · 佐伯さん (cụ nữ ~90t) + 娘.
- Giọng lấy từ `voice.fixed_cast` / `voice.cast_bank` trong `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\kaigo-sukatto.json`.
  Bà cụ chưa có giọng → chọn 1 giọng VOICEVOX nữ trầm, ghi rõ trong báo cáo.
- `look` khác nhau rõ: màu đồng phục chăm sóc/áo polo, tóc, kính. KHÔNG áo blouse trắng (trừ y tá). Cụ già sạch sẽ, đàng hoàng.
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\gan_vai.py --profile kaigo-sukatto --slug E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde
```

## 5. PROMPT ẢNH THÂN (CHỈ `--only`)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile kaigo-sukatto --slug ep02-shigoto-dekirunde --only B5W
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile kaigo-sukatto --slug ep02-shigoto-dekirunde --only B5P
```
Kiểm `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\img_prompts.txt`: cảnh có người phải có dòng `@CAST:`;
không cảnh ngã/thương tích/trói/tắm lộ thân.

## 6. HOOK — máy 1 làm trọn hình (theo hook ANH SỬA)
```bat
:: 6a. storyboard (dựng từ hook_locked.txt mới)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_storyboard.py --profile kaigo-sukatto --slug ep02-shigoto-dekirunde --force
:: 6b. master vai: make_video.Job(...).masters_from_bible()  ·  ảnh hook: pipeline\gen_images.py --cast-root <thư mục tập> --quality low   (chạy nền)
:: 6c. QC ảnh:  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\qc_hook_clip.py --hook E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\hook --anh N
:: 6d. clip Grok 6 giây (chạy nền):
set GROK_SHEET_ID=1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\hook_lane_g\grok_1tk.py E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde\hook 14
:: 6e. QC clip: qc_hook_clip.py --clip N (FAIL → chỉnh prompt clip, chạy lại ĐÚNG clip đó) · SFX: tools\hook_lane_g\sfx.py
:: 6f. HOOK_TAP.md → viết hết <<CẦN NGƯỜI>> → chạy lại thêm --kiem
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep02-shigoto-dekirunde --profile kaigo-sukatto
```
- Xem clip Grok BẰNG MẮT (Grok từng trả clip lạc đề — gặp là làm lại clip đó).
- Xong kiểm 0 Chrome GPM còn sống: `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | ? CommandLine -match 'GPMLogin'` — chỉ đóng đúng PID của GPM, CẤM kill Chrome chung.

## 7. GIAO MÁY 2 (tự ghi D3 = `Done`, H3 = `cần ảnh (N ảnh, ~Xđ)`)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --job kaigo-sukatto ep02-shigoto-dekirunde
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --bundle --profile-list kaigo-sukatto
```
- Đọc lại `_BANGIAO.txt` trong `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\Lane-O\ep02-shigoto-dekirunde\`.
- KHÔNG gọi dự án TITLE (kênh chưa có, `title_auto=false`) → báo anh còn thiếu tiêu đề cuối/thumbnail.

## 8. ĐIỂM DỪNG / BẪY
- DỪNG: D3 chưa đổi · `--nhan` CHẶN · vi phạm nặng §3 · ảnh/clip hook làm theo hook CŨ cần xoá (xoá tay thì hỏi anh; còn lại tạo mới).
- Máy 1 CẤM `--den B4` / `--den B5Q` / `--from B4` (tốn tiền thật; code chặn cứng `chan_buoc2_may1`).
- Cổng `review_may3.cong()` chặn B5W/dong_goi khi chưa `received` hoặc script đổi sau khi nhận → chạy lại `--nhan`, không đi cửa sau.
- Không sửa tay `script.txt` — mọi sửa qua `viec_tay.txt` → Opus, hoặc anh sửa ở `jobs\`.
- Ảnh / Grok chạy bằng Bash `run_in_background`, báo giờ dự kiến rồi dừng lượt; cấm `tail` log định kỳ.
- Báo cáo: chữ Nhật kèm dịch Việt; đường dẫn tuyệt đối; dòng cuối nói tool nào đang chạy + dự kiến xong.
