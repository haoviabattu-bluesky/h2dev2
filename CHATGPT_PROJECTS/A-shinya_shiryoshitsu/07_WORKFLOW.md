# 07 WORKFLOW — A-shinya_shiryoshitsu · toshi-densetsu-jp

> Lane `toshi-densetsu-jp`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# QUY TRÌNH TIÊU ĐỀ + MÔ TẢ — LANE A (`toshi-densetsu-jp`, 深夜の資料室)

Chốt 2026-09-20. **Chỉ áp dụng cho lane này** — 都市伝説/宇宙/未解決, kể tài liệu ngôi 3, khán giả 25–55 soi số. Không dùng luật
satori (cụ bà ngôi 1) hay lane D (【】 đầu + —— + ｜ dài 78). Kế hoạch + số liệu: `plans/260920-1636-lane-toshi-densetsu-jp/`.

> 🔴 **2026-09-23: mọi việc tiêu đề/thumbnail lane này đọc SOP trước** —
> `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\lanes\toshi-densetsu-jp\SOP_TIEU_DE_THUMBNAIL_2026-09-23.md`
> (đo máy kênh gốc; thay các luật §2 dưới đây ở 3 chỗ: bật 【都市伝説】 đầu · CẤM khung giải thiêng · 〜じゃない
> lift thật 0,81 chứ không phải 3,3). Ảnh nền ưu tiên ẢNH THẬT PD/CC0.

## 1. Kênh · sheet · thư mục
| | |
|---|---|
| Kênh thật | 深夜の資料室 · `UCYhbfP8greeTOL-0B_-OqLQ` (mở 09/2026; ep01–03 đăng 14–17/09, view 26/0/2 khi bắt đầu) |
| Kênh mẫu | 今夜も都市伝説 `UCoFEha9rNMFqUio-4GQITfw` · `h2dev/docs/channel_dna/imayamo-toshidensetsu` (28 video) |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep<nn>-<slug>` — **`<nn>` = STT cột A trên sheet** (SOP_TOSHI §8d) |
| Giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep<nn>-<slug>` — tool ghi đè **`listting.txt`** (AUTO_LIST đọc; bản cũ `.bak.<ts>`), tập đã đăng cần `--force` |
| Sheet | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` tab **`shinya_shiryoshitsu`**: A = STT (khớp dòng) · C = hồ sơ SPACE_RESEARCH (không phải tập) · **E = tiêu đề tool ghi** · I = thư mục CHANEL · J = ghi chú đăng (ĐÃ ĐẶT LỊCH…) |
| Config | `config/lanes/toshi-densetsu-jp.json` |

## 2. Công thức tiêu đề lane A (đo thật SERP 2026-09-20, 61 tiêu đề ngách + 28 kênh mẫu)
```
<keyword thật: tên vụ/nhân vật/cơ quan/năm> + 1 ĐIỂM LẬT (〜じゃない · 正体/真相 · 「lời cuối」) … <mảnh giấu>  +  【都市伝説 ミステリー 怖い話】
```
- **THÂN ngắn thắng**: thân 20–30 ký tự gmean 343K · 30–40 → 48K · 40–50 → 35K · 50–60 → 17K. Tổng độ dài KHÔNG phải thước đo (【】 kéo dài).
- Chốt **thân 18–32, mục tiêu 26, móc trọn trong 24** — 5 tập cũ thân 19–29 nhưng chưa có điểm lật.
- Suffix `【都市伝説 ミステリー 怖い話】` (16 ký tự) tool tự nối, lift 1.31, Fable chỉ viết thân.
- Phủ định 〜じゃない lift 3.3 (mẫu 138K kênh mẫu) · … ngắt 1.24 · **câu hỏi なぜ/とは/？ đã bão hoà** (37% có, lift 0.4 — khác bàn giao 62%).
- Tên riêng/cơ quan/năm là keyword (khác satori). Số phải có đơn vị và đúng kịch bản (khán giả bắt lỗi số).
- 7 luật đầy đủ: `title_rules` trong json (S2/S3/S3b/S3c đọc từ đó).

## 3. Khuôn `TIEU_DE_MO_TA.txt` / `listting.txt` lane A (anh chốt 2026-09-21: KHÔNG dòng tags — chỉ tiêu đề + mô tả; tags lấy từ sheet cột F)
```
<thân>【都市伝説 ミステリー 怖い話】
(trống)
<hook + 3 đoạn ngôi 3 + câu mời bình luận>
----- GẠCH -----
Timestamps: (giữ nguyên từ file cũ; chưa có → placeholder, bước 3 h2dev điền)
----- GẠCH -----
☕ cảm ơn
----- GẠCH -----
#hashtag
----- GẠCH -----
【映像・画像クレジット】 (giữ từ file cũ; thiếu → mặc định lane)
```
Tool còn ghi **`title.txt`** (dòng 1 = tiêu đề đầy đủ) để h2dev B9 (`publish_kit.py`) không đặt lại tiêu đề.

## 4. Lệnh
```bash
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
py -3.13 cli.py run     --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep06-mandela-effect --profile toshi-densetsu-jp
py -3.13 cli.py view    --slug <dir>                            # XEM.html
py -3.13 cli.py sheet   --profile toshi-densetsu-jp             # ghi cột E (khớp STT; chỉ tập có TITLE_LOCK)
py -3.13 cli.py deliver --slug <dir> --profile toshi-densetsu-jp   # listting.txt → CHANEL (bỏ qua nếu cột J ghi ĐÃ…; --force để ép)
py -3.13 cli.py all     --profile toshi-densetsu-jp --only ep08,ep10
py -3.13 cli.py emit    --slug <dir> --title 2 && py -3.13 cli.py run --slug <dir> --from lock --force   # phủ quyết
py -3.13 cli.py studio  --profile toshi-densetsu-jp             # bảng dán Studio cho video đã đăng
```
yt-dlp dính 429 → thêm `--proxy socks5h://haonguyen262.hao1:quanghao@154.198.33.150:9093`.

