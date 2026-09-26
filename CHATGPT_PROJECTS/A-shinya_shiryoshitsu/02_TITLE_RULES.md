# 02 TITLE RULES — A-shinya_shiryoshitsu · toshi-densetsu-jp

> Lane `toshi-densetsu-jp`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 26 · tối đa 32 · tối thiểu 18 · cảnh báo phần đầu 24
- prefix cố định: `【都市伝説】` · suffix cố định: `【都市伝説 ミステリー 怖い話】`

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE A (深夜の資料室 — 都市伝説/宇宙, tài liệu ngôi 3, khán giả 25-55 soi số) — bản 2026-09-23, đo bằng máy trên 32 tiêu đề kênh gốc 今夜も都市伝説 (docs/lanes/toshi-densetsu-jp/CONG_THUC_TIEU_DE_KENH_GOC.md):
1. CHỈ VIẾT THÂN: tool tự nối 【都市伝説】 ở ĐẦU và 【都市伝説 ミステリー 怖い話】 ở CUỐI. Không tự thêm 【】 nào.
2. ƯU TIÊN SỐ 1 — mở bằng MỘT TRONG HAI (đo được lift 1,65, mạnh nhất kênh gốc):
   (a) 「lời nguyên văn trong kịch bản」 đặt ngay đầu thân — 「あれは航空機じゃない」「彼らは宇宙人じゃない…未来人だ！」;
   (b) NHÂN VẬT CỤ THỂ + đã làm gì — 〜した男 / 元エリア51科学者 / 予言者ケイシー / 米海軍中佐.
   Tên vụ / cơ quan / mốc năm CÓ THẬT trong kịch bản (CIA, NASA, バミューダ, 1978年) đặt trong 12 ký tự đầu.
3. CẤM TUYỆT ĐỐI KHUNG GIẢI THIÊNG. Kênh gốc 0/31 tiêu đề nói 'chỉ là thần thoại / chỉ là nhớ sai / hoàn toàn không có'. Tiêu đề phải hứa BÍ ẨN LỚN HƠN: 'X không phải Y — mà là Z lạ hơn' (mẫu 151K: UFOは宇宙人じゃない。答えは100年前に出ていた…). Viết 「神話だった」「嘘だった」「0件」「並行世界じゃない (rồi dừng)」 = lời hứa CO LẠI trước khi người ta bấm = 0 điểm.
4. PHỦ ĐỊNH 〜じゃない CHỈ là một lựa chọn ngang hàng, KHÔNG phải mặc định: lift thật 0,81 (số 3,3 ghi 20/09 do bẫy Unicode NFD). Dùng nó thì vế sau BẮT BUỘC mở ra đáp án lạ hơn.
5. MỘT ĐIỂM LẬT, KHÔNG KỂ ĐÁP ÁN: 1 mảnh che giấu (正体/真相/秘密/隠された/封印/機密, lift 1,15) hoặc lời cuối nhân chứng. Dấu … chỉ dùng khi thật sự treo lửng (lift 0,88 — đừng dùng như dấu câu). Câu hỏi なぜ/とは/？ BÃO HOÀ (lift 0,49/0,77) — tránh.
6. CON SỐ CÓ ĐƠN VỊ đúng kịch bản (lift 1,51), viết bằng CHỮ SỐ (6分, 20歳, 59年 — không 六分). Không làm tròn, không phóng đại.
7. ĐỘ DÀI THÂN 18-32 (mục tiêu 26), móc trọn trong 24 ký tự đầu — chưa tính 2 khối 【】.
8. MÓC NHẬT lên tiêu đề khi kịch bản có (lift 1,21; 3/3 video Nhật của kênh gốc đều hé ngay trong hook): 秋田の聖母, 日航1628便.
9. MỌI danh từ/số trong tiêu đề phải GREP ĐƯỢC trong kịch bản (cả 76秒 lẫn 七十六秒). Không có = không được viết.
10. CẤM: ngôi 1 私/僕 · cảm thán 衝撃/ヤバすぎる/的中率 (lift 0,29) · 朗読 · khẳng định 宇宙人だった khi kịch bản chỉ nêu 説 · lặp nguyên chữ thumbnail · tên kênh mẫu 今夜も都市伝説.
Mẫu kênh gốc thắng: UFOは宇宙人じゃない。答えは100年前に出ていた… (151K) · 日本だけが知っていた？「月の秘密」がついにバレ始めている (120K) · 予言者ケイシーが死の直前に残した一言の意味を読み解く (112K) · 3906年の未来にタイムスリップした男…100年封印された「ディーナッハの記録」 (94K).
Tự kiểm: "Người Nhật 40 tuổi 23h lướt điện thoại: 2 dòng này nói về VỤ GÌ? thiếu mảnh nào mà phải bấm? tôi có đang HỨA ÍT HƠN so với bí ẩn người ta đang tin không?" — ghi vào ly_do_bam.

