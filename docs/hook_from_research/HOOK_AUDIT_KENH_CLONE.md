# HOOK AUDIT — 9 kênh mình đang clone (2026-09-23, TRENDING-RESEARCH → h2dev)

Người đọc: agent/tab h2dev làm lại hook, tiêu đề, mô tả, thumbnail của từng lane. Research KHÔNG sửa gì trong h2dev.
Bản xem có ảnh thumbnail: `HOOK_AUDIT_KENH_CLONE.html` cùng thư mục. Dữ liệu máy đọc: `data\analysis_<kênh>.json`.
Kho hook dùng chung (đã nạp 130 video, kiểu H01–H41, khoá K01–K23): `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\HOOK_LIBRARY.md`.
Nguyên tắc đã lưu thành skill: `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

| Lane h2dev | Kênh mẫu | Video kênh đã đọc | Tập của mình đã chấm |
|---|---|---|---|
| satori-jp-obaa | 노년의 마음소리 @simbot2 | 15 | 15 |
| toshi-densetsu-jp | 今夜も都市伝説 @konyamotosidensetu | 9 | 9 |
| irogatatarukioku | 色でたどる戦争の記録 UCaj1dslbibbHEnOAOh0tyYw | 9 | 11 |
| kenko-chiebukuro | シニアいきいき健康 UCBODlDy5sXo_49pC7KPr7vQ | 9 | 8 |
| teinengo-real | 老後の暮らし研究所 UCRkP44Mcw-K8IktdTqxC9dg | 9 | 3 |
| teinengo-tanoshimi | 老後のお金ストーリー UCI2cPqBmCPMxxKI4u2Gqs_Q | 10 | 10 |
| teinengo-fuufu | 老後のゴローさん UCxD2Exs2Q4lf7x0Q28OuKvg | 10 | 0 (chưa có tập → có khuôn tập đầu) |
| kokoro-kazoku | 癒しの心理学 UCV_8D2Agr2EaGxod0s7KBtg | 12 | 0 (chưa có tập → có khuôn tập đầu) |
| sengoku-uragawa | どっこい日本史 UCxXV78OIGchz13GAA7RGbEQ | 10 | 0 (chưa có tập → có khuôn tập đầu) |

## Giới hạn dữ liệu (đọc trước khi tin số giây)
YouTube chặn IP giữa chừng. Mốc giây THẬT: simbot2 14/15, toshi 9/9, iro 9/9 (+ một số lời hứa sau 120s là ước tính), vài video lẻ ở kenko/real/tano/fuufu.
Còn lại mốc giây của kênh mẫu là ƯỚC TÍNH từ transcript văn bản (vị trí ký tự ÷ tốc độ đọc, sai số ±5–10s). Mốc giây tập của mình:
thật khi tập đã có giọng (voice_paced.srt / voice.srt), ước tính theo char_rate profile khi chưa có. Mỗi mục trong báo cáo ghi rõ nguồn mốc.
Một số video mới của kênh mẫu mới đăng 1–6 ngày → không dùng để so thắng/thua.

## 10 kết luận chung (đúng ở nhiều kênh — chi tiết + bằng chứng ở từng kênh bên dưới)
1. **Kênh mẫu nào cũng lặp MỘT lời hứa ở 4 chỗ: tiêu đề · chữ thumbnail · câu đầu mô tả · 30–45 giây đầu hook.** Mỗi kênh nối khác nhau
   (simbot2: thumbnail = nguyên tiêu đề; toshi: chữ vàng = câu 0s, chữ đỏ = câu 45s; tano: thumbnail tách tiêu đề làm 2 dòng; kokoro: thumbnail
   nói miệng lại tiêu đề; fuufu: đáy thumbnail = câu khoá hook), nhưng không kênh nào để 4 chỗ nói 4 chuyện. Tập của mình thì thường lệch:
   satori tiêu đề↔hook khớp 3/15; iro thumbnail↔tiêu đề khớp 0/11 (TITLE_LOCK cố tình tách chữ); toshi 4/8 tiêu đề/thumbnail đi hướng giải thiêng.
2. **Câu tạo mâu thuẫn đến rất sớm**: simbot2 0–8s, fuufu ≤17s, iro ≤26s (top), toshi 0–20s, sengoku 5–25s, kenko ≤40s, kokoro 0s.
   Tập của mình chậm hơn có hệ thống: satori 9/15 trễ ≥18s hoặc mất; iro trung vị 43,9s (ep01 120s); kenko 4/8 ở 72–116s; toshi 5/8 mở bằng
   biên niên trung tính, bất thường tới ở 19–46s.
3. **Không mở bằng chào / tự giới thiệu / tiểu sử.** kenko kênh 0/6 chào — mình 7/8; kokoro kênh 0/8 tự giới thiệu; fuufu tên-tuổi luôn sau câu
   mâu thuẫn; simbot2 giới thiệu đúng 1 câu ở ~20s. Của mình: satori 05/07 mở bằng tự giới thiệu, tano 7/10 tự giới thiệu ≤22s, iro 7/11 kể
   năm sinh trong 120s (kênh 0/9), kenko 4/6 tập có giọng đọc to chữ 「タイトル」 ở 0,3s (ep01 đã dựng final với lỗi này).
4. **Câu hỏi / lời hứa của tiêu đề được nói ra trong ~30–45 giây.** sengoku top 0–31s vs video thấp 61–68s; tano lõi tiêu đề ≤36s ở 6/7;
   kokoro top trung vị 43s vs thấp 105s; simbot2 ~31s. Của mình: satori 8/15 chưa hứa trong 90s; toshi lời hứa trễ tới 7–25 phút ở 4 tập.
5. **Mỗi kênh có một câu "nghi thức" khoá hook — phải giữ**: simbot2 「điều cuối vẫn khó nói」 (K12); toshi chuỗi なぜ + 「それでは…最初から辿っていこう」
   (K13); iro 「この写真をカラー化してみる」 + miễn trừ AI + 「N枚の写真で辿っていく」 (K16); tano 「この時の俺はまだ知らなかった」 (K03) sau câu người khác;
   fuufu câu khoá lặp lại ở cuối video; kokoro 「〜ではなく〜」 + gỡ tội; sengoku 「さあ、教科書には載らない歴史の裏側へ」 (K23).
   Tập của mình bỏ rơi: iro カラー化 0/11, N枚 0/11; toshi なぜ ≥2 chỉ 2/8; satori 1/15; tano K03 đúng chỗ 1/10.
6. **Chép CƠ CHẾ, không chép CÂU của một video hit.** iro 11/11 tập mở bằng cùng câu 「（まず、）この一枚の（肖像）写真をご覧いただ…」 nhưng mất phần làm nên hook;
   real 3/3 tập dùng khung 「A俺とB同期 どっちが」 của đúng 1 video (kênh dùng 7 kiểu mở khác nhau cho 7 video).
7. **Giấu đáp án, đừng đọc trước danh sách.** kenko kênh 0/6 nêu tên món trong 120s, mục 1 ở 329–410s — mình 8/8 đọc trước cả 5 mục; kenko và tano:
   thumbnail cho thấy mục GIỮA danh sách, giấu 第1位 (0/4 và 4/4).
8. **Lời hứa không giữ = rủi ro comment bắt lỗi.** Phải grep mọi vế tiêu đề/thumbnail trong script.txt. Đã thấy: satori ep04 「四文字」 không có,
   ep07 thumbnail 「僕でも下ろせない」 không có; tano ep06 「1円も使わず」「若返る」 bị chính script phủ nhận, ep02 「趣味」「夢中」, ep05 「静かに楽しく」 không có;
   iro ep01/02 ngoặc kép cho câu diễn ý, ep05 thumbnail ghi 米国本土 (Attu là Alaska), ep06 tiêu đề 2年7ヶ月 vs hook 三年後.
9. **Đề tài/độ nổi tiếng đặt trần view trước hook** (toshi, iro, real, tano, sengoku đều có video hook tốt mà view thấp vì đề tài hẹp).
   Sửa hook là cần nhưng không đủ; chọn đề tài theo bằng chứng từng kênh (iro: người thường/người trẻ 7/8 video ≥10k; tano: N選 vui/rẻ 85k vs 7,5k;
   sengoku: trục 織田–豊臣–徳川; fuufu: tiêu đề có 「夫婦」 / 2 người đối lập; real: một QUYẾT ĐỊNH chung, không cần số tiền).
10. **Gate h2dev đang đo ĐỘ DÀI, không đo THỨ TỰ.** toshi `hook_chars` sàn 650 làm 4–5/9 video của chính kênh mẫu trượt; kenko `hook_chars`+`hook_marker`
    thưởng thói quen đọc trước danh sách; tano gate không nhìn 0–60s. Đề xuất thêm gate thứ tự: câu chốt ≤Ns, lõi tiêu đề ≤30–36s, chữ thumbnail có
    trong hook, không chào ở 0s, câu nghi thức của kênh có mặt (ngưỡng từng lane ở phần kênh).

## Vệ sinh file cần chốt trước khi đăng
satori 01/11 có 2 thumbnail khác nhau (DANG-TAI trỏ thumb_final.png, thumbnail_final.png mới hơn), 09 thumb_text.txt cũ; toshi ep03 2 thumbnail,
6/8 TIEU_DE_MO_TA.txt khác S4_MO_TA.json, ep08 mốc chương dính thân bài, ep10 mốc chương còn placeholder; iro ep01 2 thumbnail, không tập nào có
DANG-TAI.txt; kenko/tano/real gần như chưa có thumbnail + mô tả.

## Thứ tự ưu tiên đề xuất cho h2dev
1. Tập CHƯA dựng (rẻ nhất): toshi ep10, kenko ep02–08, tano ep02–10, real ep01–03, satori 02/03/05/13 — sửa script mở đầu trước khi thu giọng.
2. Lời hứa không giữ (mục 8) — sửa tiêu đề/thumbnail, không cần dựng lại.
3. Tập đã dựng có hook hỏng nặng: satori 07/05/01, iro ep01/ep03/ep05/ep07, toshi ep08/ep06/ep05, kenko ep01 (đọc 「タイトル」) — dùng hook repair mode.
4. Gate thứ tự (mục 10) để lỗi không lặp ở tập sau.


## 노년의 마음소리 (simbot2) → lane `satori-jp-obaa`

Kênh: https://www.youtube.com/@simbot2

Một khung cố định 15/15: câu thoại nghịch lý giây 0 (H22/H23) → lật thêm 1 lần → giới thiệu 1 câu ~20s → hứa N điều + 'điều cuối vẫn khó nói' ~31s (K12) → hỏi thẳng khán giả. Tiêu đề hứa THÔNG TIN, hook là CHUYỆN làm bằng chứng; chữ thumbnail = nguyên tiêu đề; mô tả = tiêu đề.

### Khung hook theo giây
- **0–10s · Câu thoại nghịch lý** — Người trong cuộc nói điều trái lẽ, hoặc người kể tự thú hành động lạ Ví dụ: 「어머니, 그 돈 저도 못 꺼냅니다.」 (TISOm_7M_vM)
- **10–25s · Lật thêm một lần** — Câu thứ hai làm câu đầu khó hiểu hơn Ví dụ: 「외로운 영감? 아니야. 외로운 영감은 오래 걸려.」 (l0p1EnDcXYM)
- **15–30s · Giới thiệu 1 câu** — Tuổi, tên, nơi ở, sống một mình bao năm Ví dụ: 「저는 올해 일흔셋 된 박순례라고 합니다.」 (TISOm_7M_vM)
- **25–50s · Hứa đúng lời tiêu đề + điều cuối khó nói** — Đọc lại tiêu đề thành N điều, nhử điều cuối Ví dụ: 「셋째는 지금도 입에 올리기가 조심스럽습니다.」 (Hhe56wqubbU)
- **35–60s · Hỏi thẳng khán giả** — Hỏi về chính cuộc sống người xem rồi 'chuyện bắt đầu từ…' Ví dụ: 「여러분은 어떠십니까?」 (66weQbaUZuk)

- Tiêu đề: Lời hứa thông tin: vấn đề/câu hỏi + 'N가지 / 진짜 이유 / 충격적인 진실' + người có thẩm quyền (은행 지점장, 간호사, 장례지도사).
- Thumbnail: Chỉ chữ, không nhân vật, chép NGUYÊN tiêu đề (15/15), nền hoa mờ, chữ 3 màu viền dày.
- Mô tả: Tiêu đề chép lại hoặc viết lại một chút (15/15).
- 4 phần nối nhau: Một lời hứa lặp ở 4 chỗ: tiêu đề = thumbnail = mô tả; hook là bằng chứng sống và đọc lại lời hứa ở ~giây 30. 14/15 cảnh mở trúng chủ đề tiêu đề trong 10 giây đầu.
- Số đếm: Câu chốt giây 0–8: 15/15 · giới thiệu trung vị ~20s · hứa N điều trung vị ~31s · 'điều cuối khó nói' 15/15
- Ngoại lệ: Tập 01 mở bằng chuyện bạn chuyển nhà, giây 35 mới nối về tiêu đề (vẫn 1 triệu view nhờ đề tài lương hưu).

Thắng vs thua: Top (01 1,01tr; 07 726k) và thấp nhất (05 174k) dùng cùng khung; 05 thua do dài 44 phút và đề tài tang lễ hẹp, không do hook.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clone | 1,011,142 | 5 | 35 | 28 | 35 | H22 H23 K12 | 10 | P | K | P | 연금 310만 원을 말한 뒤 40년 계모임이 깨졌습니다… 노후에 말하면 안 되는 4가지 |
| clone | 327,668 | 5 | 28 | 12 | 28 | H22 K12 | 10 | K | K | K | 부모님이 오래 살수록 자식의 삶까지 무너질 수 있습니다. 부모와 함께 지옥으로 끌려가지 않으려면 절대 잊지 말아야 할 3가지 |
| clone | 415,706 | 0 | 55 | 46 | 55 | H23 K03 K12 | 11 | K | K | K | 노년 재혼·동거, 무엇이 가장 무서울까요? 직접 겪은 세 사람의 이야기｜많은 분들이 "진작 볼 걸" 후회합니다 |
| clone | 669,370 | 3 | 25 | 12 | 25 | H22 K12 | 11 | K | K | K | 요양원에서 진짜 무서운 건 학대가 아니었습니다… 74세 노인이 석 달을 못 버티고 짐을 싼 이유 |
| clone | 173,756 | 5 | 47 | 25 | 47 | H22 K12 | 11 | K | K | K | "절대 장례식을 치르지 마라" 갈수록 늘어나는 노인들의 유언… 장례지도사가 털어놓은 가슴 찢어지는 3가지 진실 |
| clone | 478,311 | 3 | 30 | 20 | 30 | H22 K12 | 11 | K | K | K | 70세가 넘은 여성들이 여전히 남자를 찾는 진짜 이유… 예상 밖이었습니다 |
| clone | 725,736 | 0 | 30 | 16 | 30 | H22 K12 | 11 | K | K | K | 만약 어느 날 갑자기 세상을 떠난다면… 은행 예금 전액을 자녀가 받을 수 있을까? 은행 지점장이 밝힌 충격적인 진실 |
| clone | 319,314 | 8 | 31 | 18 | 31 | H22 K12 | 11 | K | K | K | 【전직 은행원의 경고】70세가 넘어서도 여기에 돈을 넣어 두고 있다면 당장 멈추세요｜은행은 절대 알려주지 않습니다 |
| clone | 241,044 | 32 | 50 | 38 | 50 | H22 K12 | 10 | K | K | K | 나이 들어 돈이 있다면 가장 먼저 사야 할 3가지… 늦으면 반드시 후회합니다 |
| clone | 207,120 | 0 | 45 | 33 | 45 | H22 K12 | 10 | K | K | K | 죽기 한 달 전부터 몸에 나타나는 변화｜간호사가 알려줬습니다 |
| clone | 536,781 | 0 | 25 | 15 | 25 | H23 K12 | 10 | K | K | K | "통장에 얼마 있냐"는 자식 물음에 81세가 내놓은 기막힌 대답 |
| clone | 190,242 | 20 | 38 | 28 | 38 | H23 K12 | 11 | K | K | K | 70세를 막 넘겼는데 몇 년 안 돼 세상을 떠나는 노인이 많습니다… 대체 왜일까요? |
| clone | 155,057 | 0 | 30 | 18 | 30 | H04 H23 K12 | 11 | K | K | K | 65세에 ‘이만큼의 돈’이 있는 사람은… 노후의 승자입니다｜이 기준, 놀랄 만큼 정확합니다 |
| clone | 657,031 | 0 | 35 | 25 | 35 | H22 K03 K12 | 11 | K | K | K | 60세 이후, 절대 가까이하면 안 되는 여자 4부류… 잘못 만나면 말년이 처참합니다 |
| clone | 431,117 | 0 | 22 | 12 | 22 | H22 K12 | 11 | K | K | K | 나이 들수록 예금은 어디에 둬야 할까? 73세 노인의 방법이 너무 현명했습니다 |

#### 연금 310만 원을 말한 뒤 40년 계모임이 깨졌습니다… 노후에 말하면 안 되는 4가지 — https://www.youtube.com/watch?v=vU5PWT2zLDs
- Câu chốt (5s): 「김장김치 두통을 싸들고 50년직이 명잔의 아파트에 갔습니다. 그런데 문을 연 건 처음 보는 젊은 여자였습니다. 명잔네는 3년 전에 이사를 갔다더군요. 3년입니다. 저만 몰랐던 거지요. 그 주 목요일 하 벤치에서 따져」
- Câu khoá (35s): 「Hứa 5 chuyện (4 lời mất bạn + 1 điều bạn giữ), chuyện thứ 4 là 'vết nhơ của tôi'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 친한 사이일수록 절대 입 밖으로 꺼내지 마세요… 73세 노인이 뼈저리게 후회한 4가지
- Hook↔tiêu đề: P — Mở bằng chuyện bạn chuyển nhà, không phải chuyện lương hưu. Tới giây 35 mới nối về tiêu đề: 'hôm nay kể những điều tôi mất vì lỡ miệng'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: P — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Bí ẩn 'bạn giấu địa chỉ' bật ở giây 5, câu đáp khó hiểu ở giây 20 — người xem cần 'cả một mùa' như người kể mới hiểu.
- Điểm yếu: Tiêu đề hứa '4 điều không nên nói' nhưng hook là truyện bạn thân; kênh vẫn 1 triệu view nhờ đề tài lương hưu.

#### 부모님이 오래 살수록 자식의 삶까지 무너질 수 있습니다. 부모와 함께 지옥으로 끌려가지 않으려면 절대 잊지 말아야 할 3가지 — https://www.youtube.com/watch?v=YU0rS1qW_aY
- Câu chốt (5s): 「새벽 2시 부엌이었습니다. 물을 마시러 나왔다가 냉장고 문꼬이를 잡은 채 그대로 굳어 버렸지요. 베란다에서 딸이 울면서 전화를 하고 있었거든요. 나 요즘 무서운게 뭔지 알아? 엄마가 오래 살까 봐 무서워. 나 쓰레기」
- Câu khoá (28s): 「Vì 1 lý do 40 năm trước + 3 điều giữ nhà khỏi sập; điều 3 'run tay'; giọng con giống giọng ai 40 năm trước」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: “부모님의 장수가 두려운 저는 쓰레기인가요?” 간병 지옥에서 가족 모두가 파멸하지 않으려면 절대 잊지 말아야 할 3가지
- Hook↔tiêu đề: K — Câu thoại ở giây 5 ('sợ mẹ sống lâu') chính là nỗi sợ trong tiêu đề. Mô tả trích nguyên câu đó. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Câu thoại tàn nhẫn nhất có thể từ con → mẹ, rồi lật ngay 'tôi không giận' — mâu thuẫn chồng mâu thuẫn trong 20s.
- Điểm yếu: Tiêu đề trừu tượng (3 điều không quên) không nhắc câu thoại.

#### 노년 재혼·동거, 무엇이 가장 무서울까요? 직접 겪은 세 사람의 이야기｜많은 분들이 "진작 볼 걸" 후회합니다 — https://www.youtube.com/watch?v=Kmxva85WKec
- Câu chốt (0s): 「7년을 남편처럼 산 사람의 장례식에서 저는 방명록에 아는 사람이라고 적었습니다. 장례식장 입구에서는 흰봉투를 만지작거렸지요. 부위금으로 5만 원이면 너무 야박하고 10만 원이면 남들이 이상하게 볼 거 같고 7년을 한」
- Câu khoá (55s): 「'Lúc đó tôi chưa biết trong hộp của ông có tờ giấy ghi tên tôi' + 3 người, câu trả lời cuối 'phải lấy hơi'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 노년 재혼·동거, 무엇이 가장 무서울까요? 직접 겪은 세 사람의 이야기｜많은 분들이 "진작 볼 걸" 후회합니다
- Hook↔tiêu đề: K — Ghi 'người quen' ở sổ tang = nỗi sợ của sống chung không đăng ký. Tới giây 55 nói lại lời hứa '3 người'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Hành động nhỏ (ghi 2 chữ) gói trọn nỗi đau pháp lý của sống chung không đăng ký; K03 ở giây 20 cài bí ẩn tờ giấy.
- Điểm yếu: 

#### 요양원에서 진짜 무서운 건 학대가 아니었습니다… 74세 노인이 석 달을 못 버티고 짐을 싼 이유 — https://www.youtube.com/watch?v=Fgc8IQvQVj8
- Câu chốt (3s): 「어르신,이 가방은 누구 겁니까? 요양원 현관에서 짐을 실어 주던 직원이 물었습니다.  하나는 내 거고 하나는 죽은 사람 거예요. 내가이 가방 인자한테 짜장면 빚이 있어서 그것부터 갚으러 가는 길입니다. 저는 올해 이」
- Câu khoá (25s): 「3 điều phải hỏi trước khi vào; điều 3 'vẫn dè dặt'; hỏi khán giả 'có đang gập dần chỗ của mình?'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 74세에 요양원에 들어갔다가 88일 만에 뛰쳐나온 이유… 입소 전 꼭 확인해야 할 3가지
- Hook↔tiêu đề: K — Giây 0 là cảnh xách túi rời viện dưỡng lão. Giây 16 nói luôn '88 ngày thì ra' đúng như tiêu đề. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Câu đáp 'túi của người chết' + 'nợ tô mì' ở giây 5 — kỳ quặc, ấm áp, không đoán được.
- Điểm yếu: 

#### "절대 장례식을 치르지 마라" 갈수록 늘어나는 노인들의 유언… 장례지도사가 털어놓은 가슴 찢어지는 3가지 진실 — https://www.youtube.com/watch?v=Hhe56wqubbU
- Câu chốt (5s): 「지난해 11월 끝자락이었습니다. 1은 넘은 할머니 한 분이 제 상담실 탁자 앞에 꽃꼬이 앉으시더니 인사가 책 끝나기도 전에 이렇게 물으셨습니다. 우리 영감이 그럽디다. 나는 받으면 안 되는 사람이야 하고요. 지도사님」
- Câu khoá (47s): 「3 sự thật; điều 3 dè dặt; 2 cụ cho phép kể; hỏi khán giả có người thân nói câu đó không」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: "내가 죽은 뒤 장례식은 치르지 마라"는 노인들, 도대체 무슨 사연일까? 장례지도사가 털어놓은 3가지 현실
- Hook↔tiêu đề: K — Câu 'đừng tổ chức đám tang' của tiêu đề xuất hiện ở giây 38, người kể là giám đốc tang lễ như tiêu đề. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Câu thoại bí ẩn + chuyên gia 32 năm thú nhận không hiểu → người xem được mời giải đố cùng.
- Điểm yếu: Video 44 phút, view thấp nhất nhóm (174k).

#### 70세가 넘은 여성들이 여전히 남자를 찾는 진짜 이유… 예상 밖이었습니다 — https://www.youtube.com/watch?v=sYRr33eHYSM
- Câu chốt (3s): 「응급실 복도에서 내 딸이 소리를 질렀습니다.이 여자분이 왜 우리 아버지 보호자예요? 네. 아버지 휴대폰 비상 연락처에 왜이 아줌마가 1번이냐고요? 나는 혀가 굳어 말 한마디 못 하고 침대에 누워 그 소리를 다 들었습」
- Câu khoá (30s): 「Lý do thật đàn bà 70+ tìm đàn ông — tôi hiểu ở hành lang đó; 'đồn sai, con sai, tôi cũng sai'; hỏi khán giả có tên để ghi ô bảo lãnh」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 70세가 넘은 여성들은 왜 여전히 남자를 찾을까요? 그 이유는 뜻밖이었습니다
- Hook↔tiêu đề: K — Giây 30 đọc gần nguyên tiêu đề: 'lý do thật đàn bà 70+ tìm đàn ông, tôi hiểu ở hành lang bệnh viện'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Chi tiết 'số khẩn cấp số 1' biến tin đồn tiêu cực thành câu hỏi, và câu 30s trả thẳng về tiêu đề.
- Điểm yếu: 

#### 만약 어느 날 갑자기 세상을 떠난다면… 은행 예금 전액을 자녀가 받을 수 있을까? 은행 지점장이 밝힌 충격적인 진실 — https://www.youtube.com/watch?v=TISOm_7M_vM
- Câu chốt (0s): 「어머니 그 돈 저도 못 꺼냅니다. 은행에서 25년 밥을 먹고 지점장까지 단 큰아들이 제 아버지 빈소 복도에서 그리 말했습니다. 세상에 남도 아니고 자식이 그것도 은행 지점장이라는 사람이 아버지 통장에든 돈을 못 꺼낸」
- Câu khoá (30s): 「Chuyện ngân hàng con kể riêng; 'nhà nào có sổ tiết kiệm cũng không phải chuyện người khác'; sổ cuối cùng 'nghẹn'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 만약 어느 날 갑자기 세상을 떠난다면… 은행 예금 전액을 자녀가 받을 수 있을까? 은행 지점장이 밝힌 충격적인 진실
- Hook↔tiêu đề: K — Câu mở chính là tiêu đề: con trai giám đốc ngân hàng cũng không rút được tiền của bố. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Nghịch lý kép (con + chuyên gia vẫn bất lực) đúng nỗi sợ khán giả; khớp tiêu đề 100%.
- Điểm yếu: Video 726k — hook mạnh nhất nhóm.

#### 【전직 은행원의 경고】70세가 넘어서도 여기에 돈을 넣어 두고 있다면 당장 멈추세요｜은행은 절대 알려주지 않습니다 — https://www.youtube.com/watch?v=Kb5Ej4ZNBgQ
- Câu chốt (8s): 「금자야, 그 서류. 내일 나랑 은행 가서 물리자. 아이고야. 첫말로 네가 뭔데 자꾸 물리라 말아야 은행 직원이라도 되나? 내가 그걸 팔던 사람이라 그런다. 38년을이 손으로 습관을 준 금자손이 그대로 멈췄습니다. 새」
- Câu khoá (31s): 「1 điều ngân hàng không bao giờ nói trước; chuyện 1 cụ giấu 18 năm; 'sổ trong tủ bạn có thể in cùng chữ'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 【전직 은행원의 경고】70세가 넘어서도 여기에 돈을 넣어 두고 있다면 당장 멈추세요｜은행은 절대 알려주지 않습니다
- Hook↔tiêu đề: K — Giây 10 là 'tôi là người từng bán nó' = cựu nhân viên ngân hàng cảnh báo. Giây 31 đọc lại tiêu đề. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Câu 'tao là người từng bán nó' lật vai người kể ở giây 10 — uy tín nội gián.
- Điểm yếu: 

#### 나이 들어 돈이 있다면 가장 먼저 사야 할 3가지… 늦으면 반드시 후회합니다 — https://www.youtube.com/watch?v=rNGGuRG-wu0
- Câu chốt (32s): 「지난달 월요일 아침 은행 창구에서 있었던 일부터 말씀드려야겠습니다. 번호표를 뽑고 한시간을 기다려서 통장하고 손수건에 싼 인도장을 내밀고 360만 원을 현금으로 찾겠다고 했지요. 그런데 젊은 창고 직원이 통장을 받아」
- Câu khoá (50s): 「3 thứ nên mua; 'thứ rẻ nhất 25.000 won lại đáng sợ nhất' — để cuối; 'đặt tay lên ngực'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 나이 들어 돈이 있다면 가장 먼저 사야 할 3가지… 늦으면 반드시 후회합니다
- Hook↔tiêu đề: K — Cảnh rút tiền ở ngân hàng, giây 50 đọc lại tiêu đề: 'có tiền thì mua 3 thứ trước'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Nghi lừa đảo → lật thành tự lừa mình; teaser giá rẻ nhất đáng sợ nhất rất cụ thể.
- Điểm yếu: 

#### 죽기 한 달 전부터 몸에 나타나는 변화｜간호사가 알려줬습니다 — https://www.youtube.com/watch?v=66weQbaUZuk
- Câu chốt (0s): 「죽는다던 사람이 부엌에서 국수를 삼고 있었습니다. 골목까지 멸치육수 냄새가 흘러나오기에 설마하고 문을 열었더니 보름 넘게 미음도 겨우 넘기던 사람이 머리까지 곱게 빚고 서서 웃는 겁니다. 예 왔니? 배고프지? 저는 」
- Câu khoá (45s): 「'Yeongja, đây là dấu hiệu thứ 4' → 6 dấu hiệu trước khi mất, dấu hiệu 6 để cuối; hỏi 'đã nói hết lời chào cuối chưa?'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 죽기 한 달 전부터 몸에 나타나는 변화｜간호사가 알려줬습니다
- Hook↔tiêu đề: K — Giây 25 'đây là dấu hiệu thứ 4', giây 45 hứa 6 dấu hiệu do y tá dạy = tiêu đề. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Câu đầu tiên đã là nghịch lý (sắp chết – đang nấu), câu 25s biến niềm vui thành dấu hiệu tử vong — cú lật mạnh.
- Điểm yếu: Thumbnail chỉ có chữ, không cảnh.

#### "통장에 얼마 있냐"는 자식 물음에 81세가 내놓은 기막힌 대답 — https://www.youtube.com/watch?v=DXXwIxhcfF0
- Câu chốt (0s): 「설날 아침이었습니다. 저는 40여선 먹은 아들 앞에 통장 대신 공책 한 권을 밀어 놓았습니다. 긴장날 네가 물었던 것 오늘 대답해 주마. 아들은 그 공책을 딱 두 장 넘기고는 떡국상 앞에서 울음을 터트렸습니다. 46」
- Câu khoá (25s): 「Câu trả lời của bà chị 81 tuổi; chuyện nặng hơn ở sau; 'con hỏi thì bạn có cười trả lời được không?'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: "노후 통장에 얼마 있는지, 자식에게 말해야 하나…" 81세 노인이 내놓은 뜻밖의 답
- Hook↔tiêu đề: K — Giây 0 trả lời đúng câu hỏi trong tiêu đề (con hỏi mẹ có bao nhiêu), giây 25 nhắc 'câu trả lời của bà 81 tuổi'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Vật thay thế (vở thay sổ) + phản ứng quá mức (đàn ông 46 tuổi khóc) → người xem muốn biết trong vở viết gì.
- Điểm yếu: 

#### 70세를 막 넘겼는데 몇 년 안 돼 세상을 떠나는 노인이 많습니다… 대체 왜일까요? — https://www.youtube.com/watch?v=FBkmqYvEyXQ
- Câu chốt (20s): 「여기 다 적어 놨어. 통장이 어느 서랍에 있고 도장이 어디 있고 보험은 뭐가 들었는지 나 없어도 임자 고생하지 말라고 남편이 석다를 공들여쓴 공책이었습니다. 저는 그걸 받아드는 대신 남편이 보는 앞에서 북 찢어버렸습」
- Câu khoá (38s): 「Vì sao người vừa qua 70 ra đi sớm; 'đáng sợ nhất không phải bệnh mà là AI khiến ông bắt đầu'; 'nếu ông nhà hay cho đồ đi…'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 70세를 막 넘겼는데 몇 년 안 돼 세상을 떠나는 노인이 많습니다… 대체 왜일까요?
- Hook↔tiêu đề: K — Giây 20 'cuốn này xong là ông chết' trả lời câu hỏi tiêu đề 'vì sao qua 70 thì ra đi sớm'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Hành động bạo liệt của vợ hiền + lời giải thích ở giây 20 như một lời nguyền.
- Điểm yếu: 

#### 65세에 ‘이만큼의 돈’이 있는 사람은… 노후의 승자입니다｜이 기준, 놀랄 만큼 정확합니다 — https://www.youtube.com/watch?v=djMUfpGoUQI
- Câu chốt (0s): 「통장에는 2억이 넘는 돈이 들어 있었습니다. 그런데 저는 재작년 겨울 보일러가 죽은 집에서 전기 장판 한 장에 이불 두 채를 덮고 사흘밤을 잤습니다. 설비 기사 번호를 눌러 놓고는 통화 단추 하나를 끝내 못 눌렀지요」
- Câu khoá (30s): 「Công thức người thắng tuổi già học ở quán canh; con số phía sau dè dặt; 'sổ của bạn tháng trước tăng hay giảm?'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 65세에는 얼마가 있어야 노후의 승자일까요? 답은 바로 '이 금액'입니다｜이 기준, 놀랄 만큼 정확합니다
- Hook↔tiêu đề: K — Có 200 triệu mà chịu lạnh = câu hỏi 'bao nhiêu tiền thì thắng'. Giây 30 hứa 'công thức'. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Nghịch lý có-nhiều-mà-thiếu bằng con số cụ thể + câu hỏi khán giả tự nhẩm sổ mình.
- Điểm yếu: 

#### 60세 이후, 절대 가까이하면 안 되는 여자 4부류… 잘못 만나면 말년이 처참합니다 — https://www.youtube.com/watch?v=l0p1EnDcXYM
- Câu chốt (0s): 「거울 속에서 그 여자가 웃으며 물었습니다. 원장님,  세상에서 제일 쉬운 영감이 어떤 영감인 줄 아세요? 파마로들을 말던 제 손이 저도 모르게 멈췄지요. 여자는 제 대답을 기다리지도 않고 옆자리에 앉은 젊은 여자한테」
- Câu khoá (35s): 「'Câu tiếp theo tôi không quên được' + 4 loại đàn bà, học từ tuổi già của anh trai; câu trả lời cuối để cuối」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 60세 이후, 절대 가까이하면 안 되는 여자 4부류… 잘못 만나면 말년이 처참합니다
- Hook↔tiêu đề: K — Kẻ lừa bàn nghề trong gương = 'loại đàn bà phải tránh'. Giây 35 hứa 4 loại. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Nghe lỏm kẻ lừa bàn nghề — người xem thành người trong cuộc; câu 'không phải ông cô đơn' lật dự đoán.
- Điểm yếu: 

#### 나이 들수록 예금은 어디에 둬야 할까? 73세 노인의 방법이 너무 현명했습니다 — https://www.youtube.com/watch?v=HD-ADEBz5oM
- Câu chốt (0s): 「이 돈을요, 내가 못 찾아가게 좀 막아주시오. 은행 창고에서 그런 말이 들려왔습니다. 창고아가 씨가 당황해서 되묻더군요. 천생님, 본인 예금인데 본인이 못 찾으시게요. 옆 창고에 앉아있던 저는 저도 모르게 고개를 돌」
- Câu khoá (22s): 「4 chỗ để tiền của cụ 73 tuổi; chỗ thứ 4 'nghẹn'; 'có tiền trong sổ chưa chắc là tiền của mình'」
- Chữ thumbnail: = nguyên văn tiêu đề · Mô tả: 나이 들수록 예금은 어디에 둬야 할까? 73세 노인의 방법이 너무 현명했습니다
- Hook↔tiêu đề: K — Câu xin ngân hàng chặn tiền của chính mình = 'để tiền ở đâu', sau đó hứa 4 chỗ. · Thumb↔tiêu đề: K — Chữ thumbnail chép nguyên tiêu đề · Thumb↔hook: K — Giống hook↔tiêu đề vì thumbnail = tiêu đề
- Vì sao giữ người: Yêu cầu ngược đời ở giây 0, người kể là người ngồi quầy bên nghe lỏm.
- Điểm yếu: Không lấy được transcript theo mốc giây (YouTube chặn) — nguyên văn lấy từ competitor.txt h2dev.

### Các tập của mình

9/15 tập đẩy câu chốt muộn ≥18s hoặc bỏ mất; 8/15 chưa hứa N điều trong 90s; chỉ 1/15 có câu 'điều cuối khó nói'; 05 và 07 mở bằng tự giới thiệu. Tiêu đề JP kiểu truyện nên chỉ 3/15 trúng hook 30s đầu; 7/12 thumbnail lệch hẳn tiêu đề.

#### Tập 01 — 「3年前に越されましたよ」毎週会う50年の親友が住所を隠した理由
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-01-vU5PWT2zLDs` · có final.mp4 · ưu tiên cao ()
- Mốc: chốt 32 · giới thiệu — · hứa — (voice_paced.srt)
- Thumbnail: thumbnail_final.png (mới hơn). Gói đăng DANG-TAI.txt lại trỏ thumb_final.png = 「光江の家｜三年前から｜知らない女｜正体は誰｜五十年の友が黙り続けた」 — 毎週会っていたのに｜3年前に｜引っ越していた｜私だけ知らなかった
- Tiêu đề↔hook: P — Câu trong ngoặc của tiêu đề có trong hook nhưng ở giây 32. · Thumb↔tiêu đề: K · Thumb↔hook: K
- Vấn đề: tả cảnh 25s đầu, câu 'đã chuyển 3 năm' ở giây 32, tới giây 90 chưa có lời hứa N điều.
- **Sửa:** Bỏ 25 giây tả hộp thức ăn/mùi; mở ngay bằng người lạ mở cửa 'đã chuyển đi 3 năm'. Đưa câu chất vấn ở ghế đá + câu đáp khó hiểu của bạn vào trước giây 20.
- Video mẫu: vU5PWT2zLDs

#### Tập 02 — 【老老介護】手帳の最後に鉛筆で「たすけて」…倒れたのは80歳の母ではなく娘
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY` · chưa có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 39 · giới thiệu 65 · hứa — (voice_paced.srt)
- Thumbnail: thumbnail_final.png — 娘が泣いた｜長生きが怖い｜40年前の私も｜娘を責められなかった
- Tiêu đề↔hook: L — Tiêu đề nói 「たすけて」 và 'người ngã là con gái', hook là cảnh con gái khóc lúc 2h sáng. Hook khớp thumbnail, không khớp tiêu đề. · Thumb↔tiêu đề: L · Thumb↔hook: K
- Vấn đề: câu thoại ở giây 39, tự giới thiệu 65s, chưa hứa gì trước 90s.
- **Sửa:** Mở bằng NGUYÊN câu thoại của con gái (sợ mẹ sống lâu, 'tao là rác nhỉ?'), không dẫn địa danh/giờ trước. Sau đó 'tôi không giận — vì 1 chuyện 40 năm trước'.
- Video mẫu: YU0rS1qW_aY

#### Tập 03 — 籍は入れぬまま七年…四十九日の後、事実婚の妻に長男が届けた封筒の中身
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-03-Kmxva85WKec` · chưa có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 18 · giới thiệu 74 · hứa 83 (voice_paced.srt)
- Thumbnail: thumbnail_final.png — 本当の夫婦だ｜延命治療の相談に｜入れなかった｜法律上は赤の他人
- Tiêu đề↔hook: P — '7 năm' và chữ 'người quen' có ở giây 18. 'Phong bì con trưởng mang tới' không được nhử trong 90 giây đầu. · Thumb↔tiêu đề: L · Thumb↔hook: L
- Vấn đề: mở đúng cảnh nhưng đẩy 'tờ giấy có tên tôi' ra khỏi 90s đầu — mất câu khoá K03.
- **Sửa:** Giữ cảnh mở, nhưng rút gọn còn 15 giây và thêm lại câu khoá 'lúc đó tôi chưa biết trong hộp của ông có tờ giấy ghi tên tôi'.
- Video mẫu: Kmxva85WKec

#### Tập 04 — 特養で本当に怖いのは虐待ではなかった…元看護婦が遺した四文字の言葉
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-04-Fgc8IQvQVj8` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 23 · giới thiệu 35 · hứa 60 (voice_paced.srt)
- Thumbnail: thumb_final.png — 親友が逝った｜涙が出なかった｜心が渇いていた｜気づいた瞬間、家に帰った
- Tiêu đề↔hook: P — Hook có cảnh rời viện, nhưng 'bốn chữ' của tiêu đề không có trong script.txt: tìm「文字」và mọi câu「」dài 4 ký tự đều không ra. · Thumb↔tiêu đề: L · Thumb↔hook: L
- ⚠ Lời hứa không giữ: Tiêu đề hứa 「元看護婦が遺した四文字の言葉」 — không có「文字」hay câu「」4 ký tự nào trong script.txt
- Vấn đề: giữ cấu trúc (hứa 3 điều 60s, điều 3 sợ 78s) nhưng bỏ dạng hội thoại, chậm gấp đôi.
- **Sửa:** Đổi đoạn tường thuật thành hội thoại: nhân viên hỏi 'túi này của ai?' — 'một của tôi, một của người đã mất'. Cấu trúc sau đó đã đúng, chỉ cần nén một nửa.
- Video mẫu: Fgc8IQvQVj8

#### Tập 05 — 葬式の帰り、79歳の夫が漏らした一言「わしは受け取ってはいけない人間じゃ」
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-05-Hhe56wqubbU` · chưa có final.mp4 · ưu tiên cao ()
- Mốc: chốt 44 · giới thiệu 0 · hứa — (voice_paced.srt)
- Thumbnail: thumbnail_final.png — 弔いに丁寧な夫が｜香典帳は40年｜自分だけ拒んだ｜まだ終わっていない弔いがある
- Tiêu đề↔hook: P — Câu trích của tiêu đề ở giây 44. Hook mở bằng tự giới thiệu. Mô tả lại trích một câu khác (「わしが死んでも葬式はするな」). · Thumb↔tiêu đề: P · Thumb↔hook: L
- Vấn đề: mở bằng tự giới thiệu 24s (kiểu H12 bị cấm), câu thoại ở giây 44.
- **Sửa:** Đang mở bằng tự giới thiệu (kiểu H12 bị hook_stage cấm). Đưa câu thoại của cụ bà 'ông nhà tôi bảo: tôi là người không được nhận' lên giây 0.
- Video mẫu: Hhe56wqubbU

#### Tập 06 — 78歳一人暮らしの私が倒れた朝…合鍵で駆け込んだのは「男を探す女」と噂の71歳
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 28 · giới thiệu 59 · hứa — (voice_paced.srt)
- Thumbnail: thumb_final.png — 娘は疑った｜「お金ですか」と｜薬の時間まで知っていた｜恋でも、金でもなかった
- Tiêu đề↔hook: P — Hook ở bệnh viện, con gái chất vấn bà. Cảnh 'chạy vào bằng chìa khoá dự phòng' của tiêu đề không nằm trong hook. · Thumb↔tiêu đề: P · Thumb↔hook: K
- Vấn đề: tả phòng bệnh 18s, câu hỏi con gái ở giây 28 và bỏ chi tiết 'số khẩn cấp số 1'; câu nối về tiêu đề không có trong 90s.
- **Sửa:** Mở bằng tiếng hét của con gái và thêm lại chi tiết bị mất: 'số khẩn cấp số 1 của bố là bà này'. Nối ngay về tiêu đề: 'lý do thật tôi hiểu ở hành lang đó'.
- Video mẫu: sYRr33eHYSM

#### Tập 07 — 夫を亡くした翌日、通帳が凍り督促状が届いた…通夜で義弟が囁いた一言
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-07-TISOm_7M_vM` · có final.mp4 · ưu tiên cao ()
- Mốc: chốt — · giới thiệu 0 · hứa 14 (voice_paced.srt)
- Thumbnail: thumb_final.png. Câu 'con cũng không rút được' là câu của bản Hàn; script.txt JP không có nguyên câu này — 母さん｜その金は｜僕でも｜下ろせない｜夫が遺した三行の遺言
- Tiêu đề↔hook: L — Tiêu đề: tài khoản bị đóng băng + câu thì thầm của em chồng. Hook: tự giới thiệu rồi kể buổi sáng chồng ngã. Hai chi tiết đó không có trong 90 giây đầu. · Thumb↔tiêu đề: L · Thumb↔hook: L
- ⚠ Lời hứa không giữ: Thumbnail 「その金は僕でも下ろせない」 là câu bản Hàn, script.txt JP không có nguyên câu
- Vấn đề: bỏ hẳn câu thoại này khỏi 90s đầu, mở bằng tự giới thiệu (H12) rồi kể tuần tự sáng hôm đó.
- **Sửa:** Hook mạnh nhất kênh gốc (726k) bị bỏ hẳn. Mở bằng câu của con trai giám đốc ngân hàng: 'mẹ ơi, tiền đó con cũng không rút được'.
- Video mẫu: TISOm_7M_vM

#### Tập 08 — 元本非保証の信託に移った定期預金1800万円…30分で通帳に戻した三つの質問
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-08-Kb5Ej4ZNBgQ` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt — · giới thiệu 29 · hứa 60 (voice_paced.srt)
- Thumbnail: thumb_final.png — 「その書類｜預金じゃ｜なかった」｜老後を守る警告｜元銀行員が明かす真実
- Tiêu đề↔hook: P — Hook có 'trả giấy về ngân hàng', nhưng 「元本非保証」 và '3 câu hỏi' của tiêu đề không có trong 90 giây đầu. · Thumb↔tiêu đề: K · Thumb↔hook: K
- Vấn đề: giữ hội thoại nhưng bỏ câu lật 'tôi từng bán nó'; hứa 1 điều ở 60s (KO 31s).
- **Sửa:** Giữ hội thoại ở ghế đá nhưng thêm câu lật vai: 'vì tôi là người từng bán nó' (bản JP đang thiếu).
- Video mẫu: Kb5Ej4ZNBgQ

#### Tập 09 — 夫に補聴器を諦めさせた声の正体…今度は73歳の私の耳元でささやいた
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-09-rNGGuRG-wu0` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 38 · giới thiệu 59 · hứa 83 (voice_paced.srt)
- Thumbnail: thumbnail_final.png (thumb_text.txt CŨ ghi khác: 夫の遺した｜五十万円｜私が下ろす) — 娘にも黙って｜50万円｜銀行の窓口で｜詐欺ですかと聞かれた
- Tiêu đề↔hook: P — 'Tiếng nói' có ở giây 38 (tiếng nói tiết kiệm), còn 'máy trợ thính' không có trong 90 giây đầu. · Thumb↔tiêu đề: L · Thumb↔hook: K
- Vấn đề: khá sát (ngân hàng 0s, câu hỏi 30s, 'giọng tiết kiệm' 38s) nhưng tự giới thiệu 59s, hứa 3 thứ ~90s, chưa có teaser 25.000.
- **Sửa:** Gần đạt. Chỉ cần nén: tự giới thiệu trước giây 45, hứa 3 thứ + câu nhử 'thứ rẻ nhất lại đáng sợ nhất' trước giây 70.
- Video mẫu: rNGGuRG-wu0

#### Tập 10 — 抗がん剤をやめた40年の親友が枕元に残した千円札一枚…11年越しの借りの正体
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-10-66weQbaUZuk` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 14 · giới thiệu — · hứa — (voice_paced.srt)
- Thumbnail: chưa có thumbnail — 
- Tiêu đề↔hook: P — Người bạn thân có ngay giây 0, nhưng 'thôi hoá trị', 'tờ 1000 yên', 'món nợ 11 năm' đều không được nhử. · Thumb↔tiêu đề:  · Thumb↔hook: 
- Vấn đề: dài dòng không khí 29s, không có câu 'dấu hiệu thứ 4' và lời hứa 6 dấu hiệu trong 90s.
- **Sửa:** Mở bằng câu nghịch lý 'người được bảo sắp chết đang đứng nấu mì', rồi câu lật 'đây là dấu hiệu thứ 4' trước giây 30. Hứa 6 dấu hiệu.
- Video mẫu: 66weQbaUZuk

#### Tập 11 — 息子に通帳の残高を聞かれ、笑ってごまかした…5年で消えた930万円の行き先
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 13 · giới thiệu — · hứa — (voice_paced.srt)
- Thumbnail: thumb_final.png (DANG-TAI). Bản mới hơn thumbnail_final.png = 「全財産は約250万｜葬儀代は書けず｜420円ノートで筆止まる」 — 通帳に｜いくらあるか｜息子に｜言うべきか｜八十一の姉さんの答え
- Tiêu đề↔hook: P — Tiêu đề là cảnh 'cười cho qua', hook là cảnh đưa cuốn vở ngày Tết (xảy ra sau đó). Cùng chuyện nhưng là 2 cảnh khác nhau. · Thumb↔tiêu đề: L · Thumb↔hook: P
- Vấn đề: mất vế 'thay vì sổ tiết kiệm' và không có tự giới thiệu/lời hứa trong 90s.
- **Sửa:** Thêm lại vế tương phản 'đẩy cuốn vở THAY VÌ sổ tiết kiệm'. Tự giới thiệu + lời hứa 'câu trả lời của bà 81 tuổi' trước giây 40.
- Video mẫu: DXXwIxhcfF0

#### Tập 12 — 夫が一年近く書いた終活ノートを目の前で破いた…始まりは古稀祝いの一言
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-12-FBkmqYvEyXQ` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 67 · giới thiệu — · hứa — (voice_paced.srt)
- Thumbnail: chưa có thumbnail — 
- Tiêu đề↔hook: K — Xé cuốn sổ ở giây 0–8, đúng câu đầu của tiêu đề. · Thumb↔tiêu đề:  · Thumb↔hook: 
- Vấn đề: mở đúng (xé sổ 0s) nhưng câu giải thích 'ông sẽ chết' ở giây 67–80 (KO 20s).
- **Sửa:** Mở đúng (xé sổ ở giây 0). Kéo câu 'cuốn này xong là ông chết, bố tôi y như vậy' từ giây 67 lên giây 20.
- Video mẫu: FBkmqYvEyXQ

#### Tập 13 — 通帳に1700万あるのに、修理代22万が惜しくて三晩震えた72歳
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-13-djMUfpGoUQI` · chưa có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 2 · giới thiệu 57 · hứa 79 (voice_paced.srt)
- Thumbnail: chưa có thumbnail — 
- Tiêu đề↔hook: K — 1700万, 22万, 3 đêm ở giây 0–12, đúng nguyên tiêu đề. · Thumb↔tiêu đề:  · Thumb↔hook: 
- Vấn đề: giữ tốt nhất nhóm (1700万 + 3 đêm ở giây 0–7), chỉ chậm phần hứa (79s).
- **Sửa:** Tốt nhất nhóm. Chỉ bỏ đoạn cây hồng/tả cảnh, đưa tự giới thiệu + lời hứa 'công thức người thắng tuổi già' lên trước giây 40.
- Video mẫu: djMUfpGoUQI

#### Tập 19 — 山歩きの女に850万円を送金…契約の朝、76歳の兄に残ったのはバナナ箱二つ
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-19-l0p1EnDcXYM` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 0 · giới thiệu 68 · hứa — (voice_paced.srt)
- Thumbnail: thumb_final.png — 六十過ぎたら｜近づくな｜四人の女｜その正体は｜美容室ばあさんが暴く衝撃の代償
- Tiêu đề↔hook: P — Hook là kẻ lừa nói chuyện trong gương. '850 vạn' và 'người anh 76 tuổi' không có trong 90 giây đầu. Mô tả trích một câu khác với câu trong hook. · Thumb↔tiêu đề: L · Thumb↔hook: P
- Vấn đề: đổi câu thành 'ai rộng hầu bao nhất' (mất vế lật 'không phải ông cô đơn'), tự giới thiệu 68s, chưa hứa 4 loại trong 90s.
- **Sửa:** Giữ câu gốc 'ông già nào dễ nhất?' + câu lật 'ông cô đơn à? không, ông cô đơn lâu lắm' (bản JP đổi thành 'ai rộng hầu bao nhất' mất cú lật).
- Video mẫu: l0p1EnDcXYM

#### Tập 21 — 老後資金に自ら鍵をかけた元郵便屋の理由…配達先の畳の下の800万円と孤独死
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-21-HD-ADEBz5oM` · có final.mp4 · ưu tiên vừa ()
- Mốc: chốt 0 · giới thiệu 27 · hứa 51 (voice_paced.srt)
- Thumbnail: thumb_final.png — 七十三歳｜銀行で聞いた｜奇妙な一言｜その真意とは｜老後のお金・四つの置き場所
- Tiêu đề↔hook: K — 'Tự khoá tiền của mình' đúng câu mở ở giây 0 (người nói là người ngồi quầy bên). · Thumb↔tiêu đề: P · Thumb↔hook: K
- Vấn đề: sát nhất nhóm, chỉ thiếu 'chỗ thứ 4'.
- **Sửa:** Sát nhất nhóm. Thêm 'bốn chỗ để tiền' + 'chỗ thứ tư đến giờ vẫn nghẹn' vào ngay sau câu giới thiệu.
- Video mẫu: HD-ADEBz5oM

### Lưu ý dữ liệu
- Tập 21: kênh gốc không có mốc giây (YouTube chặn), số liệu ~ là ước tính từ competitor.txt.

---

## 今夜も都市伝説 → lane `toshi-densetsu-jp`

Kênh: https://www.youtube.com/@konyamotosidensetu

Kênh dùng MỘT khung hook cho cả 9/9 video (và hook_chars của 28 video cũ trong transcripts.json đều 606–1126 chữ, trừ 1 video 1917): 0–4s đọc tít (chữ vàng thumbnail hoặc nửa đầu tiêu đề) → 0–20s năm + người thường + điều bất khả (hoặc giả định 『もしあなたが』) → 40–60s một lời trích/khẳng định chấn động = chữ đỏ thumbnail → 55–85s chuỗi 2–3 câu なぜ → 85–115s lời mời 『それでは…最初から辿っていこう』 (+ CTA đăng ký/hype ở 6 video từ 2026-08-26) → 第1章. Gói đăng: tiêu đề 'niềm tin mở rộng' (chính thể/真相/秘密/真実 + người cụ thể), thumbnail 2 băng chữ toàn khung (vàng trên, đỏ dưới viền đen, thường 「」 hoặc ●●), mô tả = 【都市伝説 ミステリー 怖い話】 + chép lại tiêu đề. 4 thứ nói cùng một câu: câu 0s của hook = chữ vàng; câu 45s của hook = chữ đỏ; tiêu đề = cả hai nối bằng …; mô tả dòng 1 = tiêu đề.

### Khung hook theo giây
- **0–4s · Đọc tít (title-card)** — Câu ≤20 chữ, nguyên văn chữ vàng thumbnail hoặc nửa đầu tiêu đề. 8/9 (OU1r đọc tên chương 1). Ví dụ: 「UFOは宇宙人じゃない。」 (GTwoNSPbEv8)
- **0–20s · Năm + người thường + điều bất khả / hoặc giả định ngôi 2** — 6/9 có năm + nơi + nghề trong 20s đầu (OU1r 13.3s, GTwo 0.4–4.3s, HqaY 3.4s, gWF 3.4s, UO4 17.2s, huF9 18s). 4/9 dùng 『もし(も)あなたが…としたら』 (saIym, zgi, UO4, huF9). Ví dụ: 「1987年6月26日、オーストラリアの…ごく平凡な58歳の牧場主が眠りから目を覚ました。」 (OU1r2W68F0Y)
- **10–60s · Chuỗi chi tiết cảm giác / tăng cấp** — 3–5 câu ngắn dựng hình (翼はない。プロペラもない。/ 見覚えのない天井、聞いたこともない言葉、鏡に映った自分ではない誰かの顔) — không có câu bình luận trừu tượng. Ví dụ: 「翼はない。プロペラもない。ジェットエンジンの炎も見えない。」 (GTwoNSPbEv8)
- **40–60s · Lời trích / khẳng định = chữ đỏ thumbnail** — Chữ đỏ thumbnail được đọc (hoặc đáp án ●● được trỏ tới) trong hook ở 5/9 (HqaY, UO4, GTwo, 8miF, saIym); một phần 3/9; lệch 1/9 (huF9). Ví dụ: 「彼は地球の人間ではなかった。」 (HqaY3BLROJU)
- **55–100s · Chuỗi câu hỏi なぜ** — ≥2 câu hỏi 'vì sao/là gì' trong hook: 8/9 (zgi chỉ 1). Thường nối bằng そして. Ví dụ: 「なぜ遠く離れたアメリカで生涯を終えた予言者が最後の最後に東の果てにあるこの島国を指したのでしょうか?」 (HqaY3BLROJU)
- **85–115s · Lời mời + (CTA) → 第1章** — Lời mời 9/9; nguyên câu 『それでは…を最初から辿っていこう』 4/9; CTA 『本編が始まる前に…ハイプで応援してくださいね』 (118 chữ) 6/9 — chỉ các video từ 2026-08-26 trở đi (OU1r 08-14, GTwo 08-21, gWF không có). 第1章 ở 99.6–~167s, trung vị ~115s. Ví dụ: 「それでは100年もの沈黙を破って明かされるある教師が見た未来の記憶を最初から辿っていこう。」 (gWF_9MYtji8)

- Tiêu đề: Công thức: [(tuỳ) 【都市伝説】/【ピラミッドの正体】] + {người cụ thể 〜した男 / 予言者ケイシー / テスラ} hoặc {lời trích 「…」} + {bí ẩn: 正体/真相/秘密/真実/本当の目的/答え/なぜ…のか} + 【都市伝説 ミステリー 怖い話】. Đếm: 9/9 khung 'niềm tin mở rộng' (0/9 tiêu đề giải thiêng); 8/9 có danh từ 'đáp án bị giấu' (正体 4, 真相 1, 秘密 1, 真実 2, 答え 1 — UO4 dùng なぜ…のか); 5/9 xoay quanh 1 người 『〜した男/技術者』; 4/9 có 「」 lời trích; 3/9 nêu đích danh nhân vật lịch sử (ケイシー 2, ディーナッハ 1). Độ dài cả khối 43–95 ký tự; thân không tính 【】 26–76 (top: 26, 32, 46, 55, 34, 72). Không có mẫu 'ngắn thắng dài' trong kênh này: video #1 dài 90 ký tự.
- Thumbnail: Bố cục cố định 9/9: 2 băng chữ trải NGANG toàn khung — trên: vàng viền đen, font có chân (Mincho) — dưới: đỏ viền đen, font nét cọ sần, to nhất; chủ thể AI điện ảnh ở giữa; nền xanh navy/đêm 8/9 (OU1r tím-hồng). Chữ đỏ trong 「」 6/9; ●● che đáp án 4/9 (đều thuộc 6 top: OU1r, GTwo, gWF, 8miF); dòng trắng nhỏ dẫn vào chữ đỏ 5/9 (人類の脅威は、/100年前に答えは出ていた/キリストの正体は…/エドガー・ケイシーが語った/火星の恐ろしい真相); mũi tên đỏ 5/9; có hình người (AI, không phải ảnh thật) 7/9. Chữ vàng thường là 『chủ thể + した男』 (5/9) hoặc 『X が暴露した / X が正しかった / 本当の理由』.
- Mô tả: 9/9: dòng 1 = 【都市伝説 ミステリー 怖い話】 + chép nguyên thân tiêu đề (huF9 vẫn chép tiêu đề CŨ sau khi đổi tên). Sau đó: チャンネル登録よろしくお願いします！ → (3 video mới nhất) link メンバー → 🌕あなたにおすすめの動画🌕 + 1–3 tiêu đề/link video cũ → 音声：VOICEVOX青山龍星 → 16 hashtag cố định. 0/9 có mốc chương (timestamps), 0/9 có đoạn tóm tắt nội dung. Mô tả KHÔNG phải đòn bẩy của kênh — chỉ lặp tiêu đề + đẩy người xem sang video khác.
- 4 phần nối nhau: Một lời hứa đi qua 4 chỗ: chữ VÀNG thumbnail = câu 0s của hook (8/9 trùng tít hoặc thumbnail); chữ ĐỎ thumbnail = câu 45–55s của hook hoặc đáp án ●● mà hook trỏ tới (5/9 khớp); TIÊU ĐỀ = ghép hai ý đó bằng … hoặc ｜; MÔ TẢ dòng 1 = tiêu đề. Ví dụ trọn vẹn nhất: HqaY3BLROJU — tiêu đề 『予言者ケイシーが死の直前に残した一言』 → hook 0.3s 『予言者が死の直前に残した一言。』 → hook 48–51s 『彼は地球の人間ではなかった』 → thumbnail đỏ 「彼は地球の人間ではない」 → mô tả dòng 1 = tiêu đề.
- Số đếm: {'title_card_0_4s': '8/9', 'year_person_in_20s': '6/9', 'moshi_anata': '4/9', 'thumb_red_in_hook': 'K 5/9 · P 3/9 · L 1/9', 'naze_questions_ge2': '8/9', 'invite_before_ch1': '9/9', 'cta_before_ch1': '6/9 (từ 2026-08-26)', 'ch1_time_s': '99.6–~167, trung vị ~115', 'hook_chars_to_ch1': '575–1126 (gồm CTA 118 chữ nếu có); phần kể không CTA ~501–1126', 'japan_teased_in_title_or_hook': '3/9 (OU1r 95s, saIym 0.3s + tiêu đề, HqaY 57–68s + tiêu đề) + zgi (tiêu đề 日本沈没, hook 74s)', 'japan_chapter4_exact': '2/6 video có transcript đủ (OU1r, HqaY)', 'debunk_titles': '0/9', 'desc_timestamps': '0/9', 'thumb_two_band_fullwidth': '9/9', 'thumb_masked_ceremony': '●● 4/9 · 「」 6/9'}
- Ngoại lệ: OU1r2W68F0Y (#1, 172k) mở bằng tên chương 1 thay vì tít, câu trích tiêu đề không có trong 90s, không có CTA — thắng nhờ đề tài (người được mời lên hành tinh khác + 2 Chúa Kitô + làng Nhật). GTwoNSPbEv8 (#2, 150k) hook dài nhất (1126 chữ, 第1章 ~167s) và 0 lần nhắc Nhật Bản trong cả câu chuyện. gWF_9MYtji8 (#5, 93k) không CTA, 0 lần nhắc Nhật trong câu chuyện 1, số trong tiêu đề (3906年/100年) lệch lời đọc (2000年後/90年). huF9eadlDeQ đổi tiêu đề sau khi đăng; thumbnail và mô tả vẫn theo tiêu đề cũ. Video dài 51–76 phút là GHÉP 2 câu chuyện: 5/6 video top có câu chuyện thứ 2 (bài cũ) nối sau câu chuyện chính (đếm 第1章 lặp lại trong transcripts.json); riêng GTwo là 1 câu chuyện 51 phút.

Thắng vs thua: So được top (6 video, 69k–172k, đăng 2026-08-14 → 09-05, 18–40 ngày tuổi) với 3 video 'new' (4.769–13.739 view) — nhưng 3 video new mới đăng 2026-09-20/21/22, tức 1–3 ngày tuổi lúc tải, nên chênh view chủ yếu là TUỔI VIDEO, không phải công thức. Hook: điểm top 10–11/12 (trung bình 10,5), new 8–11 (UO4 11 ngang top). Khung hook của new còn ĐẦY ĐỦ hơn top (3/3 có 『もしあなたが』, 3/3 có dấu 'không phải chuyện bịa', 3/3 có CTA), nên hook không phải chỗ khác biệt. Chỗ khác thật ở GÓI ĐĂNG: 2/3 video new có gói lệch — zgi tiêu đề 95 ký tự nhồi 2 đề tài (的中率85% + アカシックレコード + ポールシフト), câu 0s theo thumbnail chứ không theo tiêu đề, 85% không bao giờ được đọc; huF9 bị đổi tiêu đề sau khi đăng, thumbnail và mô tả vẫn theo bản cũ, chữ đỏ thumbnail không có trong hook. Top 6/6 có câu 0s trùng tiêu đề hoặc thumbnail và mô tả đồng bộ. Về đề tài: Cayce xuất hiện cả ở top (HqaY 112k — khung 'lời cuối về Chúa Kitô + Nhật') lẫn new (zgi — khung 'năng lực + dự đoán 85%'); video top xoay quanh 'danh tính thật của loài người/Chúa/Mặt Trăng do một người được chọn nghe trực tiếp'. Bằng chứng hook không quyết định view trong kênh này: 28 video cũ trong transcripts.json đều cùng khung, hook 606–1126 chữ; P_gCT2xX1Fk 648 chữ → 2.000 view, 4xsecoMLW7c 611 → 4.300, trong khi gWF 606 → 93k. View do đề tài + gói đăng.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 172,056 | 3.7 | 106.3 | 13.3 | 57.2 | H24 K13 | 10 | P | K | P | 【都市伝説】「人類には核兵器より恐ろしいものがある」440光年先の惑星ティアウーバへ招待された男が宇宙人へ質問…人類の正体、イエスキリストの正体とは？【都市伝説 ミステリー】 |
| top | 150,701 | 0.4 | 41.1 | 52.8 | 109.0 | H26 H24 K06 K13 | 11 | K | K | K | 【都市伝説】UFOは宇宙人じゃない。答えは100年前に出ていた…【ミステリー 怖い話】 |
| top | 120,668 | 0.3 | 70.4 | — | 100.1 | H24 H25 K15 K13 | 11 | K | P | K | 日本だけが知っていた？「月の秘密」がついにバレ始めている【都市伝説   ミステリー 怖い話】 |
| top | 112,543 | 48.0 | 61.3 | 3.4 | 91.9 | H24 K14 K13 | 11 | K | K | K | 日本に隠されたキリスト宇宙人説の真相。予言者ケイシーが死の直前に残した一言の意味を読み解く【都市伝説 ミステリー 怖い話】 |
| top | 93,670 | 41.9 | 77.3 | 3.4 | 86.0 | H24 K02 K13 | 10 | K | K | P | 3906年の未来にタイムスリップした男…100年封印された「ディーナッハの記録」に描かれた人類の正体とは？【都市伝説 ミステリー 怖い話】 |
| top | 69,157 | 29.2 | 45.0 | — | 73.5 | H24 K14 K13 | 10 | K | K | K | 【都市伝説】【ピラミッドの正体】遂に判明！？絶対に暴いてはいけない、ピラミッドの本当の目的とは？【エジプト ミステリー 怖い話】 |
| new | 4,769 | 0.4 | 74.2 | 13.3 | 90.2 | H24 H25 K15 K13 | 8 | P | P | K | 【的中率85%】日本沈没を予言した男エドガー・ケイシーの正体…眠ったまま病を見抜く力の真実｜ヤバすぎる…日本沈没、アトランティス、ポールシフトの真実とは？【都市伝説 ミステリー 怖い話】 |
| new | 11,432 | 47.8 | 54.2 | 17.2 | 90.6 | H24 H25 K14 K15 K13 | 11 | K | K | K | UFOに乗った技術者の告白｜宇宙人はなぜ「技術だけ進んだ文明は滅びる」と告げたのか？【都市伝説 ミステリー 怖い話 】 |
| new | 13,739 | 43.6 | 61.0 | 18.0 | 84.0 | H24 H25 K15 K13 | 8 | P | P | L | CIAが隠した超能力実験の記録…死から生還した男が見た火星ピラミッドの中身とは？スターゲート計画とは？CIA公式記録に残る火星リモートビューイングの真実【都市伝説 ミステリー 怖い話】 |

#### 【都市伝説】「人類には核兵器より恐ろしいものがある」440光年先の惑星ティアウーバへ招待された男が宇宙人へ質問…人類の正体、イエスキリストの正体とは？【都市伝説 ミステリー】 — https://www.youtube.com/watch?v=OU1r2W68F0Y
- Câu chốt (3.7s): 「地球には別の呼び名がある悲しみの星。そう呼んだのは地球の外側にいる知的存在だった。」
- Câu khoá (106.3s): 「なぜ地球は悲しみの星と呼ばれたのか。そして私たちが本当に向き合うべき脅威とは何なのか。最後まで見ればあなたはきっとこう思うはずだ。」
- Chữ thumbnail: 上段(vàng): 宇宙人と対話した男 ｜ dòng trắng nhỏ: 人類の脅威は、 ｜ dưới(đỏ): 核兵器ではなく●●だった · Mô tả: 【都市伝説 ミステリー 怖い話】「人類には核兵器より恐ろしいものがある」440光年先の惑星ティアウーバへ招待された男が宇宙人へ質問…人類の正体、イエスキリストの正体とは？
- Hook↔tiêu đề: P — Hook có người đàn ông được mời lên sao (44–54s) và 2 Chúa Kitô (89.8s) nhưng câu trích tiêu đề 「人類には核兵器より恐ろしいものがある」 không được nói trong 90s; chỉ tới 106–112s mới hỏi 『本当に向き合うべき脅威とは何なのか』. · Thumb↔tiêu đề: K — Thumb chép lõi tiêu đề: 『宇宙人と対話した男』 = 招待された男が宇宙人へ質問; 『核兵器ではなく●●』 = 核兵器より恐ろしいもの, che đáp án bằng ●●. · Thumb↔hook: P — 『対話した男』 khớp 47–54s (sinh vật 3m nói chuyện); 『人類の脅威』 chỉ chạm ở 64s (核戦争で滅び) và 106s (脅威とは何なのか) — ngoài mốc 90s một chút.
- Vì sao giữ người: Mở bằng một cái nhãn bí ẩn (Trái Đất = 『悲しみの星』) do kẻ ngoài Trái Đất đặt, rồi thả vào trải nghiệm cơ thể rất cụ thể (1987, 58 tuổi, giọng nói trong đầu, chân mất cảm giác mặt đất). Sau đó liệt kê 4 thứ 『sẽ được thấy』 như mục lục bí mật, câu hỏi khoá ở 106s trùng đúng lời hứa thumbnail (mối đe doạ lớn hơn vũ khí hạt nhân).
- Điểm yếu: Câu trích làm nên tiêu đề không có trong 90s đầu; không có CTA trước 第1章 (video tháng 8, trước khi kênh thêm CTA). Là video ghép 2 câu chuyện (câu chuyện Tiauba 0–~2205s, sau đó là bài Cayce 2026 cũ) nên 66 phút ≠ độ dài 1 câu chuyện.

#### 【都市伝説】UFOは宇宙人じゃない。答えは100年前に出ていた…【ミステリー 怖い話】 — https://www.youtube.com/watch?v=GTwoNSPbEv8
- Câu chốt (0.4s): 「UFOは宇宙人じゃない。」
- Câu khoá (41.1s): 「多くの人はここで宇宙人を思い浮かべるはずです。しかし今回その答えを探していくうちに私たちは宇宙ではなく100年以上前の地球へたどり着くことになります。」
- Chữ thumbnail: 上段(vàng): テスラが正しかった ｜ trắng nhỏ: 100年前に答えは出ていた ｜ dưới(đỏ): 「UFOの正体は●●だ」 · Mô tả: 【都市伝説 ミステリー 怖い話】UFOは宇宙人じゃない。答えは100年前に出ていた…
- Hook↔tiêu đề: K — Câu đầu tiên 0.4s là nguyên văn nửa đầu tiêu đề; 『答えは100年前に出ていた』 được nói ở 46.8–50s (宇宙ではなく100年以上前の地球へ). · Thumb↔tiêu đề: K — Thumb dòng trắng 『100年前に答えは出ていた』 = nguyên văn tiêu đề; 『UFOの正体は●●だ』 là cách viết lại 『UFOは宇宙人じゃない』 kiểu che đáp án. · Thumb↔hook: K — テスラ xuất hiện 55.5s, 『正体』 được trỏ tới ở 41–50s; ●● (= máy bay do con người chế tạo) không lộ trong hook.
- Vì sao giữ người: Phủ định niềm tin phổ biến ngay giây 0, nhưng phủ định để dẫn tới bí ẩn LỚN HƠN (công nghệ bị giấu của Tesla), không phải để giải thiêng. 3 câu 『không có cánh / không cánh quạt / không lửa phản lực』 dựng hình tức thì, và câu hỏi 『vậy đó là gì?』 được trả lời bằng một hướng bất ngờ (100 năm trước trên Trái Đất).
- Điểm yếu: Cảm xúc chỉ là tò mò, không sợ; 第1章 muộn (~167s theo transcript ước tính) — hook dài 1126 chữ, dài nhất trong 9 video mà vẫn 150k, nên độ dài không phải là thứ quyết định.

#### 日本だけが知っていた？「月の秘密」がついにバレ始めている【都市伝説   ミステリー 怖い話】 — https://www.youtube.com/watch?v=saIym-x8dPc
- Câu chốt (0.3s): 「もしも今夜あなたが何気なく見上げる月の裏側に日本人なら誰もが知っているあの形が静かに立っていたとしたら」
- Câu khoá (70.4s): 「なぜこれほど遠く離れた時代と場所で語られてきた物語がまるで示し合わせたかのように同じ一点を指し示しているのでしょうか?人類が半世紀近くも月から遠ざかっていたその本当の理由とは何だったのでしょうか?」
- Chữ thumbnail: 上段(vàng): NASAが月を見捨てた本当の理由 ｜ mũi tên đỏ chỉ cổng torii ｜ dưới(đỏ): 「月の裏側に鳥居がある」 · Mô tả: 【都市伝説 ミステリー 怖い話】日本だけが知っていた？「月の秘密」がついにバレ始めている
- Hook↔tiêu đề: K — 0.3s nói nguyên văn 『日本だけが知っていた月の秘密』; 『バレ始めている』 = 87–93s 『AIという新しい目が…静かに暴き始めています』. · Thumb↔tiêu đề: P — Tiêu đề nói 『月の秘密』 chung chung; thumb nói cụ thể 2 thứ tiêu đề không có (NASA bỏ Mặt Trăng, torii trên mặt sau Mặt Trăng) — bổ sung chứ không lặp. · Thumb↔hook: K — Torii được tả không gọi tên ở 3.8–31s (日本人なら誰もが知っているあの形…神聖な場所の入り口); 『本当の理由』 = 78–84s (人類が半世紀近くも月から遠ざかっていたその本当の理由).
- Vì sao giữ người: Kết hợp 3 đòn: giả định ngôi 2 gắn với hành động đời thường (tối nay ngẩng nhìn trăng), hình ảnh Nhật ai cũng biết (torii) mà hook CỐ Ý không gọi tên để thumbnail gọi tên, và niềm tự hào ngầm 『chỉ Nhật biết』. Đóng dấu 『公式に認めた紛れもない事実の話です』 ở 13.7–17.4s làm người xem hoài nghi cũng ở lại.
- Điểm yếu: Câu 『世界中の宇宙機関が公式に認めた』 phóng đại (có thể bị bắt lỗi); CTA 106–120s ăn 14s trước 第1章. Thumb 『NASAが月を見捨てた』 mạnh hơn hook 『月から遠ざかっていた』.

#### 日本に隠されたキリスト宇宙人説の真相。予言者ケイシーが死の直前に残した一言の意味を読み解く【都市伝説 ミステリー 怖い話】 — https://www.youtube.com/watch?v=HqaY3BLROJU
- Câu chốt (48.0s): 「彼は地球の人間ではなかった。」
- Câu khoá (61.3s): 「なぜ遠く離れたアメリカで生涯を終えた予言者が最後の最後に東の果てにあるこの島国を指したのでしょうか?そしてなぜこの国には遠い昔から天から降りてきた存在を静かに迎え入れ祈りを捧げ続けてきた文化が途切れることなく残り続けているのでしょうか?」
- Chữ thumbnail: 上段(vàng): エドガーケイシーが暴露した ｜ trắng nhỏ: キリストの正体は… ｜ dưới(đỏ): 「彼は地球の人間ではない」 · Mô tả: 【都市伝説 ミステリー 怖い話】日本に隠されたキリスト宇宙人説の真相。予言者ケイシーが死の直前に残した一言の意味を読み解く
- Hook↔tiêu đề: K — 0.3s nói nguyên văn 『予言者が死の直前に残した一言』; 『日本に隠された』 = 57.5–68s 東の島 / 島国; 『キリスト』 = người sống 2000 năm trước (30–35s). · Thumb↔tiêu đề: K — Thumb nêu tên ケイシー + キリストの正体 = đúng 2 danh từ của tiêu đề; chữ đỏ là chính 『一言』 mà tiêu đề hứa. · Thumb↔hook: K — Chữ đỏ 「彼は地球の人間ではない」 được đọc ở 48–51.4s, gần như nguyên văn (ではなかった).
- Vì sao giữ người: Cấu trúc 『câu nói cuối đời』: hé 30% (có một câu), rồi 50s sau mới đọc câu đó — đúng câu in đỏ trên thumbnail, nên người bấm vì thumbnail được 『trả thưởng』 trước 1 phút. Ngay sau đó chuyển bí ẩn sang Nhật (東の島) để người xem Nhật thấy chuyện là của mình.
- Điểm yếu: Không nói tên Cayce trong 90s (chỉ 『1人の男』), trong khi tiêu đề + thumbnail đều nêu tên; khó dựng hình (lời nói, giấc ngủ). Video ghép: câu chuyện 1 ~1829s, sau là bài 『月に行かなくなった理由』 cũ.

#### 3906年の未来にタイムスリップした男…100年封印された「ディーナッハの記録」に描かれた人類の正体とは？【都市伝説 ミステリー 怖い話】 — https://www.youtube.com/watch?v=gWF_9MYtji8
- Câu chốt (41.9s): 「彼が目覚めたのは2000年後の世界だったのです。」
- Câu khoá (77.3s): 「なぜこれほどまでに隠され続けなければならなかったのか。そしてこの記録に書かれた未来は本当に私たちの行末なのでしょうか?」
- Chữ thumbnail: 上段(vàng): 3906年の未来にタイムスリップした男 ｜ mũi tên đỏ chỉ chuỗi tiến hoá người ｜ dưới(đỏ): 「人類の正体は●●だった」 · Mô tả: 【都市伝説 ミステリー 怖い話】3906年の未来にタイムスリップした男…100年封印された「ディーナッハの記録」に描かれた人類の正体とは？
- Hook↔tiêu đề: K — 0.3s đọc nguyên văn nửa đầu tiêu đề; 『封印された』 = 65–77s. Nhưng tiêu đề nói 『100年封印』 còn hook nói 『90年もの長期に』 và 『2000年後の世界』 ≠ 3906年 — lệch số nhỏ. · Thumb↔tiêu đề: K — Chữ vàng = nguyên văn nửa đầu tiêu đề; chữ đỏ 『人類の正体は●●』 = 『人類の正体とは？』 cuối tiêu đề. · Thumb↔hook: P — Chữ vàng khớp 0.3s; 『人類の正体』 chỉ được chạm lỏng ở 48–62s (人類の脳ものが静かに変わり始める), chưa thành một câu khẳng định.
- Vì sao giữ người: Chuyện 『ngủ 1 năm tỉnh dậy trong cơ thể người khác ở tương lai』 tự nó là cảnh dựng hình được (trần lạ, gương lạ); hook đi theo trình tự cảm giác của nhân vật nên người xem trải nghiệm cùng. Không có CTA, 第1章 tới sớm nhất nhóm (99.6s).
- Điểm yếu: Số lệch giữa tiêu đề (3906年, 100年) và lời đọc (2000年後, 90年); cảm xúc chính là tò mò, không đánh vào nỗi sợ/tự hào của người Nhật (0 lần 『日本』 trong câu chuyện 1).

#### 【都市伝説】【ピラミッドの正体】遂に判明！？絶対に暴いてはいけない、ピラミッドの本当の目的とは？【エジプト ミステリー 怖い話】 — https://www.youtube.com/watch?v=8miFpRik5Lg
- Câu chốt (29.2s): 「王の墓であるはずなのになぜか肝心の遺体も宝物の痕跡も見つからないというあまりにも奇妙な内部構造」
- Câu khoá (45.0s): 「このピラミッドはそもそも墓などではなかったのではないか。」
- Chữ thumbnail: 上段(vàng): 遂に正体が判明 ｜ mũi tên đỏ chỉ đỉnh kim tự tháp ｜ dưới(đỏ): ピラミッドの正体は●●だった · Mô tả: 【都市伝説 ミステリー 怖い話】【ピラミッドの正体】遂に判明！？絶対に暴いてはいけない、ピラミッドの本当の目的とは？
- Hook↔tiêu đề: K — 0.3s đọc nguyên văn 『ピラミッドの本当の目的とは?』; 『遂に判明』 = 47–59s 『つい先日…発見が世界を駆け巡った』. · Thumb↔tiêu đề: K — 『遂に正体が判明』 + 『ピラミッドの正体は●●』 = 【ピラミッドの正体】遂に判明 trong tiêu đề. · Thumb↔hook: K — Đáp án ●● được trỏ tới ở 45s (墓などではなかった) mà không lộ.
- Vì sao giữ người: Mâu thuẫn 1 câu dễ nhớ: 『là mộ mà không có xác』. Đề tài quen nên hook dùng 『phát hiện mới tuần trước』 (つい先日) để biến chuyện cũ thành tin mới.
- Điểm yếu: Đề tài kim tự tháp đã bão hoà → độ bất thường thấp nhất nhóm top (1/2); view thấp nhất trong 6 top (69k) dù hook đủ khung.

#### 【的中率85%】日本沈没を予言した男エドガー・ケイシーの正体…眠ったまま病を見抜く力の真実｜ヤバすぎる…日本沈没、アトランティス、ポールシフトの真実とは？【都市伝説 ミステリー 怖い話】 — https://www.youtube.com/watch?v=zgiDcRLQteY
- Câu chốt (0.4s): 「もし誰にも打ち明けたことのない病の原因を会ったこともない誰かが遠く離れた場所からぴたりと言い当てたとしたら」
- Câu khoá (74.2s): 「そしていつか私たちの暮らすこの国日本の運命にまで触れる重い予言でした。彼は一体何を見ていたのでしょうか?」
- Chữ thumbnail: 上段(vàng): アカシックレコードにアクセスした男 ｜ trắng nhỏ: エドガー・ケイシーが語った ｜ dưới(đỏ): 日本沈没とポールシフトの真実 · Mô tả: 【都市伝説 ミステリー 怖い話】【的中率85%】日本沈没を予言した男エドガー・ケイシーの正体…眠ったまま病を見抜く力の真実｜ヤバすぎる…日本沈没、アトランティス、ポールシフトの真実とは？
- Hook↔tiêu đề: P — Tiêu đề mở bằng 【的中率85%】日本沈没を予言した男; hook không nói 85%, không nêu tên ケイシー, 『日本沈没』 chỉ được chạm gián tiếp ở 74–78s (この国日本の運命にまで触れる重い予言). · Thumb↔tiêu đề: P — Thumb nói Akashic Records + ポールシフト; tiêu đề nói 的中率85% + 眠ったまま病を見抜く — trùng 『日本沈没』, 『ケイシー』, phần còn lại khác. · Thumb↔hook: K — Chữ vàng đọc nguyên văn ở 0.4s; 『日本沈没』 ≈ 74–78s (ポールシフト không có trong 90s).
- Vì sao giữ người: Giả định ngôi 2 về chuyện riêng tư nhất (bệnh chưa kể ai) rồi đóng dấu 『không phải bịa』; danh sách năng lực tăng dần (chữa bệnh → tài nguyên → án mạng → tiền kiếp → tương lai Nhật).
- Điểm yếu: Mới đăng (2026-09-22, ~1 ngày khi tải) nên 4.769 view KHÔNG so được với top. Gói đăng lệch nhau: câu mở theo thumbnail, tiêu đề theo con số 85% không bao giờ được đọc. Chỉ 1 câu hỏi mở. Đề tài Cayce đã có HqaY (112k) → kênh lặp nhân vật.

#### UFOに乗った技術者の告白｜宇宙人はなぜ「技術だけ進んだ文明は滅びる」と告げたのか？【都市伝説 ミステリー 怖い話 】 — https://www.youtube.com/watch?v=UO4dRHRuBBE
- Câu chốt (47.8s): 「あなたたちの文明はかつてこの地球で1度崩れたのと同じ段階に再び入っている。」
- Câu khoá (54.2s): 「なぜ宇宙の彼方からやってきたその存在は地球の誰よりも進んだ科学を持ちながらその技術を決して私たちに渡そうとしなかったのでしょうか?なぜ選ばれたのはなだたる科学者たちではなく無名の1人の技術者だったのでしょうか?」
- Chữ thumbnail: 上段(vàng): UFOに乗った男の告白 ｜ dưới(đỏ): 「地球文明は滅びの段階だ」 · Mô tả: 【都市伝説 ミステリー 怖い話 】UFOに乗った技術者の告白｜宇宙人はなぜ「技術だけ進んだ文明は滅びる」と告げたのか？
- Hook↔tiêu đề: K — 0.5s 『UFOに乗った男の告白』 (tiêu đề ghi 技術者の告白); 『技術だけ進んだ文明は滅びる』 = 84–90s 『技術だけが先に進み…文明に何が起きるのか』; câu なぜ ở 54s khớp 『なぜ…告げたのか』. · Thumb↔tiêu đề: K — Chữ vàng ≈ nửa đầu tiêu đề; chữ đỏ 『地球文明は滅びの段階だ』 = cách nói khác của 『技術だけ進んだ文明は滅びる』. · Thumb↔hook: K — Chữ đỏ được đọc gần nguyên văn ở 47.8–54.2s.
- Vì sao giữ người: Khung 4 bước đầy đủ nhất trong 3 video mới: giả định ngôi 2 (sao tắt dần) → năm + người vô danh → lời cảnh báo = chữ đỏ thumbnail → 2 câu なぜ nghịch lý (vì sao không đưa công nghệ, vì sao chọn người vô danh).
- Điểm yếu: Mới đăng (2026-09-21, ~2 ngày) nên 11.432 view chưa so được. Nhân vật (Daniel Fry) không nêu tên; cảm xúc chính là tò mò.

#### CIAが隠した超能力実験の記録…死から生還した男が見た火星ピラミッドの中身とは？スターゲート計画とは？CIA公式記録に残る火星リモートビューイングの真実【都市伝説 ミステリー 怖い話】 — https://www.youtube.com/watch?v=huF9eadlDeQ
- Câu chốt (43.6s): 「しかしその場所は地球ではありませんでした。さらに異常なのはその時間です。現在ではなく100万年前。」
- Câu khoá (61.0s): 「なぜ国家はこんな研究に本気で取り組んだのでしょうか?なぜその記録は長い間封印されていたのでしょうか?そして何よりその男が見たものは本当にただの想像だったのでしょうか?」
- Chữ thumbnail: 上段(vàng): 火星をリモートビューイングした男 ｜ trắng nhỏ: 火星の恐ろしい真相 ｜ dưới(đỏ): 「火星に行ったら確実に死にます」 · Mô tả: 【都市伝説 ミステリー 怖い話】「火星移住＝死」リモートで火星内部を見た男が暴露した真実…火星ピラミッドの中にあるものとは…米国が隠す超能力研究の真実と遠隔透視で見た火星の恐ろしい真相
- Hook↔tiêu đề: P — Tiêu đề HIỆN TẠI (CIAが隠した超能力実験の記録…死から生還した男…火星ピラミッド) — CIA/実験 khớp 21.9–25.4s, nhưng 『火星』 không được nói trong 90s (chỉ 『地球ではありませんでした』), 『死から生還』 và 『ピラミッド』 không có. · Thumb↔tiêu đề: P — Thumb giữ góc tiêu đề cũ (火星移住＝死 / リモートで火星内部を見た男); tiêu đề mới chuyển sang CIA — 2 thứ chỉ chung 『火星』. · Thumb↔hook: L — Chữ đỏ 「火星に行ったら確実に死にます」 không có trong 90s đầu; chữ vàng chỉ khớp câu 0.4s.
- Vì sao giữ người: Câu hỏi trực tiếp về trải nghiệm ai cũng có (déjà vu) biến chuyện CIA xa lạ thành chuyện của người xem; đóng dấu 『公式記録』 ở 57s giữ người hoài nghi; 3 câu なぜ liên tiếp.
- Điểm yếu: Mới đăng (2026-09-20, ~3 ngày) — 13.739 view không so được. Tiêu đề đã bị ĐỔI (dòng 1 mô tả còn tiêu đề cũ 「火星移住＝死」…) → dấu hiệu kênh A/B tiêu đề khi video mới chậm; thumbnail vẫn theo tiêu đề cũ nên cả gói lệch.

### Các tập của mình

8 tập có script + voice (ep12 chưa viết). So với công thức kênh mẫu: (1) Câu title-card 0–4s: 2/8 (ep03 『地下の格納庫に、九機の円盤が並んでいた』, ep06 『獄中で死亡した』), thêm ep05 mở bằng 『5機』 ở 0.2s; 5/8 mở bằng biên niên trung tính 『〜年〜月、〜で…』 và điều bất thường đầu tiên tới ở 19–46s (kênh mẫu 8/9). (2) Lời hứa tiêu đề trả trong 90s: K 2/8 (ep02, ep03), P 5/8, L 1/8 (ep08); lời hứa trễ nặng nhất: ep06 並行世界 25:25, ep10 76秒 15:10, ep01 父 8:43, ep05 原因不明 7:31. (3) ≥2 câu なぜ trong hook: 2/8 (ep04, ep06) vs kênh mẫu 8/9; ep01, ep02, ep03, ep10 không có câu なぜ nào. (4) Thumbnail khung 2 băng toàn khung của kênh mẫu: 3/8 (ep08 mới, ep10, ep03 bản giao CHANEL); 5/8 còn mẫu cột trái cũ, trong đó 3 tập (ep02, ep05, ep06) dùng nền hành tinh chung không liên quan đề tài. Chữ đỏ thumbnail có trong 90s: K 5/8, P 1/8, L 1/8 (ep10). (5) Khung giải thiêng trong tiêu đề/thumbnail 4/8 (ep02 欺瞞, ep03 bản cũ 嘘, ep05 神話/原因不明じゃなかった, ep06 並行世界じゃない) — kênh mẫu 0/9. (6) Nhật được hé trong hook 3/8 (ep04, ep05 chỉ so diện tích, ep08 ở 103s); ep03 không có chương Nhật (vi phạm gate). (7) Mô tả: 6/8 TIEU_DE_MO_TA.txt khác S4_MO_TA.hook_line (chỉ ep03, ep10 khớp); ep08 mốc chương hỏng; ep10 mốc chương còn placeholder; DANG-TAI.txt 7/7 vẫn ghi 『CHƯA CÓ ảnh bìa』. Điểm tốt: 第1章 trung vị ~115s giống kênh mẫu (trừ ep08 173s), 8/8 có lời mời trước 第1章, neo dữ kiện dày. Thứ tự sửa: ep10 (chưa render) → ep08 → ep06 → ep05 → ep01/ep02 → ep04 → ep03.

#### Tập ep01-valentich — セスナ上空の光はUFOか金星か…父が語る息子の恐怖【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep01-valentich` · Đã có final.mp4 (29,8 phút) + đã giao E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep01-valentich (thumbnail giống hệt assets). · ưu tiên vừa (Đã giao; hook không rỗng (neo dày) và thumbnail khớp hook, nhưng 2/3 ý tiêu đề trễ >6 phút. Sửa bằng hook-repair đầu video + đổi thumbnail là đủ.)
- Mốc: chốt 39.5 · giới thiệu 12.3 · hứa 101.7 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep01-valentich\thumbnail_final.png (09-17; chỉ 1 file; DANG-TAI.txt mục 4 vẫn ghi 『CHƯA CÓ ảnh bìa』 — file cũ chưa cập nhật) — Ảnh thật: vàng 『20歳が / 消えた夜』 · đỏ 『「あれは航空機じゃない」』 — cột trái kiểu mẫu cũ, nền Cessna + ánh xanh lục (đúng đề tài). thumb_text.txt khớp ảnh.
- Tiêu đề↔hook: P — 『金星』 có ở 80.8s nhưng chữ 『UFO』 không được đọc trong 90s (lần đầu 390s) và 『父が語る息子の恐怖』 lần đầu ở 523s (8:43). · Thumb↔tiêu đề: P — Thumb (20歳/航空機じゃない) và tiêu đề (UFOか金星か/父) chia 2 góc, không chung danh từ nào; người chỉ đọc tiêu đề không biết đây là vụ mất tích. · Thumb↔hook: K — 『20歳』 13.4s, 「あれは航空機じゃない」 39.5s — cả 2 dòng thumbnail có trong 40s đầu.
- ⚠ Lời hứa không giữ: 『父が語る息子の恐怖』: có trong script (父親グイド, 恐怖心) nhưng lần đầu ở 523s — không có trong 90s.
- ⚠ Lời hứa không giữ: 『UFO』 trong tiêu đề: hook 0–114s không nói UFO lần nào; lần đầu 390s (tên chương 2).
- Vấn đề: 0–24s là lịch trình trung tính: 『登録記号はVH-DSJ』 (9.6s), 『目的地は…キング島です』 (16.3s) — điều bất thường đầu tiên ở 24.5s; kênh mẫu 8/9 có câu title-card ở 0–4s.
- Vấn đề: Câu mạnh nhất 「あれは航空機じゃない」 nằm ở 39.5s; 『6分後』 ở 52.8s.
- Vấn đề: Không có câu なぜ nào; khoá duy nhất là câu chọn 107–111s 『あなたはどちらの記録を信じることになるでしょうか』.
- Vấn đề: Chương Nhật (第4章 日航1628便事件 1986) không được hé trong hook — bỏ phí lợi thế kênh mẫu dùng ở OU1r/HqaY.
- Vấn đề: Thumbnail theo mẫu cột trái cũ, không phải 2 băng toàn khung như 9/9 thumbnail kênh mẫu.
- **Sửa:** 0–5s: đổi câu mở thành title-card lời cuối, theo HqaY3BLROJU (『予言者が死の直前に残した一言』): gợi ý 「〝あれは航空機じゃない〟——20歳のパイロットが残した最後の交信。」 rồi 19時06分→19時12分 (6分) trong 15s đầu. Bỏ 『登録記号はVH-DSJ』 khỏi hook (để ở 第1章).
- **Sửa:** 30–60s: đưa cặp 『UFOか、金星か』 thành câu nghịch lý (đêm đó 金星・火星・水星 sáng trên trời — hiện ở 78.5s) và hé 1 câu về người cha (dữ kiện 523s) để tiêu đề được trả trong 60s.
- **Sửa:** 60–100s: thêm 2 câu なぜ (vì sao không tìm thấy mảnh nào trong 4 ngày; vì sao 5 năm sau 1 tấm カウルフラップ dạt vào đảo Flinders) + hé 日航1628便 (1986, phi công Nhật cũng báo 'không phải máy bay') như OU1r hé làng Nhật ở 95s.
- **Sửa:** Thumbnail: chuyển sang bố cục 2 băng toàn khung: vàng 『6分後に消えた20歳』 · trắng nhỏ 『最後の交信』 · đỏ 「あれは航空機じゃない」 (giữ câu trích — đang khớp hook).
- **Sửa:** Mô tả: dòng 1 nên chép tiêu đề (9/9 kênh mẫu), và chốt 1 phiên bản (TIEU_DE_MO_TA hay S4_MO_TA) — hiện 2 bản khác nhau.
- Video mẫu: HqaY3BLROJU (lời cuối làm title-card, đọc lại ở 48s) + OU1r2W68F0Y (hé chương Nhật ở 95s)

#### Tập ep02-walton — ウォルトンが消えた5日間…迫る2,500ドルの罰金【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton` · Đã có final.mp4 (33,9 phút) + đã giao CHANEL (thumbnail giống assets). · ưu tiên vừa (Hook có neo tốt và tiêu đề được trả trong 90s; mất điểm vì chi tiết mạnh nhất (lời trăng trối) bị giấu ở 99s và thumbnail nền chung chung.)
- Mốc: chốt 19.4 · giới thiệu 13.2 · hứa 122.8 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\thumbnail_final.png (09-12; 1 file) — Ảnh thật: vàng 『全米震撼の / ＵＦＯ誘拐』 · đỏ 『検査結果は / 「重大な欺瞞」』 — cột trái mẫu cũ; nền là hành tinh/thiên thạch chung chung, KHÔNG liên quan rừng Arizona/UFO. thumb_text.txt khớp ảnh.
- Tiêu đề↔hook: K — Mất tích 19.4–23.4s, trở về 11月11日 39.1s (≈5 ngày, dù cụm 『5日間』 chỉ được đọc lần đầu ở 373s), 2,500ドルの罰金 77.7s — cả 2 ý tiêu đề có trong 90s. · Thumb↔tiêu đề: P — Thumb (UFO誘拐/重大な欺瞞) và tiêu đề (5日間/罰金) chia vai, không chung danh từ; ghép lại mới ra 'vụ bắt cóc UFO có động cơ tiền'. · Thumb↔hook: K — 『重大な欺瞞』 61.6s; 『UFO誘拐』 ≈ 51.1s (宇宙船に連れ去られ). 『全米震撼』: script chỉ có 全米で報道 (698s), chữ 震撼 không có.
- ⚠ Lời hứa không giữ: Không có lời hứa sai; 『全米震撼』 hơi mạnh hơn script (全米で報道).
- Vấn đề: Chi tiết mạnh nhất của cả tập — 『2026年2月…ロジャースが世を去ります。その死の床で家族に残された言葉』 — nằm ở 99.2–112.6s, không có trên tiêu đề lẫn thumbnail.
- Vấn đề: Không có câu なぜ; khoá 114–129s là câu giả định dài 『もし…根ざしていたとしたら、どうでしょうか』 + 『境界線を見極めることになるはずです』.
- Vấn đề: 第1章 ở 132s (kênh mẫu trung vị ~115s); hook 891 chữ.
- Vấn đề: Chương Nhật (第4章 神隠しと記憶の喪失) không được hé trong hook.
- Vấn đề: Nền thumbnail là ảnh hành tinh dùng chung (giống ep05, ep06, ep08 bản cũ) — không dựng được cảnh 'người bị bắt khỏi rừng'.
- **Sửa:** 0–5s: title-card theo HqaY3BLROJU: 「あの夜トラックを運転していた男が、死の床で残した言葉。」 rồi mới vào 1975年11月5日 — lời trăng trối 2026 là 'một câu cuối đời' y như công thức video 112k.
- **Sửa:** Giữ nguyên chuỗi 13–81s (đang tốt: người, giờ, 50 người tìm, ポリグラフ, 罰金).
- **Sửa:** 90–120s: thay câu giả định bằng 2 câu なぜ (vì sao báo cáo 『重大な欺瞞』 bị giấu; vì sao đội thợ rừng đang sắp bị phạt 2,500ドル lại gặp UFO đúng lúc đó) + hé 神隠し (chương 4) 1 câu.
- **Sửa:** Thumbnail: nền cảnh rừng đêm + cột sáng; vàng 『森から消えた22歳』 · trắng nhỏ 『死の床の告白』 · đỏ 「重大な欺瞞」 (giữ, đang khớp 61.6s).
- **Sửa:** Cân nhắc tiêu đề dùng lời trăng trối (dữ kiện 106s) thay 『迫る』 — ví dụ khung 『ウォルトン事件、運転手が死の床で残した一言…消えた5日間の真相』.
- Video mẫu: HqaY3BLROJU (lời cuối đời làm trục hook + thumbnail) · OU1r2W68F0Y (người thường bị đưa đi, tả cảm giác cơ thể)

#### Tập ep03-bob-lazar — 「地下に9機の円盤」エリア51の男を公文書で追うと…【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep03-bob-lazar` · Đã có final.mp4 (27,5 phút) + đã giao CHANEL. CÓ 2 THUMBNAIL KHÁC NHAU: bản giao CHANEL (09-20 13:06) ≠ assets\thumbnail_final.png (09-11). · ưu tiên thấp (Tập tốt nhất lane: câu chốt ở 0.2s, lời hứa tiêu đề trả trong 30s, thumbnail bản giao đúng khung kênh mẫu. Chỉ cần chốt file thumbnail.)
- Mốc: chốt 0.2 · giới thiệu 15.1 · hứa 97.1 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep03-bob-lazar\thumbnail.png (09-20, bản giao — MỚI hơn) · E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep03-bob-lazar\thumbnail_final.png (09-11, bản cũ) — Bản giao CHANEL (mới): vàng 『S-4地下格納庫』 · trắng nhỏ 『1989年の証言』 · đỏ 『「九機の円盤が並んでいた」』 — 2 băng toàn khung, đúng kiểu kênh mẫu. Bản assets (cũ): vàng 『宇宙船を / 告発した男』 · đỏ 『「物理学者」 / は嘘だった』 (cột trái). thumb_text.txt = bản CŨ.
- Tiêu đề↔hook: K — 『地下に9機の円盤』 = câu 0.2s; エリア51 30.1s; 公文書 97.1s. · Thumb↔tiêu đề: K — Bản giao: chữ đỏ 「九機の円盤が並んでいた」 = lời trích trong tiêu đề (lặp ý nhưng đúng công thức kênh mẫu: đỏ = câu trích). Bản cũ: 『物理学者は嘘』 = đáp án của 『公文書で追うと…』 → P. · Thumb↔hook: K — Bản giao: đỏ = câu 0.2s gần nguyên văn, 『1989年』 15.1s, S-4 33.9s. Bản cũ: 『物理学者』 43.8–65.8s nhưng chữ 『嘘』 không có trong script (script: 裏づける書類は一枚もない).
- ⚠ Lời hứa không giữ: Chỉ ở thumbnail bản CŨ: 『「物理学者」は嘘だった』 mạnh hơn script (script chỉ nói không có hồ sơ nào xác nhận). Bản giao CHANEL không có lỗi này.
- Vấn đề: Hai thumbnail khác nhau + thumb_text.txt cũ → dễ đăng nhầm bản cũ.
- Vấn đề: VI PHẠM gate require_japan_hook_chapter: 第4章 『極秘施設S-4と軍事機密の実態』 không có chữ Nhật nào (0 lần 日本/日本人 trong cả script) — SOP §10 đã định móc Nhật 相模原 nhưng script không làm.
- Vấn đề: Không có câu なぜ; khoá 101.5–107s 『私たちが目にすることになるのは、宇宙の謎ではないのかもしれません』 là hé kết quả (K06) — ổn nhưng thiếu câu hỏi.
- Vấn đề: Tên ボブ・ラザー không được đọc trong hook (lần đầu ở ký tự 964, sau 第1章) — người tìm theo tên không nghe thấy trong 2 phút đầu.
- **Sửa:** Chốt đăng bản thumbnail CHANEL (09-20) và cập nhật thumb_text.txt cho khớp — đây là tập duy nhất có thumbnail + hook + tiêu đề cùng nói một câu (H24 + K14).
- **Sửa:** 85–100s: thêm 1–2 câu なぜ trước lời mời, ví dụ ý 『vì sao lời khai của một người không có hồ sơ đại học nào vẫn sống 30 năm』 (dữ kiện 60–92s).
- **Sửa:** Nếu làm lại: bổ sung chương Nhật (相模原 theo SOP §10) hoặc ghi rõ ngoại lệ cho gate.
- Video mẫu: GTwoNSPbEv8 (câu 0s = tiêu đề; phủ định dẫn tới đáp án khác) · UO4dRHRuBBE (câu trích = chữ đỏ)

#### Tập ep04-fermi-paradox — 確認信号は0件…フェルミの問いが残した2つの結末【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep04-fermi-paradox` · Đã có final.mp4 (31,1 phút) + đã giao CHANEL. Script có 6 marker (第1章 xuất hiện 2 lần). · ưu tiên thấp (Tiêu đề và thumbnail khớp hook về ý; hook có Nhật; chỉ cần kéo câu trích lên 0s và đổi khung thumbnail.)
- Mốc: chốt 13.6 · giới thiệu 5.5 · hứa 96.6 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep04-fermi-paradox\thumbnail_final.png (09-16; 1 file) — Ảnh thật: vàng 『無数に存在 / するはずの』 · đỏ 『文明が「１つ / もない」謎』 — cột trái mẫu cũ; nền chảo radio + dải Ngân Hà (đúng đề tài). thumb_text.txt khớp.
- Tiêu đề↔hook: P — Ý 『0件』 có ở 57.1s dưới dạng 『痕跡は何ひとつ見つかっていません』 (chữ 『1件も検出』 lần đầu 1474s); 『2つの結末』 = 希望/警告 ở 100–106s (ngoài 90s một chút). · Thumb↔tiêu đề: K — Cùng một nghịch lý (vô số sao / 0 tín hiệu) nói bằng 2 cách, không lặp chữ. · Thumb↔hook: K — 『無数に存在するはず』 = 24.8–41.9s (2,000億〜7×10の22乗); 『1つもない』 = 57.1s.
- ⚠ Lời hứa không giữ: 『確認信号は0件』: không có nguyên cụm; tương đương 『痕跡は何ひとつ』 (57s) và 『1件も検出されて(いない)』 (1474s) — không sai nhưng từ 'tín hiệu' không được nói trong hook.
- Vấn đề: 0–12s là khung cảnh + tên người trước khi tới câu trích (13.6s) — câu 「で、みんなどこにいるんだ？」 mới là title-card đúng.
- Vấn đề: 24.8–54s là chuỗi số liệu (恒星数, 7×10の22乗, ドレイク方程式, 500万〜5,000万年) — neo dày nhưng không có hình người/cảnh.
- Vấn đề: Hook có Nhật (西はりま天文台 81–91s) — tốt, đúng kiểu HqaY hé Nhật trước 第1章.
- Vấn đề: Thumbnail mẫu cột trái cũ, không có chủ thể/hình người.
- **Sửa:** 0–5s: đưa câu trích lên đầu: 「〝で、みんなどこにいるんだ？〟——1950年、昼食の席の一言。」 (title-card = câu trích, theo HqaY3BLROJU).
- **Sửa:** Hoặc mở theo H25 như saIym-x8dPc: 『もし今夜あなたが見上げる星空の、どこにも誰もいないのだとしたら。』 rồi mới tới Fermi.
- **Sửa:** Rút chuỗi số 24–54s còn 2 câu; đưa 『確認された信号は、今も1件もない』 thành 1 câu ngắn trước 60s để tiêu đề được trả nguyên chữ.
- **Sửa:** Thumbnail 2 băng: vàng 『〝みんなどこにいるんだ？〟』 · trắng nhỏ 『1950年、フェルミの一言』 · đỏ 『確認信号は「0件」』.
- Video mẫu: saIym-x8dPc (giả định ngôi 2 với bầu trời đêm + hé Nhật) · HqaY3BLROJU (một câu nói làm trục)

#### Tập ep05-bermuda-triangle — バミューダ5機失踪、報告書は「原因不明」じゃなかった【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle` · Đã có final.mp4 (33,0 phút) + đã giao CHANEL. · ưu tiên cao (Lời hứa tiêu đề trễ 7,5 phút, 40s hook là câu trừu tượng, và cả gói dùng khung giải thiêng mà kênh mẫu không dùng — trong khi script có sẵn chi tiết người mẹ để sửa.)
- Mốc: chốt 0.2 · giới thiệu — · hứa 114.1 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\thumbnail_final.png (09-16; 1 file) — Ảnh thật: vàng 『魔の三角 / 海域の謎は』 · đỏ 『作られた「神 / 話」だった』 (ngắt dòng giữa chữ 神|話) — cột trái mẫu cũ; nền hành tinh chung (không có biển/máy bay). thumb_text.txt khớp.
- Tiêu đề↔hook: P — 『5機失踪』 = câu 0.2s; nhưng 『報告書は「原因不明」じゃなかった』 chỉ được nói mơ hồ ở 111.8s (公式な事故報告書を洗い直せば…実態は明白); chữ 原因不明 lần đầu 451s. · Thumb↔tiêu đề: P — Tiêu đề nói báo cáo Hải quân; thumbnail nói 'thần thoại do người dựng' — cùng hướng giải thiêng, khác đối tượng. · Thumb↔hook: K — 『魔の三角』 48.2s; 『神話が作られていった』 94.3–96.4s.
- ⚠ Lời hứa không giữ: Lõi tiêu đề (báo cáo gốc không ghi 『原因不明』 — Hải quân sửa chữ vì mẹ đại uý Taylor phản đối, dữ kiện có ở ký tự 2844 ≈ 451s) không có trong 90s đầu.
- Vấn đề: 23.6–60s là đoạn tả chung (vẽ tam giác trên bản đồ, 魔の三角地帯, アトランティス, 時空の裂け目) — không có người, không có năm cho tới 60.5s.
- Vấn đề: 74.9–96s là câu bình luận trừu tượng: 『なぜ巨大な幻影が定着し、人々の理性を麻痺させ続けたのか』, 『極めて現実的な過程が存在していました』.
- Vấn đề: Tiêu đề + thumbnail cùng khung GIẢI THIÊNG (thần thoại được dựng) — kênh mẫu 0/9 tiêu đề kiểu này; GTwoNSPbEv8 có phủ định nhưng dẫn tới bí ẩn lớn hơn.
- Vấn đề: Chi tiết người thật đắt nhất (mẹ của đại uý Taylor phản đối → Hải quân đổi thành 『原因不明』) bị giấu tới 7,5 phút.
- Vấn đề: Nền thumbnail là hành tinh chung, không phải biển/5 máy bay.
- **Sửa:** 0–10s: giữ 『5機・14名が消えた』 nhưng thêm ngay title-card báo cáo: 「海軍の報告書は、最初から〝原因不明〟ではありませんでした。」
- **Sửa:** 20–50s: kể 1 câu về mẹ đại uý Taylor và việc Hải quân đổi chữ (dữ kiện 451s) — đây là câu hé 30% đúng kiểu K14, có cảm xúc (người mẹ) mà hook hiện không có.
- **Sửa:** Cắt đoạn 23.6–60s (tam giác bản đồ) còn 1 câu; thay 74.9–96s bằng 2 câu なぜ cụ thể (vì sao một chữ trong báo cáo đổi mà thành huyền thoại 50 năm; vì sao Nhật cũng có 『魔の海』 — ドラゴン・トライアングル/明神礁 của chương 4).
- **Sửa:** Tiêu đề/thumbnail: chuyển từ 'thần thoại giả' sang 'bí mật trong báo cáo' — ví dụ đỏ 「原因不明」に書き換えた理由 · vàng 『消えた5機と14人』 · nền biển đêm + 5 máy bay.
- Video mẫu: GTwoNSPbEv8 (phủ định dẫn tới đáp án lớn hơn, sự kiện có năm trong 5s) · HqaY3BLROJU (hé 1 câu trong tài liệu)

#### Tập ep06-mandela-effect — マンデラ効果は並行世界じゃない…鍵は1974年の実験【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep06-mandela-effect` · Đã có final.mp4 (32,9 phút) + đã giao CHANEL. · ưu tiên cao (Lời hứa trung tâm của tiêu đề (並行世界) trễ 25 phút — đúng loại lời hứa không giữ dễ bị comment bắt lỗi; 55s hook là giảng giải.)
- Mốc: chốt 0.3 · giới thiệu — · hứa 74.9 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep06-mandela-effect\thumbnail_final.png (09-16; 1 file) — Ảnh thật: vàng 『獄中で死んだ / はずの男が』 · đỏ 『「大統領」に / なっていた』 — cột trái mẫu cũ; nền hành tinh chung. thumb_text.txt khớp.
- Tiêu đề↔hook: P — 『1974年の実験』 50.6s; nhưng 『並行世界』 — lời hứa chính của tiêu đề — không được nhắc trong hook; lần đầu ở 1525s (25:25). · Thumb↔tiêu đề: P — Thumb kể biến cố (chết trong tù → tổng thống), tiêu đề kể lời bác bỏ (không phải thế giới song song) — cùng chủ đề Mandela, khác vai. · Thumb↔hook: K — Chữ vàng + đỏ = đúng câu 0.3–16s.
- ⚠ Lời hứa không giữ: 『並行世界じゃない』: script có (9934 ký tự trở đi) nhưng hook không hề nêu giả thuyết thế giới song song để rồi bác bỏ; người bấm vì 'thế giới song song' phải đợi 25 phút.
- Vấn đề: Câu mở tốt (lời khẳng định sai ở 0.3s = thumbnail) nhưng 23.9–79s là giảng giải: 『認知心理学』, 『大脳生理学が解明した情報再構築プロセスのデータ』, 『構造的な真相を検証していきます』 — 0 hình ảnh.
- Vấn đề: Ví dụ gần người Nhật nhất (ピカチュウの尻尾, 82.6s) lại nằm cuối hook; kênh mẫu dùng thứ quen thuộc ở 0–20s (saIym: 月を見上げる).
- Vấn đề: Khung giải thiêng (『じゃない』 → trí nhớ sai): phủ định dẫn tới đáp án NHỎ hơn — ngược H26 (GTwo phủ định dẫn tới đáp án lớn hơn).
- Vấn đề: Chương Nhật (第4章 ピカチュウの尻尾) yếu: chỉ 2 lần nhắc Nhật.
- **Sửa:** 0–15s: giữ câu Mandela (đang khớp thumbnail) nhưng chèn ngay câu giả định ngôi 2 theo H25: 「あなたの覚えているピカチュウの尻尾の先は、黒かったでしょうか。」 (dữ kiện 82.6s) — Nhật + đời thường.
- **Sửa:** 15–40s: nêu giả thuyết song song mà tiêu đề sẽ bác: 『これを〝並行世界から紛れ込んだ記憶〟だと考える人がいます』, rồi 50s: 『鍵を握るのは1974年のある実験』.
- **Sửa:** Thay đoạn 23.9–79s bằng 2 câu なぜ cụ thể (vì sao hàng nghìn người lạ nhớ CÙNG một điều sai; vì sao 92% người được hỏi nhớ sai chiếc đồng hồ Bologna — dữ kiện 99.9–111.5s).
- **Sửa:** Tiêu đề: giữ bí ẩn thay vì đóng nó — hướng 『何千人が同じ〝嘘の記憶〟を持つ理由…鍵は1974年の実験』 (bỏ phủ định 並行世界じゃない khỏi tiêu đề hoặc đưa lên hook).
- Video mẫu: saIym-x8dPc (giả định ngôi 2 với thứ quen thuộc của người Nhật) · GTwoNSPbEv8 (phủ định để mở bí ẩn lớn hơn)

#### Tập ep08-fatima-akita — ファティマの56年後…秋田の聖母像が101回流した涙【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep08-fatima-akita` · Đã có final.mp4 (28,4 phút) + đã giao CHANEL (thumbnail giao = thumbnail_final.png mới 09-22). · ưu tiên cao (Tiêu đề lệch hook (cả 2 danh từ ngoài 90s), thumbnail lệch tiêu đề, 第1章 muộn nhất lane (173s), mô tả có mốc chương hỏng — 4 chỗ kéo 4 hướng.)
- Mốc: chốt 44.0 · giới thiệu 11.9 · hứa 168.1 (voice.srt (mốc thật))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep08-fatima-akita\thumbnail_final.png (09-22 17:59, bản B, = bản giao CHANEL) · bản cũ thumbnail_final.png.bak.20260922-151001 (09-21) — Bản đang dùng (B): vàng 『七万人が見上げた太陽』 · trắng nhỏ 『1917年の証言』 · đỏ 『「地上に向かって落下」』 — 2 băng toàn khung đúng kiểu kênh mẫu. Bản cũ (.bak): vàng 『バチカン / が認めた』 · đỏ 『「101回」 / 涙を流した』 (cột trái). thumb_text.txt = bản CŨ (バチカンが認めた/「101回」涙を流した) → lệch ảnh thật.
- Tiêu đề↔hook: L — 『56年後』 ở 102.7s và 『101回』 ở 133.1s — cả 2 danh từ của tiêu đề nằm ngoài 90s; 0–90s chỉ có Fátima. · Thumb↔tiêu đề: L — Thumbnail nói mặt trời Fátima (七万人, 落下), tiêu đề nói nước mắt tượng Akita (101回) — không chung chi tiết nào; thumbnail không có chữ Nhật/秋田 dù Nhật là tài sản mạnh nhất của tập. · Thumb↔hook: P — 『七万人』 38.1s, 『1917年』 0.2s khớp; nhưng chữ đỏ 『地上に向かって落下』 không có trong hook (309s).
- ⚠ Lời hứa không giữ: Thumbnail đỏ 「地上に向かって落下」: có trong script (309s) nhưng không có trong 90s.
- ⚠ Lời hứa không giữ: Tiêu đề 『101回流した涙』: có (133s) nhưng ngoài 90s.
- ⚠ Lời hứa không giữ: Bản thumbnail CŨ 『バチカンが認めた』 sẽ là lời hứa sai (script ghi 1984 chỉ là 新潟教区が公式に認めた, 『必ずしも「バチカンが世界に対して公式…」』) — may là đã thay; nhưng thumb_text.txt vẫn giữ chữ cũ, dễ bị dùng lại.
- Vấn đề: 0–44s là biên niên + đọc tên 3 đứa trẻ (11.9–16.1s) + số buổi hiện ra — điều bất thường đầu tiên 『説明のつかない現象』 ở 46.5s và vẫn không tả gì (không nói mặt trời xoay/rơi).
- Vấn đề: 54–102s là 3 lời tiên tri — nội dung chương 2 bị kéo lên hook.
- Vấn đề: 第1章 ở 172.8s (muộn nhất lane; kênh mẫu ~115s); hook 1090 chữ gần trần.
- Vấn đề: Chỉ 1 câu なぜ ở 162.9s.
- Vấn đề: Ba chỗ nói ba chuyện: tiêu đề = Akita 101 lần; thumbnail = mặt trời 1917; mô tả dòng 1 = cả hai; hook 90s = Fátima + tiên tri.
- **Sửa:** 0–5s: title-card theo tiêu đề: 「秋田の修道院で、木彫りの聖母像が101回涙を流した。」 rồi 1973年 + máu ở tay phải (dữ kiện 123.5s) trong 15s đầu — Nhật lên đầu như saIym-x8dPc (『日本だけが知っていた』 0.3s).
- **Sửa:** 15–45s: lùi 56 năm: 『その56年前、ポルトガル。7万人が見上げた太陽が「地上に向かって落下」するように見えた』 — trả chữ đỏ thumbnail trước 45s (K14).
- **Sửa:** Bỏ khỏi hook: tên 3 đứa trẻ (11.9–16.1s) và 3 lời tiên tri (54–102s) — để ở 第1章/第2章.
- **Sửa:** 70–100s: 2 câu なぜ (vì sao Giáo hội mất 11 năm; vì sao hai sự việc cách 56 năm và nửa vòng Trái Đất lại được đặt cạnh nhau) → lời mời → 第1章 trước ~115s.
- **Sửa:** Thumbnail: giữ khung B nhưng cho Nhật vào một dòng — ví dụ trắng nhỏ 『56年後、秋田で』 hoặc đổi đỏ sang 『「101回」涙を流した』 (nhưng bỏ 『バチカンが認めた』).
- **Sửa:** Sửa mốc chương trong mô tả (tên chương đang dính thân bài) và cập nhật thumb_text.txt.
- Video mẫu: saIym-x8dPc (đưa Nhật lên câu 0s) · OU1r2W68F0Y (hook liệt kê 'sẽ thấy gì' kèm làng Nhật)

#### Tập ep10-tesla-tictac — テスラの死から61年後、米海軍が撮った76秒の映像【都市伝説 ミステリー 怖い話】
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep10-tesla-tictac` · CHƯA có final.mp4 (có voice.srt 31,3 phút + thumbnail); CHANEL chỉ có thumbnail.png; TIEU_DE_MO_TA.txt còn placeholder 『Timestamps: [CHƯA CÓ — trích từ voice_paced.srt thật]』; không có DANG-TAI.txt. · ưu tiên cao (Chưa render nên sửa hook tốn ít nhất; hiện 0 câu なぜ, thumbnail lệch hook hoàn toàn (L), lời hứa 76秒 trễ 15 phút, hook dưới sàn gate.)
- Mốc: chốt 30.4 · giới thiệu 8.3 · hứa 87.6 (voice.srt (mốc thật; voice chưa qua dựng))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep10-tesla-tictac\thumbnail_final.png (09-22 16:02, bản B; = CHANEL\\ep10-tesla-tictac\\thumbnail.png) — Ảnh thật: vàng 『白い物体に接近した海軍中佐』 · trắng nhỏ 『数秒で60マイル先へ』 · đỏ 『「弾丸のようであった」』 — 2 băng toàn khung đúng kiểu kênh mẫu; nền trời xanh sáng ban ngày (kênh mẫu 8/9 tối). Không có thumb_text.txt.
- Tiêu đề↔hook: P — 『テスラの死』 0.2–8.3s, 『61年』 24.1s, 『米海軍』 30.4s khớp; nhưng 『76秒の映像』 không có trong hook — script viết 『七十六秒』 lần đầu ở 910s (15:10). · Thumb↔tiêu đề: P — Cùng sự kiện Hải quân 2004 nhưng thumbnail nói 中佐/60マイル/弾丸, tiêu đề nói テスラ/61年/76秒 — không chung chữ nào. · Thumb↔hook: L — Cả 3 dòng thumbnail nằm ở phút 12–14 (中佐 720s, 弾丸 829s, 60マイル 842s); hook chỉ có 『白く滑らかな楕円形の物体と遭遇』 (34.9s).
- ⚠ Lời hứa không giữ: 『76秒の映像』: có trong script (七十六秒, 910s) nhưng ngoài 90s — và viết bằng chữ Hán nên TITLE_LOCK báo FACT PASS mà grep 『76秒』 không thấy.
- ⚠ Lời hứa không giữ: Thumbnail 『弾丸のようであった』/『数秒で60マイル先へ』: có (829s/842s) nhưng không trong hook.
- Vấn đề: Tập này là bản của GTwoNSPbEv8 (150k, cùng Tesla + Hải quân 2004) nhưng đảo trình tự: kênh mẫu mở bằng vật thể 2004 + 『UFOは宇宙人じゃない』 ở 0s, tập mình mở bằng cái chết Tesla 1943 (sự kiện không bất thường).
- Vấn đề: 57–100s toàn câu trừu tượng không câu hỏi: 『夜空を見上げるとき、私たちは…想像しがちです』, 『傾向があります』, 『冷静に確認していく必要があります』.
- Vấn đề: 0 câu なぜ trong hook; khoá duy nhất 51.8–54.6s 『見えない糸で結ばれているのかもしれません』.
- Vấn đề: Hook 617 chữ < sàn gate 650.
- Vấn đề: Chương Nhật mạnh (第4章 河野防衛大臣 + AARO 『ホットスポット』 広島・長崎, 29 lần nhắc Nhật) không được hé trong hook.
- Vấn đề: Mô tả còn placeholder mốc chương.
- **Sửa:** Sửa TRƯỚC khi dựng (rẻ nhất lane — chưa render): 0–10s theo GTwoNSPbEv8: title-card vật thể + 76 giây, ví dụ 「2004年11月、米海軍の赤外線カメラが76秒間、翼のない白い物体を追い続けました。」 rồi 3 câu dựng hình ngắn và lời chứng 『ライフル弾のように』 (dữ kiện 829s) trước 30s — trả luôn chữ đỏ thumbnail.
- **Sửa:** 35–55s: lật hướng (K06/H26): 『答えを探していくと、たどり着くのは宇宙ではなく、1943年1月のニューヨークの一室です』 → cái chết Tesla + tài liệu bị lấy đi.
- **Sửa:** 60–95s: thay đoạn trừu tượng bằng 3 câu なぜ (vì sao tài liệu trả lại thiếu thùng; vì sao Lầu Năm Góc công nhận video; vì sao năm 2023 báo cáo Mỹ nêu tên 広島・長崎 là 'điểm nóng') → lời mời → 第1章.
- **Sửa:** Thumbnail: giữ bố cục; đổi nền sang trời đêm/biển tối cho khớp 8/9 kênh mẫu; có thể thêm 『76秒』 vào dòng trắng nhỏ để nối với tiêu đề.
- **Sửa:** Điền mốc chương thật vào TIEU_DE_MO_TA.txt trước khi đăng.
- Video mẫu: GTwoNSPbEv8 (cùng đề tài, cùng nguồn, 150.701 view — mở bằng vật thể 2004, lật về Tesla ở 43–55s)

#### Tập ep12-boriska-mars — —
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep12-boriska-mars` · CHƯA có script/tiêu đề/thumbnail/voice — chỉ có competitor.txt, evidence.json, series_ctx.txt, stock_queries.txt. · ưu tiên thấp (Chưa có gì để sửa; áp công thức ngay từ lúc viết.)
- Mốc: chốt — · giới thiệu — · hứa — (không có (chưa có giọng))
- Thumbnail: — — —
- Tiêu đề↔hook: — — Chưa có tiêu đề. · Thumb↔tiêu đề: — — Chưa có. · Thumb↔hook: — — Chưa có.
- Vấn đề: Chưa sản xuất. Video nguồn của kênh mẫu chỉ 24k (thấp hơn 6 top), đề tài Boriska/Sao Hoả là nhóm view trung bình của kênh (8be97qgwPYI 20k, xsL_7JTZRg8 13k).
- **Sửa:** Khi viết: giữ câu 0s kiểu video nguồn 「地球は核戦争で滅ぶ。」 (H24 dạng câu trích) — đó là câu thumbnail đỏ nên dùng.
- **Sửa:** Trong 20s: 1996年 + ロシアの小さな町 + 生後15日 (neo có sẵn trong competitor); 40–55s câu 『お母さん、僕は火星から来たんだ』 làm K14; 2–3 câu なぜ trước 第1章 ~110s.
- **Sửa:** Chương Nhật: hé trong hook (ví dụ tàu thăm dò Sao Hoả của Nhật / MMX nếu series_ctx có nguồn), không chỉ để ở chương 4.
- Video mẫu: IM_VpzBDjyU (nguồn trực tiếp) · UO4dRHRuBBE (lời cảnh báo về nền văn minh = chữ đỏ thumbnail)

### Nguyên tắc
- **Câu đầu tiên (0–4s) đọc lại đúng chữ vàng thumbnail hoặc nửa đầu tiêu đề.** — cơ chế: Người vừa bấm nghe lại đúng câu làm họ bấm → xác nhận 'đúng video' trước khi kịp phân vân; sau đó mới đến năm/người/điều bất khả. · bằng chứng: 8/9 video kênh mẫu: GTwoNSPbEv8 0.4s 『UFOは宇宙人じゃない。』 (150.701 view), HqaY3BLROJU 0.3s 『予言者が死の直前に残した一言。』 (112.543), gWF_9MYtji8 0.3s 『3906年の未来にタイムスリップした男』 (93.670); ngoại lệ OU1r2W68F0Y đọc tên chương 1. Tập mình 2/8 (ep03, ep06). · vì sao: Là thay đổi rẻ nhất (1 câu) mà khớp cả 4 phần gói đăng; hook-repair của h2dev có thể ghép vào đầu video đã dựng. · áp dụng: Mọi tập toshi-densetsu-jp: câu 1 của script = câu ≤20 chữ lấy từ chữ vàng thumbnail hoặc tiêu đề. Cấm câu mở kiểu lịch trình (『〜の夕方、〜空港から離陸しました』). Gate đề xuất: 30 chữ đầu script phải chứa ≥1 danh từ riêng/con số của tiêu đề.
- **Chữ đỏ thumbnail phải là một câu có mặt trong hook (40–60s), không phải câu ở giữa video.** — cơ chế: Người bấm vì câu đỏ; nghe thấy nó trong 1 phút là được 'trả thưởng' và tin phần còn lại cũng sẽ được trả. Câu đỏ ở phút 12–15 = 12 phút chờ. · bằng chứng: Kênh mẫu K 5/9: HqaY3BLROJU 「彼は地球の人間ではない」 đọc ở 48–51s; UO4dRHRuBBE 「地球文明は滅びの段階だ」 ở 47.8–54.2s; video duy nhất L là huF9eadlDeQ (đổi tiêu đề sau khi đăng). Tập mình: ep10 cả 3 dòng thumbnail ở 720–842s (L), ep08 『落下』 ở 309s. · vì sao: Thumbnail khớp tiêu đề nhưng lệch hook là loại lời hứa bị comment bắt lỗi (bẫy đã ghi trong skill youtube-hook-research). · áp dụng: Khi làm thumbnail (B7), chỉ chọn chữ đỏ từ các câu nằm trong 0–90s của voice.srt; nếu câu hay nhất nằm sâu trong video thì đưa câu đó lên hook trước rồi mới in lên thumbnail.
- **Hook kết thúc bằng 2–3 câu なぜ cụ thể rồi mới mời vào 第1章.** — cơ chế: Câu hỏi 'vì sao' không trả lời = lời hứa của cả video; lời mời 『それでは…最初から辿っていこう』 báo ranh giới hook/thân bài. · bằng chứng: Kênh mẫu ≥2 câu hỏi 8/9, lời mời 9/9 (4/9 nguyên câu それでは…辿っていこう), 第1章 trung vị ~115s. Tập mình ≥2 câu なぜ chỉ 2/8; ep10 thay câu hỏi bằng 『私たちは冷静に確認していく必要があります』. · vì sao: Lane mình kể chuyện theo hồ sơ — câu hỏi là cách giữ người xem không cần phóng đại, hợp luật hedge của lane. · áp dụng: Gate đề xuất: đoạn trước 第1章 có ≥2 câu kết thúc bằng 『のでしょうか』/『のか』 chứa なぜ hoặc 何; mỗi câu phải có 1 danh từ cụ thể (tên, năm, số).
- **Tiêu đề hứa bí ẩn LỚN hơn, không hứa giải thiêng; phủ định chỉ dùng khi nó mở ra đáp án kỳ lạ hơn.** — cơ chế: Khán giả kênh này tìm 'điều sách giáo khoa không nói' (CHANNEL_DNA Audience). 『X không phải Y, mà là Z bí ẩn hơn』 giữ người; 『X chỉ là thần thoại/trí nhớ sai』 làm lời hứa co lại trước khi xem. · bằng chứng: 0/9 tiêu đề kênh mẫu (và 0/31 tiêu đề đã đọc: 28 trong transcripts.json + 3 video mới) kiểu giải thiêng; GTwoNSPbEv8 phủ định 『UFOは宇宙人じゃない』 nhưng dẫn tới Tesla/100 năm trước — 150.701 view. Tập mình 4/8 giải thiêng (ep02, ep03 bản cũ, ep05, ep06). · vì sao: Lane giữ tính hồ sơ + hedge là đúng (luật lane), nhưng có thể đặt tiêu đề vào phần CÒN chưa giải thích được hoặc bí mật trong hồ sơ, thay vì vào kết luận bác bỏ. · áp dụng: Viết tiêu đề theo phần dư bí ẩn: ep05 → 『海軍が報告書を「原因不明」に書き換えた理由』 thay vì 『神話だった』; ep06 → 『何千人が同じ〝嘘の記憶〟を持つ理由』. Nếu dùng 『じゃない』 thì vế sau phải là bí ẩn mới (H26).
- **Có Nhật thì đưa Nhật lên tiêu đề/hook; chỉ có chương 4 Nhật mà không hé thì không giúp gì.** — cơ chế: Người xem Nhật ở lại khi thấy chuyện nước ngoài 'dính' tới mình ngay đầu; chương 4 ở phút 18–20 không kéo được click hay giữ chân 1 phút đầu. · bằng chứng: 3/3 video kênh mẫu có nội dung Nhật đều hé trong hook (saIym-x8dPc 0.3s 『日本だけが知っていた』 120.668 view; HqaY3BLROJU 57s 『東の島』 112.543; OU1r2W68F0Y 95s 『日本のある小さな村』 172.056). Nhưng GTwoNSPbEv8 (150k) và gWF_9MYtji8 (93k) không nhắc Nhật → Nhật là đòn bẩy, không phải điều kiện. Tập mình: chương Nhật 7/8, hé trong hook 3/8. · vì sao: Gate require_japan_hook_chapter=4 đang ép đúng thứ kênh mẫu không bắt buộc (vị trí chương 4) và bỏ qua thứ kênh mẫu làm (hé ở hook). · áp dụng: Mỗi tập: 1 câu hé chương Nhật trong 60–100s (ep10 広島・長崎 hotspot, ep01 日航1628便, ep02 神隠し). Nếu móc Nhật mạnh (ep08 秋田) thì đưa lên câu 0s và tiêu đề.
- **Trong kênh này view do đề tài + gói đăng quyết định, không do độ dài hay khung hook.** — cơ chế: Kênh dùng cùng một khung hook cho mọi video; cái khác nhau giữa 2.000 và 172.000 view là đề tài (danh tính loài người/Chúa/Mặt Trăng qua lời một người được chọn) và gói đăng có đồng bộ hay không. · bằng chứng: 28 video trong transcripts.json: hook 606–1126 chữ ở 27/28; P_gCT2xX1Fk 648 chữ → 2.000 view, 4xsecoMLW7c 611 → 4.300, gWF_9MYtji8 606 → 93.670. 3 video mới (4.769–13.739) có khung hook đủ nhất nhưng mới 1–3 ngày; 2/3 có gói lệch (zgiDcRLQteY tiêu đề 85% không được đọc, huF9eadlDeQ đổi tiêu đề sau khi đăng). · vì sao: Tránh sửa sai chỗ: kéo dài/cắt ngắn hook không cứu được đề tài yếu; và gate hook_chars không phân biệt được video thắng/thua. · áp dụng: Chọn đề tài theo nhóm top (ai đó nghe/thấy trực tiếp 'sự thật về loài người'); gate hook đo TRẬT TỰ (câu 0s, câu đỏ thumbnail trong 90s, ≥2 câu なぜ) thay vì chỉ đếm chữ; hạ sàn hook_chars về ~500 chữ phần kể (kênh mẫu 8/9 ở 501–760 nếu bỏ CTA).
- **Mô tả của kênh mẫu chỉ lặp tiêu đề; đừng đầu tư vào mô tả dài — nhưng giữ nó đồng bộ và không lỗi.** — cơ chế: Mô tả không hiện trên thumbnail/đề xuất; kênh dùng mô tả để lặp từ khoá tiêu đề + đẩy sang video cũ (🌕あなたにおすすめの動画🌕). · bằng chứng: 9/9 dòng 1 = 【都市伝説 ミステリー 怖い話】 + tiêu đề; 0/9 mốc chương; 0/9 đoạn tóm tắt; 8/9 có 3 link video cũ. Tập mình: 6/8 TIEU_DE_MO_TA.txt khác S4_MO_TA.hook_line, ep08 mốc chương dính thân bài, ep10 mốc chương còn placeholder. · vì sao: Lỗi mô tả (mốc chương rác, 2 bản khác nhau) là thứ duy nhất ở mô tả có thể gây hại; nội dung dài không mang lại gì theo dữ liệu kênh mẫu. · áp dụng: Dòng 1 mô tả = tiêu đề (hoặc câu title-card 0s); thêm khối 'video liên quan' trỏ tập cũ của lane; chỉ giữ 1 nguồn mô tả (TIEU_DE_MO_TA.txt) và kiểm mốc chương trước khi đăng.

### Lưu ý dữ liệu
- Mốc giây kênh mẫu lấy từ raw hook_segments (transcript tự động, mốc thật) — 9/9 có segments lúc viết file. Transcript tự động nghe sai vài chữ (牧上主 = 牧場主, ケシー = ケイシー, 赤シックレコード = アカシックレコード); nguyên văn trong seed giữ như transcript.
- Số chữ hook và vị trí 第N章 của 6 video top đo trên transcripts.json của h2dev (không có mốc giây) — mốc 第1章 ~115s/~125s/~167s của HqaY/saIym/GTwo là ƯỚC TÍNH theo vị trí ký tự ÷ tốc độ trung bình. 3 video new không có trong transcripts.json nên không đo được chương Nhật của chúng.
- View 3 video 'new' (đăng 2026-09-20/21/22) là số 1–3 ngày tuổi — không dùng để kết luận công thức yếu.
- Tập của mình chưa có số liệu view/retention (không có dữ liệu đăng trong thư mục) — mọi nhận xét là so khung với kênh mẫu, chưa phải đo hiệu quả.
- ep10 dùng voice.srt (chưa dựng final.mp4); nếu dựng có đệm/nhịp khác, mốc giây có thể dịch vài giây.
- Tốc độ đọc tương đương: kênh mẫu 356–383 chữ/phút (full_chars ÷ duration), profile lane 380,3 → mốc giây hai bên so trực tiếp được.
- Không chạy hook_library.py add, không sửa patterns.json/hooks.jsonl, không sửa gì trong h2dev.

---

## 色でたどる戦争の記録 → lane `irogatatarukioku`

Kênh: https://www.youtube.com/channel/UCaj1dslbibbHEnOAOh0tyYw

Kênh là 'triển lãm ảnh có người thuyết minh': mở bằng 1 bức ảnh có NGƯỜI (dân thường/người trẻ) → 1 câu lật nơi chốn/danh tính/thời điểm trong ≤26s → miễn trừ AI ~27s → nghi thức 「この写真をカラー化してみる」 + 3–4 màu cụ thể → 1 con số chính xác đến từng chữ số → câu hứa lộ trình 「〜を15枚の写真で辿っていく」 ở ~115–150s. Tiêu đề = sự kiện đắt nhất của cả video (thường nằm giữa/cuối video), thumbnail = cụm đầu tiêu đề + 1 con số trên khung cố định, mô tả = kể lại cảnh mở của hook bằng văn xuôi có ngày giờ.

### Khung hook theo giây
- **0–20s · Mời nhìn 1 bức ảnh + tả chi tiết thấy được** — Câu mời rồi 3–5 câu ngắn tả người/đồ vật/chữ trên biển hiệu. 4/9 dùng nguyên câu 「まずこの1枚(の白黒写真)を見ていただけるだろうか」, hDkg dùng 「これから何枚かの写真を見ていただく」; juow mở bằng con số, 3 video mới tả thẳng không mời. Ví dụ: 「まずこの1枚の白黒写真を見ていただけるだろうか?駅の階段の途中に女性が座り込んでいる。その膝の前に小さな女の子が立っている。」 (NNy4YQKQe5c 0.2s)
- **8–26s · Câu lật** — Một câu làm người xem sửa lại điều vừa đoán: nơi này không phải Nhật, 2 người kia là dân đảo, ảnh chụp 2 giờ trước khi xuất kích. 5/6 video top lật ở ≤25.8s (WUOH là ngoại lệ, 86.3s). Ví dụ: 「昭和の初めのどこかの地方都市の風景に見える。だがここは日本の本土ではない。」 (F1TBU19nQ_k 19.3–23.5s)
- **20–75s · Miễn trừ AI (~27s, gần như nguyên văn cố định)** — 9/9 video. Ở 8/9 video đặt SAU câu lật (WUOH đặt trước). Ví dụ: 「この動画では当時の白黒写真をAIで補正し、色を推定して再現している。当時カラーカメラで撮られていたらこう映っていたかもしれない姿だ。細部の色は実際と異なる場合がある。注目して欲しいのは色の正確さではなく、写真に映る人々の表情とその時代の空気だ。」 (4J5Il-hMN6E 30.7–57.0s)
- **28–87s · Nghi thức tô màu** — 「この写真をカラー化してみる」 rồi 3–4 câu màu cụ thể (chất liệu + màu). 9/9 video, kể cả 3 video mới. Ví dụ: 「この写真をカラー化してみる。…階段のコンクリートは乾いた灰色。女の子の服に小さな青い花模様が浮かび上がる。床に敷かれた新聞紙だけが白く残っている。」 (NNy4YQKQe5c 62.0–78.0s)
- **80–117s · Con số chính xác** — Số lẻ đến từng chữ số + phép quy đổi (1/10 dân số, 4 người có 1). 6/6 video top có trong 120s. Ví dụ: 「厚生省の児童局が全国で一斉に数えた結果である。…そしてこの調査に沖縄県は含まれていない。」 (NNy4YQKQe5c 81.4–115.7s)
- **105–150s · Khoá + hứa lộ trình** — Hé kết cục ('1 năm sau thị trấn này biến mất', 'họ thuộc phía sống sót') rồi hứa phạm vi + số ảnh. 8/9 có lời hứa (4 trong 120s thật, 2 ước tính 144–151s). Ví dụ: 「写真をよく見てほしい。…見送りの人々である。その中には息子の敵国となった国から海を渡ってきた親たちがいる。(今日)はこの若者たちの2年半を15枚の写真で辿っていく。」 (WUOHhqJQ8d8 102.9–118.6s)

- Tiêu đề: 【sự kiện/nơi/năm】 + khoảnh khắc trong ảnh hoặc nghịch lý + (——) hệ quả ｜ con số ｜実際の写真をAIフルカラー復元. 9/9 có 【】, 9/9 có số trong phần lõi, 9/9 đúng 3 đoạn ngăn bởi 2 dấu ｜, 9/9 đuôi 「実際の写真をAIフルカラー復元」; 「——」 chỉ 3/9 (đúng 3 video top đầu). Phần lõi 35–65 ký tự (6 video top 57–65). Nội dung tiêu đề là sự việc đắt nhất của video, chỉ 4/9 nằm trong hook (hDkg + 3 video mới).
- Thumbnail: Khung cố định 9/9: dải đỏ dọc bên trái chữ trắng 「カラーでよみがえる」, ảnh chiếm ~45% trái, nền đen phải, 2 khối chữ ngăn bởi 1 vạch đỏ; mỗi khối = 1 dòng trắng + 1 dòng vàng viền đỏ. Khối trên = cụm đầu tiêu đề (6/9 khớp tiêu đề), khối dưới = nhãn sự kiện/con số. 7/9 có chữ số (6/6 top). 0/9 có tên người. Ảnh: 6/6 top là mặt người (trẻ em, thiếu niên, dân đảo, cặp vợ chồng, đám đông nisei); 2/9 KHÔNG tô màu (hDkg top 1 và WUOH). 3 video mới: tàu, máy bay nhỏ trong khung viền trắng, lính + chó.
- Mô tả: Dòng 1 = cảnh mở/con số của hook viết lại thành văn xuôi (8/9; ms0j là ngoại lệ). Đoạn đầu dài 742–2.996 ký tự kể lại cả câu chuyện với ngày giờ/số liệu. Sau đó các mục ■ (映像について/色について 9/9, 写真出典 9/9, 参考資料 9/9, 運営者情報 8/9). 0/9 có Timestamps. Hashtag 3–8 cái. Câu hỏi mời bình luận: 0/6 video top, 2/9 tổng (ms0j, Upbb) — kênh hỏi gia đình khán giả ở CUỐI lời đọc (theo CHANNEL_DNA), không trong mô tả.
- 4 phần nối nhau: Tiêu đề và thumbnail là 1 lời hứa (thumbnail chép cụm đầu tiêu đề ở 6/9). Hook KHÔNG lặp lời hứa đó ngay (chỉ hDkg làm vậy) mà mở bằng ảnh đầu của dòng thời gian + 1 cú lật, rồi trả lời hứa bằng câu 'N bức ảnh sẽ dẫn tới…'. Mô tả nối hook: dòng 1 = cảnh mở của hook. Tức là: title+thumb bán kết cục, hook bán hành trình tới kết cục, mô tả xác nhận hook.
- Số đếm: {'video_phan_tich': 9, 'top': 6, 'new': 3, 'mo_bang_moi_nhin_anh_まず1枚': '4/9 (NNy4, 4J5I, F1TB, WUOH) + hDkg biến thể 「これから何枚かの写真を見ていただく」', 'cau_lat_truoc_26s': '5/6 top (0.2 · 8.2 · 22.9 · 23.5 · 25.8s); WUOH 86.3s', 'mien_tru_AI_trong_loi_doc': '9/9, bắt đầu 20.2–75.8s; đặt sau câu lật 8/9', 'nghi_thuc_カラー化してみる_trong_120s': '9/9 (28.4–86.6s)', 'con_so_chinh_xac_trong_120s': '6/6 top', 'loi_hua_lo_trinh': '8/9 (trong 120s thật: juow 29.2, WUOH 114.6, NNy4 115.7, F1TB 118.8, ms0j 99.2, Upbb 59.5; ước tính 4J5I ~144, hDkg ~151)', 'cau_khong_biet_trong_120s': 'top 0/6; new 3/3 (ms0j 2, Upbb 2, SO9N 1)', '写真をよく見てほしい_ca_video': 'hDkg 2 · NNy4 11 · 4J5I 4 · juow 1 · F1TB 9 · WUOH 13 (đếm trong transcripts.json)', 'thumb_khop_title': 'K 6/9, P 3/9, L 0/9', 'title_khop_hook': 'K 4/9 (hDkg + 3 new), P 5/9', 'thumb_co_so': '7/9 (6/6 top)', 'thumb_co_ten_nguoi': '0/9', 'thumb_anh_khong_to_mau': '2/9', 'title_do_dai_loi': '35–65 ký tự (top 57–65)', 'title_co_——': '3/9', 'desc_timestamps': '0/9', 'do_dai_video': '23.3–28.6 phút (9/9 ≥ 23 phút)', 'toc_do_doc_0_120s': '~4,5–4,7 ký tự/giây (transcripts.json)', 'video_kenh_≥10k': '8/28 video trong danh sách kênh; 7/8 là dân thường/người trẻ (特攻の少年, 上野の孤児, 沖縄の住民, 引き揚げ, サイパンの家族, 二世の若者, 広島の電車), 1/8 là tàu (長門 11.000)'}
- Ngoại lệ: ['hDkgnTPJw5g (top 1, 119.799 view): cả 4 phần cùng 1 câu — ảnh/sự kiện của tiêu đề nằm ở 16–27s, thumbnail là đúng ảnh đó (không tô màu).', 'WUOHhqJQ8d8: miễn trừ AI 20.2s đặt trước câu lật 86.3s — video thấp nhất trong 6 video top (12.744).', 'juowNKaQvek: mở bằng con số 660万人 không có ảnh; tiêu đề (mẹ chờ 13 năm), thumbnail (vợ chồng gặp lại sau 8 năm) và hook (660万) nói 3 chuyện khác nhau — vẫn 18.596 view.', 'NNy4YQKQe5c: thumbnail ghi 「戦争が終わって7年後の顔」 trong khi tiêu đề là 【昭和21年】.', "3 video mới (ms0j, Upbb, SO9N): không có câu mời nhìn ảnh, chủ thể là vật (tàu, máy bay) hoặc đảo trống, có 1–2 câu 'không biết/không xác nhận được' trong 120s đầu, mô tả dài phần giải thích nguồn."]

Thắng vs thua: Khác nhau chủ yếu ở ĐỀ TÀI, hook chỉ là yếu tố phụ. (1) 6 video top đều có mặt người thường/người trẻ và 1 mâu thuẫn cảm xúc (cười 2 giờ trước khi chết, trẻ mồ côi không ai dừng lại, phía sống sót là ngoại lệ, mẹ chờ 13 năm, thị trấn Nhật không ở Nhật, con đánh cho nước đang đánh cha mẹ). Video hook điểm thấp nhất trong top (juowNKaQvek 8/12, mở bằng con số không có ảnh) vẫn 18.596 view; video mới ms0jtVqHheA hook 9/12 nhưng chủ thể là con tàu, không có người, chỉ 72 view. Trong danh sách 28 video của kênh, các đề tài chỉ huy/chính khách/khí tài đều thấp: 吉田茂 ~1.000, 二・二六 2.200, ペリリュー 3.300, マンザナー 3.600, 大和 7.200, 榛名 6.800. (2) Hook có tạo khác biệt ở TRONG nhóm cùng đề tài người: hDkg đặt ảnh của tiêu đề + mốc 2 giờ vào 16–27s và gấp đôi video thứ 2; WUOH lật muộn nhất (86.3s, miễn trừ AI đặt trước) và thấp nhất nhóm top. (3) 3 video mới còn 1 điểm chung: có câu 'không biết/không xác nhận được' trong 2 phút đầu (0 ở video top) — nhưng chúng mới đăng 11–59 giờ nên chưa thể kết luận view; đây là tương quan, chưa phải nguyên nhân.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 119,799 | 22.9 | 11.8 | — | 0.2 | H28 K16 | 12 | K | K | K | 【特攻】出撃2時間前、17歳は子犬を抱いて笑っていた——翌朝、この写真に写る全員が帰らなかった｜残された最後の一枚｜実際の写真をAIフルカラー復元 |
| top | 62,207 | 25.8 | 111.2 | — | 115.7 | H27 H16 K02 K16 | 9 | P | P | P | 【昭和21年 上野駅】疎開から帰ると家も親もなかった——地下道で靴を磨いて生きのびた子どもたち｜孤児は12万3511人｜実際の写真をAIフルカラー復元 |
| top | 48,898 | 8.2 | 105.0 | — | — | H27 K16 | 10 | P | K | P | 【沖縄戦】島の人の85%が柵の中にいた——持ち出せたのは頭に載る分だけだった｜収容者は4月1日の21人から6月末に28万4625人｜実際の写真をAIフルカラー復元 |
| top | 18,596 | 0.2 | 25.2 | — | 29.2 | H16 K16 | 8 | P | P | P | 【岸壁の母】舞鶴に船が着くたび、母は13年間ずっと同じ場所に立っていた｜660万人が海を渡って帰った引き揚げの記録｜実際の写真をAIフルカラー復元 |
| top | 17,568 | 23.5 | 114.2 | — | 118.8 | H27 K06 K16 | 9 | P | K | P | 【1944年サイパン】銃を提げた海兵隊員が手を引いた少年は、2万6000人が隠れた島から出てきた｜島の暮らしは1年で消えた｜実際の写真をAIフルカラー復元 |
| top | 12,744 | 86.3 | 102.9 | — | 114.6 | H27 K17 K16 | 9 | P | P | K | 【第442連隊】親は収容所の柵の中、息子は最前線へ｜二世だけの部隊が、包囲された211人を救うために800人を失った｜実際の写真をAIフルカラー復元 |
| new | 72 | 44.5 | 95.9 | — | 99.2 | H27 K06 K16 | 9 | K | K | K | 【駆逐艦涼月】修理を打ち切られ、入り江に隠されたまま終戦を迎えた艦｜戦った2年半より、港を守った78年のほうが長い｜実際の写真をAIフルカラー復元 |
| new | 102 | 0.0 | — | — | 59.5 | H29 | 8 | K | K | K | 【ラバウル】日本兵が修理した隼は豪州へ｜750号機からたどる終戦後の人々｜実際の写真をAIフルカラー復元 |
| new | 4,158 | 22.5 | 95.6 | — | — | H27 | 10 | K | K | K | 【キスカ島】5千人が去った島に、連合軍が上陸した｜残された犬と空の陣地｜実際の写真をAIフルカラー復元 |

#### 【特攻】出撃2時間前、17歳は子犬を抱いて笑っていた——翌朝、この写真に写る全員が帰らなかった｜残された最後の一枚｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=hDkgnTPJw5g
- Câu chốt (22.9s): 「5人の少年が1匹の子犬を囲んで笑っている写真だ。その写真が撮られたのは彼らが出撃する2時間前だったと記録されている」
- Câu khoá (11.8s): 「そして最後に1枚の写真を見ていただきたい」
- Chữ thumbnail: カラーでよみがえる｜出撃 2時間前｜子犬を抱く17歳・最後の写真 (ảnh ĐEN TRẮNG, không tô màu) · Mô tả: 昭和20年5月26日、出撃予定の2時間前。鹿児島県の万世飛行場で、子犬を抱いて笑う5人の特攻隊員の写真が撮られました。最年少は17歳。写真の5人は、翌朝全員が帰らぬ人となりました。本動画では、この写真をはじめとする特攻隊員たちの実際の記録写真をAIでカラー復元し、80年前を生きた若者たちの最後の日々をたどります。
- Hook↔tiêu đề: K — Tiêu đề 「出撃2時間前、17歳は子犬を抱いて笑っていた」 được nói gần nguyên văn ở 16.1–26.8s. · Thumb↔tiêu đề: K — Thumbnail dùng đúng 3 cụm của tiêu đề: 出撃2時間前 · 子犬を抱く17歳 · 最後の写真 (=残された最後の一枚). · Thumb↔hook: K — Ảnh trên thumbnail chính là ảnh được tả ở 16–27s; con số 2時間前 là câu chốt ở 22.9s.
- Vì sao giữ người: Đặt nụ cười (con cún, tuổi 17) sát cạnh đồng hồ đếm ngược tới cái chết (2 giờ) trong 1 câu — người xem không cần biết bối cảnh vẫn thấy nghịch lý. Câu 'ảnh cuối cùng sẽ xem sau' giữ vòng mở tới hết video.
- Điểm yếu: Đoạn miễn trừ AI 30.4–56.8s chen ngay sau câu chốt, ảnh 1 thật sự (Philippines 1944) bắt đầu 56.8s — 26s không có thông tin mới. Thumbnail không tô màu dù kênh bán 'カラーでよみがえる'.

#### 【昭和21年 上野駅】疎開から帰ると家も親もなかった——地下道で靴を磨いて生きのびた子どもたち｜孤児は12万3511人｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=NNy4YQKQe5c
- Câu chốt (25.8s): 「(誰)も足を止めていない。1946年昭和21年の上野駅である」
- Câu khoá (111.2s): 「そしてこの調査に沖縄県は含まれていない。この動画が辿るのはその子供たちが集まった1つの場所の記録だ」
- Chữ thumbnail: カラーでよみがえる｜戦争が終わって 7年後の顔｜上野公園の子ども 12万3511人 · Mô tả: 昭和21年、1946年の上野駅。階段の途中に女性が座り込み、その足元では人が新聞紙を敷いて眠っている。行き交う人は誰も足を止めない。1945年3月10日の空襲で東京の下町は一夜のうちに焼け、死者はおよそ10万人にのぼったとされる。家を失った人々は、まず上野を目指した。上野駅が東北・北関東へ向かう列車の起点だったからである。田舎に縁故のある人は汽車で去り、行く先のない人が駅に残った。親を失った子どもたちも、そこに残った。駅の下を通る細長い
- Hook↔tiêu đề: P — Con số 12万3511 (tiêu đề) có ở 81.4–90s; 疎開・靴磨き・地下道 trong tiêu đề chưa xuất hiện trong 120s. · Thumb↔tiêu đề: P — Khớp con số 12万3511 và 上野; nhưng '戦争が終わって7年後の顔' lệch với 【昭和21年】 (=1 năm sau chiến tranh) của tiêu đề. · Thumb↔hook: P — Ảnh thumbnail là cậu bé mặt lấm lem, hook mở bằng ảnh người phụ nữ trên cầu thang; chỉ chung con số (84s) và 上野.
- Vì sao giữ người: Cảnh đời thường 'không ai dừng lại' làm người xem tự hỏi đây là đâu, lật ra ga Ueno 1946 ở 30s; rồi con số 12万3511 + câu 'Okinawa không nằm trong số đó' biến thống kê thành vết thương còn thiếu.
- Điểm yếu: Câu chốt 'không ai dừng lại' nhẹ; con số mạnh nhất tới 81s mới có. Thumbnail ghi '7年後' mâu thuẫn với 昭和21年 trong tiêu đề.

#### 【沖縄戦】島の人の85%が柵の中にいた——持ち出せたのは頭に載る分だけだった｜収容者は4月1日の21人から6月末に28万4625人｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=4J5Il-hMN6E
- Câu chốt (8.2s): 「右の2人はヘルメットをかぶった兵だ。左の2人はこの島に住んでいた人である」
- Câu khoá (105.0s): 「そしてこの写真の中の2人は生き延びた側の人だ」
- Chữ thumbnail: カラーでよみがえる｜島の人の 85%が柵の中｜沖縄戦を生きた 住民の記録 · Mô tả: 1945年3月26日、午前8時4分。沖縄県の慶良間諸島、阿嘉島に米軍が上陸した。8時25分に慶留間島、9時に座間味島。沖縄戦で、米軍が日本の土を踏んだ最初の朝である。6日後の4月1日、艦船およそ1400隻から1500隻、兵員およそ18万3000人が、読谷から嘉手納、北谷にかけての西海岸に上陸する。日本軍はこの海岸で反撃せず、上陸は静かに終わった。その日、米軍が保護した住民の数は、記録の上ではわずか21人である。島には、まだ数十万の人が残
- Hook↔tiêu đề: P — Cùng chủ đề dân thường Okinawa, nhưng 85%/柵/21人→28万4625人 của tiêu đề không có trong 120s đầu. · Thumb↔tiêu đề: K — Thumbnail chép nguyên cụm đầu tiêu đề 「島の人の85%が柵の中」. · Thumb↔hook: P — Ảnh thumbnail (người phụ nữ đội bó củi) khác ảnh mở đầu; 85% không nằm trong hook.
- Vì sao giữ người: Ảnh đặt lính Mỹ và dân đảo cạnh nhau rồi nói 'hai người này thuộc phía sống sót' — người xem hiểu ngay số phận mặc định là chết, sống mới là ngoại lệ.
- Điểm yếu: Tới 120s vẫn chưa nói 'hàng rào / 85%' của tiêu đề; lời hứa lộ trình ~144s (ước tính) muộn.

#### 【岸壁の母】舞鶴に船が着くたび、母は13年間ずっと同じ場所に立っていた｜660万人が海を渡って帰った引き揚げの記録｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=juowNKaQvek
- Câu chốt (0.2s): 「660万人。これは終戦の時日本の外にいた日本人の数だ」
- Câu khoá (25.2s): 「全員に同じ課題を突きつけた。生きて日本に帰ること。この動画はその帰り道の記録だ」
- Chữ thumbnail: カラーでよみがえる｜8年ぶりに 妻と再会｜引き揚げ船が着いた日・舞鶴の記録 · Mô tả: 660万人。これは、終戦のとき日本の外にいた日本人の数である。当時の日本の人口のおよそ一割が、兵士として、開拓民として、商人として、海の向こうにいた。敗戦は、その全員に同じ課題を突きつけた。生きて、日本に帰ること。昭和20年8月9日にソ連軍が国境を越えた満州では、国策で渡ったおよそ27万人の開拓民が、背負えるだけの荷物と子供の手だけを持って港を目指した。同年11月、中国・塘沽の埠頭は、船を待つ日本人で埋め尽くされている。満州からの出口と
- Hook↔tiêu đề: P — 660万人 của tiêu đề ở 0.2s; nhưng 岸壁の母 (nhân vật chính của tiêu đề) không có trong 120s. · Thumb↔tiêu đề: P — Chung 舞鶴/引き揚げ; thumbnail kể chuyện 'gặp lại vợ sau 8 năm' — khác người mẹ chờ 13 năm của tiêu đề. · Thumb↔hook: P — Hook là con số tổng, thumbnail là 1 cặp vợ chồng — chỉ chung chủ đề hồi hương.
- Vì sao giữ người: Con số 660万 kèm quy đổi '1/10 dân số' làm quy mô thành cảm giác; câu 'một cuộc chiến khác bắt đầu sau khi chiến tranh kết thúc' là nghịch lý khoá cả video.
- Điểm yếu: Mở bằng con số trừu tượng, không có mặt người trong 30s đầu; tiêu đề/thumbnail/hook kể 3 người khác nhau (mẹ 13 năm, vợ chồng 8 năm, 660万 nói chung). Vẫn 18,6k nhờ đề tài.

#### 【1944年サイパン】銃を提げた海兵隊員が手を引いた少年は、2万6000人が隠れた島から出てきた｜島の暮らしは1年で消えた｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=F1TBU19nQ_k
- Câu chốt (23.5s): 「だがここは日本の本土ではない。東京から南へおよそ2300km、太平洋に浮かぶサイパン島である」
- Câu khoá (114.2s): 「この1年後、この町は地上から消える」
- Chữ thumbnail: カラーでよみがえる｜銃を提げた兵士が 少年の手を引いた｜逃げ場のない島は 南北20キロ · Mô tả: 東京から南へおよそ2300キロ、太平洋にサイパン島がある。第一次世界大戦のあと国際連盟の委任で日本が統治した南洋群島の島の1つで、1921年に南洋興発という会社が生まれてからは、砂糖の島として栄えた。1943年8月の統計では日本人2万9348人が住み、ガラパンの街には映画館があり、カフェがあり、写真館があった。島で生まれ、日本の本土を一度も見たことのない子どもも大勢いた。1944年6月13日、海の上からの砲撃が始まる。6月15日、アメリ
- Hook↔tiêu đề: P — Chỉ vế cuối 「島の暮らしは1年で消えた」 có ở 114.2s; cậu bé và 2万6000人 chưa xuất hiện trong 120s. · Thumb↔tiêu đề: K — Thumbnail chép vế đầu tiêu đề (lính cầm súng dắt tay cậu bé). · Thumb↔hook: P — Chỉ chung đảo Saipan; ảnh cậu bé không có trong hook, 南北20キロ không được nói trong 120s.
- Vì sao giữ người: Tả 1 con phố trông như thị trấn Nhật rồi lật 'đây không phải Nhật' — người xem sửa lại nhận thức ngay trong 25s; câu 'một năm sau thị trấn này biến mất' mở vòng.
- Điểm yếu: Ảnh và câu trong thumbnail/tiêu đề (cậu bé + lính) không có trong 2 phút đầu; cảm xúc ở hook chủ yếu là hoài niệm.

#### 【第442連隊】親は収容所の柵の中、息子は最前線へ｜二世だけの部隊が、包囲された211人を救うために800人を失った｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=WUOHhqJQ8d8
- Câu chốt (86.3s): 「国籍はアメリカである。だがこの時親の祖国と生まれた国は戦争をしていた」
- Câu khoá (102.9s): 「写真をよく見てほしい。…集まっているのは見送りの人々である。その中には息子の敵国となった国から海を渡ってきた親たちがいる」
- Chữ thumbnail: カラーでよみがえる｜募集は1500人 志願は1万人近く｜ハワイの日系二世 1943年3月 (ảnh gần như đen trắng/nâu) · Mô tả: 1943年3月、ハワイ、ホノルルのイオラニ宮殿前の広場を、若い男たちの隊列が埋め尽くした。アメリカ陸軍に志願した日系二世の壮行式で、集まったのは2686人だったと記録されている。二世とは、日本から移り住んだ親のもとでアメリカに生まれた世代のことで、国籍はアメリカである。だがこのとき、親の祖国と生まれた国は戦争をしていた。募集は1500人だったが、ハワイでは1万人近くが志願したという。同じころ、アメリカ本土の事情は違っていた。前の年、西海
- Hook↔tiêu đề: P — Cùng 442; nhưng 'cha mẹ trong hàng rào trại' và 211人/800人 của tiêu đề không có trong 120s (bố mẹ ở Hawaii đi tiễn con). · Thumb↔tiêu đề: P — Chung chủ đề nisei 442, nhưng số liệu thumbnail (1500/1万) khác số liệu tiêu đề (211/800). · Thumb↔hook: K — Thumbnail = đúng ảnh mở đầu + đúng con số 1500/1万 nói ở 94.7s.
- Vì sao giữ người: Mâu thuẫn quốc tịch (Mỹ) và tổ quốc của cha mẹ (Nhật đang đánh Mỹ) + chi tiết ẩn trong ảnh (cha mẹ đứng tiễn) biến 1 ảnh đám đông thành câu chuyện gia đình.
- Điểm yếu: Miễn trừ AI 20.2–47.2s đặt TRƯỚC mâu thuẫn; câu chốt tới 86s mới có — 6/6 top chỉ video này để chốt sau 60s, và là video thấp nhất trong 6.

#### 【駆逐艦涼月】修理を打ち切られ、入り江に隠されたまま終戦を迎えた艦｜戦った2年半より、港を守った78年のほうが長い｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=ms0jtVqHheA
- Câu chốt (44.5s): 「戦いは終わったのに傷は残ったままだった」
- Câu khoá (95.9s): 「なぜ終戦から3ヶ月経ってもこの艦は壊れたままだったのか」
- Chữ thumbnail: カラーでよみがえる｜修理されず 入り江に隠された｜駆逐艦涼月 1945年の記録 · Mô tả: 1945年4月7日、戦艦「大和」とともに沖縄へ向かった防空駆逐艦「涼月」は、2番砲塔のわきに爆弾の直撃を受けました。甲板は約7.6メートルにわたって破れ、舷側の破口は水線下およそ90センチまで広がります。それでも艦は沈まず、艦首を深く沈めたまま、後ろ向きに佐世保へ帰り着いたと伝えられています。
- Hook↔tiêu đề: K — Ảnh tàu hỏng nằm trong vịnh (0–48s) + câu hỏi 'vì sao vẫn hỏng' (95.9s) = nửa đầu tiêu đề; 'đê chắn sóng' của vế sau có ở 108s. · Thumb↔tiêu đề: K — 修理されず/入り江に隠された/涼月 = đúng tiêu đề. · Thumb↔hook: K — Thumbnail là đúng ảnh mở đầu (tàu trong vịnh, 2 người đi xuống dốc).
- Vì sao giữ người: Câu hỏi 'chiến tranh đã hết 3 tháng sao tàu vẫn hỏng' đúng kiểu nghịch lý thời gian; lời hứa rõ phạm vi.
- Điểm yếu: Không có con người (2 người quay lưng, 'どんな人なのかは分からない' 59.4s) → cảm xúc 0; không có con số trong 120s. 72 view lúc lấy số liệu nhưng video mới đăng ~11 giờ — chưa so được.

#### 【ラバウル】日本兵が修理した隼は豪州へ｜750号機からたどる終戦後の人々｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=Upbbpdck--A
- Câu chốt (0.0s): 「日本の戦闘機が、オーストラリアへ送られた。その機体を修理し、梱包したのは、日本の兵士たちだった」
- Câu khoá (—s): 「—」
- Chữ thumbnail: カラーでよみがえる｜日本兵が直した隼 機体は豪州へ｜ラバウル 終戦後の記録 (ảnh nhỏ có viền trắng + chữ AUSTRALIAN WAR MEMORIAL) · Mô tả: 日本の戦闘機・隼は、日本兵に修理と梱包をされ、オーストラリアへ送られました。
- Hook↔tiêu đề: K — Tiêu đề 「日本兵が修理した隼は豪州へ」 được nói ở 0.0–3.8s. · Thumb↔tiêu đề: K — Thumbnail lặp gần nguyên tiêu đề. · Thumb↔hook: K — Ảnh thumbnail là ảnh 750号機 được tả ở 8.6–25s.
- Vì sao giữ người: Nghịch lý 'lính Nhật tự sửa máy bay Nhật để gửi cho Úc' đặt ngay giây 0.
- Điểm yếu: 81.9–100.8s nói liền 3 câu 'không biết': 「写真の3人がその作業をした人々かは分からない」「修理に当たった人数は決まらない」「名簿を結び付けてはいない」 — tự đóng câu hỏi vừa mở. Ảnh thumbnail nhỏ, người tí hon. Video ~35 giờ tuổi (102 view) — chưa so được.

#### 【キスカ島】5千人が去った島に、連合軍が上陸した｜残された犬と空の陣地｜実際の写真をAIフルカラー復元 — https://www.youtube.com/watch?v=SO9NUm_0YNI
- Câu chốt (22.5s): 「ところが、この施設を使っていた日本の守備隊は、もういなかった」
- Câu khoá (95.6s): 「米海軍の写真説明は、この犬が日本軍によって島に残されたと記している」
- Chữ thumbnail: カラーでよみがえる｜上陸した島に 守備隊がいない｜キスカ撤退 残された一枚 · Mô tả: 兵士の隣に、一匹の犬が座っている。後ろには、かつて日本軍が使った電話交換施設が見えます。1943年8月15日、アリューシャン列島のキスカ島で撮られた写真です。
- Hook↔tiêu đề: K — '5千人が去った島に連合軍が上陸' = 22.5–28.1s; 'con chó bị bỏ lại' ở 0s và 95.6s. · Thumb↔tiêu đề: K — 守備隊がいない = 5千人が去った; 残された一枚 ≈ 残された犬. · Thumb↔hook: K — Ảnh thumbnail là ảnh lính + chó được tả từ 0s.
- Vì sao giữ người: Đổ bộ vào đảo mà kẻ thù đã biến mất — nghịch lý chiến thuật rõ trong 25s; có con chó làm điểm cảm xúc.
- Điểm yếu: Không có lời hứa lộ trình trong 120s; khép vòng bằng 'không xác nhận được' ở 113–118s. 4.158 view trong ~2,5 ngày — tốt nhất trong 3 video mới nhưng chưa đủ tuổi để so với top.

### Các tập của mình

11/11 tập đã có final.mp4; không tập nào có DANG-TAI.txt nên chưa rõ trạng thái đăng. Mình chép đúng CÂU MỞ của kênh mẫu (11/11 「まず、この一枚の(肖像)写真をご覧いただ…」) nhưng không chép được phần làm nên hook: (a) ảnh mở 9/11 là chân dung 1 người (mẫu 9/9 là ảnh cảnh/nhiều người/vật) nên 0–25s chỉ còn tả quân phục, huân chương; (b) câu chốt trung vị 43.9s (18.4–120.2s) so với mẫu 23.2s ở 6 video top; ep01 120.2s, ep03 76.0s; (c) miễn trừ AI trong lời đọc 2/11 (mẫu 9/9); 「この写真をカラー化してみる」 0/11 (mẫu 9/9); lời hứa 'N枚の写真で辿る' 0/11 (mẫu 8/9); (d) 7/11 kể năm sinh trong 120s đầu (mẫu 0/9). Gói đăng: tiêu đề↔hook K 0/11, P 7/11, L 4/11 (ep03, ep05, ep07, ep11); thumbnail↔hook K 4/11 (ep06, ep08, ep10, ep11), P 3/11, L 4/11 (ep01, ep02, ep03, ep07); thumbnail↔tiêu đề K 0/11, P 5/11, L 6/11 — trong khi mẫu K 6/9. Nguyên nhân gốc: TITLE_LOCK 10/11 tập ghi chủ trương 'thumbnail và tiêu đề không lặp chữ nào / chia vai' — ngược công thức kênh mẫu. Thumbnail có tên người 11/11 (mẫu 0/9), có chữ số 5/11 (mẫu 6/6 top). Tiêu đề lõi 66–77 ký tự, 11/11 dài hơn tiêu đề dài nhất của mẫu (65). Lời hứa có vấn đề: 2 thumbnail đặt ngoặc cho câu diễn ý (ep01 「死ぬな、真実を語れ」, ep02 「床の隙間を直して」), 1 thumbnail khẳng định câu script tự nghi (ep07), 1 thumbnail nói quá sự thật (ep05 米国本土), 1 tiêu đề bỏ 'という' (ep04), 1 số tuổi không có trong lời đọc (ep04 47歳), 1 cặp số lệch (ep06 2年7ヶ月 vs 三年後). Độ dài video 7,1–18,3 phút, giảm dần từ ep01 tới ep11 (mẫu 23,3–28,6). Tập tốt nhất: ep08 (11/12, cùng ảnh với video 119k của mẫu) và ep10 (10/12). Ưu tiên sửa: cao ep01, ep03, ep05, ep07; vừa ep02, ep04, ep06, ep08, ep09, ep11; thấp ep10. Mọi sửa tiêu đề/thumbnail/mô tả làm được ngay không cần dựng lại video; sửa hook cần thu lại giọng + dựng lại.

#### Tập ep01 — 【沖縄戦】首里城地下の壕でランタンを囲む4人の将校——撮影から2か月3週間後、中央と隣の2人は島の南端で最期を迎えた｜1945年4月の一枚｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep01-ushijima-mitsuru` · Có final.mp4 (2026-09-21 14:27); không có DANG-TAI.txt → chưa rõ đã đăng · ưu tiên cao (Thumbnail có câu trong ngoặc không có nguyên văn trong script (dễ bị comment bắt lỗi) + 2 bộ thumbnail chưa chốt + câu chốt muộn nhất lane (120.2s). Sửa thumbnail/tiêu đề không cần dựng lại.)
- Mốc: chốt 120.2 · giới thiệu 110.2 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep01-ushijima-mitsuru\thumbnail_final.png (09-16 08:53, giống từng byte thumbnail.png 09-11) — CŨ hơn thumbnail_TEST_v2…v7.png (09-17 14:30–15:22); thumb_text.txt (09-17 15:21) khớp thumbnail_TEST_v7.png — thumbnail_final.png: 沖縄陥落の夜｜部下にただ一人｜「死ぬな、真実を語れ」｜[banner] 牛島満、最期の命令. thumbnail_TEST_v7.png: 沖縄陥落の夜｜ただ一人の部下に｜「死ぬな、真実を語れ」｜牛島満、最期の命令 (chữ to hơn). v2–v6: cùng chữ với final, chỉ khác cỡ/vị trí.
- Tiêu đề↔hook: P — 「四人の将校」 7.6s và ランタン 39.2s có trong hook, nhưng vế chốt 「2か月3週間後…最期」 ở 120.2s (ngoài 90s). · Thumb↔tiêu đề: L — Thumbnail nói mệnh lệnh cuối cho 1 cấp dưới, tiêu đề nói bức ảnh 4 sĩ quan; không chung cụm nào (TITLE_LOCK ghi cố ý 'không trùng chữ nào'). · Thumb↔hook: L — Mệnh lệnh cuối ở 579.5s (最後の命令) và 925.6s (真実を); 90s đầu chỉ tả ảnh + miễn trừ.
- ⚠ Lời hứa không giữ: Thumbnail đặt trong ngoặc 「死ぬな、真実を語れ」 nhưng script.txt không có câu này (grep 死ぬな = 0). Nguyên văn ~925s: 「もしお前が死ねば、この沖縄の戦いの真実を知る者が、誰もいなくなってしまう。…これは軍司令官としての、お前への命令である」 — ngoặc kép cho câu diễn ý.
- ⚠ Lời hứa không giữ: 「沖縄陥落」: script.txt có 0 lần chữ 陥落.
- ⚠ Lời hứa không giữ: Vế hệ quả của tiêu đề 「2か月3週間後」 ở 120.2s — không nằm trong 90s đầu.
- Vấn đề: 0–54.1s chỉ tả ảnh (「天井は丸太と土で組まれ」「傍らには金属の枠を持つランタンが一つ」) không có mâu thuẫn; kênh mẫu lật ở 8–26s.
- Vấn đề: Miễn trừ AI 66.0–98.5s (32s) đặt TRƯỚC câu chốt 120.2s; kênh mẫu đặt sau câu lật ở 8/9.
- Vấn đề: Không có 「この写真をカラー化してみる」 (0 lần); không có lời hứa lộ trình.
- Vấn đề: Hai bộ thumbnail chưa chốt: thumbnail_final.png (09-16) và thumbnail_TEST_v7.png (09-17, khớp thumb_text.txt).
- Vấn đề: Banner thumbnail là tên người (牛島満); kênh mẫu 0/9 thumbnail có tên.
- **Sửa:** Không cần dựng lại: chốt 1 file thumbnail; bỏ ngoặc 「」 hoặc dùng cụm có trong script — script có 「生きて語り続けよという言葉」 (~930s) → ví dụ 最後の命令は『生きて語れ』 vẫn là diễn ý nên KHÔNG đặt ngoặc.
- **Sửa:** Cho thumbnail và tiêu đề cùng 1 lời hứa như hDkgnTPJw5g: thumbnail lấy vế đầu tiêu đề + số, ví dụ 「ランタンを囲む4人｜2か月3週間後｜2人は島の南端で」.
- **Sửa:** Nếu dựng lại: đưa câu 120.2s lên 0–15s, cắt đoạn tả ảnh 54s còn ~15s, miễn trừ AI lùi sau câu chốt và rút về ~27s như mẫu, thêm 「この写真をカラー化してみる」 + 3 màu (ánh lửa đèn, gỗ, quân phục), thêm câu hứa 「この壕から島の南端まで、N枚の写真で辿っていく」. Câu mở mẫu: 「この写真の中央の二人は、2か月と3週間後、島の南端の壕で自ら命を絶つ。」
- Video mẫu: hDkgnTPJw5g (hệ quả của ảnh nói ở 16–27s) + 4J5Il-hMN6E (Okinawa, lật danh tính người trong ảnh ở 8.2s)

#### Tập ep02 — 【硫黄島】正面を見据えるこの司令官は万歳突撃を禁じた——最後の夜、階級章をすべて外したという｜2万2786人を率いた男の遺体は見つからなかった｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep02-kuribayashi-iwojima` · Có final.mp4 (2026-09-21 14:34); không có DANG-TAI.txt · ưu tiên vừa (Hook đã có câu chốt ở 36.9s khớp 1 phần tiêu đề; lỗi chính là thumbnail dùng ngoặc cho câu diễn ý và nói chuyện ở phút 6.)
- Mốc: chốt 36.9 · giới thiệu 86.1 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep02-kuribayashi-iwojima\thumbnail_final.png (09-16 09:10, bố cục ảnh bên phải). thumbnail.png (09-11) là bản cũ: cùng chữ, ảnh cắt sát mặt phủ toàn khung. — 妻への手紙は｜「床の隙間を｜直して」だった｜[banner] 栗林忠道、最期の36日 (2 file cùng chữ)
- Tiêu đề↔hook: P — 2万2786人 (36.9s) và 遺体 (43.7s) có trong hook; 万歳突撃 323.2s, 階級章 806.0s. · Thumb↔tiêu đề: L — Tiêu đề: cấm banzai/tháo quân hàm/thi thể. Thumbnail: thư gửi vợ/sàn nhà. Không chung cụm (TITLE_LOCK cố ý chia vai). · Thumb↔hook: L — 手紙 345.2s, 床/隙間 355.8s, 三十六日 837.7s — không có gì trong 90s.
- ⚠ Lời hứa không giữ: Thumbnail trích 「床の隙間を直して」 nhưng script chỉ viết 「家の床下にできた隙間の直し方を、絵まで添えて説明する」 (~355s) — ngoặc kép cho câu diễn ý.
- ⚠ Lời hứa không giữ: 階級章をすべて外した (tiêu đề) ở 806.0s; 36日 (banner) ở 837.7s.
- Vấn đề: 0–36.9s tả mũ/quân hàm/huân chương (帽章, 襟章, 略綬) — ảnh chân dung không có gì để lật.
- Vấn đề: Miễn trừ AI 48.8–81.2s; sau đó 86–111s tiểu sử (sinh 1891 ở 93.3s, 陸大次席) — kênh mẫu 0/9 nói năm sinh trong 120s.
- Vấn đề: Ảnh thứ 2 (106.9s) lại là chân dung; không có 「この写真をカラー化してみる」; không có lời hứa lộ trình.
- **Sửa:** Không cần dựng lại: bỏ ngoặc 「」 trên thumbnail hoặc đổi thumbnail sang lời hứa hook đã nói: 「2万2786人を率いた男｜遺体は｜見つからなかった」.
- **Sửa:** Nếu dựng lại: mở bằng câu 36.9–43.7s ở 0–10s kiểu juowNKaQvek (con số ở 0.2s): 「2万2786人を率いたこの男の遺体は、ついに見つからなかった。」; dời tiểu sử năm sinh ra sau 2 phút.
- Video mẫu: juowNKaQvek (con số ở giây 0) + hDkgnTPJw5g

#### Tập ep03 — 【ペリリュー】大佐は連隊旗を焼いて消えたとされる——それでも34人の兵は洞窟に潜み続け、投降は2年5か月後の1947年4月22日だった｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep03-nakagawa-peleliu` · Có final.mp4 (2026-09-21 14:38); không có DANG-TAI.txt · ưu tiên cao (Tiêu đề và thumbnail đều không có gì trong 4,5 phút đầu, hook tự chê ảnh mở; điểm hook thấp nhất lane (3/12).)
- Mốc: chốt 76.0 · giới thiệu 19.7 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep03-nakagawa-peleliu\thumbnail_final.png (09-16 09:10, file duy nhất) — たった4日のはずが｜73日間｜守り抜いた男｜[banner] 中川州男、ペリリューの最期
- Tiêu đề↔hook: L — 連隊旗 767.4s, 1947年4月22日 832.6s, 二年五か月 844.0s — không chi tiết nào của tiêu đề trong 120s; hook nói về ảnh mờ, vô danh. · Thumb↔tiêu đề: L — Cùng Peleliu nhưng không chung cụm: thumbnail 4日/73日, tiêu đề 連隊旗/34人/2年5か月. · Thumb↔hook: L — 四日 276.5s, 七十三日 535.5s; 「守り抜」 0 lần trong script.
- ⚠ Lời hứa không giữ: Toàn bộ chi tiết tiêu đề ở 767–844s (phút 12–14); toàn bộ chi tiết thumbnail ở 276–536s.
- ⚠ Lời hứa không giữ: 「守り抜いた男」 — script không có chữ 守り抜 (đảo vẫn thất thủ; đây là diễn ý).
- Vấn đề: 5–66s tự hạ giá ảnh mở đầu: 「これといって目を引くところのない、実に地味な一枚だ」「この写真は解像度が非常に低く、鮮明とは言い難い」 — kênh mẫu dùng ảnh mở là ảnh đắt nhất.
- Vấn đề: Câu chốt 76.0s mơ hồ (「ある戦術」 không nói là gì).
- Vấn đề: Không có miễn trừ AI trong lời đọc (script 0 chữ 'AI'); không có nghi thức tô màu; tiểu sử năm sinh 116.7s.
- Vấn đề: Kênh mẫu đã làm cùng đề tài (Eblvw8hqX4Y, 3.300 view) với tiêu đề 「3日で終わると言われた戦いは、46度の島で73日続いた｜34人は…2年5か月洞窟にいた」.
- **Sửa:** Không cần dựng lại: cho tiêu đề và thumbnail cùng 1 lời hứa — thumbnail đã có cặp 4日/73日 thì tiêu đề mở bằng chính cặp đó: 【ペリリュー】「4日で終わる」はずの島で、この大佐は73日間戦い続けた——… (lõi ≤65 ký tự).
- **Sửa:** Nếu dựng lại: bỏ đoạn 'ảnh mờ, vô danh' 5–66s; câu mở mẫu 「『4日で終わる』と言われた島で、この大佐は73日間戦い続けた。」 ở 0–10s, rồi lật: 34 người còn trong hang tới 1947.
- Video mẫu: F1TBU19nQ_k (lật nhận thức ở 23.5s) + 4J5Il-hMN6E

#### Tập ep04 — 【戦艦大和】着任時、47歳の艦長は長男に「死に場所を得た」と書き送った——翌年4月、総員退去の後も艦橋を離れなかった｜残る肖像写真はこの一枚だけ｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep04-aruga-yamato` · Có final.mp4 (2026-09-21 14:43); không có DANG-TAI.txt · ưu tiên vừa (Có 1 claim tiêu đề mạnh hơn script (艦橋) và 1 con số không có trong lời đọc (47歳); sửa rẻ.)
- Mốc: chốt 18.4 · giới thiệu 15.4 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep04-aruga-yamato\thumbnail_final.png (09-16 09:10, file duy nhất) — 片道分の燃料だけ｜積んで出撃した｜最後の艦長｜[banner] 有賀幸作、戦艦大和の最期
- Tiêu đề↔hook: P — 「残る肖像写真はこの一枚だけ」 32.6s có; 死に場所 302.4s, 総員退去 583.8s. · Thumb↔tiêu đề: P — Chung 大和/艦長; thumbnail 片道燃料, tiêu đề 死に場所/艦橋 — không chung cụm. · Thumb↔hook: P — 最後の艦長 23.4s có; 片道分の燃料 375.3s.
- ⚠ Lời hứa không giữ: 「47歳」 — script.txt không có tuổi nào (0 chữ 歳). Phép tính 1897-08-21 → 1944-12-10 = 47 đúng nhưng người xem không nghe.
- ⚠ Lời hứa không giữ: Tiêu đề khẳng định 「総員退去の後も艦橋を離れなかった」, script viết 「離れることを拒んだという」 và mô tả viết 「残された証言には食い違いがあり」 — tiêu đề bỏ mất 'という'.
- Vấn đề: 29.8s 「正確な年は分かっていない」 — câu 'không biết' trong 30s đầu (video top kênh mẫu: 0 câu loại này trong 120s).
- Vấn đề: 60.9–68.3s 「後にどのような最期を…何も読み取ることはできない」; 72–150s là ảnh tàu chạy thử 1941 không có người.
- Vấn đề: Không miễn trừ AI, không nghi thức tô màu, không lời hứa lộ trình.
- **Sửa:** Không cần dựng lại: thêm 「という」 vào vế 艦橋; bỏ 「47歳」 hoặc giữ nhưng biết là không có trong lời đọc; thumbnail lấy cụm đầu tiêu đề: 「長男への手紙｜『死に場所を得た』｜最後の艦長」 (câu này CÓ nguyên văn ~302s).
- **Sửa:** Nếu dựng lại: mở bằng câu thư ở 0–10s kiểu hDkg: 「この男は着任の時、長男に『死に場所を得た』と書き送った。」; dời 「正確な年は分かっていない」 xuống mô tả.
- Video mẫu: hDkgnTPJw5g (đưa chi tiết của tiêu đề vào 25s đầu)

#### Tập ep05 — 【アッツ島】軍医は「私はまだ三十三歳なのに死ぬ」と書いた——同じ日記に、病院の患者をどうしたかが記されていた｜米軍約11000名vs守備隊約2600名｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep05-yamazaki-attu` · Có final.mp4 (2026-09-21 14:47); không có DANG-TAI.txt · ưu tiên cao (Thumbnail có lỗi sự thật (本土) + tiêu đề trả lời ở phút 11 + tiêu đề và thumbnail nói 2 nhân vật khác nhau.)
- Mốc: chốt 51.7 · giới thiệu 23.3 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep05-yamazaki-attu\thumbnail_final.png (09-16 09:10, file duy nhất) — 米国本土で唯一の｜バンザイ突撃｜霧の中に消えた男｜[banner] 山崎保代、アッツ島の19日間
- Tiêu đề↔hook: L — 三十三歳 671.2s, 日記 668.2s, 患者 678.1s — lời hứa tiêu đề trả ở phút 11; hook nói Yamazaki. · Thumb↔tiêu đề: L — Tiêu đề = quân y + nhật ký; thumbnail = Yamazaki + banzai; không chung cụm (TITLE_LOCK cố ý chia vai). · Thumb↔hook: P — バンザイ突撃 55.9s và アメリカの領土 51.7s có; 霧 342.8s, 十九日 515.4s.
- ⚠ Lời hứa không giữ: Thumbnail 「米国本土で唯一の」 — script nói 「アメリカの領土の上で」. Attu thuộc lãnh thổ Alaska (năm 1943 chưa là bang), không phải 本土 → thumbnail nói quá script.
- ⚠ Lời hứa không giữ: Tiêu đề hứa 'bệnh nhân đã bị làm gì' — trả ở 678.1s.
- Vấn đề: 5–23s tả quân phục 「ごく典型的な一枚」 — tự nói ảnh không có gì đặc biệt.
- Vấn đề: 143–195s tranh luận lý do chiếm đảo, kết bằng 「どちらが正しいのか、今も結論は出ていない」 trong 3,5 phút đầu.
- Vấn đề: Không miễn trừ AI, không nghi thức tô màu; câu mạnh nhất lane (nhật ký quân y 「私はまだ三十三歳なのに死ぬ」) nằm ở phút 11.
- **Sửa:** Không cần dựng lại: sửa thumbnail 「米国本土で唯一の」 → 「アメリカ領で唯一の」; chọn 1 lời hứa cho cả tiêu đề và thumbnail — nếu giữ tiêu đề quân y, thumbnail nên là 「『私はまだ33歳なのに死ぬ』｜軍医の日記｜患者は…」.
- **Sửa:** Nếu dựng lại: mở bằng câu nhật ký ở 0–15s kiểu hDkg: 「『私はまだ三十三歳なのに死ぬ』。一人の軍医は、最後の突撃の朝、日記にそう書いた。」; dời đoạn tranh luận 143–195s xuống sau.
- Video mẫu: hDkgnTPJw5g (hệ quả đặt trong 25s) + 4J5Il-hMN6E

#### Tập ep06 — 【真珠湾】189機を発艦させた日、この肖像の男はまだ何も知らない——2年7ヶ月後、遺体を見つけたのは米海兵隊だった｜空母6隻を率いた提督の写真｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep06-nagumo-saipan` · Có final.mp4 (2026-09-21 14:51); không có DANG-TAI.txt · ưu tiên vừa (Hook và thumbnail đã khớp; chỉ lệch số giữa tiêu đề và thumbnail — sửa rẻ.)
- Mốc: chốt 40.4 · giới thiệu 28.7 · hứa 56.3 (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep06-nagumo-saipan\thumbnail_final.png (09-16 10:32, file duy nhất) — 真珠湾を勝利｜に導いた男｜三年後、サイパンの｜洞窟で消えた｜[banner] 南雲忠一、栄光から最期まで
- Tiêu đề↔hook: P — Cùng kết cục (洞窟 47.1s) nhưng số khác: tiêu đề 2年7ヶ月 (355.6s), hook 「およそ三年後」 40.4s; 189機 153.7s, 遺体 742.1s. · Thumb↔tiêu đề: P — Cùng người/kết cục; thumbnail 三年後 vs tiêu đề 2年7ヶ月. · Thumb↔hook: K — 三年後/洞窟 40.4–47.1s; 勝利 ≈ 「栄光の絶頂」 52.1s.
- ⚠ Lời hứa không giữ: Hai con số cho cùng 1 khoảng: tiêu đề 2年7ヶ月 (tính từ 12/1941), hook + thumbnail 'およそ三年後' (tính từ ảnh 1941–42).
- ⚠ Lời hứa không giữ: 「遺体を見つけたのは米海兵隊」 ở 742.1s; 「何も知らない」 ở 770.1s.
- Vấn đề: 0–28.7s tả quân phục/huân chương; 86–120s tiểu sử (sinh 1887 ở 91.0s).
- Vấn đề: Không miễn trừ AI, không nghi thức tô màu. Lời hứa 56.3s 「この一枚の写真から始まる物語は、その落差そのものである」 không có phạm vi/số ảnh.
- **Sửa:** Không cần dựng lại: thống nhất 1 con số (dùng 2年7ヶ月 cho cả thumbnail: 「2年7ヶ月後、サイパンの洞窟で」).
- **Sửa:** Hook đã đúng khung (hé kết cục ở 40s) — nếu dựng lại chỉ cần kéo câu 40.4s lên ~10s và thêm hứa lộ trình: 「真珠湾からサイパンの洞窟までの2年7ヶ月を、N枚の写真で辿っていく」.
- Video mẫu: F1TBU19nQ_k (「この1年後、この町は地上から消える」 — hé kết cục + mốc thời gian)

#### Tập ep07 — 【タラワの戦い】腰まで海に浸かり進んだ米海兵、第一波は死傷率約75%——だが守備隊約4700名のうち捕虜となった日本兵は17名｜1943年11月20日上陸｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep07-shibasaki-tarawa` · Có final.mp4 (2026-09-21 14:55); không có DANG-TAI.txt · ưu tiên cao (Ba bộ phận kéo 3 hướng + thumbnail khẳng định câu mà script tự nghi; sửa tiêu đề là đủ để 3 phần còn 2 hướng.)
- Mốc: chốt 36.5 · giới thiệu 19.0 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep07-shibasaki-tarawa\thumbnail_final.png (09-16 16:32, file duy nhất) — 「百万人が百｜年かけても｜落とせない」島は｜76時間で陥落した｜[banner] 柴崎恵次、タラワ・ベチオ島の指揮官
- Tiêu đề↔hook: L — Tiêu đề kể phía lính Mỹ: 腰まで 232.3s, 七十五 283.4s, 十七名 497.1s; hook là chân dung Shibasaki. · Thumb↔tiêu đề: L — Thumbnail = phía Nhật (câu 'trăm vạn người trăm năm' + 76 giờ), tiêu đề = phía Mỹ (lội nước, 75%, 17 tù binh) — cùng trận, 2 góc ngược nhau. · Thumb↔hook: L — 七十六時間 405.6s, 百万人/百年 445.8s.
- ⚠ Lời hứa không giữ: Thumbnail trích 「百万人が百年かけても落とせない」 như sự thật; script ~445s tự nghi: 「もしこの言葉が本当に語られたのだとすれば」 → thumbnail mạnh hơn script.
- ⚠ Lời hứa không giữ: Ba chi tiết của tiêu đề đều sau 3 phút 50 giây; mô tả dòng 1 lại theo góc 76 giờ (khác tiêu đề).
- Vấn đề: 14.0s 「撮影された場所も、正確な年も分かっていない」 và 118.3s 「正確にはどちらなのか、この記録でも確認できていない」 — 2 câu 'không xác định' trong 2 phút đầu (video top kênh mẫu: 0).
- Vấn đề: 80–116s tiểu sử (sinh 1894 ở 86.0s); không miễn trừ AI, không nghi thức tô màu, không lời hứa lộ trình.
- Vấn đề: 3 bộ phận nói 3 chuyện: hook = chân dung duy nhất, thumbnail = 76 giờ, tiêu đề = lính Mỹ lội nước.
- **Sửa:** Không cần dựng lại: viết lại tiêu đề theo góc thumbnail + mô tả, thêm 'とされた' cho khớp script: 【タラワの戦い】「百万人が百年かけても落とせない」とされた島は76時間で落ちた——守備隊約4700名、捕虜は17名 (rút lõi ≤65).
- **Sửa:** Nếu dựng lại: mở bằng 76 giờ ở 0–10s; chuyển 2 câu 'không xác định' khỏi 120s đầu xuống mô tả (kênh mẫu để kiểu này ở mục ■ 映像について).
- Video mẫu: F1TBU19nQ_k (lật ở 23.5s) + juowNKaQvek (con số ở giây 0)

#### Tập ep08 — 【特攻】写真の五人は自ら「ほがらか隊」と名乗った——出撃前夜、17歳は父へ遺書と遺髪を封筒で送り、宴では涙を見せる者もいた｜五人は全員17歳か18歳｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep08-araki-kamikaze` · Có final.mp4 (2026-09-21 14:58); không có DANG-TAI.txt · ưu tiên vừa (Hook tốt nhất lane (11/12); chỉ cần sửa tiêu đề (rẻ) để dùng đúng chi tiết đã làm video mẫu đạt 119k, và giải thích chênh lệch mốc giờ trước khi bị comment.)
- Mốc: chốt 56.9 · giới thiệu 49.1 · hứa 67.4 (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep08-araki-kamikaze\thumbnail_final.png (09-16 18:17, file duy nhất) — 子犬を抱いた17歳｜その15時間後｜誰も帰らなかった｜[banner] 荒木幸雄、「ほがらか隊」最後の一日
- Tiêu đề↔hook: P — 5 người, 17 tuổi có ở 0–54s; ほがらか隊 296.9s, 遺書/遺髪 261.9s, 涙 281.9s. Tiêu đề không nhắc 子犬 — chi tiết mạnh nhất của hook. · Thumb↔tiêu đề: P — Chung 17歳 và ほがらか隊 (banner); 子犬/15時間/帰らなかった không có trong tiêu đề. · Thumb↔hook: K — 子犬 13.2s, 十五時間 59.1s, 帰ってこなかった 64.3s — 3 dòng thumbnail đều trong 65s.
- ⚠ Lời hứa không giữ: Không có lời hứa sai; ほがらか隊 ở 296.9s (~5 phút).
- ⚠ Lời hứa không giữ: Cùng 1 ảnh với video top kênh mẫu hDkgnTPJw5g (119.799 view) nhưng mẫu nói 「出撃する2時間前」 (mô tả mẫu: 出撃予定の2時間前), mình nói 「十五時間から十七時間後」 — người đã xem video mẫu có thể comment. Chưa kiểm bên nào đúng.
- Vấn đề: Câu chốt 56.9s (mẫu với cùng ảnh: 22.9s); 26–41s kể ai chụp 「整備隊長がたまたま拾ってきた子犬を…」 chen giữa ảnh và câu chốt.
- Vấn đề: Không miễn trừ AI, không nghi thức tô màu.
- Vấn đề: Tiêu đề bỏ 子犬 và mốc giờ — đúng 2 thứ làm tiêu đề mẫu 119k.
- **Sửa:** Không cần dựng lại: tiêu đề đưa 子犬 + mốc giờ lên đầu như hDkg, ví dụ 【特攻】子犬を抱いて笑った17歳は、15時間後に飛び立った——五人は自ら「ほがらか隊」と名乗っていた｜… (lõi ≤65); thêm 1 câu trong mô tả về mốc 5/26 chiều → 5/27 5 giờ sáng và nguồn.
- **Sửa:** Nếu dựng lại: kéo câu 56.9s lên ~20s (cắt đoạn 'ai chụp' 26–41s xuống sau).
- Video mẫu: hDkgnTPJw5g (cùng ảnh)

#### Tập ep09 — 【第442連隊】家族が収容所で暮らす同じ日、22歳の二世兵はイタリアの敵陣へ単身で突撃した——手榴弾は跳ね返り、戦友二人の穴へ転がり込んだ｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep09-munemori-442nd` · Có final.mp4 (2026-09-21 15:00); không có DANG-TAI.txt · ưu tiên vừa (Lời hứa chính của thumbnail (gia đình trong trại) có trong video nhưng muộn; sửa banner rẻ, sửa hook cần dựng lại.)
- Mốc: chốt 31.7 · giới thiệu 25.2 · hứa — (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep09-munemori-442nd\thumbnail_final.png (09-16 18:21, file duy nhất) — 家族は収容所の｜柵の中にいた｜それでも彼は｜戦友を守った｜[banner] 宗森貞夫、日系人初の名誉勲章
- Tiêu đề↔hook: P — 22歳 31.7s có; 'gia đình ở trại' 109.3s (>90s; 51.7s chỉ là tên ảnh toàn cảnh trại); 単身 277.5s, 手榴弾 282.0s, 跳ね返 288.9s. · Thumb↔tiêu đề: P — Chung 収容所 và 戦友; banner 名誉勲章 không có trong tiêu đề. · Thumb↔hook: P — Trại xuất hiện ở 51.7s như 1 ảnh nhưng câu 'gia đình ở trong' 109.3s; 柵 481.4s, 名誉勲章 412.8s.
- ⚠ Lời hứa không giữ: 「柵」 chỉ có 1 lần trong script, ở 481.4s (đoạn kết).
- ⚠ Lời hứa không giữ: Banner 「日系人初の名誉勲章」 — script: 「日系人として、第二次世界大戦で初めて名誉勲章を受けた人物」 → banner bỏ vế 'Thế chiến II'.
- ⚠ Lời hứa không giữ: 「家族が収容所で暮らす同じ日」: script có 「息子が敵陣地へ突撃していたその頃、家族はこの宿舎の中で、いつもと同じ一日」 (~300s) — có, nhưng ở phút 5.
- Vấn đề: 0–25s tả quân phục/徽章; 50–62s ảnh trại mà không nói gia đình ở đó; 62–110s tiểu sử (sinh 1922 ở 68.0s).
- Vấn đề: Câu chốt 'chết cùng tuổi 22' yếu hơn mâu thuẫn quốc tịch ↔ cha mẹ mà video mẫu cùng đề tài dùng (WUOHhqJQ8d8 86.3s).
- Vấn đề: Không miễn trừ AI, không nghi thức tô màu, không lời hứa lộ trình.
- **Sửa:** Không cần dựng lại: banner đổi thành 「第二次大戦・日系人初の名誉勲章」 hoặc bỏ tên, dùng số (22歳).
- **Sửa:** Nếu dựng lại: đưa câu 109.3s 「同じ頃、両親と兄弟姉妹は、このマンザナー強制収容所に送られている」 lên ngay sau ảnh chân dung (~15s): 「この若者がアメリカ軍の軍服を着ていた頃、彼の母は、同じアメリカが作った収容所の柵の中にいた。」
- Video mẫu: WUOHhqJQ8d8 (cùng 442; mâu thuẫn tổ quốc cha mẹ)

#### Tập ep10 — 【1943年マンザナー】アンセル・アダムスにレンズを向け返した眼鏡の収容者がいた——所長が彼にスタジオを許した理由｜ロンドン受賞・ロス五輪を撮った写真家｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep10-miyatake-manzanar` · Có final.mp4 (2026-09-21 15:03); không có DANG-TAI.txt · ưu tiên thấp (Hook ↔ thumbnail đã khớp (hỏi ở 55s, thumbnail trả lời); chỉ tiêu đề dài và lệch góc.)
- Mốc: chốt 43.9 · giới thiệu 30.9 · hứa 59.1 (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep10-miyatake-manzanar\thumbnail_final.png (09-16 18:34, file duy nhất) — カメラを禁じられた｜収容所で｜彼は密造カメラ｜を作った｜[banner] 写真家・宮武東洋、マンザナーの記録. Ảnh là ảnh thật của Ansel Adams (photos\main01_miyatake_portrait.jpg) nhưng bản tô màu nền xanh trời, da mịn → trông như ảnh chụp hiện đại.
- Tiêu đề↔hook: P — アンセル・アダムス 28.3s, 眼鏡 5.2s, ロンドン 38.9s có; オリンピック 116.4s; 所長…スタジオ 238.3s; tiêu đề 'レンズを向け返した' vs script 'レンズを向け合っていた' (gần nghĩa). · Thumb↔tiêu đề: P — Chung 収容所/写真家; thumbnail = máy ảnh lậu, tiêu đề = Adams + studio. · Thumb↔hook: K — Hook 54.9s 「彼は密かに、あるものを作り上げていた」 — thumbnail trả lời đúng câu đố này (密造 294.6s, 組み立て 189.8s).
- ⚠ Lời hứa không giữ: Không có lời hứa sai; 「所長が…許した理由」 trả ở 238–250s (Weston giới thiệu).
- Vấn đề: Tiêu đề lõi 76 ký tự (mẫu dài nhất 65).
- Vấn đề: Không miễn trừ AI, không nghi thức tô màu.
- Vấn đề: Ảnh thumbnail tô màu kiểu hiện đại (nền xanh trời phẳng); kênh mẫu giữ hạt phim/tông cũ.
- **Sửa:** Không cần dựng lại: rút tiêu đề ≤65 và đưa 'カメラを禁じられた収容所' (khớp thumbnail + hook) lên đầu, ví dụ 【マンザナー】カメラを禁じられた収容所で、この写真家はレンズ1本からカメラを作った——撮ったのはアンセル・アダムス.
- **Sửa:** Cân nhắc tô lại ảnh thumbnail tông ấm/cũ hơn.
- Video mẫu: WUOHhqJQ8d8 (chi tiết ẩn trong ảnh) + hDkgnTPJw5g

#### Tập ep11 — 【二・二六事件】「老人ですから、とどめはお止め下さい」妻の一言で大尉は軍刀を収めた——救われた侍従長の命は9年後、終戦へとつながった｜実際の写真をAIカラー化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep11-ando-226incident` · Có final.mp4 (2026-09-21 15:08); không có DANG-TAI.txt · ưu tiên vừa (Hook và thumbnail đã khớp nhau ở 40–51s; chỉ tiêu đề đi hướng khác — sửa rẻ.)
- Mốc: chốt 46.3 · giới thiệu 21.6 · hứa 54.4 (srt (voice_paced.srt))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep11-ando-226incident\thumbnail_final.png (09-16 18:58, file duy nhất) — 「あの人は西郷の｜ような人だ」｜その人を撃｜った雪の朝｜[banner] 安藤輝三、二・二六事件
- Tiêu đề↔hook: L — Câu trong ngoặc của tiêu đề ở 210.2s, 軍刀 214.0s, 九年後 351.0s; hook nói câu Saigo. · Thumb↔tiêu đề: L — Thumbnail = câu Saigo + bắn; tiêu đề = câu vợ van xin + 9 năm sau; không chung cụm (TITLE_LOCK cố ý chia vai). · Thumb↔hook: K — 西郷 40.5s, 撃つ 51.4s, 雪 74.1s — cả 3 dòng thumbnail trong 75s.
- ⚠ Lời hứa không giữ: Tiêu đề 「終戦へとつながった」 — script 0 lần chữ 終戦, nói 「戦争そのものを終わらせる決断を下す」 (cùng nghĩa, không lỗi).
- ⚠ Lời hứa không giữ: Câu trong ngoặc của tiêu đề ở 210.2s (phút 3,5).
- Vấn đề: Câu Saigo bị cắt đôi giữa 2 cue 36.5s 「…こう語っていたという。『あの」 / 40.5s 「人は西郷隆盛のような人で」 → phụ đề cháy vào video sẽ ngắt giữa câu trích.
- Vấn đề: 78–117s tiểu sử (sinh 1905 ở 84.0s); không miễn trừ AI, không nghi thức tô màu; lời hứa 54.4s 「これは、その男の物語である」 không có phạm vi.
- Vấn đề: Video chỉ 7,1 phút (mẫu 23–28 phút).
- **Sửa:** Không cần dựng lại: tiêu đề dùng cùng nghịch lý với thumbnail/hook, ví dụ 【二・二六事件】「西郷のような人だ」と敬った侍従長を、この大尉は自ら撃った——妻の一言で命は救われ、9年後に終戦を決めた (rút lõi ≤65).
- **Sửa:** Kiểm lại cắt cue 36.5/40.5s trong voice_paced.srt trước khi cháy phụ đề.
- Video mẫu: hDkgnTPJw5g (1 nghịch lý = tiêu đề = thumbnail = hook)

### Nguyên tắc
- **Chọn chủ thể là người thường hoặc người trẻ trong chiến tranh, không phải chỉ huy hay khí tài.** — cơ chế: Khán giả (con cháu thế hệ chiến tranh) tự đặt ông bà mình vào khuôn mặt thiếu niên, trẻ mồ côi, dân đảo; tướng lĩnh và tàu chiến là chuyện quyết định chiến lược, xa đời họ. · bằng chứng: 7/8 video ≥10k của kênh là dân thường/người trẻ (hDkgnTPJw5g 119.799, NNy4YQKQe5c 62.207, 4J5Il-hMN6E 48.898, juowNKaQvek 18.596, F1TBU19nQ_k 17.568, WUOHhqJQ8d8 12.744, 8eDo6PiKUKo 10.000). Các video chỉ huy/chính khách/khí tài của chính kênh này: 吉田茂 _OAk6vBQfYU ~1.000, 二・二六 VEzkSc-fifQ 2.200, ペリリュー Eblvw8hqX4Y 3.300, 大和 WSdnDWdO5-U 7.200. juowNKaQvek hook chỉ 8/12 vẫn 18.596; ms0jtVqHheA (tàu, không người) hook 9/12 có 72 view (video mới ~11 giờ — xem caveats). · vì sao: Đề tài quyết định trần view mạnh hơn hook; hook tốt không cứu được chủ thể không có mặt người. · áp dụng: 9/11 tập của mình mở bằng chân dung chỉ huy. Trong mỗi tập, đưa 'người thường' của câu chuyện lên ảnh mở + thumbnail: ep05 quân y 33 tuổi và bệnh nhân, ep09 mẹ Nawa trong trại, ep02 vợ Yoshiko, ep01 dân thường Okinawa. Khi chọn đề tài mới, ưu tiên trụ cột dân thường/người trẻ.
- **Lật nhận thức trong 25 giây đầu, trước đoạn miễn trừ AI.** — cơ chế: Miễn trừ AI là 27s không có thông tin mới; nếu nó đến trước câu lật, người xem chưa có lý do để chịu nghe. · bằng chứng: 5/6 video top lật ở ≤25.8s (juow 0.2, 4J5I 8.2, hDkg 22.9, F1TB 23.5, NNy4 25.8) và 8/9 đặt miễn trừ SAU câu lật. Ngoại lệ WUOHhqJQ8d8: miễn trừ 20.2s, lật 86.3s — thấp nhất trong 6 video top (12.744). Tập của mình: trung vị 43.9s; ep01 miễn trừ 66.0s rồi mới lật 120.2s. · vì sao: Câu lật là lý do để ở lại; miễn trừ chỉ chịu được khi người xem đã có câu hỏi. · áp dụng: Câu thứ 2–4 của tập phải là câu lật (nơi chốn/danh tính/hệ quả). Với ảnh chân dung không có gì để lật, nói hệ quả ngay: 「この男は、2か月と3週間後…」. Miễn trừ đặt sau, dài ~27s như nguyên văn mẫu.
- **Giữ nghi thức 「この写真をカラー化してみる」 + miễn trừ AI trong LỜI ĐỌC ở mọi tập.** — cơ chế: Tiêu đề hứa 'AI復元'; khoảnh khắc ảnh đen trắng chuyển màu + 3–4 câu tả màu cụ thể là cú 'reveal' thị giác thứ hai ngay sau câu lật, và là chữ ký nhận diện kênh. · bằng chứng: 9/9 video mẫu có cả hai trong 120s đầu, kể cả 3 video mới (nghi thức ở 28.4–86.6s). Tập của mình: miễn trừ trong lời đọc 2/11 (ep01, ep02), nghi thức 0/11 (grep 「カラー化」 = 0 ở cả 11 script). · vì sao: Không có nghi thức thì kênh chỉ còn là slideshow ảnh màu; người xem không thấy phần 'phục chế' mà tiêu đề bán. · áp dụng: Thêm vào khung kịch bản lane D: sau câu lật → miễn trừ ~27s → 「この写真をカラー化してみる」 + 3 câu màu (chất liệu + màu, ví dụ 「軍服は深いオリーブ色。足元の土だけが白く乾いている」) — đồng bộ hình: ảnh đen trắng quét sang màu đúng lúc câu này.
- **Nói rõ lộ trình của video: 「〜の{thời gian}を{N}枚の写真で辿っていく」.** — cơ chế: Người xem biết còn bao nhiêu ảnh và điểm đến; video tư liệu 25 phút cần 1 hợp đồng rõ. · bằng chứng: 8/9 video mẫu có câu hứa (6/6 top): juow 29.2s, WUOH 114.6s 「この若者たちの2年半を15枚の写真で辿っていく」, NNy4 115.7s, F1TB 118.8s; ước tính 4J5I ~144s, hDkg ~151s. Chỉ SO9NUm_0YNI không có. Tập của mình: 0/11 có N ảnh; 4/11 có câu mơ hồ (ep06 56.3s, ep08 67.4s, ep10 59.1s, ep11 54.4s). · vì sao: Câu hứa biến chuỗi ảnh thành hành trình có đích, giảm rời video ở phút 2–3 khi tiểu sử bắt đầu. · áp dụng: Đặt ngay sau con số lớn (80–120s): 「今日は{nhân vật}の{N}年を{N}枚の写真で辿っていく」 — N lấy đúng số slot trong anchors.txt.
- **Không đặt câu 'không biết / không xác nhận được' trong 2 phút đầu; để độ dè dặt ở 'とされる/という' và ở mô tả.** — cơ chế: Câu 'không biết' trong hook báo trước bí ẩn không có lời giải — người xem không còn lý do chờ. · bằng chứng: 6/6 video top: 0 câu loại này trong 120s. 3/3 video mới có (ms0j 2, Upbb 2 — 3 câu liên tiếp 81.9–100.8s, SO9N 1 và tự khép vòng 113–118s 「そこまでは、この写真から確かめられない」). Kênh mẫu dồn phần nguồn/độ chắc vào mục ■ 映像について của mô tả. Tập của mình: ep04 29.8s, ep07 14.0s và 118.3s, ep05 183.4s. Lưu ý: 3 video mới mới đăng 11–59 giờ nên đây là tương quan. · vì sao: Giữ được sự trung thực (lane cấm bịa) mà không giết câu hỏi mở. · áp dụng: Trong 120s đầu chỉ dùng hedge mềm (とされる/という/伝えられている); câu 'không xác định' về ngày/nơi chụp chuyển xuống thân video hoặc mô tả.
- **Tiêu đề và thumbnail là MỘT lời hứa; thumbnail có số, không có tên người.** — cơ chế: Người xem thấy thumbnail và tiêu đề cùng lúc; hai câu khác nhau là hai lời hứa, không lời nào được củng cố. Tên một người lạ không có sức kéo với người chưa biết nhân vật, con số/tuổi thì có. · bằng chứng: Mẫu: thumbnail↔tiêu đề K 6/9, P 3/9, L 0/9; thumbnail có chữ số 6/6 video top; có tên người 0/9 (hDkg: 「出撃2時間前｜子犬を抱く17歳・最後の写真」 = đúng 3 cụm tiêu đề). Mình: K 0/11, L 6/11; TITLE_LOCK 10/11 tập ghi cố ý 'không lặp chữ nào'; tên người trên banner 11/11; chữ số 5/11. · vì sao: Chia vai giữa tiêu đề và thumbnail là quy tắc của tool tiêu đề h2dev, không có trong kênh mẫu. · áp dụng: Đổi luật trong tool tiêu đề (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\irogatatarukioku.json — thuộc h2dev/YT-TITLE-RESEARCH, research chỉ đề xuất): thumbnail = rút gọn cụm đầu tiêu đề + 1 con số; banner tên người → nhãn sự kiện + năm (kiểu 「キスカ撤退 残された一枚」).
- **Tiêu đề lõi (bỏ đuôi ｜実際の写真…) không quá 65 ký tự.** — cơ chế: Vế hệ quả sau 「——」 là phần bán video; tiêu đề càng dài thì vế đó càng dễ bị cắt ở danh sách đề xuất/di động (cơ chế hiển thị, không đo được trong kênh này). · bằng chứng: 9/9 tiêu đề mẫu có lõi 35–65 ký tự (6 video top 57–65). 11/11 tiêu đề của mình 66–77 ký tự — dài hơn tiêu đề dài nhất của mẫu. Không có số liệu view trực tiếp chứng minh độ dài gây giảm view; đây là giới hạn quan sát được của kênh mẫu. · vì sao: Giữ trong khoảng kênh mẫu đã dùng là lựa chọn an toàn khi chưa có số đo riêng. · áp dụng: Thêm cổng 'lõi ≤65' vào tool tiêu đề; tiêu đề đang 66–77 thì bỏ vế số liệu thứ 3 hoặc rút cụm mô tả ảnh.

### Lưu ý dữ liệu
- 3 video 'new' được lấy số liệu khi mới đăng: ms0jtVqHheA ~11 giờ (72 view), Upbbpdck--A ~35 giờ (102), SO9NUm_0YNI ~59 giờ (4.158); 6 video top đăng 2026-08-29…09-09. View của 2 nhóm KHÔNG so trực tiếp được — mọi kết luận 'video mới thấp vì…' chỉ là tương quan.
- Mốc giây của 9 video mẫu lấy từ hook_segments trong E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\raw (phụ đề tự động YouTube). Transcript có lỗi nghe (カ垢化=カラー化, 性格さ=正確さ, 裁判島=サイパン島, 愛の裏=…) — trích dẫn trong seed giữ nguyên văn transcript; trong analysis một số câu trích đã đọc theo nghĩa đúng.
- Mốc >120s của video mẫu là ƯỚC TÍNH = vị trí ký tự ÷ (len/duration) trong E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\irogatatarukioku\_raw\transcripts.json (4,5–4,7 ký tự/giây). Kiểm chéo: F1TB 'この1年後' ước tính 119.6s vs thật 114.2–118.8s; NNy4 'この動画が辿る' 122.7s vs thật 115.7s → sai số ~±7s.
- intro_t: kênh mẫu không có người kể tự giới thiệu (0/9) nên intro_t của video mẫu = null. Ở tập của mình intro_t = mốc nêu tên nhân vật (「名前を…という」), vì đó là tương đương gần nhất.
- Mốc giây tập của mình lấy từ voice_paced.srt; final.mp4 (09-21) có mtime sau srt nên coi như khớp. Một số cue srt chứa nhiều câu (vd ep02 36.9s, ep04 107.5s) nên mốc có thể sớm hơn thực tế vài giây.
- Không có DANG-TAI.txt ở cả 11 tập — không xác định được bản thumbnail/tiêu đề nào đã đăng, và không tra kênh của mình trên YouTube.
- ep08 dùng cùng ảnh với video top kênh mẫu; mẫu ghi 「出撃する2時間前」, mình ghi 「十五時間から十七時間後」 — chưa kiểm nguồn gốc bên nào đúng.
- char_rate profile = voice.char_rate 280,9 chữ/phút (không cần vì mọi tập có srt thật); tốc độ đọc đo được 0–120s ~4,4–4,8 ký tự/giây ở cả hai bên.
- Retention (heatmap) của kênh mẫu không lấy được (đã thử nhiều cách trước đây) — mọi nhận định 'giữ chân' là suy từ cấu trúc hook + view, không phải số retention.
- View trong raw (lúc tải hook) hơi khác view trong danh sách chọn video (vd hDkg 119.799 vs 119.000) do thời điểm lấy.
- Thumbnail tập ep10: ảnh gốc là ảnh thật của Ansel Adams (đã đối chiếu photos\main01_miyatake_portrait.jpg với img\000.png); nhận xét 'trông hiện đại' chỉ nói về cách tô màu.

---

## シニアいきいき健康 → lane `kenko-chiebukuro`

Kênh: https://www.youtube.com/channel/UCBODlDy5sXo_49pC7KPr7vQ

Một lời hứa, 4 cách nói: tiêu đề hứa CẢ DANH SÁCH (đối tượng tuổi + N món + động từ 'âm thầm'), thumbnail zoom vào MỘT món giữa danh sách và giấu tên bằng この食品/「これ」/〇〇, hook mở bằng triệu chứng/thói quen của CHÍNH người xem ở giây 0 rồi trước ~40s lật nguyên nhân sang chỗ không ngờ, hứa N món KHÔNG nêu tên và kéo mở đầu dài tới mục đầu (329–410s); mô tả thì nhắc lại hook và liệt kê hết đáp án cho người đọc/SEO. Không chào, không khối cấp cứu, không đọc trước danh sách.

### Khung hook theo giây
- **0–10s · Cơ thể/thói quen của chính người xem** — 6/6 video mở ở giây 0 bằng triệu chứng hoặc việc người xem vừa làm sáng nay; 0/6 mở bằng chào/cảm ơn. Ví dụ: 「夜中に2°3°と目が覚めてトイレに向かう。布団に戻ってもなかなか寝つけず気づけば窓の外が明るくなっている。」 (JCyxahsO0ew 0.1s (thật))
- **10–25s · Chặn lối thoát 'do tuổi' / khen nỗ lực rồi 'でも'** — 6/6 có trong 0–45s một câu gạt lời giải thích 'tuổi rồi' hoặc khen nỗ lực rồi 'nhưng'. Ví dụ: 「その真剣な知恵を私は心から尊敬しています。でも今日その努力に1つだけ大切なお話をしなければなりません。」 (kN6wHIqYA0Q 9.8–17.8s (thật); 66ADns1W2mA ~10s 「その変化を年のせいで片付けないでください」)
- **20–50s · Câu chốt: lật nguyên nhân (H30)** — Câu chốt thật ở 21.8s và 37.0s (2 video có mốc thật); 4 video ước tính 0–43s. Trung vị ~23s. Ví dụ: 「しかしその原因は暴行[=膀胱]だけにあるのではありません。実は皆さんの足の裏側ふハぎ[=ふくらはぎ]という場所に夜間尿の本当の鍵が隠れているのです。」 (JCyxahsO0ew 37.0s)
- **40–100s · Hứa N mục, giấu tên** — 3/6 hứa con số N trong 120s (kN6wHIqYA0Q 51.7s thật; 66ADns1W2mA ~53s, YZNmQJxGuRc ~96s ước tính); 4Q0fF3Ud57Q hứa 'món 100円' không số (~78s), JCyx hứa nội dung 101s + '3 điều' ~140s, 966f chỉ hứa chung ~43s. 6/6 không nêu tên món nào trong 120s. Ví dụ: 「これからお話する約13分で100年まで元気に生きた方々が…食べていた地[=9つ]の食品その食べ方の共通点そして今日から取り入れられる具体的方法について詳しくお伝えします。」 (kN6wHIqYA0Q 51.7s)
- **50–120s · Uy tín người nói + tương tác** — 4/6 tự nhận kinh nghiệm y khoa trong 120s (52–115s); kN6wHIqYA0Q xin comment 2 lần 78–110s và là video duy nhất có 82 comment (các video khác 3–16). Ví dụ: 「長年この分野に携わってきたものとしてこれほど大切な情報をお届けできることを心から嬉しく思います。」 (kN6wHIqYA0Q 67.9s)
- **120–410s · Cơ chế + ẩn dụ, mục đầu tới muộn** — 3/3 video đếm ngược đã chọn vào mục đầu ở 329–410s (1.597–1.822 chữ không dấu cách); 8/9 video đếm ngược trong transcripts.json của kênh: 1.598–1.916 chữ (314–410s). Ví dụ: 「さあ、では第10位から発表してまいりましょう。」 (YZNmQJxGuRc ~410s (ước tính))

- Tiêu đề: [Đối tượng tuổi 〜の方へ： HOẶC nhãn cảnh báo ご注意ください：/要注意、] + [N]つの[món/thói quen] + [cơ quan] + [động từ bí mật/khẳng định: 密かに…続けていた / 防いでいた / 削り続けています] + [đuôi ——ほとんどの方がご存知ない / 〜の方は必見]. Đếm: 9/9 bắt đầu bằng đối tượng hoặc nhãn cảnh báo; 7/9 có số N; 7/9 có tuổi/シニア/高齢者; 0/9 rào (かもしれない/検討/ことがある); 6/6 video top dài 37–51 chữ, 3 video mới 32–33 chữ; 8/9 không nêu tên món trong tiêu đề (trừ JCyxahsO0ew nêu ふくらはぎ).
- Thumbnail: Nền đen 9/9; 4 dòng chữ 9/9; màu dòng cam→trắng→đỏ→xanh lá 7/9 (66ADns1W2mA, 966fNPIqSi4 dùng vàng kim + đỏ, thêm 2 ảnh xếp dọc); ảnh THẬT 1 món bên phải 8/9 (JCyxahsO0ew dùng tranh minh hoạ người già đi tiểu đêm); 9/9 KHÔNG ghi tên món bằng chữ (この食品 / 「これ」 / 〇〇 / この食べ物 / 見逃される食品 / 卵の11倍); dòng cuối là lợi ích/cảm xúc 7/9 (朝までぐっすり!!, 医師も驚いた, 筋肉が変化!, 10年分老化を防ぐ!, 今夜から試す, 血流が変わる!, 驚きの美肌習慣), 2/9 là mệnh lệnh đỏ (今すぐ食べてください, 必ず見てください). 0/9 chép nguyên tiêu đề. Món trên ảnh là mục GIỮA danh sách: ごぼう = 第8位 (kN6wHIqYA0Q), trứng = 第5位 (66ADns1W2mA), きなこ = 第5位 (YZNmQJxGuRc), かつお節 = món thứ 3/3 (4Q0fF3Ud57Q) — 0/4 là 第1位. 2/6 thumbnail top có khẳng định KHÔNG có trong lời (4Q0fF3Ud57Q '10年分老化を防ぐ', YZNmQJxGuRc '卵の11倍' '3ヶ月').
- Mô tả: Dòng đầu nhắc lại hook (5/6 video top: JCyxahsO0ew, kN6wHIqYA0Q, 66ADns1W2mA, 4Q0fF3Ud57Q, YZNmQJxGuRc; 966fNPIqSi4 mở bằng 'この動画では…' rồi dòng 2 mới là hook) → đoạn cơ chế → 'nhiều năm làm với bệnh nhân' 6/6 → LIỆT KÊ HẾT đáp án 6/6 (kN6wHIqYA0Q 第9位 白湯…第1位 青魚; 66ADns1W2mA 第5位 卵…第1位) → CTA like/sub/share LINE → 免責事項 → hashtag. 3 video mới (09/21–23) đổi sang khung 「見ると分かること：」 gạch đầu dòng + 「参考情報・出典：」 (0/6 video top có).
- 4 phần nối nhau: Tiêu đề hứa cả danh sách; thumbnail lấy MỘT món giữa danh sách, giấu tên — là 'mẩu thử' của cùng lời hứa (thumbnail↔tiêu đề: 4/6 K, 1 P, 1 L). Hook nói lại lời hứa bằng cơ thể người xem và giữ bí mật tên món (hook↔tiêu đề: 4/6 K, 1 P, 1 L). Mô tả là chỗ duy nhất lộ đáp án. Món trên thumbnail xuất hiện ~330–1.170s nên người bấm vì thumbnail được trả lời giữa video, còn 第1位 giữ người tới cuối.
- Số đếm: {'open_no_greeting': '6/6 (0/6 mở bằng chào)', 'key_line_by_45s': '6/6 (thật: 21.8s, 37.0s; ước tính: 0, ~17, ~26, ~43s)', 'item_names_hidden_in_120s': '6/6', 'emergency_block_in_120s': '0/6 (JCyxahsO0ew có 1 câu miễn trừ ~12s ở 110s)', 'countdown_first_item_chars': '66ADns1W2mA 1.597 chữ/329s · kN6wHIqYA0Q 1.765/342s · YZNmQJxGuRc 1.822/410s (ước tính)', 'title_len_top6': '37–51 chữ (6/6 trong 35–55)', 'thumb_item_is_rank1': '0/4 video đếm ngược có ảnh món', 'views_per_day_at_audit': 'JCyxahsO0ew 3.064 · kN6wHIqYA0Q 3.425 · 66ADns1W2mA 2.513 · 4Q0fF3Ud57Q 1.808 · 966fNPIqSi4 1.614 · YZNmQJxGuRc 736'}
- Ngoại lệ: ["JCyxahsO0ew (top 1, 79.668 view) KHÔNG phải video đếm ngược — là video 'cơ chế + cách làm'; hook tự nói đáp án ふくらはぎ ở 45s, chỉ giấu hành động.", "YZNmQJxGuRc: tiêu đề '4つの節約食品が筋肉を傷つけ' nhưng nội dung là 'top 10 món tốt' — tiêu đề/thumbnail/hook 3 lời hứa khác nhau.", '66ADns1W2mA và 966fNPIqSi4 cùng tiêu đề, đăng cách 1 ngày, 2 kịch bản khác nhau (45.230 vs 27.438 view).', '4Q0fF3Ud57Q vào mục thật ở ~917s (checklist 12 dấu hiệu + cơ chế chiếm 44% video) mà vẫn 36k.']

Thắng vs thua: Ba video 'new' (9B8uVZDg1ZA, Hlkpj3AkUPY, 2YaaL5KS3-k) mới 0–2 ngày tuổi, không có transcript và bộ đếm view còn trễ (like 99–102 > view 30–70) → KHÔNG so được. So trong nhóm top (cùng đăng 28/08–06/09, tuổi 17–26 ngày): (1) Khác biệt nằm ở HOOK + GÓI ĐĂNG, không ở đề tài. Đề tài 'cơ bắp/đạm' có ở 4 video với 736–2.513 view/ngày; video thấp nhất YZNmQJxGuRc (736/ngày) cùng đề tài với 66ADns1W2mA (2.513/ngày) nhưng là video duy nhất có tiêu đề↔hook = L và thumbnail↔tiêu đề = L. (2) Hai video cao nhất JCyxahsO0ew (3.064/ngày) và kN6wHIqYA0Q (3.425/ngày) có K ở cả 3 cặp và câu chốt ở mốc thật 37.0s và 21.8s. (3) Cặp cùng tiêu đề 66ADns1W2mA (45.230) vs 966fNPIqSi4 (27.438): bản thắng hứa '5つの食品' ở ~53s và đếm ngược 第5位…第1位; bản thua chỉ hứa 'điều quan trọng' ở ~43s, không có số N trong 120s, không đếm ngược. (4) Like/view: 3 video đầu 5,0–7,1%, YZNmQJxGuRc 3,6%, 4Q0fF3Ud57Q 3,7% — hai video có thumbnail hứa điều không có trong lời có like thấp nhất.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 79,668 | 37.0 | 101.1 | — | 101.1 | H01 H16 H30 | 11 | K | K | K | 夜間頻尿・尿漏れで悩む方へ。ふくらはぎケアと食事改善で夜中のトイレ回数をゼロに近づける方法を医師が解説 |
| top | 71,922 | 21.8 | 51.7 | 67.9 | 51.7 | H31 H16 H30 K09 | 9 | K | K | K | 70歳以上の方へ：長寿者が密かに続けていた9つの食習慣——ほとんどの方がご存知ない |
| top | 45,230 | 26 | 53 | 70 | 53 | H01 H30 K09 | 11 | K | K | K | 高齢者の方へ：70代から積極的に摂りたい5つの食品が筋肉の衰えを防いでいた |
| top | 36,167 | 0 | 53 | — | 73 | H32 H30 H33 | 11 | K | P | P | ご注意ください：3つの一見体に良さそうな食習慣が、密かに筋肉を削り続けています——60代以上の方は必見 |
| top | 27,438 | 17 | 35 | 52 | 43 | H08 | 7 | P | K | P | 高齢者の方へ：70代から積極的に摂りたい5つの食品が筋肉の衰えを防いでいた |
| top | 16,190 | 43 | 96 | 115 | 96 | H31 H16 K09 | 5 | L | L | P | ご注意ください：4つの一見無害な節約食品が密かに筋肉を傷つけています—シニアの方は必見 |
| new | 58 | — | — | — | — |  | — | — | P | — | 要注意、70歳を過ぎたら知っておきたい足先の冷えと血管内皮の真実 |
| new | 30 | — | — | — | — |  | — | — | K | — | 血圧と動脈硬化が気になる方へ：5つの種が薬に頼らず血管を守る理由 |
| new | 70 | — | — | — | — |  | — | — | K | — | 60代以上の方へ：シミが消えない本当の理由と台所にある5つの解決策 |

#### 夜間頻尿・尿漏れで悩む方へ。ふくらはぎケアと食事改善で夜中のトイレ回数をゼロに近づける方法を医師が解説 — https://www.youtube.com/watch?v=JCyxahsO0ew
- Câu chốt (37.0s): 「しかしその原因は暴行[=膀胱]だけにあるのではありません。実は皆さんの足の裏側ふハぎ[=ふくらはぎ]という場所に夜間尿の本当の鍵が隠れているのです。」
- Câu khoá (101.1s): 「今日はこのふハぎの仕組みを正しく知っていただき、今夜からぐっすり眠れる体を一緒に目指していきましょう。」
- Chữ thumbnail: 夜間頻尿｜ふくらはぎを｜〇〇するだけ｜朝までぐっすり!! · Mô tả: 夜中に何度もトイレで目が覚めて、布団に戻ってもなかなか寝つけない…そんな夜を何年も繰り返していませんか？実は65歳を過ぎると、7割以上の方がこの悩みを抱えていると言われています。80歳を超えると、ほとんどの方が経験するというデータもあるほどです。
- Hook↔tiêu đề: K — 0.1s nói đúng 夜間頻尿 của tiêu đề, 45s nói ふくらはぎ — 2 từ khoá tiêu đề đều có trước 50s (mốc thật). · Thumb↔tiêu đề: K — Thumbnail lặp 夜間頻尿 + ふくらはぎ của tiêu đề, chỉ giấu hành động bằng 〇〇 và đổi 'ゼロに近づける' thành lợi ích cảm nhận 朝までぐっすり. · Thumb↔hook: K — ふくらはぎ ở 45s, 'ぐっすり眠れる体' ở 104–108s; phần giấu 〇〇 (マッサージ/足上げ) đúng là thứ hook chưa nói.
- Vì sao giữ người: Cảnh mất ngủ vì đi tiểu đêm ở giây 0 là cảnh người xem 65+ vừa trải qua đêm qua; 37 giây sau lật nguyên nhân sang bộ phận không ai nghĩ tới (bắp chân), nên người xem ở lại để biết 'làm gì với bắp chân' — đúng chỗ thumbnail giấu bằng 〇〇.
- Điểm yếu: Câu hỏi mở chỉ còn 'làm thế nào' vì chính hook đã nói đáp án ふくらはぎ ở 45s. Không phải video đếm ngược (chỉ 'hứa 3 điều' ~140s ước tính) — thắng nhờ triệu chứng cụ thể + cơ chế bất ngờ, không nhờ list. Có 1 câu miễn trừ y khoa ở 110s (~12s).

#### 70歳以上の方へ：長寿者が密かに続けていた9つの食習慣——ほとんどの方がご存知ない — https://www.youtube.com/watch?v=kN6wHIqYA0Q
- Câu chốt (21.8s): 「実は長寿の方がち[=日常的に]口にしていた食品は高金カナ[=高価な]サプリメントでも特別な健康食品でもありませんでした。ごく普通の昔から日本の食卓に並んでいた食材だったのです。」
- Câu khoá (51.7s): 「これからお話する約13分で100年まで元気に生きた方々が…地上的に[=日常的に]食べていた地の[=9つの]食品その食べ方の共通点そして今日から取り入れられる具体キ[=的な]方法について詳しくお伝えします。」
- Chữ thumbnail: 100歳まで元気な人｜毎日食べていた｜この食品｜医師も驚いた · Mô tả: 100歳を超えた方々が毎日食べていたのは、高価なサプリメントでも特別な健康食品でもありませんでした。昔から私たちの食卓に並んでいた、ごく普通の食材だったのです。
- Hook↔tiêu đề: K — Tiêu đề 'nhờ 9 thói quen ăn của người thọ, phần lớn không biết' = hook 21.8s (người thọ ăn đồ thường) + 51.7s (9 món, cách ăn). Mốc thật. · Thumb↔tiêu đề: K — Tiêu đề nói 9 món, thumbnail zoom vào 1 món (ảnh ごぼう, chữ giấu この食品) — cùng lời hứa, thu nhỏ còn 1 mục. Món trên ảnh là 第8位, không phải 第1位. · Thumb↔hook: K — '100歳まで元気な人 毎日食べていた' ≈ 56–64s 「100年まで元気に生きた方々が日常的に食べていた」; tên ごぼう chỉ lộ ~477s (ước tính) — đúng chỗ giấu. '医師も驚いた' không có câu tương ứng trong 120s.
- Vì sao giữ người: Mở bằng hỏi-về-bữa-sáng-hôm-nay rồi tôn vinh nỗ lực và 'nhưng' — người xem nghiêm túc với ăn uống thấy được thừa nhận, rồi bị chạm tự ái bằng 'người 100 tuổi không ăn đồ đắt'. Danh sách 9 món giấu tên kéo tới 第9位 ở ~342s.
- Điểm yếu: Mở đầu dài: tới 342s (ước tính, ~1.765 chữ) mới vào 第9位; 78–110s tốn ~30s xin comment. Không có cảnh/cảm giác cơ thể nên điểm 'dựng hình' thấp. Nhưng đây là video DUY NHẤT trong 6 có comment cao (82 vs 3–16) — lời xin comment trong hook có hiệu quả.

#### 高齢者の方へ：70代から積極的に摂りたい5つの食品が筋肉の衰えを防いでいた — https://www.youtube.com/watch?v=66ADns1W2mA
- Câu chốt (26s): 「ネタ切り[=寝たきり]になってしまった方の多くが実際に動けなくなる、ずっと前から何年もかけて静かに筋肉を失い続けていたということです。」
- Câu khoá (53s): 「今日は多くの専門家がこう霊社[=高齢者]に積極的に進める5つの食品についてお伝えします。どれもスーパーで手にはいるものばかりです。でも知っているかどうかで数年後の体は大きく違ってきます。」
- Chữ thumbnail: 70歳以降｜見逃される食品｜筋肉が死んでいく｜今すぐ食べてください · Mô tả: 70歳を過ぎたら、足腰の衰えは「年のせい」ではありません。
- Hook↔tiêu đề: K — Tiêu đề '70代 / 5つの食品 / 筋肉の衰えを防いでいた' — 0s nói 70歳, ~26s mất cơ, ~53s 5つの食品 (ước tính). · Thumb↔tiêu đề: K — Thumbnail đổi giọng từ lợi ích (防いでいた) sang sợ hãi (筋肉が死んでいく) + mệnh lệnh, nhưng cùng một lời hứa: 1 món 70歳 nên ăn. Ảnh trứng = 第5位. · Thumb↔hook: K — '見逃される' ≈ ~61s 「知っているかどうかで」; 'mất cơ âm thầm' ~26–44s. Trứng (ảnh) không được nêu trong 120s — giấu đúng chỗ.
- Vì sao giữ người: Triệu chứng chân nặng/leo cầu thang là thứ người 70+ tự nhận ra; câu 'đừng đổ cho tuổi' chặn lối thoát, câu 'người nằm liệt đã mất cơ từ nhiều năm trước' biến triệu chứng nhỏ thành nỗi sợ lớn, rồi hứa 5 món mua ở siêu thị.
- Điểm yếu: Mốc giây là ƯỚC TÍNH (raw rỗng). Tự giới thiệu 'nhiều năm làm y khoa người già' ở ~70s là tuyên bố uy tín không kiểm chứng được. Mục 1 (第5位) tới ~329s.

#### ご注意ください：3つの一見体に良さそうな食習慣が、密かに筋肉を削り続けています——60代以上の方は必見 — https://www.youtube.com/watch?v=4Q0fF3Ud57Q
- Câu chốt (0s): 「今すぐ手を止めてください。その湯で卵をお口に入れる前に」
- Câu khoá (53s): 「真面目に食べているそのタンパ質が筋肉の材料になるどころか体の中である恐ろしいことを静かに引き起こしているかもしれないのです。」
- Chữ thumbnail: 特に60歳からは｜豆腐・卵より｜「これ」が｜10年分老化を防ぐ！ · Mô tả: 毎日お肉も卵もしっかり食べているのに、なぜか太ももが細くなる。階段がつらくなる。これは食べる量の問題ではありません。
- Hook↔tiêu đề: K — Tiêu đề 'thói quen trông tốt cho cơ thể âm thầm bào cơ' = hook 0s (trứng), ~5–40s (ăn đạm mà đùi teo), ~45s 常識の落とし穴. Nhưng con số '3つ' không xuất hiện trong 120s. · Thumb↔tiêu đề: P — Tiêu đề nói 3 thói quen HẠI; thumbnail nói 1 món TỐT hơn đậu phụ/trứng (かつお節). Điểm chung chỉ là đậu phụ/trứng = 'thói quen trông tốt'. · Thumb↔hook: P — Trứng có ở 0s, 'món 100円' ở ~80s; nhưng '10年分老化を防ぐ' không có trong CẢ transcript (grep 10年/老化 = 0), かつお節 chỉ xuất hiện ~1.172s.
- Vì sao giữ người: Lệnh 'dừng tay' ở giây 0 kèm đúng món người xem đang ăn (trứng luộc) gây giật mình; phần sau chứng minh nỗ lực ăn đạm lại thất bại (đùi teo) — mâu thuẫn chính người xem đang sống — rồi checklist tự đếm giữ người xem tới ~260s.
- Điểm yếu: Mốc giây ƯỚC TÍNH. Mục thật (粉豆腐) tới ~917s — mở đầu + checklist + cơ chế chiếm 44% video. Thumbnail hứa '10 năm' không có trong lời. Tự giới thiệu ~420s. Like 3,7% thấp hơn 3 video đầu (5–7%).

#### 高齢者の方へ：70代から積極的に摂りたい5つの食品が筋肉の衰えを防いでいた — https://www.youtube.com/watch?v=966fNPIqSi4
- Câu chốt (17s): 「もう年だから仕方ないと。でも少し待ってください。実は同じ。70代でも毎日数kmを歩き旅行を楽しんでいる方がいる。一方でわずか数年で杖が必要になり外出を避けるようになってしまう方もいます。」
- Câu khoá (35s): 「その差を生み出している大きな原因の1つが毎日の食事なのです。今日は70代以降の筋肉を守るために本当に大切なことを分かりやすくお伝えしていきます。」
- Chữ thumbnail: 70歳過ぎたら｜この食品不足で｜筋肉が崩壊します｜必ず見てください · Mô tả: この動画では、70代以降に筋肉が急激に衰えていく本当の原因と、毎日の食卓でできる具体的な対策をわかりやすくお伝えします。
- Hook↔tiêu đề: P — Tiêu đề hứa '5つの食品'; hook tới 120s chỉ hứa 'điều quan trọng để giữ cơ', số 5 xuất hiện ~1.062s (ước tính). · Thumb↔tiêu đề: K — Cùng tiêu đề với 66ADns1W2mA; thumbnail '70歳過ぎたら この食品不足で 筋肉が崩壊' = lời hứa tiêu đề theo chiều sợ hãi. · Thumb↔hook: P — Hook có 'bữa ăn là nguyên nhân' (~35s) nhưng không có 'thiếu một món' — khung 'この食品不足' không được hook nhắc.
- Vì sao giữ người: So sánh 2 người cùng 70 tuổi (H08) là nỗi sợ quen của khán giả; nhưng ngay sau đó chỉ hứa chung chung nên không có câu hỏi cụ thể để chờ.
- Điểm yếu: Cùng tiêu đề với 66ADns1W2mA (đăng sau 1 ngày) nhưng 27k vs 45k: hook thiếu con số N và thiếu 'món ăn' trong 120s, danh sách không đếm ngược (chỉ 'これはまだ1つ目です' ~330s). Mốc ƯỚC TÍNH.

#### ご注意ください：4つの一見無害な節約食品が密かに筋肉を傷つけています—シニアの方は必見 — https://www.youtube.com/watch?v=YZNmQJxGuRc
- Câu chốt (43s): 「実は60歳以上の方の実に7割以上がある栄養素性的[=慢性的]に不足した状態で毎日を過ごしていると言われています。」
- Câu khoá (96s): 「これから12分から15分でなぜタンパ質がこれほど重要なのか、どれくらい食べればいいのか。そして今日からスーパーで帰る[=買える]筋肉を守る最強食品トップ店[=10]について具体的にお話しします。」
- Chữ thumbnail: 卵の11倍｜タンパク質が多い｜3ヶ月で｜筋肉が変化！ · Mô tả: 毎朝、なんとなく体が重い。疲れがとれない。足腰に力が入らない——その不調、実はタンパク質不足のサインかもしれません。
- Hook↔tiêu đề: L — Tiêu đề: '4 món ăn tiết kiệm trông vô hại đang làm hại cơ'. Hook: thiếu đạm + 'top 10 món tốt'. grep 節約/無害/傷つけ trong toàn transcript = 0. · Thumb↔tiêu đề: L — Thumbnail nói 1 món TỐT (きなこ, 'gấp 11 lần trứng', '3 tháng cơ thay đổi'); tiêu đề nói 4 món HẠI. Ngược chiều và khác số. · Thumb↔hook: P — Đạm có ở hook (~43–110s); きなこ = 第5位 ~836s; '11倍' và '3ヶ月' không có trong toàn transcript.
- Vì sao giữ người: Khung mở giống hệt kN6wHIqYA0Q (hỏi sáng nay → tôn vinh → でも) và có số liệu 7割, nên hook tự nó không tệ.
- Điểm yếu: Ba lời hứa khác nhau: tiêu đề (4 món hại) ≠ thumbnail (1 món tốt, số không có trong video) ≠ hook (top 10 món tốt). Người bấm vì tiêu đề không được trả lời → 736 view/ngày, thấp nhất nhóm top dù cùng đề tài cơ bắp với 66AD (2.513/ngày). Mốc ƯỚC TÍNH.

#### 要注意、70歳を過ぎたら知っておきたい足先の冷えと血管内皮の真実 — https://www.youtube.com/watch?v=9B8uVZDg1ZA
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: 寝る前の油で｜血管が若返る｜３つのオイル｜今夜から試す · Mô tả: 夜になると足先が冷たくなる、ふくらはぎがよくつる——そんな悩みを「歳のせい」だとあきらめていないだろうか。
- Hook↔tiêu đề: — — Không lấy được transcript — không chấm. · Thumb↔tiêu đề: P — Tiêu đề nói 足先の冷え + 血管内皮, không có 'dầu' hay số 3; thumbnail đổi hẳn sang '3 loại dầu trước khi ngủ' (chỉ mô tả mới nói dầu). · Thumb↔hook: — — Không lấy được transcript — không chấm.
- Vì sao giữ người: Không lấy được transcript — chỉ phân tích gói đăng.
- Điểm yếu: Đăng 2026-09-23 (0–2 ngày trước lúc audit), 58 view nhưng 102 like (like > view = bộ đếm view API còn trễ) → KHÔNG dùng làm 'video thua'. Mô tả đổi kiểu hẳn so với 6 video top: có 「見ると分かること：」 gạch đầu dòng + 「参考情報・出典：」 (3/3 video mới, 0/6 video top).

#### 血圧と動脈硬化が気になる方へ：5つの種が薬に頼らず血管を守る理由 — https://www.youtube.com/watch?v=Hlkpj3AkUPY
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: この５つの種で｜血管スッキリ!?｜70歳からでも｜血流が変わる！ · Mô tả: 健康診断でコレステロールや血圧の数値を指摘されても、自覚症状が何もないまま、そのまま普段の生活を続けていませんか。実は、動脈の中のプラークは固まって動かないものではなく、日々の食事によって育つことも、抑えられることもある生きた組織です。
- Hook↔tiêu đề: — — Không lấy được transcript — không chấm. · Thumb↔tiêu đề: K — Cùng '5つの種' + 血管 của tiêu đề; thêm tuổi 70歳 mà tiêu đề không có. · Thumb↔hook: — — Không lấy được transcript — không chấm.
- Vì sao giữ người: Không lấy được transcript — chỉ phân tích gói đăng.
- Điểm yếu: Đăng 2026-09-22 (0–2 ngày trước lúc audit), 30 view nhưng 99 like (like > view = bộ đếm view API còn trễ) → KHÔNG dùng làm 'video thua'. Mô tả đổi kiểu hẳn so với 6 video top: có 「見ると分かること：」 gạch đầu dòng + 「参考情報・出典：」 (3/3 video mới, 0/6 video top).

#### 60代以上の方へ：シミが消えない本当の理由と台所にある5つの解決策 — https://www.youtube.com/watch?v=2YaaL5KS3-k
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: キッチンにある｜この食べ物で｜シミが消える⁉｜驚きの美肌習慣 · Mô tả: 鏡を見るたびに増えていく顔や手のシミ。高いクリームや美容液を使っても、なかなか薄くならないと感じていませんか。実は、シミは単なる日焼けの跡ではなく、肌の中で今も続いている「色素の過剰な生産」です。この動画では、台所にある身近な5つの食品が、シミが作られる仕組みのどこに働きかけるのかを、分かりやすく解説します。
- Hook↔tiêu đề: — — Không lấy được transcript — không chấm. · Thumb↔tiêu đề: K — 台所 + シミ của tiêu đề; thu 5 giải pháp về 1 'この食べ物' (ảnh nha đam). · Thumb↔hook: — — Không lấy được transcript — không chấm.
- Vì sao giữ người: Không lấy được transcript — chỉ phân tích gói đăng.
- Điểm yếu: Đăng 2026-09-21 (0–2 ngày trước lúc audit), 70 view nhưng 101 like (like > view = bộ đếm view API còn trễ) → KHÔNG dùng làm 'video thua'. Mô tả đổi kiểu hẳn so với 6 video top: có 「見ると分かること：」 gạch đầu dòng + 「参考情報・出典：」 (3/3 video mới, 0/6 video top).

### Các tập của mình

8 tập (1 có final.mp4, 5 có giọng, 2 chỉ script); 0/8 có thumbnail, mô tả hay file đăng. So với công thức kênh mẫu: (1) 7/8 mở bằng chào/cảm ơn/tôn vinh (kênh 0/6). (2) Câu chốt: ep01 25.6s, ep02 30.0s, ep06 35.6s, ep07 ~36s đạt ≤40s; ep03 72.4s, ep05 72.8s, ep04 83.9s, ep08 ~116s trượt — 4/8. (3) 8/8 đọc trước cả danh sách trước mục đầu (kênh 0/6), 6/8 thêm câu 'thứ tự không phải mức độ'. (4) 5/8 có khối cấp cứu 119 trong 120s đầu, dài 17–58s (kênh 0/6). (5) 4/6 tập đã có giọng đọc to chữ 'タイトル' ở 0.3s (ep01, ep02, ep03, ep04) — ep01 đã dựng final.mp4 với lỗi này; ep07, ep08 script vẫn có dòng タイトル. (6) Tiêu đề: 7/8 ngắn 20–31 chữ (< 35), 1/8 có tuổi, 4/8 rào; ep06 là tập duy nhất đúng khuôn nhưng 4 cụm trong tiêu đề không có trong script. (7) Lời hứa tiêu đề muộn/thiếu trong 90s: ep03 (筋肉 180.9s), ep04 (糖尿病 186.3s), ep05 (むくみ 151.8s), ep06 (60歳/抗炎症/ご存知ない = 0), ep07 (認知機能 ~352s), ep08 (百寿者 ~680s). Tập gần khuôn nhất: ep05 (không khối 119, không preview trong 120s). Ưu tiên sửa: ep01 (sắp đăng), ep08 và ep03 (clone đề tài video top nhưng chốt chậm 2–5 lần, chưa/đã có giọng).

#### Tập ep01 — 転倒や骨折のリスクに関わるかもしれない、五つの食事の工夫のお話
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep01-tento-kossetsu` · có final.mp4 (B8 2026-09-20), chưa có thumbnail/mô tả, chưa đăng (không có DANG-TAI.txt) · ưu tiên cao (Là tập DUY NHẤT đã có final.mp4 — sắp đăng. Lỗi 'タイトル' đọc to ở 0.3s + 58s khối 119 nằm ngay trong video đã dựng.)
- Mốc: chốt 25.6 · giới thiệu — · hứa 48.3 (real (voice.srt, cùng giờ tạo với voice.mp3 dùng cho final.mp4))
- Thumbnail: — — —
- Tiêu đề↔hook: P — 転倒/骨折/五つの食事の工夫 tới 48.3s mới nói (ngoài lần TTS đọc tiêu đề ở 0.3s). Triệu chứng ふらつく ở 17s khớp 転倒 nhưng không nêu từ đó. · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: Không có lời hứa nào bị thất hứa về nội dung (転倒 3 lần, 骨折 7 lần trong script). Nhưng tiêu đề 'かもしれない…お話' không hứa gì cụ thể nên cũng không có gì để giữ.
- Vấn đề: 0.3–7.5s TTS đọc to chữ 「タイトル：」 + cả tiêu đề (voice.srt cue 1 = 「タイトル：転倒や骨折の」). final.mp4 dựng từ voice.mp3 này nên video đã xong mở bằng tiếng 'タイトル'.
- Vấn đề: 7.5s lời chào/tôn vinh 「心からの敬意を捧げます」 đứng TRƯỚC triệu chứng. Kênh mẫu 0/6 video mở bằng chào; kN6wHIqYA0Q đặt câu tôn vinh ở 9.8s SAU một câu hỏi về người xem.
- Vấn đề: Câu chốt 25.6–28.8s 「実は体からの大切な注意信号です」 không có con số/nguyên nhân bất ngờ (so JCyxahsO0ew 14.4s 「65歳を過ぎると7割以上」, 37s nguyên nhân ở bắp chân).
- Vấn đề: 56.7–114.5s = 58 giây dặn gọi 119/AED (đột quỵ, chóng mặt, ngã gãy, ngừng thở) — gần nửa 2 phút đầu. Kênh mẫu 0/6 video có khối cấp cứu trong 120s.
- Vấn đề: 114.5s–~150s đọc trước cả 5 mục 「第五位は…第一位は日本の伝統を誇る、身近で良質な発酵食品です」 — kênh mẫu 0/6 lộ tên mục trước mục đầu.
- Vấn đề: 「この順位は番組の構成上のもので、効果の優劣を示すものではありません」 — tự tháo lực kéo của đếm ngược; kênh mẫu không có câu nào như vậy.
- Vấn đề: Tiêu đề 31 chữ (< gate 35), không có tuổi/đối tượng, rào 'かもしれない', đuôi 'のお話'.
- **Sửa:** Xoá dòng 「タイトル：…」 khỏi script.txt trước TTS (hoặc để pipeline bỏ dòng này); với final.mp4 hiện có: cắt 0–7.5s hoặc làm lại voice.
- **Sửa:** Giây 0: bắt đầu bằng 「階段の一段が高く感じたり、平らな床でふらつくことは、ございませんか。」 (đang ở 12.6s). Câu tôn vinh 7.5s chuyển sau câu này (mẫu kN6wHIqYA0Q 0–21.8s).
- **Sửa:** Trước 30s chèn câu lật nguyên nhân theo H30, dùng số có trong series_ctx.txt, mẫu JCyxahsO0ew 37s: 「その原因は年齢だけではありません。実は毎日の食卓に…」.
- **Sửa:** Khối 119 (56.7–114.5s) rút còn 1 câu (~8s) trong hook; phần đầy đủ chuyển xuống ngay trước mục đầu tiên có hành động rủi ro (đúng lane_rules: 'TRƯỚC hoặc CÙNG lúc với hành động rủi ro', không bắt buộc ở giây đầu).
- **Sửa:** Bỏ đoạn đọc trước 5 mục + câu 'không phải ưu劣'. Thay bằng câu nhử mục 1 không nêu tên, mẫu H34: 「特に第一位は、あまりにも身近すぎて、まさかこれと思われるかもしれません。」.
- **Sửa:** Tiêu đề theo khuôn kênh (35–55 chữ): 「70代の方へ：転ぶ前に見直したい5つの食品——第一位は毎日の食卓にありました」 (câu gợi ý, khẳng định phải khớp tư liệu).
- **Sửa:** Thumbnail (khi làm): 4 dòng cam/trắng/đỏ/xanh, ảnh 1 món giữa danh sách (vd 小魚 = 第二位 hoặc プルーン = 第四位, KHÔNG phải 第一位), chữ giấu tên: 「70歳から｜転ぶ人は｜「これ」が足りない｜骨が変わる！」 — chỉ dùng khẳng định có trong script.
- Video mẫu: JCyxahsO0ew (cấu trúc 0–50s), 66ADns1W2mA (0–53s: triệu chứng → đừng đổ cho tuổi → hứa 5 món không nêu tên)

#### Tập ep02 — 気づかないうちに進む「筋肉の減少」5つのサイン
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep02-sarukopenia-sign` · có voice.mp3 + prompt ảnh (B5W/B5P), chưa có video/thumbnail/mô tả · ưu tiên vừa (Giọng đã có nhưng chưa dựng video — sửa lúc này còn rẻ (chỉ làm lại 2 phút đầu + TTS).)
- Mốc: chốt 30.0 · giới thiệu — · hứa 65.0 (real (voice.srt))
- Thumbnail: — — —
- Tiêu đề↔hook: K — Mở 6.3s bằng dấu hiệu cơ bắp (đứng dậy bật tiếng, đổi tay xách túi), 32.7s サルコペニア, 71.4s 五つのサイン. Cụm 「筋肉の減少」 trong tiêu đề không có nguyên văn trong script (0 lần), nhưng ý khớp. · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「筋肉の減少」 (tiêu đề) — 0 lần nguyên văn trong script.txt (script dùng 筋肉の衰え/サルコペニア). Không phải thất hứa nội dung, chỉ lệch chữ.
- Vấn đề: 0.3–6.2s TTS đọc 「タイトル…」 (voice.stt.srt cùng giờ tạo cũng nghe ra 'タイトル気づかないうちに').
- Vấn đề: 6.3–20s cảnh mở tốt nhất trong 8 tập (thao tác cụ thể, có cháu) nhưng không có con số/nguyên nhân bất ngờ trước 30s; câu chốt 30–37s chỉ gọi tên bệnh 「サルコペニアと呼ばれる、筋肉の衰え」.
- Vấn đề: 74.2s 「この順位は医学的な危険度ではなく…目安として」 tự tháo đếm ngược.
- Vấn đề: 84–112s đọc trước cả 5 dấu hiệu, lộ luôn 第一位 「指輪っかテスト」 ở 108.4s — đây là bài tự kiểm tra hấp dẫn nhất (kiểu checklist của 4Q0fF3Ud57Q) mà lại bị bán trước.
- Vấn đề: Tiêu đề 23 chữ, không tuổi/đối tượng.
- **Sửa:** Xoá dòng タイトル trước TTS.
- **Sửa:** Giữ cảnh 6.3s làm giây 0; trước 25s thêm câu hậu quả kiểu 66ADns1W2mA ~26s (người nằm liệt đã mất cơ âm thầm từ nhiều năm) — chỉ dùng dữ kiện có trong series_ctx.txt.
- **Sửa:** Bỏ đoạn 84–112s. Giữ 指輪っかテスト làm câu nhử: 「第一位は、今この場で、指二本だけで確かめられます。最後にご一緒にやってみましょう。」 (H34 + H33).
- **Sửa:** Tiêu đề: 「60歳以上の方へ：気づかないうちに筋肉が減っている5つのサイン——第一位は指だけで分かります」.
- **Sửa:** Thumbnail: ảnh bàn tay vòng bắp chân KHÔNG (đó là 第一位) — dùng dấu hiệu giữa danh sách (vd nắp chai = 第二位): 「70歳から｜瓶のフタが｜開かない人は｜筋肉が危ない」.
- Video mẫu: 4Q0fF3Ud57Q (checklist tự đếm ~98s), 66ADns1W2mA (0–53s)

#### Tập ep03 — 良かれと思って実は筋肉・腎臓に負担をかける食習慣5つ
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep03-eiyou-machigai` · có voice.mp3 + prompt ảnh, chưa có video/thumbnail/mô tả · ưu tiên cao (Câu chốt muộn nhất trong nhóm đã có giọng (72s) và tiêu đề lệch hook (L) — nhưng khái niệm giống hệt video 36k của kênh mẫu, sửa đúng khuôn là dùng được ngay.)
- Mốc: chốt 72.4 · giới thiệu — · hứa — (real (voice.srt); lời hứa 5 mục ~126–132s (ngoài 120s))
- Thumbnail: — — —
- Tiêu đề↔hook: L — Tới 90s không có 筋肉 (lần đầu 180.9s) và 良かれ (126.8s); 腎臓 lần đầu 109.4s. 0–72s là chào + khối 119. · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「筋肉」 (tiêu đề) có 4 lần trong script nhưng lần đầu ở 180.9s; 「負担」 lần đầu 503s. Không xuất hiện trong 90s đầu.
- Vấn đề: 0.3–7.4s TTS đọc 「タイトル:良かれと思って…」.
- Vấn đề: 7.5–24.9s chào + cảm ơn + tôn vinh (17s) trước khi nói gì về người xem.
- Vấn đề: 24.9–72s = 47 giây khối 119 (đột quỵ, TIA, đau ngực, sưng chân).
- Vấn đề: Câu chốt 72.4s 「健康のために信じてきた食習慣の中に、栄養不足を招く要素が、静かに紛れ込んでいる」 — đúng ý tiêu đề nhưng muộn gấp ~70 lần so với 4Q0fF3Ud57Q (0s, cùng khái niệm 'thói quen trông tốt').
- Vấn đề: ~155–194s (ước tính theo voice) đọc trước cả 5 mục; cuối script có 「お伝えした順位は危険度の差ではなく」.
- Vấn đề: Tiêu đề 26 chữ, không tuổi/đối tượng.
- **Sửa:** Xoá dòng タイトル; bỏ lời chào 7.5–24.9s.
- **Sửa:** Giây 0 theo H32 (mẫu 4Q0fF3Ud57Q 0s): 1 câu dừng tay với món có trong script, vd 「その野菜ジュースを飲む前に、少しだけ聞いてください。」 (野菜ジュース = 第四位 của chính tập này).
- **Sửa:** Đưa câu 72.4s lên ~10s; đưa 109.4s 「腎臓を気遣うあまり、必要な栄養量を大幅に下回ってしまう方」 lên ~20s.
- **Sửa:** Khối 119 còn 1 câu trong hook; phần đầy đủ đặt trước 第二位 (プロテイン) và 第一位 (断つ肉/魚) — chỗ có hành động rủi ro.
- **Sửa:** Tiêu đề: 「ご注意ください：60代以上が良かれと思って続ける5つの食習慣が、筋肉と腎臓に負担をかけています」 (khuôn 4Q0fF3Ud57Q, 50 chữ).
- **Sửa:** Thumbnail: ảnh 野菜ジュース (第四位): 「60歳から｜毎朝の｜「これ」が｜筋肉を減らす」.
- Video mẫu: 4Q0fF3Ud57Q

#### Tập ep04 — 血管・糖尿病の異変が足に出る5つのサイン
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep04-ashi-sign` · có voice.mp3 + prompt ảnh, chưa có video/thumbnail/mô tả · ưu tiên vừa (Có câu mở tốt sẵn (11.9s), sửa chủ yếu là cắt/đảo thứ tự; nhưng 48s khối 119 phải xử lý.)
- Mốc: chốt 83.9 · giới thiệu — · hứa 111.8 (real (voice.srt))
- Thumbnail: — — —
- Tiêu đề↔hook: P — 足 có từ 11.9s; nhưng 血管 lần đầu 118.1s, 糖尿病 lần đầu 186.3s, サイン 111.8s — nửa tiêu đề không có trong 90s. · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「糖尿病」 (tiêu đề) — 6 lần trong script nhưng lần đầu 186.3s; 「異変」 lần đầu 922s. Không có trong 90s.
- Vấn đề: 0.3–5.8s TTS đọc 「タイトル:」.
- Vấn đề: 5.9s lời cảm ơn trước câu hỏi 11.9s (câu hỏi 'lần cuối nhìn bàn chân' là câu mở tốt, đang bị đẩy xuống).
- Vấn đề: 29.8–77.8s = 48 giây khối 119 (tắc mạch cấp, sưng, đau ngực, vết thương đổi màu).
- Vấn đề: Câu chốt/số liệu 83.9s 「末梢動脈疾患を抱える患者さんは、国内にも数百万人」 — muộn; không có câu lật nguyên nhân.
- Vấn đề: ~125s đọc trước cả 5 dấu hiệu (五つ目…一つ目 trong 60 chữ).
- Vấn đề: Tiêu đề 20 chữ — ngắn nhất 8 tập; không tuổi.
- **Sửa:** Xoá dòng タイトル + lời cảm ơn; giây 0 = 11.9s 「皆さんがご自分の足先を、最後に見つめたのはいつ頃でしょうか。」 tiếp 16.9–26s triệu chứng.
- **Sửa:** Đưa 83.9s (数百万人) lên ~25s, nối 1 câu kiểu H30: 足のだるさは腰や膝のせいだけではない (đã có ở 94.9–100.9s — đưa lên ~30s).
- **Sửa:** Khối 119 → 1 câu trong hook; phần đầy đủ trước mục có hành động (xoa bóp/ngâm chân).
- **Sửa:** Bỏ đoạn đọc trước 5 dấu hiệu; nhử: 「一つ目のサインは、靴下を脱ぐだけで分かります。」 chỉ khi đúng nội dung mục 1.
- **Sửa:** Tiêu đề: 「放置厳禁：60歳以上の足に現れる5つのサイン——血管と糖尿病の異変は足先から始まります」 (khuôn 'dấu hiệu cơ thể' của kênh, 40+ chữ).
- Video mẫu: JCyxahsO0ew (triệu chứng → số liệu → nguyên nhân ở bộ phận bất ngờ trong 50s)

#### Tập ep05 — 脚のむくみが関係する夜間頻尿で検討したい5つの工夫
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep05-kettsuryuu-hinnyou` · có voice.mp3 + prompt ảnh, chưa có video/thumbnail/mô tả · ưu tiên vừa (Tập gần khuôn nhất, chỉ cần cắt 12s đầu + đảo câu chốt; nhưng trùng đề tài với video top-1 của kênh mẫu nên phải khác ở tiêu đề/thumbnail.)
- Mốc: chốt 72.8 · giới thiệu — · hứa 99.9 (real (voice.srt))
- Thumbnail: — — —
- Tiêu đề↔hook: P — 夜間頻尿 ở 43.1s (cảnh 12s đúng chủ đề); nhưng むくみ — chữ đầu tiêu đề — lần đầu 151.8s; 工夫 133.2s. · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「むくみ」 (từ đầu tiêu đề) lần đầu 151.8s — không có trong 90s. 「ふくらはぎ」 (đáp án chính của hook, 91.5s) lại KHÔNG có trong tiêu đề.
- Vấn đề: 0.5–12s chào + cảm ơn + 'hãy tưởng tượng' (11,5s) trước cảnh.
- Vấn đề: Cảnh 12–31s gần như chép cảnh 0–11s của JCyxahsO0ew (cùng đề tài 夜間頻尿/ふくらはぎ) nhưng chậm 12s.
- Vấn đề: Câu chốt 72.8–94.6s 「原因は、多くの場合、膀胱そのものではありません…ふくらはぎの血流こそが」 — JCyxahsO0ew nói cùng câu ở 37–49s. 43–66s chèn hướng dẫn 日本泌尿器科学会 trước câu chốt.
- Vấn đề: Tiêu đề rào 'で検討したい' (lời của bác sĩ, không phải của khán giả), 25 chữ, không tuổi, bỏ mất chữ ふくらはぎ.
- Vấn đề: Tập DUY NHẤT không có khối 119 trong 120s (chỉ 1 câu 'hỏi bác sĩ' ở 112.7s) — gần khuôn kênh nhất. NHƯNG ngay sau 120s là 「今夜のお品書き」 (chữ 640–1000, ~125–175s ước tính) đọc trước cả 5 mục, lộ 第一位 「夕方の足上げ」 — đúng hành động mà thumbnail JCyxahsO0ew giấu bằng 〇〇.
- **Sửa:** Bỏ 0.5–12s; giây 0 = 「夜中の二時半、ふと目が覚めて…」.
- **Sửa:** Đưa 72.8–94.6s (膀胱ではなく、ふくらはぎ) lên ~30–40s — ngay sau cảnh; dời câu 日本泌尿器科学会 (43.1s) xuống sau câu chốt để làm bằng chứng.
- **Sửa:** Tiêu đề: 「夜間頻尿で悩む70代の方へ：ふくらはぎを整える5つの習慣で夜中のトイレが減る理由」 — chỉ khẳng định mức script đã viết.
- **Sửa:** Thumbnail theo đúng thumbnail JCyxahsO0ew nhưng khác chữ: 「夜中のトイレ｜膀胱ではなく｜ふくらはぎ｜寝る前に〇〇」.
- **Sửa:** Bỏ đoạn 「今夜のお品書き」 (5 mục); giữ 第一位 夕方の足上げ làm bí mật, nhử bằng H34: 「第一位は、夕食の前にたった三十分、あることをするだけです。」.
- Video mẫu: JCyxahsO0ew

#### Tập ep06 — 60歳以上の方へ：5つの抗炎症食品が腸と脳を静かに守っていた——ほとんどの方がご存知ない
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep06-koenshou-shokuhin` · có title.txt + voice.mp3 + prompt ảnh (luồng lean), chưa có video/thumbnail/mô tả · ưu tiên vừa (Tiêu đề đã đúng khuôn nhưng 4 cụm trong tiêu đề không có trong script — rủi ro comment bắt lỗi; sửa 1 dòng tiêu đề là xong phần lớn.)
- Mốc: chốt 35.6 · giới thiệu — · hứa 99.1 (real (voice.srt))
- Thumbnail: — — —
- Tiêu đề↔hook: P — 腸と脳 ở 59.2s, 5 món ở 99.1s; nhưng 60歳, 抗炎症, 静かに守, ご存知ない — 0 lần trong CẢ script (grep). · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「60歳以上」 — 0 lần trong script.
- ⚠ Lời hứa không giữ: 「抗炎症」 — 0 lần (script dùng インフラメイジング/炎症から守る).
- ⚠ Lời hứa không giữ: 「ほとんどの方がご存知ない」 nhưng 106–115s đã đọc trước cả 5 món, món nào cũng là thứ ai cũng biết (発酵食品、食物繊維、青魚、野菜と果物、油と木の実).
- Vấn đề: 0.3–8s chào + cảm ơn.
- Vấn đề: 35.6s thuật ngữ 「インフラメイジング」 và 65.8s 「パキスタン・イスラマバードで成人140人」 — bằng chứng xa lạ với người xem Nhật 70 tuổi; kênh mẫu dùng tên viện Nhật (SOP lại cấm copy thói tên viện mơ hồ — nên chọn nguồn Nhật có thật trong tư liệu).
- Vấn đề: 81–98s khối 119 (17s — ngắn hơn ep01/03/04, chấp nhận được nhưng vẫn trong hook).
- Vấn đề: 106–115s đọc tên cả 5 món trước 第5位 (130s).
- Vấn đề: Tiêu đề chép khuôn aWXuORPaoH0 (5.800 view, không phải video top); 44 chữ — tập DUY NHẤT đạt title_len.
- **Sửa:** Bỏ 0.3–8s; giây 0 = 「しっかり食べているのに力が出ない、眠っているはずなのに朝がつらい…」.
- **Sửa:** Câu ẩn dụ 23.9s giữ (ẩn dụ đời thường là DNA kênh). Thay 'インフラメイジング' bằng 1 câu thường (痛みも熱もない小さな炎症) ở ~30s.
- **Sửa:** Bỏ 106–115s; câu nhử H34: 「第1位は、毎日の台所にあるのに、ほとんどの方が使い方を間違えています。」 — chỉ khi nội dung mục 1 thật sự nói cách dùng dầu.
- **Sửa:** Sửa tiêu đề cho khớp script: bỏ '60歳以上' hoặc thêm vào script; đổi '抗炎症食品' thành chữ script dùng: 「60歳以上の方へ：腸と脳を炎症から守る5つの食品——第1位は台所の油でした」.
- **Sửa:** Thumbnail: ảnh 青魚 (第3位 — giữa danh sách): 「60歳から｜物忘れが｜増えた人は｜「これ」を食べて」 — chỉ dùng khẳng định script có (腸と記憶の関連).
- Video mẫu: kN6wHIqYA0Q (câu hỏi → tôn vinh → 'nhưng' → người thọ ăn đồ thường → hứa N món giấu tên)

#### Tập ep07 — 認知機能の低下で見られることがある5つの変化
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep07-monowasure-sign` · mới có script.txt (B3/B3Q/B3F), chưa có giọng · ưu tiên thấp (Chưa có giọng — sửa trong script, không tốn TTS lại; làm trước khi chạy B4.)
- Mốc: chốt 36 · giới thiệu — · hứa — (est (318.6 chữ/phút, chưa có giọng); lời hứa 5 mục ~140s)
- Thumbnail: — — —
- Tiêu đề↔hook: P — 変化 ~104s, 認知機能 lần đầu ~352s (ước tính); hook dùng 'あの病気' thay vì từ tiêu đề. · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「認知機能」 — từ đầu tiêu đề, lần đầu ~352s (ước tính), không có trong 90s.
- Vấn đề: 0–21s chào + khen (~21s ước tính).
- Vấn đề: ~27–36s cảnh quên (冷蔵庫の前で目的を忘れ) tốt nhưng đứng sau lời chào.
- Vấn đề: ~63–107s khối 119 (~44s ước tính: đột quỵ, sảng, uống quá liều thuốc).
- Vấn đề: ~171–210s đọc trước 5 mục, lộ 第一位 「しまい忘れた財布を、誰かに盗られたと疑ってしまう」 — câu gây sốc nhất tập bị bán trước ở 203s thay vì làm hook.
- Vấn đề: ~147s + ~155s hai câu rào 'thứ tự chỉ vì tiện kể', 'không phải độ nặng'.
- Vấn đề: Tiêu đề 22 chữ, rào 'ことがある', không tuổi.
- **Sửa:** Trước khi làm giọng: xoá dòng タイトル + lời chào; giây 0 = 「冷蔵庫の前で目的を忘れ、名前が喉まで出かかっても出てこない。」.
- **Sửa:** ~10–25s: câu lật theo H30 từ đoạn ~125s đã có: 「おかずの一品を忘れても、後で思い出せるなら加齢による変化です。しかし…」 — đây chính là câu phân biệt mà người xem muốn nghe.
- **Sửa:** Giữ 第一位 (財布を盗られたと疑う) làm câu nhử không nêu nội dung: 「第一位は、ご家族が一番見逃しやすく、ご本人は決して認めないサインです。」 (H34).
- **Sửa:** Khối 119 → 1 câu; phần đầy đủ trước mục có liên quan.
- **Sửa:** Tiêu đề: 「70代の方へ：物忘れと認知症の境目がわかる5つの変化——第一位はご家族が最初に気づきます」.
- Video mẫu: 66ADns1W2mA (triệu chứng → 'đừng đổ cho tuổi' → hậu quả → hứa N)

#### Tập ep08 — 自立して暮らす百寿者の食事で見られた五つの傾向
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep08-hyakusaisha-shuukan` · mới có script.txt (B3/B3Q/B3F), chưa có giọng · ưu tiên cao (Clone trực tiếp đề tài video #2 kênh mẫu nhưng câu chốt chậm 5 lần và có ~2 phút rào trước mục đầu; chưa làm giọng nên sửa bây giờ không tốn TTS.)
- Mốc: chốt 116 · giới thiệu — · hứa — (est (318.6 chữ/phút, chưa có giọng); lời hứa 5 mục ~239s)
- Thumbnail: — — —
- Tiêu đề↔hook: P — 百歳 ~89s, 普通の食品 ~118s, 傾向 ~239s, 百寿者 chỉ 1 lần ~680s (ước tính). · Thumb↔tiêu đề: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM'). · Thumb↔hook: — — Chưa có thumbnail: không có file ảnh nào trong thư mục tập (SOP_LANE_E §1b: cột E/F/G TITLE-DESCRIPTION/TAGS/THUMBNAIL 'TẠM THỜI CHƯA LÀM').
- ⚠ Lời hứa không giữ: 「百寿者」 — 1 lần trong script, ~680s.
- ⚠ Lời hứa không giữ: 「五つの傾向」 — lời hứa ~239s, mục đầu ~256s (ước tính); không có trong 90s.
- Vấn đề: 0–23s hai câu tôn vinh liền nhau (~23s) trước khi nói gì về người xem.
- Vấn đề: ~42–61s khuyên đi bác sĩ, ~137–167s rào điều tra, ~167–239s khối 119 (~70s) — tổng ~2 phút rào/cảnh báo trước mục đầu.
- Vấn đề: Câu chốt ~116s 「百歳を超えて元気な方々の食卓には、高価な食品や輸入食材ではなく、日本人におなじみの普通の食品」 — kN6wHIqYA0Q (cùng đề tài, 71.922 view) nói gần nguyên câu này ở 21.8s (mốc thật). Chậm ~5 lần.
- Vấn đề: Mốc số liệu mạnh (キューサイ 2019, 100 người, 900 bữa ~89s) nằm sau 1,5 phút.
- Vấn đề: ~249s rào 'thứ tự chỉ vì tiện kể'; ~256s đọc trước 5 mục.
- Vấn đề: Tiêu đề 23 chữ, rào 'で見られた', '傾向' trừu tượng; kN6wHIqYA0Q cùng đề tài dùng '9つの食習慣——ほとんどの方がご存知ない'.
- **Sửa:** Theo đúng khung kN6wHIqYA0Q 0–68s: giây 0 hỏi bữa ăn hôm nay (1 câu), ~10s tôn vinh + 'nhưng hôm nay', ~20s câu 116s (không phải đồ đắt mà đồ thường), ~40s キューサイ 100人・900食 (đang ở 89s), ~55s hứa 5 thói quen giấu tên.
- **Sửa:** Gộp 42–61s + 137–167s + khối 119 thành 1–2 câu trong hook; phần đầy đủ trước mục có hành động.
- **Sửa:** Tiêu đề: 「70歳以上の方へ：自立して暮らす百歳の方々が毎日続けていた5つの食習慣——高価な食品はありませんでした」 (≈50 chữ).
- **Sửa:** Thumbnail: ảnh món giữa danh sách (vd 旬の野菜 = 四つ目): 「100歳まで自立｜毎日食べていた｜この食品｜高い物ではない」 — khuôn kN6wHIqYA0Q.
- Video mẫu: kN6wHIqYA0Q

### Nguyên tắc
- **Giây 0 là cơ thể/thói quen của người xem — không chào, không cảm ơn.** — cơ chế: Khán giả 60+ tự nhận ra triệu chứng của mình (đi tiểu đêm, chân nặng, ăn sáng) nên ở lại để nghe tiếp về chính mình; lời chào không chứa thông tin nên là chỗ bấm thoát. · bằng chứng: 6/6 video top mở bằng triệu chứng/thói quen (JCyxahsO0ew 0.1s 「夜中に2°3°と目が覚めて」; kN6wHIqYA0Q 0.2s 「今朝も朝食をきちんと召し上がった方は」); 0/6 mở bằng chào. Của mình: 7/8 tập mở bằng chào/cảm ơn/tôn vinh (ep01 7.5s, ep03 7.5–24.9s, ep04 5.9s, ep05 0.5–12s, ep06 0.3–8s, ep07 0–21s ước tính, ep08 0–23s ước tính). · vì sao: Mỗi giây chào là một giây người xem chưa có lý do ở lại; kênh mẫu dành giây đó cho câu có triệu chứng. · áp dụng: hook_stage/QC: cấm câu đầu chứa こんにちは/こんばんは/感謝/ありがとう/敬意. Câu tôn vinh (DNA kênh) chỉ được đặt sau câu hỏi/triệu chứng, tối đa 1 câu (H31).
- **Câu chốt lật nguyên nhân phải có trước ~40s.** — cơ chế: Triệu chứng chỉ gây đồng cảm; câu 'nguyên nhân không phải chỗ bạn nghĩ' mới tạo câu hỏi cụ thể cho cả video (vì sao lại là bắp chân? món thường là món gì?). · bằng chứng: Mốc thật: JCyxahsO0ew 37.0s, kN6wHIqYA0Q 21.8s; 4 video ước tính 0–43s. Của mình: ep03 72.4s, ep04 83.9s, ep05 72.8s (cùng câu JCyxahsO0ew nói ở 37s), ep08 ~116s (cùng câu kN6wHIqYA0Q nói ở 21.8s). · vì sao: Hai video view/ngày cao nhất có câu chốt sớm nhất; tập của mình clone đúng đề tài của chúng nhưng nói câu chốt chậm 2–5 lần. · áp dụng: Mỗi script: đánh dấu câu chốt H30; gate đo vị trí ký tự của câu đó ≤ 40s × 318,6/60 ≈ 210 chữ (không tính tiêu đề).
- **Giấu tên các mục; không đọc trước danh sách; mục 1 chỉ được nhử.** — cơ chế: Tên món chưa biết là lý do xem tiếp; đọc trước 5 mục trả lời luôn câu hỏi của thumbnail/tiêu đề, người xem có thể rời đi với đáp án. · bằng chứng: 6/6 video top không nêu tên món nào trong 120s; mục đầu đếm ngược ở 329–410s. Của mình: 8/8 tập đọc trước cả 5 mục trước mục đầu (ep02 lộ 第一位 指輪っかテスト ở 108.4s; ep07 lộ 'nghi bị trộm ví' ~203s). 6/8 tập còn thêm câu 'thứ tự không phải mức độ' (ep01, ep02, ep06, ep07, ep08 ở phần mở; ep03 ở cuối video). · vì sao: Đếm ngược chỉ có lực khi người xem không biết 第一位 là gì. · áp dụng: Xoá đoạn 'あらかじめご案内' và câu 'thứ tự chỉ vì tiện kể'; thay bằng 1 câu H34 sau lời hứa N. Mô tả video được phép liệt kê đáp án (kênh mẫu làm 6/6).
- **Tiêu đề, thumbnail, hook phải cùng một lời hứa; thumbnail chỉ khác ở chỗ thu còn 1 món.** — cơ chế: Người bấm theo tiêu đề/thumbnail cần nghe lại đúng lời hứa đó trong 30–60s đầu; lệch thì họ nghĩ bấm nhầm. · bằng chứng: YZNmQJxGuRc: tiêu đề '4 món hại' / thumbnail '1 món tốt, 11 lần trứng' / hook 'top 10 món tốt' (L/L/P) → 736 view/ngày, like 3,6%; JCyxahsO0ew và kN6wHIqYA0Q K/K/K → 3.064 và 3.425 view/ngày, like 7,1% và 5,0%. Của mình: ep03 筋肉 lần đầu 180.9s, ep04 糖尿病 186.3s, ep05 むくみ 151.8s, ep06 60歳/抗炎症/ご存知ない 0 lần trong script. · vì sao: Lệch lời hứa là nguyên nhân rõ nhất trong 6 video top để giải thích video thấp nhất; đề tài không giải thích được (cùng đề tài với video 2.513/ngày). · áp dụng: Trước khi khoá tiêu đề: grep từng từ khoá tiêu đề trong script, lần đầu phải ≤ 90s; mọi khẳng định trên thumbnail phải có nguyên văn trong script (kênh mẫu vi phạm ở 2/6 — mình không chép thói đó).
- **Tiêu đề theo khuôn: đối tượng tuổi/nhãn cảnh báo + N + động từ khẳng định, 35–55 chữ, không rào.** — cơ chế: Tiền tố '70歳以上の方へ' / 'ご注意ください' lọc đúng người xem trên trang chủ; động từ khẳng định (防いでいた, 削り続けています) tạo lời hứa; từ rào (かもしれない, 検討したい, ことがある) xoá lời hứa. · bằng chứng: 9/9 tiêu đề kênh mẫu mở bằng đối tượng hoặc nhãn cảnh báo; 0/9 rào; 6/6 video top 37–51 chữ. Của mình: 1/8 có đối tượng tuổi (ep06), 4/8 rào (ep01 かもしれない, ep05 検討したい, ep07 ことがある, ep08 見られた), 7/8 ngắn 20–31 chữ. · vì sao: Lane y khoa cần cẩn trọng nhưng sự cẩn trọng thuộc về lời trong video (miễn trừ, nguồn), không cần nằm trong tiêu đề — kênh mẫu đặt miễn trừ trong mô tả. · áp dụng: Tiêu đề khẳng định điều script THẬT SỰ nói (vd '…続けていた5つの食習慣'), không khẳng định chữa bệnh; gate title_len [35,55] đang có — áp cho cả dòng タイトル trong script.
- **Khối cảnh báo cấp cứu không được chiếm hook: 1 câu trong hook, phần đầy đủ đặt ngay trước hành động rủi ro.** — cơ chế: 58 giây hướng dẫn 119/AED trong 2 phút đầu đẩy câu chốt ra sau 70s và đổi giọng video từ 'bí mật sức khoẻ' sang 'thủ tục an toàn'. · bằng chứng: Kênh mẫu 0/6 có khối cấp cứu trong 120s (JCyxahsO0ew chỉ 1 câu miễn trừ ~12s ở 110s). Của mình 5/8 có trong 120s: ep01 56.7–114.5s (58s), ep03 24.9–72s (47s), ep04 29.8–77.8s (48s), ep06 81–98s (17s), ep07 ~63–107s (~44s ước tính); ep08 ~167–239s. · vì sao: lane_rules của profile chỉ yêu cầu cảnh báo đứng TRƯỚC hoặc CÙNG lúc hành động rủi ro — không bắt buộc ở giây đầu; dời xuống vẫn đúng luật mà trả lại 40–58s cho hook. · áp dụng: script_qc/hook_stage: đo số chữ của đoạn chứa 一一九/119/救急車/AED trong 120s đầu — tối đa 1 câu (~60 chữ); đoạn đầy đủ gắn vào mục đầu có hành động.
- **Thumbnail lấy 1 món GIỮA danh sách, giấu tên bằng đại từ, không lấy 第1位.** — cơ chế: Người bấm vì 'この食品' được trả lời giữa video (giữ họ qua nửa đầu), còn 第1位 vẫn là bí mật cho nửa sau. · bằng chứng: ごぼう = 第8位 (kN6wHIqYA0Q), trứng = 第5位 (66ADns1W2mA), きなこ = 第5位 (YZNmQJxGuRc), かつお節 = món 3/3 (4Q0fF3Ud57Q): 0/4 là 第1位; 9/9 không ghi tên món bằng chữ. · vì sao: Tách 2 móc tò mò (thumbnail và 第1位) thay vì dùng chung một. · áp dụng: B7 thumbnail: chọn món/dấu hiệu 第四位–第二位 làm ảnh; chữ 4 dòng cam/trắng/đỏ/xanh theo khuôn '{tuổi}から｜{nhóm người/triệu chứng}｜「これ」/この食品｜{lợi ích có trong script}'.

### Lưu ý dữ liệu
- Mốc giây có thật chỉ cho JCyxahsO0ew và kN6wHIqYA0Q (raw hook_segments, api+proxy2). 66ADns1W2mA, 4Q0fF3Ud57Q, 966fNPIqSi4, YZNmQJxGuRc: raw rỗng lúc audit (đã mở lại raw trước khi ghi file — vẫn rỗng) → mốc ƯỚC TÍNH = vị trí ký tự ÷ (len(transcript)/duration) từ E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\ikiiki-kenko\_raw\transcripts.json. Kiểm chéo trên JCyxahsO0ew: câu '65歳' thật 14.4s, ước tính ~15.5s (lệch ~1s).
- 3 video 'new' (9B8uVZDg1ZA, Hlkpj3AkUPY, 2YaaL5KS3-k) không có trong transcripts.json và raw rỗng → không lấy được transcript; chỉ phân tích tiêu đề/mô tả/thumbnail; KHÔNG ghi vào seed file (seed chỉ 6 bản ghi có hook).
- Transcript là ASR: 暴行=膀胱, ふハぎ=ふくらはぎ, ネタ切り=寝たきり, こう霊社=高齢者, 大空くらい=第9位, 地の食品=9つの食品… Trích dẫn giữ nguyên ASR, chỗ sửa đặt trong [=…].
- Tập của mình: KHÔNG có thumbnail, title-description hay DANG-TAI.txt ở cả 8 tập (SOP_LANE_E §1b: cột E/F/G 'tạm thời chưa làm'); tiêu đề lấy từ dòng 'タイトル' trong script.txt (ep06 từ title.txt). Mọi chấm thumbnail của mình = '—'.
- voice.srt của ep01–ep06 có cùng giờ tạo với voice.mp3 → mốc thật. voice.stt.srt của ep01/ep03/ep05 CŨ hơn voice.mp3 (không dùng). ep05 script.txt sửa 14:48 sau voice 14:43 → voice hiện tại có thể lệch script vài câu.
- Chấm 'tự giới thiệu' (intro_t): narrator của lane KHÔNG tự xưng bác sĩ (profile + lane_rules) nên intro_t của mình luôn null — đây là chủ ý an toàn, KHÔNG khuyên sửa. Kênh mẫu tự nhận kinh nghiệm y khoa không kiểm chứng được.
- Kênh mẫu có 2/6 thumbnail với khẳng định không có trong lời — không đưa vào công thức để chép.

---

## 老後の暮らし研究所 → lane `teinengo-real`

Kênh: https://www.youtube.com/channel/UCRkP44Mcw-K8IktdTqxC9dg

Kênh mẫu = truyện manga ngôi 1「俺」về 1 quyết định tiền hưu. Khuôn thắng (4 video ≥100k): câu 0–30s nói lại TIỀN ĐỀ của tiêu đề (câu hỏi 2 lựa chọn, hoặc con số + nghịch lý) → tự giới thiệu tên-tuổi-nghề → niềm tin 'ずっとそう思っていた' → 'だが' + con số/phong bì → giọng thứ hai (đồng nghiệp/vợ/người lạ) vào trước ~100s. Tiêu đề = 【漫画】+tuổi+quyết định+…+mốc thời gian+cảm xúc, KHÔNG cần số tiền. Thumbnail = dải đen chữ vàng/trắng (chủ đề 4–9 chữ, không chép tiêu đề) + 2 panel + bong bóng nội tâm ≤5 chữ + nhãn vàng. Mô tả = câu hỏi/「〜とは――」+ tóm truyện có tuổi-tên-số + '最後までご覧ください' + 関連動画 + #年金 #老後 #老後資金.

### Khung hook theo giây
- **0–5s · Tiền đề của tiêu đề** — Câu đầu là câu hỏi 2 lựa chọn HOẶC con số lớn + hành vi trái với nó. 5/7 transcript mở bằng tiền đề/con số của tiêu đề (XbwqD, K8t, O84, _VX, _fJ ở 11s). Ví dụ: 「60歳でやめた俺と65歳まで残った同僚 どっちが幸せだったのか。 / 退職金2500万円。それでも俺はスーパーで100円の惣菜を手に取っては棚に戻していた。」 (XbwqD2SktC0 (0.3s) / K8tTrxijqEo (0s))
- **8–25s · Tự giới thiệu 1 câu** — 「俺の名前は＋tên＋tuổi＋nghề cũ」. 5/7 trong ≤25s (XbwqD 8s, _VX ~8s, dY3 ~10s, K8t ~23s, _fJ 0s); O84 ~78s, EANAD ~45s. Không phân biệt thắng/thua. Ví dụ: 「俺の名前は宮本浩司66歳元郵便局だ。」 (XbwqD2SktC0 (8.1s))
- **10–70s · Niềm tin sắp vỡ** — 'ずっとそう思っていた/思っていた/はずだ' — 9/9 transcript (7 video chọn + 2 video thấp bổ sung) có trong 120s. Ví dụ: 「だから老後は何とかなる。ずっとそう思っていた。」 (O84L0zOtrxo (~17s))
- **25–100s · Cú lật bằng con số/phong bì** — 'だが' + số cụ thể hoặc thư. 5/7 transcript có con số tiền trong 120s (XbwqD 87s, O84 4–30s, K8t 0s, dY3 64–98s, _fJ 11s). Ví dụ: 「去年の今頃通帳には920万円あった。1年で67万円減っている。」 (O84L0zOtrxo (~26–30s))
- **50–120s · Câu khoá = câu hỏi của cả video** — Nói ra thứ người xem sẽ chờ tới cuối: cả 2 bên đều trả giá (K11), số của tiêu đề thành bí ẩn (K02), N điều (K09). Ví dụ: 「自由を選んだ俺にも地獄があり、安定を選んだアイにも後悔があったからだ。…答えは思っていたより残酷だった。」 (XbwqD2SktC0 (62.8–80.2s))
- **85–105s · Giọng thứ hai** — Vợ/đồng nghiệp/người lạ nói 1 câu làm lung lay nhân vật. 4/4 video ≥100k có trong ~100s (XbwqD 同僚 37s, _VX 妻 ~87s, O84 藤原 ~100s, K8t 常連 ~102s); 0/2 video 50–72k (EANAD, dY3) có. Ví dụ: 「老後破綻する人にはな、決まって同じ金の使い方がある。」 (K8tTrxijqEo (~102s))
- **80–130s · Trăng mật hưu trí (SAU câu khoá)** — Liệt kê tự do (目覚まし・平日の映画館・昼ビール) đặt SAU câu khoá ở video thắng (XbwqD 82–121s); ở EANAD nó chiếm 0–126s và thay luôn hook. Ví dụ: 「平日の映画館は驚くほど空いていて、これが定年後の特権かと思った。」 (XbwqD2SktC0 (~121s))

- Tiêu đề: 【漫画】＋[tuổi NN歳 / trạng thái]＋[quyết định: 定年退職した男/年金を受け取った男/辞めるな]＋'…'＋[mốc: 5年後/2年後/2か月/その先]＋[kết: 絶望しました/衝撃の現実/本当の理由/末路/最強な理由]. Đếm: 【漫画】9/9; có tuổi 8/9 (trừ iJr; K8t dùng '50代後半'); '…' 8/9 (_VX dùng '！'); mốc thời gian 5/9 (top6: 4/6); SỐ TIỀN chỉ 3/9 và chỉ 1/6 top (O84 67万円) — trong khi 3/5 video còn lại có tiền (_fJ 2000万, iJr 478万/18万, và e_Zo7 1700万 ngoài mẫu). Dài 27–41 ký tự ở 6 top; video dài nhất 49 (_fJ) là 1 trong các video thấp.
- Thumbnail: Dải đen trên cùng, 1 dòng 4–9 chữ: từ khoá màu vàng (hoặc đỏ) + phần còn lại màu trắng — là CHỦ ĐỀ, không chép tiêu đề (8/9 có dải này; iJr thay bằng cột dọc giữa). Dưới: 2 panel trái/phải (8/9; iJr 4 ô), mỗi panel 1 ông già Nhật vẽ bán thực, bong bóng oval trắng chữ dọc = câu nội tâm ≤5 chữ (「もう自由だ」「話が違う…」「安いから…」「一杯だけ」) 9/9, nhãn vàng viền đen ở đáy = tuổi/lựa chọn/mốc thời gian 9/9. Ba biến thể: trước-sau cảm xúc (trái cười, phải khóc/thất thần) 4/9 (_VX, EANAD, dY3, Zog); 2 lựa chọn song song 1/9 (XbwqD); xếp hạng 第3位/第2位 3/9 (K8t, O84, _fJ). Nhãn mốc thời gian '2か月後…/数年後…/1年後…' 3/9. Không có số tiền/phần trăm 7/9 (chỉ Zog '年金24%減', iJr '月6万…').
- Mô tả: Dòng 1 = câu hỏi hoặc「〜とは――。」(4/9: O84, _VX, EANAD, dY3) hoặc câu phá định kiến/giới thiệu chủ đề; rồi tóm truyện có tuổi nhân vật (8/9; XbwqD không có nhân vật) kèm số tiền spoil (退職金2500万円, 貯金853万円, 年金13万円…); chuỗi ≥4 từ khoá ngăn bằng '、' 4/9; 'ぜひ最後までご覧ください' 5/9; hỏi khán giả 'あなたなら…？コメントで' 3/9; '関連動画↓' + link 8/9 (dY3 không); hashtag '#年金 #老後 #老後資金' 9/9 y hệt.
- 4 phần nối nhau: Tiêu đề đặt TIỀN ĐỀ (ai, tuổi, quyết định, mốc thời gian) → thumbnail không lặp tiêu đề mà cho 2 cảm xúc/2 lựa chọn bằng câu nội tâm → hook 0–30s nói lại tiền đề đó bằng lời nhân vật (XbwqD 0.3s, K8t 0s, O84 30s, _fJ 11s) → mô tả spoil con số + gợi câu hỏi để comment. Chỗ nối yếu nhất của kênh là thumbnail↔hook: 2/7 video có transcript lệch (O84 'P': xếp hạng không có trong video; _fJ 'L').
- Số đếm: {'videos_chon': 9, 'co_transcript': 7, 'transcript_moc_that': 2, 'transcript_uoc_tinh': 5, 'khong_transcript': 2, 'mo_bang_tien_de_tieu_de_trong_30s': '5/7 (XbwqD, K8t, O84, _VX, _fJ)', 'niem_tin_思っていた_trong_120s': '9/9 (7 chọn + e_Zo7Ht5OH8 79s + WblFD81yjOI 49s)', 'giong_thu_hai_truoc_105s': '4/4 video ≥100k · 0/2 video 50–72k', 'tu_gioi_thieu_truoc_25s': '5/7', 'tieu_de_co_so_tien': '1/6 top · 3/9 tổng', 'tieu_de_co_tuoi': '8/9', 'thumbnail_2_panel': '8/9', 'thumbnail_khong_so_tien': '7/9', 'thumbnail_xep_hang': '3/9', 'hashtag_giong_het': '9/9'}
- Ngoại lệ: ["O84L0zOtrxo 174k dù thumbnail hứa bảng xếp hạng 第3位/第2位 mà transcript không có '第N位' nào — lệch thumbnail không giết video khi tiêu đề + hook khớp.", "_VXUim2J9QM 109k dù '62歳' (vế chính tiêu đề) mãi ~391s mới xuất hiện — tiêu đề mệnh lệnh「60歳で辞めるな！」tự kéo click, hook chỉ cần khớp vế đầu.", "O84L0zOtrxo tự giới thiệu ~78s (muộn nhất) vẫn 174k — thời điểm '俺の名前は' không quyết định.", 'iJrKlKBAabY phá cả khuôn tiêu đề (không nhân vật/cảm xúc) lẫn thumbnail (4 ô) — 8,4k sau 5 ngày, chưa đủ tuổi để kết luận.']

Thắng vs thua: TOP ≥100k (XbwqD 313k, K8t 184k, O84 174k, _VX 109k) vs GIỮA (EANAD 72k, dY3 50k) vs THẤP đã đủ tuổi (e_Zo7Ht5OH8 ~10–11k, WblFD81yjOI 10k — cả hai đã được link trong mô tả XbwqD ngày 2026-08-03 nên ≥7 tuần tuổi; chỉ có transcript, KHÔNG có thumbnail/raw) vs MỚI (_fJ 10k@14 ngày, iJr 8,4k@5 ngày, Zog ~0@0 ngày). (1) KHÁC Ở ĐỀ TÀI trước hết: 2 video thấp có hook ĐỦ khuôn — e_Zo7 mở「俺は部長だぞ」0s, tự giới thiệu 8s, 'そう思っていた' 79s, phong bì 119s; WblFD mở「あと1年我慢すれば俺の勝ちだ」0s, tự giới thiệu 3s, con số 15万3000→21万7000 ở 26s, phong bì 大家 ~111–121s — vẫn chỉ 10k. Tiền đề của chúng hẹp (cựu 部長 từ chối 再雇用; độc thân thuê nhà hoãn lương hưu tới 70), còn 4 top là quyết định/nỗi sợ gần như ai 58–67 cũng có (nghỉ 60 hay 65; tiền tự hao dù không tiêu gì lớn; cách tiêu làm nghèo). (2) KHÁC Ở HOOK thứ hai, trong nhóm cùng đề tài rộng: 2 video giữa (EANAD, dY3 — đều 独身) dành 0–58s/0–126s cho tự do trước khi có con số/câu hỏi, không có giọng thứ hai trong 120s; 4 top đều có câu hỏi/con số ≤30s và giọng thứ hai ≤~102s. (3) GÓI ĐĂNG: số tiền trên tiêu đề 1/6 top vs 3/5 video còn lại; tiêu đề hứa LIST mà hook kể TRUYỆN (_fJ, thumbnail 'L') ra 10k dù dùng lại khuôn thumbnail của K8t 184k. (4) NHIỄU THỜI ĐIỂM: 6 top đăng 06-25→08-26, 3 video tháng 9 đều thấp — có thể kênh mất đà đề xuất; không tách được bằng dữ liệu hiện có.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 312,820 | 0.32 | 58.48 | 8.12 | 70.16 | H18 H08 K11 K06 | 10 | K | P | K | 【漫画】60歳で定年退職した男…5年後、65歳まで働いた同僚との差に絶望しました |
| top | 184,212 | 0 | 73 | 24 | 115 | H04 H17 K07 K09 | 11 | K | K | K | 【漫画】50代後半から要注意…老後破産する人がやっている貧乏になるお金の使い方6選 |
| top | 174,239 | 26 | 46 | 78 | — | H03 H15 K02 | 10 | K | P | P | 【漫画】65歳で定年退職した男…2年後、貯金が67万円消えた本当の理由を知りました |
| top | 109,004 | 0 | 99 | 9 | — | H21 K01 K06 | 8 | P | K | P | 【漫画】60歳で辞めるな！62歳で年金受給が最強な理由 |
| top | 72,196 | 0 | 114 | 45 | — | H35 K06 | 7 | P | P | K | 【漫画】65歳で退職した独身男…たった2か月で絶望しました |
| top | 50,615 | 0 | 117 | 10 | — | H15 K01 | 9 | K | K | K | 【漫画】65歳、独身、年金生活…その先に待っていた衝撃の現実 |
| new | 12 | — | — | — | — |  | — | N/A | P | N/A | 【漫画】60歳で年金を受け取った男…65歳まで待たなかった15年後の末路 |
| new | 8,435 | — | — | — | — |  | — | N/A | P | N/A | 【漫画】年収別のリアルな年金生活。日本人の平均年収478万円…年金は平均約18万円 |
| new | 10,398 | 11.24 | 19.84 | 0.24 | — | H12 H04 K02 K04 | 6 | P | K | L | 【漫画】60歳を過ぎたら絶対に行ってはいけない場所5選…退職金2000万円を失った67歳男性の末路 |

#### 【漫画】60歳で定年退職した男…5年後、65歳まで働いた同僚との差に絶望しました — https://www.youtube.com/watch?v=XbwqD2SktC0
- Câu chốt (0.32s): 「60歳でやめた俺と65歳まで残った同僚 どっちが幸せだったのか。」
- Câu khoá (58.48s): 「だが、今俺は簡単にそう言えなくなった。自由を選んだ俺にも地獄があり、安定を選んだアイにも後悔があったからだ。60歳でやめるのが正解か、65歳まで働くのが正解か。答えは思っていたより残酷だった。」
- Chữ thumbnail: [dải đen trên] 65歳(vàng)で定年退職(trắng) · [panel trái, nhà kho, người trẻ chỉ tay vào ông già cầm bảng kẹp] bong bóng「年下上司」「給料激減」 nhãn vàng「65歳まで働く」 · [panel phải, ôm hoa, đồng nghiệp vỗ tay] bong bóng「もう自由だ」 nhãn vàng「60歳で退職」 · Mô tả: 今回は「60歳で定年退職する人」と「65歳近くまで働く人」、どちらが幸せな老後を送れるのかを漫画形式で分かりやすく解説します。
- Hook↔tiêu đề: K — Câu 0.3s lặp đúng cặp 60歳 vs 65歳 của tiêu đề; '5年後' khớp tuổi 66 ở 8s (60+5). · Thumb↔tiêu đề: P — Dải đầu ghi「65歳で定年退職」ngược tiêu đề「60歳で定年退職した男」; chỉ 2 nhãn dưới mới đủ cặp 60/65. · Thumb↔hook: K — Hai panel = đúng 2 lựa chọn hook đặt ra; 「年下上司」có trong hook (29.3s「年下の上司」); riêng「給料激減」chưa có trong 120s (給料 lần đầu ~211s).
- Vì sao giữ người: H18 đặt câu hỏi của tiêu đề ngay giây 0 nên người bấm vào nghe đúng thứ mình tò mò; K11 ở 62.8s phá kỳ vọng 'nghỉ sớm = sướng' bằng cách nói cả 2 bên đều trả giá — người xem không đoán được bên thắng nên ở lại để cân. Đề tài là quyết định mà gần như mọi khán giả 58–65 đều đang phải chọn.
- Điểm yếu: Tiền đầu tiên mãi 87s; từ 8s tới 50s là tự giới thiệu + liệt kê lý do chán việc (không có cảnh). Thumbnail ghi 65歳 trên dải đầu trái với tiêu đề 60歳.

#### 【漫画】50代後半から要注意…老後破産する人がやっている貧乏になるお金の使い方6選 — https://www.youtube.com/watch?v=K8tTrxijqEo
- Câu chốt (0s): 「退職金2500万円。それでも俺はスーパーで100円の惣菜を手に取っては棚に戻していた。」
- Câu khoá (73s): 「酒もギャンブルもしていない。投資で大損したわけでもない。それなのになぜこんなことになったのか。」
- Chữ thumbnail: [dải đen trên] 貧乏(đỏ)になる(trắng)お金の使い方(vàng) · [trái, quán nhậu, cười uống bia] bong bóng「華金だ」「今日くらい」 nhãn vàng「第3位」 · [phải, cửa hàng tiện lợi, mở ví] bong bóng「安いから…」 nhãn vàng「第2位」 · Mô tả: 老後破産を招くのは、ギャンブルや投資の失敗だけではありません。
- Hook↔tiêu đề: K — Tiêu đề hứa '老後破産する人…お金の使い方6選' — 102s nói gần nguyên văn「老後破綻する人…同じ金の使い方」và 115s chốt '6つ'. Riêng '50代後半から要注意' không có (nhân vật 65 tuổi). · Thumb↔tiêu đề: K — Dải đầu「貧乏になるお金の使い方」là cụm lõi của tiêu đề; 第3位/第2位 = dạng xếp hạng của '6選'. · Thumb↔hook: K — Panel bia khớp cảnh 85–99s (vào 居酒屋 uống một mình「嫌なことを忘れる」); panel「安いから…」= mục 第6位「安いから買う」ở 150s, ngay sau 120s. Chữ bong bóng「華金だ」「今日くらい」không có nguyên văn trong transcript.
- Vì sao giữ người: Nghịch lý 2 con số ở giây 0 (2500万 vs 100円) bắt người xem tự tìm lời giải; tới 102–115s một người lạ biến lời giải thành danh sách 6 mục có xếp hạng — người xem có lý do ở lại tới 第1位 (1120s). List được bọc trong truyện nên không khô.
- Điểm yếu: Là dạng LIST (6選) — SOP h2dev đã tách sang nhịp lane G; lane F chỉ học phần mở nghịch lý + người lạ, không học khung xếp hạng. '50代後半から要注意' trên tiêu đề không được hook nhắc.

#### 【漫画】65歳で定年退職した男…2年後、貯金が67万円消えた本当の理由を知りました — https://www.youtube.com/watch?v=O84L0zOtrxo
- Câu chốt (26s): 「去年の今頃通帳には920万円あった。1年で67万円減っている。」
- Câu khoá (46s): 「それなのに67万円消えている。どう考えてもおかしかった。」
- Chữ thumbnail: [dải đen trên] 老後貧乏(vàng)になる人の特徴(trắng) · [trái, quán nhậu, uống cạn cốc bia] bong bóng「一杯だけ」 nhãn vàng「第3位」 · [phải, kệ drugstore cầm chai nước giặt] bong bóng「安いから…」 nhãn vàng「第2位」 · Mô tả: 67歳で初めて気付いた「お金が減る本当の理由」とは――。
- Hook↔tiêu đề: K — Con số 67万円 của tiêu đề nói ở ~30s và lặp 3 lần tới 67s; '2年後' khớp 81s「2年前に定年退職した」; '本当の理由' = câu hỏi 46–67s. · Thumb↔tiêu đề: P — Thumbnail đổi khung sang bảng xếp hạng「老後貧乏になる人の特徴」第3位/第2位 — tiêu đề là truyện 1 người mất 67万円; con số 67万 không có trên ảnh. · Thumb↔hook: P — 「安いから…」= cảnh mua đồ 特売 ở ~155–173s (ngay sau 120s); 「一杯だけ」(quán nhậu) không có trong 120s; transcript KHÔNG có '第N位' nào — video không xếp hạng như thumbnail hứa.
- Vì sao giữ người: H03 đưa bảng cân đối 3 con số trong 12s (853万/14万6000/持ち家) khiến người xem tự so với sổ của mình, rồi K02 lật: sổ hụt 67万 mà không tiêu gì lớn — hậu quả có sẵn, nguyên nhân bị giấu (loại D). Chi tiết 580円 cà phê (58–67s) cho não một hình ảnh cụ thể của nghịch lý.
- Điểm yếu: Tự giới thiệu muộn (78s) nhưng không hại — 0–78s toàn con số và cảnh. Thumbnail hứa xếp hạng mà video không có (rủi ro comment bắt lỗi như vụ タニジン); video vẫn 174k nên lỗi này không giết view ở đây.

#### 【漫画】60歳で辞めるな！62歳で年金受給が最強な理由 — https://www.youtube.com/watch?v=_VXUim2J9QM
- Câu chốt (0s): 「60歳でやめたら家計は本当に持つのか?そう聞かれた瞬間俺は返事に詰まった。」
- Câu khoá (99s): 「少しって毎月いくらのこと?その数字を俺は1度も出していなかった。」
- Chữ thumbnail: [dải đen trên] 62歳(vàng)で年金受給(trắng) · [trái, ngả người thư giãn] bong bóng「毎日が休日」 nhãn vàng「60歳で定年」 · [phải, khóc cầm 銀行通帳] bong bóng「話が違う…」 nhãn vàng「退職金が消える」 · Mô tả: 60歳で定年退職するか、65歳まで働くか。老後資金、退職金、年金受給、再雇用、繰り上げ受給で迷う方へ。
- Hook↔tiêu đề: P — Vế '60歳で辞めるな' khớp câu hỏi 0s; vế chính '62歳で年金受給が最強' vắng cả 120s — '62歳' như một lựa chọn chỉ xuất hiện ~391s, chữ '最強' ~1224s. · Thumb↔tiêu đề: K — 62歳/60歳 đều có; panel khóc「退職金が消える」minh hoạ đúng lý do của '辞めるな'. · Thumb↔hook: P — Panel trái (mơ nghỉ, 72–78s xem 温泉宿) và nỗi sợ rút 退職金 (87–101s) có trong hook; con số 62 của dải đầu thì không.
- Vì sao giữ người: Mở bằng câu hỏi mà khán giả 59 tuổi đang tự hỏi, người hỏi là vợ (người giữ sổ) → câu hỏi có sức nặng thật; K01 biến nó thành câu hỏi của cả video. Đề tài 'nghỉ 60 hay 65' là quyết định chung → 137 comment, 768 like (cao nhất 9 video).
- Điểm yếu: Lời hứa '62歳が最強' để tới ~6,5 phút — tiêu đề mệnh lệnh「辞めるな！」mới là thứ kéo click, hook chỉ giữ bằng câu hỏi chung. 0–80s là đời công sở (共有フォルダー…), ít cảnh.

#### 【漫画】65歳で退職した独身男…たった2か月で絶望しました — https://www.youtube.com/watch?v=EANADckKWT4
- Câu chốt (0s): 「65歳になった日、俺は42年間勤めた会社を退職した。」
- Câu khoá (114s): 「誰にも縛られず自分のためだけに生きる毎日。65歳、俺の第2の人生は希望と期待に満ちた最高のスタートを切ったはずだった。」
- Chữ thumbnail: [dải đen trên] 定年後の(trắng)本当の敵(vàng) · [trái, cười ôm hoa, đồng nghiệp quay lưng] bong bóng「最高」「自由だ」 nhãn vàng「65歳で退職」 · [phải, nền tối, mặt buồn] bong bóng「虚しい…」 nhãn vàng「2か月後…」 · Mô tả: 65歳で定年退職した独身男性が、自由な老後を夢見た先で直面した「本当の孤独」とは――。
- Hook↔tiêu đề: P — 65歳・退職 có ở 0s, 独身 ở 45s; nhưng '2か月で絶望' không có dấu hiệu nào trước ~113s, chữ '2ヶ月' ở ~271s. · Thumb↔tiêu đề: P — 65歳で退職 + 2か月後 khớp; dải đầu「本当の敵」là lời hứa mới không có trong tiêu đề, còn '独身' của tiêu đề không có trên ảnh. · Thumb↔hook: K — Panel trái (hoa, 自由だ) = đúng 0–26s; panel phải (虚しい) là phần sau 120s (虚し ~426s).
- Vì sao giữ người: Chỉ sống nhờ trớ trêu kịch tính: tiêu đề/thumbnail đã nói '2 tháng sau tuyệt vọng', nên 2 phút liệt kê tự do (旅行・歴史小説・平日の映画館) được nghe như đếm ngược. Mọi thứ phụ thuộc vào gói đăng.
- Điểm yếu: 0–30s không có mâu thuẫn, không có con số, không có người thứ hai; câu khoá duy nhất là 'はずだった' ở ~2 phút. Video 72k — thấp nhất nhóm top trừ dY3, cùng kiểu mở chậm.

#### 【漫画】65歳、独身、年金生活…その先に待っていた衝撃の現実 — https://www.youtube.com/watch?v=dY3HfjtmvXI
- Câu chốt (0s): 「老後は自由だと思っていた。65歳、独身、持ち家ありだからお金の心配だけはないと思っていた。」
- Câu khoá (117s): 「年金13万円。本当にこの先も大丈夫なのだろうか。」
- Chữ thumbnail: [dải đen trên] 独身(vàng)の年金生活(trắng) · [trái, cầm mô hình tàu điện, cười] bong bóng「1人を楽しむ」「もう働かない」 nhãn vàng「65歳」 · [phải, áo rách bẩn, khóc] bong bóng「金が無い…」 nhãn vàng「数年後…」 · Mô tả: 老後は本当に自由なのでしょうか――。
- Hook↔tiêu đề: K — 65歳・独身・年金生活 đều ở 0–64s; '衝撃の現実' = phong bì 修繕積立金 gần gấp đôi ở 88–98s, còn trong 120s. · Thumb↔tiêu đề: K — Dải đầu「独身の年金生活」+ nhãn 65歳/数年後… = đúng 3 từ khoá + 'その先' của tiêu đề. · Thumb↔hook: K — Mô hình tàu điện trên tay = 45s「鉄道模型を眺める」; 「もう働かない」≈ 31s「もう早朝出勤はない」; 「金が無い…」≈ 修繕積立金 88–117s.
- Vì sao giữ người: H15 báo trước niềm tin sẽ vỡ ('思っていた' 2 lần trong 3s) nên người xem chờ cú vỡ; cú vỡ là một vật lý cụ thể — phong bì 修繕積立金 với 2 con số (1万5000→2万9000).
- Điểm yếu: Cú tát phong bì tới 88s mới đến, 0–58s là liệt kê tự do của người độc thân (giống EANAD). Tiêu đề không có con số/biến cố cụ thể ('衝撃の現実' chung chung). Đăng sớm nhất (2026-06-25) khi kênh chưa có đà — 50k.

#### 【漫画】60歳で年金を受け取った男…65歳まで待たなかった15年後の末路 — https://www.youtube.com/watch?v=ZogHjPo8cX0
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: [dải đen trên] 60歳(vàng)で年金受給(trắng) · [trái, quán nhậu có biển 焼き鳥, uống bia] bong bóng「俺は自由だ」 nhãn vàng「年金24%減」(24% đỏ) · [phải, nền mây đen, trừng mắt nhìn 預金通帳] bong bóng「話が違う…」 nhãn vàng「1年後…」 · Mô tả: 60歳から年金を受け取る「繰り上げ受給」。65歳まで待つ場合と比べて、年金はいくら減るのか？本当に後悔しない選択なのか？
- Hook↔tiêu đề: N/A — Không lấy được transcript (raw rỗng, không có trong transcripts.json) — không chấm hook. · Thumb↔tiêu đề: P — Tiêu đề hứa '15年後の末路', thumbnail ghi '1年後…'; 年金24%減 = 0,4%×60 tháng繰上げ, khớp '60歳で年金を受け取った'. · Thumb↔hook: N/A — Không có transcript.
- Vì sao giữ người: Chưa đánh giá hook. Gói đăng chép khuôn của _VXUim2J9QM (dải 'NN歳で年金受給' + bong bóng「話が違う…」+ sổ tiết kiệm).
- Điểm yếu: Đăng 2026-09-23 (12 view lúc tải) — quá mới để kết luận. ĐÂY LÀ CÙNG ĐỀ TÀI 繰上げ với tập ep03 của mình.

#### 【漫画】年収別のリアルな年金生活。日本人の平均年収478万円…年金は平均約18万円 — https://www.youtube.com/watch?v=iJrKlKBAabY
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: [cột giữa dọc] 年収別(đỏ)の年金生活(vàng) · 4 ô: 年収300万円 bong bóng「月6万」(ông già làm siêu thị) · 年収500万円「月15万」(ăn mì ly) · 年収750万円「月18万」(sân golf) · 年収1100万円「月25万」(nhà hàng rượu vang) · Mô tả: 現役時代の年収1100万円、750万円、500万円、300万円。収入が大きく違う4人が老後を迎えたとき、意外な「お金の差」が生まれていました。
- Hook↔tiêu đề: N/A — Không lấy được transcript — không chấm hook. · Thumb↔tiêu đề: P — Cùng chủ đề 年収別 nhưng số lệch: tiêu đề '平均年収478万円…年金は平均約18万円', thumbnail lại gắn 月18万 cho 年収750万円 và 月15万 cho 年収500万円. · Thumb↔hook: N/A — Không có transcript.
- Vì sao giữ người: Chưa đánh giá hook. Là video DUY NHẤT trong 9 phá khuôn: tiêu đề không có nhân vật/tuổi/cảm xúc, thumbnail 4 ô thay vì 2 panel.
- Điểm yếu: 8.435 view sau 5 ngày (2026-09-18) — thấp hơn mọi video top cùng tuổi nhưng còn quá mới; ghi nhận là 'phá khuôn + view thấp', chưa đủ để kết luận nhân quả.

#### 【漫画】60歳を過ぎたら絶対に行ってはいけない場所5選…退職金2000万円を失った67歳男性の末路 — https://www.youtube.com/watch?v=_fJim8rkhhM
- Câu chốt (11.24s): 「元管理職で2000万円もの退職金をもらった俺がどうして今お金に困っているのか。」
- Câu khoá (19.84s): 「話は1年前に遡る。」
- Chữ thumbnail: [dải đen trên] 60歳(vàng)過ぎて(trắng)絶対行くな(đỏ) · [trái, quán nhậu, vest] bong bóng「一杯だけ」 nhãn vàng「第3位」 · [phải, trường đua ngựa cầm vé] bong bóng「勝てば十倍」 nhãn vàng「第2位」 · Mô tả: 「60代が絶対に行ってはいけない場所5選」をご紹介します。
- Hook↔tiêu đề: P — Vế sau tiêu đề (退職金2000万円・67歳・末路) có đủ ở 0–14s; vế chính '行ってはいけない場所5選' không xuất hiện trong 120s — không có lời hứa danh sách, không nơi nào được gọi tên. · Thumb↔tiêu đề: K — 「60歳過ぎて絶対行くな」= rút gọn vế đầu tiêu đề; 第3位/第2位 = '5選'. · Thumb↔hook: L — Quán nhậu, trường đua, xếp hạng — không cái nào có trong 120s; 120s đầu là chuyện rảnh rỗi sau nghỉ hưu.
- Vì sao giữ người: Nghịch lý 2000万 vs giao báo ở 11s là câu chốt tốt, K04 quay về 1 năm trước đúng khuôn. Nhưng người bấm vì thumbnail/tiêu đề '5 nơi không được đến' sẽ không nghe thấy danh sách nào trong 2 phút.
- Điểm yếu: Mở bằng tự giới thiệu (H12 — h2dev cấm). Tiêu đề 49 ký tự (dài nhất, vượt gate 44). Gói đăng hứa LIST, hook là TRUYỆN: 10k sau 14 ngày dù dùng lại khuôn thumbnail của K8tTrxijqEo (184k).

### Các tập của mình

3/3 tập mới xong kịch bản (LOCK), 0/3 có giọng, 0/3 có TIEU_DE_MO_TA.txt, 0/3 có thumbnail; ep01 còn thiếu cả title.txt (tựa làm việc nằm ở dòng 1 series_ctx.txt) → cột thumb_title/thumb_hook không chấm được ở cả 3 tập. Hook↔tiêu đề: ep03 K, ep02 P, ep01 L. 3/3 tập mở bằng cùng khung 'A した俺と、B した同期/日高 + どっちが/答え' — khung của ĐÚNG 1 video kênh mẫu (XbwqD), trong khi 7 transcript kênh mẫu dùng 7 kiểu mở khác nhau (H18, H03, H04, H21, H35, H15, H12); ep01 gần như chép nguyên câu. Giọng thứ hai trong 120s: ep02 có (日高「俺は課長だぞ」46s), ep01 (千恵子 91s) có, ep03 không (thoại đầu 158s). Tiền đầu tiên: ep03 5s, ep01 100s, ep02 106s. Tự giới thiệu 14–17s (đạt, kênh mẫu 5/7 trong ≤25s). Lặp chéo giữa các tập: tên 日高 2/3, '段ボール工場' 2/3, tên '修一' 2/3, '手札' 3/3 (97–106s), cảnh 目覚まし+映画館客N人+ビール 2/3 — khán giả xem liền nhiều tập sẽ nhận ra. Ưu tiên: ep01 cao, ep02 vừa, ep03 vừa (vì va chạm đề tài với ZogHjPo8cX0 đăng 2026-09-23).

#### Tập ep01 — 【漫画】60歳で退職した俺と働き続けた妻…5年後、夫婦の月収に8万円の差が出た理由 (tựa LÀM VIỆC lấy từ dòng 1 series_ctx.txt — không có title.txt)
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep01-fuufu-nenkin-sa` · Kịch bản LOCK (B3S PASS 2026-09-21, 7.238 chữ ≈ 25,5'), B5W/B5P xong. CHƯA giọng, CHƯA title.txt, CHƯA TIEU_DE_MO_TA.txt, CHƯA thumbnail. · ưu tiên cao (Tiêu đề và hook nói về 2 người khác nhau (妻 vs 日高) và con số của tiêu đề sai bản chất — đúng lỗi làm _fJim8rkhhM chỉ 10k (gói hứa một đằng, hook làm một nẻo). Đang thiếu cả title.txt nên sửa lúc này rẻ nhất.)
- Mốc: chốt 0 · giới thiệu 17 · hứa 8 (est — chưa có giọng: mốc giây = số chữ (bỏ xuống dòng) ÷ 284 chữ/phút × 60 (profile teinengo-real char_rate))
- Thumbnail: — — chưa có thumbnail
- Tiêu đề↔hook: L — Tiêu đề hứa 'tôi vs VỢ vẫn đi làm, chênh 8万円/tháng'. Hook 0–30s so tôi với đồng nghiệp 日高 (câu 0s); vợ chỉ được nhắc 1 câu ở 27s「介護施設の事務を続けている」; '8万円の差' nằm ở ~1360s (22,7' / 25,5'). · Thumb↔tiêu đề: N/A — Chưa có thumbnail (thư mục tập không có ảnh thumb/thumb_text.txt; SOP_LANE_F §2b: thumbnail ngoài phạm vi hiện tại). · Thumb↔hook: N/A — Chưa có thumbnail (thư mục tập không có ảnh thumb/thumb_text.txt; SOP_LANE_F §2b: thumbnail ngoài phạm vi hiện tại).
- ⚠ Lời hứa không giữ: '夫婦の月収に8万円の差': script (~1360s) so 年金 額面 13万1千 của 俺 với 手取り 21万2千 của 千恵子「その時点で八万円の差があった」— cùng lúc 俺 còn 送迎と帳簿の七万 (~1410s) nên chênh 月収 thật chỉ ~1万1千; qc_final_review.txt đã ghi đúng lỗi này. Giữ chữ '月収' là tựa sai bản chất.
- ⚠ Lời hứa không giữ: '働き続けた妻' không phải trục của hook: cụm 働き続け chỉ xuất hiện 1 lần (~1297s); đối thủ trong câu hỏi mở đầu là 日高 (39 lần trong script).
- ⚠ Lời hứa không giữ: Không chi tiết nào của tiêu đề (妻 đi làm, 8万) được nêu thành câu hỏi trong 90s đầu.
- Vấn đề: Câu 0–8s「六十歳で会社を出た俺と、六十五歳まで残った日高。どっちが幸せだったのか。」gần như chép nguyên câu 0.3s của XbwqD2SktC0「60歳でやめた俺と65歳まで残った同僚 どっちが幸せだったのか。」— cả khung lẫn chữ.
- Vấn đề: 11s「ただその答えは、五年前の俺には、想像もつかないものだった」là biến thể của câu XbwqD 80s「答えは思っていたより残酷だった」(SOP §2c đã cảnh báo chép câu biểu tượng).
- Vấn đề: 35–53s (≈18s) tả chiếc 電卓 12 chữ số trước khi có biến cố hay con số nào — kênh mẫu top không dành đoạn 0–60s nào cho đồ vật không mang số.
- Vấn đề: Tiền đầu tiên ở 100s (退職金一千四百八十万円); câu hỏi của video không gắn với con số nào của tiêu đề.
- Vấn đề: Cảnh trăng mật (目覚まし 60s, 映画館客六人 78s, 生ビール 84s) trùng gần y hệt ep03 (目覚まし 71s, 映画館客四人 80s, ビール 88s) và XbwqD (映画・平日の映画館・昼からビール 118–129s).
- Vấn đề: Tên 日高 (đồng nghiệp đối chiếu) dùng lại ở ep02.
- **Sửa:** CAO — Chọn một trục và khoá cả tiêu đề lẫn 10s đầu vào trục đó. Giữ góc 'vợ chồng' (góc mới, handoff §13): mở bằng con số chênh lệch, kiểu O84L0zOtrxo (67万 ở ~30s, lặp 3 lần tới 67s). Câu mở mẫu: 「六十で辞めた俺と、働き続けた千恵子。五年後、同じ家に入る金は、妻のほうが月に八万円多かった。」 — rồi nhắc lại '八万' lần 2 trước 30s (K02).
- **Sửa:** CAO — Sửa chữ tiêu đề cho đúng phép so trong script: không dùng '夫婦の月収'; ví dụ '…5年後、俺の年金と妻の手取りに月8万円の差' (khớp câu ~1360s). Hoặc sửa script cho 8万 là chênh 月収 thật — việc của h2dev, không sửa ở đây.
- **Sửa:** VỪA — Chuyển 日高 xuống vai 'nhân vật phản chiếu' vào ~100s (như 藤原 của O84 ở ~100s, người lạ của K8t ở 102s), không để 日高 là vế B của câu hỏi mở.
- **Sửa:** VỪA — Rút 電卓 (35–53s) còn 1 câu; kéo 'ここで、手札を言っておく' (97s) + 3 con số lên trước 60s.
- **Sửa:** THẤP — Đổi 1–2 chi tiết trăng mật (映画館/ビール) để 3 tập không lặp nhau; đổi tên 日高 ở ep02.
- Video mẫu: O84L0zOtrxo (con số tiêu đề làm bí ẩn trong 30s) + XbwqD2SktC0 (so 2 lựa chọn — học cấu trúc, không chép câu)

#### Tập ep02 — 【漫画】60歳で再雇用を選んだ俺…給料が半分になった1年後、元部下に見た残酷な現実
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep02-saikoyou-hanbun` · Kịch bản LOCK (Sol PASS 2026-09-20, 6.533 chữ ≈ 23,0'), B5W/B5P xong. CHƯA giọng, CHƯA TIEU_DE_MO_TA.txt, CHƯA thumbnail. · ưu tiên vừa (Tiêu đề không nói dối (payoff có thật) nhưng hook chĩa vào người khác; sửa 10–30s đầu là đủ, không đụng thân bài.)
- Mốc: chốt 0 · giới thiệu 15 · hứa 54 (est — chưa có giọng: mốc giây = số chữ (bỏ xuống dòng) ÷ 284 chữ/phút × 60 (profile teinengo-real char_rate))
- Thumbnail: — — chưa có thumbnail
- Tiêu đề↔hook: P — Mọi danh từ của tiêu đề có trong 60s đầu (一年後 7s, 再雇用 33s, 半分 36s, 元部下 37s, 残酷 58s). Nhưng câu hỏi của hook là 'tôi vs 同期 日高 ai mất nhiều hơn', còn tiêu đề hứa điều thấy ở 元部下 — 元部下 (遠藤) chỉ có tên ở ~363s, payoff ở ~874s. · Thumb↔tiêu đề: N/A — Chưa có thumbnail (thư mục tập không có ảnh thumb/thumb_text.txt; SOP_LANE_F §2b: thumbnail ngoài phạm vi hiện tại). · Thumb↔hook: N/A — Chưa có thumbnail (thư mục tập không có ảnh thumb/thumb_text.txt; SOP_LANE_F §2b: thumbnail ngoài phạm vi hiện tại).
- ⚠ Lời hứa không giữ: '元部下に見た残酷な現実': có thật trong script (~874s「残酷な現実というのは、こういうことだった」— ghế của 俺 được giữ nhờ ca đêm của 元部下 遠藤) nhưng 90s đầu chỉ có 3 chữ '上司は元部下' (37s); người xem không biết 元部下 là ai cho tới ~363s.
- ⚠ Lời hứa không giữ: '給料が半分': script ghi 額面 30万→17万 (~57%, ~150s) và tự nói 'ほぼ半分' — chấp nhận được, nhưng con số chưa có trong 90s đầu.
- Vấn đề: Khung câu 0–11s「黄色いヘルメットをかぶった俺と、家で新聞を読んでいる同期の日高。一年後、どっちが多くを失っていたか。」lại là khung XbwqD2SktC0 (俺 vs 同僚, どっちが…) — lần thứ 2 trong 3 tập.
- Vấn đề: 11s「これは金の話であり、金じゃない話でもある。」— câu trừu tượng, không hình, không số, chiếm vị trí 11–15s (nhịp contradiction).
- Vấn đề: 54s「答えは、俺の想像の外にあった。」là biến thể câu XbwqD 80s「答えは思っていたより残酷だった」.
- Vấn đề: Tiền đầu tiên ở 106s (退職金が1,150万円); lương 17万 (con số cho '半分') ở ~150s.
- Vấn đề: Tên 日高 trùng ep01; '段ボール工場' + tên '修一' trùng ep03 (真壁修一 元段ボール工場製造課長 vs 柴垣修一 元段ボール工場生産管理係長).
- **Sửa:** VỪA — Mở bằng 元部下 thay vì 日高: câu thoại của người trong cuộc ở giây 0 (kiểu _VXUim2J9QM mở bằng câu hỏi của vợ). Câu mở mẫu: 「『先輩、来週ちょっといいですか』。去年まで俺の部下だった男が、今は俺の契約を決める。」 — câu「先輩、来週ちょっといいですか」đã có sẵn ở ~417s.
- **Sửa:** VỪA — Đưa '額面30万→17万' lên trước 30s để 'nửa lương' thành con số (K02), bỏ câu 11s「これは金の話であり…」.
- **Sửa:** VỪA — Giữ câu 58s「残酷だったのは俺に対してだけじゃなかった」nhưng chỉ thẳng vào 元部下 (đó là payoff 874s) để lời hứa tiêu đề được đặt trong 60s.
- **Sửa:** THẤP — Đổi tên 日高 (trùng ep01) và 1 trong 2 cặp '段ボール工場/修一' (trùng ep03).
- Video mẫu: _VXUim2J9QM (mở bằng câu thoại người thứ hai) + O84L0zOtrxo (con số trong 30s)

#### Tập ep03 — 【漫画】63歳で年金を繰り上げた男…月2万円減った先に待っていた本当の後悔
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep03-kuriage-koukai` · Kịch bản LOCK (Sol PASS 2026-09-20, 6.490 chữ ≈ 22,9'), B5W/B5P xong. CHƯA giọng, CHƯA TIEU_DE_MO_TA.txt, CHƯA thumbnail. · ưu tiên vừa (Hook tốt nhất trong 3 tập (K02 ở 5s, khoá 34–62s); rủi ro chính KHÔNG nằm ở hook mà ở va chạm đề tài với video kênh mẫu đăng cùng ngày — cần tách gói đăng trước khi làm thumbnail.)
- Mốc: chốt 5 · giới thiệu 14 · hứa 52 (est — chưa có giọng: mốc giây = số chữ (bỏ xuống dòng) ÷ 284 chữ/phút × 60 (profile teinengo-real char_rate))
- Thumbnail: — — chưa có thumbnail
- Tiêu đề↔hook: K — 63歳 + 年金に手を付けた ở 0s, '月2万円少ない' ở 5s (con số tiêu đề làm câu chốt), '後悔' = 48s「二度目のはいを、俺は今も悔やんでいる」, '先に待っていた' = 52s「減ったのは、月2万円だけじゃなかった」. · Thumb↔tiêu đề: N/A — Chưa có thumbnail (thư mục tập không có ảnh thumb/thumb_text.txt; SOP_LANE_F §2b: thumbnail ngoài phạm vi hiện tại). · Thumb↔hook: N/A — Chưa có thumbnail (thư mục tập không có ảnh thumb/thumb_text.txt; SOP_LANE_F §2b: thumbnail ngoài phạm vi hiện tại).
- ⚠ Lời hứa không giữ: Không có lời hứa gãy: 月2万円 (21万→19万) có ở 5s và ~430–457s; 'bản chất hối hận' (注意書き: 障害年金の事後重症・遺族厚生年金は65歳まで) trả ở ~520–600s. Chữ '後悔' không xuất hiện nguyên văn (script dùng 悔やんでいる) — không phải lỗi.
- Vấn đề: Khung 0–5s「63歳で年金に手を付けた俺と、まだ手を付けない同期。」vẫn là 'A俺と、B同期' — 3/3 tập dùng cùng khung mở của một video kênh mẫu (XbwqD).
- Vấn đề: Người thứ hai: 同期 không có tên tới 蒲生 ~520s; câu thoại đầu tiên ở 158s (芳江). Không có giọng thứ hai trong 120s.
- Vấn đề: Cảnh trăng mật 67–106s (目覚まし・九時・映画館客四人・ビール) trùng ep01; '段ボール工場' + '修一' trùng ep02.
- Vấn đề: Va chạm đề tài: kênh mẫu vừa đăng ZogHjPo8cX0 (2026-09-23)「60歳で年金を受け取った男…65歳まで待たなかった15年後の末路」— cùng 繰上げ, khung tiêu đề gần giống hệt ('NN歳で年金を〜た男…〜'), thumbnail「60歳で年金受給」+「年金24%減」+「話が違う…」.
- **Sửa:** VỪA — Đưa cảnh 窓口 (34–52s) lên giây 0 để mở bằng CẢNH thay vì khung 'A俺とB同期' — đây là chi tiết riêng của tập mà ZogHjPo8cX0 không có. Câu mở mẫu: 「二年前、年金事務所の窓口で、俺は二度『はい』と言った。二度目のはいを、今も悔やんでいる。」 rồi '月2万円' ngay sau (≤15s).
- **Sửa:** VỪA — Tiêu đề/thumbnail phải khác ZogHjPo8cX0: đừng dùng dải 'NN歳で年金受給'. Gợi ý chữ thumbnail: dải đầu「年金繰上げの落とし穴」hoặc「読まなかった1行」; trái (quầy 年金事務所, gật đầu) bong bóng「はい」 nhãn「月2万円減」; phải (phòng chờ bệnh viện) bong bóng「知らなかった…」 nhãn「2年後…」. Tiêu đề có thể thêm vế 注意書き/'読まなかった' để tách khỏi video kia.
- **Sửa:** THẤP — Cho 同期 một tên + 1 câu thoại trong 120s (như 藤原 của O84 ở ~100s), hoặc thay chữ 同期 ở 0s bằng 蒲生.
- **Sửa:** THẤP — Đổi chi tiết trăng mật để không trùng ep01.
- Video mẫu: O84L0zOtrxo (con số tiêu đề ≤30s + câu hỏi 'vì sao') — ep03 đã làm đúng phần này; phần mở bằng cảnh học K8tTrxijqEo (cảnh cụ thể ở 2s)

### Nguyên tắc
- **Tiêu đề thắng nhờ một QUYẾT ĐỊNH chung của khán giả, không nhờ số tiền.** — cơ chế: Người 58–67 bấm vì thấy câu hỏi của chính mình (nghỉ 60 hay 65, sao tiền cứ hao) — con số tiền trên tiêu đề chỉ là hoàn cảnh của nhân vật, không phải câu hỏi của họ. · bằng chứng: Số tiền trên tiêu đề: 1/6 top (O84L0zOtrxo 67万円 — và ở đó con số CHÍNH là bí ẩn) vs 3/5 video còn lại (_fJim8rkhhM 2000万 10k, iJrKlKBAabY 478万/18万 8,4k, e_Zo7Ht5OH8 1700万 ~10k). Tuổi 'NN歳' có ở 8/9. · vì sao: Luật cứng lane hiện ghi 'tựa PHẢI có SỐ TIỀN' — dữ liệu kênh mẫu không ủng hộ; bắt buộc số tiền dễ đẩy tiêu đề về dạng 'hoàn cảnh riêng' (1700万の元部長) thay vì 'quyết định chung'. · áp dụng: Tựa lane F: bắt buộc tuổi + quyết định + mốc thời gian + cảm xúc; chỉ đưa số tiền khi chính con số là bí ẩn của video (kiểu '67万円消えた本当の理由', '月2万円減った先に' của ep03).
- **Trong 30s đầu phải nói lại tiền đề/con số của tiêu đề bằng lời nhân vật.** — cơ chế: Người vừa bấm cần xác nhận 'đúng cái mình bấm vào' trước khi chịu nghe tự giới thiệu và backstory. · bằng chứng: XbwqD2SktC0 0.3s (313k), K8tTrxijqEo 0s (184k), O84L0zOtrxo ~30s 67万 lặp 3 lần tới 67s (174k); EANADckKWT4 'tuyệt vọng' chỉ hé ~113–126s, '2ヶ月' ~271s (72k); dY3HfjtmvXI cú '衝撃' 88–98s (50k); _fJim8rkhhM '5選' không có trong 120s (10k). · vì sao: Là cách rẻ nhất để giữ người từ giây 5 tới 60; kênh mẫu có ngoại lệ (_VX 62歳 ở ~391s) nhưng khi đó vế đầu tiêu đề vẫn được nói ở 0s. · áp dụng: Kiểm máy: mỗi tập, lấy danh từ/con số chính của title.txt, grep trong 142 chữ đầu (=30s × 284/60). ep03 đạt; ep01 phải đưa '妻/8万' vào; ep02 phải đưa '元部下' vào như vế chính.
- **Cú đảo 'ずっとそう思っていた → だが' là động cơ của cả kênh, phải có trong 120s.** — cơ chế: Nói trước niềm tin rồi báo nó sai biến người xem thành người biết trước, chờ xem nó vỡ ra sao. · bằng chứng: 9/9 transcript có trong 120s: O84 ~17s, dY3 0–3s, _VX ~27s, K8t ~58s, XbwqD 50.8→58.5s, _fJ 62s, EANAD ~74/113s, e_Zo7 79s, WblFD 49s. · vì sao: Là mẫu số chung của cả video top lẫn video thấp → không đủ để thắng, nhưng thiếu là lệch giọng kênh. · áp dụng: Giữ (3/3 tập đã có: ep01 11s, ep02 49s, ep03 11s). Đừng dùng lại nguyên câu「答えは思っていたより残酷だった」— 3/3 tập đang có biến thể của nó.
- **Giọng thứ hai phải vào trước ~100s.** — cơ chế: Một câu của người khác (vợ hỏi sổ, người lạ phán, đồng nghiệp chọn ngược) làm câu hỏi của video có người phản biện — không chỉ là độc thoại than thở. · bằng chứng: 4/4 video ≥100k: XbwqD 同僚 37s, _VX 妻 ~87–98s, O84 藤原 ~100s, K8t 常連 ~102s. 0/2 video 50–72k (EANAD, dY3 — độc thân, không ai nói với họ trong 120s). · vì sao: Tương quan trên 6 video, lẫn với yếu tố 独身; nhưng rẻ để làm và không hại. · áp dụng: ep03 hiện thoại đầu ở 158s và 同期 vô danh tới ~520s → cho 蒲生 hoặc 芳江 1 câu trước 100s. ep01/ep02 đã có (91s / 46s).
- **Trăng mật hưu trí là thân, không phải hook — đặt sau câu khoá.** — cơ chế: Liệt kê tự do không có mâu thuẫn; nó chỉ căng khi người xem đã biết cái giá (câu khoá) từ trước. · bằng chứng: XbwqD2SktC0: câu khoá 62.8–80.2s rồi mới trăng mật 82–129s (313k). EANADckKWT4: trăng mật chiếm 0–126s, câu khoá là 'はずだった' ở cuối (72k). dY3HfjtmvXI: 18–58s tự do độc thân trước con số đầu 64s (50k). · vì sao: Đúng thứ tự thì cùng một đoạn tự do trở thành 'đếm ngược'. · áp dụng: 3/3 tập đã đặt đúng (trăng mật ep01 53–97s, ep02 78–104s, ep03 67–106s, đều sau câu khoá). Giữ; chỉ đổi chi tiết để không trùng nhau.
- **Mỗi tập một kiểu mở — đừng khoá lane vào khung của 1 video hit.** — cơ chế: Khán giả xem liên tiếp nhiều video một kênh; câu mở lặp lại báo hiệu 'đã biết truyện' và dễ bị coi là chép kênh mẫu. · bằng chứng: 7 transcript kênh mẫu = 7 kiểu mở (H18 XbwqD, H03 O84, H04 K8t, H21 _VX, H35 EANAD, H15 dY3, H12 _fJ); khung 'A俺とB同僚 どっちが' chỉ 1/9 (XbwqD). Tập của mình dùng khung đó 3/3. · vì sao: Kênh mẫu tự đổi kiểu mở nhưng giữ khuôn thumbnail (O84→K8t→_fJ; _VX→Zog) — đổi hook, giữ gói nhận diện. · áp dụng: Gán trước kiểu mở cho từng tập theo đề tài: so sánh 2 lựa chọn → H18 (tối đa 1/5 tập); tiền hao → H03+K02; thủ tục/giấy tờ → mở bằng cảnh quầy (ep03 窓口); người khác quyết định mình → H21/H02 (ep02 元部下).
- **Thumbnail: chủ đề 4–9 chữ + 2 câu nội tâm, không số tiền; gói nhận diện dùng lại được nhưng không cứu đề tài hẹp.** — cơ chế: Ảnh nhỏ trên điện thoại chỉ đọc được 1 dải chữ lớn + 2 bong bóng; câu nội tâm ('話が違う…') truyền cảm xúc nhanh hơn con số. · bằng chứng: Dải đầu 8/9, 2 panel 8/9, bong bóng nội tâm 9/9, không tiền 7/9. Khuôn xếp hạng bia/安いから: O84 174k → K8t 184k → _fJ 10k (cùng khuôn, đề tài/hook khác). · vì sao: Khuôn giúp nhận diện kênh; hiệu quả vẫn do tiêu đề + hook quyết định. · áp dụng: Dựng TEMPLATE thumbnail lane F theo khuôn này (hiện SOP §6 ghi chưa có). Chữ trên thumbnail phải có trong 120s đầu (tránh 'L' như _fJ). Tránh dải 'NN歳で年金受給' cho ep03 vì trùng ZogHjPo8cX0.

### Lưu ý dữ liệu
- Mốc giây của 5 video (K8t, O84, _VX, EANAD, dY3) là ƯỚC TÍNH = vị trí ký tự ÷ (len transcript/duration), tốc độ 4,35–4,76 ký tự/giây (kể cả dấu cách ASR). Kiểm trên XbwqD2SktC0 (có mốc thật): câu 'だが、今俺は…' ước tính 58s vs thật 58.48s; 'だが今' khoá ước 62s vs thật 62.84s — sai số ~±1s ở 60s đầu, có thể lớn hơn ở phút thứ 2.
- Mốc thật (hook_segments) chỉ có ở XbwqD2SktC0 và _fJim8rkhhM. Đã mở lại raw 7 video còn lại ngay trước khi ghi file: hook_segments vẫn rỗng (transcript_via=none).
- ZogHjPo8cX0 và iJrKlKBAabY: không có transcript ở raw lẫn transcripts.json/VIDEO_ANALYSIS → chỉ phân tích gói đăng; KHÔNG đưa vào seed file A (không có hook để chấm).
- Transcript là ASR: 老語=老後, 最雇用=再雇用, 退食金=退職金, 持ち入え=持ち家, '3万円か' ở dY3 ~64s là 13万円 (mô tả xác nhận 年金13万円), '相材'=惣菜, 'シーナ'=椎名?. Trích dẫn trong file đã sửa các lỗi hiển nhiên ở key_line/lock_line; hook_0_30s trong seed giữ nguyên ASR (bỏ [音楽] và dấu cách).
- View: lấy từ raw (tải 2026-09-23); transcripts.json (2026-09-16) có số cũ hơn (VD XbwqD 299k vs 313k). Tag 'top/new' theo selection.json; không có video tag 'low' trong selection → dùng e_Zo7Ht5OH8 & WblFD81yjOI (10k, ≥7 tuần tuổi) làm đối chứng thấp CHỈ qua transcript, không có thumbnail/raw.
- Tương quan trên ≤9 video, lẫn yếu tố thời điểm đăng (6 top đăng 06-25→08-26; tháng 9 đều thấp) — các luận điểm là quan sát, chưa phải nhân quả.
- Tập của mình: chưa có giọng → mốc giây ước tính theo 284 chữ/phút (profile teinengo-real, @0.95); script.txt đã bỏ xuống dòng khi đếm. Chưa có thumbnail/mô tả ở cả 3 tập (đúng phạm vi SOP_LANE_F §2b) → thumb_title/thumb_hook ghi N/A.
- Chữ trên thumbnail kênh mẫu chép từ ảnh E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\thumbs\<id>.jpg đã mở xem từng cái (9/9).

---

## 老後のお金ストーリー → lane `teinengo-tanoshimi`

Kênh: https://www.youtube.com/channel/UCI2cPqBmCPMxxKI4u2Gqs_Q

Kênh làm 1 khuôn cho video list: 0–12s một nghịch lý đời hưu (tự nói hoặc thoại) → 12–38s một NGƯỜI KHÁC nói câu làm tiền đề (bạn cùng tuổi, sếp cũ, người lạ) → 29–48s 「この時の俺はまだ知らなかった…」 → ~40s mới tự giới thiệu → 60–120s tiểu sử “mới hưu vui, nửa năm sau chán” → mục 1 ở 226–356s (17–29% kịch bản). Số N hiếm khi nói trong 90s đầu (1/7). Tiêu đề = 【漫画】+定年後/60代+tính từ cực cấp+danh từ+N選…vế phần thưởng; thumbnail tách tiêu đề làm 2 dòng (băng đen trên + dòng đỏ dưới), tranh hiện các hạng GIỮA và giấu hạng 1; mô tả 250–500 chữ, câu đầu hỏi thẳng nỗi đau, không hashtag.

### Khung hook theo giây
- **0–12s · Nghịch lý đời hưu** — Một câu đặt 2 sự thật đá nhau (có thời gian mà tiền rò; có đủ mà vẫn thiếu; rảnh nên không đi), hoặc câu thoại sốc giá. 7/7 video có transcript mở kiểu này, không tả cảnh. Ví dụ: 「定年から時間だけはたっぷりできた。でも暇だから出かければコーヒー代、ガソリン代、買い物代。」 (AOe-E69mLzA)
- **12–38s · Người khác nói câu tiền đề** — Bạn cùng tuổi/sếp cũ/người lạ nói 1 câu lật cách nghĩ và (ở video list) nêu ĐIỀU KIỆN của danh sách: ai cũng làm được, không phiền ai, 0 yên. 5/7 ≤38s (bgUq 33s, AOe 14,6s, ASBV 0–29s, _G9s 29s, YKjW 15s); BeIZ ~54s; _EhP chỉ nhắc ~22s. Ví dụ: 「お前は暇を潰そうとするから金がかかるんだよ。1人でできる。誰にも迷惑をかけない。そして一円も使わない。」 (AOe-E69mLzA)
- **26–40s · Nghi ngờ lời hứa** — Nhân vật chính hỏi lại, biến lời người khác thành câu hỏi của cả video. Ví dụ: 「そんな過ごし方が本当にいくつもあるのか。」 (AOe-E69mLzA)
- **29–48s · Báo trước (K03)** — 「この時の俺はまだ知らなかった」+ điều sẽ đổi. 5/7 (_EhP ~31s, ASBV ~31s, _G9s ~37s, bgUq 42,6s biến thể 衝撃を受けた, AOe 48,6s). Ví dụ: 「この時の俺はまだ知らなかった。20年以上前の俺の常識がこの一晩で大きく変わることを。」 (ASBVa_H_leI)
- **38–71s · Tự giới thiệu 1–2 câu** — Tên + tuổi + năm làm/nghề + mới hưu bao lâu. Trung vị 42s (ASBV ~38, _G9s ~42, bgUq 52,7, AOe 55,4, YKjW 71,4); 2/7 giới thiệu ngay 0–3s (_EhP, BeIZ). Ví dụ: 「俺の名前は山田和夫。66歳。精密機器メーカーで42年間営業職として働き、1年前に定年退職した。」 (AOe-E69mLzA)
- **60–120s · Tiểu sử “vui rồi chán”** — Mới hưu tưởng tự do → nửa năm sau 8 giờ rưỡi đã hết việc → cảnh vợ hỏi 「今日は出かけないの?」. Ví dụ: 「ようやく自由になった。そう思ってたところが半年もするとその自由にも慣れてくる。」 (AOe-E69mLzA)
- **226–356s · Mục 1** — 1つ目 (thói quen) hoặc 第5位 (xếp hạng địa điểm) — 17–29% kịch bản, 1.363–2.089 chữ không tính khoảng trắng (5 video list có transcript + DfIBG3fJW6o). Ví dụ: 「まずは1つ目。少し早起きをすることだ。」 (bgUqNHYZbq0)

- Tiêu đề: 【漫画】(10/10) + chủ thể 定年後 (6/10) hoặc 60代/６０代 (3/10) + tính từ cực cấp/lạ (最強・一流だけが・格式の高い・なぜか老けない・驚くほど・豪華/高級 — 8/10) + danh từ cụ thể + N選 (7/10 video chọn; 9/20 cả kênh) + 「…」 vế phần thưởng/lật (実は1円もかからない・同年代と差がつく意外な共通点・【世間の非常識】). Dài 33–45 ký tự ở 7 video tốt; video 1,1k dài 52. Chỉ 1/10 dùng 「」.
- Thumbnail: Băng ĐEN đặc trên 10/10, chữ đầu VÀNG 10/10 (定年後 6/10, 60代 2/10), 1 cụm ĐỎ trong băng trên 5/10 — đúng 5 trong 6 video view cao nhất (bgUq, BeIZ, AOe, _EhP, _G9s); dòng ĐỎ viền trắng lớn phía dưới 8/10 (thiếu ở bgUq, ASBV — 2 ảnh dùng nhãn vàng thay); ≥2 khung 7/10; bong bóng TRẮNG hình oval DỌC 8/10; nhãn vàng 3/10 (hạng hoặc đặc điểm); ≥1 mặt thư thái/cười 9/10 — ảnh duy nhất chỉ có mặt khổ là YKjW (1.159 view). Ở 4/4 video xếp hạng soát được (bgUq, BeIZ, AOe, _G9s) tranh hiện các hạng dưới 1 và GIẤU hạng 1.
- Mô tả: 247–508 ký tự, 0/10 hashtag, 0/10 link. Câu 1 hỏi thẳng nỗi đau hoặc nêu nghịch lý (6/10 dạng câu hỏi 「〜ませんか？」「〜でしょうか？」). Đoạn 2 tóm nhân vật + tuổi + người dẫn đường (6/10: AOe 「66歳で定年退職した男性が、元上司から教わった」, _EhP, ASBV, _D8q, rapoU, bgUq 中村). Đoạn 3 liệt kê các mục nhưng giấu mục cuối (AOe: 断捨離・空や雲・議会・昼寝 + 「最後にたどり着いたのは…意外な“最高の暇つぶし”」). Câu chốt nhắm người xem 「60代・70代の方におすすめです」 hoặc 「ご覧いただければ幸いです」 (8/10); xin comment 2/10 (BeIZ, _G9s); miễn trừ 2/10 (BeIZ, H-Dk).
- 4 phần nối nhau: Một lời hứa đi qua 4 chỗ nhưng mỗi chỗ nói một phần: tiêu đề nêu đủ (chủ thể + N選 + phần thưởng); thumbnail tách tiêu đề làm 2 dòng (băng trên 10/10 lấy chữ tiêu đề; dòng dưới 6/8 lấy tiếp từ tiêu đề) và cho XEM các mục giữa; hook chứng minh bằng một người thật trong truyện, nói lõi tiêu đề trong ≤36s ở 6/7 (AOe 「一円も使わない」 23s, ASBV 「2万円」 0s, bgUq 「7つのこと」 36s); mô tả hỏi thẳng nỗi đau + liệt kê mục trừ mục cuối. Ngoại lệ đáng chú ý: _EhP lấy dòng đỏ thumbnail 「お金や健康ではない」 từ HOOK (0–20s), không từ tiêu đề.
- Số đếm: {'videos_chon': 10, 'co_transcript': '7/10 (3 mốc giây thật: bgUq, AOe, YKjW; 4 ước tính: BeIZ, _EhP, ASBV, _G9s); 3 không có (_D8q, rapoU, H-Dk)', 'mo_nghich_ly_0_12s': '7/7', 'nguoi_khac_noi_le_38s': '5/7 (+BeIZ ~54s, _EhP chỉ nhắc ~22s)', 'k03_le_48s': '5/7', 'tu_gioi_thieu_trung_vi_s': 42, 'so_N_trong_90s': '1/7 (bgUq 「7つ」 36s); AOe 「いくつも」 26s', 'muc1_s': '226–356 (6 video list)', 'title_N_sen': '7/10 video chọn; 9/20 cả kênh — trung vị 85k (N選) vs 7,5k (11 video không N選)', 'thumb_bang_den': '10/10', 'thumb_do_trong_bang_tren': '5/10 (= 5/6 video view cao nhất)', 'thumb_dong_do_duoi': '8/10', 'thumb_bong_bong_doc': '8/10', 'thumb_giau_hang1': '4/4 video xếp hạng soát được', 'thumb_chi_mat_kho': '1/10 (YKjW 1.159 view)', 'desc_hashtag': '0/10', 'desc_cau_hoi_dau': '6/10'}
- Ngoại lệ: ['BeIZhu1I4Tw (172k): hook 120s không nhắc 神社, không K03, người khác nói ở ~54s — thắng nhờ đề tài tra cứu 神社5選.', 'ASBVa_H_leI (108k): không phải list N選 — video trải nghiệm 1 chuyến, không có hook_marker; thumbnail không có dòng đỏ dưới.', 'bgUqNHYZbq0 (202k): thumbnail in 「第3位/第2位」 trong khi video đếm 1つ目→7つ目 (không có chữ 位 nào) — lệch nhỏ vẫn thắng.', 'H-Dk8XBmw90 (7,6k): thumbnail đúng khuôn (N選, 2 khung, bong bóng dọc, dòng đỏ) nhưng đề tài làm thêm vì lo lương hưu → thấp: thumbnail đúng khuôn không cứu đề tài lệch.']

Thắng vs thua: Top (bgUq 202k, BeIZ 172k, AOe 157k) so với thấp (YKjW 1.159, rapoU 4.230/3 ngày, H-Dk 7.560/5 ngày): khác ở ĐỀ TÀI, không ở hook. Hook YKjW (có mốc giây thật) đủ 4 nhịp — niềm tin sai 0,2s, 3 giọng hối hận 15–36s, K11 「60歳でも後悔して65歳でも後悔する」 35,8s, câu khoá 64s — chấm 8/12, BẰNG BeIZ 172k. Cái khác: (1) đề tài — cả 20 video, 9 video N選 vui/rẻ/du lịch/sức khoẻ trung vị 85k, 11 video còn lại trung vị 7,5k; 6/6 tiêu đề có 年金/貧乏/破綻/後悔/失敗/不安 đều ≤16k (zHtHiHEcXV0 16k, Or6odB2b70M 12,8k, 61lcBV32roE 11,6k, H-Dk8XBmw90 7,6k, rapoUAXE7y8 4,2k, YKjWwJZrKXY 1,2k), 0/6 video ≥85k chạm chủ đề tiền-sợ; (2) thumbnail — YKjW là ảnh duy nhất chỉ có mặt ôm đầu + câu doạ 「間違うと老後貧乏」, rapoU băng trên toàn vàng không cụm đỏ và 1 khung, trong khi 5/6 video cao nhất có cụm ĐỎ trong băng trên; H-Dk lại đúng khuôn thumbnail mà vẫn thấp → thumbnail không cứu đề tài lệch; (3) tiêu đề — YKjW 52 ký tự liệt kê 4 mốc tuổi, dài nhất kênh (7 video tốt 33–45). Video mới _D8qcebhsPU (「一流だけがやっている休日の過ごし方5選」, thumb 「ダラダラする/予定ゼロ/一流はこれをやる」) đạt 26.720 view sau ~7 giờ — đúng công thức N選 + nghịch lý “lười mới là hạng nhất” — xác nhận chiều ngược lại.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 202,002 | 0.2 | 33.2 | 52.7 | 36.1 | H08 K18 K09 K03 | 9 | K | K | P | 【漫画】なぜか老けない50代男性が「毎日やっていること」7選…同年代と差がつく意外な共通点 |
| top | 172,445 | 0.0 | 53.7 | 3.3 | — | H12 H17 | 8 | P | K | P | 【漫画】一生に一度は参拝したい…定年後に行くべき格式の高い神社5選 |
| top | 157,196 | 14.6 | 26.4 | 55.4 | 20.5 | H04 H17 K18 K03 | 10 | K | K | K | 【漫画】定年後、最強の暇つぶし5選…実は1円もかからない楽しみ方がありました |
| top | 114,338 | 9.8 | 31.0 | 0.0 | 25.4 | H12 H04 K03 | 9 | K | K | K | 【漫画】６０代から人生が驚くほど心地よくなる定年後に見つけたちょうどいい生き方５選 |
| top | 107,767 | 0.0 | 28.7 | 38.2 | 31.0 | H22 H14 K03 | 11 | K | K | K | 【漫画】夜行バスに2万円！？新幹線より高い豪華夜行バスに65歳で乗ってみた結果… |
| top | 85,336 | 29.0 | 36.6 | 41.5 | — | H17 K03 | 8 | K | K | P | 【漫画】定年後は一人旅が最高、60代から一度は行きた有名の温泉地5選 |
| low | 1,159 | 0.2 | 64.0 | 71.4 | 35.8 | H15 H18 K11 K01 | 8 | K | K | P | 【漫画】年金は何歳から受け取るべき？60歳、65歳、70歳、75歳、知らないと後悔する受給年齢の落とし穴 |
| new | 26,720 | — | — | — | — |  | — | — | K | — | 【漫画】定年後、一流だけがやっている休日の過ごし方5選【世間の非常識】 |
| new | 4,230 | — | — | — | — |  | — | — | P | — | 【漫画】６０代だから話せる、人生最大の失敗。それでも人生は終わらなかった |
| new | 7,560 | — | — | — | — |  | — | — | K | — | 【漫画】定年後、年金だけでは不安な人へ…65歳から始めやすい最強バイト5選 |

#### 【漫画】なぜか老けない50代男性が「毎日やっていること」7選…同年代と差がつく意外な共通点 — https://www.youtube.com/watch?v=bgUqNHYZbq0
- Câu chốt (0.2s): 「あれ?お前って中学校の同窓会にわかわかしい男性が入ってきた。周りと違う肌質で今時の洋服を着ている。俺だよ。中村あだよ。(ASR: 若々しい/中村だよ)」
- Câu khoá (33.2s): 「いや、特別なことはしていないよ。誰でもできる簡単な7つのことをやっているだけだ。一体それは何なんだ?」
- Chữ thumbnail: băng đen trên: 「老けない人の」(vàng)「共通点」(đỏ) | 2 khung, nhãn vàng 「第3位」「第2位」 | bong bóng dọc 「孤独な生活」「肉を食う」 | không có dòng đỏ dưới | 2 mặt tươi cười, tóc đen (nhân vật 55 tuổi) · Mô tả: 同じ50代でも、実年齢より若々しく見える人と、年齢以上に老けて見える人がいます。
- Hook↔tiêu đề: K — Tiêu đề 「なぜか老けない50代男性」 = cảnh 0,2s bạn cùng lớp trẻ hẳn; 「7選」 = 「7つのこと」 ở 36,1s. · Thumb↔tiêu đề: K — Băng trên 「老けない人の共通点」 ghép 2 cụm của chính tiêu đề (老けない + 共通点). · Thumb↔hook: P — Thumbnail là 2 mục (孤独 = 5つ目 ~826s, 肉 = 6つ目 ~1047s), hook 0–60s là cảnh họp lớp; hai thứ chỉ nối qua chủ đề “không già”. Nhãn 「第3位/第2位」 không có trong video (video đếm 1つ目→7つ目).
- Vì sao giữ người: H08 bản GHEN TỊ chứ không thương hại: cùng tuổi mà người kia trẻ → khán giả tự hỏi “mình thuộc bên nào”. Người kia tự nói điều kiện 「特別なことはしていない・誰でもできる」 (33s) nên lời hứa có người bảo chứng; 「衝撃を受けた」 (42s) báo có cú lật.
- Điểm yếu: Nhãn hạng 第3位/第2位 trên thumbnail không khớp cách đếm trong video (1つ目→7つ目; 7つ目 là 「一番難しい」). Tự giới thiệu 52,7s dài 35 giây tiểu sử (bóng chày, gương) trước khi vào mục 1 ở ~356s — mục 1 muộn nhất trong 6 video list của kênh.

#### 【漫画】一生に一度は参拝したい…定年後に行くべき格式の高い神社5選 — https://www.youtube.com/watch?v=BeIZhu1I4Tw
- Câu chốt (0.0s): 「まさか67歳になって旅に出るとはな。」
- Câu khoá (53.7s): 「寺さん、現役の頃から同じこと言ってましたよ。確かに元気なうちに行かないとそのうちが来る前に行けなくなりますよ。(…)金も時間もある。足も動く。それなのに行かないなら一体いつ行くんだ。」
- Chữ thumbnail: băng đen trên: 「定年後」(vàng)「に」(trắng)「参拝したい」(đỏ) | 2 khung: cổng 稲荷 (伏見稲荷 = 第3位) / điện 出雲大社 (= 第2位) — không nhãn hạng | bong bóng dọc 「一人旅」「自由」 | dòng đỏ dưới 「有名神社5選」 | 2 mặt thư thái · Mô tả: 定年退職後、時間に余裕ができたからこそ訪れてみたい日本の神社。
- Hook↔tiêu đề: P — Hook 0–120s không có chữ 神社 hay số 5; chỉ có quyết định đi một mình. Lời hứa “đền 5選” chỉ lộ ở ~298s (第5位 宇佐神宮). · Thumb↔tiêu đề: K — Băng trên 「定年後に参拝したい」 + dòng dưới 「有名神社5選」 = 2 nửa của tiêu đề (一生に一度は参拝したい / 定年後に行くべき…神社5選). · Thumb↔hook: P — Bong bóng 「一人旅」「自由」 khớp hook (quyết định đi một mình ~87s); 2 ngôi đền trên ảnh (第3位/第2位) không xuất hiện trong 120s đầu.
- Vì sao giữ người: Mâu thuẫn “rảnh nên KHÔNG đi” (~32s) đúng tâm lý người mới hưu; câu của đồng nghiệp cũ biến nó thành nỗi sợ thời gian còn lại (~54–67s: 行けなくなりますよ, 膝, 階段). Video sống chủ yếu nhờ nhu cầu tra cứu “đền nên đi 1 lần trong đời”.
- Điểm yếu: Tự giới thiệu ở 3s (H12) trước khi có mâu thuẫn; câu của người khác tới ~54s (muộn nhất trong nhóm list); không có câu báo trước K03; hook không nhắc 神社 — 172k nhờ ĐỀ TÀI, không nhờ hook (điểm 8/12, bằng video 1,1k YKjWwJZrKXY).

#### 【漫画】定年後、最強の暇つぶし5選…実は1円もかからない楽しみ方がありました — https://www.youtube.com/watch?v=AOe-E69mLzA
- Câu chốt (14.6s): 「お前は紐を潰そうとするから金がかかるんだよ。1人でできる。誰にも迷惑をかけない。そして一延も使わない。(ASR: 紐=暇, 一延=一円)」
- Câu khoá (26.4s): 「そんな過ごし方が本当にいくつもあるのか。(…)この時の俺はまだ知らなかった。定年後の暇そのものがこんなに贅沢だったなんて。」
- Chữ thumbnail: băng đen trên: 「定年後、」(vàng)「最強の」(đỏ)「暇つぶし」(trắng) | 4 khung, nhãn vàng 「5位」「4位」「3位」「2位」 (giấu 1位) | dòng đỏ dưới 「※1円もかからない」 | 4 mặt thư thái/cười · Mô tả: 定年後、時間はあるのに「何をして過ごせばいいか分からない」「暇を潰すたびにお金がかかる」と感じていませんか？
- Hook↔tiêu đề: K — 「1円もかからない」 = 23s 「一円も使わない」; 「暇つぶし」 = 11s 「暇を潰すために」. · Thumb↔tiêu đề: K — Băng trên 「定年後、最強の暇つぶし」 và dòng dưới 「※1円もかからない」 gần như chép nguyên 2 vế tiêu đề. · Thumb↔hook: K — Dòng đỏ 1円もかからない = câu 20–26s; 4 khung hạng 5→2 = lời hứa “nhiều cách” ở 26s, hạng 1 bị giấu.
- Vì sao giữ người: Nghịch lý rò tiền vì rảnh (0–11s) là nỗi lo chung của người mới hưu; câu của người đi trước (14,6s) vừa chẩn bệnh vừa đưa điều kiện của danh sách (20–26s) nên người xem ở lại để kiểm “có thật 0 yên không”; K03 ở 48,6s cam kết có cú lật trước khi vào tiểu sử.
- Điểm yếu: Tiểu sử 55–120s (42 năm bán hàng, sáng 8 giờ rưỡi) dài; mục 1 ở ~356s. Chấm lại 10/12 (kho cũ 8/12) vì thumbnail khớp hook nguyên văn (1円) và cảnh tiêu tiền dựng hình được.

#### 【漫画】６０代から人生が驚くほど心地よくなる定年後に見つけたちょうどいい生き方５選 — https://www.youtube.com/watch?v=_EhPtM6cRFk
- Câu chốt (9.8s): 「ロモ(老後)資金はある程度準備した。健康にも大きな問題はない。妻との仲も悪くない。それなのになぜか毎日が満たされなかった。(…)お金も健康もあるのに俺には何が足りないんだ。」
- Câu khoá (31.0s): 「その人から聞いたのは俺が今まで考えもしなかった定年後の生き方だった。この時の俺はまだそれを知らなかった。こんなにも素晴らしい定年後の生き方があるなんて。」
- Chữ thumbnail: băng đen trên: 「定年後、」(vàng)「最高の」(đỏ)「生き方」(trắng) | 1 khung: ông dang tay trên đồi, trời xanh, mặt cười | dòng đỏ dưới 「お金や健康ではない」 | không bong bóng, không nhãn · Mô tả: 定年後、幸せに暮らすために本当に大切なものとは何でしょうか？
- Hook↔tiêu đề: K — 「定年後に見つけた…生き方」 = ~25s 「考えもしなかった定年後の生き方」. · Thumb↔tiêu đề: K — Băng trên 「定年後、最高の生き方」 lấy 定年後/生き方 của tiêu đề (đổi ちょうどいい → 最高). · Thumb↔hook: K — Dòng đỏ 「お金や健康ではない」 là đúng câu hỏi 0–20s 「お金も健康もあるのに…何が足りない」 (dòng này KHÔNG có trong tiêu đề — lấy từ hook + câu 2 mô tả).
- Vì sao giữ người: H04 bản hưu trí: có đủ tiền, sức khoẻ, vợ mà vẫn thiếu → người xem “đủ điều kiện” tự nhận ra mình; câu hỏi “thiếu gì” được thumbnail trả lời nửa chừng (không phải tiền, không phải sức khoẻ) nên phải xem.
- Điểm yếu: Người dẫn đường chỉ được NHẮC ở ~22s, chưa có câu thoại của ông cho tới ~110s. Hình ảnh trừu tượng (cảm giác trống) — dựng hình yếu hơn video trải nghiệm.

#### 【漫画】夜行バスに2万円！？新幹線より高い豪華夜行バスに65歳で乗ってみた結果… — https://www.youtube.com/watch?v=ASBVa_H_leI
- Câu chốt (0.0s): 「2万円バスに2万円も払うのか。普通の夜行バスじゃないぞ。完全個室の豪華夜行バスだ。それでも新幹線より高いじゃないか。」
- Câu khoá (28.7s): 「でもそれって20年以上前の話だろう。(…)今の夜行バス本当に昔と同じだと思うか?この時の俺はまだ知らなかった。20年以上前の俺の常識がこの一晩で大きく変わることを。」
- Chữ thumbnail: băng đen trên: 「60代」(vàng)「で高級夜行バス旅」(trắng) | 2 khung: ngồi ghế da uống cà phê mặt thư thái / ngó vào phòng riêng mặt ngạc nhiên | bong bóng dọc 「片道2万」「11席だけ」 | nhãn vàng 「極上シート」「完全個室」 | không dòng đỏ dưới · Mô tả: 夜行バスに片道約2万円。
- Hook↔tiêu đề: K — 「夜行バスに2万円!?新幹線より高い」 là nguyên câu thoại 0–7s. · Thumb↔tiêu đề: K — Băng trên 「60代で高級夜行バス旅」 = 「豪華夜行バスに65歳で乗ってみた」 rút gọn; 「片道2万」 = 「2万円」 của tiêu đề. · Thumb↔hook: K — 「片道2万」「完全個室」 đều có ở 0–5s; 「11席だけ」「極上シート」 lấy từ mô tả.
- Vì sao giữ người: Con số giá vô lý nói ra thành câu thoại ở giây 0 + niềm tin cũ “không bao giờ đi lại” (H14) + bạn thách “có còn như xưa không” → người xem ở lại để xem niềm tin sụp.
- Điểm yếu: Không phải list N選 (ngoại lệ duy nhất ≥85k trong 20 video). Không có hook_marker nên gate hook_chars của h2dev không đo được dạng video này.

#### 【漫画】定年後は一人旅が最高、60代から一度は行きた有名の温泉地5選 — https://www.youtube.com/watch?v=_G9s-Ig6-E8
- Câu chốt (29.0s): 「でもね、1人で来ても1人で帰るとは限りませんから。」
- Câu khoá (36.6s): 「え、まあ、そのうち分かりますよ。この時の俺にはその言葉の意味が分からなかった。」
- Chữ thumbnail: băng đen trên: 「60代」(vàng)「は一人旅が」(trắng)「最高」(đỏ) | 2 khung: biển 「日本三古泉」 (道後/有馬 — hạng 4/3) và biển 「銀山温泉」 (= 第5位) — giấu 草津 hạng 1 | bong bóng dọc 「気楽に行ける！」「これぞ贅沢！」 | dòng đỏ dưới 「日本の名湯5選」 | 2 mặt thư thái · Mô tả: 定年後、自由な時間が増えたら一人でゆっくり旅をしてみたいと思ったことはありませんか？
- Hook↔tiêu đề: K — 「定年後は一人旅が最高」 = câu hỏi của hook (0–9s: một mình có vui không); 「温泉地5選」 chưa có trong 120s (5つ ở ~297s). · Thumb↔tiêu đề: K — Băng trên 「60代は一人旅が最高」 + 「日本の名湯5選」 = 2 vế tiêu đề (温泉地 → 名湯). · Thumb↔hook: P — Hook nói “lúc đầu thấy cô đơn”; thumbnail đã là kết quả 「気楽に行ける！」「これぞ贅沢！」 — đúng hướng nhưng là phần thưởng chứ không phải cảnh mở.
- Vì sao giữ người: Câu đố của người đi trước (~29s) đặt ngay sau lời thú nhận “cô đơn” → người xem muốn biết “không về một mình” nghĩa là gì; lời hứa list chỉ đến ở ~300s.
- Điểm yếu: Tiêu đề lỗi chính tả 「行きた」「有名の温泉地」 vẫn 85k — đề tài 温泉 kéo. Thumbnail không trả lời câu đố của hook.

#### 【漫画】年金は何歳から受け取るべき？60歳、65歳、70歳、75歳、知らないと後悔する受給年齢の落とし穴 — https://www.youtube.com/watch?v=YKjWwJZrKXY
- Câu chốt (0.2s): 「年金受給は60歳では早すぎる。でも75歳まで待つのは遅すぎる。だったら普通に65歳でいい。俺はずっとそう思っていた。」
- Câu khoá (64.0s): 「60歳でも後悔して65歳でも後悔する。それなら遅くもらえば正解なのか。(…)全員が損を避けようとして全員が迷っているなら年金は何歳からが正解なんだ。」
- Chữ thumbnail: băng đen trên: 「年金」(vàng)「何歳が正解？」(trắng) | 1 khung: ông ôm đầu, mặt khổ | bong bóng dọc 「知らなかった…」 | dòng dưới 「間違うと」(trắng)「老後貧乏」(đỏ) | KHÔNG có mặt thư thái nào · Mô tả: 年金は60歳・65歳・70歳・75歳、何歳から受け取るのが正解なのでしょうか？
- Hook↔tiêu đề: K — Tiêu đề liệt kê 60/65/70/75 tuổi; hook 0–55s đưa đúng các mốc đó qua từng giọng, câu khoá 64s = câu hỏi tiêu đề. · Thumb↔tiêu đề: K — Băng trên 「年金 何歳が正解？」 = 「年金は何歳から受け取るべき？」 rút gọn. · Thumb↔hook: P — Câu hỏi khớp câu khoá 64s, nhưng 「老後貧乏」 không có trong hook (hook nói 後悔, không nói nghèo).
- Vì sao giữ người: K11 “lựa chọn nào cũng hối hận” (35,8s) chặn đường đoán nhanh; về cơ chế hook ổn ngang BeIZhu1I4Tw (cùng 8/12).
- Điểm yếu: 1.159 view: thua vì ĐỀ TÀI (tiền/lương hưu trừu tượng, lệch lời hứa vui-rẻ của kênh), tiêu đề 52 ký tự dài nhất kênh, thumbnail chỉ có mặt khổ + câu doạ 「間違うと老後貧乏」 — KHÔNG phải vì hook.

#### 【漫画】定年後、一流だけがやっている休日の過ごし方5選【世間の非常識】 — https://www.youtube.com/watch?v=_D8qcebhsPU
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: băng đen trên: 「定年後、」(vàng)「休日の過ごし方」(trắng) | 2 khung: nằm sofa cười to / vươn vai mặt thư thái | bong bóng dọc 「ダラダラする」「予定ゼロ」 | dòng dưới 「一流」(đỏ)「は」「これをやる」(đỏ) · Mô tả: 定年後、毎日が自由になったはずなのに、なぜか疲れる。
- Hook↔tiêu đề: — — không lấy được transcript (IpBlocked, không có trong transcripts.json) · Thumb↔tiêu đề: K — Băng trên 「定年後、休日の過ごし方」 chép vế đầu tiêu đề; 「一流はこれをやる」 = 「一流だけがやっている」. · Thumb↔hook: — — không lấy được transcript
- Vì sao giữ người: Gói đăng là nghịch lý “người hạng nhất thì ĐÀN ĐÀ, không lịch” (ダラダラする/予定ゼロ + 【世間の非常識】) — cùng cơ chế với AOe (第1位 何もしない). 26.720 view sau ~7 giờ (đăng 2026-09-23 03:00 UTC, raw tải 17:06 giờ máy) — mở màn nhanh nhất trong các số có được.
- Điểm yếu: Không có transcript nên không chấm hook.

#### 【漫画】６０代だから話せる、人生最大の失敗。それでも人生は終わらなかった — https://www.youtube.com/watch?v=rapoUAXE7y8
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: băng đen trên: 「定年後だから話せる」 (toàn vàng, không cụm đỏ) | 1 khung: cụ hói tay đặt ngực, mỉm cười, trời xanh | bong bóng 「何とかなった」 | dòng đỏ dưới 「人生最大の失敗」 · Mô tả: 60代になった今だからこそ話せる、人生で忘れられない失敗。
- Hook↔tiêu đề: — — không lấy được transcript · Thumb↔tiêu đề: P — Dòng dưới 「人生最大の失敗」 chép tiêu đề, nhưng băng trên đổi 「６０代だから話せる」 thành 「定年後だから話せる」; mô tả lại nói nhân vật 70 tuổi — 3 chỗ 3 mốc tuổi. · Thumb↔hook: — — không lấy được transcript
- Vì sao giữ người: —
- Điểm yếu: 4.230 view sau 3 ngày: đề tài trừu tượng (人生・失敗, không N選, không hành động cụ thể) — đúng loại luật lane cấm; băng trên không có cụm đỏ; 1 khung.

#### 【漫画】定年後、年金だけでは不安な人へ…65歳から始めやすい最強バイト5選 — https://www.youtube.com/watch?v=H-Dk8XBmw90
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: băng đen trên: 「定年後」(vàng)「の最強バイト」(trắng) | 2 khung: bảo vệ bãi xe nhìn màn hình / tài xế ngả ghế, 2 mặt thư thái | bong bóng dọc 「見るだけ」「座ってるだけ」 | dòng dưới 「気楽に働ける仕事5選」 (đỏ viền trắng) · Mô tả: 定年後、もう週5日で働くのはしんどい。でも年金だけでは少し不安…そんな悩みを抱える60代は少なくありません。
- Hook↔tiêu đề: — — không lấy được transcript · Thumb↔tiêu đề: K — 「定年後の最強バイト」 + 「…仕事5選」 = 2 vế tiêu đề. · Thumb↔hook: — — không lấy được transcript
- Vì sao giữ người: Gói đăng đúng khuôn (N選, 2 khung, bong bóng “chỉ ngồi/chỉ nhìn”).
- Điểm yếu: 7.560 view sau 5 ngày dù đúng khuôn thumbnail: đề tài là LÀM THÊM vì 「年金だけでは不安」 — động cơ lo tiền, ngược lời hứa vui/rẻ/tự do của kênh.

### Các tập của mình

10 tập đều là N選 vui/rẻ (đúng đề tài thắng của kênh) và tiêu đề 36–43 ký tự (kênh 33–45) — phần ĐỀ TÀI đã đúng. Chỗ lệch nằm ở THỨ TỰ 60 giây đầu và ở GÓI ĐĂNG. (1) Mở 0s bằng nghịch lý: 10/10 ✓ (kênh 7/7). (2) Người khác nói câu tiền đề ≤35s: 4/10 (ep01 24s thật, ep04 0s, ep08 0s, ep09 30s) — kênh 5/7; 6 tập còn lại câu mạnh nhất của người dẫn đường nằm ở 91–245s (ep02 「暇つぶしに、金を払うのか」 ~194s, ep05 宮田 ~191s, ep07 諸星 ~214s, ep03 鵜飼 ~245s). (3) K03 「この時の俺はまだ知らなかった」 ≤48s: 1/10 (ep09 33s; ep01 54s sát ngưỡng) — kênh 5/7; 8/10 tập đặt ở 97–152s, SAU 60–90 giây tiểu sử. (4) Tự giới thiệu: 7/10 tập ở ≤22s (6,5–22s) — kênh trung vị 42s, tức mình kể tiểu sử TRƯỚC khi có lý do để nghe. (5) Lõi tiêu đề nói ra trong 30s: 5/10 K (ep01, 04, 07, 08, 10), 5/10 P (ep02 1000円 ~263s, ep03 城下町 ~273s, ep05 距離 ~101s, ep06 無料 ~249s, ep09 図書館 ~195s). (6) Lời hứa gãy trong tiêu đề (grep script.txt): 3/10 — ep06 「1円も使わず」 bị script phủ nhận (「電車代も宿代もかかる」) và 「若返る」 bị phủ nhận (「若返った、と胸を張る気はない」); ep07 「節約なのに」 bị nói nước đôi; ep02 「趣味」「夢中」 0 lần; thêm ep05 「静かに楽しく」 0 lần. (7) Mục 1: ep02–ep10 ước 247–296s (trong dải kênh 226–356s); ep01 465s thật — muộn hơn mọi video kênh. (8) Gói đăng: 9/10 không có thumbnail, 10/10 không có thumb_text.txt, 10/10 không có mô tả thật (ep09 TIEU_DE_MO_TA.txt chỉ chép tiêu đề); ep01 là tập duy nhất có final.mp4 nhưng thiếu cả thumbnail lẫn mô tả. Thumbnail duy nhất (ep09) có băng trên không lấy chữ tiêu đề (kênh 10/10 lấy), bong bóng ngang che mắt, chỉ hiện 第5位. (9) Trùng lặp giữa các tập (người xem xem liền kênh sẽ thấy): ラジオ体操 ở ep01/ep02/ep08, 図書館 ở ep02 (第2位)/ep07 (2つ目)/ep09; nhân vật làm công ty 段ボール ở ep03/ep05/ep08; tên 柴崎 ở ep04 (người dẫn đường), ep05 (nhân vật chính), ep06 (người dẫn đường). Gate h2dev hook_chars [1200,2300] + hook_marker 1つ目/第5位: KHỚP kênh ở vĩ mô (kênh 1.363–2.089 chữ trước mục 1; ep02–10 là 1.324–1.586 ✓; ep01 2.452 vượt trần) nhưng MÙ với 0–60s — nó không thấy câu người khác ở giây mấy, K03 ở giây mấy, lõi tiêu đề có trong 30s không; và 3/10 video kênh (ASBV 108k, rapoU, YKjW) không có marker nên gate không áp được cho dạng trải nghiệm/không-list. Đề nghị thêm 3 kiểm: giọng người khác ≤35s, K03 ≤50s, chữ lõi tiêu đề ≤30s.

#### Tập 01 — 【漫画】60代から始める「朝の習慣」5選…1年後、体と気持ちが驚くほど軽くなる理由
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep01-asa-shukan` · có final.mp4 (21/09) + review_vi.mp4; THIẾU TIEU_DE_MO_TA.txt, thumb_text.txt, thumbnail — chưa đăng được · ưu tiên cao (Video đã xong nhưng thiếu cả thumbnail lẫn mô tả — việc nhỏ, chặn đăng. Hook đã đúng khuôn bgUq (H08 16s + người khác nói 24–39s) nên không cần sửa lời.)
- Mốc: chốt 16.1 · giới thiệu 60.8 · hứa 31.9 (voice.srt thật (「五つある」 5:47 = 347s, 「一つ目」 7:45 = 465s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: K — 「朝にな、小さいことを、いくつかやってるだけだ」(28,6–33,3s) + 「誰でもできる。金もかからん」(37,7s) = 朝の習慣; mốc 「1年後」 có thật ở kết (「そして一年。体は五キロ軽く」 ~21 phút). · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- Vấn đề: Gói đăng chưa có: không TIEU_DE_MO_TA.txt, không thumb_text.txt, không ảnh thumbnail — tập DUY NHẤT đã có final.mp4 lại là tập chưa đăng được.
- Vấn đề: Mục 1 「一つ目」 ở 465s (7:45, srt thật) — muộn hơn cả 6 video list của kênh (226–356s). Hồi 1+2 = 2.452 chữ (không tính khoảng trắng), vượt trần gate hook_chars 2300.
- Vấn đề: Câu báo trước 「だが当時の俺は、その意味をまだ理解していなかった」 ở 54,2s — trong khung kênh (29–48s) nhưng tới 60,8s mới tự giới thiệu, rồi 60–120s tiểu sử (食品卸 40 năm, vợ mất, xe đạp) trước khi có 「五つある」 ở 347s.
- **Sửa:** Làm gói đăng theo bgUqNHYZbq0: băng trên lấy chữ tiêu đề, ví dụ 「60代の{朝の習慣}」 với 1 cụm ĐỎ (kiểu 「最強の」/「共通点」); 2 khung là 2 mục giữa (「三つ目」 ラジオ体操 · 「四つ目」 朝の散歩), GIẤU 「五つ目」 何もしない十分間 (cú lật hướng nội); dòng đỏ dưới 「※金もかからない」 (lời 大場 37,7s).
- **Sửa:** Mô tả theo khuôn kênh (xem formula.description): câu 1 hỏi thẳng 「定年後、朝起きても何もすることがない…と感じていませんか？」; đoạn 2 「64歳の男性が、同い年なのに10歳若く見える友人から…」; đoạn 3 liệt kê 水・朝日・ラジオ体操・散歩, giấu mục 5.
- **Sửa:** KHÔNG dựng lại video để dời mục 1 — đã render xong; chỉ ghi nhận cho tập sau: mục 1 nên ≤356s.
- Video mẫu: bgUqNHYZbq0

#### Tập 02 — 【漫画】定年後、月1000円以下で夢中になれる趣味5選…暇な毎日が待ち遠しくなった
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep02-1000yen-shumi` · chỉ có script.txt LOCK (chưa giọng/ảnh/video) · ưu tiên vừa (Hook khung đúng (0s nghịch lý) nhưng câu của người khác + lời hứa 1000円 muộn ~4 phút; chưa ghi giọng nên dời đoạn còn rẻ.)
- Mốc: chốt 0.0 · giới thiệu 7.8 · hứa 252 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: P — Mở 0s 「自由になったはずなのに、財布だけが忙しい」 = rò tiền vì rảnh (khớp 「暇な毎日」), nhưng lõi tiêu đề 「月1000円以下」 ở ~263s (「予算枠は月に1000円まで」), chữ 「趣味」 và 「夢中」 không có lần nào trong script. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- ⚠ Lời hứa không giữ: 「趣味」 (tiêu đề) — 0 lần trong script.txt; người dẫn đường gọi là 「金のかからない過ごし方が、五つある」 (~252s).
- ⚠ Lời hứa không giữ: 「夢中になれる」 — 0 lần 「夢中」.
- Vấn đề: Câu “sát thủ” của người dẫn đường 三枝 「暇つぶしに、金を払うのか」 ở ~194s — đúng câu AOe-E69mLzA đặt ở 14,6s (「お前は暇を潰そうとするから金がかかるんだよ」).
- Vấn đề: Điều kiện của danh sách 「担当は自分一人。誰かに頭を下げる工程はゼロ。予算枠は月に1000円まで」 ở ~259–266s — AOe đặt ở 20–26s.
- Vấn đề: Từ 8s tới ~146s là tiểu sử + cảnh tiêu tiền (ゴルフ練習場/喫茶店/本屋/通販) do chính nhân vật kể; giọng người khác đầu tiên là vợ ở ~99s. K03 「この時の俺はまだ知らなかった。空欄は、埋めなくていいということを」 ở ~142s (kênh 29–48s).
- Vấn đề: Trùng tập khác: 第2位 「平日の昼間から、図書館で本を読む」 (~827s) trùng đề ep09; 第1位 「朝のラジオ体操と、目的を決めない散歩」 (~997s) trùng ep01 三つ目/四つ目 và ep08 1つ目.
- **Sửa:** Giữ câu 0s; đưa cảnh ダイソー + câu 「暇つぶしに、金を払うのか」 lên ~10–15s (khuôn AOe 14,6s). Câu mở mẫu: 「暇つぶしに、金を払うのか」——ダイソーの園芸棚の前で、元上司の三枝さんにそう言われた。
- **Sửa:** Đưa điều kiện 「担当は自分一人…予算枠は月に1000円まで」 lên ngay sau (~20–25s) — đây là chỗ nói ra 「1000円」 của tiêu đề.
- **Sửa:** K03 dời lên ~30s, tự giới thiệu 「俺の名前は榊原隆志、65歳」 sau K03 (~35–45s), tiểu sử + cảnh tiêu tiền để sau.
- **Sửa:** Tiêu đề: đổi 「趣味」 thành cụm có trong script (「過ごし方」) HOẶC cho 三枝 nói chữ 趣味 một lần; bỏ 「夢中」 nếu không có cảnh nào gọi đúng như vậy. Thumbnail: 「定年後、{最強の}過ごし方」 + dòng đỏ 「※月1000円以下」, 2 khung 第3位 俳句投稿 / 第2位 (đổi mục trùng ep09) — giấu 第1位.
- Video mẫu: AOe-E69mLzA

#### Tập 03 — 【漫画】定年後の一人旅は平日が最高…60代が歩くべき「静かな城下町」5選
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep03-jokamachi` · chỉ có script.txt LOCK · ưu tiên vừa (Tiêu đề và kịch bản khớp, không lời hứa gãy; chỉ cần dời 1 câu thoại + K03.)
- Mốc: chốt 0.0 · giới thiệu 22.0 · hứa 273 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: P — 「平日にゆっくり城でも見て回る」 ở ~6s và 「いつでも行ける。だから今日は、行かなくていい」 ~12s khớp 「平日が最高」; 「一人旅」 ở ~146s, 「城下町…五つ」 ở ~273s. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- Vấn đề: Mâu thuẫn 0–17s chép đúng BeIZhu1I4Tw (~32s 「いつでも行けると思うから今日じゃなくていい」) — tốt; nhưng câu của đồng nghiệp 松ヶ根 「俺は膝をやった…あの石段はもう無理だ」 tới ~92–105s (BeIZ ~54s).
- Vấn đề: K03 「この時の俺はまだ知らなかった。この一人旅が、俺の「いつか」を根こそぎ変えてしまうことを」 ở ~142s.
- Vấn đề: Câu mạnh nhất về lời hứa 「笹岡さんは城を見たんじゃなくて、城の前を通過したんですね」 (鵜飼, ~245s) nằm sau 4 phút.
- Vấn đề: 40–77s là tả đồng hồ + sách 城めぐり trong ngăn kéo — không có mâu thuẫn mới.
- **Sửa:** Cắt/dời đoạn 40–77s; đặt câu 松ヶ根 (膝・石段) ở ~25–35s như BeIZ đặt câu đồng nghiệp ~54s nhưng sớm hơn vì mở đầu của mình ngắn hơn.
- **Sửa:** K03 lên ~40s; có thể nhắc 「平日に静かに歩ける城下町」 trong K03 để lời hứa tiêu đề có mặt trước 60s.
- **Sửa:** Thumbnail: 「60代は{城下町}が最高」 + dòng đỏ 「静かな城下町5選」, 2 khung 第3位 郡上八幡 / 第2位 萩, giấu 第1位 竹田 (khuôn BeIZ/_G9s).
- Video mẫu: BeIZhu1I4Tw

#### Tập 04 — 【漫画】60代から夜ぐっすり眠れるようになった「夕方の習慣」5選…薬に頼らず朝が変わる
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep04-yugata-suimin` · chỉ có script.txt LOCK · ưu tiên thấp (Hook đã có giọng người khác ở 0s và tiêu đề khớp; chỉ tối ưu vị trí K03.)
- Mốc: chốt 0.0 · giới thiệu 9.3 · hứa 277 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: K — 0s 「年のせいじゃない。夕方のせいだ」 = 「夕方の習慣」; 「3時に目が覚める」 ~52s, 「睡眠薬をもらおうかと」 ~73s = 「夜ぐっすり」「薬に頼らず」. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- Vấn đề: Câu người khác ở 0s (H17) nhưng người nói (柴崎) chỉ lộ mặt ở ~162–170s; giữa đó 110 giây tiểu sử + triệu chứng không quay lại câu đố.
- Vấn đề: K03 「この夕方の居眠りが、夜中の3時につながる大きな原因の一つだった」 ở ~119s — câu này chính là lời giải hé 20–40% (loại E) nhưng đến quá muộn.
- Vấn đề: Cụm 「夕方の習慣」 của tiêu đề không có nguyên văn trong script (chỉ có 夕方 riêng lẻ).
- **Sửa:** Sau câu 0s, cho biết ai nói trong ≤15s (khuôn bgUqNHYZbq0: bạn cùng tuổi trông khác hẳn — 柴崎 「いつも顔色が悪く、胃薬を手放さなかった」 nay 「背筋…」).
- **Sửa:** Dời K03 (dòng 夕方の居眠り→夜中の3時) lên ~35–45s, trước phần tả 9時就寝/3時覚醒.
- **Sửa:** Thumbnail: 「60代、夜{ぐっすり}」 + dòng đỏ 「※薬に頼らない」; 2 khung 三つ目 ぬるめの風呂 / 四つ目 スマホを置く; giấu 五つ目 「早く寝ようとしない」.
- Video mẫu: bgUqNHYZbq0

#### Tập 05 — 【漫画】定年後の夫婦が「ちょうどいい距離」を保つ暮らし方5選…毎日が静かに楽しくなる
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep05-fufu-kyori` · chỉ có script.txt LOCK · ưu tiên vừa (Lõi tiêu đề 距離 chỉ tới ở 101s, câu mạnh nhất nằm ở 191–222s; 1 lời hứa phụ trong tiêu đề không có trong script.)
- Mốc: chốt 0.0 · giới thiệu 9.9 · hứa 245 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: P — 0–5s 「金も、体も、夫婦仲も、何ひとつ問題はない…なのに…居場所を探していた」 khớp 夫婦; chữ 「距離」 đầu tiên ở ~101s, 「ちょうどいい距離」 chỉ 1 lần ở câu kết (~1133s). · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- ⚠ Lời hứa không giữ: 「毎日が静かに楽しくなる」 — 「静かに」 và 「楽しく」 đều 0 lần trong script.txt (kết là 「ちょうどいい距離を、自分で選んで生きていく」).
- Vấn đề: Mở 0s chép đúng khung _EhPtM6cRFk (tiền/sức khoẻ/vợ đều ổn mà vẫn thiếu) nhưng _EhP có K03 ở ~31s, mình ~97s; giữa đó 10–90s là tiểu sử (段ボール 40 năm, 資材課長, vợ 62 tuổi 花屋, 手芸).
- Vấn đề: Không có giọng người khác trong 90s; người dẫn đường 宮田 xuất hiện ~191s với câu rất mạnh 「あんた、会社を辞めてから、奥さんとの距離を、はかり間違えてる顔だな」 và ~222s 「定年で変わるのは、金でも体でもない。人との距離だ」.
- Vấn đề: Tên 柴崎 dùng cho nhân vật chính ep05 nhưng cũng là người dẫn đường ở ep04 và ep06; 3 tập (ep03, ep05, ep08) nhân vật đều làm công ty 段ボール.
- **Sửa:** Giữ câu 0–5s, đưa ngay câu 宮田 「…奥さんとの距離を、はかり間違えてる顔だな」 lên ~10–15s, rồi 「何が足りないのか。金でも、健康でもない。この時の俺はまだ知らなかった。足りないのは「距離」だということを」 ở ~25–35s (khuôn _EhP 20–31s); tiểu sử sau đó.
- **Sửa:** Tiêu đề: bỏ 「静かに楽しくなる」 hoặc thay bằng vế có thật trong script; thumbnail theo đúng _EhP: 「定年後、夫婦の{距離}」 + dòng đỏ 「お金や体ではない」 (lời 宮田 ~222s) — 2 khung 三つ目 台所に俺の担当 / 四つ目 妻の予定を管理しない, giấu 五つ目.
- Video mẫu: _EhPtM6cRFk

#### Tập 06 — 【漫画】60代から一度は歩きたい「無料の絶景散歩道」5選…1円も使わず体が若返る
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep06-muryo-sanpo` · chỉ có script.txt LOCK · ưu tiên cao (2 lời hứa trong tiêu đề bị chính kịch bản phủ nhận nguyên văn — sửa rẻ (chỉ đổi chữ) nhưng để nguyên là người xem bắt lỗi.)
- Mốc: chốt 0.0 · giới thiệu 6.5 · hứa 252 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: P — Tấm bưu thiếp 「いつか歩く」 (~36–41s) hé chủ đề đi bộ; 「無料」 đầu tiên ~249s, 「1円」 ~335s; 「絶景」 và 「散歩道」 0 lần. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- ⚠ Lời hứa không giữ: Tiêu đề 「1円も使わず」 nhưng script ~245s 「電車代も宿代もかかる。でも、通行料は0円」, ~335s 「宿代は出る。でも、道そのものは1円も取らない」, và nhân vật mua vé đặc cấp đi 木曽 (~136–142s) — chính kịch bản phủ nhận tiêu đề.
- ⚠ Lời hứa không giữ: Tiêu đề 「体が若返る」 nhưng script ~1248s 「若返った、と胸を張る気はない」 — phủ nhận nguyên văn.
- ⚠ Lời hứa không giữ: 「絶景」「散歩道」 — 0 lần trong script.txt.
- Vấn đề: Câu đồng nghiệp 大久保 「行けるうちに行っとけ。体は待ってくれんぞ」 ở ~91–100s (khuôn BeIZ ~54–60s).
- Vấn đề: K03 「この一枚の絵はがきが、俺の朝を丸ごと変えてしまうことを」 ở ~128s.
- Vấn đề: Câu người dẫn đường mạnh nhất 「深谷さんは、行った場所の数は多い。でも歩いた道は、まだ一本もない」 ~222s.
- **Sửa:** Sửa tiêu đề trước (rủi ro comment bắt lỗi cao nhất lane): bỏ 「1円も使わず」 và 「若返る」, thay bằng điều script nói thật — 「通行料0円」/「道そのものは1円も取らない」 và 「ベルトの穴が、ひとつ内側に戻った」 (~1248s).
- **Sửa:** Hook: đưa câu 大久保 lên ~20–30s ngay sau bưu thiếp; K03 ~40s; tiểu sử 運行管理 42 năm để sau.
- **Sửa:** Thumbnail: 「60代、{最高の}古い道」 + dòng đỏ 「※通行料0円」 (KHÔNG ghi 1円も使わず), 2 khung 第3位 高尾山1号路 / 第2位 山の辺の道, giấu 第1位 馬籠→妻籠.
- Video mẫu: BeIZhu1I4Tw

#### Tập 07 — 【漫画】定年後の食費が楽しみに変わる「台所の習慣」5選…節約なのに毎日が待ち遠しい
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep07-daidokoro` · chỉ có script.txt LOCK · ưu tiên vừa (Hook 0s tốt, nhưng lời hứa 「節約」 bị kịch bản nói nước đôi.)
- Mốc: chốt 0.0 · giới thiệu 8.6 · hứa 235 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: K — 0s 「定年して一番増えた出費は、旅行でもゴルフでもなく、昼飯だった」 = 「食費」; 「冷蔵庫を開けても、何をどうすればいいかわからない」 ~55s = 台所. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- ⚠ Lời hứa không giữ: 「節約なのに」 — script ~961s 「それは、節約になるのか」「なるかもしれないし、ならないかも」: kịch bản né đúng lời hứa; 「食費」 chỉ xuất hiện 1 lần dưới dạng câu hỏi (~601s 「本当にこれで、食費が変わるのか」).
- Vấn đề: Câu mở 0s mạnh (loại C) nhưng 8,6–99s là tiểu sử + ngày trống do chính nhân vật kể; giọng người khác đầu tiên là vợ ~132s, người dẫn đường 諸星 ~183s.
- Vấn đề: Câu lật cách nghĩ 「あんた、飯を『出てくる物』だと思ってるだろう」 (~214s) và 「足りないのは、金でも暇でもない」 (~225s) — cùng vai trò câu 佐藤さん AOe 14,6s nhưng muộn 3,5 phút.
- Vấn đề: K03 ~99s.
- **Sửa:** Sau câu 0s, đưa câu 諸星 「飯を『出てくる物』だと思ってるだろう」 lên ~15–20s; K03 ~30s; tự giới thiệu ~35–45s.
- **Sửa:** Tiêu đề: giữ 「節約」 chỉ khi thêm 1 câu có số tiền giảm thật trong kịch bản; nếu không, đổi vế sau sang điều có thật (~1173s 「夕方の買い物が待ち遠しい」).
- **Sửa:** Thumbnail: 「定年後、台所の{習慣}」 + dòng đỏ 「一番の出費は昼飯」 (câu 0s), 2 khung 三つ目 だしをとる / 四つ目 期限表示を読む, giấu 五つ目.
- Video mẫu: AOe-E69mLzA

#### Tập 08 — 【漫画】60代の体が軽くなる「歩き方」5つのコツ…毎日の散歩が一番の薬になった
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep08-arukikata` · chỉ có script.txt LOCK · ưu tiên thấp (Hook khớp tiêu đề và khung kênh tốt nhất sau ep01; chỉ dời 2 câu.)
- Mốc: chốt 0.0 · giới thiệu 41.8 · hứa 232 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: K — 0s 「秘訣なんてない。毎朝、歩いてるだけだ」 + 13,8s 「同い年のはずなのに…若く見えた」 = 「歩き方」「体が軽くなる」. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- Vấn đề: Khung 0–42s gần đúng bgUqNHYZbq0 (bạn cùng tuổi trẻ hơn, câu 「秘訣なんてない」 ≈ 「特別なことはしていないよ」, tự giới thiệu 41,8s ≈ 52,7s). Chỗ lệch: bgUq nói 「誰でもできる簡単な7つのこと」 ở 36s, mình 「金はかからん。ただ、5つある」 ở ~232s.
- Vấn đề: K03 「諦めた場所のすぐ先に、一番安い薬が、転がっていたことを」 ở ~152s (bgUq 42s).
- **Sửa:** Đưa 「金はかからん。ただ、5つある」 vào đoạn thoại 0–35s (ngay sau 「それで、これだけ差がつくのか」 ~34s).
- **Sửa:** Đưa K03 (一番安い薬) lên ~38s, trước 「俺の名前は柏木誠一」.
- **Sửa:** Thumbnail kiểu bgUq: 「60代、{老けない}歩き方」 + 2 khung 2つ目 姿勢 / 3つ目 歩幅半足; KHÔNG in 「速く歩くな」 (là 5つ目, mục cuối).
- Video mẫu: bgUqNHYZbq0

#### Tập 09 — 【漫画】定年後に人生が変わった「図書館の使い方」5選…実は0円で一番贅沢な場所
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep09-toshokan` · script.txt LOCK + thumbnail_final.png (bản C, THUMB.json chosen C, published=false); TIEU_DE_MO_TA.txt chỉ có 1 dòng tiêu đề · ưu tiên cao (Tập đi đầu ở khâu gói đăng (đã chọn thumbnail C) nhưng thumbnail không nói 図書館/0円, bong bóng che mắt, mô tả trống — sửa trước khi đăng.)
- Mốc: chốt 0.0 · giới thiệu 41.4 · hứa — (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep09-toshokan\thumbnail_final.png (07:57, 801.000 byte = y hệt research\thumb\final_set\thumbnail_C.png). Bản cũ: thumbnail_final.png.bak.20260923-075050 (「外出の欄が飲み代より多い｜妻の家計簿｜暇に金を払っていた」, không băng đen, chữ mảnh) và .bak.20260923-075753 (cùng chữ bản C nhưng có dải đỏ ở đáy). Không có DANG-TAI.txt. — băng đen trên: 「買った本」(vàng)「は積むだけ」(trắng) | nhãn vàng 「第5位」 | bong bóng NGANG 「真剣に読むのね」 đè lên mắt nhân vật khung phải | dòng đỏ dưới 「本屋に行くな」 | khung trái ôm má hoảng, khung phải cười đọc sách + vợ
- Tiêu đề↔hook: P — Khung 0–41s đúng AOe (nghịch lý 「時間が余るほど、財布が軽くなる」 0s → 「暇は敵じゃない」 29,7s → 「当時の俺にはわからなかった」 33,2s → tự giới thiệu 41,4s) nhưng lõi tiêu đề vắng: 「図書館」 đầu tiên ~195s, 「0円」 ~622s, 「贅沢」 ~1026s. · Thumb↔tiêu đề: P — Băng trên 「買った本は積むだけ」 không dùng chữ nào của tiêu đề (kênh: 10/10 băng trên lấy từ tiêu đề); không có 図書館 hay 0円; chỉ 「本屋に行くな」 ngầm chỉ thư viện. · Thumb↔hook: L — Trong 0–90s không có sách/hiệu sách; cảnh 「本屋で本を衝動買いする。読まない本が、居間に積み上がった」 ở ~122s, 「本屋に行くのをやめろ」 (第5位) ở ~282–290s.
- Vấn đề: Tiêu đề hứa 図書館/0円 nhưng hook 90s chỉ nói tiền rò + 「暇は敵じゃない」; điều kiện của danh sách 「ひとりでできること。誰にも迷惑をかけないこと。金がかからないこと」 ở ~255s (AOe đặt 20–26s).
- Vấn đề: Thumbnail: băng trên không lấy chữ tiêu đề; bong bóng ngang che mắt nhân vật (kênh: bong bóng dọc hình oval cạnh mặt 8/10); chỉ hiện 1 hạng (第5位 = mục yếu nhất) thay vì các hạng giữa rồi giấu hạng 1 như bgUq/AOe/BeIZ/_G9s.
- Vấn đề: Không có mô tả.
- Vấn đề: h2dev đang thử hook_stage 20–30s cho chính đề này: _test-hook-fable khoá 「「お前、毎日どこへ行ってるんだ」…「0円だ。一番贅沢な場所に通ってる」…そんな場所が、この町のどこにある。」 (158 chữ ≈ 29s) — khớp khung kênh (giọng người khác 0s, lời hứa 0円 ~15s, câu hỏi mở); _test-hook-upstream khoá 「「ここ、いくらかかるんですか」…0円ですよ…」 (182 chữ ≈ 34s) nói 図書館 ở ~18s nhưng script thử của nó vẫn để K03 ở ~164s và 「5つ」 ~268s.
- **Sửa:** Hook: sau 「暇は敵じゃない」 (29,7s) đưa điều kiện 3 vế + 「0円」 lên ~35s (khuôn AOe 20–26s); hoặc dùng bản hook đã khoá ở _test-hook-fable (lời hứa 0円/一番贅沢 trong 30s).
- **Sửa:** Thumbnail theo AOe/bgUq: băng trên 「定年後、{図書館}が最強」 (1 cụm đỏ), dòng đỏ 「※0円で一番贅沢」 hoặc giữ 「本屋に行くな」; 2 khung 第3位 司書に聞く / 第2位 CD・DVDを平日に — giấu 第1位 「ただ座る」; bong bóng dọc đặt cạnh mặt, không đè mắt.
- **Sửa:** Mô tả: câu 1 「定年後、暇つぶしのたびにお金が出ていく…と感じていませんか？」; đoạn 2 「65歳の男性が、先に定年した大迫さんから…」; đoạn 3 liệt kê 取り寄せ・新聞・司書・CD/DVD, giấu 第1位.
- Video mẫu: AOe-E69mLzA

#### Tập 10 — 【漫画】60代の一人旅で行くべき「日帰り温泉のある小さな町」5選…平日ならほぼ独り占め
- Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep10-higaeri-onsen` · chỉ có script.txt LOCK · ưu tiên vừa (Hook đúng khuôn, chỉ chậm 25s do 1 đoạn tả; sửa bằng cắt, không viết mới.)
- Mốc: chốt 18.1 · giới thiệu 70.9 · hứa 292 (ước tính = số chữ (bỏ khoảng trắng) trong script.txt ÷ 321,5 chữ/phút × 60 (đối chứng ep01: 俺の名前は ước 59,0s vs voice.srt 60,8s))
- Thumbnail: không có file thumbnail nào trong thư mục tập — —
- Tiêu đề↔hook: K — 5,6–18s 「和歌山の山あいの湯船に、一人で浸かっている。平日の昼、湯の峰温泉の公衆浴場…客は俺一人」 = 「平日ならほぼ独り占め」 dựng thành cảnh. · Thumb↔tiêu đề: — — chưa có thumbnail · Thumb↔hook: — — chưa có thumbnail
- Vấn đề: Khung chép _G9s-Ig6-E8 (lần đầu tắm suối một mình → thú nhận lạc lõng → câu đố của người lạ → 「意味が分からなかった」 → tự giới thiệu) nhưng chậm ~25s ở mọi mốc: câu đố 女将 「お一人さんは、帰りの荷物が増えますよ」 53,9s (_G9s 29s), K03 65,9s (_G9s 37s), tự giới thiệu 70,9s (_G9s 42s).
- Vấn đề: Đoạn chậm là 25–50s: 「正直に言う。落ち着かなかった。…「いい湯だな」…腕時計に目をやった」.
- **Sửa:** Cắt/gộp 25–50s thành 1 câu; để câu 女将 ≤30s, K03 ≤37s, tự giới thiệu ≤45s — đúng nhịp _G9s.
- **Sửa:** Thumbnail kiểu _G9s: 「60代は{一人湯}が最高」 + dòng đỏ 「日帰り温泉5選」 hoặc 「平日はほぼ独り占め」, 2 khung 第3位 別所温泉 / 第2位 城崎温泉 (biển tên trong tranh), giấu 第1位 野沢; bong bóng 「一人でいい」 kiểu 「これぞ贅沢！」.
- Video mẫu: _G9s-Ig6-E8

### Nguyên tắc
- **Đề tài N選 vui/rẻ/đi chơi/sức khoẻ quyết định view nhiều hơn hook; chủ đề tiền-sợ hay trừu tượng chết dù hook tốt.** — cơ chế: Khán giả 60+ của kênh bấm để lấy một danh sách dùng được ngay và để thấy tuổi hưu dễ chịu; đề tài doạ tiền đẩy họ đi (lời hứa kênh là 楽しみ, không phải 不安). · bằng chứng: 20 video kênh: 9 video N選 trung vị 85k vs 11 video không N選 trung vị 7,5k; 6/6 tiêu đề chứa 年金/貧乏/破綻/後悔/失敗/不安 đều ≤16k (YKjWwJZrKXY 1.159, rapoUAXE7y8 4.230, H-Dk8XBmw90 7.560, 61lcBV32roE 11,6k, Or6odB2b70M 12,8k, zHtHiHEcXV0 16k); hook YKjW chấm 8/12 = BeIZhu1I4Tw 172k. · vì sao: Để không sửa hook nhằm cứu một đề tài sai, và không dạy kho rằng kiểu hook K11/H18 yếu. · áp dụng: Giữ 10 tập hiện tại (đều N選 vui/rẻ). Mở bằng rò tiền được (AOe 157k làm vậy) nhưng lời hứa phải là vui/0 yên, không được là “lương hưu không đủ”. Không làm đề 年金/バイト ở lane này (để teinengo-real).
- **Trong ≤35 giây phải có một NGƯỜI KHÁC nói câu làm tiền đề (và ở video list: nói luôn điều kiện của danh sách); nhân vật chính chỉ phản ứng.** — cơ chế: Câu của người đi trước vừa lật niềm tin của khán giả vừa bảo chứng lời hứa (“người thật đã làm được”); nhân vật chính nghi ngờ thay cho người xem nên người xem ở lại để kiểm. · bằng chứng: 5/7 video có transcript: AOe-E69mLzA 14,6s 「お前は暇を潰そうとするから金がかかるんだよ…一円も使わない」 (157k), bgUqNHYZbq0 33s 「特別なことはしていないよ。誰でもできる簡単な7つのこと」 (202k), ASBVa_H_leI 0–29s 「今の夜行バス本当に昔と同じだと思うか?」 (108k), _G9s-Ig6-E8 ~29s 「1人で来ても1人で帰るとは限りませんから」 (85k), YKjWwJZrKXY 15s. Ngoại lệ BeIZ ~54s. · vì sao: Ở tập mình câu này ĐÃ CÓ sẵn trong script nhưng nằm ở 91–245s; dời lên là tăng giữ chân mà không cần viết mới. · áp dụng: ep02 「暇つぶしに、金を払うのか」 194s→~12s; ep05 宮田 191s→~12s; ep07 諸星 214s→~18s; ep03 松ヶ根 92s→~30s; ep06 大久保 91s→~25s; ep10 女将 54s→≤30s; ep09 thêm điều kiện 3 vế 255s→~35s.
- **Câu báo trước 「この時の俺はまだ知らなかった…」 đặt ở 29–48s, SAU câu của người khác và TRƯỚC tự giới thiệu/tiểu sử.** — cơ chế: Nó là điểm cam kết: người xem biết chắc có cú lật nên chịu nghe 60–120s tiểu sử “mới hưu vui, nửa năm sau chán” đi sau nó. · bằng chứng: 5/7: _EhPtM6cRFk ~31s, ASBVa_H_leI ~31s, _G9s-Ig6-E8 ~37s, bgUqNHYZbq0 42,6s (「中村から話を聞いた俺は衝撃を受けた」), AOe-E69mLzA 48,6s; tự giới thiệu trung vị 42s. Tập mình: 8/10 đặt K03 ở 97–152s, 7/10 tự giới thiệu ≤22s. · vì sao: Thứ tự của mình (tiểu sử trước, K03 sau) bắt người xem nghe 60–90s tiểu sử khi chưa có lý do. · áp dụng: Mỗi tập: nghịch lý 0s → câu người khác ≤35s → K03 ≤48s → 「俺の名前は…」 → tiểu sử. Câu K03 đã có sẵn trong mọi script, chỉ dời.
- **Thumbnail tách chính tiêu đề làm 2 dòng: băng đen trên = chữ tiêu đề (vàng + 1 cụm ĐỎ), dòng đỏ viền trắng dưới = vế phần thưởng; tranh hiện các hạng giữa và GIẤU hạng 1; luôn có ≥1 mặt thư thái.** — cơ chế: Người xem đọc cùng một lời hứa ở 2 chỗ nên hiểu trong 1 giây; thấy hạng 3–2 mà không thấy hạng 1 tạo câu hỏi “vậy hạng 1 là gì”; mặt thư thái bán lời hứa 楽しみ. · bằng chứng: Băng trên lấy chữ tiêu đề 10/10; cụm đỏ trong băng trên 5/10 = bgUq, BeIZ, AOe, _EhP, _G9s (5/6 video view cao nhất); 4/4 video xếp hạng soát được giấu hạng 1 (bgUq 第3位/第2位, AOe 5位–2位, BeIZ 稲荷=3位/出雲=2位, _G9s giấu 草津); ảnh duy nhất chỉ mặt khổ = YKjW 1.159 view. · vì sao: Thumbnail duy nhất của mình (ep09) có băng trên 「買った本は積むだけ」 không dính chữ tiêu đề, chỉ hiện 第5位, bong bóng ngang che mắt. Renderer bands_manga (theo BAO_CAO_DO_THUMB_DNA) chỉ tô VÀNG trong băng trên — thiếu cụm ĐỎ mà 5/6 video cao nhất đều có. · áp dụng: Mỗi tập: băng trên 「定年後、{最強の}＋danh từ tiêu đề」 hoặc 「60代は{X}が最高」; dòng đỏ = N選 hoặc vế phần thưởng có thật trong script (ep06 「※通行料0円」, KHÔNG 「1円も使わず」); 2 khung = mục hạng 3 và 2, không in mục cuối; bong bóng dọc cạnh mặt.
- **Chữ lõi của tiêu đề phải được nhân vật nói ra trong ≤36 giây, và mọi vế tiêu đề phải có nguyên văn trong kịch bản.** — cơ chế: Người bấm vào vì một chữ (1円, 2万円, 老けない); nghe thấy nó sớm là xác nhận “đúng video mình tìm”; vế tiêu đề bị kịch bản phủ nhận là mồi cho comment bắt lỗi. · bằng chứng: 6/7 video kênh khớp tiêu đề trong hook: AOe 「一円も使わない」 23s, ASBVa_H_leI 「2万円」 0s, bgUq 「7つのこと」 36s, _EhP 「定年後の生き方」 ~25s, YKjW các mốc tuổi 0–43s, _G9s 一人旅 0s; ngoại lệ BeIZ (神社 không có trong 120s) sống nhờ đề tài tra cứu. · vì sao: Tập mình 5/10 để lõi tiêu đề sau 90s (ep09 図書館 195s, ep06 無料 249s, ep02 1000円 263s) và 3/10 có vế tiêu đề bị script phủ nhận hoặc không có. · áp dụng: Trước khi khoá gói đăng: grep từng vế tiêu đề/thumbnail trong script.txt; vế nào 0 lần hoặc bị phủ nhận thì sửa tiêu đề (rẻ) chứ không để nguyên. Cho người dẫn đường nói chữ lõi trong câu ≤35s.
- **Mô tả 250–500 chữ theo 4 đoạn: hỏi thẳng nỗi đau → nhân vật + tuổi + người dẫn đường → liệt kê các mục trừ mục cuối → câu nhắm 60代・70代; không hashtag.** — cơ chế: Dòng đầu hiện dưới video/ở kết quả tìm kiếm: câu hỏi 「〜ませんか？」 là tấm gương cho người xem; giấu mục cuối giữ tò mò giống thumbnail. · bằng chứng: 10/10 mô tả 247–508 ký tự, 0/10 hashtag; 6/10 câu đầu là câu hỏi; AOe-E69mLzA liệt kê 断捨離・空や雲・議会・昼寝 và giấu mục 1 bằng 「最後にたどり着いたのは…意外な“最高の暇つぶし”」; 8/10 có câu nhắm 60代・70代/「ご覧いただければ幸いです」. · vì sao: 10/10 tập mình chưa có mô tả (ep09 chỉ có tiêu đề). SOP h2dev yêu cầu hashtag #定年後 #60代… trong khi kênh mẫu 0/10 dùng — cần anh chốt theo kênh hay theo SOP. · áp dụng: Viết TIEU_DE_MO_TA.txt theo 4 đoạn trên, dùng đúng tên/tuổi/người dẫn đường/mục trong script; ưu tiên ep01 (đã có video) và ep09.

### Lưu ý dữ liệu
- Mốc giây: bgUqNHYZbq0 và AOe-E69mLzA lấy hook_segments thật trong raw; YKjWwJZrKXY lấy segments thật trong E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneG_from_research\data\transcripts_okane.json; BeIZhu1I4Tw, _EhPtM6cRFk, ASBVa_H_leI, _G9s-Ig6-E8 là ƯỚC TÍNH (vị trí chữ ÷ tổng chữ × thời lượng từ E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougo-money-story\_raw\transcripts.json) — sai số vài giây, nhất là đoạn có nhạc.
- 3 video _D8qcebhsPU, rapoUAXE7y8, H-Dk8XBmw90 không có transcript (raw hook_segments rỗng do IpBlocked, không có trong transcripts.json/transcripts_okane.json) — chỉ phân tích gói đăng, KHÔNG đưa vào file seed. Đã mở lại raw ngay trước khi ghi file: vẫn rỗng.
- Tập của mình: chỉ ep01 có mốc giây thật (voice.srt); ep02–ep10 ước tính theo 321,5 chữ/phút (đối chứng ep01: ước 59,0s vs thật 60,8s).
- View lấy từ raw (tải 2026-09-23); transcripts.json cũ hơn có số view thấp hơn. _D8qcebhsPU mới đăng ~7 giờ nên 26.720 là số mở màn, chưa so được với video cũ.
- Transcript tự động nghe sai: 丁年=定年, 一延=一円, 紐=暇, 阪神半義=半信半疑, ロモ資金=老後資金, わかわかしい=若々しい, 追い=老い. Nguyên văn trong seed giữ như transcript.
- Đếm thumbnail trên 10 ảnh đã mở bằng mắt: nhãn vàng 3/10, bong bóng dọc 8/10 — khác số máy đo trong E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\teinengo-tanoshimi\BAO_CAO_DO_THUMB_DNA.md (nhãn vàng 16/19, bong bóng 12/19 trên 19 ảnh). Báo cáo đó cũng chỉ ghi cụm VÀNG trong băng trên; 5/10 ảnh ở đây có thêm cụm ĐỎ.
- hooks.jsonl đã có bgUqNHYZbq0 (9/12) và AOe-E69mLzA (8/12). Seed này giữ bgUq 9/12, chấm lại AOe 10/12 (khớp thumbnail nguyên văn 1円 + cảnh tiêu tiền dựng hình được), đổi mã AOe từ H17 thành H04+H17 và thêm K18 — cần anh duyệt K18 trước khi chạy hook_library.py add (mã này chưa có trong patterns.json).
- Không đọc được retention; “khác ở đề tài không ở hook” là suy từ số view + điểm hook, không đo giữ chân.
- Không sửa gì trong h2dev, patterns.json, hooks.jsonl, HOOK_LIBRARY.md; không chạy hook_fetch.py.

---

## 老後のゴローさん → lane `teinengo-fuufu`

Kênh: https://www.youtube.com/channel/UCxD2Exs2Q4lf7x0Q28OuKvg

Khuôn 6/6 video top có transcript: cảnh HIỆN TẠI chứa mâu thuẫn trong ≤15s (du thuyền mà vợ chồng không nói câu nào; 70 tuổi cầm cờ giữa nắng trong khi đồng kỳ đi câu) → con số đời nhân vật → câu khoá ≤45s nói trước 'kết quả không như mong đợi' (「これは〜という話だ」 / 「だが〜」 / 「原因は〜じゃない」) → quay về ngày quyết định + tên-tuổi sau giây 30 → gieo 1 câu nhỏ của vợ/người kia sẽ trả ở cuối. Tiêu đề = 【漫画】+tuổi+(夫婦/2 người đối lập)+リアル/現実+câu hỏi とは？; thumbnail = dải đen chữ vàng/trắng chép lõi tiêu đề + (a) 2 panel đối lập có nhãn vàng hoặc (b) 1 cảnh + dòng đỏ đáy = câu khoá hook; mô tả = khối chào kênh cố định, KHÔNG mang nội dung video.

### Khung hook theo giây
- **0–7s · Cảnh hiện tại có mâu thuẫn (event+contradiction trong 1–2 câu)** — Không mở bằng tên. Đặt người xem vào khoảnh khắc tệ nhất của quyết định hưu trí, có số đếm cụ thể; vế mâu thuẫn tới ngay câu thứ 2–3. 6/6 top có câu chốt ≤17s, 5/6 ≤12s. Ví dụ: 「豪華客船の3日目の夜、夕食は指定席で毎晩同じ4人の他人と同じテーブルに座る。笑い声は絶えない。ただ俺と隣の妻の間にだけ会話がない。今日1日一言もかわしていない。」 (Scnn76gZ8E8 (0–16s, mốc thật))
- **7–25s · Người đối chứng / con số đời mình** — Hoặc người cùng tuổi cùng xuất phát nhưng sống khác (H08: r4jN, hyLp, OIeZ), hoặc tuổi+năm làm việc+khoản tiền đổ vào quyết định (Scnn). Con số có trong 30s đầu ở 5/6. Ví dụ: 「同じ日に定年したはずの同期は5年も前に仕事をやめて悠々と釣り糸を垂れている。給料も退職金もあいつと俺で大して変わらなかったはずだ。」 (r4jNE1oTv8Q (~12–24s, ước tính))
- **17–45s · Câu khoá: nói trước kết cục ngược, giấu nguyên nhân** — 6/6 có câu khoá ≤45s (trung vị ~26s). 3 biến thể: 「これは〜という話だ」 (Scnn, r4jN; + Hgo2qFDF0bM ngoài mẫu), 「だが/なのに〜」 phủ định điều nhân vật tin (xxMK, r4jN, OIeZ), tóm hành trình 3 lần (gpVr). Ví dụ: 「これはその船の中が本当はどうだったかという話だ。そして俺が14日かけて買ったものが旅ではなかったという話だ。」 (Scnn76gZ8E8 (23.5–33s, mốc thật))
- **26–50s · Lùi về ngày quyết định + tên/tuổi/nghề** — Tự giới thiệu luôn đứng SAU câu chốt: 13s (Scnn), 33s (gpVr), 35s (hyLp), 41s (xxMK), 50s (r4jN); OIeZ không có tên+tuổi trong 120s. Thường đi kèm 「話は〜に遡る」 (gpVr ~29s; bZp51t9b-_g ~36s ngoài mẫu) hoặc 「定年の日、…」 (Scnn 33s). Ví dụ: 「話は3ヶ月前に遡る。俺の名前は哲夫。68歳。タクシー運転手を40年やって63歳で引退した。年金は月14万円。」 (gpVr3OYPA-E (~29–40s, ước tính))
- **50–120s · Gieo 1 câu nhỏ của vợ mà chồng hiểu sai** — Câu ngắn của vợ bị chồng đọc là 'đồng ý' — sẽ được lật ở cuối và chính là 'bài học'. Scnn: 52s 「いいわねとだけ言った。俺はそれを賛成だと受け取った」, 64s 「窓ないのね」 → trả ~1125s 「あの船ね、本当は行きたくなかったの」. bZp51t9b-_g (ngoài mẫu): ~115s 「み子は微笑んだ。でもその目は笑っていなかった」. Ví dụ: 「パンフレットを食卓に広げた時(セ)子はいいわねとだけ言った。俺はそれを賛成だと受け取った。〔STT「時子」= 時、セツコ〕」 (Scnn76gZ8E8 (52–58s, mốc thật))
- **cuối (~−90s) · Lặp lại câu khoá + người dẫn ngôi 3 + câu hỏi khán giả** — 5/6 video top lặp lại gần nguyên văn 1 câu của 0–45s trong 90s cuối (Scnn 「14日かけて買ったのは旅ではなかった」, gpVr 3 lần, OIeZ 冷蔵庫/脳10歳, r4jN 「働けるうちは働くのが1番だと信じて」, xxMK 「熟年離婚より残酷だと言われる家庭内別居」); hyLp thì không. Kết bằng câu hỏi 「あなたの〜はありませんか?」 + 「もし心当たりがあれば是非コメントで…」 + 「このチャンネルでは老後の暮らしにまつわる物語をお届けしています」 (4/6 nguyên văn; xxMK và hyLp — 2 video cũ — chỉ hỏi comment). Ví dụ: 「俺が14日かけて買ったのは旅ではなかった。この一言だった。」 (Scnn76gZ8E8 (~1209s, ước tính))

- Tiêu đề: 45/45 tiêu đề bắt đầu 【漫画】; 31/45 có tuổi (65歳/60代/70歳…); độ dài trung vị 42 ký tự (top 10: 31–46). Khuôn ăn view nhất: 2 người/2 lựa chọn đối lập hoặc 1 cặp 夫婦 + 1 quyết định hưu trí lớn + câu hỏi kết cục. Số đếm (cả kênh 45 video, trung vị kênh 29.075): có 「夫婦」 9/45 trung vị 125.792 (không có: 21.568); có vế đối lập (VS / 〜男と、〜男 / どっち) 7/45 trung vị 107.973; có 「どっち」 2/45 — cả 2 ≥219k (838k, 219k); có 「リアル/現実」 5/45 trung vị 175.123; có 「N年後」 6/45 trung vị 69.928 (chỉ 1 video >200k); có số tiền 「万」 6/45 trung vị 11.266 (0/10 top); 「N選」 4/45 trung vị 32.761 (0/10 top). Khuôn nguyên văn đứng đầu: 「【漫画】退職金で豪華クルーズ旅をした65歳夫婦のリアル…14日間で知った現実とは？」 (963k), 「【漫画】６０代・７０代夫婦の熟年離婚 VS 熟年家庭内別居、どっちが幸せなのか？」 (838k), 「【漫画】70歳でまだ働く男と、65歳で卒業した男。5年後、差がついた本当の理由とは？」 (549k).
- Thumbnail: 9/9 ảnh mở được: dải đen ngang trên cùng chữ khối rất to, từ khoá vàng + phần còn lại trắng, = lõi tiêu đề viết gọn (9/9); 6/9 dải trên có 「リアル」 hoặc 「現実」. Hai bố cục: (a) CHIA ĐÔI 2 panel đối lập, mỗi panel 1 nhãn vàng viền đen ở đáy nói tên lựa chọn (xxMK 「60代で熟年離婚」/「家庭内別居」, r4jN 「働き続ける70歳」/「働かない70歳」, hyLp 「年収1000万円、年金13万円」/「年収600万円、年金15万円」, gpVr, D39b) — 5/9; (b) 1 cảnh + dòng chữ ĐỎ gradient viền trắng rất to ở đáy (Scnn 「14日間で買ったのは旅ではなかった…」, s98p 「走れなくなったのは車ではなかった…」, OIeZ/OyFd 「〜習慣７選」) — 4/9. Bong bóng thoại dọc (câu nói nội tâm, thường có 「…」) 7/9; nhãn tên 「名前(年齢)」 3/9 (Scnn, r4jN, D39b); mũi tên đỏ 2/9 (chỉ ở khuôn sức khoẻ 7選). Tranh manga màu nước nhạt, người già Nhật, 1 bên buồn/1 bên vui.
- Mô tả: 9/9 mô tả là khối chào kênh cố định mở bằng 「【老後のゴローさん】へようこそ。」 (7/9 ở dòng 1; 2/9 dòng 1 là quảng cáo LINE 「▼ ゴローさんが紹介した「無料勉強会」が気になる方はコチラ」 r4jN / 「老後資金の安心度診断」 D39b). 0/9 có tóm tắt riêng của video, 0/9 hashtag, 0/9 chương. 6/9 có đoạn miễn trừ 「⚠︎本動画のサムネイル・タイトルは、…あえて断定的な表現を用いる場合があります」 — toàn bộ video từ 2026-07-23 trở đi có, 3 video Feb–Apr (xxMK, gpVr, hyLp) không có. Mô tả KHÔNG tham gia vào lời hứa.
- 4 phần nối nhau: Một lời hứa đi qua 3 chỗ, mô tả đứng ngoài: tiêu đề = dải đen thumbnail (9/9); dòng đáy/2 panel của thumbnail = cảnh hoặc câu khoá của 0–45s (thumb_hook K ở 3/6: Scnn, r4jN, hyLp); câu khoá lặp lại ở cuối video (5/6). Mẫu hoàn chỉnh nhất: Scnn76gZ8E8 — 1 câu 「14日かけて買ったのは旅ではなかった」 xuất hiện ở tiêu đề (vế 「14日間で知った現実とは？」), đáy thumbnail, giây 27–33 và ~1209s.
- Số đếm: Video top có transcript: 6 (Scnn mốc thật, 5 ước tính). Câu chốt ≤17s: 6/6 (≤12s: 5/6). Câu khoá ≤45s: 6/6 (≤30s: 5/6). Tự giới thiệu sau câu chốt: 6/6 (≥30s: 4/6, không có trong 120s: 1/6). Có số trong 30s đầu: 5/6. Kể ngôi 1 俺: 4/6. Lặp câu hook ở cuối: 5/6. Thumbnail mở được 9/9: chia đôi 5/9, dòng đỏ đáy 4/9, bong bóng 7/9, nhãn tên 3/9. Mô tả boilerplate 9/9. Không có transcript: 4/10 video chọn (OyFd, D39b, s98p, U5yg).
- Ngoại lệ: OIeZvtYreOg (236k) thắng dù thumbnail lệch video (ảnh lái xe ven biển + 「習慣７選」 không có trong truyện) — gói 'sức khoẻ/list' kéo click, truyện vẫn là vợ chồng ở cuối. xxMKVprVh-I (838k) thumbnail có câu 「離婚しましょ」 không hề có trong video và lộ kết 「日曜日だけ夫婦の時間」. gpVr3OYPA-E thumbnail hứa 「熟年結婚成立」 nhưng nhân vật chỉ bắt đầu hẹn hò. 2 video cũ (xxMK, hyLp) kể ngôi 3 「男は/光一は」, 4 video Apr–Sep kể ngôi 1 「俺」.

### Khuôn cho tập đầu
```json
{
 "note": "Lane teinengo-fuufu CHƯA CÓ TẬP NÀO (our_eps rỗng) — đây là khuôn cho tập 1, mỗi phần có ví dụ nguyên văn kênh mẫu. Không phải kịch bản.",
 "hook_theo_giay": [
  {
   "t": "0–7s",
   "viec": "1 cảnh hiện tại: vợ chồng ở nơi đáng mơ ước / hoặc tờ giấy vợ đưa — mâu thuẫn trong câu thứ 2",
   "vi_du": "豪華客船の3日目の夜、…ただ俺と隣の妻の間にだけ会話がない。今日1日一言もかわしていない。 (Scnn76gZ8E8 0–16s) · おい、今日の昼飯は何だ? はあ。絶望はいつも突然やってくる。これちゃんと読んでサインしてね。…家庭内別居に関する契約書。 (xxMKVprVh-I 0–15s ước tính)"
  },
  {
   "t": "7–25s",
   "viec": "tuổi + số năm làm + khoản tiền đổ vào quyết định (退職金/年金) — 1 câu, không kể đời",
   "vi_du": "俺は藤沢(コウキチ)65歳〔STT「藤沢後」〕。ホームセンターに38年勤めた。最後は店長だ。その退職金で憧れの14日間の豪華客船に乗った。 (Scnn76gZ8E8 13–27s)"
  },
  {
   "t": "20–45s",
   "viec": "câu khoá 「これは〜という話だ」 hoặc 「だが〜」: nói trước 'thứ nhận được không phải thứ đã mua/mong'",
   "vi_du": "そして俺が14日かけて買ったものが旅ではなかったという話だ。 (Scnn76gZ8E8 27–33s) · この時男は熟年離婚じゃなくて良かったと思っていた。だが離婚より残酷な現実が男を待ち受けていた。 (xxMKVprVh-I ~19–29s)"
  },
  {
   "t": "30–60s",
   "viec": "lùi về ngày định đoạt (定年の日 / 話は〜に遡る)",
   "vi_du": "定年の日、退職金の額を見て真っ先に浮かんだのが船だった。 (Scnn76gZ8E8 33–40s) · 話は3ヶ月前に遡る。 (gpVr3OYPA-E ~29s)"
  },
  {
   "t": "50–90s",
   "viec": "gieo 1 câu ngắn của vợ bị chồng hiểu là đồng ý (sẽ trả ở cao trào)",
   "vi_du": "パンフレットを食卓に広げた時(セ)子はいいわねとだけ言った。俺はそれを賛成だと受け取った。〔STT「時子」= 時、セツコ〕 (Scnn76gZ8E8 52–59s) · 窓ないのね。 (Scnn76gZ8E8 64s)"
  }
 ],
 "tieu_de": {
  "khuon": "【漫画】{退職金で/定年後}{quyết định lớn}した{65歳}夫婦の{リアル/現実}…{thời lượng/N年後}で{知った/気づいた}{現実/本当の理由}とは？  hoặc  【漫画】{60代・70代}夫婦の{lựa chọn A} VS {lựa chọn B}、どっちが幸せなのか？",
  "do_dai": "38–46 ký tự (trung vị kênh 42)",
  "vi_du": [
   "【漫画】退職金で豪華クルーズ旅をした65歳夫婦のリアル…14日間で知った現実とは？ (963k)",
   "【漫画】６０代・７０代夫婦の熟年離婚 VS 熟年家庭内別居、どっちが幸せなのか？ (838k)",
   "【漫画】退職金で念願の田舎に移住した６５歳の老夫婦…田舎と都会、どっちが幸せなのか？ (219k, bZp51t9b-_g)"
  ],
  "tranh": "Không đưa số tiền vào tiêu đề (6/45, trung vị 11k); không dùng tiêu đề 1 người không đối lập như 「持ち家35年ローン完済直後、65歳で待っていたのは？」 (3.966)."
 },
 "chu_thumbnail": {
  "khuon": "Dải đen trên: 「{lõi tiêu đề}の{リアル}」 (từ khoá vàng, phần còn lại trắng). Bố cục (b) cho chuyến đi/quyết định 1 cặp: 2 vợ chồng rầu giữa khung cảnh vui + nhãn tên 「{họ tên}({tuổi})」 + 1 bong bóng thoại nội tâm có 「…」 + dòng đỏ đáy = CÂU KHOÁ của hook dạng 「{N日間}で買ったのは{thứ đã mua}ではなかった…」. Bố cục (a) cho đề tài VS: chia đôi, mỗi bên 1 bong bóng + 1 nhãn vàng tên lựa chọn.",
  "vi_du": [
   "退職金で豪華クルーズ旅をした65歳夫婦のリアル / まだ7日もある… / 藤沢コウキチ(65) 藤沢セツコ(63) / 14日間で買ったのは旅ではなかった… (Scnn76gZ8E8)",
   "熟年離婚と家庭内別居のリアル / 離婚しましょ / 60代で熟年離婚 | 意外と楽だよな / 日曜日だけ夫婦の時間 / 家庭内別居 (xxMKVprVh-I)"
  ],
  "tranh": "Đừng đặt câu thoại không có trong video (xxMK 「離婚しましょ」) và đừng lộ kết (「日曜日だけ夫婦の時間」) — kênh mẫu vẫn thắng nhưng đó là rủi ro comment bắt lỗi."
 },
 "mo_ta": {
  "khuon": "Dòng 1–7: khối chào kênh cố định (của kênh mình, viết 1 lần). Sau đó 2 dòng trống + đoạn miễn trừ 「⚠︎本動画のサムネイル・タイトルは、内容をわかりやすくお伝えするため、あえて断定的な表現を用いる場合があります…」. Không cần tóm tắt video — kênh mẫu 0/9 có.",
  "vi_du": "【老後のゴローさん】へようこそ。\\nこのチャンネルは、老後を「不安な時間」ではなく「楽しみな時間」に変えるための場所です。\\n年金やお金の話、健康のこと、夫婦関係や一人暮らしのリアル、ちょっと笑える日常まで。 (9/9 video)",
  "tranh": "Kênh mình không có sản phẩm LINE thì đừng chép khối 「▼ ゴローさんが紹介した…」 (chỉ 2/9, là quảng cáo)."
 }
}
```

Thắng vs thua: Không so được HOOK thắng/thua trong kênh này: 6 video top đều có transcript, còn 3 video mới + 1 video thấp đều không (bị chặn IP, không có trong transcripts.json). Khác biệt đo được nằm ở ĐỀ TÀI + GÓI: (1) 5/6 top là quan hệ 2 người (vợ chồng: Scnn, xxMK; 2 đồng kỳ: r4jN, hyLp; bạn đời mới: gpVr) — video thấp nhất U5ygHCC7cSA 「持ち家35年ローン完済直後、65歳で待っていたのは？」 (3.966 sau 91 ngày) chỉ 1 người, không có vế đối lập, trong khi cùng đề tài nhà ở nhưng có đối lập 「持ち家にこだわった６５歳夫婦と賃貸を貫いた６８歳独身の末路」 được 176k. (2) Cả kênh: tiêu đề có 「夫婦」 trung vị 125.792 vs 21.568; có vế đối lập trung vị 107.973 vs 28.897. (3) 3 video 'new' mới 2–6 ngày (6.758 / 9.103 / 15.847) — chưa phải video thua; s98pzTeoiEU chép nguyên khuôn tiêu đề+thumbnail của Scnn (963k) nhưng mới 6 ngày, không đủ để kết luận khuôn không lặp lại được. (4) Yếu tố thời gian gây nhiễu: 17 video trước 2026-06 trung vị 111.890, 25 video 2026-06→09-14 trung vị 28.719 — kênh đang có đợt thấp hơn, nên so video cũ với video mới phải cẩn thận. Trong 6 top: điểm hook cao nhất (12, Scnn 963k) cũng là video có 3 chỗ lặp 1 lời hứa; gpVr điểm thấp nhất (9) vẫn 350k nhờ đề tài 婚活 (婚活 là đề tài có 3/4 video ≥125k).

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 963,453 | 6.6 | 27.2 | 13.4 | 23.5 | H06 K19 K06 | 12 | K | K | K | 【漫画】退職金で豪華クルーズ旅をした65歳夫婦のリアル…14日間で知った現実とは？ |
| top | 839,065 | 12 | 26 | 41 | 26 | H21 K03 K06 | 11 | K | K | P | 【漫画】６０代・７０代夫婦の熟年離婚 VS 熟年家庭内別居、どっちが幸せなのか？ |
| top | 549,223 | 12 | 25 | 50 | 44 | H01 H08 K07 K19 | 11 | K | K | K | 【漫画】70歳でまだ働く男と、65歳で卒業した男。5年後、差がついた本当の理由とは？ |
| top | 350,411 | 17 | 26 | 33 | 31 | H06 K20 K04 | 9 | K | K | P | 【漫画】シニアの婚活バスツアーとは？熟年結婚は本当にあるのか？ |
| top | 322,991 | 6 | 18 | 35 | 24 | H08 K07 | 10 | K | K | K | 【漫画】老後貧困のリアル、受け取る年金額による食生活の違い貧富の差がヤバ過ぎる・・・ |
| top | 237,018 | 0 | 26 | 64 | 31 | H01 H08 K07 | 11 | P | P | P | 【漫画】“脳が10歳若い”シニアが、こっそり楽しんでいる習慣とは？ |
| new | 6,758 | — | — | — | — |  | — | N/A | P | N/A | 【漫画】60代になっても老けない長寿体質の人が持っている共通点とは？ |
| new | 9,103 | — | — | — | — |  | — | N/A | K | N/A | 【漫画】貯金が正解だと信じ続けた50代の男が、妻に言われて気づいたお金の置くべき場所とは？ |
| new | 15,847 | — | — | — | — |  | — | N/A | K | N/A | 【漫画】退職金で憧れの豪華キャンピングカー旅をした65歳夫婦の現実とは？ |
| low | 3,966 | — | — | — | — |  | — | N/A | N/A | N/A | 【漫画】持ち家35年ローン完済直後、65歳で待っていたのは？ |

#### 【漫画】退職金で豪華クルーズ旅をした65歳夫婦のリアル…14日間で知った現実とは？ — https://www.youtube.com/watch?v=Scnn76gZ8E8
- Câu chốt (6.6s): 「笑い声は絶えない。ただ俺と隣の妻の間にだけ会話がない。今日1日一言もかわしていない。」
- Câu khoá (27.2s): 「これはその船の中が本当はどうだったかという話だ。そして俺が14日かけて買ったものが旅ではなかったという話だ。」
- Chữ thumbnail: [dải đen trên, chữ vàng+trắng] 退職金で豪華クルーズ旅をした65歳夫婦のリアル ｜ [bong bóng thoại của chồng] まだ7日もある… ｜ [nhãn tên] 藤沢コウキチ(65) / 藤沢セツコ(63) ｜ [chữ đỏ gradient viền trắng, đáy] １４日間で買ったのは旅ではなかった… · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: K — Tiêu đề 「退職金で豪華クルーズ旅をした65歳夫婦のリアル…14日間で知った現実とは？」: 0s là du thuyền, 13–23s đủ 退職金·65歳·14日間, 27s hé 'cái thật sự mua được' = đúng câu hỏi 「知った現実とは？」. · Thumb↔tiêu đề: K — Dải trên chép gần nguyên nửa đầu tiêu đề; dòng đỏ đáy 「14日間で買ったのは旅ではなかった…」 trả lời một nửa vế 「14日間で知った現実とは？」 mà không lặp lại. · Thumb↔hook: K — Dòng đỏ đáy gần như nguyên văn câu khoá 27–33s 「俺が14日かけて買ったものが旅ではなかった」; ảnh = 2 vợ chồng rầu giữa boong tàu đang tiệc = đúng tương phản H06 của giây 0–10 (hook đặt ở bàn ăn, thumb đặt ở boong — cùng cơ chế). Bong bóng 「まだ7日もある…」 là cảnh ~617s (ước tính, 「あと7日」), không ở hook nhưng cùng tâm trạng.
- Vì sao giữ người: Hai tầng: (1) tương phản xa hoa–im lặng trong 7 giây đầu (H06) khiến người xem hỏi 'vợ chồng này bị gì'; (2) câu khoá 27s nói thẳng 'thứ mua được không phải chuyến đi' — biến 20 phút thành câu đố 'vậy là mua cái gì'. Câu đó lặp nguyên văn ở ~1209s 「俺が14日かけて買ったのは旅ではなかった。この一言だった」 và in lên thumbnail — 3 chỗ, 1 lời hứa.
- Điểm yếu: Gần như không có. Tự giới thiệu ở 13.4s hơi sớm (tên bị STT nghe thành 「藤沢後」) nhưng đi kèm con số 38年/店長 nên vẫn là 'stake', không phải giới thiệu suông.

#### 【漫画】６０代・７０代夫婦の熟年離婚 VS 熟年家庭内別居、どっちが幸せなのか？ — https://www.youtube.com/watch?v=xxMKVprVh-I
- Câu chốt (12s): 「これちゃんと読んでサインしてね。 は?なんだよこれ。家庭内別居に関する契約書。 もう限界です。早くサインしてください。」
- Câu khoá (26s): 「この時男は熟年離婚じゃなくて良かったと思っていた。だが離婚より残酷な現実が男を待ち受けていた。」
- Chữ thumbnail: [dải đen, chữ vàng+trắng] 熟年離婚と家庭内別居のリアル ｜ [trái, bong bóng của vợ] 離婚しましょ ｜ [nhãn vàng trái] 60代で熟年離婚 ｜ [phải, bong bóng chồng] 意外と楽だよな ｜ [bong bóng chữ đỏ] 日曜日だけ夫婦の時間 ｜ [nhãn vàng phải] 家庭内別居 · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: K — Tiêu đề 「熟年離婚 VS 熟年家庭内別居、どっちが幸せなのか？」: giây ~12 đã có 契約書 家庭内別居, giây ~19 nhắc 熟年離婚, giây ~26 so sánh 'còn tàn nhẫn hơn ly hôn' = đúng trục VS. · Thumb↔tiêu đề: K — 「熟年離婚と家庭内別居のリアル」 = cặp từ của tiêu đề; 2 nhãn vàng 「60代で熟年離婚」「家庭内別居」 chia đôi khung đúng như chữ VS. · Thumb↔hook: P — Hook là cảnh đưa 契約書 — thumbnail không có tờ giấy nào. Bong bóng 「離婚しましょ」 KHÔNG có trong transcript (grep 離婚しましょ = 0; vợ chưa bao giờ đòi ly hôn). Bong bóng 「日曜日だけ夫婦の時間」 là kết truyện ~1183s (「毎週日曜はこの契約書の内容は無効とする」) — thumbnail lộ kết.
- Vì sao giữ người: Mở bằng 1 câu thoại gia trưởng rất quen (「今日の昼飯は何だ?」) rồi 10 giây sau là tờ hợp đồng ly thân — khán giả nam 60+ tự thấy mình trong câu hỏi cơm. Câu khoá 'tưởng may mắn nhưng tàn nhẫn hơn ly hôn' (K03+K06) làm cả video thành lời giải cho câu hỏi VS.
- Điểm yếu: Người kể ngôi 3 (「男は」) + tự giới thiệu ở ~41s kèm 1 đoạn giới thiệu con trai dài tới ~70s làm nhịp 30–90s chậm. Thumbnail hứa 1 cảnh ly hôn không có trong video. Transcript chỉ có ước tính mốc giây (raw rỗng).

#### 【漫画】70歳でまだ働く男と、65歳で卒業した男。5年後、差がついた本当の理由とは？ — https://www.youtube.com/watch?v=r4jNE1oTv8Q
- Câu chốt (12s): 「同じ日に定年したはずの同期は5年も前に仕事をやめて悠々と釣り糸を垂れている。給料も退職金もあいつと俺で大して変わらなかったはずだ。」
- Câu khoá (25s): 「なのになぜ俺だけがまだここに立っているのか。…だがその言葉はもっと大事なことから目をそらすための言い訳に過ぎなかった。これはその差の正体に70歳になってようやく気づいた俺の話だ。」
- Chữ thumbnail: [dải đen] 70歳 "働く男"と"辞めた男"のシニア生活 ｜ [trái, bong bóng] まだ働かないと… ｜ [nhãn tên] 佐伯タケシ(70) ｜ [nhãn vàng] 働き続ける70歳 ｜ [phải, bong bóng chữ đỏ] もう5年働いてない ｜ [nhãn tên] 三浦ススム(70) ｜ [nhãn vàng] 働かない70歳 · Mô tả: ▼ ゴローさんが紹介した「無料勉強会」が気になる方はコチラ
- Hook↔tiêu đề: K — Tiêu đề 「70歳でまだ働く男と、65歳で卒業した男。5年後、差がついた本当の理由とは？」: 0s người 70 tuổi còn làm, ~12s người nghỉ 5 năm trước, ~25s câu hỏi 'vì sao' = 「本当の理由」. · Thumb↔tiêu đề: K — 「70歳 "働く男"と"辞めた男"」 = cặp của tiêu đề; lệch nhỏ: tiêu đề nói 65歳で卒業, thumbnail ghi cả hai (70). · Thumb↔hook: K — Panel trái = đúng cảnh giây 0 (bảo vệ cầm cờ ở giao lộ nắng, khăn quanh cổ — transcript ~66s 「首に巻いたタオルはもう汗で絞れるほどだ」); 「もう5年働いてない」 ≈ ~217s 「俺はもう5年も前に仕事はやめた」. Panel phải vẽ ngồi hiên uống trà, còn video là câu cá — lệch hình nhỏ.
- Vì sao giữ người: Tự hỏi 'vì sao chỉ mình còn đứng đây' rồi tự đập ngay câu thần chú 「働けるうちは働くのが1番」 là lời bào chữa (K07) — người xem 65–70 tuổi đang tự nói câu đó nên bị chạm. Chốt bằng 「これは…気づいた俺の話だ」 (K19) biến cả video thành lời giải 'cái chênh lệch là gì'.
- Điểm yếu: Độ bất thường thấp (70 tuổi đi làm bảo vệ không lạ). Tự giới thiệu ~50s hơi muộn nhưng không hại vì 0–45s đã đủ câu hỏi. Cuối video (~1240–1290s) chèn lời mời 「無料で学べる勉強会」 qua LINE — quảng cáo kẹp vào giọng kể chuyện.

#### 【漫画】シニアの婚活バスツアーとは？熟年結婚は本当にあるのか？ — https://www.youtube.com/watch?v=gpVr3OYPA-E
- Câu chốt (17s): 「俺はこのバスに3回乗った。1回目は騙されて、2回目は笑われて、3回目にようやく気づいた。」
- Câu khoá (26s): 「本当に大事なものはずっと隣にあったってことに。話は3ヶ月前に遡る。」
- Chữ thumbnail: [dải đen, 'リアル' vàng] 68歳シニア婚活バスツアーのリアル ｜ [trái, bếp tối, bong bóng] 誰かと話したい… ｜ [nhãn vàng] 朝も夜も一人… ｜ [phải, xe buýt sáng, bong bóng đỏ] してもええぞ ｜ [bong bóng xanh] 結婚するか？ ｜ [chữ đỏ viền trắng giữa khung] 老後婚活のパートナーの見つけ方 ｜ [nhãn vàng] 熟年結婚成立 · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: K — Tiêu đề 「シニアの婚活バスツアーとは？熟年結婚は本当にあるのか？」: giây 0 đã ở trên xe buýt, 17–29s hé đáp án 'thứ quý giá ở ngay bên cạnh'. · Thumb↔tiêu đề: K — 「68歳シニア婚活バスツアーのリアル」 khớp; 「熟年結婚成立」 trả lời câu hỏi tiêu đề; thêm 1 lời hứa hướng dẫn 「老後婚活のパートナーの見つけ方」 mà tiêu đề không có. · Thumb↔hook: P — Panel trái (bếp tối, ấm nước, 「誰かと話したい…」) khớp đoạn ~60–90s 「今はケトルの湯だけだ」, không phải cảnh giây 0. 「熟年結婚成立」 không xảy ra với nhân vật: cuối truyện chỉ 「正式に交際を始めた」 (~1380s); chữ 成立 trong transcript là của cặp khác (~712–742s).
- Vì sao giữ người: Mở cảnh cô đơn giữa đám đông háo hức (H06) rồi tóm cả hành trình theo nhịp 3 lần — '1 bị lừa, 2 bị cười, 3 mới hiểu' — người xem biết chắc có 2 cú ngã trước khi có kết đẹp, nên ở lại xem ngã thế nào. Câu 3 lần được lặp lại nguyên nhịp ở đoạn kết người dẫn (~1400s).
- Điểm yếu: Tự giới thiệu kiểu 「俺の名前は哲夫。68歳」 ở ~33s (h2dev hook_stage cấm 「俺の名前は」 làm câu mở — ở đây không phải câu mở nên chấp nhận được). Cảm xúc hook lặng, không có câu thoại. Thumbnail hứa 'kết hôn thành' + 'cách tìm bạn đời' — video không dạy cách, cũng không cưới.

#### 【漫画】老後貧困のリアル、受け取る年金額による食生活の違い貧富の差がヤバ過ぎる・・・ — https://www.youtube.com/watch?v=hyLpBbmnvIA
- Câu chốt (6s): 「同じ会社で40年働き、同じ日に定年退職を迎えた2人の男。それなのに1人の食卓にはバランスの取れた温かい食事。もう1人の食卓にはマーガリンを塗った食パンが1枚だけ。」
- Câu khoá (18s): 「なぜここまで差がつくのでしょうか?年金額に差があるから。理由はそれだけではないのです。」
- Chữ thumbnail: [dải đen, chữ vàng+trắng] 老後貧困のリアルな 年金と食生活 ｜ [trái, chữ đỏ] 貯金0円 ｜ [bong bóng] こんなはずじゃなかった… ｜ [nhãn vàng] 年収1000万円、年金13万円 ｜ [phải, chữ đỏ] 貯金1500万円 ｜ [bong bóng] 幸せだ ｜ [nhãn vàng] 年収600万円、年金15万円 · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: K — Tiêu đề 「老後貧困のリアル、受け取る年金額による食生活の違い貧富の差がヤバ過ぎる」: 2 bàn ăn ở giây 6–16, chữ 年金額 ở giây ~20. · Thumb↔tiêu đề: K — 「老後貧困のリアルな年金と食生活」 = rút gọn tiêu đề; 2 panel giàu/nghèo = 貧富の差. · Thumb↔hook: K — 2 panel (bánh mì khô vs hamburg) = đúng 2 bàn ăn của giây 6–16. Số trên thumbnail chỉ khớp một phần: 年金13万 (~699s) và 貯金1500万 (~674s) có thật; 年収1000万/600万 và 貯金0円 không có nguyên văn (transcript chỉ nói 'lương đỉnh 80万/tháng' ~382s).
- Vì sao giữ người: Hai người xuất phát y hệt (cùng công ty, cùng ngày nghỉ) rồi ra 2 bàn ăn trái ngược — người xem 60+ tự so mình (H08). Câu 'vì lương hưu? không chỉ thế' (K07 biến thể) chặn đáp án dễ, buộc xem tiếp.
- Điểm yếu: Người kể ngôi 3 kính ngữ (「でしょうか」) làm hook xa cách, cảm xúc thấp. Điều bất thường thật (người lương CAO lại ăn bánh mì) chỉ nằm trên thumbnail, hook không nói ra. Tự giới thiệu ~35s kéo theo 1 đoạn tiệc chia tay ở công ty tới ~120s.

#### 【漫画】“脳が10歳若い”シニアが、こっそり楽しんでいる習慣とは？ — https://www.youtube.com/watch?v=OIeZvtYreOg
- Câu chốt (0s): 「冷蔵庫の前で何を取りに来たのか思い出せない。今週で4回目だ。床屋では同じ話を3度したと言われた。」
- Câu khoá (26s): 「俺とあいつで一体何が違うんだ。原因はサボっていたことじゃない。きちんと済ませていた方だった。」
- Chữ thumbnail: [dải đen, 脳が若い vàng] 実は脳が若い60代 ｜ [ảnh: ông lão lái ô tô ven biển, mũi tên đỏ chỉ vào ông] ｜ [chữ đỏ gradient đáy] 内緒で楽しんでいる習慣７選 · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: P — Tiêu đề 「"脳が10歳若い"シニアが、こっそり楽しんでいる習慣とは？」: câu hỏi 'não trẻ/già' có ngay giây 0–26, nhưng chữ 「こっそり楽しんでる」 và 「7つ」 chỉ xuất hiện ở ~276s (ước tính) qua lời ông radio. · Thumb↔tiêu đề: P — 「実は脳が若い60代」 ≈ 「脳が10歳若いシニア」; nhưng thumbnail thêm khung list 「習慣７選」 mà tiêu đề không có (tiêu đề chỉ 「習慣とは？」). · Thumb↔hook: P — Thumbnail là 1 ông vui vẻ lái xe ven biển — video không có cảnh này (chữ 車 xuất hiện 1 lần ~724s, không liên quan; 運転/ドライブ = 0). Hook là người đãng trí trước tủ lạnh. Chỉ khớp ở ý 'có người não trẻ'.
- Vì sao giữ người: Cảnh đãng trí có đếm (4 lần/tuần, 3 lần cùng 1 chuyện) chạm nỗi sợ lẫn của 60+; câu tự trả lời 'không phải vì lười mà vì làm quá đều đặn' (K07) lật niềm tin 'chăm tập não là đủ' — người xem đang tập 脳トレ phải xem tiếp.
- Điểm yếu: Lời hứa danh sách 7 điều tới ~276s mới có (ngoài 120s). Nhân vật không có tên+tuổi trong 120s (chỉ 課長 gọi 「森下さん」 ~64s). Thumbnail dạng list 7選 + ảnh lái xe là gói 'sức khoẻ' khác hẳn giọng truyện của video.

#### 【漫画】60代になっても老けない長寿体質の人が持っている共通点とは？ — https://www.youtube.com/watch?v=OyFdwyhTVVQ
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: [dải đen, 老けない vàng] 実は老けない60代 ｜ [ảnh: cụ bà cười trên ghế công viên, mũi tên đỏ] ｜ [chữ đỏ gradient đáy] 長寿体質の人だけが知る習慣７選 · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: N/A — không lấy được transcript (raw hook_segments rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) — không phân tích hook, chỉ phân tích gói · Thumb↔tiêu đề: P — Tiêu đề hỏi 「長寿体質の人が持っている共通点とは？」, thumbnail đổi thành 「習慣７選」 — cùng ý nhưng thêm khung list 7 mục; dải trên 「実は老けない60代」 khớp 「60代になっても老けない」. · Thumb↔hook: N/A — không lấy được transcript (raw hook_segments rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) — không phân tích hook, chỉ phân tích gói
- Vì sao giữ người: 
- Điểm yếu: Mới đăng 2026-09-21 (2 ngày tuổi khi đo) — 6.758 view chưa phải kết quả cuối. Thumbnail chép nguyên khuôn của OIeZvtYreOg (実は〜60代 + mũi tên đỏ + 〜習慣７選) nhưng nhân vật là nữ, không có cặp vợ chồng.

#### 【漫画】貯金が正解だと信じ続けた50代の男が、妻に言われて気づいたお金の置くべき場所とは？ — https://www.youtube.com/watch?v=D39bUfMK4jQ
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: [dải đen, chữ vàng+trắng] 貯金が正解と信じた50代の現実 ｜ [trái, phòng tối, cầm sổ] bong bóng: 今月も減ってない ｜ [nhãn tên] 宮原マサハル(58) ｜ [nhãn vàng] 老後の不安 ｜ [phải, bếp sáng, vợ đứng sau] bong bóng chồng: え？ ｜ bong bóng vợ chữ đỏ: そのお金いつ使うの？ ｜ [nhãn vàng] 迎えた老後 · Mô tả: ▼ ゴローさんが紹介した「老後資金の安心度診断」が気になる方はコチラ
- Hook↔tiêu đề: N/A — không lấy được transcript (raw hook_segments rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) — không phân tích hook, chỉ phân tích gói · Thumb↔tiêu đề: K — 「貯金が正解と信じた50代の現実」 = nửa đầu tiêu đề; câu vợ 「そのお金いつ使うの？」 = vế 「妻に言われて気づいた」. · Thumb↔hook: N/A — không lấy được transcript (raw hook_segments rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) — không phân tích hook, chỉ phân tích gói
- Vì sao giữ người: 
- Điểm yếu: Mới đăng 2026-09-18 (5 ngày) — 9.103 view chưa phải kết quả cuối. Đề tài tiền (50代, không phải 60+ vợ chồng) + mô tả mở bằng quảng cáo LINE 「老後資金の安心度診断」 → video có mục đích bán lead; nhân vật 58 tuổi lệch khán giả chính.

#### 【漫画】退職金で憧れの豪華キャンピングカー旅をした65歳夫婦の現実とは？ — https://www.youtube.com/watch?v=s98pzTeoiEU
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: [dải đen, chữ vàng+trắng] 退職金で豪華キャンパー旅をした65歳夫婦のリアル ｜ [bong bóng chồng] もう帰りたい… ｜ [ảnh: 2 vợ chồng rầu trước xe cắm trại, nhóm khác đang vui uống bia] ｜ [chữ đỏ gradient đáy] 走れなくなったのは車ではなかった… · Mô tả: 【老後のゴローさん】へようこそ。
- Hook↔tiêu đề: N/A — không lấy được transcript (raw hook_segments rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) — không phân tích hook, chỉ phân tích gói · Thumb↔tiêu đề: K — Dải trên = tiêu đề 「退職金で憧れの豪華キャンピングカー旅をした65歳夫婦の現実とは？」 (キャンピングカー → キャンパー, 現実 → リアル); dòng đỏ đáy trả lời 「現実とは？」. · Thumb↔hook: N/A — không lấy được transcript (raw hook_segments rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) — không phân tích hook, chỉ phân tích gói
- Vì sao giữ người: 
- Điểm yếu: Mới đăng 2026-09-17 (6 ngày) — 15.847 view. Đây là bản CHÉP KHUÔN y hệt Scnn76gZ8E8 (tiêu đề 退職金で豪華〇〇旅をした65歳夫婦, thumbnail cùng bố cục, dòng đáy 「〜のは〜ではなかった…」). Chưa đủ tuổi để kết luận khuôn này có lặp lại được thành công hay không.

#### 【漫画】持ち家35年ローン完済直後、65歳で待っていたのは？ — https://www.youtube.com/watch?v=U5ygHCC7cSA
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: — · Mô tả: —
- Hook↔tiêu đề: N/A — không có raw, không có transcript · Thumb↔tiêu đề: N/A — không có file thumbs\U5ygHCC7cSA.jpg — không đọc được chữ trên ảnh, không đoán · Thumb↔hook: N/A — không có dữ liệu
- Vì sao giữ người: 
- Điểm yếu: Thiếu hẳn raw + thumbnail + transcript. Tiêu đề lấy từ data\tanijin_v2\cand_profiles.json: 「【漫画】持ち家35年ローン完済直後、65歳で待っていたのは？」 — 3.966 view sau 91 ngày (thấp nhất kênh). So với video cùng đề tài nhà ở Hgo2qFDF0bM (176k): tiêu đề này 1 người, không có vế đối lập (持ち家 vs 賃貸), không có 夫婦, không có chữ リアル/現実, dài ~31 ký tự (trung vị kênh 42).

### Các tập của mình

Lane teinengo-fuufu CHƯA CÓ TẬP NÀO (0 tập: không có thư mục ep*, không có profile, không có kịch bản — E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-fuufu.md mục 2 ghi '❌ CHƯA: profile JSON · giọng · char-rate · SOP · danh sách tập · bất kỳ kịch bản nào'). Không có gì để chấm. Tập 1 dùng formula.khuon_tap_dau; đề tài đề xuất sẵn trong BAT_DAU_LANE (熟年離婚 VS 家庭内別居) chính là xxMKVprVh-I (838k) — nếu làm, lấy khung hook của Scnn76gZ8E8 (mốc thật, 12/12) thay vì khung ngôi 3 của xxMK, và KHÔNG chép câu 「離婚しましょ」/kết 「日曜日だけ」 lên thumbnail.

### Nguyên tắc
- **Câu mâu thuẫn phải nằm trong 15 giây đầu; tên–tuổi để sau.** — cơ chế: Người xem 60+ quyết định ở lại theo câu hỏi 'chuyện gì đang sai', không theo 'ai đang kể'. Tên đặt trước mâu thuẫn là 10 giây không có câu hỏi. · bằng chứng: 6/6 video top có câu chốt ≤17s (Scnn 6.6s mốc thật; hyLp ~6s; OIeZ 0s; r4jN ~12s; xxMK ~12s; gpVr ~17s). Tự giới thiệu luôn đến sau: Scnn 13.4s, gpVr ~33s, hyLp ~35s, xxMK ~41s, r4jN ~50s, OIeZ không có tên+tuổi trong 120s. · vì sao: Khớp luật h2dev hook_stage (cấm 「俺の名前は」 làm câu mở) và có bằng chứng ở kênh mẫu 963k. · áp dụng: Tập 1 teinengo-fuufu: câu đầu là cảnh vợ chồng (bàn ăn im lặng / tờ giấy vợ đưa / ghế trống bên cạnh); tên+tuổi+số năm làm việc gộp trong 1 câu ở 13–40s.
- **Câu khoá ở giây 20–45 phải nói trước kết cục NGƯỢC kỳ vọng, và câu đó được lặp lại ở cuối video.** — cơ chế: Nói trước 'thứ nhận được không phải thứ đã mua' biến 20 phút thành 1 câu hỏi duy nhất (vậy là gì?). Lặp lại ở cuối cho người xem cảm giác được trả lời đúng lời hứa. · bằng chứng: Câu khoá ≤45s ở 6/6 top (trung vị ~26s). Lặp gần nguyên văn ở 90s cuối ở 5/6: Scnn 27s→~1209s 「俺が14日かけて買ったのは旅ではなかった」; gpVr 17s→cuối 「1回目で騙されて、2回目で笑われて」; xxMK 26s→cuối 「熟年離婚より残酷だと言われる家庭内別居」; r4jN 29s→cuối 「働けるうちは働くのが1番だと信じて」; OIeZ 0s→cuối 「冷蔵庫の前でも今でも時々止まります」. · vì sao: Là thiết bị duy nhất có ở gần như mọi video top, kể cả video điểm hook thấp nhất (gpVr). · áp dụng: Viết câu cuối (câu bài học) TRƯỚC, rồi đặt bản 'hé 30%' của nó ở 20–35s dạng 「これは〜という話だ」 (K19).
- **Dòng chữ lớn ở đáy thumbnail nên là chính câu khoá của hook, không phải câu mới.** — cơ chế: Người đã click vì câu trên thumbnail nghe lại đúng câu đó ở giây 27 → xác nhận 'đúng video mình muốn', không bỏ đi. · bằng chứng: Scnn76gZ8E8 (963k, kênh trung vị 29k): đáy thumbnail 「14日間で買ったのは旅ではなかった…」 = câu 27–33s mốc thật = câu ~1209s. Ngược lại 3 thumbnail có chữ/cảnh không có trong video (xxMK 「離婚しましょ」, gpVr 「熟年結婚成立」, OIeZ ảnh lái xe) vẫn thắng — nên đây là cách làm của video tốt nhất, không phải điều kiện bắt buộc. · vì sao: Không tốn thêm gì và loại rủi ro comment bắt lỗi thumbnail sai (đã gặp ở タニジン, xem skill youtube-hook-research). · áp dụng: thumb_text dòng đáy = câu khoá 20–35s rút gọn ≤16 chữ, kết bằng 「…」; dải trên = lõi tiêu đề + 「のリアル」.
- **Tiêu đề lane này nên có 「夫婦」 hoặc 2 người/2 lựa chọn đối lập; tránh tiêu đề 1 người không đối lập và tránh số tiền trong tiêu đề.** — cơ chế: Khán giả 60+ tự đặt mình vào 1 trong 2 phía rồi xem để biết phía mình thắng hay thua. · bằng chứng: 45 video kênh: 「夫婦」 9/45 trung vị 125.792 vs 21.568; vế đối lập 7/45 trung vị 107.973 vs 28.897; 「どっち」 2/2 ≥219k; số tiền 「万」 6/45 trung vị 11.266 (0/10 top). Video thấp nhất đã chọn U5ygHCC7cSA là 1 người, không đối lập (3.966). · vì sao: Đây là tín hiệu mạnh nhất trong dữ liệu kênh và trùng đúng trục lane (vợ chồng). · áp dụng: Khuôn: 【漫画】{退職金で/定年後}{quyết định}した{65歳}夫婦の{リアル}…{N日間/N年後}で知った現実とは？ hoặc {A} VS {B}、どっちが幸せなのか？. Luật lane 「…5年後…」 trong BAT_DAU_LANE chỉ có bằng chứng yếu (N年後 6/45, trung vị 69.928) — dùng khi đề tài cần, không bắt buộc.
- **Trong 90 giây đầu gieo 1 câu ngắn của vợ mà chồng đọc sai là 'đồng ý'; cao trào là lúc câu đó được lật.** — cơ chế: Người xem (nhất là vợ) nhận ra câu đó là chịu đựng trước nhân vật — tạo căng thẳng ngầm suốt video mà không cần phản diện. · bằng chứng: Scnn76gZ8E8 52s 「いいわねとだけ言った。俺はそれを賛成だと受け取った」 + 64s 「窓ないのね」 → ~1125s 「あの船ね、本当は行きたくなかったの」 → ~1150s 「38年あなたが決めたことに1度も反対したことがなかったから反対の仕方が分からなかったの」. bZp51t9b-_g (219k, ngoài mẫu): ~115s 「み子は微笑んだ。でもその目は笑っていなかった」. · vì sao: Đây là thứ phân biệt lane vợ chồng với lane tiền (teinengo-real) — trục cảm xúc là hiểu lầm im lặng, không phải mất tiền. · áp dụng: Script tập 1: đặt 1 câu thoại 3–6 chữ của vợ ở 50–90s (「いいわね」「そうね」「窓ないのね」 kiểu), chồng độc thoại diễn giải sai; trả ở ~85% thời lượng.
- **Mô tả video không cần mang nội dung; chỉ cần khối chào kênh cố định + đoạn miễn trừ.** — cơ chế: Kênh mẫu dồn toàn bộ lời hứa vào tiêu đề+thumbnail+hook; mô tả chỉ làm nhận diện kênh và giảm rủi ro chính sách với tiêu đề khẳng định mạnh. · bằng chứng: 9/9 mô tả là cùng 1 khối 「【老後のゴローさん】へようこそ。…」; 0/9 tóm tắt, 0/9 hashtag; 6/9 có miễn trừ — 100% video từ 2026-07-23, 0/3 video Feb–Apr. · vì sao: Không có bằng chứng mô tả ảnh hưởng view (kể cả video 963k cũng chỉ có boilerplate) — đừng tốn công. · áp dụng: Viết 1 khối chào kênh teinengo-fuufu (lấy từ branding KENH.json) + đoạn miễn trừ, dùng lại mọi tập; thời gian dồn cho câu khoá và thumbnail.

### Lưu ý dữ liệu
- Chỉ Scnn76gZ8E8 có mốc giây thật (raw hook_segments 41 đoạn). 5 video top còn lại dùng mốc ƯỚC TÍNH = vị trí ký tự ÷ (len(transcript)/duration) từ E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\rougo-no-goro\_raw\transcripts.json; kiểm trên Scnn sai số ~±3–4s (câu 「乗って最初に分かったのは」 ước tính ~56s, thật 59.8s).
- 4/10 video chọn KHÔNG có transcript: OyFdwyhTVVQ, D39bUfMK4jQ, s98pzTeoiEU (raw rỗng, không có trong transcripts.json/VIDEO_ANALYSIS) và U5ygHCC7cSA (thiếu cả raw lẫn thumbnail; tiêu đề/view lấy từ E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\tanijin_v2\cand_profiles.json). Không phân tích hook, không bịa lời thoại; 4 video này KHÔNG được đưa vào file seed (kho hook cần nguyên văn 0–30s).
- Đã mở lại raw lúc 17:36 ngày 2026-09-23 trước khi ghi: vẫn chỉ Scnn có segments.
- Transcript là phụ đề tự động — tên riêng bị nghe sai: 「藤沢後」=藤沢コウキチ (thumbnail), 「せ子」=セツコ, 「最木たけし/再木」=佐伯タケシ (thumbnail), 「その田勝」=園田勝, 「高一/光一」. Trích dẫn trong file giữ gần nguyên transcript, chỉ sửa khi thumbnail cho tên đúng.
- Video 'new' mới 2–6 ngày tuổi — view chưa ổn định, không coi là video thua. Kênh có đợt giảm: trung vị trước 2026-06 = 111.890, 2026-06→09-14 = 28.719 — so sánh đếm tiêu đề trên cả 45 video bị nhiễu bởi thời gian (vd 24/45 tiêu đề kết thúc 「とは？」 có trung vị thấp hơn chủ yếu vì toàn là video mới).
- Bằng chứng ngoài mẫu chọn (bZp51t9b-_g 219k, Hgo2qFDF0bM 176k) có transcript trong transcripts.json — chỉ dùng làm ví dụ phụ, không tính vào đếm 6/6.
- Lane teinengo-fuufu chưa có tập nào (không có eps_teinengo-fuufu.json, không có profiles\profiles\teinengo-fuufu.json, thư mục assets\teinengo-fuufu chỉ có branding) → our_eps rỗng; thay bằng formula.khuon_tap_dau.
- Scnn76gZ8E8 đã có sẵn trong hooks.jsonl (nguồn tanijin 2026-09-23, patterns H06/K06, 12 điểm). Bản seed mới giữ H06 + 12 điểm, thêm closer K19 và các trường thumb_* — khi add sẽ ghi đè bản cũ theo video_id.

---

## 癒しの心理学 → lane `kokoro-kazoku`

Kênh: https://www.youtube.com/channel/UCV_8D2Agr2EaGxod0s7KBtg

Kênh GIẢI THÍCH tâm lý ngôi 2 (giọng chuyên gia không mặt, không tên, không tự giới thiệu). Một video = một nghịch lý quan hệ gia đình ('tốt mà ra xấu' / 'gần mà xa'). Hook 0–45s làm 4 việc theo thứ tự: nêu nghịch lý với chính người xem → cụ thể hoá (2 kiểu người / độc thoại tự nghi) → gỡ tội + loại đáp án người xem tự nghĩ → hứa. Sau đó neo 1 số liệu Nhật hoặc 1 học giả trước phút 2, rồi câu khoá 'không phải X mà là Y'. Tiêu đề = nghịch lý về quan hệ phổ quát; thumbnail = cùng câu đó nói miệng 2 dòng; mô tả dòng 1 = câu hỏi '〜ていませんか？' phản chiếu giây 0.

### Khung hook theo giây
- **0–10s · Câu chốt nghịch lý (≤47 chữ)** — Nói với 'あなた' hoặc 'cha mẹ' một nghịch lý tốt→xấu. Không chào, không tên kênh, không cảnh tả. 5/8 video (đúng 5 video top) mở kiểu này. Ví dụ: 「外では誰よりも親切で霊に正しいあなたがなぜ家のドアを開けて入った瞬間世界で最も鋭いトを立てる人になってしまうのでしょうか?」 (3mqrh3HS6xw (0s))
- **8–25s · Cụ thể hoá bằng 2 kiểu người hoặc độc thoại tự nghi** — Đặt 2 cha mẹ cạnh nhau (hy sinh→xa / chẳng làm gì→được tin) hoặc đọc to câu người xem đang tự hỏi. Ví dụ: 「そのためある親は一生子供のために犠牲を払ってきたのに結局最も遠い存在になってしまい。ある親は特別なことをしてあげなかったのに子供が一生で1番最初に頼る存在になります。」 (AJLE5ny--Vo (12–21s); biến thể kz3V03RdzJU 8–13s 「私の言い方が悪いのかな?私が神経質なだけなのかな?」)
- **20–45s · Gỡ tội + loại đáp án** — Phủ nhận nguyên nhân người xem đang tự trách (tính cách, nhạy cảm, thiếu yêu) và đẩy sang 'cơ chế não/tâm lý'. 5/5 video top có trong ≤108s; 0/3 video thấp. Ví dụ: 「これは単に正確の問題ではありません。あなたの脳が安全だと信じ込んだ瞬間に引き起こす知名的なエラーのせいなのです。」 (3mqrh3HS6xw (20s); AJLE5ny--Vo 30s 「この違いはお金でも教育でもありません。さらに驚くべきことに愛の大きさですらないという事実です。」; pbK_ZUSMfWY 43s)
- **23–45s · Lời hứa của video** — 1 câu nói người xem sẽ HIỂU gì + LÀM được gì. Top-5 trung vị 43s; 3 video thấp trung vị 105s. Ví dụ: 「この動画を最後までご覧いただければなぜ愛するほど腹が立つのかという不毛な真実と共に一瞬の爆発で一生かけて気づいてきた信頼を壊さないための具体的な脳のコントロール法を学ぶことができます。」 (3mqrh3HS6xw (32s))
- **45–110s · Neo số liệu Nhật / học giả + checklist triệu chứng** — 1 số liệu cơ quan Nhật hoặc 1 học giả có tên (7/8 trong 120s); hoặc checklist 'bạn có từng…' để người xem tự nhận. Ví dụ: 「もしかしたらこのような経験はありませんか?子供のために全てを譲ってきたのに。肝心な大切な話は親ではなく友達に先に相談する。」 (AJLE5ny--Vo (69–82s); số liệu: x4bNtrZxlBg 47s 厚生労働省…23.5% · pbK_ZUSMfWY 52s リンジーギブソン)
- **100–150s · Câu khoá 'không phải X mà là Y' → vào mục 1** — Chốt lại câu hỏi của cả video bằng khung ではなく (8/8 trong 140s); video có N mục thì vào 'mục 1' ở đây; CTA đăng ký 1 câu là tuỳ chọn (2/8). Ví dụ: 「しかし問題は愛の量ではなく子供の脳が親をどんな人として記憶したかにあります。」 (AJLE5ny--Vo (108s); oeufz0zIDVg 61s 「愛がないからではなく愛だけでは一緒には暮らせないからです」)

- Tiêu đề: {'rule': "Tiêu đề = 1 nghịch lý/đảo vai về một quan hệ ai cũng có, 24–37 ký tự, prefix 【心理学】 (6/7 video ≥40k). Tránh khung 'điều cấm 絶対〜いけない' (2/2 chỉ 19–25k).", 'templates': [{'khuon': '【心理学】{người A}は{điều ai cũng nghĩ quan trọng}よりも「これ」を{記憶している}', 'vi_du': '【心理学】子どもは親の愛よりも「これ」を記憶している', 'video': 'AJLE5ny--Vo 836.543'}, {'khuon': '【心理学】{việc tưởng là tốt}すると{quan hệ}が崩れる理由', 'vi_du': '【心理学】子どもと同居すると親子関係が崩れる理由', 'video': 'oeufz0zIDVg 120.960'}, {'khuon': '【心理学】{người thân nhất}に{hành vi xấu}してしまう人の心理', 'vi_du': '【心理学】一番大切な人にすぐ怒ってしまう人の心理', 'video': '3mqrh3HS6xw 88.281'}, {'khuon': '{tuổi}なのに{so sánh hạ thấp}…「{thuật ngữ tâm lý}」のゾッとする特徴{N}選', 'vi_du': '50代なのに会話は小学生…「情緒的に未熟な人」のゾッとする特徴3選', 'video': 'pbK_ZUSMfWY 76.644'}, {'khuon': '【心理学】{vai bất ngờ}も{điều}をストレスに感じる意外な{N}つの理由｜{nhãn}', 'vi_du': '【心理学】親も子の帰省をストレスに感じる意外な5つの理由｜親子関係の真相', 'video': 'FYppHHdHgNs 50.826'}], 'avoid': '【心理学】…を絶対やってはいけない{N}つのこと (a1DE 25.391, o9Bo 19.191); đề tài cá nhân không phải quan hệ (4q3Opuzy1gw); tiêu đề câu hỏi dài 40 ký tự (pg7eWMff4JE — còn quá mới để kết luận).'}
- Thumbnail: {'rule': 'Nhân vật đầu tròn trắng không mặt người thật (14/14) trong phòng nội thất ấm; 2 dòng chữ to ở đáy (11/14): dòng 1 TRẮNG = đối tượng + tình huống (thường 7 ký tự), dòng 2 VÀNG = kết luận/đảo (5–14 ký tự). KHÔNG chép tiêu đề (0/14 chép nguyên) — viết lại thành câu nói miệng; ở video ≥40k luôn dạng khẳng định (7/7). Nền ấm cam cho đề tài thương/ấm, nền tối/đỏ cho xung đột (3mqr, pbK, BaZu).', 'khuon': '{đối tượng}が{tình huống}｜{kết luận ngắn, khẳng định}', 'vi_du': ['体だけ成長した｜幼稚な大人 (pbK_ZUSMfWY — = câu hook 13s)', '身近な人にだけ｜キレる人の心理 (3mqrh3HS6xw — = câu hook 0s)', '親と子が離れて｜暮らすべき心理学的な理由 (oeufz0zIDVg — = câu khoá 58s)', '子供が来るのは｜客が来ること (FYppHHdHgNs)'], 'loi_gap': 'AJLE5ny--Vo chữ 「す」 cuối bị cắt khỏi khung; x4bNtrZxlBg dòng vàng 「妻が体調を崩します」 là ý chỉ có ở ~11 phút (P với hook).'}
- Mô tả: {'rule': "Dòng 1 = câu hỏi/nỗi đau '〜ていませんか？' phản chiếu câu giây 0–40 của hook (8/8); dòng 2 = '実は…かもしれません' lật; dòng 3 = '今回は心理学の視点から…を解説します'; khối 【動画の要約】 3–4 câu; khối 【この動画のポイント】 đúng 3 gạch '・' (25/25); 5 hashtag có #心理学.", 'khuon': '{nỗi đau/niềm tin của người xem}ていませんか？\n実は、{đảo ngược}かもしれません。\n今回は心理学の視点から、{câu hỏi của video}と{giải pháp}を解説します。\n\n【動画の要約】\n{3–4 câu tóm tắt: không phải X mà là Y}\n\n【この動画のポイント】\n・{điều hiểu 1}\n・{điều hiểu 2}\n・{kỹ năng dùng ngay}\n\n#心理学 #{quan hệ} #{vấn đề} #{thuật ngữ} #{rộng}', 'vi_du': ['「家族だから一緒に暮らすのは当たり前」そう思っていませんか？ / 実は、大人になった子供と同居することで、知らず知らずのうちにお互いの関係が壊れてしまうケースが少なくありません。 (oeufz0zIDVg)', '外では礼儀正しいのに、家では大切な人に冷たく当たっていませんか？ (3mqrh3HS6xw — = câu hook 0s)']}
- 4 phần nối nhau: Một luận điểm, 4 chỗ nói cùng một câu: TIÊU ĐỀ nói nghịch lý dạng tin tức → THUMBNAIL nói lại bằng khẩu ngữ 2 dòng (8/12 khớp, 4/12 một phần, 0 lệch) và dòng vàng thường là chính 1 câu trong hook ≤60s (pbK 13s, 3mqr 0s, oeuf 58s) → HOOK giây 0 là câu tiêu đề nói với 'あなた' (7/8 khớp tiêu đề) → MÔ TẢ dòng 1 là câu hook giây 0–40 đổi thành câu hỏi '〜ていませんか？' (8/8). Hai chỗ lệch nhẹ đều ở video thấp hơn: x4bN (thumbnail hứa ý ở phút 11), a1DE (tiêu đề hứa '3 điều cấm' mà hook tới 135s mới nói).
- Số đếm: {'kenh_tong_video': 25, 'video_co_transcript_phan_tich': 8, 'video_da_chon_khong_transcript': 4, 'thumbnail_da_mo_anh': 14, 'tu_gioi_thieu_trong_120s': '0/8', 'mo_bang_nghich_ly_noi_voi_nguoi_xem_khong_canh': '5/8 (AJLE, oeuf, 3mqr, pbK, kz3V = đúng 5 video view cao nhất có transcript: 48k–836k)', 'mo_bang_canh_cu_the': '3/8 (x4bN 42,6k · a1DE 25,4k · o9Bo 19,2k)', 'cau_hoi_nazeka_trong_45s': '8/8', 'khung_X_dewa_naku_Y_trong_140s': '8/8 (AJLE 108s · oeuf 61s · 3mqr 20s · pbK 43s · kz3V 46s · x4bN 83s · a1DE 102s · o9Bo 74s)', 'go_toi_trong_110s': '5/8 — đúng 5 video top; 0/3 video thấp', 'loi_hua_noi_dung_giay': 'top-5: 23/32/43/69/116 (trung vị 43s) · 3 thấp: 88/105/135 (trung vị 105s)', 'so_lieu_hoac_hoc_gia_trong_120s': '7/8 (AJLE: Bowlby ở ~163s)', 'CTA_dang_ky_som_duoi_3_phut': '2/8 (AJLE ~155s, oeuf ~83s); 6/8 chỉ ở cuối', 'hua_N_muc_trong_hook': '4/8 (pbK ~143s, x4bN 88s, a1DE 135s, o9Bo 105s) — trùng 4/4 tiêu đề có con số', 'chu_0_30s_sau_khi_bo_khoang_trang': '138–145 chữ (tốc độ 277–290 chữ/phút, trung vị ~282)', 'prefix_【心理学】_toan_kenh': '13/25', 'prefix_trong_video_>=40k': '6/7 (thiếu: pbK_ZUSMfWY 76.644)', 'video_>=40k_dai_>=15_phut': '7/7', 'video_duoi_15_phut': '7 video, cao nhất 8,511 view', 'tieu_de_絶対いけない': '2/25 (a1DE 25.391 · o9Bo 19.191)', 'tieu_de_nghich_ly_dao_vai_trong_>=40k': '5/7 (AJLE, oeuf, 3mqr, pbK, FYpp)', 'mo_ta_dong1_co_ませんか': '15/25 (≥40k: 4/7)', 'mo_ta_dong1_phan_chieu_hook_0_40s': '8/8 video có transcript', 'mo_ta_3_bullet_ポイント': '25/25', 'mo_ta_【動画の要約】': '16/25 (≥40k: 5/7)', 'mo_ta_5_hashtag': '21/25', 'mo_ta_co_#心理学': '20/25', 'thumb_nhan_vat_dau_tron_trang': '14/14', 'thumb_2_dong_chu': '14/14', 'thumb_dong1_trang_dong2_vang': '13/14 (d5y1wW8MgEU đảo: vàng trên, trắng dưới)', 'thumb_chu_o_day_anh': '11/14 (trên: AJLE, kz3V; trái: d5y1)', 'thumb_chep_nguyen_tieu_de': '0/14 (tất cả viết lại; AJLE gần nguyên nhất)', 'thumb_dang_khang_dinh_trong_>=40k': '7/7; dạng câu hỏi 3/14 (pg7e, BaZu, 4q3O — cả 3 đăng 18–22/09)', 'thumb_title_KPL_12_video': '8K / 4P / 0L', 'hook_title_KPL_8_video': '7K / 1P / 0L', 'thumb_hook_KPL_8_video': '6K / 2P / 0L'}
- Ngoại lệ: ["pbK_ZUSMfWY: KHÔNG prefix, khung 'ゾッとする特徴3選' mà 76.644 view và nhiều comment nhất (306) — prefix không phải điều kiện.", "AJLE5ny--Vo: tiêu đề giấu 「これ」 nhưng hook trả lời ngay giây 0 — không giữ bí ẩn vẫn 836k (câu hỏi được chuyển sang 'vì sao hy sinh mà con xa').", 'AJLE5ny--Vo: thumbnail cắt mất chữ 「す」 vẫn 836k.', 'oeufz0zIDVg: dài nhất kênh 26,7 phút vẫn #2 (120.960).', 'FYppHHdHgNs: 50.826 view nhưng like 0,42% và 1 comment — view không đi cùng gắn kết.', "CTA đăng ký sớm chỉ 2/8 (đều là 2 video top: AJLE ~155s, oeuf ~83s) — CHANNEL_DNA.md ghi 'nhất quán' là sai.", "x4bNtrZxlBg mở bằng cảnh cụ thể (H01) vẫn 42.558 — cảnh mở không 'chết', chỉ kém 5 video mở nghịch lý."]

### Khuôn cho tập đầu
```json
{
 "ghi_chu": "Lane kokoro-kazoku CHƯA có tập nào → khuôn để h2dev viết tập 1. Quy đổi giây→chữ theo 282 chữ/phút (trung vị 8 transcript sau khi bỏ khoảng trắng/[音楽]; phải đo lại bằng calibrate.py khi đã có giọng).",
 "hook_theo_giay": [
  {
   "t": "0–10s",
   "chu_tich_luy": "≤47",
   "viec": "Câu chốt nghịch lý nói với người xem (không chào, không tên kênh)",
   "vi_du_ja": "子供は親が自分をどれほど愛してくれたかよりも、親のそばでどんな感情を感じながら育ったかをより長く記憶しています。",
   "video": "AJLE5ny--Vo 0s"
  },
  {
   "t": "10–25s",
   "chu_tich_luy": "≤118",
   "viec": "2 kiểu người đối lập HOẶC đọc to câu tự nghi",
   "vi_du_ja": "私の言い方が悪いのかな?私が神経質なだけなのかな?とご自分を疑っていませんか?",
   "video": "kz3V03RdzJU 8–13s"
  },
  {
   "t": "20–40s",
   "chu_tich_luy": "≤188",
   "viec": "Gỡ tội + loại đáp án",
   "vi_du_ja": "この違いはお金でも教育でもありません。さらに驚くべきことに愛の大きさですらないという事実です。",
   "video": "AJLE5ny--Vo 30s"
  },
  {
   "t": "30–45s",
   "chu_tich_luy": "≤212",
   "viec": "Lời hứa: hiểu gì + làm được gì",
   "vi_du_ja": "この動画はあなたが単に繊細だから辛いのではないということを心理学的に明確に証明します。",
   "video": "pbK_ZUSMfWY 43s"
  },
  {
   "t": "45–110s",
   "chu_tich_luy": "≤517",
   "viec": "1 số liệu Nhật có nguồn hoặc 1 học giả có tên + checklist 'bạn có từng…'",
   "vi_du_ja": "厚生労働省の人口同体統計によると同居期間が20年以上の夫婦による熟年離婚の割合が離婚全体の23.5%を記録し、過去最高を更新しました。",
   "video": "x4bNtrZxlBg 47s"
  },
  {
   "t": "100–150s",
   "chu_tich_luy": "≤705",
   "viec": "Câu khoá 'không phải X mà là Y' → vào mục 1 (nếu có N mục); CTA đăng ký 1 câu tuỳ chọn",
   "vi_du_ja": "しかし問題は愛の量ではなく子供の脳が親をどんな人として記憶したかにあります。",
   "video": "AJLE5ny--Vo 108s"
  }
 ],
 "cam": [
  "Tự giới thiệu/tên kênh trước câu chốt (0/8 video mẫu có)",
  "Khối số liệu dài trước khi có luận điểm (a1DE 40–97s)",
  "Hứa N mục sau 90s (x4bN 88s, o9Bo 105s, a1DE 135s đều là nhóm thấp)",
  "Trả lời câu hỏi mở trước giây 20 (kz3V hứa giải pháp ở 23s → câu hỏi yếu, 9/12)"
 ],
 "tieu_de": {
  "khuon": "【心理学】{quan hệ}は{điều ai cũng tin}よりも「{ẩn}」を{動詞}  |  【心理学】{việc tưởng tốt}すると{quan hệ}が崩れる理由  |  【心理学】{vai bất ngờ}も{điều}を{cảm xúc xấu}に感じる意外な{N}つの理由",
  "vi_du": [
   "【心理学】子どもは親の愛よりも「これ」を記憶している",
   "【心理学】子どもと同居すると親子関係が崩れる理由",
   "【心理学】親も子の帰省をストレスに感じる意外な5つの理由｜親子関係の真相"
  ],
  "do_dai": "24–37 ký tự (trung vị 26 ở 7 video ≥40k)"
 },
 "chu_thumbnail": {
  "khuon": "Dòng 1 trắng ~7 ký tự: {đối tượng + tình huống} | Dòng 2 vàng 5–14 ký tự: {kết luận khẳng định = 1 câu có trong hook ≤60s}",
  "vi_du": [
   "体だけ成長した｜幼稚な大人",
   "身近な人にだけ｜キレる人の心理",
   "子どもは親の愛より｜『これ』を一生覚えていま(す)"
  ],
  "kiem": "Mở ảnh xuất ra kiểm chữ không bị cắt mép (lỗi AJLE)."
 },
 "mo_ta": {
  "khuon": "xem formula.description.khuon",
  "vi_du_nguyen_van": "子どもが一生覚えているのは、親の愛の大きさではなく親のそばで感じた「感情の記憶」です。\n犠牲を払ってきたのに心が離れてしまう親と、一生信頼される親の違いはどこにあるのでしょうか。\n今回は、子どもの心を一生繋ぎ止める「心理的安全性」と「真の愛着」の築き方を解説します。\n\n【動画の要約】…\n\n【この動画のポイント】\n・愛の量や犠牲ではなく「安全基地」としての体験が絆を深める\n・過ちを正す際も存在否定をせず、基準と受容を両立させる大切さ\n・解決策の提示より「感情の共感」が子どもの脳に信頼を刻む\n\n#心理学 #親子の悩み #子育ての悩み #愛着障害 #人間関係",
  "video": "AJLE5ny--Vo"
 },
 "tap1_lane_doc": "BAT_DAU_LANE/kokoro-kazoku.md đề xuất tập 1 「【心理学】親が\"してあげたこと\"より\"してしまったこと\"を子どもは覚えている」 = đúng khuôn H37 của AJLE5ny--Vo. Câu mở mẫu (1 câu): 「子どもは、親が“してあげたこと”よりも、親のそばで“してしまったこと”のほうを、ずっと長く覚えています。」 — sau đó 2 kiểu cha mẹ + loại đáp án ('không phải tiền, không phải giáo dục') trước giây 40.",
 "gate_de_xuat_cho_profile": {
  "cau_chot_t_max": 5,
  "go_toi_t_max": 45,
  "loi_hua_t_max": 45,
  "so_lieu_hoac_hoc_gia_t_max": 120,
  "tu_gioi_thieu": "cấm trong 120s",
  "do_dai_phut": "18–24 (≈5.000–6.800 chữ ở 282 chữ/phút)",
  "char_rate_tham_chieu": "277–290 chữ/phút (transcript tự động, không phải số calibrate)"
 }
}
```

Thắng vs thua: So 5 video top có transcript (AJLE 836.543 · oeuf 120.960 · 3mqr 88.281 · pbK 76.644 · kz3V 48.367) với 3 video thấp hơn (x4bN 42.558 · a1DE 25.391 · o9Bo 19.191): khác ở CẢ hook lẫn đề tài, và hai thứ đi cùng nhau nên không tách được. (1) Hook: 5/5 top mở bằng nghịch lý nói với người xem, có câu gỡ tội trong ≤108s, hứa nội dung trung vị 43s; 3/3 thấp mở bằng cảnh cụ thể, chèn khối số liệu, hứa N mục ở 88–135s (trung vị 105s), không có câu gỡ tội — khung 'cảnh báo/điều cấm'. (2) Đề tài: top là quan hệ ai cũng có (cha mẹ–con nói chung, người thân gần nhất, người khó chịu, vợ chồng nói không hiểu nhau); thấp là tình huống hẹp (chồng mới nghỉ hưu, con đã cưới về quê, ra mắt thông gia). (3) Tiêu đề: 2/2 tiêu đề 絶対〜いけない chỉ 19–25k; cùng đề tài 帰省, tiêu đề đảo vai FYppHHdHgNs được 50.826 (gấp 2× a1DE). (4) Cặp duy nhất giữ nguyên đề tài: d5y1wW8MgEU (9,6 phút, 05/2026, thumb chữ nhỏ 「体だけ大人｜大人の特徴」) 2.849 view vs pbK_ZUSMfWY (17,9 phút, 07/2026, thumb cảnh kịch tính 「体だけ成長した｜幼稚な大人」) 76.644 → gói + độ dài (và tuổi kênh) đổi view 27×. Kết luận: ở kênh này đề tài phổ quát + khung nghịch lý/gỡ tội thắng; hook cảnh mở không phải nguyên nhân thua (x4bN vẫn 42k). Nhóm 'new' (4q3Opuzy1gw <1 ngày 432 view, pg7eWMff4JE ~2 ngày 5.864, BaZu68sdDeo ~5 ngày 10.003) chưa đủ tuổi để xếp thua; BaZu chậm hơn FYpp ở cùng tuổi (10k@5 ngày vs 12.611@~2 ngày) dù đề tài trùng lõi video 836k — tiêu đề BaZu không có nghịch lý.

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 836,543 | 0 | 30 | — | 116 | H37 K21 K22 | 11 | K | K | K | 【心理学】子どもは親の愛よりも「これ」を記憶している |
| top | 120,960 | 21 | 58 | — | 69 | H38 K21 | 10 | K | P | K | 【心理学】子どもと同居すると親子関係が崩れる理由 |
| top | 88,281 | 0 | 20 | — | 32 | H36 K22 | 11 | K | K | K | 【心理学】一番大切な人にすぐ怒ってしまう人の心理 |
| top | 76,644 | 0 | 43 | — | 43 | H36 K22 | 11 | K | P | K | 50代なのに会話は小学生…「情緒的に未熟な人」のゾッとする特徴3選 |
| top | 50,826 | — | — | — | — |  | — | N/A | P | N/A | 【心理学】親も子の帰省をストレスに感じる意外な5つの理由｜親子関係の真相 |
| top | 48,367 | 0 | 37 | — | 23 | H36 K22 K21 | 9 | K | K | K | 【夫婦心理学】会話が噛み合わない相手と暮らす中で、自分を守る心理テクニック |
| extra(có transcript) | 42,558 | 0 | 35 | — | 88 | H01 K02 K21 | 10 | K | P | P | 【心理学】定年後に夫婦関係が急激に悪化する6つの段階 |
| extra(có transcript) | 25,391 | 15 | 102 | — | 135 | H38 K21 K02 | 9 | P | K | P | 結婚した子供が帰省した時に親が「絶対やってはいけない」3つのこと |
| extra(có transcript) | 19,191 | 0 | 65 | — | 105 | H38 K21 | 10 | K | K | K | 両家の親同士で絶対に言ってはいけない3つの言葉 |
| new | 10,003 | — | — | — | — |  | — | N/A | K | N/A | 【心理学】子供と心の距離が離れていく親の共通点 |
| new | 5,864 | — | — | — | — |  | — | N/A | K | N/A | 子どもの頃は一番近かったのに、なぜ年を重ねるときょうだいがよそよそしくなるのか？ |
| new | 432 | — | — | — | — |  | — | N/A | K | N/A | 何でも一人で抱えて疲れる人｜助けを求めるのが苦手な理由 |

#### 【心理学】子どもは親の愛よりも「これ」を記憶している — https://www.youtube.com/watch?v=AJLE5ny--Vo
- Câu chốt (0s): 「子供は親が自分をどれほど愛してくれたかよりも、親のそばでどんな感情を感じながら育ったかをより長く記憶しています。」
- Câu khoá (30s): 「この違いはお金でも教育でもありません。さらに驚くべきことに愛の大きさですらないという事実です。（→108s: しかし問題は愛の量ではなく子供の脳が親をどんな人として記憶したかにあります。）」
- Chữ thumbnail: 子どもは親の愛より｜『これ』を一生覚えていま（chữ「す」cuối bị cắt khỏi mép phải ảnh） · Mô tả: 子どもが一生覚えているのは、親の愛の大きさではなく親のそばで感じた「感情の記憶」です。
- Hook↔tiêu đề: K — Tiêu đề giấu 「これ」; câu giây 0 nói luôn đáp án (感情を感じながら育ったか) — giữ lời hứa ngay, rồi chuyển câu hỏi sang 'vì sao hy sinh mà con vẫn xa'. · Thumb↔tiêu đề: K — Ảnh chép gần nguyên tiêu đề, đổi 記憶している → 『これ』を一生覚えていま(す) — thêm 「一生」. Lỗi kỹ thuật: chữ 「す」 cuối bị cắt khỏi khung. · Thumb↔hook: K — 「一生覚えています」 = câu giây 0 「より長く記憶しています」 + chữ 「一生」 ở giây 12; ảnh 3 vòng ký ức mẹ-con ấm = 'ký ức cảm xúc'.
- Vì sao giữ người: Định luật ngược đánh thẳng nỗi sợ số 1 của cha mẹ 60–80 (hy sinh cả đời mà con xa), đặt 2 kiểu cha mẹ cạnh nhau (hy sinh → xa nhất / chẳng làm gì → được tin đầu tiên), rồi loại lần lượt 3 đáp án người xem tự nghĩ ra (お金・教育・愛の大きさ). Người xem hết giả thuyết nên phải ở lại; checklist 69–99s cho họ tự nhận 'đúng nhà mình'.
- Điểm yếu: 0–68s hoàn toàn trừu tượng, không có cảnh/nhân vật nào; lời hứa nội dung tới 116s (muộn nhất nhóm top-5 có transcript); CTA đăng ký chen ở ~155s trước khi vào nội dung. 836k gấp 7× video #2 — phần lớn nhờ đề tài phổ quát nhất kênh (MỌI cha mẹ), đừng quy hết cho hook.

#### 【心理学】子どもと同居すると親子関係が崩れる理由 — https://www.youtube.com/watch?v=oeufz0zIDVg
- Câu chốt (21s): 「ですが不思議なことに同居を始めた途端言葉遣い1つに傷つきドアを閉める音1つに寂しさを覚え食事の時間にまで顔色を伺うようになってしまいます。」
- Câu khoá (58s): 「子供と同居してはいけない理由。正確に言えば愛がないからではなく愛だけでは一緒には暮らせないからです。」
- Chữ thumbnail: 親と子が離れて｜暮らすべき心理学的な理由 · Mô tả: 「家族だから一緒に暮らすのは当たり前」そう思っていませんか？
- Hook↔tiêu đề: K — Chữ 同居 xuất hiện ~21s (同居を始めた途端), nguyên cụm 「子供と同居してはいけない理由」 ở ~58s. · Thumb↔tiêu đề: P — Cùng luận điểm nhưng lật chiều: tiêu đề nói hậu quả (親子関係が崩れる理由), ảnh nói đơn thuốc (離れて暮らすべき心理学的な理由). · Thumb↔hook: K — Ảnh = câu khoá ~58s 「子供と同居してはいけない理由」 viết lại theo chiều khẳng định; hình 2 người đứng 2 phòng tách đôi.
- Vì sao giữ người: Nói hộ đúng câu cha mẹ tự bào chữa ('con mình thì sao'), rồi lật bằng 3 chi tiết nghe/nhìn được (言葉遣い1つ・ドアを閉める音1つ・食事の時間の顔色) — người đang sống chung nhận ra nhà mình. Câu 'không phải thiếu yêu, mà yêu thôi không đủ' vừa gỡ tội vừa đặt câu hỏi.
- Điểm yếu: 0–15s mở bằng câu hỏi 'bạn có từng nghĩ thế này' (chậm hơn kiểu tuyên bố); transcript ghi 「人、」 ở giây 0 — có thể là 「皆さん、」 bị nghe sai. CTA đăng ký 2 câu ở 83–102s trước khi vào nội dung. Dài nhất kênh (26,7 phút) mà vẫn #2 → độ dài không phải vấn đề.

#### 【心理学】一番大切な人にすぐ怒ってしまう人の心理 — https://www.youtube.com/watch?v=3mqrh3HS6xw
- Câu chốt (0s): 「外では誰よりも親切で霊に正しいあなたがなぜ家のドアを開けて入った瞬間世界で最も鋭いトを立てる人になってしまうのでしょうか?」
- Câu khoá (20s): 「これは単に正確の問題ではありません。あなたの脳が安全だと信じ込んだ瞬間に引き起こす知名的なエラーのせいなのです。」
- Chữ thumbnail: 身近な人にだけ｜キレる人の心理 · Mô tả: 外では礼儀正しいのに、家では大切な人に冷たく当たっていませんか？
- Hook↔tiêu đề: K — Câu giây 0 là tiêu đề nói bằng ngôi 2: 一番大切な人にすぐ怒ってしまう ↔ 家のドアを開けて入った瞬間…鋭いトゲを立てる人. · Thumb↔tiêu đề: K — すぐ怒ってしまう → キレる; 一番大切な人 → 身近な人にだけ — cùng nghĩa, khẩu ngữ, ngắn hơn. · Thumb↔hook: K — Ảnh vẽ đúng giây 0: văn phòng xám bên trái, nhà lửa đỏ bên phải, mặt nạ cười rơi xuống đất (= 外では…家では).
- Vì sao giữ người: Nghịch lý ngoài–trong (内弁慶) mà gần như ai cũng có, hỏi thẳng 'あなた' → chạm; 20s sau gỡ tội ngay ('không phải tính cách, là lỗi của não') → người xem được tha; 32s hứa mang về một thứ dùng được. Ba bước chạm–tha–hứa trong 50 giây.
- Điểm yếu: 51–113s đi vào giải thích văn hoá 迷惑 + số 70% nhân viên che cảm xúc — trừu tượng, không cảnh; câu hỏi 'なぜ…' giây 0 lặp lại gần nguyên văn ở ~113s (lãng phí). Transcript tự động nghe sai 霊に正しい(礼儀正しい)/正確(性格)/知名的(致命的).

#### 50代なのに会話は小学生…「情緒的に未熟な人」のゾッとする特徴3選 — https://www.youtube.com/watch?v=pbK_ZUSMfWY
- Câu chốt (0s): 「自分は何も悪くないはずなのになぜあの人と話すだけでどっと疲れ果てしまうのでしょうか?年齢は50代なのに会話の質は5歳児と変わらない。体だけが大きくなった大人たちのせいです。」
- Câu khoá (43s): 「この動画はあなたが単に繊細だから辛いのではないということを心理学的に明確に証明します。」
- Chữ thumbnail: 体だけ成長した｜幼稚な大人 · Mô tả: 50代なのに話が通じない、会話の後にどっと疲れる...。
- Hook↔tiêu đề: K — 50代なのに会話は小学生 ↔ giây 8 「年齢は50代なのに会話の質は5歳児と変わらない」 (lệch chữ nhỏ: tiêu đề 小学生, hook 5歳児; 小学生 xuất hiện ~156s). · Thumb↔tiêu đề: P — Ảnh bỏ 「50代」 và 「3選」, đổi thành 「体だけ成長した幼稚な大人」 — cùng đối tượng, khác chữ, không còn con số. · Thumb↔hook: K — 「体だけ成長した」 = câu giây 13 「体だけが大きくなった大人たち」; ảnh người lớn mặc yếm ăn vạ + người kiệt sức bò dưới sàn = giây 0.
- Vì sao giữ người: Đẩy lỗi ra ngoài: người xem được xác nhận 'không phải tại bạn' trong 43 giây; hình ảnh 50 tuổi = 5 tuổi vừa buồn cười vừa đúng, ai cũng nghĩ ngay tới 1 người cụ thể → kéo bình luận (306, tỉ lệ 0,40% cao nhất 7 video ≥40k).
- Điểm yếu: Lời hứa '3選' không nói rõ trong hook (chỉ 'dấu hiệu thứ 1' ở ~143s); không có prefix 【心理学】. Bản đầu cùng đề tài d5y1wW8MgEU (9,6 phút, 25/05, thumb 「体だけ大人｜大人の特徴」) chỉ 2.849 view — bản làm lại 17,9 phút + thumb cảnh kịch tính mới lên 76k; không phải chỉ nhờ hook.

#### 【心理学】親も子の帰省をストレスに感じる意外な5つの理由｜親子関係の真相 — https://www.youtube.com/watch?v=FYppHHdHgNs
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: 子供が来るのは｜客が来ること · Mô tả: 「今週末、遊びにおいで」という親の言葉。その直後の溜息の理由を知っていますか？
- Hook↔tiêu đề: N/A — không có lời thoại để so · Thumb↔tiêu đề: P — Tiêu đề hứa '5 lý do', ảnh chỉ đưa 1 kết luận đảo 「子供が来るのは客が来ること」; ý 'khách' không có trong tiêu đề (mô tả nói 「3日間の大工事」). · Thumb↔hook: N/A — không có lời thoại để so
- Vì sao giữ người: Chỉ từ gói: tiêu đề đảo vai (không phải con mệt khi về quê, mà CHA MẸ cũng mệt) — lật định kiến 'cha mẹ lúc nào cũng mong con về'. Mô tả dòng 1 gợi hook mở bằng câu thoại 「今週末、遊びにおいで」 + tiếng thở dài — CHƯA kiểm được bằng lời thoại.
- Điểm yếu: Like 0,42%, 1 bình luận / 50.826 view — tương tác thấp nhất nhóm ≥40k (nhiều view từ gợi ý, ít người gắn bó). View 12.611 lúc snapshot DNA (~2 ngày tuổi) → 50.826 sau 9 ngày.

#### 【夫婦心理学】会話が噛み合わない相手と暮らす中で、自分を守る心理テクニック — https://www.youtube.com/watch?v=kz3V03RdzJU
- Câu chốt (0s): 「同じ言語で話しているはずなのになぜ自分の家で息が詰まってしまうのでしょうか?」
- Câu khoá (37s): 「話の通じないパートナーと暮らしている時真っ先に崩れてしまうものは何でしょうか?それは愛ではありません。自分がまともかどうかという確信、つまり自分への信頼です。」
- Chữ thumbnail: 話が通じない配偶者と｜楽に暮らす心理テク · Mô tả: 言葉が通じないパートナーとの生活で、自分の心が限界を感じていませんか？「自分が悪いのでは」と自分を責める必要はありません。相手を変えようとするのをやめ、心の尊厳を守る実践心理戦略をお伝えします。
- Hook↔tiêu đề: K — 会話が噛み合わない相手と暮らす ↔ giây 0 同じ言語で話しているはずなのに…息が詰まる; 自分を守る心理テクニック ↔ 23s 自分の心を完璧に守る実践心理戦略. · Thumb↔tiêu đề: K — 相手 → 配偶者, 自分を守る心理テクニック → 楽に暮らす心理テク — cùng nội dung, rút gọn. · Thumb↔hook: K — Ảnh 2 người ngồi 2 đầu sofa: 1 người bình thản uống trà (楽に暮らす), 1 người khoanh tay quay đi (話が通じない) = giây 0 + 23s.
- Vì sao giữ người: Đọc to đúng câu tự nghi người xem đang nghĩ trong đầu (私の言い方が悪いのかな?) → người xem thấy mình 'được nghe thấy'; lời hứa 'không cần đổi đối phương' giải phóng gánh nặng mà vợ/chồng lâu năm đã bỏ cuộc.
- Điểm yếu: Lời hứa giải pháp ra quá sớm (23s) nên câu hỏi mở yếu; nghịch lý 'cùng ngôn ngữ mà nghẹt thở' nhẹ; tiêu đề 37 ký tự dài nhất nhóm ≥40k; transcript nghe sai 糸(意図)/家庭再半所頃(家庭裁判所)/現稿.

#### 【心理学】定年後に夫婦関係が急激に悪化する6つの段階 — https://www.youtube.com/watch?v=x4bNtrZxlBg
- Câu chốt (0s): 「妻が外出着を着て玄関で靴を履いた瞬間、後ろから低い夫の声が聞こえてきます。どこ行くの?その短い一言に妻は靴紐を結ぶ手を止め、思わず固まってしまいます。」
- Câu khoá (35s): 「30年を共に乗り越え子供たちを育て上げた夫婦がなぜ夫の定年退職直後に他人以下の関係に冷め切ってしまうのでしょうか。」
- Chữ thumbnail: 夫が家にいると｜妻が体調を崩します · Mô tả: 定年退職を迎えた後、夫婦の関係がなぜか重苦しくなり、すれ違ってしまうと感じていませんか？
- Hook↔tiêu đề: K — 定年 ở 24s (夫が定年退職してからまだたったの4ヶ月), 急激に悪化 ở 35s, 6つの段階 ở 88s — đúng chữ tiêu đề, dù con số N đến muộn. · Thumb↔tiêu đề: P — Ảnh chọn 1 triệu chứng cụ thể (妻が体調を崩します = 主人在宅ストレス症候群), tiêu đề nói '6 giai đoạn'. · Thumb↔hook: P — Cảnh 'どこ行くの' đúng chủ đề chồng ở nhà, nhưng ý 'vợ phát bệnh' (夫源病・主人在宅ストレス症候群) chỉ xuất hiện ~658s (ước tính) — ngoài hook.
- Vì sao giữ người: Một câu thoại 4 chữ rất thường (どこ行くの?) mà vợ nào có chồng mới nghỉ hưu cũng nghe hằng ngày — cảnh nhỏ chính xác làm khán giả nữ nhận ra ngay; số liệu 23,5% đổi chuyện nhà thành xu hướng xã hội; 'nhận ra ở 4 giai đoạn đầu thì cứu được' giữ hy vọng.
- Điểm yếu: Lời hứa '6 giai đoạn' tới 88s; khối số liệu 47–72s dày; thumbnail hứa 'vợ phát bệnh' mà hook không nhắc. Like 0,53% — thấp.

#### 結婚した子供が帰省した時に親が「絶対やってはいけない」3つのこと — https://www.youtube.com/watch?v=a1DEZVB6CrQ
- Câu chốt (15s): 「しかし不思議なことに数時間後に子供が立ち去って玄関のドアが閉まると親の心の一角には寂しさと虚しさが残り。肝心の子供は来る前よりずっと疲れた顔で帰っていきます。」
- Câu khoá (102s): 「子供の足を左右するのは食卓に並べられた豪華な料理やご馳想の数々ではなく、その家に滞在している間、自分という人間がどれほど尊重されたかという体験です。」
- Chữ thumbnail: 結婚した子が帰省｜絶対NGな行動3選 · Mô tả: 結婚した子どもが帰省した際、良かれと思ってやった行動が逆効果になっていませんか？本動画では、親が無意識にやってしまいがちな3つの行動と、子どもの足を遠ざけないための具体的な改善策を徹底解説します！
- Hook↔tiêu đề: P — Cảnh 帰省 ở giây 0 đúng đề tài, nhưng '絶対やってはいけない3つ' chỉ tới ~135s. · Thumb↔tiêu đề: K — Rút gọn: 結婚した子供が帰省した時に親が「絶対やってはいけない」3つのこと → 結婚した子が帰省｜絶対NGな行動3選. · Thumb↔hook: P — Ảnh cha mẹ soi kính lúp (= điều cấm thứ 1 'thẩm tra', ~154s) + bàn tiệc (khớp 0s); chữ '3選' không có trong 120s đầu.
- Vì sao giữ người: Cảnh chuẩn bị tận tình rất quen với cha mẹ 60–70 → cú lật 'con về mệt hơn lúc đến' làm họ giật mình vì chính mình từng thấy; câu 'không phải món ăn mà là được tôn trọng' đổi thước đo.
- Điểm yếu: 40–97s là khối số liệu 帰省ブルー trước khi có luận điểm; N mục hứa ở ~135s; tiêu đề kiểu 'điều cấm', không prefix. Cùng đề tài 帰省, FYppHHdHgNs đảo vai (親も…ストレスに感じる) được 50.826 view, gấp 2×.

#### 両家の親同士で絶対に言ってはいけない3つの言葉 — https://www.youtube.com/watch?v=o9BoLvxu18k
- Câu chốt (0s): 「両家の顔合わせの席で謙のつもりで口にしたうちの子は本当に至らない点が多くてという一言。この丁寧な謙遜が10年後に子供夫婦の離婚原因になったり義の実家からの攻撃の武器に変わったりすることをご存知でしょうか?」
- Câu khoá (65s): 「多くの方が両家の親の関係が逆シして対立が生じる理由を霊が足りないからと考えがちです。しかし実態は完全に逆です。」
- Chữ thumbnail: 相手の親に｜絶対言ってはいけない言葉3選 · Mô tả: 両家の親同士で絶対に言ってはいけない3つの言葉とは？両家顔合わせ食事会から孫の祝い事まで、配慮や謙遜のつもりで発した一言が離婚原因や大きな誤解を生む理由を徹底解説します。
- Hook↔tiêu đề: K — Câu giây 0 chính là 1 ví dụ '言ってはいけない言葉' giữa 両家の親同士. · Thumb↔tiêu đề: K — 両家の親同士で → 相手の親に; 3つの言葉 → 言葉3選. · Thumb↔hook: K — Ảnh bàn tiệc ra mắt, 3 người căng thẳng, 1 người toát mồ hôi = cảnh giây 0.
- Vì sao giữ người: Hậu quả rất xa (10 năm sau, ly hôn) gắn vào câu nói lịch sự nhất → người xem buộc tự hỏi 'mình đã nói câu đó chưa'; 74s lật 'không phải thiếu lễ mà thừa lễ'.
- Điểm yếu: Tình huống hẹp (chỉ ai sắp/đã ra mắt thông gia); cảm xúc thấp (lo xã giao hơn là đau); không prefix, không #心理学; like 0,78%. Transcript nghe sai 3大絶対金(禁)/霊(礼).

#### 【心理学】子供と心の距離が離れていく親の共通点 — https://www.youtube.com/watch?v=BaZu68sdDeo
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: 尽くしてきたのに｜なぜ離れていく？ · Mô tả: 「子供のために良かれと思って連絡しているのに、なぜか避けられている気がする…」そんな悩みを抱えていませんか？
- Hook↔tiêu đề: N/A — không có lời thoại để so · Thumb↔tiêu đề: K — Ảnh đổi 'điểm chung của cha mẹ bị con xa' thành lời than của cha mẹ 「尽くしてきたのに｜なぜ離れていく？」. · Thumb↔hook: N/A — không có lời thoại để so
- Vì sao giữ người: Chỉ từ gói: đề tài trùng lõi AJLE5ny--Vo (hy sinh mà con xa — đúng câu giây 12 của video 836k), mô tả có khái niệm 「愛の配送事故」.
- Điểm yếu: Mới ~5 ngày, 10.003 view; so với FYppHHdHgNs (12.611 view lúc ~2 ngày tuổi) thì chậm hơn. Tái dùng đề tài hit nhưng tiêu đề 【心理学】子供と心の距離が離れていく親の共通点 không có nghịch lý/đảo vai như tiêu đề hit.

#### 子どもの頃は一番近かったのに、なぜ年を重ねるときょうだいがよそよそしくなるのか？ — https://www.youtube.com/watch?v=pg7eWMff4JE
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: 一番近かったきょうだい｜なぜ他人より気まずい？ · Mô tả: 大人になり、きょうだいと会っても会話が続かず気まずいと感じたことはありませんか？
- Hook↔tiêu đề: N/A — không có lời thoại để so · Thumb↔tiêu đề: K — Ảnh rút tiêu đề 40 ký tự còn 「一番近かったきょうだい｜なぜ他人より気まずい？」 — thêm phép so sánh 'hơn cả người dưng' sắc hơn tiêu đề. · Thumb↔hook: N/A — không có lời thoại để so
- Vì sao giữ người: Chỉ từ gói: nghịch lý 'gần nhất hồi nhỏ → xa lạ khi già'; tiêu đề dạng câu hỏi dài nhất kênh (40 ký tự), không prefix.
- Điểm yếu: Mới ~2 ngày — 5.864 view chưa so được với video ≥40k (đều ≥9 ngày tuổi).

#### 何でも一人で抱えて疲れる人｜助けを求めるのが苦手な理由 — https://www.youtube.com/watch?v=4q3Opuzy1gw
- Câu chốt (—s): 「—」
- Câu khoá (—s): 「—」
- Chữ thumbnail: 迷惑をかけたくなくて｜一人で抱えていませんか · Mô tả: 何でも一人で抱え込んで疲れ果てていませんか？「大丈夫です」と笑いながら一人で抱え込む完璧主義が、あなたの心を少しずつ削り取っているかもしれません。
- Hook↔tiêu đề: N/A — không có lời thoại để so · Thumb↔tiêu đề: K — Ảnh viết lại tiêu đề thành câu hỏi thẳng người xem: 迷惑をかけたくなくて一人で抱えていませんか. · Thumb↔hook: N/A — không có lời thoại để so
- Vì sao giữ người: Chỉ từ gói: đề tài cá nhân (không nhờ được ai) — lệch 4 trụ cột quan hệ gia đình của kênh; không prefix; thumbnail dạng câu hỏi.
- Điểm yếu: Mới <1 ngày (đăng 2026-09-22 21:15 UTC) — 432 view KHÔNG dùng để kết luận.

### Các tập của mình

0 tập để chấm: E:\CLAUDE\YOUTUBE\h2dev\assets\kokoro-kazoku\ chỉ có branding\ (KENH.json, avatar, banner); chưa có E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\kokoro-kazoku.json, chưa SOP_LANE_H.md, chưa kịch bản nào. formula.khuon_tap_dau + principles là khuôn cho tập 1 (hook theo giây, tiêu đề, chữ thumbnail, mô tả — mỗi cái có ví dụ nguyên văn kênh mẫu).

### Nguyên tắc
- **Mở giây 0 bằng một nghịch lý nói thẳng với người xem — không chào, không tên kênh, không tả cảnh.** — cơ chế: Kênh là giải thích tâm lý, không kể chuyện: người xem bấm vào vì câu hỏi 'sao nhà mình lại thế này'. Nghịch lý 'tốt mà ra xấu' chính là câu hỏi đó; nói với 'あなた/親' làm họ tự đặt mình vào ngay. · bằng chứng: 0/8 video tự giới thiệu trong 120s. 5/8 mở bằng nghịch lý không cảnh (AJLE5ny--Vo 836.543 · oeufz0zIDVg 120.960 · 3mqrh3HS6xw 88.281 · pbK_ZUSMfWY 76.644 · kz3V03RdzJU 48.367) = đúng 5 video view cao nhất có transcript; 3/8 mở bằng cảnh (x4bNtrZxlBg 42.558 · a1DEZVB6CrQ 25.391 · o9BoLvxu18k 19.191). · vì sao: Khán giả 60–80 nghe giọng chuyên gia không mặt; 1 câu nghịch lý đúng nỗi đau thay được cả cảnh mở và giới thiệu. Cảnh mở vẫn sống (x4bN 42k) nhưng kém hơn trong mẫu này. · áp dụng: Câu 1 ≤47 chữ (≈10s ở 282 chữ/phút), khuôn H36 「〜はずなのに、なぜ〜てしまうのでしょうか？」 hoặc H37 「〜は〜よりも〜を長く覚えています」. Gate hook_stage: câu chốt ≤5s, cấm câu chào/tên kênh trước nó.
- **Gỡ tội sớm: nói rõ 'không phải lỗi/tính cách/thiếu yêu của bạn, mà là cơ chế' trước giây 45.** — cơ chế: Nỗi đau của khán giả kênh này đi kèm TỘI LỖI (hy sinh mà con xa, nói sai?). Bị cảnh báo thì phòng thủ; được tha thì ở lại để nghe cơ chế. · bằng chứng: 5/5 video top có câu gỡ tội trong ≤108s: 3mqrh3HS6xw 20s 「これは単に正確の問題ではありません」, pbK_ZUSMfWY 43s 「あなたが単に繊細だから辛いのではない」, oeufz0zIDVg 61s 「愛がないからではなく」, AJLE5ny--Vo 99–108s 「自分を責めてしまいます。しかし問題は愛の量ではなく」, kz3V03RdzJU 8–13s gọi tên tự nghi. 0/3 video thấp (x4bN, a1DE, o9Bo dùng khung cảnh báo/điều cấm). pbK (gỡ tội rõ nhất) có 306 comment, tỉ lệ 0,40% cao nhất nhóm ≥40k. · vì sao: Lane doc đã chốt 'KHÔNG dạy đời, không đổ lỗi' — số liệu kênh mẫu cho thấy đây không chỉ là giọng văn mà là thiết bị giữ người ở phút 1. · áp dụng: 1 câu khuôn K22 trước 45s: 「これは決してあなたの〜のせいではありません。〜という心の仕組みのせいなのです。」 Với đề tài 'sai lầm của cha mẹ' (dễ thành đổ lỗi) càng phải có câu này.
- **Hứa nội dung video trong ≤45 giây.** — cơ chế: Sau nghịch lý + gỡ tội, người xem cần biết 'ở lại được gì'. Hứa muộn = 60–120s chỉ có số liệu, dễ rời. · bằng chứng: Mốc lời hứa top-5: kz3V 23s · 3mqr 32s · pbK 43s · oeuf 69s · AJLE 116s (trung vị 43s). 3 video thấp: x4bN 88s · o9Bo 105s · a1DE 135s (trung vị 105s). Mốc là ƯỚC TÍNH ±10s. · vì sao: Chênh trung vị 62s nhất quán giữa 2 nhóm; ngoại lệ AJLE (116s) bù bằng đề tài phổ quát nhất + loại đáp án ở 30s. · áp dụng: Đặt câu hứa trong 212 chữ đầu script, khuôn 3mqr: 「この動画を最後までご覧いただければ、〜という理由と、〜する具体的な方法が分かります。」 Nếu tiêu đề có N, nói N ngay trong câu hứa (x4bN nói '6つの段階' ở 88s là quá muộn).
- **Neo 1 số liệu Nhật có nguồn hoặc 1 học giả có tên trước phút 2 — nhưng SAU lời hứa, không trước câu chốt.** — cơ chế: Giọng không mặt cần 'bằng chứng chuyên gia' thay cho khuôn mặt; số liệu cơ quan Nhật/học giả nổi tiếng làm lời an ủi thành lời giải thích đáng tin. · bằng chứng: 7/8 có trong 120s: o9Bo 21s 最高裁, x4bN 47s 厚生労働省 23.5%, pbK 52s リンジーギブソン, a1DE 55s 65.4%, 3mqr 70s 約70%, kz3V 81s 4時間26分, oeuf ~120s 家族システム理論; AJLE có Bowlby ở ~163s. Nhưng a1DE đặt khối số liệu 40–97s TRƯỚC luận điểm → 25.391. · vì sao: Lane doc bắt 'khái niệm/nghiên cứu nêu tên phải có thật' — đây cũng là thứ kênh mẫu dùng làm điểm neo, nên phải có trong series_ctx.txt có nguồn. · áp dụng: series_ctx.txt mỗi tập ≥1 số liệu JP có URL nguồn + 1 học giả; đặt ở 45–110s sau câu hứa, tối đa 2 câu số liệu liền nhau.
- **Tiêu đề: nghịch lý/đảo vai về một quan hệ ai cũng có — tránh khung 'điều cấm 絶対〜いけない' và tình huống hẹp.** — cơ chế: Đảo vai (cha mẹ CŨNG mệt khi con về) lật định kiến nên tò mò; 'điều cấm' chỉ hút người đang ở đúng tình huống đó. · bằng chứng: 5/7 tiêu đề ≥40k là nghịch lý/đảo vai. 2/2 tiêu đề 絶対〜いけない: a1DEZVB6CrQ 25.391, o9BoLvxu18k 19.191. Cùng đề tài 帰省: FYppHHdHgNs 「親も子の帰省をストレスに感じる意外な5つの理由」 50.826 vs a1DEZVB6CrQ 「…親が「絶対やってはいけない」3つのこと」 25.391. · vì sao: Cặp FYpp/a1DE giữ nguyên đề tài, chỉ đổi khung tiêu đề (và thumbnail) → gấp 2× view (cảnh báo: FYpp mới 9 ngày, like 0,42%). · áp dụng: Dùng 3 khuôn trong formula.khuon_tap_dau.tieu_de; giữ prefix 【心理学】 (6/7 video ≥40k có, rẻ) nhưng đừng coi là nguyên nhân (pbK 76k không có).
- **Thumbnail: viết lại tiêu đề thành câu nói miệng 2 dòng (trắng: đối tượng / vàng: kết luận), dạng khẳng định, và dòng vàng phải là câu có trong hook ≤60s.** — cơ chế: Người xem đọc thumbnail trong 1 giây; câu khẩu ngữ ngắn + nhân vật đầu tròn cảm xúc rõ đọc nhanh hơn tiêu đề dài. Khi dòng vàng nằm trong hook, người bấm vào nghe lại đúng câu đó ngay → không cảm thấy bị lừa. · bằng chứng: 14/14 nhân vật đầu tròn trắng, 14/14 hai dòng, 13/14 trắng-trên vàng-dưới, 0/14 chép nguyên tiêu đề, 7/7 video ≥40k dạng khẳng định. Dòng vàng = câu hook: pbK 13s 「体だけが大きくなった大人たち」, 3mqr 0s, oeuf 58s. Cùng đề tài 'người lớn chưa trưởng thành': d5y1wW8MgEU (9,6 phút, thumb 「体だけ大人｜大人の特徴」 chữ nhỏ bên trái) 2.849 view vs pbK_ZUSMfWY (17,9 phút, thumb 「体だけ成長した｜幼稚な大人」 cảnh ăn vạ + người kiệt sức) 76.644. · vì sao: Cặp d5y1/pbK là bằng chứng duy nhất giữ nguyên đề tài mà đổi gói → 27× view (lẫn cả độ dài + tuổi kênh, không tách được). · áp dụng: thumb_text.txt: dòng 1 ~7 ký tự, dòng 2 5–14 ký tự; grep dòng 2 trong 282 chữ đầu script.txt — không có thì sửa script hoặc sửa thumbnail; kiểm ảnh xuất không cắt chữ (lỗi AJLE).
- **Độ dài 18–24 phút; không làm video dưới 15 phút.** — cơ chế: Khán giả lớn tuổi xem dài (nghe như radio); video dài có đủ chỗ cho 3 mục + ví dụ + giải pháp. · bằng chứng: 7/7 video ≥40k dài ≥15 phút; 7 video, cao nhất 8,511 view. oeufz0zIDVg dài nhất 26,7 phút vẫn #2. · vì sao: Tương quan có lẫn tuổi kênh (video ngắn phần lớn đăng tháng 5 khi kênh mới), nhưng không có video ngắn nào vượt 8,5k. · áp dụng: Mục tiêu ≈5.000–6.800 chữ (282 chữ/phút) — đo lại bằng calibrate.py khi đã chốt giọng.

### Lưu ý dữ liệu
- 0/9 raw trong HOOK_LIBRARY\raw có hook_segments (transcript_via='none', IpBlocked); mở lại lúc ghi file vẫn rỗng. Mọi mốc giây là ƯỚC TÍNH = vị trí ký tự ÷ (số chữ/thời lượng) từ E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\iyashi-no-shinrigaku\_raw\transcripts.json; sai số ±5–10s, lệch thêm nếu video có nhạc intro/outro.
- transcripts.json là phụ đề TỰ ĐỘNG, nhiều chữ nghe sai; trích dẫn giữ nguyên văn: 霊に正しい(礼儀正しい), 正確(性格), 知名的(致命的), トを立てる(トゲ), 韓国(監獄), 規制ブルー(帰省ブルー), 境界戦/教会戦(境界線), 3大絶対金(禁), 新辺調査(身辺調査), 暗足(安息), 内弁形(内弁慶), 糸(意図), 家庭再半所頃(家庭裁判所), 人、(có thể 皆さん、).
- 4/9 video được chọn không có transcript ở bất kỳ đâu (FYppHHdHgNs, BaZu68sdDeo, pg7eWMff4JE, 4q3Opuzy1gw) → chỉ chấm gói đăng, KHÔNG đưa vào seed (bản ghi kho không có nguyên văn hook sẽ dạy sai).
- Thêm 3 video ngoài danh sách chọn (x4bNtrZxlBg, a1DEZVB6CrQ, o9BoLvxu18k, tag 'extra') vì có transcript — cần nhóm view thấp hơn để so. Thumbnail 3 video này + d5y1wW8MgEU + okAdnozYTyk tải từ i.ytimg.com vào C:\Users\admin\AppData\Local\Temp\claude\e--CLAUDE-YOUTUBE-TRENDING-RESEARCH\f9ed46c9-a58f-4769-99ca-1dafd7dd5a7e\scratchpad\ch\xthumbs\ (không ghi vào HOOK_LIBRARY\thumbs).
- View/like/comment/mô tả của 25 video lấy lại qua YouTube Data API videos.list ngày 2026-09-23 (C:\Users\admin\AppData\Local\Temp\claude\e--CLAUDE-YOUTUBE-TRENDING-RESEARCH\f9ed46c9-a58f-4769-99ca-1dafd7dd5a7e\scratchpad\ch\kokoro_all_meta.json) — số mới hơn raw/transcripts.json.
- Mẫu hook chỉ 8 transcript; mọi so sánh top/thấp là TƯƠNG QUAN, kiểu hook trùng hoàn toàn với độ rộng đề tài.
- Lane doc E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kokoro-kazoku.md §5 ghi 'Title LUÔN có prefix 【心理学】 (5/21 thiếu prefix chết 1–4k)': số mới — prefix 13/25; pbK_ZUSMfWY không prefix 76.644, a1DE 25.391, o9Bo 19.191; các video không prefix mà dưới 5k đều đăng tháng 5 và <15 phút → prefix nên giữ nhưng không phải nguyên nhân.
- CHANNEL_DNA.md ghi CTA đầu video 1:30–2:30 'nhất quán' và hook 'luôn' tái hiện hoạt cảnh: thực tế CTA sớm 2/8, mở bằng cảnh 3/8.
- Mã H36..5 chưa có trong patterns.json → hook_library.py add sẽ từ chối seed cho tới khi thêm các mã này (theo brief không tự sửa patterns.json).
- Lane kokoro-kazoku chưa có tập nào, chưa có profile JSON/char_rate — số chữ/giây trong khuon_tap_dau dùng tốc độ kênh mẫu (282 chữ/phút), phải đo lại sau khi chốt giọng.

---

## どっこい日本史 → lane `sengoku-uragawa`

Kênh: https://www.youtube.com/channel/UCxXV78OIGchz13GAA7RGbEQ

Một khung lặp lại: [0–5s] tên nhân vật/trận nổi tiếng + kết cục hoặc thông thuyết → [5–25s] cú đảo ('thắng mà thua', 'đúng hết mà thua', 'giai thoại do đời sau viết') → [20–40s] bằng chứng gốc hoặc con số → [22–40s] câu hỏi なぜ = gần như nguyên văn tiêu đề → [26–74s, trung vị 42s] khẩu hiệu 「さあ、教科書には載らない歴史の裏側へ。今宵も皆様をお連れしましょう。」 → lùi về 'ことの始まりは…'. Gói đăng lặp CÙNG một nghịch lý ở 3 chỗ: tiêu đề (【tên】+ câu hỏi), dòng vàng thumbnail (nghịch lý 7–11 chữ không tên), dòng mô tả thứ 2–3 (「…本当に…だったのでしょうか」). View thì đi theo ĐỘ NỔI TIẾNG của nhân vật/trận trước, rồi mới tới hook: video hook yếu nhất nhóm top (g9NiHpRWP0g, 6/12) vẫn 466k, video hook đảo thông thuyết từ giây 8 (lG0EzwtTfmw) chỉ 3,3k.

### Khung hook theo giây
- **0–5s · Tên quen + kết cục hoặc thông thuyết** — Câu 1 luôn có TÊN riêng (người/trận). 3 biến thể: câu hỏi kết cục (Tun), tuyên bố sốc (Sd), kết cục trần (g9). Không mở bằng bối cảnh chung — BTCIRj8agB4 mở bằng 12s bối cảnh là điểm yếu duy nhất của nó. Ví dụ: 「名門田家はなぜ滅んだのか。 / この戦いにおいて今川吉本は全てにおいて正しかった。 / 天勝11年4月 静で柴田勝は橋秀吉に破れました。」 (Tun00Fq_i0w / SdRuge8_gvM / g9NiHpRWP0g)
- **5–25s · Cú đảo (nghịch lý hoặc 'đời sau bịa')** — Đặt 2 sự thật đá nhau cạnh nhau, hoặc tuyên bố giai thoại là hậu thế viết. Ở 6 video top câu đảo rơi vào 0–17s (Sd 0s, g9 9s, Tun 13s, h9 15s, BT 17s; riêng Qb 58s). Video thấp: gV 56s, z9 24s nhưng hỏi ở 61s. Ví dụ: 「ですがこうした話は刑事が死んでから100年以上経って書かれたものです。 / 長くての河戦で勝ったのは家康でした。でも天下を握に行ったのは秀吉。」 (h9tW20hT2ks / BTCIRj8agB4)
- **13–40s · Bằng chứng gốc hoặc con số cụ thể** — Một vật chứng có tên + nơi lưu giữ, hoặc 1 con số đập mắt — chính là chữ trên thumbnail khi có (41人). 5/10 video có trong 40s đầu (h9, ki5, Tun, lG0 5000の命, Sd 2万). Ví dụ: 「刑事が自分の手で書いた日記。前田刑事道中日記です。今も山形県の市立米沢図書館に保管されています。 / 最後まで勝よりに従った武士はわずか41人でした。 / その手紙は今も残っています。」 (h9tW20hT2ks / Tun00Fq_i0w / ki5cLTt95AM)
- **22–40s · Câu hỏi của cả video = đọc lại tiêu đề** — Top 6: h9 22s, Sd 24s, BT 27s, Tun 0s+29s, Qb 31s/58s (g9 không hỏi). Thấp: ki5 39s (mới 5 ngày), z9 61s, gV 68s, lG0 không hỏi. Có thể hé 30% đáp án ngay sau (Tun 31s). Ví dụ: 「安はなぜ秀吉に頭を下げることになったのでしょうか? / ではなぜ破れたのでしょうか? / 答えは武田を強くしたものと滅ぼしたものが同じだったことにあります。」 (BTCIRj8agB4 / SdRuge8_gvM / Tun00Fq_i0w)
- **26–74s (trung vị 42s) · Khẩu hiệu nghi thức (K23)** — Đặt NGAY SAU câu hỏi (7/8 video có cả hai: hỏi trước, khẩu hiệu sau 5–17s). Có ở 8/10 video đã chọn (7 nguyên văn + 1 biến thể z9) và 11/21 cả kênh — có cả ở video 3,3k nên nó là DẤU NHẬN DIỆN, không phải yếu tố thắng. Ví dụ: 「さあ、教科書には乗らない歴史の裏側へ。こ宵いも皆様をお連れしましょう。 (ASR; đúng: さあ、教科書には載らない歴史の裏側へ。今宵も皆様をお連れしましょう。)」 (h9tW20hT2ks (39s), BTCIRj8agB4 (32s), lG0EzwtTfmw (26s))
- **38–75s · Lùi về điểm khởi đầu (K04)** — Sau khẩu hiệu: 'ことの始まりは…' hoặc lùi về tuổi thơ. Riêng h9 kể lại GIAI THOẠI nổi tiếng dạng kịch trước (44–130s) rồi mới vào bằng chứng — giữ fan manga không cụt hứng. Đoạn tiểu sử tuổi thơ ngay sau hook (ki5 50s+, z9 70s+) là chỗ yếu. Ví dụ: 「ことの始まりは信長が倒れた翌年です。 / 全ての始まりは本能寺の変で織田信長と光継者だった信太田が倒れたことでした。 / まず1番有名な水ブの話からお話しましょう。」 (BTCIRj8agB4 / g9NiHpRWP0g / h9tW20hT2ks)

- Tiêu đề: {'formula': '【人物名 or 合戦名】+ nghịch lý/định kiến + câu hỏi (なぜ〜のか / 本当に〜のか / 〜とは？ / どんな人だった？) + ｜戦国', 'counts': {'bat_dau_bang_【】': '10/10 (cả kênh 21/21)', 'ket_thuc_bang_cau_hoi': '10/10 (？/のか/とは？)', 'co_なぜ': '5/10 — BTCIRj8agB4, Tun00Fq_i0w, SdRuge8_gvM, ki5cLTt95AM, z9DmSetqjuA (cả kênh 12/21)', 'co_｜戦国': '7/10', 'do_dai_ky_tu': {'h9tW20hT2ks': 37, 'g9NiHpRWP0g': 29, 'QbPKiRRXM5E': 36, 'BTCIRj8agB4': 39, 'Tun00Fq_i0w': 32, 'SdRuge8_gvM': 33, 'ki5cLTt95AM': 32, 'z9DmSetqjuA': 44, 'gVasfPnkTqU': 41, 'lG0EzwtTfmw': 39}, 'dai_do_dai': '29–44 ký tự'}, 'examples': ['【小牧・長久手の戦い】勝った家康は、なぜ最後に秀吉へ従ったのか｜徳川家康｜戦国', '【桶狭間の戦い】すべて正しかった男の最期…今川義元はなぜ敗れたのか', '【柴田勝家】3万の軍が半日で崩壊！賤ヶ岳の戦いの真実とは？', '【前田慶次】漫画・花の慶次のモデルとなった前田慶次はどんな人だった？｜戦国'], 'note': 'Chỉ 1/10 có tên tác phẩm đại chúng (花の慶次) — chính là video 774k. Video thấp nhất (lG0) là video duy nhất trong 10 mà 【】 chứa tên thành chứ không có tên người/trận nổi tiếng, và thân tiêu đề lại đứng về phía thông thuyết.'}
- Thumbnail: {'formula': 'Dòng VÀNG viền đen dính mép trên = nghịch lý 7–11 chữ KHÔNG chứa tên nhân vật chính; dòng ĐỎ viền TRẮNG dính mép dưới = TÊN (+「の最期」). Đọc liền thành 1 câu. 1 mặt cận biểu cảm nặng hoặc thế đối đầu 2 người; nền bối cảnh 1 màu chủ đạo (tuyết đêm, lửa, mưa sét, vách vàng).', 'counts': {'co_dong_vang': '9/10 (thiếu: lG0EzwtTfmw 3,3k)', 'co_dong_do': '10/10', 'dong_do_co_の最期': '4/10 — h9tW20hT2ks, Tun00Fq_i0w, SdRuge8_gvM, ki5cLTt95AM', 'dong_vang_kieu_〜のに': '3/10 — g9NiHpRWP0g 勝っていたのに総崩れ (466k), BTCIRj8agB4 勝ったのに頭を下げた (213k), SdRuge8_gvM 正しかったのに負けた (91k): cả 3 đều ở nhóm top', 'dong_vang_co_so': '1/10 — Tun00Fq_i0w 残ったのは、たった41人', 'dong_vang_la_cau_hoi': '1/10 — ki5cLTt95AM 秀吉に何をした？', 'dong_vang_chua_ten_nhan_vat_chinh': '0/9 (ki5 có tên 秀吉 = nhân vật đối thủ, không phải chính)', 'so_ky_tu_vang': '7–11 (作られた傾奇者 7 · 茶釜と果てた男 7 · 誰も呼んでいない 8 · 織田家崩壊の始まり 9 · 秀吉に何をした？ 9 · 勝っていたのに総崩れ 10 · 勝ったのに頭を下げた 10 · 正しかったのに負けた 10 · 残ったのは、たった41人 11)', 'so_ky_tu_do': '4–9 (清須会議 4 · 徳川家康 4 · 賤ヶ岳の戦い 6 · 千利休の最期 6 · 7 ×4 · 大悪人、松永久秀 8 · 備中高松城の水攻め 9)', 'bo_cuc': '1 mặt cận: 5/10 (h9, g9, Tun, Sd, z9) · 2 người đối đầu: 4/10 (BT, ki5, gV, lG0) · 4 người: 1/10 (Qb)', 'anh_thap_do_phan_giai': '1/10 — gVasfPnkTqU chỉ có bản 480×360, chữ thu nhỏ không dính mép (5,3k)'}, 'examples': ['勝ったのに頭を下げた｜徳川家康', '正しかったのに負けた｜今川義元の最期', '残ったのは、たった41人｜武田勝頼の最期', '作られた傾奇者｜前田慶次の最期']}
- Mô tả: {'formula': 'Dòng 1: 「{人物/合戦}を「{視点}」から描く歴史解説ドラマです。」 · Dòng 2: bối cảnh + 「━━なぜ〜のでしょうか。」 · Dòng 3: 「{人物}は、本当に{通説}だったのでしょうか。」 · Dòng 4: 「近年の研究をもとに、…教科書では語られない{X}の実像を、漫画イラストによるドラマ形式で丁寧に解説いたします。」 · 「戦国武将や日本史がお好きな方は、ぜひ最後までご覧ください。」 · chương 0:00… (5–6 chương, chương 1 = câu hỏi) · 【本動画の主な参考文献・一次資料】 · câu hỏi comment · đăng ký · 🪭おすすめ動画 · 3 dòng ※ (創作・脚色 / AIイラスト / パブリックドメイン) · 5 hashtag', 'counts': {'dong1_歴史解説ドラマです': '7/10 — h9tW20hT2ks, g9NiHpRWP0g, QbPKiRRXM5E, BTCIRj8agB4, Tun00Fq_i0w, SdRuge8_gvM, ki5cLTt95AM', 'co_歴史解説ドラマ_o_bat_ky_dau': '9/10', 'co_本当に…でしょうか': '8/10 — h9tW20hT2ks, g9NiHpRWP0g, QbPKiRRXM5E, BTCIRj8agB4, Tun00Fq_i0w, SdRuge8_gvM, ki5cLTt95AM, z9DmSetqjuA', 'co_教科書では語られない_hoac_bien_the': '9/10', 'co_漫画イラストによるドラマ形式': '7/10', 'co_chuong_0:00': '10/10', 'co_muc_tai_lieu_goc': '10/10', 'co_cau_hoi_comment_ぜひコメントで教えてください': '3/10 — h9tW20hT2ks, BTCIRj8agB4, z9DmSetqjuA (3 video đăng 08-28, 09-04, 09-11; ki5 09-18 lại không có → chưa thành khuôn cố định)', 'co_おすすめ動画': '7/10', 'co_disclaimer_創作・脚色': '10/10'}, 'examples': ['賤ヶ岳の戦いを「敗者・柴田勝家」の視点から描く歴史解説ドラマです。', '小牧・長久手の戦いを「勝った側の徳川家康」から描く歴史解説ドラマです。', '武田勝頼と武田家滅亡を「凡庸な二代目」の通説から見直す歴史解説ドラマです。🪭', '柴田勝家は、本当に秀吉に力の差で押し切られただけの、古い武将だったのでしょうか。'], 'note': '3 video KHÔNG mở mô tả bằng khuôn dòng 1 chính là 3 video view thấp nhất (z9DmSetqjuA 16k, gVasfPnkTqU 5,3k, lG0EzwtTfmw 3,3k). Chỉ là tương quan — mô tả ảnh hưởng view ít hơn tiêu đề/thumbnail — nhưng làm theo khuôn không tốn gì.'}
- 4 phần nối nhau: Một nghịch lý, 4 chỗ: tiêu đề nêu nó thành câu hỏi → thumbnail nén nó vào dòng vàng 7–11 chữ + tên ở dòng đỏ → hook nói lại nó trước giây ~30 rồi đọc lại câu hỏi tiêu đề → mô tả dòng 2–3 viết lại câu hỏi ('本当に…だったのでしょうか'). Khớp trọn 3 chỗ (title/thumb/hook đều K): BTCIRj8agB4 (213k). Khớp title↔hook K ở 6/10 (h9, Qb, BT, Tun, Sd, ki5). Chỗ hay gãy nhất là thumbnail↔hook: chỉ 4/10 K (BT, Tun, Sd, gV) — thumbnail thường đưa chi tiết nằm giữa/cuối video (g9 '勝っていた' ~910s, z9 '呼んでいない' ~652s, h9 '最期' ~1273s).
- Số đếm: {'so_video_phan_tich': 10, 'so_video_ca_kenh': 21, 'cau_hoi_truoc_32s': '6/10 (h9 22 · Sd 24 · BT 27 · Tun 0 · Qb 31 · lG0 không hỏi nhưng đảo ở 8) — thấp: z9 61, gV 68; g9 không hỏi', 'khau_hieu': '8/10 đã chọn (7 nguyên văn + z9 biến thể), 11/21 cả kênh; thời điểm 26/32/38/39/45/47/67/69s', 'canh_kich_hoa_trong_15s_dau': '4/10 (Qb, ki5, z9, gV); 6/10 mở bằng giọng kể', 'bang_chung_goc_trong_40s': '2/10 nêu vật chứng có tên (h9 道中日記 29s, ki5 手紙 24s); 3/10 nêu con số đập mắt (Tun 41人 13s, lG0 5000の命 15s, Sd 2万の大軍 ~37s) → tổng 5/10; Sd nêu văn bản gốc 今川仮名目録追加 ở ~101s (ngoài 40s)', 'toc_do_doc': '288–329 chữ/phút (bỏ [音楽] + khoảng trắng); trung vị ~325 → 30s ≈ 160 chữ', 'thoi_luong': '19,2–24,5 phút (1151–1467s)'}
- Ngoại lệ: ['g9NiHpRWP0g (466k): hook không nhắc nghịch lý của tiêu đề/thumbnail, không có câu hỏi なぜ — thắng nhờ trận lớn + là tập 2 nối tiếp 清須会議 + gói đăng mạnh.', "SdRuge8_gvM (91k, 06-12): chưa có khẩu hiệu; mở bằng 'Hôm nay giải mã từ mắt kẻ thua' (27s) — khung cũ trước khi kênh chốt nghi thức.", 'h9tW20hT2ks (774k): sau khi tuyên bố giai thoại là bịa (15s) vẫn dành 44–130s kể lại giai thoại dạng kịch — ngoại lệ có chủ đích với nhân vật có fandom manga.', 'lG0EzwtTfmw (3,3k): hook đảo thông thuyết đạt khung, nhưng video đầu kênh, tiêu đề không có tên người, thumbnail thiếu dòng vàng.', "gVasfPnkTqU (5,3k): cùng kiểu 'giai thoại→đời sau bịa' như h9 nhưng cú đảo ở 56s thay vì 15s."]

### Khuôn cho tập đầu
```json
{
 "_why": "Lane sengoku-uragawa CHƯA có tập nào → đây là khuôn để viết tập 1. Mỗi dòng có ví dụ nguyên văn (transcript ASR, trong ngoặc là chữ đúng) + video mẫu.",
 "hook_theo_giay": [
  {
   "t": "0–5s",
   "viec": "Câu 1 có TÊN nhân vật/trận + kết cục hoặc câu hỏi kết cục. Không mở bằng 'thời loạn…' chung chung.",
   "vi_du_ja": "名門田家はなぜ滅んだのか。 (名門武田家はなぜ滅んだのか。)",
   "mau": "Tun00Fq_i0w"
  },
  {
   "t": "5–18s",
   "viec": "Cú đảo: 'ai cũng biết X — nhưng' hoặc 'thắng A mà thua B'. Nếu nhân vật có game/manga, gọi tên sự nổi tiếng đó ở câu 1–2 rồi đảo.",
   "vi_du_ja": "前田刑事ゲームや漫画で名前を見たことがある方も多いと思います。…ですがこうした話は刑事が死んでから100年以上経って書かれたものです。 (前田慶次…)",
   "mau": "h9tW20hT2ks"
  },
  {
   "t": "13–25s",
   "viec": "1 con số hoặc 1 vật chứng có tên + nơi lưu giữ (đây là nguyên liệu dòng vàng thumbnail).",
   "vi_du_ja": "最後まで勝よりに従った武士はわずか41人でした。 / 今も山形県の市立米沢図書館に保管されています。",
   "mau": "Tun00Fq_i0w / h9tW20hT2ks"
  },
  {
   "t": "22–30s",
   "viec": "Đọc câu hỏi tiêu đề gần như nguyên văn. Được hé 30% đáp án dạng nghịch lý ngay sau.",
   "vi_du_ja": "安はなぜ秀吉に頭を下げることになったのでしょうか? (家康はなぜ…) / 答えは武田を強くしたものと滅ぼしたものが同じだったことにあります。",
   "mau": "BTCIRj8agB4 / Tun00Fq_i0w"
  },
  {
   "t": "30–45s",
   "viec": "Khẩu hiệu nghi thức của lane (tự đặt câu riêng cho kênh mình, KHÔNG chép nguyên văn khẩu hiệu kênh mẫu — đó là thương hiệu của họ).",
   "vi_du_ja": "さあ、教科書には載らない歴史の裏側へ。今宵も皆様をお連れしましょう。 (kênh mẫu — chỉ để tham chiếu vị trí)",
   "mau": "h9tW20hT2ks 39s · BTCIRj8agB4 32s"
  },
  {
   "t": "45–120s",
   "viec": "Lùi về 'ことの始まりは…' NHƯNG vẫn trong xung đột (cảnh có thoại), tránh tiểu sử tuổi thơ khô ngay sau hook. Nhân vật có fandom → dựng lại giai thoại nổi tiếng trước.",
   "vi_du_ja": "ことの始まりは信長が倒れた翌年です。 / まず1番有名な水ブの話からお話しましょう。",
   "mau": "BTCIRj8agB4 / h9tW20hT2ks"
  }
 ],
 "cam": [
  "Để câu hỏi của video sau 45s (z9DmSetqjuA 61s → 16k, gVasfPnkTqU 68s → 5,3k).",
  "Kể trọn giai thoại 1 phút rồi mới nói 'là bịa' (gVasfPnkTqU 56s) — nói 'là bịa' trước, kể sau (h9tW20hT2ks 15s).",
  "Thumbnail đưa chi tiết chỉ xuất hiện sau phút 10 mà hook không nhắc (z9 呼んでいない ~652s).",
  "Mở 10s+ bằng bối cảnh chung không có tên/cảnh (BTCIRj8agB4 0–12s)."
 ],
 "tieu_de": {
  "khuon": "【{人物名}】{thông thuyết/nghịch lý}は、なぜ{kết cục ngược}のか｜{từ khoá phụ}｜戦国",
  "vi_du": [
   "【小牧・長久手の戦い】勝った家康は、なぜ最後に秀吉へ従ったのか｜徳川家康｜戦国",
   "【武田家滅亡】武田勝頼はなぜ、最強の名門を守れなかったのか｜戦国",
   "【前田慶次】漫画・花の慶次のモデルとなった前田慶次はどんな人だった？｜戦国"
  ],
  "luat": "Tên trong 【】 phải là người/trận có game-anime; nếu có tác phẩm đại chúng nổi (漫画/大河) thì đặt vào thân tiêu đề như h9. Tiêu đề và hook phải đứng CÙNG phía (lG0 tiêu đề khen 奇策, hook chê → P)."
 },
 "thumbnail": {
  "khuon": "Vàng (7–10 chữ, không tên): {đã A}のに{B} · Đỏ (4–7 chữ): {人物名}の最期 hoặc {合戦名}",
  "vi_du": [
   "勝ったのに頭を下げた / 徳川家康",
   "正しかったのに負けた / 今川義元の最期",
   "勝っていたのに総崩れ / 賤ヶ岳の戦い",
   "残ったのは、たった41人 / 武田勝頼の最期"
  ],
  "luat": "Chữ dòng vàng phải xuất hiện (ý hoặc chữ) trong 30s đầu của hook — 4/10 video mẫu làm được và đều không bị lệch. Ảnh ≥1280×720, chữ dính mép như 9/10 mẫu."
 },
 "mo_ta": {
  "khuon": [
   "{人物/合戦}を「{視点}」から描く歴史解説ドラマです。",
   "{bối cảnh 1 câu}━━{câu hỏi tiêu đề}でしょうか。",
   "{人物}は、本当に{通説}だったのでしょうか。",
   "{近年の研究/現存する手紙}をもとに、教科書では語られない{X}の実像を、漫画イラストによるドラマ形式で丁寧に解説いたします。",
   "戦国武将や日本史がお好きな方は、ぜひ最後までご覧ください。",
   "0:00 {câu hỏi} / 5 chương …",
   "【本動画の主な参考文献・一次資料】 …",
   "{câu hỏi mở cho người xem}━━ぜひコメントで教えてください。",
   "※ 3 dòng: 創作・脚色 / AIイラスト / パブリックドメイン参考 · 5 hashtag #{人物} #戦国時代 #日本史 #{đối thủ} #{合戦}"
  ],
  "vi_du": [
   "賤ヶ岳の戦いを「敗者・柴田勝家」の視点から描く歴史解説ドラマです。",
   "羽柴秀吉と織田信雄の対立に家康が加わった戦国の大戦━━長久手で勝った家康は、なぜ二年半後、秀吉に膝をついたのでしょうか。",
   "徳川家康は、本当に秀吉に敗れて従ったのでしょうか。",
   "もしあなたが家康なら、勝ったあとでも秀吉に頭を下げられたでしょうか━━ぜひコメントで教えてください。"
  ]
 },
 "cau_mo_mau_ngan": "(gợi ý 1 câu, không phải kịch bản) 「{人物}。ゲームで知っている方も多いと思います。ですがその姿は、死後{N}年経って書かれたものでした。」"
}
```

Thắng vs thua: TOP (≥91k: h9 774k, g9 466k, Qb 219k, BT 213k, Tun 142k, Sd 91k) vs THẤP (z9 16k, gV 5,3k, lG0 3,3k; ki5 68k mới 5 ngày để riêng). (1) ĐỀ TÀI là khác biệt lớn nhất: 6/6 top là trục 織田–豊臣–徳川 hoặc nhân vật có fandom manga (花の慶次), trận/hội nghị ai cũng học; 3 video thấp là tập 'bên lề' (tuổi trẻ 利家, 松永久秀, 1 cuộc vây thành không tên người). Bằng chứng tách được: g9 hook 6/12 vẫn 466k; lG0 hook đảo ở 8s vẫn 3,3k. (2) HOOK khác ở thời điểm câu hỏi: top hỏi/đảo trước 32s ở 5/6 (h9 22, Sd 24, BT 27, Tun 0, Qb 31); thấp hỏi ở 61s (z9), 68s (gV), không hỏi (lG0). Điểm hook trung bình top 9,5/12 (9,6,9,10,11,10) vs thấp 7,7 (8,9,6). (3) GÓI ĐĂNG: 3/3 dòng vàng kiểu '〜のに' nằm ở top; video thấp có thumbnail thiếu dòng vàng (lG0) hoặc ảnh 480×360 chữ nhỏ (gV); 3/3 video thấp không mở mô tả bằng khuôn 「〜から描く歴史解説ドラマです」 (7/7 còn lại có). (4) Thời điểm đăng không giải thích: z9 (08-28) và gV (08-21) đăng giữa lúc h9 (09-04) và BT (09-11) bùng nổ. Kết luận: thua do đề tài trước, hook muộn sau; hook tốt không cứu được đề tài không tên (lG0), hook yếu vẫn thắng nếu đề tài + gói đăng mạnh (g9).

### Từng video kênh mẫu

| nhóm | view | chốt | khoá | giới thiệu | hứa | mã | /12 | hook↔TĐ | thumb↔TĐ | thumb↔hook | tiêu đề |
|---|---|---|---|---|---|---|---|---|---|---|---|
| top | 774,148 | 15 | 22 | 39 | 29 | H39 K10 K23 | 9 | K | P | P | 【前田慶次】漫画・花の慶次のモデルとなった前田慶次はどんな人だった？｜戦国 |
| top | 466,929 | 9 | 32 | 47 | 39 | H40 K23 K04 | 6 | P | K | P | 【柴田勝家】3万の軍が半日で崩壊！賤ヶ岳の戦いの真実とは？ |
| top | 219,874 | 58 | 64 | 69 | 31 | H41 K01 K23 K04 | 9 | K | P | P | 【柴田勝家】信長亡き後、誰が織田家を動かすか？勝家と秀吉、清須会議｜戦国 |
| top | 213,564 | 17 | 27 | 32 | 27 | H40 K23 K04 | 10 | K | K | K | 【小牧・長久手の戦い】勝った家康は、なぜ最後に秀吉へ従ったのか｜徳川家康｜戦国 |
| top | 142,996 | 13 | 29 | 38 | 31 | H40 K10 K23 K04 | 11 | K | P | K | 【武田家滅亡】武田勝頼はなぜ、最強の名門を守れなかったのか｜戦国 |
| top | 91,235 | 0 | 24 | — | 27 | H39 K10 | 10 | K | K | K | 【桶狭間の戦い】すべて正しかった男の最期…今川義元はなぜ敗れたのか |
| new | 68,395 | 34 | 39 | 45 | 17 | H41 K23 K04 | 10 | K | P | P | 【千利休】秀吉を支えた茶人は、なぜ切腹を命じられたのか｜戦国時代 |
| new | 16,291 | 24 | 61 | 67 | 54 | H41 K23 K04 | 8 | P | K | L | 【前田利家】織田信長に追放された男は、なぜ戦場に現れたのか｜前田利家・執念の二年｜戦国」 |
| new | 5,370 | 56 | 68 | — | 59 | H39 H41 K10 | 9 | P | P | K | 【松永久秀】「稀代の悪人」は本当に奈良の大仏を焼いたのか｜信長が欲した平蜘蛛｜戦国 |
| low | 3,396 | 8 | 15 | 26 | 15 | H39 K10 K23 | 6 | P | P | P | 【備中高松城】教科書が教えない、歴史の裏側ー兵を失わず勝利を手にする奇策とは？ |

#### 【前田慶次】漫画・花の慶次のモデルとなった前田慶次はどんな人だった？｜戦国 — https://www.youtube.com/watch?v=h9tW20hT2ks
- Câu chốt (15s): 「ですがこうした話は刑事が死んでから100年以上経って書かれたものです。」
- Câu khoá (22s): 「では本物の刑事とはどんな人だったのかそれを知ると[音楽]の手がかりが残っています。」
- Chữ thumbnail: 作られた傾奇者｜前田慶次の最期 · Mô tả: 「花の慶次」のモデル、前田慶次の生涯を「記録」から描く歴史解説ドラマです。
- Hook↔tiêu đề: K — Tiêu đề hỏi 「前田慶次はどんな人だった？」 và nêu 漫画・花の慶次; hook mở bằng 「ゲームや漫画で…」 (0s) và hỏi đúng câu đó ở 22s. · Thumb↔tiêu đề: P — Dòng vàng 「作られた傾奇者」 là góc 'giai thoại bịa' — tiêu đề không nói; dòng đỏ 「前田慶次の最期」 hứa cái chết, tiêu đề hỏi 'là người thế nào'. · Thumb↔hook: P — 「作られた」 khớp câu 15s (viết sau 100 năm); 「最期」 KHÔNG có trong 120s đầu — cái chết chỉ tới chương 19:29 (「死ん」 ở ~1273s).
- Vì sao giữ người: Người xem vào vì yêu 花の慶次; câu 15s 'những chuyện đó được viết sau khi ông chết 100 năm' đe doạ đúng thứ họ yêu, rồi 29–38s đưa ra nhật ký chính tay ông viết (có nơi lưu trữ) làm lời hứa đáp án. Mẹo giữ chân: sau khẩu hiệu vẫn DỰNG LẠI giai thoại nổi tiếng (水風呂 48–80s, 髷 82–115s, 猿の面 117s+) nên fan không bị cụt hứng.
- Điểm yếu: Hook không có cảm xúc/tính mạng (stake chỉ là 'bằng chứng'); thumbnail hứa 「最期」 mà 120s đầu không đặt vấn đề cái chết. 774k chủ yếu nhờ độ nổi tiếng của 花の慶次 (video DUY NHẤT trong 21 có tên tác phẩm manga trong tiêu đề) — đừng quy hết cho hook.

#### 【柴田勝家】3万の軍が半日で崩壊！賤ヶ岳の戦いの真実とは？ — https://www.youtube.com/watch?v=g9NiHpRWP0g
- Câu chốt (9s): 「しかしこの戦いで終わったのは[音楽] 1人の武将の命だけではありません。」
- Câu khoá (32s): 「その [音楽]勝井が倒れたことで秀吉の前から 小田中最大の対抗者が消えました。」
- Chữ thumbnail: 勝っていたのに総崩れ｜賤ヶ岳の戦い · Mô tả: 賤ヶ岳の戦いを「敗者・柴田勝家」の視点から描く歴史解説ドラマです。
- Hook↔tiêu đề: P — Hook nói đúng trận và kết cục (thua), nhưng con số của tiêu đề 「3万の軍が半日で崩壊」 vắng: '3万' ở ~235s, '半日' ở ~911s. · Thumb↔tiêu đề: K — 「勝っていたのに総崩れ」 + 「賤ヶ岳の戦い」 = cùng nghịch lý 'đang thắng thì sụp nửa ngày' của tiêu đề, nói ngắn hơn. · Thumb↔hook: P — Tên trận khớp 0s; vế 'đang thắng' (勝ちかけていた) chỉ xuất hiện ở ~910s.
- Vì sao giữ người: Đặt kết cục ở câu đầu rồi nâng tầm: cái chết của 1 người = ngã rẽ thiên hạ sang 秀吉. Người xem biết kết mà không biết 'sụp thế nào', nên lời hứa thật nằm ở tiêu đề/thumbnail chứ không ở hook.
- Điểm yếu: Hook là loại yếu nhất trong 6 video top (6/12): không lặp nghịch lý 'đang thắng mà sụp nửa ngày' của tiêu đề và thumbnail. 466k nhờ (1) trận lớn hệ 織田 + nhân vật có game, (2) là TẬP 2 nối tiếp 清須会議 (QbPKiRRXM5E kết bằng 「次は柴田勝が最後に選んだ戦場静の物語へ続きます」), (3) nghịch lý mạnh ở tiêu đề + thumbnail. Ví dụ rõ nhất cho 'video thắng dù hook yếu'.

#### 【柴田勝家】信長亡き後、誰が織田家を動かすか？勝家と秀吉、清須会議｜戦国 — https://www.youtube.com/watch?v=QbPKiRRXM5E
- Câu chốt (58s): 「この日の勝の判断は[音楽]400年 経った今も答えが出ていません。」
- Câu khoá (64s): 「正しかっ たのか、他に[音楽]道はなかったのか。」
- Chữ thumbnail: 織田家崩壊の始まり｜清須会議 · Mô tả: 清須会議を、柴田勝家の視点から描く歴史解説ドラマです。
- Hook↔tiêu đề: K — Tiêu đề 「信長亡き後、誰が織田家を動かすか？勝家と秀吉、清須会議」 = câu hỏi 31–37s của hook, cùng cảnh 清須. · Thumb↔tiêu đề: P — 「清須会議」 khớp; 「織田家崩壊の始まり」 là kết luận mạnh hơn tiêu đề (tiêu đề chỉ hỏi ai lãnh đạo). · Thumb↔hook: P — 清須会議 khớp 0–51s; hook không nói 'sụp đổ' — nói 'đến nay chưa có đáp án'.
- Vì sao giữ người: Cảnh 4 người ngồi quanh 1 chiếc ghế trống là hình ảnh dễ dựng, và câu 58s 'phán quyết của 勝家 400 năm vẫn chưa có đáp án — đúng hay không còn đường nào khác' biến video thành phiên toà để người xem tự xử (K01 hai lựa chọn).
- Điểm yếu: Câu khoá tới 58–68s — muộn nhất trong 6 video top; 37–51s là đoạn tổng quát 「全国の大名たちがその行方を見つめる中…」. Thắng nhờ đề tài 清須会議 (rất nổi) + mở chuỗi 2 tập với 賤ヶ岳.

#### 【小牧・長久手の戦い】勝った家康は、なぜ最後に秀吉へ従ったのか｜徳川家康｜戦国 — https://www.youtube.com/watch?v=BTCIRj8agB4
- Câu chốt (17s): 「長くての河戦で勝ったの は家康でした。 でも天下を握に行ったのは 秀吉。」
- Câu khoá (27s): 「安はなぜ秀吉に頭を 下げることになったのでしょうか?」
- Chữ thumbnail: 勝ったのに頭を下げた｜徳川家康 · Mô tả: 小牧・長久手の戦いを「勝った側の徳川家康」から描く歴史解説ドラマです。
- Hook↔tiêu đề: K — Câu 27s gần như chép tiêu đề 「勝った家康は、なぜ最後に秀吉へ従ったのか」. · Thumb↔tiêu đề: K — 「勝ったのに頭を下げた」+「徳川家康」 = rút gọn đúng nghịch lý tiêu đề. · Thumb↔hook: K — Cụm 'thắng / cúi đầu' có nguyên trong hook ở 17–29s (「頭を下げ」 ~29s).
- Vì sao giữ người: Nghịch lý thắng-trận-thua-thiên-hạ khớp 3 chỗ (tiêu đề/thumbnail/hook); người xem biết 家康 cuối cùng thắng tất cả nên câu 'vì sao lại cúi đầu' chạm đúng hiểu biết có sẵn của họ.
- Điểm yếu: 12s đầu là đoạn bối cảnh trừu tượng không có cảnh (dễ rơi người xem lướt). Like/view chỉ 0,16% (thấp nhất trong 10) — view nhiều nhưng tương tác mỏng.

#### 【武田家滅亡】武田勝頼はなぜ、最強の名門を守れなかったのか｜戦国 — https://www.youtube.com/watch?v=Tun00Fq_i0w
- Câu chốt (13s): 「最後まで勝より[音楽]に従った武士は わずか41人でした。」
- Câu khoá (29s): 「その男がなぜ?」
- Chữ thumbnail: 残ったのは、たった41人｜武田勝頼の最期 · Mô tả: 武田勝頼と武田家滅亡を「凡庸な二代目」の通説から見直す歴史解説ドラマです。🪭
- Hook↔tiêu đề: K — Câu đầu tiên (0s) = câu hỏi tiêu đề 「武田勝頼はなぜ、最強の名門を守れなかったのか」. · Thumb↔tiêu đề: P — Tiêu đề hỏi 'vì sao không giữ được'; thumbnail đưa con số 41 người + 「最期」 — cùng câu chuyện, khác góc (hậu quả vs nguyên nhân). · Thumb↔hook: K — 「41人」 ở 13–17s; 「最期」 được báo bằng 「しかしその代で武田は滅びました」 ~10s.
- Vì sao giữ người: Mật độ cao nhất kênh: câu hỏi ở 0s, con số 41 ở 13s, đảo định kiến 'không phải bị bỏ rơi từ đầu' ở 18s, và hé đáp án dạng nghịch lý ở 31s ('cái làm Takeda mạnh cũng là cái diệt Takeda') — người xem có một câu trả lời đủ lạ để muốn xem chứng minh.
- Điểm yếu: Không có cảnh/thoại trong 44s đầu (toàn giọng kể). 142k thấp hơn 2 video 柴田勝家 dù hook tốt hơn — đề tài 'diệt vong' nổi nhưng 勝頼 kém nổi hơn 慶次/勝家.

#### 【桶狭間の戦い】すべて正しかった男の最期…今川義元はなぜ敗れたのか — https://www.youtube.com/watch?v=SdRuge8_gvM
- Câu chốt (0s): 「この戦いにおいて今川吉本は全てにおいて 正しかった。」
- Câu khoá (24s): 「ではなぜ破れたの でしょうか?」
- Chữ thumbnail: 正しかったのに負けた｜今川義元の最期 · Mô tả: 桶狭間の戦いを「敗者・今川義元」の視点から描く歴史解説ドラマです。
- Hook↔tiêu đề: K — 「すべて正しかった男…なぜ敗れたのか」 = câu 0s + câu 24s. · Thumb↔tiêu đề: K — 「正しかったのに負けた」 = nửa đầu tiêu đề rút gọn; 「今川義元の最期」 = 'すべて正しかった男の最期'. · Thumb↔hook: K — 「正しかった」 ở 0–3s; cái chết (最後の太刀) chỉ báo trước bằng tiêu đề chương, hook chưa nói — vẫn cùng lời hứa.
- Vì sao giữ người: Đảo thẳng điều ai cũng học (奇襲・酒宴で油断) ngay giây 0 bằng một câu khẳng định tuyệt đối 'đúng trong mọi thứ' — người xem phải ở lại để thấy 'đúng hết mà vẫn thua' là thế nào.
- Điểm yếu: 31–55s là liệt kê năng lực (法・同盟・2万) dạng thuyết giảng, cảnh kịch hoá đầu tiên ~74s. Video cũ (06-12) nên chưa có khẩu hiệu; view 91k tích 3 tháng, nhưng like/view 1,28% + 393 comment = video được 'fan cứng' yêu nhất trong nhóm top.

#### 【千利休】秀吉を支えた茶人は、なぜ切腹を命じられたのか｜戦国時代 — https://www.youtube.com/watch?v=ki5cLTt95AM
- Câu chốt (34s): 「ところが[音楽]その秀吉が理球に 伏を命じることになります。」
- Câu khoá (39s): 「秀吉に徴用 [音楽]された千の球はなぜ伏を命じられ たのか。」
- Chữ thumbnail: 秀吉に何をした？｜千利休の最期 · Mô tả: 千利休の最期の16日を「京を追われた夜の舟」から描く歴史解説ドラマです。
- Hook↔tiêu đề: K — Câu 39s = tiêu đề 「秀吉を支えた茶人は、なぜ切腹を命じられたのか」. · Thumb↔tiêu đề: P — 「千利休の最期」 khớp; 「秀吉に何をした？」 đổi hướng câu hỏi thành 'lỗi của 利休', tiêu đề hỏi 'vì sao bị ra lệnh'. · Thumb↔hook: P — 最期 = '最後の16日' (17s) khớp; 'đã làm gì 秀吉' không có trong hook — câu gần nhất 「あなたは2人の間に何があったと思いますか」 ở ~1127s (CTA cuối).
- Vì sao giữ người: Cảnh chiếc thuyền đêm + '16 ngày cuối' tạo đồng hồ đếm ngược, bức thư còn lưu giữ làm bằng chứng; câu hỏi tiêu đề đọc nguyên văn ở 39s.
- Điểm yếu: Nghịch lý (người bảo trợ ra lệnh chết) tới 34s sau 20s cảnh yên tĩnh; 50–130s sau khẩu hiệu là tiểu sử tuổi thơ 吉郎 (sinh 1522, học trà) — đoạn dễ rơi người xem nhất trong 10 video. 68k sau 5 ngày = đang chạy tốt, chưa phải kết quả cuối.

#### 【前田利家】織田信長に追放された男は、なぜ戦場に現れたのか｜前田利家・執念の二年｜戦国」 — https://www.youtube.com/watch?v=z9DmSetqjuA
- Câu chốt (24s): 「その 獣編みをまたは信長がいる[音楽]矢倉の 下で着たのです。」
- Câu khoá (61s): 「では または追われた織田の家へどうやって帰っ たのでしょうか。」
- Chữ thumbnail: 誰も呼んでいない｜戦場の前田利家 · Mô tả: 前田利家は、本当に槍働きだけの猛将だったのでしょうか。
- Hook↔tiêu đề: P — Tiêu đề hỏi 「なぜ戦場に現れたのか」; hook hỏi 'quay lại bằng cách nào' ở 61s và không nhắc 'chiến trường'. · Thumb↔tiêu đề: K — 「誰も呼んでいない」+「戦場の前田利家」 = 'bị đuổi mà vẫn xuất hiện ở chiến trường' của tiêu đề. · Thumb↔hook: L — 'Không ai gọi' / 'chiến trường' vắng trong 120s đầu: 「呼ばれていない」 lần đầu ~652s (chương 9:36 呼ばれていない戦場へ).
- Vì sao giữ người: Cảnh chém người hầu của chủ ngay dưới lầu chủ là biến cố cực lạ và dễ dựng; thoại 「犬か。犬が来たのか」 cho người xem biệt danh 犬 của 利家 (fan game biết).
- Điểm yếu: Câu hỏi của video tới 61s và lệch tiêu đề; lời hứa của thumbnail/tiêu đề (tự ý ra trận không ai gọi) nằm ở phút 9–15. 70s+ lại lùi về tuổi thơ 荒子/犬千代. Đăng 08-28 giữa lúc kênh đang lên (h9 09-04 774k) mà chỉ 16k → không đổ cho tuổi kênh.

#### 【松永久秀】「稀代の悪人」は本当に奈良の大仏を焼いたのか｜信長が欲した平蜘蛛｜戦国 — https://www.youtube.com/watch?v=gVasfPnkTqU
- Câu chốt (56s): 「ここ までの話は後の世が作ったものです。」
- Câu khoá (68s): 「本当の久秀はどんな男 でなぜここまで言われることになったの でしょうか?」
- Chữ thumbnail: 茶釜と果てた男｜大悪人、松永久秀 · Mô tả: 織田信長に背き、東大寺大仏殿を焼き、将軍を討ったと言われる戦国の梟雄━━稀代の悪人と呼ばれた男の実像に迫ります。
- Hook↔tiêu đề: P — 「大仏を焼いたのか」 chỉ lướt qua ở ~66s trong danh sách tội; hook hỏi 'là người thế nào', còn 0–56s là 平蜘蛛 (vế thứ 2 của tiêu đề). · Thumb↔tiêu đề: P — 「大悪人、松永久秀」 khớp 「稀代の悪人」; 「茶釜と果てた男」 khớp vế 「信長が欲した平蜘蛛」 — thumbnail bỏ vế 大仏 là câu hỏi chính của tiêu đề. · Thumb↔hook: K — 0–56s chính là cảnh 'chết cùng ấm trà', 59s 「悪人」.
- Vì sao giữ người: Giai thoại 平蜘蛛 nổ tung là cảnh điện ảnh nhất trong 10 video, và cú 'tất cả là đời sau bịa' đảo ngược nó.
- Điểm yếu: Cú đảo tới 56s — người xem đã xem 1 phút một chuyện mà video sắp nói là bịa; câu hỏi 68s; tiêu đề có 2 lời hứa (大仏 + 平蜘蛛). Thumbnail là file DUY NHẤT trong 10 chỉ có 480×360 (không có bản maxres) và chữ thu nhỏ không dính mép như 9 cái kia. 5,3k dù đăng 08-21 giữa giai đoạn kênh tăng — gói đăng + hook muộn là nghi phạm, nhưng không tách được khỏi yếu tố đề tài (久秀 không thuộc trục 織田–豊臣–徳川 chính).

#### 【備中高松城】教科書が教えない、歴史の裏側ー兵を失わず勝利を手にする奇策とは？ — https://www.youtube.com/watch?v=lG0EzwtTfmw
- Câu chốt (8s): 「しかしビッチ中 高松城の水攻めの真実は決してそんな 綺麗事ではありません。」
- Câu khoá (15s): 「その裏にあったの は5000の命と莫大な金[音楽]を天秤 にかけた戦国史場最も残酷で泥臭い極限の 騙し合い[音楽]だったのです。」
- Chữ thumbnail: 備中高松城の水攻め (không có dòng vàng) · Mô tả: 備中高松城――。
- Hook↔tiêu đề: P — Tiêu đề đứng về phía thông thuyết 「兵を失わず勝利を手にする奇策とは？」, hook ở 8s nói điều ngược lại (không phải chuyện đẹp) — cùng sự kiện, ngược khung. · Thumb↔tiêu đề: P — Chỉ có tên sự kiện 「備中高松城の水攻め」, không có dòng vàng nghịch lý nào. · Thumb↔hook: P — Tên sự kiện khớp; không có gì của cú đảo 8s hay '5000 mạng' lên ảnh.
- Vì sao giữ người: Cấu trúc đảo thông thuyết đầy đủ trong 25s (thông thuyết → 'bạn cũng được dạy thế' → 'không phải chuyện đẹp' → 5000 mạng) — về hook là ổn.
- Điểm yếu: Thua vì lý do khác hook: video ĐẦU TIÊN của kênh (2026-04-10), tiêu đề không có tên nhân vật (chỉ có tên thành), thumbnail thiếu dòng vàng, mô tả chưa theo khuôn, và 32–130s là bài giảng kinh tế không nhân vật. Không nên kết luận 'kiểu hook đảo thông thuyết yếu'.

### Các tập của mình

Lane sengoku-uragawa chưa có tập nào (0 tập: E:\CLAUDE\YOUTUBE\h2dev\assets\sengoku-uragawa\ chỉ có branding\). Không có gì để chấm; dùng formula.khuon_tap_dau làm khuôn tập 1. 3 kiểm tra nên thành gate khi viết tập 1: (a) câu hỏi tiêu đề trong ~160 chữ đầu, (b) chữ dòng vàng thumbnail có trong ~160 chữ đầu, (c) ≥1 tài liệu gốc có nơi lưu trữ trước ~190 chữ (35s).

### Nguyên tắc
- **Chọn nhân vật/trận thuộc trục 織田–豊臣–徳川 hoặc có fandom manga/game TRƯỚC khi nghĩ tới hook.** — cơ chế: Người xem click vì đã biết tên; 'mặt sau' chỉ hấp dẫn khi 'mặt trước' đã quen. · bằng chứng: g9NiHpRWP0g hook 6/12 → 466k; lG0EzwtTfmw hook đảo ở 8s nhưng tiêu đề không tên người → 3,3k; h9tW20hT2ks (花の慶次 trong tiêu đề) 774k; cả kênh: 春日局 10k, 寧々 4,4k, 近藤勇 6,4k, ジョン万次郎 5,1k. · vì sao: Không hook nào bù được một cái tên không ai tìm — kênh mẫu chứng minh cả chiều thuận và nghịch. · áp dụng: Tập 1–3 của sengoku-uragawa chọn từ danh sách còn trống đã kiểm (織田信長/豊臣秀吉/伊達政宗/真田幸村/上杉謙信/武田信玄), đưa tên game/anime/大河 vào thân tiêu đề nếu có.
- **Nói câu hỏi của tiêu đề (gần nguyên văn) trước giây ~30.** — cơ chế: Người xem đến với câu hỏi của tiêu đề; nghe lại nó xác nhận 'đúng video mình muốn', chưa nghe thì cảnh kịch hoá chỉ là cảnh lạ. · bằng chứng: Top: h9 22s, Sd 24s, BT 27s, Tun 0s, Qb 31s. Thấp: z9 61s (16k), gV 68s (5,3k). ki5 39s (68k/5 ngày) ở giữa. · vì sao: Là đòn bẩy hook duy nhất trong kênh có tương quan rõ với view mà không đổi đề tài. · áp dụng: Gate cho lane: câu chứa 「なぜ」/「本当に」 lặp ≥60% chữ tiêu đề phải xuất hiện trong ~160 chữ đầu (≈30s ở 325 chữ/phút).
- **Kiểu 'giai thoại → đời sau bịa' phải nói 'bịa' TRƯỚC khi kể giai thoại dài.** — cơ chế: Kể giai thoại trọn 1 phút rồi mới lật khiến người xem không biết video nói về gì và cảm thấy mất thời gian với thứ vừa bị phủ định. · bằng chứng: Cùng kiểu mở H39: h9tW20hT2ks lật ở 15s rồi mới dựng giai thoại (44–130s) → 774k; gVasfPnkTqU dựng giai thoại 0–56s rồi lật → 5,3k. · vì sao: Giữ được cả 2 cái lợi: tò mò 'thật thế nào' + vẫn được xem cảnh giai thoại hấp dẫn. · áp dụng: Tập có giai thoại nổi tiếng: 0–5s gọi tên + 'ai cũng biết qua game', ≤18s 'những chuyện đó viết sau N năm', ≤30s vật chứng, rồi mới dựng giai thoại.
- **Thumbnail = 2 dòng đọc liền; dòng vàng là nghịch lý '〜のに〜' không có tên, dòng đỏ là tên (+の最期).** — cơ chế: Nghịch lý tạo câu hỏi trong 1 lần nhìn; tên ở dòng đỏ lớn bảo đảm người biết nhân vật nhận ra ngay. · bằng chứng: 3/3 dòng vàng '〜のに' đều ở top (g9 466k, BT 213k, Sd 91k); 9/10 có dòng vàng, cái duy nhất thiếu là lG0 3,3k; gV (5,3k) là cái duy nhất 480×360 chữ thu nhỏ. · vì sao: Kênh dùng template cố định 21/21 nên khác biệt nằm ở CHỮ dòng vàng — nơi đáng tối ưu. · áp dụng: Mỗi tập viết 3 phương án dòng vàng: 1 '〜のに', 1 con số (たった41人), 1 'được tạo ra/bịa' (作られた…); chọn cái có trong 30s đầu hook.
- **Chữ trên thumbnail phải có mặt trong 30s đầu hook.** — cơ chế: Thumbnail là lời hứa thứ 2; nếu hook không nhắc, người vào vì thumbnail không thấy lời hứa được xác nhận. · bằng chứng: thumb↔hook K ở 4/10 (BT, Tun, Sd, gV); L ở z9DmSetqjuA ('呼んでいない' ~652s) — 16k; BT (K cả 3 chỗ) 213k. · vì sao: Thumbnail↔hook là mắt xích gãy nhiều nhất trong kênh mẫu (6/10 chỉ P/L) — làm đúng là lợi thế so với chính kênh mẫu. · áp dụng: Kiểm máy: grep chữ dòng vàng (hoặc từ khoá của nó) trong ~160 chữ đầu script; không có → đổi chữ thumbnail hoặc đưa câu đó lên.
- **Neo hook bằng bằng chứng gốc có tên + nơi lưu giữ.** — cơ chế: Khán giả sử (nam 40+) cần lý do tin 'mặt sau' không phải bịa tiếp; vật chứng có địa chỉ biến lời hứa thành kiểm chứng được. · bằng chứng: h9tW20hT2ks 29–38s 『前田慶次道中日記』 + 市立米沢図書館 (774k); ki5cLTt95AM 24s 「その手紙は今も残っています」; mô tả có mục tài liệu gốc 10/10. · vì sao: Là thứ tách kênh 'mặt sau lịch sử' khỏi kênh kể giai thoại, và khớp luật cứng lane (không bịa, tách truyền thuyết/sử liệu). · áp dụng: series_ctx.txt của mỗi tập phải có ≥1 tài liệu gốc có nơi lưu trữ; hook nêu nó trước ~35s; mô tả liệt kê ở 【本動画の主な参考文献・一次資料】.
- **Làm chuỗi 2 tập cho nhân vật lớn, tập 1 kết bằng lời hẹn tập 2.** — cơ chế: Người xem xong tập 1 có sẵn câu hỏi kết cục; mô tả + màn cuối dẫn thẳng sang. · bằng chứng: QbPKiRRXM5E (清須会議, 07-31, 219k) kết bằng 「次は柴田勝が最後に選んだ戦場静の物語へ続きます」 → g9NiHpRWP0g (賤ヶ岳, 08-07) 466k dù hook yếu. Chỉ 1 cặp trong kênh — bằng chứng mỏng. · vì sao: Cặp duy nhất trong kênh đã cho video view cao thứ 2 dù hook yếu nhất nhóm top. · áp dụng: Với 1 nhân vật lớn (vd 織田信長), lên kế hoạch 2 tập theo mốc thời gian; màn cuối tập 1 hẹn tên trận/sự kiện tập 2; tập 2 mô tả link tập 1.

### Lưu ý dữ liệu
- MỐC GIÂY LÀ ƯỚC TÍNH (timing_source='est') cho cả 10/10 video: raw\<id>.json đều có hook_segments RỖNG (transcript_via='none', đã mở lại ngay trước khi ghi file). Mốc = vị trí ký tự ÷ (len(transcript)/duration) trên transcripts.json của h2dev, tính cả token [音楽]. Sai số dự kiến ±5–10s vì nhạc/thoại ngắt quãng; so sánh GIỮA các video vẫn dùng được, số tuyệt đối không.
- Trích dẫn giữ NGUYÊN VĂN ASR (có lỗi tên riêng): 刑事=慶次, 小田/小だ=織田, 勝井/勝=勝家, 静=賤ヶ岳, 橋=羽柴, 乗らない=載らない, こ宵い=今宵, 線の利球/理球=千利休, 伏=切腹, 吉本=義元, 田家=武田家, 安/言=家康, A62年=永禄2年, 獣編=拾阿弥, 平雲=平蜘蛛, 規作=奇策, ビッチ中=備中.
- intro_t: kênh KHÔNG có tự giới thiệu người kể; intro_t ghi thời điểm khẩu hiệu nghi thức (tương đương 'lời chào kênh'). null = không có khẩu hiệu trong 120s (SdRuge8_gvM, gVasfPnkTqU). promise_t = lúc video nói sẽ cho xem gì (bằng chứng/góc nhìn/đếm ngược), không phải 'N điều'.
- View lấy từ raw (tải 2026-09-23). ki5cLTt95AM mới 5 ngày (68k) nên không xếp vào top/thấp khi so. Tương tác lệch: like/view cao nhất ở video cũ view thấp (lG0 1,86%, Sd 1,28%) — fan cứng giai đoạn đầu; video top gần đây like/view 0,16–0,53%.
- gVasfPnkTqU: thumbnail trong HOOK_LIBRARY\thumbs chỉ 480×360 — có thể YouTube không có bản maxres cho video này (thumbnail tải lên nhỏ) hoặc tải về bị hạ cấp; đã so với E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\_raw\thumbs\18_5k_gVasfPnkTqU.jpg cùng dung lượng 26.544 byte → cùng nguồn. Chưa kiểm được trực tiếp trên YouTube (IP bị chặn).
- E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\sengoku-uragawa\BAO_CAO_DO_THUMB_DNA.md có tiêu đề sai ('LANE G teinengo-tanoshimi') và bảng §3 (băng nền đen, nhãn vàng, panel so sánh) + §5 mục 4 là nội dung của lane tanoshimi, KHÔNG áp dụng cho kênh này. Bảng §2 đo máy cũng trượt: BTCIRj8agB4 và SdRuge8_gvM ghi '—' băng trên dù ảnh có dòng vàng rõ; ki5cLTt95AM màu băng trên #4C3825 (sai, ảnh là vàng). Chỉ dùng từ file đó: màu #FBEE08/#D90304 và tỉ lệ cao/rộng dòng chữ. Nên sửa file đó (việc của dự án research, chưa làm trong lượt này).
- E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\sengoku-uragawa.md §4 bước 2 vẫn ghi 'ref_lock … 1 võ tướng chibi' và 'thumbnail = chibi nhân vật' — mâu thuẫn với §1 cùng file và THUMBNAIL_PATTERNS.md (không phải chibi). Chỉ đọc, không sửa (ngoài phạm vi).
- Chưa có profile E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\sengoku-uragawa.json → không có char_rate của lane; con số 160 chữ ≈ 30s dùng tốc độ đọc đo từ kênh mẫu (288–329 chữ/phút, bỏ [音楽]/khoảng trắng).
- Mọi nhận định 'thắng vì X' là tương quan trên 10 video của 1 kênh; đề tài và hook bị lẫn vào nhau (video đề tài lớn cũng thường hook tốt hơn). Chỗ tách được rõ: g9 (hook yếu, view cao) và lG0 (hook đạt, view thấp).
- our_eps rỗng: lane sengoku-uragawa chưa có tập nào (E:\CLAUDE\YOUTUBE\h2dev\assets\sengoku-uragawa\ chỉ có branding\; không có eps_sengoku-uragawa.json trong scratchpad) → thay bằng formula.khuon_tap_dau.