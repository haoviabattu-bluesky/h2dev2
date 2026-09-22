# PHƯƠNG ÁN LANE F (`teinengo-real`) — TỪ KỊCH BẢN ĐÃ KHOÁ → ẢNH + VIDEO Ở MÁY 2 — CHỜ ANH DUYỆT

Viết 2026-09-21 sau khi 3/3 kịch bản `Done` (ep01 luồng cũ, ep02–ep03 lean). **Chưa code gì, chưa tốn đồng nào.**
Khung: **máy 1 (tab này) chỉ làm phần cần NỘI DUNG (0đ) → đóng gói → máy 2 chạy ảnh + video.**
Giọng + tiêu đề/mô tả làm SAU CÙNG (anh chốt) → video ghép ở máy 2 chỉ chạy khi anh đã chốt giọng.
Nền tảng: copy nguyên khuôn Lane G (`docs/PHUONG_AN_LANE_G_BUOC2_3.md` C1–C6 đã code + test thật ep01) — Lane F chỉ khai field
profile + 4 việc code mới (mục 3), không sửa nhánh Lane G/E.

---

## 0. NĂM ĐIỂM — ✅ ANH DUYỆT THEO KHUYẾN NGHỊ (2026-09-21): Q1=(b) theo kênh mẫu · Q2=(A) 縦書き · Q3=10s/ảnh · Q4=(a) ep01 2 chặng · Q5=máy 2. Bắt đầu code C1→C8.

| # | Câu hỏi | Lựa chọn | Khuyến nghị của em | Vì sao |
|---|---|---|---|---|
| Q1 | **Kiểu vẽ** | (a) giữ suffix đã khai: seinen tối, màu xám-xanh "kịch tính tiền mất" · (b) **theo kênh mẫu**: anime nét sạch, tỉ lệ người thật, cel shading mềm, màu theo cảnh (nhà ấm vàng / đêm xanh lạnh) | **(b)** | Em vừa trích khung hình thật kênh mẫu (mục 1): KHÔNG tối kiểu seinen, là anime ấm thông thường. 70/30 = giữ cái khán giả đã quen mắt, không tự "sáng tạo" phần hình. (a) là em tự suy từ chữ "kịch tính" khi chưa xem hình. |
| Q2 | **Chữ trên hình** | (A) **縦書き hộp trắng/bóng thoại** như kênh mẫu (code mới `tate_text.py`, ~3h) · (B) phụ đề cháy đáy như Lane G (đã có, 0h) · (C) không cháy chữ | **(A)** | Đây là "chữ ký" của định dạng【漫画】kênh mẫu — mỗi câu hiện thành cột dọc trong hộp trắng, câu thoại「」thành bóng thoại. Bỏ nó là video trông khác hẳn dù ảnh giống. (B) là phương án lùi nếu anh không muốn tốn 3h code. |
| Q3 | **Mật độ ảnh** | 13s/ảnh (đã khai, ≈106 ảnh, ≈10.000đ/tập) · **10s/ảnh** (≈137 ảnh, ≈12.500đ/tập) · 9s = kênh mẫu đo thật (≈152 ảnh, ≈14.000đ) | **10s** | Kênh mẫu đo thật 9,0s/ảnh (mục 1). 10s gần mẫu, đỡ 15% tiền so với 9s; 13s thưa hơn mẫu 44% → video "đứng hình" lâu hơn hẳn thứ khán giả quen. |
| Q4 | **Tập đầu ep01 vẽ 2 chặng?** | (a) máy 2 vẽ master + **5 ảnh mẫu rồi DỪNG** → Syncthing đưa về → em xem 1 phút → máy 2 vẽ nốt · (b) cổng vision tự động, máy 2 chạy 1 mạch | **(a) cho ep01, (b) từ ep02** | Bài học Lane G ep01: lỗi KIỂU ảnh (trang manga nhiều ô) là lỗi hệ thống, nhìn 5 ảnh là biết, nhìn muộn = đốt 7.000đ. Cổng vision (C2) vẫn chạy ở (b) nhưng lần đầu của lane nên có mắt người. |
| Q5 | **Master REF-LOCK vẽ ở đâu** | máy 1 (~600đ, em xem bằng mắt) · **máy 2** (cùng lệnh B5, QC `qc_character` tự động, gộp vào chặng 5 mẫu ở Q4) | **máy 2** | Anh muốn máy 1 chỉ kịch bản; master + 5 mẫu về cùng 1 chuyến Syncthing nên em vẫn xem được ở Q4(a) mà không phải chạy gpti2 ở đây. |

