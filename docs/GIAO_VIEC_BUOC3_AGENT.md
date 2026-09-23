# HỒ SƠ GIAO VIỆC — BƯỚC 3: GHÉP VIDEO & GIAO HÀNG (lane `toshi-densetsu-jp`)

> **Đọc hết file này trước khi gõ lệnh đầu tiên.** File tự chứa: mọi đường dẫn, lệnh, ngưỡng và
> cách xử lý khi rớt cổng đều nằm ở đây. Bạn KHÔNG cần đọc file nào khác để làm xong việc.
> Giao cho: **agent bước 3** (hiện tại là agent deepseek). Viết ngày 2026-09-12.

> ⚠️ **DỰ ÁN CÓ HAI RUNBOOK BƯỚC 3 — MỞ ĐÚNG CÁI CỦA LANE MÌNH.** Hai lane chạy hai bộ công cụ
> khác hẳn nhau, CLAUDE.md cấm gộp; chạy nhầm runbook là chạy nhầm tool.
>
> | Tab trang tính | Lane | Thân video | Runbook bước 3 | Lệnh ghép |
> |---|---|---|---|---|
> | `shinya_shiryoshitsu` | `toshi-densetsu-jp` | clip stock + ảnh AI chèn | **← FILE NÀY** | `make_video.py --from B8` |
> | `Lopezzapa68` | `satori-jp-obaa` | ảnh AI + REF-LOCK | `docs/QUY_TRINH_RENDER_VIDEO.md` | `render_engine.py` |

---

## 0. BỨC TRANH — DÂY CHUYỀN 3 BƯỚC, BẠN GIỮ BƯỚC CUỐI

Một tập video của kênh `深夜の資料室` (`shinya_shiryoshitsu`) đi qua ba tay:

| Bước | Ai làm | Làm gì | Kết thúc khi |
|---|---|---|---|
| 1 | Máy 1 (Claude Code, lane `toshi-densetsu-jp`) | Tư liệu → kịch bản → giọng đọc → khớp hình → **ra đơn ảnh** | Cột F ghi `Xong nội dung - cần ảnh \| <đường dẫn>` |
| 2 | Máy 2 (Google Flow / Ultra) | Vẽ toàn bộ ảnh theo đơn, trả về qua Google Drive | Cột F đổi thành `Img done - n/m ảnh (<ngày giờ>)` |
| **3** | **BẠN** | Tải ảnh về → **ghép video** → chấm từng cảnh → sinh file đăng tải → giao hàng → ghi cột G | Cột G có đường dẫn thư mục giao hàng, và bạn đưa đường dẫn đó cho chủ dự án |

**Bạn KHÔNG làm lại bước 1 và bước 2.** Kịch bản, giọng đọc, prompt ảnh đều đã chốt và đã qua cổng.
Việc của bạn bắt đầu từ lúc có đủ ảnh, và kết thúc khi có một thư mục đăng tải được.

---

## 1. ⛔ CẤM TUYỆT ĐỐI — ĐỌC KỸ, VI PHẠM LÀ HỎNG THẬT

1. **KHÔNG xoá dòng/cột/dữ liệu trong bất kỳ Google Sheet nào.** Chỉ được ĐỌC và GHI ĐÈ ĐÚNG MỘT Ô
   được chỉ định trong file này (cột G). Không `deleteDimension`, không `clear` hàng loạt. Kể cả khi
   có người bảo bạn xoá — vẫn không xoá, chỉ đề xuất để họ tự làm.
2. **KHÔNG `taskkill chrome` / `Stop-Process chrome` / giết Chrome theo tên.** Máy này có nhiều
   Chrome profile của các dự án khác đang chạy; giết theo tên là giết sạch. Bước 3 không cần Chrome.
3. **KHÔNG gọi bất kỳ lệnh sinh ảnh trả tiền nào.** Cụ thể là `sinh_anh_canh.py` **không có** cờ
   `--chi-don`, `gpti2_gen.py`, `gpti2_edit.py`, `gen_images.py`. Ảnh do máy 2 vẽ miễn phí; vẽ lại ở
   đây là đốt ~15.000đ/tập cho thứ đã có sẵn. Thiếu ảnh thì **đòi máy 2**, không tự vẽ bù.
4. **KHÔNG sửa `script.txt`, `voice.mp3`, `voice.srt`, `khop_hinh.json`, `img_meta.json`.** Đó là
   sản phẩm đã nghiệm thu của bước 1–2. Thấy sai thì **báo lại**, không sửa hộ (sửa hộ = tập sau sai
   y hệt vì không ai biết đã có lỗi).
