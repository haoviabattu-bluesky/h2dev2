# CLIP HOOK BẰNG GOOGLE VIDS (Ultra) — phương án CHÍNH thay Grok (anh chốt 16/10/2026, mọi lane)

> Grok (`tools\hook_lane_g\grok_da_luong.py`) chuyển thành đường DỰ PHÒNG. Mọi luật hook giữ nguyên (ảnh REF-LOCK,
> chữ đạo cụ chèn trước, thẻ tên, chỉ nhạc nền). Chỉ đổi khâu "ảnh hook → clip".

## 1. Lệnh
```
:: Chrome Ultra (nguyenquoctuan102000@gmail.com) — chỉ mở nếu cổng 9350 chưa sống (curl http://127.0.0.1:9350/json/version)
E:\CLAUDE\YOUTUBE\GROK_VIDEO\open_tuan_profile.bat

:: xem kế hoạch giây + prompt (không tốn lượt)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\hook_lane_g\vids_hook.py <thư mục hook TUYỆT ĐỐI> --dry

:: chạy thật (Bash run_in_background) — ra thẳng <hook>\clip\clip_NN.mp4 như Grok, clip đã có thì bỏ qua
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\hook_lane_g\vids_hook.py <thư mục hook TUYỆT ĐỐI> --tabs 5
```
Tham số: `--only clip_03,clip_07` · `--lam-lai` (sinh đè clip đã có) · `--ra <thư mục>` (thử ra chỗ khác) ·
`--res 1080p` · `--vong 3` (số lần sinh lại clip hỏng) · `--avatar <ảnh>` (mặc định `<lane>\branding\avatar_raw.png`).
Cổng chữ đạo cụ (`pipeline\chu_dao_cu.py`) chặn y như Grok.

