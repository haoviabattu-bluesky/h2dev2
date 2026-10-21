# INSIGHT TỪ BÌNH LUẬN THẬT — Lane K `yakkyoku-sukatto` (kênh mẫu 千種テンカ / @iyaku_labo)

Bước 1 (Claude Code) đọc và chắt lọc ngày 2026-09-26 từ 186 bình luận khán giả / 7 video
(nguyên văn xếp theo lượt thích: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\COMMENTS_TOP.md`,
dữ liệu gốc `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\iyaku_labo\comments.json`).
Khối **ĐƯA VÀO PROMPT** ở cuối file được `lean_script.py` tự nhồi vào prompt model VIẾT (S2) — sửa khối đó là đổi
cách viết của mọi tập sau.

## 1. Video nào nổ và vì sao (view đo thật)
| Video (câu cửa miệng) | View | Bình luận |
|---|---|---|
| 「じゃあ、辞めます」 (vậy thì tôi nghỉ) | 307.286 | 80 |
| 「自分、仕事できるんで」 (tôi làm được việc mà) | 57.847 | 76 |
| 「残業代入んないんで」 (có được trả tiền làm thêm đâu) | 34.496 | 32 |
| 「代わりはいくらでもいる」 (thay người thì thiếu gì) | 20.261 | 13 |

Cả 4 video dài đều là **một nhân vật đáng ghét + câu cửa miệng**. Video càng làm người xem **ức chế** thì càng nổ:
bình luận top của video 307k toàn là giận/phán xét nhân vật.

## 2. Năm tín hiệu rút ra
1. **Cơn giận là động cơ tương tác.** Top like: 「辞職を匂わす言葉を口にする人は早々に切ったほうがいい」 (ai dọa nghỉ thì
   cắt sớm, 345 like) · 「辞める辞める詐欺。卑怯者だと思う」 (lừa dọa nghỉ, đồ hèn, 268) · 「自分、仕事出来るんでって言う奴で
   仕事出来る人を見た事ない」 (chưa thấy ai nói câu đó mà làm được việc, 94). → Nhân vật chính phải **đủ đáng ghét** trong
   hành vi cụ thể, không được mờ nhạt.
2. **Người xem mang chuyện thật của họ vào.** 「昔勤務してた衣料品店にいたパートさんも『じゃあ辞めます』…三度目に『分かりました』
   と言われて辞めていきました」 (bà bán thời gian ở tiệm quần áo cũ cũng nói vậy, lần 3 bị đáp "được thôi", 218 like) ·
   chuyện tiệc chia tay mà người dọa nghỉ vẫn không nghỉ (69). → Chi tiết đời thường kiểu "lần thứ 3 bị đồng ý" là thứ
   khán giả nhận ra ngay — ưu tiên loại chi tiết này.
3. **Họ thương người tốt lặng lẽ gánh việc.** 「まともな上司がいる薬局で羨ましい」 (thích nhà thuốc có sếp tử tế, 230) ·
   「静かにフォローしながら職場が回っていくのがすごい」 (hay ở chỗ mọi người lặng lẽ đỡ việc mà nơi làm vẫn chạy). → Phải cho
   thấy RÕ cái giá người khác trả (đúng khung 7 chặng đang có).
4. **Cuối cùng họ chuyển sang thương hại/tự soi mình.** 「きっと寂しい人だったの」 (chắc là người cô đơn) · 「気の毒な面はある」
   (cũng đáng thương) · 「『答えを自分の外に探している』心に深く刺さりました…私自身も反省すべきことは沢山あります」 (câu "tìm câu
   trả lời ở bên ngoài mình" đâm thẳng vào tim, tôi cũng phải tự xem lại). → Kết cần 1 câu đạo lý ngắn đáng nhớ + 1 nhịp vị tha.
5. **Họ bắt lỗi nghiệp vụ và lỗ hổng cốt truyện.** 「一日平均処方箋40枚に薬剤師1人以上」 (định mức 1 dược sĩ / 40 đơn mỗi ngày —
   "người làm phim có hiểu nhầm gì không?") · みなし残業 (tiền làm thêm khoán): 「法律上残業をする義務はない」 (luật không bắt buộc
   làm thêm) và 「店長はなぜ固定残業代について言わなかった？」 (sao cửa hàng trưởng không nói về tiền khoán?) · khách đến sát giờ đóng
   cửa 「老人もかなり厚かましい」 (ông cụ cũng khá quá quắt). → Nghiệp vụ dược và luật lao động phải ĐÚNG; người "bị hại" cũng
   không được vô lý, kẻo khán giả quay sang bênh nhân vật xấu.

## 3. Góp ý sản xuất (không phải kịch bản — chuyển tab lane xem)
- Khen: 「イラスト上手い」 (tranh đẹp), 「誤字、読み間違いがない…クオリティー高い」 (không sai chữ/đọc sai, chất lượng cao) → giữ cổng
  phụ đề/đọc đúng.
- Chê: nhân vật dân thường dùng chức danh như công chức (「官称」); mặt nhân vật trông như chính trị gia, 「薬局職員の人相じゃない」
  (không giống nhân viên nhà thuốc).
- Bình luận chính trị (自民党, 立憲共産党…) → BỎ QUA, không đưa vào kịch bản.

## ĐƯA VÀO PROMPT
- Khán giả kênh mẫu tương tác mạnh nhất khi nhân vật chính ĐÁNG GHÉT RÕ RÀNG qua hành vi cụ thể (bình luận top toàn là giận, phán xét). Đừng làm nhân vật chính mờ nhạt hay "chỉ hơi phiền".
- Mỗi lần câu cửa miệng được dùng, phải cho thấy một người tử tế cụ thể trả giá (ăn trưa lúc 3 giờ, về muộn, con chờ) — khán giả thương những người lặng lẽ gánh việc và ghét sự vô tâm.
- Ưu tiên chi tiết đời thường mà người đi làm nào cũng từng gặp (lần thứ 3 bị "được thôi", tiệc chia tay mà không nghỉ) — khán giả kể lại đúng những chi tiết kiểu này trong bình luận.
- Người bị ảnh hưởng (bệnh nhân, khách) KHÔNG được vô lý, đến sát giờ vô cớ, hay đòi hỏi quá đáng — nếu không khán giả sẽ quay sang bênh nhân vật xấu.
- Nghiệp vụ nhà thuốc và luật lao động phải đúng (định mức dược sĩ theo đơn thuốc, みなし残業 = tiền làm thêm khoán, trách nhiệm cửa hàng trưởng) — khán giả kênh này bắt lỗi rất nhanh.
- Kết có 1 câu đạo lý ngắn, sắc, dễ nhớ (kiểu 「答えを自分の外に探している」 — tìm câu trả lời ở bên ngoài mình) và 1 nhịp thương cảm với chính nhân vật xấu (cô đơn, sợ bị thay thế) — không hả hê.
