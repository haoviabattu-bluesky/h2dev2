# INSIGHT TỪ BÌNH LUẬN THẬT — Lane J `teinengo-fuufu` (kênh mẫu 老後のゴローさん)

Bước 1 (Claude Code) chắt lọc ngày 2026-09-30 từ **648 bình luận / 15 video** kênh mẫu (YouTube Data API
`commentThreads order=relevance`, tối đa 100/video, gom 2026-09-28).
Dữ liệu gốc: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\comments_15videos.json` ·
phân tích đầy đủ: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\PHAN_TICH_BINH_LUAN_15VIDEO.md`.
Khối **ĐƯA VÀO PROMPT** ở cuối file được `lean_script.py` tự nhồi vào prompt model VIẾT (S2) vì profile khai
`channel_dna_dir: docs/channel_dna/rougo-no-goro`.

## 1. Chủ đề nào kéo cảm xúc (648 bình luận)
| Nhóm | Số BL | Like cao nhất |
|---|---|---|
| Làm tiếp hay nghỉ | 167 (25,8%) | 236 |
| Tiền / tài chính | 110 (17,0%) | 177 |
| **Gia đình / chồng vợ** | 64 (9,9%) | **447** |
| **Chê hình vẽ già** | 18 (2,8%) | **446** |
| Cô đơn | 18 (2,8%) | 447 |

→ Bàn nhiều nhất là chuyện đi làm, nhưng **like cao nhất là chuyện VỢ CHỒNG** — đúng trục Lane J.

## 2. Năm tín hiệu
1. **Nỗi đau số 1 của khán giả nữ: công sức bị coi là đương nhiên.**
   「私がインフルエンザになった時、夫は何にもしてくれなくて、死にそうになりながら食事の仕度をした。一人で暮らしたい」 447👍
   (tôi bị cúm, chồng không làm gì, suýt chết vẫn phải nấu cơm — tôi muốn sống một mình) ·
   「家事をすることはそこまで苦じゃないけど、感謝がないことは許せない」 254👍 (làm việc nhà không khổ, không được cảm ơn mới không tha thứ được) ·
   「うちの旦那は感謝の言葉は言います。ありがとうって。でも何もしません」 93👍 (chồng tôi có nói cảm ơn, nhưng không làm gì cả).
2. **Họ phán xét cách chồng nhìn vợ.** 「妻に対して『俺に反抗的』って思う時点で妻を下に見てますよね」 336👍
   (nghĩ vợ "chống đối mình" là đã coi vợ thấp hơn) · 「俺が養ってやってる！これを言われたら夫婦は終わり」 62👍
   (câu "tao nuôi mày" nói ra là vợ chồng hết). → Chồng trong truyện vô tâm chứ không ác; sự tỉnh ngộ phải thật.
3. **Họ bắt lỗi số liệu lương hưu ngay.** 「年金は手続きしないと振り込まれません」 43👍 (phải làm thủ tục mới nhận lương hưu) ·
   「年金600万円？300万円で天井」 34👍 (lương hưu 600 vạn/năm? trần là 300 vạn) · 「年金15万で小遣い5万円て非現実的」 9👍
   (lương hưu 15 vạn mà tiêu vặt 5 vạn là phi thực tế). → Số chế độ đúng tư liệu; số cá nhân phải hợp lý với mức sống thật.
4. **Chuyện làm hay nghỉ: hai phe đều có lý.** 「立ち仕事のバイトは出来なくなるまでやる。金貰って運動してると思ってる」 177👍
   (làm đến khi không làm được, coi như được trả tiền để tập thể dục) ↔ 「64歳で仕事を辞めた時は70歳までは働こうと…登山やギターを始めたらもう仕事をする気は失せていました」 43👍
   (nghỉ 64 định làm tới 70, bắt đầu leo núi với guitar là hết muốn đi làm). → Không phán ai đúng; câu hỏi cuối để mở.
   Cảnh báo sức khoẻ: 「２万歩…私は3か月で膝を壊し、２年間リハビリ」 32👍 (2 vạn bước/ngày, 3 tháng hỏng gối, 2 năm phục hồi) → vận động ≤10.000 bước.
5. **Chê hình vẽ già — việc của khâu ảnh, không phải kịch bản.** 「この絵は80歳ですね」 446👍 (hình này 80 tuổi rồi) ·
   「今の60代 こんな昭和な感じの描き方は違う」 252👍 (60 tuổi bây giờ không vẽ kiểu Showa). Đã đưa vào `image.character_sheet`.

## 3. Bỏ qua
Bình luận khoe tài sản, chính trị, chê giọng bán hàng LINE của kênh mẫu — không đưa vào kịch bản.

## ĐƯA VÀO PROMPT
- Khán giả là vợ chồng người Nhật 60–75 tuổi. Bình luận được like nhiều nhất là của người VỢ: công sức việc nhà bị coi là đương nhiên, "cảm ơn suông mà không làm gì", nấu cơm cho chồng cả khi mình đang ốm. Nỗi đau của vợ phải hiện bằng VIỆC CỤ THỂ như vậy, không nói chung "vợ khổ".
- Người chồng kể chuyện là người vô tâm vì thói quen cả đời đi làm, KHÔNG phải kẻ ác: không quát, không nói "tao nuôi mày", không coi vợ là "chống đối". Khán giả ghét cay đắng kiểu chồng coi vợ thấp hơn mình — sự tỉnh ngộ của anh ta phải bằng hành động, không chỉ bằng lời cảm ơn.
- Số liệu lương hưu và chế độ phải đúng như tư liệu: lương hưu phải làm thủ tục mới nhận, trả 2 tháng một lần, có mức trần; tiền tiêu vặt và chi tiêu cá nhân phải hợp với mức lương hưu thật. Khán giả bắt lỗi sai số ngay trong bình luận.
- Chuyện đi làm tiếp hay nghỉ hẳn: cả hai phe đều có lý, đừng phán xét phe nào; con số vận động hợp lý (không đi 2 vạn bước mỗi ngày).
- Cuối video hỏi khán giả một câu 2–3 lựa chọn về chính cuộc sống vợ chồng họ và mời kể chuyện nhà mình trong bình luận — đây là loại bình luận nhiều nhất.
