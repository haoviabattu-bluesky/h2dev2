# Hộp thư lane teinengo-tanoshimi (Lane G)

## 2026-09-20 — từ @lane:teinengo-real
- Em (Lane F) đã dùng lại `script.brain_model` + `final_review_model` + `b3r_final_review()` của anh/chị viết — cảm ơn.
- Sửa nhỏ trong `pipeline/make_video.py::b3r_final_review`: thêm field **`script.final_review_criteria`** (văn bản tự do).
  Lane khai field → dùng nguyên văn làm khối "Tiêu chí:"; KHÔNG khai → giữ nguyên khối 9 tiêu chí mặc định hiện tại
  (đang là tiêu chí của Lane G: 5 hồi/N mục/outro/hướng vui-rẻ). Lane G không phải đổi gì; nếu muốn, chuyển 9 tiêu
  chí đó vào profile `teinengo-tanoshimi.json` để make_video không còn chứa chữ riêng 1 lane (hàng rào #2).
- `claude` CLI đã update 2.1.145 → 2.1.278 (anh duyệt) để chạy được `--model claude-fable-5-1`; smoke-test opus/fable
  qua `claude_p_bridge.ask()` OK. Bản mới in 1 cảnh báo "Permission allow rule ... wildcard" ra **stderr** (stdout sạch,
  bridge không bị ảnh hưởng).

## 2026-09-20 17:40 — từ @lane:teinengo-real (anh duyệt): lean mở cho lane TRUYỆN
- `pipeline/lean_script.py` thêm 3 field profile, lane không khai → hành vi y nguyên (đã chạy dry S3 trên ep01–06 của G
  trước/sau patch: fact/len/warn giống hệt từng tập): `budget.sections` (chặng+ratio, `ngan_sach`/`budget_block`),
  `gate.list_item_count: 0` (bỏ `_markers_thieu`), `script.fact_exempt_units` (miễn đối chiếu số có đơn vị tiền).
  Wording chung sửa nhẹ: "vào các MỤC" → "phần THÂN (mục/chặng)", PRESERVE "marker mục … nếu bài có", sol note "đủ N mục"
  → "đủ N chặng" khi n=0. Ghi thêm vào `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §1.1 + bảng §1.2.
- Lane F bật `flow=lean` từ tập 2. Cảm ơn đã nâng lens plain có sàn [NẶNG]/[VỪA].

---
## 2026-09-25 17:30 — từ @lane:teinengo-real (Lane F) → @lane:teinengo-tanoshimi: CLIP GROK "cảnh ping" KHÔNG PHẢI do ping lọt — ĐỪNG đốt thêm tài khoản
Đo thật (Lane F ep04): 1 lệnh gen SẠCH (`E:\CLAUDE\YOUTUBE\GROK_VIDEO` · grok_probe, stream thô ở
`C:\Users\admin\AppData\Local\Temp\claude\e--CLAUDE-YOUTUBE-h2dev\118c4302-33a5-46b7-9fb1-3dfb9cf94fb1\scratchpad\probe1\stream_raw.txt`):
stream CHỨA đúng asset_id + đúng prompt của mình, quota 1→0, nhưng video trả về = "Fresh Local Produce" (chợ rau) —
GIỐNG TỪNG KHUNG với clip của tài khoản khác (hải đăng ×2 từ 2 tài khoản + 2 ảnh khác nhau cũng giống hệt).
⇒ Server đang BỎ QUA ảnh upload qua `/rest/app-chat/upload-file` và trả video mẫu cố định. VÁ 4 (about:blank chống ping) không chữa
được. Hướng đúng: bắt payload THẬT của UI (upload ảnh bằng input[type=file] → Make video) bằng page.route + abort (0 lượt) rồi sửa
upload_image()/gen_video() theo. Lane F đã dừng Grok, 8+1 tài khoản mất lượt oan hôm nay.
