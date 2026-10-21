> BẢN DỰNG TAY 2026-09-26 — số đo từ 6 tiêu đề thật của kênh mẫu + gate đã khai trong profile.

# 02 TITLE RULES — M · teinengo-anaba

## Số đo từ 6 tiêu đề THẬT của kênh mẫu 大人の盲点
| View | Ký tự | Tiêu đề gốc (dịch) |
|---|---|---|
| 92.034 | 53 | 【漫画】60代以降でも気楽に働ける人気のアルバイト・パート7選｜64歳男性が見つけた"無理なく続く仕事" (7 việc làm thêm người 60+ làm thoải mái ｜ "việc làm bền không gắng sức" mà người đàn ông 64 tuổi tìm ra) |
| 26.982 | 48 | 【漫画】60代以降でも一人で一生遊べる人気の娯楽・趣味7選｜定年後が待ち遠しくなる楽しみ (7 thú vui chơi một mình cả đời) |
| 11.145 | 47 | 【漫画】周りから愛される60代が使う魔法の口癖7選｜幸せな人生・人間関係を作る秘訣 (7 câu cửa miệng được mọi người quý) |
| 10.442 | 51 | 【漫画】60代が「楽そう」で選ぶと後悔するアルバイト・パート13選｜定年後の仕事選びの落とし穴 (13 việc trông nhàn mà chọn là hối hận) |
| 6.634 | 58 | 【漫画】なぜ定年後も働き続けるシニアが増えたのか？60代以降が退職後に再就職・アルバイトをする7つの理由とは (vì sao ngày càng nhiều người hưu vẫn đi làm?) |
| 1.005 | 51 | 【漫画】60代の再就職で月5万円を目指すには？無理なく続けやすい定年後のアルバイト・パート11選 (nhắm 5 vạn yên/tháng thì làm gì?) |

Trung bình 51 ký tự, dao động hẹp 47–58.

## Công thức lặp
`【漫画】 + [đối tượng: 60代 / 60代以降 / 定年後] + [trạng thái hoặc nỗi sợ hoặc mục tiêu] + N選 ｜ [vế phụ: nhân vật cụ thể hoặc lời hứa]`
Từ khoá bắt buộc xuất hiện: 【漫画】 · 60代 hoặc 定年後 · アルバイト・パート hoặc 仕事 · ○選.

## Luật của lane (đã khai trong `profile.script.gate`, đo từ 6 transcript)
1. Tiền tố 【漫画】 bắt buộc. `title_suffix_ignore` bỏ 【漫画】 khi đếm phần lõi.
2. Tổng **40–56 ký tự** (gate), mục tiêu 41–50. Phần lõi (bỏ 【漫画】) 37–52 ký tự.
3. Luôn có **số mục N選**, N khớp `list_item_count` = 7 và khớp số mục thật trong kịch bản.
4. Dùng dấu ｜ tách vế chính và vế phụ, giống 6/6 video kênh mẫu có vế phụ.
5. **Góc LỢI ÍCH thắng góc CẢNH BÁO**: hit 92k là "làm thoải mái", còn "chọn là hối hận" chỉ 10k — chênh 2–5 lần.
   Chỉ dùng góc cảnh báo khi tập đó thật sự là tập bẫy.
6. Thêm móc **TIẾT KIỆM** mà kênh mẫu chưa dùng: 0円 (0 yên) · 交通費0円 (0 yên tiền đi lại) · 年金を減らさず (không bị trừ lương hưu) ·
   資格なし (không cần bằng cấp). Đối thủ cùng thể loại vượt 180k view đều gắn móc này.
7. Số viết chữ số Ả Rập nửa độ rộng (60代, 7選, 5万円, 週3日).
8. **Không lộ hạng 1** — hạng 1 là phần thưởng cuối video, thumbnail cũng giấu.
9. Mọi vế phải có trong kịch bản: nghề, số giờ, lương giờ, số ca đều phải tra ra được.

## KHÔNG được
- Đề tài ngoài trụ cột việc làm: sở thích, du lịch, chơi 0 yên (Lane G) · drama mất tiền (Lane F) · trục vợ chồng (Lane J).
- Chép nguyên tiêu đề hit của kênh mẫu — mượn khuôn câu, đổi hết chữ.
- Hứa thu nhập như cam kết (「月10万円確実」 — chắc chắn 10 vạn/tháng).
- Dùng tên nhân vật kênh mẫu 高瀬 hoặc câu 「盲点だった。」.
- Chê bai người trẻ, người tuyển dụng, hay vơ đũa cả nắm một nghề.

## Mười tập đã lên lịch
Xem `09_VIDEO_GOC.md` — mỗi tập đã gắn sẵn ĐÚNG 1 video gốc; tiêu đề tập phải theo khuôn câu của video gốc đó.