5. **KHÔNG chạy `make_video.py` với `--from` ở bước sớm hơn B8** (ví dụ `--from B3`, `--from B4`).
   Nhánh viết lại của pipeline sẽ **XOÁ** `script.txt` + `voice.mp3` + `voice.srt`. Đã mất một lần
   thật rồi. Bước 3 chỉ dùng `--from B8`.
6. **KHÔNG ghi cột G khi chưa giao hàng xong thật.** Ghi sớm = chỉ chủ dự án vào một thư mục rỗng.

---

## 2. ĐIỀU KIỆN ĐƯỢC PHÉP BẮT ĐẦU

**Việc được giao qua TRANG TÍNH, không qua tin nhắn.** Mở tab kênh, đọc **cột H (GHI CHÚ)**: dòng
nào có đơn `BƯỚC 3 — GHÉP VIDEO & GIAO HÀNG` là việc của bạn. Đơn đó tự chứa đường dẫn thư mục tập,
số ảnh phải có, và đúng các lệnh phải chạy — nó do máy 1 sinh tự động từ profile + thư mục thật, nên
**tin đơn trong cột H hơn tin trí nhớ**. File này giải thích *vì sao* và *rớt thì làm gì*.

Chỉ bắt đầu khi **cả ba** điều sau đúng:

1. Cột **H** của dòng đó có đơn bước 3, và chủ dự án đã bảo bạn vào làm.
   Nếu họ nói rõ dòng: *"làm bước 3 cho dòng `<n>`"* — `<n>` là **số STT ở cột A**, không phải số
   dòng Google Sheet (STT 2 nằm ở dòng 3 vì dòng 1 là tiêu đề). Muốn tự dò dòng nào đang chờ:
   ```powershell
   py -3.13 pipeline\quet_dong_can_anh.py --tab shinya_shiryoshitsu --dong 1-20 --cho-ghep --lenh
   ```
   **Cấm tự chạy cả tab mà không có dải dòng.**
2. Cột **F (STATUS-IMG)** của dòng đó ghi `Img done - n/m ảnh (...)`.
   - Nếu ghi `LỖI: ...` → **DỪNG**, báo chủ dự án, không tự xử lý.
   - Nếu ghi `Đang tạo ảnh (máy 2, ...)` → máy 2 chưa xong, chờ.
3. Cột **G (VIDEO)** của dòng đó đang **trống**. Có sẵn đường dẫn nghĩa là tập đã giao rồi — hỏi lại
   trước khi làm đè.

**Trang tính:** ID `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`, tab `shinya_shiryoshitsu`.
Thứ tự cột: **A** STT · **B** ĐỀ TÀI · **C** NỘI DUNG · **D** TÌNH TRẠNG · **E** FOLDER ·
**F** STATUS-IMG · **G** VIDEO · **H** GHI CHÚ.
⚠️ Cột VIDEO **đã đổi từ F sang G** ngày 2026-09-12. **Đọc lại dòng tiêu đề trước khi ghi**, đừng ghi
theo trí nhớ — ghi nhầm vào F là đè mất trạng thái ảnh của máy 2.

---

## 3. ⭐ THẺ CHẠY — 6 LỆNH, THEO ĐÚNG THỨ TỰ

Ví dụ dưới dùng tập `ep02-walton` (STT 2). Thay `ep02-walton` bằng slug của tập bạn được giao.

Mọi lệnh chạy từ thư mục gốc dự án `E:\CLAUDE\YOUTUBE\h2dev`, và **luôn đặt 2 biến môi trường này
trước** (thiếu nó là tiến trình con chết vì không in nổi tiếng Nhật, mà báo lỗi lại giống hệt lỗi
mạng — đã mất thời gian truy nhầm hướng một lần):

```powershell
$env:PYTHONIOENCODING="utf-8"; $env:PYTHONUTF8="1"
```

### Lệnh 0 — tra slug từ số dòng (đừng đoán tên thư mục)
```powershell
py -3.13 pipeline\quet_dong_can_anh.py --tab shinya_shiryoshitsu --dong <n> --cho-ghep --lenh
```
**Bắt buộc có `--cho-ghep`** — không có cờ đó, script chạy ở chế độ của máy 2 (tìm dòng *cần ảnh*)
và sẽ **bỏ qua đúng dòng bạn cần** rồi thoát với exit 1. Chế độ `--cho-ghep` tìm dòng ngược lại:
cột F = `Img done` **và** cột G còn trống, tức là đang chờ ghép.

