# HƯỚNG DẪN TỐI ƯU PIPELINE BƯỚC 1 — SATORI-JP-OBAA
## Tài liệu giao việc cho Claude / Claude Code

**Ngày:** 2026-09-18  
**Phạm vi:** `satori-jp-obaa`  
**Mục tiêu:** Tối ưu pipeline Bước 1 đang chạy thật, KHÔNG viết lại toàn bộ hệ thống từ đầu, KHÔNG làm giảm chất lượng nội dung, và KHÔNG chuyển các quyết định cần hiểu truyện sang model rẻ hoặc thuật toán cơ học.

---

# 0. MỤC TIÊU CỦA LẦN TỐI ƯU NÀY

Pipeline hiện tại đã hoạt động và đã được vá qua nhiều lỗi production thật. Vì vậy:

- Không được "refactor cho đẹp" rồi làm mất các rào cứng đã có.
- Không được thay các bước cần hiểu nội dung bằng chia đều / heuristic đơn giản.
- Không được dồn mọi việc sang model rẻ chỉ để giảm chi phí.
- Ưu tiên: **giảm token Claude bằng cách để máy/model rẻ chuẩn bị ứng viên, còn Claude quyết định ở các điểm thật sự cần hiểu nội dung**.
- Bất cứ thay đổi nào cũng phải giữ được khả năng truy vết lỗi và rollback.

Mục tiêu cuối cùng là biến Bước 1 thành một pipeline có:

1. Một luồng chính thống duy nhất.
2. Các cổng QC rõ ràng.
3. Không có vòng lặp vô hạn.
4. Có cơ chế escalation khi tự sửa không hội tụ.
5. Có manifest đánh dấu trạng thái READY.
6. Có QC cho transcript, prompt ảnh, mapping ảnh và asset.
7. Có handoff sạch cho bước render/compositor.

---

# 1. NGUYÊN TẮC KIẾN TRÚC BẮT BUỘC GIỮ

## 1.1. Bước 1 là "đầu não"

Mọi thứ cần hiểu nội dung phải được hoàn tất trong Bước 1:

- chọn chủ đề;
- đọc transcript đối thủ;
- viết kịch bản;
- thiết kế nhân vật;
- viết prompt ảnh;
- phân loại AI/STOCK;
- gán ảnh vào đúng đoạn;
- chọn chữ thumbnail;
- viết title/description/chapter/hashtag;
- quyết định sửa lỗi semantic.

Bước 2 và Bước 3 chỉ được nhận đầu vào đã chuẩn hoá và làm việc cơ học.

### TUYỆT ĐỐI KHÔNG:
- để bước 3 tự viết metadata;
- để compositor tự đoán ảnh thuộc đoạn nào;
- chia đều ảnh theo số đoạn;
- tự trích frame stock để "bù cho đủ ảnh";
- tự suy luận lại nội dung đã được Bước 1 quyết định.

---

# 2. HỢP NHẤT HAI BIẾN THỂ PIPELINE A/B

Hiện tại đang tồn tại:

- A: Claude interactive chạy từng bước.
- B: `brain_channel.py` chạy headless.

Không xoá A, nhưng phải đổi vai trò.

## Thiết kế mới

```text
NORMAL FLOW
brain_channel.py
    ↓
automatic gates
    ↓
PASS
    ↓
continue pipeline

FAIL
    ↓
auto-fix tối đa N lần
    ↓
vẫn FAIL
    ↓
ESCALATION
    ↓
Claude interactive / human review
```

### Quy tắc:

- **Biến thể B = pipeline chính.**
- **Biến thể A = escalation/debug mode.**
- Không coi A/B là hai pipeline ngang hàng nữa.
- Mọi logic dùng chung phải nằm trong module chung, không copy code riêng cho A/B.

### Yêu cầu triển khai:

Tìm các đoạn logic trùng giữa:
- `brain_channel.py`
- `brain_steps.py`
- runbook interactive
- QC scripts

Tách thành các hàm/module dùng chung nếu an toàn.

