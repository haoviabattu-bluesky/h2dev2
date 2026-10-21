# yt_stock.py — LẤY TƯ LIỆU HÌNH TỪ YOUTUBE (Creative Commons BY) LÀM B-ROLL

Tool: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\yt_stock.py` · Test: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\tests\test_yt_stock.py`
Dựng 2026-09-23. Dùng được cho **mọi lane kể tài liệu**, không khoá lane nào (thư mục tập truyền qua tham số).

## 1. Vì sao có tool này

Kho stock của dự án đang có NASA + Wikimedia + Pexels — toàn ảnh/clip **hiện đại**. Phim tư liệu
lịch sử (1940s–1970s: tàu chiến, máy bay, tin thời sự, họp báo) gần như chỉ còn ở YouTube. Và
YouTube có một lớp video mà **chính chủ kênh khai giấy phép Creative Commons Attribution** — dùng
lại hợp pháp, điều kiện duy nhất là ghi nguồn. Đó là lớp duy nhất tool này đụng tới.

## 2. Ba luật cứng (là lý do tool tồn tại, đừng nới)

| Luật | Cài ở đâu trong code |
|---|---|
| Chỉ tải video có `license` **đúng từng ký tự** `Creative Commons Attribution license (reuse allowed)`. Mọi giá trị khác, **kể cả `None`** (= giấy phép YouTube tiêu chuẩn), là từ chối. | `la_cc_by()` + `kiem_dung_duoc()` — chạy **trước** mọi lệnh tải, sai là ném `KhongDuocPhep`, không tải byte nào. Có test `test_tai_tu_choi_khi_khong_phai_cc_by`. |
| CC BY **bắt buộc ghi nguồn** ⇒ không dựng nổi dòng credit đầy đủ (tên video + kênh + URL + giấy phép) thì không tải. | `dong_credit()` — thiếu tên kênh hoặc URL là từ chối. |
| B-roll **không được mang chữ nước ngoài** trên hình (luật dự án). | `--crop-bottom <tỉ lệ>` cắt đáy khung lúc chuẩn hoá + in cảnh báo. Máy **không soi hộ** — vẫn phải tự xem lại clip. |

⚠️ **Không được tin bộ lọc CC của trang tìm kiếm YouTube.** `extract_flat` (cái mà trang kết quả trả
về) **không có trường `license`**, nên phải gọi `extract_info` **lần thứ hai** cho từng video mới
đọc được giấy phép thật. Verify thật 2026-09-23: `yP0Ias0Jcek` → `None` (từ chối) ·
`DtpAIIVCMQw` / `YH7f8WiGjys` / `jx5GQIn47Ko` → CC BY (nhận).

## 3. Ba lệnh

```
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline

REM 1) TÌM — chỉ liệt kê, không tải gì
py -3.13 yt_stock.py tim --query "bermuda triangle 1945 newsreel" --n 15 --json "E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\yt_cc.json"

REM 2) TẢI các đoạn đã chọn vào kho stock CỦA TẬP
py -3.13 yt_stock.py tai --id DtpAIIVCMQw --ranges 120-128,300-306 ^
  --out "E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\stock" ^
  --chapter 2 --crop-bottom 0.17 --query "wwii bomber archive footage"

REM 3) SINH LẠI credits.txt của tập từ manifest (nguồn chân lý)
py -3.13 yt_stock.py credits --tap "E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle"
```

- `--ranges` nhận giây (`120-128`) hoặc `mm:ss` (`2:00-2:08`), nhiều đoạn ngăn bằng dấu phẩy.
  Mỗi đoạn ra một file riêng, **tải đúng đoạn đó** chứ không tải cả video rồi cắt.
- `--chapter` ghi vào manifest để `stock_cut.py` biết clip thuộc chương nào.
- `--crop-bottom 0.17` = bỏ 17 % đáy khung. Để 0 thì tool tự nhắc.
- `--query` nên ghi lại từ khoá đã dùng — `stock_cut.nap_kho()` đọc field này để khớp clip với đoạn lời.

## 4. Tool nhả ra cái gì

