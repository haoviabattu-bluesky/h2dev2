# GOLDEN_001_hidden_move — "bạn thân giấu chuyện chuyển nhà 3 năm"

- **Lane:** satori_jp (`satori-jp-obaa`) · **Tập:** 1 · slug `assets/satori_jp/simbot2-01-vU5PWT2zLDs`
- **Trạng thái:** FINAL QC PASS + **HUMAN APPROVED 2026-09-17** ("Tôi rất hài lòng với mẫu này") → đồng thời là `MASTER_REFERENCE.png`
- **Loại hook:** NGHỊCH LÝ QUAN HỆ (hai sự thật cùng đúng nhưng không thể cùng tồn tại) + "chỉ mình tôi bị giấu"
- **Ảnh:** `../MASTER_REFERENCE.png`

## Title
`50年の親友が姿を消した理由…煮しめの重箱を抱えて立ち尽くした、73歳の私が知った哀しい真実【朗読】`
→ Lý do người bạn thân 50 năm biến mất… sự thật buồn mà tôi, 73 tuổi, biết được khi đứng chết trân ôm hộp nishime.

## Story core (3 câu)
Shizuko 73 tuổi mang nishime đến chung cư thăm Mitsue — bạn 50 năm — thì người lạ mở cửa: "bà ấy chuyển đi 3 năm trước", trong khi suốt 3 năm đó hai bà vẫn gặp nhau mỗi thứ Năm bên sông Edogawa. Shizuko tự thú 4 lần cái miệng mình làm mất tình bạn (nói số lương hưu, kể bệnh, khoe con, than con). Sự thật của Mitsue: chồng Parkinson, bán nhà trả viện dưỡng lão, đi dọn vệ sinh sáng sớm, chỉ thứ Năm mới kẻ lông mày để trước mặt bạn được là "người không bệnh" — im lặng 50 năm là hàng rào, không phải bức tường.

## Strongest hook (đã chọn)
**"Tuần nào cũng gặp" ↔ "đã chuyển nhà 3 năm trước"** — nghịch lý người xem không tự giải được, phải click.
Phụ: "chỉ mình tôi không biết" (biến "giấu" thành "giấu riêng tôi, người bạn 50 năm").
Bí mật PHẢI giữ: chồng bệnh / bán nhà / dọn vệ sinh / lông mày / hàng rào.

## Final Japanese copy (APPROVED)
```
WHITE|毎週会っていたのに
YELLOW|3年前に
RED|引っ越していた
BANNER|私だけ知らなかった
```
毎週会っていたのに → Tuần nào cũng gặp nhau, vậy mà…
3年前に → Từ 3 năm trước
引っ越していた → Đã chuyển nhà rồi
私だけ知らなかった (banner) → Chỉ mình tôi là không biết

Font đo thật: 78 / 196 / 100px · banner ≈100px · cột 0.60 · `--fit-each`.

## Hình (concept, KHÔNG copy sang tập khác)
Shizuko một mình, 1/3 phải, hành lang chung cư tối, ôm bọc furoshiki 2 tầng jubako cao ngang ngực, mắt mở to ướt, môi hé (sốc câm), cửa sau lưng hé sáng có bóng mờ cô gái lạ. **Phân công:** hình kể cảnh title đã hứa (重箱を抱えて立ち尽くした), chữ kể điều title giấu (vẫn gặp hàng tuần · 3 năm · chỉ tôi).

## Các bản bị loại / yếu — và vì sao

| Bản | Text | Vì sao yếu |
|---|---|---|
| v1 (máy viết cũ) | 光江の家 / 三年前から / 知らない女 / 正体は誰 + banner 五十年の友が黙り続けた | "知らない女 / 正体は誰" đẩy sang hướng bí ẩn danh tính người lạ — **sai trọng tâm** (video không phải về cô gái đó); 4 mảnh rời, không thành 1 nghịch lý |
| v5 (tool) | 73歳の私 / 重箱を抱えて / 立ち尽くした + banner 親友は三年前に消えていた | **lặp title** gần như nguyên văn (73歳・重箱・立ち尽くした); banner nói "biến mất" = đúng thứ title đã nói → thumbnail không thêm thông tin |
| Phương án B (cú sốc) | 親友の家のドアを開けたのは / 知らない女性だった / 「三年前に越されましたよ」 | Dựng lại cảnh title đã gợi; dòng 1 dài 14 ký tự khó đọc 1 giây; nghịch lý bị đẩy xuống banner |
| Phương án C (cảm xúc) | 木曜日だけ / 眉を描いて来ていた親友 / その理由を知った夜 + 涙が止まらなかった | Chi tiết lông mày ở phút 27/30 → **lộ hướng đáp án** (giấu bệnh); khó thể hiện bằng hình. Hợp Shorts cắt đoạn kết hơn |
| Bản 4 dòng + banner 親友が私に隠していたもの | 毎週会っていたのに / 3年前に引っ越していた / 私だけ知らなかった / banner | Banner **lặp ý** (title đã có 真実); 4 dòng làm hook nhỏ |
| Bản KHÔNG banner (model tự bỏ) | 3 dòng + 私だけ知らなかった nhỏ, không banner | **VI PHẠM TEMPLATE** — banner đỏ là visual identity kênh; model tự quyết bỏ = sai |
| Bản có banner nhưng base-size chung (68/78/95px) | như final nhưng dàn đều, chữ nhỏ | "Đọc được ở 360px" nhưng **không đủ cho senior**; dòng dài nhất ép cả khối, khoảng trống dàn đều |

