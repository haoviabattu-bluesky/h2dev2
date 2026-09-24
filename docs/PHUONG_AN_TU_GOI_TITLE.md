# PHƯƠNG ÁN — Giao máy 2 xong thì TỰ gọi dự án YT-TITLE-RESEARCH (mọi lane)

> ✅ **ĐÃ LÀM (2026-09-24).** P1–P4 dưới đây đã code xong + verify `--dry` trên tập thật của cả 6 lane
> đã bật (satori, A, D, E, F, G) — xem log cuối file. Giữ tài liệu này làm bản thiết kế/tra cứu.

Anh chốt 2026-09-24:
1. Tập nào của lane nào giao máy 2 xong thì tự chạy dự án tiêu đề, anh không gõ tay nữa.
2. Code dự án TITLE giữ nguyên ở `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH`, không copy sang h2dev.
3. Thumbnail: máy tự chọn (lấy bản Opus/Fable đề xuất).
4. Tiêu đề · mô tả · tags · thumbnail giao HẾT cho TITLE; h2dev thôi làm (bật `publish.listing_external`).

## Bước P1 — `E:\CLAUDE\YOUTUBE\h2dev\pipeline\goi_title.py` (1 hàm chung, mọi đường giao gọi vào)
- Vào: đường dẫn tuyệt đối thư mục tập. Lane **tự dò** bằng cách so với `slug_dir` của mọi profile
  (không dựa vào trí nhớ người gõ). Có truyền `--profile` mà lệch với lane dò được → DỪNG.
- Cổng trước khi chạy (thiếu cái nào là DỪNG + in đúng tên file thiếu, KHÔNG để TITLE rơi về luật satori):
  profile h2dev · `YT-TITLE-RESEARCH\config\lanes\<id>.json` · `<id>.thumb.yaml` · thư mục `deliver_root`
  · `script.txt` · `HOOK_TAP.md` (nếu lane bật hook).
- Chạy NỀN, tách khỏi shell (không bắt việc giao máy 2 phải chờ):
  `cli.py run --slug <tập> --profile <id>` → `thumb-publish` (không `--choose` = lấy bản đề xuất; đề xuất
  không "accept" thì `--choose <bản đề xuất>`) → `sheet-publish`.
- Ghi `<tập>\research\TU_DONG_TITLE.log` + `TU_DONG_TITLE.json` (đang chạy / xong / lỗi ở bước nào).
- Khoá chống chạy đôi; tập đã publish thumbnail rồi thì bỏ qua.
- Có `--dry` (chỉ in lane dò được + cổng + lệnh, không chạy) và `--wait` (chạy chặn, để test).

## Bước P2 — nối vào CẢ 3 đường giao máy 2
| Đường | Chỗ nối |
|---|---|
| `pipeline\dong_goi_may2.py --job` (E, F, G) | cuối `cmd_job`, trước `return dst` |
| `pipeline\drive_handoff.py upload-job` (satori, A) | sau khi copy xong, chỉ khi thư mục nguồn nằm trong `slug_dir` 1 lane |
| `pipeline\goi_buoc2_3.py` (A) | cuối lệnh gói |
Mỗi đường có cờ `--no-title` để tắt khi cần.

## Bước P3 — tắt B7/B9 bên h2dev: `publish.listing_external: true`
satori-jp-obaa · toshi-densetsu-jp · irogatatarukioku · kenko-chiebukuro (F, G đã bật sẵn).
Hệ quả đã kiểm trong code: make_video bỏ B7/B9; `giao_hang.py` không đòi thumbnail/listting;
`qc_final.py` bỏ kiểm ảnh bìa (kiểm hook vẫn chạy).
⚠️ Lane A: `title.txt` do TITLE ghi (cờ `write_title_txt`) — cổng hook/gói đăng h2dev đọc file này; kiểm lại 1 tập.

## Bước P4 — sửa nhỏ bên TITLE (sửa tại chỗ, không copy)
- Nối `promise.txt` vào prompt S1 (hàm `promise()` có sẵn nhưng chưa ai gọi).
- `run` trả mã thoát ≠ 0 khi hỏng giữa chừng (để P1 ghi đúng trạng thái lỗi).
- Có tab khác đang làm ở TITLE (vừa tạo `teinengo-real.json` 14:15 hôm nay) → chỉ đụng đúng 2 chỗ trên.

