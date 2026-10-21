# SOP — LANE G: 定年後の楽しみ方 (hưu trí Nhật, MANGA STORY ngôi 1 + list N選 lối sống VUI/RẺ)

> Kênh mẫu: 老後のお金ストーリー `https://www.youtube.com/channel/UCI2cPqBmCPMxxKI4u2Gqs_Q`
> (5.260 sub · 16 video · median 34.612 view · kênh mới 61 ngày lúc nghiên cứu 2026-09-13).
> Kênh của mình: **定年後の楽しみ方** `@teinengo-tanoshimi` · `UClETn8eAXgRRKM4PkYEKzvA`
> (profile `teinengo-tanoshimi`, mail GMAIL dòng 8 `cobbytheona159@gmail.com`, NOTE dòng 4).
> Cửa vào: `docs/BAT_DAU_LANE/teinengo-tanoshimi.md` (đọc trước, file này là chi tiết vận hành).
> Lập 2026-09-20 (Giai đoạn 2). Khuôn chép từ `SOP_LANE_E.md`, sửa theo đặc thù manga story.

| Anh nói | Profile | SOP |
|---|---|---|
| "hưu trí Nhật · manga kịch tính tiền · Lane F" | `teinengo-real` | `BAT_DAU_LANE/teinengo-real.md` |
| "hưu trí Nhật · manga list N選 vui/rẻ · Lane G · 定年後の楽しみ方" | **`teinengo-tanoshimi`** | **file này** |
| "sức khoẻ người già · liệt kê bác sĩ · Lane E" | `kenko-chiebukuro` | `SOP_LANE_E.md` |

Nguồn nghiên cứu (2 nguồn, bổ nhau):
```
FlowHandoff_local/results/laneG_from_research/          ← TRENDING-RESEARCH, anh duyệt 2026-09-13
├── LANE_G_HANDOFF.md            14 mục: HIT/MISS §3 · title §4 · hook §5 · cấu trúc §6 · SEO §12 · tập 1 §13 · rủi ro §14
├── channel_analysis_老後のお金ストーリー.json
└── data/transcripts_okane.json  3 transcript CÓ TIMESTAMP (153k / 42k / 986v)
docs/channel_dna/rougo-money-story/                     ← Channel Analyzer K1+K2, 8 video top, QC DNA 11/11 (copy 2026-09-20)
├── CHANNEL_DNA.md               audience / 4 trụ cột / 3 công thức hook / 5 hồi / 7 quy tắc viết
├── VIDEO_ANALYSIS/*.json        8 file — đầu vào cho K3 retrieve_videos.py
├── TAG_STATS.json
└── _raw/transcripts.json        8 transcript thật (KHÔNG timestamp) — dùng đo gate
```

---

## 0. BẢNG DELTA — khác Lane E/F chỗ nào

| Khâu | Lane E (kenko) | Lane F (teinengo-real) | **Lane G (file này)** |
|---|---|---|---|
| Người kể | Bác sĩ ngôi 2, nói với khán giả | Manga ngôi 1, 2 nhân vật ĐỐI LẬP | **Manga ngôi 1「俺」, nam 60–67, + 1 MENTOR khai sáng** |
| Cảm xúc | lo → hiểu → yên tâm | lo âu → chấp nhận → bài học (tiền MẤT) | **tò mò → khao khát → đồng cảm → phấn chấn (sống VUI/RẺ)** |
| Cấu trúc | `list_countdown` 第5位→第1位, mỗi mục 1 người ẩn danh | 2 số phận + ngoặt | **`manga_list`** (nhánh mới `ai_steps._cau_truc_block`): 5 hồi, N選, mục cuối = cú lật hướng nội |
| Thoại「」 | ≤5% | nhiều | **≤40%** (ước từ 20–36% câu mang đuôi hội thoại ở 3 transcript) — `_pacing_block` tự đổi câu dặn khi ≥25% |
| Nhân vật lặp | KHÔNG (ref_lock=false) | 2 nhân vật REF-LOCK trong tập | **1 nhân vật chính REF-LOCK trong tập (@REF), mentor @REF2 nếu ≥5 cảnh; KHÔNG xuyên tập** |
| Giọng | Dependable Woman (kho) | chưa | **CLONE RIÊNG từ kênh mẫu `clone_2658912`, 323,7 chữ/phút** (§0c, anh duyệt 2026-09-20) |
| Thời lượng | 20' | — | **20'** (kênh mẫu 18,5–28', median ~22') |
| Rủi ro nội dung | y khoa | số chế độ 年金 | **Địa điểm/giá/thông tin Nhật phải có nguồn** (series_ctx.txt); claim "若返る" không được thành y khoa tuyệt đối |
| Ken Burns | tắt (zoom 1.0) | — | **tắt** (khán giả 60+) |

## 0b. CHANNEL ANALYZER — ĐÃ CHẠY 8 VIDEO (K1+K2), K3 chạy mỗi tập

