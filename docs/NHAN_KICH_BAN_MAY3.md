# NHẬN KỊCH BẢN MÁY 3 → LÀM TIẾP (file hướng dẫn DUY NHẤT cho máy 1 sau khi anh soát xong)
> Anh chốt 2026-09-30, sửa 2026-10-02. Áp cho mọi lane chuẩn (F G J K L M N O; không áp satori).
> Máy 3 (anh) soát THỦ CÔNG → khi anh báo **"anh sửa xong kịch bản <lane> <tập>"** hoặc cột D = `Đã sửa kịch bản`,
> tab máy 1 đọc ĐÚNG file này rồi làm từ §1 tới hết. KHÔNG đọc lại SOP/CHANNEL_DNA/profile từ đầu; việc riêng lane
> (cast, nhân vật, Grok) chỉ tra mục "⚡ ĐỌC NHANH" + mục LỆNH CHẠY của SOP lane (bảng ở `E:\CLAUDE\YOUTUBE\h2dev\CLAUDE.md`).
> 02/10: BỎ file hướng dẫn riêng từng tập (`HUONG_DAN_NHAN_MAY3.md`) + ghi cột K ở mốc giao máy 3 — chỉ còn file này.
> 02/10: thêm mốc **ANH DUYỆT CLIP HOOK** (có giọng + phụ đề Việt) trước khi giao máy 2 — `dong_goi_may2` chặn cứng nếu chưa duyệt.
> Tiêu đề/mô tả/thumbnail TẮT toàn dự án (01/10) — KHÔNG gọi TITLE.