### forbid_phrases
```
[
 "今夜も都市伝説"
]
```

### separators_ok
False

### ctr_hint
Có 1 ĐIỂM LẬT rõ (phủ định điều ai cũng tin: 〜じゃない/ではなく · 1 mảnh che giấu: 正体/真相/秘密/隠された/封印 · lời cuối nhân chứng 「…」) mà KHÔNG kể đáp án? Có con số CÓ ĐƠN VỊ từ kịch bản (59年, 5機, 6分間)? Tiêu đề chỉ nêu tên vụ + 'の真実' chung chung, hoặc kể luôn đáp án → ctr ≤ 4.

### brevity_hint
keyword + điểm lật trọn trong ≤{head_warn} ký tự đầu? thân {target_min}–{max_chars} chưa tính khối 【】 (mục tiêu {target_chars})? Quá {max_chars} hoặc dưới {target_min} = 0 điểm và KHÔNG được chọn.

### length_block
ĐỘ DÀI (luật cứng): tiêu đề bạn viết là PHẦN THÂN, tool sẽ tự nối khối 【都市伝説 ミステリー 怖い話】 (16 ký tự) vào cuối — KHÔNG tự viết tag. Thân {target_min}–{max_chars} ký tự (mục tiêu {target_chars}); cú móc + keyword trọn trong {head_warn} ký tự đầu vì điện thoại cắt ở ~2 dòng. Dữ liệu SERP 2026-09-20 (75 tiêu đề ngách): THÂN 20–30 ký tự gmean 128K, 30–50 → 31K, 50–60 → 22K — thân NGẮN thắng gấp 4 lần; 【】 đuôi lift 1.31; … ngắt 1.24; câu hỏi なぜ/とは lift 0.4 (bão hoà, không thắng). Một tiêu đề = MỘT điểm lật.

## Nhịp hook kênh mẫu (tiêu đề phải khớp lời hứa hook)
- 0–4s Đọc tít (title-card): Câu ≤20 chữ, nguyên văn chữ vàng thumbnail hoặc nửa đầu tiêu đề. 8/9 (OU1r đọc tên chương 1).
- 0–20s Năm + người thường + điều bất khả / hoặc giả định ngôi 2: 6/9 có năm + nơi + nghề trong 20s đầu (OU1r 13.3s, GTwo 0.4–4.3s, HqaY 3.4s, gWF 3.4s, UO4 17.2s, huF9 18s). 4/9 dùng 『もし(も)あなたが…としたら』 (saIym, zgi, UO4, huF9).
- 10–60s Chuỗi chi tiết cảm giác / tăng cấp: 3–5 câu ngắn dựng hình (翼はない。プロペラもない。/ 見覚えのない天井、聞いたこともない言葉、鏡に映った自分ではない誰かの顔) — không có câu bình luận trừu tượng.
- 40–60s Lời trích / khẳng định = chữ đỏ thumbnail: Chữ đỏ thumbnail được đọc (hoặc đáp án ●● được trỏ tới) trong hook ở 5/9 (HqaY, UO4, GTwo, 8miF, saIym); một phần 3/9; lệch 1/9 (huF9).
- 55–100s Chuỗi câu hỏi なぜ: ≥2 câu hỏi 'vì sao/là gì' trong hook: 8/9 (zgi chỉ 1). Thường nối bằng そして.
- 85–115s Lời mời + (CTA) → 第1章: Lời mời 9/9; nguyên câu 『それでは…を最初から辿っていこう』 4/9; CTA 『本編が始まる前に…ハイプで応援してくださいね』 (118 chữ) 6/9 — chỉ các video từ 2026-08-26 trở đi (OU1r 08-14, GTwo 08-21, gWF không có). 第1章 ở 99.6–~167s, trung vị ~115s.