K1+K2 chạy 2026-09-16 tại máy 1 → `FlowHandoff_local/results/channel_dna/rougo-money-story/` (96s,
QC DNA 10.254 ký tự 11/11 ĐẠT) → copy sang `docs/channel_dna/rougo-money-story/` 2026-09-20.
8 video = top view (40k–176k), kênh có 16 video → **còn 8 video chưa phân tích** (đều <40k, gồm cả 5
MISS) — đủ cho pattern THẮNG, không cần chạy thêm trừ khi muốn học thêm pattern THUA.

Mỗi tập (Giai đoạn 3 bước 2) chọn `competitor.txt` bằng K3:
```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 -X utf8 retrieve_videos.py --dna-dir ..\docs\channel_dna\rougo-money-story --topic "<đề tài tập, tiếng Nhật>" --top 3
```
Ưu tiên transcript **cùng dạng đếm** với tập mình (1つ目 cho thói quen / 第5位 cho xếp hạng) — xem §3.
Transcript thô ở `_raw/transcripts.json` (8 video, không timestamp) hoặc `data/transcripts_okane.json`
(3 video có timestamp — dùng khi cần mốc giây).

## 0c. GIỌNG — K4 vân tay + CLONE RIÊNG (2026-09-20)

**K4** (`voice_fingerprint.py --ids bgUqNHYZbq0,BeIZhu1I4Tw,AOe-E69mLzA,0DinnkWTJmg --start-s 60 --dur-s 50`):
F0 = 117,6 / 105,3 / 116,8 / 114,3 Hz (nam thấp), cosine MFCC thấp nhất 0,941 → **CÙNG 1 GIỌNG NAM
trên cả 4 video** → clone 1 lần dùng chung cho lane (khác Lane E có ≥2 giọng).

**Clone** (anh chốt 2026-09-20: clone RIÊNG, không dùng chung voice_id Lane F):
- Mẫu: video 176k `bgUqNHYZbq0`, đoạn **0:52,7–1:20** (27s, đoạn tự giới thiệu「俺は石川県…」, không
  có `[音楽]` trong transcript), `remove_background=true`.
- `POST /v3/text-to-speech/voice-clone` → **`voice_id = 2658912`** → dùng `clone_2658912`.
- Test 145 chữ speed 1.0 → 27,4s; **F0 output 116,8 Hz KHỚP nguồn** (105–118) → đúng giới NAM
  (xác minh bằng số đo theo skill §6b, không theo cảm nhận). Chi phí clone + test: **481 credit**.
- Trang nghe A/B: `scratchpad/voiceG/compare.html` (`http://127.0.0.1:8766/compare.html`).
- ✅ **ANH DUYỆT 2026-09-20** → `voice.id="clone_2658912"` đã ghi profile. Anh chốt thêm: video gốc nào
  giọng NỮ thì tính sau (hiện 4/4 video đo đều nam).

## 0d. CHAR-RATE — ĐÃ ĐO 2026-09-20: **323,7 chữ/phút** (230 chữ story → 42,6s) → 20' = **6.474 chữ**

```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 -X utf8 calibrate.py --profile teinengo-tanoshimi
```
`calib_style=story`. Số thô từ test clone: 145 chữ / 27,4s ≈ 318 chữ/phút (câu ngắn, có thoại) — chỉ
tham khảo, **calibrate.py mới là số ghi vào profile**. Kênh mẫu đo thô 312–362 chữ/phút (tính cả nhạc).
Hàng rào #1: `rate_measured()` false → `make_video.py` DỪNG, không mượn số lane khác.

## 1. QUYẾT ĐỊNH ĐÃ CHỐT (2026-09-20)

- `body.mode="ai_images"`, manga tươi sáng (`image.style_suffix`), **`ref_lock=true`** cho nhân vật
  chính của TẬP (không xuyên tập — kênh mẫu rời rạc, mỗi video 1 người kể khác).
- `script.structure="manga_list"` (nhánh MỚI, field-driven: `gate.list_item_count` 5/7, `gate.list_order`
  auto/ascending/countdown, `script.outro_line`). **Không đụng nhánh `list_countdown` của Lane E.**
- `script.engine="claude_p"` (Claude viết PASS 0/1, Gemini nén + chấm B3Q/B3F), `sol_qc=true` (B3S).
- `script.mode="story"` (hư cấu nhân vật, `_chong_trung_block` bắt đổi tên/nghề/vùng) NHƯNG mọi địa
  điểm/giá/thông tin Nhật CHỈ lấy từ `series_ctx.txt` (`ctx_label` nói rõ) — hard rule handoff §3.3.
- Outro nguyên văn kênh mẫu「ご視聴いただきありがとうございました。いいねとコメントもお待ちしています。」
  (8/8 video — câu chào chung, không phải câu biểu tượng) + **CTA comment giữa video** ở 45–55%.
