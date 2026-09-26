# LƯỚI ĐỠ KHI GEMINI-3.8-FLASH (ramclouds) HỎNG

Chốt 2026-09-26. Áp dụng MỌI LANE và CẢ HAI MÁY, không phải khai gì trong profile: lưới nằm trong
công cụ.

Máy 1 viết kịch bản nên được dùng 9router. Máy 2 chỉ vẽ ảnh và dựng video, ở đó **không có
9router** — nên phần QC chạy tại máy 2 phải có lưới bằng model gọi được từ xa. Đó là lý do tồn tại
của tài liệu này.

## 1. Gemini đang làm những việc gì

Hai lõi, mọi bước đều đi qua một trong hai.

| Lõi | File | Ai dùng |
|---|---|---|
| Văn bản | `pipeline/llm_client.py::chat()` | mọi bước viết, chấm, tóm tắt |
| Nhìn ảnh | `pipeline/qc_character.py::_chat()` | mọi bước soi ảnh và clip |

| Bước | File | Gemini làm gì | Chạy ở máy |
|---|---|---|---|
| B3 | `ai_steps.py`, `lean_script.py` | viết bản nháp, nén theo khúc, đặt tiêu đề/mô tả | 1 |
| B3Q | `qc_script.py` | chấm mâu thuẫn nội dung, 伏線 (phục bút, manh mối gieo ra không trả) | 1 |
| B3F | `qc_facts.py` | đối chiếu chi tiết kịch bản với tư liệu | 1 |
| B4V | `detect_voice.py` | đọc transcript suy ra giới/tuổi người kể để chọn giọng | 1 |
| B5K | `khop_hinh.py` | nối từng đoạn lời khoảng 15 giây với một từ khoá hình | 1 |
| B5P | `phan_loai_stock.py` | phân mỗi dòng prompt là ảnh AI hay clip stock | 1 |
| B5 | `stock_fetch.py` | chọn clip khớp nhất trong ứng viên Pexels | 1 |
| B5A | `soi_kho.py`, `tim_anh_that.py` | **nhìn ảnh**: clip có đúng thứ từ khoá đã hứa | 1 |
| B5A | `audit_stock.py` | **nhìn ảnh**: loại clip lộ mặt người lạ hoặc chữ to | 1 |
| B5RQ/B5Q | `qc_character.py`, `qc_visual.py` | **nhìn ảnh**: master và cả loạt ảnh đúng tuổi/giới/trang phục | **2** |
| B7.5 | `sinh_img_doan.py` | gán mỗi ảnh vào đoạn lời thứ mấy | 1 |
| B8Q | `qc_canh.py`, `qc_visual.py` | **nhìn ảnh**: hình đang hiện có ăn với lời đang đọc | **2** |
| B11 | `giao_hang.py`, `ban_xem_viet.py` | dịch và tóm tắt cho giao hàng, bản xem thử tiếng Việt | 1 |
| K2 | `channel_analyzer.py` | phân tích video kênh mẫu, tổng hợp CHANNEL_DNA | 1 |

## 2. Đo 15 model rẻ ở 3 proxy, trên CÙNG hai tấm ảnh thật

Mốc so sánh là chính `gemini-3.8-flash`: ảnh 1 đọc ra **52/M**, ảnh 2 **70/F**.
Cột thời gian: việc JSON / viết tiếng Nhật / nhìn hai ảnh.

| provider:model | JSON | Nhật | Nhìn ảnh 1 / ảnh 2 | giây |
|---|---|---|---|---|
| ramclouds:gemini-3.8-flash (mốc) | đạt | đạt | 52/M · 70/F | 13/14/47 |
| ramclouds:gemini-3.1-flash-lite | đạt | đạt | 55/M · 75/F | 24/9/51 |
| ramclouds:glm-5.3-flash | rỗng | rỗng | 55/M · 75/F | 2/9/41 |
| ramclouds:qwen3.8-flash | đạt | đạt | **hỏng · 30/M** | 2/6/29 |
| ramclouds:grok-4.5 và grok-4.6 | lỗi | lỗi | 503 · 503 | 249/0/2 |
| ramclouds:deepseek-v4.1-flash | đạt | đạt | **rỗng · rỗng** | 2/4/9 |
| ns24:deepseek-v4.1-flash | đạt | đạt | 55/M · 75/F | **0/0/7** |
| ns24:glm-5.3-flash | rỗng | rỗng | 54/M · 75/F | 3/4/18 |
| ns24:qwen3.8-max | đạt | đạt | 60/M · 75/F | 4/10/14 |
| ns24:kimi-k3 | rỗng | rỗng | 50/M · 78/F | 4/9/23 |
| hhtech:glm-5.3-flash | đạt | đạt | 55/M · 75/F | 3/7/38 |
| hhtech:grok-4.6 | đạt | đạt | 55/M · 78/F | 3/10/24 |
| hhtech:kimi-k3 | đạt | đạt | 58/M · 80/F | 4/4/24 |

