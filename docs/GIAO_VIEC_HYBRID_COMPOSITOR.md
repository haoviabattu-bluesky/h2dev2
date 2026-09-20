# GIAO VIỆC — COMPOSITOR HYBRID STOCK + AI (bước 3, giao agent khác)

> Người giao: Claude Code (đầu não, bước 1) · Ngày: 2026-09-16 · Mức: cần agent bước 3 (Hermes/
> DeepSeek) viết code + chạy render. **Claude Code không tự dựng/ghép video — xem CLAUDE.md mục
> "⛔ CẤM TUYỆT ĐỐI"**, đây là bàn giao thuật toán, không phải báo cáo đã làm.

## 0. Việc này là gì

Ghép 1 video hybrid (stock thật xen ảnh AI) cho MỘT tập bất kỳ đã có đủ input ở mục 1, theo đúng
chính sách slot đã duyệt (`references` trong skill Hermes `hybrid-stock-ai-slot-compositor.md` +
quyết định bổ sung dưới đây, đã thay thế 1 phần logic cũ). Đây là **bản thử cô lập**, không đụng
pipeline chính, không ghi đè `final.mp4`, không giao hàng, không ghi Sheet — dừng ở việc tạo ra
`final_stock_mix.mp4` + `mixed_timeline.json` để chủ dự án xem và duyệt.

## 1. Input cần có (đọc-only, không sửa)

Trong thư mục tập (`assets/satori_jp/<slug>/`):
- `img/001.png…NNN.png` — ảnh AI, mỗi ảnh 1 slot.
- `anchors.txt` — map `NNN.png|<câu neo>` để tính mốc thời gian thật của từng slot.
- `voice_paced.srt` + `voice_paced.wav` — phụ đề + audio đã giãn nhịp (nguồn thời lượng thật).
- `stock/manifest.csv` (17 cột, xem ep1/ep21 làm mẫu) — asset thật đã tải, cột `status=OK` mới
  dùng được; `prompt_line` nối asset với dòng `img_prompts.txt` (= số thứ tự ảnh AI/slot).
- `stock/_filler/*.jpg` — pool ảnh thiên nhiên chung (không cần khớp nội dung), dùng khi 2 slot
  video thật đứng liền nhau.

Output ghi vào `scratch_analysis/stock_hybrid_<slug>/output/`:
`final_stock_mix.mp4`, `mixed_timeline.json`, `README.md` (kèm chính sách + giới hạn), và nếu cần
phụ đề Việt để soát nội dung thì thêm `final_stock_mix_vi_preview.mp4` (bản riêng, không dùng đăng).

## 2. Xây timeline CHUẨN (trước khi ghép)

1. Với mỗi ảnh `img/NNN.png`, tra `anchors.txt` ra câu neo → tìm câu đó trong `voice_paced.srt` →
   mốc bắt đầu thật `S_raw[i]`.
2. `S[0] = 0` (ép cứng, không dùng mốc cue đầu tiên — mở đầu có thể có khoảng lặng).
3. `S[N] = audio_len` (đọc bằng `imageio_ffmpeg`, xem cách làm trong
   `scratch_analysis/stock_hybrid_ep1_static/compose_hybrid_ep1_static.py::media_seconds`).
4. Độ dài chuẩn từng slot: `L[i] = S[i+1] - S[i]`.
5. Với mỗi slot có `manifest.status == OK` cho `prompt_line == i`: nạp `V[i]` = độ dài thật của
   asset (0 nếu là ảnh tĩnh — ảnh tĩnh không có khái niệm "ngắn/dài hơn chuẩn", luôn dùng trọn `L[i]`
   đứng yên, không zoom/pan/rung, xem mục 4).

## 3. Quyết định biên (đã suy nghĩ kỹ, ÁP DỤNG ĐÚNG NHƯ SAU — không tự đổi số)

Ba câu hỏi biên đã đặt ra và chốt lại (thay 1 phần đề xuất ban đầu — đọc kỹ, đề xuất ban đầu về
"trần = mượn trọn slot kế" và "sàn 1,5s bỏ hẳn cảnh" đã bị BÁC, dùng bản dưới đây):

