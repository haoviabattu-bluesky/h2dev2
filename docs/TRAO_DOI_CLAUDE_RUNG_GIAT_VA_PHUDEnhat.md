# TRAO ĐỔI CLAUDE CODE — BỎ HIỆU ỨNG "RUNG GIẬT" + CHÁY PHỤ ĐỀ NHẬT TOÀN BỘ VIDEO

Ngày: 2026-09-21 · Người đo: Hermes (bước 3) · Trạng thái: **ĐÃ ĐO, CHƯA SỬA GÌ**

Anh chốt 2026-09-21:
> 1. HIỆN TẠI CÁC VIDEO ĐỀU CẦN BỎ KHÔNG DÙNG HIỆU ỨNG RUNG GIẬT GIẬT RẤT KHÓ XEM
> 2. CÀI PHỤ ĐỀ TIẾNG NHẬT CHO TOÀN BỘ VIDEO

File này ghi **số đo thật** để bên bước 1 quyết định sửa gì. Hermes KHÔNG sửa code/pipeline/data
của dự án (đúng quy tắc) — chỉ đo, viết spec, chờ lệnh.

---

## PHẦN A — NGUỒN "RUNG GIẬT" (đã truy tới gốc, có số đo)

### A.1. ẢNH AI (lane satori) — do `zoompan` làm tròn x,y về số nguyên

`pipeline/assemble.py::render_clip()` dựng filter:

```
sw, sh = W*(zoom+0.13), H*(zoom+0.13)          # 2400x1350 khi zoom=1.12
vf = fit_filter(...), zoompan=z='min(zoom+zstep,zoom)':d=frames:
     x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=WxH:fps=30
```

`x`/`y` của zoompan là **SỐ NGUYÊN** → không trượt đều mà **nhảy từng nấc**.

**Phép thử A/B ở đúng độ phân giải 1920×1080** (script `scratch_analysis/_ab_zoompan.py`, dùng
nguyên công thức trên, ảnh `assets/satori_jp/simbot2-01-vU5PWT2zLDs/img/001.png`, 8 giây):

| Chế độ | MAD | dxP90 | dyP90 | số lần dx đổi chiều | Kết luận |
|---|---|---|---|---|---|
| A) zoompan `zoom=1.12` (**HIỆN TẠI**) | 3.280 | 1.15 | 1.13 | **20** | dịch chuyển KHÔNG đều |
| B) zoompan `zoom=1.0` (đứng yên) | 0.000 | 0.00 | 0.00 | 0 | ổn định tuyệt đối |
| C) không zoompan (scale+crop) | 0.000 | 0.00 | 0.00 | 0 | ổn định tuyệt đối |

Chuỗi dịch ngang 24 khung đầu của chế độ A (đơn vị px, đo bằng phase correlation):

```
dx = [-0.16, -0.2, 1.06, -0.2, -0.75, 1.08, -0.18, -0.16, -0.23, 0.74, -0.2, -0.24, 1.1, ...]
dy = [-0.18, -0.25, -0.02, -0.24, 1.09, -0.02, -0.2, -0.19, -0.01, -0.22, 1.08, ...]
```

→ cứ ~4 khung có **1 khung nhảy +1px rồi trả về ~0** = **răng cưa**. Mắt người đọc đúng thành
"giật giật". Chế độ B/C thì `dx = dy = 0` mọi khung.

Mô phỏng trực tiếp công thức `x` của zoompan (`scratch_analysis/_chung_minh_giat.py`, 240 khung):

```
x 12 khung đầu        : [0, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7]
delta x 24 khung      : [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, ...]
số khung x DỊCH (delta!=0): 128/239  (53.6%)   <- hơn NỬA số khung bị nhảy 1px
zoom 1.0                  : 0/239   (0.0%)
```

**Đối chiếu quy ước đã duyệt:** `youtube-video-render` §"QUY ƯỚC HÌNH ẢNH MẶC ĐỊNH — hybrid stock + AI
(user duyệt 2026-09-15)" ghi rõ: *"Ảnh AI: **đứng yên hoàn toàn** — không zoom, không pan, không rung."*
⇒ **`zoom=1.12` của assemble.py ĐANG VI PHẠM quy ước đã duyệt.** Đây là lỗi, không phải lựa chọn thẩm mỹ.