---
## CÔNG THỨC TIÊU ĐỀ KÊNH GỐC (tài liệu lane)

# Công thức TIÊU ĐỀ của KÊNH GỐC lane A — 今夜も都市伝説 (`UCoFEha9rNMFqUio-4GQITfw`)

Đo bằng máy 2026-09-23 trên **32 video có view** (crawl 37, bỏ 5 video view=0 chưa đủ tuổi).
View trung bình nhân toàn kênh: **25,695**. Lift = gmean nhóm CÓ / gmean nhóm KHÔNG.

> ⚠ **Bẫy đo đã dính**: tiêu đề yt-dlp trả về ở dạng Unicode **NFD** (ぜ = せ + dấu đục rời).
> Regex viết bằng kana dựng sẵn khớp **0** dòng mà không báo lỗi — `なぜ` ra 0/32, `じゃない` ra 3 thay vì 7.
> Luôn `unicodedata.normalize('NFC', title)` trước khi đo. Con số 'phủ định lift 3.3' ghi ngày 2026-09-20 nhiều khả năng dính bẫy này.

## 1. Độ dài THÂN (bỏ MỌI khối 【】, cả đầu lẫn đuôi)

| Thân (ký tự) | Số video | gmean view |
|---|---|---|
| 0–35 | 5 | 63,067 |
| 35–45 | 12 | 21,310 |
| 45–55 | 9 | 22,916 |
| 55–70 | 3 | 22,799 |
| 70–120 | 3 | 19,323 |

**Kết luận: thân ≤35 ký tự gmean 63.067 — gấp ~3 lần mọi nhóm dài hơn.** Luật thân 18–32 của lane (đo từ SERP
ngày 2026-09-20) được xác nhận lại trên CHÍNH kênh gốc → giữ nguyên.

## 2. Đặc trưng nào đi kèm view cao

| Lift | Có / tổng | gmean CÓ | gmean KHÔNG | Đặc trưng |
|---|---|---|---|---|
| **1.65** | 14/32 | 34,093 | 20,622 | 「lời trích」 trong thân |
| **1.65** | 15/32 | 33,543 | 20,310 | nhân vật cụ thể (男/博士/飛行士/科学者/少年/元米軍…) |
| **1.51** | 14/32 | 32,370 | 21,470 | con số |
| **1.37** | 10/32 | 31,844 | 23,307 | 【】 ở ĐẦU tiêu đề |
| **1.36** | 7/32 | 32,594 | 24,039 | 「lời trích」 MỞ ĐẦU thân |
| **1.21** | 6/32 | 30,013 | 24,790 | móc NHẬT (日本/日本人) |
| **1.15** | 18/32 | 27,313 | 23,754 | 正体/真相/秘密/隠され/封印/極秘/暴露 |
| **0.88** | 20/32 | 24,532 | 27,756 | … ngắt giữa câu |
| **0.81** | 7/32 | 21,848 | 26,888 | phủ định じゃない/ではなかった |
| **0.80** | 8/32 | 21,784 | 27,149 | ｜ chia 2 vế |
| **0.77** | 18/32 | 22,926 | 29,751 | とは？ / のか？ đuôi câu hỏi |
| **0.63** | 2/32 | 16,547 | 26,460 | ●● / ○○ che đáp án (TRONG TIÊU ĐỀ) |
| **0.56** | 5/32 | 15,848 | 28,100 | NASA/CIA/FBI/米軍/ソ連 |
| **0.49** | 4/32 | 13,778 | 28,087 | なぜ / どうして |
| **0.29** | 4/32 | 8,654 | 30,017 | cảm thán ヤバすぎる/衝撃/完全暴露/的中率 |