| Hằng số | Giá trị | Lý do |
|---|---|---|
| `DRIFT_MAX` | 2,5 giây | Trần dịch một ranh giới. Mượn "trọn slot kế" (đề xuất cũ) làm ảnh AI của slot đó biến mất khỏi màn hình trong khi lời thoại của nó vẫn đang đọc — đúng lỗi "cảnh lạc lời" đã từng đo được ở lane stock (30% cảnh lạc, B8Q vẫn báo sạch). 2,5s là đủ để hấp thụ lệch nhẹ mà không gây lạc nội dung rõ rệt. |
| `MIN_SLOT` | 2,5 giây | Sàn dưới của MỌI slot sau khi co giãn. Không dùng 1,5s (quá ngắn cho giọng kể chậm của người già — khán giả chưa kịp nhận ra hình đã đổi). |
| `MAX_CLIP` | 15 giây | Một clip stock không được chạy liên tục quá 15s dù nó dài hơn — clip Pexels thường có chuyển động lặp/loop nhẹ, chạy quá lâu lộ vòng lặp, phản tác dụng "chuyển động tự nhiên". |
| Ranh giới đầu/cuối | Cố định tuyệt đối | `S[0]=0`, `S[N]=audio_len` không bao giờ bị dịch — chỉ ranh giới NẰM GIỮA 2 slot liên tiếp mới co giãn. Chống trôi tích luỹ và tránh khung đen/tiếng thừa ở đầu-cuối video. |
| Khi slot chạm sàn | **KHÔNG BAO GIỜ bỏ hẳn slot** (đề xuất cũ có ngoại lệ `@REF` — bỏ luôn ngoại lệ đó, không cần nữa) | Ảnh AI đã vẽ đúng ngữ cảnh + đúng neo lời — bỏ 1 slot là làm lệch vĩnh viễn hình so với lời từ đó về sau. Đổi hướng: khi slot kế bị bóp chạm sàn, **cắt bớt đuôi clip stock của slot đang mượn** thay vì hy sinh slot kế (cắt 1-2s đuôi 1 clip cảnh thiên nhiên không ai nhận ra; bỏ nguyên 1 slot thì nhận ra ngay). |

## 4. Thuật toán ghép — làm tuần tự đúng thứ tự dưới đây

Ký hiệu: `i = 0..N-1` (slot theo thứ tự ảnh AI); `S[i]`/`L[i]` như mục 2; `V[i]` = độ dài clip thật
tại slot i (chỉ áp dụng slot có video `status=OK`; ảnh tĩnh stock hoặc không có stock thì bỏ qua
toàn bộ bước 4, dùng thẳng `L[i]` như slot ảnh AI thường).

**Bước A — Chèn filler khi 2 slot video liền nhau (làm TRƯỚC khi tính co giãn):**
Với mọi cặp `(i, i+1)` mà cả hai đều có `status=OK, media_type=video`:
- Lấy 1 ảnh bất kỳ chưa dùng trong `stock/_filler/` (xoay vòng, không lặp lại ảnh filler quá 1 lần
  trong cùng video nếu pool đủ).
- Filler chiếm `FILLER_DUR = 3 giây`, đặt ở **ĐẦU slot i+1** (không đụng slot i): tức là trong
  khoảng `[S[i+1], S[i+1]+3s]` hiện ảnh filler đứng yên (không zoom/pan), sau đó clip thật của
  slot i+1 mới bắt đầu chạy TỪ FRAME 0 của nó trong phần thời lượng còn lại của slot i+1.
- Nếu `L[i+1] < 2 × MIN_SLOT` (tức chèn 3s filler sẽ làm phần clip thật còn lại dưới sàn) → **huỷ
  clip thật của slot i+1**, dùng ảnh AI gốc cho slot i+1, KHÔNG chèn filler (ảnh AI đứng cạnh video
  thật ở slot i vẫn ổn, không cần filler ngăn giữa ảnh AI và video thật).
- Xử lý theo thứ tự trái → phải; nếu slot i+1 bị huỷ ở bước này thì cặp `(i+1, i+2)` tính lại từ
  đầu (coi slot i+1 như slot ảnh AI thường khi xét cặp kế tiếp).

**Bước B — Tính ranh giới co giãn `B[i]` cho từng slot còn lại (video/ảnh chưa bị huỷ ở bước A):**
Duyệt `i = 0..N-1`, mỗi `B[i]` (ranh giới GIỮA slot i và i+1) tính **từ mốc chuẩn gốc `S[i+1]`**,
không cộng dồn từ `B[i-1]`:

