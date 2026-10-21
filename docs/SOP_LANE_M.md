# SOP — LANE M: 定年後の穴場ノート【漫画】 (hưu trí Nhật, MANGA CHIBI ngôi 1 + xếp hạng 7選 VIỆC LÀM tuổi 60)

> Kênh mẫu: 大人の盲点【漫画でわかる人生の裏側】 (Điểm mù của người lớn) `@otonanomouten` · `UCsWLzQF-6knOsQlHYBNtvwg`
> (526 sub · 6 video · hit 92.034 view — đo 2026-09-26).
> Kênh của mình: **定年後の穴場ノート【漫画】** (Sổ tay chỗ hay ít người biết sau nghỉ hưu) `@teinengo-anaba` — anh TỰ setup (K2).
> Profile `teinengo-anaba` · thư mục = tab = giao hàng = `M-teinengo-anaba` (K1).
> Cửa vào: `docs/BAT_DAU_LANE/teinengo-anaba.md` (đọc trước). Lập 2026-09-26 (Giai đoạn 2), khuôn `SOP_LANE_G.md` + cơ chế khoá mặt xuyên tập của `SOP_LANE_L.md`.

| Anh nói | Profile | SOP |
|---|---|---|
| "hưu trí Nhật · manga list N選 vui/rẻ · Lane G" | `teinengo-tanoshimi` | `SOP_LANE_G.md` |
| "hưu trí Nhật · manga N選 việc làm thêm tuổi 60 · Lane M · 定年後の穴場ノート" | **`teinengo-anaba`** | **file này** |
| "hưu trí Nhật · manga kịch tính tiền · Lane F" | `teinengo-real` | `SOP_LANE_F.md` |

Nguồn nghiên cứu:
```
E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\GIAO_VIEC_OTONANOMOUTEN_2026-09-26.md   hồ sơ giao việc (verdict §4: nhân vật riêng, góc lợi ích + móc tiết kiệm, 18–24', mục đầu <4')
E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\otonanomouten\                          dữ liệu thô (comments.json · transcripts · thumbs · competitors.json)
E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\otonanomouten\
├── CHANNEL_DNA.md          K1+K2 6 video + bổ sung tay chữ thumbnail thật + đính chính
├── VIDEO_ANALYSIS\*.json   6 file — đầu vào K3 retrieve_videos.py
├── TAG_STATS.json
├── COMMENTS_TOP.md         53 bình luận xếp theo like
├── COMMENT_INSIGHT.md      ⭐ khối "## ĐƯA VÀO PROMPT" tự nhồi vào S2
└── _raw\transcripts.json + segments\*.json (CÓ mốc giây) — dùng đo gate
```

---

## 0. BẢNG DELTA — khác Lane G/L chỗ nào

| Khâu | Lane G (tanoshimi) | Lane L (shakai) | **Lane M (file này)** |
|---|---|---|---|
| Đề tài | lối sống VUI/RẺ | hiện tượng xã hội なぜ | **CHỈ việc làm tuổi 60** (K4) |
| Người kể | 俺 + mentor, đổi theo tập | ngôi 3 + Sakura | **俺 = 田島誠 63t CỐ ĐỊNH + vợ 春江 61t** |
| Cấu trúc | `manga_list` (mentor, mục cuối hướng nội) | `structure_block` 6 chặng | **`structure_block` xếp hạng 第7位→第1位, truyện ĐAN XEN, mỗi mục 5 phần (tên · số · ưu · bẫy · ai hợp)** |
| Mục đầu | 1.200–2.300 chữ | — | **750–1.150 chữ, trước phút 4 (K8)** |
| Cảm xúc | tò mò → phấn chấn | KÍCH → GIẢI TOẢ → VỊ THA | **KÍCH → GIẢI TOẢ → VỊ THA** (K6, `cung_cam_xuc` vắng = bật) |
| Khoá mặt | REF-LOCK trong tập | Sakura xuyên tập (`fixed_refs`) | **makoto + harue xuyên tập (`fixed_refs`)** + vai phụ theo tập (cast mode) |
| Giọng | clone kênh mẫu | đa giọng ai33 | **ĐA GIỌNG — 7 giọng clone từ video gốc (§0c)** |
| Thời lượng | 20' | 18' | **22'** |
| mode | story | fiction_facts | **fiction_facts** (lương giờ/chế độ phải có nguồn — K9) |

## 0b. CHANNEL ANALYZER — ĐÃ CHẠY 6/6 VIDEO (K1+K2), K3 chạy mỗi tập

