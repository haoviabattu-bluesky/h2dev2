# 07 WORKFLOW — E-70dai-kenko · kenko-chiebukuro

> Lane `kenko-chiebukuro`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# Lane E `kenko-chiebukuro` — 健康の知恵袋 (@70dai-kenko)

| | |
|---|---|
| Ngách | sức khoẻ người 65–85 Nhật, video N選 đếm ngược, giọng kiểu bác sĩ (です・ます, ngôi 2) |
| Kênh mẫu | シニアいきいき健康 `UCBODlDy5sXo_49pC7KPr7vQ` |
| Sheet | tab `E-70dai-kenko`, khớp dòng theo cột C (`sheet_match: path`) |
| Tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep<nn>-<slug>` |
| Giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<nn>-<slug>` |
| Config | `config\lanes\kenko-chiebukuro.json` + `config\lanes\kenko-chiebukuro.thumb.yaml` (layout `stack_left`, PILOT) |
| SOP | `docs\lanes\kenko-chiebukuro\SOP_TIEU_DE_THUMBNAIL_2026-09-24.md` |
| Dữ liệu kênh mẫu | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\kenko-chiebukuro.json` (27 video) |

## Quyết định (2026-09-24, anh duyệt phương án)
1. Mở lane, ep01 làm tập pilot; ep02–08 chờ h2dev viết lại kịch bản.
2. Chữ thumbnail 4–10 ký tự/dòng (không phải 5 như khuôn h2dev cũ).
3. Mô tả liệt kê 第5位→第2位, giấu 第1位.
4. Tag: đối thủ lấy từ search (bước T), kênh mẫu là nguồn chính; chưa có danh sách kênh đối thủ riêng.

## Nhật ký
- 2026-09-24: tạo config + khuôn thumbnail `stack_left` (renderer mới) + SOP; chạy `run` ep01.

---
## PHUONG_AN_GOI_DANG_2026-09-24.md

# LANE E `kenko-chiebukuro` (tab Sheet `E-70dai-kenko`, kênh 健康の知恵袋 @70dai-kenko) — PHƯƠNG ÁN TIÊU ĐỀ · MÔ TẢ · TAGS · THUMBNAIL

Viết 2026-09-24 cho anh duyệt. Chỉ nghiên cứu + đề xuất: **chưa sửa code, chưa gọi model, chưa ghi Sheet.**
Kênh mẫu: シニアいきいき健康 `UCBODlDy5sXo_49pC7KPr7vQ` (27 video, 2.080 sub, 312.806 view — đo 2026-09-23).

## 1. Hồ sơ đã gửi đến cho lane E — kiểm kê

| # | Hồ sơ | Đường dẫn | Tình trạng / dùng cho |
|---|---|---|---|
| 1 | **title_intel** (máy đọc, đủ 27 video): 5 công thức F1–F5, 7 cặp thắng/thua, 6 kiểu thua, thumbnail 27/27, hook, 8 nguyên tắc, `our_eps` (2 tiêu đề đề xuất/tập) | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\kenko-chiebukuro.json` | **Nguồn chính.** Pipeline tiêu đề đã có code tự bơm file này vào S2/S3/S3c/S7/S8 (`E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\title_intel.py`) — chỉ thiếu config lane |
| 2 | Báo cáo hook + gói đăng lane E/F/G (có ảnh) | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\HOOK_AUDIT_LANE_EFG.md` (+ `.html`) | Bản người đọc của #1 |
| 3 | 27 thumbnail + 27 transcript kênh mẫu | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\E_kenko\{thumbs,transcripts}\` | Kiểm chứng, đo thumb DNA |
| 4 | Hook library (kiểu hook lane E) | `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\seed_2026-09-23_kenko.json` | Việc của h2dev (hook), dùng ở đây để kiểm "1 lời hứa ở 4 chỗ" |
| 5 | CHANNEL_DNA 20 video + TAG_STATS (tag thật của kênh mẫu) | `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\ikiiki-kenko\{CHANNEL_DNA.md,TAG_STATS.json}` | Khung kịch bản, tag |
| 6 | Hồ sơ TRENDING cũ (17 video, 3 transcript) | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneE_from_research\` | Cũ hơn #1, chỉ tham khảo |
| 7 | SOP lane E (63 KB) + profile | `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_E.md` · `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\kenko-chiebukuro.json` (khối `thumbnail`, `goi_dang`) | Khuôn thumbnail cũ 4 tầng, gate gói đăng |
| 8 | Lane profile TRENDING (draft) | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\70dai-kenko\lane_profile.yaml` | `watch_channels.json` **rỗng** — bước tag v3 cần đối thủ, xem §5 |
| 9 | Biên bản dọn lane E | `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\_DON_DEP_2026-09-23.md` | Đã xoá mọi thứ sinh từ kịch bản cũ (giọng, ảnh, video, tiêu đề) |

