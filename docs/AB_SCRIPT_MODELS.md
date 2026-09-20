# A/B THẬT: MODEL NÀO VIẾT ĐƯỢC KỊCH BẢN SATORI JP THAY CLAUDE

Ngày đo **2026-09-07**. Điều kiện giống nhau tuyệt đối cho mọi bài thi:

- **Nguồn**: `assets/satori_jp/ep3-sougi/competitor.txt` (transcript Hàn, 15.110 chữ) — chính video đã lên.
- **System prompt**: nguyên văn `skills/youtube-script/SKILL.md` (12KB).
- **User prompt**: khối kích hoạt thật (LENGTH 30 phút · ngôi 1 cụ bà · 6 yêu cầu bắt buộc: chỉ xuất bản
  cuối, 9.000–9.500 chữ, Nhật hoá 100%, cấu trúc mở–伏線–cao trào–悟り–3 kết–hỏi khán giả, giữ nhân phẩm).
- **Mốc so sánh**: `assets/satori_jp/ep3-sougi/script.txt` — bản **Claude** viết, 9.245 chữ (29,9 phút), đã lên video.
- Output tất cả nằm ở `assets/_ab_script/`.

## 1. BẢNG KẾT QUẢ (1 call, skill ở system)

| Bài thi | Giây | Chữ | ~Phút | Nhật hoá (kw/9) | Marker rác | Kết luận |
|---|---|---|---|---|---|---|
| **ramclouds : gemini-3.8-flash** | 91 | 16.306 | 52,8 | **8/9** | sạch | ⭐ văn hay nhất, nhưng dài gấp 1,76 lần |
| ns24 : gemini-3.8-flash | 73 | 16.084 | 52,1 | 3/9 | sạch | văn ổn, Nhật hoá nhạt hơn ramclouds |
| ramclouds : gpt-5.6-luna | 165 | 11.052 | 35,8 | 6/9 | sạch | ổn định nhất về độ dài (2 lần: 11.052 / 10.930) |
| ns24 : gpt-5.6-sol | 293 | 7.495 | 24,3 | 6/9 | sạch | ❌ **bị cắt giữa câu**, `finish_reason=None`, `out_tok=0` |
| ramclouds : MiniMax-M3 | 77 | 6.091 | 19,7 | 2/9 | ❌ `**`, `SCRIPT COMPLETED`, `脚本完成` | quá ngắn + lọt marker nội bộ |
| ramclouds : gpt-5.6-sol | 6 | 75 | — | — | — | ❌ hỏi lại bằng **tiếng Việt** (3/3 lần) |
| ns24 : gpt-5.6-terra | 44 | 132 | — | — | — | ❌ `[Codex error: servers overloaded]` |
| ns24 : gpt-5.6-luna | 25 | 132 | — | — | — | ❌ cùng lỗi Codex |

## 2. ĐO ĐỘ KHỚP GIỌNG ĐỌC (chỗ khác biệt thật giữa Claude và model)

| Bản | Chữ | Phút | Chữ/câu | **Phẩy/câu** | Hội thoại 「」 |
|---|---|---|---|---|---|
| **CLAUDE (baseline đã lên video)** | 9.245 | 29,9 | 24,4 | **3,34** | **0%** |
| gemini-3.8-flash (1 call) | 16.306 | 52,8 | 37,6 | 1,59 | 28% |
| gpt-5.6-luna | 11.052 | 35,8 | 25,1 | 1,18 | 11% |
| MiniMax-M3 | 6.091 | 19,7 | 26,0 | 1,24 | 18% |

3 thứ Claude tự làm mà **skill chưa ghi thành luật** nên model không làm:

1. **Băm dấu phẩy theo nhịp thở** (3+ phẩy/câu) — cho giọng cụ bà đọc chậm, hụt hơi.
2. **Hội thoại ≤10%**, thuần lời kể (bản Claude 0%).
3. **Câu hé tập sau** để nối series (bản Claude: 「次は、旅立ちが、近づいた人の…」).

## 3. KHOÁ ĐỘ DÀI: 2 CÁCH ĐÃ THỬ

### ❌ Cách 1 — chia 3 khúc, mỗi khúc ra chỉ tiêu 3.100–3.500 chữ

Kết quả: 5.997 / 7.763 / 6.840 = **20.600 chữ (66,7 phút)**. → **gemini KHÔNG đếm chữ**, mọi chỉ tiêu số
lượng bằng lời đều bị bỏ qua. Đừng tin `文字数` trong prompt.

