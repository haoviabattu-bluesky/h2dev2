# 07 WORKFLOW — G-teinengo-tanoshimi

> Lane `teinengo-tanoshimi`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# LANE `teinengo-tanoshimi` (tab `teinengo-tanoshimi`) — sinh bởi `lane-init` 2026-09-23

**Thumbnail: Trạng thái: PILOT — chưa khoá** — khuôn `config/lanes/teinengo-tanoshimi.thumb.yaml` sinh từ DNA (`docs/lanes/teinengo-tanoshimi/thumb/research/thumb_dna.json`), mô-típ ở `docs/lanes/teinengo-tanoshimi/thumb/TEMPLATE.md`.

**Tiêu đề: ĐÃ CÓ LUẬT (chốt 2026-09-24)** — `title_rules` trong `config/lanes/teinengo-tanoshimi.json` (file 02_TITLE_RULES của Project ChatGPT). Dòng "chưa có luật" cũ đã lỗi thời.

## 1. Kênh · sheet · thư mục

| | |
|---|---|
| Kênh mẫu | https://www.youtube.com/channel/UCI2cPqBmCPMxxKI4u2Gqs_Q, https://www.youtube.com/channel/UCxD2Exs2Q4lf7x0Q28OuKvg, https://www.youtube.com/channel/UCjlh_Ko4lEpJIqftz5mxNXQ, https://www.youtube.com/channel/UCRkP44Mcw-K8IktdTqxC9dg, https://www.youtube.com/channel/UCdN_h3ClY8tfQRfIBv2HZVw |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep<nn>-<slug>` |
| Giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-tanoshimi\ep<nn>-<slug>` |
| Sheet | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` tab **`teinengo-tanoshimi`** (cột khớp dòng: TODO — xem `sheet_match` lane gần nhất) |
| Config | `config/lanes/teinengo-tanoshimi.json` + `config/lanes/teinengo-tanoshimi.thumb.yaml` |

## 2. Lệnh

```bash
py -3.13 -X utf8 cli.py thumb --slug <ep> --profile teinengo-tanoshimi        # pilot thumbnail (tốn gpti2)
py -3.13 -X utf8 cli.py lane-lock --profile teinengo-tanoshimi               # sau khi thumb-publish tập pilot
```

## 3. Nhật ký

- 2026-09-23: lane-init từ DNA đo 2026-09-22 (nền `toshi-densetsu-jp`).

---
## PHUONG_AN_GOI_DANG_2026-09-24.md

# PHƯƠNG ÁN GÓI ĐĂNG LANE G `teinengo-tanoshimi` (tab `G-teinengo-tanoshimi`) — 2026-09-24

Kênh mình: chưa có video công khai · Kênh mẫu: **老後のお金ストーリー** `UCI2cPqBmCPMxxKI4u2Gqs_Q` (6.360 sub, 20 video,
trung vị **1.376 view/ngày**, video mạnh nhất 95.648 view/24h).

**Đã đọc `our_eps` cả 10 tập** trong `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\teinengo-tanoshimi.json`
(lỗi đã đo + 20 đề xuất tiêu đề đã grep script) — xử lý từng tập ở §6.

---

## 1. Hồ sơ đã nhận cho lane G — kiểm kê