Ba điều rút ra, đều phải trả giá mới biết:

1. **Cùng tên model, khác nhà, khác hẳn khả năng.** `deepseek-v4.1-flash` ở ns24 nhìn ảnh rất tốt
   và nhanh nhất bảng; đúng model đó ở ramclouds trả rỗng khi có ảnh. Đừng suy từ nhà này sang nhà
   kia.
2. **Ô "rỗng" của glm và kimi KHÔNG phải model dở.** Đó là model có suy nghĩ trước, và phần suy
   nghĩ ăn vào chính hạn `max_tokens`. Cho hạn nhỏ thì nội dung trả về rỗng trong khi HTTP vẫn 200,
   trông y hệt "model không làm được". Đã kiểm lại thủ công: cùng câu hỏi, nâng hạn lên 200 token
   là `glm-5.3-flash` trả đúng `{"ok":true}`. Vì vậy mọi bậc dự phòng đều dùng hạn rộng 700 token.
3. **`qwen3.8-flash` đọc ảnh sai tới 40 tuổi.** Loại, vì cổng QC sẽ đánh trượt oan ảnh đúng.

Chỉ ramclouds công bố giá máy đọc được (`/api/pricing`). Theo đó `gemini-3.8-flash` hệ số 0,375
còn `gemini-3.1-flash-lite` 0,125 và `glm-5.3-flash` 0,3. ns24 và hhtech không có endpoint giá.

## 3. Đã lắp gì

**Nhìn ảnh** (`qc_character._chat`, lõi dùng chung của mọi bước soi ảnh, gồm cả bước chạy ở máy 2):

| Bậc | Đường | Vì sao |
|---|---|---|
| 1 | ramclouds gemini-3.8-flash | giữ nguyên, không đổi gì khi nó sống |
| 2 | ns24 deepseek-v4.1-flash | khớp mốc, nhanh nhất, đổi hẳn nhà |
| 3 | hhtech glm-5.3-flash | khớp mốc, nhà thứ ba |
| 4 | gpt-5.6-sol qua `sol_client` | lời cuối, đắt và chậm hơn nên xếp sau |

**Văn bản** (`llm_client.CHAINS`): hai việc `short` và `analysis` thêm bậc rẻ
`ns24:deepseek-v4.1-flash`, rồi mới tới gpt-5.6-sol. Việc `script` **không** nhận deepseek vào
chuỗi: phép thử chỉ chứng minh nó viết nổi hai câu tiếng Nhật, không chứng minh nổi bài kể mười
nghìn chữ. Viết vẫn là gemini rồi tới sol.

**9router**: vẫn là đường đầu của `sol_client` ở **cả hai máy** — máy 2 dùng 9router từ trước tới
nay. Bản sáng 26/09 từng thêm phép tự dò cổng 20128 để "máy 2 khỏi chờ", dựa trên giả định sai là
máy 2 không có 9router; đã gỡ. Muốn bỏ thì đặt tay `SOL_DUNG_9ROUTER=0`, không để máy đoán hộ.

**Đã gỡ hẳn `ramclouds:gpt-5.6-luna`** khỏi cả ba chuỗi: model này không còn trong danh mục của
ramclouds nữa (`/v1/models` còn 18 tên, không có nó) nên luôn trả 503. Giữ lại chỉ tốn hai lượt thử
và mười giây chờ mỗi lần gemini hỏng, đúng lúc đang cần rơi xuống lưới cho nhanh.

Ngoài ra `phan_loai_stock.py` và `stock_fetch.py` trước đây ghim cứng `provider="ramclouds"` nên
chuỗi chỉ còn một mắt xích. Đã đổi sang `task="short"`, vẫn gemini đi đầu nhưng có người đỡ phía sau.

## 4. Nghiệm thu, bằng cách giả lập từng tầng chết

