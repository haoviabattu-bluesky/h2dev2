# 07 WORKFLOW — irogatatarukioku

> Lane `irogatatarukioku`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# QUY TRÌNH TIÊU ĐỀ + MÔ TẢ — LANE D (`irogatatarukioku`, 色が語る記憶)

Chốt 2026-09-20. **Chỉ áp dụng cho lane này** — lịch sử WW2, ảnh THẬT tô màu, người kể ngôi 3. Không dùng luật satori.
Kế hoạch + số liệu: `plans/260920-1639-lane-d-irogatatarukioku/`.

## 1. Kênh · sheet · thư mục
| | |
|---|---|
| Kênh thật | 色が語る記憶 · `UCtRuxojb7218QeFBf5TBCQQ` (mở 09/2026; 6 video ep01–06 đăng 13–18/09, view 0–11 khi bắt đầu) |
| Kênh mẫu | 色でたどる戦争の記録 `UCaj1dslbibbHEnOAOh0tyYw` · `h2dev/docs/channel_dna/irogatatarukioku` (20 video, đã crawl 2026-09-16) |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep<nn>-<slug>` (script.txt · thumb_text.txt · series_ctx.txt · TIEU_DE_MO_TA.txt) |
| Giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\ep<nn>-<slug>` (cùng tên) — tool chép `TIEU_DE_MO_TA.txt` vào, XOÁ `listting.txt` cũ |
| Sheet | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` tab **`irogatatarukioku`**: C = hồ sơ SPACE_RESEARCH (không phải tập) · **E = tiêu đề tool ghi** · F = tags (anh làm sẵn) · **I = thư mục CHANEL** (khớp theo tên thư mục) · J = ghi chú đăng · K = tình trạng |
| Config | `config/lanes/irogatatarukioku.json` |

## 2. Công thức tiêu đề lane D (đo thật, không suy diễn)
```
【sự kiện/địa danh/năm】 + hook 1 KHOẢNH KHẮC trong ảnh (vai+tuổi/số) —— hệ quả tàn khốc ｜ số liệu chính xác ｜実際の写真をAIカラー化
```
- Kênh mẫu 20/20 mở 【】, 19/20 có ｜, 73–81 ký tự. ≥70 ký tự gmean 7.2K vs <70 → 2.1K. Có `——` 23K vs 3.6K.
- SERP rộng ep08 (181 tiêu đề, 93 ngách): nhóm **31–40 ký tự = đúng định dạng cũ của mình = tệ nhất** (gmean 1.4K);
  71–85 ký tự gmean 8.6K. Kênh thứ 2 `AIで蘇る戦争の記憶` cùng công thức → 107K/682K/399K.
- Độ dài chưa tính suffix: **60–90, mục tiêu 78, 【】+hook trọn trong 35 ký tự đầu** (điện thoại cắt ~40).
- Suffix của mình `｜実際の写真をAIカラー化` (tool tự nối). CẤM `AIフルカラー復元` / `色でたどる` (của kênh mẫu).
- Tên riêng: được phép, không bắt buộc; kênh mẫu thắng bằng vai + tuổi + số. Tên riêng + địa danh bắt buộc ở tags (sheet cột F).
- 7 luật đầy đủ: `title_rules` trong json (prompt S2/S3/S3b/S3c đọc từ đó).

## 3. Khuôn `TIEU_DE_MO_TA.txt` lane D (anh chốt 2026-09-20)
```
<tiêu đề đầy đủ có suffix>
(trống)                              ← KHÔNG có dòng tags (tags trên sheet cột F)
<hook + 2-3 đoạn + câu mời bình luận>
(trống)
当時の白黒写真をAIで色付けし…          ← khối miễn trừ, GIỮ NGUYÊN từ file cũ
----- GẠCH -----
Timestamps: (giữ nguyên từ file cũ)
----- GẠCH -----
☕ 最後までご覧いただき、心より感謝申し上げます。
----- GẠCH -----
#hashtag
----- GẠCH -----
【映像・画像クレジット】 (giữ nguyên từ file cũ — nguồn ảnh Public Domain, BẮT BUỘC)
```

## 4. Lệnh
```bash
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
py -3.13 cli.py run     --slug E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep08-araki-kamikaze --profile irogatatarukioku
py -3.13 cli.py view    --slug <dir>                          # XEM.html
py -3.13 cli.py sheet   --profile irogatatarukioku            # ghi cột E (chỉ tập có TITLE_LOCK)
py -3.13 cli.py deliver --slug <dir> --profile irogatatarukioku   # chép sang CHANEL + xoá listting.txt
py -3.13 cli.py all     --profile irogatatarukioku --only ep07,ep09
py -3.13 cli.py emit    --slug <dir> --title 2 && py -3.13 cli.py run --slug <dir> --from lock --force   # phủ quyết
```
yt-dlp dính 429 → thêm `--proxy socks5h://haonguyen262.hao1:quanghao@154.198.33.150:9093`.