- Không Ken Burns (`assemble.zoom=1.0`), như Lane E.

## 1b. DANH SÁCH 10 TẬP ĐẦU + CỘT SHEET TAB `teinengo-tanoshimi`

### Cột A→K (header thật đã tạo 2026-09-20, giống Lane E §1b)
| Cột | Field | Cách ghi |
|---|---|---|
| A | STT | = số ep. Thư mục `assets/teinengo-tanoshimi/ep<NN>-<slug>` khớp số này. |
| B | NỘI DUNG | Tiêu đề làm việc tiếng Nhật (đúng title formula §4 handoff). |
| C | FOLDER | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep<NN>-<slug>\` — chỉ điền khi thư mục đã tồn tại. |
| D | KỊCH BẢN | **`Done`** (anh chốt 20/09: chỉ 1 chữ, không sha/số đo — chi tiết đã ở `bench.jsonl`+`script.lock.json`) = 3 lớp tự duyệt đạt (máy S3 · Sol lens plain PASS · Claude Code đọc bản LOCK) — KHÔNG ghi "chờ anh duyệt" (memory `tu-duyet-khong-day-len-anh`). `escalate` = kèm lý do 1 câu ở K + ESCALATION_REPORT. Khi mở rộng phạm vi: `done` = thêm B4 giọng + B4Q + B5W/B5P + master REF-LOCK. |
| E/F/G | TITLE-DESCRIPTION / TAGS / THUMBNAIL | Bước 1 PHẢI để lại `TIEU_DE_MO_TA.txt` + `thumb_text.txt` trong thư mục tập (luật ⛔ CLAUDE.md); ô sheet ghi theo lệnh anh. F KHÔNG dùng làm marker. |
| H | STATUS-IMG | 1 ô 2 dòng: `Xong nội dung - cần ảnh` ⏎ `E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs\<slug>\` (KHÔNG `h2dev\`). Chỉ ghi khi anh bảo giao. |
| I | VIDEO | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-tanoshimi\ep<NN>-<slug>\` — khi B11 xong thật. |
| J | LIST | tuỳ anh. |
| K | GHI CHÚ | trạng thái từng cổng, cảnh báo. |

### 10 tập (✅ anh duyệt 2026-09-20, đã ghi tab `teinengo-tanoshimi` A2:B11 + K ghi trụ cột/slug)
Nguyên tắc: mỗi tập = 1 list 5選 CỤ THỂ (hành động/địa điểm + lợi ích), dàn đều 5 trụ cột, né 7 đề
tài kênh mẫu đã đốt (老けない7選 · 神社5選 · 夜行バス · 温泉地5選 · 生き方5選 · 疲労回復7選 · 暇つぶし5選),
CẤM trừu tượng (年金受給/人生/育ち). Title 36–43 ký tự (gate 33–50).

| STT | Trụ cột | Tiêu đề làm việc | Slug | Đếm | Ghi chú tư liệu |
|---|---|---|---|---|---|
| 1 | Trẻ khoẻ | 【漫画】60代から始める「朝の習慣」5選…1年後、体と気持ちが驚くほど軽くなる理由 | `ep01-asa-shukan` | 1つ目 | Handoff §13 đề xuất. Thói quen phổ thông, tư liệu nhẹ. |
| 2 | Thú vui rẻ | 【漫画】定年後、月1000円以下で夢中になれる趣味5選…暇な毎日が待ち遠しくなった | `ep02-1000yen-shumi` | 第5位 | Giá thật từng thú vui (nguồn). |
| 3 | Du lịch | 【漫画】定年後の一人旅は平日が最高…60代が歩くべき「静かな城下町」5選 | `ep03-jokamachi` | 第5位 | 5 thành cổ thật + phí vào cửa/ga gần — nguồn chính thức. |
| 4 | Phục hồi | 【漫画】60代から夜ぐっすり眠れるようになった「夕方の習慣」5選…薬に頼らず朝が変わる | `ep04-yugata-suimin` | 1つ目 | ⚠️ tránh claim y khoa tuyệt đối; thêm câu tham khảo bác sĩ nếu nhắc thuốc. |
| 5 | Sống vừa đủ | 【漫画】定年後の夫婦が「ちょうどいい距離」を保つ暮らし方5選…毎日が静かに楽しくなる | `ep05-fufu-kyori` | 1つ目 | Trụ cột #1 DNA (khoảng cách vừa phải). |
| 6 | Thú vui 0円 + Du lịch | 【漫画】60代から一度は歩きたい「無料の絶景散歩道」5選…1円も使わず体が若返る | `ep06-muryo-sanpo` | 第5位 | 5 đường đi bộ thật miễn phí (nguồn). |
| 7 | Sống vừa đủ/rẻ | 【漫画】定年後の食費が楽しみに変わる「台所の習慣」5選…節約なのに毎日が待ち遠しい | `ep07-daidokoro` | 1つ目 | Số tiền ví dụ = CÁ NHÂN (được đổi), không dùng thống kê giả. |
| 8 | Trẻ khoẻ | 【漫画】60代の体が軽くなる「歩き方」5つのコツ…毎日の散歩が一番の薬になった | `ep08-arukikata` | 1つ目 | ⚠️「薬」là ẩn dụ — không claim chữa bệnh. |
| 9 | Thú vui 0円 | 【漫画】定年後に人生が変わった「図書館の使い方」5選…実は0円で一番贅沢な場所 | `ep09-toshokan` | 第5位 | Dịch vụ thư viện công thật (nguồn: trang thư viện). |
| 10 | Du lịch 温泉 | 【漫画】60代の一人旅で行くべき「日帰り温泉のある小さな町」5選…平日ならほぼ独り占め | `ep10-higaeri-onsen` | 第5位 | Góc 日帰り/小さな町 khác 温泉地5選 kênh mẫu; giá vé 日帰り thật. |

- STT = ưu tiên DỰ KIẾN, đổi ở sheet không đổi file này. **CHỈ tập anh chỉ định mới bắt đầu** (memory
  `chi-chay-dong-duoc-chi-dinh`).
- Cột "Đếm": thói quen → 1つ目→5つ目; xếp hạng địa điểm/đồ vật → 第5位→第1位 (đúng cách kênh mẫu). Profile
  để `list_order="auto"` (prompt tự chọn theo đề tài); muốn ép thì đổi field trước khi chạy tập.

## 1c. PHẠM VI HIỆN TẠI — CHỈ TỚI KỊCH BẢN (anh chốt 2026-09-20)

> ⭐ **TỪ 20/09 15:30 lane này chạy `script.flow="lean"`** (`pipeline/lean_script.py`, thiết kế `docs/QUY_TRINH_KICH_BAN_GON.md` v2):
> Fable viết đúng ngân sách → máy đo (S3) → **Sol lens plain có sàn mức độ = lời cuối** → patch ≤2 (mỗi patch: máy + Sol lại)
> → PASS khoá sha256 `script.lock.json` | ESCALATE (`ESCALATION_REPORT.md`, pha asset BLOCK) | BLOCK. B3Q/B3F/B3S/B3R/B3G
> KHÔNG chạy nữa (state `skipped=lean_flow`). Bảng dưới đây mô tả luồng CŨ đã dùng cho ep01 lượt đầu — giữ để đối chiếu.
> Lệnh vẫn là `make_video.py --profile teinengo-tanoshimi --slug <ep> --den B3G`. File tập cần thêm: `title.txt` (tiêu đề làm việc,
> để Sol kiểm "lời hứa tiêu đề") + dòng `SỐ ĐƯỢC PHÉP:` đầu `series_ctx.txt` (máy đối chiếu số kanji/arabic).
> Sau LOCK: **không ai sửa script.txt** — cần sửa thì chạy lại B3 (lean) để Sol chấm lại; sửa tay = FINAL_QC_STALE, B5W dừng.

Giai đoạn đầu của lane này **chỉ làm phần kịch bản**: B2 hồ sơ đề tài → B3 viết → gate → B3Q → (B3F
bỏ qua vì `mode=story`) → B3S → **B3R (Fable nghiệm thu cuối)** → **DỪNG**. KHÔNG chạy: giọng (B4), prompt ảnh (B5W/B5P), REF-LOCK,
tiêu đề/mô tả/tags, thumbnail, sinh ảnh, video. Lệnh: thêm **`--den B3G`**. Cột D tạm ghi `script-qc`
(chưa phải `done` — `done` theo §1b nghĩa là đã có cả giọng + prompt ảnh). Mở rộng sang giọng/prompt
ảnh khi anh nói.

**Ai làm gì trong phần kịch bản (đúng luật "Claude chỉ làm bước 1 — đầu não"):**

| Việc | Ai/máy/model | Cách kiểm |
|---|---|---|
| Chọn tập, tạo thư mục, ghi cột C | Claude Code (tab này) | — |
| `competitor.txt` — chọn 1 transcript kênh mẫu cùng dạng đếm | Claude Code chạy K3 `retrieve_videos.py` (thuần Python, 0 LLM) rồi chọn tay | cùng dạng 1つ目/第5位 với tập |
| `series_ctx.txt` — tư liệu thật (địa điểm/giá/thông tin Nhật) CÓ URL | Claude Code tự tra WebSearch, ghi nguồn từng dòng | anh soi được URL |
| B3 PASS 0 bóc KHUNG (giấu bản gốc, chống sao chép) | `claude -p` headless, **Claude Fable 5.1** (`script.brain_model`, anh chốt 2026-09-20; `claude_p_bridge.py`, `--tools ""`) | khung chỉ có chức năng nhịp, không tên/số |
| B3 PASS 1 viết nháp dài (cấu trúc `manga_list` 5 hồi + luật nhịp tiếng Nhật) | `claude -p` **Fable 5.1** — A/B 2026-09-20 cùng prompt: Fable 1.380 chữ/neo 6,5 ✓ vs Opus 5 1.279 chữ/neo 4,7 ✗, cùng ~70s | ≥ target×1.3 chữ |
| B3 PASS 2 nén về 6.474 chữ + ép nhịp/hội thoại/phẩy (cơ học) | **gemini-3.8-flash** qua ramclouds (`llm_client` chain `script`, fallback gpt-5.6-luna/ns24) | `ai_steps.check` gate |
| Gate số (chữ · phẩy/câu · chữ/hơi · thoại% · marker · kết câu · `、` cắt cụm) | máy, `ai_steps.check` + `fix_gate.py` nắn tự động ≤2 lượt | ngưỡng = `profile.script.gate` (đo từ kênh mẫu) |
| B3Q QC nội dung: mâu thuẫn nhân vật/tuổi · 伏線 gieo↔trả · trùng ý · sót Hàn/Latin · mở đầu (`hook_marker`) · so nhịp 70/30 với bản gốc | tầng A máy (miễn phí) + tầng B **gemini-3.8-flash** (JSON schema cứng); tự sửa lỗi vừa, HỎNG thì dừng | `QcError` hạ tầng ≠ PASS (503 không được tính 0 lỗi) |
| B3F kiểm dữ kiện ↔ tư liệu | **BỎ QUA** (`mode=story`: `qc_facts` tất định sẽ báo mọi tên/tuổi hư cấu là "không có trong nguồn") | → thay bằng dòng dưới |
| **B3G (tay)** đối chiếu địa điểm/giá/thông tin Nhật trong script với `series_ctx.txt` | **Claude Code (tab này) đọc thẳng**, chỉ với tập có địa điểm/giá (3/6/9/10 nặng nhất) | mọi tên riêng/giá phải chỉ được dòng nguồn |
| B3S nghiệm thu HỢP LÝ/HỢP LỆ chung (anh chốt 20/09: KHÔNG y khoa) | **GPT-5.6-sol** `lens="plain"` — hỏi thẳng "kịch bản đã hợp lý chưa, chỗ nào không hợp lý liệt kê để sửa" (`script_qc` trong profile; ep01 lượt đầu chạy nhầm lens medical); FIX → **Fable** sửa tại chỗ 1 lần; REMAKE → dừng | Đo thật bản cuối ep01 với lens plain: FIX 7 điểm logic THẬT (mở đầu đá họp lớp · tiêu đề hứa "1 năm sau" nhưng kết ngay hôm sau · mục 2 gộp 2 thói quen · uống cả chai trái lời khuyên · 64 tuổi nghỉ hưu 1 năm lệch mốc 60/65 · gộp 3 thông tin ラジオ体操 thành tuyệt đối) — không một điểm y khoa ảo nào |
| **B3R nghiệm thu cuối** (mới 2026-09-20): biên tập viên Nhật đọc toàn bài theo 9 tiêu chí (5 hồi/N mục · 4 phần mỗi mục · CTA giữa · outro · địa điểm/giá phải có trong series_ctx · thoại tự nhiên · hướng VUI/RẺ · claim sức khoẻ · câu TTS gãy) → JSON PASS/FIX/REMAKE → `qc_final_review.txt` | **Fable 5.1** (`script.final_review_model`); FIX → Fable sửa tại chỗ 1 lần rồi chấm lại; REMAKE → dừng | test khô 2026-09-20: bản chỉ có Hồi 1+2 → REMAKE đúng, 7 issue, 67s. Cùng họ với model viết → KHÔNG thay B3S, chỉ là lớp cuối |
| Báo anh + đưa `qc_final_review.txt` | Claude Code (tab này) | anh duyệt |

Không có máy 2, không có Hermes/DeepSeek trong phần này — toàn bộ chạy trên máy 1 từ lệnh 1 dòng.
⚠️ `claude -p` PHẢI dùng CLI ≥2.1.251 (Fable): `claude_p_bridge.find_claude()` tự chọn binary MỚI NHẤT trên máy (hiện
bản native của extension VSCode 2.1.278; bản npm trên PATH 2.1.145 không có Fable và alias `opus` của nó là **Opus 4.7**). Ép
bản khác bằng env `CLAUDE_CLI`. Nên `claude update` bản npm khi tiện.
Chi phí ước 1 tập: `claude -p` Fable tiêu quota gói (không hoá đơn) · Gemini nén+QC ~vài nghìn đ ·
sol QC ~vài trăm đ. Thời gian ước 15–30 phút/tập (đo lại ở tập 1).

## 1d. TEST THẬT TẬP 1 (2026-09-20) — số đo + 6 lỗi pipeline đã vá ngay trong ngày

Chạy 2 lượt `make_video.py --den B3R/B3G`, tổng ~50 phút máy (lượt 2 thuần: 22,8 phút B2→B3R + ~8 phút B3G).

| Mốc | Model | Kết quả |
|---|---|---|
| PASS 0 bóc khung | Fable | 2.711 ký tự, 72s |
| PASS 1 nháp | Fable | 8.830 chữ, thoại 31%, 276s |
| PASS 2 nén | Gemini 3.8 Flash | 6.954 chữ, thoại 39%, gate ĐẠT ngay |
| B3Q | Gemini | SUA (3 lỗi vừa tự sửa: trùng ý mở đầu in-media-res) |
| B3S | GPT-5.6-sol → Fable FIX → sol | FIX → FIX (sol đòi cảnh báo y tế kiểu Lane E; Fable thêm 1.100 chữ) |
| B3R | Fable | FIX (4: outro sai 2 dấu 、 · thiếu câu hỏi dẫn giữa mục · 大場 lên lớp y tế · 「……」×5) → Fable sửa → PASS (3 nhẹ) |
| B3G (mới) | máy + Gemini nén/hạ thoại | 7.810 → nén 6.808 → hạ thoại 49%→29% → 6.755 chữ ĐẠT |
| Sửa tay (Claude Code) | — | 2 câu: dữ kiện 6000/8000歩 bị nén làm SAI · 「再会した」mâu thuẫn thời gian |
| **Bản cuối** | | **6.764 chữ ≈ 20,9' · phẩy/câu 1,15 · chữ/hơi 10,9 · thoại 29% · 5 mục 一つ目〜五つ目 · CTA @62% · outro nguyên văn** |

**6 lỗi pipeline dùng chung phơi ra và đã vá (đều field-driven, lane khác không đổi hành vi):**
1. `write_script` không gọi `go_cat_cum` → 1 dấu 、 làm vứt bản 7.005 chữ tốt và viết lại từ đầu → nay gỡ tất định ngay trong vòng (`_go_cat_neu_ja`).
2. `trim_chunked` phình → `LLMError` văng cả B3, MẤT bản nháp → nay bọc, giữ bản đang có; lưu `script_pass1_raw.txt`.
3. Prompt nén xoá thoại「」thành gián tiếp (26%→8%) → lane `dialogue_ratio_max ≥ 25%` cấm nén thoại.
4. Sau B3 KHÔNG còn cổng số: B3S/B3R FIX làm phình +21%, thoại 43% mà state PASS → thêm **B3G** (gỡ 、 · nén nếu DÀI · hạ thoại nếu vượt · dừng nếu còn lỗi) + `max_chars` 1,08× cho mọi lượt FIX qua `claude_p_bridge`.
5. `reduce_dialogue` prompt satori "chỉ giữ câu đắt" hạ 49%→13% (2 khúc còn 2–5%) → lane manga dùng `DIALOG_ASK_MANGA_JA` nhắm ~85% ngưỡng, giữ掛け合い → 29%.
6. Gemini nén làm SAI DỮ KIỆN (6.000/8.000歩 đảo nghĩa) mà B3Q/B3S/B3R đều lọt → **Claude Code vẫn phải đọc dòng số liệu đối chiếu series_ctx trước khi báo anh** (bước B3G-tay trong bảng §1c). Cân nhắc sau: cổng tất định "mọi số trong script phải có trong series_ctx" (mượn tầng A của `qc_facts.py`, bỏ tên nhân vật).

**Điểm còn treo về CHẤT (chưa sửa code):** Hồi 1+2 = 35% kịch bản (kênh mẫu 19–29%) — mo_dau báo `qua_dai`; ~~sol áp chuẩn y khoa~~ ĐÃ SỬA 20/09 → `script_qc.lens="plain"` (hỏi thẳng hợp lý/hợp lệ); bản cuối ep01 chấm lại bằng lens plain → **FIX 7 điểm logic thật** (`qc_sol_plain_ep01.txt`), lớn nhất: tiêu đề hứa「1年後」mà kịch bản kết ngay sáng hôm sau → cần thêm đoạn nhảy 1 năm, CHƯA sửa, chờ anh; 104 đoạn <40 chữ (thoại 1 dòng) — cần soi khi làm `img_doan.txt`.

## 1e. TẬP 2 `ep02-1000yen-shumi` — luồng lean trọn (2026-09-20 16:12, LOCK sha 84beda216e)
Fable viết đúng ngân sách **+1,6%** ngay lần đầu (rủi ro lớn nhất của luồng lean → đã đo, đạt). Vòng Sol ESCALATE 1 lần
(3 FIX liên tiếp, mỗi patch sinh 1 lỗi đạo cụ mới) → lớp 3 sửa tay theo báo cáo → chạy lại PASS → lớp 3 đọc bản khoá phát hiện
2 lỗi LANE (CTA bị dời cuối · câu bám gốc) → đưa vào `viec_tay.txt` → mở lock → 1 patch → Sol PASS → LOCK. Chi tiết số đo ở
`docs/QUY_TRINH_KICH_BAN_GON.md` đầu file. **Quy ước lớp 3 từ nay:** đọc bản khoá → có lỗi thì ghi `viec_tay.txt` (1 dòng/việc, có
trích câu) + `gate_common.ghi_lock(d,"ESCALATE",reason=...)` → chạy lại `make_video --den B3G`; KHÔNG sửa thẳng `script.txt`.

## 1f. 10/10 TẬP KỊCH BẢN XONG (2026-09-20 tối) — sheet D2:D11 = `Done`
ep03–ep10 chạy trong ~2h (2–3 tập song song). Bảng benchmark + 7 vá trong ngày + bài học S1 ở `docs/QUY_TRINH_KICH_BAN_GON.md`
(mục BENCHMARK 10/10). Quy ước lớp 3 đã dùng thật 6 lần: `viec_tay.txt` (1 dòng/việc, trích câu, kèm "mọi phần khác giữ nguyên") →
chạy lại `--den B3G`; khi bản viết đầu lệch hẳn tiêu đề thì sửa `series_ctx.txt` (đổi "gợi ý" → "BẮT BUỘC") + đổi tên file cũ `_lan1_*`
+ xoá `B3` trong state.json → viết lại từ đầu (ep05, ep06). Phạm vi vẫn CHỈ kịch bản — B4 giọng/B5W prompt ảnh chưa chạy tập nào.

⚠️ Hook bắt buộc khoá trước S2 (dài ≈ hook video gốc). Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.

## 2. LỆNH CHẠY (Giai đoạn 3 — 1 tập anh chỉ định)

```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
:: 1) thư mục tập + hồ sơ đề tài
mkdir ..\assets\teinengo-tanoshimi\ep01-asa-shukan
py -3.13 -X utf8 retrieve_videos.py --dna-dir ..\docs\channel_dna\rougo-money-story --topic "60代 朝の習慣 5選 体が軽くなる" --top 3
::    → chọn 1 transcript cùng dạng đếm → competitor.txt (KHUNG KỂ, PASS 0 sẽ bóc khung, giấu bản gốc)
::    → series_ctx.txt = TƯ LIỆU THẬT có nguồn (địa điểm/giá/thông tin Nhật) — tự tra WebSearch, ghi URL
:: 2) chạy tới HẾT bước 1 rồi DỪNG
py -3.13 -X utf8 make_video.py --profile teinengo-tanoshimi --slug ep01-asa-shukan --den B3G
```
> ⛔ **2026-09-27 — SOÁT BẰNG CHATGPT WEB (mặc định, thay máy 3):** lệnh trên tự DỪNG sau khi khoá và in 3 lệnh `soat_kb_gptweb.py --lan1` → thẩm định/phản biện (cổng giữ mở) → `--chot` → viec_tay → `--xong` (docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md §4b). Đoạn máy 3 dưới đây TẠM ẨN.
> (cũ, tạm ẩn) ⛔ **2026-09-26 — lệnh trên giờ TỰ DỪNG sau khi khoá kịch bản** và gửi máy 3 soát (`FlowHandoff_local\jobs\G-teinengo-tanoshimi\<slug>\review\`,
> cột D = `Chờ kiểm tra kịch bản`). Chờ anh báo D = `Đã sửa kịch bản` → `py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile teinengo-tanoshimi --slug <slug>`
> rồi mới đi tiếp B5W/hook/`dong_goi_may2`. Chi tiết: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §4c.
```
::    (--den B3G = PHẠM VI HIỆN TẠI §1c: dừng sau nghiệm thu cuối + đo lại gate số; bỏ --den khi anh mở rộng sang giọng/prompt ảnh)
```
Bước 1 phải để lại trong thư mục tập: `script.txt` (+gate) · `characters.json` · `img_prompts.txt` ·
`img_doan.txt` · master REF-LOCK nhân vật chính · `thumb_text.txt` · `TIEU_DE_MO_TA.txt` (tiêu đề + mô
tả + hashtag `#定年後 #60代 #シニアライフ #老後 #暇つぶし` + tags — bước 2/3 KHÔNG tự viết nội dung).
Xong → cột D `done` + K → **DỪNG**. Không tự `upload-job` lần đầu (⛔ CLAUDE.md).

