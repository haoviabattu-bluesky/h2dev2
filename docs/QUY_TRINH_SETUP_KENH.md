# QUY TRÌNH SETUP KÊNH — mail nuôi hàng loạt + branding kênh sản xuất thật

> Đã dọn khỏi CLAUDE.md 2026-09-16 (chỉ cần đọc khi đang MỞ 1 kênh mới, không phải mỗi lần sản xuất
> video — CLAUDE.md chỉ giữ 1 dòng trỏ sang file này).

## QUY TRÌNH BATCH: TẠO KÊNH + UP AVATAR (`tools/channel_setup.py`)
Lệnh của anh dạng **"tạo kênh, up ảnh cho dòng x-y"** → chạy:
`py -3.13 tools\channel_setup.py 3` (1 dòng) hoặc `3-5` (dải, tuần tự từng dòng).
KHÔNG nói rõ dòng → PHẢI HỎI dòng nào, cấm chạy tất cả (quy tắc anh chốt 2026-09-06).
Flow mỗi dòng (verify thật trên dòng 3): đọc mail cột B → tìm profile GPM trùng tên (quét hết
trang, GPM không filter name) → start lấy ws CDP (port đổi mỗi lần) → `youtube.com/create_channel`
giữ TÊN MẶC ĐỊNH bấm Create channel (không có dialog = đã có kênh) → gpti2 sinh avatar động vật
hoạt hình (1024x1024 medium, re-save Pillow xoá C2PA, lưu `assets/avatars/`) → Studio
`/editing/profile` up Picture → ghi sheet cột TÊN KÊNH/NGÀY TẠO KÊNH (tra theo header) → stop profile.
Bẫy Studio đã dính: dialog `ytcp-warm-welcome-dialog` chặn click (bấm Continue), tooltip Ask
Studio che Publish (Close/Escape), ≥3 nút Upload phải phân biệt bằng innerText tổ tiên
(`profile picture` vs `top of your channel`), thành công = Publish `aria-disabled=true`.
Ghi sheet bằng service account trực tiếp (MCP gsheets hay đứt 10054 khi write).
Chưa gồm (mở rộng sau theo SOP M1-03): banner, đổi vị trí thị trường, xác minh, add quyền, ngâm kênh.
Tool này chỉ dùng cho **mail nuôi hàng loạt** (avatar động vật ngẫu nhiên) — KHÔNG dùng cho kênh
sản xuất nội dung thật, xem quy trình đầy đủ ngay dưới đây.

## ⭐ QUY TRÌNH SETUP KÊNH ĐẦY ĐỦ (user chốt 2026-09-10 — BẮT BUỘC trước khi làm việc khác)
Khi triển khai 1 kênh THẬT (kênh sẽ đăng nội dung, khác mail nuôi hàng loạt ở trên), phải hoàn tất
**TOÀN BỘ** các bước A+B dưới đây rồi mới được chuyển sang việc khác (viết kịch bản, sản xuất
video...). Dừng ở avatar/tên/mô tả cơ bản là THIẾU quy trình, không tính là xong.

**A. Branding (Studio → Customization → Profile — trang `/editing/profile`, gom cả A+B mục 8-10):**
1. Avatar — icon/emblem khớp bản sắc kênh (KHÔNG dùng avatar động vật ngẫu nhiên của
   `channel_setup.py` — cái đó chỉ cho mail nuôi).
2. Banner — khung cố định của ngách (màu/bố cục theo mô-típ đã chốt), overlay tên kênh bằng PIL
   Yu Gothic Bold (`C:\Windows\Fonts\YuGothB.ttc`) — model gpti2 KHÔNG render chữ Nhật chuẩn.
3. Name (display Name, khác Handle) — theo tên đã chốt trong hồ sơ/handoff đề tài.
4. Description — theo bản mô tả đã duyệt.

**B. Settings (modal "Settings" ở sidebar trái Studio — KHÔNG vào thẳng URL `/settings`, ra lỗi
"Oops"). Chi tiết selector từng mục xem memory dự án `channel-settings-checklist`:**
5. General → Currency = **VND — Vietnamese Dong** (mặc định USD, phải tự đổi).
6. Channel → Advanced settings → Audience = **"No, set this channel as not made for kids..."**
   (mặc định Google để "review mỗi video", phải đổi).
7. Upload defaults → Basic info: Description = 5 hashtag riêng của kênh (lấy từ hồ sơ đề tài, đừng
   copy hashtag của kênh khác). Advanced settings: Video language + Title/description language =
   đúng ngôn ngữ kênh (Nhật/Hàn...).
8. Profile → Handle = handle CÓ Ý NGHĨA khớp tên kênh, không để mặc định `@TênGmailNgẫuNhiên`.
9. Profile → Links → Add link (Studio tự điền sẵn `Youtube` + channel URL — chỉ cần dọn dòng rỗng
   thừa nếu bấm Add link quá 1 lần).
10. Profile → Contact info → Email = mail cột B của dòng sheet (mail đăng nhập kênh).

**⚠️ Trước khi sửa bất kỳ mục nào ở B, RELOAD trang thật để kiểm tra trạng thái hiện tại** — nhiều
mục (Links, Contact email, đôi khi cả Handle) có thể **ĐÃ ĐÚNG SẴN** do Google tự điền mặc định;
đừng suy diễn từ form đang mở dở, và đừng ghi đè nếu đã đúng.

