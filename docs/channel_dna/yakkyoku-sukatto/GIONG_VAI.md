# GIỌNG ↔ VAI của kênh mẫu 千種テンカ (UCEBA1RFfkXQtqgiDVLh4bcw) — đo bằng máy 2026-09-24

Cách đo: tiếng 4 video gốc (`_raw\audio\*.webm`) cắt theo mốc phụ đề → "vân giọng" Resemblyzer → so với mẫu
từng giọng VOICEVOX sinh bằng engine local (`E:\CLAUDE\YOUTUBE\VOICEVOX_ENGINE\gan_giong_kenh_mau.py`).
Ứng viên mỗi video = đúng danh sách giọng kênh ghi ở mục ▼素材 (tư liệu) trong mô tả. Kết quả chi tiết từng câu:
`_raw\audio\giong_<video_id>.json`. Vai được suy ra bằng cách ĐỌC các câu mà máy gán cho giọng đó.

## 1. Ba giọng CỐ ĐỊNH — có ở cả 4/4 video, cùng vai
| Giọng VOICEVOX | Vai | Bằng chứng (câu máy gán) |
|---|---|---|
| **玄野武宏** (Kurono Takehiro, nam trầm) | **NGƯỜI KỂ** ngôi 3 | 134–145 đoạn/video, toàn câu kể 「彼は…」 (anh ta…) |
| **黒沢冴白** (Kurosawa Kohaku, nam) | **NHÂN VẬT CHÍNH** — cả câu thoại LẪN độc thoại nội tâm 「俺…」 (tôi…) | 「そこまで言うならじゃあやめます」 (nói vậy thì tôi nghỉ) · 「面倒な仕事は全部俺に回ってくる」 (việc phiền toái dồn hết cho tôi) |
| **波音リツ** (Namine Ritsu, nữ) | **事務さん** (nhân viên hành chính) | 「お取り寄せの分は明日の午前中に届きます」 (thuốc đặt sẽ tới sáng mai) · 「これは私が書く書類ではないと…」 (giấy này đâu phải tôi viết) |

⚠️ Độc thoại nội tâm 「俺…」 KHÔNG do người kể đọc mà do giọng nhân vật chính → kịch bản phải gắn vai cho cả câu nội tâm.

## 2. Vai PHỤ — đổi theo tập, lấy từ kho giọng
| Video | Vai → giọng |
|---|---|
| 「じゃあ、辞めます」 (vậy tôi nghỉ) | パートさん (dược sĩ bán thời gian) + người phỏng vấn nhà thuốc mới → **四国めたん** · 店長 (quản lý): chưa xác định — nhiều khả năng **阿井田茂 (AivisSpeech)**, chưa cài nên chưa đo |
| 「自分、仕事できるんで」 (tôi làm việc giỏi mà) | người phỏng vấn chính → **四国めたん** · 後輩 (đàn em nam) → **白上虎太郎** · 先輩 (đàn chị) → **冥鳴ひまり** · phỏng vấn công ty 2 (ông lớn tuổi) → **麒ヶ島宗麟** · phỏng vấn công ty 3 (nữ 30 tuổi) → **九州そら** · 店長 chỗ mới → **夜語トバリ** · nhân viên mới cuối truyện → **春日部つむぎ** · 店長 cũ: có thể **阿井田茂** |
| 「残業代入んないんで」 (không có tiền tăng ca) | 店長 → **雀松朱司** · エリアマネージャー (quản lý khu vực, người đọc hợp đồng) → **東北イタコ** · 新人 (nhân viên mới nữ) → **春日部つむぎ** · パート/đàn chị → **冥鳴ひまり** · cụ ông bệnh nhân → **ちび式じい** |
| 「代わりはいくらでもいる」 (thiếu gì người thay) | người phỏng vấn (từng là người giao hàng) → **離途** · vai phụ nhỏ: 春日部つむぎ / 冥鳴ひまり / 雀松朱司 |

## 3. Quy tắc phân vai rút ra (dùng khi viết `cast.json` cho từng tập)
- 3 giọng cố định ở mục 1: không đổi xuyên kênh.
- Mỗi vai có thoại = 1 giọng; vai phụ chọn theo giới/tuổi: 店長 nam → 雀松朱司 (hoặc 阿井田茂) · người phỏng vấn/người đưa hậu quả → 四国めたん / 離途 / 東北イタコ · đồng nghiệp nữ trẻ → 春日部つむぎ · đàn chị/パート → 冥鳴ひまり · đàn em nam → 白上虎太郎 · người lớn tuổi → ちび式じい / 麒ヶ島宗麟.
- Một giọng phụ được dùng lại cho vai nhỏ khác nếu 2 vai không xuất hiện cùng cảnh (V1: 四国めたん đọc cả パート lẫn người phỏng vấn).
- Số giọng/tập = người kể + số vai có thoại (đo thật: 5–11).

## 4. Điều khoản — đã đọc từ engine
Cả 14 giọng: 「VOICEVOX:<tên>とクレジットを記載すれば、商用・非商用で利用可能」 (ghi tên "VOICEVOX:<tên>" là được dùng thương mại
và phi thương mại). → mô tả video PHẢI có khối ▼素材 liệt kê đúng các giọng đã dùng trong tập, như kênh mẫu.

## 5. Độ tin cậy / còn thiếu
- Phụ đề tự động đôi khi gộp lời kể + lời thoại trong 1 đoạn → vài câu bị gán lẫn; vai CHÍNH (mục 1) rất chắc
  (hàng chục–trăm đoạn, đúng ngữ nghĩa), vai phụ 1–8 đoạn nên chỉ đủ để nhận dạng vai, không dùng làm số đo.
- Chưa đo: **阿井田茂 (AivisSpeech)** — cần cài AivisSpeech Engine (miễn phí) để xác nhận có phải giọng 店長 ở video 1–2.