## 3. GATE — ngưỡng đã đo (chi tiết + nguồn trong `profile.script.gate._gate_note`)

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| title_len | 33–50 | ĐO THẬT 7 HIT: 33–45 ký tự (MISS 986v: 52) |
| hook_chars (trước marker mục 1) | 1200–2300 | ĐO THẬT 6/8 video: 1365–2092 chữ = Hồi 1+2 chiếm 19–29% (1 outlier 4105; 2 video không có marker) |
| hook_marker | `1つ目`/`一つ目`/`第5位`/`第7位` | field mới `qc_script.mo_dau` (2026-09-20) — lane không có 第1章 vẫn đo được mở đầu |
| hook_anchor_per_1000 | ≥6,0 | video TOP 176k chỉ 7,6 neo/1000 — manga story không dày số liệu, KHÔNG dùng 18 của toshi |
| list_item_count | 5 | 4/7 HIT là 5選, 3/7 là 7選 — đổi 7 theo tập nếu cần |
| comma_per_sentence | 0,5–2,5 | HIỆU CHỈNH (ASR gần như không có 、) từ câu ngắn 17–22 chữ/câu (đo thật) |
| chars_per_breath | 7–18 | HIỆU CHỈNH tương tự |
| dialogue_ratio_max | 40% | ƯỚC từ 20–36% câu mang đuôi hội thoại ở 3 transcript (ASR không có 「」) |
| require_next_ep_teaser | false | video độc lập |