## 4b. Thứ tự với h2dev (QUAN TRỌNG — bước 3 viết lại mô tả)
1. h2dev bước 1: kịch bản đạt B3Q/B3F.
2. **Tool chạy** → `TIEU_DE_MO_TA.txt` + `title.txt` + cột E.
3. h2dev bước 3 (agent khác): B8 ghép → **B9 sinh lại gói đăng tải** (lấy tiêu đề từ `title.txt`, nhưng mô tả do Opus của tool bị thay bằng bản AI của h2dev) → B11 chép `listting.txt` vào CHANEL.
4. **Chạy lại `emit` + `deliver`** (0 LLM, cache) → mô tả tool + Timestamps thật + credit quay lại `listting.txt`.
Tập đã dựng trước khi có tool (ep04, ep05): tool chạy → `deliver` ngay, không cần bước 3.

## 5. Bảng tiêu đề cũ → mới (batch 2026-09-20)
| Tập | Tiêu đề cũ thân (ký tự) | Tiêu đề mới thân (ký tự) | QC Sol | ESC |
|---|---|---|---|---|
| ep04-fermi-paradox | 「みんなどこにいるんだ」―宇宙の沈黙が突きつける最悪の答え (29) | 確認信号は0件…フェルミの問いが残した2つの結末 (23) | QC1 FAIL → QC2 FAIL | 1 (thumb) |
| ep05-bermuda-triangle | 5機の爆撃機が消えた日―バミューダトライアングルの真実 (27) | バミューダ5機失踪、報告書は「原因不明」じゃなかった (27) | QC1 FAIL → QC2 FIX → QC3 FAIL (T1 tranh chấp) | 0 |
| ep06-mandela-effect | (chưa có) | マンデラ効果は並行世界じゃない…鍵は1974年の実験 (26) | QC1 FAIL → QC2 FAIL → QC3 FIX | 0 |
| ep01-valentich (đã đăng) | 「あれは航空機じゃない」20歳のパイロットが消えた夜 (26) | セスナ上空の光はUFOか金星か…父が語る息子の恐怖 (25) | QC1 FIX → QC2 PASS | 0 |
| ep02-walton (đã đăng) | 「あれは全部狂言だった」死の間際の告白 (19) | ウォルトンが消えた5日間…迫る2,500ドルの罰金 (25) ⁽ᴼᵖᵘˢ⁾ | QC1 FAIL → QC2 FAIL → QC3 PASS | 0 |
| ep03-bob-lazar (đã đăng) | CIAが59年隠した基地の正体―ボブ・ラザーの内部告発 (27) | 「地下に9機の円盤」エリア51の男を公文書で追うと… (26) ⁽ᴼᵖᵘˢ⁾ | QC1 FAIL → QC2 FIX → QC3 FIX (D SPOILER còn 2) | 0 |
| ep08-fatima-akita | (chưa có) | ファティマの56年後…秋田の聖母像が101回流した涙 (25) ⁽ᴼᵖᵘˢ⁾ | QC1 FAIL → QC2 FIX → QC3 PASS | 0 |
| ep10-tesla-tictac | (chưa có) | テスラの死から61年後、米海軍が撮った76秒の映像 (26) ⁽ᴼᵖᵘˢ⁾ | QC1 FIX → QC2 FAIL → QC3 PASS | 0 |

⁽ᴼᵖᵘˢ⁾ = S2/S3/S3c/S3b chạy bằng Opus (`--writer opus --picker opus`) vì Fable hết quota 2026-09-21 04:46; ep01 S2 Fable · ep02 S1/S2 Fable, S3 trở đi Opus.
Sheet cột E 8/8 · CHANEL 6/6 thư mục có `listting.txt` mới không dòng tags (ep01–06, AUTO_LIST parse OK 0 lỗi, bản cũ `.bak`) · ep01–03 đã đăng: đổi trên YouTube theo bảng dán Studio
`data/DOI_TIEU_DE_STUDIO_toshi-densetsu-jp.md` (3 video id khớp) · ep06/08/10 chưa dựng → sau bước 3 h2dev chạy `emit` + `deliver` lại (§4b).

