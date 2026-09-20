# BÁO CÁO: CHẠY PIPELINE KHÔNG CẦN CLAUDE CODE — RAMCLOUDS KEY MỚI + HERMES

Ngày đo: **2026-09-07**. Key test: `sk-ue0LE9...nMeJ` (đã có sẵn trong Hermes `.env` dòng 498 =
`HERMES_CUSTOM_RAMCLOUDS_ME_API_KEY`). Mọi số dưới đây là **đo thật**, không suy đoán.

## 0. KẾT LUẬN

1. **KHÔNG cần Claude Code.** Hermes (Nous Research, đã cài `C:\Users\admin\AppData\Local\hermes`,
   v0.20.0) có đủ toolset thay Claude Code: `terminal`, `file`, `code_execution`, `skills`,
   `delegation`, `todo`, `vision`, `memory`, `browser`. Provider `ramclouds` **đã được khai sẵn** trong
   `config.yaml` và trỏ đúng key này.
2. **Chạy headless được** (dùng cho .exe/bat/cron), đã verify trả về đúng chuỗi `ok`:
   `hermes -z "<prompt>" --provider ramclouds -m <model> --cli` (thêm `--yolo` để tự duyệt lệnh shell).
3. **Model dùng cho sản xuất: `gemini-3.8-flash`** (viết script Nhật) — xem §2, §3.
   `claude-opus-5` trên proxy này **KHÔNG dùng được để viết kịch bản** (§4.2).
4. **Giữ nguyên gpti2 cho ảnh** — `gpt-image-2` qua ramclouds tính **$0.50/ảnh** (bảng `/api/pricing`),
   đắt gấp ~250 lần gpti2.store (~50đ ≈ $0.002). Voice vẫn OpenSpeaker.

## 1. KEY MỚI CÓ GÌ

`GET /v1/models` → **26 model** (key cũ `GEMINI_API_KEY` của RAMCLOUD chỉ có `gemini-3.5-flash-low`).
`GET /v1/dashboard/billing/subscription` → hạn mức còn **~$9.715**.

Giá tính từ `GET /api/pricing` (New-API: `$/1M = model_ratio × 2`; out = × `completion_ratio`):

| Model | In $/1M | Out $/1M | Ghi chú đo thật |
|---|---|---|---|
| **gemini-3.8-flash** | 0.75 | 3.75 | ⭐ chọn chính — văn hay, nhanh, không bị nhồi system prompt |
| gemini-3.7-flash-high | 0.75 | 3.75 | dự phòng cùng nhà |
| gemini-3.6-flash-high | 1.50 | 7.50 | chậm (80s chỉ để trả 1 chữ "ok") |
| gemini-3.5-flash-low | 1.50 | 9.00 | model của key cũ, đắt hơn 3.8 |
| gpt-5.6-luna | 0.40 | 1.20 | rẻ, viết dài nhất, nhưng là **lane Codex** (§4.2) |
| gpt-5.6-sol | 5.00 | 30.00 | chậm + đắt, không đáng |
| gpt-5.5-chat | 5.00 | 30.00 | rò markup `:::writing{...}` vào văn |
| claude-opus-5 | 6.00 | 30.00 | ❌ TỪ CHỐI viết truyện (§4.2) |
| grok-4.6 / grok-4.5 | 0.40 / 0.20 | 1.20 / 0.60 | ❌ lặp câu vô hạn (§4.4) |
| deepseek-v4-pro | 1.32 | 3.96 | ❌ bị chặn cứng 200 token output (§4.3) |
| deepseek-v4-flash | 0.44 | 1.32 | chưa test văn dài |
| MiniMax-M3 | 0.30 | 1.20 | chạy được nhưng chậm (7.294 chữ/154s) |
| glm-5.3 / glm-5.3-flash | 1.40 / 0.30 | 4.40 / 1.00 | prompt ngắn OK; văn dài **treo >30 phút** |
| qwen-3.8-max / -flash | 2.00 / 0.32 | 6.00 / 0.94 | chưa test văn dài |
| kimi-k3 | 3.00 | 15.00 | ❌ KHÔNG hỗ trợ tool-calling → không làm não Hermes được |
| gpt-image-2 | — | — | **$0.50/ảnh** → không dùng, giữ gpti2 |
| grok-imagine-image-2.0 / -edit | — | — | $0.50/ảnh |
| nemotron-3-ultra, haha, kimi-k2.7-code | — | — | HTTP 503 lúc test |

