# Lane Google Flow "Create Tool" — 3 tool trong `pipeline\`

Từ **2026-09-23** dự án **mặc định sinh ảnh bằng "Create Tool" của Google Flow**, không gõ từng prompt
nữa.

| Bước | Lệnh | Việc |
|---|---|---|
| 1. Ra đơn | `py -3.13 pipeline\don_flow_tool.py --job <slug> --dong 28-45` | bộ 3 file |
| 2. Chạy lô | `py -3.14 pipeline\chay_flow_tool.py --bo3 "<thư mục bộ 3>"` | lái Flow, tải ZIP |
| 3. Nghiệm thu + giao | `py -3.13 pipeline\nghiemthu_flow_tool.py <zip> --bo3 "<thư mục bộ 3>" --giao "<tập>\img"` | 7 phép, đạt mới chép ảnh |

⚠️ **Bước 2 phải `py -3.14`** — máy này chỉ bản 3.14 có `playwright`. Bước 1 và 3 chạy `py -3.13`.

## ⛔ KHÔNG PHẢI "chạy nền không ai trông"

Kiểm chứng thật 2026-09-23, 3 lượt độc lập: **2/3 lượt tự động trót lọt, 1 lượt phải cứu tay**
(chất lượng ảnh thì 3/3 đạt). `chay_flow_tool.py` đã cài sẵn cách xử 3 kiểu hỏng dưới đây, nhưng
**vẫn phải có người ngó màn hình** khi nó chạy. Đừng giao lô rồi bỏ đi.

## 3 kiểu hỏng khi đang chạy — runner xử thế nào

| Kiểu hỏng | Dấu hiệu | `chay_flow_tool.py` làm gì |
|---|---|---|
| **1. Treo vĩnh viễn ở RUNNING** | app tham chiếu biến không tồn tại → mọi lệnh lỗi ngầm, dòng nằm mãi ở RUNNING, **không bao giờ sang FAILED** (đo thật: treo 30 phút, DONE=0/FAILED=0) | đếm số không đổi quá `--dung-hinh` (mặc định 300 s) → bấm nút **"Sửa lỗi"** của Flow |
| **2. Vá xong app dựng lại sạch trơn** | mất ref, mất đơn, Generate All khoá lại | `nap_du_lieu()` nạp lại toàn bộ ref + đơn + parallel rồi bấm Generate All lần nữa (tối đa 2 lần vá/lô) |
| **3. Bảng đếm reset về 0 + ZIP rỗng, ảnh còn trong RAM** | app vẫn ghi `Images currently in memory: 18` | đọc chỉ số đó làm tín hiệu xong, bấm lại Download ZIP. **Cấm kết luận "mất lô"** trước khi làm đủ 2 việc đó |

Thêm: dán chữ bằng `fill()` của Playwright có bản **không ăn** (app đọc state React chứ không đọc
DOM) → `dat_chu()` gọi **native setter** rồi bắn `input`/`change`.

### Chờ bằng điều kiện, không ngủ theo nhịp

Bản đầu ngủ cứng 20 giây mỗi vòng rồi mới đọc bảng đếm → xong rồi vẫn nằm đó tới 20 giây.
Nay chờ **trong trình duyệt** bằng `Frame.wait_for_function(JS_XONG)`: vị từ JS tự đọc
`TOTAL/DONE/FAILED` (thử **cả hai chiều** đặt số) và cả `images in memory`, nên đủ ảnh là bật ra ngay.
Vẫn cắt thành lát 30 giây để giữ nhịp kiểm "đứng hình" của kiểu hỏng #1.
Đo thật 2026-09-24: đủ ảnh lúc `07:27:33` → ZIP tải xong `07:27:34` — **trễ 1 giây**.

### Retry Failed — đã nối vào luồng

Chạy xong mà `FAILED > 0` thì `retry_failed()` bấm nút **"Retry Failed"** (vẽ lại CHỈ các dòng hỏng),
chờ lại, tối đa **2 vòng**, rồi mới tải ZIP. App không có nút đó thì nó **in danh sách nút đang có**
chứ không im lặng bỏ qua.

