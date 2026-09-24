# PHƯƠNG ÁN LANE G — TỪ KỊCH BẢN ĐÃ KHOÁ → VIDEO HOÀN CHỈNH (bước 2+3), CHỜ ANH DUYỆT

Viết 2026-09-20 tối, sau khi 10/10 kịch bản `Done`. Chưa chạy gì. Anh duyệt → em code + chạy test ep01 tại máy 1
→ đóng gói cho máy 2 (làm sau cùng, theo lời anh).

---

## 0. TRẢ LỜI 3 ĐIỂM ANH NÊU

**1. Giọng có để cuối được không?** — Gần như được, với 1 ràng buộc kỹ thuật thật:
- Ảnh phải **neo theo câu đang đọc** (mỗi ảnh hiện đúng lúc câu của nó vang lên — cách satori làm bằng
  `img_doan.txt` → `sinh_neo.py` → `anchors.txt`). Việc *neo* cần file giọng + SRT. Còn *nội dung* ảnh (ảnh nào thuộc
  đoạn nào) thì **không phụ thuộc giọng** — đó là chuyện kịch bản.
- Vì vậy thứ tự đúng là: **prompt ảnh + gán đoạn → vẽ ảnh → GIỌNG → neo → ghép**. Giọng đứng ngay trước ghép = "bước
  cuối" đúng như anh nghĩ. Đổi giọng sau khi xem video chỉ tốn chạy lại `B4 → neo → B8` (~15' máy, 0 lượt LLM, ảnh giữ
  nguyên).
- Giọng chạy ở **máy 2** (bundle đã có `tts.py` + key), không phải máy 1. Giọng mặc định = `clone_2658912` anh đã duyệt.

**2. Tiêu đề / mô tả / thumbnail** — dự án khác lo → em **bỏ B7 (thumbnail) và B9 (listting)**; B10/B11 hiện đòi có
thumbnail + `TIEU_DE_MO_TA.txt` mới cho giao → thêm 1 field profile `publish.listing_external=true` để B10 chỉ kiểm
video/phụ đề, B11 giao 3 file `final.mp4` · `phude.srt` · `review-vi.mp4` (không đòi thumbnail/listting).

**3. Ảnh + video ở máy 2, nhưng test trọn 1 tập ở máy 1 trước** — đúng tiền lệ Lane E ep01 (anh cho ngoại lệ 1 lần
"chạy hết để nắm quy trình rồi mới soạn hồ sơ giao"). Rào `CLAUDE.md` "Claude chỉ bước 1" vẫn nguyên cho tập 2–10
và mọi lane khác; ep01 Lane G là ngoại lệ có phép, em ghi rõ vào SOP.

---

## 1. PHÂN CHIA MÁY 1 / MÁY 2 (đề xuất — em chọn theo tiêu chí "cái gì cần NỘI DUNG thì máy 1, cái gì chỉ chạy lệnh thì máy 2")

