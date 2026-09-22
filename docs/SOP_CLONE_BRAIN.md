# SOP — CLONE VIDEO BẰNG "BỘ NÃO CLAUDE" (tool `brain_*` + `render_engine`)

> Runbook cho nhánh **não Claude**: `brain_channel.py` → `brain_steps.py` (gọi `claude -p` headless)
> → `render_engine.py`. Khác hẳn nhánh **não ramcloud** (`make_video.py`/`gui_video.py`) — hai tool
> TÁCH HẲN, cấm gộp, xem memory `hai-tool-exe-tach-han`.
>
> Chốt ngày 2026-09-11 sau 8 lượt chạy thật trên kênh simbot2. Mọi con số trong file này là **đo
> thật**, không phải ước lượng.

> ⚠️ **NIÊM từ tập SAU tập 11 (anh chốt 2026-09-22):** satori chuyển sang `script.flow=lean` qua
> `make_video.py --profile satori-jp-obaa` (Fable viết 1 lần S2 → Opus vá S4 → Sol chấm S5), thay cho
> `brain_channel.py` — lý do: agent ở nhánh này tự viết+tự sửa lặp, không tách vai viết/sửa/chấm, ngược
> nguyên tắc chung mọi lane (xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §0a). Tập 11 đang dở (đã giao
> máy 2, nửa sau quy trình chưa nghiệm thu) vẫn chạy NỐT theo file này — không đổi pipeline giữa chừng.
> File này giữ lại tham khảo lịch sử, không dùng cho tập mới. Xem memory `lane-satori-lean-flow-2026-09-22`.

---

## ⭐ THẺ CHẠY — QUY TRÌNH CHUẨN MỘT VIDEO (đọc cái này trước, phần dưới là lý do)

Ba lệnh, bốn cổng. Mọi tập đều đi đúng đường này, không chế thêm.

### Bước 1 — chọn video
```bat
py -3.13 pipeline\brain_channel.py --channel "https://www.youtube.com/@simbot2" ^
    --profile satori-jp-obaa --limit 20
```
Chọn video **view cao, chưa làm**. Số thứ tự trong bảng chính là `--pick`.

### Bước 2 — phần CHỮ, dừng trước khâu tốn tiền
Chạy `make_video_one(..., stop_before_render=True)` (mẫu: `scratchpad/run_sach_v11.py`, sửa `id`
với `idx`). Ra: `script.txt` · `characters.json` · `img_prompts.txt` · `thumb_text.txt` + 2 ảnh
master đã QC. **Chưa TTS, chưa gen loạt ảnh ⇒ 0 đồng** (trừ ~150–330đ ảnh master).

#### ⭐⭐ QUY TRÌNH QC BƯỚC 1 CHUẨN LANE SATORI (anh chốt 2026-09-18, chứng nhận trên STT9 — MỌI TẬP TỪ ĐÂY ÁP DỤNG)

Toàn bộ nằm trong `make_video_one(..., stop_before_render=True)` (`brain_channel.py`), **tự chạy, không
làm tay bước nào**. Ký hiệu: 🔒 chặn cứng · ⚠️ WARN ghi log, đi tiếp · ✍️ Claude sửa tại chỗ.

```
 1  B2   bóc bản gốc Hàn            fetch_script.py                  → competitor.txt + .segments.json
 2  B2Q  cổng transcript 🔒          qc_transcript.py (0 LLM)         coverage<0.80 / dup>0.15 = dừng
 3  B3   viết script Nhật 70/30     Claude (claude -p, pha "script") → dan_y.txt · script.txt · voice.json
 4  CỔNG SỐ 🔒                       gate_check + fix_gate + qc_tien  máy nắn độ dài; tiền quy đổi 1:10 won = dừng
 5  B3Q  cổng nội dung              qc_script.py = GEMINI-3.8-flash  ĐẠT / SỬA / HỎNG (mâu thuẫn, bám gốc 70/30)
         ✍️ ≤3 vòng sửa tại chỗ; số lỗi không giảm → ESCALATION_REPORT.md, dừng
         ⛔ KHÔNG còn tầng 2 Claude chấm (qc_claude.py TẮT khi lane có sol — cùng model chấm nhau vô nghĩa)
 6  B3S  trọng tài độc lập          qc_script_sol.py = GPT-5.6-SOL   lens "story", 1 call cả tập, ~2,7 phút
         PASS         → bước 7
         FIX          → ✍️ Claude sửa CHỈ mục ghi SAI (bỏ CHƯA HAY) → sol chấm lại ĐÚNG 1 lần
                        → PASS / FIX nhẹ đều qua · REMAKE → nhánh dưới
         REMAKE       → ✍️ Claude kiểm từng lỗi sol nêu, xoá/sửa cái SAI thật, TỰ chấm lại,
                        ghi logs/B3S_claude_verdict.txt dòng đầu `PASS` (lỗi nhẹ vẫn PASS)
                        hoặc `SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC` 🔒 → ESCALATION_REPORT.md, dừng
         resume: script.txt chưa đổi (sha256 trong logs/B3S_latest.json) → bỏ qua, không chấm lại
 7  ASSETS                          Claude (pha "assets", cấm sửa script, ≤2 lượt)
                                    → characters.json · master.txt · img_prompts.txt · img_doan.txt
                                      thumb_text.txt · thumb_bg_prompt.txt · TIEU_DE_MO_TA.txt
 8  FINGERPRINT + STALE 🔒          gate_common (sha256)             script đổi sau khi có asset = dừng
 9  REF-LOCK                        ima2/gpti2 + QC vision           2 master nhân vật (~150-330đ)
10  B5P  prompt ↔ dữ kiện truyện ⚠️  qc_prompt_consistency.py gemini  story_facts.json; PROMPT_CONFLICT / AMBIGUOUS
11  B55  ảnh ↔ đoạn ⚠️               qc_img_doan.py gemini            FAIL cơ học 🔒 · SUSPICIOUS · semantic ⚠️
12  ⏸ DỪNG TRƯỚC RENDER             0 TTS, 0 ảnh loạt                → anh duyệt → giao máy 2 → Hermes
```

