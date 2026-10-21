✅ ĐÃ LÀM 2026-10-01 — giao máy 2 xong (E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\L-shakai-no-naze\ep07-kuruma-banare)
# LANE INBOX → `@lane:shakai_no_naze` (Lane L · 社会のなぜ研究室 — Phòng nghiên cứu Vì sao của xã hội)

> **Từ:** tab Lane L ngày 2026-09-30 · **Việc:** nhận kịch bản TẬP 7 anh/máy 3 đã sửa → làm tiếp tới giao máy 2.
> Tab mới: đọc HẾT file này, rồi CHỈ đọc thêm `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` (§2–§4) và mục §2 + §5
> của `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_L.md`. Không đọc lại CHANNEL_DNA/profile, không viết lại kịch bản.

## 0. TẬP ĐANG CHỜ
| Mục | Giá trị |
|---|---|
| Tập | **STT 7** — なぜ今の若者は車を買わなくなったのか【漫画】 (Vì sao giới trẻ bây giờ không mua ô tô nữa) |
| Slug | `ep07-kuruma-banare` |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep07-kuruma-banare` |
| File anh sửa | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\L-shakai-no-naze\ep07-kuruma-banare\script.txt` (hook = đoạn đầu) |
| Sheet | tab `L-shakai-no-naze`, **dòng 8** — cột D đang `Chờ kiểm tra kịch bản`; anh sửa xong sẽ đổi thành `Đã sửa kịch bản` |
| Trạng thái 30/09 | bản máy viết: 5.064 chữ ≈ 16,4', lock PASS; hook cao trào (Fable 5.1, 2 phương án, Sol chọn 1, 173 chữ) |
| Nhân vật | 平田翔太 (Hirata, 27, sales không có xe — **main**) · 店長 大迫 (Ōsako, 56) · さくら (Sakura, 23, lễ tân — người hỏi) · 佳奈 (Kana, 24, khách, y tá) · 母 của 佳奈 · 本部 課長 堀 (Hori, 48, nữ — giải thích số liệu) · con trai 大迫 (25, gọi điện) |
| Tư liệu số | `...\ep07-kuruma-banare\series_ctx.txt` [D1]–[D6] (JAMA 2025, 総務省 小売物価統計, カーシェア財団) |

⚠️ **ĐỪNG nhầm** thư mục `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep07-taishoku-daikou` (退職代行 — dịch vụ xin nghỉ việc hộ):
KHÔNG phải tập 7 của sheet, phạm luật §5.5 → không nhận, không giao. `ep08`–`ep10` trong `assets\shakai_no_naze\` cũng lệch sheet
(sheet: 8 = 年賀状 thiệp năm mới · 9 = 転勤 chuyển công tác · 10 = 燃え尽き kiệt sức). **Tập N = dòng STT N của sheet.**

## 1. KIỂM ĐÃ SỬA CHƯA
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --trang-thai --profile shakai_no_naze
```
Dòng 8 chưa `Đã sửa kịch bản` → báo anh 1 dòng rồi DỪNG (chỉ khi anh bảo "cứ nhận" mới thêm `--force` ở bước 2).

## 2. NHẬN BẢN SỬA (0 LLM)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --nhan --profile shakai_no_naze --slug ep07-kuruma-banare
```
- CHẶN (ngắn <70% ngân sách / số ngoài `series_ctx.txt`) → báo anh lý do, KHÔNG sửa hộ.
- Mở `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep07-kuruma-banare\hook\hook_locked.txt` so với đoạn đầu `script.txt`
  (hook có 2 dòng: câu thoại 「車も持ってない奴に、車が売れるか」 + đoạn kể). Lệch ranh giới → khoá lại tay theo lệnh ở
  `NHAN_KICH_BAN_MAY3.md` §2. Tuyệt đối không sửa `script.txt`.
- Lớp 3 nhanh (luật §5 SOP_LANE_L): mọi số xã hội nằm trong [D1]–[D6]; câu なぜ được trả lời; Sakura chỉ là người hỏi;
  không trả thù/hả hê. Có lỗi → báo anh, không tự sửa.

## 3. LÀM TIẾP (đúng thứ tự — lệnh chi tiết SOP_LANE_L §2)
```bat
cd /d E:\CLAUDE\YOUTUBE\h2dev
:: A. characters.json (tay, sau khi đọc bản đã sửa): sakura theo khuôn §0d SOP + mọi vai có thoại/≥2 cảnh
::    {id,name,vai,age,gender,look,ref:true,voice:{voice_id}} — voice_id lấy trong voice.cast_bank; 平田 "main":true;
::    sakura khai "inner_voice": true. Mẫu: E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep06-fukugyou-kyuuzou\characters.json
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\gan_vai.py --profile shakai_no_naze --slug E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep07-kuruma-banare
:: B. prompt ảnh thân (CHỈ --only; cấm --from/--den B4/B5 ở máy 1)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile shakai_no_naze --slug ep07-kuruma-banare --only B5W
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile shakai_no_naze --slug ep07-kuruma-banare --only B5P
:: C. hook — máy 1 làm trọn HÌNH (docs\QUY_TAC_VIDEO_HOOK.md): storyboard dựng lại theo hook đã nhận
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_storyboard.py --profile shakai_no_naze --slug ep07-kuruma-banare --force
::    → ảnh hook @CAST (anh_hook.py <thư mục tập>\hook — Google Flow Ultra → 9router → gpti2) → QC → clip Grok (tools\hook_lane_g\grok_da_luong.py, đa luồng 5–10, chạy nền)
::    → qc_hook_clip.py → SFX hook → hook_timeline.json THEO SỐ CÂU (shots[].cau=[a,b], sfx[].cau + lech; máy 1 KHÔNG lồng giọng hook)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep07-kuruma-banare --profile shakai_no_naze
:: D. SFX thân (Opus chọn chỗ đặt tiếng → sfx_plan.txt; thiếu file này dong_goi DỪNG)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\sfx_than.py --profile shakai_no_naze --slug E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep07-kuruma-banare --plan
:: E. giao máy 2 (tự ghi D8 = Done, H8 = cần ảnh; tự gọi TITLE-RESEARCH làm tiêu đề/mô tả/thumbnail)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --job shakai_no_naze ep07-kuruma-banare
```
- Ảnh/Grok/TTS chạy bằng Bash `run_in_background`, báo giờ dự kiến rồi dừng lượt (không tail log định kỳ).
- Máy 1 KHÔNG vẽ ảnh thân, KHÔNG lồng giọng, KHÔNG dựng video (bước 2/3 là máy 2).
- Mẫu hoàn chỉnh để đối chiếu (hook/, _ref_*, vai.txt, sfx_plan.txt, HOOK_TAP.md): `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep06-fukugyou-kyuuzou`.

## 4. XONG → BÁO ANH (đường dẫn tuyệt đối) + cập nhật mục 2 TRẠNG THÁI của
`E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\shakai_no_naze.md`, rồi đánh dấu file này `✅ ĐÃ LÀM <ngày>` ở dòng đầu.
