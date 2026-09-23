# QUY TRÌNH GIAO VIỆC MÁY 1 → MÁY 2 (chốt 2026-09-23)

> Anh chốt: **máy 1 chỉ làm phần cần HIỂU NỘI DUNG. Mọi việc cơ học giao hết máy 2.**
> Trước mốc này máy 1 còn ôm lồng tiếng — nay chuyển sang máy 2.

## 1. Ranh giới

| Việc | Ai làm | Vì sao |
|---|---|---|
| Kịch bản · hook · khoá `script.lock.json` | **máy 1** | cần hiểu nội dung, phải qua Sol |
| `img_prompts.txt` (prompt ảnh) | **máy 1** | quyết định "đoạn này cần hình gì" = việc nội dung; `CLAUDE.md` mục CẤM gọi đích danh |
| Ảnh REF nhân vật (`_ref/`, `characters.json`) | **máy 1** | anh chốt 2026-09-21 — không để máy 2 vẽ mù mặt nhân vật |
| Tiêu đề · mô tả · chữ thumbnail | **máy 1** | 2 tập satori từng lọt lên với listing rỗng vì bước sau tưởng phải tự viết |
| **Giọng đọc `voice.mp3` + phụ đề `voice.srt`** | **máy 2** | cơ học: giọng đã ghim cứng trong hồ sơ kênh (voice_id · speed · fx), không còn phán đoán |
| Vẽ ảnh · dựng `final.mp4` | **máy 2** | cơ học |

**Nguyên tắc chung:** việc nào mà kết quả chỉ phụ thuộc tham số đã ghi sẵn trong profile thì giao
máy 2. Việc nào phải đọc kịch bản rồi quyết định thì giữ máy 1.

## 2. Chuyển việc thì phải chuyển CẢ CỔNG

Giao lồng tiếng sang máy 2 mà không giao cổng = giao luôn rủi ro. Hai cổng bắt buộc chạy ở máy 2:

### 2a. Cổng PHỦ CHỮ — `tts.py::kiem_phu_chu()` (ngưỡng 95%)
So số chữ trong phụ đề server trả về với **kịch bản gốc**. Thiếu quá 5% → `SystemExit`, chạy lại.

**Vì sao cần:** đo thật 2026-09-23 trên hook `ep05-bermuda-triangle` (208 chữ) — chạy TTS 4 lượt
cùng một đoạn text thì **3 lượt nuốt trọn một câu**, mỗi lượt nuốt một câu khác nhau (lượt 1 và 3
mất câu cuối, lượt 2 mất câu áp cuối, lượt 4 đủ). Không báo lỗi gì.

**Vì sao cổng cũ không bắt được:** cổng độ dài có sẵn so `mp3` với `SRT` — mà hai thứ đó đều do
CÙNG server sinh ra nên khớp nhau trong cái sai: mp3 ngắn đúng bằng phần bị nuốt, SRT cũng ngắn y
hệt. Chỉ có so với kịch bản gốc mới lòi ra. Test giữ chốt: `pipeline/tests/test_tts_phu_chu.py`.

### 2b. Nắn phụ đề theo kịch bản — `srt_from_script.py`
Phụ đề server là bản MÁY NGHE, sai chữ đồng âm. Phải nắn lại theo `script.txt` trước khi cháy chữ.
Lệnh: `py -3.13 srt_from_script.py --srt voice.srt --script script.txt --out voice.srt`

## 3. Máy 2 chạy gì

Máy 2 có sẵn toàn bộ mã nguồn (`dong_goi_may2.py --bundle` copy hết `pipeline/*.py` + profile của
lane). Sau khi nhận job:

```
py -3.13 make_video.py --profile <lane> --slug <tập> --from B4
```

`--from B4` = bắt đầu từ lồng tiếng, vì B0–B3 (kịch bản) máy 1 đã làm và đã khoá sha256.
Cổng `kiem_lock()` sẽ chặn nếu `script.txt` bị sửa sau khi khoá.

**Máy 2 cần thêm 1 thứ so với trước:** khoá API ai33 (`AI33_API_KEY`) để chạy TTS. Đặt vào biến môi
trường trên máy 2, không ghi vào file trong gói job.

## 4. Gói job máy 1 gửi đi

`pipeline/dong_goi_may2.py --job --profile <lane> --slug <tập>` → `FlowHandoff_local\jobs\<slug>\`

| File | Bắt buộc |
|---|---|
| `script.txt` | ✅ |
| `script.lock.json` | ✅ (máy 2 kiểm sha trước khi chạy) |
| `img_prompts.txt` | ✅ |
| `characters.json` · `_ref/` | khi lane có REF-LOCK |
| `title.txt` · `series_ctx.txt` · `competitor.txt` · `state.json` | ✅ |
| `hook/` (`hook_locked.txt`, `hook_lock.json`, `hook_storyboard.json`, `grok_jobs.csv`) | khi lane bật hook |
| `_BANGIAO.txt` | ✅ — quy cách vẽ + lệnh chạy |
| ~~`voice.mp3`~~ · ~~`voice.srt`~~ | ❌ **bỏ từ 2026-09-23** — máy 2 tự sinh |

Bỏ được ~30 MB mỗi tập qua Syncthing, và máy 1 hết phải chờ lồng tiếng.

## 5. Hook thì sao

Xem `docs\QUY_TAC_VIDEO_HOOK.md` §5b — mỗi lane một cách dựng hình khác nhau, khai ở
`script.hook.visual`. Hai kiểu giao việc:

- **`lien_mach_than`** (vd `kenko-chiebukuro`): hook nằm ngay trong `script.txt`, máy 2 không phải
  làm gì thêm — lồng tiếng và dựng như bình thường là hook có sẵn ở 30 giây đầu.
- **`anh_ai_ref_grok` · `tu_lieu_that` · `anh_that_to_mau` · `manga_ai_ref`**: hook là clip RIÊNG.
  Máy 1 gửi kèm `hook/`, máy 2 dựng clip hook rồi nối vào trước `final.mp4` → `final_with_hook.mp4`,
  qua 4 phép kiểm ở `QUY_TAC_VIDEO_HOOK.md` §2 (mức tiếng · fps/độ phân giải · kiểu phụ đề · điểm nối).

## 6. Máy 2 trả hàng về

`FlowHandoff_local\results\<tên-tab-sheet>\<slug>\` — ví dụ lane E là `results\70dai-kenko\<slug>\`.

⚠️ **Bài học 2026-09-23:** máy 2 xếp theo `results\<tên-tab>\<slug>\` chứ không phải
`results\<slug>\`. Quét dọn mà chỉ nhìn một tầng thì bỏ sót — đã sót thật 1,52 GB.

Xong thì ghi cột trạng thái trên Google Sheet theo quy ước của lane (lane E: cột H, một ô,
`Video done - <slug>` + xuống dòng + đường dẫn).