**Đường gọi hiện tại (2 đường, cùng ra 1.12 — sửa phải sửa cả hai):**
1. `pipeline/render_engine.py` B8 gọi `assemble.py` **KHÔNG truyền `--zoom`** → rơi vào default 1.12.
2. `pipeline/make_video.py:2081` truyền `"--zoom", a.get("zoom", 1.12)` → lấy từ profile.
3. `profiles/profiles/satori-jp-obaa.json` khai `assemble.zoom = 1.12`.

### A.2. CLIP STOCK (lane toshi + tập hybrid satori) — rung là TÍNH CHẤT FOOTAGE, pipeline KHÔNG thêm

Phép đo trên 6 clip Pexels gốc của `assets/toshi-densetsu-jp/ep01-valentich/stock/`
(`scratch_analysis/_tach_nguon_toshi.py`) — so bản GỐC với bản ĐÃ QUA transform của pipeline
(scale+crop 1920×1080 rồi encode lại):

| clip | GỐC: dxP90 dyP90 dxFl dyFl | QUA PIPELINE: dxP90 dyP90 dxFl dyFl |
|---|---|---|
| pexels_10273125 | 4.95 7.06 **11 8** | 7.76 7.35 **8 8** |
| pexels_10302787 | 1.72 1.85 7 2 | 2.87 3.14 3 1 |
| pexels_10323686 | 0.97 1.14 0 0 | 0.33 0.52 0 0 |
| pexels_10323725 | 5.19 2.19 **22 0** | 4.46 2.04 **21 0** |
| pexels_10406880 | 0.16 0.17 1 0 | 0.21 0.16 6 0 |
| pexels_10419525 | 0.53 0.38 2 4 | 0.46 0.13 0 0 |
| **TỔNG** | **57** | **47** |

→ Pipeline **không thêm** rung (47 ≤ 57, thậm chí giảm). `stock_cut.py` đường video chỉ làm
`scale=W:H:force_original_aspect_ratio=increase,crop=W:H`, **không zoompan**.

⇒ Rung của lane toshi đến từ **footage Pexels cầm tay**. Muốn hết phải: (a) `vidstab` 2-pass, hoặc
(b) lọc kho ưu tiên clip tripod/tĩnh, hoặc (c) chấp nhận. **Không thể "tắt" bằng 1 dòng code.**

### A.3. Bảng chẩn đoán 19 video đã giao (phase correlation ở 1920×1080)

`scratch_analysis/_do_rung_goc.py` — đo 4 mốc/video, lấy cửa sổ đảo chiều mạnh nhất:

| video | madMed | dxP90 | dyP90 | dxFl | dyFl | verdict |
|---|---|---|---|---|---|---|
| Lope/ep01 | 2.701 | 1.14 | 0.41 | 1 | 12 | pan mượt |
| Lope/ep02 | 0.000 | 0.00 | 0.00 | 0 | 0 | ĐỨNG YÊN |
| Lope/ep03 | 0.939 | 0.33 | 0.40 | 1 | 3 | pan mượt |
| Lope/ep04 | 0.772 | 1.06 | 0.18 | 5 | 1 | pan mượt |
| Lope/ep05 | 1.795 | 1.77 | 2.01 | 4 | 6 | pan mượt |
| Lope/ep06 | 2.187 | 1.00 | 1.11 | 28 | 1 | pan mượt |
| Lope/ep07 | 0.632 | 0.37 | 0.19 | 1 | 1 | pan mượt |
| Lope/ep08 | 0.858 | 1.20 | 0.20 | 0 | 0 | pan mượt |
| Lope/ep09 | 2.532 | 13.14 | 7.79 | 1 | 1 | pan mượt |
| Lope/ep10 | 0.000 | 0.00 | 0.00 | 0 | 0 | ĐỨNG YÊN |
| Lope/ep11 | 1.982 | 1.03 | 0.26 | 3 | 1 | pan mượt |
| Lope/ep12 | 0.000 | 0.00 | 0.00 | 0 | 0 | ĐỨNG YÊN |
| Lope/ep19 | 0.368 | 0.29 | 0.16 | 0 | 0 | zoom, không dịch |
| Lope/ep21 | 3.507 | 1.04 | 0.14 | **30** | 0 | *** RUNG *** |
| shin/ep01 | 4.200 | 0.94 | 1.15 | **134** | 7 | *** RUNG *** |
| shin/ep02 | 8.806 | 1.13 | 1.12 | **103** | 17 | *** RUNG *** |
| shin/ep03 | 3.386 | 0.91 | 1.10 | **101** | 27 | *** RUNG *** |
| shin/ep04 | 4.336 | 0.78 | 1.10 | **116** | 17 | *** RUNG *** |
| shin/ep05 | 6.839 | 0.91 | 1.16 | **77** | 15 | *** RUNG *** |

