# KẾ HOẠCH GHÉP HOOK CHO CÁC TẬP SATORI CHƯA ĐĂNG (2026-09-24)

Lane `satori-jp-obaa` · tab sheet `Lopezzapa68` · `script.hook.visual = anh_ai_ref_grok`.
Phạm vi: các tập **cột J (ĐÃ ĐĂNG) còn rỗng** = STT **5, 8, 9, 10, 12, 13**.

---

## PHẦN 1 — KIỂM LẠI PHƯƠNG ÁN ĐÃ CHẠY (`ep3-sougi`)

### 1a. Bốn phép kiểm bắt buộc (`docs/QUY_TAC_VIDEO_HOOK.md` §2) — ĐẠT HẾT

| Phép kiểm | Số đo thật 2026-09-24 | Kết luận |
|---|---|---|
| Mức tiếng | hook 0–26s: **−21,7 LUFS** · thân 40–160s: **−21,6 LUFS** → lệch **0,1 LU** | ĐẠT (ngưỡng 0,2) |
| Độ phân giải + fps | cả hai 1920×1080 · 30 fps · yuv420p(tv, bt709) | ĐẠT |
| Khung đen điểm nối | `blackdetect d=0.05 pix_th=0.10` cửa sổ 20–35s → **0 dòng** | ĐẠT |
| Tổng thời lượng | 29:58,66 + 26,47 = 30:25,13 ≈ **30:25,16** thật | ĐẠT (không mất khung) |

File: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\ep3-sougi\final_with_hook.mp4` (628 MB · 30:25).
Ghép bằng concat demuxer, danh sách ở `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\ep3-sougi\_noi.txt`
(`hook/hook_final_JP_lv.mp4` + `final.mp4`).

### 1b. NĂM ĐIỂM YẾU PHẢI VÁ TRƯỚC KHI NHÂN BẢN

1. **⛔ Hook đang nằm trên một bản video KHÔNG dùng được.** `ep3-sougi\final.mp4` là bản dựng
   **07/09** (606 MB · 29:58), thumbnail đề *静子の終活ノート③* — branding cũ, **không có dòng nào
   trong sheet**. Bản thật sẽ đăng của cùng câu chuyện là STT5 →
   `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep05-simbot2-05-Hhe56wqubbU\final.mp4` (dựng 17/09, 29:41,
   kịch bản `simbot2-05-Hhe56wqubbU\script.txt` khác hẳn). ⇒ Về kỹ thuật phương án đã chứng minh,
   nhưng **chưa có tập nào thật sự có hook**. Việc đầu tiên là làm lại hook cho ĐÚNG bản ep05.
   Tin tốt: **văn bản hook dùng lại được gần như nguyên** (cùng câu chuyện, cùng lời hứa
   「わしが死んでも葬式はするな」 trong tiêu đề ep05) — chỉ phải vẽ lại ảnh theo `_ref/_ref2` của ep05
   và sinh clip mới, vì mặt nhân vật hai bản khác nhau.
2. **Không có script dựng lại được.** Lane A có
   `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\hook\_dung_hook.py`;
   satori **không có** — 7 bước cắt/ghép/nắn tiếng làm bằng lệnh rời, chạy lại là dựng tay lần nữa.
   ⇒ Việc #1 của tập pilot: viết `hook\_dung_hook.py` cho satori (bảng cảnh ở đầu file, đọc
   `hook_timeline.json`), để 5 tập sau chỉ đổi slug.
3. **Hook là bản PHÓNG TO từ 720p24.** Clip Grok gốc `clip/clip_01.mp4` = **1280×720 · 24 fps**
   (gói Pro khoá 1080p), `_seg/seg_01.mp4` đã thành 1920×1080 · 30 fps. Nghĩa là 26 giây đầu —
   đúng đoạn quyết định giữ người xem — kém nét hơn thân video (thân dựng từ ảnh 2560×1440) và có
   nhân đôi khung do 24→30 fps. **Không sửa được trong Grok**; chấp nhận, nhưng đừng để cảnh nào
   trong hook là cận mặt lớn hết khung (chỗ lộ mờ rõ nhất).
4. **`hook/source.json` của ep3-sougi rỗng** (`video_hook_verdict: khong_soi_duoc`,
   `promise_match: NA`) ⇒ H1/H3 bị bỏ qua, hook viết ra **không được đối chiếu với hook kênh mẫu**.
   Với 5 tập tới thì có video nguồn simbot2 thật (ep09 đã có `hook\source.json` + `frames\` từ
   23/09) — chạy đủ H1→H4 được, đừng bỏ.
5. **Thiếu `title.txt`/`promise.txt`** ở cả 6 tập ⇒ cổng khớp lời hứa của Sol chấm hook trong chân
   không. Tiêu đề thật đang ở **cột E của sheet** và dòng 1 của
   `CHANEL\Lopezzapa68\<ep>\TIEU_DE_MO_TA.txt`. ⇒ Ghi `title.txt` + `hook\promise.txt` **trước H4**.

---

## PHẦN 2 — HIỆN TRẠNG 6 TẬP (đo 2026-09-24)

| STT | slug | final.mp4 giao hàng | Tiêu đề | Thumb | img/ | REF master | hook/ |
|---|---|---|---|---|---|---|---|
| 5 | `simbot2-05-Hhe56wqubbU` | ✅ 29:41 (17/09) | ✅ trong TIEU_DE_MO_TA | ✅ | 90 | `_ref` `_ref2` | ❌ |
| 8 | `simbot2-08-Kb5Ej4ZNBgQ` | ✅ (17/09) | ✅ | ✅ | 115 | `_ref` | ❌ |
| 9 | `simbot2-09-rNGGuRG-wu0` | ✅ (21/09) | ✅ | ✅ | 109 | `_ref` `_ref_kunio` | 🔄 chỉ H1 |
| 10 | `simbot2-10-66weQbaUZuk` | ✅ (21/09) | ✅ | ✅ | 119 | `_ref` `_ref_etsuko` | ❌ |
| 12 | `simbot2-12-FBkmqYvEyXQ` | ✅ (21/09) | ✅ | ✅ | 125 | `_ref` `_ref_haruyoshi` | ❌ |
| 13 | `simbot2-13-djMUfpGoUQI` | ❌ **chưa dựng** | ❌ | ❌ | 106 | `_ref` `_ref_kimiyo` | ❌ |

⇒ **5 tập ghép hook được ngay**; **ep13 phải xong video trước** (hiện mới có ảnh, chưa qua bước 3),
nên xếp cuối và làm hook song song trong lúc chờ.

---

## PHẦN 3 — 8 BƯỚC CHO MỖI TẬP (lệnh thật, đổi `<SLUG>`)

Thư mục làm việc: `E:\CLAUDE\YOUTUBE\h2dev\pipeline`

```
:: B-0  Neo lời hứa (LÀM TRƯỚC, nếu thiếu là Sol chấm hook trong chân không)
::      lấy dòng 1 của E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\<ep>\TIEU_DE_MO_TA.txt
::      ghi vào ...\assets\satori_jp\<SLUG>\title.txt  và  ...\<SLUG>\hook\promise.txt (1 câu)