⚠️ 3 chỉ số HIỆU CHỈNH/ƯỚC phải đo lại bằng B3Q sau kịch bản đầu tiên (bài học toshi: đừng chép cảm
giác thành gate cứng).

## 4. LUẬT CỨNG RIÊNG LANE (handoff §3 — đã trả giá thật ở kênh mẫu)

1. Chủ đề CỤ THỂ: N選 + hành động/địa điểm + lợi ích rõ. Trừu tượng (年金受給/人生/育ち) chết 986v–3k.
2. GIỮ HƯỚNG VUI/RẺ — kịch tính tiền mất là Lane F.
3. Địa điểm/giá/thông tin Nhật có nguồn (URL trong `series_ctx.txt`); nhân vật + tình tiết hư cấu.
4. QC giọng (B4Q) trước khi giao. Giọng nam trung niên, thoại 2 nhân vật.
5. CTA comment giữa video (kênh mẫu like-rate 0,3–1,6%).
6. Title `【漫画】{trạng thái}…{N}選…{lợi ích cụ thể}`; thumbnail manga + nam trung niên + chữ lớn.
7. Mục cuối luôn là cú lật HƯỚNG NỘI (DNA quy tắc 5); sáng hôm sau khép cảnh đầu (quy tắc 7).

## 5. THUMBNAIL — template là GIẢ THUYẾT, chưa FREEZE