Không refactor lớn nếu chưa có regression test.

---

# 3. THÊM B1Q — TOPIC SELECTION SCORE

B1 hiện chỉ dựa mạnh vào view + độ mới rồi Claude chọn.

Cần bổ sung scoring cơ học trước khi đưa ứng viên cho Claude.

## Mục tiêu

Thay vì Claude phải đọc danh sách lớn:

```text
500 video
→ scoring
→ top 30
→ shortlist 10
→ Claude chọn 1-3
```

## Có thể dùng các feature:

- `views`
- `age_days`
- `views_per_day`
- hiệu suất tương đối so với median của chính kênh;
- title pattern;
- chủ đề đã làm hay chưa;
- độ trùng với episode trước;
- khả năng Nhật hoá;
- khả năng kể thành video dài;
- mức phù hợp với lane người già.

## Không cần ML phức tạp ở giai đoạn đầu.

Có thể tạo:

```text
topic_score =
  velocity_score
+ relative_performance
+ recency_score
+ lane_fit
+ repeatability
- duplicate_penalty
```

Lưu breakdown score để Claude biết vì sao video được shortlist.

## Output đề xuất

`topic_candidates.json`

Ví dụ:

```json
[
  {
    "video_id": "...",
    "title": "...",
    "views": 1200000,
    "age_days": 42,
    "views_per_day": 28571,
    "relative_channel_score": 2.8,
    "duplicate_penalty": 0.2,
    "final_score": 8.4,
    "reasons": [
      "high relative performance",
      "recent",
      "topic chưa dùng"
    ]
  }
]
```

---

# 4. THÊM B2Q — TRANSCRIPT INTEGRITY QC

Đây là gate mới bắt buộc.

Hiện transcript có fallback:
1. YouTube timedtext
2. yt-dlp auto subtitle
3. Whisper

Nhưng cần kiểm transcript có đầy đủ thật không.

## Input

- video duration;
- transcript/timestamp;
- `competitor.txt`;
- nguồn transcript đã dùng.

## Kiểm tra cơ học

### 4.1 Coverage

```text
coverage = transcript_last_timestamp / video_duration
```

Mục tiêu đề xuất:

```text
coverage >= 0.92
```

Không dùng ngưỡng cứng tuyệt đối nếu transcript nguồn không có timestamp; trong trường hợp đó phải dùng fallback metric khác.

### 4.2 Large gap

Phát hiện các khoảng không có transcript bất thường.

Ví dụ:

```text
max_gap > 30s → WARN/FAIL
```

Nên bỏ qua intro/outro nếu có lý do hợp lệ.

### 4.3 Duplicate block

Phát hiện subtitle/transcript bị lặp block dài.

### 4.4 Density

Kiểm ký tự/phút quá thấp bất thường.

### 4.5 Empty ending / abrupt cut

Nếu transcript kết thúc quá sớm so với video → FAIL.

## Output

`qc_transcript.json`

Ví dụ:

```json
{
  "status": "PASS",
  "source": "yt-dlp",
  "video_duration": 1832.4,
  "last_timestamp": 1815.0,
  "coverage": 0.9905,
  "max_gap_sec": 12.1,
  "duplicate_ratio": 0.01,
  "warnings": []
}
```

Nếu FAIL:
- thử source fallback tiếp theo;
- chỉ đưa cho Claude nếu mọi source đều không đạt.

---

# 5. GIỮ B3Q NHƯ CỔNG QUAN TRỌNG NHẤT

Không được bỏ hoặc đơn giản hoá B3Q.

B3Q hiện có:
- machine QC;
- Gemini semantic QC;
- Claude Opus independent QC.

Đây là thiết kế tốt.

## Giữ nguyên nguyên tắc:

```text
SCRIPT
→ machine QC
→ cheap semantic QC
→ independent high-quality QC
→ PASS
```

## Quy tắc sửa:

