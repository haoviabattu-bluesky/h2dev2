# LANE F `teinengo-real` — BẮT ĐẦU TẬP 9 `ep09-shuu3-shigoto` (viết 2026-10-01, sau khi giao máy 2 tập 8)

> **File này THẮNG `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\HUONG_DAN_TAP_TIEP_THEO.md`** (file tool tự sinh bảo "tạo hồ sơ + viết"
> — SAI với tập 9: kịch bản tập 9 ĐÃ KHOÁ từ 27/09).
> Tab mới: mở đầu báo cáo bằng `@lane:teinengo-real`, đọc HẾT file này. Chạy mọi lệnh tại `E:\CLAUDE\YOUTUBE\h2dev`.

## 0. THAM SỐ
| | |
|---|---|
| Thư mục `<D>` | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep09-shuu3-shigoto` |
| Dòng sheet | 10 (tab `F-teinengo-real`) |
| Tiêu đề | 【漫画】65歳で年金生活を始めた俺…週3日の駐車場の仕事が人生を変えた理由 (tôi 65 tuổi bắt đầu sống bằng lương hưu… lý do công việc bãi đỗ xe 3 ngày/tuần đổi đời tôi) |
| Kịch bản | LOCK PASS 27/09 (Sol 4 lượt, 2 patch, `manual_after_many_fix_no_remake`), 6.444 chữ. Hook khoá kiểu CŨ (Sol), chưa qua máy 3 |

## 1. LUỒNG (anh chốt 30/09 → 01/10)
1. Gửi máy 3: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --share --profile teinengo-real --slug ep09-shuu3-shigoto`
   (thử `--dry` trước; ô D10 phải trống/đang chờ mới ghi). Báo anh đường dẫn `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\F-teinengo-real\ep09-shuu3-shigoto\script.txt` rồi DỪNG.
2. Anh sửa xong (D10 = `Đã sửa kịch bản`) → làm y hệt tập 8 theo `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md`. Mẫu chạy thật: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep08-kodomo-enjo\`.

## 2. ĐIỂM MỚI TỪ TẬP 8 (bắt buộc)
- **Giọng chậm + nghỉ (anh chốt 01/10):** profile Lane F đã `voice.speed` 0.90 + `voice.pace: true`. `profiles.char_rate_at` + `prompt_doan._n_anh` giờ tự quy đổi theo `voice.speed` (tập 8: 129 → 136 ảnh). Không đổi lại.
- **Ảnh khớp tuổi:** `characters.json` + REF theo `E:\CLAUDE\YOUTUBE\h2dev\docs\QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md` (look ghi % tóc bạc + nếp nhăn bằng nét vẽ + "must read as …"). Tập 8 REF đo 60/60 cho tuổi 63/61 → PASS.
- **Hook tới hết cao trào:** profile đã `script.hook.den_cao_trao: true`. `review_may3 --nhan` rút hook theo SỐ ĐOẠN hook cũ → hay cắt thiếu: tự khoá lại hook tới hết khối hook anh viết (tập 8 khoá tới 「俺は、どこで間違えたのか。」, 183 chữ, 9 cảnh, 39s).
- **Viết `<D>\hook\ghi_chu_canh.txt`** (gọi điện hay gặp mặt) TRƯỚC `hook_storyboard.py --force`.
- **Nhạc nền hook:** dùng lại `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\_bgm\piano_cand1.mp3` (Suno piano nhẹ, 190s) — cắt đoạn liền ≥ độ dài hook, fade-in 2s, -16 LUFS → `<D>\hook\sfx\99_nhac_piano.mp3`; `hook_timeline.json`: `"sfx": []` + `"nen"` (khuôn tập 8). Cấm SFX đồ vật.
- **Grok:** `grok_1tk.py` PHẢI nhận đường dẫn TUYỆT ĐỐI (tương đối = mất 1 tài khoản). Sau khi xong, Chrome GPM còn mở thì chỉ xem profile nào — profile không phải của mình (tập 8 thấy `fc3737ea…` của việc khác) thì KHÔNG đụng.
- **TTS hook "ĐỌC THIẾU"** lặp lại → gọi thẳng `openspeaker_tts.synthesize` lưu mp3+srt, tự `kiem_phu_chu`, rồi `tts.chuan_muc` (mục 3 runbook `teinengo-real_TAP_TIEP.md`).
- Tiêu đề/mô tả/thumbnail: TẮT toàn dự án từ 01/10 (tool `goi_title` tự bỏ qua).

## 3. ĐIỂM SOI RIÊNG TẬP 9
- **Trùng kết với tập 6 + tập 8:** tập 6 và tập 8 đều kết bằng việc ở **bãi giữ xe đạp (駐輪場)**; tập 9 là **bãi đỗ xe ô tô (駐車場)** làm TRỤC CHÍNH. Khi anh soát nên phân biệt rõ hình ảnh (ô tô, barrier, chòi gác) — prompt ảnh tránh vẽ xe đạp.
- Số chế độ (在職老齢年金 — chế độ giảm lương hưu khi vừa đi làm vừa nhận) chỉ dùng số có trong `<D>\series_ctx.txt`.
- Tuổi hiện tại 65 (tiêu đề "65歳") — REF phải nhìn 62–68, hook không được ghi tuổi khác 65.
