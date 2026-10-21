# BLOCK GIỚI THIỆU NHÂN VẬT trong HOOK (anh chốt 12/10/2026, mẫu Lane O ep10 — dùng được MỌI lane)

Anh nói **"block giới thiệu"** (hoặc "freeze giới thiệu", "đóng băng gõ chữ") = kiểu này, KHÁC thẻ tên động (`the_ten_hook.py`):

1. Cảnh nhân vật **LỘ MẶT LẦN ĐẦU** (clip Grok, ảnh: mặt bên PHẢI, nửa trái tường/nền trống). Các shot TRƯỚC đó KHÔNG lộ rõ mặt người này (chỉ gáy/tay/dáng) — viết vào prompt ảnh.
2. **ĐÓNG BĂNG** khung hình ngay trong video (chớp trắng 0,18s, ảnh bớt màu ~45%) — không dựng profile card riêng.
3. Dải tối bên trái, gõ theo cụm: `Họ Tên｜NN歳` (to) → từng dòng `nhãn｜nội dung` (仕事 / 経験 / 資格 / 得意 / 性格 / 過去 / 現在 / 本音…), 3–5 dòng, ≤16 chữ/dòng.
4. **KHÔNG đọc** chữ block (chỉ 1 câu VO ngắn ở shot lộ mặt ngay trước). Dòng cuối giữ ≥3s. 9–14s/người.
5. Chỉ nhạc nền (luật 12) — không tiếng gõ phím. Màu = màu thẻ tên của lane (`script.hook.the_ten.mau/mau_phu`, đổi được ở `script.hook.block_gioi_thieu`).
6. Người có block → không làm thẻ tên (tool tự ghi `the_ten.json` `bo_qua`).

Ảnh mẫu anh đã duyệt: `E:\CLAUDE\YOUTUBE\h2dev\docs\hook_mau\block_gioi_thieu_ep10O_usami.jpg`, `..._kitami.jpg`.

## Lệnh (máy 1, SAU khi đủ clip Grok, TRƯỚC `xem_thu_hook_giong.py`)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập> --nhap   :: nháp hook\block_gioi_thieu.json
:: sửa: sau_shot (shot lộ mặt), ten "Họ Tên", tuoi, dong [[nhãn, nội dung]...], dur_s; khung cuối nhắm mắt/mờ → "t": giây lấy khung
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập>          :: render + chèn shot vào timeline
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\block_gioi_thieu.py --profile <lane> --slug <tập> --kiem
```
Ra `hook\clip\clip_NN.mp4` (số shot mới, không đổi tên file cũ) + shot LẶNG `{"freeze": true, "block": id, "lang_s"}` trong
`hook_timeline.json` + ảnh soi `hook\qc\block_<id>_soi.jpg` (PHẢI mở xem: chữ không đè mặt). Máy 2 chỉ ghép (`cau_vai.lang_hook`)
→ giao máy 2 kèm `dong_goi_may2.py --bundle`.

## Bẫy đã gặp (ep10)
- Khung cuối clip Grok nhân vật nhắm mắt → đặt `"t": 1.0` (chớp trắng che chỗ nhảy hình).
- Ảnh AI hay vẽ thêm người lộ mặt ở cửa/nền trước block → prompt "Nobody else's face is visible", soát ảnh trước Grok.
- Dòng dài (vd 「じゃあ、辞めます」で前職を退職) chạm gần mặt — tool cảnh báo, không tự cắt chữ anh viết.
