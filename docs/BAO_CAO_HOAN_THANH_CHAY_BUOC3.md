# BÁO CÁO HOÀN THÀNH — chay_buoc3.py

Ngày làm: 13/09/2026 · Model thực hiện: deepseek-v4-flash (Hermes, session VIDEO RENDER) · Thời gian làm: ~75 phút

## 1. Đã sửa gì (VIỆC 0)

Sửa bug `folder_pattern`: 2 hàm tìm thư mục tập bằng glob cứng `ep{nn:02d}-*` — SAI cho lane satori
(tên thư mục `simbot2-{nn:02d}-<videoID>`) và vô tình khớp 8 thư mục nháp cũ `ep06-nenkin-kai`... `ep14-kaimono`.

**File: `profiles/profiles/satori-jp-obaa.json`** — thêm field:
```json
"slug_dir": "assets/satori_jp",
"folder_pattern": "simbot2-{nn:02d}-*",
```

**File: `profiles/profiles/toshi-densetsu-jp.json`** và **`irogatatarukioku.json`** — thêm field (giữ hành vi cũ):
```json
"slug_dir": "assets/toshi-densetsu-jp",
"folder_pattern": "ep{nn:02d}-*",
```

**File: `pipeline/ghi_cot_video.py`** — `thu_muc_tap()` (dòng ~71):
- Trước: `m = sorted(p for p in goc.glob(f"ep{stt:02d}-*") if p.is_dir())`
- Sau: đọc `mau = prof.get("folder_pattern") or "ep{nn:02d}-*"` rồi `goc.glob(mau.format(nn=stt))`

**File: `pipeline/quet_dong_can_anh.py`**:
- `thu_muc_lane()` (dòng ~92): đổi return từ `Path` → `(Path, profile_dict)` để trả kèm profile
- `slug_tu_dia()` (dòng ~114): dùng `goc, prof = thu_muc_lane(tab)` + đọc `folder_pattern` từ profile

**Kết quả 2 lệnh kiểm (dán nguyên văn output thật):**
```
STT 11 -> E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0
STT 6 -> E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM
```
Trước đây 2 lệnh này trả về `ep11-saikon` / `ep06-nenkin-kai` (sai). Không xoá 8 thư mục nháp cũ.

## 2. File mới đã tạo

- `pipeline/chay_buoc3.py` — 327 dòng, cấu trúc:
  - `chay_lenh()` — chạy lệnh `py -3.13` ngoài, 3 loại retry (A hạ tầng 10s→30s→90s · B cổng nội dung retry ngay · C không retry)
  - `doc_trang_tinh()` — đọc F/G/B qua `quet_dong_can_anh.svc()` (cơ chế đọc chung, không tự viết lại API)
  - `ghi_cot_h()` — ghi cột H (GHI CHÚ), nối ` | ` không đè, rào đọc tiêu đề cột thật (copy từ ghi_don_buoc3)
  - `viet_bao_cao()` — mỗi lần chạy 1 file mới `BAO_CAO_BUOC3/<tab>_dong<STT>_<yyyymmdd_HHMM>.txt`
  - `main()` — 8 bước A→H đúng thứ tự hồ sơ: A đọc trạng thái → B tìm thư mục (qua `ghi_cot_video.thu_muc_tap`) → C download-result → D đếm ảnh (RÀO CỨNG) → E sinh img_doan.txt (nếu chưa có) → F render_engine → G giao_hang → H ghi_cot_video

## 3. Kết quả 3 test bắt buộc (mục 5)

- **Test 1 (VIỆC 0, STT 6 + 11): PASS** — output thật:
  ```
  STT 11 -> E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0
  STT 6 -> E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM
  ```
- **Test 2 (--dong 4 --thu): PASS** — dừng đúng ở BƯỚC A, không chạy bước nào khác, KHÔNG ghi gì. Output thật, thời gian chạy ~1 giây:
  ```
  === Lopezzapa68 · STT 4 ===
    BƯỚC A: cột VIDEO đã có giá trị — tập đã giao xong
    (--thu) không ghi gì cả. Bỏ --thu để chạy thật.
  ```
- **Test 3 (--dong 999 --thu): PASS** — báo lỗi rõ ràng, không crash traceback trần. Output thật:
  ```
  === Lopezzapa68 · STT 999 ===
    BƯỚC A: cột STATUS-IMG chưa ghi 'Img done': '(trống)'
    (--thu) không ghi gì cả. Bỏ --thu để chạy thật.
  ```

## 4. Quyết định thiết kế đáng chú ý

