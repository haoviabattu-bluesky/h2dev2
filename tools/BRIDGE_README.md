# BRIDGE ĐIỀU PHỐI TỰ ĐỘNG — LANE A (toshi-densetsu-jp)

> Cơ chế tự động hoá vòng hỏi-đáp giữa **DeepSeek (agent bước 3)** và **Claude (máy 1 —
> người giám sát pipeline)**. DeepSeek hỏi → watcher đánh thức Claude → Claude tự quyết
> và ghi trả lời vào file → DeepSeek đọc và tiếp tục. **Không cần người ngồi trung gian.**

## Quy ước FILE GIAO VIỆC (thay cho note cột H)

File: `E:\CLAUDE\YOUTUBE\h2dev\CLAUDE-DEEPSEEK.TXT`

| Ai | Ghi gì | Marker |
|---|---|---|
| **DeepSeek** | Báo cáo + câu hỏi cần Claude quyết | Mục `Câu hỏi cho Claude:` (kèm số câu hỏi) |
| **Claude** (qua watcher) | Trả lời TỪNG câu hỏi, ghi vào CUỐI file | Khối `CLAUDE → DEEPSEEK TRẢ LỜI (...)` |

- DeepSeek **KHÔNG ghi cột H nữa** — chỉ ghi đè file giao việc (giữ lại phần trả lời cũ
  hoặc thay bằng báo cáo mới tuỳ vòng).
- Watcher chỉ xử lý khi: file có `Câu hỏi cho Claude` VÀ **chưa có** `CLAUDE → DEEPSEEK TRẢ LỜI`.
- Claude KHÔNG sửa nội dung cũ của file — chỉ THÊM khối trả lời vào cuối.

## Vận hành

- Script: `tools\bridge_watcher.py` (chế độ `--once` mỗi 3 phút qua Task Scheduler
  `HermesBridgeWatcher`; có `--watch [giây]`, `--test`, `--force`).
- Mỗi lần Claude trả lời xong: log vào `tools\bridge_watcher.log`, backup bản gốc vào
  `tools\_backup_giao_viec\`.
- Watcher **tự tính số liệu** từ `qc_canh.json`/`state.json` và nhúng vào prompt của
  Claude — worker **không được tự suy diễn** cấu trúc JSON (đã dính lỗi 1 lần: Claude tưởng
  "0 lạc" vì tìm field `lac` không tồn tại; lạc thật = `muc == 0`).
- Claude chạy với `--allowedTools "Read,Write,Edit"` (KHÔNG Bash) → chỉ đọc + ghi trả lời,
  không thể chạy lệnh/`--force-qc`/tự ý `make_video`.

## Vòng lặp ĐẦY ĐỦ (tự động 100%)

```
DeepSeek ghi câu hỏi vào CLAUDE-DEEPSEEK.TXT
   → (≤3 phút) Task Scheduler chạy watcher
   → watcher gọi `claude -p` → Claude tự quyết, ghi trả lời vào cuối file
   → watcher gửi 📬 tin báo vào topic Telegram toshi (thread 555548)
   → DeepSeek đọc file, tiếp tục bước 3, ghi đè báo cáo mới
   → vòng lặp lại. KHÔNG cần người trung gian.
```

## Dừng / khởi động lại

```bat
schtasks /End /TN HermesBridgeWatcher
schtasks /Delete /TN HermesBridgeWatcher /F
schtasks /Create /TN HermesBridgeWatcher /TR "E:\CLAUDE\YOUTUBE\h2dev\tools\bridge_watcher_cron.bat" /SC MINUTE /MO 3 /F
```

## Chưa làm (bước sau nếu cần)

- Hỗ trợ lane satori (`CLAUDE-DEEPSEEK-satori.TXT`) với prompt/runbook riêng.
- Cảnh báo quyết định Claude có dấu hiệu sai số liệu (hiện đã giảm rủi ro bằng
  `tinh_so_lieu_qc()` — watcher tự tính, worker không tự suy diễn JSON).