| Phép thử | Kết quả |
|---|---|
| Nhìn ảnh, mọi thứ bình thường | 52/M và 72/F |
| Nhìn ảnh, ramclouds chết | 58/M và 75/F, **7 giây cho hai ảnh** |
| Nhìn ảnh, chỉ còn sol | 52/M, 14 giây |
| `qc_visual._vision` khi ramclouds chết | 60/M, 4 giây |
| Chuỗi chữ, chỉ còn bậc rẻ | `ns24:deepseek-v4.1-flash` trả JSON đúng, 1 giây |
| Cổng QC dùng chung khi mọi gemini chết | trả JSON đúng |
| Chuỗi `script` khi mọi gemini chết | rơi thẳng xuống gpt-5.6-sol, trả đúng |
| `sol_client.py` ở máy 1 | cả ba đường đều sống |
| `sol_client.py` giả lập máy 2 | bỏ qua 9router, hai đường còn lại sống |

Chênh lệch tuổi giữa các bậc nằm trong khoảng cho phép sẵn có của cổng (lệch quá 12 tuổi mới bị
gắn cờ), nên lưới bật lên không làm cổng đổi kết luận.

## 5. Một điều cần nói thẳng về số liệu sức khoẻ proxy

Trong cùng buổi đo, 9router có lúc trả 401 và hhtechapi có lúc trả 503/502/521, sau đó **cả hai tự
hồi phục** và tới cuối buổi cả ba đường sol đều sống. Nghĩa là các con số hỏng ở trên là ảnh chụp
một thời điểm, không phải kết luận lâu dài. Kiểm lại bất cứ lúc nào:

```
py -3.13 E:\CLAUDE\YOUTUBE\h2dev\pipeline\sol_client.py
py -3.13 E:\CLAUDE\YOUTUBE\h2dev\pipeline\llm_client.py --ping
```

## 6. Về `gpt-6-sol`

Đã thử, chưa dùng được: 9router không có model này, ns24 và hhtech đều trả 502 quá tải. Khi nào một
đường sống thì đổi `SOL_TAIL` trong `pipeline/llm_client.py` và các hằng `*_MODEL` trong
`pipeline/sol_client.py`.


## 7. `gpt-5.6-sol` CHẤM ẢNH KHÔNG ỔN ĐỊNH — và đó KHÔNG phải lỗi của đường ns24

Máy 2 báo cổng QC ảnh chê oan bốn vòng liên tiếp, mỗi vòng một lý do khác, trên ảnh sạch; nghi là
"phải chạy dự phòng ns24 nên model kém đi". Đã đo lại bằng **đúng câu hỏi QC thật**, trên **đúng hai
tấm ảnh đó** (`assets\shakai_no_naze\ep01-shusse-shitakunai\img.png` và `018.png`, cả hai đã
soi mắt thường: một cảnh liền, không chữ, không méo), **5 lượt mỗi ô**. Ô "sạch" nghĩa là chấm đúng.

| đường:model | ảnh 001 | ảnh 018 | lời chê oan |
|---|---|---|---|
| ns24 : gpt-5.6-sol | 4/5 | 5/5 | "méo mó" ×1 |
| 9router : cx/gpt-5.6-sol | **2/5** | 5/5 | "méo mó" ×3 |
| ramclouds : gemini-3.8-flash | 5/5 | 5/5 | không |
| ns24 : deepseek-v4.1-flash | 5/5 | 5/5 | không |
| hhtech : glm-5.3-flash | 5/5 | 5/5 | không |

Kết luận đi ngược với giả thiết ban đầu: **lỗi nằm ở model `gpt-5.6-sol`, không nằm ở đường ns24** —
cùng model đó chạy qua 9router còn sai NHIỀU GẤP BA. Bật lại 9router không chữa được việc chê oan.

Ba model còn lại chấm đúng 10/10, nên thang dự phòng ở §3 (ns24 deepseek → hhtech glm → sol) đặt sol
xuống cuối là đúng chỗ: chỉ chạm tới nó khi không còn gì khác.

**Còn một hiểu nhầm nữa cần đính chính:** không có chuyện "cổng QC bốc bừa ảnh khác để chê mỗi
lần". Danh sách ảnh mẫu là CỐ ĐỊNH, tính bằng công thức chia đều, không hề ngẫu nhiên — với 155 ảnh
và `qc_sample: 10` thì luôn là ảnh 1, 18, 35, 52, 69, 87, 104, 121, 138, 155. Đúng hai tấm máy 2
kiểm tay là hai tấm đầu danh sách. Thứ đổi mỗi vòng là phán quyết của model, không phải danh sách.

**Đã vá** (`qc_visual.qc_images`): một tấm bị chê thì **hỏi lại bằng model khác**, chỉ giữ lý do mà
cả hai cùng thấy; một model kêu mà model kia bảo sạch thì coi như sạch và ghi vào
`bo_qua_vi_khong_dong_y` để còn lần ra. Thà bỏ sót một ảnh xấu còn hơn đẩy cả loạt vào vòng vẽ lại
không có điểm dừng.
