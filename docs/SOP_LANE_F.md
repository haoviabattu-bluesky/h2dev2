# SOP — LANE F: 定年後のリアル (hưu trí/tiền Nhật, manga story ngôi 1「俺」kịch tính tiền)

> Kênh mẫu: 老後の暮らし研究所 (https://www.youtube.com/channel/UCRkP44Mcw-K8IktdTqxC9dg).
> Kênh của mình: **定年後のリアル** `@teinengo-real` · `UCIimxP275YufOXXIlu9y9Lg` (profile
> `teinengo-real`, mail dòng 7 sheet GMAIL — VirgiliTraino95@gmail.com, GPMLogin cùng tên).
> Cửa vào lane: `docs/BAT_DAU_LANE/teinengo-real.md` (đọc trước, file này là chi tiết vận hành).
> Viết 2026-09-20 (giai đoạn 2), theo khuôn `SOP_LANE_E.md`.

| Anh nói | Profile | SOP |
|---|---|---|
| "video satori / người già / Nhật kể chuyện đời" | `satori-jp-obaa` | `SOP_SATORI_JP.md` |
| "sức khoẻ người già / Lane E / 健康の知恵袋" | `kenko-chiebukuro` | `SOP_LANE_E.md` |
| "hưu trí Nhật / manga kịch tính tiền / Lane F / 定年後のリアル" | **`teinengo-real`** | **file này** |
| "hưu trí Nhật / manga list N選 vui-rẻ / Lane G / 定年後の楽しみ方" | `teinengo-tanoshimi` | `BAT_DAU_LANE/teinengo-tanoshimi.md` |

Nguồn nghiên cứu (2 tầng, cả 2 đã có sẵn trên máy 1):
```
FlowHandoff_local/results/laneF_from_research/        ← TRENDING-RESEARCH bàn giao, anh duyệt 2026-09-13
├── LANE_F_HANDOFF.md                                  ← đọc trước (14 mục: công thức thắng §9, title §4, hook §5,
│                                                         7 chặng §6, anti-pattern §10, tên/tag §12, đề tài tập 1 §13)
├── channel_analysis_老後の暮らし研究所.json              ← Channel DNA dạng JSON (schema chuẩn)
├── report_2lanes.html                                 ← báo cáo duyệt (Lane F = phần "ĐÁNG LÀM")
└── data/transcripts_LaneF.json                        ← transcript THẬT 3 video (2 story + 1 list), có timestamp
docs/channel_dna/rougonokurashi/                       ← Channel Analyzer K1+K2 (8 video top view, 2026-09-16)
├── CHANNEL_DNA.md · TAG_STATS.json · VIDEO_ANALYSIS/*.json · _raw/transcripts.json
```
⚠️ Chỉ 3/12 video có transcript thật ở tầng 1; tầng 2 có 8 bản phân tích + transcript thô. Trong 3
transcript thật, **`K8tTrxijqEo` (…6選) là dạng LIST — nhịp của Lane G**, không dùng để đo gate hay
làm `competitor.txt` cho Lane F.

---

## 0. BẢNG DELTA — khác các lane kia chỗ nào

| Khâu | Satori | Lane E | **Lane F** |
|---|---|---|---|
| Người kể | Cụ già ngôi 1 私, tâm tình | Bác sĩ ngôi 2, giải thích | **Nam 60–67 ngôi 1「俺」, hồi ức, だ・である体, KHÔNG kính ngữ** |
| Giọng | ElevenLabs Ado @0.92 · 270 chữ/ph | MiniMax Dependable Woman @0.88 · 321 chữ/ph | **`clone_2658911`** (clone giọng kênh mẫu, video 294k view) @**0.95** · **284,0 chữ/ph** (đo 2026-09-20) — xem §0c |
| Cấu trúc | 悟り 3 tầng kết | List đếm ngược 5 mục | **7 chặng story** (`script.structure_block` khai trong profile — hook so sánh số phận → trăng mật + số khởi điểm → cú tát phong bì + tiền tụt theo mốc → nhân vật thứ 2 → ngoặt → payoff thực tế → kết triết lý + câu hỏi 2–3 ngã rẽ) |
| Chế độ script | fiction (đổi tên/nghề tự do) | documentary (số liệu từ tư liệu) | **`fiction_facts`** (MỚI 2026-09-20): nhân vật hư cấu NHƯNG số CHẾ ĐỘ phải có trong `series_ctx.txt` → **B3F CHẠY** |
| Thời lượng | 30' | 20' | **22' = 6.248 chữ** (kênh mẫu hit 23,7–24,2'; handoff 16–24') |
| Nhân vật lặp | CÓ (REF-LOCK 1) | KHÔNG | **CÓ, 2 nhân vật TRONG TẬP** (@REF = 俺, @REF2 = người đối lập), KHÔNG xuyên tập |
| Thân video | Ảnh AI thật | Tranh vẽ tay ấm | **Manga seinen** (nét mực rõ, cel-shading màu trầm), `ima2` 0đ, 8 luồng |
| Thumbnail | Chân dung REF-LOCK + banner đỏ | Nền đen + chữ 4 tầng + ảnh đồ ăn | **Chân dung GẦN THẬT kịch tính (khác thân video manga — cố ý) + nền tối + chữ vàng/đỏ/trắng 3 tầng**, `require_face=true` |
| Rủi ro | — | Y khoa | **Số chế độ sai** (khán giả 60+ biết rõ chế độ của họ) + **giọng bán hàng/thuyết giáo** + **nhầm sang Lane G** (lối sống vui) |

---

## 0b. CHANNEL ANALYZER — ĐÃ CHẠY (K1+K2 8 video, 2026-09-16; copy về `docs/channel_dna/rougonokurashi/` 2026-09-20)

K3 chạy tại chỗ, không cần mạng/API key:
```bash
cd E:\CLAUDE\YOUTUBE\h2dev
py -3.13 -X utf8 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\rougonokurashi --topic "<đề tài tiếng Nhật>" --top-n 3
```
Verify 2026-09-20 với đề tài tập 1 → top 3: `dY3HfjtmvXI` / `K8tTrxijqEo` / `O84L0zOtrxo`. **Lọc tay
sau K3**: bỏ `K8tTrxijqEo` (list), ưu tiên video CÙNG DẠNG STORY và CÙNG TRỤ CỘT. Transcript thô của
8 video ở `_raw/transcripts.json`; 2 transcript có timestamp ở tầng 1 (`XbwqD2SktC0`, `O84L0zOtrxo`).

**5 trụ cột CHANNEL_DNA** (dàn 10 tập theo đây): #1 thời điểm nghỉ/nhận lương hưu · #2 chi phí ẩn &
bẫy thủ tục (税/保険/修繕積立金) · #3 sĩ diện cựu quản lý · #4 độc thân & nhà ở · #5 tái thiết, làm
nhẹ để kết nối. **6 giai đoạn story** của DNA (trăng mật → cú tát phong bì → vùng vẫy → nhân vật
phản chiếu → tái thiết → chiêm nghiệm) đã gộp vào 7 chặng của `structure_block`.

## 0c. K4 — GIỌNG KÊNH MẪU + CLONE (2026-09-20, đo thật, KHÔNG đoán theo văn phong)

`pipeline/voice_fingerprint.py` trên 6 video (`assets/teinengo-real/_voice/k4/voice_fingerprint_report.json`):

| video | view | F0 trung vị | cụm MFCC |
|---|--:|--:|---|
| XbwqD2SktC0 (60 vs 65) | 294.900 | 109,2 Hz | A |
| O84L0zOtrxo (67万円) | 165.066 | 127,0 Hz | A |
| _VXUim2J9QM (62歳最強) | 91.245 | 97,0 Hz | A |
| K8tTrxijqEo (6選 list) | 136.317 | 145,5 Hz | B |
| WblFD81yjOI (70歳繰り下げ) | — | 120,3 Hz | B |
| e_Zo7Ht5OH8 (元部長1700万) | — | 127,0 Hz | B |

Toàn bộ **nam** (97–145 Hz). Cosine trong cụm A 0,95–0,97, trong cụm B 0,98–0,997, giữa A–B 0,85–0,92
→ kênh mẫu dùng **≥2 giọng nam**, cụm A là của 2 video story hit nhất. **Clone từ cụm A**:
- Nguồn: `XbwqD2SktC0` đoạn 0:40–1:06 (26 s, narration thuần, sau intro) →
  `assets/teinengo-real/_voice/clip_XbwqD2SktC0_40s.mp3`.
- `POST /v3/text-to-speech/voice-clone` (`remove_background=true`) → **`voice_id=2658911`** → profile
  `voice.id = clone_2658911`. Cost: 333 credit clone + ~160 credit test/calib.
- **Xác minh output** (luật skill §6b): TTS câu test 128 chữ → F0 output **107,4 Hz** vs nguồn
  **104,6 Hz** → khớp, nam → `narrator.gender="male"` là số đo, không phải cảm nhận.
- `calibrate.py --style story` → **284,0 chữ/phút @0.95** (mẫu 230 chữ / 48,6 s). Kênh mẫu đọc
  265–269 chữ/phút — nếu anh muốn sát hơn thì hạ `speed` 0.92 rồi **đo lại** (đổi speed = đổi char_rate).
- Nghe A/B: `assets/teinengo-real/_voice/compare.html` (serve `py -3.13 -m http.server 8765` trong
  thư mục đó). **Anh DUYỆT giữ voice_id 2026-09-20.** Ghi chú của anh: video gốc nào giọng NỮ thì tính sau
  (clone riêng nhóm đó khi tới tập, không dùng giọng này đọc thay).

---

## 1. QUYẾT ĐỊNH ĐÃ CHỐT (2026-09-20)

- `body.mode = "ai_images"`, manga seinen (không chibi, không watercolor như Lane E), ảnh qua **ima2**
  (GPT OAuth, 0đ) — fallback `gpti2_edit.py` khi bị siết quota; KHÔNG giao máy 2 vẽ ở tập 1 (giống
  Lane E §5b: máy 1 tự vẽ bước 2).
- **REF-LOCK 2 nhân vật trong tập** (`image.ref_lock=true`): `characters.json` mỗi tập khai `@REF`
  (俺: tuổi/nghề/ngoại hình) + `@REF2` (người đối lập). Kênh RỜI RẠC → tập sau người khác, không mượn
  master của tập trước. Cách làm REF-LOCK: `docs/SOP_SATORI_JP.md` §B5.0.
- `script.engine = "claude_p"` (Claude viết PASS 0+1; Gemini nén/phẩy; B3Q/B3F Gemini; B3S sol).
- `script.mode = "fiction_facts"` → **mỗi tập BẮT BUỘC có `series_ctx.txt`** (số liệu chế độ hưu trí
  Nhật CÓ NGUỒN: 年金 theo tuổi, % 繰上げ/繰下げ, 住民税/国保 năm đầu, 高年齢求職者給付金, 再雇用
  lương giảm, 遺族年金…). Thiếu file → B3F dừng (đúng thiết kế). Số CÁ NHÂN nhân vật (退職金/貯金) tự
  đặt nhưng nhất quán từ đầu đến cuối.
- Không có `research` trong profile (không qua cổng B0/`qc_hoso.py` của SPACE_RESEARCH) — tư liệu
  chế độ do lane tự tra (WebSearch, nguồn 日本年金機構/厚労省/自治体) và ghi nguồn cạnh từng số.
- `assemble.zoom = 1.0` (khán giả 60+, tắt Ken Burns như Lane E). Chuyển cảnh theo công thức đo
  (skill `video-chuyen-canh`) là việc bước 3.

## 1b. DANH SÁCH 10 TẬP + QUY TẮC TRANG TÍNH `teinengo-real`

### Cột A→K (header thật đã tạo 2026-09-20)
A=STT · B=NỘI DUNG · C=FOLDER · D=KỊCH BẢN · E=TITLE-DESCRIPTION · F=TAGS · G=THUMBNAIL ·
H=STATUS-IMG · I=VIDEO · J=LIST · K=GHI CHÚ — **cách ghi y hệt Lane E §1b** (đọc bảng bên đó, không chép
lại đây): C chỉ điền khi thư mục tồn tại; **D = `done`** khi B3/B3Q/B3F/B3S/B4/B4Q/B5W/B5P đều đạt
(kịch bản QC + giọng QC + prompt ảnh); E/F/G tạm chưa làm trừ khi có lệnh; **H = 1 ô 2 dòng**
`Xong nội dung - cần ảnh` + `E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs\<slug>\` (**KHÔNG có `h2dev\`**);
I chỉ khi B11 giao xong; K = trạng thái từng cổng.

### 10 tập đầu (STT = ưu tiên dự kiến; dàn đều 5 trụ cột; KHÔNG trùng tựa hit kênh mẫu)
| STT | Trụ cột | Tựa làm việc (tiếng Nhật, đã đo ≤44 ký tự) | Góc mới so với kênh mẫu | Slug |
|---|---|---|---|---|
| 1 | #1 | 【漫画】60歳で退職した妻と俺…5年後、夫婦の年金に月8万円の差が出た理由 (37) | VỢ CHỒNG — kênh mẫu toàn 俺 đơn độc (handoff §13) | `ep01-fuufu-nenkin-sa` |
| 2 | #3 | 【漫画】61歳で再雇用を選んだ俺…給料が半分になった1年後、元部下に見た残酷な現実 (41) | 再雇用 nhìn từ người CHẤP NHẬN (kênh mẫu: người từ chối) | `ep02-saikoyou-hanbun` |
| 3 | #1 | 【漫画】63歳で年金を繰り上げた男…月2万円減った先に待っていた本当の後悔 (37) | 繰上げ (kênh mẫu chỉ làm 繰下げ 70 & 62) | `ep03-kuriage-koukai` |
| 4 | #2 | 【漫画】65歳で退職した俺…翌年届いた住民税と保険料の封筒で貯金が98万円消えた (40) | Thuế năm đầu kể thành STORY có số (bản kênh mẫu MISS vì tựa khô) | `ep04-juuminzei-futou` |
| 5 | #4 | 【漫画】62歳で妻を亡くした男…遺族年金の現実を知った日、初めて通帳を開いた (38) | 遺族年金 — chưa ai khai thác | `ep05-izoku-nenkin` |
| 6 | #2 | 【漫画】64歳、築35年のマンション…修繕積立金が月3万円になった日、家を手放した (41) | 修繕積立金 làm trục chính (kênh mẫu chỉ nhắc phụ) | `ep06-shuuzen-tsumitate` |
| 7 | #4 | 【漫画】66歳、独身、貯金1200万円…退職して3年、誰とも話さなくなった理由 (39) | Cô đơn = chi phí ẩn (khác 「2か月で絶望」 của kênh mẫu) | `ep07-kodoku-kaiwa` |
| 8 | #3 | 【漫画】60歳で辞めた元課長…息子夫婦への援助で退職金1500万円が3年で消えた (40) | Tiền chảy sang con cái — sĩ diện với gia đình | `ep08-kodomo-enjo` |
| 9 | #5 | 【漫画】65歳で年金生活を始めた俺…週3日の駐車場の仕事が人生を変えた理由 (37) | Payoff tái thiết làm TRỤC (kênh mẫu chỉ để ở kết) | `ep09-shuu3-shigoto` |
| 10 | #1/#3 | 【漫画】59歳で早期退職した男…割増退職金2000万円で勝ったと思った2年後の現実 (41) | 早期退職 割増 — chưa có | `ep10-souki-taishoku` |

Nguyên tắc: mỗi tựa = nhân vật + tuổi + SỐ TIỀN + cảm xúc (luật cứng §3 handoff); tựa cuối do B7
viết lại theo gate `title_len` [26,44] — tựa trên là ĐỀ TÀI, không phải tựa đăng. **Chỉ tập anh chỉ
định mới bắt đầu** (memory `chi-chay-dong-duoc-chi-dinh`). Lane F ≠ Lane G: tập nào ngả sang "lối
sống vui/rẻ N選" là của G, đừng viết ở đây.

⚠️ Hook 20–30s bắt buộc trước S2 — xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.

## 2. LỆNH CHẠY (tập đầu tiên)

```bash
cd E:\CLAUDE\YOUTUBE\h2dev
mkdir assets\teinengo-real\ep01-fuufu-nenkin-sa
# hồ sơ đề tài (bước 1, Claude tự soạn):
#   competitor.txt  = 1 transcript story cùng trụ cột (K3 → lọc tay; tập 1 gợi ý XbwqD2SktC0 — cùng dạng "so sánh 2 số phận")
#   series_ctx.txt  = số liệu chế độ CÓ NGUỒN (tập 1: 厚生年金 vợ/chồng theo năm đóng, 第3号被保険者, 加給年金, 振替加算, 繰上げ減額率 0,4%/月…)
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug ep01-fuufu-nenkin-sa
```
Chạy tới HẾT bước 1 rồi **DỪNG**: B3 + gate → B3Q/B3F/B3S → B4 + B4Q → B5W + B5P → `characters.json`
+ master REF-LOCK @REF/@REF2 → `TIEU_DE_MO_TA.txt` + `thumb_text.txt` (bước 1 PHẢI để lại, bước
2/3 không tự sinh). KHÔNG `drive_handoff.py upload-job` lần đầu nếu anh chưa nói "giao sang máy 2".

## 2b. ⭐ PHẠM VI HIỆN TẠI (anh chốt 2026-09-20): CHỈ TỚI KỊCH BẢN + QC — ai làm gì, máy nào, QC ra sao

Mốc dừng = **B3R đạt** (`make_video.py --den B3R`). KHÔNG chạy B4 giọng, B5W prompt ảnh, B7 thumbnail,
tiêu đề/mô tả/tags, sinh ảnh, video — cho tới khi anh mở rộng. Cột D sheet ghi `script-qc-done` (chưa
phải `done`, vì `done` = kịch bản + giọng + prompt ảnh).

| # | Bước | Ai / máy / model | Việc cụ thể | QC / cổng |
|---|---|---|---|---|
| 0 | Chọn tập | **Anh** | "cho làm tập X" (theo STT tab sheet) | — |
| 1 | Hồ sơ đề tài | **Claude Code (tab này, Opus)** | Tạo `assets/teinengo-real/ep<NN>-<slug>/`; `competitor.txt` = 1 transcript STORY cùng trụ cột (K3 `retrieve_videos.py` → lọc tay, bỏ bài list); `series_ctx.txt` = số chế độ CÓ NGUỒN (WebSearch 日本年金機構/厚労省/自治体, ghi URL cạnh từng số); ghi cột C | Tự kiểm: mỗi số trong `series_ctx.txt` có nguồn; không có số nào "nhớ mang máng" |
| 2 | B3 PASS 0 — bóc khung | **Claude `claude -p` FABLE 5.1** (`script.brain_model=claude-fable-5-1`, quota OAuth MAX, 0đ; anh chốt 2026-09-20) qua `claude_p_bridge.py` | Bóc `beats` từ competitor.txt (nhịp sự kiện, KHÔNG chép tên/thoại) | Claude tab này soi `beats` bằng mắt: lọt tên/thoại gốc → sửa |
| 3 | B3 PASS 1 — viết nháp | **Claude `claude -p` FABLE 5.1** | Viết dài hơn mục tiêu theo `structure_block` 7 chặng + `fiction_facts` + persona 俺; số chế độ lấy từ `series_ctx.txt` | — |
| 4 | B3 PASS 2 — nén + nhịp | **Gemini 3.8 Flash (ramclouds, fallback ns24)** — máy 1 | Nén về 6.248 chữ (22' × 284), chèn 、 đúng nhịp; `fix_gate.py` nắn cơ học | **gate_check.py** (máy đo, 0đ): chữ ±12%, 0,6–2,0 phẩy/câu, 6–12 chữ/nhịp, hội thoại ≤20%, không marker/Hàn/Latin |
| 5 | B3Q — nhất quán | **Gemini 3.8 Flash** (`qc_script.py`) | Mâu thuẫn nội bộ (貯金 lệch giữa các chặng, tuổi/năm sai, lặp câu), tự sửa (`fix`) tối đa `--tries 2` | Verdict ĐẠT / HỎNG; HỎNG sau 2 lượt → dừng, Claude tab này **sửa TẠI CHỖ** (memory `sua-tai-cho-khong-viet-lai`) |
| 6 | B3F — đúng nguồn | **Gemini 3.8 Flash** (`qc_facts.py`) — CHẠY vì `mode=fiction_facts` | Hỏi "số chế độ này ở ĐÂU ra" đối chiếu `series_ctx.txt`; số cá nhân nhân vật không bị soi | Lỗi dữ kiện → **DỪNG HẲN**, không nối vào vòng viết lại (memory `b3f-khong-duoc-noi-vao-vong-viet-lai`); Claude sửa số hoặc bổ sung nguồn |
| 7 | B3S — QC độc lập khác hãng | **GPT-5.6-sol** (9router local `localhost:20128`, `qc_script_sol.py`) | Chấm luận đề/hook/giọng (bán hàng? thuyết giáo? có 俺 hồi ức không?), số liệu hợp lý, hook ≥450 chữ có neo số | PASS/FIX → qua; REMAKE → Claude sửa nhẹ theo 4 chiến lược (`docs/QC_SCRIPT_GPT_SOL.md`), rồi **chạy lại B3Q** (memory `dau-phay-cat-cum-va-b3q-hoi-quy`) |
| 7b | **B3R** — nghiệm thu cuối | **FABLE 5.1** (`script.final_review_model`, tiêu chí riêng lane ở `script.final_review_criteria` — 8 mục: 7 chặng, số chế độ có nguồn + số cá nhân nhất quán, mật độ số, giọng 俺, không trượt Lane G/tư vấn, kết không phép màu, an toàn, TTS đọc được) | Đọc như biên tập viên bản cuối → JSON verdict + issues → `qc_final_review.txt`; FIX → Fable sửa tại chỗ 1 lần rồi chấm lại; test khô 2026-09-20: stub 270 chữ bị REMAKE đúng lý do, 69 s | PASS/FIX qua; REMAKE → dừng, em đọc báo cáo rồi báo anh. Cùng họ với model viết nên KHÔNG thay B3Q/B3F/B3S |
| 8 | Nghiệm thu | **Em** (đọc `qc_final_review.txt` + script) rồi **Anh** | Đọc lại `script.txt` toàn bài theo §4 luật cứng (cú tát vật lý? nhân vật phản chiếu có tên+tuổi+số? kết điểm rơi trung gian + câu hỏi 2–3 ngã rẽ?); ghi cột D `script-qc-done`, cột K trạng thái từng cổng; báo anh đường dẫn | Anh đọc: em tự dịch tóm tắt tiếng Việt từng chặng vào `script_tomtat_vi.txt` (Claude tab này viết, không qua model khác) để anh duyệt nhanh; `review_vi` của profile là bản xem thử VIDEO, thuộc bước 3, ngoài phạm vi |

Lệnh:
```bash
cd E:\CLAUDE\YOUTUBE\h2dev
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug ep<NN>-<slug> --den B3G
# (từ tập 2, 2026-09-20: `script.flow="lean"` → 1 lệnh chạy S1Q→S2 Fable→S3 máy→S5 Sol plain→patch ≤2→LOCK; xem
#  docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md. Hồ sơ tập cần thêm `title.txt` (1 dòng, 26–44 ký tự) và dòng
#  `SỐ ĐƯỢC PHÉP:` trong series_ctx.txt liệt kê số CHẾ ĐỘ được dùng (%, 歩, 年間…; tiền 万円/円 được miễn).
#  Xong: cột D ghi `Done` sau khi em đọc bản khoá (lớp 3). ep01 làm bằng luồng cũ --den B3R.)
```
Chi phí/tập tới mốc này: Fable PASS 0+1 + B3R = quota OAuth (0đ hoá đơn; CLI `claude` cập nhật 2.1.278 ngày 2026-09-20 vì Fable cần ≥2.1.251 — dùng chung mọi lane, smoke-test opus/fable đều OK); Gemini PASS 2 + B3Q + B3F ≈ vài
trăm đồng (ramclouds); B3S ≈ 0đ (9router). Chưa tốn credit ai33 (B4 chưa chạy).

Sau mốc này, khi anh mở rộng: **B4 giọng** (ai33 `clone_2658911`, ~8.000 credit/tập ≈ 1.000đ) + **B4Q**
nghe máy (`qc_audio.py`) → **B5W** prompt ảnh + `characters.json` 2 nhân vật + **B5P** WARN → master
REF-LOCK (ima2) → cột D `done`. Rồi mới tới tiêu đề/mô tả/thumbnail/ảnh/video (chưa bật).

### 2c. BÀI HỌC TẬP 1 (test 2026-09-20, 5 lượt chạy, ~50 phút, 0đ ngoài vài trăm đồng Gemini)
1. **B3S phải khai `script_qc.lens="story"` + `domain_focus` trong profile** — thiếu là GPT-sol chấm bằng lens y khoa
   mặc định (đòi list N mục/bác sĩ/gọi 119) → REMAKE sai cổng (memory `moi-model-cung-truot-la-loi-cong`). Đã khai.
2. **Năm sinh nhân vật quyết định 2 luật**: nam sinh ≤昭和36/4/1 có 特別支給; sinh ≤昭和37/4/1 → 繰上げ 0,5%/tháng
   (không phải 0,4%). Chọn năm sinh TRƯỚC khi viết số 繰上げ; ghi vào `series_ctx.txt` (C1b/C3b).
3. **Lượt sửa headless của B3S (Fable) làm kịch bản PHÌNH +150–300 chữ mỗi lần** và tự đổi số lẻ (652→630 theo mốc)
   → sau B3S luôn chạy lại `gate_check.py`; vượt +12% thì Claude cắt câu dư tại chỗ, đừng để Fable sửa thêm lượt nữa.
4. B3Q Gemini có thể "bắt sai" số chế độ bằng kiến thức cũ của nó (đòi 68.000/408.100 = mức 令和6) trong khi
   `series_ctx` có nguồn 令和7 — tin B3F (đối chiếu nguồn), không tin trí nhớ Gemini; 2 lỗi "thấp" này bỏ qua được.
5. **Câu hỏi kết + câu biểu tượng của kênh mẫu (「自由は無料ではない」「皆さんなら60歳で自由を取りますか…」) bị
   Fable chép gần nguyên văn** vì chính `structure_block` dẫn ví dụ đó → đã sửa structure_block thành "tự đặt lời,
   không chép"; B3Q lượt cuối bắt được "nghi sao chép" → viết lại 2 câu.
6. Số ĐẠT thật tập 1: 6.995 chữ / 24,6' · 0,92 phẩy/câu · 9,7 chữ/nhịp · hội thoại 9% · 70/30 bám gốc 73–75%.
7. **B3S = hỏi thẳng, không lăng kính (anh chốt 2026-09-20)**: `script_qc.lens="plain"` — prompt chỉ hỏi "kịch bản này
   đã hợp lý chưa, điểm nào không hợp lý liệt kê để sửa"; `domain_focus` chỉ 2 câu bối cảnh (thể loại, ngôi kể).
   Kết quả ĐO THẬT tốt hơn hẳn 2 lens cũ: bắt được tựa sai bản chất (8万 là THU NHẬP tháng chứ không phải 年金),
   dòng tiền sau 2024 không cộng khớp, so sánh không đồng nhất (手取り vs 年金). Lens medical/story vẫn giữ cho E/satori.
8. **`script.sol_fix_headless=false`** cho lane này: lượt Fable sửa mù theo báo cáo sol chèn dữ kiện MỚI sai
   (điều kiện 扶養 lệch mốc, "thuế trả thừa") + phình chữ → sol lượt sau bắt đúng câu vừa chèn. B3S chỉ báo cáo,
   Claude tab đọc rồi sửa tay, chạy lại từ B3Q. Sol KHÔNG hội tụ về PASS (mỗi vòng ra 3–5 điểm nhẹ dần) → dừng
   khi các điểm còn lại là "chưa hay"/đại lượng trước-sau khấu trừ, không phải lỗi logic.

### 2d. BENCHMARK LEAN TẬP 2 (2026-09-20, `bench.jsonl` ep02-saikoyou-hanbun) — lane truyện chạy được
| Lượt | Kết quả | Fable | Sol | Thời gian | Nguyên nhân |
|---|---|---|---|---|---|
| 1 | ESCALATE | 4 | 2 | 13' | Fable đi theo khung video mẫu (元部長 TỪ CHỐI) → viết 俺 từ chối, ngược tựa; Sol bắt ngay "lời hứa tiêu đề". S2 viết thiếu −22% (4.855) phải nới |
| 2 (force) | ESCALATE | 4 | 2 | 15' | Đúng tiền đề sau khi ghim「TIỀN ĐỀ BẮT BUỘC」đầu series_ctx; S2 viết đúng ngân sách (−4,6%); Sol soi dòng tiền (10万 dư không cộng, "thu nhập = 0", ngoại suy 1.400万) |
| 3 (viec_tay 8 việc) | **PASS** | 2 | 2 | 5'49 | patch → S3 → Sol lần 2 PASS |
| 4 (lớp 3, viec_tay 2 việc bám gốc) | **PASS** | 2 | 2 | 5'43 | khoá sha 143aaca37b, 6.533 chữ (+4,6%) |
Bài học: (1) **tiền đề tập phải nằm NGAY ĐẦU `series_ctx.txt`** dưới nhãn「TIỀN ĐỀ BẮT BUỘC」, đặc biệt khi góc mới ĐẢO VAI so với
video mẫu — beats của competitor đứng cuối prompt và rất mạnh; (2) `title.txt` là tựa LÀM VIỆC, Sol dùng để kiểm lời hứa — sửa tựa
theo truyện khi Sol đúng (61→60); (3) Sol plain soi cộng trừ tiền nghiêm — đây là điểm mạnh, viết `viec_tay` càng cụ thể (trích câu + câu thay) thì
1 vòng là PASS; (4) lớp 3 vẫn cần: 2 câu bám kênh mẫu (hook「思っていたより残酷」,「じいじ、また来てね」) máy chỉ WARN bigram, Sol không biết.
Tổng: 12 lượt Fable · 8 lượt Sol · ~40' máy · 0đ — so với ep01 luồng cũ: 8 lượt QC + 5 vòng sửa tay ~50' người.

**ep03 (cùng ngày, `ep03-kuriage-koukai`)**: lượt 1 ESCALATE (Sol: 19万 額面 vs 手取り; "quay lại nhà máy" không có cơ sở; vợ 蒲生 chưa nhận 年金) →
viec_tay 6 việc → còn 2 (赤字 10万, bỏ「はんこ」vì đơn 年金 nay không cần dấu) → PASS lần 1 → lớp 3 sửa 1 lặp ý + 2 câu bám mẫu → PASS lần 1.
Tổng 8 Fable · 5 Sol · ~25' máy. **Quy luật sau 2 tập**: lần chạy đầu luôn ESCALATE ở dòng tiền (Sol soi 額面/手取り, nhịp trả 2 tháng, số cộng
lệch) → viết `viec_tay` trích câu + câu thay → vòng sau PASS ngay; lớp 3 luôn phải soi câu bám kênh mẫu (hook「思っていたより残酷/静か」,
「袋お願いします」,「じいじ」) — máy chỉ WARN, Sol không biết. Ghi sẵn vào profile `script_qc.lane_rules` dòng "額面 vs 手取り phải nói rõ, 年金 trả 2 tháng/lần".

## 3. GATE — ngưỡng đã đo/hiệu chỉnh (chi tiết trong `profile.script.gate._gate_note`)

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| title_len | 26–44 | ĐO THẬT 8 tiêu đề VIDEO_ANALYSIS (27–41 kể cả【漫画】) |
| hook_chars (120 s đầu) | 450–700 | ĐO THẬT 2 transcript story (505–526). ⚠️ `qc_script.mo_dau()` chỉ đo khi có marker 第1章 — lane này không có chương → số này là tham chiếu cho B3S/người đọc, chưa phải cổng máy |
| chars/câu (tham chiếu) | 16,5–18,8 trung bình, median 15–17 | ĐO THẬT — câu RẤT NGẮN, khác hẳn Lane E |
| comma_per_sentence | 0,6–2,0 | HIỆU CHỈNH (ASR 0,15/câu không tin được; câu ~17 chữ) |
| chars_per_breath | 6–12 | HIỆU CHỈNH từ 2 số trên (cue STT trung bình 17,8 chữ ≈ 1 câu = 1 nhịp) |
| dialogue_ratio_max | 20% | ƯỚC LƯỢNG (ASR không có「」; đối thoại ngắn với nhân vật 2 ~10–15%) |
| neo số/1.000 chữ | 8–13 | ĐO THẬT toàn bài (không có cổng máy, ghi trong `structure_block`) |
| require_next_ep_teaser | false | Video độc lập |

⚠️ 3 chỉ số HIỆU CHỈNH/ƯỚC LƯỢNG phải đo lại bằng B3Q sau kịch bản đầu tiên rồi sửa profile.

## 4. LUẬT CỨNG RIÊNG LANE (handoff §3/§10 + DNA "Rules")
- Nhân vật chính nam 59–69, nghề bình thường, có khoản tiền "trông an toàn" (800–2.500万) + niềm tin ngây thơ.
- Phải có **cú tát vật lý** (phong bì/thông báo/cơn chóng mặt) và **nhân vật phản chiếu** có tên+tuổi+số.
- Kết = **điểm rơi trung gian** (việc nhẹ 週2–3日 5–6万, cắt sĩ diện, hội đoàn) — cấm trúng số/việc lương cao.
- Kết bằng câu hỏi 2–3 ngã rẽ + 「是非コメントで聞かせてください」; xin đăng ký 1 câu, không ép.
- Giọng nam tự nhiên, KHÔNG bán hàng/thuyết giáo; số chế độ có nguồn; nhân vật hư cấu không gắn tên thật.
- KHÔNG nội dung nhạy cảm kiểu なるほど雑学; KHÔNG viết chéo sang Lane G.

## 5. PUBLISH
`publish.upload_channel = teinengo-real` (thư mục `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real\ep<NN>-<slug>\`),
`publish.sheet_tab = teinengo-real`. Hashtag/tag seed trong profile `publish` (từ `branding/KENH.json`
+ `TAG_STATS.json`: 老後 · 年金 · お金 lặp 8/8 video kênh mẫu). Category People & Blogs, 2–3 video/tuần.

## 5b. PHÂN VAI (cập nhật 2026-09-21, thay bản cũ nói "ima2" — đã bỏ ima2, xem `docs/PHUONG_AN_LANE_F_BUOC2_3.md`)
Máy 1 (Claude Code) làm tới `characters.json` + B5W (Fable/Opus 5 viết prompt theo đoạn) + B5P (WARN) rồi
đóng gói qua `pipeline/dong_goi_may2.py --job teinengo-real <slug>` → **MÁY 2** vẽ ảnh (gpti2, cổng B5S
5 ảnh mẫu trước khi vẽ cả loạt) + ghép video (chữ DỌC 縦書き overlay, `tate_text.py`, KHÔNG phải phụ đề
ngang) khi anh đã chốt giọng. Chi tiết đầy đủ + 5 quyết định Q1–Q5 (kiểu vẽ theo kênh mẫu · 縦書き ·
10s/ảnh · ep đầu 2 chặng có người xem · master vẽ ở máy 2): `docs/PHUONG_AN_LANE_F_BUOC2_3.md`. Việc máy
2: `FlowHandoff_local/shared/GIAO_VIEC_MAY2_LANE_F.md`.

## 6. CÒN TREO (nói thẳng)
- Voice clone anh đã duyệt 2026-09-20. Chưa có TEMPLATE.md/MASTER_REFERENCE thumbnail — chốt sau tập 1 (thumbnail hiện NGOÀI phạm vi §2b).
- `hook_chars` chưa là cổng máy cho lane không chương (cần thêm `hook_marker` tuỳ chọn vào
  `qc_script.mo_dau` nếu muốn — chưa làm, tránh sửa cổng dùng chung khi chưa có tập nào).
- Danh sách 10 tập đã ghi tab sheet A2:B11 (2026-09-20).

## HOOK 20–30 GIÂY ĐẦU — CÁCH CỦA RIÊNG LANE NÀY

> ⚠️ Mỗi lane một kiểu hook khác nhau. **Đừng mượn cách của lane khác.**

| | |
|---|---|
| Kiểu mở (`script.hook.patterns`) | H23 H35 |
| Câu khoá (`script.hook.closer`) | K19 |
| Cách dựng hình (`script.hook.visual`) | `manga_ai_ref` |
| Nguồn hình | manga AI, REF-LOCK cùng bộ nhân vật với thân video |
| Công tắc (`script.hook.enabled`) | đang TẮT |

Runbook dựng đầy đủ (7 bước + 4 phép kiểm trước khi ghép): `docs\QUY_TAC_VIDEO_HOOK.md`, bảng so sánh
cách dựng của mọi lane ở §5b. Nguyên tắc nội dung hook: `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

Viết hook: `py -3.13 pipeline\hook_stage.py --profile teinengo-real --slug <tập> --mode repair`