- Nếu slot i là ảnh (AI hoặc ảnh stock tĩnh) → `B[i] = S[i+1]` (không đổi).
- Nếu slot i là video và `V[i] > L[i]` (dài hơn chuẩn):
  - Nếu slot i+1 CŨNG là video, hoặc i là slot cuối cùng (`i == N-1`) → không có chỗ mượn,
    `d = 0`: cắt clip đúng tại `L[i]` (không được lấn sang video khác hoặc lấn ra ngoài video).
  - Ngược lại: `d = min(V[i] − L[i], DRIFT_MAX, MAX_CLIP − L[i], L[i+1] − MIN_SLOT)`, lấy
    `d = max(d, 0)`. `B[i] = S[i+1] + d`. Clip cắt tại `L[i] + d` (chạy từ frame 0 tới đó).
- Nếu slot i là video và `V[i] < L[i]` (ngắn hơn chuẩn), thiếu `g = L[i] − V[i]`:
  - Nếu `g ≤ DRIFT_MAX` → `B[i] = S[i+1] − g` (ranh giới dịch sớm lên, slot i+1 dài ra bù).
  - Nếu `g > DRIFT_MAX` → **không dịch ranh giới** (`B[i] = S[i+1]`): trong khoảng thời lượng của
    slot i, phát clip thật hết `V[i]` giây rồi **đóng băng KHUNG HÌNH CUỐI của chính clip đó** (frame
    cuối cùng, đứng yên) cho `g` giây còn lại — không lặp clip từ đầu.
    ⚠️ **SỬA 2026-09-16: KHÔNG dùng "ảnh AI gốc của slot i" cho việc này nữa** — từ nay máy 2 CHỈ vẽ
    ảnh AI cho các dòng thuộc nhóm AI trong `stock_plan.tsv` (xem mục 3b), các dòng STOCK **không có
    ảnh AI dự phòng** trong `img/`. Freeze-frame của chính clip là lựa chọn duy nhất còn lại — đúng
    tinh thần lane này (người xem chủ yếu NGHE, đứng hình 1-2 giây trên khung cảnh không quan trọng).
  - Nếu `V[i] < 1,5s` (quá ngắn để có ý nghĩa là B-roll) → coi như KHÔNG có stock, dùng thẳng ảnh AI
    trọn `L[i]` (bỏ qua toàn bộ nhánh video cho slot này).

**Bước C — Chạm sàn (áp dụng SAU bước B, kiểm tra lại toàn bộ):**
Sau khi có mọi `B[i]`, tính độ dài thực tế mỗi slot `L'[i] = B[i] − B[i-1]` (với `B[-1] = S[0] = 0`).
Nếu có `L'[i] < MIN_SLOT`:
- Nguyên nhân luôn là slot `i-1` (video dài hơn chuẩn) đã mượn `d` khiến slot i bị bóp. Giảm `d`
  của slot `i-1` xuống đúng mức để `L'[i] = MIN_SLOT` (tức cắt clip của slot `i-1` ngắn lại thêm,
  KHÔNG bỏ slot i). Tính lại `B[i-1]` và lan truyền ảnh hưởng sang `B[i-2]` nếu cần (rất hiếm, chỉ
  xảy ra khi 2 slot liền kề đều mượn về cùng 1 phía).
- Ghi log rõ slot nào bị điều chỉnh ở bước này để đưa vào báo cáo.

**Bước D — Dựng clip từng slot rồi nối (giữ nguyên kỹ thuật render đã verify ở ep1):**
Với mỗi slot: ảnh AI/ảnh stock → `-loop 1 -t <duration>` đứng yên (không zoom/pan/rung); video stock
→ cắt đúng đoạn đã tính ở trên, giữ chuyển động gốc, chuẩn hoá `scale+crop` về 1920×1080. Nối toàn
bộ bằng `ffmpeg concat`, mux với `voice_paced.wav`.

## 3b. Từ STT2 trở đi — máy 2 CHỈ vẽ nhóm AI, `img/` sẽ CÓ LỖ HỔNG (anh chốt 2026-09-16)

Trước đây (STT1/ep21) máy 2 vẽ đủ 100% mọi dòng kể cả dòng đã có stock. **Từ STT2 đổi hướng: máy 2
chỉ vẽ những dòng nhóm `AI` trong `stock_plan.tsv`** (marker + LLM xác định có người) — dòng nhóm
`STOCK` (đã có video/ảnh thật thay thế) **không cần vẽ nữa**, tiết kiệm việc cho máy 2 thật (không
phải chuyện tiền — Flow 0đ — mà đỡ thao tác thủ công/thời gian tab).

