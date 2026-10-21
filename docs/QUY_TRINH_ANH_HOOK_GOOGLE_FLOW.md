# ẢNH HOOK BẰNG GOOGLE FLOW (Ultra) → 9router → gpti2 — anh chốt 16/10/2026, mọi lane

> Cùng tài khoản Ultra làm clip Vids (`nguyenquoctuan102000@gmail.com`, `E:\CLAUDE\YOUTUBE\TUAN_PROFILE`, cổng 9350) giờ vẽ luôn
> ẢNH hook. Thay `gen_images.py --cast-root` / `hook\_gen_ima2.py` riêng từng tập. Ảnh THÂN bài (máy 2) không đổi.

## 1. Lệnh
```
:: xem kế hoạch (không vẽ)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\anh_hook.py <thư mục tập TUYỆT ĐỐI>\hook --dry

:: chạy thật (Bash run_in_background) — đọc <hook>\img_prompts_hook.txt, ra <hook>\img\NNN.png, ảnh đã có thì bỏ qua
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\anh_hook.py <thư mục tập TUYỆT ĐỐI>\hook

:: xem profile Ultra có đang bị tập khác giữ không
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\khoa_ultra.py
```
Tham số: `--chi 3,7` (vẽ lại vài ảnh: thêm `--lam-lai`, ảnh cũ chuyển `img\_cu_<giờ>\`, không xoá) · `--tabs 2` (số tab Flow
TRONG 1 tập, mỗi tab 1 dự án riêng) · `--nguon 9router|gpti2` (bỏ qua Google) · `--nguon google` (CHỜ khoá thay vì sang 9router) ·
`--ref <master>` cho prompt kiểu `@REF` (Lane F) · `--prompts/--out/--cast-root` khi không theo chỗ mặc định.

## 2. Thứ tự nguồn (tool tự chuyển, ghi nguồn từng ảnh vào `img\manifest.json` + `img\_anh_hook_log.csv`)
| # | Nguồn | Khi nào |
|---|---|---|
| 1 | **Google Flow** · Nano Banana Pro · 16:9 · x1 · **0 tín dụng** | profile Ultra RẢNH + cổng 9350 sống (chết thì tool tự mở lại bằng `open_tuan_profile.bat`) |
| 2 | **9router** (`img_9router.py`, Codex 0đ) | cổng BẬN (tập khác đang giữ profile — ảnh hoặc clip Vids) · cổng không mở được · ảnh Google lỗi/bị từ chối/quá 240s |
| 3 | **gpti2** (`gpti2_edit` có ref / `gpti2_gen`) — tốn VNĐ | 9router lỗi 2 lần. Dòng `@GROK` (trẻ em) đi Grok thay gpti2 |

⛔ **Các tập KHÔNG chạy profile Ultra song song.** `anh_hook.py` và `tools\hook_lane_g\vids_hook.py` cùng giữ khoá
`E:\CLAUDE\YOUTUBE\TUAN_PROFILE.lock` (`pipeline\khoa_ultra.py`, hệ điều hành tự nhả khi tiến trình chết). Ảnh hook gặp khoá bận
→ KHÔNG chờ, sang 9router ngay. Clip Vids gặp khoá bận → CHỜ tới lượt (`--cho-khoa 360` phút).

## 3. Tool làm gì trên Flow (đo thật 16/10, ep11-bento-line Lane N)
- Mỗi tab: `flow.google.com` → **Dự án mới** → đặt Hình ảnh · 16:9 · **Nano Banana Pro** (model tự trôi về 2.1 mỗi dự án) · x1 ·
  tắt chip Tác nhân.
- Khoá mặt: master `_ref_<id>\001.png` chép thành `img\_flow_ref\ref_<id>.png` → nút **+** → tải lên (lần đầu trong dự án) → tìm theo
  tên → **Thêm vào câu lệnh**; chờ tới khi ô soạn hiện đủ N ảnh. Prompt thêm đầu câu "Attached reference images, in order: 1 = kawai, 2 = harumi…".
- Bấm Tạo → chờ UUID ảnh mới (`flow-content.google/image/<uuid>`) → menu ảnh → **Tải xuống 2K** → cắt đúng 16:9 → PNG 2560x1440
  (cỡ chuẩn ảnh hook cũ). 2K hỏng → lấy bản gốc 1376x768 phóng lên.
- Kết quả: 4/4 ảnh đạt (1 và 2 người), mặt khớp master rất sát, 70–128 giây/ảnh gồm cả tải ref + 2K. Chữ trên giấy tờ vẫn là ô trắng
  → vẫn CHÈN CHỮ bằng `chu_dao_cu.py` như cũ.

## 4. Bẫy đã dính (16/10)
1. `page.url` của Playwright là bản ĐỆM, không đổi khi chỉ ngủ chờ → đọc `location.href` (tool từng báo "không vào được dự án mới" oan).
2. Ảnh ref vừa tải còn đang xử lý: bấm chọn được nhưng ô soạn chỉ hiện biểu tượng chờ → phải đợi ô soạn có đủ `<img>`.
3. Bảng chọn: có lúc bấm thẻ là thêm thẳng, có lúc chỉ chọn → còn lớp phủ thì bấm "Thêm vào câu lệnh".
4. Chữ tiếng Việt trong DOM Flow có chỗ lưu dạng tổ hợp → so khớp chữ bằng JS `normalize('NFC')`, đừng dùng `get_by_text`.
5. Tải 2K ở tab NỀN ra file 0 byte → đưa tab lên trước khi tải; tải qua CDP phải `save_as`, không dùng `download.path()`.
6. Không reload trang khi đang chờ ảnh (đổi link ảnh, mất dấu UUID — skill `veo3_flow_automation.md` §11.4). Lỗi giữa chừng → tool
   đóng tab đó, việc sau mở dự án mới.
7. Không kill Chrome; tool chỉ đóng tab nó mở.
