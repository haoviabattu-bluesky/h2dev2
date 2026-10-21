# INSIGHT TỪ BÌNH LUẬN THẬT — Lane G `teinengo-tanoshimi` (kênh mẫu 老後のお金ストーリー)

Bước 1 (Claude Code) đọc và chắt lọc ngày 2026-09-26 từ 214 bình luận khán giả / 20 video
(nguyên văn xếp theo lượt thích: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougo-money-story\COMMENTS_TOP.md`,
dữ liệu gốc `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\G_tano\comments.json`).
Khối **ĐƯA VÀO PROMPT** ở cuối file được `lean_script.py` tự nhồi vào prompt model VIẾT (S2) — sửa khối đó là đổi
cách viết của mọi tập sau.

**Lưu ý đọc trước:** kênh G là dạng **liệt kê N選** (5 địa điểm/7 thói quen/5 cách tiêu khiển…), không phải truyện
1 nhân vật xuyên suốt như Lane F — tín hiệu "giận" ở đây thường là giận **cách đóng khung phân loại người** (kiểu
"一流"/"下流老人"), không phải giận 1 nhân vật cụ thể.

## 1. Video nào nổ và vì sao (view đo thật)
| Video (dịch) | View | Bình luận |
|---|---|---|
| なぜか老けない50代男性が「毎日やっていること」7選 (7 việc người 50 tuổi không già làm mỗi ngày) | 203.730 | 45 |
| 一生に一度は参拝したい…定年後に行くべき神社5選 (5 đền thờ nên đi sau nghỉ hưu) | 174.228 | 0 |
| 定年後、最強の暇つぶし5選…実は1円もかからない (5 cách giết thời gian sau nghỉ hưu — 0 yên) | 166.621 | 42 |
| ６０代から人生が心地よくなる…ちょうどいい生き方５選 (5 cách sống vừa đủ để đời thoải mái từ tuổi 60) | 115.219 | 11 |
| 夜行バスに2万円！？豪華夜行バスに65歳で乗ってみた結果 (Xe khách đêm giá 2 vạn yên, thử ở tuổi 65) | 108.242 | 18 |
| 定年後、一流だけがやっている休日の過ごし方5選【世間の非常識】 (5 cách nghỉ cuối tuần chỉ giới "hạng nhất" làm) | 95.648 | 15 |

Video có **"0 yên/miễn phí" ngay trong tiêu đề** (166k view) kéo tương tác rất mạnh dù không phải video xem nhiều
nhất. Video xem nhiều thứ 2 (174k, đền thờ) lại **0 bình luận** — chủ đề thuần liệt kê địa danh không có góc tranh
luận thì view cao nhưng không ai bình luận gì.

## 2. Năm tín hiệu rút ra
1. **Khán giả THÍCH tranh luận/bổ sung mục còn thiếu trong danh sách N選, không chỉ đọc thụ động.** Video "7 thói
   quen không già" có hẳn cuộc tranh luận: 「肉を食べるっていうよりたんぱく質をしっかり取るってことじゃないのかなあ」
   (không phải ăn thịt mà là nạp đủ đạm chứ, 38 like) · 「酒タバコ好きな人ってほんと老けてるやつ多い」 (người mê rượu
   thuốc thường già nhanh, 25 like) · nhiều người tự thêm mục riêng (温泉, 筋トレ cụ thể). → Cố tình để lại **1–2 mục
   trong danh sách có thể gây tranh cãi nhẹ** (ví dụ rượu/bia) để khán giả tự vào bàn luận, thay vì liệt kê toàn ý
   an toàn.
2. **"0 yên/miễn phí" là từ khoá kéo tương tác mạnh nhất đo được.** Video "1円もかからない" (không tốn 1 yên nào) đạt
   42 bình luận dù view thấp hơn video đền thờ — khán giả chia sẻ đúng sở thích giết thời gian miễn phí của họ. →
   Ưu tiên góc "miễn phí/rẻ" khi liệt kê hoạt động cho người già, đây là từ khoá hiệu quả hơn "sang trọng/cao cấp".
3. **Khán giả PHẢN ỨNG MẠNH với khung phân loại đẳng cấp kiểu "一流/勝ち組/下流老人".** Video dùng khung "chỉ giới
   hạng nhất mới làm" bị phản bác: 「なんでそんなに予定で埋めたがるのか😅暇でダラダラ最高じゃん」 (sao phải lấp đầy lịch
   làm gì, ườn oài mới sướng, 13 like) và 1 bình luận gay gắt hẳn: 「資本主義の競争概念を老後を迎えた高齢者にまで持ち込む
   狭い価値観…下流老人とののしる…人として下等である」 (mang tư duy cạnh tranh tư bản áp vào cả người già nghỉ hưu, mắng
   họ là "hạ lưu", đó mới là hạng thấp kém). → **Tránh khung phân loại đẳng cấp** ("chỉ người thành công mới…"),
   nên đóng khung là "cách nào cũng được, tuỳ mỗi người" thay vì áp 1 chuẩn "đúng".
4. **Giọng đọc đều đều/vô cảm bị chê nặng ở video liệt kê địa danh.** 「大野和彦さん、抑揚のない一本調子の陰気な語り口で、
   全く旅の良さが伝わらない」 (giọng đều đều u ám, không truyền tải được cái hay của chuyến đi, 6 like) · 「ちょっとだけ、
   棒読みやね」 (đọc hơi như trả bài, 1 like). → Video dạng liệt kê địa điểm ĐẶC BIỆT cần giọng đọc có nhấn nhá/cảm
   xúc, đọc phẳng sẽ bị chê ngay dù nội dung tốt.
5. **Câu hỏi tương tác cuối mô tả kiểu quiz hầu như KHÔNG hiệu quả.** 2 video có bảng câu hỏi trắc nghiệm cuối mô tả
   ("bạn đồng cảm với nhân vật nào 1-2-3-4-5") chỉ nhận đúng 1 bình luận/video, và bình luận đó cũng không trả lời
   câu hỏi. → Đừng dựa vào dạng CTA quiz cuối mô tả để tăng tương tác thật, không có bằng chứng nó hiệu quả.

## 3. Góp ý sản xuất (không phải kịch bản — chuyển tab lane xem)
- Chê giọng đọc đơn điệu/đọc như trả bài ở video liệt kê địa danh (xem tín hiệu 4).
- Chê chất lượng AI: 「キャラが安定しなかったり適当なAI絵と間違った日本語音声で内容が入ってこんつまらん」 (nhân vật
  không nhất quán, tranh AI qua loa, giọng tiếng Nhật sai làm chán) — 1 video cụ thể, cần soi nhất quán khuôn mặt.
- Có 1 bình luận chỉ lỗi thực tế địa lý ("金色の鳥居…ひろめ市場付近にある神社" chỉ rõ vị trí sai) — nội dung liệt kê địa
  danh cần kiểm tra địa lý/tên gọi chính xác vì khán giả địa phương sẽ bắt lỗi ngay.

## ĐƯA VÀO PROMPT
- Trong danh sách N選, cố tình để lại 1–2 mục có thể gây tranh luận nhẹ (ví dụ thói quen gây tranh cãi) thay vì toàn mục an toàn — đây là thứ khiến khán giả vào bàn luận/bổ sung ý kiến riêng.
- Ưu tiên góc "miễn phí/tốn ít tiền" khi liệt kê hoạt động cho người già — hiệu quả hơn hẳn góc "sang trọng/đẳng cấp".
- Tuyệt đối tránh khung phân loại đẳng cấp kiểu "chỉ người thành công/hạng nhất mới làm được" hay ngụ ý người khác là "hạng dưới" — khán giả phản ứng rất gay gắt với kiểu đóng khung này. Đóng khung là lựa chọn cá nhân, không có đúng-sai.
- Nếu liệt kê địa danh/quán/địa điểm cụ thể, kiểm tra tên gọi và vị trí địa lý chính xác — khán giả địa phương bắt lỗi ngay khi sai.
- Không dùng câu hỏi tương tác kiểu trắc nghiệm ở cuối mô tả để câu tương tác — dữ liệu cho thấy không hiệu quả.
- Giọng kể cần có nhấn nhá/cảm xúc thật, tránh giọng đều đều kiểu đọc báo cáo — đặc biệt quan trọng với nội dung liệt kê địa điểm/trải nghiệm.
