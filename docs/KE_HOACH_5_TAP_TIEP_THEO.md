# Kế hoạch 5 tập tiếp theo — lane satori-jp-obaa (2026-09-17)

Đã chọn 5 video **cao view nhất trong nhóm CHƯA dùng** của kênh nguồn simbot2
(`https://www.youtube.com/@simbot2`), theo đúng tiêu chí B1 trong `docs/SOP_SATORI_JP.md`
("cao view + gần đây ≤1-2 tháng"). Đối chiếu với TOÀN BỘ 24 video hiện có trên kênh (quét bằng
`yt-dlp --flat-playlist`) và 10 video đã dùng (STT1,2,3,4,5,6,7,11,19,21) để đảm bảo không trùng.

5 video còn lại có view cao hơn (66k-69k, đăng gần đây hơn nhưng hiệu suất thấp hơn hẳn) đã bị loại
vì view quá thấp so với nhóm chọn — xem bảng đối chiếu đầy đủ ở mục cuối file.

## 5 video đã chọn + gán STT

| STT | Slug dự kiến | Video nguồn | View | Đăng | Số ngày trước (từ 17/09) |
|---|---|---|---|---|---|
| 8  | `simbot2-08-Kb5Ej4ZNBgQ`  | https://www.youtube.com/watch?v=Kb5Ej4ZNBgQ  | 318.739 | 2026-08-01 | 47 |
| 9  | `simbot2-09-rNGGuRG-wu0`  | https://www.youtube.com/watch?v=rNGGuRG-wu0  | 240.624 | 2026-07-19 | 60 |
| 10 | `simbot2-10-66weQbaUZuk`  | https://www.youtube.com/watch?v=66weQbaUZuk  | 206.708 | 2026-08-04 | 44 |
| 12 | `simbot2-12-FBkmqYvEyXQ`  | https://www.youtube.com/watch?v=FBkmqYvEyXQ  | 190.022 | 2026-07-22 | 57 |
| 13 | `simbot2-13-djMUfpGoUQI`  | https://www.youtube.com/watch?v=djMUfpGoUQI  | 154.146 | 2026-07-26 | 53 |

(STT11 đã có sẵn dữ liệu — bỏ qua khi gán số; dùng STT8/9/10/12/13, đúng các ô trống liền kề trong
trang tính.)

## Nội dung gốc (Hàn) + tựa đề Nhật đã soạn sẵn cho cột ĐỂ TÀI

**STT8 — Kb5Ej4ZNBgQ**
- Gốc: 【전직 은행원의 경고】70세가 넘어서도 여기에 돈을 넣어 두고 있다면 당장 멈추세요｜은행은 절대 알려주지 않습니다
- (Cảnh báo của cựu nhân viên ngân hàng: nếu qua 70 tuổi vẫn để tiền ở đây thì dừng ngay — ngân hàng
  không bao giờ nói cho bạn biết)
- Tựa Nhật: 元銀行員の警告——七十歳を過ぎてこの場所にお金を置いているなら、今すぐやめてください

**STT9 — rNGGuRG-wu0**
- Gốc: 나이 들어 돈이 있다면 가장 먼저 사야 할 3가지… 늦으면 반드시 후회합니다
- (Nếu có tiền lúc về già, 3 thứ nên mua đầu tiên... trễ là chắc chắn hối hận)
- Tựa Nhật: 老後にお金があるなら真っ先に買うべき三つのもの——遅れれば必ず後悔します

**STT10 — 66weQbaUZuk**
- Gốc: 죽기 한 달 전부터 몸에 나타나는 변화｜간호사가 알려줬습니다
- (Những thay đổi cơ thể xuất hiện từ 1 tháng trước khi mất | y tá đã nói cho biết)
- Tựa Nhật: 死の一か月前から体に現れる変化——看護師が教えてくれたこと

**STT12 — FBkmqYvEyXQ**
- Gốc: 70세를 막 넘겼는데 몇 년 안 돼 세상을 떠나는 노인이 많습니다… 대체 왜일까요?
- (Vừa qua 70 tuổi mà nhiều người già mất trong vài năm... vì sao vậy?)
- Tựa Nhật: 七十歳を超えて数年で旅立つ人が多いのは、いったいなぜなのか

