# QUY TẮC DỰNG VIDEO HOOK 20–30 GIÂY ĐẦU (mọi lane)

Chốt 2026-09-23 sau khi chạy trọn vẹn tập thật đầu tiên: `assets\satori_jp\ep3-sougi` →
`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\ep3-sougi\final_with_hook.mp4` (30:25, 1920×1080, 30fps).
Đây là **cách dựng** hook. Cách VIẾT hook (nội dung, cổng chấm, khoá sha256) ở
`docs\PHUONG_AN_HOOK_VIDEO.md` + `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.
Nguyên tắc nội dung (10 nguyên tắc + khung 9 kênh mẫu):
`C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

## 0. Luật trên hết

⛔ **PHÂN VAI HOOK MÁY 1 / MÁY 2 (anh chốt 2026-09-24 — MỌI lane: đang làm, chưa làm, và tập đã làm)**
- **MÁY 1 làm trọn phần hình của hook:** viết hook → vẽ ảnh hook (`gpti2`, qua `pipeline\gpti2_edit.py`)
  → **sinh clip video hook** (hiện dùng **Grok free**: `E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py`. Tài khoản Grok
  = **profile GPM** tên = email cột B tab **GROK**, mỗi tài khoản 1 clip/24h. **Chỉ dùng dòng** có D SIGNUP=`done` + có
  profile GPM + cột E **trống hoặc đã quá ≥24h** — tra bằng `E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_tai_khoan.py chon`,
  dùng xong `grok_tai_khoan.py ghi <dòng>`; mở profile bằng `E:\CLAUDE\YOUTUBE\GROK_VIDEO\gpm_grok_mo.py <email>`) → **QC**
  (`pipeline\qc_hook_clip.py --anh N` trước Grok, `--clip N` sau Grok) → sinh SFX (ai33) → `hook_timeline.json`.
  Nguồn sinh clip đổi thì anh sẽ báo — tới lúc đó giữ Grok free.