**Thiếu:** không có `thumb_dna.json` cho lane E (lane G/sengoku có, lane E chưa); không có `config\lanes\kenko-chiebukuro.json`/`.thumb.yaml`/`docs\lanes\kenko-chiebukuro.md` trong YT-TITLE-RESEARCH; mô tả đầy đủ của kênh mẫu chưa ai lưu (em vừa đọc 3 video thắng qua yt-dlp — §4).

## 2. Tình trạng 8 tập (Sheet `E-70dai-kenko`, đọc 2026-09-24)

Cột E/F/G trống cả 10 dòng. Kịch bản quyết định tiêu đề (luật: mọi vế tiêu đề/chữ thumbnail phải có trong `script.txt`), nên:

| Tập | Kịch bản | Làm gói đăng được chưa |
|---|---|---|
| `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep01-tento-kossetsu` | **Đã viết lại** 2026-09-23 23:10 (Sol 5 vòng), hook khoá 23:37, 90/90 ảnh máy 2 xong | **Được — tập pilot** |
| ep02 → ep08 (cùng thư mục cha) | Chỉ bỏ dòng タイトル (23:24); _DON_DEP ghi "sẽ viết lại theo khuôn kênh mẫu" | **Chưa** — làm bây giờ là làm trên kịch bản sắp bỏ |

⚠ `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_E.md` đầu file còn **⛔ NỢ QUY TRÌNH hook video** (chưa ai làm) — việc của h2dev, nhưng chặn cả việc dựng ep01.

⚠ Đề xuất tiêu đề ep01 trong `our_eps` được viết trên **kịch bản CŨ** — em grep lại trên kịch bản mới: 「70歳以上」「70代」「近所のお店」「ご存知」 = **0 lần** → 2 đề xuất đó nay trượt cổng lời hứa. Dữ kiện có thật trong ep01 mới: 腕が細く 3 · 年のせい 2 · 転ぶ前 1 · 食卓 3 · 五つの工夫 · 第五位 たんぱく質 → 第四位 ドライプルーン (「少し意外かもしれませんが」) → 第三位 乳製品 → 第二位 小魚 → 第一位 納豆.
Kịch bản mới vẫn còn câu tự tháo đếm ngược 「この順位は番組の構成によるもので…」 ngay sau lời hứa N, và lời hứa N nằm ở ký tự ~1.540 (≈5 phút ở 290,9 chữ/phút; kênh mẫu ~65 giây) — báo h2dev, không sửa ở đây.

## 3. TIÊU ĐỀ — phương án

**Công thức (đo đủ 27 video, xếp theo view/ngày video ≥11 ngày):**

