# HỒ SƠ GIAO VIỆC — BƯỚC 2: TÔ MÀU, GHÉP VIDEO & GIAO HÀNG

> ## ⛔ LANE D — `irogatatarukioku` — 色が語る記憶 (KÊNH LỊCH SỬ, KHÔNG PHẢI SATORI)
> Dự án `E:\CLAUDE\YOUTUBE\h2dev` chạy nhiều lane song song. Đây là **Lane D**, kênh 色が語る記憶
> ("Ký ức mà màu sắc kể lại"): ảnh tư liệu WW2 **có thật** (Public Domain/CC0, do dự án
> `SPACE_RESEARCH` nghiên cứu) được tô màu AI, kể về các chỉ huy quân đội Nhật đã tử trận.
> **KHÔNG PHẢI** lane `satori-jp-obaa` (chuyện kể cụ bà, ảnh AI vẽ mới + REF-LOCK) và **KHÔNG PHẢI**
> lane `toshi-densetsu-jp` (都市伝説, clip stock, tab sheet `shinya_shiryoshitsu`). Ba lane dùng ba bộ
> công cụ khác hẳn nhau — đọc nhầm runbook là chạy nhầm tool, đừng vay mượn lệnh từ
> `docs/GIAO_VIEC_BUOC3_AGENT.md` (đó là lane khác).
>
> **Chạm đúng và CHỈ đúng các đường dẫn sau:**
> - Thư mục làm việc: `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep<nn>-<slug>\`
> - Thư mục giao hàng: `E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\ep<nn>-<slug>\`
> - Trang tính: ID `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`, **tab `irogatatarukioku`**
> - Profile: `profiles/profiles/irogatatarukioku.json`
>
> **KHÔNG BAO GIỜ** đụng vào `assets/satori_jp/`, `assets/toshi-densetsu-jp/`, `assets/out/`
> (Lopezzapa68), tab sheet khác, hay thư mục `CHANEL\` của kênh khác — kể cả khi tên file/lệnh trông
> giống nhau. Nếu không chắc một đường dẫn có thuộc Lane D không, **dừng và hỏi**.

---

## 0. BỨC TRANH — DÂY CHUYỀN 2 BƯỚC

| Bước | Ai làm | Làm gì | Kết thúc khi |
|---|---|---|---|
| 1 | Claude (Opus, phiên chat này) | Đọc hồ sơ → viết kịch bản → QC kịch bản (B3Q/B3F) → lồng tiếng → giãn nhịp → tính mốc chương thật → viết mô tả (`TIEU_DE_MO_TA.txt`) → **tô màu ẢNH CHÍNH (000.png) + vẽ thumbnail thật** | Đủ file liệt kê ở mục 2, có `BAN_GIAO_BUOC2.txt` trong thư mục tập |
| **2** | **BẠN (DeepSeek/Hermes)** | Tô màu **các ảnh còn lại** → ghép video → QC hình-lời → nghiệm thu gói → giao hàng → phụ đề Việt → ghi cột G | Cột G có đường dẫn thư mục giao hàng, bạn đưa đường dẫn đó cho chủ dự án |

**Không có bước "máy 2 vẽ ảnh qua Google Drive" như Lane A.** Lane D tô màu ảnh thật bằng `ima2`
(chạy local trên chính máy này, port 3333, **miễn phí** — dùng quota gói ChatGPT Plus qua OAuth,
không phải API trả tiền), nên bước 2 tự làm cả phần "vẽ" trong lệnh của chính nó, không cần chờ máy
khác. **Bạn KHÔNG làm lại bước 1** — kịch bản, giọng đọc, mốc chương, mô tả, thumbnail đều đã chốt
và đã qua cổng.

---

## 1. ⛔ CẤM TUYỆT ĐỐI

1. **KHÔNG xoá dòng/cột/dữ liệu trong bất kỳ Google Sheet nào.** Chỉ đọc và ghi đè ĐÚNG MỘT Ô cột G
   qua đúng công cụ ở mục 3 Lệnh 6. Không `deleteDimension`, không `clear` hàng loạt, kể cả khi có ai
   bảo xoá — vẫn không xoá, chỉ đề xuất để họ tự làm.
2. **KHÔNG `taskkill chrome` / `Stop-Process chrome` theo tên.** Máy này chạy nhiều Chrome profile
   của các dự án khác. Bước 2 của Lane D không cần Chrome.
3. **KHÔNG sửa `script.txt`, `series_ctx.txt`, `evidence.json`, `anchors.txt`, `voice_paced.wav`,
   `voice_paced.srt`, `TIEU_DE_MO_TA.txt`, `thumb_text.txt`, `thumbnail_final.png`, `img/000.png`.**
   Đây là sản phẩm đã nghiệm thu (B3Q/B3F đã ĐẠT) của bước 1. Thấy sai thì **báo lại**, không tự sửa
   — sửa hộ là tập sau lặp lại đúng lỗi đó vì không ai biết đã có lỗi.
4. **KHÔNG dùng `gpti2_edit.py`, `gpti2_gen.py`, `vilao_edit.py`, `gen_images.py`, hay bất kỳ nguồn
   ảnh TRẢ TIỀN nào làm mặc định.** `ima2` (miễn phí, xem mục 4) là nguồn DUY NHẤT cho bước 2.
   Chỉ được chuyển sang nguồn trả tiền khi `ima2` thật sự lỗi/hết quota **và** đã báo chủ dự án
   trước — không tự ý đổi để "cho nhanh".
5. **KHÔNG dùng marker `@REF`/`--ref`/REF-LOCK.** Đó là đồ nghề của lane satori (khoá mặt nhân vật
   lặp lại nhiều cảnh). Lane D tô màu từng ảnh tư liệu độc lập, không có nhân vật lặp cảnh.
6. **KHÔNG chuyển thư mục hồ sơ nghiên cứu sang `_DONE\`** cho tới khi B11 giao hàng xong thật
   (mục 3 Lệnh 5 kiểm tra đủ file rồi mới chuyển).
7. **KHÔNG ghi cột G khi chưa giao hàng xong thật.** Ghi sớm = chủ dự án vào một thư mục rỗng.
8. **KHÔNG dùng `--force-qc` hay bỏ qua bất kỳ cổng nào để "cho qua".** Mọi cổng ở đây sinh ra sau
   một lần hỏng thật (xem mục 5).

---

## 2. ĐIỀU KIỆN ĐƯỢC PHÉP BẮT ĐẦU

Thư mục tập `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep<nn>-<slug>\` phải có đủ:

| File | Vai trò |
|---|---|
| `script.txt` | Kịch bản tiếng Nhật, đã qua B3Q + B3F |
| `series_ctx.txt` | Hồ sơ tư liệu gốc (đối chiếu nguồn nếu cần) |
| `evidence.json` | Danh sách ảnh bằng chứng + license |
| `anchors.txt` | `NNN.png\|câu neo nguyên văn trong script.txt` — BẮT BUỘC cho `assemble.py --anchors` |
| `colorize_map.txt` | `slot\|ảnh nguồn trong photos_src\|kích thước ima2` cho từng ảnh — **nguồn chân lý duy nhất** để biết tô ảnh nào, đừng tự suy luận từ tên file |
| `photos_src\` | Ảnh gốc đen trắng, chưa tô màu |
| `img\000.png` | Ảnh chính ĐÃ tô màu sẵn (bước 1) — dùng luôn, đừng tô lại |
| `voice_paced.wav` + `voice_paced.srt` | Giọng đọc đã giãn nhịp, phụ đề đã nắn khớp kịch bản |
| `TIEU_DE_MO_TA.txt` | Tiêu đề + mô tả + mốc chương thật — chép nguyên sang `listting.txt` khi giao hàng, không sửa |
| `thumb_text.txt` + `thumbnail_final.png` | Chữ phủ + ảnh bìa đã dựng xong |
| `BAN_GIAO_BUOC2.txt` | Bản tóm tắt riêng của tập đó — đọc trước, có thể có ghi chú đặc biệt cho tập này |

Thiếu bất kỳ file nào ở trên → **DỪNG, báo chủ dự án**, đừng đoán/tự tạo thay.

Số tập (`<nn>`) = **STT cột A** của trang tính, tab `irogatatarukioku`. Dòng sheet thật = STT + 1
(dòng 1 là tiêu đề). Ví dụ STT 5 nằm ở dòng sheet số 6.

---

## 3. ⭐ THẺ CHẠY — THEO ĐÚNG THỨ TỰ

Ví dụ dưới dùng tập `ep05-yamazaki-attu` (STT 5). Thay bằng slug + STT thật của tập bạn được giao.
Mọi lệnh chạy từ `E:\CLAUDE\YOUTUBE\h2dev`, Bash dùng `/` trong đường dẫn, luôn đặt trước:
```bash
export PYTHONIOENCODING=utf-8
```
(PowerShell: `$env:PYTHONIOENCODING="utf-8"; $env:PYTHONUTF8="1"`)

Đặt `EP=assets/irogatatarukioku/ep05-yamazaki-attu` cho gọn lệnh dưới đây.

### Lệnh 1 — tô màu các ảnh còn lại bằng `ima2`
Đọc `$EP/colorize_map.txt`: mỗi dòng (trừ dòng đã ghi "ĐÃ XONG Ở BƯỚC 1" và dòng bookend cuối) là
một ảnh cần tô. Gọi `ima2.cmd edit` cho từng ảnh:
```bash
"C:/Users/admin/AppData/Roaming/npm/ima2.cmd" edit "$EP/photos_src/<ảnh nguồn>" \
  --prompt "Colorize this black-and-white historical WWII photograph (<năm+trận đánh lấy từ series_ctx.txt>, Pacific War). Keep the composition, camera framing, every object, person's exact pose, position and count, background and setting completely unchanged pixel-for-pixel in layout -- do not add, remove, move, crop, or redraw anything. Only estimate and apply natural, historically plausible color. Preserve the original photographic grain, contrast and softness -- do not sharpen, no cinematic color grading, no vignette, no stylization. The result should look like a real color photograph taken at the time, not a painting." \
  --model gpt-5.6-luna --quality high --size <kích thước trong colorize_map.txt> \
  -o "$EP/img/<slot>.png" --json