### ⭐ TOOL THAM SỐ HOÁ (2026-09-20, verify thật trên kênh 定年後のリアル / Lane F, dòng 7 GMAIL)
```
py -3.13 tools\channel_branding.py --config assets\<lane>\branding\KENH.json --check-only   # đọc trạng thái, KHÔNG sửa
py -3.13 tools\channel_branding.py --config ... --steps profile --no-sheet                    # A: banner/avatar/tên/handle/mô tả/links/email
py -3.13 tools\channel_branding.py --config ... --steps settings --no-sheet                   # B: currency/country/keywords/audience/upload defaults/2 ngôn ngữ
py -3.13 tools\channel_branding.py --config ...                                               # A+B + ghi sheet (GMAIL: TÊN KÊNH/NGÁCH/THỊ TRƯỜNG/KÊNH_CLONE · NOTE: NHẬN KÊNH/MAIL/HANDLE/KÊNH)
```
Một file `KENH.json` cạnh ảnh = 1 nguồn chân lý (mẫu: `assets/teinengo-real/branding/KENH.json`).
Ảnh: `avatar_raw.png` sinh ima2 (0đ) + `banner_final.png` = nền ima2 → `pipeline/banner_text.py`
overlay tên PIL. Mỗi mục reload đọc trước, đúng rồi thì bỏ qua; không thấy phần tử → chụp `_s_*.png`
vào thư mục branding rồi báo. Bản cũ `channel_branding_laneD.py`/`_laneE.py` giữ để tham khảo, KHÔNG dùng.

**SAU KHI SETUP XONG (anh chốt 2026-09-20), 3 việc bắt buộc:** (1) tool tự tạo tab sheet tên = `lane_id` với
header A→K giống `70dai-kenko`; (2) viết `docs/BAT_DAU_LANE/<lane_id>.md` theo khuôn `teinengo-real.md` (định danh,
trạng thái, tài liệu ở đâu, quy trình bước nào trước, cột sheet); (3) 1 dòng bảng lane `CLAUDE.md` + 1 dòng
`docs/DANH_BA_LANE.md`. Câu "thực hiện lane <mã>" của anh trỏ thẳng vào file (2).

**Bẫy đã trả giá 2026-09-20 (đều đã vá trong tool, đọc để khỏi "sửa lại cho gọn"):**
- **GPM `start` trả `success` nhưng websocket RỖNG** khi profile đang đóng dở → mỗi lần gọi lại là mở
  THÊM 1 cửa sổ cùng profile (anh thấy 3 cửa sổ). Tool chỉ thử 2 lượt có stop+chờ 12s, không lặp.
  `--keep-open` xong mà chạy lại ngay = `ProfileInUse`. GPM `stop` báo OK nhưng có thể còn sót tiến trình
  chrome của đúng profile đó → chỉ đóng theo PID đối chiếu `--user-data-dir` chứa id profile.
- **Reload ngay sau Publish trang Profile đọc ra giá trị CŨ** (tên/handle/mô tả cập nhật trễ 10–30s)
  dù đã lưu thật → verify phải chờ 15s + reload tối đa 3 lần, đừng kết luận "mất hết" rồi làm lại.
- Sidebar Studio thu gọn thì chữ "Settings" ẩn → bấm icon `ytcp-navigation-drawer #settings-item`.
- Modal Settings = `<ytcp-settings-dialog>`; tab/tab con là CHỮ THƯỜNG (không `role=tab`), có bản sao ẩn →
  lọc `is_visible()` trước khi bấm. Dropdown = `ytcp-dropdown-trigger` chứa nhãn ("Country of residence",
  "Currency", "Video language", "Title and description language") — tìm theo NHÃN, đừng tìm chữ "Select".
  Option menu = `tp-yt-paper-item`. Radio Audience = `tp-yt-paper-radio-button[aria-checked]`.
- **Bấm Save là modal TỰ ĐÓNG** (toast "Settings saved") → mục tiếp theo phải mở lại modal; Save disabled
  (không đổi gì) thì modal vẫn mở, đừng mở thêm (backdrop chặn click).
- **Ghi sheet PHẢI tra cột theo TÊN header** (`col(svc, "TÊN KÊNH")`), không hardcode chữ cái: sheet đã chèn
  cột PHONEVER làm TÊN KÊNH lùi F→G; tin bảng cột trong tài liệu là ghi đè nhầm (dính 16/09 và 20/09).
- Hộp Google "Verify it's you" có thể bung trên trang Profile → bấm Next mở **POPUP accounts.google.com** (tab
  hiện tại không đổi — đo thật Lane I) → tool tìm trang popup trong context rồi điền mật khẩu → TOTP cột C.
- **Handle bị từ chối im lặng**: gõ handle đã có người dùng thì YouTube hiện "This handle isn't available. Here's one
  available: @xxx" ngay dưới ô, Publish VẪN bấm được và mọi thứ khác lưu bình thường, riêng handle giữ cũ (đo thật
  Lane H: `@kokoro-kazoku` bị chiếm) → tool đọc khối cha ô handle, báo lỗi kèm gợi ý, trả handle cũ; verify reload
  sau Publish là lớp chặn cuối. Đổi handle khác trong KENH.json rồi chạy lại `--steps profile`.