- sửa đúng lỗi;
- không rewrite toàn bộ script nếu không cần;
- sau khi sửa phải chạy lại toàn bộ gate liên quan;
- nếu cùng một lỗi FAIL >= 3 lần:
  - DỪNG AUTO-RETRY;
  - tạo báo cáo escalation;
  - chuyển interactive review.

## Cần chuẩn hoá rule này thành helper dùng chung

Ví dụ:

```python
MAX_AUTO_RETRIES = 2
ESCALATE_ON_ATTEMPT = 3
```

Không hardcode mỗi script một kiểu.

---

# 6. THÊM B5P — PROMPT CONSISTENCY QC

Đây là thay đổi ưu tiên cao nhất.

Hiện có thể xảy ra:
- script nói chồng đã chết nhưng prompt sau vẫn có chồng;
- tuổi nhân vật sai;
- quần áo thay đổi vô lý;
- nhà ở khác bối cảnh;
- vật chứng xuất hiện trước khi cốt truyện giới thiệu;
- thời gian/ngày/đêm sai;
- quan hệ nhân vật sai.

## Input

- `script.txt`
- `characters.json`
- `img_prompts.txt`

## Mục tiêu

Kiểm **prompt ảnh có phù hợp với toàn bộ state của câu chuyện**, không chỉ đoạn hiện tại.

## Cách làm đề xuất

### Bước 1 — tạo Story Facts

Từ script, sinh một cấu trúc facts.

Ví dụ:

```json
{
  "characters": {
    "A": {
      "age": 72,
      "relationship": "widow",
      "husband_status": "deceased"
    }
  },
  "timeline": [
    {
      "segment": 1,
      "location": "home",
      "time": "morning",
      "facts": ["husband already deceased"]
    }
  ]
}
```

Có thể tạo cùng lúc B3 hoặc cache lại sau B3Q.

### Bước 2 — kiểm từng prompt

Mỗi prompt cần trả:

```json
{
  "prompt_id": 87,
  "status": "PASS",
  "conflicts": []
}
```

Hoặc:

```json
{
  "prompt_id": 87,
  "status": "FAIL",
  "conflicts": [
    {
      "type": "character_state",
      "detail": "prompt depicts deceased husband alive in current timeline"
    }
  ]
}
```

## Kiểm các nhóm sau

- character identity;
- tuổi;
- giới;
- quan hệ;
- tình trạng sống/chết;
- quần áo;
- location;
- time of day;
- season;
- chronology;
- object state;
- money/document/event facts;
- số người trong cảnh.

## Quan trọng

Không tự sửa prompt bằng regex nếu lỗi là semantic.

Có thể:
1. model rẻ phát hiện;
2. Claude sửa prompt cụ thể bị lỗi.

---

# 7. TỐI ƯU B5Q — QC ASSET ẢNH

Không chỉ sample 20 ảnh trong tổng hàng trăm ảnh.

Chia thành 3 tầng:

## Tầng A — 100% mechanical

Chạy với mọi ảnh:

- file tồn tại;
- decode được;
- kích thước;
- aspect ratio;
- file size;
- ảnh đen/trắng bất thường;
- pHash/dHash để tìm duplicate;
- near duplicate;
- alpha lỗi nếu có;
- tên file liên tục.

Không cần LLM.

## Tầng B — vision sample rộng hơn

Ví dụ:
- 20–30% ảnh;
- hoặc tối thiểu 60 ảnh;
- hoặc adaptive sampling theo risk.

Kiểm:
- hỏng hình;
- nhân vật sai;
- lỗi tay/mặt nghiêm trọng;
- cảnh vô lý;
- chữ rác lớn;
- style lệch.

## Tầng C — suspicious-only high-quality review

Các ảnh:
- similarity bất thường;
- confidence thấp;
- liên quan nhân vật chính;
- cảnh cao trào;
- cảnh có nhiều nhân vật;
- ảnh model rẻ flag.

→ mới gửi model tốt hơn.

### Mục tiêu

Không cần dùng model đắt kiểm 300/300 ảnh, nhưng cũng không được kiểm chỉ ~6-7%.

---

