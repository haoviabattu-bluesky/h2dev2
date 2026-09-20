# QC thumbnail + viết chữ thumbnail — HẠ TẦNG DÙNG CHUNG (GPT-5.6-sol + Opus)

Áp dụng cho **mọi lane** của dự án. Xây + verify thật 2026-09-17 trên `kenko-chiebukuro/ep01-tento-kossetsu`
(3 vòng QC + 2 vòng sửa prompt ảnh nền) và `satori-jp-obaa/simbot2-01-vU5PWT2zLDs` (so sánh trực tiếp
2 quy trình viết chữ, chốt dùng Opus — xem mục "VIẾT CHỮ THUMBNAIL" bên dưới).

## QUY TRÌNH CHUẨN (thứ tự đúng, đọc trước khi làm thumbnail cho lane bất kỳ)

1. **Viết chữ thumbnail** — `pipeline/write_thumb_text_opus.py` (Opus viết 3 phương án → Opus
   context MỚI QC tiếng Nhật/sự thật → chọn bản PASS). Mặc định cho lane có `ref_lock`/nhân vật
   (khuyến nghị bật cho mọi lane sau khi verify riêng — xem field `thumbnail.text_engine`).
2. **Sinh ảnh nền** — `gen_images.py`. **BẮT BUỘC kiểm tra ref_lock**: lane có `image.ref_lock=true`
   và prompt nền đánh dấu `@REF`/`@REF2` thì PHẢI truyền `--ref`/`--ref2` đúng ảnh master nhân vật
   CHÍNH xuất hiện trong cảnh đó (`_ref/001.png` theo quy ước) — KHÔNG được để marker bị bỏ qua
   câm lặng (bug thật đã vá 2026-09-17, xem mục "BUG ĐÃ VÁ" bên dưới).
3. **Phủ chữ** — `thumbnail_text.py` (flags theo `profile.thumbnail`, xem `_thumb_flags()` trong
   `make_video.py`).
4. **QC ảnh cuối** — `pipeline/qc_thumbnail_sol.py` (GPT-5.6-sol, có vision). Lặp bước 1/3→4 tối đa
   3 vòng nếu FIX (đọc mục CẦN SỬA, sửa đúng chỗ đó, KHÔNG đổi nội dung/claim chỉ để né QC).

