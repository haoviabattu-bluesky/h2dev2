# QUY TRÌNH GIAO VIỆC MÁY 1 → MÁY 2 (chốt 2026-09-23)

> Anh chốt: **máy 1 chỉ làm phần cần HIỂU NỘI DUNG. Mọi việc cơ học giao hết máy 2.**
> Trước mốc này máy 1 còn ôm lồng tiếng — nay chuyển sang máy 2.

## 1. Ranh giới

| Việc | Ai làm | Vì sao |
|---|---|---|
| Kịch bản · hook · khoá `script.lock.json` | **máy 1** | cần hiểu nội dung, phải qua Sol |
| `img_prompts.txt` (prompt ảnh) | **máy 1** | quyết định "đoạn này cần hình gì" = việc nội dung; `CLAUDE.md` mục CẤM gọi đích danh |
| Ảnh REF nhân vật (`_ref/`, `characters.json`) | **máy 1** | anh chốt 2026-09-21 — không để máy 2 vẽ mù mặt nhân vật |
| Tiêu đề · mô tả · tags · thumbnail | **dự án YT-TITLE-RESEARCH** | 2026-09-24 — giao HẾT cho dự án khác, xem mục 6 dưới. Trước mốc này là máy 1 (2 tập satori từng lọt lên với listing rỗng vì bước sau tưởng phải tự viết) |
| **Giọng đọc `voice.mp3` + phụ đề `voice.srt`** | **máy 2** | cơ học: giọng đã ghim cứng trong hồ sơ kênh (voice_id · speed · fx), không còn phán đoán |
| Vẽ ảnh · dựng `final.mp4` | **máy 2** | cơ học — **ảnh vẽ trên Google Flow bằng FLOW TOOL, KHÔNG chạy Playwright** (anh chốt 2026-09-24); gpti2 chỉ dự phòng |

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
cd <FlowHandoff_local của máy 2>\shared\buoc2_3_tool\pipeline
py -3.13 make_video.py --profile <lane> --slug <tập> --redo-voice
```

⚠️ **CHẠY TỪ ĐÂU: luôn là `shared\buoc2_3_tool\pipeline` (cây BUNDLE), KHÔNG phải `h2dev\pipeline`
của máy 2.** Bundle là cây duy nhất được máy 1 làm mới mỗi lần đóng gói, nên profile + cổng mới
(`kiem_phu_chu`, `kiem_lock`) chỉ chắc chắn có ở đó; `h2dev\pipeline` bên máy 2 là checkout git
riêng, có thể cũ hơn nhiều ngày. Chạy sai cây sẽ báo "Không có profile '<lane>'" — đó là dấu hiệu
đang đứng ở `h2dev\pipeline`, không phải profile thiếu. (Máy 2 hỏi đúng chỗ này 24/09 vì §3 bản cũ
không ghi `cd`.) KHÔNG copy profile/tts.py/gate_common.py từ bundle sang `h2dev` cho "đồng bộ 2 cây"
— hai cây khác thế hệ, trộn tay là mất luôn cách biết bản nào đang chạy.

`--redo-voice` = lồng tiếng lại (KHÔNG dùng `--from B4`: nó xoá state B5W → pipeline gọi LLM viết lại img_prompts.txt, lệch với ảnh đã vẽ — máy 2 bắt được 2026-09-24), vì B0–B3 (kịch bản) máy 1 đã làm và đã khoá sha256.
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

`FlowHandoff_local\results\video_render\<publish.upload_channel>\<slug>\` — ví dụ lane E là
`results\video_render\kenko-chiebukuro\<slug>\`. ⛔ **MỘT CHỖ DUY NHẤT cho MỌI lane (chốt 2026-09-24).**

Vì sao không theo tên tab sheet nữa: (1) đây là chỗ `make_video.py` B11 TỰ ghi (bundle đặt `upload_dir =
../../../results/video_render`), không ai phải gõ tay; (2) tên tab ĐỔI được (24/09 `70dai-kenko` → `E-70dai-kenko`),
`upload_channel` thì không; (3) trước đây tài liệu này ghi `results\<tên-tab>\` còn `dong_goi_may2.py` ghi
`results\video_render\<upload_channel>\` → 2 nguồn cãi nhau, máy 2 giao lệch (kenko ep01 ở `results\70dai-kenko\`,
Lane F ở `results\video_render\teinengo-real\`). Nguồn chân lý nay là code `dong_goi_may2.py` (dòng TRẢ HÀNG của
`_BANGIAO.txt`) — tài liệu chỉ nhắc lại; muốn đổi thì sửa code.

Phụ đề: lane không cháy chữ (`burn_subs=false`) giao `voice.srt` (cho final.mp4) + `voice_with_hook.srt`
(cho final_with_hook.mp4, `ghep_hook_noi_truoc.py` tự sinh).

⚠️ **Bài học 2026-09-23:** hàng xếp 2 tầng `results\video_render\<kênh>\<slug>\` chứ không phải
`results\<slug>\`. Quét dọn mà chỉ nhìn một tầng thì bỏ sót — đã sót thật 1,52 GB.

Xong thì ghi cột trạng thái trên Google Sheet theo quy ước của lane (lane E: cột H, một ô,
`Video done - <slug>` + xuống dòng + đường dẫn).

⛔ **CỘT SHEET KHI MÁY 1 GIAO (anh chốt 2026-09-24, MỌI lane):** tập xong phần máy 1 → **cột D (KỊCH BẢN) = `Done`**
(để mọi người biết tập đã xong) + **cột H (STATUS-IMG) = `cần ảnh (...)`** = LỆNH GIAO VIỆC cho máy 2.
`dong_goi_may2.py --job` tự ghi cả hai (không đè ô đã có chữ khác).

## 7. Tiêu đề · mô tả · tags · thumbnail — TỰ gọi dự án YT-TITLE-RESEARCH (2026-09-24)

`pipeline/goi_title.py` được gọi TỰ ĐỘNG ở cuối cả 3 đường giao máy 2
(`dong_goi_may2.py --job`, `drive_handoff.py upload-job`, `goi_buoc2_3.py`) — anh không gõ tay nữa.
Chi tiết đầy đủ: `docs/PHUONG_AN_TU_GOI_TITLE.md`.

- **Công tắc từng lane — `publish.title_auto` (anh chốt 2026-09-24):** KÊNH MỚI MẶC ĐỊNH TẮT. Anh chạy
  setup TITLE tập đầu bằng tay, ưng rồi mới bật: `py -3.13 pipeline\goi_title.py --bat <lane>`
  (`--tat <lane>` để tắt, `--trang-thai` xem mọi lane). Đang BẬT: satori-jp-obaa, toshi-densetsu-jp,
  kenko-chiebukuro, teinengo-real, teinengo-tanoshimi. Đang TẮT: irogatatarukioku (chưa từng chạy
  thumbnail bên TITLE lần nào).
- **Điều kiện kèm:** `publish.listing_external: true` (h2dev **thôi** tự viết tiêu đề/mô tả/thumbnail,
  bỏ B7/B9 — hai bên KHÔNG được cùng ghi 1 file).
- **Nhịp chạy:** tiêu đề+mô tả (~10') → **tags ‖ thumbnail song song** → sol-check → publish → Sheet.
  Đo thật ep02 Lane F lúc chạy nối đuôi: 35–45 phút.
- **Nhận lane:** `goi_title.py` tự dò `id` profile bằng cách so đường dẫn tập với `slug_dir` —
  không đoán theo tên. `--profile` sai lệch với lane dò được → DỪNG.
- **Cổng trước khi chạy:** thiếu cấu hình bên `YT-TITLE-RESEARCH\config\lanes\<id>.{json,thumb.yaml}`,
  thiếu `deliver_root` (thư mục CHANEL), chưa bật `listing_external`, hoặc `HOOK_TAP.md` chưa đạt
  (lane có hook) → DỪNG kèm lý do, KHÔNG chạy bừa.
- **Thumbnail: máy TỰ CHỌN** (không cần ai xem 3 ảnh A/B/C) — lấy đề xuất của Opus; nếu Opus vẫn đòi
  sửa sau 2 vòng thì `goi_title.py` tự ép `--choose` theo `chosen` trong `fable_review.json`.
- Chạy NỀN, không chặn lệnh giao máy 2. Theo dõi: `<tập>\research\TU_DONG_TITLE.log` +
  `TU_DONG_TITLE.json` (`running:*` / `done` / `error:*`).
- Tắt tạm thời 1 lần: `--no-title` (đường `dong_goi_may2.py`/`goi_buoc2_3.py`) hoặc env
  `GOI_TITLE_TAT=1` (đường `drive_handoff.py`).