## 0. Luồng tổng (để biết mình đang ở đâu)
Cột D/K do tool TỰ GHI (03/10, bảng đủ: `E:\CLAUDE\YOUTUBE\h2dev\docs\TRANG_THAI_COT_D_K.md`).
| Mốc | Ai | Cột D sau mốc |
|---|---|---|
| Chặng 1 bắt đầu: `make_video.py --den B3G` | máy 1 | `Đang chạy kịch bản bước 1` |
| Chặng 1: hồ sơ → `make_video.py --den B3G` (hook Fable 2 PA → S2 Fable 5.1 → đo → vá → LOCK) → máy tự chép `script.txt` sang `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\<tab>\<slug>\` rồi DỪNG | máy 1 | `Chờ kiểm tra kịch bản` (+ dòng 2 = đường dẫn) · **K = thư mục anh sửa + lệnh `--nhan` + file này** |
| Anh sửa thẳng `jobs\<tab>\<slug>\script.txt` (hook = đoạn đầu; không sửa cũng được) | anh | `Đã sửa kịch bản` |
| **§1 file này** `review_may3.py --nhan` xong | máy 1 | `Đang làm Hook` |
| **§2–§5 file này:** cast → prompt ảnh → hình + clip hook → dựng CLIP HOOK XEM THỬ → DỪNG | máy 1 | `Chờ duyệt hook` (+ dòng 2 = đường dẫn video) |
| Anh xem clip hook: được → đổi D; chưa được → nói chỗ sửa | anh | `Đã duyệt hook` |
| **§6 file này:** nhận duyệt → giao máy 2 | máy 1 | `Đã giao máy 2` + H = `cần ảnh (N ảnh, ~Xđ)` · **K = câu anh dán cho máy 2** |

Tìm tập đang chờ ở lane:
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --trang-thai --profile <lane>
```
In các dòng có D = `Chờ kiểm tra kịch bản` / `Đã sửa kịch bản` / `Chờ duyệt hook` / `Đã duyệt hook`. Slug ở cột C.
Thư mục tập = `E:\CLAUDE\YOUTUBE\h2dev\<slug_dir của profile>\<slug>\` (vd `E:\CLAUDE\YOUTUBE\h2dev\assets\M-teinengo-anaba\ep05-...\`).

## 1. Nhận bản anh sửa (0 LLM, không sửa 1 chữ)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --nhan --profile <lane> --slug <slug>
```
Tool tự: kiểm D = `Đã sửa kịch bản` (chạy lại khi D = `Đang làm Hook` cũng được) · lưu bản cũ `script.truoc_may3_<ts>.txt` · chép bản anh vào thư mục tập · đo chỉ-đọc
(`NHAN_MAY3.md`) · hook: đầu bài đổi → lấy đúng số đoạn đầu làm hook mới + **khoá lại** `hook\hook_locked.txt` · ký lại lock PASS
· ghi D = `Đang làm Hook`.
- **CHẶN** (ngắn <70% ngân sách, hoặc số liệu ngoài `series_ctx.txt`) → báo anh 1 dòng lý do, **không sửa hộ**.
- **D chưa đổi** → nhắc anh. Chỉ khi anh bảo "cứ nhận" mới thêm `--force`.
- **Kiểm ranh giới hook** (hook dài ≈ hook video gốc — luật viết hook 17/10: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`; KHÔNG chấm lại hook anh sửa theo luật cũ): mở `<thư mục tập>\hook\hook_locked.txt`, so với đoạn đầu `script.txt`. Lệch ranh giới → khoá lại tay đúng đoạn:
  ```bat
  py -3.13 -X utf8 -c "import sys;sys.path.insert(0,r'E:\CLAUDE\YOUTUBE\h2dev\pipeline');import hook_stage;from pathlib import Path;d=Path(r'<thư mục tập>');t=Path(r'<file chứa đúng đoạn hook>').read_text(encoding='utf-8').strip();o=hook_stage.doc_lock(d) or {};print(hook_stage.khoa(d,t,mode=o.get('mode','upstream'),extra={'source':'may3_tay'}))"
  ```
- Tuyệt đối không sửa `script.txt` (sha lệch = mọi bước sau dừng).
- ⭐ **Học bản anh sửa** (04/10, chỉ đọc, 0 LLM) — làm ngay sau khi nhận, trước §2:
  `py -3.13 -X utf8 C:\Users\admin\.claude\skills\youtube-kich-ban\hoc_ban_sua.py <thư mục tập> --out <thư mục tập>\HOC_BAN_SUA.md`
  → rút luật, ghi `C:\Users\admin\.claude\skills\youtube-kich-ban\BAI_HOC.md` (skill `youtube-kich-ban` §5), báo anh 3–5 dòng.

## 2. Cast + giọng
`characters.json` theo mục nhân vật của SOP lane (vai chính khoá mặt xuyên tập + vai phụ; MỌI vai có lời phải khai `age` + `gender`, vai già tách riêng khỏi vai nhóm) → gán vai từng câu (`vai.txt`). ⛔ (22/10) Giọng vai KHÔNG tự tìm, KHÔNG hỏi anh duyệt: `gan_vai.py` tự gọi `pipeline\kho_giong.py` lấy giọng theo KHUNG TUỔI từ kho chung `E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.json` (cụ bà ≥65 = Naoko + old-mild + 0.85…) — xem `docs/KHO_GIONG_THEO_TUOI.md`:
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\gan_vai.py --profile <lane> --slug <thư mục tập>
```

## 3. Prompt ảnh thân bài (CHỈ `--only`; cấm `--from`/`--den` B4/B5 ở máy 1)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile <lane> --slug <slug> --only B5W
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile <lane> --slug <slug> --only B5P
```

### 3b. Số liệu động — ĐÃ CHUYỂN SANG MÁY 2 (anh chốt 2026-10-07) · máy 1 BỎ QUA
Máy 1 KHÔNG chạy `so_lieu_dong.py`, KHÔNG duyệt `so_lieu_dong.json`; `dong_goi_may2 --job` không chặn nữa, chỉ tự ghi mục
SỐ LIỆU ĐỘNG vào `_BANGIAO.txt` khi lane bật `mg.so_lieu_dong` (hiện: Lane L). Máy 2 tự sinh + lọc theo 6 luật cố định
(`E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\motion_graphics\HUONG_DAN_MAY2.md` §2 bước 0) để mọi tập cùng một đường QC.
Việc của máy 1 chỉ còn: `SỐ ĐƯỢC PHÉP` trong `series_ctx.txt` phải đủ + đúng (máy 2 chỉ lọc trong danh sách đó).

## 4. Hình + clip hook (máy 1 làm trọn, theo hook ANH SỬA)
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_storyboard.py --profile <lane> --slug <slug> --force
```
→ ảnh hook (16/10: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\anh_hook.py <thư mục tập>\hook` chạy nền — Google Flow Ultra cổng 9350, các tập KHÔNG dùng profile song song, cổng bận → 9router → gpti2; `docs\QUY_TRINH_ANH_HOOK_GOOGLE_FLOW.md`) → QC ảnh (`qc_hook_clip.py --hook <thư mục tập>\hook --anh N`;
mặt + cảm xúc + tuổi đúng `docs\QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md`) → ⛔ **CHÈN CHỮ VÀO ẢNH** đạo cụ có chữ là điểm nhấn
(giấy tờ/biển/màn hình — anh chốt 10/10, `docs\QUY_TAC_CHU_TREN_DAO_CU_HOOK.md`: `pipeline\chu_dao_cu.py --nhap` → `--tim NNN` →
khai `hook\chu_tren_vat.json` → chạy, soi `hook\chu\NNN_soi.jpg`; ảnh không cần chữ ghi `bo_qua`; tool clip chặn nếu chưa xong) → clip **Google Vids** (16/10 phương án CHÍNH: `tools\hook_lane_g\vids_hook.py <hook TUYỆT ĐỐI> --tabs 5` — ảnh→video, số giây khớp lời, tự che logo bằng avatar kênh, **chạy nền**; `docs\QUY_TRINH_CLIP_HOOK_GOOGLE_VIDS.md`; clip Vids hỏng hẳn → dự phòng Grok `tools\hook_lane_g\grok_da_luong.py <hook TUYỆT ĐỐI>`)
→ QC clip (`qc_hook_clip.py --clip N`) → **chỉ nhạc nền** `hook\sfx\99_nhac_*.mp3`, cấm SFX đồ vật, kiểm bối cảnh (gọi điện ≠ gặp mặt)
theo `docs\QUY_TAC_HOOK_DAI_VA_NHAC_NEN.md` → HOOK_TAP.md:
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_tap_md.py --slug <thư mục tập> --profile <lane>
```
Ảnh/clip hook làm theo hook CŨ (trước khi anh sửa) → phải làm lại; xoá tay thì hỏi anh.
Chi tiết lệnh Grok/master vai phụ: SOP lane mục hook (mẫu `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_M.md` §2 mục F).

## 5. ⛔ CLIP HOOK XEM THỬ (giọng + phụ đề Việt) → DỪNG chờ anh duyệt
1. Viết `<thư mục tập>\hook\phu_de_vi.json` = dịch Việt TỪNG CÂU hook, khoá theo số câu trong `vai.txt`/`hook_timeline.json`
   (`{"1": "câu dịch", "2": "..."}`; câu thoại để trong ngoặc kép “…”). Dịch sát nghĩa, đủ mọi câu (thiếu → hiện "(chưa dịch)").
2. Dựng clip (clip Grok + giọng ai33 theo vai + nhạc nền + phụ đề Nhật/Việt; giọng cache trong `_xem_thu_giong\`, chạy lại không tốn credit):
   ```bat
   py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\hook_lane_g\xem_thu_hook_giong.py --profile <lane> --hook <thư mục tập>\hook
   ```
   → `<thư mục tập>\XEM_THU_hook_giong_phude_VI.mp4` (nằm ngoài `hook\` nên không bị gửi nhầm sang máy 2).
   Nghỉ giữa câu theo luật chung với giọng thân máy 2 (`cau_vai.khe_nghi`: câu ≥0,5s · dòng trống ≥1,1s · mảnh câu 0,2s);
   chỗ đổi cảnh/thời gian trong hook (hồi tưởng, 翌週 (tuần sau)…) → khai `"nghi_doan_sau": [số câu…]` trong `hook_timeline.json` (06/10, Lane O ep04).
   Cảnh KHÔNG LỜI (motion ngày/địa điểm) = shot không `cau`, khai `"lang_s": 3.0`; giữ mặt sau câu cho thẻ tên = `"nghi_sau_s": 2.5`
   trên shot có lời (12/10, Lane L ep15 `hook\_mk_hook.py`). Máy 2 tự chèn lặng vào giọng thân (`cau_vai.lang_hook`) → phải `--bundle`.
   Chữ motion bối cảnh cháy thẳng vào clip bằng HyperFrames (`hook\mg_motion\cNN\`, clip gốc cất `hook\clip\_goc_mg\`).
   Tự xem trước: trích 3–4 khung (`qc_visual._frame`) soát phụ đề không tràn, câu khớp cảnh; shot dài hơn clip được GIÃN CHẬM như máy 2 (10/10),
   log báo shot "giãn >1,6 lần" → tách cảnh theo ranh giới câu (thêm ảnh/clip số mới, không đổi tên file cũ — mẫu ep05 Lane O `hook\_mk_hook.py`).
   (Chữ trên đạo cụ đã chèn vào ẢNH ở §4 trước Grok; `duyet_hook --gui` chặn nếu clip sinh từ ảnh chưa có chữ.)
   ⛔ TRƯỚC khi dựng: THẺ TÊN ĐỘNG cho nhân vật chính (anh chốt 10/10, mọi lane — `docs\QUY_TAC_THE_TEN_NHAN_VAT_HOOK.md`;
   sửa 14/10: lời hook ĐƯỢC đọc tên-tuổi song song thẻ). Kiểu thẻ theo lane (`script.hook.the_ten`); `duyet_hook --gui` chặn nếu thiếu:
   ```bat
   py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <slug> --nhap
   py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <slug>
   ```
   (giữa 2 lệnh sửa `hook\the_ten.json`: Họ␣Tên, kana, nghề, chip, `bo_qua`). Clip xem thử + `ghep_hook_noi_truoc.py` máy 2 tự chồng
   thẻ; `dong_goi_may2` gửi kèm `hook\the_ten\`. Soi khung: thẻ che mặt → `"vi_tri": "tren_phai"` cho thẻ đó, render lại.
3. Gửi anh duyệt (kiểm video mới hơn hook/clip/phụ đề, ghi `duyet_hook.json` + D = `Chờ duyệt hook` + dòng 2 = đường dẫn video):
   ```bat
   py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\duyet_hook.py --gui --profile <lane> --slug <slug>
   ```
4. Báo anh ĐƯỜNG DẪN ĐẦY ĐỦ của video rồi **DỪNG LƯỢT**. Không giao máy 2.

Anh yêu cầu sửa → sửa đúng chỗ (prompt clip / ảnh / phụ đề / nhạc; sửa LỜI hook thì phải khoá lại hook như §1) → chạy lại bước 2–3.

## 6. Anh duyệt → giao máy 2
Anh báo **"anh duyệt hook <lane> <tập>"** hoặc D = `Đã duyệt hook`:
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\duyet_hook.py --nhan --profile <lane> --slug <slug>
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --job <lane> <slug>
```
- ⭐ (21/10) Trên MÁY 2 (`MAY.local`=2, làm A→Z): `--job` KHÔNG đóng gói sang `jobs\` — viết `_BANGIAO.txt` ngay trong thư mục tập,
  D = `Chờ dựng video`, rồi làm tiếp chặng dựng theo `E:\CLAUDE\YOUTUBE\h2dev\docs\MAY2_LAM_A_DEN_Z.md` §4.
- Anh duyệt ngay trong chat mà chưa đổi ô D → `--nhan ... --force`.
- `--nhan` chặn nếu hook/clip/phụ đề/vai đổi SAU khi gửi anh xem → dựng lại §5.
- `dong_goi_may2 --job` tự: đóng gói `jobs\<tab>\<slug>\` · ghi D = `Đã giao máy 2` + H = `cần ảnh (N ảnh, ~Xđ)` ·
  đè cột K DÒNG TẬP NÀY = câu anh dán cho máy 2 (`_BANGIAO.txt` + lệnh chặng 1) · viết
  `<slug_dir>\HUONG_DAN_TAP_TIEP_THEO.md` + đè cột K dòng tập kế. Em đọc lại `_BANGIAO.txt` tự kiểm đúng thư mục.
- Đổi code/profile dùng ở máy 2 → thêm `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\dong_goi_may2.py --bundle --profile-list <lane>`.
- Bổ sung bài học tập này cho tab tập kế: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\huong_dan_tab_moi.py --loai tiep --profile <lane> --slug <slug> --ghi-chu-file <file .md>`.

## 7. Bẫy
- Cổng `review_may3.cong()` chặn B4/B5W/dong_goi khi chưa `received` hoặc script đổi sau khi nhận → chạy lại `--nhan`, không đi cửa sau.
- Cổng `duyet_hook.cong()` chặn `dong_goi_may2 --job` khi chưa duyệt hook. Job đã giao trước 02/10 (có `_BANGIAO.txt`) = đóng gói SỬA → chỉ cảnh báo.
- Grok / ảnh / TTS chạy bằng `run_in_background`, báo giờ dự kiến rồi dừng lượt; không ngồi `tail` log.
- Giọng trong clip xem thử là bản DUYỆT; máy 2 vẫn lồng giọng chính thức (B4) như cũ.
- Lane có `soat:"gptweb"` (chỉ khi anh bảo) mới dùng `soat_kb_gptweb.py`. Mặc định là `soat:"may3"`.