### ✅ Cách 2 — PASS 2 nén lại + ép nhịp (ĐÃ ĂN)

Đưa bản 16.306 chữ vào, yêu cầu nén còn 9.000–9.500 + 3 luật ở §2. Kết quả sau **45,5 giây**:

| Chỉ số | Trước nén | **Sau nén** | Mốc Claude |
|---|---|---|---|
| Chữ | 16.306 | **10.423 (33,7 phút)** | 9.245 (29,9) |
| Phẩy/câu | 1,59 | **4,63** | 3,34 |
| Hội thoại | 28% | **0%** | 0% |
| Marker rác | sạch | sạch | sạch |
| Hé tập sau | không | **có** | có |

Trích bản sau nén: 「昨年の、暮れ近い、北風の吹く、寒い日の、ことで、ございます」 — **đúng nhịp băm phẩy của bản
Claude**; kết thúc: 「…コメント欄で、お聞かせ願えませんでしょうか。次回は、遺品整理で見つかった、一通の破かれた
手紙が繋ぐ、母と娘の和解の物語をお届けいたします」.

→ Vẫn dư ~10% so với 30 phút (EP3 thật 30 phút, EP4 thật 34 phút nên 33,7 là **chấp nhận được**); gate cho
phép nén thêm 1 lượt nếu muốn sát 30.

## 4. CHỐT KIẾN TRÚC BƯỚC B3 CHO TOOL

```
PASS 1  gemini-3.8-flash (ramclouds)  ~91s  → bản giàu chi tiết, dài 16k chữ
PASS 2  gemini-3.8-flash (ramclouds)  ~46s  → nén về 9.000-9.500 + băm phẩy + hội thoại ≤10% + hé tập sau
GATE    đếm chữ ÷309 · quét marker · quét hangul/latin · phẩy/câu ≥3 · phải kết thúc bằng 。
FALLBACK  gpt-5.6-luna (ramclouds)          → khi gemini lỗi; độ dài ổn định nhất, cần PASS 2 nhẹ hơn
```
Tổng ~137 giây, ~$0.05/kịch bản. **KHÔNG dùng**: `ramclouds:gpt-5.6-sol` (hỏi lại tiếng Việt),
`ns24:gpt-5.6-*` (lỗi Codex overload trả về dưới dạng nội dung), `MiniMax-M3` (ngắn + lọt marker).

## 5. VIỆC PHẢI SỬA TRONG `skills/youtube-script/SKILL.md`

Thêm 3 luật §2 vào mục VOICEOVER-READY (Claude cũng nên theo cho nhất quán) + ghi rõ "nếu dài quá thì
chạy PASS 2 nén" thay vì tin vào chỉ tiêu số chữ.

## 6. BẪY MỚI PHÁT HIỆN (bổ sung cho `docs/REPORT_RAMCLOUDS_HERMES.md`)

1. **Lỗi upstream trả về dưới dạng NỘI DUNG**: `[Codex error: Our servers are currently overloaded]` với
   HTTP 200 + `finish_reason=stop`. Tool phải quét chuỗi `[Codex error`, `overloaded`, và độ dài tối thiểu.
2. **Stream kết thúc không có `finish_reason`** (`ns24:gpt-5.6-sol`): văn bị cắt giữa câu mà không có dấu
   hiệu lỗi. → Bắt buộc kiểm ký tự cuối phải là 。！？」.
3. **Lane Codex bỏ qua system prompt tiếng Việt**: `ramclouds:gpt-5.6-sol` hỏi lại bằng tiếng Việt 3/3 lần,
   kể cả khi nhồi skill vào user message + chỉ thị tiếng Anh. Nhưng `ramclouds:gpt-5.6-luna` **lại chạy tốt**
   với cùng cách gọi → hành vi khác nhau theo từng model trong cùng lane, phải test từng con, không suy luận.
4. **Cùng 1 tên model, 2 provider ra chất khác nhau**: `gemini-3.8-flash` ramclouds Nhật hoá 8/9 từ khoá,
   ns24 chỉ 3/9 (cùng prompt, cùng nhiệt độ) → ramclouds tốt hơn cho việc này.
5. **ns24 nghẽn khi gọi song song**: 10 request cùng lúc → chỉ 1 con trả kết quả sau 15 phút. Chạy tuần tự
   hoặc ≤2 luồng với provider này.