## 5b. CẦN XEM / ESCALATE em đã quyết
| Tập | Việc | Lý do |
|---|---|---|
| ep04 | Thumbnail: dòng 「文明が『１つもない』」 mạnh hơn kịch bản (kịch bản chỉ nói CHƯA THẤY tín hiệu nào, không nói không có văn minh) → đề nghị 「文明が『見つからない』」 hoặc 「信号は0件」 | Sol T1 MISLEADING HIGH nhắm vào thumb; Fable ESCALATE vì ngoài quyền tiêu đề. Em GIỮ tiêu đề (確認信号は0件 đúng nguyên văn kịch bản). Thumb là việc bước 2 h2dev. |
| ep05 | (đã quyết: GIỮ tiêu đề) | Sol T1 MISLEADING: 「報告書は原因不明じゃなかった」 có thể đọc là hồ sơ cuối cũng không phải 原因不明. Fable REJECT_WEAK_EVIDENCE: kịch bản tự phân biệt 報告書 (kết luận lỗi định vị + hết xăng) với 公式記録 (bị sửa thành 原因不明 vì 配慮 gia đình Taylor); tiêu đề dùng đúng chữ 報告書 và đây chính là điểm lật chương 1. Em đồng ý giữ — đúng công thức 〜じゃない của lane. |
| ep03 | Mô tả còn 2 SPOILER (D1 「物理学者だったと裏づける証拠が一枚も出てこない」, D2 CIA công nhận Area 51) sau 2 vòng Opus sửa | Em giữ: D2 là sự kiện công khai 2013 (không phải twist riêng của video), D1 là điểm nhấn kênh mẫu cũng đưa lên mô tả. Anh muốn kín hơn → `revise --force` thêm vòng. |
| ep06 | (đã quyết: GIỮ tiêu đề) | Sol T1 SPOILER MEDIUM ×2 lượt: 「並行世界じゃない」 lộ kết luận. Fable REJECT ×2: luật 3 cho phép phủ định niềm tin chung, mảnh giấu là 1974年の実験; cùng cấu trúc mẫu 138K của kênh mẫu. |

## 6. Khi nào can thiệp tay
- XEM.html mục 5 có **ESCALATE** → anh đọc lý do 2 bên, giữ hoặc `emit --title N`.
- Sol `SKIPPED` → chạy lại `qc-sol` sau.
- Tập chưa có `TIEU_DE_MO_TA.txt` → `run` tạo mới với placeholder Timestamps; bước 3 h2dev điền mốc thật.

## 7. Đo sau khi đăng
`cli.py track --profile toshi-densetsu-jp --deep` mỗi ngày → `data/track.csv` (dùng chung mọi lane, phân biệt theo video_id). So CTR Home/Suggested trong Studio sau 7 ngày,
tối thiểu 5 tập tool. Kênh mới 0 sub → views thấp không chỉ do tiêu đề.

## 8. Nhật ký quyết định
| Ngày | Quyết định |
|---|---|
| 2026-09-20 | Anh giao toàn quyền; chốt T1–T11 (brainstorm §10): tag = suffix, thân 18/26/32, tên riêng OK, ngôi 3, deliver listting.txt không xoá, title.txt, sheet STT, studio cho ep01–03, thứ tự ep06→04/05→08/10. |
| 2026-09-20 | Phase 1 SERP: thân ngắn 20–30 thắng gấp 7 lần 30–40; câu hỏi bão hoà → luật 3 đổi: … và 「」 ưu tiên, ？ chỉ khi là điểm lật thật. |
| 2026-09-20 | Phase 2: 4 vá (sheet_match=stt · deliver_name · write_title_txt · fixed block theo chỉ số) + seed_name_rule; satori/lane D golden diff rỗng; tests 26/26. |
| 2026-09-21 | Phase 3: 8/8 tập khoá, sheet E 8/8, deliver ep04/05, Studio 3 video. Fable hết quota 04:46 → thêm `--writer/--picker` CLI, 4 tập cuối chạy Opus. 3 ESCALATE/tranh chấp em quyết giữ (§5b). |
| 2026-09-21 | ep01–03 đã đăng: tool KHÔNG đổi trên YouTube; anh tự quyết dán theo bảng Studio (view 26/0/2 nên đổi ít rủi ro). |
| 2026-09-22 | Fable vẫn hết quota → thêm `model_writer_override`/`model_picker_override: "opus"` vào `config/lanes/toshi-densetsu-jp.json` (đọc trong `cli.py _ctx`, không cần gõ `--writer/--picker` mỗi lệnh nữa). CHỈ lane này đổi — satori/lane D vẫn writer=picker=claude-fable-5-1. Khi Fable có quota lại: XOÁ 2 khoá này trong json (không chỉ sửa giá trị) để quay lại Fable. |
| 2026-09-21 | Anh chốt: `listting.txt` chỉ tiêu đề + mô tả (bỏ dòng tags, `tieu_de_keywords_line=false`); giao CẢ tập đã đăng (`--force`) → 6/6 CHANEL cập nhật. |
| 2026-09-23 | Fable có quota lại (ping OK) → XOÁ `model_writer_override`/`model_picker_override` khỏi `config/lanes/toshi-densetsu-jp.json` theo đúng ghi chú 2026-09-22; lane quay về dùng `claude-fable-5-1` cho S2/S3/S3c/S3b theo `config/models.json`. Không đụng lane khác — `satori-jp-obaa.json` đang tự có override riêng của tab satori (đặt 2026-09-22), không phải của lane này. |