Hệ quả cần biết trước khi giao việc:
1. **`img/` của tập hybrid sẽ THIẾU ảnh cho mọi dòng STOCK** — không còn "ảnh AI dự phòng" cho các
   dòng đó (đã sửa mục 4 Bước B ở trên: dùng freeze-frame thay vì ảnh AI). Vì vậy **pipeline chuẩn
   `chay_buoc3.py`/`render_engine.py` sẽ KHÔNG chạy được nữa cho tập này** (cổng chặn tiền "đếm
   `img/*.png` ≥ số dòng `img_prompts.txt`" sẽ luôn báo thiếu) — tập từ STT2 trở đi **chỉ có một
   đường ra là compositor hybrid**, không còn bản "100% AI" làm phương án dự phòng.
2. **Job gửi máy 2 phải đánh dấu rõ dòng nào BỎ QUA.** `img_prompts.txt` giữ nguyên (không được sửa
   — mục 8), nên đánh dấu bằng file phụ đi kèm trong CHÍNH thư mục job (sẽ được `upload-job` cuốn
   theo tự động vì nó đệ quy cả thư mục): copy `stock_plan.tsv` vào gốc thư mục tập (không phải
   `scratch_analysis/`) TRƯỚC khi `upload-job`, và thêm 1 dòng ghi chú đầu `_BANGIAO.txt` (tự sinh,
   không sửa tay) không đủ — phải tạo thêm file `HUONG_DAN_MAY2_STOCK.txt` ở gốc thư mục tập, nội
   dung: liệt kê rõ danh sách số dòng KHÔNG cần vẽ (lấy từ `stock_plan.tsv` cột `group=STOCK`) +
   1 câu "các dòng còn lại vẽ như thường, ĐỪNG tạo file .png cho các dòng liệt kê ở trên". Việc tạo
   file này thuộc bước 1 (Claude Code làm khi chuẩn bị job, KHÔNG phải sửa pipeline).
3. STT2 là ca đầu tiên đi qua đường này; từ STT3 đã đúc thành tool (mục 3c). Agent bước 3 khi nhận
   báo cáo `img/` thiếu so với `img_prompts.txt` cho tập có `stock_plan.tsv` ở gốc thư mục:
   ⚠️ **chỉ ĐÚNG THIẾT KẾ khi số ảnh thiếu = đúng số dòng nhóm `STOCK` (giữ nguyên) trong
   `stock_plan.tsv` lúc bàn giao** — mọi dòng khác (nhóm `AI`/`AI_FALLBACK`) **PHẢI CÓ ĐỦ ảnh trong
   `img/` khi bước 1 bàn giao**, không có ngoại lệ. Nếu thiếu ảnh ở dòng KHÔNG PHẢI nhóm `STOCK` thì
   đó là bước 1 CHƯA chạy xong `hybrid_chuan_bi.py` — trả lại, đừng tự gen bù ở bước 3.

## 3c. Khi audit_stock.py loại 1 dòng STOCK → BẮT BUỘC AI_FALLBACK, đừng dừng lại báo (2026-09-18)

**Sự cố đã xảy ra:** STT3 audit xong 22 dòng STOCK, chỉ 8 dòng thật sự dùng được (`status=OK`); 14
dòng còn lại (dính mặt người rõ/chữ to/file hỏng) bị bỏ ngỏ — báo cáo liệt kê "thiếu ảnh/thiếu
audio/thiếu anchors" rồi DỪNG chờ hỏi, dù đây đều là việc bước 1 tự làm được, rẻ (14 ảnh ≈ 700đ).

**Luật cố định từ nay — không cần hỏi lại mỗi lần:**
- Dòng STOCK có `manifest.csv status=OK` → giữ nguyên nhóm `STOCK`, **KHÔNG được có ảnh trong
  `img/`** (bước 3 dùng clip thật từ `stock/manifest.csv`, xem mục 3b — cấm trích khung tĩnh, xem
  memory `img-thieu-o-tap-hybrid-la-dung-thiet-ke`).
- Dòng STOCK có status khác OK (`REJECT_FACE`/`REJECT_TEXT`/`BAD_FILE`/`NONE`) → **TỰ ĐỘNG đổi
  nhóm sang `AI_FALLBACK`** trong `stock_plan.tsv`, rồi **TỰ SINH ảnh bằng gpti2** cho đúng dòng đó
  (`gen_images.py --start <dòng> --limit 1`, ~50-110đ/ảnh tuỳ có `@REF` hay không) — **được phép
  mặc định, không cần hỏi lại**, vì chi phí nhỏ và đây là việc bước 1 vốn đã làm quen (giống hệt
  cách vẽ REF-LOCK/gap-fill).

**Phân việc CỤ THỂ cho tập hybrid (chốt cứng, đọc kỹ trước khi báo "thiếu"):**

| Việc | Ai làm | Công cụ |
|---|---|---|
| Vẽ ảnh cho dòng nhóm `AI` | **Bước 2 (máy 2)** | Google Flow, trả về `FlowHandoff_local/results/<slug>/` |
| Đổi dòng STOCK bị loại → `AI_FALLBACK` | **Bước 1** | `hybrid_chuan_bi.py` (mục A) |
| Tự vẽ bù ảnh cho dòng `AI_FALLBACK` | **Bước 1** | `hybrid_chuan_bi.py` (mục C, gọi `gen_images.py`) |
| Copy ảnh máy 2 từ FlowHandoff vào `img/` | **Bước 1** | `hybrid_chuan_bi.py` (mục B) — máy 2 KHÔNG tự copy |
| Sinh giọng đọc + giãn nhịp + QC nghe | **Bước 1** | `hybrid_chuan_bi.py` (mục D: tts.py → srt_from_script.py → pace_audio.py → qc_audio.py) |
| Rào STALE + mapping invariant (mới 2026-09-18) | **Bước 1** | `hybrid_chuan_bi.py` (ngay TRƯỚC `sinh_neo.py`): `gate_common.kiem_stale` (sha256 script ≠ lúc sinh `img_prompts/img_doan` → exit 1) + `qc_img_doan --no-llm` (malformed/≠ số prompt/thiếu-trùng ID/ngoài 1..N/giảm thứ tự → exit 1); SUSPICIOUS chỉ nhắc chạy có LLM, không chặn |
| Sinh `anchors.txt` | **Bước 1** | `hybrid_chuan_bi.py` (mục E: `sinh_neo.py`) |
| Dựng `final_stock_mix.mp4` từ input đã đủ | **Bước 3 (compositor)** | thuật toán mục 2-5 file này |
| Trích khung tĩnh từ `stock/*.mp4` nhét vào `img/` | **KHÔNG AI ĐƯỢC LÀM** | cấm tuyệt đối, xem mục 3b + memory |

**Lệnh chuẩn (chạy 1 lần, tự bỏ qua phần đã xong, tự dừng đúng chỗ nếu có gate thật rớt):**
```bash
py -3.13 hybrid_chuan_bi.py --slug ..\assets\satori_jp\<slug> --profile <id_profile_giong>
```
Ra `>> ĐỦ ĐIỀU KIỆN GIAO BƯỚC 3` mới được bàn giao cho compositor. Ra `>> CHƯA ĐỦ` thì đọc đúng dòng
báo thiếu — chỉ 2 tình huống được phép DỪNG THẬT (không tự làm tiếp): (a) máy 2 chưa trả đủ ảnh
nhóm `AI` (việc của bước 2, chờ), (b) `B4Q` (QC nghe) rớt (cổng chất lượng nội dung thật, cần xem
xét chứ không tự sửa/gen lại). Mọi trường hợp khác (thiếu AI_FALLBACK, thiếu audio thô, thiếu
anchors) là script tự làm, không phải lý do để dừng.

## 5. Trường hợp biên đặc biệt phải xử lý đúng

1. **Chuỗi ≥3 slot video liền nhau**: bước A xử lý tuần tự trái→phải, mỗi cặp xét độc lập dựa trên
   trạng thái MỚI NHẤT (sau khi cặp trước có thể đã huỷ 1 slot) — không xét trước toàn chuỗi rồi mới
   chèn, tránh chèn 2 filler liền nhau.
2. **Slot đầu tiên (i=0) hoặc slot cuối cùng (i=N-1) là video dài hơn chuẩn**: slot 0 không có "slot
   trước" để ảnh hưởng ngược, slot N-1 không có "slot sau" để mượn → cả hai đều rơi vào nhánh
   `d=0` (cắt đúng `L[i]`, không mượn) ở bước B, không cần xử lý riêng.
3. **Video ngắn gần 0 giây thực tế dùng được** (`V[i] < 1,5s`, ví dụ lỗi tải chỉ còn vài frame): coi
   như không có stock, dùng thẳng ảnh AI (đã nêu trong bước B) — không cố "ghép nối" một mẩu video
   gần như vô nghĩa.
4. **Ranh giới cộng dồn không neo gốc**: bắt buộc mọi `B[i]` tính từ `S[i+1]` GỐC (chuẩn ban đầu),
   không tính từ `B[i-1]` — nếu tính lũy kế, sai số 2,5s mỗi slot sẽ cộng dồn qua hàng chục slot và
   làm cuối video lệch hẳn khỏi audio.

## 5b. RỦI RO LỆCH LỜI DO DRIFT — bắt buộc có cổng riêng kiểm (bổ sung 2026-09-16, user hỏi thẳng)

Thuật toán mục 4 CỐ Ý cho phép ranh giới giữa 2 slot dịch tối đa `DRIFT_MAX=2,5s` để giữ chuyển động
tự nhiên của video thật — đây LÀ đánh đổi thật, không phải không có cái giá: trong 2,5 giây đó, hình
đang chiếu có thể sớm/muộn hơn đúng lúc câu chuyện nhắc tới nó. Ở tốc độ đọc của lane này (~309
chữ/phút ≈ 5,15 chữ/giây), 2,5s ≈ 13 ký tự — chưa hết nửa câu ngắn, nên đây là lệch VI MÔ tại ĐÚNG
ranh giới có clip stock, không phải lệch tích luỹ lan ra toàn video (mục 4 đã ép mọi `B[i]` neo vào
`S[i+1]` gốc, không cộng dồn) — khác hẳn về bản chất với lỗi "ảnh trôi dần cuối video" mà `anchors.txt`
từng sinh ra để sửa (lỗi đó là lệch liên tục hàng chục giây, không giới hạn).

**Vẫn phải đo bằng máy, không suy luận bằng lý thuyết ở trên là đủ.** Bắt buộc thêm bước:
1. Với MỖI slot có `d ≠ 0` hoặc `g` dùng nhánh freeze-frame (tức MỌI slot bị mục 4 điều chỉnh ranh
   giới), trích 1 khung hình đúng tại `B[i]` (điểm ranh giới mới) bằng `qc_visual._frame`.
2. Đối chiếu khung đó với câu thoại đang đọc tại đúng giây đó (`voice_paced.srt`) bằng
   `qc_visual._vision(prompt, frame_path, model="gemini-3.8-flash")` (schema tự do, hỏi model:
   "khung hình này có còn phù hợp với câu thoại đang đọc tại giây này không? trả lời matches/score
   1-5/lý do ≤15 từ" — mẫu y hệt `SYNC_SCHEMA` đã có trong `qc_visual.py`, TÁI DÙNG không viết mới).
   **Model: `gemini-3.8-flash` qua ramclouds** — ĐÚNG model mặc định của `_vision()`, cùng model đã
   dùng cho `qc_video()`/`qc_images()`/`audit_stock.py` trong dự án này, KHÔNG đổi sang model khác.
   Lý do chọn: (a) đây là engine vision DUY NHẤT đã được wire sẵn qua `qc_visual._vision()` — không
   phải chọn thêm, là tái dùng; (b) `deepseek-v4-flash` (dùng ở mục 3b để phân loại/chọn stock) là
   model THUẦN VĂN BẢN, không nhận ảnh — không dùng được cho bước này; (c) việc "khung hình có khớp
   câu thoại không" giống hệt bài toán `SYNC_SCHEMA` đã verify nhiều lần trong `qc_video()`, không
   cần model mạnh hơn cho một câu hỏi match/không-match đơn giản. `_vision()` đã tự bọc lỗi hạ tầng
   thành `QcError` (phân biệt lỗi máy vs lỗi nội dung) — không cần code thêm.
3. Ngưỡng: điểm trung bình các slot có drift ≥ 3/5 và KHÔNG có slot nào ≤2/5 mới được báo ĐẠT. Slot
   nào rớt → không tự sửa số (không tự đổi `DRIFT_MAX`), báo lại kèm số đo, để đầu não quyết fallback
   riêng cho slot đó (ví dụ bỏ stock, dùng ảnh AI vẽ bù riêng đúng 1 tấm cho slot đó — chi phí rẻ hơn
   nhiều so với vẽ lại cả 126 tấm).
4. Ghi điểm từng slot có drift vào `mixed_timeline.json` (field `drift_qc_score`) — đây là cổng NGỮ
   NGHĨA thật, khác với cổng kỹ thuật ở mục 6 (thời lượng/decode/độ phân giải).

## 6. Kiểm tra bắt buộc trước khi báo ĐẠT (ad-hoc, không phải cổng B8Q chính thức)

- Tổng `Σ L'[i]` = `audio_len` chính xác (sai số ≤ 0,05s).
- Không slot nào `L'[i] < MIN_SLOT` sau bước C.
- Không clip nào chạy quá `MAX_CLIP`.
- `ffmpeg -v error -i final_stock_mix.mp4 -f null -` exit 0 (decode sạch).
- Có đủ track video + audio, đúng 1920×1080.
- Hash các file input gốc (`img_doan.txt`/`anchors.txt`/`img_prompts.txt`/`script.txt`/`final.mp4`
  hiện có nếu đã render trước đó) KHÔNG đổi trước/sau.
- `mixed_timeline.json` liệt kê đủ N slot, mỗi slot ghi rõ `mode` (ai / stock_video_trim /
  stock_video_borrow / stock_video_ai_tail / stock_image / filler), `target_duration_s`,
  `actual_duration_s`, và với slot bị điều chỉnh ở bước C thì ghi thêm `adjusted_by_step_c: true`.

## 7. Áp dụng cho tập cụ thể — `simbot2-21-HD-ADEBz5oM` (dữ liệu đã có sẵn, Pha 1 đã xong)

- Input đã tồn tại đủ: `assets/satori_jp/simbot2-21-HD-ADEBz5oM/{img/,anchors.txt,voice_paced.srt,
  voice_paced.wav,stock/manifest.csv,stock/_filler/}`.
- `manifest.csv` sau nghiệm thu (xem `docs/TRAO_DOI_HYBRID_simbot2-21-HD-ADEBz5oM.md`): **14 dòng
  `status=OK`** dùng được (13 video + 1 ảnh) trên 126 slot, còn lại giữ ảnh AI; **8 ảnh filler** sẵn
  trong `stock/_filler/`.
- Output ghi vào `scratch_analysis/stock_hybrid_simbot2-21-HD-ADEBz5oM/output/`.
- Ghi báo cáo nối vào CUỐI `docs/TRAO_DOI_HYBRID_simbot2-21-HD-ADEBz5oM.md` (mục mới, giữ nguyên
  nội dung cũ), khuôn `[AGENT] <giờ> VIỆC n: OK/LOI + số đo thật`.

## 8. Cấm

1. Không sửa `pipeline/`, `script.txt`, `img_prompts.txt`, `img_doan.txt`, `anchors.txt`, `img/`,
   `characters.json`, master/REF, `final.mp4` gốc.
2. Không giao hàng, không ghi Google Sheet cho tới khi chủ dự án duyệt bản preview.
   ⚠️ **Khi ĐƯỢC giao hàng thật (chốt 2026-09-17 sau sự cố thật):** thư mục tập (bước 1) đã có sẵn
   `TIEU_DE_MO_TA.txt` (tiêu đề+mô tả+hashtag do bước 1 viết) — **chép NGUYÊN VĂN** file đó thành
   `listting.txt` trong thư mục giao hàng, chỉ điền mốc chương thật (tìm câu mở đầu đoạn trong
   `voice_paced.srt`, thay vào chỗ `[CHƯA CÓ...]`). **TUYỆT ĐỐI không tự viết tiêu đề/mô tả mới** —
   công cụ bước 3 không hiểu nội dung, tự viết ra placeholder rỗng thì người xem thật sẽ thấy (đã xảy
   ra thật với 2 tập: `listting.txt` giao hàng chỉ còn 463-665 byte, không tiêu đề/mô tả/mốc chương).
   Thiếu `TIEU_DE_MO_TA.txt` ở bước 1 → dừng lại, báo chủ dự án, đừng tự bịa.
3. Không tự đổi 4 hằng số ở mục 3 (`DRIFT_MAX`, `MIN_SLOT`, `MAX_CLIP`, `FILLER_DUR`) — thấy bất hợp
   lý thì báo lại bằng số đo thật, không tự sửa rồi chạy.
4. Không cộng dồn ranh giới từ `B[i-1]` — luôn neo `S[i+1]` gốc (mục 5.4).