**Hai luật bắt buộc của B3S (rút từ STT10, 2026-09-19 — đừng bỏ):**
1. **Sửa theo sol xong PHẢI chạy lại B3Q.** Sol chỉ đọc bản Nhật đứng một mình: nó không thấy bản gốc
   Hàn và không theo dõi 伏線 toàn tập. Đo thật: sửa theo sol (bỏ chi tiết tip 1.000 yên vì "không tự
   nhiên ở Nhật") làm **gãy 伏線** cuốn sổ cuối truyện, và 3 câu viết lại thành **dịch sát bản gốc** →
   B3Q nhảy từ DAT sang HONG/SAO_CHEP. `check_b3s` nay tự chạy hồi quy B3Q + 1 lượt sửa nếu rớt.
2. **Không đuổi sol về 0 lỗi.** Sol không ổn định: mỗi lượt soi ra một tập con khác nhau. Đo thật
   STT10 qua 6 lượt: 57 → 20 → 7 → 14 → 5 → 12 mục SAI, trong đó lượt sau nêu cả mục chưa từng nêu.
   Đúng chính sách = sửa 1 lượt, chấm lại 1 lượt, còn FIX nhẹ thì đi tiếp.
3. **Dấu 、 sai chỗ giờ là cổng số.** `ai_steps.dem_cat_cum/go_cat_cum` (regex, 0 LLM) bắt 、 cắt
   て+trợ động từ (「塞いで、まいりました」), 「のでございます」, động từ+こと; `gate_check` báo lỗi,
   `fix_gate` tự gỡ trước khi đo và sau mỗi lượt gemini chèn nhịp. Nguyên nhân gốc: cổng chỉ ĐẾM 、
   (4,5–9 chữ/nhịp) nên máy nhét 、 vào chỗ duy nhất còn trống là giữa cụm động từ. Số đo tồn đọng:
   STT9 106 chỗ (đã gỡ), STT10 25, STT7 29, STT11 33 (2 tập sau đã đăng — ghi nhận, không sửa lại).

**Sau khi máy dừng ở 12, Claude (tab này) làm NGAY, không hỏi:** đọc `logs/B5P_latest.json` +
`logs/B55_mapping_latest.json`, sửa tay mọi dòng `PROMPT_CONFLICT`/`would_block` trong `img_prompts.txt`
theo đúng đoạn truyện (đọc đoạn, không đoán), chạy lại `qc_prompt_consistency.py --slug <d> --mode warn
--reuse-facts` tới `would_block=0`, rồi `gate_common.py --slug <d> --stamp`. `AMBIGUOUS` = cảnh minh
hoạ/ẩn dụ, giữ nếu hợp lý. Xong mới báo anh gói bước 1 sẵn sàng. (STT9: 4 dòng, 62 giây chấm lại.)

**Cổng WARN-only tạm thời:** B5P/B55 semantic đang `--mode warn` cho 2 tập production kế tiếp (STT10, STT11)
để đo `would_block` đúng bao nhiêu; ≥80% là lỗi thật → đổi sang `--mode fail` ở chỗ gọi trong
`brain_channel.py` (khi đó máy tự chặn + bắt Claude sửa trong flow, bỏ bước sửa tay ở trên). Cơ học
(số dòng, ID, thứ tự, STALE) đã 🔒 từ đầu, không đợi.

| Cổng | Model | Đo gì | Tốn (STT9 đo thật) |
|---|---|---|---|
| `qc_transcript.py` (B2Q) | 0 LLM | coverage/gap/dup/cpm transcript gốc | 0đ · 0,1s |
| `gate_check.py` + `fix_gate.py` | 0 LLM (+LLM rẻ khi nén) | độ dài · phẩy/câu · nhịp thở · % hội thoại | 1s (nén 2-5') |
| `qc_tien.py` | 0 LLM | số tiền = bản gốc ÷10 → chặn | 1s |
| `qc_script.py` (B3Q) | gemini-3.8-flash | đọc hiểu · mâu thuẫn · bám gốc 60–80% | 40s |
| `qc_script_sol.py` (B3S) | **GPT-5.6-sol** (9router `cx/gpt-5.6-sol`) | 6 lăng kính story: mâu thuẫn dữ kiện · số học & tiền Nhật thật · dấu vết Hàn · logic hành vi · tuyệt đối hoá · nhịp đọc — tách SAI/CHƯA HAY | 2,7'/lượt ×2 + Claude sửa 11' |
| `gate_common.kiem_stale` | 0 LLM | sha256 script ≠ lúc sinh asset → FAIL | 0s |
| `qc_prompt_consistency.py` (B5P) | gemini-3.8-flash | prompt ↔ story facts; cơ học FAIL, semantic WARN | 14 call · 212s |
| `qc_img_doan.py` (B55) | gemini-3.8-flash | ảnh ↔ đoạn; cơ học FAIL, SUSPICIOUS, semantic WARN | 6 call · 99s |

**Toàn tập STT9 đo thật: phần chữ + QC 47 phút** (27' lần chạy B3Q+B3S+sửa, 19,6' lần resume assets→B55;
không tính 116' lần đầu chạy bằng quy trình cũ 2 tầng không hội tụ). Log đủ tại `<slug>/logs/`
(`B3S_sol_001/002.txt`, `B5P_latest.json`, `B55_mapping_latest.json`, `artifact_meta.json`).

#### Migration tập cũ chưa stamp (2026-09-18)
- (a) Tập chưa có `artifact_meta.json` → chạy `py -3.13 qc_prompt_consistency.py --slug <d>` + `py -3.13 qc_img_doan.py --slug <d>`
  xem prompt/mapping còn khớp script hiện tại không, RỒI MỚI `py -3.13 gate_common.py --slug <d> --stamp`. **Cấm stamp mù**
  cho tập biết là stale (STT7: script 07:58 mới hơn prompt 07:35 → phải rà prompt trước).
- (b) Tập đã giao hàng (ep01/04/06/07…) KHÔNG cần stamp trừ khi làm lại.
- (c) STT3 đã stamp (Task 1); STT8/STT2/STT5 chưa — stamp khi đụng tới.

#### Production = dừng trước render
Sản xuất luôn gọi `make_video_one(..., stop_before_render=True)` (`chay_phan_chu.py` đã truyền tường minh). Nhánh
`render_engine.py` ở cuối hàm chỉ cho test / tập non-hybrid cũ; handoff thật = máy 2 vẽ ảnh → Hermes ghép (không đổi).

### Bước 3 — gen ảnh + dựng video
```bat
py -3.13 pipeline\render_engine.py --slug "assets\satori_jp\<slug>" ^
    --profile satori-jp-obaa --quality low --workers 8
```
12 bước: ảnh → TTS → giãn nhịp → SRT → ghép → QC hình → **B8V bản phụ đề Việt để anh soi nội dung**
→ thumbnail → gói đăng tải → B10 nghiệm thu. Video đăng **không cháy phụ đề** (YouTube tự bật CC);
muốn cháy thì thêm `--burn-sub`.

### Bước 4 — giao hàng
Bản đăng `final.mp4` + `voice.srt` (up làm CC) + `thumbnail_final.png` + gói tiêu đề/mô tả.
Bản `final_vi.mp4` chỉ để anh duyệt nội dung, **không đăng**.

---

### Cổng rớt thì làm gì — LUẬT CỨNG

**SỬA TẠI CHỖ TRÊN BẢN CŨ. Cấm xoá đi chạy lại.** Chạy lại là sinh chữ mới ⇒ bộ lỗi mới ⇒ không bao
giờ hội tụ (đo thật: chạy trọn gói 73 phút + $16 quota rồi vẫn FAIL, trong khi sửa tại chỗ 2 nhát
Edit là ĐẠT).

| Cổng rớt | Làm gì |
|---|---|
| Cổng số (dài/ngắn, phẩy, nhịp thở) | `fix_gate.py` — **MÁY nắn**, Claude không tự cắt (tự cắt: 26 phút; máy: 2,4 phút) |
| Cổng tiền | Tra `docs/SO_LIEU_THAT_JP.md` → không có thì WebSearch → ghi bổ sung vào bảng. **Cấm quy đổi theo tỉ giá, cấm bịa** |
| B3Q gemini bám gốc >90% | BỎ HẲN 2–3 nhịp gốc + THÊM 3–4 nhịp tự nghĩ. Sửa câu chữ không gỡ được (cổng chấm KHUNG SỰ KIỆN) |
| B3S sol FIX | Máy đã tự lo (Claude sửa mục SAI → sol chấm lại 1 lần). Mục CHƯA HAY **bỏ qua** — đuổi theo PASS tuyệt đối là vòng lặp vô tận (sol không bao giờ tự PASS văn phổ thông) |
| B3S sol REMAKE | Máy đã tự lo (Claude kiểm từng lỗi, tự chấm). Chỉ khi ra `SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC` mới tới tay anh: đọc `logs/B3S_sol_00N.txt` + `B3S_claude_verdict.txt`, quyết lại cốt truyện |
| B5P `PROMPT_CONFLICT` / B55 semantic ≤2 | Claude tab này sửa tay dòng prompt theo đoạn truyện, chấm lại `--reuse-facts`, `--stamp` (xem mục QUY TRÌNH QC ở trên) |
| STALE | Sửa script sau khi có asset → rà/viết lại `img_prompts.txt` + `img_doan.txt` theo bản mới rồi `gate_common.py --stamp`. **Cấm stamp mù** |

Muốn thử một bản vá ở tầng cổng thì **chấm lại kịch bản cũ** (`qc_script_sol.py --script <script cũ>
--profile satori-jp-obaa`, ~3 phút), đừng chạy lại cả pipeline.

### Thời gian & chi phí thật một tập

| Khoản | Số đo |
|---|---|
| Phần chữ + QC đủ 12 mốc (quy trình sol, STT9) | **~47 phút** (B3S FIX 1 vòng + sửa tay 4 prompt) |
| Phần chữ, đường thông suốt (cũ, trước sol) | 18–20 phút |
| Cào nguồn dính 429 (phải nghe lại bằng whisper) | +4 phút |
| Mỗi lượt chấm B3S sol | 2,7 phút (cả tập 1 call) — thay tầng 2 Claude cũ 9–11 phút |
| Ảnh: ~120 tấm × 50đ + 2 master | **≈ 6.000–8.000đ** |
| Giọng OpenSpeaker ~8.400 chữ | ≈ 1.500đ |

### ⚠️ TRẠNG THÁI CHỨNG NHẬN (cập nhật 2026-09-11) — đọc trước khi tin tưởng chạy hàng loạt

| Chặng | Tình trạng |
|---|---|
| Bước 1–2 (phần chữ + 4 cổng) | ✅ **Đã chứng minh** — tập 11 qua sạch cả 4 cổng với bộ cổng hiện tại |
| Bước 3–4 (ảnh → video → giao hàng) | ⚠️ **Code chạy được nhưng CHƯA chứng nhận với cấu hình mới**. Hai tập đã dựng trọn (`simbot2-vU5PWT2zLDs` 9/9, `simbot2-02` 10/9) đều làm theo cấu hình CŨ: phụ đề cháy vào hình, chưa có B8V bản tiếng Việt, chưa có `qc_tien`, chưa có cổng tầng 2 phân mức. `simbot2-02` đến giờ vẫn còn 2 dấu vết quy đổi tiền. |

⇒ Tập 11 là **lượt chứng nhận** cho nửa sau. Chạy trọn Bước 3 một lần, soi kết quả, rồi mới nhân ra
các tập khác. Trước khi có lượt đó, **đừng chạy hàng loạt**.

---
## 0b. RANH GIỚI HỒ SƠ — KÊNH vs TẬP (user chốt hướng 3, 2026-09-11)

| | Ở đâu | Ai viết | Đổi theo |
|---|---|---|---|
| Danh tính **KÊNH** (giọng văn, ngôi kể, nhịp văn, char_rate, ngưỡng gate) | `profiles/profiles/<id>.json` | **Người** (hoặc `calibrate.py` đo) | Hiếm khi |
| Danh tính **NGƯỜI KỂ CỦA TẬP** (giới, tuổi, nghề, tiểu sử, khuôn mặt) | `voice.json` + `characters.json` trong thư mục tập | `detect_voice` + Claude | **Từng tập** |

Kênh satori là kênh **RỜI RẠC** — mỗi video một người kể khác nhau (kênh gốc simbot2 cũng vậy). Nên
`narrator.gender` để **TRỐNG**: `detect_voice` đọc transcript video gốc rồi tự chọn giọng nam/nữ cho
đúng người kể của tập đó. `narrator.persona` chỉ tả mức chung ("một người già Nhật kể chuyện đời
mình, ấm, chậm, chiêm nghiệm").

⛔ **TUYỆT ĐỐI KHÔNG ghi tiểu sử của một tập vào profile.** Đo thật 2026-09-11: gặp mâu thuẫn giữa
profile ("thợ may sống cô độc Osaka") và cốt truyện tập (viện dưỡng lão Nagano), bộ não chọn cách
dễ — **sửa hồ sơ CẢ KÊNH cho khớp một tập**, ghi hẳn "mở viện dưỡng lão ở Kanto, nay là cư dân một
viện ở Nagano sau khi trẹo khớp háng" vào `narrator.persona`. Mọi tập sau sẽ thừa hưởng tiểu sử đó.
Mâu thuẫn kiểu này thì **sửa TẬP, không bẻ KÊNH**.

Rào đã dựng: `brain_channel._khoa_profile()` chụp file profile trước mỗi lần gọi bộ não,
`_kiem_profile()` so lại sau — khác thì **tự khôi phục + cảnh báo** (gắn ở cả 3 chỗ gọi bộ não).

## 0. NGUYÊN TẮC LỚN NHẤT — PHÂN VAI

**Claude VIẾT. Máy ĐO và NẮN.**

| Việc | Ai làm | Vì sao |
|---|---|---|
| Cốt truyện, thoại, cảm xúc, bản địa hoá | **Claude** | Đây là giá trị của cả kiến trúc này |
| Sửa lỗi logic / mâu thuẫn / sao chép nguồn | **Claude** | Phải HIỂU nội dung mới sửa được |
| Ép độ dài, mật độ dấu phẩy, nhịp thở, tỉ lệ hội thoại | **MÁY** (`fix_gate.py`) | Claude **không đếm được ký tự khi đang sinh chữ** |

Vi phạm nguyên tắc này là lỗi đắt nhất của cả pipeline. Bằng chứng đo thật (mục tiêu 8.100 ký tự):

| Cách làm | Nháp đầu | Kết cục |
|---|---|---|
| Dặn "viết đúng ~8.100 chữ" | 20.000 (×2,5) | Claude tự cắt **35 phút**, cạn ngân sách, vẫn thừa 97 chữ |
| Thêm "đừng viết dài rồi cắt" | 10.906 (×1,35) | vẫn phải cắt |
| Thêm "viết đúng 64 đoạn × 126 ký tự" | 16.014 (×2,0) — viết ra **104 đoạn** | vẫn phải cắt |
| Thêm "viết 10 đoạn rồi dừng đo" | (bỏ qua lệnh) | vẫn phải cắt |
| Thêm dàn ý 64 dòng đánh số | 16.685 (×2,0) | **tự viết lại 5 lần = 26 phút**, cạn ngân sách, tập FAIL |
| **Giao việc cắt cho `fix_gate.py`** | 9.701 (×1,2) | **máy nén xong trong 2,4 phút, 0 quota Claude** |

---

## 1. CHẠY MỘT VIDEO

### 1.1 Quét kênh, chọn video
```bat
py -3.13 pipeline\brain_channel.py --channel "https://www.youtube.com/@simbot2" ^
    --profile satori-jp-obaa --limit 20
```
In ra bảng STT · view · thời lượng · tiêu đề. Chọn video **view cao, chưa làm**.

### 1.2 Chạy trọn gói
```bat
py -3.13 pipeline\brain_channel.py --channel "https://www.youtube.com/@simbot2" ^
    --profile satori-jp-obaa --pick 4
```

### 1.3 Chạy tới TRƯỚC khâu tốn tiền (khuyến nghị khi thử nghiệm)
Gọi `make_video_one(..., stop_before_render=True)` — dừng sau khi xong phần chữ + ảnh master, **chưa
TTS, chưa gen loạt ảnh**. Script mẫu: `scratchpad/run_videoNN_test.py`.

Nhớ **in mốc thời gian** ở mọi callback (xem §5).

---

## 2. CÁC BƯỚC VÀ CỔNG

| Bước | Ai chạy | Ra gì | Cổng chặn |
|---|---|---|---|
| B2 | Python | `competitor.txt` (transcript đối thủ) | thiếu = bỏ tập |
| B2Q (mới 2026-09-18) | Python `qc_transcript.py --slug <d>` | `logs/B2Q_latest.json` | FAIL (coverage<80% / dup>15% / rỗng / sidecar hỏng) = dừng; WARN/SKIPPED đi tiếp (SKIPPED chỉ hợp lệ tập bóc trước 2026-09-18) |
| B2 giọng | Python (`detect_voice`) | `voice.json` — giọng RIÊNG từng video | — |
| B2b | Python (`ai_steps.analyze_comments`) | `comment_insight.json` | **không bao giờ chặn** |
| Hàng rào lane | Python | — | `gate_declared()` chưa khai → **DỪNG trước khi tiêu tiền** |
| B3 | **Claude** | `dan_y.txt` → `script.txt` | cổng số học + B3Q |
| B3 nắn số | **MÁY** `fix_gate.py` | ghi đè `script.txt` | — |
| B3Q | Claude + `qc_script.py` | — | logic/văn hoá/sao chép 70/30 |
| B3 pha SCRIPT / B5 pha ASSETS (mới 2026-09-18) | **Claude** `run_creative(phase="script"\|"assets")` | pha script chỉ ra `script.txt`; pha assets (sau B3Q đạt, ≤2 lượt, cấm sửa script) ra `characters.json` · `img_prompts.txt` · `img_doan.txt` · `thumb_text.txt` · `TIEU_DE_MO_TA.txt` | thiếu file của đúng pha (`NEED_BY_PHASE`) = dừng; `BRAIN_BLOCKED` = dừng |
| B5 | **Claude** | `characters.json`, `master.txt`, 2 ảnh master, `img_prompts.txt` | `qc_character.py` |
| Stamp + STALE (mới 2026-09-18) | Python `gate_common.ghi_fingerprint` / `kiem_stale` | `artifact_meta.json` (sha256 script ↔ img_prompts/img_doan) | sha256 script ≠ lúc sinh → **chặn cứng**; chưa có meta + script mới hơn artifact >2s → chặn; còn lại WARN |
| B5P (mới 2026-09-18) | Python `qc_prompt_consistency.py --slug <d>` (gemini-3.8-flash) | `logs/B5P_latest.json` (`metrics.semantic.would_block`) | FAIL cơ học/STALE/LLM hạ tầng = dừng; PROMPT_CONFLICT/AMBIGUOUS = WARN (mode warn, chưa bật `--mode fail`) |
| B55 mapping (mới 2026-09-18) | Python `qc_img_doan.py --slug <d>` (gemini-3.8-flash) | `logs/B55_mapping_latest.json` | FAIL cơ học (malformed/≠ số prompt/thiếu-trùng ID/ngoài 1..N/giảm thứ tự/STALE/thiếu img_doan.txt/LLM hạ tầng) = dừng; SUSPICIOUS + semantic ≤2 = WARN |
| B7 | **Claude** | `thumb_text.txt` | — |
| B4→B10 | Python (`render_engine.py`) | giọng → ảnh → video → gói đăng tải | B4Q·B5Q·B8Q·B10 |

### 2.1 Cổng SỐ HỌC (chặn cứng, máy đo, 0 đồng)
```bat
py -3.13 pipeline\gate_check.py --profile satori-jp-obaa --script <script.txt> --minutes 30
```
Ngưỡng lấy từ `profile.script.gate` (satori-jp-obaa): độ dài **mục tiêu ±12%** · **2,5-6,0 dấu
phẩy/câu** · **4,5-9,0 ký tự/nhịp thở** · **hội thoại ≤15%**.

### 2.2 Nắn về đúng cổng — BẰNG MÁY
```bat
py -3.13 pipeline\fix_gate.py --script <script.txt> --profile satori-jp-obaa --minutes 30
```
Chuỗi 3 bước, mỗi bước **chỉ nhận bản mới khi số lỗi GIẢM**:
1. `ai_steps.trim_chunked` — nén theo khúc có hạn mức (nén cả bản 1 lượt thì ĐỨNG YÊN)
2. `them_nhip()` / `ai_steps.reduce_commas` — **hai chiều**: thiếu nhịp thì THÊM 、, thừa phẩy thì TÁCH CÂU
3. `ai_steps.reduce_dialogue` — hạ tỉ lệ hội thoại

`them_nhip()` có **chốt bất biến**: bỏ hết 、 và khoảng trắng thì bản mới phải giống hệt bản cũ —
LLM lén đổi chữ là BỎ khúc đó. Verify thật: 9,0 → 7,7 ký tự/nhịp thở trong **0,5 phút**, chữ nghĩa
giữ nguyên 100%.

### 2.3 Cổng NỘI DUNG B3Q (Claude tự sửa, máy không làm hộ được — nhưng MÁY PHẢI XÁC MINH)
```bat
py -3.13 pipeline\qc_script.py --profile satori-jp-obaa --script <script.txt> --competitor <competitor.txt>
```
Chấm bằng **khung sự kiện**: giữ **60-80%** nhịp gốc → ĐẠT · **>90% hoặc <50%** → rớt · một câu dịch
sát bản gốc = **SAO CHÉP = hỏng nặng**. Ngoài ra soi logic, mâu thuẫn, số học, sót văn hoá nguồn.

⛔ **KHÔNG TIN BỘ NÃO TỰ KHAI ĐÃ QC.** `brain_channel.check_b3q()` chạy LẠI cổng này bằng máy sau khi
bộ não xong; rớt thì gọi bộ não sửa đúng các chỗ bị nêu (≤3 lượt), vẫn rớt thì **CHẶN**, không cho
sang khâu tốn tiền.

**2026-09-18 — B3Q chỉ còn 1 tầng gemini; tầng 2 `qc_claude.py` TẮT khi lane có `script.sol_qc`.** Lý do
anh chốt: Claude chấm văn Claude viết = cùng model tự nhận đúng, và 3 giám khảo (gemini + Claude + Claude
viết) cãi nhau làm B3Q STT9 không hội tụ 116 phút (7→6→1→5 lỗi). Vai "bắt cái gemini mù" (tiền quy đổi,
dấu vết Hàn, mâu thuẫn dữ kiện) chuyển sang **B3S GPT-5.6-sol** — khác hãng thật sự, 2,7 phút thay 10
phút. Chi tiết B3S: mục "QUY TRÌNH QC BƯỚC 1 CHUẨN" ở THẺ CHẠY + `docs/QC_SCRIPT_GPT_SOL.md`.

Vì sao phải verify (đo thật 2026-09-11): bộ não chạy B3Q, gặp Gemini chặn content-policy, tự kết
luận *"lỗi hạ tầng, không phải script sai"* rồi đi tiếp. Chạy lại thật thì kịch bản đó có **14 lỗi**:
nhân vật khai 74 tuổi thợ may nhưng kịch bản dựng thành 78 tuổi từng làm y tá mở viện dưỡng lão ·
còn sót 「水キムチ」 của bản gốc Hàn · mốc thời gian tự mâu thuẫn. Tin lời tự khai = xuất bản kịch bản hỏng.

⚠️ **Bẫy đi kèm — chính sách nội dung chặn CÂM:** ngách satori toàn tang ma/viện dưỡng lão nên Gemini
chặn thường xuyên, và nó trả câu từ chối **dưới dạng NỘI DUNG BÌNH THƯỜNG, HTTP 200** (không phải
lỗi). `llm_client` có chuỗi đổi model dự phòng nhưng không nhận ra câu đó ⇒ coi là output hợp lệ ⇒
**cả chuỗi đứng yên**. Đã thêm các dấu hiệu (`prompt could not be submitted`, `prohibited use
policy`, `contains sensitive words`…) vào `llm_client.BAD_CONTENT` để tự nhảy sang `gpt-5.6-luna`.

### 2.4 Cổng DỮ LIỆU THẬT — tiền (máy) + chi tiết đời thật (người tra)

**Triệu chứng đã đo (2026-09-11).** Nhân bản kịch bản Hàn → Nhật, bộ não **quy đổi con số tiền theo
tỉ giá — chia 10 — rồi giữ nguyên cấu trúc số**: `130만원 → 十三万円` · `82만원 → 八万二千円` ·
`3.000만원 → 三百万円`. Soi lại toàn dự án: **14 dấu vết**, có cả trong video đã dựng xong. Gemini
(tầng 1) **mù hoàn toàn** với lỗi này, hai lượt liền báo ĐẠT. Đây là **dấu vân tay của bản sao chép**
— nặng hơn dịch sát câu chữ, vì khán giả bản xứ nhìn mức lương hưu là biết ngay không phải chuyện
nước mình.

**Tiền = máy soi (tất định, 1 giây, 0 đồng)** — đã nối làm tầng 0 của `check_b3q()`:
```bat
py -3.13 pipeline\qc_tien.py --script <script.txt> --competitor <competitor.txt>
```
Nó đọc số Hán-Nhật (kể cả kiểu bất quy tắc `一三万`), đối chiếu từng số với bản gốc, trùng đúng tỉ lệ
1:10 là **chặn**. Có sàn 100円 để `一円`/`十円` (thành ngữ "không một xu") không báo động giả.

**⚠️ Tiền chỉ là MỘT LOẠI — mọi chi tiết đời thật đều phải tra được (anh chốt 2026-09-11).** Sửa xong
phần tiền vẫn còn nguyên một lớp chi tiết sai kiểu y hệt, máy không đong đếm được:

| Loại | Sai thật đã gặp | Sự thật |
|---|---|---|
| Lịch chi trả | "đầu tháng ra lĩnh lương hưu" (bê nhịp hằng tháng của bản gốc) | Nhật trả **6 lần/năm, ngày 15 các tháng CHẴN**, mỗi lần 2 tháng |
| Thuật ngữ y tế | 「延命の不同意書」 (dịch sát) | 事前指示書 / リビング・ウィル |
| Loại hình viện | bắt cụ bà nộp "tiền đặt cọc vào viện" | 特養 **không thu tiền vào**; có thu thì là 有料老人ホーム |
| Phong tục | mang 南瓜の煮物 đi thăm bệnh (= 호박죽 Hàn), nấu 赤飯 thay 김장 | phải là thứ người Nhật thật sự làm trong đúng hoàn cảnh đó |

Quy trình bắt buộc, **giống hệt phần tiền**:
1. Tra bảng dữ liệu đã kiểm chứng của dự án: **`docs/SO_LIEU_THAT_JP.md`** (bảng tiền + bảng
   *Thủ tục · lịch · phong tục*).
2. Không có → **WebSearch số/sự thật**, dùng đúng con số đó, rồi **ghi bổ sung một dòng vào chính
   file đó** kèm nguồn + ngày tra. Sổ tự dày lên theo từng tập, tập sau khỏi tra lại và số liệu
   thống nhất giữa các tập.
3. Tra không ra → **viết mờ đi hoặc bỏ hẳn**. *Một chi tiết mơ hồ mà đúng còn hơn một chi tiết cụ
   thể mà sai.* Cấm bịa cho "nghe hợp lý" — bịa chính là cách lỗi ÷10 tái sinh dưới dạng khác.

Luật này nằm **trong prompt** (`brain_steps.creative_prompt`, khối 💴 + 🔎) chứ không phải ở tầng điều
phối — đúng nguyên tắc §0: công cụ nào bộ não phải dùng thì phải nằm trong chính đề bài của nó.


### 2.5 CỔNG PHẢI CÓ THỂ ĐẠT ĐƯỢC — bài học đắt nhất (2026-09-11)

**Triệu chứng.** Tập 11 chạy trọn gói **73 phút**, tốn **$16 quota**, rồi FAIL. Cổng tầng 2 báo 16 lỗi
→ bộ não sửa đúng 14 chỗ nó nêu → chấm lại ra **20 lỗi MỚI**. Cổng số học ĐẠT, cổng tiền SẠCH,
tầng 1 ĐẠT hai lượt. Nghĩa là kịch bản không hỏng — **cổng hỏng**.

**Nguyên nhân.** Tầng 2 là một LLM được hỏi "tìm lỗi đi", và cổng **chặn khi tổng số lỗi > 0**. Hỏi
kiểu đó thì lần nào cũng tìm ra được, vì phần lớn cái nó nêu là **ý kiến văn phong** ("người bản xứ
thường nói khác", "nên chọn số tròn hơn") chứ không phải sai sự thật. Số 0 là mức không bao giờ với
tới. **Cổng không thể đạt thì không phải cổng, là vòng lặp.**

**Cách vá (đã làm).**
1. Giám khảo phải khai MỨC cho từng lỗi, ranh giới định nghĩa chặt trong đề bài:
   · `CHAN` = kiểm chứng được, ai soi lại cũng kết luận y hệt (bất khả thi, sai thủ tục/phép tính,
     sót dấu vết bản gốc, quy đổi tỉ giá, hai đoạn nói ngược nhau, câu dịch gần nguyên văn).
   · `GOPY` = mọi thứ còn lại, KỂ CẢ khi nó rất chắc (văn phong, xưng hô, mức độ tự nhiên, thị hiếu).
   Dòng không khai mức → xếp vào GOPY (mặc định nghiêm khắc làm hỏng cả kịch bản đúng).
   Đề bài nói thẳng cho giám khảo biết vòng lặp 16→20 đã xảy ra, và "không có lỗi CHAN nào là kết
   quả hợp lệ và tốt".
2. `check_b3q()` chỉ cộng danh sách `CHAN` vào lỗi chặn; góp ý in ra rồi thôi.
3. Vòng sửa: từ 1 lượt → `VONG_SUA_B3Q = 3` lượt **sửa tại chỗ**, và **dừng ngay khi số lỗi chặn
   không giảm** (không giảm = sửa nữa cũng vô ích, chỉ đốt lượt).

**Số đo chứng minh** — CÙNG một kịch bản, CÙNG giám khảo, không đổi một chữ:

| | Cổng cũ | Cổng mới |
|---|---|---|
| Kết luận | 20 lỗi → CHẶN → FAIL | **2 lỗi chặn** + 18 góp ý |
| Sau khi sửa đúng 2 chỗ đó | — | **ĐẠT** · 0 chặn · 7 góp ý |

18/20 vòng sửa trước đây là đuổi theo ý kiến văn phong. Hai lỗi thật còn lại sửa xong trong 2 nhát
Edit: `松飾り` treo đầu tháng 12 (tục Nhật treo 26–28/12) và `月々十三万八千円` (= 130만원 quy theo
tỉ giá) đổi thành `月々十四万円` — nằm trong dải thật 10–15万 của 特養.

**Luật rút ra, áp cho MỌI cổng dùng LLM sau này:** cổng phải phân biệt *sai* với *chưa hay*, và chỉ
được chặn ở cái sai. Trước khi dựng cổng LLM, hỏi: **"mẫu nào thì cổng này trả về ĐẠT?"** — không
trả lời được câu đó thì đừng nối nó vào luồng chặn.

**Luật thứ hai (anh chốt cùng ngày):** kịch bản trượt cổng thì **sửa tại chỗ trên bản cũ**, cấm xoá
đi chạy lại. Chạy lại sinh chữ mới ⇒ bộ lỗi mới ⇒ không bao giờ hội tụ. Muốn thử một bản vá ở tầng
cổng thì chấm lại kịch bản cũ (`qc_claude.py --script <script cũ>`, ~10 phút) chứ đừng chạy lại cả
pipeline (73 phút) — rẻ hơn 7 lần.

---

## 3. SOI TĨNH TRƯỚC KHI GEN ẢNH (0 đồng — luôn làm)

Trước khi tiêu ~10.000đ tiền ảnh, soi `img_prompts.txt`:

| Kiểm | Vì sao | Đã bắt được thật |
|---|---|---|
| Số ảnh thật | Đếm mọi dòng là SAI — dòng tiêu đề `═══` bị `gen_images` bỏ qua | 162 dòng ≠ 127 ảnh |
| Cảnh trẻ em | gpti2/Azure **chặn 7/7** ảnh trẻ em | 1 cảnh bé gái → gắn `@GROK` |
| Bịa thương hiệu thật | Prompt mơ hồ "notification screenshot" → model bịa **thông báo SoftBank + link lừa đảo** | 4 prompt → thêm "no company logos, no real brand names" |
| Thiếu `no text` | Model vẽ chữ sai vào ảnh | 0/127 (đạt) |
| Prompt trùng | Ảnh lặp = phí tiền + video nhàm | 0 |
| Marker REF-LOCK | Thiếu = mặt đổi từng cảnh | 59/127 có `@REF`/`@REF2` |

⚠️ **Đừng sửa mù.** Nghi gpti2 viết sai chữ Hán → gen thử 6 ảnh (360đ) → **hoá ra viết ĐÚNG hoàn
toàn** (`隆之 新居 / 五百万 家の種銭だ`, tự thêm đúng thuật ngữ sổ sách `摘要`・`収入金額`). Nếu sửa
theo phỏng đoán đã phá mất mấy cảnh đắt giá nhất.

---

## 4. SỐ ĐO THẬT (8 lượt chạy, 2026-09-10 → 11)

### Thời gian phần chữ
| Lượt | Thời gian | Ghi chú |
|---|---|---|
| Trước mọi bản vá | **45,7′** + FAIL | dò luật 11′ · tự cắt 35′ · cạn ngân sách |
| Sau vá prompt (luật + lệnh đo) | 39′ | |
| Sau vá dàn ý + chạy song song master | 35,4′ | (có thêm B3Q — thực chất 28,3′) |
| Bản vá sai kiến trúc (fix_gate đặt sau) | **46,6′** + FAIL | tự viết lại 5 lần |
| **Sau vá phân vai (`fix_gate` trong luồng)** | **B3 xong ở 16,3′** | |

### Phân bổ điển hình
- **Sinh chữ thuần: ~13 phút (34%)** — 8-16k ký tự Nhật + ~34KB prompt ảnh. **Trần cứng**, không nén được.
- Đọc/lập kế hoạch: ~3-6′ · Gen + QC 2 ảnh master: ~7′ · Máy nắn số: 1-5′ · QC nội dung: ~7′

### Chi phí một video 30 phút
- Quota Claude: **$5-6** (là quota gói MAX, **không phải hoá đơn thẻ** — máy này không có `ANTHROPIC_API_KEY`)
- Ảnh: **~10.000-13.000đ** (127-150 ảnh; `@REF` 110đ, thường 50đ)
- Giọng ElevenLabs: ~13.000 credit ≈ **1.500đ**
- Nắn số bằng máy: LLM rẻ, không đáng kể

---

## 5. LUÔN ĐO THỜI GIAN (user chốt)

`render_engine.py` in `⏱ x.x phút` mỗi bước + tổng ở TÓM TẮT. Driver gọi `claude -p` phải in mốc
`+phút` trước mọi dòng:
```python
def log(s): print(f"[{dt.datetime.now():%H:%M:%S} · +{(time.perf_counter()-T0)/60:5.1f}′] {s}")
ok = bc.make_video_one(video, prof, ..., on_line=log)
```
Không có đồng hồ thì **không chẩn đoán được gì** — chính nhờ mốc "+phút" mới phân biệt được "6,7 phút
im lặng = đang sinh 16.000 ký tự (trần cứng)" với "2,2 phút im lặng = đang `sleep` vô ích (cắt ngay)".

---

## 6. LỖI ĐÃ VÁ — ĐỪNG LẶP LẠI

| # | Lỗi | Cách chữa |
|---|---|---|
| 1 | `acceptEdits` làm Claude kẹt xin quyền Bash (chạy nền không ai duyệt) | `bypassPermissions` |
| 2 | QC 70/30 lặp 14+ lượt không hội tụ (chỉ có khẩu hiệu, không có ngưỡng) | Ghi ngưỡng 60-80% + bắt lập bản đồ nhịp trước khi viết |
| 3 | Bắt Claude trúng 4 ngưỡng nó không đo nổi | `gate_check.py` + nhúng lệnh vào prompt |
| 4 | `check_gate()` trả tuple → **luôn truthy → chặn cả kịch bản ĐẠT** | Trả list lỗi. Bài học: verify phải có **ca ĐẠT**, không chỉ ca RỚT |
| 5 | `render_engine` đếm 162 ảnh trong khi `gen_images` sinh 127 → B5 không bao giờ resume được | Đếm bằng chính `gen_images.parse_prompts()` |
| 6 | Chạy sai Python (`python` = uv 3.11 thiếu `imageio_ffmpeg`) | Luôn `py -3.13` |
| 7 | Prompt trỏ `pipeline/profiles/` (thư mục **không tồn tại**) → Glob dò mỗi lượt | `profiles._find()` rồi ghi đường dẫn tuyệt đối |
| 8 | Claude đọc source `ai_steps.py` để dò luật cổng (4-5′/lượt) | Ghi đủ luật + "đây là toàn bộ cổng chặn, đừng dò thêm" |
| 9 | Claude tự `sleep 30` + đọc log phiên khác (2,2′) | Dặn "mọi lệnh chạy ĐỒNG BỘ, cấm sleep" |
| 10 | **`fix_gate.py` đặt SAU khi bộ não xong → không bao giờ được gọi** | Đưa lệnh vào **trong prompt** (NHỊP 3) |
| 11 | `them_nhip` bản đầu thêm quá tay → thủng trần chiều ngược lại | Nhắm **giữa dải**, điều kiện nhận kiểm cả 2 chiều |
| 12 | Để bản nháp cũ trong thư mục tập → bộ não lấy ra sửa dù đã đổi tên | Chuyển hẳn file ra NGOÀI thư mục |
| 13 | Sửa 1 khâu giữa pipeline làm **stale mọi khâu sau** dù file "đã tồn tại" | Xoá cascade xuôi dòng (vd sửa giọng thì xoá `final.mp4`) |
| 14 | **Không có cổng nào ép B3Q** — bộ não tự khai "QC xong" là pipeline tin luôn (kịch bản 14 lỗi vẫn đi tiếp) | `check_b3q()` chạy lại bằng máy, rớt thì bắt sửa rồi CHẶN |
| 15 | Chính sách nội dung của Google trả câu từ chối dưới dạng **nội dung HTTP 200** → chuỗi đổi model dự phòng đứng yên, QC chết câm | Thêm dấu hiệu vào `llm_client.BAD_CONTENT` để tự nhảy model |
| 17 | **Bộ não sửa file profile CỦA KÊNH** cho khớp cốt truyện một tập | `_khoa_profile()` chụp ảnh profile trước mỗi lượt gọi, `_kiem_profile()` khôi phục + cảnh báo nếu bị đổi |
| 16 | Tắt phụ đề cháy làm **B8Q rớt oan** ("khung không thấy chữ") | Thêm cờ `--no-sub` cho `qc_visual.py`, `render_engine` tự truyền theo `assemble.burn_subs` |
| 18 | **Cổng tầng 2 chặn theo TỔNG số lỗi ⇒ không bao giờ mở được** — hỏi LLM "tìm lỗi đi" thì lần nào cũng có, phần lớn là ý kiến văn phong. Đo thật: 16 lỗi → sửa đúng 14 chỗ → **20 lỗi MỚI**; 73 phút + $16 quota rồi FAIL trong khi 3 cổng kia đều ĐẠT | Giám khảo phải khai mức `CHAN` (kiểm chứng được) / `GOPY` (văn phong, kể cả khi nó rất chắc); chỉ `CHAN` mới chặn. Cùng kịch bản: cổng cũ 20 chặn → cổng mới **2 chặn**, sửa 2 nhát là ĐẠT |
| 19 | Rớt cổng thì chỉ cho **1 lượt sửa**, còn lỗi là vứt cả tập báo FAIL | `VONG_SUA_B3Q = 3` lượt **sửa TẠI CHỖ**, và **dừng ngay khi số lỗi chặn không giảm** (không giảm = sửa nữa chỉ đốt lượt) |
| 20 | `qc_tien` **không đọc được số Hàn có 천/백/십** (`4천만 원`, `7천만 원`, `3천 원`) → sót 3/18 số ở vế bản gốc, cổng vẫn báo SẠCH (lỗi câm) | `doc_so_han()` + regex nhận chuỗi nhiều cụm (`1억 5천만 원`); test 18/18. Quét lại toàn dự án: **11 dấu vết còn tồn ở 5 tập cũ** |
| 21 | **Claude (viết hồ sơ giao việc) bảo bỏ `--ep`/`--ten` khi gọi `giao_hang.py`** ("tool tự suy ra") mà KHÔNG kiểm quy ước cũ đang dùng — `so_tap()` chỉ đoán được số tập từ tên thư mục dạng `epNN-...`; lane satori đặt tên `simbot2-NN-<videoID>` (không có "ep") → rơi mặc định `1` → giao hàng sai tên `ep01-...` cho cả tập 11. Hồ sơ CŨ (`GIAO_DEEPSEEK_3TAP.md`) đã truyền tường minh `--ep 06 --ten oita-onna` từ trước, lẽ ra phải soi lại quy ước đang chạy thật trước khi viết spec mới, không giả định tool "tự suy ra" được | LUÔN truyền `--ep {STT}` tường minh trong lệnh gọi `giao_hang.py` — STT đã biết sẵn từ tham số dòng lệnh, không dựa vào tên thư mục để đoán |
| 22 | **Bắt được một lỗi ở 2 file thì phải quét HẾT các file cùng họ, không dừng ở 2/3** — bug glob cứng `ep{stt:02d}-*` (giả định MỌI lane đổi tên thư mục thành `ep<NN>-<slug>`) bắt được ở `ghi_cot_video.thu_muc_tap()` và `quet_dong_can_anh.slug_tu_dia()`, vá xong tưởng hết — bỏ sót đúng cùng giả định đó nằm trong `giao_hang.so_tap()` (file thứ 3, cùng lane, cùng ngày) → phải sửa lại lần nữa ở lỗi #21 | Khi thấy MỘT giả định sai (vd "thư mục nào cũng đặt tên ep<NN>-..."), `grep` toàn bộ `pipeline/*.py` tìm lại đúng giả định đó ở MỌI nơi, không chỉ vá đúng 2 chỗ đã lộ ra qua triệu chứng |
| 23 | **Thumbnail ra 0 CHỮ + mờ toàn khung, câm lặng không báo lỗi** (đo thật ep07/ep11, 2026-09-14) — 2 nguyên nhân độc lập: (a) `thumbnail.art_style` không có trong profile → nhánh viết `thumb_bg_prompt.txt` trong `brain_steps.py` tự tắt (`if art_style else ""`), không ai biết vì không có cảnh báo; (b) `thumb_text.txt` viết dòng trơn không có dấu `\|`, `thumbnail_text.parse_text()` lặng lẽ bỏ qua MỌI dòng thiếu `\|` → 0 chữ được vẽ, `thumbnail_text.py` vẫn thoát mã 0 báo "✓ Thumbnail" bình thường | Thêm `thumbnail.art_style` vào profile; `brain_steps.py` B7 nay ép rõ khuôn `MÀU\|chữ` + bắt buộc marker `@REF ` cho `thumb_bg_prompt.txt`; `render_engine.do_b7()` thêm cổng máy `_kiem_thumb_text()` CHẶN CỨNG trước khi ghép nếu không có dòng nào đúng khuôn — im lặng ra sản phẩm hỏng nguy hiểm hơn dừng hẳn |

---

## 7. LIÊN QUAN
- `docs/SOP_SATORI_JP.md` — runbook ngách satori (nội dung/thumbnail/đăng tải)
- Skill global `claude_headless_agent_tool.md` — **kỹ thuật chung, mang sang dự án khác được**
- Memory: `hai-tool-exe-tach-han` · `audit-render-engine-vs-make-video` ·
  `bao-cao-test-phai-kem-thoi-gian` · `may-dung-oauth-max-khong-phai-api-key`