1. **`--thu` hoàn toàn không ghi gì** (kể cả báo cáo + cột H): lượt test đầu em để nó ghi như chạy thật — phát hiện sai, đã sửa + khôi phục ô H5 về `ĐÃ ĐĂNG`. Nay --thu chỉ in ra trạng thái, exit 0.
2. **BƯỚC H dùng `retry_toi_da=1`**: `ghi_cot_video.py` có rào riêng (4 kiểu chặn) — retry vô ích, chỉ làm loãng log. Lỗi ở đây luôn là loại C (cần người xem), không thử cách khác để né rào (đúng hồ sơ 3.3).
3. **Phân biệt B/A cho render_engine bằng chuỗi dấu hiệu** (`DỪNG ở`, `B4Q`, `B5Q`, `B8Q`...): hồ sơ không cho cơ chế cụ thể, em chọn heuristic này — cổng nội dung thì retry ngay (render_engine tự resume), hạ tầng thì retry có nghỉ.
4. **`chay_lenh()` tự xoá `PYTHONPATH`** khỏi env tiến trình con: venv Hermes (numpy cp311) làm vỡ `py -3.13` — nếu không xoá, mọi lệnh con chết vì import numpy sai bản (đã dính thật trong phiên).
5. **BƯỚC E gọi thẳng `sinh_img_doan.py`** (sinh img_doan.txt bằng LLM) — tool đã có, tự bỏ qua nếu file tồn tại, đúng hồ sơ.
6. Báo cáo vận hành ghi vào `BAO_CAO_BUOC3/` (ngoài docs/) — đúng đường dẫn hồ sơ mục 4, tên file có mốc giờ nên không đè nhau.

## 5. Rủi ro / việc CHƯA làm

- **Chưa test đường chạy thật** (STT có ảnh đủ → render → giao hàng): hồ sơ cấm chạy thật STT 11/19, và chạy thật tốn ~1.500đ TTS + 30 phút. `--thu` đã xác nhận STT 6 sẵn sàng (Img done 133/133, VIDEO trống) nhưng chưa bấm nút thật.
- Chưa kiểm tra lần chạy thật của `sinh_img_doan.py` (gọi LLM tốn quota) — chỉ verify tool tồn tại + docstring khớp tham số `--slug`.
- `ghi_cot_h` dùng service account trực tiếp (không phải MCP gsheets như hồ sơ gợi ý): môi trường chạy `py -3.13` không có MCP, và rào chắn (đọc tiêu đề cột, nối không đè) đã copy nguyên từ ghi_don_buoc3/ghi_cot_video — hành vi an toàn tương đương.
- Retry loại B dùng chuỗi dấu hiệu — nếu render_engine đổi câu chữ thông báo, phân loại có thể lệch sang A (retry có nghỉ, vẫn không mất dữ liệu).

## 6. Câu hỏi cho người giao việc

- Có muốn em chạy thật 1 tập (VD STT 6 — đang Img done 133/133) để chứng nhận đường render→giao→ghi G end-to-end, hay để cron/script khác tự gọi khi tới lượt?
- Cột H cho lane satori: hồ sơ nói dùng MCP gsheets — em thay bằng service account (rào tương đương). Anh muốn giữ vậy hay nhờ Claude Code viết tool `ghi_don_buoc3.py` cho lane satori để đồng nhất với Lane A?

## PHẦN 2 — BẢN VÁ V2 (ngày 13/09/2026)

### Đã sửa

1. **VÁ 1 (spam báo cáo khi chưa sẵn sàng)** — nhánh `if not san_sang:` trong `main()` trước đây vẫn gọi `viet_bao_cao()` + `ghi_cot_h()` như lần chạy thật; nay chỉ log + return 0 (giống nhánh `--thu`). "Chưa tới lượt" (máy 2 chưa vẽ xong / tập đã giao) là trạng thái BÌNH THƯỜNG — cron định kỳ chạy nhiều dòng sẽ spam cột H + file báo cáo rỗng nếu ghi.
   - Trước:
   ```python
   if not san_sang:
       ...
       ket_qua = "DỪNG Ở BƯỚC A (trạng thái bình thường)"
       if a.thu:
           ... return 0
       ra = viet_bao_cao(...); ghi_cot_h(...)
       return 0
   ```
   - Sau:
   ```python
   if not san_sang:
       if tam_dung: ly_do = "cột GHI CHÚ (H) có dấu 'TẠM DỪNG' — ..."
       elif video:  ly_do = "cột VIDEO đã có giá trị — tập đã giao xong"
       else:        ly_do = "cột STATUS-IMG chưa ghi 'Img done': ..."
       log(f"=== {a.tab} · STT {a.dong} ===")
       log(f"  BƯỚC A: {ly_do}")
       if a.thu: log("  (--thu) không ghi gì cả...")
       return 0
   ```