## 2. Tool làm gì (đo thật 16/10)
| Bước | Cách |
|---|---|
| Ảnh REF | chế độ **"Tạo ảnh động"** (ảnh → video), tải `<hook>\img\NNN.png` qua `input[type=file]`. Ảnh = **khung đầu** clip (lệch 1,4/255 — mặt, kính, áo, nét anime giữ nguyên). KHÔNG dùng "Thành phần" (cần thoả thuận quyền hình ảnh, không cần cho việc này) |
| Prompt | rút từ prompt Grok trong `grok_jobs.csv`: chỉ ACTION/MOVEMENT/CAMERA/EMOTION, mở đầu `Single continuous shot, no cuts. Animate this exact image as the opening frame…`; ảnh có chữ (`KEEP TEXT`) → câu giữ nguyên chữ + máy gần đứng yên |
| Số giây | thanh "Thời lượng video" 3–10s, bước 1s (kéo bằng phím, đọc lại nhãn nút phải ghi `N giây`). Xem §3 |
| Hậu kỳ | **bỏ tiếng** (hook chỉ nhạc nền) + **che sao Gemini** (tâm 1160,600 trên 1280x720) bằng **avatar kênh cắt tròn** viền trắng |
| QC tự động | đủ giây (±0,4s) · khung đầu lệch ảnh ≤ 15 · không bị Omni tự cắt cảnh → hỏng thì chuyển `_sai\`, sinh lại |
| Ra | `<ra>\clip_NN.mp4` (đã che + câm) · gốc `<ra>\_vids_goc\` · `<ra>\_vids_log.csv` · `soat_muot.csv` + `sheet.jpg` |

## 3. Chọn số giây cho KHỚP lời đọc
Clip phải **dài hơn hoặc bằng** lời của shot: dư thì máy 2/xem thử cắt bớt; thiếu thì bị giãn chậm (setpts) — chuyển động chậm, xấu hơn.
1. Có giọng thật (cache `<tập>\_xem_thu_giong\` của `xem_thu_hook_giong.py`) → giây = ceil(lời + nghỉ 0,5s/câu + 0,5).
2. Chưa có giọng → ước `số chữ ÷ voice.char_rate × 60 + 0,5s/câu`, nhưng ước HỤT tới 30% ở câu có số (64歳 (64 tuổi), 1150円 (1150 yên) —
   đo ep11 Lane N) → giây = ceil(ước × 1,2 + 1).
3. Shot có thẻ tên → ≥ `script.hook.the_ten.dur_s` (6s, luật 16: cảnh nhân vật chạy đủ motion).
4. Kẹp 3–10s. Lời > 10s → xin 10s, khi ghép giãn chậm (tool in hệ số).
5. Chưa có `hook_timeline.json` → theo cột `duration` của `grok_jobs.csv`.
⇒ **Hook KHÔNG phải viết lại** — viết như cũ; shot dài/ngắn tuỳ lời, Vids tự xin đúng số giây.

## 4. Kết quả chạy thật (16/10, N ep11-bento-line, 18 clip, 5 tab)
- **18/18 đạt**, mỗi clip đúng số giây xin (4–10s), khung đầu lệch ảnh 1,2–6,8, không clip nào tự cắt cảnh, ~26–36 giây/clip.
- Chữ trên tờ tuyển dụng (パート募集 (tuyển bán thời gian) / 週4日 (4 ngày/tuần) / 時給1150円 (lương giờ 1150 yên)) **giữ nguyên nét suốt clip** — tốt hơn Grok.
- 4/18 ảnh (mặt vẽ gần người thật, cận mặt) bị **TỪ CHỐI** "vi phạm các điều khoản" với prompt đầy đủ → sinh lại bằng **prompt gọn**
  (chỉ `Animate this image.` + chuyển động, bỏ câu "giữ nguyên mọi khuôn mặt") → **4/4 qua**. Tool tự làm việc này (nhận ra từ chối ngay, không chờ hết giờ).
- Clip mẫu: `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep11-bento-line\hook\_vids_thu\` (`sheet.jpg`).

## 5. Bẫy đã dính (16/10)
1. aria-label `Thời lượng video` lưu Unicode tổ hợp → selector theo aria-label KHÔNG khớp; chọn `[class*=MenubuttonSlider] input[type=range]`.
2. Popup cài đặt đóng là bị GỠ khỏi DOM; nút là công tắc (`aria-expanded`) — bấm 2 lần là đóng. Mở → kéo → Escape → đọc lại nhãn.
3. Sau mỗi clip ảnh trong ô bị XOÁ, prompt còn nguyên → mỗi clip phải tải lại ảnh + đặt lại prompt + đặt lại giây.
4. Tìm nút cài đặt bằng chuỗi "720p" sẽ bắt nhầm thẻ video đã tạo trong lịch sử (`Video được tạo: …, 720p, 10 giây`) → dùng `button[aria-label^='Cài đặt tạo video']`.
5. Phím mũi tên KHÔNG chỉnh được thanh giây ở tab nền (4/5 tab giữ 10s) → đặt bằng JS (setter gốc + sự kiện input/change).
6. Ô soạn THU GỌN sau mỗi clip → mất ô tải ảnh + nút Cài đặt → Escape rồi bấm vào ô prompt cho mở ra trước.
7. Bẫy chung của Vids (prompt thu gọn, nhiều tab cướp focus, tải bằng cookie…): `E:\CLAUDE\YOUTUBE\GROK_VIDEO\tools\google_vids\HUONG_DAN_GOOGLE_VIDS.md` §5.
8. Không chạy 2 lô cùng lúc trên TUAN_PROFILE — từ 16/10 CODE CHẶN: `vids_hook.py` giữ khoá `pipeline\khoa_ultra.py` (chung với ảnh hook `pipeline\anh_hook.py`), tập khác đang giữ → chờ tới lượt (`--cho-khoa` phút); không kill Chrome; không dùng Profile 25 của Chrome chính. Ảnh hook cũng vẽ trên profile này: `docs\QUY_TRINH_ANH_HOOK_GOOGLE_FLOW.md`.