| # | Bước | Ai | Cần não? | Sản phẩm |
|---|---|---|---|---|
| 1 | Kịch bản LOCK PASS (đã xong 10/10) | Máy 1 (Fable+Sol+Claude Code) | có | `script.txt` + `script.lock.json` |
| 2 | **Hồ sơ nhân vật** `characters.json` (俺 + mentor của TẬP: tên/tuổi/giới/ngoại hình tiếng Anh) | Máy 1 — Claude Code đọc script viết | có | `characters.json` |
| 3 | **Master REF-LOCK** 2 ảnh (gpti2 medium, manga style) + QC tuổi/giới (`qc_character.py`) | Máy 1 (lệnh, ~600đ) | QC vision | `_ref/001.png`, `_ref2/001.png` |
| 4 | **Prompt ảnh + gán đoạn** — Fable viết 1 lượt: mỗi dòng `đoạn|tag|prompt` (tag MAIN/MENTOR/BOTH/NONE/CHILD) → `img_prompts.txt` (@REF/@REF2/@REF12/@GROK) + `img_doan.txt` | Máy 1 (Fable 0đ) | có | 2 file + fingerprint |
| 5 | Cổng B5P (prompt↔cốt truyện) + B55 (mapping ảnh↔đoạn, chống chia đều) | Máy 1 (máy) | — | `logs/B5P_*.json`, `logs/B55_*.json` |
| 6 | Gói job Syncthing `FlowHandoff_local/jobs/<slug>/` + `_BANGIAO.txt` + ghi sheet cột H | Máy 1 | — | job folder |
| 7 | **B4 giọng** `clone_2658912` + B4Q (phủ kịch bản + soi sóng âm) | **Máy 2** | — | `voice.mp3`, `voice.srt` |
| 8 | **B5 vẽ ảnh** gpti2 (~86 ảnh: @REF/@REF2 110đ, cảnh vật 50đ) + B5Q (QC mẫu 10 ảnh, vẽ lại ảnh hỏng) | **Máy 2** | QC vision | `img/001..086.png` |
| 9 | **Neo** `sinh_neo.py` (img_doan + SRT → `anchors.txt`, kiểm mỗi ảnh ≥1s) | **Máy 2** | — | `anchors.txt` |
| 10 | **B8 ghép** `assemble.py --anchors` (zoom 1.0, xfade 0.5, không cháy phụ đề) + B8Q (khớp lời) | **Máy 2** | QC vision | `final.mp4` |
| 11 | B10 (chỉ kiểm video/phụ đề) + B11 giao `final.mp4`·`phude.srt`·`review-vi.mp4` → `results/video_render/teinengo-tanoshimi/<slug>/` (⛔ chỗ trả hàng DUY NHẤT mọi lane, chốt 24/09 — `docs\QUY_TRINH_GIAO_VIEC_MAY2.md` §6) | **Máy 2** | — | Syncthing đưa về máy 1 |
| 12 | Em kiểm bản về (độ dài, B8Q log) → copy `CHANEL\teinengo-tanoshimi\epNN-slug\` → ghi cột I VIDEO | Máy 1 | đọc | sheet |

**Test ep01 tại máy 1: em chạy cả 7–11 tại máy 1 (ngoại lệ 1 lần).** Từ ep02: dừng ở #6.

Vì sao giọng + ảnh + neo ở máy 2 mà không ở máy 1: máy 2 đã có bundle chạy gpti2 + `make_video --from B8` cho Lane A
(toshi) — cùng khuôn; giọng ở máy 2 đúng ý anh "giọng là bước cuối"; máy 1 rảnh làm kịch bản lane khác.

---

## 2. VIỆC CODE TRƯỚC KHI CHẠY (tất cả field-driven, lane khác không đổi hành vi)

| # | Việc | File | Ước | Vì sao |
|---|---|---|---|---|
| C1 | `image.prompts_by="fable_doan"`: Fable viết prompt theo ĐOẠN kèm tag nhân vật → `img_prompts.txt` + `img_doan.txt` cùng lúc; đếm/format sai → hỏi lại 1 lần rồi BLOCK | `pipeline/lean_script.py` (hàm mới) + `make_video.b5w_write_prompts` rẽ nhánh | ~1h | B5W hiện dùng Gemini + storyboard theo SRT (cần giọng trước); satori chứng minh "não gán đoạn, máy đặt neo" khớp lời hơn chia đều; Fable 0đ |
| C2 | `image.characters_from_bible=true`: `gen_cmd` đọc `characters.json` → `--ref` master chính, `--ref2` master mentor; `gen_images.py` thêm tag `@REF12` (cảnh 2 người → gửi cả 2 ảnh tham chiếu, gpti2 nhận tới 8) | `make_video.py`, `gen_images.py`, `ai_steps` marker | ~45' | Lane G khoá 2 mặt (profile `_ref_lock_note`); make_video hiện chỉ 1 master từ `image.character_sheet` |
| C3 | `assemble.sync="anchors"`: trước B8 chạy `sinh_neo.py` (nếu chưa có `anchors.txt`), B8 truyền `--anchors` | `make_video.b8_assemble` | ~20' | make_video chưa nối neo (SOP_LANE_E §0d ghi rõ nhánh này không có img_doan) |
| C4 | `publish.listing_external=true`: bỏ B7/B9, B10 không đòi thumbnail/title, B11 giao 3 file | `make_video`, `qc_final.py`, `giao_hang.py` | ~25' | điểm 2 của anh |
| C5 | `--den`/`--from` kiểm `kiem_lock` trước B4 (đã có ở B5W) — thêm ở B4 để máy 2 không đọc giọng cho bản script lệch sha | `make_video.b4_voice` | 5' | khoá SHA sau Sol PASS |
| C6 | Test hồi quy: Lane E `ep01` `--only B8 --dry-run` không đổi lệnh (không khai field mới → nhánh cũ) | — | 10' | hàng rào #2 |

Tổng code ~2h45. **Không** sửa `script.txt` nào (sha đã khoá).

---

## 2b. ĐÃ CODE (2026-09-20 21:30, anh duyệt C1–C6, CHƯA chạy ep01 — chờ anh xem code)

| # | Thay đổi | Ở đâu |
|---|---|---|
| C1 | `pipeline/prompt_doan.py` (mới, ~170 dòng): Fable viết `đoạn|TAG|prompt` → `img_prompts.txt` (@REF/@REF2/@REF12/@GROK + style) + `img_doan.txt` + fingerprint; kiểm khuôn (đúng N dòng, đoạn không giảm, trần ảnh/đoạn = ≥4 s lời, tag hợp lệ, mặt ≤50%), hỏi lại 1 lần rồi BLOCK | `make_video.b5w_write_prompts` rẽ nhánh khi `image.prompts_by=="fable_doan"` → chạy B55 `qc_img_doan --mode warn` ngay sau (FAIL cơ học = dừng) |
| C2 | `masters_from_bible()` + `_master_ok()`: đọc `characters.json` (ref_marker @REF/@REF2, master path), thiếu ảnh → gpti2 medium nền xám + QC `qc_character.py --img` (nay exit 2 khi lệch tuổi/giới/trẻ con) tối đa 2 lượt; `gen_cmd` → `--ref`/`--ref2` | `make_video.py`; `gen_images.py` thêm tag `@REF12` (gửi cả 2 master, gpti2 nhận 8) |
| C3 | `assemble.sync=="anchors"`: B8 kiểm `img_doan.txt` + `voice.srt`, chạy `sinh_neo.py` (khi thiếu/cũ) → `assemble --srt --anchors` (+`--burn-sub` chỉ khi burn_subs) | `make_video.b8_assemble` |
| C4 | `publish.listing_external`: B7/B9 ghi `skipped`, `qc_final.kiem` bỏ kiểm ảnh bìa/gói đăng, `giao_hang` chỉ đòi final.mp4, giao mp4 + phude.srt + review-vi.mp4 + tomtat | `make_video.py`, `qc_final.py`, `giao_hang.py` |
| C5 | `kiem_lock("B4")` trước TTS | `make_video.b4_voice` |
| C6 | Hồi quy: Lane E ep01 lệnh B8 y cũ (`--zoom 1.0 --transition xfade --xfade 0.5`, không --anchors/--srt); 4 cờ = False; `gen_cmd` Lane E không đổi. Lane G 4 cờ = True, B7/B9 skip. Test offline prompt_doan: parse 94 dòng/158 đoạn PASS B55 cơ học, bắt được tag lạ/thừa dòng/đoạn giảm | chạy thật trong phiên |
| + | Profile Lane G khai 4 field (+ ghi chú); `ep01/characters.json` (俺 篠宮敏郎 64 @REF · mentor 大場誠一 64 @REF2) viết từ script LOCK | `profiles/profiles/teinengo-tanoshimi.json`, `assets/.../ep01-asa-shukan/characters.json` |

**Thứ tự bước thật của `make_video.py` cho Lane G** (main() giữ nguyên, các bước lane không cần tự skip):
B3 lean (skip vì lock PASS) → **B4 → B4Q → B5W(fable_doan+B55) → B5P → B5(master×2 + ảnh) → B5Q → B7(skip) → B8a neo → B8 → B8Q → B9(skip) → B10 → B11**.
Giọng vẫn đứng trước ảnh trong 1 lượt chạy (khung make_video) — nhưng nội dung ảnh KHÔNG dùng SRT, nên đổi giọng sau = chạy lại
`--from B4`? KHÔNG (xoá state B5W → Fable viết lại prompt). Đúng cách: xoá `voice.mp3/voice.srt/anchors.txt/final.mp4` + pop state
B4/B4Q/B8/B8Q → chạy lại lệnh thường (B5W/B5 skip vì đã có file). Em sẽ đóng thành cờ `--redo-voice` nếu anh muốn.

## 3. LỆNH CHẠY TEST EP01 (sau khi anh xem code OK)
```
# 1) 0đ — Fable viết prompt + gán đoạn, B55, fingerprint
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-tanoshimi --slug ep01-asa-shukan --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-tanoshimi --slug ep01-asa-shukan --only B5P
# 2) xem tiền trước khi vẽ (không vẽ)
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-tanoshimi --slug ep01-asa-shukan --only B5 --dry-run
# 3) NGOẠI LỆ test tại máy 1: giọng → master → ảnh → neo → ghép → QC → giao
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-tanoshimi --slug ep01-asa-shukan
```
(Lệnh cũ trong bản phương án dùng `--from B4 --den B5P --dry-run` là SAI: `--dry-run` bỏ B5W, `--from B4` xoá state B5W → đã thay bằng 3 lệnh trên.)



**Số đo dự kiến ep01 (7.112 chữ ≈ 22'):** ~94 ảnh (14s/ảnh) · @REF+@REF2 ≤35% → ~33×110 + 61×50 ≈ **6.700đ** + 2 master
≈ 600đ · giọng ≈ 9.200 credit (~1.200đ) · Gemini QC ~200đ → **≈ 8.700đ/tập**. Thời gian máy: B4 3' · B5 5–8' (24 luồng)
· B8 8–12' · B8Q 5' → **~30'**.

---

## 4. CỔNG DỪNG (không đẩy lên anh trừ khi lỗi thiết kế)

| Cổng | Ngưỡng | Rớt → |
|---|---|---|
| QC master (`qc_character`) | tuổi ±12, đúng giới, manga style, mặt rõ | vẽ lại master tối đa 2 lần; vẫn rớt → sửa `characters.json` |
| B5P prompt↔truyện | mode WARN (lane mới) — chỉ chặn lỗi cơ học/STALE | sửa prompt tại chỗ |
| B55 mapping | số dòng = số prompt, đoạn hợp lệ, không chia đều máy móc | Fable viết lại img_doan |
| B4Q | phủ ≥95% kịch bản, không rụng đoạn, credit đủ TRƯỚC khi gọi | đọc `qc_audio`, chạy lại B4 |
| B5Q | 10 ảnh mẫu: méo tay/chữ lạ/sai người | vẽ lại ảnh hỏng (đã có) |
| sinh_neo | mọi ảnh ≥1s, neo là cue thật | giảm ảnh dồn 1 đoạn trong img_doan |
| B8Q | sync_score, khung đen, độ dài = audio | vẽ lại ảnh lệch (`fix_weak_images` đã có) → ghép lại, tối đa 2 lượt |
| Lớp 3 | em xem `review-vi.mp4` mốc 0/5/10/15/20' + 3 mốc B8Q chê | ghi việc, không sửa tay |

---

## 5. RỦI RO THẬT & CÁCH ĐỠ
1. **Mặt manga trôi** giữa ảnh @REF (gpti2 edit bê bối cảnh master) — đã có `REF_TAIL` ép "same face, new scene"; master
   nền xám trơn; QC mẫu B5Q. Nếu >30% ảnh sai mặt → hạ tỉ lệ @REF (chỉ cận/trung cảnh), cảnh xa để plain.
2. **Fable đếm sai số prompt / tag** — máy kiểm số dòng, hỏi lại 1 lần, không tự vá.
3. **gpti2 429/402** — 3 key round-robin đã có; hết tiền → dừng báo (không đổi sang ima2 — anh đã bỏ).
4. **Máy 2 chưa hoàn chỉnh** — bundle `shared/buoc2_3_tool/` hiện chỉ đủ Lane A; em cập nhật bundle chung (+
   `lean_script`/`gate_common`/`sinh_neo`/`qc_img_doan`/`pace_audio`/`ban_xem_viet`… + profile Lane G) và viết
   `GIAO_VIEC_MAY2_LANE_G.md` (cài 1 lần + mỗi tập) — **làm sau khi ep01 test xong**, theo lời anh.
5. **Đổi giọng sau khi xem** — chỉ B4 → neo → B8 (15'), ảnh giữ; em ghi lệnh sẵn vào SOP.

---

## 6. SAU TEST — SOP/tài liệu sẽ cập nhật
`docs/SOP_LANE_G.md` §2 (lệnh 2 pha máy 1 / máy 2, cột H/I), `docs/BAT_DAU_LANE/teinengo-tanoshimi.md`, bundle máy 2 +
`FlowHandoff_local/shared/GIAO_VIEC_MAY2_LANE_G.md`, memory. Anh chỉ cần: xem `review-vi.mp4` ep01 khi em báo xong.


## 7. KẾT QUẢ TEST EP01 TẠI MÁY 1 (2026-09-21, 3 lượt, giao `E:\CLAUDE\YOUTUBE\CHANEL	einengo-tanoshimi\ep01-asa-shukan\`)
| Lượt | Gì | Kết quả | Tiền |
|---|---|---|---|
| 1 | B4 giọng clone 22:28 · 2 master · 94 ảnh · neo 94/94 · ghép 2,8' · B8Q ĐẠT 3,5 · giao | **Ảnh sai kiểu**: ~40% ảnh nhân vật ra TRANG MANGA NHIỀU Ô (chữ "manga illustration" + master kiểu "reference sheet") | 6.900 ảnh + 600 master + giọng ~1.100 |
| 2 | sửa master = 1 chân dung đơn, suffix cấm panel, vẽ lại 41 ảnh mặt | ảnh mặt đẹp, nhất quán; B8Q trượt 3/10 mốc (ảnh cảnh vật cũ vẫn collage; `fix_weak_images` trỏ SAI ảnh vì chia đều thay vì tra anchors → đã vá) | +4.500 |
| 3 | vẽ lại 50 ảnh cảnh vật suffix mới | B5Q còn 2/10 mẫu collage (022, 032 — cảnh nhiều người từ sau); B8Q ĐẠT 3,5; B10 0 nặng; B11 giao 3 file + tomtat | +2.700 |
**Tổng ≈ 15.800đ + 55' máy** — gấp đôi dự kiến vì em không vẽ thử 5 ảnh trước khi vẽ cả loạt.
**Còn treo:** ~10–20% ảnh cảnh vật vẫn có thể ra collage (gpti2 bias "manga") → thử đổi đầu prompt sang "single-panel anime illustration" hoặc bỏ chữ "manga"; B5Q "không khớp prompt" ở 042 (prompt "no face visible" nhưng ảnh có mặt) — vision đúng, prompt lỗi nhỏ.
**Luật mới cho tập sau (ghi SOP §2):** B5 vẽ **5 ảnh mẫu** (`gen_images --limit 5`) → lớp 3 xem → mới vẽ 94. Đã làm ở tập này thì tiết kiệm được ~7.000đ.

**2026-09-21 06:36 — anh chốt: video Lane G PHẢI cháy phụ đề tiếng Nhật** → `assemble.burn_subs=true` (profile), B8 nhánh anchors
truyền `--burn-sub --font Yu Gothic`; ghép lại 4,8' (không vẽ ảnh) → B8Q ĐẠT 3,9 · B10 0 nặng · giao lại. Đã soi khung 5:00: chữ
trắng viền đen đáy khung, đúng câu đang đọc. `phude.srt` vẫn giao kèm.