## Thumbnail (S7, gộp 2026-09-22)
Phong cách khoá của lane ở `config/lanes/toshi-densetsu-jp.thumb.yaml` (mẫu kênh / TEMPLATE ở `docs/lanes/toshi-densetsu-jp/thumb/`). `run` tự chạy sau
`deliver`; ảnh chọn `<slug>/thumbnail_final.png`, 3 ảnh + điểm Fable/Opus trong `research/XEM.html` mục 7. DỪNG chờ anh →
`py -3.13 cli.py thumb-publish --slug <dir> --profile toshi-densetsu-jp [--choose B]` mới ghi Sheet G + CHANEL. Chi tiết `docs/thumbnail.md`.

---
## SOP_TIEU_DE_THUMBNAIL_2026-09-23.md

# SOP TIÊU ĐỀ + THUMBNAIL — LANE A (`toshi-densetsu-jp`, kênh 深夜の資料室) · 2026-09-23

> 🔴 **BƯỚC 0 BẮT BUỘC (anh chốt 2026-09-24, mọi tập):** đọc `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\toshi-densetsu-jp.json`
> (luật kênh mẫu + mục `our_eps` của đúng tập) trước khi viết tiêu đề/chữ thumbnail. Đọc bắt buộc, áp dụng LINH HOẠT: chỉ lấy điểm hợp với tập, không phải luật cứng. Tool tự bơm vào prompt, còn `sheet-publish`/`thumb-publish`
> chặn tập chưa đọc. Xem mục "LUẬT BẮT BUỘC" trong `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\CLAUDE.md`.

> ⚠ **CHỈ DÙNG CHO LANE NÀY.** Lane satori (`docs\lanes\satori-jp-obaa\SOP_TIEU_DE_THUMBNAIL_2026-09-23.md`),
> lane D, lane G có kênh mẫu khác → SOP khác. Bê công thức satori sang đây là ra tiêu đề sai ngách.
>
> **Anh đã chốt 2026-09-23:** (1) áp cho **cả 8 tập cũ + tập mới**; (2) **bật 【都市伝説】 ở đầu tiêu đề** cho cả kênh;
> (3) **đo máy DNA thumbnail kênh gốc trước** — đã đo xong, số liệu ở §3; (4) **ảnh thumbnail ưu tiên số 1 là ẢNH THẬT** (§3c).
>
> Vì sao có file này: 3 tập đã đăng được 26 / 0 / 2 view → lane **không có CTR của chính mình**, mọi luật phải rút từ kênh gốc.

## 1. Nguồn dữ liệu (đo ngày 2026-09-23, không phải phỏng đoán)

| | |
|---|---|
| Kênh mình | 深夜の資料室 · `UCYhbfP8greeTOL-0B_-OqLQ` |
| Kênh gốc | 今夜も都市伝説 · `UCoFEha9rNMFqUio-4GQITfw` — 32 video có view, trung vị 24.500 |
| Công thức tiêu đề (máy) | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\lanes\toshi-densetsu-jp\CONG_THUC_TIEU_DE_KENH_GOC.md` |
| DNA thumbnail (máy, OpenCV+OCR) | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\data\thumb_dna\toshi-densetsu-jp\out\thumb_dna.json` + `BAO_CAO_DO_THUMB_DNA.md` + `thumbs\win\*.jpg` (28 ảnh) |
| Cấu hình đo (chạy lại được) | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\tools\thumb_dna_measure\lanes\toshi-densetsu-jp.json` |
| Audit hook + gói đăng 9 video kênh gốc + 8 tập của mình | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\HOOK_AUDIT_KENH_CLONE.md` (mục 今夜も都市伝説) |
| Dữ liệu hook từng video | `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\seed_2026-09-23_toshi.json` · khuôn: `patterns.json` (7 pattern + 5 closer `lanes_fit=toshi-densetsu-jp`) |
| 10 nguyên tắc gói đăng | `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md` |

**Lệnh đo lại:**
```bash
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\tools\thumb_dna_measure\run_measure.py --lane toshi-densetsu-jp --all
```