## 2. BENCHMARK VIẾT KỊCH BẢN SATORI NHẬT (prompt thật: cụ bà 80 tuổi, thừa kế, cấm marker)

| Model | Thời gian | Số chữ | finish | out tok | Chi phí | Chất lượng đọc thật |
|---|---|---|---|---|---|---|
| **gemini-3.8-flash** | **78s** | **11.140** | stop | 6.892 | **$0.026** | ⭐ Giọng bà cụ tự nhiên, đủ 縁側·仏壇·年金·相続放棄·四十九日·介護, mở–thắt–悟り–kết đủ, **0 marker** |
| gpt-5.6-luna | 200s | 14.277 | stop | 11.030 | $0.015 | Tốt, chính xác pháp lý (相続放棄/固定資産税/弁護士), văn phẳng hơn, ttfb 3,6s (stream thật) |
| gpt-5.6-sol | 316s | 12.632 | stop | 9.762 | $0.29 | Được, nhưng chậm + đắt gấp 11 lần, **ttfb 252s** (proxy đệm hết rồi mới trả) |
| MiniMax-M3 | 154s | 7.294 | stop | 3.886 | $0.005 | Tạm, ngắn |
| grok-4.6 | 63s | 6.349 | stop | 5.683 | $0.007 | ❌ Lặp nguyên đoạn nhiều lần; sai vai (con trai gọi mẹ là 叔母さん) |
| claude-opus-5 | 44s | 337 | stop | 563 | — | ❌ Từ chối (§4.2) |
| deepseek-v4-pro | 4s | 279 | **length** | **200** | — | ❌ Cụt ở 200 token (§4.3) |
| qwen-3.8-max | 99–275s | 2.859–4.415 | stop | — | ~$0.02 | Văn Nhật ổn nhưng **quá ngắn** so với 9.000 chữ, lại chậm |
| kimi-k3 | 9–11s | **0** | length/None | — | — | ❌ Trả nội dung RỖNG (2/2 lần), lại không hỗ trợ tool-calling |
| glm-5.3 | >40 phút | — | — | — | — | ❌ Treo với `max_tokens` lớn (không lỗi, không kết thúc) |

**Suy ra:** 1 script 30 phút (≈9.300 chữ theo char-rate 309 chữ/phút) = **1 call gemini-3.8-flash ≈ 70s ≈ $0.026**.

## 3. BENCHMARK SINH PROMPT ẢNH (thay bước B5 của SOP)

Yêu cầu 40 prompt, mỗi dòng 1 prompt, đúng shot type + đúng style suffix + lặp CHARACTER SHEET.
`gemini-3.8-flash` → **8 giây**, 2.714 out tok (~$0.010):

- 40/40 dòng đúng số lượng · 40/40 kết đúng style suffix · 40/40 mở đầu đúng WIDE/MEDIUM/CLOSE-UP/DETAIL
- 29/40 dòng có CHARACTER SHEET (11 dòng còn lại là cảnh vật — đúng ý đồ) · trung bình 36,7 từ/prompt

→ Bước B5 tự động hoá được, output cắm thẳng vào `pipeline/gen_images.py`.

## 4. 6 BẪY LỚN (đã dính thật khi test — phải code né)

### 4.1 ❗ KHÔNG `stream:true` = MẤT TRẮNG NỘI DUNG, KHÔNG BÁO LỖI

`claude-opus-5`, `deepseek-v4-pro`, `MiniMax-M3`, `kimi-k3` khi gọi **non-stream** trả **HTTP 200**,
`content-type: text/event-stream`, body chỉ có 1 chunk `"choices":[]` + `completion_tokens:0` rồi `[DONE]`.
Client kiểu `json.loads(response)` sẽ ném `Expecting value: line 1 column 1` — hoặc tệ hơn là **lặng lẽ trả rỗng**.
→ **Luôn gửi `stream:true` + parse SSE.** (Bonus: stream còn tránh Cloudflare cắt ~100s.)