## Human feedback (nguyên văn ý)
1. Template kênh HARD LOCK: nhân vật phải · chữ to trái · **red bottom banner bắt buộc, không optional, cấm tự bỏ**.
2. Senior typography: "readable ≠ good enough"; **fit từng dòng độc lập, dòng ngắn được to hơn dòng dài, khối sát nhau, FONT SIZE > khoảng trống**; render ≥2 variant rồi chọn bản TO NHẤT còn sạch.
3. Bản final: "Tôi rất hài lòng với mẫu này." → freeze.

## Why final worked
- Title nói "biến mất"; thumbnail nói "vẫn gặp hàng tuần" → hai cái đối nhau, người xem đọc cả hai mới thấy
  có chuyện lạ (TITLE + THUMBNAIL = 1 câu hỏi mới). 0/5 từ khoá title bị lặp.
- Tách 1 câu thành `3年前に` (trigger, vàng, 196px) + `引っ越していた` (hook, đỏ, 100px): con số đập vào mắt
  trước, động từ giải thích ngay dưới — đúng tốc độ đọc của người lớn tuổi.
- Banner `私だけ知らなかった` biến sự kiện thành nỗi đau cá nhân, không lặp 3 dòng trên, không lộ đáp án.
- Hình kể đúng cảnh title hứa (ôm hộp, đứng chết trân, cửa lạ hé sáng) nên chữ được rảnh tay kể phần title giấu.

## Generalizable principles (dùng được cho tập khác)
- Tìm thông tin **title cố tình giấu** → đó là đất của thumbnail.
- Nghịch lý 2 vế > cú sốc 1 vế; khoảnh khắc cụ thể > khái niệm.
- Câu dài chứa con số → tách con số ra dòng riêng để nó được phóng to (fit-each).
- Banner = payoff cá nhân / chốt hạ, không lặp ý, không lộ đáp án.
- Chi tiết cảm xúc nhất thường LÀ đáp án → giữ lại, không lên thumbnail.
- Quy trình A/B/C → so → chọn; kiểm lặp title; kiểm spoil; mọi dòng đối chiếu script.

## Case-specific decisions (KHÔNG tái dùng)
- Chữ "3年前", cấu trúc `〜のに / 〜に / 〜ていた`, banner "私だけ〜".
- Hành lang chung cư + cửa hé + bóng cô gái lạ + bọc furoshiki 2 tầng jubako.
- Thứ tự màu TRẮNG → VÀNG → ĐỎ (vì context đứng trước, trigger giữa, hook cuối — tập khác có thể ngược).
- Cột chữ 0.60 dừng ở tay áo x≈770 — phụ thuộc pose của nền tập này.

## Bài học CONTENT
- Title đã nói gì thì thumbnail **không nói lại** — tìm thông tin title cố tình giấu (ở đây: "vẫn gặp hàng tuần").
- Nghịch lý 2 vế (A đúng + B đúng nhưng mâu thuẫn) mạnh hơn cú sốc 1 vế (người lạ mở cửa).
- Câu nói cụ thể trong script > khái niệm trừu tượng ("bí mật của tình bạn").
- Dòng "chỉ mình tôi" biến sự kiện thành nỗi đau cá nhân — không suy ra được từ title → đáng giữ.
- Chi tiết cảm xúc nhất (lông mày thứ Năm) thường là **đáp án** → không lên thumbnail.
- Mọi dòng phải đối chiếu được nguyên văn script; trích dẫn chỉ dùng khi đúng lời nhân vật.

## Bài học TYPOGRAPHY
- Tách câu dài `3年前に引っ越していた` thành 2 dòng theo ranh giới trợ từ → tiếng Nhật vẫn liền, hook to gấp 1,5.
- Dòng 4 ký tự có thể lên ~200px và ĐƯỢC PHÉP to hơn hook — con số/mốc thời gian là trigger.
- Cột chữ chỉ nới được tới mép tay áo nhân vật → **nền phải ghim chủ thể 1/3 phải + đạo cụ cầm cao**, nếu không banner che đạo cụ và chữ đè vai.
- Kiểm 360px là bắt buộc nhưng tiêu chí là "đập vào mắt", không phải "đọc được".

## Anti-overfitting rules (đọc trước khi dùng golden này cho tập khác)
- **Đừng tìm "3年前" trong mọi tập.** Nguyên tắc là "mốc thời gian/con số bất thường làm trigger", không phải con số này.
- **Đừng tái dùng cấu trúc `のに / 〜に / 〜ていた`.** Cấu trúc câu phải mọc từ nghịch lý của tập đó.
- **Đừng tái dùng hành lang + cửa hé + hộp quà.** Mỗi tập gen hình mới đúng cảnh cao trào của script.
- **Đừng mặc định banner = "私だけ〜".** Banner = payoff của tập đó; chỉ giữ vai trò "chốt hạ không lặp ý".
- Nếu tập không có nghịch lý 2 vế, **đừng ép**: chọn hook mạnh nhất thật của tập (cú sốc / bí mật) rồi vẫn áp geometry + typography của TEMPLATE.
- Cái ĐƯỢC copy từ golden này: quy trình 3 phương án A/B/C → so → chọn; phân công hình/chữ; kiểm lặp title; kiểm spoil.
