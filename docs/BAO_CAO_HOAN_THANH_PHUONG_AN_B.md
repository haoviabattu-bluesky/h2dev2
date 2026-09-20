# BÁO CÁO HOÀN THÀNH — Phương án B (neo ảnh tập 11)

Ngày làm: 13/09/2026 · Model: deepseek-v4-flash (Hermes) · Thời gian: ~2 giờ

## 1. VIỆC 1 — sửa sinh_neo.py

**Lỗi cũ:** chọn neo bằng "cue SỚM NHẤT còn cách neo trước ≥1 giây" → mọi ảnh trong cùng đoạn dồn hết về ĐẦU đoạn, để trống phần sau (đo thật bản cũ trên đĩa: 23 ảnh <3s, 1 ảnh <1s, MAX 282,3s).

**Trước (dòng ~147, comment `CHON NEO TUAN TU TOAN CUC`):**
```python
chon, cue_truoc = {}, -10.0
for p in anh:
    i, j = dai[m[p.name] - 1]
    k = next((t for t in range(i, j + 1) if cues[t][0] - cue_truoc >= TOI_THIEU_GIAY), None)
    ...
    chon[p.name] = k
    cue_truoc = cues[k][0]
```

**Sau (trải đều theo thời gian trong dải cue của đoạn):**
```python
chon, cue_truoc = {}, -10.0
da_dat = collections.Counter()
for p in anh:
    so_doan = m[p.name]
    i, j = dai[so_doan - 1]
    n_trong_doan = len(nhom[so_doan])
    k_thu = da_dat[so_doan]                 # anh nay la anh thu may (0-based) trong doan
    da_dat[so_doan] += 1
    t0 = cues[i][0]
    t1 = cues[j + 1][0] if j + 1 < len(cues) else cues[-1][0] + 1.0
    muc = t0 + (t1 - t0) * k_thu / n_trong_doan       # moc thoi gian mong muon, trai deu
    ung = [t for t in range(i, j + 1) if cues[t][0] - cue_truoc >= TOI_THIEU_GIAY]
    if not ung:
        loi.append(...); break
    k = min(ung, key=lambda t: abs(cues[t][0] - muc))  # cue GAN MOC NHAT trong so con hop le
    chon[p.name] = k
    cue_truoc = cues[k][0]
```
(thêm `import collections`; dùng lại `nhom` — dict đoạn→ảnh đã có sẵn trong file, không xây lại)

**Số đo (mô phỏng đúng `anchor_durations` — script tạm đọc `voice_paced.wav` qua ffprobe để lấy audio_len thật, không phải cues[-1]):**

| Chỉ số | Bản cũ trên đĩa | Bản mới (sau cả 2 việc) |
|---|---|---|
| ảnh <3s | 23 | **3** |
| ảnh <1s (lỗi cứng) | 1 | **0** |
| thời lượng dài nhất | 282,3s | **102,8s** |
| trung bình | 14,7s | 14,7s |

## 2. VIỆC 2 — thuật toán mới sinh_img_doan.py

**GIỮ NGUYÊN:** `doc_doan()`, `doc_prompt()`, `suc_chua()`, `can_bang()` (đã test 200 ca, không viết lại).

**Thay:** `hoi_mot_lo()` + toàn bộ vòng lặp gọi nó trong `main()`. Thêm 2 hàm mới `doan_trung_tam()` (trung tâm theo TỈ LỆ THỜI GIAN THẬT từ SRT, fallback độ dài đoạn nếu chưa có TTS) và `cua_so()`.

**Cách hỏi mới:** mỗi ảnh một câu MULTIPLE-CHOICE trong cửa sổ RIÊNG của nó (`K=4` → cửa sổ ~9 đoạn quanh trung tâm, viết đầy đủ đoạn 200 ký tự không cắt cụt) — thay cho cách cũ (hỏi cả lô + mục lục 52 đoạn cắt cụt 70 ký tự → model bão hoà dồn về cuối).

**Vòng lặp:** K bắt đầu 4, `can_bang()` làm lưới an toàn cuối; nếu `None` → nới K 4→6→9 (tối đa 3 lần), vẫn None → báo "kịch bản quá ngắn", exit 1.

**Kết quả chạy thật trên tập 11 (121 ảnh · 52 đoạn · 415 cue):**
- Lô 1-5: **121/121 ảnh LLM trả đủ** (30/30 × 4 + 1/1), K=4 không cần nới
- `bu thieu 0 dong` · `can bang doi 10 dong = 8,3%` (mục tiêu <15%) ✅
- Phủ 46/52 đoạn (6 đoạn không có ảnh — trong đó có đoạn 46, xem mục 3)

**Số lần K phải nới rộng: 0** (chạy 3 lần thử đều K=4 đủ xếp vừa).

⚠️ **2 lần chạy thử không đạt đã ghi nhận (bài học, không phải kết quả cuối):**
- Lần 1: regex chưa chấp nhận prefix "ANH " (LLM lặp lại dòng đề bài `ANH 001.png|1`) → 0/30 mỗi lô, toàn bộ vá máy (can_bang 112 dòng). Đã sửa regex → `(?:ANH\s+)?`.
- Lần 2 (thử prompt nhấn mạnh "quyết định theo nội dung, đừng chọn giữa cho an toàn"): tệ hơn hẳn — can_bang 26 dòng (21%), đoạn 30 + 46 trống, đoạn 12 dồn 8 ảnh. **Đã REVERT về prompt hồ sơ gốc** (bản cuối dùng = khung 3.3, can_bang 8,3%).