- **Giao máy 2 phải KÈM ĐỦ ảnh + clip hook** trong `<tập>\hook\` (`img\`, `clip\`, `sfx\`, `qc\`,
  `hook_timeline.json`, công cụ ghép). `pipeline\dong_goi_may2.py` tự gói các thư mục này và **DỪNG nếu
  thiếu clip** nào so với `hook_timeline.json`. Cảnh chưa QC PASS → vẫn gói nhưng in cảnh báo, phải được anh duyệt.
- **MÁY 2 CHỈ GHÉP** (clip + SFX vào đầu/đè hình đầu `final.mp4` → `final_with_hook.mp4`). Máy 2 KHÔNG vẽ ảnh
  hook, KHÔNG sinh clip, KHÔNG thay clip bằng ảnh tĩnh. Thiếu gì → dừng, báo máy 1.
- Đây là NGOẠI LỆ có chủ đích của luật "Claude Code chỉ làm Bước 1" (CLAUDE.md): riêng hình hook thì máy 1 làm luôn.
- Mỗi cảnh hook phải **thấy mặt nhân vật + cảm xúc đúng ngữ cảnh** (khai `ky_vong` từng shot trong
  `hook_timeline.json`); lời hook kể chuyện nhân vật thì **ngôi thứ nhất 「私」**.
- Mẫu đã chạy thật trọn bộ: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep01-tento-kossetsu\hook\`.
**Tập đã có kịch bản/đã dựng video thì CHỈ thêm hook vào đầu.** Không viết lại `script.txt`,
không đụng `voice.mp3`, `img\`, `final.mp4`. Bản cũ giữ nguyên, bản mới là file MỚI
`final_with_hook.mp4`. (Anh chốt 2026-09-23.)

## 0b. XONG VIỆC MÁY 1 = PHẢI GỬI FILE HOOK TEXT (anh chốt 2026-09-24, mọi lane)

⛔ Hook không chỉ là video — nó là **lời hứa của cả tập**, và hai bên khác phải đọc được nó bằng chữ:

| Ai đọc | Để làm gì |
|---|---|
| Dự án tiêu đề `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH` | S1 rút sự thật → S2 tiêu đề · S4 mô tả · S7 chữ thumbnail |
| **Máy 2** | dựng/ghép đúng hook, không tự suy diễn nội dung |

**File:** `<thư mục tập>\HOOK_TAP.md`. **Sinh + nghiệm thu:**

```
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\<lane>\<epNN-slug> --profile <lane>
```

`--kiem` chỉ nghiệm thu · `--ghi-de` viết lại (⚠️ XOÁ phần viết tay).

**Chia việc — đừng trộn lại:**
- **MÁY** rút phần TẤT ĐỊNH: mốc giây + lời đọc JP (`hook_timeline.json`) + lời Việt (`hook_vi.srt`) +
  hình từng cảnh (`ky_vong`) + **từ khoá đã grep được trong `script.txt`** (so cả 76秒 ↔ 七十六秒 — đây
  chính là luật G2, liệt kê sẵn để bên viết tiêu đề không phải đoán) + danh sách ảnh/file.
- **NGƯỜI (bước 1)** viết phần cần HIỂU NỘI DUNG: lời hứa tiếng Việt, điều **CẤM lộ**, ảnh nào mạnh
  nhất. Tool để dấu `<<CẦN NGƯỜI: …>>`; **còn sót là cổng chặn giao hàng.**

**Hai cổng chặn (không phải nhắc nhở):**
- `dong_goi_may2.py` — cửa DUY NHẤT hàng ra khỏi máy 1: thiếu file hoặc còn chỗ chưa viết → `SystemExit`.
  `HOOK_TAP.md` + `promise.txt` đã nằm trong `JOB_FILES` nên tự đi kèm gói.
- `qc_final.py` B10 — mức `cao` (khác G1–G8 để mức `vua`): đây là **gói giao thiếu file**, không phải
  chuyện hay/dở của nội dung.

**Đầu nhận đã nối:** `YT-TITLE-RESEARCH/src/step_common.py::hook_tap()` + `promise()`, bơm vào prompt
**S1** (`prompts/s1_summarize.md`, placeholder `{hook_tap}` + `{promise}` — nối `{promise}` 2026-09-24,
trước đó hàm có sẵn nhưng chưa ai gọi). Chọn S1 vì S2/S3/S4 đều ăn `S1_TOM_TAT.json` — vào S1 là hook
lan xuống cả chuỗi bằng MỘT chỗ sửa. Prompt ghi rõ hook là **ràng buộc cứng**: không sửa chữ hook để
khớp tiêu đề; lệch thì ghi vào `khong_duoc_noi_qua`.

**Mẫu người viết đầy đủ:** `assets\kenko-chiebukuro\ep01-tento-kossetsu\HOOK_TAP.md`.
**Còn nợ:** `assets\satori_jp\ep3-sougi` có hook nhưng chưa có file này — cũng vì vậy `goi_title.py`
(mục dưới) DỪNG tự động cho tập này, phải sinh `HOOK_TAP.md` trước.

**2026-09-24: dự án tiêu đề nay được TỰ GỌI** (không phải anh gõ `cli.py run` tay nữa) —
`pipeline\goi_title.py`, nối ở cuối cả 3 đường giao máy 2. Chi tiết: `docs\QUY_TRINH_GIAO_VIEC_MAY2.md`
§7 và `docs\PHUONG_AN_TU_GOI_TITLE.md`.


> 2026-09-24 (Lane K ep01): `pipeline\ghep_hook_noi_truoc.py` nay TỰ nhận tập mà `script.txt` ĐÃ mở bằng hook (luồng lean chép hook vào đầu script) → chế độ THAY HÌNH: phủ clip hook lên 0–T của final.mp4, giữ tiếng thân, tổng độ dài không đổi (đúng mục 9.5 'upstream'). Trước bản vá này tập kiểu đó bị NỐI TRƯỚC → nghe hook 2 lần. Tập script không chứa hook vẫn nối trước như cũ. Luôn truyền `--tap` bằng đường dẫn TUYỆT ĐỐI (công cụ chạy ffmpeg trong thư mục hook\).

## 1. Bảy bước, theo đúng thứ tự

| # | Việc | Lệnh / công cụ | Ra file |
|---|---|---|---|
| 1 | Viết + khoá hook | `pipeline\hook_stage.py --profile <lane> --slug <tập> --mode repair` | `hook\hook_locked.txt` · `hook_lock.json` |
| 2 | **Lồng tiếng hook TRƯỚC khi vẽ** | `pipeline\tts.py --script hook\hook_locked.txt --out hook\hook_voice.mp3 --profile <lane>` | `hook_voice.mp3` + `.srt` |
| 3 | Cắt cảnh theo mốc câu THẬT | đọc `hook_voice.srt`, mỗi cảnh = 1 câu, không chia đều | `hook\hook_timeline.json` |
| 4 | Vẽ ảnh, khoá mặt bằng ảnh CỦA CHÍNH TẬP | `pipeline\gen_images.py --ref <img\NNN.png> --ref2 <img\NNN.png> --quality low --orient landscape` | `hook\img\001..00N.png` |
| 5 | Sinh clip 6 giây | `E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py --jobs <csv> --out hook\clip --no-audio --gap 5` | `hook\clip\clip_NN.mp4` |
| 6 | Cắt + nối + lồng tiếng + cháy phụ đề | ffmpeg (xem §3) | `hook\hook_final.mp4` · `_JP` · `_VI` |
| 7 | **Cân mức tiếng** rồi ghép vào video cũ | ffmpeg concat, `-c:v copy` | `final_with_hook.mp4` |

## 2. Bốn thứ BẮT BUỘC khớp, kiểm từng cái trước khi ghép

| Phải khớp | Đo bằng | Số thật ở ep3 | Hỏng thì sao |
|---|---|---|---|
| **Mức tiếng** | `ffmpeg -af ebur128` | hook −16,3 → hạ **−5,4 dB** cho bằng thân −21,7 LUFS | `tts.py` chuẩn hoá mọi giọng về −16, video cũ ở −21,7 → hook oang oang rồi tụt hẳn, đúng 30 giây quyết định ở lại hay thoát |
| **Độ phân giải + fps** | `ffmpeg -i` | clip Grok 1280×720@24 → scale 1920×1080, `fps=30`, `setsar=1` | concat demuxer hỏng hoặc phải encode lại cả 30 phút thân video |
| **Kiểu phụ đề cháy** | copy y nguyên `force_style` của `pipeline\assemble.py` | `FontName=Meiryo,FontSize=18,Outline=2,Shadow=1,MarginV=45,Alignment=2` | nhìn ra ngay hai đoạn ghép từ hai nơi |
| **Điểm nối sạch** | `ffmpeg -vf blackdetect` quanh mốc nối | 0 khung đen | giật/chớp ở giây 26 |

Nghiệm thu sau khi ghép: đo lại mức tiếng ở **3 mốc** (trong hook · ngay sau điểm nối · giữa phim),
lệch nhau phải **< 0,5 LUFS**. Ở ep3: −21,7 / −21,6 / −21,8.

## 3. Khuôn lệnh ffmpeg (đã chạy thật)
```
# 6a. cắt từng clip đúng mốc + nâng lên khuôn video cũ
-i clip_NN.mp4 -t <dung_s> -vf "scale=1920:1080:force_original_aspect_ratio=decrease,
   pad=1920:1080:-1:-1,fps=30,setsar=1" -an -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p