| Nguồn | Đường dẫn | Có gì dùng được |
|---|---|---|
| Title intel (23/9 23:28, 149 KB) | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\teinengo-tanoshimi.json` | 5 công thức tiêu đề F1–F5 · 7 cặp thắng/thua · 6 mẫu tiêu đề thua · công thức thumbnail + đối chiếu thắng/thua · hook 8 nhịp · 7 nguyên tắc · 20 video kênh mẫu · **`our_eps` 10 tập của mình: lỗi đo được + 2 đề xuất tiêu đề/tập đã grep script** |
| Audit hook lane E/F/G | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\HOOK_AUDIT_LANE_EFG.md` §681–1000 | hook hiện tại từng tập + mốc giây thật (ep01 lấy từ `voice.srt`, 9 tập còn lại ước từ char-rate 321,5) |
| DNA thumbnail đo máy | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\teinengo-tanoshimi\thumb_dna.json` + `BAO_CAO_DO_THUMB_DNA.md` | đo 19/19 thumbnail kênh gốc (bản 23/9 đã sửa 3 lỗi đo) |
| Khuôn thumbnail đang chạy | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\teinengo-tanoshimi.thumb.yaml` | layout `bands_manga`, `dna_measured: true`, pilot ep09 Opus chấm 45/45 |
| Kịch bản | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep01..ep10\script.txt` | 10/10 LOCK |
| **Mô tả + tags kênh mẫu** | tôi đo hôm nay → `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\data\thumb_dna\kenh_goc_UCI2cP\desc_tags.json` | **Chưa ai đo trước đó** — số liệu ở §4, §5 |

**Thiếu trong hồ sơ:** không có dữ liệu nào về MÔ TẢ và TAGS của kênh mẫu → tôi đã tự đo 10 video (§4, §5).

## 2. Hiện trạng thật (Sheet `G-teinengo-tanoshimi` + đĩa)

| | |
|---|---|
| Kịch bản | 10/10 Done |
| Ảnh minh hoạ | 10/10 Done (81–96 ảnh/tập) |
| Cột E tiêu đề · F tags · G thumbnail | **0/10 — trống hết** |
| Video dựng xong | chỉ `ep01-asa-shukan` (`voice.mp3` + `final.mp4`); CHANEL mới có ep01 |
| Gói đăng | `ep09-toshokan` có `TIEU_DE_MO_TA.txt` + `thumbnail_final.png` (pilot khuôn 23/9, **chưa publish**) |

Tiêu đề đang nằm ở cột B là **bản nháp cũ** (= `title_now` trong `our_eps`) — research đã chấm là có lỗi ở 10/10 tập.

## 3. TIÊU ĐỀ — phương án

### 3.1 Vấn đề lớn nhất: lane G chưa có luật tiêu đề
`E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\teinengo-tanoshimi.json` đang ghi
`"title_rules": "TODO: luật tiêu đề lane này chưa viết…"` → nếu chạy S2/S3 bây giờ, Fable viết bằng **luật mặc định của
satori** (cụ bà ngôi 1, 40 ký tự, động từ sự cố) — sai ngách. Phải viết `title_rules` lane G trước khi chạy tập nào.

### 3.2 Khung chốt (từ 5 công thức đo được)

| Mã | Khung | Dùng cho tập | Bằng chứng |
|---|---|---|---|
| **F1** | `【漫画】定年後、{最強の/一流だけがやっている}{đề tài}{N}選…実は{1円もかからない/○○しない}{phần thưởng}` | ep02, ep07, ep09 | AOe 13.885/ngày (10,1× trung vị); bản làm lại `_D8q` 95.648 view/24h |
| **F2** | `【漫画】一生に一度は{歩き/参拝し}たい…定年後に行くべき{tính từ hẹp}{địa điểm}{N}選` | ep03, ep06, ep10 | BeIZ 3,7× · `_G9s` 2,1× |
| **F3** | `【漫画】なぜか{老けない}{tuổi+giới}が「{毎朝やっていること}」{N}選…同年代と差がつく意外な共通点` | ep01, ep08 | bgUq 4,1× (nhiều view nhất kênh) |
| **F4** | `【漫画】{60代}から人生が{心地よく}なる…定年後に見つけた{danh từ dịu}{N}選` + thumbnail phủ định | ep04, ep05 | `_EhP` 6× |
| **F5** | `【漫画】{thứ quen}に{giá sốc}！？{chuẩn quen}より高い{bản sang}に{tuổi}で{thử}てみた結果…` | (chưa tập nào hợp) | ASBV 3,9× |

### 3.3 Luật cứng đề xuất cho `title_rules`
1. **Tiền tố `【漫画】` bắt buộc** — 20/20 video kênh mẫu có.
2. **Độ dài thân 33–45 ký tự** (kênh mẫu ổn định từ 18/8). Tiêu đề >45 nằm trọn trong nhóm thua → đổi
   `title_target_chars` 40 → **40**, `title_max_chars` 48 → **45**, `title_head_warn` → 24.
3. **Bắt buộc có `定年後` / `60代` / `65歳`** — 14/15 video sau bước ngoặt có; video duy nhất bỏ (`_Az1`) tụt 5,8× so với
   video cùng đề tài.
4. **Bắt buộc có `N選`** trừ khi là khung F5 — sau hit: 7 video N選 trung vị 5.124/ngày vs 4 video không N選 824 (**6,2×**).
5. **CẤM chữ sợ trên tiêu đề**: `年金・貧乏・破綻・後悔・失敗・不安・衝撃・残酷・地獄・末路` (đã có sẵn `fear_words` trong config,
   cần nối vào prompt). 4/4 video ≥11 ngày có chữ sợ đều ≤455 view/ngày.
6. **CẤM từ nhạt**: `おすすめ・人気・有名・最古級` (cặp `_G9s` 2.894 vs `LGoe` 1.580 cùng đề tài).
7. **CẤM lộ kết cục/trấn an trên tiêu đề** (`それでも人生は終わらなかった`, `実は贅沢なほど自由な老後生活` — cả hai ~1,1×).
8. **Mọi vế phải grep được trong `script.txt`**; vế bị script phủ nhận thì bỏ. Cực cấp (`最強`/`一流`) được phép không có
   trong script **chỉ khi** danh sách trả đủ phần thưởng — đây là ngoại lệ đo được của kênh mẫu, không phải tự do bịa.

### 3.4 Cách chạy
- Đã có 20 đề xuất tiêu đề sẵn (2/tập) trong `our_eps`, **mỗi vế đã được research grep trong script** kèm mốc giây.
  → Rẻ nhất và chắc nhất: **dùng `title-ask`** đưa 2 ứng viên đó + 1 bản Fable tự viết cho Sol chọn, thay vì chạy S2 từ đầu.
- Bơm `{title_intel}` đã tự động (9 prompt) — chỉ cần lane có `title_rules` thật.

## 4. MÔ TẢ — phương án (số liệu tôi đo hôm nay, 10 video kênh mẫu)

| Đặc điểm | Kênh mẫu | Khuôn tool đang dùng cho lane G (kế thừa satori) |
|---|---|---|
| Độ dài | **247–508 ký tự** (trung vị 365) | 3–4 đoạn × 3–5 câu ≈ 700–1.100 ký tự |
| Ngôi kể | **ngôi 3 giới thiệu nội dung** ("66歳の男性が…教わります") | ngôi 1 của nhân vật (bà cụ) |
| Hashtag | **0/10** | có (`#a #b`) |
| Timestamps | **0/10** | có khối Timestamps |
| Khối credit/nguồn | **0/10** | có |
| Câu cảm ơn/CTA cuối | 1/10 | có |
| Nhắc `60代/65歳/老後/定年後` | **10/10** | không bắt buộc |
| Cụm `今回の漫画では` | 6/10 | không có |
| Liệt kê 3+ câu trong 「」 | 7/10 | không có |