## 5. Bảng tiêu đề cũ → mới (batch 2026-09-20, 11/11 xong, 10–15 phút/tập)
| Tập | Tiêu đề cũ (ký tự) | Tiêu đề mới chưa suffix (ký tự) | QC Sol | ESC |
|---|---|---|---|---|
| ep01-ushijima-mitsuru | 沖縄陥落の夜、彼は部下にただ一人こう命じた「死ぬな、真実を語れ」 (32) | 【沖縄戦】首里城地下の壕でランタンを囲む4人の将校——撮影から2か月3週間後、中央と隣の2人は島の南端で最期を迎えた｜1945年4月の一枚 (69) | QC1 FIX → QC2 FAIL → QC3 PASS | 0 |
| ep02-kuribayashi-iwojima | 妻への手紙は「床の隙間を直して」だった――36日後、彼は戦死した (32) | 【硫黄島】正面を見据えるこの司令官は万歳突撃を禁じた——最後の夜、階級章をすべて外したという｜2万2786人を率いた男の遺体は見つからなかった (71) | QC1 FIX → QC2 FIX | 2 |
| ep03-nakagawa-peleliu | 73日間、彼は"4日で終わる"はずの島を守り抜いた――そして軍旗を焼いた (36) | 【ペリリュー】大佐は連隊旗を焼いて消えたとされる——それでも34人の兵は洞窟に潜み続け、投降は2年5か月後の1947年4月22日だった (67) | QC1 FAIL → QC2 FAIL → QC3 FAIL → QC4 FIX | 1 |
| ep04-aruga-yamato | 片道分の燃料だけを積んで――大和、最後の艦長が艦橋を離れなかった理由 (34) | 【戦艦大和】着任時、47歳の艦長は長男に「死に場所を得た」と書き送った——翌年4月、総員退去の後も艦橋を離れなかった｜残る肖像写真はこの一枚だけ (72) | QC1 FAIL → QC2 FIX | 0 |
| ep05-yamazaki-attu | 米国本土で唯一のバンザイ突撃――雪のアッツ島、彼が霧の中に消えるまでの19日間 (39) | 【アッツ島】軍医は「私はまだ三十三歳なのに死ぬ」と書いた——同じ日記に、病院の患者をどうしたかが記されていた｜米軍約11000名vs守備隊約2600名 (75) | QC1 FIX → QC2 FAIL → QC3 FAIL | 1 |
| ep06-nagumo-saipan | 真珠湾攻撃を成功させた提督は、三年後サイパンの洞窟で消えていった (32) | 【真珠湾】189機を発艦させた日、この肖像の男はまだ何も知らない——2年7ヶ月後、遺体を見つけたのは米海兵隊だった｜空母6隻を率いた提督の写真 (71) | QC1 FIX → QC2 FAIL → QC3 FAIL → QC4 PASS | 0 |
| ep07-shibasaki-tarawa | 「百万人が百年かけても落とせない」と豪語した島は、わずか76時間で陥落した (37) | 【タラワの戦い】腰まで海に浸かり進んだ米海兵、第一波は死傷率約75%——だが守備隊約4700名のうち捕虜となった日本兵は17名｜1943年11月20日上陸 (77) | QC1 FAIL → QC2 PASS | 1 |
| ep08-araki-kamikaze | 子犬を抱いた17歳――「ほがらか隊」5人が出撃前日に残した1枚の写真 (34) | 【特攻】写真の五人は自ら「ほがらか隊」と名乗った——出撃前夜、17歳は父へ遺書と遺髪を封筒で送り、宴では涙を見せる者もいた｜五人は全員17歳か18歳 (74) | QC1 FIX → QC2 FIX → QC3 FIX → QC4 FIX | 0 |
| ep09-munemori-442nd | 家族は強制収容所マンザナーにいた。それでも彼は、戦友を守って死んだ (33) | 【第442連隊】家族が収容所で暮らす同じ日、22歳の二世兵はイタリアの敵陣へ単身で突撃した——手榴弾は跳ね返り、戦友二人の穴へ転がり込んだ (69) | QC1 FAIL → QC2 PASS | 0 |
| ep10-miyatake-manzanar | カメラ禁止の収容所で、木箱に隠したレンズが撮り続けた同胞の日常 (31) | 【1943年マンザナー】アンセル・アダムスにレンズを向け返した眼鏡の収容者がいた——所長が彼にスタジオを許した理由｜ロンドン受賞・ロス五輪を撮った写真家 (76) | QC1 PASS | 0 |
| ep11-ando-226incident | 「あの人は西郷のような人だ」と言った男が、その人を撃った雪の朝 (31) | 【二・二六事件】「老人ですから、とどめはお止め下さい」妻の一言で大尉は軍刀を収めた——救われた侍従長の命は9年後、終戦へとつながった (66) | QC1 FAIL → QC2 FIX | 0 |

