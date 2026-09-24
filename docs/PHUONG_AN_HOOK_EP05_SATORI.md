# PHƯƠNG ÁN THÊM HOOK — TẬP 5 SATORI (`simbot2-05-Hhe56wqubbU`) — 2026-09-24

Sheet `Lopezzapa68` STT5 · cột J (ĐÃ ĐĂNG) rỗng · video đã giao, chưa đăng.
Bản video của record: `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep05-simbot2-05-Hhe56wqubbU\final.mp4`
Thư mục tài sản: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-05-Hhe56wqubbU\`

---

## 1. ĐO THẬT TẬP 5 (2026-09-24)

| Hạng mục | Số đo | Ý nghĩa cho hook |
|---|---|---|
| Thời lượng | **29:41,23** | ghép hook 26–30s → ~30:08 |
| Hình | 1920×1080 · 30 fps · yuv420p(tv, **bt709**) · 1.372 kb/s | hook phải ra ĐÚNG bộ này |
| Tiếng | AAC 44.1 kHz stereo · **−16,0 LUFS** (60–180s), −16,3 toàn bài | ⚠️ xem §2.1 |
| Phụ đề cháy | **KHÔNG** (soi khung ở giây 900: sạch chữ) | ⚠️ xem §2.2 |
| Phụ đề rời | `phude.srt` giao kèm để bật CC | ⚠️ xem §2.3 |
| Giọng | `voice.json`: `elevenlabs_rDiGqdvxRVKhplqZE31x` "Papa Ji – Deep, Wise Japanese", nam trầm, `speed 0.92`, `fx old-med` | hook đọc bằng ĐÚNG bộ này |
| Ảnh khoá mặt | `_ref\001.png` bà 72 tuổi · `_ref2\001.png` ông 79 tuổi trồng hạt dẻ | master REF-LOCK cho ảnh hook |
| Ảnh thân | 91 tấm trong `img\` | không đụng tới |

## 2. BỐN ĐIỂM KHÁC ep3-sougi — KHÔNG ĐƯỢC BÊ NGUYÊN FILE CŨ SANG

### 2.1 Mức tiếng lệch 5,7 LU
Hook cũ nắn về **−21,7 LUFS** (khớp thân ep3-sougi). Tập 5 lại ở **−16,0 LUFS** — to hơn hẳn.
Dán nguyên hook cũ vào = 26 giây đầu **nhỏ tiếng rõ rệt** rồi video mới vống lên. Phải nắn hook về
−16,0 LUFS đo từ chính `CHANEL\Lopezzapa68\ep05-simbot2-05-Hhe56wqubbU\final.mp4`, lệch cho phép ≤ 0,2 LU.

### 2.2 Tập 5 KHÔNG cháy phụ đề, hook cũ thì CÓ
`hook_final_JP_lv.mp4` của ep3-sougi có chữ Nhật cháy vào hình. Tập 5 sạch chữ (đã soi khung).
Ghép vào là 26 giây đầu có chữ rồi tắt ngóm — lộ ngay là hàng chắp. ⇒ Hook tập 5 **dựng bản KHÔNG
cháy chữ**.

### 2.3 Ghép hook thì phải DỊCH CẢ FILE PHỤ ĐỀ
Vì lane không cháy chữ, `phude.srt` là thứ duy nhất mang phụ đề tới người xem. Chèn 26 giây vào đầu
mà không dịch mốc thì **toàn bộ CC lệch 26 giây suốt 30 phút**. Đây là cái bẫy không có ở ep3-sougi
(bản đó chưa giao CC). Phải: dịch mọi mốc `+<đúng thời lượng hook>` rồi chèn các dòng lời hook lên
đầu, và kiểm dòng cuối khớp thời lượng video mới.

### 2.4 Mặt nhân vật phải là mặt của TẬP 5
Ảnh hook cũ sinh từ REF của ep3-sougi. Bắt buộc vẽ lại 7 ảnh hook bằng `_ref\001.png` + `_ref2\001.png`
của chính tập 5, nếu không người xem thấy hai ông bà khác mặt ngay sau 26 giây.

## 3. VÌ SAO TẬP NÀY RẤT ĐÁNG THÊM HOOK

30 giây mở đầu hiện tại (đo từ `voice.srt`): **17,7 giây đầu là tự giới thiệu** —
「私は岐阜県中津川市で、葬祭ディレクターを、三十二年、務めております。田中修一と申します、今年で六十七になります」
(*Tôi làm giám đốc tang lễ ở Nakatsugawa, Gifu, 32 năm. Tôi tên Tanaka Shuichi, năm nay 67 tuổi*).
Đúng ba thứ `NGUYEN_TAC_HOOK_GOI_DANG.md` cấm trong 30 giây đầu: **chào hỏi · tự giới thiệu · khai
tuổi**. Mâu thuẫn của câu chuyện (người 40 năm không bỏ đám tang nào lại cấm làm đám tang cho mình)
mãi phút thứ 2 mới xuất hiện.

## 4. VĂN BẢN HOOK — TÁI SỬ DỤNG ĐƯỢC, NHƯNG PHẢI CHẤM LẠI

Hook đã khoá của ep3-sougi (cùng câu chuyện) đối chiếu với tập 5:

| Chi tiết trong hook | Tập 5 | |
|---|---|---|
| 五十年、連れ添った夫 (chồng 50 năm) | TIEU_DE_MO_TA: 五十年連れ添った七十九歳のご主人 | ✅ khớp |
| 四十年、他人様の通夜を欠かさない (40 năm không bỏ đám nào) | tiêu đề: **40年**香典を欠かさぬ | ✅ khớp |
| 財産は、栗畑一つ (tài sản chỉ một vườn hạt dẻ) | `_ref2` = ông nông dân trồng hạt dẻ | ✅ khớp |
| Không nêu tên nhân vật | tập 5 tên khác (Chiyoko 72) | ✅ không vướng |

⇒ Dùng được. Nhưng **vẫn chạy đủ H1→H4** (`--mode repair`) thay vì bê thẳng, vì hai lý do: (a) tập 5
**có video nguồn thật** (simbot2 `Hhe56wqubbU`) nên H1/H3 soi được hook kênh mẫu — thứ ep3-sougi
thiếu hẳn; (b) tiêu đề tập 5 hứa **「2つの現実」** (2 sự thật) — Sol phải chấm hook có dẫn đúng vào
lời hứa đó không. Bản cũ đưa vào làm **ứng viên thứ 4** để đối chiếu, thắng thì dùng.

## 5. BẢY BƯỚC (lệnh thật, chạy tại `E:\CLAUDE\YOUTUBE\h2dev\pipeline`)

```
:: B0 — neo lời hứa (thiếu thì Sol chấm hook trong chân không)
::   title.txt  <- dòng 1 của CHANEL\Lopezzapa68\ep05-simbot2-05-Hhe56wqubbU\TIEU_DE_MO_TA.txt
::   hook\promise.txt <- 1 câu: người 40 năm không bỏ đám tang nào lại cấm làm đám tang cho mình,
::                       lý do nằm ở việc ông chưa từng đụng đũa vào mâm cơm tang

