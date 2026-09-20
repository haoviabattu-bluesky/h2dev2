# QUY TRÌNH GIAO VIỆC SINH ẢNH CHO MÁY 2 — qua cột STATUS-IMG

> Dựng 2026-09-11 sau job test `simbot2-11-test7` (7/7 ảnh, 1 lỗi thật đã sửa vào skill §11.3c/d).
> Máy 2 = máy riêng, cùng LAN, có Chrome Flow Ultra (đăng nhập CHUNG tài khoản Google với máy 1) +
> Claude Code riêng. Trung gian dữ liệu là **Google Drive** (`FlowHandoff/jobs+results+shared`,
> xem memory `hai-may-drive-handoff-flow`), KHÔNG phải LAN share — máy 2 phải làm việc được kể cả
> khi máy 1 tắt.
>
> **Đây là quy trình DÙNG CHUNG cho MỌI kênh/lane của dự án** (mọi tab của trang tính
> `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`), không riêng 1 lane. Khác biệt giữa các lane
> chỉ nằm ở **LOẠI JOB** (mục 2), không phải quy trình bàn giao — quy trình (cột STATUS-IMG,
> Drive jobs/results/shared, `qc_can_anh.py`) là MỘT, dùng lại y hệt cho mọi kênh mới.
>
> **Hai loại job đang có (2026-09-11):**
> | | Loại A — REF-LOCK | Loại B — plain prompt |
> |---|---|---|
> | Lane ví dụ (tên **tab trang tính**) | `Lopezzapa68` — mã lane thật là **`satori-jp-obaa`**, thư mục `assets/satori_jp/` | `shinya_shiryoshitsu` — mã lane thật là **`toshi-densetsu-jp`**, thư mục `assets/toshi-densetsu-jp/` |
> | Có nhân vật lặp lại xuyên video? | Có (Character/@mention) | Không |
> | File hồ sơ | `img_prompts.txt` + `characters.json` + `_ref/001.png` | `img_ai/prompts.txt` (`tên file<TAB>prompt`) + `img_ai/img_meta.json` |
> | Máy 2 có cần tạo Character trên Flow? | Có (Upload master, mục 4) | Không |
> | Số tab chia việc | 5 tab CHUNG 1 project (bắt buộc) | Mỗi tab 1 project riêng cũng được (§11.2) |
> | Ràng buộc khung hình | không cố định | **16:9 bắt buộc, ngang ≥1280px** (máy 1 crop 1920×1080) |
> | Job thật đã chạy | `simbot2-11-test7` (7 ảnh) | `ep01-valentich` (308 ảnh — 5 test ĐẠT, đang chạy 303 còn lại, xem mục 4b) |

---

## ⭐ CÁCH GIAO VIỆC — NÓI THEO DÒNG, KHÔNG NÓI SLUG (anh chốt 2026-09-11, áp cho MỌI tab)

Anh giao việc cho máy 2 bằng **tab + số dòng**, đúng một trong hai câu:

> **"Vào tab `<tên tab>`, chạy job tạo ảnh cho dòng `<n>`."**
> **"Vào tab `<tên tab>`, chạy job tạo ảnh cho dòng `<x>-<y>`"** — dòng nào có cột STATUS-IMG ghi
> *"Xong nội dung - cần ảnh"* thì chạy, **lần lượt từ trên xuống dưới**; dòng khác bỏ qua.

**Số dòng là STT ở cột A**, không phải số dòng của Google Sheet (STT 11 nằm ở dòng 12 vì dòng 1 là
tiêu đề). Cứ nói theo STT, máy tự cộng bù.

**Không bắt ai gõ slug.** Slug (`simbot2-11-DXXwIxhcfF0`) là chuỗi dài vô nghĩa với người đọc; để
MÁY tra từ dòng ra slug:

```bat
py -3.13 pipeline\quet_dong_can_anh.py --tab <tên tab> --dong 11        (hoặc --dong 5-12)
py -3.13 pipeline\quet_dong_can_anh.py --tab <tên tab> --dong 5-12 --lenh   (in sẵn lệnh download-job)
```