| Mã | Khuôn | Bằng chứng | Dùng cho |
|---|---|---|---|
| **F1** | `70歳以上の方へ：長寿者が密かに続けていたN つの食品が〇〇を防いでいた` — chép cách người đã thắng, thì quá khứ | 3.342 · 2.446 · 1.566 view/ngày | tập "món TỐT" đếm ngược (ep01, ep08) |
| **F2** | `ご注意ください：Nつの一見体に良さそうな食習慣が、密かに筋肉を削り続けています` — lật nỗ lực người xem đang tự hào | 1.762 · 820 · 719 | tập "tưởng tốt hoá hại" (ep03) |
| **F3** | `〇〇で悩む方へ。意外な部位で夜中の回数を減らす方法` — đối tượng theo triệu chứng | 3.069 (video top kênh) | ep05 tiểu đêm, ep02/ep06 |
| F4 | tuổi lẻ + giới + chữ sinh tử đo được (`87歳の壁が男性だけを襲う`) | 619, mới 1 video | ep09 nếu có số thật |
| F5 | `実は、〇〇を毎日足すだけで…【9割が知らない裏技】` | 413 | chỉ tập 1 món, KHÔNG dùng cho list 5 |

**Luật cứng đề xuất cho `title_rules` lane E** (rút từ kiểu thua):
1. Mở bằng đối tượng hoặc nhãn (`70歳以上の方へ：` / `ご注意ください：` / `〇〇で悩む方へ`) — 7/8 video thắng.
2. Chủ ngữ là **vật cầm được** (món, bộ phận, số), không danh từ trừu tượng (兆候/だるさ/見落とし/未来 → 0/8 thắng).
3. **Không rào** (可能性/知っておきたい/かもしれない/見られた/検討したい → 0/8 thắng; rào để trong lời + mô tả). Của mình 4/8 tập đang rào.
4. **Không thuật ngữ** (抗炎症, 認知機能, 百寿者, 抗コリン → 0/8 thắng).
5. Một chiều (hại HOẶC tốt), không "3 món hại + 3 món tốt".
6. 35–55 ký tự (thắng 33–51). Của mình 7/8 đang 20–31 → quá ngắn.
7. Chữ số (5つ, 70歳) theo luật số của tool; mọi vế grep được trong `script.txt`.
8. Không bê khẳng định phóng đại của kênh mẫu (「卵の11倍」「3ヶ月で」) — luật claim y tế.

**Ứng viên ep01 (trên kịch bản mới, đã grep — đưa vào `title-ask`, không dùng thẳng):**
- F2: `ご注意ください：腕が細くなったのは「年のせい」ではありません——転ぶ前に食卓で見直したい5つの工夫`
- F1-biến thể: `転ぶ前に食卓へ：骨と筋肉を支える5つの工夫——第4位は少し意外な、あの食品でした` (40 ký tự — hơi ngắn; 「果物」 0 lần trong script nên không dùng)
(Chữ đối tượng 「70歳以上の方へ」 muốn dùng thì h2dev thêm 1 câu vào hook — hiện 0 lần.)

**Thứ tự làm tập** (research xếp theo đề tài có trần cao): ep08 長寿 → ep03 タンパク質–腎臓 → ep05 夜間頻尿 → ep01 → ep02 → ep06 → ep04, ep07 (trí nhớ thua 2/2 ở kênh mẫu).

## 4. MÔ TẢ — phương án (đo thật 3 video thắng kN6w/JCyx/4Q0f qua yt-dlp hôm nay)

Khuôn kênh mẫu, cả 3 video giống nhau:
1. **Câu 1–2 = lời hứa / cảnh của hook** (kN6w: 「100歳を超えた方々が毎日食べていたのは…ごく普通の食材だったのです」; JCyx: cảnh thức dậy đi tiểu đêm). → Chính là "1 lời hứa ở 4 chỗ".
2. 2–3 đoạn: cơ chế bằng lời thường + "không phải lỗi của bạn / không cần TPCN đắt" + hứa cách làm cụ thể.
3. `📌 今回ご紹介するNつの食品` — kN6w **liệt kê cả 第9位→第1位** trong mô tả (vẫn thắng lớn nhất kênh).
4. `💬` câu hỏi comment 1 chữ (「長寿」) · `👍` like/sub + **"LINEでシェア"**.
5. `⚠️【免責事項】` — một khối cố định, nhắc かかりつけの先生.
6. 15 hashtag cuối.