**Bài học đắt giá (verify thật, đọc kỹ)**: ngay cả khi bước 1 (Opus viết + Opus tự QC văn bản) đã
chọn ra 1 phương án PASS, **bước 4 (QC ẢNH CUỐI) vẫn bắt được lỗi mà bước 1 bỏ sót** — 2 lần liền
trên `satori ep01`: banner "3年前に消えた" (nghe như "biến mất" — sai, vì 2 người vẫn gặp nhau đều
đặn) rồi "3年前に引っ越した本当の理由" (đánh tráo "lý do CHUYỂN NHÀ" thành "lý do GIẤU CHUYỆN chuyển
nhà" — khác nhau). QC-văn-bản-thuần (chỉ đọc từng dòng rời) không thấy được các suy diễn này —
**KHÔNG được bỏ qua bước 4 dù bước 1 đã PASS.** (Chạy lại lần nữa cùng ngày còn thấy y hệt: 1 phương
án khác lại lọt "親友は三年前に消えていた" qua vòng Opus tự QC — mẫu lỗi LẶP LẠI, không phải ngẫu
nhiên, càng khẳng định bước 4 không thể bỏ.)

## FILE DỊCH TIẾNG VIỆT — cho người không đọc được tiếng Nhật

`write_thumb_text_opus.py` (từ 2026-09-17) TỰ SINH THÊM 1 file `<tên>_vi.txt` cạnh
`thumb_text.txt`/`thumb_text_v*.txt`, cùng format `MÀU|nội dung` nhưng là NGHĨA TIẾNG VIỆT của đúng
dòng tiếng Nhật ở vị trí tương ứng (Opus dịch ngay trong lượt QC thứ 2, cùng lúc chốt bản cuối —
không tốn thêm lượt gọi riêng). Quy ước đặt tên `_vi` khớp với `voice_vi.srt`/`tomtat_vi.txt` đã
dùng sẵn trong dự án. File CLI gọi trực tiếp cũng tự ghi 2 file (chính + `_vi`) cạnh nhau khi có
`--out`. Nếu tự tay sửa `thumb_text.txt` (áp dụng CẦN SỬA từ QC ảnh cuối) thì **nhớ sửa luôn file
`_vi` tương ứng** — 2 file KHÔNG tự đồng bộ với nhau, tool chỉ sinh 1 lần lúc viết chữ ban đầu.

## DỰ PHÒNG KHI 9ROUTER LỖI — proxy ns24.io

`sol_client.py` (từ 2026-09-17) **tự động fallback**: gọi proxy 9router LOCAL trước, LỖI GÌ CŨNG
(connection refused/timeout/HTTP khác 200 — vd máy chưa bật 9router, đổi máy khác, cổng 20128 bận)
tự chuyển sang proxy **ns24.io** (`https://api.ns24.io/v1`, model `gpt-5.6-sol` — KHÔNG có prefix
`cx/`, khác 9router). Verify thật: model tồn tại + trả lời đúng + đọc được ảnh (vision OK) qua
`curl`/httpx trực tiếp, và verify cả kịch bản fallback thật (trỏ sai cổng 9router → tự chuyển ns24,
vẫn trả lời đúng). Người gọi `qc_thumbnail_sol.py`/`gen_thumb_bg_prompt_sol.py` KHÔNG cần biết đang
dùng đường nào — `sol_client.chat()` tự xử lý, chỉ in cảnh báo ra stderr khi phải dùng dự phòng.

⚠️ ns24 (cũng như ramclouds) **BẮT BUỘC `stream:true` + User-Agent** (thiếu 1 trong 2 là mất trắng
nội dung câm lặng hoặc bị Cloudflare chặn 403 — bài học đã ghi ở `llm_client.py`, áp dụng y hệt ở
nhánh dự phòng của `sol_client.py`). Key ns24 dùng CHUNG với key mặc định của `llm_client.py`
(cùng 1 tài khoản, khác model được gọi).

Kiểm nhanh cả 2 đường: `py -3.13 pipeline/sol_client.py` — in riêng trạng thái CHÍNH và DỰ PHÒNG,
chỉ FAIL (exit 1) khi CẢ HAI đều hỏng.

## VIẾT CHỮ THUMBNAIL — Opus (khuyến nghị) thay vì 1 lượt Gemini cũ

`pipeline/write_thumb_text_opus.py` thay cho `ai_steps.write_thumb_text()` (1 lượt Gemini/ramclouds,
KHÔNG có vòng QC nào). Cơ chế: 2 lần gọi `claude -p --model opus` RIÊNG BIỆT (qua
`pipeline/claude_p_bridge.py`, mỗi lần là 1 phiên headless MỚI hoàn toàn, không mang thiên kiến của
lượt trước) — lượt 1 viết 3 phương án khác góc độ, lượt 2 (context mới) QC tiếng Nhật + đối chiếu sự
thật, chọn bản PASS mạnh nhất (có thể tự sửa nhỏ trước khi chốt).

```
py -3.13 write_thumb_text_opus.py --profile <lane-id> \
    --title-file listting.txt --summary-file tomtat.txt --out thumb_text.txt
```
(Ở B7 THẬT trong pipeline chưa có tiêu đề chốt — `--title`/`--title-file` là TUỲ CHỌN, không truyền
thì tool tự nhận diện góc hook từ `--script-file`/`--summary`.)

**Bật cho 1 lane**: thêm `"text_engine": "opus_dual_qc"` vào `profile.thumbnail` (đã bật cho
`satori-jp-obaa` sau khi verify). `make_video.py` (`b7_thumb`) tự đọc field này, KHÔNG cần sửa code
mỗi lần bật thêm lane — lane chưa khai vẫn dùng `ai_steps.write_thumb_text()` cũ (an toàn, không đổi
hành vi lane chưa verify).

## BUG ĐÃ VÁ 2026-09-17 — REF-LOCK bị bỏ qua câm lặng khi sinh ảnh nền thumbnail

`make_video.py` (`b7_thumb`) gọi `gen_images.py` cho ảnh nền RIÊNG (`_thumb/001.png`) mà KHÔNG hề
truyền `--ref`, dù prompt (`thumb_bg_prompt.txt`) đánh dấu `@REF` và profile có `ref_lock=true` — hệ
quả: `gen_images.py` (dòng `elif tag=='ref' and refs:`) route prompt về `'plain'` vì thiếu `--ref`,
ảnh nền ra một khuôn mặt NGẪU NHIÊN, không phải nhân vật chính của tập (đo thật: mặt hoàn toàn khác
`characters.json` mô tả). Đã vá: `b7_thumb` giờ tự đọc marker đầu `thumb_bg_prompt.txt`, nếu `@REF`
thì truyền `--ref self.f("_ref")/"001.png"`; nếu `@REF2` thì dò thư mục `_ref_*/` đầu tiên tìm được
làm `--ref2` (heuristic — tập có ≥2 nhân vật phụ dùng chung kiểu tên `_ref_*` phải tự chỉ định tay).
**Kiểm tra lại mọi lane có `ref_lock=true` đã render thumbnail TRƯỚC ngày này** — có thể đang dùng
mặt sai nhân vật mà không ai biết vì marker bị bỏ qua câm lặng, không báo lỗi gì.

## Tại sao cần model thứ 2 cho QC ảnh

## Tại sao cần model thứ 2

Mọi cổng QC khác trong pipeline (`qc_visual.py`, `qc_script.py`, `qc_facts.py`) đều dùng Gemini qua
ramclouds. Cùng một nhà cung cấp + một lối tư duy chấm điểm thì lỗi hệ thống của Gemini (vd bỏ qua
claim y tế tuyệt đối, không đọc ra lỗi ngắt dòng tiếng Nhật) sẽ lọt qua mọi lớp QC. Thumbnail là
khung hình DUY NHẤT người xem thấy TRƯỚC KHI bấm play — đáng để có 1 lớp chấm bằng model khác hẳn.

**GPT-5.6-sol** chạy qua proxy **9router LOCAL** (khác hẳn ramclouds/ns24):
- Endpoint: `http://localhost:20128/v1` (chỉ chạy được trên máy đã bật 9router — máy khác sẽ
  connection refused, không phải lỗi code)
- Model id: `cx/gpt-5.6-sol` (**PHẢI có prefix `cx/`** — gọi thiếu prefix ra lỗi model not found)
- API key + base URL đã khai trong `pipeline/keys.py` qua `keys.get("sol", ...)` /
  `keys.get("sol_base_url", ...)` — đổi máy khác chỉ cần sửa `keys.json`, không cần sửa code.

## 3 tool dùng chung (đã verify chạy thật)

### 0. `pipeline/write_thumb_text_opus.py` — viết chữ thumbnail (Opus, xem mục ở trên)

### 1. `pipeline/qc_thumbnail_sol.py` — chấm thumbnail ĐÃ RENDER

```
py -3.13 qc_thumbnail_sol.py --thumb thumbnail.png --title-file listting.txt --profile <lane-id>
```
(`--title-file`: dòng ĐẦU của file là tiêu đề, đúng quy ước `listting.txt` của dự án. Có thể dùng
`--title "..."` trực tiếp, và `--summary`/`--summary-file` để đưa thêm tóm tắt nội dung.)

Chấm 6 mục (chữ tiếng Nhật · thumbnail↔title · lỗi ảnh AI · bố cục/khả năng đọc · sức hút ·
claim/độ chính xác) → trả **PASS / FIX / REMAKE** (exit code 0/2/3 — dùng được trong script khác).
Output đầy đủ in ra stdout, `--out file.txt` lưu lại nếu cần.

**Quy trình khi FIX/REMAKE** (đã verify đúng 3 vòng trên ep01, KHÔNG bịa thêm bước):
1. Đọc mục `CẦN SỬA` trong output.
2. Chỉ sửa ĐÚNG chỗ đó, giữ nguyên phần còn lại (KHÔNG tự ý đổi tiêu đề video, KHÔNG đổi
   nội dung/claim chỉ để né QC).
3. Render lại, chạy `qc_thumbnail_sol.py` lần nữa.
4. Lặp tối đa 3 vòng — quá 3 vòng vẫn FIX/REMAKE thì dừng lại hỏi user, đừng tự ý lặp vô hạn
   (nguyên tắc chung `cong-llm-phai-dat-duoc` đã có trong memory dự án).

### 2. `pipeline/gen_thumb_bg_prompt_sol.py` — viết lại PROMPT ảnh nền khi nội dung/bố cục sai

Dùng khi lỗi nằm ở **ảnh nền AI** (vd thiếu số lượng vật thể tiêu đề yêu cầu, bố cục sai) — KHÔNG
dùng khi lỗi là do tool overlay chữ (xem mục "Lỗi KHÔNG phải do ảnh AI" bên dưới, dễ nhầm).

```
py -3.13 gen_thumb_bg_prompt_sol.py --title-file listting.txt --profile <lane-id> \
    --old-prompt thumb_bg_prompt.txt --feedback "mô tả cụ thể cái gì sai" \
    --write-to thumb_bg_prompt.txt
```
Trả về ĐÚNG 1 đoạn prompt tiếng Anh hoàn chỉnh, dán thẳng vào `gen_images.py --prompts ... --quality medium`.

### ⚠️ Lỗi KHÔNG phải do ảnh AI — đừng gọi nhầm tool

Bài học thật (ep01, vòng sửa thứ 3): thumbnail bị "thọt lõm" (ảnh không cao kín khung) + mờ mép
trái — tưởng lỗi ảnh AI nhưng thật ra là do `thumbnail_text.py` tự động co ảnh 82%
(`--photo-scale`) + làm mờ dải chuyển tiếp 60px. Ảnh gpti2 sinh ra vốn đã đúng. **Trước khi gọi
`gen_thumb_bg_prompt_sol.py`, luôn mở `_thumb/001.png` (ảnh nền THÔ, chưa phủ chữ) ra xem trước** —
nếu ảnh thô đã đúng mà bản overlay chữ mới sai, sửa flag/tham số của `thumbnail_text.py`
(vd cờ `--flat-bg` — xem `_flat_bg_note` trong profile.json của lane có dùng `dedicated_bg`), KHÔNG
sinh lại ảnh vô ích.

**Bug tương tự #2 đã vá (2026-09-17, satori ep01)**: banner đỏ dưới cùng co hộp NHỎ HƠN chiều cao
mực chữ thật (hệ số `*0.87` cũ trong `thumbnail_text.py`), khiến nét đuôi Hiragana (した/けた...) đè
ra ngoài viền đỏ khi banner ngắn/chữ to. Đã bỏ hệ số co, tăng đệm 16→40px quanh tâm chữ — hộp giờ
LUÔN ≥ chiều cao mực thật. Không cần tham số CLI mới, tự áp dụng cho mọi lane có `BANNER|`.

## Form riêng của mỗi lane — khai trong `profiles/profiles/<id>.json`

Field `thumbnail_qc` (tuỳ chọn — không khai thì tool tự dùng bản mặc định chung, ít đặc thù hơn):

```json
"thumbnail_qc": {
  "claim_focus": "Đoạn text CHÈN VÀO mục 6 CLAIM/ĐỘ CHÍNH XÁC của qc_thumbnail_sol.py — mỗi \
ngách rủi ro claim khác nhau (sức khỏe: claim y tế tuyệt đối · truyền thuyết đô thị/bí ẩn: đừng \
biến giả thuyết thành sự thật khoa học đã chứng minh · lịch sử/WW2: đừng bịa chú thích/nguồn ảnh)",
  "image_prompt_constraints": "Đoạn text THAY THẾ HẲN ràng buộc bố cục mặc định của \
gen_thumb_bg_prompt_sol.py — mô tả đúng khung ảnh của lane (vd trái đen/phải ảnh thật, hay full-\
bleed không tách khung, tỉ lệ portrait...). Không khai thì tool tự suy từ `thumbnail.side_width` +\
`thumbnail.art_style` sẵn có trong profile."
}
```

Ví dụ đã khai thật: `profiles/profiles/kenko-chiebukuro.json` → `thumbnail_qc.claim_focus` (rủi ro
claim y tế) + `thumbnail_qc.image_prompt_constraints` (khung trái-đen/phải-ảnh-thật, side_width
62%, yêu cầu thể hiện ĐỦ số lượng khi tiêu đề ghi rõ con số như "5選").

**Lane mới muốn dùng QC này**: thêm 1 block `thumbnail_qc` vào profile.json của lane đó theo đúng
2 field trên — không sửa code của 2 tool, không sửa `docs/` này (chỉ ví dụ ở đây mới cần cập nhật
nếu muốn, không bắt buộc).

## Selftest nhanh khi đổi máy / nghi ngờ 9router chưa bật

```
py -3.13 pipeline/sol_client.py
```
In `✓ ... → 'OK'` là kết nối được; báo lỗi thì kiểm 9router đã chạy ở cổng 20128 chưa
(`curl http://localhost:20128/v1/models`).