**Khuôn mô tả đề xuất cho lane G (4 khối, 250–420 ký tự):**
```
① Câu hỏi/nghịch lý mở — lấy Ý từ hook 0–30s (không chép nguyên văn)
   vd: 定年後、毎日が自由になったはずなのに、なぜか疲れる。そんな感覚はありませんか？
② 1 đoạn giới thiệu: tuổi + đã hưu bao lâu + gặp ai + học được gì
   vd: 定年退職して1年、66歳の男性。公園で出会った老人から、定年後を心地よく生きる「ちょうどいい生き方」を教わります。
③ 1 dòng liệt kê các mục bằng danh từ ngăn 、 (đúng 5 mục của tập, không spoil hạng 1)
   vd: 夫婦関係、元同僚との付き合い、趣味、人間関係、孤独との向き合い方。
④ 1 câu chốt: đối tượng + "5つの…を漫画で紹介します"
```
**Bỏ hẳn** (vì kênh mẫu 0/10 dùng): hashtag · Timestamps · khối credit · CTA cảm ơn dài.
→ Cần khai riêng trong `config\lanes\teinengo-tanoshimi.json`: `doan_spec`, `pov_note`, `desc_doan_range: [3,4]`,
`tieu_de_keywords_line: false`, `desc_fixed_blocks: []`, và tắt khối Timestamps/hashtag cho lane này.

