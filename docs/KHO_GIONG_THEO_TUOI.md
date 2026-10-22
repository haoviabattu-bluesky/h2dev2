# KHO GIỌNG CHUNG THEO KHUNG TUỔI (anh chốt 22/10/2026)

**Vì sao:** tập nào cũng phải đi tìm giọng rồi bắt anh duyệt, cụ bà cứ bị giọng trẻ (Nữ C `clone_2669056`, もち子さん…)
vì `cast_bank` của lane xếp theo VAI, không theo TUỔI. Nay mọi giọng đã làm + anh đã chốt nằm trong 1 kho, mỗi giọng
khai khoảng tuổi nghe đúng → máy tự chọn, không hỏi lại.

- Kho: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.json` (đi theo git → máy 2 có cùng kho).
- Công cụ: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py`, TỰ CHẠY trong `gan_vai.py`, `tools\hook_lane_g\xem_thu_hook_giong.py`,
  `tts_voicevox.py` → characters.json được sửa tại chỗ (voice có thêm `kho` = mã giọng, `_note` = lý do đổi).

## Luật máy áp
1. Vai có `age` + `gender` → giọng phải nằm trong khoảng tuổi của mục kho. Dưới 60 tuổi lệch ±8 vẫn đạt; từ 60 trở lên chỉ ±3.
2. Giọng sai tuổi / ngoài kho / dính danh sách `cam` → thay bằng giọng kho. Thứ tự ưu tiên: giọng lane đang dùng → anh đã duyệt →
   đã dùng → dự phòng; chưa ai trong tập dùng; không trùng giọng người kể; giọng quát/hách dịch chỉ khi vai có từ khoá.
3. Người kể `ke` = giọng người kể của profile, vai `voice.fixed_cast` đúng giọng khai → giữ (màu kênh). `ke` ngôi 1 và chính
   nhân vật đó (vd 語り（林房江）+ 林房江) → cùng giọng.
4. Vai ≥65 chưa khai speed, lane chưa đọc chậm (voice.speed > 0.9) → speed 0.85.
5. Anh tự chốt giọng ngoài kho cho 1 vai → khai `"giu": true` trong voice của vai đó (máy không đụng, trừ khi dính `cam`).
6. Không có giọng hợp → DỪNG, báo rõ. Lane VOICEVOX (K) muốn giọng cụ bà → bật `voice.ai33_cho_vai` trong profile (như Lane O).
7. Vai NHÓM không có tuổi (`nu_phu`, `nam_phu`) → chỉ cảnh báo; vai già phải tách riêng ra để có giọng già.

## Lệnh
```bat
:: in kho theo khung tuổi
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --bang
:: kiểm + sửa 1 tập (thêm --chi-xem để chỉ xem)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --profile senior_korekara --tap E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep16-tatamiya-41nen
:: quét mọi tập mọi lane, chỉ báo
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --soat
:: anh vừa chốt giọng mới → thêm vào kho (lần sau tự dùng)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --them --ma F_gia_moi --voice-id clone_XXXX --gioi F --tuoi 70-95 --ten "mô tả" --speed 0.85 --fx old-mild --lane senior_korekara --nguon "anh chốt dd/mm tập ..."
```
Anh chê 1 giọng ở 1 khung tuổi → thêm 1 dòng vào `cam` trong kho (voice_id/speaker, gioi, tu_tuoi, den_tuoi, ly_do).