Script CHỈ ĐỌC trang tính, dùng chung mọi tab/lane. Nó lấy slug từ đoạn cuối đường dẫn ở cột E
(FOLDER), không có thì bóc trong cột F sau dấu `|`. In ra đúng thứ tự phải chạy, kèm tiêu đề tập
để đối chiếu bằng mắt. Dòng đã `Đang tạo ảnh` / `Img done` / `LỖI:` đều in ra để biết nhưng **không
đưa vào danh sách chạy** — tránh làm trùng.

⚠️ `--dong` là **bắt buộc**. Không có dòng thì script không chạy — đúng luật cứng của dự án: lệnh
không rõ dòng thì **HỎI**, cấm tự chạy cả tab (memory `chi-chay-dong-duoc-chi-dinh`).

---

## TÓM TẮT — TAB-KÊNH KHÁC (LANE KHÁC) MUỐN DÙNG QUY TRÌNH NÀY THÌ LÀM GÌ

Không cần đọc lại từ đầu mỗi lần — 6 bước sau là toàn bộ việc phía **máy 1** cho MỘT tập:

1. **Xác định lane của mình là Loại A hay Loại B** (bảng trên). Có nhân vật lặp lại xuyên video
   (REF-LOCK, Character) → Loại A. Chỉ ảnh minh hoạ đơn lẻ (b-roll AI cho đoạn stock không có) →
   Loại B.
2. Ra đơn đúng định dạng lane mình: Loại A tự viết `img_prompts.txt`+`characters.json`+`_ref/`
   theo SOP sẵn có của lane; Loại B chạy `sinh_anh_canh.py --slug <tập> --chi-don`. **Trước khi
   viết prompt, đọc skill `veo3_flow_automation.md` §11.3c (thiếu mention → bịa người lạ), §11.3d
   (bối cảnh sai quốc gia), §11.3f (bịa số hiệu/ngày tháng dù ghi "no text")** — 3 lỗi thật đã
   dính, là lỗi PROMPT của lane chứ không phải lỗi máy 2, viết chặt từ đầu đỡ vẽ lại.
3. Chạy cổng: `py -3.13 pipeline\qc_can_anh.py --folder "<đường dẫn tập>"` — script tự nhận diện
   loại, ĐẠT mới đi tiếp.
