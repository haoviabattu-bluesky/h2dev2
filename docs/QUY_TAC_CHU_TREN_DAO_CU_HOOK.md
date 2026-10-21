# ⛔ QUY TẮC CHỮ TRÊN ĐẠO CỤ HOOK — chèn chữ vào ẢNH bằng code TRƯỚC khi sinh clip (anh chốt 10/10/2026, MỌI lane)

> Ảnh hook (gpti2/ima2) cố tình vẽ giấy tờ/biển/màn hình TRƠN (chữ AI = chữ lạ, méo). Ở cảnh mà CHỮ trên đạo cụ là điểm
> nhấn (giấy kết hôn 婚姻届, bảng bán nhà 売家, 退職届 (đơn nghỉ việc), 通帳 (sổ ngân hàng) số dư, tin nhắn LINE, biên bản có
> tên…) tờ giấy trắng làm cảnh mất nghĩa. Anh chốt: **máy 1 điền chữ vào ẢNH trước, rồi MỚI sinh video** từ ảnh có chữ.
> Grok sinh clip từ ảnh có chữ mà làm lỗi/méo chữ → đó là giới hạn của Grok, KHÔNG phải lỗi khâu này (không sửa clip).
> Tool: `pipeline\chu_dao_cu.py`.

## 1. Luật
1. **Thứ tự:** vẽ ảnh hook → QC ảnh → **chèn chữ vào ảnh** → sinh clip Grok. `grok_da_luong.py` CHẶN nếu ảnh nghi có chữ chưa
   quyết hoặc ảnh đã khai chưa chèn. Clip đã sinh từ ảnh trơn → phải sinh lại từ ảnh có chữ (`duyet_hook --gui` chặn).
2. **Ảnh nào cần chữ:** chữ trên đạo cụ được lời hook nhắc tới hoặc là lý do cảm xúc của cảnh (tên trên biên bản, 離婚届 trên
   bàn, 売家 trước nhà, số dư sổ, câu tin nhắn). Giấy tờ phông nền, chữ không ai cần đọc → để trơn, ghi `bo_qua` kèm lý do.
3. **Nội dung chữ:** tiếng Nhật đúng thể thức thật (tiêu đề form, mục 氏名/日付…), tên/số khớp `characters.json` + `SỐ ĐƯỢC PHÉP`,
   KHÔNG lộ thông tin thân bài chưa tới, ít chữ (1 tiêu đề + ≤4 dòng), đọc được ở 720p. Chữ nằm trên MẶT PHẲNG của vật (không
   vắt qua nắp phong bì/nếp gấp) — chọn `goc` trùm đúng vùng phẳng.
4. **Hình:** chữ dán theo phối cảnh của mặt đạo cụ (4 góc), in kiểu mực (multiply — ăn bóng/ánh sáng của giấy), tay/vật che
   thì không đè lên. Soi `hook\chu\NNN_soi.jpg` (trước | sau) trước khi sinh clip.
5. **Prompt Grok** của ảnh đã chèn tự sửa trong `grok_jobs.csv`: bỏ "no text" + thêm `KEEP TEXT:` (giữ nguyên chữ, không thêm
   chữ, máy quay gần như đứng yên, tay không che chữ) — giúp Grok giữ chữ tốt nhất có thể.
6. **Từ khâu vẽ** (`hook_storyboard.py`): shot đạo cụ có chữ → mặt TRƠN, phẳng, gần chính diện, chiếm ≥20% khung, không tay
   che, viền rõ, camera gần như đứng yên.
7. Ảnh gốc trơn cất ở `hook\img\_goc\` (không gửi máy 2); chạy lại luôn đi từ bản gốc.

## 2. Kiểu tờ chữ (`mau`)
| `mau` | Dùng cho | Hình |
|---|---|---|
| `giay_to` | biên bản, hợp đồng, 婚姻届, 退職届 dạng form, thông báo | tiêu đề Minchō giữa, gạch kẻ, các dòng 「氏名　…」, `dau` = con dấu đỏ |
| `phong_bi` (hoặc `doc: true`) | phong bì đứng 退職届/遺言書, thư dọc | chữ dọc lớn giữa, dòng phụ dọc góc trái dưới |
| `bien` | biển 売家/貸家, biển cửa hàng, giấy dán | chữ đậm to căn giữa, mặc định đỏ, phủ thẳng (`tron: phu`) |
| `man_hinh` | màn hình điện thoại/máy tính, LINE | thanh tiêu đề + bóng thoại (dòng bắt đầu `>` = bên phải, xanh) |
| `nhan` | phong bì nằm ngang, bảng tên, nhãn, sổ 1–2 dòng | chữ căn giữa vừa khung |
Tuỳ chọn: `font` (SM Minchō / NJ Gothic / MR tròn), `mau_chu`, `tron` (`nhan` multiply / `phu` phủ), `che` (false = bỏ lọc
tay che), `ti_le` (cao/rộng tờ thật). Thứ tự `goc` quyết định chiều chữ: cạnh TRÁI-TRÊN→PHẢI-TRÊN là "đỉnh" tờ chữ.

## 3. Quy trình (máy 1 — `docs\NHAN_KICH_BAN_MAY3.md` §4, sau QC ảnh hook, TRƯỚC Grok)
```bat
:: 1) liệt kê ảnh nghi có đạo cụ mang chữ (prompt Grok + lời shot) → <tập>\hook\chu_tren_vat.json, mọi ảnh "(CHƯA QUYẾT)"
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập> --nhap
:: 2) ảnh cần chữ: dò mặt phẳng → <tập>\hook\chu\NNN_tim.jpg đánh số tứ giác + in toạ độ 'goc'
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập> --tim 028
:: 3) khai "anh" (img + vat: goc, mau, tieu_de, dong…), bỏ khỏi bo_qua; ảnh không cần chữ: ghi lý do thật vào bo_qua
:: 4) chèn chữ vào ảnh + sửa prompt Grok → soi <tập>\hook\chu\NNN_soi.jpg → rồi mới chạy grok_da_luong.py
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\chu_dao_cu.py --profile <lane> --slug <tập>
```
Tứ giác dò sai (bóng lá, phong bì nghiêng) → tự đo 4 góc trên ảnh `_tim.jpg` (toạ độ 0–1).
Mẫu thật (Lane O ep05, ảnh mẫu `E:\CLAUDE\YOUTUBE\h2dev\docs\chu_dao_cu_mau\`): ảnh 028 — 3 tờ 退職面談記録 (biên bản phỏng vấn
nghỉ việc) mang tên 菊池美羽/北条千秋/日下部蒼 + dấu 施設長; ảnh 023 — phong bì 退職届 日下部蒼.

## 4. Cổng
- `grok_da_luong.py` (trước khi sinh clip): còn ảnh "(CHƯA QUYẾT)" / ảnh có từ khoá đạo cụ chữ (document, envelope, sign, screen,
  届, 記録, 看板, giấy, biển…) chưa khai `anh` hoặc `bo_qua` / ảnh khai chưa chèn hoặc cũ hơn `chu_tren_vat.json` → DỪNG.
  (`--bo-kiem-chu` chỉ khi anh cho phép.)
- `duyet_hook.py --gui`: như trên + clip của ảnh có chữ sinh TRƯỚC khi chèn → DỪNG (sinh lại clip). Chữ méo trong clip không xét.