# 6b. nối + lồng giọng
-f concat -safe 0 -i list.txt -c copy  →  -i noi.mp4 -i hook_voice.mp3 -c:v copy -c:a aac -shortest
# 6c. cháy phụ đề Nhật (KHÔNG dùng .srt của STT — reflow từ bản khoá trước)
pipeline\srt_from_script.py --srt hook_voice.srt --script hook_locked.txt --out hook_jp.srt
-vf "subtitles=hook_jp.srt:force_style='FontName=Meiryo,FontSize=18,...,MarginV=45,Alignment=2'"
# 7. cân tiếng rồi ghép (video KHÔNG encode lại)
-i hook_final_JP.mp4 -af volume=<chênh>dB -c:v copy -c:a aac -ar 44100 -ac 2
-f concat -safe 0 -i _noi.txt -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart
```

## 4. Bẫy đã trả giá
1. **Grok không báo lỗi khi thiếu ảnh.** Prompt của mình chỉ tả CHUYỂN ĐỘNG (đúng cho ảnh→video: mặt và
   bối cảnh đã nằm trong ảnh, tả lại là mời model vẽ đè). Nếu ảnh chưa gắn, Grok chạy text→video và bịa
   ra cảnh hoàn toàn khác — **đã xảy ra thật**, nhận về một bãi biển không người. Dùng `grok_batch.py`
   (tự upload lấy mã tệp) thay vì bấm tay. Bấm tay thì kiểm: URL phải nhảy sang `/imagine/post/<id>` và
   hiện đúng tấm ảnh.
2. **Đặt 720p, không phải 480p/1080p.** 1080p vẫn nằm trong menu nhưng gói Pro bị khoá → server trả 403,
   giao diện không báo gì.
3. **`srt_from_script.py` có thể nuốt dấu 「 ở câu đầu** (phủ 99,2%) — soi lại cue 1 bằng mắt.
4. **Ảnh khoá mặt lấy từ `img\` của CHÍNH tập đó**, đừng vẽ mặt mới: hook nối vào video cũ mà hai người
   khác nhau thì lộ ngay. Ở ep3 dùng `img\007.png` (ông) + `img\002.png` (bà) — chọn ảnh CHỈ CÓ 1 người.
5. **Clip 6 giây nhưng cảnh chỉ dùng 2,6–5,7 giây** — sinh 6 giây rồi cắt đuôi, không kéo giãn, không tua.
   Cảnh ngắn hơn ~3 giây với khán giả lớn tuổi là hơi chớp; cân nhắc mượn thêm 1 giây của cảnh sau.

## 5. Kiểu hook + câu khoá đã khai cho từng lane
Khai ở `profiles\profiles\<lane>.json` → `script.hook.patterns` / `script.hook.closer`; `hook_stage.py`
đọc `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\patterns.json` (130 video · H01–H41 · K01–K23) rồi nối cơ chế +
khuôn câu + điều cấm vào prompt viết hook.

| Lane | patterns | closer | Câu nghi thức của kênh mẫu |
|---|---|---|---|
| `satori-jp-obaa` ✅ đang bật | H22 H23 H38 | K12 | hứa N điều + 'điều cuối đến giờ vẫn khó nói' (15/15) |
| `toshi-densetsu-jp` | H24 H25 H26 H27 H39 | K13 | 2–3 câu なぜ → 『それでは…最初から辿っていこう』 (8/9) |
| `irogatatarukioku` | H27 H28 H29 | K16 | 「この写真をカラー化してみる」 + 「N枚の写真で辿っていく」 (9/9, 8/9) |
| `kenko-chiebukuro` | H30 H31 H32 H33 H34 | K18 | điều kiện của danh sách; **không đọc trước tên món** (kênh 0/6, mình 8/8 sai) |
| `teinengo-real` | H23 H35 | K19 | 「これは〜という話だ」 |
| `teinengo-tanoshimi` | H30 H34 | K03 | 「この時の俺はまだ知らなかった」 ở 29–48s (5/7) |

### 5b. CÁCH DỰNG HÌNH — hook là VIDEO SINH (mặc định mọi lane, anh chốt 2026-09-24)

⛔ **LUẬT MỚI 2026-09-24 — đọc trước bảng bên dưới.** Hook **KHÔNG còn là video ghép từ ảnh render**.
Mặc định MỌI LANE: hook là **VIDEO SINH từ Google Flow (Veo) hoặc Grok Imagine**, như
`satori-jp-obaa` đã chạy thật ở `ep3-sougi`. Ảnh tĩnh / clip stock chỉ là **NGOẠI LỆ**.

Khai bằng **hai field tách nhau** (trộn vào một field là chỗ sinh lỗi — đã dính thật 2026-09-24):

| Field | Nghĩa | Cổng S1L kiểm |
|---|---|---|
| `script.hook.visual` | **nguồn hình + cách khoá mặt**, riêng từng lane, cấm mượn của nhau. Có code đọc (`dong_goi_may2.py`) và SOP từng lane trỏ vào — đừng đổi tên cho gọn | không |
| `script.hook.visual_kind` | `"video_sinh"` (mặc định) \| `"anh_tinh"` | ⛔ khác `video_sinh` mà không có `visual_exception` → **DỪNG** |
| `script.hook.visual_exception` | lý do dùng ảnh tĩnh, viết rõ | ⛔ bắt buộc khi `anh_tinh` |
| `script.hook.sfx` | `true` — **hiệu ứng âm thanh BẮT BUỘC** | ⛔ thiếu → **DỪNG** |

**Hai ngoại lệ chính danh** (lý do cứng, KHÔNG phải tiền lệ cho lane khác): `toshi-densetsu-jp` và
`irogatatarukioku` bán **SỰ THẬT CÓ HỒ SƠ** — đưa clip AI sinh vào hook là tự phá đúng thứ kênh đang
bán, chưa kể phá quy ước ghi nguồn `credits.txt`.

**Lane đã đổi cách dựng vì luật này:** `kenko-chiebukuro` từ `lien_mach_than` (hook nằm trong
`script.txt`, không dựng clip riêng) → `anh_ai_clip_grok` + `video_sinh`. Hai thứ cũ loại trừ nhau.
Hệ quả phải làm theo: (a) mất lợi thế "không có điểm nối" nên **phải cân mức tiếng + khớp fps/độ phân
giải** theo §2; (b) gói giao máy 2 nay đi nhánh "hook là clip riêng" của `dong_goi_may2.py`, tức máy 2
nhận thêm đơn vẽ ảnh hook; (c) `docs/SOP_LANE_E.md` mục hook cần sửa theo.

**Kịch bản phải đổi theo clip:** 20–30 giây đầu bị ràng buộc bởi thứ dựng được thành clip 5–6 giây —
một chủ thể, một chuyển động tả được bằng lời. Cấm cảnh cần ≥3 nhân vật cùng hành động, cấm đổi bối
cảnh giữa một cảnh, cấm chữ/biểu đồ trên hình; chừa chỗ cho tiếng thật của cảnh. Luật này được nhồi
**tự động** vào prompt của model VIẾT (`qc_goi_dang.khoi_luat_cho_prompt`), không phải dặn tay.

### 5b-1. Bảng nguồn hình từng lane — mỗi lane MỘT kiểu, không được mượn của nhau

Khai ở `profiles\profiles\<lane>.json` → `script.hook.visual` (+ `_visual_note` ghi rõ nguồn hình và
điều cấm). Đây là field profile chứ không phải quy ước trong tài liệu, vì hàng rào #2 của dự án:
khác biệt giữa lane chỉ được thể hiện bằng field profile.

| Lane | `visual` | Nguồn hình | Cấm | Đã chạy thật |
|---|---|---|---|---|
| `satori-jp-obaa` | `anh_ai_ref_grok` | ảnh AI gpti2, khoá mặt bằng ảnh **của chính tập** trong `img\` → clip Grok 6s | tư liệu thật, clip stock | ✅ `ep3-sougi` |
| `toshi-densetsu-jp` | `tu_lieu_that` | **100% tư liệu thật** trong `stock\` của tập: clip Pexels/NASA + ảnh public domain | ảnh AI, clip AI | ✅ `ep05-bermuda-triangle` |
| `irogatatarukioku` | `anh_that_to_mau` | ảnh chiến tranh thật trong `_src_photos\`, tô màu AI, **ảnh đứng yên** | vẽ người bằng AI | ❌ chưa |
| `kenko-chiebukuro` | `anh_ai_clip_grok` | ảnh AI minh hoạ của tập → clip Grok, nối vào trước `final.mp4` (ĐỔI 2026-09-24 từ `lien_mach_than`) | ảnh thật, hook liền mạch trong script | ❌ chưa |
| `teinengo-real` · `teinengo-tanoshimi` | `manga_ai_ref` | manga AI, REF-LOCK cùng bộ nhân vật với thân video | ảnh thật | ❌ chưa |

**Vì sao phải tách:** gọi lane satori mà đi lấy tư liệu thật như Lane A là sai hai tầng — kênh satori
kể chuyện hư cấu nên không có "tư liệu" nào để lấy, và nhân vật trong hook phải khớp mặt với thân
video (khoá bằng chính ảnh của tập). Ngược lại, Lane A bán **sự thật có hồ sơ**; đưa ảnh AI vào hook
là tự phá thứ kênh đang bán, chưa kể vi phạm quy ước chú thích nguồn ở `credits.txt`.

**Hai kiểu ghép, cũng khác nhau theo lane:**
- **Ghép trước** (`satori-jp-obaa`, `toshi-densetsu-jp`, `irogatatarukioku`): tập đã dựng xong
  `final.mp4` → dựng clip hook riêng rồi nối vào trước, ra `final_with_hook.mp4`, file cũ giữ nguyên.
  Phải qua 4 phép kiểm ở §2.
- **Liền mạch** (`kenko-chiebukuro`): tập dựng lại từ đầu → hook nằm ngay trong `script.txt`, không có
  điểm nối nên không phải cân mức tiếng, không phải khớp dải màu.

Lane H/I/J (`kokoro-kazoku`, `sengoku-uragawa`, `teinengo-fuufu`) chưa có profile — khi lập thì khai
H36/H37 + K21/K22 · H39/H40/H41 + K23 · H36/H37 + K19/K20/K22.

✅ `script.hook.enabled` nay **BẬT ở cả 6 lane** (3 lane cuối bật 2026-09-24 — luật chốt 23/09 mà tới
24/09 mới có 3/6 lane bật, nên nay do **cổng S1L** chặn thay vì trông vào người nhớ). Hook chỉ áp cho
tập VIẾT MỚI (`lean_script.se_viet_moi`) — tập đã khoá script không bị đụng; tập đã dựng muốn thêm
hook thì `hook_stage.py --mode repair`.

## 6. Việc còn nợ (từ 10 nguyên tắc, chưa code)
Nguyên tắc 10 đòi cổng đo **THỨ TỰ**, hiện `qc_script*.py` chỉ đo độ dài/nhịp. Sáu phép kiểm tất định
cần thêm: (a) câu đầu không chào/không tự giới thiệu · (b) câu chốt ≤ N giây (ngưỡng theo kênh) ·
(c) lõi tiêu đề xuất hiện ≤30–45s · (d) mỗi dòng chữ thumbnail có trong hook hoặc trong 90s ·
(e) câu nghi thức của kênh có mặt · (f) **mọi vế tiêu đề/thumbnail grep được trong `script.txt`, so cả
dạng chữ số lẫn chữ Hán** (`76秒` ↔ `七十六秒` — toshi ep10 lọt vì lý do này).