:: B1 — H1..H4: bóc hook video nguồn, viết 3 hook, cổng tất định + Sol, khoá sha256
py -3.13 hook_stage.py --profile satori-jp-obaa --slug simbot2-05-Hhe56wqubbU --mode repair

:: B2 — lồng tiếng hook: ĐÚNG voice_id/speed/fx trong voice.json, BẮT BUỘC qua cổng phủ chữ 95%
::      -> hook\hook_voice.mp3 + hook_voice.srt -> sinh hook_timeline.json theo mốc CÂU

:: B3 — 7 ảnh hook, khoá mặt bằng master của CHÍNH tập 5
py -3.13 gpti2_edit.py --ref ..\assets\satori_jp\simbot2-05-Hhe56wqubbU\_ref\001.png ^
                       --ref2 ..\assets\satori_jp\simbot2-05-Hhe56wqubbU\_ref2\001.png ...

:: B4 — clip Grok 6s/canh (0d, quota Pro; profile E:\CLAUDE\YOUTUBE\GROK_PROFILE cong 9334)
cd E:\CLAUDE\YOUTUBE\GROK_VIDEO
py -3.13 grok_batch.py --jobs ..\h2dev\assets\satori_jp\simbot2-05-Hhe56wqubbU\hook\grok_jobs.csv --gap 5