**STT13 — djMUfpGoUQI**
- Gốc: 65세에 '이만큼의 돈'이 있는 사람은… 노후의 승자입니다｜이 기준, 놀랄 만큼 정확합니다
- (Người có "từng này tiền" ở tuổi 65... là người thắng cuộc tuổi già | tiêu chuẩn này chính xác
  đến bất ngờ)
- Tựa Nhật: 六十五歳でこれだけのお金がある人は老後の勝者——驚くほど正確な基準

## Đã ghi vào trang tính

Tab `Lopezzapa68`, cột A (STT) + B (ĐỂ TÀI, tựa Nhật ở trên) + E (FOLDER, đường dẫn dự kiến) + H
(GHI CHÚ: nguồn, view, ngày đăng, link, trạng thái "Đã CHỌN, CHƯA làm bước 1"). Cột F/G để trống —
CHƯA có ảnh/video, chưa bắt đầu sản xuất.

## Lệnh triển khai khi có lệnh "làm tập N"

Theo đúng `docs/SOP_SATORI_JP.md` B1-B5 (dùng pipeline "não Claude" — `brain_channel.py` —
như đã dùng cho tập 5), dừng trước bước render (`stop_before_render=True`), sau đó chạy hybrid
stock+AI (`phan_loai_stock.py` → `stock_fetch.py` → `audit_stock.py`, dùng bản trong
`scratch_analysis/stock_hybrid_simbot2-05-Hhe56wqubbU/` làm mẫu, đổi model sang `gemini-3.8-flash`
nếu `deepseek-v4-flash` vẫn lỗi 403), rồi TTS + pace + anchors + thumbnail — đúng quy trình đã áp
dụng cho tập 5. Sau khi xong bước 1 cho từng tập: DỪNG, KHÔNG tự `upload-job` sang máy 2 nếu chưa có
xác nhận thêm (đúng hàng rào "chỉ làm bước 1" trong CLAUDE.md).

## Bảng đối chiếu toàn bộ 14 video CHƯA dùng còn lại của kênh (để tham khảo khi cần thêm tập sau STT13)

| Video ID | View | Ngày đăng | Ghi chú |
|---|---|---|---|
| Kb5Ej4ZNBgQ | 318.739 | 2026-08-01 | ✅ đã chọn STT8 |
| rNGGuRG-wu0 | 240.624 | 2026-07-19 | ✅ đã chọn STT9 |
| 66weQbaUZuk | 206.708 | 2026-08-04 | ✅ đã chọn STT10 |
| FBkmqYvEyXQ | 190.022 | 2026-07-22 | ✅ đã chọn STT12 |
| djMUfpGoUQI | 154.146 | 2026-07-26 | ✅ đã chọn STT13 |
| PeI50JbaoNI | 68.696 | 2026-09-12 | view thấp hơn hẳn nhóm trên, mới đăng nên chưa rõ sức hút thật |
| -Gt6QYEFS38 | 66.209 | 2026-09-06 | tương tự |
| XOnRgF-qJxU | 36.403 | 2026-08-19 | view thấp |
| EEgZ6iFWwnQ | 25.691 | 2026-09-15 | quá mới (2 ngày), chưa đủ dữ liệu view |
| 318aUixOmRM | 19.964 | 2026-07-29 | view thấp |
| 3skfbgjTM7M | 13.085 | 2026-08-13 | view thấp |
| 1ex2yTPAsGA | 13.205 | 2026-07-12 | view thấp + hơi cũ (67 ngày) |
| KrerPxaFZdE | 8.961  | 2026-09-09 | view rất thấp |
| qM2bYD3Cy9o | 4.242  | 2026-07-04 | view thấp nhất + cũ nhất (75 ngày) |

Nguồn số liệu: `yt-dlp --flat-playlist` quét kênh + `yt-dlp` đọc riêng từng video lấy `upload_date`
thật (flat-playlist không trả upload_date), chạy trực tiếp 2026-09-17.