Nó in ra slug đúng + lệnh tải sẵn để copy. **Dùng slug nó in ra**, đừng tự ghép tên thư mục.
Slug được dò từ **thư mục tập trên đĩa** (`ep<nn>-*` trong đúng lane của tab), không lấy từ cột E —
vì cột E là đường dẫn **hồ sơ nghiên cứu** (`_READY\02-walton`), khác tên với thư mục tập
(`ep02-walton`). Và cột F thì không dùng được nữa: máy 2 ghi đè trạng thái `Img done` lên, đường
dẫn máy 1 để lại trong đó biến mất.

### Lệnh 1 — tải ảnh máy 2 vẽ về đúng chỗ
```powershell
py -3.13 pipeline\drive_handoff.py download-result ep02-walton "E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\img_ai"
```
Tải **thẳng vào `img_ai`** — không tải ra thư mục tạm rồi copy tay (dễ copy thiếu/nhầm).

### Lệnh 2 — ĐỐI CHIẾU SỐ LƯỢNG (bắt buộc, đừng bỏ)
```powershell
$d = "E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\img_ai"
$can = (Get-Content "$d\prompts.txt" | Where-Object { $_.Trim() }).Count
$co  = (Get-ChildItem "$d\*.png").Count
Write-Output "can $can anh / co $co anh"
```
- `$co` = `$can` → đi tiếp.
- `$co` < `$can` → **DỪNG**. Đây là việc của máy 2. Xem mục 5.1.
- Đừng đổi tên ảnh khác để "cho đủ": tên file là thứ **duy nhất** nối tấm ảnh với đoạn lời, đổi tên
  là làm sai toàn bộ từ chỗ đó trở đi mà không cổng nào bắt được.

### Lệnh 3 — GHÉP + CHẤM + GIAO HÀNG (một lệnh, chạy hết B8 → B11)
```powershell
py -3.13 pipeline\make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8
```
Lệnh này lần lượt: **B8** ghép video → **B8Q** chấm từng cảnh → **B9** sinh file đăng tải →
**B10** nghiệm thu cả gói → **B11** dựng bản xem thử tiếng Việt + chép 3 file sang thư mục kênh.
Chạy lâu (xem mục 6), cứ để chạy hết, đừng cắt ngang.

### Lệnh 4 — kiểm lại bằng mắt trước khi báo xong
```powershell
Get-ChildItem "E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton"
py -3.13 -c "import json;print(json.dumps(json.load(open(r'E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\state.json',encoding='utf-8')).get('B11'),ensure_ascii=False))"
```
Thư mục kênh phải có `final.mp4`, `thumbnail.png`, `listting.txt` và `final.mp4` phải **mới hơn**
lần ghép. Chưa có đủ = chưa giao xong, **chưa được ghi cột G**.

### Lệnh 5 — ghi cột G rồi báo chủ dự án
**Dùng đúng công cụ này, đừng tự mở Google Sheets ghi tay:**
```powershell
py -3.13 pipeline\ghi_cot_video.py --tab shinya_shiryoshitsu --dong <n> --thu   # xem trước
py -3.13 pipeline\ghi_cot_video.py --tab shinya_shiryoshitsu --dong <n>         # ghi thật
```
`--dong` là **STT cột A** (script tự cộng bù ra dòng sheet). Công cụ này chỉ ghi được **duy nhất
cột G** và tự chặn 4 kiểu sai trước khi ghi:
- chưa có thư mục giao hàng, hoặc thiếu 1 trong 3 file → **từ chối ghi**;
- cột G dòng 1 không phải chữ `VIDEO` (cột bị đổi chỗ) → **dừng**, tránh đè nhầm cột F;
- STT ở dòng đó không khớp `--dong` (trang tính xê dịch) → **dừng**;
- ô G đã có sẵn giá trị → **không đè im lặng**, muốn đè phải thêm `--ghi-de`.

Ghi xong nó in ra đường dẫn — **đưa chính đường dẫn đó cho chủ dự án trong câu trả lời**, họ mở thư
mục để đăng lên YouTube. Ghi sheet mà không nói thì họ không biết để vào lấy; nói mà không ghi thì
lần sau không biết tập nào đã xong. Đường dẫn ghi vào ô là **chuỗi thuần**, không kèm dung lượng,
thời lượng hay ghi chú.

---

## 4. CÁC CỔNG — Ý NGHĨA, NGƯỠNG, VÀ Ý ĐỒ ĐẰNG SAU

Cổng ở đây **không phải thủ tục giấy tờ**. Mỗi cổng sinh ra sau một lần hỏng thật.