**3 bẫy đo đã dính hôm nay:**
1. **Unicode NFD** — tiêu đề yt-dlp trả về `ぜ` = `せ` + dấu đục rời. Regex kana dựng sẵn khớp **0 dòng mà không báo lỗi**
   (`なぜ` ra 0/32, `じゃない` ra 3 thay vì 7). Luôn `unicodedata.normalize("NFC", t)`.
   → `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\tools\title_formula_kenh_goc.py` hiện chỉ có regex tiếng HÀN và không normalize.
2. **`thumb_text.txt` của tập mình KHÔNG phải chữ trên ảnh thật** — ep03, ep08, ep10 đã đổi thumbnail sang khuôn mới mà file text còn bản cũ.
   Luôn đọc chữ **từ ảnh** (`thumbnail.png` trong CHANEL là bản đang dùng).
3. **`report_md.py` khoá cứng tiêu đề "LANE G teinengo-tanoshimi"** — báo cáo sinh ra cho lane A vẫn in tên lane G ở dòng 1 và trỏ path lane G.
   Số liệu trong bảng vẫn đúng của lane A; sửa chỗ hardcode khi rảnh.

## 2. TIÊU ĐỀ

```
【都市伝説】 + 「lời nguyên văn trong kịch bản」 HOẶC 〈nhân vật cụ thể〉+ đã làm gì  …  1 mảnh bị giấu
             + 【都市伝説 ミステリー 怖い話】   (tool tự nối)
```

### 2a. Đòn bẩy đo trên 32 tiêu đề kênh gốc

| Đòn bẩy | Lift | Lane A hiện làm |
|---|---|---|
| 「lời trích」 trong thân | **1,65** | 3/8 |
| nhân vật cụ thể (男/博士/飛行士/科学者/少年/元米軍) | **1,65** | 2/8 |
| con số | 1,51 | 8/8 ✅ |
| **【】 ở ĐẦU** | **1,37** | **0/8** → anh đã chốt BẬT |
| 「lời trích」 đứng MỞ ĐẦU thân | 1,36 | 1/8 |
| móc 日本 | 1,21 | 1/8 |
| 正体/真相/隠され/封印 | 1,15 | 3/8 |
| … ngắt | 0,88 | 6/8 (đang dùng như dấu câu) |
| 〜じゃない | **0,81** | — số "lift 3,3" ghi 20/09 là do bẫy NFD, **không còn đứng vững** |
| とは？ / のか？ · なぜ · ●● trong tiêu đề · ヤバすぎる/衝撃 | 0,77 / 0,49 / 0,63 / 0,29 | 0/8 ✅ giữ nguyên lệnh cấm |

### 2b. Luật cứng

1. **【都市伝説】 ở đầu** (không tính vào thân) — anh chốt bật cho cả kênh.
2. **Ưu tiên 1 = 「lời nguyên văn」 hoặc NHÂN VẬT + hành động.** Phủ định 〜じゃない chỉ là một lựa chọn ngang hàng.
3. 🔴 **CẤM khung GIẢI THIÊNG.** Kênh gốc **0/31 tiêu đề** nói "chỉ là thần thoại / chỉ là nhớ sai / không hề có".
   Tiêu đề phải hứa **bí ẩn LỚN HƠN**: `X không phải Y — mà là Z lạ hơn` (mẫu 151K: `UFOは宇宙人じゃない。答えは100年前に出ていた…`).
   **Tập mình đang 4/8 giải thiêng** (ep03 `「物理学者」は嘘だった`, ep04 `0件`, ep05 `作られた神話`, ep06 `並行世界じゃない`) → phải viết lại.
4. **Thân 18–32 ký tự** (mục tiêu 26, móc trọn trong 24). Lưu ý trung thực: đây **không phải đòn bẩy đã chứng minh** —
   thân top-6 kênh gốc là 26/32/46/55/34/72; nhóm ≤35 ký tự có gmean 63.067 nhưng chỉ n=5. Giữ 18–32 vì nó nằm trong vùng top và hợp màn hình dọc.
5. **Con số có đơn vị, đúng kịch bản, viết bằng CHỮ SỐ** (`61年` không `六十一年`) — `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\numerals.py`.
6. **Có yếu tố Nhật thì đưa lên tiêu đề** (3/3 video Nhật của kênh gốc đều hé ngay trong hook; 120K/112K/172K).
7. **Mọi danh từ trong tiêu đề phải grep được trong `script.txt`** — cả dạng chữ số lẫn chữ Hán (`76秒` ↔ `七十六秒`; ep10 từng trượt QC vì lỗi này).

## 3. THUMBNAIL

### 3a. Số đo máy trên 28 thumbnail kênh gốc (so với 8 thumbnail của mình)