# 8. B5.5 — SEMANTIC-ASSISTED IMAGE MAPPING

Đây là bước rất tốn Claude nhưng KHÔNG được quay lại cách chia đều.

## Tuyệt đối cấm

```text
ảnh 1-3 → đoạn 1
ảnh 4-6 → đoạn 2
...
```

hoặc bất kỳ công thức chia đều nào.

## Thiết kế mới

Máy chỉ **gợi ý ứng viên**.

Claude vẫn là người quyết định semantic cuối.

### Pipeline:

```text
script paragraph
    ↓
embedding/search
    ↓
top-K matching image prompts
    ↓
Claude chọn mapping cuối
```

## Có thể làm theo batch

Ví dụ mỗi đoạn:

```json
{
  "paragraph": 14,
  "candidate_prompts": [
    {"prompt_id": 81, "score": 0.89},
    {"prompt_id": 82, "score": 0.84},
    {"prompt_id": 80, "score": 0.76}
  ]
}
```

Claude chỉ cần:
- xác nhận;
- đổi thứ tự;
- loại candidate sai;
- giữ monotonic order.

## Các constraint bắt buộc

- mapping không giảm theo timeline;
- mọi prompt phải được dùng đúng ý đồ;
- không map ảnh trước khi sự kiện xảy ra;
- không để một đoạn quá nhiều ảnh nếu không đủ câu neo;
- `sinh_neo.py` vẫn là gate cơ học sau mapping.

## Thêm QC mapping

Sau khi tạo `img_doan.txt`, thêm semantic audit:

Sample hoặc toàn bộ mapping bằng model rẻ:

```text
image prompt
vs
mapped paragraph
```

Score 1–5.

Các score thấp mới gửi Claude xem.

---

# 9. HYBRID STOCK — THÊM SEMANTIC STOCK QC + PROVENANCE

Hiện audit stock không chỉ cần kiểm:
- mặt người;
- logo;
- chữ.

Phải kiểm clip có **đúng nội dung cần minh hoạ**.

## audit_stock mới nên có 3 lớp

### 9.1 Technical
- decode;
- duration;
- resolution;
- corrupt.

### 9.2 Safety/visual cleanliness
- mặt người rõ nếu lane không muốn;
- logo;
- watermark;
- chữ lớn.

### 9.3 Semantic relevance
So:
- yêu cầu từ prompt;
- frame đại diện của clip.

Trả:

```json
{
  "semantic_score": 4,
  "status": "PASS",
  "reason": "matches elderly woman entering a bank-like interior"
}
```

Ngưỡng thấp → `AI_FALLBACK`.

## Lưu provenance

Mỗi asset stock cần metadata:

```json
{
  "provider": "pexels",
  "asset_id": "...",
  "source_url": "...",
  "creator": "...",
  "license": "...",
  "downloaded_at": "...",
  "query": "...",
  "prompt_id": 91
}
```

Lưu thành:

`stock_manifest.json`

Điều này phục vụ audit bản quyền sau này.

---

# 10. CHUẨN HOÁ RETRY / ESCALATION CHO TOÀN BỘ PIPELINE

Không được có logic kiểu:

```text
retry until PASS
```

## Mẫu chuẩn

```text
Attempt 1
    ↓ FAIL
auto-fix
    ↓
Attempt 2
    ↓ FAIL
auto-fix
    ↓
Attempt 3
    ↓ FAIL
ESCALATE
```

Tuỳ gate có thể dùng 2 hoặc 3 retry, nhưng phải hữu hạn.

## Khi escalation

Tạo file:

`ESCALATION_REPORT.md`

Nội dung:

- step;
- gate;
- input;
- attempts;
- lỗi từng lần;
- thay đổi đã thử;
- output hiện tại;
- đề xuất Claude interactive xem gì.

### Không được:

- retry 10-20 lần;
- burn quota;
- thay đổi ngẫu nhiên prompt cho tới khi model nói PASS.

---

# 11. THUMBNAIL QC — SỬA LOGIC "CHẠY TỚI KHI PASS"