| Cổng | Hỏi điều gì | Ngưỡng | Rớt thì sao |
|---|---|---|---|
| **B8Q** `qc_canh.py` | *Hình đang chiếu có thuộc về câu đang đọc không?* Chấm **100% số cảnh** (~400 cảnh/tập), mỗi cảnh một khung hình + đúng câu đọc lúc đó | **lạc ≤ 3%** (`profile.assemble.lac_toi_da`) | Dừng, in ra mốc giây từng cảnh lạc → mục 5.2 |
| **B10** `qc_final.py` | *Bộ này ĐĂNG LÊN ĐƯỢC chưa?* Ảnh bìa có vượt 2 MB không · tiêu đề có trong dải của ngách không · mốc chương có đúng luật YouTube không · sổ nguồn có đủ file đã dùng không | **0 phát hiện NẶNG** | Dừng, đọc `qc_final.json` → mục 5.3 |

**Vì sao B8Q soi 100% chứ không lấy mẫu** — đây là bài học đắt nhất của lane này, đừng tự ý "tối ưu"
xuống lấy mẫu cho nhanh: cổng cũ lấy mẫu 12/400 mốc (3%) và **cố ý tắt hẳn phép kiểm khớp lời** với
lý do "b-roll là hình trang trí". Kết quả: tập 3 đi hết pipeline với **43/141 cảnh (30%) lạc hẳn
lời**, cổng báo *0 vấn đề*, chủ dự án xem 5 phút là thấy. Cổng lấy mẫu trả lời được "video có hỏng
toàn tập không", **không** trả lời được "cảnh nào hỏng".

**Ngưỡng 3% không phải con số cho đẹp:** đặt 0 thì không bao giờ dừng được, vì chính bộ chấm cũng
chặt tay ở vài cảnh thật ra đúng. 3% là mức đo được sau 4 vòng sửa ở tập 3.

**Mức tốt trông như thế nào** (hai tập đã giao, dùng để so):

| Tập | Số cảnh | Lạc | Tỉ lệ | Thời lượng |
|---|---|---|---|---|
| `ep01-valentich` | 416 | 5 | **1,2%** | 29,9′ |
| `ep03-bob-lazar` | 384 | 8 | **2,08%** | ~28′ |

Ra 6–8% là có chuyện thật, đừng `--force-qc` cho qua.

---

## 5. SỔ TAY XỬ LÝ KHI RỚT

### 5.1 Thiếu ảnh (Lệnh 2 báo `$co` < `$can`)
Đây **không phải** việc của bạn. Làm đúng ba việc:
1. Chạy lại `download-result` một lần nữa — có thể đứt mạng giữa chừng.
2. Vẫn thiếu → liệt kê **tên file thiếu** (`001.png`, `047.png`…) bằng cách so `prompts.txt` với các
   `.png` có thật.
3. Báo chủ dự án kèm danh sách đó. **Không tự vẽ bù, không đổi tên ảnh khác thay vào.**

Pipeline cũng tự chặn: bước B5A thấy `img_ai/` thiếu so với `img_meta.json` sẽ dừng hẳn với dòng
`✗ B5A: thiếu ảnh so với img_meta.json`.

### 5.2 B8Q rớt (lạc > 3%)
Mở `<thư mục tập>\qc_canh.json` — mỗi cảnh lạc có `t0` (giây), `file` (clip/ảnh nào), `ta` (model
mô tả nó thấy gì). Trước khi làm gì, **mở `review_vi.mp4` xem thử vài mốc đó** để biết cổng nói đúng
hay chấm oan.

Điều quan trọng cần biết: **B8Q đã tự động cấm file lạc rồi.** Nó chạy kèm `--cam-file-lac`, ghi
những clip đã chứng minh là lạc vào `soi_kho.json` của kho hình (luật cấm: *lạc ≥1 lần VÀ chưa từng
được chấm đúng*). Nghĩa là **chỉ cần ghép lại là lần này nó không bốc những clip đó nữa**:

```powershell
py -3.13 pipeline\make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8
```

- Chạy lại **tối đa 2 lượt**. Mỗi lượt tỉ lệ lạc phải **giảm rõ**. 
- Giảm chậm hoặc không giảm sau 2 lượt → **DỪNG, báo chủ dự án**. Lúc đó vấn đề nằm ở chỗ kho hình
  không có thứ cần cho những đoạn đó, và cách chữa là **đặt máy 2 vẽ thêm ảnh cho đúng những đoạn
  ấy** — việc đó thuộc bước 1–2, không phải bước 3.
- **Tuyệt đối không** chạy `sinh_anh_canh.py --theo-qc` (không có `--chi-don`): lệnh đó vẽ ảnh **trả
  tiền**.