## 5. TAGS — phương án

**Đo thật kênh mẫu: chỉ 3–5 tag/video** (không phải 30–40 như các lane khác), toàn tag ngắn 2–6 ký tự:
`シニア漫画` (4/10) · `シニア` (3/10) · `定年後` · `シニアライフ` · `孤独` · `老後の楽しみ` · `一人旅` (2/10 mỗi tag) ·
rồi `老後の過ごし方`, `定年退職`, `老後趣味`, `暇つぶし`, `夫婦関係`, `シニア旅行`, `60代`, `年金生活`…

**2 lựa chọn — cần anh quyết:**
- **(A) Bám kênh mẫu:** 4–6 tag ngắn/tập = `シニア漫画` + `定年後` + 2–3 tag theo đề tài tập. Rẻ (0 LLM), giống hệt kênh mẫu.
- **(B) Chạy bước T (TAG v3) như lane A/D:** 30–40 tag lấy từ video đối thủ thật, ô ~500 ký tự. Tốn Sonnet+Opus mỗi tập,
  và **lệch hẳn kênh mẫu**.

Tôi đề xuất **(A)** cho 10 tập đầu: kênh mẫu 6.360 sub sống bằng tiêu đề + thumbnail chứ không bằng tag; cấu hình
`tags` hiện tại (`stuffing_tags: 40`, `max_chars: 500`) đang kế thừa satori nên nếu chạy (B) thì phải sửa ngưỡng trước.

## 6. THUMBNAIL — phương án

