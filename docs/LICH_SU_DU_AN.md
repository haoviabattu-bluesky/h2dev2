# LỊCH SỬ DỰ ÁN (dọn từ CLAUDE.md 2026-09-29 — mục "LỘ TRÌNH" cũ)

> File LỊCH SỬ, không phải nguồn chân lý hiện tại — trạng thái THẬT của từng lane nằm ở bảng router
> đầu `CLAUDE.md` + `docs/BAT_DAU_LANE/<lane>.md` + `docs/channel_dna/`. Đọc file này chỉ khi cần
> biết dự án bắt đầu ra sao, không cần đọc để làm 1 tập mới.

- [x] Tạo Chrome profile + login khoá học (2026-09-06)
- [x] Bóc toàn bộ catalog + prompt + skill + sheet nguồn (2026-09-06)
- [x] **Chốt ngách đầu tiên: WORLD WAR II HISTORY (English)** (2026-09-07) — RPM cao, có prompt WW2
      sẵn. Sau này gác lại làm TEMPLATE, chuyển hẳn sang thị trường Nhật Bản (RPM cao hơn, đỡ cạnh
      tranh hơn — xem `pipeline/README.md`).
- [x] **Dựng pipeline WW2** (2026-09-07): 3 skill (`skills/youtube-script`, `youtube-image-prompts`,
      `youtube-thumbnail`) + tool `pipeline/` (fetch_script.py, gpti2_gen.py, gen_images.py, assemble.py).
- [x] **Mở LANE A: 都市伝説/vũ trụ/bí ẩn (JP)** (2026-09-10) — profile `toshi-densetsu-jp`, tool
      `stock_cut.py` + `qc_numbers.py`, SOP riêng `docs/SOP_TOSHI_DENSETSU_JP.md`.
- Từ đó dự án mở rộng dần thành nhiều lane song song (B → M), mỗi lane có profile + SOP riêng — xem
  bảng router ở đầu `CLAUDE.md` cho trạng thái hiện tại, đừng lần theo mục này.