Giữ hai lớp QC hiện tại:
- Gemini layer;
- GPT-5.6-sol independent layer.

Nhưng đổi retry logic.

## Trạng thái chuẩn

### PASS
Kết thúc.

### FIX
Sửa đúng lỗi được nêu.

Cho phép tối đa 2 vòng tự sửa.

### REMAKE
Tạo concept mới hoặc background mới.

Cho phép tối đa 2 remake.

### Sau giới hạn
Escalate.

## Nên lưu lịch sử

`thumbnail_qc_history.json`

Ví dụ:

```json
[
  {
    "attempt": 1,
    "result": "FIX",
    "issues": ["text too dense"]
  },
  {
    "attempt": 2,
    "result": "PASS"
  }
]
```

---

# 12. METADATA PHẢI LÀ REQUIRED ARTIFACT

Giữ nguyên yêu cầu:

`TIEU_DE_MO_TA.txt` là bắt buộc.

Pipeline không được READY nếu thiếu.

Nên validate thêm:

- title không rỗng;
- description không rỗng;
- chapter đủ số;
- hashtag có;
- không còn placeholder nếu đã có audio;
- chapter timestamp monotonic;
- timestamp không vượt duration.

---

# 13. FINAL VIDEO QC — ĐỔI B9 THÀNH FINAL SMOKE TEST

Claude xem 4 frame không đủ để gọi là full QC.

Đổi tên chức năng:

```text
B9 = FINAL SMOKE TEST
```

## Full video QC nên nằm ở B8Q

B8Q có thể sample:

- mỗi 10% timeline;
- scene boundary;
- random frames;
- frame quanh anchor;
- cảnh mở đầu;
- cao trào;
- kết.

Ví dụ 20–30 frame/video.

## B9 chỉ cần xác nhận:

- video mở được;
- frame đầu;
- frame giữa;
- frame cuối;
- subtitle burn-in;
- không lỗi layout rõ ràng;
- không black frame cuối.

---

# 14. THÊM PIPELINE MANIFEST — SOURCE OF TRUTH

Đây là thay đổi kiến trúc quan trọng.

Không dùng việc "file nào tồn tại" làm trạng thái duy nhất.

Mỗi episode cần:

`pipeline_manifest.json`

Ví dụ:

```json
{
  "schema_version": 1,
  "pipeline_version": "2026.09.18",
  "episode_id": "...",
  "profile": "satori-jp-obaa",
  "source_video_id": "...",

  "artifacts": {
    "competitor": "competitor.txt",
    "script": "script.txt",
    "characters": "characters.json",
    "voice": "voice_paced.wav",
    "subtitle": "voice_paced.srt",
    "image_prompts": "img_prompts.txt",
    "image_mapping": "img_doan.txt",
    "anchors": "anchors.txt",
    "thumbnail": "thumbnail_final.png",
    "metadata": "TIEU_DE_MO_TA.txt"
  },

  "qc": {
    "topic": "PASS",
    "transcript": "PASS",
    "script": "PASS",
    "audio": "PASS",
    "prompt_consistency": "PASS",
    "character": "PASS",
    "images": "PASS",
    "mapping": "PASS",
    "thumbnail": "PASS",
    "metadata": "PASS"
  },

  "mode": "hybrid",
  "ready_for_render": true
}
```

## `ready_for_render = true` chỉ khi

TẤT CẢ required artifact tồn tại + tất cả required QC PASS.

Bước render chỉ đọc manifest.

Nếu false → refuse render và báo rõ gate nào chưa đạt.

---

# 15. CHUẨN HOÁ TRẠNG THÁI PIPELINE

Dùng enum rõ ràng:

```text
PENDING
RUNNING
PASS
WARN
FAIL
ESCALATED
SKIPPED
```

Không dùng các chuỗi tuỳ ý ở từng script.

Mỗi gate nên output chung format:

```json
{
  "gate": "B5P",
  "status": "PASS",
  "attempt": 1,
  "blocking_issues": [],
  "warnings": [],
  "metrics": {},
  "timestamp": "..."
}
```

