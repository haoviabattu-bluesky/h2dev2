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
- `image.seconds_per_image=8` là **TẠM** — chưa đo nhịp cảnh kênh mẫu; đo bằng skill `video-chuyen-canh` trên `wG4fI9voims` trước B5W tập 1.

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

## 2. LỆNH CHẠY (Giai đoạn 3 — 1 tập anh chỉ định)

```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
:: 0) Đọc COMMENT_INSIGHT.md + bình luận đúng video gốc trong COMMENTS_TOP.md (K5)
:: 1) thư mục tập + hồ sơ (ghi cột C ngay)
mkdir ..\assets\M-teinengo-anaba\ep01-suwatte-anaba
py -3.13 -X utf8 retrieve_videos.py --dna-dir ..\docs\channel_dna\otonanomouten --topic "60代 座って働ける アルバイト 7選" --top 3
::    competitor.txt  = transcript video gốc (cột K)
::    series_ctx.txt  = SỐ ĐƯỢC PHÉP + [Dn] lương giờ/chế độ CÓ URL (mhlw.go.jp, nenkin.go.jp, trang tuyển dụng…) + QUY ƯỚC
::                    (lỗi khán giả đã bắt → quy ước; 7 việc BẮT BUỘC có tên; hạng 1 trả lời tiêu đề thế nào)
::    title.txt · promise.txt (1 câu) · characters.json kiểu CAST (makoto, harue, vai phụ)
:: 2) viết → tự DỪNG sau LOCK, gửi máy 3 (D = "Cần check kịch bản")
py -3.13 -X utf8 make_video.py --profile teinengo-anaba --slug ep01-suwatte-anaba --den B3G
:: 3) anh báo D = "Đã sửa kịch bản" →
py -3.13 -X utf8 review_may3.py --nhan --profile teinengo-anaba --slug ep01-suwatte-anaba
:: 4) ĐA GIỌNG: characters.json (CAST, mỗi vai có voice.voice_id theo §0c) → gắn vai từng câu (Opus, chỉ đọc bản khoá):
py -3.13 -X utf8 gan_vai.py --profile teinengo-anaba --slug ..\assets\M-teinengo-anaba\ep01-suwatte-anaba
:: 5) B5W (Opus) → B5P → hook storyboard (Fable) → ảnh hook → clip Grok → QC (Sol) → SFX → hook_timeline.json (mốc THEO CÂU,
::    máy 1 KHÔNG lồng giọng) → HOOK_TAP.md → dong_goi_may2.py --job (tự ghi D=Done + H=cần ảnh) → giao máy 2. Claude Code KHÔNG render.
```
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
**K12 — Luật dự án chung vẫn áp:** Claude chỉ làm BƯỚC 1 (không render); hook 20–30s là video sinh + SFX (cổng S1L); máy 3 soát kịch bản
sau LOCK; xong tập ghi D=`Done` + H=`cần ảnh`; mọi chữ Nhật trong báo cáo kèm dịch tiếng Việt; báo cáo ghi đường dẫn tuyệt đối.


## 6. HOOK 20–30 GIÂY ĐẦU — CÁCH CỦA RIÊNG LANE NÀY

| | |
|---|---|
| Kiểu mở (`script.hook.patterns`) | H02 (người ngoài nói thẳng 1 câu hạ bệ — kiểu hit 92k) · H01 (cảnh đau có giờ + cơ thể) · H21 (câu thoại vợ lật kỳ vọng) |
| Câu khoá (`script.hook.closer`) | K09 — hứa 7 mục ngay trong câu chuyện (để vào 第7位 trước phút 4) |
| Cách dựng hình | `manga_chibi_fixed_ref_grok`: ảnh chibi khoá mặt makoto/harue (+ vai phụ của tập) → clip Grok 6s + SFX |
| Công tắc | BẬT (`enabled:true`, `visual_kind:video_sinh`, `sfx:true`) |

Runbook dựng: `docs\QUY_TAC_VIDEO_HOOK.md`. Nguyên tắc nội dung: `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

## 7. CÒN TREO (nói thẳng)
- Giọng đã chốt (đa giọng, §0c) nhưng CHƯA calibrate → `make_video` bị hàng rào #1 CHẶN cho tới khi đo.
- `seconds_per_image` chưa đo (§1).
- Comma/breath/dialogue là số SUY từ ASR — đo lại sau tập 1.
- Tập 10 dùng video gốc 1k view / 0 bình luận — nguồn yếu, chỉ mượn khung tính thu nhập.
- `channel_id` chưa có (anh tự setup kênh).