```
- Kiểm `ima2 ping` trước (server phải `status:ready`, cổng `127.0.0.1:3333`). Không tự `ima2 serve`
  nếu server đã chạy — chỉ khởi động khi ping thất bại thật.
- Dòng cuối `colorize_map.txt` ghi "COPY of 000.png (bookend)" — đó **không phải** một ảnh cần tô,
  chỉ cần copy file `$EP/img/000.png` sang đúng số slot ghi trong dòng đó. Không gọi `ima2` cho slot
  này (tốn thời gian vô ích, dù không tốn tiền).
- Gọi tuần tự hoặc song song tối đa ~8 luồng đều an toàn (đã verify không rate-limit ở mức đó).
  Mỗi ảnh quality=high mất ~30–100 giây.
- Ảnh nào bị Azure/OAuth từ chối vì content-policy (thường do prompt nhắc quá thẳng từ chiến đấu/vũ
  khí) → rút bớt từ ngữ nhạy cảm trong prompt, mô tả trung tính hơn (vd "military equipment" thay vì
  "weapon", "aged document" thay vì nói rõ nội dung tài liệu), thử lại tối đa 3 lần. Vẫn lỗi → báo
  chủ dự án kèm tên ảnh, KHÔNG tự ý bỏ ảnh đó khỏi video.
- Xong đủ ảnh → đối chiếu: số file trong `img/` phải bằng đúng số dòng `anchors.txt`.

### Lệnh 2 — ghép video
```bash
py -3.13 pipeline/assemble.py --img "$EP/img" --audio "$EP/voice_paced.wav" \
  --srt "$EP/voice_paced.srt" --anchors "$EP/anchors.txt" --fit blur --burn-sub \
  --out "$EP/final.mp4"