4. `py -3.13 pipeline\drive_handoff.py upload-job <slug> <thư_mục_hồ_sơ>` — lệnh này **tự đối
   chiếu Drive với local ở cuối và trả exit≠0 nếu thiếu file**. Không tin dòng "up: ..." trên màn
   hình: một lần timeout giữa chừng từng để lại job 6/9 file mà `list-jobs` vẫn hiện như đã xong.
   Nghi ngờ thì chạy lại `verify-job <slug> <thư_mục_hồ_sơ>` (0đ, vài giây).
   **CHƯA verify ĐẠT thì CHƯA được ghi cột F** — ghi sớm là lừa máy 2 tải về một job hỏng.

   ⚠️ **`<thư_mục_hồ_sơ>` của Loại B là `<thư mục tập>\img_ai`, KHÔNG phải thư mục tập.**
   `upload-job` đi **đệ quy cả cây thư mục**, nên trỏ vào thư mục tập là nó bắt đầu đẩy luôn
   `stock/` (vài GB clip) lên Drive mà không hỏi gì và không có bước nào kêu. Đã dính thật
   2026-09-12 với `ep02-walton`: **618 MB clip đã lên Drive** trước khi dừng được, trong khi job
   `ep01-valentich` làm đúng thì trên Drive chỉ có **0,3 MB / 3 file**. Đã thêm rào `BO_QUA_DUOI`
   trong `drive_handoff.py` (bỏ mọi đuôi video/audio) — nhưng rào đó chỉ chặn hậu quả nặng nhất,
   vẫn phải trỏ đúng thư mục.

   ⚠️ **Slug lấy theo cột F, không lấy theo cột E.** Hai cột là hai không gian tên khác nhau:
   cột E là hồ sơ nghiên cứu (`_READY\02-walton\`), cột F là thư mục tập (`...\ep02-walton` —
   số tập bắt buộc có tiền tố `ep`). Job trên Drive đặt theo THƯ MỤC TẬP, nên bản cũ của
   `quet_dong_can_anh.py` (ưu tiên cột E) tra ra `02-walton` = job không tồn tại, và máy 2 sẽ báo
   "không thấy job" dù máy 1 đã up đủ. Đã đổi sang ưu tiên cột F (2026-09-12).
5. Ghi cột **F (STATUS-IMG)** đúng tab kênh mình trên trang tính
   `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` = `Xong nội dung - cần ảnh | <đường dẫn cục bộ>`.
   Báo máy 2 **theo dòng**, không đọc slug: *"Vào tab `<tên tab>`, chạy job tạo ảnh cho dòng
   `<n>`"* (hoặc một dải `<x>-<y>`). Máy 2 tự tra slug bằng `quet_dong_can_anh.py`, và loại job /
   số ảnh / bảng marker→nhân vật đã nằm sẵn trong `_BANGIAO.txt` của chính job đó.
6. Khi cột F đổi thành `Img done - n/m ảnh` → làm bước **"MÁY 1 NHẬN LẠI"** ở mục 4c bên dưới, rồi
   chạy hậu kỳ riêng của LANE MÌNH (ghép ảnh vào video, QC, dán nhãn nếu cần) — quy trình chung này
   dừng ở chỗ giao nhận ảnh, không biết/không cần biết hậu kỳ của từng lane.

Đã verify thật 2 lần độc lập (2 loại job khác nhau, cả 2 lần đều lộ ra ít nhất 1 lỗi thật rồi vá
được ngay từ vòng đầu — xem mục 4b/mục 7): `simbot2-11-test7` (Loại A) và `ep01-valentich` (Loại B).

---

## 0. RANH GIỚI HAI BÊN

| | Máy 1 (viết nội dung) | Máy 2 (sinh ảnh) |
|---|---|---|
| Viết script, tính char-rate, viết `img_prompts.txt` | ✅ | ❌ |
| Viết `characters.json` (bible), tính toán tuổi quan hệ | ✅ | ❌ |
| Sinh ảnh MASTER REF-LOCK (`_ref/001.png`...) bằng gpti2 | ✅ | ❌ |
| Upload hồ sơ lên Drive `jobs/<slug>/`, ghi cột `STATUS-IMG` | ✅ | ❌ |
| Tạo Character trên Flow (upload master có sẵn) | ❌ | ✅ |
| Sinh ảnh hàng loạt qua Flow (Nano Banana Pro, đa tab) | ❌ | ✅ |
| Vá ảnh lỗi/thiếu bằng gpti2 nếu <20% (xem mục 5) | ❌ | ✅ |
| Upload kết quả lên Drive `results/<slug>/`, ghi `STATUS-IMG` | ❌ | ✅ |
| Ghép video, thumbnail, đăng | ✅ | ❌ |

Máy 2 KHÔNG tự viết/sửa `img_prompts.txt` hay `characters.json` — thấy prompt có vẻ sai thì BÁO LẠI
(mục 6), không tự sửa hộ.

---

## 1. VÒNG ĐỜI 1 TẬP — cột F `STATUS-IMG`

Điều phối qua **spreadsheet `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`**, mỗi kênh 1 tab
(`Lopezzapa68`, `shinya_shiryoshitsu`, `irogatatarukioku`...), mỗi dòng = 1 tập. Cột đã có sẵn:
**A** STT · **B** ĐỀ TÀI · **C** NỘI DUNG · **D** TÌNH TRẠNG · **E** FOLDER · **F** `STATUS-IMG` ·
**G** VIDEO · **H** GHI CHÚ.

| Giá trị cột F | Ai ghi | Ý nghĩa |
|---|---|---|
| (trống) | — | chưa tới bước cần ảnh |
| `Xong nội dung - cần ảnh \| <đường dẫn cục bộ máy 1>` | Máy 1 | script+prompt+master đã sẵn sàng, đã upload job lên Drive |
| `Đang tạo ảnh (máy 2, <ngày giờ>)` | Máy 2 | tự đánh dấu NGAY khi bắt đầu nhận job — tránh máy 1 tưởng chưa ai nhận, tránh nhận trùng nếu có nhiều phiên |
| `Img done - <n>/<m> ảnh (<ngày giờ>)` | Máy 2 | xong, `n`=số ảnh thật đưa vào `results/`, `m`=tổng số dòng `img_prompts.txt` |
| `LỖI: <mô tả ngắn>` | Máy 2 | vướng thứ máy 2 không tự quyết được (xem mục 6) — máy 1 phải vào xử lý, KHÔNG tự chạy tiếp |

**Đường dẫn trong cột F là đường dẫn CỤC BỘ trên máy 1** (vd
`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0\`) — chỉ để máy 1 biết chỗ đặt ảnh
về sau. Máy 2 KHÔNG đọc trực tiếp đường dẫn này (không có SMB share) — **slug** (tên thư mục cuối
cùng, vd `simbot2-11-DXXwIxhcfF0`) là khoá nối sang Drive: máy 2 luôn tìm job qua
`drive_handoff.py download-job <slug>`.

---

## 2. HỢP ĐỒNG — hồ sơ phải có ĐỦ trước khi ghi "cần ảnh"

Bắt buộc có trong thư mục job (và đã `upload-job` lên Drive) TRƯỚC khi đổi cột F:

**Loại A (REF-LOCK):**

| File | Bắt buộc | Ghi chú |
|---|---|---|
| `img_prompts.txt` | ✅ | mỗi dòng 1 cảnh, marker `@REF`/`@REF2` (quy ước cũ gen_images.py) |
| `characters.json` | ✅ nếu có REF-LOCK | bible: name/age/gender/look/relationships |
| `_ref/001.png`, `_ref_<tên>/001.png` | ✅ nếu có REF-LOCK | **PHẢI đã tạo sẵn bằng gpti2 ở MÁY 1** — máy 2 LUÔN tạo Character bằng Upload ảnh này (không mô tả lại bằng chữ, không tốn credit — §11.3b). Tên thư mục lấy theo `characters.json[].master`, **không cố định phải là `_ref2`** |
| `REF_<tên>_master.png`, `REF2_<tên>_master.png` ở GỐC job | tự sinh | Bản **phẳng** của chính 2 ảnh trên, `upload-job` tự đặt lên Drive. Để máy 2 chạy bản `drive_handoff.py` CŨ (chưa đệ quy thư mục con) vẫn tìm thấy master — khỏi phải cập nhật đồng bộ hai máy mới chạy được |
| `_BANGIAO.txt` | tự sinh | `upload-job` tự viết: loại job · số dòng prompt · bảng marker→nhân vật→file · cảnh báo cảnh nhiều nhân vật. **Job tự mô tả mình**, máy 2 không cần đọc tin nhắn của máy 1 |

**Loại B (plain prompt, không nhân vật lặp — vd toshi-densetsu-jp):**

| File | Bắt buộc | Ghi chú |
|---|---|---|
| `img_ai/prompts.txt` | ✅ | mỗi dòng `<tên file>.png<TAB><prompt tiếng Anh>`, tên file liên tục `001.png`→`NNN.png` — đây là khoá DUY NHẤT nối ảnh với đoạn lời |
| `img_ai/img_meta.json` | ✅ | sổ ghép của máy 1 (đoạn lời `t0`/`t1` ↔ tên file) — máy 2 ĐỌC, KHÔNG sửa |
| `characters.json`, `_ref/` | ❌ không cần | lane này không REF-LOCK |

**Máy 1 chạy cổng `qc_can_anh.py` trước khi ghi cột F** (mục 3) — không tự suy "chắc đủ rồi".

⚠️ **Bẫy đã dính thật (§11.3c, chỉ áp dụng Loại A)**: cảnh có ≥2 nhân vật mà `img_prompts.txt` chỉ
đánh 1 marker (`@REF` hoặc `@REF2`) trong khi TÊN nhân vật kia chỉ nằm trong câu mô tả (chữ thường)
→ Flow tự bịa người lạ thay vào chỗ nhân vật thật. `qc_can_anh.py` tự dò cảnh nghi vấn kiểu này.

---

## 3. CỔNG TRƯỚC KHI GIAO — `pipeline/qc_can_anh.py`

```bash
py -3.13 pipeline\qc_can_anh.py --folder "<đường dẫn tập>"
```

Script **tự nhận diện loại job**: thấy `<folder>/img_ai/prompts.txt` → kiểm theo Loại B (tên file
liên tục 001..NNN, `img_meta.json` khớp số dòng); không thấy thì tìm `<folder>/img_prompts.txt` →
kiểm theo Loại A (bảng dưới).

| Kiểm (Loại A) | Vì sao chết người nếu bỏ qua |
|---|---|
| `img_prompts.txt` tồn tại, không rỗng | máy 2 không có gì để chạy |
| Mỗi dòng `@REF`/`@REF2` phải có `_ref`/`_ref2` tương ứng đã tồn tại ảnh | máy 2 không tạo Character được, đứng job |
| **Dò cảnh nhiều nhân vật thiếu mention** (heuristic: dòng có `@REF` nhưng lại chứa TÊN nhân vật thứ 2 trong `characters.json` dạng chữ thường, không có `@REF2`) | lặp lại đúng lỗi 006 (bịa người lạ) |
| `characters.json` có đủ field `name`/`age`/`gender`/`master` cho từng nhân vật xuất hiện | máy 2 không biết map tên nào ra ảnh nào |
| Không dòng nào để trống prompt | Flow submit lỗi giữa batch |

ĐẠT mới ghi cột F. TRƯỢT thì sửa hồ sơ rồi chạy lại cổng — không upload job lỗi lên Drive.

---

### 3b. CỔNG VẬN CHUYỂN — ba lỗi câm của `drive_handoff.py` đã vá (2026-09-11)

`qc_can_anh.py` chỉ gác **nội dung hồ sơ**. Tầng **vận chuyển** trước đây không ai gác, và nó hỏng
theo kiểu tệ nhất: nhìn thì tưởng xong.

| Lỗi | Hậu quả thật | Đã vá |
|---|---|---|
| `files().list()` **không phân trang** — Drive API mặc định trả tối đa 100 file, không cảnh báo gì | Job Loại B `ep01-valentich` có **308 ảnh** ⇒ `download-result` chỉ lấy về 100 tấm, máy 1 ghép video thiếu 208 cảnh mà không bước nào kêu | Mọi chỗ liệt kê chạy hết `pageToken`, `pageSize=1000` |
| **Không đệ quy thư mục con** (`if not f.is_file(): continue`) | `_ref/001.png` — ảnh master REF-LOCK, bắt buộc theo mục 2 — **không bao giờ lên được Drive**. Job Loại A duy nhất chạy được trước đó (`simbot2-11-test7`) là do có người làm phẳng bằng tay | Upload/download đi hết cây thư mục; thêm bản phẳng ở gốc cho tương thích ngược |
| **Đứt giữa chừng vẫn coi như xong** | Một lần timeout mạng làm job chỉ lên 6/9 file, `list-jobs` vẫn hiện bình thường | Mọi thao tác mạng có **thử lại + backoff**; `upload-job` tự đối chiếu cuối lệnh; thêm `verify-job`/`verify-result` |

Rút ra: **công cụ vận chuyển phải tự chứng minh đã chuyển đủ**, đừng để người dùng suy ra từ việc
"không thấy báo lỗi". Cùng một bài học với §2.5 của `SOP_CLONE_BRAIN.md` (cổng phải đạt được) và với
`qc_can_anh.py` (cổng phải đọc nguồn chân lý, đừng đoán tên thư mục).

⚠️ Bản `drive_handoff.py` mới **đã up vào `shared/`**. Máy 2 `download-shared` trước mỗi job là tự
động có bản mới. Nhưng kể cả quên, bản phẳng `REF_*_master.png` ở gốc job vẫn cứu — **không còn
đường nào dẫn tới thiếu master trong im lặng**.

---

## 4. QUY TRÌNH MÁY 2 (khi thấy cột F = "Xong nội dung - cần ảnh")

**Chung cho cả 2 loại:**
1. `drive_handoff.py download-shared <tmp>` — LUÔN lấy skill/script mới nhất trước (quy ước đã chốt).
2. Đọc kỹ skill `veo3_flow_automation.md` §11 (đặc biệt §11.1b model Pro, §11.3e 4 bẫy đa tab).
3. **Tra dòng ra slug** — anh giao việc theo dòng, không theo slug:
   `py -3.13 pipeline\quet_dong_can_anh.py --tab <tab> --dong <n hoặc x-y> --lenh`
   Nhiều job thì chạy **lần lượt từ trên xuống**, xong hẳn một job mới sang job kế.
4. Ghi ngay cột F = `Đang tạo ảnh (máy 2, <giờ>)` — tránh nhận trùng.
5. `drive_handoff.py download-job <slug> <tmp>` rồi **đọc `_BANGIAO.txt`** trong job: loại job, số
   dòng prompt, bảng marker→nhân vật→file master, cảnh báo cảnh nhiều nhân vật. Job tự mô tả mình.
5. Ép model **Nano Banana Pro** + `x1` + `Never confirm` — làm lại mỗi project mới (§11.1b).

**Riêng Loại A (REF-LOCK):**
6a. Tạo Character bằng **Upload** đúng file `_ref/001.png`/`_ref2/001.png` (không mô tả chữ).
7a. Chia `img_prompts.txt` cho 5 tab, TẤT CẢ tab cùng mở CHUNG 1 project (bắt buộc cho REF-LOCK, §11.3c mention đủ nhân vật).

**Riêng Loại B (plain prompt):**
6b. KHÔNG cần tạo Character. Chia `img_ai/prompts.txt` cho N tab, mỗi tab **project riêng** cũng
    được (§11.2 đã verify không cần chung project khi không REF-LOCK).
7b. **Vẽ thử 5 dòng đầu trước** — báo lại: thời gian/tấm, kích thước thật, có đúng 16:9 không
    (≥1280px ngang), có dính chữ/logo không. Chờ máy 1 duyệt mới chạy hết batch còn lại.

**Chung tiếp:**
8. Giãn submit giữa các tab ≥15s (né rate-limit §11.3e mục 2), đóng panel Agent trước khi thao tác
   (§11.3e mục 3).
9. Đếm ảnh lỗi/thiếu — áp quy tắc mục 5 bên dưới.
10. Ghi `manifest.json` đúng format §11.6 (idx/tab/uuid/prompt/bytes; Loại A thêm `character`).
11. `drive_handoff.py upload-result <slug> <thư_mục_anh>` — CHỈ file `.png` đặt đúng tên cột 1,
    KHÔNG đổi tên tấm khác để "cho đủ số" khi thiếu (báo thiếu, xem mục 6).
12. Ghi cột F = `Img done - <n>/<m> ảnh (<giờ>)`.

### 4b. Job Loại B đầu tiên đã lên Drive thật (2026-09-11)

Slug `ep01-valentich` (lane `shinya_shiryoshitsu`/toshi-densetsu-jp) — **308 ảnh**, đã qua cổng
`qc_can_anh.py` (ĐẠT), đã `upload-job` thật lên `FlowHandoff/jobs/ep01-valentich/`
(`prompts.txt` + `img_meta.json`), đã ghi cột F tab `shinya_shiryoshitsu` dòng 2. Đây là job Loại B
đầu tiên chạy qua đường Drive thật (khác `simbot2-11-test7` là Loại A). Lưu ý số 308 ≠ 77: 77 là số
ĐOẠN LỜI cần ảnh (`CU_THE`), mỗi đoạn ra 3–5 góc máy khác nhau nên nhân thành 308 ẢNH thật cần vẽ
(xem `docs/GIAO_VIEC_ANH_MAY2.md` mục "Vì sao chỉ vẽ một phần" để hiểu gốc con số).

**Lỗi thật lộ ra ngay ở vòng test 5 ảnh đầu (trước khi đốt hết batch)**: prompt phong cách
"archival/documentary" tự bịa số hiệu đăng ký máy bay kiểu Mỹ + timestamp sai năm dù đã ghi "no
text" — xem skill §11.3f. Đã vá tận gốc ở `pipeline/sinh_anh_canh.py` (hằng `DUOI`, áp dụng mọi
lane/mọi tập từ nay) + patch lại cả 308 dòng `prompts.txt` của job này + `upload-job` lại (đè bản
cũ). Đây chính là lý do bước "vẽ thử 5 tấm đầu, chờ duyệt" ở mục 4 nhánh 7b tồn tại — bắt lỗi hệ
thống ở quy mô 5 ảnh, không phải 308 ảnh.

### 4c. MÁY 1 NHẬN LẠI KẾT QUẢ (khi cột F = "Img done - n/m ảnh")

Quy trình chung dừng ở đây — bước sau là chung cho cả 2 loại, hậu kỳ riêng lane thì mở SOP của lane
đó (Loại A xem SOP satori; Loại B xem `docs/GIAO_VIEC_ANH_MAY2.md` mục 4):

1. `drive_handoff.py download-result <slug> <tập>\img_ai\` (Loại B) hoặc thư mục ảnh tương ứng
   (Loại A) — tải thẳng vào đúng chỗ pipeline lane đó đang chờ đọc, không qua thư mục tạm rồi copy
   tay (dễ quên/copy nhầm).
2. **Đối chiếu số lượng + tên file với `prompts.txt`** — n/m máy 2 báo phải khớp số file `.png`
   thực nhận; tên thiếu thì đúng là thiếu tấm đó (không suy diễn máy 2 gửi thiếu do lỗi khác).
3. Đọc `manifest.json` máy 2 gửi kèm — ảnh nào `"engine": "gpti2"` (vá theo mục 5) thì biết để
   không hiểu nhầm là ảnh Flow khi hậu kiểm.
4. Chạy hậu kỳ riêng lane (vd Loại B: `make_video.py --profile <lane> --slug <tập> --from B8` rồi
   `qc_canh.py` chấm 100% cảnh, trần lạc 3%).
5. Ghi cột **TÌNH TRẠNG** (cột D, không phải STATUS-IMG) sang bước tiếp theo của lane nếu lane đó
   dùng cột D để theo dõi tiến độ toàn tập — STATUS-IMG chỉ theo dõi riêng khâu ảnh.

---

## 5. NGƯỠNG FALLBACK GPTI2 — <20% lỗi/thiếu

Nếu số ảnh lỗi/thiếu sau khi chạy Flow (rate-limit không retry nổi, policy chặn, hoặc chất lượng rõ
sai — mặt lệch hẳn, thiếu người, hoặc sai tỉ lệ 16:9) **< 20% tổng số ảnh** của tập đó:
- **CHO PHÉP** vá bằng gpti2: Loại A dùng `gpti2_edit.py --ref _ref/001.png --quality low` (giữ mặt);
  Loại B dùng `gpti2_gen.py` với đúng prompt cột 2 của dòng đó, size ngang 16:9 (không cần `--ref`,
  không có nhân vật để giữ mặt) — sinh bù ĐÚNG các ảnh đó, giữ nguyên số thứ tự `NNN.png`.
- Ghi rõ trong `manifest.json` mỗi ảnh vá: `"engine": "gpti2"` (khác `"engine": "flow"` các ảnh còn
  lại) — để máy 1 biết ảnh nào từ nguồn nào khi hậu kiểm.

Nếu **≥ 20%** lỗi/thiếu: **DỪNG lại, KHÔNG tự vá hết bằng gpti2** — ghi cột F = `LỖI: <n>/<m> ảnh
hỏng, vượt ngưỡng 20%, lý do: <mô tả>`. Tỉ lệ lỗi cao thường là dấu hiệu vấn đề GỐC (prompt sai định
dạng, Character tạo sai, project bị lỗi) — vá hết bằng gpti2 sẽ che mất vấn đề đó, y hệt bài học
`b3f-khong-duoc-noi-vao-vong-viet-lai` (lỗi dữ liệu phải dừng hẳn, không nối vào vòng sửa tự động).

`gpti2_gen.py`/`gpti2_edit.py` + key cần có sẵn trên máy 2 (đẩy qua `shared/` nếu chưa có — **đây là
API key thật, tốn tiền nếu lộ, cảnh báo y hệt khi gửi token Drive**).

---

## 6. BÁO LỖI — khi nào máy 2 phải DỪNG thay vì tự quyết

Ghi `LỖI:` vào cột F (không tự sửa hộ, không tự bỏ qua) khi:
- Thiếu file bắt buộc mà cổng `qc_can_anh.py` đáng lẽ đã chặn (phòng trường hợp máy 1 quên chạy cổng).
- ≥20% ảnh lỗi/thiếu (mục 5).
- Nghi ngờ `img_prompts.txt` sai cảnh/sai nhân vật rõ ràng (đừng tự đoán ý viết lại).
- Hết credit Google Flow VÀ không đủ để dùng gpti2 vá (báo cả 2 số dư).

Mỗi lỗi ghi đủ: **số đo thật** (n/m ảnh, giá trị cụ thể) + **vì sao dừng ở đây** — không ghi chung
chung "có vấn đề".

---

## 7. SỔ LỖI ĐÃ GẶP (xem đủ chi tiết ở skill `veo3_flow_automation.md` §11)

| Lỗi | Chặn ở đâu từ nay |
|---|---|
| Cảnh nhiều người chỉ mention 1 nhân vật → Flow bịa người lạ | `qc_can_anh.py` dò cảnh nghi vấn (mục 3) + §11.3c |
| Model tự trôi về Nano Banana 2 mỗi project mới | §11.1b — máy 2 luôn ép lại |
| Character mới tạo ở project A không thấy được ở project B | mục 1/4 — mọi tab REF-LOCK dùng CHUNG 1 project |
| Reload trang làm mất UUID ảnh mới | §11.4 — cấm reload khi đang tải ảnh |
| Overlay kẹt khi dùng @mention | §11.5 hàm `wait_no_overlay()` |
| Rate-limit "asking too fast" khi submit tab cách nhau <5s | §11.3e — giãn ≥15s + auto retry |
| Bối cảnh lẫn thương hiệu sai quốc gia (bưu điện ra kiểu Mỹ) | §11.3d — ghi rõ quốc gia/cấm thương hiệu thật trong prompt |

---

## 8. LIÊN QUAN
- `E:\CLAUDE\YOUTUBE\h2dev\pipeline\veo3_flow_automation.md` (đồng bộ `shared/`) — kỹ thuật đầy đủ §11
- `pipeline/drive_handoff.py` — cầu nối Drive (jobs/results/shared)
- `pipeline/qc_can_anh.py` — cổng kiểm, tự nhận diện Loại A/B
- `pipeline/quet_dong_can_anh.py` — tra tab+dòng ra slug (chỉ đọc trang tính, dùng chung mọi lane)
- `docs/GIAO_VIEC_ANH_MAY2.md` — chi tiết PHÍA MÁY 1 của Loại B (lệnh `sinh_anh_canh.py --chi-don`
  ra đơn, `make_video.py --from B8` ghép lại + lý do vì sao chỉ vẽ một phần đoạn lời). File này
  (`GIAO_VIEC_MAY2_ANH.md`) là quy trình BÀN GIAO chuẩn dùng chung mọi lane; file kia là chi tiết
  kỹ thuật riêng của lane `stock_clips` — đọc cả hai khi làm job Loại B.
- memory `hai-may-drive-handoff-flow`, `flow-veo3-nano-banana-image-gen`
- `docs/GIAO_VIEC_SPACE_RESEARCH.md` — mẫu gốc của kiểu quy trình cột-trạng-thái này