K1+K2 chạy ở TRENDING-RESEARCH 2026-09-26 (6 video = toàn bộ kênh), copy về `docs\channel_dna\otonanomouten\`.
Bước vision K1b lỗi JSONDecodeError 6/6 → chữ thumbnail đã **đọc tay từ ảnh thật** (CHANNEL_DNA §BỔ SUNG TAY).
Kênh mẫu mới 6 video — **khi kênh ra thêm ≥4 video, chạy lại K1+K2** (`channel_analyzer.py`; nếu là kênh máy 2 đã làm thì cổng tự chặn, xem CLAUDE.md).

Mỗi tập (Giai đoạn 3 bước 2) chọn `competitor.txt` bằng K3 (0 LLM, 0 mạng):
```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 -X utf8 retrieve_videos.py --dna-dir ..\docs\channel_dna\otonanomouten --topic "<đề tài tập, tiếng Nhật>" --top 3
```
Ưu tiên video gốc ghi ở cột K sheet (§1b). Video VIỆC LÀM của kênh mẫu: `wG4fI9voims` (92k, 31 bl) · `TIoRmIZKkAg` (10k, 4 bl) ·
`SN2VjauDlJA` (6,6k, 1 bl) · `HvLbO2pqUcI` (1k, 0 bl — nguồn yếu). `do0n9Wirigs` (sở thích) và `vritvBsvYjc` (câu cửa miệng) KHÔNG
dùng làm video gốc (K4 — ngoài trụ cột).

## 0c. GIỌNG — ĐA GIỌNG, CLONE TỪNG NHÂN VẬT (anh duyệt 2026-09-26)

Kênh mẫu đọc MỖI NHÂN VẬT MỘT GIỌNG → Lane M chạy chế độ ĐA GIỌNG như Lane L (`voice.provider="ai33"`, `tts_voicevox.py`
nhánh ai33 đọc `vai.txt`; `gan_vai.py` ở máy 1 gắn vai từng câu; `script.gate.dialogue_own_sentence=true`).
7 giọng clone từ video gốc tập 1 `wG4fI9voims` (mẫu cắt tay đoạn 1 người nói, `remove_background`), anh nghe và duyệt CẢ 7:

| Vai | voice_id | Khai ở profile | F0 mẫu → clone |
|---|---|---|---|
| Người kể + ông 田島誠 (makoto) | `clone_2665004` | `voice.narrator` (+ `voice.id` cho calibrate) | 129 → 139 Hz |
| Vợ 春江 (harue) | `clone_2664998` | `voice.fixed_cast.harue` | 205 → 208 Hz |
| Cố vấn/案内役 | `clone_2664996` | `cast_bank` | 168 → 198 Hz (anh duyệt đạt) |
| Chủ nhiệm/quản lý cắt ca | `clone_2664997` | `cast_bank` | 151 → 162 Hz |
| Trưởng ca/đàn anh tử tế | `clone_2664999` | `cast_bank` | 152 → 145 Hz |
| Đồng nghiệp nữ lớn tuổi | `clone_2665001` | `cast_bank` | 216 → 208 Hz |
| Khách nữ nổi giận | `clone_2665002` | `cast_bank` | 239 → 232 Hz |

- Anh chốt: 井上 (đồng nghiệp nữ) và khách giận để **RIÊNG 2 giọng** dù âm sắc gần nhau.
- Nghe lại: `E:\CLAUDE\YOUTUBE\h2dev\assets\M-teinengo-anaba\_voice_clone\compare_clone.html` (mẫu gốc + clone từng vai).
- `characters.json` của tập: `voice: {voice_id}` lấy theo bảng trên. Vai mới không khớp loại nào → HỎI ANH trước khi clone thêm (K11).
- Tốc độ đọc: `calibrate.py --profile teinengo-anaba` đo giọng người kể = số KHỞI ĐIỂM; đo lại từ video thật ep01 (có nghỉ câu, đổi giọng).
- Bộ 9 giọng kho thử trước đó (`_voice_test\`) BỎ, không dùng.

## 0d. NHÂN VẬT — ảnh gốc lane (khoá mặt XUYÊN TẬP, K10)

| id | Nhân vật | Ảnh gốc | QC vision |
|---|---|---|---|
| `makoto` | 田島誠 (たじま まこと) 63t — cựu 総務 hãng văn phòng phẩm 38 năm, hết 再雇用 ở 63; tóc muối tiêu, kính gọng mảnh bạc, áo len vàng mù tạt, sổ tay xanh lá「穴場ノート」 | `assets\M-teinengo-anaba\_ref_kenh\makoto\001.png` (+ `full.png` toàn thân) | ~64/M ĐẠT |
| `harue` | 田島春江 (はるえ) 61t — part-time 品出し siêu thị 12 năm, có chính kiến, hiểu nghề part-time hơn chồng | `assets\M-teinengo-anaba\_ref_kenh\harue\001.png` | ~58/F ĐẠT |

- Ông vẽ bằng gpti2 **edit từ avatar kênh** (`branding\avatar_raw.png`) nên mặt khớp avatar; vợ vẽ edit lấy nét từ ảnh ông (bản vẽ text thuần lệch nét, đã bỏ).
- Cảnh thử 2 người cùng khung (gpti2 low, 2 ảnh nguồn): `_ref_kenh\_thu\canh_thu.png` — giữ mặt/kính/áo cả hai ĐẠT.
- Chi phí 5 ảnh thử: ≈2.070đ (ông 2×490 · vợ 430 bỏ + 490 · cảnh 170).
- Mỗi tập: `characters.json` kiểu CAST `{id, ref:true}` với id ĐÚNG `makoto`/`harue` → `make_video.masters_from_bible` tự chép ảnh gốc;
  vai phụ (quản lý, đồng nghiệp…) có master riêng của tập. ≤3 mặt khoá/ảnh.
- **CẤM vẽ lại ảnh gốc** sau khi tập đầu dùng. Cấm dùng 高瀬健一 / 恵子 / 「盲点だった。」 (K10).

## 1. QUYẾT ĐỊNH ĐÃ CHỐT (2026-09-26)

- `body.mode="ai_images"`, manga chibi (`image.style_suffix` có "full head of hair" + "five-finger hands" — khán giả kênh mẫu bắt lỗi hói kiểu Xavier).
- `script.flow="lean"`, `engine=claude_p`, `brain_model=claude-fable-5-1` (VIẾT 1 lần) · `patch_model=claude-opus-5` (VÁ) · Sol lens `plain` + `lane_rules`.
- `script.structure_block` (field-driven) — không dùng nhánh `manga_list` của Lane G (nhánh đó ép mentor + mục cuối hướng nội + "không kịch tính", trái K6/K8).
  ⚠️ `lean_script.budget_block` vẫn in câu "mỗi mục: … 案内役 giải thích …" cho lane dạng mục — ở lane này 案内役 = 春江/người tại chỗ làm; không sửa code.
- `outro_line` = 「最後までご覧いただき、本当にありがとうございました。少しでも参考になったら高評価とチャンネル登録で、また穴場ノートを一緒にめくってください。」
  (Cảm ơn đã xem đến cuối. Nếu có ích, hãy bấm thích và đăng ký kênh để cùng lật tiếp cuốn sổ chỗ hay) — đủ 3 ý K7.
- `cung_cam_xuc` / `cam_on_cuoi` / `review_may3` **cố ý VẮNG = BẬT**. Hook `video_sinh` + `sfx:true`, `goi_dang.enabled:true` (cổng S1L qua).
- `publish.listing_external=true` (TITLE-RESEARCH làm tiêu đề/mô tả/thumbnail), `title_auto=false` (kênh mới — anh `--bat` mới chạy).
- Ảnh tĩnh tuyệt đối (`assemble.zoom=1.0`). Nhạc nền không "ngớ ngẩn" (K11).
- `image.seconds_per_image=8.6` — **ĐO THẬT 2026-09-26** (skill `video-chuyen-canh`, video 92k `wG4fI9voims`): 218 cảnh/31,4' · trung bình 8,6 s (trung vị 9,3) · 95% cắt thẳng, 5% blur-in/xfade · Ken Burns ~1,01 (gần như đứng yên). Khung thật = manga bán thực + **bóng thoại chữ dọc không đuôi** (như Lane L); `黒田` là bà tóc bạc. **Bóng thoại BẬT (anh chốt 2026-09-26, bắt buộc):** `assemble.bubble` chép bộ số mức C của Lane L (không đuôi, chữ dọc, kể 72px / thoại 56px), `burn_subs=false` (mọi câu đã hiện trong bóng). Máy 2 vẽ ở B8 từ `voice_roles.json` + `img_faces.json` — máy 1 không làm gì thêm, ảnh vẫn cấm chữ/bóng.
- `source_lang="ja,en"` bắt buộc — thiếu thì B2 kéo phụ đề Hàn (ep01 lần đầu dính). competitor.txt ep01 dùng bản YouTube ASR `_raw` (tốt hơn whisper).

## 1b. 10 TẬP ĐẦU + CỘT SHEET TAB `M-teinengo-anaba`

Cột A→S theo cửa vào mục 6. Đã ghi A2:B11 (tựa Nhật + dịch) + K2:K11 (video gốc) 2026-09-26. **CHỈ tập anh chỉ định mới bắt đầu.**
**Thứ tự (anh chốt 2026-09-26): xếp theo VIEW video gốc giảm dần** — 92k (`wG4fI9voims`) → 10k (`TIoRmIZKkAg`) → 6,6k (`SN2VjauDlJA`) → 1k (`HvLbO2pqUcI`); cùng video gốc thì tập nào khớp sát lợi ích của hit hơn (ô chữ thumbnail 座れて快適/午後は自由, mô tả 接客が少ない, mục 開店前の品出し; bình luận top 14 like) lên trước.
Nguyên tắc: chỉ việc làm (K4) · góc LỢI ÍCH (thắng góc cảnh báo 2–5 lần) · bám hit 92k 「気楽に働ける…7選」 · thêm móc TIẾT KIỆM (0円 /
交通費0円 / 年金を減らさず) mà kênh mẫu chưa dùng · không trùng tựa kênh mẫu & Lane G · tiêu đề 41–50 ký tự (gate 40–56).

| STT | Tựa làm việc (dịch) | Video gốc |
|---|---|---|
| 1 | 【漫画】60代でも座って働ける穴場バイト7選｜資格なし・初期費用0円で始められる"無理なく続く仕事" (7 việc ngồi làm được, không bằng cấp, 0 yên vốn) | `wG4fI9voims` 92k |
| 2 | 【漫画】定年後に「週3日・午前だけ」で働ける穴場バイト7選｜午後は自由で体もラクだった (3 ngày/tuần, chỉ buổi sáng) | `wG4fI9voims` |
| 3 | 【漫画】人と話さなくていい60代の穴場バイト7選｜接客が苦手な元会社員でも続いた静かな仕事 (ít phải nói chuyện) | `wG4fI9voims` |
| 4 | 【漫画】朝2時間だけ働ける60代の穴場バイト7選｜早起きが得意な人ほど得をする仕事 (chỉ 2 tiếng buổi sáng) | `wG4fI9voims` |
| 5 | 【漫画】再雇用を断った63歳が見つけた穴場の仕事7選｜同じ会社に残るより毎日が軽くなった理由 (từ chối tái tuyển dụng) | `wG4fI9voims` |
| 6 | 【漫画】60代でもシフトを削られにくい穴場バイト7選｜月18日が11日に減った俺が見つけた安定する職場 (khó bị cắt ca — cú KÍCH 18→11 ca từ bình luận top) | `TIoRmIZKkAg` 10k |
| 7 | 【漫画】60代の再就職で採用される人が面接で必ず聞く7つの質問｜求人票に書いていない条件の確かめ方 (7 câu hỏi khi phỏng vấn) | `TIoRmIZKkAg` |
| 8 | 【漫画】事務・総務の経験がそのまま活きる60代の穴場の仕事7選｜元会社員の経験は武器になる (tận dụng kinh nghiệm văn phòng) | `TIoRmIZKkAg` |
| 9 | 【漫画】年金を減らさずに働ける60代の穴場バイト7選｜在職老齢年金で損しないちょうどいい稼ぎ方 (đi làm không bị trừ lương hưu) | `SN2VjauDlJA` 6,6k |
| 10 | 【漫画】家から自転車10分で通える60代の穴場バイト7選｜交通費0円で手取りが減らない仕事 (xe đạp 10 phút, 0 yên đi lại) | `HvLbO2pqUcI` 1k ⚠️ nguồn yếu |

## 1d. TẬP 1 `ep01-suwatte-anaba` — chạy thật 2026-09-26 (5 lượt B3, LOCK PASS 19:00, gửi máy 3)

| Lượt | Kết quả | Nguyên nhân → xử lý |
|---|---|---|
| 1 | ESCALATE | Hook khoá chứa thoại dính lời dẫn (「はい」とだけ答えた) trong khi lane bật `dialogue_own_sentence` → S3 đòi vừa chép nguyên văn hook vừa tách thoại. **Vá code** `hook_stage.check`: kiểm luật này ngay lúc khoá hook (field-driven). Khoá lại hook. |
| 2 | ESCALATE | Opus (claude -p, không đọc được file) được bảo "chép lại hook" mà không được đưa hook → bịa đoạn gần giống. **Vá code** `lean_script.do_tat_dinh`: việc HOOK kèm NGUYÊN VĂN hook. 6 việc lớp 3 (bám gốc ×4, lớn tiếng với vợ, CTA trùng) Opus làm đủ. |
| 3 | ESCALATE | Sol đòi "mỗi mục có lương giờ" (do lane_rules em viết) → Opus bịa 千二百円 → S3 bắt. Sửa lane_rules: lương từng việc CỐ Ý không nêu. |
| 4 | ESCALATE | lane_rules vẫn quá cứng (đòi giờ bắt đầu–kết thúc mọi mục) → patch Sol dài quá trần. Nới: ≥1 con số HOẶC điều kiện có nguồn. |
| 5 | **PASS** | Sol FIX→PASS→PASS · 7.527 chữ · 第七位 ở ~3,3' · D2 = `Chờ kiểm tra kịch bản` · ghi chú lớp 3 cho máy 3: `FlowHandoff_local\jobs\M-teinengo-anaba\ep01-suwatte-anaba\review\GHI_CHU_LOP3_MAY1.md` |

Bài học lane: (1) `lane_rules` là lệnh cho Sol — viết cứng quá là tự tạo vòng lặp; (2) hồ sơ tập cấm số nào thì lane_rules phải nói rõ cấm, kẻo Sol đòi và Opus bịa.

> ⭐ **2026-09-27 — Lane M chuyển sang CÁCH CHẠY CHUNG** (docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md §4b): bỏ vòng `review_may3.share` → BAO_CAO giả → D=Đã sửa → `--nhan`; thay bằng `soat_kb_gptweb.py --xong`. Tin lượt 1 lấy bối cảnh/cấu trúc/luật từ `script.soat_gptweb` trong profile (nội dung y như bản cũ). Lệnh ở mục C bên dưới thay tương ứng.

## 1e. SOÁT KỊCH BẢN BẰNG CHATGPT WEB THAY MÁY 3 (anh chốt 2026-09-26, TEST riêng Lane M)
Lane M KHÔNG chờ máy 3: sau LOCK, tab lane tự đưa kịch bản vào **đúng hội thoại anh chỉ định** trong Project ChatGPT
`M-teinengo-anaba` (Chrome `E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE`, cổng 9335, model `gpt-5-6`):
https://chatgpt.com/g/g-p-6ab7b6307fcc81918a542065f7c6cd85-m-teinengo-anaba/c/6ab7b795-063c-83ec-b11b-3c7f8cc99d7e

1. Lượt 1: bối cảnh kênh + RÀNG BUỘC CỨNG (số chỉ từ series_ctx, 7 mục, thoại tách câu, không quát vợ, ±5% độ dài) + kịch bản → GPT chấm + danh sách sửa (trích nguyên văn → câu thay).
2. Tab lane đọc từng mục: hợp lý → nhận; chưa hợp lý → phản biện có lý do; 1 lượt cuối để GPT chốt.
3. Tổng hợp thành `viec_tay.txt` (thay thế NGUYÊN VĂN) → `make_video --den B3G` (Opus vá → S3 → Sol ×2 → LOCK). Không sửa tay.
4. Ghi `BAO_CAO_SUA.md` vào `jobs\M-teinengo-anaba\<slug>\review\` → cột D = `Đã sửa kịch bản` → `review_may3.py --nhan`.
Công cụ (không tạo chat mới, dùng khoá + selector của `gpt_web_client`, link hội thoại ở `profile.script.soat_gptweb.url`): `E:\CLAUDE\YOUTUBE\h2dev\pipeline\soat_kb_gptweb.py` (`--lan1` tự dựng tin lượt 1 từ title/series_ctx/script; `--tin <file>` lượt tiếp); nguyên văn 2 lượt hỏi/đáp ep01 cùng thư mục.

**Ep01 (2026-09-26):** GPT chấm 8,6/10 (hook 9,2). Nhận 9 sửa: rút câu giới thiệu nhưng GIỮ 4 lời hứa tiêu đề · đưa tên hạng 4 lên trước chuyện 柳瀬 · cắt mạnh đoạn 在職老齢年金 · thay gag găng tay (giống kết video gốc) bằng callback tờ lịch · 湿布 callback ở hạng 7 · 「また、都合のいい数字だけ見ていた」 ở hạng 5 · đóng khung giờ làm là "tin tuyển dụng này" · bỏ khái quát 保護者 · bỏ 「ずっと椅子だ」. Phản biện thắng 2: giữ 「倉庫に騙された」 (nấc trước trưởng thành) và giữ lời hứa tiêu đề. Sol bắt thêm: lời hứa 初期費用0円 vs 年会費, giới hạn 月10日 chỉ của シルバー, hạng 1 thiếu ai hợp/không hợp, tiêu chí xếp hạng, xác nhận có ghế ở hạng 1/3. Bản khoá cuối **7.684 chữ**, sha a42dfcb1aa…, 第七位 ở ~3,4'.

**Bẫy đã trả giá (lượt 8):** bài vượt TRẦN ngân sách 32 chữ → S3 ra việc `NÉN: rút 595–743` (tính về ĐÍCH chứ không về trần) → Opus nén cả bài, **xoá luôn dữ kiện [D7] 二十時間以上** và mọi câu "có ghế" → Sol quay ra bắt "hạng 1 không xác nhận ngồi". Xử: khôi phục bản trước patch (`script.pre_patch1.txt`), nâng `target_minutes` 22→23 (vẫn trong 18–24'), chạy lại chỉ với việc thay thế nguyên văn. **Luật: bản soát bổ sung nội dung thì kiểm độ dài dự kiến < trần TRƯỚC khi chạy; đừng để S3 tự nén.**

**Bẫy chờ GPT treo (vá 2026-09-30, ep04):** hội thoại soát của lane là 1 hội thoại CỐ ĐỊNH dùng cho mọi tập → rất dài → ChatGPT chỉ
render vài tin cuối, nên `gpt_web_client._wait_answer` (đếm số khối trả lời trên DOM) không bao giờ thấy "tin mới" và treo tới 2 giờ dù GPT
đã trả lời. Đã thay bằng `pipeline\gptweb_pool.py::_cho_tra_loi` (đọc backend `/backend-api/conversation` tìm trả lời cho ĐÚNG tin mình gửi
+ fallback DOM đổi chữ; đo thật nhận ra sau 22 giây). Nếu vẫn treo: `soat_kb_gptweb.py --doc` chỉ đọc, KHÔNG gửi lại.

**Ep04 `ep04-asa-2jikan` (2026-09-30):** GPT 8,7/10 (hook 9,2) · nhận 10/12 + phản biện thắng 2 (không đổi tiêu đề ở chặng KB — đề xuất
「朝2〜3時間」 ghi trong `soat_gptweb\BAO_CAO_SUA.md` cho khâu tiêu đề; giữ cảnh kho hàng vì cắt là rơi dưới sàn độ dài) · khoá 6.833 chữ sha 89b90a2374.

**Ep02 `ep02-shuu3-gozen` (2026-09-26, giao máy 2 23:25):** 7.863 chữ, sha 2c30c7fdce · GPT 8,8/10 (hook 9,3), nhận cả 9 góp ý, không cần phản biện ·
8 vai CAST (+ 大村館長, 榊係長, 佐伯, 送迎運転手, 西野; 柳瀬 dùng lại master ep01) · 171 prompt · hook 4 cảnh gộp theo câu, 4 clip Grok PASS.
Bẫy mới: (1) Sol bắt mãi 1 lỗi cấp TIÊU ĐỀ (「体もラクだった」 thì quá khứ) sau khi mọi lỗi nội dung đã sửa → khoá tay theo luật lean "FIX nhiều vòng, không REMAKE"
(`gate_common.ghi_lock(d,'PASS',...)` + `review_may3.share` → BAO_CAO_SUA.md → D=Đã sửa → `--nhan`); bản khoá = bản trước patch Sol vượt trần.
(2) Grok free clip **10 giây → 429** (mất 3 tài khoản) — giữ **6 giây**, cảnh dài hơn thì `ghep_hook_noi_truoc` tự giãn chậm.
(3) Mỗi cảnh hook phải khớp RANH GIỚI CÂU (hook_timeline theo số câu): storyboard cắt giữa câu → gộp lại thành 4–5 cảnh.

## 2. LỆNH CHẠY — "chạy tập X" = làm HẾT máy 1 rồi giao máy 2 (anh chốt 2026-09-26)
⭐ **30/09 anh chốt — THAY dòng gạch dưới:** khoá xong là DỪNG, giao máy 3/anh soát (bỏ bước C); nhận + làm tiếp theo
`E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` rồi từ bước D.
~~Không dừng chờ máy 3: kịch bản khoá xong thì tab lane tự soát bằng ChatGPT web (§1e) và đi tiếp tới đóng gói.~~
```bat
cd E:\CLAUDE\YOUTUBE\h2dev
:: A. HỒ SƠ (tay, tab lane) — thư mục assets\M-teinengo-anaba\epNN-<slug>\, ghi cột C sheet ngay
::    competitor.txt (transcript video gốc cột K) · series_ctx.txt (SỐ ĐƯỢC PHÉP + [Dn] có URL chính thức + QUY ƯỚC:
::    7 việc BẮT BUỘC có tên, KHÁC danh sách các tập trước; tình tiết mới, không lặp tập trước) · title.txt = cột B · promise.txt
:: B. VIẾT + KHOÁ (Fable viết hook+thân, Opus vá, Sol ×2) — tự dừng, ghi D = "Chờ kiểm tra kịch bản"
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-anaba --slug epNN-<slug> --den B3G
:: C. SOÁT CHATGPT WEB (thay máy 3, §1e): lượt 1 → tab lane thẩm định → (phản biện 1 lượt) → viec_tay.txt
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-anaba --slug epNN-<slug> --lan1
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-anaba --slug epNN-<slug> --tin <file phản biện>
::    viết viec_tay.txt (thay thế NGUYÊN VĂN, ước lượng độ dài < trần) → ghi_lock ESCALATE → chạy lại B
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common;from pathlib import Path;gate_common.ghi_lock(Path('assets/M-teinengo-anaba/epNN-<slug>'),'ESCALATE',reason='soat ChatGPT web')"
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-anaba --slug epNN-<slug> --den B3G
::    lớp 3 đọc bản khoá → BAO_CAO_SUA.md vào FlowHandoff_local\jobs\M-teinengo-anaba\epNN-<slug>\review\ → D = "Đã sửa kịch bản"
py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile teinengo-anaba --slug epNN-<slug>
:: D. CAST + GIỌNG: characters.json (makoto/harue + vai phụ, voice_id từ cast_bank, look khác nhau rõ) →
py -3.13 -X utf8 pipeline\gan_vai.py --profile teinengo-anaba --slug assets\M-teinengo-anaba\epNN-<slug>
:: E. PROMPT ẢNH — dùng --only (--from B5W KHÔNG bỏ B4 = lồng tiếng ở máy 1, SAI ranh giới)
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-anaba --slug epNN-<slug> --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-anaba --slug epNN-<slug> --only B5P
:: ⛔ DỪNG HẲN Ở ĐÂY trước khi sang F — B4 (lồng giọng) và B5/B5Q (vẽ ảnh THÂN VIDEO hàng loạt) là VIỆC
::    CỦA MÁY 2, KHÔNG được tự gõ `--den B5Q`/`--den B8`/`--from B4` ở đây dù chỉ để "thử". Sự cố thật
::    2026-09-27 (ep03): máy 1 lỡ chạy cả B4+B5, tốn ~14.000đ ảnh + credit giọng thật không hoàn được.
::    `pipeline/make_video.py::_chan_buoc2_o_may1` nay CHẶN CỨNG B4/B5 trên máy 1 cho lane này
::    (`profile.body.chan_buoc2_may1: true`) — lệnh trên vẫn chạy được vì --only B5W/B5P không chạm B4/B5.
:: F. HOOK (máy 1 làm trọn hình): storyboard (Fable) → sửa cảnh không thấy mặt → img_prompts_hook.txt (@CAST) + grok_jobs.csv (id clip_NN, 6s)
py -3.13 -X utf8 pipeline\hook_storyboard.py --profile teinengo-anaba --slug epNN-<slug>
::    master vai phụ: make_video.Job(...).masters_from_bible() · ảnh hook: anh_hook.py <tập>\hook (Google Flow Ultra → 9router → gpti2)
::    QC ảnh: qc_hook_clip.py --hook <tập>\hook --anh N  ·  hook_timeline.json THEO SỐ CÂU (shots[].cau, sfx[].cau+lech)
set GROK_SHEET_ID=1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
py -3.13 -X utf8 tools\hook_lane_g\grok_da_luong.py <tập TUYỆT ĐỐI>\hook   :: đa luồng 5–10, tự --close từng profile GPM
::    QC clip: qc_hook_clip.py --clip N (FAIL → chỉnh prompt clip, chạy lại đúng clip đó) · SFX: tools\hook_lane_g\sfx.py
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\M-teinengo-anaba\epNN-<slug> --profile teinengo-anaba   :: viết hết <<CẦN NGƯỜI>> rồi --kiem
:: G. GIAO MÁY 2 (tự ghi D = Đã giao máy 2 + K = lệnh máy 2, H = cần ảnh) — đọc lại _BANGIAO.txt
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job teinengo-anaba epNN-<slug>
```
⚠️ Máy 2 chạy từ cây bundle `FlowHandoff_local\shared\buoc2_3_tool\` (Syncthing), KHÔNG từ git: đổi profile/code dùng ở máy 2 thì chạy lại
`py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list teinengo-anaba` (ep01 máy 2 báo CHẶN vì thiếu bước này, 26/09).
Kiểm cuối: `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | ? CommandLine -match 'GPMLogin'` = 0.
Lớp 3 (đọc bản khoá) kiểm thêm riêng lane: mục đầu trước phút 4 · mỗi mục đủ 5 phần · số lương/chế độ khớp [Dn] đúng điều kiện ·
nửa đầu có thật sự ức chế · 春江 không bị quát · không có 高瀬/恵子/盲点だった · kết đủ cảm ơn + 高評価 + チャンネル登録.

## 3. GATE — ngưỡng đã ĐO (chi tiết trong `profile.script.gate._gate_note` + `goi_dang._nguon`)

| Chỉ số | Giá trị | Nguồn đo (6 transcript `_raw`, segments có mốc giây) |
|---|---|---|
| target_minutes | 22 | kênh mẫu 27,7–40,4' (hit 31,4'); verdict hồ sơ 18–24' |
| list_item_count / order | 7 / countdown | 4/6 video 7選; 5/5 video có marker đều 第N位 đếm ngược |
| hook_marker | 第7位 | — |
| hook_chars (trước mục đầu) | 750–1.150 | kênh mẫu 1.345–2.785 chữ = mục đầu ở 245–554s; K8 ép <240s |
| budget mo_dau / ket | 0,15 / 0,12 | mo_dau kênh mẫu 15–30%, ép theo K8; 第1位 bắt đầu ở 76–80% → phần sau mục cuối ~10–14% |
| hook_anchor_per_1000 | ≥12 | số trong mở đầu 15,3–22,3/1000 ở 4 video việc làm |
| câu (comma / breath) | 0,4–2 / 7–20 | câu trung vị 16,5–22 chữ; ASR không ghi 、 → SUY, đo lại sau tập 1 |
| dialogue_ratio_max | 0,45 | câu đuôi hội thoại 23–50% (hit 50%) |
| title_len | 40–56 | 41–56 ký tự kể cả【漫画】 |
| cta_mid | 0,30–0,55 | câu hỏi A/B/C + コメント ở 34–37% (3/6) |
| goi_dang contradiction / title_core / promise | 45s / 60s / 60s | mâu thuẫn đầu 3,4–63s (5/6 ≤46s); 'N選/Nつの' nói ra 33–67s (4/6); tự giới thiệu 34–58s |
| goi_dang title_core_len | 37–52 | tiêu đề bỏ【漫画】 |

## 4. THUMBNAIL (TITLE-RESEARCH làm — ghi lại để đối chiếu)
Đọc từ 6 ảnh thật: băng đen trên「60代」vàng + từ khoá đỏ → 4 khung 第5位→第2位 → băng dưới「7選」đỏ; **第1位 luôn giấu**. Hit 92k:
2 khung to 第3位/第2位 + cột dọc「60代 穴場 バイト」+ ô lợi ích dọc「午後は自由」(buổi chiều tự do)「座れて快適」(ngồi được, dễ chịu).
Nhân vật CƯỜI thắng nhăn nhó. Đối thủ >180k đều có móc 0円/安く/最強/神 — dùng ở tựa tập 1/9/10.

## 5. (CHÉP NGUYÊN TỪ CỬA VÀO) ⛔ LUẬT KHOÁ CỨNG LANE M (anh chốt 2026-09-26 — vi phạm 1 điều = DỪNG, không tự "linh hoạt")
**K1 — Tên:** thư mục làm việc = tên tab = thư mục giao hàng = `M-teinengo-anaba` (`assets\M-teinengo-anaba\`,
tab `M-teinengo-anaba`, `CHANEL\M-teinengo-anaba\`). Mã lane/profile id = `teinengo-anaba`. Cấm tạo thư mục `assets\teinengo-anaba\`.
**K2 — Kênh:** anh TỰ setup kênh + tự upload avatar/cover. Cấm chạy `tools\channel_branding.py`, cấm mở GPM vào YouTube Studio kênh này.
**K3 — Sheet:** mail `haoviabattu@gmail.com` là kênh thứ 2 của mail (GMAIL dòng 3 = Lane A) → cấm ghi đè GMAIL dòng 3 (chỉ ô ghi chú L3).
Tab `M-teinengo-anaba` header A→S cố định (mục 6), cấm đổi/xoá cột; cấm xoá dữ liệu bất kỳ sheet nào.
**K4 — Phạm vi đề tài:** CHỈ việc làm tuổi 60 — アルバイト・パート (việc làm thêm), 再就職 (tái tuyển dụng), 再雇用 (tuyển lại sau hưu),
thu nhập đi làm vs 年金 (lương hưu). Cấm sở thích/du lịch/0円 vui chơi (Lane G), cấm drama mất tiền (Lane F), cấm trục vợ chồng (Lane J).
**K5 — Bình luận trước khi viết:** mỗi tập đọc `docs\channel_dna\otonanomouten\COMMENT_INSIGHT.md` + bình luận của đúng video gốc trong
`COMMENTS_TOP.md`; lỗi dữ kiện khán giả đã bắt ghi thành QUY ƯỚC trong `series_ctx.txt`. Hai ví dụ phải nhớ:
「初月はシフト18日でしたが、次の月は11日でした」 (tháng đầu 18 ca, tháng sau 11 ca — không đủ sống) = nỗi lo thật → cú KÍCH;
「5キロの荷物を2人で持つことはない」 (không ai 2 người khiêng 5 kg) = chi tiết gốc phi thực tế → kiểm lại mọi con số trước khi clone.
**K6 — Cung cảm xúc:** KÍCH (quản lý cắt ca tuỳ tiện / nơi tuyển coi người 60 là đồ bỏ / đồng nghiệp cũ bám chức danh, leo thang ≥3 nấc)
→ GIẢI TOẢ bằng sự thật + chế độ thật → VỊ THA + 1 câu đạo lý đáng chép. Cấm viết nhẹ nhàng khô khan. Profile KHÔNG được khai `cung_cam_xuc: false`.
**K7 — Kết bắt buộc:** cảm ơn người xem đã quan tâm xem hết video + xin 1 lượt 高評価 (thích) + チャンネル登録 (đăng ký).
`script.outro_line` của lane phải chứa đủ 3 ý; máy kiểm `KẾT THIẾU`. Profile KHÔNG được khai `cam_on_cuoi: false`.
**K8 — Cấu trúc:** mục xếp hạng đầu tiên TRƯỚC phút 4 (khán giả kênh mẫu chê "nửa đầu chỉ kể chuyện"); truyện đan xen giữa các mục;
mỗi mục = ưu điểm + cái bẫy + con số (giờ, lương giờ, ca/tuần, sức nặng) + ai hợp/không hợp. Hạng 1 để cuối, giấu trên thumbnail.
**K9 — Sự thật:** lương giờ, chế độ 在職老齢年金 (lương hưu bị trừ khi đi làm), giới hạn tuổi, bảo hiểm, luật cắt ca → CÓ NGUỒN trong
`series_ctx.txt` [Dn] và nói rõ điều kiện; không nguồn thì nói định tính. Nhân vật/tình tiết hư cấu được, số chế độ thì cấm bịa.
**K10 — Nhân vật:** ông chính RIÊNG của lane (tóc muối tiêu, kính gọng mảnh, áo len vàng mù tạt, sổ tay xanh — theo `branding\avatar_raw.png`),
khoá mặt XUYÊN TẬP bằng 1 ảnh gốc lane (như Sakura Lane L). Vợ có chính kiến, chồng không quát/nói trống không với vợ.
Cấm dùng 高瀬健一 / 恵子 / câu chốt 「盲点だった。」 / tên kênh mẫu. Nét chibi dễ thương, soát lỗi ảnh AI (tóc, tay).
**K11 — Giọng:** không dùng chung voice_id với lane nào; clone giọng người thật → HỎI ANH trước khi giữ voice_id; mọi tên riêng
phải nghe thử qua TTS (kênh mẫu bị chê đọc sai 「シンリコさん」); nhạc nền không được "ngớ ngẩn" (bị chê 12 like).
**K12 — Luật dự án chung vẫn áp:** Claude chỉ làm BƯỚC 1 (không render); hook (dài ≈ hook video gốc, luật 17/10) là video sinh + SFX (cổng S1L); máy 3 soát kịch bản
sau LOCK; xong tập ghi D=`Đã giao máy 2` + K=lệnh máy 2 + H=`cần ảnh`; mọi chữ Nhật trong báo cáo kèm dịch tiếng Việt; báo cáo ghi đường dẫn tuyệt đối.


## 6. HOOK — LUẬT VIẾT + CÁCH DỰNG CỦA LANE NÀY

> ⛔ Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.

> ⛔ 14/10/2026 THẮNG bảng dưới: **KHUÔN WIN** ep05/ep06 (phần hook đã xoá 17/10) — thân bài có nút 38–40% / A/B/C 42–47% / cao trào 55–60% / 第1位 76–80% trả lời nhá. Chi tiết: `E:\CLAUDE\YOUTUBE\h2dev\docs\CONG_THUC_WIN_LANE_M.md`.
> ⛔ **2026-10-16 anh chốt: kịch bản BUỘC theo CÔNG THỨC WIN** `E:\CLAUDE\YOUTUBE\h2dev\docs\CONG_THUC_WIN_LANE_M.md` — sau B3G, trước khi giao máy 3 chạy `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kiem_cong_thuc_win.py --profile teinengo-anaba --slug <slug>` + chấm phần kiểm bằng mắt; mục ❌ → vá qua viec_tay rồi kiểm lại tới ĐẠT. Thân bài: cấm bịa cảnh bị coi thường; 第7位 (hạng 7) trước phút 4.

| | |
|---|---|
| Cách dựng hình | `manga_chibi_fixed_ref_grok`: ảnh chibi khoá mặt makoto/harue (+ vai phụ của tập) → clip Grok 6s + SFX |
| Công tắc | BẬT (`enabled:true`, `visual_kind:video_sinh`, `sfx:true`) |

Runbook dựng: `docs\QUY_TAC_VIDEO_HOOK.md`.

## 7. CÒN TREO (nói thẳng)
- Giọng đã chốt (đa giọng, §0c) nhưng CHƯA calibrate → `make_video` bị hàng rào #1 CHẶN cho tới khi đo.
- `seconds_per_image` chưa đo (§1).
- Comma/breath/dialogue là số SUY từ ASR — đo lại sau tập 1.
- Tập 10 dùng video gốc 1k view / 0 bình luận — nguồn yếu, chỉ mượn khung tính thu nhập.
- `channel_id` chưa có (anh tự setup kênh).