Không cần chốt: ảnh gpti2 quality=low (ảnh mặt 110đ, cảnh 50đ, 3 key xoay), master gpti2 medium; REF-LOCK 2 mặt/tập (@REF=俺,
@REF2=người đối lập, @REF12=cảnh 2 người); tắt Ken Burns (zoom 1.0, khán giả 60+); neo ảnh theo câu (`sinh_neo` → `--anchors`);
B7 thumbnail + B9 listing **bỏ** (`publish.listing_external=true`, dự án khác lo — như Lane G).

---

## 1. PHÁT HIỆN MỚI TỪ KHUNG HÌNH THẬT KÊNH MẪU (2026-09-21, video XbwqD2SktC0 294k view — video anh đã dùng để clone giọng)

Trước đây DNA kênh chỉ suy từ transcript (không có ảnh). Em tải 2 đoạn (180–190s, 600–660s), trích khung → `docs/laneF_visual_ref/`.

| Thứ | Đo được | Hệ quả cho profile |
|---|---|---|
| Kiểu vẽ | Anime nét sạch, tỉ lệ người thật (không chibi, không "manga trang"), cel shading mềm, **màu theo cảnh**: phòng khách ấm vàng / xưởng xám / đêm phố xanh lạnh. Nhân vật nam 60+ tóc bạc, cardigan — khớp `character_sheet` đã khai. | `style_suffix` viết lại (Q1b); giữ câu cấm panel/grid của Lane G. |
| Chữ | **縦書き** (chữ dọc) trong **hộp trắng chữ nhật** cho lời kể, **bóng thoại ellipse** cho câu「」; 1–2 cột, ~8–15 chữ/cột, đặt vào phần trống của khung (trái hoặc phải, đối diện nhân vật); đổi chữ ~3–5s/lần (theo mệnh đề), nhanh hơn đổi ảnh. | Q2(A): `tate_text.py`; prompt ảnh bắt buộc chừa **1/3 khung bên TRÁI** thoáng (không mặt người) để chữ luôn đặt trái — cố định 1 bên cho đơn giản, kênh mẫu cũng không cố định. |
| Mật độ ảnh | 60s giữa video: 7 lần đổi ảnh, khoảng cách 3,5–11s, **trung vị 9,0s** | Q3. |
| Chuyển cảnh | Cắt thẳng, không thấy crossfade rõ ở mẫu 60s (đo thô bằng diff khung; muốn chính xác thì chạy `video-chuyen-canh` sau — việc bước 3, không chặn kế hoạch này) | Giữ `xfade 0.5` mặc định dự án (khán giả già, êm hơn cắt thẳng); đổi sau nếu anh muốn đo. |
| Phụ đề đáy | KHÔNG có (chữ nằm trong hộp dọc) | `burn_subs=false` giữ nguyên; `phude.srt` vẫn giao kèm để YouTube bật CC. |

---

## 2. PHÂN CHIA MÁY 1 / MÁY 2 (theo tiêu chí: cần hiểu NỘI DUNG → máy 1; chỉ chạy lệnh + tốn tiền → máy 2)