```
`--fit blur` là bắt buộc (không phải tuỳ chọn) — nhiều ảnh tư liệu WW2 không đúng tỉ lệ 16:9, thiếu
cờ này sẽ CẮT MẤT nội dung ảnh (đã dính thật ở các tập trước). Đọc log: nếu in cảnh báo "N/M ảnh
lệch tỉ lệ khung" thì đó là chuyện bình thường, `--fit blur` đã xử lý, không phải lỗi.

### Lệnh 3 — QC hình khớp lời (B8Q)
```bash
py -3.13 pipeline/qc_visual.py video --mp4 "$EP/final.mp4" --srt "$EP/voice_paced.srt"
```
⚠️ **Bắt buộc dùng cờ `--srt`, KHÔNG dùng `--script`.** Thiếu `--srt` thì công cụ không lấy được câu
thoại tại từng mốc lấy mẫu, mọi mẫu sẽ tự động coi là "không có lời ở mốc này" và **bỏ qua hoàn toàn
việc gọi vision so khớp** — kết quả "ĐẠT, 0 vấn đề" khi đó là **số ảo** (đã dính lỗi này ở 4 tập
trước, xem mục 5.1). Lệnh đúng lấy 8 mẫu, trích khung hình, hỏi gemini-3.8-flash qua ramcloud "hình
này có khớp câu đang đọc không", chấm điểm 1–5, ngưỡng: trung bình <3,2/5 hoặc ≥30% mẫu ≤2 điểm mới
báo lỗi.

### Lệnh 4 — sinh `qc_facts.json` cho cổng B10
```bash
py -3.13 -c "
import sys, json
sys.path.insert(0, 'pipeline')
import qc_facts
script = open('$EP/script.txt', encoding='utf-8').read()
dossier = open('$EP/series_ctx.txt', encoding='utf-8').read()
result = qc_facts.kiem(script, dossier)
json.dump(result, open('$EP/qc_facts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
"
```
(B3F đã ĐẠT ở bước 1 rồi — bước này chỉ ghi lại kết quả ra file để B10 đọc, không phải chạy QC mới.)

### Lệnh 5 — nghiệm thu gói (B10)
```bash
py -3.13 pipeline/qc_final.py --slug "$EP" --profile irogatatarukioku
```
Kỳ vọng "0 phát hiện NẶNG". Rớt → xem mục 5.2.

### Lệnh 6 — giao hàng (B11)
```bash
py -3.13 pipeline/giao_hang.py --slug ep05-yamazaki-attu --profile irogatatarukioku
```
⚠️ `--slug` chỉ truyền **tên thư mục** (`ep05-yamazaki-attu`), KHÔNG truyền đường dẫn đầy đủ —
truyền cả đường dẫn sẽ bị tool tự ghép lần nữa thành đường dẫn sai (đã dính thật). Lệnh này copy
đúng 3 file (`final.mp4`, `thumbnail.png`, `listting.txt`) sang
`E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\ep05-yamazaki-attu\`. Tên thư mục giao hàng KHÔNG được
thừa tiền tố kiểu `ep5-ep05-...` — nếu thấy vậy là bug, báo chủ dự án.

### Lệnh 7 — phụ đề Việt (bản xem thử, đặt thẳng trong thư mục giao hàng)
1. Sinh `sentences_ja.json` (map câu → mốc thời gian thật) — script mẫu:
   ```python
   # đọc voice_paced.srt (khối cách nhau dòng trống; dòng 2 = "hh:mm:ss,mmm --> hh:mm:ss,mmm";
   # dòng 3 = chữ), nối chữ mọi cue BỎ khoảng trắng, ghi nhớ giây bắt đầu từng cue;
   # đọc script.txt nối các dòng không trống BỎ khoảng trắng — hai chuỗi PHẢI bằng nhau;
   # tách câu theo 。！？, với mỗi câu tra cue chứa ký tự đầu/cuối câu → suy ra giây bắt đầu/kết thúc;
   # ghi ra sentences_ja.json: [{"i":1,"start":..,"end":..,"ja":"..."}, ...]
   ```
2. Dịch từng câu sang tiếng Việt → `sentences_vi.json` (`{"1": "...", "2": "...", ...}`). Giữ đúng
   số liệu, tên riêng, và **giữ nguyên độ hedging** của câu gốc (vd "とされる/と伝えられている" dịch
   thành "được cho là/tương truyền rằng", KHÔNG khẳng định chắc như đang kể sự thật 100% nếu câu
   gốc không khẳng định).
3. Dựng `voice_vi_check.srt` từ `sentences_ja.json` (mốc thời gian) + `sentences_vi.json` (chữ Việt).
4. Burn phụ đề, dùng đúng đường dẫn ffmpeg này (không gọi `ffmpeg` trần — máy này không có trong
   PATH):
   ```bash
   FFMPEG="C:/Users/admin/AppData/Local/Programs/Python/Python313/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
   "$FFMPEG" -y -i "$EP/final.mp4" \
     -vf "subtitles=$EP/voice_vi_check.srt:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=40'" \
     -c:v libx264 -crf 20 -preset veryfast -c:a copy \
     "E:/CLAUDE/YOUTUBE/CHANEL/irogatatarukioku/ep05-yamazaki-attu/final_vi_phude.mp4"
   ```
   Ghi **thẳng vào thư mục giao hàng** (không phải thư mục tập trong `assets/`) — đây là bản để chủ
   dự án xem thử, khác `final.mp4` (bản đăng, phụ đề Nhật cháy sẵn từ Lệnh 2).

### Lệnh 8 — chuyển hồ sơ nghiên cứu sang `_DONE`
```bash
mv "E:/CLAUDE/YOUTUBE/SPACE_RESEARCH/output/_READY/d05-yamazaki-attu" \
   "E:/CLAUDE/YOUTUBE/SPACE_RESEARCH/output/_DONE/d05-yamazaki-attu"
```
(số `d05` khớp STT, xem cột E của dòng đó nếu không chắc tên thư mục hồ sơ.)

### Lệnh 9 — ghi cột G rồi báo chủ dự án
```bash
py -3.13 pipeline/ghi_cot_video.py --tab irogatatarukioku --dong 5 --thu   # xem trước
py -3.13 pipeline/ghi_cot_video.py --tab irogatatarukioku --dong 5        # ghi thật
```
`--dong` là **STT cột A** (script tự cộng ra dòng sheet thật). Công cụ này CHỈ ghi được cột G và tự
chặn: chưa có đủ 3 file trong thư mục giao hàng → từ chối; cột G dòng 1 không phải chữ "VIDEO" → dừng
(cột bị đổi chỗ); STT không khớp `--dong` → dừng; ô đã có sẵn giá trị → không đè trừ khi thêm
`--ghi-de`.

Ghi xong nó in ra đường dẫn — **đưa chính đường dẫn đó cho chủ dự án trong câu trả lời cuối cùng**,
kèm đường dẫn `final_vi_phude.mp4` để họ xem thử. Đường dẫn ghi vào ô là chuỗi thuần, không kèm dung
lượng/thời lượng/ghi chú.

---

## 4. `ima2` — CÁCH GỌI, KIỂM TRA, VÀ BẪY ĐÃ DÍNH

- Kiểm server: `ima2 ping` → kỳ vọng `status:ready`, cổng `127.0.0.1:3333`. Nếu chết, `ima2 serve`
  rồi thử lại — server dùng phiên OAuth ChatGPT Plus đã đăng nhập sẵn trên máy này, không cần login
  lại.
- **`--model` truyền TRẦN** (`gpt-5.6-luna`), KHÔNG thêm tiền tố `oauth/` khi gọi `ima2 edit` (khác
  cú pháp `ima2 gen --model oauth/...`) — sai cú pháp này báo lỗi rõ ràng, dễ nhận ra.
- **Luôn truyền `-s/--size` khớp tỉ lệ ảnh gốc.** Mặc định không truyền sẽ ép về ô vuông
  1254×1254, CẮT MẤT nội dung ảnh gốc nếu ảnh không vuông. `colorize_map.txt` đã tính sẵn size đúng
  cho từng ảnh — dùng nguyên, đừng tự đoán lại.
- Chi phí: **0đ** — dùng quota gói ChatGPT Plus qua OAuth, không phải API trả tiền theo ảnh. Không
  cần theo dõi số dư.
- Nếu `ima2` lỗi hạ tầng liên tục (không phải content-policy, không phải sai size) → báo chủ dự án,
  đừng tự chuyển sang `gpti2`/`vilao` mà không hỏi trước (mục 1.4).

---

## 5. SỔ TAY XỬ LÝ KHI RỚT

### 5.1 B8Q báo "ĐẠT" nhưng nghi ngờ là số ảo
Kiểm output có in ra dòng `sync_score` và mảng mẫu điểm số không. Nếu output CHỈ có
`{"problems": [], "infra": [], "info": {...}}` mà không có `sync_score` → bạn (hoặc lệnh trước) đã
quên `--srt`, cổng chưa thực sự chấm gì. Chạy lại đúng Lệnh 3 với `--srt`.

### 5.2 B8Q rớt thật (sync_score < 3,2 hoặc nhiều mẫu ≤2 điểm)
Mở phần `weak` trong output JSON — mỗi mẫu lệch có mốc giây + lý do model chấm. Nguyên nhân thường
gặp ở Lane D:
- Sai thứ tự ảnh trong `anchors.txt` so với nội dung ảnh thật trong `img/` (kiểm tay 2–3 mốc bị chê
  bằng cách mở đúng ảnh đó xem có khớp mô tả không).
- Ảnh tô màu bị model vẽ sai/thêm bớt chi tiết so với ảnh gốc (hiếm nhưng có thể) — so `img/NNN.png`
  với `photos_src/` tương ứng.
Sửa xong (đổi thứ tự anchor hoặc tô lại đúng 1 ảnh lỗi) → chạy lại từ **Lệnh 2** (ghép lại rồi Lệnh
3 lại). Rớt quá 2 lần liên tiếp với cùng lý do → dừng, báo chủ dự án kèm số liệu, đừng đoán tiếp.

### 5.3 B10 rớt (có phát hiện NẶNG)
Mở `qc_final.json` (nếu tool xuất ra) hoặc đọc thẳng phần in trên màn hình — mỗi phát hiện có mô tả
+ hướng sửa. Phần lớn là lỗi gói đăng tải, sửa được không cần ghép lại video:
- Ảnh bìa > 2 MB → nén lại `thumbnail_final.png` (nhưng đây là sản phẩm bước 1 — sửa xong phải báo
  lại chủ dự án, không tự sửa âm thầm vì đây thuộc mục cấm 1.3 nếu phải đổi nội dung/bố cục ảnh; nén
  dung lượng thuần không đổi nội dung thì được).
- Mốc chương sai luật YouTube (chương đầu ≠ 0:00, cách nhau <10s, chương cuối vượt độ dài video) →
  đây LÀ lỗi bước 1, báo lại, đừng tự sửa `TIEU_DE_MO_TA.txt`.
- Thiếu nguồn/ảnh bằng chứng không lên hình → đối chiếu `evidence.json` với ảnh thật đã dùng.

### 5.4 Lệnh chết giữa chừng / exit code ≠ 0
Đọc **dòng cuối của log**, đừng kết luận từ exit code. Kiểu hay gặp:
- `UnicodeEncodeError` → quên `PYTHONIOENCODING=utf-8`.
- `ima2.cmd` báo `--model must be one of: ...` → đang gọi `edit` với tiền tố `oauth/` sai cú pháp
  (xem mục 4).
- `FileNotFoundError` khi gọi `ima2` qua Python `subprocess` (không phải Bash trực tiếp) → phải gọi
  đúng file `C:\Users\admin\AppData\Roaming\npm\ima2.cmd` (không phải chỉ `ima2`) vì đây là shim
  `.cmd` của Windows, Python `subprocess.run(["ima2", ...])` không tự resolve được.
- Mọi lần thử đều báo **cùng một lý do giống hệt nhau** → nghi phép kiểm sai, không phải công cụ
  sai — báo lại thay vì tăng số lần thử.

---

## 6. SỐ ĐO THẬT (để biết bao giờ là "lâu bất thường")

Đo trên tập ~15–17 phút, 16–20 ảnh:

| Việc | Thời gian thật |
|---|---|
| Tô màu 1 ảnh qua `ima2` (quality=high) | 30–100 giây |
| Tô màu cả tập (16–19 ảnh, tuần tự) | 8–20 phút |
| Ghép video (Lệnh 2) | 2–5 phút |
| B8Q (8 mẫu, gọi vision) | 1–3 phút |
| B10 | dưới 10 giây |
| B11 | dưới 10 giây |
| Dịch + build + burn phụ đề Việt (Lệnh 7) | 3–6 phút (dịch) + 2–4 phút (ffmpeg) |
| **Tổng bước 2** | **20–40 phút** |

**Mọi báo cáo phải kèm số đo thời gian và kết quả từng cổng** — yêu cầu cứng của chủ dự án, ví dụ:
*"B8Q sync_score 4.1/5, 0/8 mẫu yếu, 2 phút. B10 0 phát hiện nặng."*

---

## 7. CHECKLIST XONG VIỆC

- [ ] Số ảnh trong `img/` khớp số dòng `anchors.txt`
- [ ] B8Q chạy với `--srt` (không phải `--script`), có `sync_score` thật trong output
- [ ] B10: 0 phát hiện NẶNG
- [ ] Thư mục `E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\ep<nn>-<slug>\` có đủ `final.mp4` +
      `thumbnail.png` + `listting.txt` **+ `final_vi_phude.mp4`**
- [ ] Hồ sơ nghiên cứu đã chuyển sang `SPACE_RESEARCH\output\_DONE\`
- [ ] Ô **G** đúng dòng (STT+1) đã ghi đường dẫn thuần qua `ghi_cot_video.py`
- [ ] Đã đưa đường dẫn thư mục giao hàng cho chủ dự án trong câu trả lời, kèm số đo thời gian và kết
      quả các cổng

---

## 8. TRA CỨU NHANH

| Thứ | Ở đâu |
|---|---|
| Thư mục gốc dự án | `E:\CLAUDE\YOUTUBE\h2dev` |
| Thư mục tập (Lane D) | `E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\ep<nn>-<slug>\` |
| Thư mục giao hàng (Lane D) | `E:\CLAUDE\YOUTUBE\CHANEL\irogatatarukioku\ep<nn>-<slug>\` |
| Trang tính + tab | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`, tab **`irogatatarukioku`** |
| Profile | `profiles/profiles/irogatatarukioku.json` |
| `ima2` server | `127.0.0.1:3333`, thực thi `C:\Users\admin\AppData\Roaming\npm\ima2.cmd` |
| ffmpeg thật (không có trong PATH) | `C:\Users\admin\AppData\Local\Programs\Python\Python313\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe` |
| Ghi cột G (có rào chắn) | `pipeline\ghi_cot_video.py --tab irogatatarukioku --dong <STT>` |
| Hồ sơ nghiên cứu gốc | `E:\CLAUDE\YOUTUBE\SPACE_RESEARCH\output\_READY\d<nn>-<slug-research>\` → xong chuyển `_DONE\` |
| Python | `py -3.13` |

**Số tập = STT cột A**, thư mục luôn `ep<nn>-<slug>` chữ Latin (`ep05-yamazaki-attu`) — chủ dự án gõ
đường dẫn tay để vào lấy file, đừng đặt tên tiếng Nhật.

---

## 9. KHI NÀO PHẢI DỪNG VÀ HỎI (thay vì tự quyết)

- Thiếu file bước 1 liệt kê ở mục 2.
- `ima2` từ chối ảnh vì content-policy sau 3 lần thử đổi prompt.
- B8Q rớt quá 2 lượt ghép lại với cùng lý do.
- B10 có phát hiện NẶNG mà bạn không chắc cách sửa, hoặc phát hiện đó đòi sửa file thuộc bước 1
  (mục 1.3 cấm tự sửa).
- Bạn thấy kịch bản/giọng đọc/mốc chương có vẻ sai — báo, tuyệt đối không tự sửa.
- Lệnh nào đó đòi tiền/API key ngoài `ima2`, hoặc bạn không chắc nó có tốn tiền không.
- Chủ dự án giao việc mà không nói rõ STT/tập nào.
- Bất kỳ lúc nào bạn không chắc một đường dẫn có thuộc Lane D (`irogatatarukioku`) hay lane khác.

Khi báo, luôn kèm: **tập nào (STT + slug)** · **đang ở bước nào** · **dòng log/số liệu thật** ·
**bạn định làm gì tiếp**. Đừng viết "có lỗi" suông.