2. **VÁ 2 (đọc "TẠM DỪNG" ở cột H)** — `doc_trang_tinh()` trả thêm cột H (`o(7)`); BƯỚC A kiểm `"TẠM DỪNG" in cot_h.upper()` → nếu có, coi KHÔNG sẵn sàng, xử lý cùng nhánh VÁ 1 (chỉ log, không ghi gì — tránh đè lên chính ghi chú giữ lại). Quy ước đã ghi vào docstring đầu file: ghi cụm bắt đầu bằng "TẠM DỪNG" vào cột H để giữ dòng thủ công.

3. **VÁ 3 (phân loại lỗi BƯỚC E)** — sau khi `chay_lenh(...)` trả `ok=False`, kiểm `"khong xep vua"`/`"không xếp vừa"` trong output → báo rõ đây là lỗi NỘI DUNG THẬT (kịch bản quá ngắn so với số ảnh, retry vô ích), kèm trích log; lỗi khác báo "thất bại sau N lần" như cũ. Cả hai đều dừng hẳn, khác nhau ở thông báo để người đọc khỏi thắc mắc "sao thử 3 lần vẫn vậy".

4. **VÁ 4 (có làm)** — BƯỚC C đổi `retry_toi_da=3` → `retry_toi_da=1`: `drive_handoff.py` đã tự retry bên trong, gọi từ `chay_buoc3.py` chỉ cần 1 lần, tránh phí thời gian khi drive lỗi thật.

### Test — dán NGUYÊN VĂN output thật

- **STT 11 --thu (trước vá)** — báo "sẵn sàng" (triệu chứng chưa đọc cột H):
  ```
  === Lopezzapa68 · STT 11 · 通帳にいくらあるか、息子に言うべきか——八十一の姉さんの答え ===
    trạng thái: STATUS-IMG='Img done - 121/121 ảnh (18:01 12/09)' · VIDEO trống
    thư mục tập: E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0
    (--thu) mọi thứ sẵn sàng — sẽ chạy: download-result → đếm → render → giao → ghi G.
  ```
- **STT 11 --thu (sau vá)**:
  ```
  === Lopezzapa68 · STT 11 ===
    BƯỚC A: cột GHI CHÚ (H) có dấu 'TẠM DỪNG' — người khác đang giữ dòng này: 'Deepseek trả lời Claude 22:56: vào kiểm tra câu trả lời tại E:\CLAUDE\YOUTUBE\h2...'
    (--thu) không ghi gì cả. Bỏ --thu để chạy thật.
  ```
- **STT 19 --thu (trước vá)** — báo "sẵn sàng":
  ```
  === Lopezzapa68 · STT 19 · 六十過ぎたら近づくな、四人の女——美容室のばあさんが暴く ===
    trạng thái: STATUS-IMG='Img done - 134/134 ảnh (19:00 12/09)' · VIDEO trống
    thư mục tập: E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-19-l0p1EnDcXYM
    (--thu) mọi thứ sẵn sàng — sẽ chạy: ...
  ```
- **STT 19 --thu (sau vá)**:
  ```
  === Lopezzapa68 · STT 19 ===
    BƯỚC A: cột GHI CHÚ (H) có dấu 'TẠM DỪNG' — người khác đang giữ dòng này: 'video ID: l0p1EnDcXYM | TẠM DỪNG — chờ sửa img_doan.txt (tool cũ), KHÔNG chạy bư...'
    (--thu) không ghi gì cả. Bỏ --thu để chạy thật.
  ```
- **STT 4 --thu, STT 999 --thu (sau vá)**:
  ```
  === Lopezzapa68 · STT 4 ===
    BƯỚC A: cột VIDEO đã có giá trị — tập đã giao xong
    (--thu) không ghi gì cả. Bỏ --thu để chạy thật.
  EXIT=0
  === Lopezzapa68 · STT 999 ===
    BƯỚC A: cột STATUS-IMG chưa ghi 'Img done': '(trống)'
    (--thu) không ghi gì cả. Bỏ --thu để chạy thật.
  EXIT=0
  ```
- **Số file trong BAO_CAO_BUOC3/ trước/sau**: 0 → 0 (KHÔNG đổi — VÁ 1 ăn)
- **Cột H dòng 4 (ô H5) trước/sau**: `'ĐÃ ĐĂNG'` → `'ĐÃ ĐĂNG'` (giống hệt — không bị thêm dòng mới)

### Câu hỏi (nếu có)

- Không có câu hỏi mới. Quy ước TẠM DỪNG đã hoạt động trên dữ liệu thật (dòng 11/19); khi nào hết giữ, bỏ cụm TẠM DỪNG khỏi cột H là dòng tự quay lại vòng chờ.