| # | Bước | Ai | Cần não? | Sản phẩm | Tiền |
|---|---|---|---|---|---|
| 1 | Kịch bản LOCK PASS (ep02/03 xong; ep01 cần khoá — mục 4.0) | Máy 1 | có | `script.txt` + `script.lock.json` | 0 (ep01 ~300đ Sol) |
| 2 | `characters.json`: 俺 + người đối lập của TẬP (tên/tuổi/giới/ngoại hình tiếng Anh, `ref_marker`) | Máy 1 — Claude Code đọc bản khoá, viết | có | `characters.json` | 0 |
| 3 | **B5W** Fable viết prompt THEO ĐOẠN + tag (MAIN/SECOND/BOTH/NONE) → `img_prompts.txt` + `img_doan.txt`; **B55** mapping; **B5P** prompt↔truyện (WARN) | Máy 1 (`claude -p` Fable, 0đ) | có | 2 file + `logs/B55_*`, `logs/B5P_*` | 0 |
| 4 | Đóng gói job → `FlowHandoff_local/jobs/<slug>/` + `_BANGIAO.txt` + ghi sheet **H** `cần ảnh` | Máy 1 (`dong_goi_may2.py`) | — | job folder | 0 |
| 5 | **B5.0 master** ×2 (gpti2 medium, nền xám, QC `qc_character` ≤2 lượt) + **B5S 5 ảnh mẫu** + cổng vision "1 cảnh, không panel, đúng kiểu" | **Máy 2** | QC vision | `_ref/001.png`, `_ref2/001.png`, `_sample/` | ~1.000đ |
| 5' | (ep01) DỪNG sau mẫu → Syncthing về → em xem → ghi `_sample/OK.txt` (hoặc sửa suffix + vẽ lại mẫu) | Máy 1 xem | có | — | 0 |
| 6 | **B5** vẽ hết (~137 ảnh, 8 luồng) + **B5Q** (10 mẫu vision, vẽ lại ảnh hỏng ≤2 lượt) | **Máy 2** | QC vision | `img/001..137.png`, `qc_images.json` | ~11.500đ |
| 7 | Báo về `results/laneF_render/<slug>/BAO_CAO_ANH.md` + ghi sheet **H** `ảnh xong (N)` | Máy 2 | — | | |
| — | **CHỜ ANH CHỐT GIỌNG** (làm sau cùng) | | | | |
| 8 | **B4** giọng (`--voice <id anh chốt>`) + B4Q (credit đủ trước, phủ ≥95%, mp3 ≥ SRT) + B4a phụ đề bám script | **Máy 2** | — | `voice.mp3`, `voice.srt` | ~1.100đ |
| 9 | **B8a** neo `sinh_neo.py` → `anchors.txt`; **B8** `assemble --anchors --tate` (zoom 1.0, xfade 0.5, chữ dọc) ; **B8Q** khớp lời | **Máy 2** | QC vision | `final.mp4` | ~200đ |
| 10 | **B10** nghiệm thu (chỉ video/phụ đề) + **B11** giao `final.mp4` · `phude.srt` · `review-vi.mp4` · `tomtat_vi.txt` → `results/video_render/teinengo-real/<slug>/` | Máy 2 | — | | |
| 11 | Em kiểm bản về (độ dài = audio, B8Q log, xem `review-vi.mp4` 5 mốc) → copy `CHANEL\teinengo-real\epNN-slug\` → ghi sheet **I** VIDEO | Máy 1 | đọc | sheet | 0 |

Máy 1 mỗi tập ≈ 10 phút, 0đ. Máy 2 chặng ảnh ≈ 25 phút; chặng video ≈ 25 phút.

---

## 3. VIỆC CODE (field-driven; lane không khai field → nhánh cũ y nguyên — hàng rào #2)

| # | Việc | File | Ước | Ghi chú |
|---|---|---|---|---|
| C1 | Profile F khai như Lane G: `image.prompts_by="fable_doan"`, `image.characters_from_bible=true`, `assemble.sync="anchors"`, `publish.listing_external=true`; đổi `seconds_per_image=10`, `workers=8`, `style_suffix` mới (Q1b + cấm panel + chừa 1/3 trái), thêm `image.sample_gate=5`, `assemble.tate={...}` | `profiles/profiles/teinengo-real.json` | 20' | Sửa `_workers_note` (ghi ima2 — sai, anh đã bỏ ima2; dùng gpti2 như G) |
| C2 | **Cổng B5S ảnh mẫu**: `image.sample_gate=N` → B5 vẽ trước N ảnh (chọn 2 @REF + 1 @REF2 + 2 cảnh đầu tiên) → `qc_visual` với schema thêm `single_scene` (không panel/grid/collage/nhiều góc nhìn) + `style_ok` → có ảnh rớt → **DỪNG**, ghi `logs/B5S_sample.json`, chép ảnh sang `_sample/`; cờ `--sample-only` (dừng sau mẫu, cho Q4a) và file `_sample/OK.txt` (lớp 3 duyệt → vẽ tiếp) | `make_video.b5_images`, `qc_visual.py` (thêm 1 field schema) | 1h | Lane G/E không khai → không đổi hành vi |
| C3 | **Bảo vệ script ở máy 2**: khi `script.lock.json` PASS, B4Q trượt → `SystemExit` DỪNG, **cấm** vào vòng "viết lại kịch bản" (vòng đó xoá `script.txt`) | `make_video.main` | 15' | Lỗi thật đã từng mất 3 file 2026-09-10; máy 2 không có Fable để viết lại nữa |
| C4 | **`tate_text.py` + `assemble --tate`** (Q2A): đọc `voice.srt` (đã reflow theo script) → mỗi cue 1 PNG RGBA 1920×1080: chữ dọc (Pillow `direction="ttb"`, feature `vert` để ー「」、。 xoay đúng; font Yu Gothic Bold/Yu Mincho), ≤14 chữ/cột, tối đa 2 cột phải→trái, **hộp trắng** bo góc nhẹ cho lời kể / **ellipse** cho cue bắt đầu bằng「; đặt cột ở 1/3 trái, canh giữa dọc; cue ngắn <0,6s gộp vào cue trước. Ghép: concat demuxer 1 input PNG-theo-thời-lượng → `overlay` vào chuỗi xfade (thêm 1 filter, vẫn 1 lần encode). `--tate-side left|right`, `--tate-font`, `--tate-size` | `pipeline/tate_text.py` (mới ~200 dòng), `assemble.py` (+~30 dòng), `make_video.b8_assemble` truyền cờ khi `assemble.tate` | 3h | Test offline 0đ: 3 ảnh + SRT giả 10 cue → mp4 20s, em xem khung. Rủi ro: Pillow bản máy 2 không có raqm → fallback xếp từng chữ thủ công (đã tính trong 3h). |
| C5 | `prompt_doan.py`: thêm luật bố cục vào lời dặn Fable: "left third of frame kept visually simple, no face there" (chỉ khi profile có `assemble.tate`) | `prompt_doan.py` | 15' | không đổi khuôn `đoạn\|TAG\|prompt` → `qc_img_doan` giữ nguyên |
| C6 | **`dong_goi_may2.py`**: (a) `--bundle` copy `pipeline/*.py` (bỏ `_bak_*`, test) + `profiles/{teinengo-real,teinengo-tanoshimi}.json` với `publish.upload_dir` **tương đối** `../../../results/video_render` + `requirements.txt` + `keys.py` → `shared/buoc2_3_tool/` (bundle hiện tại 09-17 chỉ đủ Lane A, thiếu 20+ file: `gate_common`, `sinh_neo`, `qc_img_doan`, `pace_audio`, `tts_chia`, `lean_script`…); (b) `--job teinengo-real <slug>` copy `script.txt`, `script.lock.json`, `characters.json`, `img_prompts.txt`, `img_doan.txt`, `state.json`, `logs/`, `title.txt` → `jobs/<slug>/` + `_BANGIAO.txt` (lệnh chặng A/B + tiền dự kiến) + ghi sheet H | `pipeline/dong_goi_may2.py` (mới) | 45' | Lane G cũng hưởng (bundle chung). Không đụng `drive_handoff.py` (luồng Flow cũ). |
| C7 | `FlowHandoff_local/shared/GIAO_VIEC_MAY2_LANE_F.md`: VIỆC 1 cài 1 lần (đã có Lane A → chỉ `pip install -r` lại) · VIỆC 2 mỗi tập chặng A (ảnh) · VIỆC 3 chặng B (giọng+video, chỉ khi `_BANGIAO.txt` có dòng `VOICE=`) · 6 luật cấm (không `--from` sớm hơn B4, không sửa script/profile, không `--force-qc`, báo kèm số đo…) | tài liệu | 45' | Khuôn theo `GIAO_VIEC_MAY2_BUOC2_3_VIEC2_MOI_TAP.md` |
| C8 | Hồi quy: Lane E ep01 `--only B8 --dry-run` lệnh không đổi; Lane G profile không khai `sample_gate`/`tate` → B5/B8 y cũ; `py -c "import make_video, tate_text"` trong bundle | — | 20' | |
| C9 | **ep01 F chưa có lock** (luồng cũ, D=`script-qc-done`): `gate_common.ghi_lock(d,"ESCALATE",reason="chuyển lean")` → `make_video --den B3G` → S2 dùng bản có sẵn, Sol chấm → PASS khoá sha (ESCALATE thì `viec_tay.txt` như ep02/03) | lệnh | 10' máy | ~300đ Sol |

**Tổng code ≈ 6h30** (C4 chiếm gần nửa — nếu anh chọn Q2(B) thì còn ≈ 3h30). Không sửa `script.txt` nào.

---

## 4. LỆNH CHẠY

### 4.0 Máy 1 — một lần cho ep01 (khoá kịch bản)
```
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common,pathlib;gate_common.ghi_lock(pathlib.Path('assets/teinengo-real/ep01-fuufu-nenkin-sa'),'ESCALATE',reason='chuyen sang lean de Sol cham ban da QC luong cu')"
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug ep01-fuufu-nenkin-sa --den B3G
```

### 4.1 Máy 1 — mỗi tập (0đ, ~10')
```
:: (tay) viết assets\teinengo-real\<slug>\characters.json từ bản khoá
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <slug> --only B5W      :: Fable prompt+đoạn, B55
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <slug> --only B5P      :: prompt↔truyện WARN
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <slug> --only B5 --dry-run   :: đếm ảnh + tiền, không vẽ
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job teinengo-real <slug>                          :: → jobs\<slug>\ + sheet H
```

### 4.2 Máy 2 — chặng A ảnh (theo `GIAO_VIEC_MAY2_LANE_F.md`)
```
cd FlowHandoff_local\shared\buoc2_3_tool\pipeline
xcopy /E /I ..\..\..\jobs\<slug> ..\assets\teinengo-real\<slug>
py make_video.py --profile teinengo-real --slug <slug> --only B5 --sample-only   :: ep01: master×2 + 5 mẫu rồi DỪNG
:: (ep01) chờ máy 1 ghi _sample\OK.txt · từ ep02 bỏ --sample-only (cổng vision tự chặn)
py make_video.py --profile teinengo-real --slug <slug> --only B5
py make_video.py --profile teinengo-real --slug <slug> --only B5Q
```
### 4.3 Máy 2 — chặng B (khi `_BANGIAO.txt` có `VOICE=<id>`): giọng → neo → ghép → QC → giao
```
py make_video.py --profile teinengo-real --slug <slug> --voice <id>
```
(B3 skip vì lock PASS; B5W/B5P/B5/B5Q skip vì đã có file+state; B7/B9 skip; chạy B4→B4Q→B8a→B8→B8Q→B10→B11.)
Đổi giọng sau khi xem: `--redo-voice --voice <id khác>` (đã có từ Lane G, giữ ảnh, ~15').

---

## 5. TIỀN & THỜI GIAN DỰ KIẾN 1 TẬP (~6.500 chữ ≈ 23')

| Khoản | 10s/ảnh (khuyến nghị) | 13s/ảnh |
|---|---|---|
| Ảnh: ~137 (mặt ≤50% → 65×110 + 72×50) / ~106 | 10.750đ | 8.300đ |
| Master 2 × medium + 5 mẫu (nằm trong loạt) | 600đ | 600đ |
| B5Q vẽ lại ~10% | 1.000đ | 800đ |
| Giọng ~8.200 credit | 1.100đ | 1.100đ |
| QC vision (B5S/B5Q/B8Q, ramclouds) | 300đ | 300đ |
| **Tổng/tập** | **≈ 13.800đ** | **≈ 11.100đ** |
| 3 tập đã có kịch bản | ≈ 41.000đ | ≈ 33.000đ |

Thời gian máy 2: chặng A ≈ 25' (master 2' · 137 ảnh/8 luồng ≈ 15' · B5Q 5'); chặng B ≈ 25' (B4 3' · B8 10' · B8Q 5' · B11 5').

---

## 6. CỔNG DỪNG (máy 2 tự dừng, không đẩy lên anh; em chỉ xử khi báo về)

| Cổng | Ngưỡng | Rớt → |
|---|---|---|
| lock | sha `script.txt` = lock PASS trước mọi bước tốn tiền (B4/B5W/B5) | DỪNG, báo máy 1 |
| QC master | tuổi ±12, đúng giới, 1 người, không panel | vẽ lại ≤2; vẫn rớt → máy 1 sửa `characters.json` |
| **B5S mẫu** (mới) | 5/5 `single_scene` + `style_ok` + khớp prompt | DỪNG, báo kèm `_sample/`; máy 1 sửa suffix → máy 2 vẽ lại mẫu |
| B55 / B5P | cơ học/STALE FAIL | máy 1 (đã chạy trước khi đóng gói) |
| B5Q | 10 mẫu: méo/chữ lạ/sai người/collage | vẽ lại ≤2 lượt (có sẵn) |
| B4Q | credit đủ, phủ ≥95%, mp3 ≥ SRT | DỪNG (C3: không viết lại) |
| sinh_neo | mọi ảnh ≥1s, neo là cue thật | DỪNG, báo (máy 1 sửa `img_doan.txt`) |
| B8Q | sync ≥3,5; độ dài = audio | `fix_weak_images` ≤2 lượt → vẫn rớt DỪNG |
| Lớp 3 (em) | `review-vi.mp4` mốc 0/5/10/15/20' + chữ dọc đọc được, không che mặt | ghi việc, không sửa tay |

---

## 7. RỦI RO THẬT
1. **Ảnh ra "trang manga nhiều ô"** (Lane G ep01, 15.800đ) → suffix đã có câu cấm + master 1 chân dung + cổng B5S 5 mẫu + ep01 có mắt người (Q4a).
2. **Chữ dọc xấu** (ー、「」 không xoay, kana nhỏ lệch) → Pillow raqm `vert`; test offline trước khi vào bundle; fallback xếp tay.
3. **Chữ đè lên mặt** → prompt chừa 1/3 trái + B5Q có `face_clear`; nếu vẫn đè, `--tate-side right` cho tập đó.
4. **Bundle máy 2 thiếu file** → C6 copy cả `pipeline/*.py` + smoke test `import` trước khi giao; C8.
5. **Máy 2 lỡ `--from B3`/`--from B4` xoá script** → C3 + luật cấm trong GIAO_VIEC (như Lane A).
6. **gpti2 402/429** → 3 key xoay; hết tiền DỪNG báo (không tự đổi ima2 — anh đã bỏ).
7. **Voice chưa chốt** → chặng B không chạy được; ảnh vẫn xong trước, không chặn nhau.

---

## 8. THỨ TỰ LÀM SAU KHI ANH DUYỆT
1. ✅ C1 profile → C3 → C2 → C5 → C4 (test offline, ảnh chữ dọc verify đúng) → C6 → C8 → C7 — xong 2026-09-21.
2. ✅ C9 khoá ep01 · `characters.json` 3 tập · B5W/B5P 3 tập · đóng gói cả 3 job → sheet H `cần ảnh` — xong 2026-09-21.
3. Báo anh: đường dẫn 3 job + `GIAO_VIEC_MAY2_LANE_F.md` để anh bàn giao máy 2 (em không tự giao — ⛔ CLAUDE.md).
4. Sau này anh chốt giọng → em thêm dòng `VOICE=` vào `_BANGIAO.txt` 3 tập → máy 2 chạy chặng B.

## 9. KẾT QUẢ THẬT (2026-09-21) — 3/3 tập đã đóng gói

| Tập | Lock sha | Ảnh (B5W) | B5P | Job |
|---|---|---|---|---|
| ep01-fuufu-nenkin-sa | ac2ed53246 (7.238 chữ ≈25,5') | 153 (MAIN45·MENTOR11·BOTH7·NONE90) | WARN 5 (tuổi 60 vẽ theo master 65 — giới hạn REF-LOCK, không sửa) | `jobs\ep01-fuufu-nenkin-sa\` ≈12.030đ |
| ep02-saikoyou-hanbun | 143aaca37b (6.533 chữ ≈23,0', đã Done từ 20/09) | 138 (MAIN30·MENTOR9·BOTH5·NONE94) | WARN 6 mỹ thuật nhẹ, không sửa | `jobs\ep02-saikoyou-hanbun\` ≈10.140đ |
| ep03-kuriage-koukai | e64a16a4e5 (6.490 chữ ≈22,9', đã Done từ 20/09) | 137 (MAIN39·MENTOR8·BOTH3·NONE87) | WARN 4 + 1 lỗi rõ (giới tính nhân viên quầy — đã sửa tại chỗ) | `jobs\ep03-kuriage-koukai\` ≈10.450đ |

Cả 3 chạy B5W bằng `claude-opus-5` (Fable hết quota account-wide giữa chừng — đổi lại khi quota về).
**2 lỗi hạ tầng phát hiện+vá khi test thật** (ảnh hưởng MỌI lane `flow=lean`, không riêng Lane F):
1. `lean_script.kanji_to_int()` tính sai số Hán tự dạng "AA十B万…" (vd 二十一万二千 → ra 12.020 thay vì
   212.000) → gây ESCALATE oan ở cổng "SỐ HỌC". Đã vá + verify 7 test case. **Chưa re-check các tập lean
   đã PASS trước đó của Lane F/G** — cần hỏi anh có muốn chạy lại kiểm tra không.
2. `prompt_doan.py` B5W lượt hỏng không lưu bản thô model trả về → đã thêm `logs/B5W_raw_attemptN.txt`.

Bundle máy 2 đã `--bundle` lại lần cuối (102 file pipeline + 2 profile) sau mọi sửa trên.