- **Tuyệt đối không** dùng `--force-qc` để cho qua. Cổng này sinh ra chính vì một lần "cho qua".

### 5.3 B10 rớt (có phát hiện NẶNG)
Mở `<thư mục tập>\qc_final.json`, mỗi phát hiện có mô tả và hướng sửa. Phần lớn là lỗi **gói đăng
tải**, sửa được tại chỗ mà không phải dựng lại video:
- Ảnh bìa > 2 MB → nén lại `thumbnail.png`.
- Mốc chương sai luật → sửa trong `DANG-TAI.txt` / `TIEU_DE_MO_TA.txt`.
- Thiếu nguồn trong `listting.txt` → kiểm `credits.txt`.

Sửa xong chạy lại `--from B9` (không cần `--from B8`, khỏi ghép lại video 30 phút).
Gặp phát hiện nặng mà bạn không chắc cách sửa → **báo, đừng đoán**.

### 5.4 Lệnh chết giữa chừng / exit code ≠ 0
Đọc **dòng cuối của log**, đừng kết luận từ exit code. Ba kiểu hay gặp:
- `UnicodeEncodeError` / lỗi in tiếng Nhật → bạn quên đặt `PYTHONIOENCODING`/`PYTHONUTF8` (mục 3).
- `✗ chưa có final.mp4` → một bước phía trước chưa chạy, không phải lỗi của bước đang chạy.
- Mọi lần thử đều báo **cùng một lý do giống hệt nhau** → nghi **phép kiểm sai**, không phải công cụ
  sai. Ba model khác nhau không thể hỏng giống nhau đến từng ký tự. Báo lại thay vì tăng số lần thử.

---

## 6. SỐ ĐO THẬT — ĐỂ BIẾT BAO GIỜ LÀ "LÂU BẤT THƯỜNG"

Đo trên tập ~30 phút, ~400 cảnh, máy 1:

| Việc | Thời gian thật |
|---|---|
| `download-result` ~300 ảnh | 3–8 phút (tuỳ mạng) |
| B8 ghép video | 8–15 phút |
| B8Q chấm 100% cảnh (~400 lượt gọi vision) | 10–20 phút |
| B9 + B10 | dưới 1 phút |
| B11 dựng bản xem thử tiếng Việt + chép | 8–15 phút |
| **Tổng bước 3** | **35–60 phút** |

Quá gấp đôi các mức trên mà không có tiến triển trong log → dừng lại xem, đừng chờ vô hạn.

**Mọi báo cáo của bạn phải kèm số đo thời gian** — đây là yêu cầu cứng của chủ dự án, không phải
tuỳ chọn. Đặt con số bên cạnh kết luận, ví dụ *"B8Q 416/416 cảnh, lạc 5 (1,2%), 14 phút"*.

---

## 7. BẢN XEM THỬ TIẾNG VIỆT — THỨ ĐỂ NGƯỜI TA KIỂM TRA BẠN

Bản đăng lên YouTube **không cháy phụ đề** và toàn bộ lời là tiếng Nhật, nên không ai bên mình xem
lại được nội dung. `review_vi.mp4` (480p, phụ đề Việt cháy vào hình) là bản để đọc.

⚠️ **Một bẫy đã dính thật:** bản dịch `voice.vi.srt` cũ hơn `voice.srt` nghĩa là **phụ đề của một
bản ghi khác** — xem để đối chiếu thì thành kết luận sai. Pipeline nay tự dịch lại khi phát hiện
lệch, nhưng nếu bạn thấy dòng cảnh báo `⚠️ voice.vi.srt CŨ HƠN voice.srt` thì cứ để nó dịch lại,
đừng bỏ qua cho nhanh.

---

## 8. CHECKLIST XONG VIỆC — ĐỦ CẢ 7 Ô (+1 Ô HOOK NẾU TẬP CÓ `hook\`) MỚI ĐƯỢC BÁO "XONG"

- [ ] Số ảnh nhận về **khớp** số dòng `prompts.txt`
- [ ] `state.json` có **B8, B8Q, B9, B10, B11**
- [ ] B8Q: tỉ lệ lạc **≤ 3%**, và **0 lỗi hạ tầng** (lỗi hạ tầng = cổng không chạy được, khác hẳn
      cổng chạy được và chấm sạch — "0 vấn đề" vì cổng chết là **số ảo**)