| Chỉ số | Kênh gốc (28 mẫu) | Lane A hiện tại | Kết luận |
|---|---|---|---|
| **Độ phủ chữ** | q25 **0,391** · trung vị **0,427** · q75 **0,510**; nhóm view thấp chỉ 0,21–0,27 | **0,268–0,367** (trung vị 0,32) | ❌ **cả 8 tập nằm dưới q25 của kênh gốc, sát vùng "thua"** → chữ phải TO hơn ~25% |
| Băng vàng mép trên | 27/27 | 8/8 có | ✅ |
| **Băng đỏ mép dưới** | **25/28 ở nhóm view cao, 1/4 ở nhóm view thấp** (chỉ số phân biệt mạnh nhất máy đo được) | 8/8 có | ✅ giữ |
| Số dòng chữ chính | 2–3 | **4–5** | ❌ chẻ nhiều dòng làm chữ nhỏ |
| Chiều cao băng | trên ~0,19–0,22 H · dưới ~0,21–0,23 H, rộng 0,97–0,99 W | băng hẹp hơn, nhiều tập canh cột trái | ❌ |
| Màu | vàng `#F5F62A`–`#FDFD0B` · đỏ `#EF0707`–`#F00607`, **viền đen rất dày** | viền mỏng hơn hẳn (so ảnh ep10 vs `saIym-x8dPc`) | ❌ tăng `stroke_ratio` |
| Nền | tối/xanh đêm 8/9 | ep10 nền trời sáng ban ngày | ❌ |
| Mũi tên đỏ chỉ chi tiết | 5/9 | 0/8 (engine chưa có) | thêm nếu rẻ |
| Số khung (panel) | 1/1 — không chia khung | 1 | ✅ |

### 3b. Nội dung chữ — 3 băng, **mỗi băng đứng độc lập**

| Băng | Nội dung | Mẫu kênh gốc |
|---|---|---|
| VÀNG trên (≤16) | **AI đã làm CHUYỆN GÌ** — danh ngữ `〜した男` / `X が暴露した` / `本当の理由`; đọc riêng vẫn ra nghĩa | 宇宙人と対話した男 · NASAが月を見捨てた本当の理由 · 3906年の未来にタイムスリップした男 |
| TRẮNG nhỏ (≤12, tuỳ chọn) | cầu nối: nguồn / mốc thời gian | 1917年の証言 · 100年前に答えは出ていた · キリストの正体は… |
| ĐỎ dưới (≤14, TO NHẤT) | **一 trong hai**: 「lời nguyên văn **được đọc trong 40–60 giây đầu**」 **hoặc** `●●` che ĐÚNG 1 đáp án | 「月の裏側に鳥居がある」 · 「彼は地球の人間ではない」 · 正体は●●だった |

**5 lỗi lặp lại của lane A:** (1) 0/8 dùng `●●`; (2) 5/8 băng đỏ là **một TỪ đóng ngoặc** (`「神話」`, `「大統領」`) chứ không phải câu ai nói;
(3) 3/8 **chẻ một câu làm đôi** qua 2 băng; (4) 0/8 dùng dòng trắng (engine có sẵn `roles.lead`); (5) ep08 bản cũ lặp nguyên ý tiêu đề.

### 3c. 🔴 ẢNH NỀN: ƯU TIÊN SỐ 1 LÀ ẢNH THẬT (anh chốt 2026-09-23)

**Thứ tự chọn ảnh nền:**
1. **Ảnh tư liệu THẬT, Public Domain / CC0** — Wikimedia Commons, NASA, US DoD, Library of Congress, 国立国会図書館.
   Hợp lane 資料室 nhất: ep01 Cessna VH-DSJ · ep02 rừng Apache-Sitgreaves · ep03 Area 51 ảnh vệ tinh · ep05 đội TBF Avenger + chân dung Taylor ·
   ep10 **khung hình FLIR/GIMBAL do Bộ Quốc phòng Mỹ công bố** + chân dung Tesla — đều có bản PD.
2. **Ảnh thật PD + xử lý tối/đổ bóng** để chừa chỗ cho 2 băng chữ (không bịa chi tiết mới lên ảnh).
3. **AI key art** chỉ khi đề tài **không có ảnh thật** (fermi paradox, mandela effect, khái niệm trừu tượng).