## Bước P5 — nghiệm thu
1. `goi_title.py --dry` trên 1 tập thật của mỗi lane → lane dò đúng, cổng đúng.
2. Lane H/I/J (chưa có profile/cấu hình) → phải DỪNG kèm lý do, không chạy.
3. Chạy thật 1 tập 1 lane (`--wait`) → đủ `TIEU_DE_MO_TA.txt`, `thumbnail_final.png`, CHANEL, Sheet E/G/K.
4. Cập nhật `docs\QUY_TRINH_GIAO_VIEC_MAY2.md` + `docs\QUY_TAC_VIDEO_HOOK.md` §0b (1 dòng trỏ sang file này).

Chi phí mỗi tập (tự động, không hỏi): ~3 ảnh gpti2 + 2 lượt Sol + các lượt `claude -p` (quota gói, không phải hoá đơn).
Tập đã giao TRƯỚC khi bật: không tự chạy lại; muốn làm bù thì `goi_title.py --slug <tập>` từng tập.

## Nhật ký thực hiện (2026-09-24)
- `pipeline\goi_title.py` (mới): tự dò lane theo `slug_dir`, cổng đủ 5 điều kiện, chạy nền qua
  `--worker`, thumbnail máy tự chọn (đọc `chosen` trong `fable_review.json` khi Opus chưa "accept").
- Nối vào `dong_goi_may2.py::cmd_job` (cờ `--no-title`), `drive_handoff.py` (cả nhánh local +
  Drive, env `GOI_TITLE_TAT=1` để tắt), `goi_buoc2_3.py` (cờ `--no-title`, lane cứng toshi-densetsu-jp).
- Bật `publish.listing_external: true` cho 4 profile còn thiếu: satori-jp-obaa, toshi-densetsu-jp,
  irogatatarukioku, kenko-chiebukuro (F, G đã có sẵn từ trước).
- Bên TITLE: nối `promise.txt` vào prompt S1 (`src/s1_summarize.py` + `prompts/s1_summarize.md`,
  hàm `sc.promise()` có sẵn nhưng trước đó chưa ai gọi). Không cần sửa exit code — `cli.py` vốn đã
  không bắt exception ở `main()`, lỗi giữa chừng tự thoát non-zero.
- Verify `--dry` trên tập thật: A/D/E/G → đủ điều kiện. Satori (`ep3-sougi`) → DỪNG đúng vì thiếu
  `HOOK_TAP.md` (đã biết từ trước, không phải lỗi mới). F (`ep01-fuufu-nenkin-sa`) → DỪNG vì
  `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real` chưa tồn tại (máy 2 chưa từng giao hàng lane này —
  ngoài phạm vi việc nối dây, cần tạo thư mục CHANEL hoặc giao 1 tập trước).
- Chưa làm/không thuộc phạm vi: lane H/I/J (chưa có profile h2dev), `qc_final.py`/`giao_hang.py`
  đã tự đọc `listing_external` từ trước nên không cần sửa gì thêm ở đó.

## Đợt 2 (2026-09-24 chiều) — tăng tốc A + công tắc lane
- Đo thật ep02 Lane F: tiêu đề+mô tả ~10' · tags ~9' · khoá chữ thumbnail ~10'/lượt (Fable↔Sol tối đa 4
  vòng, 2 lượt đều "escalate" = dừng chờ người) · vẽ+chấm ~5' → nối đuôi 35–45'. Ghép code TITLE vào h2dev
  KHÔNG nhanh hơn (thời gian nằm ở lượt LLM, gọi chéo dự án <1 giây) → không ghép.
- **A (đã làm, phía h2dev):** worker chạy `run --no-thumb --no-tags --no-sol-check` rồi `tags` ‖ `thumb`
  song song, log từng nhánh riêng (`TU_DONG_TITLE.tags.log` / `.thumb.log`), ghi log trực tiếp khi đang chạy,
  khoá `TU_DONG_TITLE.lock` chống chạy đôi, thumbnail "escalate" → DỪNG báo rõ (không ép publish khi chưa có ảnh).
- **B (bên TITLE, giao qua lệnh anh copy):** cờ `thumb --auto` — worker tự dò `thumb --help`, có thì truyền.
- **Công tắc `publish.title_auto`:** kênh mới mặc định TẮT; bật bằng `goi_title.py --bat <lane>` sau khi setup
  TITLE tập đầu. Bật 5 lane đã từng chạy đủ tiêu đề + thumbnail bên TITLE; lane D để tắt (0 lần thumbnail).