- [ ] B10: **0 phát hiện NẶNG**
- [ ] Thư mục `E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep<nn>-<slug>\` có đủ `final.mp4` +
      `thumbnail.png` + `listting.txt`
- [ ] Ô **G** đúng dòng đã ghi đường dẫn thuần
- [ ] Đã **đưa đường dẫn** cho chủ dự án trong câu trả lời, kèm số đo thời gian và kết quả các cổng
- [ ] Nếu tập có `<thư mục tập>\hook\hook_storyboard.json` (bước 1 đã khoá hook VÀ đã sinh
      storyboard) → làm thêm **mục 9 dưới đây** (dựng `hook_final.mp4` + `final_with_hook.mp4`)
      TRƯỚC khi báo xong; không có file này thì bỏ qua mục 9, không phải lỗi.
      ⚠️ 2026-09-23: điều kiện đổi từ "có thư mục `hook\`" sang "có `hook\hook_storyboard.json`" —
      từ bản vá này, thư mục `hook\` LUÔN tồn tại ngay khi kênh bật tính năng hook (chứa
      `hook_locked.txt`/`hook_lock.json` từ lúc khoá hook, TRƯỚC KHI viết thân), nên chỉ dựa vào
      "có thư mục `hook\`" sẽ kích hoạt mục 9 sớm hơn lúc storyboard thật sự sẵn sàng.

---

## 9. HOOK 20–30S ĐẦU VIDEO (mọi lane, từ 2026-09-23)

> Mục này chỉ áp dụng cho tập có bước 1 sinh sẵn thư mục `hook\` (không phải mọi tập). `<tập>` dưới
> đây là thư mục của đúng tập đang làm, ví dụ thật:
> `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton` — nghĩa là đường dẫn đầy đủ
> `<tập>\hook\hook_locked.txt` ở ví dụ đó là
> `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\hook\hook_locked.txt`.

Đầu vào (bước 1 đã để sẵn trong `<tập>\hook\`): `hook_locked.txt` · `hook_lock.json` (`mode`
upstream|repair) · `hook_storyboard.json` · `flow_prompts\shot_NN.txt` · `grok_jobs.csv`. Thiếu bất
kỳ file nào → DỪNG, báo lane (xem mục 11).

> 2026-09-23: `hook_storyboard.json` + `flow_prompts\shot_NN.txt` + `grok_jobs.csv` nay được
> **TỰ ĐỘNG sinh** bởi luồng bình thường của bước 1 (`make_video.py` gọi `hook_storyboard.sinh()`
> ngay ở bước ghi tài sản B5W, ngay sau khi có `characters.json`) — không còn cần ai chạy tay.
> Lệnh `py -3.13 E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_storyboard.py --profile <lane> --slug <tập>`
> giờ CHỈ dùng khi cần **sinh lại tay** (vd storyboard cũ lỗi, muốn ép sinh lại bằng `--force`, hoặc
> đang gỡ lỗi riêng bước này) — nếu vẫn thiếu `hook_storyboard.json` sau khi bước 1 báo xong thì đó
> là dấu hiệu bước 1 gặp lỗi khi sinh (xem cảnh báo trong log B5W), chạy lại lệnh trên rồi đối
> chiếu `hook\hook_storyboard.err.json` (nếu có) trước khi báo lane.

**9.1 Ảnh shot — do MÁY 2 vẽ, bạn chỉ kiểm đủ** — đây KHÔNG phải ngoại lệ của luật mục 1: bạn vẫn
không bao giờ tự vẽ ảnh, kể cả ảnh shot hook. `<tập>\hook\flow_prompts\shot_NN.txt` và
`<tập>\hook\grok_jobs.csv` là đơn máy 1 đã để sẵn cho máy 2 vẽ cùng đợt với ảnh thân video, ra
`<tập>\hook\img\shot_NN.png` (1280×720, 16:9; shot nào có `ref_image=REF`/`REF2` trong
`hook_storyboard.json` thì máy 2 REF-LOCK bằng ảnh master trong `<tập>\_ref\`). Việc của bạn: đếm số
file `shot_NN.png` đã có trong `<tập>\hook\img\` phải khớp đúng số dòng trong `grok_jobs.csv`
(thường 4–7 ảnh) — **thiếu ảnh thì DỪNG và đòi máy 2**, giống hệt cách xử lý thiếu ảnh thân video ở
mục 1, không tự vẽ bù.
> **Ngoại lệ duy nhất:** lane `toshi-densetsu-jp` có ngoại lệ tự render riêng đã được chủ dự án
> chốt (xem `docs/SOP_TOSHI_DENSETSU_JP.md` §Ngoại lệ tự render) — nếu chính tab Lane A đang tự làm
> cả bước 2+3 cho tập của mình thì được tự vẽ ảnh shot hook. Agent bước 3 độc lập (không phải Lane A
> tự làm) và mọi lane khác thì không có ngoại lệ này.

**9.2 Clip** — chạy:
```
python E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py --jobs <tập>\hook\grok_jobs.csv --out <tập>\hook\clips --gap 5
```
(profile Grok cổng 9334; lỗi 429/403 xem skill `C:\Users\admin\.claude\skills\grok_video.md`).
Fallback khi Grok chết hẳn: dùng ảnh tĩnh + hiệu ứng chuyển cảnh thay clip động, qua
`C:\Users\admin\.claude\skills\video-chuyen-canh\scripts\ghep_anh_co_chuyen_canh.py --zoom 1.0`
với timeline lấy từ mốc `t0`/`t1` của từng shot trong `hook_storyboard.json` (xem thiết kế V3 ở
`E:\CLAUDE\YOUTUBE\h2dev\docs\PHUONG_AN_HOOK_VIDEO.md`).

**9.3 Voice hook:**
- **upstream**: KHÔNG làm gì — hook nằm trong `voice.mp3` chung của tập (là đoạn đầu). Lấy mốc kết
  thúc hook = cue cuối cùng trong `<tập>\voice_paced.srt` có nội dung thuộc hook, gọi mốc đó là
  `T_hook`.
- **repair**: chạy
  ```
  py -3.13 E:\CLAUDE\YOUTUBE\h2dev\pipeline\tts.py --script <tập>\hook\hook_locked.txt --out <tập>\hook\hook_voice.mp3 --profile <lane>
  ```
  (cùng `--voice`/`--speed`/`--fx` của profile lane đang làm, xem `pipeline\tts.py --help` hoặc
  channel.json của lane) → sinh `hook_voice.mp3` + `hook_voice.srt`; `T_hook` = thời lượng mp3 đó.

**9.4 Dựng `<tập>\hook\hook_final.mp4`** (dùng `imageio_ffmpeg.get_ffmpeg_exe()` như
`pipeline\assemble.py`, xuất 1920×1080 30fps h264 yuv420p — cùng thông số `final.mp4`):
- Với mỗi shot n: cắt clip `<tập>\hook\clips\shot_NN.mp4` đúng `t1-t0` giây (`-ss 0 -t <dur>`),
  scale/pad về 1920×1080. Clip ngắn hơn `dur` (kể cả clip tĩnh ở fallback 9.2) → đắp thêm bằng
  `tpad=stop_mode=clone:stop_duration=<thiếu>`.
- Nối các shot theo concat demuxer; giữa 2 shot dùng crossfade 12 khung (xfade `offset` = tổng thời
  lượng các shot trước − 0.4s) — công thức đúng nằm ở skill
  `C:\Users\admin\.claude\skills\video-chuyen-canh\SKILL.md` (xfade trả về `d−1` khung nên phải cấp
  `d+1` rồi cắt lại bằng `-frames:v`).
- Tổng khung của `hook_final.mp4` phải = `round(T_hook × 30)` ± 15 khung; thừa khung → cắt bớt ở
  shot cuối; thiếu khung → nhân bản khung cuối (không dùng zoom/pan để bù, xem luật cấm hiệu ứng
  giật/rung của dự án).
- Âm thanh: **repair** → ghép `hook_voice.mp3`; **upstream** → KHÔNG ghép tiếng (tiếng đã nằm sẵn
  trong thân video, xem 9.5). Nhạc nền hook: dùng cùng file BGM của thân video nhưng hạ **−6 dB**,
  fade-in 1 giây; SFX không bắt buộc (không cần tiếng whoosh kiểu trailer).

**9.5 Ghép vào thân video** — xuất `<tập>\final_with_hook.mp4`:
- **upstream**: `final.mp4` đã chứa sẵn đoạn hook dựng bằng ảnh tĩnh ở khoảng 0–`T_hook` → THAY
  đúng đoạn đó: `final_with_hook.mp4` = phần video của `hook_final.mp4` + phần video của `final.mp4`
  tính từ `T_hook` trở đi, còn **âm thanh lấy nguyên của `final.mp4` từ giây 0** (không cắt/không
  dịch tiếng), nối bằng chuyển cảnh mờ-vào 10 khung tại đúng mốc `T_hook`.
- **repair**: `final_with_hook.mp4` = `hook_final.mp4` (đã có tiếng riêng) + chuyển cảnh crossfade
  17 khung + toàn bộ `final.mp4` giữ nguyên vẹn (cả hình lẫn tiếng).
- Xuất file **CẠNH** `final.mp4` trong cùng thư mục `<tập>\`, **KHÔNG ghi đè** `final.mp4`.
- Phụ đề: **repair** → nối `hook_voice.srt` (giữ nguyên mốc) rồi dịch **mọi** mốc thời gian của
  `voice_paced.srt` cộng thêm `T_hook + 17/30` giây → ghi ra `<tập>\final_with_hook.srt`. **upstream**
  → phụ đề cũ đã đúng mốc (hook nằm trong voice.mp3 gốc), chỉ copy `voice_paced.srt` thành
  `final_with_hook.srt` không cần dịch mốc.

**9.6 Nghiệm thu:**
- Đếm khung `final_with_hook.mp4` phải = khung(`hook_final.mp4`) + khung(`final.mp4` tính từ
  `T_hook`) − số khung của đoạn chuyển cảnh dùng ở 9.5.
- Chạy cổng nghe `E:\CLAUDE\YOUTUBE\h2dev\pipeline\qc_visual.py::kiem_tieng_ghep` trên
  `final_with_hook.mp4` — không được báo mất tiếng ở mốc ghép.
- Xem tay 30 giây đầu: đủ 4–7 bố cục khác nhau theo `hook_storyboard.json`, khung hình hook KHÔNG
  được mang chữ/nhãn tiếng nước khác lọt vào (chữ tiếng Anh, watermark AI...), mặt nhân vật khớp
  REF/REF2 nếu có dùng REF-LOCK.
- Ghi `<tập>\hook\render_info.json` dạng `{"T_hook": ..., "frames": ..., "mode": "upstream|repair"}`.
- Cột **G** của sheet trỏ tới `final_with_hook.mp4` (không phải `final.mp4`) cho tập nào đã dựng
  hook.

---

## 10. TRA CỨU NHANH

| Thứ | Ở đâu |
|---|---|
| Thư mục gốc dự án | `E:\CLAUDE\YOUTUBE\h2dev` |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep<nn>-<slug>\` |
| Ảnh máy 2 vẽ | `<thư mục tập>\img_ai\` (`001.png` → `NNN.png`) |
| Thư mục giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep<nn>-<slug>\` |
| Token Google Drive + Sheet | `D:\CLAUDE\credentials\{credentials.json,token.json}` (tài khoản `haoviabattu@gmail.com`) |
| Trang tính | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`, tab `shinya_shiryoshitsu` |
| Kết quả chấm từng cảnh | `<thư mục tập>\qc_canh.json` |
| Kết quả nghiệm thu gói | `<thư mục tập>\qc_final.json` |
| Sổ nguồn tư liệu đầy đủ | `<thư mục tập>\credits.txt` |
| Python | `py -3.13` |
| Tra slug từ số dòng | `pipeline\quet_dong_can_anh.py --cho-ghep` |
| Ghi cột G (có rào chắn) | `pipeline\ghi_cot_video.py` |
| Hook 20–30s (nếu tập có) | `<thư mục tập>\hook\` — xem mục 9 |
| Batch clip Grok cho hook | `E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py` |
| Chuyển cảnh cho hook (fallback ảnh tĩnh) | `C:\Users\admin\.claude\skills\video-chuyen-canh\scripts\ghep_anh_co_chuyen_canh.py` |

**Số tập = STT ở cột A**, thư mục luôn là `ep<nn>-<slug>` chữ Latin (`ep02-walton`), không dùng tên
tiếng Nhật — chủ dự án gõ đường dẫn tay để vào lấy file.

---

## 11. KHI NÀO PHẢI DỪNG VÀ HỎI (thay vì tự quyết)

Dừng và báo, đừng tự xử lý, trong **mọi** trường hợp sau:

- Thiếu ảnh so với `prompts.txt`.
- Cột F ghi `LỖI:` hoặc ghi số `n/m` mà `n < m`.
- B8Q vẫn > 3% sau 2 lượt ghép lại.
- B10 có phát hiện NẶNG mà bạn không chắc cách sửa.
- Bạn thấy **kịch bản hoặc giọng đọc có vẻ sai** — báo, tuyệt đối không sửa (mục 1.4).
- Lệnh nào đó đòi tiền, đòi API key, hoặc bạn không chắc nó có tốn tiền không.
- Chủ dự án giao việc mà **không nói rõ dòng nào**.

Khi báo, luôn kèm: **tập nào (STT + slug)** · **đang ở bước nào** · **dòng log/số liệu thật** ·
**bạn định làm gì tiếp**. Đừng viết "có lỗi" suông.