## 3. Toàn bộ tiêu đề (view giảm dần, đã chuẩn hoá NFC)

| View | Dài thân | Tiêu đề |
|---|---|---|
| 172,000 | 69 | 【都市伝説】「人類には核兵器より恐ろしいものがある」440光年先の惑星ティアウーバへ招待された男が宇宙人へ質問…人類の正体、イエスキリストの正体とは？【都市伝説 ミステリー】 |
| 151,000 | 26 | 【都市伝説】UFOは宇宙人じゃない。答えは100年前に出ていた…【ミステリー 怖い話】 |
| 120,000 | 28 | 日本だけが知っていた？「月の秘密」がついにバレ始めている【都市伝説   ミステリー 怖い話】 |
| 112,000 | 45 | 日本に隠されたキリスト宇宙人説の真相。予言者ケイシーが死の直前に残した一言の意味を読み解く【都市伝説 ミステリー 怖い話】 |
| 94,000 | 53 | 3906年の未来にタイムスリップした男…100年封印された「ディーナッハの記録」に描かれた人類の正体とは？【都市伝説 ミステリー 怖い話】 |
| 69,000 | 32 | 【都市伝説】【ピラミッドの正体】遂に判明！？絶対に暴いてはいけない、ピラミッドの本当の目的とは？【エジプト ミステリー 怖い話】 |
| 67,000 | 44 | これが月に行かなくなった理由です！アポロ飛行士が撮影してしまった「あり得ないモノ」とは？【都市伝説 ミステリー NASA】 |
| 60,000 | 36 | 「彼らは宇宙人じゃない…未来人だ！」元エリア51科学者がそう告げられた日 【都市伝説 ミステリー 怖い話】 |
| 41,000 | 41 | 元米軍人が月の地下で接触した“もう一つの人類”｜人類は月の最初の住民ではなかった…【都市伝説 ミステリー 怖い話】 |
| 39,000 | 44 | NASAが隠した惑星ニビルの正体｜5000年前から記録されていた人類滅亡のシナリオとは？【都市伝説 ミステリー 怖い話】 |
| 38,000 | 34 | 「宇宙人は、怖くない」日本の少年が遭遇した3種類の宇宙人の正体とは？【都市伝説 ミステリー UFO 怖い話】 |
| 37,000 | 79 | 「死後の魂は●●へ行き選択する…」予言者エドガーケイシーと異星人の交流記録で判明した死後の世界と宇宙の真実…13,000年も地球を守り続けている宇宙人の正体…【都市伝説 ミステリー 怖い話】 |
| 37,000 | 38 | 【実録】宇宙人250体を解剖した元米軍関係者が暴露｜彼らの正体は未来の人類だった…？【都市伝説 ミステリー 怖い話】 |
| 35,000 | 47 | 【都市伝説】地球内部で2年間暮らした男が語った「もう一つの人類文明」とは？｜地球人は我々だけではなかった…【都市伝説 ミステリー 怖い話 宇宙人】 |
| 31,000 | 43 | 【都市伝説】ニコラ・テスラが残した極秘記録の中身…天才たちが接触した宇宙人の正体と人類の真実とは？【暴露 ミステリー 怖い話】 |
| 28,000 | 46 | 「地球は核戦争で滅ぶ…」火星から転生したボリスカ少年が明かす地球滅亡のシナリオと人類選別の時【都市伝説 ミステリー スピリチュアル】 |
| 21,000 | 37 | 金星からきた男と極秘インタビュー全記録｜人類滅亡のカウントダウンがはじまる【都市伝説 ミステリー 宇宙人】 |
| 21,000 | 33 | 人類はなぜ地球へ来たのか？宇宙人が語った「滅びた故郷」と宇宙難民説【都市伝説 ミステリー 怖い話】 |
| 20,000 | 35 | 【都市伝説】人類が火星へ行ってはいけない理由｜火星に文明を見た天文学者の告白とは？【暴露 ミステリー 怖い話】 |
| 19,000 | 46 | 【ピラミッドの正体】ピラミッドは墓じゃない…ニコラ・テスラが明かしたピラミッドの真の用途とは？天才が気づいた秘密【都市伝説 ミステリー 怖い話】 |
| 18,000 | 39 | ファティマ第三の預言と日本で起きた奇跡！秋田で起きた聖母による未来の預言とは？【都市伝説 ミステリー 怖い話】 |
| 15,000 | 77 | シュメール文明・アヌンナキ・惑星ニビル…日本で30年語り継がれた都市伝説の正体を検証！アヌンナキは本当にいた？独学で古代文字を読んだ男が消された理由とは？【都市伝説 ミステリー 怖い話】 |
| 13,000 | 76 | CIAが隠した超能力実験の記録…死から生還した男が見た火星ピラミッドの中身とは？スターゲート計画とは？CIA公式記録に残る火星リモートビューイングの真実【都市伝説 ミステリー 怖い話】 |
| 13,000 | 51 | 火星に行った男が語る、衝撃の真実とは！？アメリカ政府が隠した計画、プロジェクト・ペガサスがヤバすぎる…【 都市伝説 火星 宇宙人 ニコラテスラ】 |
| 13,000 | 58 | 「人類は、二度と月に戻れない」半世紀前にできたことが、なぜ最新技術の現代にできないのか…月を歩いた12人が残した沈黙【都市伝説 アポロ計画 ミステリー】 |
| 12,000 | 45 | 月の裏側に眠る150万年前の巨大宇宙船…船内で発見された「東洋人女性」はなぜ隠されたのか？【都市伝説 ミステリー 怖い話】 |
| 11,000 | 42 | UFOに乗った技術者の告白｜宇宙人はなぜ「技術だけ進んだ文明は滅びる」と告げたのか？【都市伝説 ミステリー 怖い話 】 |
| 11,000 | 43 | UFOと宇宙人は死後の世界の住人だった！？宇宙人の正体と死後の世界の真実がヤバすぎる…【 都市伝説 エイリアン ミステリー 怖い話】 |
| 7,700 | 45 | 人類は何度も滅亡している…モヘンジョダロの"50倍の放射能"は本物か？古代核戦争の証拠7つ【都市伝説 ミステリー 怖い話】 |
| 7,400 | 49 | 【宇宙人の正体判明】「グレイは宇宙人ではなく●●人だ」天才ホーキング博士とエリア51関係者が暴露する内容がヤバすぎる…【都市伝説 ミステリー 怖い話】 |
| 5,300 | 69 | 【的中率85%】日本沈没を予言した男エドガー・ケイシーの正体…眠ったまま病を見抜く力の真実｜ヤバすぎる…日本沈没、アトランティス、ポールシフトの真実とは？【都市伝説 ミステリー 怖い話】 |
| 1,300 | 39 | 月は自然の天体ではなかった？NASAの公式データが示す"完璧すぎる設計"とは？【都市伝説 ミステリー 怖い話】 |

<!-- export 7c146d33f87d · 2026-09-26 -->
