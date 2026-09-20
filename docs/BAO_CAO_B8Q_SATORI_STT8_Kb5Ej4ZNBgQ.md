# BÁO CÁO QC KHỚP LỜI — SATORI STT 8

Ngày: 2026-09-17
Lane: satori / Lopezzapa68
STT: 8
Slug: simbot2-08-Kb5Ej4ZNBgQ

## 1. Hiện trạng

Pipeline bước 3 đã chạy xong:

- 133/133 ảnh trên đĩa.
- Render `chay_buoc3.py`: ĐẠT, tổng 19,5 phút.
- Giao hàng đã tạo tại:
  `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep08-simbot2-08-Kb5Ej4ZNBgQ`
- Cột G đã ghi đường dẫn giao hàng.
- Cột H hiện ghi `Video xong - Chờ đăng`.
- `final.mp4` giao hàng dài khoảng 31:28.

Tuy nhiên, QC model khớp lời chạy SAU khi giao hàng đã báo RỚT:

```text
=== VIDEO: 6 VẤN ĐỀ
✗ ẢNH LỆCH LỜI: trung bình 3.1/5, 5/14 mốc ≤2
```

Đây là bản kiểm tra bổ sung bằng `pipeline/qc_visual.py`, không phải kết quả B8Q nội bộ của `chay_buoc3.py`.

## 2. Lệnh QC đã chạy

```bash
env -u PYTHONPATH py -3.13 pipeline/qc_visual.py video \
  --mp4 "E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep08-simbot2-08-Kb5Ej4ZNBgQ\final.mp4" \
  --srt "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-08-Kb5Ej4ZNBgQ\voice_paced.srt" \
  --audio-sec 0 --sample 14 --no-sub
```

Lưu ý: `--audio-sec 0` được dùng vì qc_visual tự đọc duration từ MP4; duration đo bằng imageio-ffmpeg là 00:31:28.30.

## 3. Các mốc QC báo lệch

1. **67 giây — điểm 2/5**
   - Hình: phong bì tang lễ trong ngăn kéo.
   - Lời: `机の、こちら側にいた者として、`
   - Nhận xét model: hình không phải người đang ngồi ở phía bên này của bàn.

2. **470 giây — điểm 1/5**
   - Hình: một phụ nữ lớn tuổi ở đền/thần xã.
   - Lời: `私の元同僚が、そのうちの、何人かの、袖に、すがられて、辞めた。`
   - Nhận xét model: hình không liên quan đến cảnh đồng nghiệp bị nhiều người níu kéo rồi nghỉ việc.

3. **741 giây — điểm 2/5**
   - Hình: chữ viết trên phong bì phúng điếu.
   - Lời: `九州のお孫さんの名前まで、ちゃんと覚えていました。`
   - Nhận xét model: hình không minh họa việc nhớ tên người cháu ở Kyushu.

4. **1283 giây — điểm 1/5**
   - Hình: cảnh không khớp với việc chào mời chuyển sang sản phẩm/dịch vụ khác.
   - Lời: `今、皆さん、こちらに乗り換えて、いらっしゃいますよ」。`
   - Nhận xét model: hình không minh họa câu chào mời chuyển đổi.

5. **1552 giây — điểm 2/5**
   - Hình: cảnh ngoại thất lúc chạng vạng.
   - Lời: `金の細い縁取りの額には、たった一行の短い字がございました。`
   - Nhận xét model: hình không phải chiếc khung có viền vàng và một dòng chữ ngắn.

## 4. Chẩn đoán sơ bộ

Không tự kết luận ngay rằng toàn bộ anchors sai. Cần Claude Code kiểm tra từng mốc theo thứ tự:

1. Đọc `img_doan.txt`, `anchors.txt`, `voice_paced.srt` và `img_prompts.txt`.
2. Xác định ảnh thật đang hiện tại từng mốc.
3. Đối chiếu prompt/ảnh với câu neo và câu thoại tại đúng timestamp.
4. Phân loại:
   - ảnh/prompt đã sai từ bước 1;
   - anchors đặt sai câu;
   - ảnh đúng nội dung nhưng model QC hiểu sai;
   - stock/ảnh fallback bị gán sai vị trí.
5. Không đổi số trong `img_doan.txt` hoặc `anchors.txt` chỉ để làm điểm QC đẹp hơn.

## 5. Điều cấm

- Không `--force-qc`.
- Không tự sửa `script.txt`, `img_prompts.txt`, `img_doan.txt`, `anchors.txt`.
- Không tự đổi ảnh giữa các slot.
- Không tự gen lại toàn bộ ảnh.
- Không tự chạy lại render trước khi xác định nguyên nhân 5 mốc.
- Không xóa bản giao hàng hiện tại.
- Không ghi đè cột G/H trong Sheet khi chưa có quyết định xử lý.

## 6. Việc Claude Code cần trả lời

Kiểm tra 5 mốc trên và nối báo cáo vào cuối file này:

```text
[CLAUDE] <giờ> MỐC 67s: ảnh thực tế / prompt / anchor / kết luận / đề xuất
[CLAUDE] <giờ> MỐC 470s: ảnh thực tế / prompt / anchor / kết luận / đề xuất
[CLAUDE] <giờ> MỐC 741s: ảnh thực tế / prompt / anchor / kết luận / đề xuất
[CLAUDE] <giờ> MỐC 1283s: ảnh thực tế / prompt / anchor / kết luận / đề xuất
[CLAUDE] <giờ> MỐC 1552s: ảnh thực tế / prompt / anchor / kết luận / đề xuất
[CLAUDE] <giờ> KẾT LUẬN: QC sai / lỗi bước 1 / lỗi anchors / cần xử lý gì
```

## 7. Trạng thái Hermes

Hermes dừng sau QC, chưa sửa dữ liệu và chưa render lại. Bản giao hàng hiện tại vẫn được giữ nguyên để đối chiếu.

Đường dẫn báo cáo này:

```text
E:\CLAUDE\YOUTUBE\h2dev\docs\BAO_CAO_B8Q_SATORI_STT8_Kb5Ej4ZNBgQ.md
```

Đường dẫn để Claude Code đọc và xử lý:

```text
Đọc và xử lý file: E:\CLAUDE\YOUTUBE\h2dev\docs\BAO_CAO_B8Q_SATORI_STT8_Kb5Ej4ZNBgQ.md
```

# HẾT BÁO CÁO