✅ Đã xác nhận app dựng ra **đủ 7 nút** đúng khế ước:
`Parse Lines · Generate All · Resume · Retry Failed · Test One Line · Download ZIP · Clear Storage`.
⚠️ **Nhánh retry chưa chạy thật lần nào** — 3 lô thử đều `FAILED=0` nên không có gì để vẽ lại. Mới
chứng minh được nút tồn tại và bấm trúng, chưa chứng minh được kết quả sau khi bấm.

## Chi tiết bước 1 — `don_flow_tool.py`

```
py -3.13 pipeline\don_flow_tool.py --job <slug> --dong 28-45
py -3.13 pipeline\don_flow_tool.py --job <slug> --dong 28-45 --kiem        ← chỉ xem, không ghi file
```

Ra trong `assets\_flow_tool_mau\<tên>\`:

| File | Nội dung |
|---|---|
| `flow_create_tool_prompt.txt` | hướng dẫn tiếng Việt + khối tiếng Anh giữa `=== DAN TU DAY ===` / `=== DAN DEN DAY ===` |
| `flow_batch_prompts.txt` | các dòng `NNN\|TAG\|description` — **NNN = số dòng gốc** trong `img_prompts.txt` |
| `_ref_upload\<SLOT>.png` | ảnh master đã QC mặt, tên file **trùng tên ô** trong app (`MAIN.png`, `FRIEND.png`…) |

## Tham số

| Cờ | Ý nghĩa |
|---|---|
| `--job` | slug trong `E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs`, hoặc đường dẫn đầy đủ |
| `--dong` | `28-45` · `28-45,60-70` · `all` |
| `--ten` | project name (mặc định = slug) — cũng là tên thư mục ra |
| `--out` | thư mục ra khác mặc định |
| `--slot @REF2=WIFE` | đổi tên ô ref (lặp lại được). Mặc định `MAIN, FRIEND, THIRD, FOURTH, FIFTH` |
| `--khong-ref` | ép biến thể (b) dù job có nhân vật |
| `--suffix "<text>"` | style suffix **có sẵn ở cuối mọi dòng** → tool cắt ra, app nối lại (mặc định tự dò) |
| `--suffix-them "<text>"` | style suffix app **nối thêm**, không cắt gì — cho job mỗi dòng tự mang style riêng |
| `--kiem` | chỉ in kế hoạch, không ghi file nào |
| `--ghi-de` | cho ghi đè thư mục ra đã có file |

## Hai biến thể prompt — tool tự chọn, không cần cờ

| Biến thể | Khi nào | Khuôn | Khác gì |
|---|---|---|---|
| **(a) có nhân vật** | job có `characters.json` + ảnh `master` | `pipeline\flow_tool_template_va3.txt` | ô ref + thang fallback (a)/(b) + cột `strategy` |
| **(b) không nhân vật** | job thiếu `characters.json`, hoặc không nhân vật nào có `master` (kiểu lane E) | `pipeline\flow_tool_template_plain.txt` | **cắt hẳn** ô ref, thang fallback, cột `strategy`; mọi dòng TAG `PLAIN`; không sinh `_ref_upload\` |

Tool tự nhận biết; ép biến thể (b) cho job có nhân vật bằng `--khong-ref`. Bản (b) **ổn định hơn**
vì phần lớn sự cố đã gặp đều nằm ở khối ref — đã verify chạy tốt không cần ref (3/3 ảnh, 40 giây).

Thang fallback của (a) **bỏ hẳn nhánh (c)** "hết cách thì vẽ không ref": ảnh vẫn đẹp nhưng **SAI MẶT**,
lọt qua review, chỉ lộ lúc ghép video.

**Đổi khuôn = sửa file `.txt`, KHÔNG sửa code.** Khuôn (a) bóc bằng máy từ
`assets\_flow_tool_mau\simbot2-01-shizuko\flow_create_tool_prompt_va3.txt`, đã kiểm điền ngược ra đúng
bản gốc từng ký tự. Khuôn (b) bóc bằng máy từ (a), mỗi phép cắt đều assert khớp đúng 1 lần.

**3 khối BẮT BUỘC** — tool kiểm sự hiện diện của cả 3 trước khi ghi, thiếu là dừng:

1. **Interface contract** — thiếu là mỗi lần dựng ra một app khác nhau, không tự động hoá nổi.
2. **Cấm IndexedDB + tự tải ZIP + banner đỏ cấm reload** — iframe chạy app có tên miền **ngẫu nhiên đổi
   mỗi lần tải trang**, nên mọi lưu trữ trình duyệt chết theo. Đây là lời giải vụ "app dừng câm ở 46/85,
   mất sạch ảnh": lỗi nền tảng, **không vá bằng code app được**.
3. **`attempts` là số lần gọi THẬT** (1 nếu ăn ngay lần đầu). Bản thiếu câu này ghi `attempts=4` ở cả 18
   dòng → cột vô dụng.

Giữ nguyên 3 điểm đã chốt trước đó: bỏ hẳn nhánh (c) "hết cách thì vẽ không ref" (ảnh đẹp nhưng **SAI
MẶT**, chỉ lộ lúc ghép video) · có `manifest.csv` trong ZIP · ép xoá kho cũ khi đổi project name.

## ⛔ 3 LUẬT VẬN HÀNH khi chạy lô — không làm đủ là mất hàng

1. **TUYỆT ĐỐI không reload / F5 khi đang chạy.** Tải ZIP xong mới được đụng vào trang.
2. **LUÔN tự bấm "Download ZIP" rồi ĐẾM ảnh trong file.** ZIP tự động đã 2 lần bắn lúc mới xong 12/18 và
   ra file 830 byte chỉ có manifest, không một ảnh nào.
3. **Lô dài thì bấm Download ZIP giữa chừng vài lần** — nút này tải được phần đã xong bất cứ lúc nào.

## Bước 3 — nghiệm thu rồi mới giao ảnh về tập

```
py -3.13 pipeline\nghiemthu_flow_tool.py <file.zip> --bo3 "<thư mục bộ 3>" --giao "<thư mục tập>\img"
```
7 phép: đủ số ảnh · **giữ đúng NNN gốc** (không đánh lại 001…) · md5 khác nhau đôi một · 1376×768 ·
manifest đủ dòng, header đúng khế ước, `attempts` không phải hằng số vô nghĩa · **`strategy=a` cho MỌI
dòng có nhân vật** (tụt xuống `b` = chỉ giữ 1 mặt trong cảnh 2 người ⇒ làm lại cả lô) ·
`failed_prompts.txt` rỗng. **Chỉ khi ĐẠT nó mới chép ảnh vào `--giao`**; trượt thì `exit 1` và nhắc
**chưa được reload trang Flow** vì ảnh còn trong RAM.

Phép thứ 8 tool không làm thay: mở 5–6 ảnh có TAG so mặt với `_ref_upload/` — sai 1 ảnh là hỏng cả lô.

> ⚠️ Đừng dùng `D:\CLAUDE\RENDER_IMG\flow_tool_nghiemthu.py` cho lô khác lô thử: nó khoá cứng
> `CAN = [f"{n:03d}" for n in range(28, 46)]` và số 18, nên **báo trượt oan** cho mọi dải NNN khác.
> Bản trong `pipeline\` đọc dải NNN và TAG từ chính `flow_batch_prompts.txt` của lô.

## Bốn kiểu marker đều đọc được (đừng đoán thêm kiểu thứ năm)

| Kiểu | Ví dụ | Job dùng |
|---|---|---|
| marker rời, nhiều cái đầu dòng | `@REF @REF2 wide shot of...` | simbot2-* |
| marker gộp | `@REF12 MEDIUM 65-year-old...` | lane F (`ep*`), theo `flow_batch_laneF.MARKER_ORDER` |
| **`@CAST:id1,id2` (mới, 2026-09-24)** | `@CAST:shu,tencho MEDIUM two-shot...` | lane K, lane L — tập có **>5 nhân vật/tập**, xem dưới |
| không marker | `Wide shot of the riverbank...` | → `PLAIN` |

**Kiểu 1+2 (`@REF...`)** — nhân vật lấy từ `_BANGIAO.txt` (`@REF = Tên`) nếu có, không thì theo
**thứ tự nhân vật CÓ `master`** trong `characters.json`, nạp **CẢ JOB một lần** (tối đa 5 nhân vật/tập
— khuôn Create Tool chỉ có 5 ô). Nhân vật **không có `master`** = không khoá mặt = không có marker
(vd 千恵子 ở `ep01-fuufu-nenkin-sa`) — đúng, không phải thiếu ảnh.
Dòng còn sót `@...` sau khi bóc ⇒ tool **dừng** và in bảng marker đang hiểu; phải thêm vào
`bang_marker()`, **không đoán**.

**Kiểu 3 (`@CAST:id1,id2 <mô tả>`)** — dành cho job có **NHIỀU HƠN 5 nhân vật trong cả tập** (kiểu
`@REF` cũ không đủ 5 ô cho cả tập thì bó tay). Khác biệt cốt lõi: `id` khớp THẲNG vào field `id`
trong `characters.json` (không qua thứ tự @REF/@REF2), và **ô ảnh gốc tính THEO TỪNG LÔ** — chỉ gồm
nhân vật XUẤT HIỆN trong các dòng `--dong` đã chọn cho lần chạy đó, không nạp cả 8 nhân vật của tập
làm tràn khuôn 5 ô. Vượt 5 nhân vật/lô → tool tự `sys.exit`, in danh sách id + dải dòng từng người
xuất hiện, không lọt sai — chia `--dong` nhỏ hơn là xong (vd tách theo đoạn cảnh khác nhân vật).
Tên ô ref = **id viết HOA ASCII** (`SHU`, `TENCHO`, `KIRIYAMA`…, KHÔNG phải `MAIN/FRIEND`), và ảnh
trong `_ref_upload/` được **tự resize ≤1600px cạnh dài** (PNG gốc 2-4 MB làm picker Flow kẹt "Đang
tải lên" — đo thật 2/2 lần không xong sau 90s; ảnh master gốc `_ref_<id>/001.png` KHÔNG bị đụng vào).
Job KHÔNG có dòng `@CAST:` nào thì chạy đúng y hệt bản `@REF` cũ, không hồi quy.
`--slot`/`--khong-ref` KHÔNG dùng được cho job kiểu `@CAST` (tên ô cố định = id, không đổi tay).

## Khi nào vẫn dùng lane Playwright cũ

Khi cần **chạy nền không ai trông** — lane Create Tool reload là mất sạch, không resume được, và chỉ
2/3 lượt tự động trót lọt. Lane Create Tool thắng rõ ở **cảnh 2+ nhân vật cùng khung** (gửi đủ nhiều
`referenceImageMediaIds`, thứ lane cũ không làm sạch được); lô toàn `PLAIN` thì **cả hai đều chạy tốt**
kể từ khi có biến thể (b).

## ⚠️ Flow đã đổi sang giao diện tiếng Việt (2026-09-24)

`aria-label` đổi theo — `"Settings trigger"` → `"Điều kiện kích hoạt cài đặt"` — làm chết mọi selector
cũ. Đã vá `D:\CLAUDE\RENDER_IMG\flow_lib.py` tự thêm `?hl=en` vào URL project (sao lưu
`flow_lib.py.bak-2026-09-24-hl-en`). `chay_flow_tool.py` dùng chung `flow_lib` nên hưởng luôn bản vá.
Triệu chứng nếu bản vá bị mất: lô ra `0/N ảnh` trong ~75 giây, và `render_flow.py` **tự rơi xuống gpti2
tính tiền**.

Chi tiết kỹ thuật + bảng bẫy đầy đủ (biến thể UI, nạp ref 2 kiểu, tỉ lệ dựng hỏng):
`C:\Users\xxx\.claude\skills\google-flow-tool.md`