---

# 16. LOGGING VÀ DEBUG

Mỗi episode nên có:

```text
logs/
  B1_topic.json
  B2_transcript.json
  B3_script_qc.json
  B4_audio_qc.json
  B5_prompt_qc.json
  B5_asset_qc.json
  B55_mapping_qc.json
  B7_thumbnail_qc.json
```

Không overwrite lịch sử vô điều kiện.

Nếu rerun:

```text
attempt_001
attempt_002
attempt_003
```

hoặc lưu history array.

---

# 17. CẤU HÌNH MODEL KHÔNG HARDCODE KHẮP NƠI

Tạo config tập trung.

Ví dụ:

```yaml
models:
  script_writer: claude-opus
  script_qc_fast: gemini-3.8-flash
  script_qc_independent: claude-opus
  stock_classifier: deepseek-v4-flash
  thumbnail_qc: gpt-5.6-sol
```

Nếu provider fail:
- fallback theo config;
- ghi log model thực tế đã dùng;
- không silent fallback.

---

# 18. KHÔNG ĐỂ GEMINI THÀNH SINGLE POINT OF FAILURE

Gemini hiện đang gánh quá nhiều QC.

Không nhất thiết thay model ngay.

Trước mắt:

1. Tách gate thành interface chung.
2. Cho phép provider/model thay qua config.
3. Có fallback.
4. Với gate quan trọng, giữ independent judge khác family.

### Gate quan trọng nên independent:
- script;
- thumbnail;
- có thể prompt consistency.

Không cần 2 model cho mọi thứ.

---

# 19. PHÂN TÁCH "DETECTION" VÀ "DECISION"

Đây là nguyên tắc để giảm chi phí Claude.

## Model/thuật toán rẻ:
- detect;
- rank;
- shortlist;
- flag;
- tính metric;
- tạo candidate.

## Claude:
- quyết định semantic khó;
- sửa lỗi;
- resolve conflict;
- chọn giữa candidate khó;
- escalation.

Ví dụ B5.5:

```text
embedding tìm top-3
≠
embedding tự quyết mapping
```

Máy chỉ đề xuất.

Claude quyết định.

---

# 20. THỨ TỰ TRIỂN KHAI — KHÔNG LÀM TẤT CẢ CÙNG LÚC

Làm theo thứ tự:

## P0 — bắt buộc trước
1. Retry/escalation framework.
2. B2Q transcript integrity.
3. B5P prompt consistency.
4. Pipeline manifest.
5. Hợp nhất A/B về một core flow.

## P1 — hiệu suất/chất lượng
6. Semantic-assisted img_doan.
7. Asset QC nhiều tầng.
8. Hybrid semantic stock QC.
9. Thumbnail retry history.
10. Metadata validator.

## P2 — tối ưu thêm
11. Topic scoring.
12. Model config/fallback chuẩn.
13. Expanded final video sampling.
14. Dashboard/report nếu cần.

Không refactor hàng loạt P0/P1/P2 trong một commit.

---

# 21. REGRESSION TEST BẮT BUỘC

Trước khi thay logic production:

Chọn ít nhất:

- 1 tập non-hybrid đã PASS;
- 1 tập hybrid đã PASS;
- 1 tập từng có lỗi img_doan;
- 1 tập từng có lỗi script;
- 1 tập từng có lỗi thumbnail.

## Mỗi thay đổi phải test:

```text
old artifact
vs
new pipeline output
```

Không cần output giống byte-for-byte.

Nhưng phải đảm bảo:
- không mất file;
- không sai mapping;
- không bỏ QC;
- không tăng FAIL giả quá mức;
- không tự tiêu quota vô hạn.

---

# 22. CÁC RÀO CỨNG KHÔNG ĐƯỢC PHÁ