:: B-1  H1→H4: bóc hook kênh mẫu, viết 3 hook, cổng tất định + Sol, KHOÁ sha256
py -3.13 hook_stage.py --profile satori-jp-obaa --slug <SLUG> --mode repair

:: B-2  Lồng tiếng hook (BẮT BUỘC qua cổng PHỦ CHỮ — 3/4 lượt ai33 từng nuốt trọn 1 câu)
::      xuất hook_voice.mp3 + hook_voice.srt, rồi sinh hook_timeline.json từ mốc câu

:: B-3  Prompt ảnh hook + vẽ, KHOÁ MẶT bằng master của CHÍNH tập
py -3.13 gpti2_edit.py --ref ..\assets\satori_jp\<SLUG>\_ref\001.png ^
                       --ref2 ..\assets\satori_jp\<SLUG>\_ref2\001.png ...

:: B-4  Sinh clip Grok 6s/cảnh (0đ, quota Pro — profile E:\CLAUDE\YOUTUBE\GROK_PROFILE cổng 9334)
cd E:\CLAUDE\YOUTUBE\GROK_VIDEO && py -3.13 grok_batch.py --jobs ...\hook\grok_jobs.csv --gap 5

:: B-5  Cắt clip theo mốc câu → nối → cháy phụ đề JP → nắn mức tiếng về mức thân video
::      (đây là việc _dung_hook.py sẽ làm; tập pilot viết script này)

:: B-6  Ghép: concat demuxer, KHÔNG encode lại thân video
::      _noi.txt =  file 'hook/hook_final_JP_lv.mp4'  /  file 'final.mp4'

:: B-7  Nghiệm thu 4 phép kiểm (mức tiếng · fps+độ phân giải · khung đen · tổng thời lượng)
::      rồi copy final_with_hook.mp4 vào CHANEL\Lopezzapa68\<ep>\ và ghi cột K
```

**Thứ tự chạy:** ep08 (pilot, viết `_dung_hook.py` + đo tiền/thời gian thật) → ep09 → ep10 → ep12 →
ep05 (hook dùng lại văn bản của ep3-sougi sau khi soi lại với tiêu đề ep05) → ep13 (chờ video).

**Ước lượng/tập** (số thật đo từ ep3-sougi, 7 cảnh · 26,5s): 7 ảnh gpti2 + 7 clip Grok
(17:34→17:40 = **6 phút** cho 7 clip, ~50 s/clip, **0đ**) + 1 lượt TTS ~260 credit.
Tiền ảnh chưa đo thật (manifest không ghi) — pilot sẽ ghi lại. Thời gian trọn tập, nếu không phải
làm lại: **35–50 phút**; ep3-sougi mất ~1,5 giờ vì vừa làm vừa dò.

---

## PHẦN 4 — HAI ĐIỂM CẦN ANH CHỐT

1. **Ai ghép (bước 3)?** `CLAUDE.md` chỉ cho Lane A tự render; satori thì ep3-sougi máy 1 đã ghép
   (anh đồng ý tại chỗ). Giữ nguyên cách đó cho 6 tập này, hay đóng gói `hook\` giao máy 2 ghép?
2. **`ep3-sougi` xử lý sao?** Bản dựng 07/09 + `final_with_hook.mp4` 628 MB không có trong sheet,
   cùng câu chuyện với ep05 đã dựng lại. Giữ làm bản mẫu tham chiếu, hay xoá để lấy lại ~1,2 GB?