Sheet cột E 11/11 · CHANEL 11 file `TIEU_DE_MO_TA.txt`, 0 `listting.txt` · bảng dán Studio 6 video đã đăng: `data/DOI_TIEU_DE_STUDIO_irogatatarukioku.md`.
ESCALATE em đã quyết (§5b). QC "FIX" còn lại đều là THUMB_OVERLAP token chủ đề (【沖縄戦】 vs thumb 沖縄…) — không phải lỗi theo luật lane.

## 5b. CẦN XEM (ngoài phạm vi tool — em đã quyết phần tiêu đề, phần còn lại cho tab lane D)
| Tập | Việc | Lý do |
|---|---|---|
| ep02 | (đã quyết: GIỮ tiêu đề) | Sol SPOILER MEDIUM về 階級章をすべて外した + 遺体は見つからなかった; Fable ESCALATE (luật 3 vs luật 6). Em giữ vì 遺体は見つからなかった là câu MỞ ĐẦU kịch bản (khung dẫn), 階級章 có hedge という, cách chết + lời cuối vẫn giấu; kênh mẫu luôn nêu kết cục trong tiêu đề (全員が帰らなかった / 生きて帰れたのは276人) — đó là công thức. |
| ep03 | (đã quyết: GIỮ tiêu đề) | Sol 4 lượt: MISLEADING 連隊旗を焼いて消えた (Fable đã thêm とされる), SPOILER 34人・1947年4月22日. Em giữ: kênh mẫu tập Peleliu cũng đưa 「34人は終戦を知らないまま2年5か月洞窟にいた」 lên tiêu đề — đó là công thức; 消えた cố ý giấu cách chết (luật 6). |
| ep05 | Thumbnail: dòng 「米国本土で唯一の」 → 「米国領で唯一の」 (hoặc 「アメリカ領で唯一の」) | Sol FACTUAL HIGH: Attu là Alaska準州 = 「アメリカの領土」, KHÔNG phải 本土; kịch bản không dùng 本土. Tiêu đề CŨ của mình cũng sai chỗ này, tiêu đề mới đã hết. Fable ESCALATE vì ngoài quyền → em giữ tiêu đề, thumb giao bước 2 lane D. |
| ep07 | Thumbnail: dòng 「百万人が百年かけても落とせない」 nên thêm 「と伝わる」 | Sol FAIL T1 MISLEADING: thumb trình bày như lời xác nhận của Shibasaki, kịch bản nói chỉ là giai thoại Anh ngữ. Fable ESCALATE vì ngoài quyền (tiêu đề không chứa câu này) → em giữ tiêu đề, việc sửa thumb là của bước 2 lane D. |

## 6. Đề tài (ngoài phạm vi tool, ghi để SPACE_RESEARCH biết)
Top kênh mẫu: 特攻 17歳 (107K) · 戦争孤児 12万人 (60K) · 沖縄 dân thường 85% (48K) — **người thường + con số**.
Thua: 講和条約 959 · 風船爆弾 442 · **二・二六事件 152**. 11 tập của mình toàn tướng lĩnh; ep11 trùng đề tài thua nhất.
Đề xuất d12+: lính trẻ / dân thường / trẻ em / người mẹ + 1 con số.

## 7. Nhật ký quyết định
| Ngày | Quyết định |
|---|---|
| 2026-09-20 | Anh giao toàn quyền; chốt L1–L10 (plan.md): công thức kênh mẫu, 60–90/78/35, suffix riêng, tên riêng cho phép, bỏ dòng tags, deliver + xoá listting.txt, ep08 thử đầu. |
| 2026-09-20 | Phase 1: SERP rộng xác nhận nhóm 31–40 ký tự tệ nhất; giữ L2. Thêm 19 mẫu exclude (教養TV/ANN/ゆっくり/放送局…). |

## Thumbnail (S7, gộp 2026-09-22)
Phong cách khoá của lane ở `config/lanes/irogatatarukioku.thumb.yaml` (mẫu kênh / TEMPLATE ở `docs/lanes/irogatatarukioku/thumb/`). `run` tự chạy sau
`deliver`; ảnh chọn `<slug>/thumbnail_final.png`, 3 ảnh + điểm Fable/Opus trong `research/XEM.html` mục 7. DỪNG chờ anh →
`py -3.13 cli.py thumb-publish --slug <dir> --profile irogatatarukioku [--choose B]` mới ghi Sheet G + CHANEL. Chi tiết `docs/thumbnail.md`.

<!-- export 5153746a77e7 · 2026-09-26 -->