1. Không chi tiền TTS/ảnh trước khi script QC PASS.
2. Không chia đều `img_doan`.
3. Không để bước 3 tự hiểu truyện.
4. Không trích frame stock để giả thành ảnh AI còn thiếu.
5. Không bỏ `TIEU_DE_MO_TA.txt`.
6. Không auto-retry vô hạn.
7. Không dùng một model tự viết rồi tự QC duy nhất cho gate quan trọng.
8. Không xoá incident fixes cũ nếu chưa chứng minh thay thế an toàn.
9. Không silent fallback provider/model.
10. Không set `ready_for_render=true` nếu thiếu artifact hoặc QC bắt buộc.

---

# 23. DEFINITION OF DONE

Chỉ coi đợt tối ưu hoàn thành khi:

### Kiến trúc
- [ ] B là normal flow.
- [ ] A là escalation mode.
- [ ] Có core logic dùng chung.

### QC
- [ ] Có transcript QC.
- [ ] Có prompt consistency QC.
- [ ] Có mapping QC.
- [ ] Asset QC không còn chỉ phụ thuộc sample 20 ảnh.
- [ ] Hybrid có semantic stock QC.

### Control
- [ ] Mọi retry đều hữu hạn.
- [ ] Có escalation report.
- [ ] Có lịch sử attempt.

### Handoff
- [ ] Có `pipeline_manifest.json`.
- [ ] Render chỉ chạy khi `ready_for_render=true`.
- [ ] Metadata là required artifact.

### Regression
- [ ] Test ít nhất 5 episode đại diện.
- [ ] Không phá hybrid.
- [ ] Không phá non-hybrid.
- [ ] Không làm mất các rào cứng hiện tại.

---

# 24. YÊU CẦU CLAUDE TRƯỚC KHI SỬA CODE

Claude KHÔNG được bắt đầu sửa ngay.

Trước tiên phải:

1. Đọc tài liệu quy trình gốc.
2. Đọc các file code liên quan.
3. Vẽ lại dependency thực tế.
4. Đối chiếu tài liệu với code.
5. Chỉ ra phần nào tài liệu khác code đang chạy.
6. Lập danh sách file dự kiến sửa.
7. Xác định regression risk.
8. Sau đó mới sửa theo P0 → P1 → P2.

Nếu phát hiện tài liệu và code mâu thuẫn:

**CODE ĐANG CHẠY + bằng chứng production là nguồn sự thật cần kiểm tra trước; không tự động tin tài liệu hoặc tự động sửa theo tài liệu.**

---

# 25. FORMAT BÁO CÁO CLAUDE PHẢI TRẢ TRƯỚC KHI IMPLEMENT

Claude phải trả:

```text
A. CURRENT STATE
- pipeline thực tế đang chạy
- module/file liên quan
- khác biệt với tài liệu

B. PROBLEMS FOUND
- lỗi kiến trúc
- duplication
- missing gate
- risk

C. PROPOSED CHANGES
- P0
- P1
- P2

D. FILES TO MODIFY
- file
- lý do
- mức risk

E. MIGRATION PLAN
- làm theo thứ tự nào
- cách giữ backward compatibility

F. REGRESSION PLAN
- episode nào
- test gì
- pass criteria

G. QUESTIONS / BLOCKERS
- chỉ ghi những blocker thực sự không thể suy ra từ code
```

Sau khi báo cáo này được duyệt mới bắt đầu thay đổi lớn.

---

# 26. TƯ TƯỞNG CUỐI CÙNG

Không tối ưu bằng cách biến Claude thành không cần thiết.

Tối ưu bằng cách:

```text
MACHINE / CHEAP MODEL
    ↓
lọc + đo + shortlist + detect
    ↓
CLAUDE
    ↓
quyết định semantic quan trọng
```

Mục tiêu là:

**Claude đọc ít hơn nhưng đọc đúng chỗ hơn.**

Pipeline tốt không phải pipeline có ít model nhất.

Pipeline tốt là pipeline:
- biết bước nào cần trí tuệ cao;
- biết bước nào chỉ cần thuật toán;
- phát hiện lỗi sớm;
- retry hữu hạn;
- có bằng chứng QC;
- và không để lỗi semantic lọt xuống render.