**Đã loại trừ (đo, không suy diễn):**
- **KHÔNG phải lỗi fps/judder.** Cả 19 video là **CFR 30.000fps sạch** (`scratch_analysis/_check_fps.py`:
  `r_frame_rate=30.00`, đếm khung thật tại 300s và 900s đều ra đúng 300 khung/10s).
- **KHÔNG có hiệu ứng shake ngẫu nhiên trong code.** `grep -rn "shake|trembl|vibrat|jitter"`
  toàn repo (bỏ `.venv`) = 0 kết quả trong code dự án.
- **KHÔNG phải "pulse zoom"** của tool `FlowHandoff_local/shared/video_chuyen_canh_tool`
  (`--zoom-mode pulse` = ×1.053/8 khung/mỗi 4.07s). Đo chu kỳ MAD trên ep05/ep01/ep09
  (`scratch_analysis/_do_chuky.py`): không có chu kỳ ~4.07s; ep05 ra 57 đợt với khoảng cách
  0.2s (là cắt cảnh, không phải pulse).

### A.4. Việc bên bước 1 cần sửa (đề xuất, chờ anh chốt)

| # | Việc | File | Nội dung |
|---|---|---|---|
| A1 | Đưa `--zoom` về 0 cho ảnh AI | `pipeline/render_engine.py` B8 | truyền `--zoom` lấy từ `profile.assemble.zoom` (thay vì để assemble.py default 1.12) |
| A2 | Khai `zoom: 1.0` | `profiles/profiles/satori-jp-obaa.json` | `assemble.zoom` 1.12 → **1.0** (đúng quy ước đã duyệt 2026-09-15) |
| A3 | Cân nhắc mặc định | `pipeline/assemble.py` | `--zoom` default 1.12 → 1.0 (hoặc bắt buộc truyền tường minh) |
| A4 | Rung footage toshi | `pipeline/stock_cut.py` | chọn 1: thêm `vidstab` 2-pass cho slot video; chọn 2: lọc kho ưu tiên clip tĩnh; chọn 3: chấp nhận |

⚠️ **A1/A2/A3 là sửa code + profile của dự án → thuộc bước 1, Hermes KHÔNG tự sửa.**

---

## PHẦN B — PHỤ ĐỀ NHẬT "TOÀN BỘ VIDEO"

### B.1. Hiện trạng (đo trên đĩa + Sheet, 2026-09-21)