Khuôn `bands_manga` đã dựng và pilot ep09 được Opus chấm **45/45**. Đối chiếu `title_intel` có 5 điểm chưa ép —
**đã ép đủ cả 5 lúc 12:2x ngày 24/09** (xem cột "Đã làm"); bản ep01 vòng 1 (11:41) là bản CHƯA ép, giữ ở
`E:\CLAUDE\YOUTUBE\h2devssets	einengo-tanoshimi\ep01-asa-shukan
esearch	humb
ound1\` để đối chiếu:

| # | Luật đo được ở kênh mẫu | Khuôn trước 24/09 12:00 | Đã làm (24/09) |
|---|---|---|---|
| 1 | Băng đen trên **lấy ≥1 chữ nội dung của tiêu đề** (17/20; 3 video không lấy đều thua) | không ràng buộc | RULE 1 trong `content_strategy.row_schema[top].description` + mục 2b của `fable_review.criteria`; Fable phải khai đã mượn chữ nào trong `rationale` |
| 2 | Cụm **ĐỎ** = **lời khen/cực cấp/sự thật ngược thường thức** (最強の/最高の/共通点); tô đỏ chữ sợ là nhóm thua | renderer có `accent_color` nhưng luật chưa nói | RULE 2 trong `row_schema[shock]` + 2b: đỏ mà là mất mát/bệnh/tăng cân/thiếu tiền/hối hận = FAIL, đẩy xuống nhãn vàng hoặc bong bóng |
| 3 | Video xếp hạng **hiện các hạng dưới, GIẤU hạng 1** (4/4 video thắng dạng xếp hạng) | chưa có | RULE 3 trong `row_schema[lead]` + mục 2 của criteria (CẤM 第1位) |
| 4 | Bong bóng thoại **TRẮNG oval DỌC** (16/20) | renderer vẽ hộp bo góc **NGANG** | `thumbnail_engineands_manga.py::MangaBandsRenderer._bubble` vẽ ellipse + chữ xếp dọc phải→trái, chốt `bh ≥ 1,25·bw`, đuôi vẽ trước oval đè lên, và **tự nhường sang bên kia khi trùng dải cao độ với nhãn vàng** |
| 5 | Bong bóng/nhãn ghi **sự thật cụ thể hoặc mục ngược thường thức** (片道2万, 11席だけ, 孤独な生活, 肉を食う), không phải tính từ chung | chưa ép | RULE 5 trong `row_schema[lead]` và `row_schema[quote]`: tính từ cảm xúc chung (すごい効果/幸せな朝/意外な事実) = FAIL |

Giữ nguyên (đã đúng): thanh đen 0,21 H · chữ trắng + cụm vàng · dòng chốt ĐỎ viền trắng · ≥2 khung manga · ≥1 mặt thư thái.

## 7. Thứ tự làm 10 tập (theo `priority` của research)

| Ưu tiên | Tập | Lý do | Khung tiêu đề |
|---|---|---|---|
| **cao** | ep01-asa-shukan | video ĐÃ dựng xong, chỉ thiếu gói đăng; hook tốt nhất lane | F3 |
| **cao** | ep06-muryo-sanpo | lời hứa gãy nặng nhất (3/4 vế tiêu đề không có/bị phủ nhận) — phải đổi tiêu đề trước khi dựng | F2 |
| **cao** | ep09-toshokan | đã có thumbnail pilot; hook tốt thứ 2 | F1 |
| vừa | ep02, ep03, ep05, ep07, ep08, ep10 | lỗi vừa (tiêu đề có vế 0 lần trong script, trùng câu giữa các tập) | F1/F2/F3/F4 |
| thấp | ep04-yugata-suimin | chỉ lỗi nhẹ | F4 |

⚠ Research còn chỉ ra 2 lỗi **thuộc kịch bản**, không sửa được bằng gói đăng: ep08 mâu thuẫn tuổi trong script
(65歳 ở 43,7s vs 「三宅は俺の同期で、66歳だ」 ở 201,6s) và ep03↔ep06 trùng gần nguyên văn câu đồng nghiệp đau gối
(~92s cả hai). Cần báo h2dev sửa script trước khi dựng.

## 8. Việc phải làm trước khi chạy tập đầu (0 đồng, ~30 phút)

1. Viết `title_rules` lane G (§3.3) + đổi `title_target_chars`/`title_max_chars` → 40/45 + nối `fear_words` vào prompt.
2. Viết `doan_spec`/`pov_note`/`desc_*` lane G (§4) — tắt hashtag/Timestamps/credit.
3. Chốt phương án tags (A) hay (B) (§5).
4. Bổ sung 5 luật thumbnail (§6) vào `content_strategy` + `fable_review.criteria`; sửa bong bóng thoại sang oval dọc.
5. Viết `docs\lanes\teinengo-tanoshimi\SOP_TIEU_DE_THUMBNAIL_2026-09-24.md` (luật bắt buộc mỗi lane 1 SOP).

Sau đó mỗi tập: `title-ask` (chọn tiêu đề từ 2 đề xuất research + 1 bản Fable) → `emit` → `thumb` → `sol-check` →
`thumb-publish` → `sheet-publish`. Chi phí mỗi tập ≈ 3 ảnh gpti2 + 2–7 lượt Sol + 1–2 lượt Opus ≈ 8–15 phút.

<!-- export 953dd0827336 · 2026-09-26 -->