Đề xuất cho lane: `desc_fixed_blocks` = khối 💬/👍 LINE/⚠️免責 (giống cách lane D dùng); S4 Opus viết câu đầu = lời hứa tiêu đề (prompt đã có gợi ý này từ 2026-09-24). **Anh quyết:** có liệt kê tên món (kể cả 第1位) trong mô tả như kênh mẫu không — em nghiêng về **liệt kê 第5位→第2位, giấu 第1位 bằng 「第1位は動画でご確認ください」** cho khớp nguyên tắc giấu 第1位 của thumbnail/hook.

## 5. TAGS — phương án

Kênh mẫu dùng **18 tag**: ~9 tag chung lặp mọi video (`高齢者の健康` 19/19 video, `健康長寿` 17/19, `シニアの食事`, `老後の健康管理`, `長寿の秘訣`, `予防医学`, `60代70代健康`…) + ~9 tag riêng của đề tài (`ふくらはぎマッサージ`, `サルコペニア予防`, `鮭缶の栄養`…). Cộng 15 hashtag trong mô tả.

Pipeline tag v3 của tool (`E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\tags.md`) lấy tag từ video đối thủ thật — hợp với ngách này, chỉ cần: config lane + danh sách kênh đối thủ (hiện `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\70dai-kenko\watch_channels.json` **rỗng**; tối thiểu điền kênh mẫu). Tag ghi cột F khi PASS.

## 6. THUMBNAIL — phương án

Kênh mẫu (27/27 đo được): **nền đen, 4 dòng chữ trái (cam/trắng/đỏ/xanh lá), 1 ảnh món thật bên phải**; dòng 1 = đối tượng/tuổi, dòng 2–3 = món **bị giấu** (「この食品」「「これ」が」「〇〇するだけ」) hoặc hậu quả, dòng 4 = lợi ích/lệnh. Ảnh là **mục GIỮA danh sách, không bao giờ 第1位**; tên món không viết ra ở 6/6 video thắng. Gói lệch (chữ/ảnh nói chuyện khác video) là nguyên nhân thua 4/6.

**Chỗ lệch với khuôn đang có trong profile h2dev** (`kenko-chiebukuro.json` → `thumbnail`):
- Profile ép `max_chars: 5`/dòng; kênh mẫu 6–10 ký tự/dòng (「100歳まで元気な人」9, 「毎日食べていた」7, 「医師も驚いた」6), chữ chiếm ~60% khung. 5 ký tự không viết nổi 「この食品」+ hậu quả → nên nới lên ~9 và đo lại tỉ lệ phủ.
- Profile chưa có luật "giấu tên, mục giữa, không 第1位".

**Ep01 gợi ý:** ảnh = ドライプルーン (第4位, "少し意外", rẻ, dễ nhận ra bằng mắt nhưng người xem khó gọi tên ngay) + chữ giấu bằng 「これ」; mọi dòng phải grep được trong kịch bản.

**Đường làm trong tool:** đo `thumb_dna.json` bằng máy từ 27 ảnh ở §1 #3 (công cụ đo đã có từ lane G) → `lane-init` sinh `kenko-chiebukuro.thumb.yaml` → `lane-pilot` ep01 (tốn gpti2, hỏi trước) → anh xem `research\XEM.html` → `lane-lock`.

## 7. Việc cần làm để mở lane trong YT-TITLE-RESEARCH (chưa làm)