**Cổng giấy phép (bắt buộc, máy chặn):**
- Thumbnail là **ảnh CHÍNH** → **chỉ PD / CC0**.
- **YouTube CC BY (kể cả đúng chuỗi CC BY) CẤM dùng làm thumbnail** — giấy phép do chủ kênh tự khai, họ đổi/gỡ lúc nào cũng được và nhiều kênh
  khai hộ tư liệu của người khác. CC BY **chỉ được làm b-roll nền trong video**.
  Chi tiết: `C:\Users\admin\.claude\skills\stock_media_sourcing.md` · công cụ tải: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\yt_stock.py` ·
  hướng dẫn: `E:\CLAUDE\YOUTUBE\h2dev\docs\HUONG_DAN_YT_STOCK.md`.
- Mọi ảnh dùng phải vào `credits.txt` của tập (nguồn chân lý là manifest, không phải trí nhớ).

**ĐO THẬT TRÊN ep01 (2026-09-24, bản đầu tiên làm bằng ảnh PD):**

| | Bản AI cũ | Bản ẢNH THẬT (PD/CC0) |
|---|---|---|
| Sol chấm thumbnail | **7,4–7,8/10** | **6,5/10** |
| Độ phủ chữ (bộ đo kênh gốc) | 0,323 | 0,306–0,419 tuỳ số ký tự mỗi băng |
| Sol chê gì | — | "silhouette phẳng, không có phi công / vật thể lạ / tình huống truy đuổi → chưa ra cảm giác hồ sơ mất tích UFO" |

→ **Đánh đổi đã đo được:** ảnh tư liệu PD hầu như không có cảnh kịch tính (UFO, ánh sáng lạ, người trong buồng lái),
nên sức hút thị giác thấp hơn AI key art khoảng 1 điểm Sol. Ba đường đi: (a) giữ ảnh thật và chấp nhận, (b) quay lại AI
key art, (c) LAI — ảnh thật làm nền + tăng cường ánh sáng/độ tương phản của chi tiết CÓ THẬT trong ảnh (không thêm vật thể).
Chưa có CTR để phân xử; quyết định là của anh.

**Số ký tự quyết định độ phủ chữ, không phải chiều cao băng:** engine co chữ theo CHIỀU RỘNG, nên băng 12 ký tự luôn
nhỏ hơn băng 9 ký tự dù `height_ratio` có tăng. Kênh gốc trung vị **9 ký tự/băng** — muốn chữ to bằng họ thì phải viết ngắn.

**Ghi chú trung thực:** kênh gốc **7/9 dùng người do AI vẽ, 0/9 dùng ảnh tư liệu thật** (máy bắt mặt Haar 22/28 ảnh).
Nghĩa là "ảnh thật" là **lựa chọn khác biệt hoá của mình**, không phải thứ đã được kênh gốc chứng minh. Đổi lại nó hợp tên kênh
(深夜の資料室 = phòng tư liệu) và tránh hẳn rủi ro ảnh AI lỗi. Đề xuất: **8 tập cũ làm ảnh thật, 2 tập trừu tượng giữ AI**, rồi so CTR sau 7 ngày.

## 4. CỔNG KHỚP 4 MẶT + THỨ TỰ THỜI GIAN (phát hiện quan trọng nhất)

Trong 9 video kênh gốc đã mổ hook: 4 video khớp cả 3 cặp (tiêu đề↔thumbnail↔hook) = 172K/151K/120K/112K (**gmean ~137K**);
5 video lệch ≥1 cặp = 94K/69K/13,7K/11,4K/4,8K (**gmean ~26K**) → **chênh ~5 lần**.

**Khung thời gian bắt buộc của lane** (đo trên kênh gốc, `hook_stage.py` của h2dev là nơi thực thi):

| Mốc | Phải có | Kênh gốc | Tập mình |
|---|---|---|---|
| 0–4 giây | câu ≤20 chữ = **nguyên văn băng VÀNG** hoặc nửa đầu tiêu đề | 8/9 | **2/8** |
| 0–20 giây | năm + người + điều bất khả (cấm mở bằng lịch trình `〜の夕方、〜空港から離陸しました`) | 6/9 | 5/8 mở bằng biên niên |
| 40–60 giây | **câu băng ĐỎ được đọc lên** | 5/9 K | ep10 cả 3 dòng ở 720–842s (L), ep08 ở 309s |
| 55–100 giây | **≥2 câu なぜ** | 8/9 | **2/8** |
| 85–115 giây | câu nghi thức `それでは…最初から辿っていこう` (closer **K13**) rồi vào 第1章 | 9/9 | thiếu ở phần lớn tập |

**Mô tả:** kênh gốc 9/9 dòng 1 = `【都市伝説 ミステリー 怖い話】` + chép lại tiêu đề, 0/9 có mốc chương.
Lane mình viết mô tả dài hơn (hook + 3 đoạn) — giữ được, nhưng **dòng đầu phải chứa lại lời hứa của tiêu đề**, và mốc chương phải đúng
(ep08 mốc dính thân bài, ep10 còn placeholder).

## 5. Bảng việc cho 8 tập đã có + tập mới

Chữ thumbnail đọc **từ ảnh thật** trong `E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\<ep>\thumbnail.png` (không tin `thumb_text.txt`).

| Tập | Tình trạng đo được | Việc |
|---|---|---|
| ep01-valentich | thumb khớp hook (`「あれは航空機じゃない」` ở ~0:25) nhưng tiêu đề bỏ mất câu trích; `父が語る` ngoài 90s; cover 0,323 | **Viết lại tiêu đề** (trả câu trích vào tiêu đề) · tăng cỡ chữ · nền ảnh thật Cessna |
| ep02-walton | tiêu đề OK; nền "hành tinh chung chung" không liên quan Arizona; cover 0,314 | Băng vàng `〜した男` · **đổi nền sang ảnh thật** · tăng cỡ chữ |
| ep03-bob-lazar | **2 thumbnail khác nhau** (bản CHANEL 09-20 đúng khuôn mới); tiêu đề giải thiêng `「物理学者」は嘘だった` | Chốt 1 file · **sửa tiêu đề bỏ khung giải thiêng** · cover 0,346 → ≥0,39 |
| ep04-fermi | tiêu đề `0件` = giải thiêng; thumb chẻ 1 câu làm đôi; cover 0,287 | **Làm lại cả tiêu đề lẫn chữ thumbnail** (giữ AI art — đề tài trừu tượng) |
| ep05-bermuda | cả gói giải thiêng (`作られた神話`) — kênh gốc 0/31 làm vậy; lời hứa trễ 7,5 phút; cover 0,367 | **Làm lại cả gói**, đổi sang khung "bí ẩn lớn hơn"; nền ảnh thật TBF Avenger (PD) |
| ep06-mandela | `並行世界` trễ 25 phút; thumb chẻ đôi, `「大統領」` không phải lời thoại; cover **0,268** (thấp nhất) | **Làm lại cả 2** |
| ep08-fatima | thumb đã đổi sang khuôn mới (`七万人が見上げた太陽` / `「地上に向かって落下」`) nhưng câu đỏ ở 309s; tiêu đề 2 danh từ ngoài 90s; cover 0,297 | Sửa tiêu đề theo hook · tăng cỡ chữ · hoặc hé câu đỏ vào hook |
| ep10-tesla | **chưa dựng final.mp4** → sửa rẻ nhất; thumb khuôn mới nhưng nền SÁNG, cả 3 dòng chữ nằm ở 720–842s (L), 0 câu なぜ | **Ưu tiên 1**: sửa hook + nền tối + dùng khung hình FLIR (PD) |
| ep12-boriska | chưa có gì | Áp SOP ngay từ đầu |

## 6. Chuỗi lệnh 1 tập

```bash
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
# B1. Đọc 90 giây đầu: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars\script.txt
# B2. Tiêu đề + mô tả, chưa sinh ảnh
py -3.13 -X utf8 cli.py run --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp --no-thumb
# B3. Hỏi Sol chọn/chỉnh tiêu đề (0đ)
py -3.13 -X utf8 cli.py title-ask --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp --candidates <file 3 dòng>
# B4. Hỏi Sol + Fable chữ thumbnail & prompt ảnh TRƯỚC khi tốn tiền ảnh
py -3.13 -X utf8 cli.py thumb-ab --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp --advisor both --no-render
# B5. Dựng 3 ảnh + Opus chấm → E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars\research\XEM.html
py -3.13 -X utf8 cli.py thumb --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp
# B6. Cổng Sol packaging (kịch bản + tiêu đề + chữ thumbnail)
py -3.13 -X utf8 cli.py sol-check --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp
# B7. Anh duyệt → publish
py -3.13 -X utf8 cli.py thumb-publish --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp [--choose B]
py -3.13 -X utf8 cli.py sheet-publish --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp
py -3.13 -X utf8 cli.py deliver      --slug E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars --profile toshi-densetsu-jp
```

## 7. Việc phải làm trước khi chạy lô 8 tập

| # | Việc | File | Tốn |
|---|---|---|---|
| 1 | `title_rules`: bật 【都市伝説】 đầu · **cấm khung giải thiêng** · hạ 〜じゃない · siết `…` · bắt buộc 「」 hoặc nhân vật | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\toshi-densetsu-jp.json` | 0đ |
| 2 | `thumb.yaml`: độ phủ chữ **0,39–0,51** (đang ≥0,30) · băng cao 0,19–0,23 H rộng ≥0,97 W · `stroke_ratio` dày hơn · tối đa 3 dòng · bật `lead` · băng vàng `〜した男` độc lập · cấm chẻ câu | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\toshi-densetsu-jp.thumb.yaml` | 0đ |
| 3 | **Cổng máy**: grep từng vế tiêu đề + từng dòng thumbnail trong `script.txt` (cả chữ số ↔ chữ Hán) và kiểm mốc giây (băng vàng ≤4s, băng đỏ ≤60s) | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\thumb_strategy.py` + `src\qc_sol.py` | 0đ |
| 4 | Nhánh **ảnh nền PD** cho S7 (tra Wikimedia/NASA trước, AI chỉ là fallback) + cổng giấy phép chặn CC BY | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\thumb_stages.py` (+ `stock_sources.py`) | 0đ |
| 5 | Bộ đặc trưng tiếng Nhật + NFC cho công cụ đo tiêu đề | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\tools\title_formula_kenh_goc.py` | 0đ |
| 6 | (tuỳ chọn) mũi tên đỏ | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\thumbnail_engine\bands.py` | 0đ |
| 7 | Chạy lô 8 tập + ep12 | | ~1.200–1.500đ ảnh |

Việc sửa **hook 0–115 giây** (§4) thuộc h2dev (`hook_stage.py`, hook-repair) — tool này chỉ kiểm và báo lệch, không tự sửa kịch bản.

<!-- export 7c146d33f87d · 2026-09-26 -->