`CHANNEL_DNA.md §Thumbnail` chỉ SUY LUẬN (K1 không tải ảnh). Profile khai tạm: chữ 3 tầng
(YELLOW/WHITE/RED, ≤6–7 ký tự) neo trái 55% + nhân vật manga bust shot phải 45%, nền phẳng tươi,
`require_face=true`, `dedicated_bg=true`, `flat_bg=true`. **Trước tập 1 phải soi thumbnail thật** kênh
mẫu (`yt-dlp --write-thumbnail --skip-download` 8 video top) rồi hiệu chỉnh bố cục/màu ở đây + profile;
QC lớp 2 bằng `qc_thumbnail_sol.py` (form `profile.thumbnail_qc` đã khai).

## 6. CÒN TREO (nói thẳng)

- ✅ Giọng + char-rate xong; 10 tập đã ghi sheet A/B/K (dòng 2–11) 2026-09-20.
- Phạm vi hiện tại chỉ tới B3R (§1c) — giọng/prompt ảnh/REF-LOCK/tiêu đề/thumbnail chờ anh mở.
- Thumbnail thật kênh mẫu chưa soi (§5).
- `mode="story"` không kích hoạt cổng B3F kiểm dữ kiện kiểu documentary — dữ kiện thật (địa điểm/giá)
  hiện chỉ được kiểm qua `ctx_label` + B3S sol. Nếu tập 3/6/9/10 (địa điểm) lộ số bịa thì cân nhắc
  `mode="fiction_facts"` (nhánh Lane F vừa thêm 2026-09-20 trong `_chong_trung_block`) — đọc kỹ text
  nhánh đó trước, nó viết cho số chế độ 年金, không phải giá vé/địa danh.
- 8 video còn lại của kênh mẫu (<40k, gồm 5 MISS) chưa qua K2 — chỉ cần nếu muốn học pattern THUA.

## HOOK — LUẬT VIẾT + CÁCH DỰNG CỦA LANE NÀY

> Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.
> (Kiểu mở `script.hook.patterns` / câu khoá `script.hook.closer` / độ dài 20–30 giây cũ không còn là luật viết.)

| | |
|---|---|
| Cách dựng hình (`script.hook.visual`) | `manga_ai_ref` |
| Nguồn hình | manga AI, REF-LOCK cùng bộ nhân vật với thân video |
| Công tắc (`script.hook.enabled`) | đang TẮT |

Runbook dựng đầy đủ (7 bước + 4 phép kiểm trước khi ghép): `docs\QUY_TAC_VIDEO_HOOK.md`, bảng so sánh
cách dựng của mọi lane ở §5b.

Viết hook: `py -3.13 pipeline\hook_stage.py --profile teinengo-tanoshimi --slug <tập> --mode repair`
