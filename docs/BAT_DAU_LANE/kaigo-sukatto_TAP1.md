# GIAO VIỆC TAB MỚI — LANE O `kaigo-sukatto` · TẬP 1 `ep01-jaa-yamemasu`

> Viết 2026-09-30 bởi tab dựng Lane O. Tab mới: đọc HẾT file này trước, mở đầu báo cáo bằng `@lane:kaigo-sukatto`.
> Làm liền một mạch, KHÔNG dừng hỏi, trừ các điểm DỪNG ở mục 5. Soát kịch bản = **máy 3/anh** (ChatGPT web TẮT).
> Tên lane tạm "Lane-O" — chưa có kênh. Không tự setup kênh, không chạy `channel_branding.py`.

## 0. ĐÃ KIỂM (2026-09-30)
Profile `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\kaigo-sukatto.json` nạp OK · char_rate 316,7 (mượn Lane K, cùng VOICEVOX) · gate khai đủ ·
cổng S1L = 0 lỗi · S1Q hồ sơ tập 1 = 0 lỗi · tab sheet `Lane-O` dòng 2 = tập 1.

## 1. ĐỌC TRƯỚC (đúng thứ tự)
1. `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_O.md` — runbook lane (§0, §2, §5).
2. `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\kaigo-sukatto\COMMENT_INSIGHT.md`.
3. Chỉ khi cần hiểu vì sao: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\KENH_GOC_10\PHAN_TICH_10_VIDEO_VA_AP_DUNG_KAIGO.md` §2–§3.

## 2. TẬP 1 LÀ GÌ (sheet `Lane-O` dòng 2 là nguồn chân lý)
| Mục | Giá trị |
|---|---|
| Tiêu đề (B2) | 【漫画】「じゃあ、辞めます」が口ぐせの介護士が、人手不足の施設で3回目に言った結果… (Nhân viên chăm sóc có câu cửa miệng "Vậy tôi nghỉ" — kết quả khi nói lần thứ 3 ở cơ sở thiếu người) |
| Video gốc (khung) | `JmhcsfXGmfU` — 416.017 view, video mạnh nhất kênh mẫu |
| Thư mục | `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu\` |
| Hồ sơ ĐÃ CÓ | `competitor.txt` + `competitor.segments.json` (transcript video gốc) · `series_ctx.txt` ([D1] 3:1 + ユニットリーダー · [D2] tắm ≥2 lần/tuần · [D3] 民法627条 2 tuần · [D4] ヒヤリハット/事故報告; QUY ƯỚC 3 lần câu cửa miệng, người thế chỗ, cụ không bị hại) · `title.txt` · `promise.txt` |
| Bối cảnh | 1 ユニット型特養 (viện dưỡng lão đặc biệt kiểu unit) ngoại ô; nhân vật chính nam cuối 30, 9 năm ở đây |
| ⛔ Không chép | 日曜当番, 在宅の神田さん, trận bóng của con quản lý, câu kết 「あの店でその言葉を聞く人はもういない」 |

## 3. LÀM ĐÚNG THỨ TỰ (lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev`)

**A. SOI HỒ SƠ (tay, ~5')** — đọc `series_ctx.txt`, `title.txt`, `promise.txt`. Chỉ sửa nếu thấy sai; mọi số quy định phải có trong `[Dn]`.
Cột C2 đã ghi đường dẫn thư mục.

**B. VIẾT + KHOÁ** (hook Fable 2 phương án → Fable 5.1 viết thân → Opus 5 vá → LOCK) — chạy NỀN (`run_in_background`), báo giờ dự kiến (~20–40') rồi dừng lượt:
```bat
py -3.13 -X utf8 pipeline\make_video.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --den B3G
```
Máy tự DỪNG sau LOCK: chép `script.txt` vào `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\Lane-O\ep01-jaa-yamemasu\` + ghi D2 = `Chờ kiểm tra kịch bản`.
→ **DỪNG, báo anh đường dẫn đó.** (ESCALATE/lỗi → đọc đuôi log, xử theo `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §9.)

**C. SAU KHI ANH SỬA** (D2 = `Đã sửa kịch bản`) — ⭐ tab mới CHỈ đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kaigo-sukatto_TAP1_NHAN_MAY3.md` (gói sẵn C→G, đường dẫn đầy đủ). Gốc chung: `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md`:
```bat
py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile kaigo-sukatto --slug ep01-jaa-yamemasu
```
Soi 1 lượt bản nhận theo `SOP_LANE_O.md` §5 (chỉ báo, không sửa `script.txt`).

**D. CAST + GIỌNG** — viết `characters.json` theo `SOP_LANE_O.md` §2 mục D (shu = nhân vật chính + `kuchiguse: 「じゃあ、辞めます」`;
ユニットリーダー nữ; パート nữ; người thế chỗ; 施設長; 1 cụ + người nhà nếu có thoại) →
```bat
py -3.13 -X utf8 pipeline\gan_vai.py --profile kaigo-sukatto --slug assets\O-kaigo-sukatto\ep01-jaa-yamemasu
```

**E. PROMPT ẢNH** (chỉ `--only`):
```bat
py -3.13 -X utf8 pipeline\make_video.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --only B5P
```
Kiểm `img_prompts.txt` có dòng `@CAST:` cho cảnh có người; không cảnh ngã/thương tích.

**F. HOOK** — y `SOP_LANE_O.md` §2 mục F: storyboard → master vai → ảnh hook → QC → clip Grok 6 giây → QC clip → SFX →
```bat
py -3.13 -X utf8 pipeline\hook_storyboard.py --profile kaigo-sukatto --slug ep01-jaa-yamemasu --force
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\ep01-jaa-yamemasu --profile kaigo-sukatto
```
Viết hết `<<CẦN NGƯỜI>>` trong `HOOK_TAP.md` rồi chạy lại với `--kiem`. Xem clip Grok BẰNG MẮT (Grok từng trả clip lạc đề — gặp là làm lại clip đó).
Xong kiểm 0 Chrome GPM còn sống (chỉ đóng đúng PID của GPM, không kill Chrome chung).

**G. GIAO MÁY 2** (tự ghi D2 = `Done`, H2 = `cần ảnh (N ảnh, ~Xđ)`):
```bat
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job kaigo-sukatto ep01-jaa-yamemasu
py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list kaigo-sukatto
```
Đọc lại `_BANGIAO.txt`. KHÔNG gọi dự án TITLE (kênh chưa có, `title_auto=false`) — báo anh là còn thiếu tiêu đề/thumbnail.

## 4. KHÔNG LÀM LẠI
Profile · COMMENT_INSIGHT · SOP · hồ sơ tập 1 · tab `Lane-O` A2:B11/K2:K11 · router CLAUDE.md/DANH_BA — đã xong 30/09.

## 5. ĐIỂM DỪNG / BẪY
- DỪNG sau bước B (chờ anh sửa kịch bản) — đúng luật 30/09.
- Máy 1 CẤM `--den B4`/`--den B5Q`/`--from B4` (tốn tiền thật; code chặn cứng `chan_buoc2_may1`).
- Cấm 2 tiến trình `make_video` cùng slug — kiểm PID trước khi chạy lại.
- Không sửa tay `script.txt` sau khoá — mọi sửa qua `viec_tay.txt` → Opus, hoặc anh sửa ở `jobs\`.
- Máy 2 chạy từ bundle: đổi profile/code thì chạy lại `--bundle --profile-list kaigo-sukatto`.
- Báo cáo: mọi chữ Nhật kèm dịch Việt; đường dẫn tuyệt đối; dòng cuối nói tool nào đang chạy + dự kiến xong.
