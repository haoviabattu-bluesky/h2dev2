# HỒ SƠ GIAO VIỆC — BƯỚC 2+3: SINH ẢNH, GHÉP VIDEO & GIAO HÀNG

> ## ⛔ LANE E — `kenko-chiebukuro` — 健康の知恵袋 (KÊNH SỨC KHOẺ NGƯỜI GIÀ NHẬT, KHÔNG PHẢI LANE KHÁC)
> Dự án `E:\CLAUDE\YOUTUBE\h2dev` chạy nhiều lane song song. Đây là **Lane E**, kênh 健康の知恵袋:
> video liệt kê 5 thực phẩm/thói quen kiểu "bác sĩ giải thích" cho người già Nhật, minh hoạ bằng
> ẢNH AI VẼ MỚI (watercolor ấm áp), **KHÔNG có 1 nhân vật host lặp lại xuyên video** — mỗi mục trong
> danh sách 5 mục là 1 người ẩn danh khác nhau. **KHÔNG PHẢI** lane `satori-jp-obaa` (REF-LOCK 1
> nhân vật xuyên suốt) và **KHÔNG PHẢI** lane `irogatatarukioku`/Lane D (tô màu ảnh tư liệu thật
> bằng `ima2` miễn phí — đọc nhầm `GIAO_VIEC_LANE_D_BUOC2.md` là chạy nhầm tool hoàn toàn khác).
>
> **Chạm đúng và CHỈ đúng các đường dẫn sau:**
> - Thư mục làm việc: `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep<nn>-<slug>\`
> - Thư mục giao hàng: `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<nn>-<slug>\`
> - Trang tính: ID `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`, **tab `70dai-kenko`**
> - Profile: `profiles/profiles/kenko-chiebukuro.json`
>
> **KHÔNG BAO GIỜ** đụng vào `assets/satori_jp/`, `assets/toshi-densetsu-jp/`,
> `assets/irogatatarukioku/`, `assets/out/` (Lopezzapa68), tab sheet khác, hay thư mục `CHANEL\` của
> kênh khác. Không chắc một đường dẫn có thuộc Lane E không → **dừng và hỏi**.

---

## 0. BỨC TRANH — DÂY CHUYỀN 2 BƯỚC (giống hệt mô hình Lane D, khác ở nguồn vẽ ảnh)

| Bước | Ai làm | Làm gì | Kết thúc khi |
|---|---|---|---|
| 1 | Claude (phiên chat h2dev) | Tra tư liệu thật → viết kịch bản → QC (B3Q/B3F) → lồng tiếng (B4/B4Q) → viết + vẽ thumbnail (B7) | Đủ file liệt kê ở mục 2 |
| **2+3** | **BẠN (agent khác — DeepSeek/Hermes, hoặc bất kỳ agent nào chạy được lệnh Python)** | Sinh + vẽ ảnh thân video (B5/B5Q) → ghép video (B8/B8Q) → nghiệm thu (B9/B10) → giao hàng (B11) → phụ đề Việt xem thử → ghi cột G | Cột G có đường dẫn thư mục giao hàng, bạn đưa đường dẫn đó cho chủ dự án |

**KHÔNG cần Claude cho bước 2+3** — đã verify thật trên tập 1 (`ep01-tento-kossetsu`, 2026-09-16):
toàn bộ chuỗi B5→B11 chỉ là gọi lệnh `pipeline/make_video.py` (sinh prompt ảnh qua Gemini/ramcloud,
vẽ ảnh qua gpti2, QC qua Gemini vision, ghép video qua ffmpeg, nghiệm thu bằng rule cứng) — không có
bước nào cần phán xét sáng tạo. Mọi quyết định "vẽ ảnh kiểu gì", "nhân vật ra sao", "khuôn thumbnail
thế nào" đã CHỐT XONG ở bước 1 và nằm trong `profile.json`/`script.txt`/`thumb_bg_prompt.txt` —
bạn chỉ CHẠY LỆNH và ĐỌC KẾT QUẢ CỔNG, không tự quyết nội dung.

**Khác Lane D ở ĐÚNG 1 chỗ: nguồn vẽ ảnh.** Lane D dùng `ima2` (miễn phí, quota ChatGPT Plus). Lane E
dùng **`gpti2` (TRẢ TIỀN thật, ~50đ/ảnh, ~4.000-5.500đ/tập)** — chủ dự án đã xác nhận chấp nhận mức
chi phí này (2026-09-16, vì Lane E không REF-LOCK nên đơn giản hơn satori/toshi). Không tự đổi sang
`ima2`/nguồn khác để "tiết kiệm" mà không hỏi trước.

---

## 1. ⛔ CẤM TUYỆT ĐỐI

1. **KHÔNG xoá dòng/cột/dữ liệu trong bất kỳ Google Sheet nào.** Chỉ đọc và ghi đè ĐÚNG MỘT Ô cột G
   qua đúng công cụ ở Lệnh cuối. Không `deleteDimension`, không `clear` hàng loạt.
2. **KHÔNG `taskkill chrome` / `Stop-Process chrome` theo tên.** Bước 2+3 của Lane E không cần Chrome.
3. **KHÔNG sửa `series_ctx.txt`, `competitor.txt`, `script.txt`, `voice.mp3`, `voice.srt`,
   `thumb_text.txt`, `thumbnail_final.png`, `thumb_bg_prompt.txt`.** Đây là sản phẩm ĐÃ NGHIỆM THU
   (B3Q/B3F/B4Q đã ĐẠT) của bước 1. Thấy sai thì **báo lại**, không tự sửa.
4. **KHÔNG đổi `profile.json`** (voice/char_rate/image/thumbnail...) trừ khi chủ dự án yêu cầu rõ.
5. **KHÔNG dùng nguồn ảnh nào khác `gpti2`** (không `ima2`, không `vilao`, không `imgstudio`) trừ khi
   `gpti2` lỗi/hết tiền thật **và** đã báo chủ dự án trước.
6. **KHÔNG dùng marker `@REF`/`--ref` thủ công.** `write_img_prompts()` (bước 1 của B5, tự động)
   ĐÃ tự quyết cảnh nào cần khoá mặt theo `profile.image.character_sheet` — đừng can thiệp tay.
7. **KHÔNG dùng `--force-qc` để "cho qua" khi B5Q/B8Q/B10 rớt vì lý do bạn không chắc.** Rớt vì lý do
   RÕ RÀNG là false-positive (xem mục 5 sổ tay) thì được, còn lại phải dừng hỏi.
8. **KHÔNG ghi cột G khi chưa giao hàng xong thật.**
9. **KHÔNG chuyển bất kỳ dòng nào trong tab `70dai-kenko` sang trạng thái khác STT ngoài dòng bạn
   đang làm** — sheet có 10 dòng, mỗi dòng 1 tập, đừng động vào dòng khác.

---

## 2. ĐIỀU KIỆN ĐƯỢC PHÉP BẮT ĐẦU

Thư mục tập `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep<nn>-<slug>\` phải có đủ:

| File | Vai trò |
|---|---|
| `series_ctx.txt` | Tư liệu sự thật (nguồn thật, không bịa) |
| `competitor.txt` | Transcript kênh mẫu (khung kể, tham khảo nhịp) |
| `script.txt` | Kịch bản tiếng Nhật, đã qua B3Q + B3F (xem `state.json`) |
| `voice.mp3` + `voice.srt` | Giọng đọc + phụ đề bám kịch bản, đã qua B4Q |
| `thumb_text.txt` + `thumb_bg_prompt.txt` + `thumbnail_final.png` | Thumbnail đã dựng xong (B7) |
| `state.json` | Trạng thái từng bước — B2/B3/B3Q/B3F/B4/B4Q/B7 phải "done", B5 trở đi CHƯA có |

Thiếu bất kỳ file nào ở trên → **DỪNG, báo chủ dự án**, đừng đoán/tự tạo thay.

Số tập (`<nn>`) = **STT cột A** của trang tính, tab `70dai-kenko`. Dòng sheet thật = STT + 1.

---

## 3. ⭐ THẺ CHẠY — THEO ĐÚNG THỨ TỰ

Ví dụ dùng tập `ep01-tento-kossetsu` (STT 1). Thay slug + STT thật của tập bạn được giao. Mọi lệnh
chạy từ `E:\CLAUDE\YOUTUBE\h2dev\pipeline`:
```bash
export PYTHONIOENCODING=utf-8
```
(PowerShell: `$env:PYTHONIOENCODING="utf-8"; $env:PYTHONUTF8="1"`)

### ⚠️ TRƯỚC Lệnh 1 — kiểm `img_prompts.txt` KHÔNG CÒN SÓT lại từ bản kịch bản cũ
`b5_images()` chỉ sinh `img_prompts.txt` mới **KHI FILE CHƯA TỒN TẠI** (`if not pf.exists()`) — nó
KHÔNG tự so `script.txt` đã đổi hay chưa. Nếu tập này từng chạy B5 một lần (vd bằng kịch bản cũ,
rồi bước 1 viết lại `script.txt`), `img_prompts.txt` cũ vẫn còn nguyên → B5 sẽ ÂM THẦM vẽ ảnh theo
NỘI DUNG CŨ, lệch hẳn với lời đọc mới, không báo lỗi gì (đã dính thật ở tập 1 khi viết lại kịch bản
2026-09-17: 89 ảnh vẽ xong mới phát hiện dùng nhầm prompt của bản Gemini cũ, tốn 4.450đ vẽ lại lần
2). **Luôn kiểm trước khi chạy Lệnh 1:**
```bash
py -3.13 -c "import json; print(json.load(open('../assets/kenko-chiebukuro/<slug>/state.json'))['B3']['at'])"
```
So thời điểm này với thời điểm sửa đổi (`mtime`) của `img_prompts.txt` (nếu file đã có) — `img_prompts.txt`
CŨ HƠN thời điểm B3 → xoá `img_prompts.txt` + thư mục `img/` (di vào `_truoc_khi_viet_lai/` để giữ
lại phòng khi cần, đừng xoá hẳn) rồi mới chạy Lệnh 1.

### Lệnh 1 — sinh + vẽ ảnh thân video (B5)
```bash
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --only B5
```
- Tự sinh `img_prompts.txt` (gọi Gemini qua ramcloud, dùng `profile.image.character_sheet` — ĐÃ
  viết sẵn "không có nhân vật cố định, mỗi mục 1 người khác nhau", KHÔNG cần truyền `--sheet` tay).
- Tự vẽ ảnh qua `gpti2` (24 luồng), in ra số ảnh + chi phí ước tính TRƯỚC khi vẽ thật — **đọc dòng
  đó, nếu số tiền lệch xa khoảng 4.000-5.500đ (vd do video dài bất thường) thì dừng hỏi trước khi
  để nó vẽ thật**.
- Số ảnh ≈ (giây audio thật ÷ 14) — không cố định 89, phụ thuộc độ dài tập.
- Đo thật tập 1: 89 ảnh, 4 ảnh khoá mặt (@REF, tự động), 4.450đ, ~10 phút (185s vẽ + phần khác).

⚠️ **Đọc kỹ log B5 tìm dòng `⚠️ storyboard hỏng (...) → quay về cách rải đều`** — dòng này nghĩa là
bước đồng bộ ảnh-theo-câu (storyboard, gọi Gemini chia 342 cue SRT thành N khối ảnh) bị lỗi hạ tầng
tạm thời (đã gặp thật: `gemini-3.8-flash` trả quá ngắn, `ns24` 404 sai tên model, `gpt-5.6-luna` 503
— cả 3 model dự phòng cùng lỗi) và tự lùi về cách rải ảnh đều theo THỜI GIAN thay vì theo NỘI DUNG
câu nói → ảnh sẽ trôi dần lệch lời về cuối video (đúng lỗi đã ghi ở memory "so-dem-va-noi-dung-la-mot-bien").
Thấy dòng này → **ĐỪNG chạy tiếp — quay lại thử riêng bước sinh prompt (không tốn tiền vẽ) tối đa
vài lần cho tới khi KHÔNG còn dòng cảnh báo đó nữa, rồi mới cho vẽ ảnh thật**:
```bash
py -3.13 -X utf8 -c "
import ai_steps, profiles
from pathlib import Path
slug_dir = Path(r'..\assets\kenko-chiebukuro\<slug>')
prof = profiles.load('kenko-chiebukuro')
script = (slug_dir/'script.txt').read_text(encoding='utf-8')
res = ai_steps.write_img_prompts(prof, script, duration_sec=<giây audio thật lấy từ state.json B4.seconds>, srt=str(slug_dir/'voice.srt'))
print('storyboard OK?', res['storyboard'])
(slug_dir/'img_prompts.txt').write_text(chr(10).join(res['prompts']), encoding='utf-8')
if res.get('world'): (slug_dir/'world.txt').write_text(res['world'], encoding='utf-8')
"
```
`storyboard OK? True` mới chạy Lệnh 1 thật (nó sẽ thấy `img_prompts.txt` đã có sẵn nên KHÔNG sinh
lại, chỉ vẽ ảnh — không tốn thêm tiền cho bước sinh prompt). Nếu lỗi lặp lại giống hệt nhau **quá 3
lần liên tiếp** → đây không còn là "tạm thời", báo chủ dự án (có thể Gemini/ramcloud đang sập thật).

### Lệnh 2 — QC loạt ảnh (B5Q)
```bash
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --only B5Q
```
Kỳ vọng "0 vấn đề". Có vấn đề → tool tự vẽ lại tối đa 2 lượt; vẫn còn sau 2 lượt → xem mục 5.1.

### Lệnh 3 — ghép video + QC hình khớp lời (B8, B8Q)
```bash
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --only B8
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --only B8Q
```
- B8 ghép ~9-10 phút xử lý cho 1 tập ~20 phút/89 ảnh (xfade transition, KHÔNG cháy phụ đề — đúng
  thiết kế dự án, xem mục 4).
- B8Q kỳ vọng "ĐẠT", `sync_score` ≥ 4/5. **Nếu thấy lỗi "N/N khung KHÔNG thấy phụ đề" — đó là BUG
  ĐÃ SỬA (2026-09-16), không nên xuất hiện nữa; nếu vẫn thấy, ĐỪNG tự `--force-qc`, báo chủ dự án
  ngay vì có thể code bị hoàn tác.**

### Lệnh 4 — nghiệm thu gói đăng tải (B9, B10)
```bash
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --only B9
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --from B10
```
⚠️ **B10 dùng `--from B10` (KHÔNG phải `--only B10`)** — nếu trước đó B10 đã từng chạy và THẤT BẠI ở
lượt trước (vd bạn sửa gì đó rồi chạy lại), `--only` sẽ bị `skip()` bỏ qua vì B10 đã "done" (kể cả
done-vì-thất-bại) — PHẢI dùng `--from B10` để ép chấm lại thật. Đây là bẫy đã dính thật ở tập 1, xem
mục 5.2.
Kỳ vọng B10 "0 phát hiện NẶNG". Rớt vì B3F còn mục chưa rõ nguồn → xem mục 5.3, KHÔNG tự judge được
thì báo chủ dự án (đây là chỗ CẦN NGƯỜI/Claude phán xét nội dung, không phải việc cơ khí).

### Lệnh 5 — giao hàng (B11)
```bash
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu --from B10
```
(B11 tự chạy tiếp ngay sau B10 nếu B10 ĐẠT trong cùng lệnh trên — không cần lệnh riêng.) Copy
`final.mp4` + `thumbnail.png` + `phude.srt` + `listting.txt` + `review_vi.mp4` sang
`E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<nn>-<slug>\`.

### Lệnh 6 — bản xem thử tiếng Việt (nếu B11 chưa tự làm — kiểm `state.json`)
Nếu thư mục giao hàng CHƯA có `review_vi.mp4`/`review-vi.mp4`:
```bash
py -3.13 -X utf8 ban_xem_viet.py --slug "<đường dẫn thư mục tập>" --profile kenko-chiebukuro
```
File `voice.vi.srt` + `review_vi.mp4` (854×480, phụ đề Việt CHÁY vào hình, để chủ dự án đọc lại nội
dung — bản này KHÔNG đăng lên YouTube).

### Lệnh 7 — ghi cột G rồi báo chủ dự án
Dùng đúng tool có rào chắn (KHÔNG ghi tay qua MCP Sheets):
```bash
py -3.13 ghi_cot_video.py --tab 70dai-kenko --dong 1 --thu   # xem trước
py -3.13 ghi_cot_video.py --tab 70dai-kenko --dong 1         # ghi thật
```
`--dong` là **STT cột A**. Nếu tool này chưa từng chạy cho tab `70dai-kenko`, kiểm tra header cột G
dòng 1 phải đúng chữ "VIDEO" trước — sai thì dừng, báo chủ dự án (cấu trúc sheet Lane E có thể khác
Lane D một chút, xem `docs/SOP_LANE_E.md` §1b bảng cột A→H).

⚠️ **Đã vá 2026-09-17**: `--tab` của tool này trước đây PHẢI trùng y hệt `profile.publish.upload_channel`
("kenko-chiebukuro") mới tìm ra đúng lane — nhưng tên tab TRANG TÍNH thật của Lane E lại là
`70dai-kenko` (khác hẳn, theo handle YouTube @70dai-kenko), nên `--tab 70dai-kenko` từng báo lỗi
"không profile nào khai publish.upload_channel = '70dai-kenko'". Đã thêm field `publish.sheet_tab`
trong profile để tách 2 khái niệm (tên thư mục CHANEL vs tên tab sheet) — giờ `--tab 70dai-kenko`
chạy đúng. Nếu gặp lại lỗi này ở lane khác có cùng tình huống (tab sheet ≠ tên kênh) → thêm
`publish.sheet_tab` vào profile đó, ĐỪNG sửa field `upload_channel` (sẽ làm lệch tên thư mục CHANEL
đã giao trước đó).

Ghi xong, **đưa đường dẫn thư mục giao hàng cho chủ dự án trong câu trả lời cuối cùng**, kèm số đo
thời gian + kết quả từng cổng (giống mẫu Lane D: *"B5Q 0 vấn đề, B8Q sync 4,6/5, B10 0 phát hiện
nặng, tổng ~25 phút"*).

---

## 4. BỐI CẢNH KỸ THUẬT CẦN BIẾT (đừng đoán, đọc trước khi thắc mắc)

- **`burn_subs: false` là CỐ Ý** (`profile.json` → `assemble.burn_subs`) — video giao KHÔNG cháy phụ
  đề tiếng Nhật vào hình. Đây không phải lỗi, đừng "sửa giúp". File `phude.srt` giao kèm để tự up
  làm CC trên YouTube.
- **`image.character_sheet` đã viết sẵn bằng tiếng Anh, prompt-ready** trong `profile.json` — B5 tự
  dùng, không cần bạn viết lại hay truyền `--sheet`.
- **`thumb_bg_prompt.txt` đã có sẵn từ bước 1** — mô tả ảnh món ăn "hero" của tập (thường là món ở
  hạng #1), KHÔNG cần bạn tạo lại hay đổi.
- **Chi phí toàn bộ bước 2+3 của 1 tập ≈ 4.000-5.500đ** (chỉ tốn ở Lệnh 1, các lệnh còn lại 0đ hoặc
  rất rẻ — vài lượt gọi Gemini QC).

---

## 5. SỔ TAY XỬ LÝ KHI RỚT

### 5.0 B5 vẽ xong nhưng nội dung ảnh KHÔNG khớp lời đọc mới
Kiểm tra `img_prompts.txt` có phải sinh SAU LẦN B3 GẦN NHẤT không (xem cảnh báo trước Lệnh 1). Vẽ
nhầm rồi thì di `img/` + `img_prompts.txt` + `world.txt` vào `_truoc_khi_viet_lai/` (đặt tên phân
biệt, ĐỪNG xoá hẳn), xoá `B5`/`B5K`/`B5A`/`B5Q` khỏi `state.json`, rồi chạy lại đúng thứ tự (sinh
prompt riêng để kiểm `storyboard OK? True` trước, mới vẽ ảnh thật).

### 5.1 B5Q rớt (ảnh có vấn đề sau 2 lượt vẽ lại)
Mở `qc.json` hoặc đọc log — mỗi ảnh hỏng có lý do (thường: méo tay/mặt, sai phong cách, dính chữ
lạ). Vẽ lại quá 2 lượt vẫn hỏng CÙNG 1 ảnh → dừng, báo chủ dự án kèm tên file + lý do, đừng tự bỏ
ảnh đó hay đổi prompt tay.

### 5.2 B10 "bỏ qua" dù bạn vừa sửa gì đó — nghi ngờ số ảo
Nếu bạn từng sửa 1 file (vd chạy lại `qc_facts.py` cho `qc_facts.json`) rồi chạy lệnh KHÔNG có
`--from B10`, B10 sẽ IN RA "[B10] bỏ qua (đã xong ...)" và đi thẳng luôn — đây KHÔNG PHẢI nghĩa là
"đã kiểm và đạt", mà là "lần trước đã chạy (có thể đã THẤT BẠI) và không ai bắt chấm lại". Luôn dùng
`--from B10` sau khi sửa bất cứ thứ gì liên quan tới B10.

### 5.3 B10 rớt vì "B3F còn N chi tiết KHÔNG có trong tư liệu"
Đây là chỗ CẦN PHÁN XÉT NỘI DUNG (đối chiếu từng mục với `series_ctx.txt`), KHÔNG phải việc cơ khí —
**dừng lại, báo chủ dự án kèm danh sách mục cụ thể** (mở `qc_facts.json`), đừng tự `--force-qc`. Nếu
chủ dự án (hoặc Claude bước 1) đã ghi `_nghiem_thu_note` trong `qc_facts.json` giải thích rõ lý do
từng mục là false-positive/được phép — đó là bằng chứng ĐàXÉT rồi, bạn có thể chạy tiếp
`--force-qc` an toàn với đúng những mục ĐÃ có ghi chú đó (không áp dụng cho mục MỚI chưa ai xét).

### 5.4 Lệnh chết giữa chừng / exit code ≠ 0
Đọc **dòng cuối của log**, đừng kết luận từ exit code (một số lỗi Python vẫn thoát code 0 khi output
bị pipe qua công cụ khác). Mọi lần thử đều báo **cùng một lý do giống hệt nhau** → nghi phép kiểm
sai, không phải công cụ sai — báo lại thay vì tăng số lần thử.

---

## 6. SỐ ĐO THẬT

### Lần 1 (tập 1, kịch bản Gemini, 2026-09-16 — video ~20,7 phút, 89 ảnh)

| Việc | Thời gian thật |
|---|---|
| B5 (sinh prompt qua Gemini + vẽ 89 ảnh qua gpti2, 24 luồng) | ~10 phút (185s vẽ + phụ) |
| B5Q (QC 89 ảnh qua Gemini vision) | ~4 phút |
| B8 (ghép video, xfade, mux) | ~9,2 phút |
| B8Q (8-10 mẫu, gọi vision) | ~1 phút |
| B9 + B10 | dưới 1 phút |
| B11 + bản xem tiếng Việt (dịch 348 cue + burn) | ~4 phút |
| **Tổng bước 2+3** | **~30 phút** |

### Lần 2 (tập 1 làm lại, kịch bản Claude `claude_p`, 2026-09-17 — video 20,6 phút, 88 ảnh)

Lần này dính 2 lần lỗi hạ tầng storyboard liên tiếp (xem cảnh báo ở Lệnh 1) nên tốn ~3 lượt vẽ ảnh
(mất thêm tiền oan ~8.850đ do vẽ 2 lần trước khi bắt đúng lỗi) — số dưới đây là lượt ĐÚNG (lượt 3):

| Việc | Thời gian thật |
|---|---|
| B5 sinh prompt (storyboard, đã retry tới khi OK) | ~10s (không tốn tiền, chỉ gọi LLM) |
| B5 vẽ 88 ảnh qua gpti2 (24 luồng) | 451s (~7,5 phút), 4.400đ |
| B5Q (QC ảnh, 1 ảnh vẽ lại) | ~2 phút |
| B7 thumbnail (dùng nền có sẵn, chỉ đổi chữ) | <5s |
| B8 (ghép video, xfade, mux) | 290s (~4,8 phút) |
| B8Q (QC video) | ~1 phút, sync_score 3.6/5, 0 vấn đề |
| B9 + B10 | <1 phút, B10 "0 phát hiện (0 nặng)" — SẠCH ngay lần đầu, không cần force-qc |
| B11 + bản xem tiếng Việt | ~2,5 phút |
| **Tổng bước 2+3 (lượt đúng, không tính 2 lượt vẽ hỏng trước)** | **~18 phút** |

⚠️ **Việc `final.mp4`/`voice.mp3`/`thumbnail_final.png` CŨ (kịch bản Gemini) đã bị GHI ĐÈ hoàn toàn**
khi làm lại lần 2 (cùng thư mục tập, cùng thư mục CHANEL) — không còn giữ được bản video Gemini cũ
để so sánh trực tiếp bằng mắt nữa. Số liệu so sánh Bước 1 (script+giọng) giữa 2 bản đã ghi đủ ở
`docs/SOP_LANE_E.md` §0e TRƯỚC khi ghi đè, và `script.txt` bản Gemini cũ vẫn còn nguyên ở
`_truoc_khi_viet_lai/script.txt` trong thư mục tập. **Làm lại tập cho lane này (đổi script rồi render
lại) = mất bản render trước, không có cơ chế "giữ cả 2 bản" tự động** — muốn giữ cả 2 bản render thật
thì phải copy tay `CHANEL\...\ep01-tento-kossetsu\` sang thư mục khác TRƯỚC khi chạy lại B8-B11.

**Mọi báo cáo phải kèm số đo thời gian và kết quả từng cổng** — yêu cầu cứng của chủ dự án.

---

## 7. CHECKLIST XONG VIỆC

- [ ] B5Q: 0 vấn đề (hoặc đã vẽ lại tới khi đạt)
- [ ] B8Q: ĐẠT, có `sync_score` thật trong output (không phải "0 vấn đề" vì thiếu srt)
- [ ] B10: 0 phát hiện NẶNG (hoặc chỉ những mục ĐÃ có `_nghiem_thu_note` giải thích)
- [ ] Thư mục `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<nn>-<slug>\` có đủ `final.mp4` +
      `thumbnail.png` + `phude.srt` + `listting.txt` + `review_vi.mp4`
- [ ] Ô **G** đúng dòng (STT+1) đã ghi đường dẫn thuần qua `ghi_cot_video.py`
- [ ] Đã đưa đường dẫn thư mục giao hàng cho chủ dự án, kèm số đo thời gian + kết quả các cổng

---

## 8. KHI NÀO PHẢI DỪNG VÀ HỎI (thay vì tự quyết)

- Thiếu file bước 1 liệt kê ở mục 2.
- Chi phí B5 ước tính lệch xa khoảng 4.000-5.500đ.
- B5Q rớt quá 2 lượt vẽ lại cùng 1 ảnh.
- B8Q báo lỗi "thiếu phụ đề" (nghi code bị hoàn tác — xem mục 3 Lệnh 3).
- B10 có phát hiện NẶNG mà KHÔNG có `_nghiem_thu_note` giải thích sẵn trong `qc_facts.json`.
- Bạn thấy kịch bản/giọng đọc/thumbnail có vẻ sai — báo, tuyệt đối không tự sửa (thuộc bước 1).
- Chủ dự án giao việc mà không nói rõ STT/tập nào.
- Bất kỳ lúc nào không chắc một đường dẫn có thuộc Lane E (`kenko-chiebukuro`) hay lane khác.

Khi báo, luôn kèm: **tập nào (STT + slug)** · **đang ở bước nào** · **dòng log/số liệu thật** ·
**bạn định làm gì tiếp**.