## 3. Kiểm nội dung tay — đoạn 12, 30, 39, 46

**ĐOẠN 12** (bữa ăn trưa muộn sau tang lễ, bày 煮しめ/板わさ/徳利, con dâu thay nước hoa bàn thờ) — **SAI NỘI DUNG (2/2 ảnh lệch):**
- `027.png`: "elderly Japanese woman as her younger self in her late thirties standing at a Kamata market deli-shop counter smiling professionally at customers..." → thực chất thuộc ĐOẠN 11 ("私は平成が始まった頃から夫と一緒に、蒲田の小さな惣菜屋で…") — cùng cụm Kamata với 025/026 (được gán ĐÚNG đoạn 11), nhưng trung tâm thời gian của 027 (403s) rơi vào đoạn 12 (383–417s) nên LLM chọn 12.
- `028.png`: "a modern JA-Bank Nokyo local branch entrance..." → không khớp cảnh bữa ăn tang lễ (cảnh ngân hàng; bối cảnh lệch hẳn).

**ĐOẠN 30** (người khác kể chuyện con trai hút sạch tiền tiết kiệm, "nói tiền là đổi thay gia đình") — **TẠM CHẤP NHẬN, không rõ ràng sai:**
- `071.png`: flip-phone đọc thông báo ngân hàng (liên quan tài chính, bối cảnh gần)
- `072.png`: hành lang chung cư mùa đông (cảnh nền chuyển tiếp — chấp nhận được)

**ĐOẠN 39** (giữ bí mật số dư đến chết, để lại bản đồ vị trí sổ+ấn, nói chuyện tiền trên bàn ăn) — **KHỚP RÕ RÀNG ✅:**
- `089-093.png` (5 ảnh): notebook trên bàn ăn năm mới, kanji ghi tên ngân hàng + vị trí ngăn kéo, con trai khóc, con dâu hối hận → khớp chính xác nội dung đoạn.

**ĐOẠN 46** (28/12 rét đậm, chị mang dưa cải muối đến thăm, trò chuyện bên kotatsu) — **THIẾU ẢNH (0 ảnh):**
- Đã quét toàn bộ `img_prompts.txt` tìm "pickl/napa/tsukemon/cabbage/winter visit/bag of" → **KHÔNG có ảnh nào tả cảnh này**. 3 ảnh "đứng cửa vẫy tay" (018/073/114) đều là cảnh khác.
- **Nguyên nhân: lỗi NGUỒN từ bước 1 (bộ não không vẽ ảnh cho đoạn 46)** — không thuật toán gán nào tạo ra được ảnh không tồn tại. Cần bộ não vẽ thêm ~1-2 ảnh dưa cải/thăm nhà rồi chạy lại.

**Đánh giá tổng thể mục 4.5:** nội dung "sai rõ ràng" đếm được 1 đoạn (12) + 1 đoạn THIẾU nguồn (46, lỗi bước 1) — chưa đủ ngưỡng "≥2 đoạn sai rõ" để kết luận CHƯA ĐẠT cứng, nhưng **KHÔNG thể nói ĐẠT nội dung** (đoạn 12 sai, đoạn 46 không có ảnh minh hoạ cho cảnh quan trọng).

## 4. Kết quả chạy thật chay_buoc3.py --dong 11

**CHƯA CHẠY** — hồ sơ mục 5 yêu cầu "SAU KHI ĐẠT (số liệu + nội dung)". Số liệu đạt nhưng nội dung có 2 vấn đề (đoạn 12 sai, đoạn 46 thiếu nguồn) → em dừng trước bước gỡ khoá cột H + chạy thật, chờ người giao việc quyết (xem câu hỏi).

## 5. Rủi ro / việc chưa làm

- **Chưa chạy thật `chay_buoc3.py --dong 11`** (cần người giao việc chấp nhận nội dung trước — tốn ~30 phút render + gỡ khoá cột H).
- Chưa gỡ `TẠM DỪNG` ở cột H dòng 11 (giữ nguyên ghi chú giữ dòng — đúng quy ước V2).
- Đoạn 46 thiếu ảnh nguồn: cần bộ não (bước 1) vẽ ảnh "chị mang dưa cải đến thăm" rồi chạy lại `sinh_img_doan.py` + `sinh_neo.py`.
- `anchors.txt` mới đã sinh và nằm trên đĩa (121 neo hợp lệ, <1s = 0) — nếu người giao việc muốn dùng, đây là bản sẵn sàng; nếu muốn thêm ảnh đoạn 46 thì phải chạy lại cả chuỗi.
- File tạm `C:\Users\admin\AppData\Local\Temp\do_neo.py` (script đo, không commit).

## 6. Câu hỏi

1. **Đoạn 12 (ảnh 027/028 lệch):** chấp nhận (2 ảnh tuy lệch cảnh cụ thể nhưng vẫn trong mạch tài chính/quá khứ của câu chuyện) hay yêu cầu chỉnh tiếp (vd thêm hậu xử lý "ảnh liên tiếp cùng nội dung phải cùng đoạn")?
2. **Đoạn 46 thiếu ảnh nguồn:** nhờ bộ não vẽ thêm ảnh dưa cải/thăm nhà (đúng việc của bước 1) rồi em chạy lại toàn chuỗi, hay chấp nhận đoạn này không có ảnh riêng (ảnh trước sẽ giữ dài hơn ~ vài chục giây)?
3. Sau khi anh quyết 2 câu trên, em mới gỡ TẠM DỪNG + chạy thật `chay_buoc3.py --tab Lopezzapa68 --dong 11`.