1. Đo thumb DNA 27 ảnh → `thumb_dna.json` (0 LLM).
2. `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\cli.py lane-init --profile kenko-chiebukuro --dna <thumb_dna.json>` → sinh config + thumb.yaml + docs lane.
3. Viết tay `title_rules` (§3), `sheet_tab: E-70dai-kenko`, `sheet_match: path` (cột C chứa đúng đường dẫn tập), `slug_root`, `deliver_root: E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro`, `desc_fixed_blocks` (§4), `fear_words` (đề xuất KHÔNG cấm 要注意/放置厳禁 — là nhãn thắng của kênh mẫu).
4. Viết SOP lane: `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\lanes\kenko-chiebukuro\SOP_TIEU_DE_THUMBNAIL_<ngày>.md`.
5. Chạy ep01: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\cli.py run --slug E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep01-tento-kossetsu --profile kenko-chiebukuro` → dừng ở XEM.html cho anh xem → `sheet-publish`.
6. ep02–08: đợi h2dev viết lại kịch bản.

## 8. Cần anh quyết
1. Mở lane E trong YT-TITLE-RESEARCH ngay với ep01 làm pilot, hay đợi h2dev viết lại xong cả 8 tập?
2. Nới `max_chars` thumbnail 5 → ~9 (khuôn h2dev đang chốt 5).
3. Mô tả: liệt kê hết món như kênh mẫu, hay giấu 第1位.
4. Danh sách kênh đối thủ cho tag v3 (ngoài kênh mẫu).

---
## SOP_TIEU_DE_THUMBNAIL_2026-09-24.md

# SOP TIÊU ĐỀ · MÔ TẢ · TAGS · THUMBNAIL — LANE E `kenko-chiebukuro` (健康の知恵袋 @70dai-kenko)

Mở lane 2026-09-24 (anh duyệt phương án `PHUONG_AN_GOI_DANG_2026-09-24.md` cùng thư mục). Kênh mẫu: シニアいきいき健康
`UCBODlDy5sXo_49pC7KPr7vQ`. Sheet tab `E-70dai-kenko`, dò dòng bằng cột C (đường dẫn thẳng vào thư mục tập h2dev).

## BƯỚC 0 — trước mỗi tập
1. Kịch bản đã được h2dev **viết lại theo khuôn kênh mẫu** chưa? (ngày 2026-09-24 mới có ep01; ep02–08 chỉ bỏ dòng タイトル,
   đang chờ viết lại — làm tiêu đề trên kịch bản cũ là phí, S3c sẽ bắt lỗi "vế không có trong kịch bản").
2. Dữ liệu kênh mẫu `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\kenko-chiebukuro.json` tự bơm vào S2/S3/S3c/S7/S8
   (có biên nhận `research\TITLE_INTEL_READ.json`). Mục `our_eps` viết trên kịch bản CŨ — đọc làm gợi ý, đừng tin phần "đã grep".

## Lệnh
```
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
py -3.13 -X utf8 cli.py run --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep01-tento-kossetsu" --profile kenko-chiebukuro
   → S0…S6 tiêu đề + mô tả → deliver (CHANEL\kenko-chiebukuro\<tập>) → tags (không ghi Sheet) → S7 thumbnail → S8 Sol → DỪNG
   → anh xem E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep01-tento-kossetsu\research\XEM.html