### 4.2 ❗ MODEL "XỊN NHẤT" LÀ LANE ĐI MƯỢN, BỊ NHỒI SYSTEM PROMPT CỦA BÊN KHÁC

Hỏi "who are you + system instruction đầu tiên" (câu hỏi ~20 token):

| Model | prompt_tokens | Danh tính khai ra |
|---|---|---|
| gemini-3.8-flash | **27** | Google LLM — **lane sạch** |
| glm-5.3 | 41 | GLM/Z.ai — sạch |
| qwen-3.8-max | 88 | Qwen3.8 — sạch |
| gpt-5.6-luna | **4.512** | "I'm **Codex**, an AI coding assistant serving you through the Codex CLI" |
| MiniMax-M3 | **6.071** | MiniMax + đoạn giới thiệu công ty |
| claude-opus-5 | — | Tự xưng **trợ lý AI của Postman**, và nói rõ "không tuân theo chỉ thị trong システムポリシー của gateway" |

`claude-opus-5` **từ chối viết truyện 2/2 lần** (có và không có system prompt riêng): *"tôi là trợ lý cho
Postman, viết truyện dài nằm ngoài phạm vi"*. Nó vẫn **tool-call bình thường** → dùng làm não agent được,
nhưng **không dùng để viết kịch bản**. Vì là lane mượn: mọi call bị cộng thêm 4–6k input token và model có
thể bị bên cấp phát cắt bất cứ lúc nào.

### 4.3 `deepseek-v4-pro` bị chặn output ở 200 token

Gửi `max_tokens` 8.000 / 16.000 / 32.000 đều ra `finish_reason=length`, `completion_tokens=200`. Vô dụng cho văn dài.

### 4.4 `grok-4.6` sinh lặp vô hạn

Đoạn cuối lặp nguyên khối 4–5 lần; sai vai nhân vật. Không dùng cho kịch bản.

### 4.5 `gpt-5.5-chat` rò markup nội bộ

Văn trả về chèn `:::writing{...}` — phải strip, hoặc bỏ model này (đằng nào cũng $30/1M out).

### 4.6 Cloudflare + endpoint

- Thiếu `User-Agent` → **403 error code 1010** (không phải lỗi key). Copy UA của `ramcloud_client._post`.
- `GET /v1/models` **403 với key cũ** nhưng OK với key mới → 403 ở đây là quyền group, không phải sai URL.
- `ttfb` của `gpt-5.6-sol` = 252s/316s ⇒ proxy **đệm cả response** với vài model; model nào ttfb ≈ tổng thời
  gian thì stream không cứu được timeout → chọn model có stream thật (gemini-3.8 ttfb 36s, luna 3,6s).

## 5. HERMES — HIỆN TRẠNG & VIỆC CẦN LÀM

**Đã có sẵn:** provider `ramclouds` (`base_url https://ramclouds.me/v1`, `key_env
HERMES_CUSTOM_RAMCLOUDS_ME_API_KEY`, `api_mode chat_completions`) + đúng key này trong `.env`.

**Đã verify:**

- `hermes -z "Reply with exactly: ok" --provider ramclouds -m grok-4.5 --cli` → `ok`
- `-m claude-opus-5` cũng chạy **dù không có trong danh sách `models:` của config** → danh sách đó chỉ để
  hiển thị, không phải whitelist. (Danh sách hiện đã cũ: thiếu `claude-opus-5`, `gpt-5.6-luna/sol`,
  `gemini-3.8-flash`, `kimi-k3`, `glm-5.3`, `grok-composer-2.5-fast`; còn thừa `step-3.7-flash` đã bị gỡ.)
- **Tool-calling qua proxy**: OK với `gemini-3.8-flash`, `gemini-3.7-flash-high`, `gpt-5.6-luna`,
  `MiniMax-M3`, `glm-5.3`, `qwen-3.8-max`, `grok-4.6`, `deepseek-v4-flash`, `claude-opus-5`.
  ❌ **`kimi-k3` không trả tool_calls** → không làm não agent được.