:: B5 — dựng hook: cắt theo mốc câu -> nối -> KHÔNG cháy chữ -> nắn về -16,0 LUFS
::      (việc của hook\_dung_hook.py — tập này viết luôn script đó để 5 tập sau dùng lại)

:: B6 — ghép + dịch phụ đề
::      _noi.txt: file 'hook\hook_final.mp4' / file '<CHANEL>\ep05...\final.mp4'  (concat, -c copy)
::      phude_hook.srt = lời hook + (phude.srt dịch +<thời lượng hook>)

:: B7 — nghiệm thu 5 phép kiểm rồi mới giao
```

**Nghiệm thu (phải ĐẠT hết mới coi là xong):** ① mức tiếng hook vs thân lệch ≤ 0,2 LU · ② 1920×1080 ·
30 fps · bt709 khớp · ③ `blackdetect` quanh điểm nối = 0 · ④ tổng thời lượng = 29:41,23 + thời lượng
hook (không hụt khung) · ⑤ **dòng phụ đề đầu tiên của thân video trong `phude_hook.srt` bắt đầu đúng
bằng thời lượng hook + 0,5 s**, dòng cuối ≤ tổng thời lượng.

## 6. CHI PHÍ · THỜI GIAN · RỦI RO

- 7 ảnh gpti2 REF-LOCK (chưa đo giá thật — tập này ghi lại) + 7 clip Grok **0đ** (~6 phút, đo từ
  ep3-sougi) + 1 lượt TTS ~260 credit ai33. Ghép bằng `-c copy` nên **không encode lại 30 phút thân**.
- Thời gian: **45–60 phút** (nhiều hơn 35–50 phút ước cho tập thường, vì tập này viết luôn
  `_dung_hook.py` và lần đầu xử phần dịch phụ đề).
- Rủi ro đã biết: hook là bản phóng to từ **1280×720 · 24 fps** (gói Grok Pro khoá 1080p) ⇒ tránh
  cảnh cận mặt lớn hết khung trong 7 cảnh. Và ai33 từng **nuốt trọn một câu ở 3/4 lượt** — không
  được tắt cổng phủ chữ.

## 7. HAI VIỆC NGOÀI HOOK, PHÁT HIỆN LÚC KIỂM

1. **Sheet STT5 thiếu dữ liệu**: cột E (TITLE-DESCRIPTION) và G (THUMBNAIL) đang **rỗng**, dù
   `CHANEL\Lopezzapa68\ep05-simbot2-05-Hhe56wqubbU\TIEU_DE_MO_TA.txt` và `thumbnail.png` đều đã có.
   Các tập khác đều điền. Nên điền cho khỏi tưởng tập này chưa có tiêu đề/thumbnail.
2. **Tiêu đề hứa 「2つの現実」** (2 sự thật) trong khi thumbnail lại ghi `まだ終わっていない弔いがある`
   (*còn một đám tang chưa xong*) — hai lời hứa khác nhau. Luật gói đăng đòi **một lời hứa ở cả 4
   chỗ**. Nên chốt một trước khi khoá hook, vì hook phải dẫn đúng vào lời hứa đó.
