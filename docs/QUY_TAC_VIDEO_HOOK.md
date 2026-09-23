# QUY TẮC DỰNG VIDEO HOOK 20–30 GIÂY ĐẦU (mọi lane)

Chốt 2026-09-23 sau khi chạy trọn vẹn tập thật đầu tiên: `assets\satori_jp\ep3-sougi` →
`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\ep3-sougi\final_with_hook.mp4` (30:25, 1920×1080, 30fps).
Đây là **cách dựng** hook. Cách VIẾT hook (nội dung, cổng chấm, khoá sha256) ở
`docs\PHUONG_AN_HOOK_VIDEO.md` + `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.
Nguyên tắc nội dung (10 nguyên tắc + khung 9 kênh mẫu):
`C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

## 0. Luật trên hết
**Tập đã có kịch bản/đã dựng video thì CHỈ thêm hook vào đầu.** Không viết lại `script.txt`,
không đụng `voice.mp3`, `img\`, `final.mp4`. Bản cũ giữ nguyên, bản mới là file MỚI
`final_with_hook.mp4`. (Anh chốt 2026-09-23.)

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

Lane H/I/J (`kokoro-kazoku`, `sengoku-uragawa`, `teinengo-fuufu`) chưa có profile — khi lập thì khai
H36/H37 + K21/K22 · H39/H40/H41 + K23 · H36/H37 + K19/K20/K22.

⚠️ `script.hook.enabled` của 5 lane trên vẫn **TẮT** — mới khai nguyên liệu, chưa bật. Bật từng kênh sau
khi chạy thử 1 tập, theo `docs\PHUONG_AN_HOOK_VIDEO.md` §11.

## 6. Việc còn nợ (từ 10 nguyên tắc, chưa code)
Nguyên tắc 10 đòi cổng đo **THỨ TỰ**, hiện `qc_script*.py` chỉ đo độ dài/nhịp. Sáu phép kiểm tất định
cần thêm: (a) câu đầu không chào/không tự giới thiệu · (b) câu chốt ≤ N giây (ngưỡng theo kênh) ·
(c) lõi tiêu đề xuất hiện ≤30–45s · (d) mỗi dòng chữ thumbnail có trong hook hoặc trong 90s ·
(e) câu nghi thức của kênh có mặt · (f) **mọi vế tiêu đề/thumbnail grep được trong `script.txt`, so cả
dạng chữ số lẫn chữ Hán** (`76秒` ↔ `七十六秒` — toshi ep10 lọt vì lý do này).