- File: `yt_<video_id>_<nn>.mp4` trong `<tập>\stock\` (cùng chỗ với `nasa_*`, `pexels_*`, `ev0*`),
  đã chuẩn hoá h264 / fps cố định / **không tiếng** (b-roll không cần tiếng).
- Sổ giấy phép: mỗi file một dòng JSON trong `<tập>\stock\manifest.jsonl`, đúng schema
  `stock_cut.py` đang đọc — `src` = **`youtube_cc`**, kèm `id/url/title/duration_s/license/credit/
  query/chapter/file/bytes/doan/crop_bottom/accessed`. Ghi xong flush + fsync ngay (ngắt giữa chừng
  vẫn không còn file "không rõ nguồn gốc").
- Nhờ đúng schema nên **không phải sửa gì trong `stock_cut.py`**: clip YouTube vào thẳng dây chuyền
  dựng thân video như clip Pexels, và `credits.txt` tự có dòng ghi nguồn của nó.

## 5. Ba bẫy yt-dlp trên máy này (đã vá sẵn trong tool — đừng dò lại)

1. **Tải-một-phần báo thiếu ffmpeg dù máy có bundle.** Tool **tái dùng** `hook_stage._ffmpeg_tren_path()`
   (docstring bên đó ghi đủ 4 bẫy lồng nhau: gate đọc PATH chứ không đọc `ffmpeg_location` · tên file
   bundle là `ffmpeg-win-x86_64-v7.1.exe` chứ không phải `ffmpeg.exe` · kết quả dò bị NHỚ cả tiến
   trình · `ffmpeg_location` trỏ thư mục thì đè lên PATH). **Đừng viết lại hàm này.**
2. **`player_client` phải thử theo thứ tự `android` → `web` → `ios`** — `web` hay trả "Requested
   format is not available" cho chính video mà `android` tải được (`TAI_THU` trong tool).
3. **Máy chưa cài JS runtime** ⇒ yt-dlp in WARNING "No supported JavaScript runtime". Không phải
   lỗi, nhưng tải hỏng thì đó là nghi phạm đầu tiên.

## 5b. Đã chạy thật lần đầu (hook ep05, 2026-09-23) — 4 điều học được

1. **Kênh `footagefarm` KHÔNG dùng được dù khai CC BY**: bản trên YouTube là reel xem thử, có
   watermark `FOOTAGE FARM <mã>` **chắn ngang giữa khung** + timecode cháy ở đáy. `--crop-bottom`
   không cứu được watermark giữa khung. Nhìn contact sheet là loại ngay, đừng tải.
2. **Kho dùng được đã verify**: `PublicResourceOrg` (United News · STORY OF NAVAL AVIATION — sạch,
   không watermark), `Archives New Zealand`, `Time Capsule Project`. Vẫn phải soi từng đoạn: nhiều
   phim có thẻ tiêu đề tiếng Anh ở đầu cuộn, và cảnh chiến sự thường không hợp câu chuyện.
3. **Độ phân giải bị chặn ở 360p vì máy chưa có JS runtime** (bẫy #3 ở trên, tốn kém hơn tưởng):
   không giải được `nsig` ⇒ format adaptive 720p+ không hiện ra, `web`/`ios`/`mweb` trả thẳng
   "No video formats found", `android` còn đúng 1 format 360p. Client **`tv_embedded` lên được
   480p** → dùng `--clients tv_embedded,android`. Muốn nét hơn thì phải cài Deno.
4. **Soi bằng mắt = contact sheet, không mở từng video**: tải bản 360p rồi rút 12 khung trải đều
   thành 1 ảnh lưới — nhìn một lần là biết có watermark / có chữ / đúng đề tài không.

## 5c. Tư liệu của HOOK phải tự khai để được ghi nguồn

Hook đầu video không nằm trong `scenes.json` của thân video ⇒ `credits.txt` không thấy nó. Script
dựng hook phải ghi `<tập>\hook\hook_shots.json` = `[{"file": "<tên file trong kho>", "n": <số cảnh>}]`;
`yt_stock.py credits` tự gộp vào. Thiếu bước này là **thiếu ghi nguồn cho CC BY** ở đúng 30 giây mà
người xem gặp đầu tiên. Mẫu chạy thật:
`E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\hook\_dung_hook_v2.py`.

## 6. Quy trình dùng khi làm tập mới (chen vào B5 của lane kể tài liệu)

1. Soạn `stock_queries.txt` như cũ → chạy `stockfetch.py` (NASA/Wikimedia/Pexels) như cũ.
2. **Đoạn nào cần hình xưa mà kho không có** (tàu/máy bay/thành phố thập niên 40–70) → `yt_stock.py tim`
   với từ khoá tiếng Anh + mốc năm (`"1945 newsreel"`, `"archive footage 1968"`, `"gov archives arc"`).
   Kho sạch đã verify: `PublicResourceOrg`, `Archives New Zealand` — **tránh `footagefarm`**, xem §5b.
3. Mở đúng những video CC BY đó, **xem bằng mắt**, ghi lại các mốc giây đẹp → `yt_stock.py tai`
   với `--crop-bottom` đủ để cắt hết chữ/watermark đáy.
4. Xem lại từng clip đã tải: **còn chữ nước ngoài trên hình là bỏ hoặc tải lại với crop lớn hơn.**
5. Chạy tiếp B5K/B5A/B8 như bình thường — clip YouTube đã nằm trong manifest nên dây chuyền tự ăn.
6. Trước khi giao hàng: `yt_stock.py credits --tap <thư mục tập>` để `credits.txt` khớp manifest.

## 7. Lỗi "ghi sai nguồn" đã vá cùng đợt (đọc để không lặp lại)

`stock_cut.gan_bang_chung()` (ghim ảnh bằng chứng đè lên cảnh stock) trước đây **không ghi đè
`title`**, và lấy `credit` của **chính cảnh bị thay thế** làm mặc định. Hậu quả: ảnh bằng chứng đi
vào `credits.txt` với tên + tác giả của clip Pexels nó vừa thay. Trên kênh tài liệu, **ghi sai nguồn
nặng hơn thiếu nguồn**.

- Đã vá: title/credit/license lấy từ **manifest của chính file bằng chứng**; `evidence.json` chỉ được
  ghi đè tường minh; manifest thiếu title thì lùi `caption` → `evidence.json.caption` → tên file,
  **không bao giờ mượn của cảnh khác**.
- Đã chạy lại `credits.txt` cho **7 tập Lane A** (ep01–ep06, ep08): **56 dòng nguồn sai được sửa**,
  tổng số dòng không đổi, bản cũ giữ ở `<tập>\credits.txt.truoc_va_20260923`.
- Bài học chung: **nguồn chân lý của việc ghi nguồn là `manifest.jsonl`**, không phải trạng thái
  của cảnh trong `scenes.json`. Chỗ nào ghi credit mà đọc từ chỗ khác manifest là chỗ đó sắp sai.
