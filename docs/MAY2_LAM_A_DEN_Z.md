# MÁY 2 LÀM 100% A→Z (anh chốt 2026-10-21)

> Từ 21/10: **máy 2 làm toàn bộ** mỗi tập: kịch bản → anh soát → hook → anh duyệt hook → giọng → ảnh → dựng → giao.
> KHÔNG còn "máy 1 chạy kịch bản rồi đóng gói giao máy 2". Máy 1 ngừng sản xuất.
> File này viết cho agent chạy trên máy 2: làm đúng thứ tự, lệnh copy chạy được ngay, không tự chọn hướng khác.

## 1. Luật đổi trên máy 2

| Luật cũ (máy 1/máy 2 tách vai) | Từ 21/10 trên máy 2 |
|---|---|
| "Claude Code CHỈ LÀM BƯỚC 1" (CLAUDE.md §CẤM TUYỆT ĐỐI) | **Không áp dụng.** Máy 2 làm cả bước 2 (ảnh) + bước 3 (dựng `final.mp4`). |
| "Hình hook máy 1 làm, máy 2 chỉ ghép" | Máy 2 làm hình hook + clip hook + ghép. |
| Chạy từ bundle `FlowHandoff_local\shared\buoc2_3_tool\pipeline` + `xcopy` từ `jobs\` | **BỎ.** Chạy thẳng `E:\CLAUDE\YOUTUBE\h2dev\pipeline`, tập nằm sẵn ở `E:\CLAUDE\YOUTUBE\h2dev\<slug_dir>\<slug>\`. |
| `make_video` chặn B4/B5 ở máy 1 (`chan_buoc2_may1`) | Máy có `MAY.local` = `2` → không chặn. |

Mọi luật khác GIỮ NGUYÊN: hook bám cấu trúc hook gốc, anh soát kịch bản + duyệt clip hook (2 mốc DỪNG chờ anh),
không kill Chrome, không xoá dữ liệu sheet, TITLE/thumbnail TẮT, đường dẫn tuyệt đối khi báo anh, chữ Nhật kèm dịch Việt.

## 2. Cài 1 lần (theo thứ tự, mục nào đã có thì kiểm rồi bỏ qua)

1. Code (GitHub, nhánh `hook-video`):
   ```bat
   cd /d E:\CLAUDE\YOUTUBE
   if not exist h2dev\.git git clone -b hook-video https://github.com/haoviabattu-bluesky/h2dev2.git h2dev
   cd /d E:\CLAUDE\YOUTUBE\h2dev && git checkout hook-video && git pull
   ```
2. Đánh dấu máy 2 (file KHÔNG commit):
   ```bat
   echo 2> E:\CLAUDE\YOUTUBE\h2dev\MAY.local
   py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\may_hien_tai.py
   ```
   Phải in `la_may2=True`.
3. Khoá + credentials + skill + memory (gói Syncthing `FlowHandoff_local\shared\CAI_DAT_MAY2_AZ_2026-10-21\`, đọc `DOC_TRUOC.txt` trong đó):
   chép `keys.json` → `E:\CLAUDE\YOUTUBE\h2dev\keys.json`; `google-sheets-key.json` → `D:\CLAUDE\credentials\google-sheets-key.json`;
   `skills\` → `C:\Users\<user máy 2>\.claude\skills\`; `memory\` → `C:\Users\<user máy 2>\.claude\projects\e--CLAUDE-YOUTUBE-h2dev\memory\`.
4. Dữ liệu tập `assets\` (48 GB ở máy 1, không đi qua git): anh thêm thư mục `E:\CLAUDE\YOUTUBE\h2dev\assets` làm 1 folder Syncthing
   mới chia sẻ máy 1 → máy 2 (đã có sẵn `.stignore` bỏ video/âm thanh nặng + lane đã bỏ). Đồng bộ xong mới chạy tập.
5. Python + gói: `py -3.13` và `py -3.14` (Flow Tool), ffmpeg trong PATH, rồi
   ```bat
   py -3.13 -m pip install requests numpy Pillow edge-tts imageio-ffmpeg opencv-python-headless httpx scipy PyYAML google-auth google-api-python-client innertube playwright
   ```
6. `claude` CLI đăng nhập tài khoản MAX (chặng kịch bản gọi `claude -p` model Fable 5.1 / Opus 5): `claude --version` chạy được.
7. Chrome profile RIÊNG của máy 2 (KHÔNG copy profile từ máy 1 — mất cookie): đăng nhập tay 1 lần
   Google Flow/Vids tài khoản Ultra `nguyenquoctuan102000@gmail.com` ở `E:\CLAUDE\YOUTUBE\TUAN_PROFILE` cổng 9350
   (mở bằng `E:\CLAUDE\YOUTUBE\GROK_VIDEO\open_tuan_profile.bat` — thư mục `E:\CLAUDE\YOUTUBE\GROK_VIDEO` phải có trên máy 2), Grok (dự phòng).
8. Dịch vụ giọng/ảnh: VOICEVOX engine (lane O/N…, `FlowHandoff_local\shared\GIAO_VIEC_MAY2_CAI_VOICEVOX.md`), ai33 key (nằm trong `keys.json`),
   ima2 + 9router chạy local nếu dùng (`C:\Users\<user>\.claude\skills\gpt_api_codex.md`).
9. Kiểm nhanh:
   ```bat
   py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --trang-thai --profile kaigo-sukatto
   ```
   In được bảng trạng thái từ sheet = credentials + profile + sheet OK.

## 3. Cập nhật code về sau
```bat
cd /d E:\CLAUDE\YOUTUBE\h2dev && git pull
```
Không dùng bundle `buoc2_3_tool` nữa (không chạy `dong_goi_may2.py --bundle`).

## 4. Luồng 1 tập (cột D do tool tự ghi)

| Chặng | Lệnh / file hướng dẫn | Cột D sau chặng |
|---|---|---|
| 1. Kịch bản | `docs\BAT_DAU_LANE\<mã>.md` mục ⚡ ĐỌC NHANH (hoặc chạy lô, mục 5) | `Chờ kiểm tra kịch bản` → **DỪNG chờ anh** |
| 2. Hook | anh đổi D = `Đã sửa kịch bản` → `docs\NHAN_KICH_BAN_MAY3.md` §1–§5 | `Chờ duyệt hook` → **DỪNG chờ anh** |
| 3. Nhận duyệt | anh đổi D = `Đã duyệt hook` → `NHAN_KICH_BAN_MAY3.md` §6: `duyet_hook.py --nhan` + `dong_goi_may2.py --job <lane> <slug>` (trên máy 2 KHÔNG đóng gói đi đâu: viết `_BANGIAO.txt` NGAY trong thư mục tập, lệnh chạy tại chỗ) | `Chờ dựng video` |
| 4. Dựng | `xong_video.py --bat-dau` → làm HẾT `<thư mục tập>\_BANGIAO.txt` (lồng tiếng `--den B4Q` → vẽ ảnh Flow Tool → `make_video` dựng + giao; số liệu động nếu có mục đó) → `xong_video.py` | `Đang dựng video` → `Video xong` |

Lệnh chặng 4 (thay `<lane>` `<slug>`):
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\xong_video.py --profile <lane> --slug <slug> --bat-dau
:: ... làm hết _BANGIAO.txt ...
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\xong_video.py --profile <lane> --slug <slug>
```
`xong_video.py` (không cờ) chỉ ghi `Video xong` khi thấy `final.mp4` thật ở `E:\CLAUDE\YOUTUBE\CHANEL\<upload_channel>\<slug>\`
(chỗ B11 `giao_hang.py` ghi theo `publish.upload_dir`) — chưa có thì báo lỗi, không ghi.

## 5. Chạy lô nhiều tập (giữ nguyên lệnh cũ, nay chạy trên máy 2)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chay_lo_tap.py --profile <mã> --tu x --den y --dry
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chay_lo_tap.py --profile <mã> --tu x --den y
```
Trên máy 2 tool có thêm chặng `dung` (D = `Chờ dựng video`/`Đang dựng video` → đích `Video xong`). Tập vẽ >100 ảnh có thể
vượt trần 240 phút → thêm `--timeout-phut 480 --tran-usd 20` cho lô chặng dựng (`--chi-chang dung`).

## 6. Bẫy
- `git pull` báo xung đột ở file mình chưa sửa → KHÔNG `reset --hard`; dừng, báo anh.
- Không có `MAY.local` = `2` → tool coi là máy 1: `make_video` chặn B4/B5 ở lane có `chan_buoc2_may1`, `dong_goi_may2 --job` đóng gói sang `jobs\` như cũ.
- Ảnh hook + clip Vids dùng CHUNG Chrome Ultra cổng 9350 → các tập không chạy song song (`pipeline\khoa_ultra.py` tự khoá).
- Video giao nằm trên máy 2 (`E:\CLAUDE\YOUTUBE\CHANEL\...`) — báo anh đường dẫn tuyệt đối đó.