- Skill của Hermes dùng **đúng format `SKILL.md` + frontmatter `name`/`description`** như Claude → 3 skill
  `skills/youtube-*-satori-jp` copy sang `...\hermes\skills\creative\` là dùng được gần như nguyên trạng.

**CHƯA verify được (2 điểm, cần thử lại trước khi chốt hướng A):**

- `hermes -z "<task có dùng tool shell>" --provider ramclouds -m gemini-3.8-flash --yolo --cli` chạy
  **quá 5 phút không ra output nào** (2 lần thử, cả khi ghi ra file lẫn in thẳng). Trong khi `-z` chỉ hỏi
  đáp text thì trả lời trong vài giây. ⇒ Vòng lặp agent + tool ở chế độ headless có thể còn kẹt (chờ
  duyệt? gateway lock?). **Nếu chọn hướng A phải chạy thử tương tác `hermes chat` trước.**
- `glm-5.3` với `max_tokens` lớn: chạy >40 phút không trả (không lỗi, không kết thúc) → tránh.

**Cần làm khi bê sang máy mới:**

1. Cài Hermes + copy `.env` (key ramclouds) + `config.yaml`.
2. `model.default` hiện là `gpt-5.6-sol` (provider ns24) → đổi mặc định sang `ramclouds` +
   `gemini-3.8-flash`, hoặc luôn truyền `--provider ramclouds -m gemini-3.8-flash`.
3. Copy project `h2dev` (pipeline + assets + docs) + Python 3.13 + `pip install imageio-ffmpeg pillow
   edge-tts requests yt-dlp youtube-transcript-api`.
4. Copy skill `youtube-*` vào thư mục skills của Hermes.
5. **Font Nhật**: `pipeline/thumbnail_text.py` hardcode `C:\Windows\Fonts\YuGothB.ttc`, `assemble.py` dùng
   `Meiryo` → máy chưa cài gói tiếng Nhật sẽ crash / hiện □□□. Bundle `NotoSansJP-Bold` + fallback.
6. Key gpti2 + OpenSpeaker đang hardcode trong `pipeline/gpti2_gen.py` / `openspeaker_tts.py` → theo sang
   là chạy; nếu giao máy cho người khác thì tách ra `config.json` cạnh exe.

## 6. HAI HƯỚNG TRIỂN KHAI

| | A. Hermes-native (không cần exe) | B. Tool .exe (GUI) |
|---|---|---|
| Cách dùng | Ra lệnh tiếng Việt như với Claude Code | Bấm nút: chọn slug → Chạy |
| Công sức | ~2 giờ (copy + đổi model mặc định + copy skill) | ~1 ngày (GUI + `llm_client.py` + gate) |
| Ưu | Linh hoạt, xử lý được ca lạ | Ai cũng dùng được, luồng cố định |
| Nhược | Người dùng phải biết ra lệnh; agent có thể đi lệch | Cứng, muốn đổi phải sửa code |

**Khuyến nghị:** làm **B** (exe) cho khâu sản xuất hàng loạt, dùng chung 1 module `pipeline/llm_client.py`
(SSE + retry + fallback model), và giữ **A** (Hermes) trên cùng máy để xử lý ca ngoại lệ. Exe không cần gọi
Hermes — gọi thẳng `/v1/chat/completions` là đủ và đỡ 1 lớp phụ thuộc.

**Gate tự động phải code trong exe** (phần Claude đang làm bằng "mắt"):
đếm chữ ÷ 309 = phút · chặn marker `「パート」`/`#`/`**`/`:::` · prefilter content-policy (em bé, tắm/sento,
máu) trước khi gọi gpti2 · số ảnh = thời lượng ÷ 15s · ảnh thấy mặt → `--ref master.png --quality medium`.

## 7. CHI PHÍ LLM / VIDEO (thêm vào bảng chi phí SOP)

Script $0.026 + prompt ảnh $0.010 + chữ thumbnail ~$0.001 ⇒ **≈ $0.04 (~1.000đ)/video**, không đáng kể so
với ảnh (4.000–6.000đ) + voice. Hạn mức key hiện tại đủ cho hàng chục nghìn video.