19 video đã giao ở `E:\CLAUDE\YOUTUBE\CHANEL\{Lopezzapa68,shinya_shiryoshitsu}\ep*\`.

| Đã cháy phụ đề Nhật? | Tập |
|---|---|
| ✅ CÓ | Lope ep09, ep10, ep12 (Hermes cháy 2026-09-21) |
| ❌ KHÔNG | **16 tập còn lại** |

Tất cả 19 tập **đều có `phude.srt` tiếng Nhật** trong thư mục giao (đã kiểm 5 dòng đầu: ví dụ
`秋の煮しめを詰めた、重箱を二段、風呂敷に` — lane satori; `1978年10月21日の夕方、メルボルン近郊の` — lane toshi).
Thiếu **duy nhất** ở `shinya_shiryoshitsu/ep06-mandela-effect` (chưa giao, không có `phude.srt`).

Cách cháy hiện dùng: `scratch_analysis/burn_phude_nhat.py`, style **lấy nguyên từ `assemble.py --burn-sub`**
(`FontName=Meiryo, FontSize=18, PrimaryColour=&H00FFFFFF, OutlineColour=&H00000000, BorderStyle=1,
Outline=2, Shadow=1, MarginV=45, Alignment=2`), `-c:a copy` nên **thời lượng không đổi**
(đo thật stt9/10/12: delta +0.000s).

### B.2. ⚠️ XUNG ĐỘT THỨ TỰ — ĐỌC TRƯỚC KHI LÀM

Cháy phụ đề là **ghi vĩnh viễn vào hình, KHÔNG GỠ ĐƯỢC**. Nếu cháy trước rồi sau đó mới dựng lại video
để bỏ rung giật (Phần A) thì **công cháy bị bỏ đi và phải cháy lại từ đầu**.

**Thứ tự đúng: (1) chốt xong chuyện rung giật → (2) cháy phụ đề lên bản hình CUỐI.**

### B.3. Tập nào còn sửa được (đọc Sheet, không đoán)

Cột `J` (Lopezzapa68) / `J` (shinya_shiryoshitsu) = tình trạng đăng:

| Tab | ĐÃ ĐĂNG / ĐÃ ĐẶT LỊCH → **KHÔNG thay được** | Chưa đăng → **thay được** |
|---|---|---|
| Lopezzapa68 | STT 1, 6, 7, 11 (Done) · 19, 21 (đã đặt lịch 17:30) | STT 2, 3, 4, 5, 8, 9, 10, 12 |
| shinya_shiryoshitsu | STT 1, 3 (thay title 21-9) · 2 (đã đặt lịch) | STT 4, 5 |

Video đã lên YouTube **không thể** thay file — chỉ còn đường đăng lại video mới (mất view/lịch sử).

**Phân loại đường dựng lại 14 tập satori** (đo trên đĩa — `stock_plan.tsv` là dấu hiệu hybrid,
nhưng ep01/ep21 cũng có clip stock dù thiếu file này):

| Đường | Tập | Cách dựng lại |
|---|---|---|
| HYBRID (có `stock_plan.tsv`) | 02, 03, 05, 08, 09, 10, 12 | chạy lại compositor `scratch_analysis/stock_hybrid_satori_stt*/compose_*.py` (đã tắt zoompan sẵn) |
| AI thuần | 04, 06, 07, 11, 19 | `assemble.py --zoom 1.0` |
| Có stock clip nhưng thiếu `stock_plan.tsv` | 01 (33 clip), 21 (21 clip) | cần bước 1 xác nhận đường dựng gốc trước khi dựng lại |

---

## PHẦN C — CẦN ANH CHỐT (Hermes dừng ở đây, không tự làm)

1. **Phạm vi cháy phụ đề:** chỉ 11 tập CHƯA đăng (cháy được, không phá gì) — hay cả 9 tập đã đăng
   (phải đăng lại video mới)?
2. **Phạm vi bỏ rung giật:** sửa code để các tập SAU sạch (nhanh, 0đ) — hay dựng lại cả các tập cũ
   đã giao (14 tập satori: `assemble.py --zoom 1.0 --burn-sub` cho tập thuần ảnh; tập hybrid phải
   chạy lại compositor; ~10–20 phút/tập)?
3. **Lane toshi (5 tập đều RUNG THẬT):** chấp nhận vì là footage cầm tay — hay muốn thử `vidstab`?

**Hermes làm ngay được khi anh chốt:** cháy phụ đề (script riêng trong `scratch_analysis/`, không
đụng code dự án) + dựng lại tập thuần ảnh bằng `assemble.py --zoom 1.0` (đây là bước 3, việc của Hermes).
**Phải bên bước 1 làm:** sửa `render_engine.py` / `assemble.py` / profile (A1–A3) + `stock_cut.py` (A4).

---

## GHI BÁO CÁO (nối vào CUỐI file, giữ nguyên nội dung phía trên)