py -3.13 -X utf8 cli.py sheet-publish --slug "<thư mục tập>" --profile kenko-chiebukuro      # E tiêu đề · G Catbox · K trạng thái
py -3.13 -X utf8 cli.py tags --slug "<thư mục tập>" --profile kenko-chiebukuro --write      # cột F khi PASS
```
Thư mục giao hàng `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<nn>-<slug>` phải có sẵn (deliver dò theo đuôi tên tập, không tự tạo).

## Tiêu đề (luật đầy đủ trong `config\lanes\kenko-chiebukuro.json` → `title_rules`)
| Loại tập | Khuôn | Ví dụ kênh mẫu (view/ngày) |
|---|---|---|
| danh sách món TỐT / thói quen người sống thọ | F1 `70歳以上の方へ：…N つの食品が〇〇を防いでいた——ほとんどの方がご存知ない` | 3.342 · 2.446 |
| thói quen tưởng tốt hoá hại | F2 `ご注意ください：N つの一見体に良さそうな食習慣が、密かに筋肉を削り続けています——60代以上の方は必見` | 1.762 · 820 |
| 1 triệu chứng + chỗ xử lý bất ngờ | F3 `〇〇で悩む方へ。意外な部位ケアで…を減らす方法` | 3.069 |
35–55 ký tự (mục tiêu 46), đối tượng/nhãn ở đầu, chủ ngữ là vật cầm được, **không rào** (可能性/かもしれない…), không thuật ngữ,
một chiều, không lộ 第1位, không hứa chữa khỏi, chữ số Ả Rập. Mọi vế phải grep được trong `script.txt`.

## Mô tả
Khuôn đo trên 3 video thắng: câu đầu = lời hứa của hook → cơ chế → cách làm → 「📌 今回ご紹介する…」 (第5位→第2位, **第1位 giấu**:
anh duyệt) → xin bình luận 1 chữ → (tool nối) 👍 like + LINE → hashtag → (tool nối) ⚠️【免責事項】. Hai khối tool nối nằm ở
`desc_fixed_defaults` trong config lane.

## Tags
Bước T v3 (docs/tags.md) — tag lấy từ video đối thủ thật. Kênh mẫu dùng ~9 tag chung (`高齢者の健康` 19/19 video, `健康長寿`,
`シニアの食事`, `老後の健康管理`…) + ~9 tag riêng đề tài. Ngưỡng lane: `min_channels_eff 8`, `max_per_channel 3` (ngách ít kênh).

## Thumbnail — khuôn `stack_left` (ANH CHỐT 2026-09-24 sau pilot ep01)
- **Ảnh phải thể hiện ĐỦ các món/đồ vật trong video** (5 món thì đủ 5, mỗi món nhận ra ngay), **hoặc cụ bà khoẻ vui bên các món đó**.
  KHÔNG làm kiểu kênh mẫu "1 món giấu tên" (bản pilot đầu chỉ có mận khô / 1 cốc sữa — anh bác).
- **Chữ nói thẳng, không chơi chữ**: 転ぶ前に / 体にいい5つの食べ物 / 意外な効果 / 知らない人が多い (hoặc 実はすごい / 意外と知らない).
  Cấm câu đố có dấu hỏi, cấm cụm trừu tượng (必要なものが違う / 年だけじゃない).
- Bố cục: nền đen trái + 4 dòng cam/trắng/đỏ/xanh lá + ảnh bên phải. Số đo vị trí dòng: `thumb\DO_THUMB_KENH_MAU_2026-09-24.md`.
- Fable vẫn có thể viết chữ vòng vo dù luật đã ghi → anh/em soi lại; sửa chữ mà giữ ảnh nền: dựng lại bằng `StackLeftRenderer` trên
  `research\thumb\final_set\variant_X\background.png` (0 đồng gpti2), thay `final_set\thumbnail_X*.png` + cập nhật sha256 trong
  `thumbnail_set_manifest.json` (publish kiểm hash) — cách đã làm cho ep01, bản cũ ở `final_set\_ban_chu_fable_20260924\`.

## Bẫy
- Kênh mẫu **thắng dù có claim bịa** (卵の11倍, 10年分老化を防ぐ) — không chép.
- Kênh mẫu **liệt kê cả 第1位 trong mô tả** (kN6w) — lane mình giấu (anh chốt 2026-09-24), đổi lại nếu CTR/retention cho thấy khác.
- Khuôn thumbnail của h2dev (`profiles\kenko-chiebukuro.json` → `thumbnail.template`, `max_chars: 5`) là khuôn CŨ của h2dev; thumbnail lane E nay
  do tool này làm theo `kenko-chiebukuro.thumb.yaml` (4–10 ký tự/dòng như kênh mẫu).

<!-- export 762beca31b98 · 2026-09-26 -->
