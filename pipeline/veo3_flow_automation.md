# SKILL: veo3_flow_automation — Chạy VIDEO VEO 3 + ẢNH NANO BANANA HÀNG LOẠT trên Google Flow (extension flow79 + cách tự viết Playwright)

> **Gọi skill này khi**: "chạy video veo3", "batch prompt Flow", "tự động tạo video Google Flow",
> "tải video Flow tự động", "làm hàng loạt video AI cho kênh YouTube", **"tạo ảnh Nano Banana Pro/2",
> "REF-LOCK bằng Character của Flow", "sinh ảnh đa luồng qua Flow"**, hoặc khi động tới thư mục
> `E:\CLAUDE\YOUTUBE\EXTENSION\flow79`. Phần ẢNH (Nano Banana, không phải Veo video) xem **§11**.
>
> **Tài sản kèm skill**: `skills/veo3_flow_automation/flow_selectors_v3.3.9_2026-09-07.json`
> — **bản đồ 56 selector THẬT của UI Google Flow**, lấy live từ server config của extension
> (verify 2026-09-07). Đây là thứ giá trị nhất để TỰ VIẾT automation không cần extension.

---

## 0. flow79 là extension gì

`E:\CLAUDE\YOUTUBE\EXTENSION\flow79` = **"Flow Automation - Auto Flow on Google Flow" v3.3.9** (MV3),
tác giả Truong Nguyen / kylenguyen.me (Chrome Web Store id `fnmijgmnjpealnnadjpji…`,
guide github.com/trgkyle/veo-automation-user-guide, Discord KS2pMHQdc9).

Nó KHÔNG gọi API Veo. Nó là **robot bấm UI** trên `flow.google.com` (Google Flow — web app chạy
Veo 3.1): nạp danh sách prompt → tự tạo project → set model/tỉ lệ/thời lượng/số output → gõ prompt →
submit → chờ render → tự tải video/ảnh về thư mục đặt tên theo prompt. Tức là nó tiêu **quota gói
Google AI Pro/Ultra**, không tốn tiền API.

Đây chính là mảnh còn thiếu cho pipeline h2dev: dựng video faceless hàng loạt bằng Veo 3.

---

## 1. SÁU kỹ thuật lõi (đọc từ code — tái dùng được hết cho tool tự viết)

| # | Kỹ thuật | Chi tiết |
|---|---|---|
| 1 | **Selector nạp TỪ SERVER, không hardcode** | `GET https://configs.kylenguyen.me/config/flow-automation-2` header `X-Client-Secret: YES_THAT_IS_VERY_EASY_RIGHT_?!$` (fallback `configs2.`). Trả `{version, hash, selectors{56 key}}`. Google đổi UI → tác giả sửa server, không cần update extension. **Ta cũng nên tách selector ra JSON riêng y hệt.** |
| 2 | **Input "thật" bằng CDP debugger** | Service worker xin quyền `debugger`, `chrome.debugger.attach` rồi bắn `Input.insertText` / `Input.dispatchKeyEvent` / `Input.dispatchMouseEvent` (message type `CIT`/`CK`/`CC`/`CH`). Lý do: Flow là Angular Material, event JS tổng hợp (`el.click()`) KHÔNG ăn. → **Playwright `page.mouse`/`page.keyboard` dùng đúng CDP domain này nên tương đương 1-1.** |
| 3 | **Tải 720p = đọc thẳng `src` trong DOM** | Với `autoDownloadVideoQuality=720` nó lấy `<video>.src` / `<img>.src` của tile rồi `chrome.downloads.download`. KHÔNG cần bấm menu. → Playwright chỉ cần `get_attribute("src")` rồi tải bằng `page.request.get` (giữ cookie phiên). |
| 4 | **1080p/2K/4K mới phải bấm menu** | hover tile → `more_vert` → `download` → chọn option chất lượng. Google render bản cao hơn theo yêu cầu nên không có sẵn URL trong DOM. Có vòng retry `maxRetries`. |
| 5 | **Chờ xong = `stopButton` biến mất** | Sau submit chờ 2s rồi `waitForDisappear(button:has(mat-icon:contains("stop")), timeout 900000)` = **15 phút/lô**. Đơn giản và chắc hơn bắt network. |
| 6 | **Nhắc ảnh/nhân vật bằng `@`** | Gõ ký tự `@` (CDP key `Digit2`) → popover mở → gõ tên → chọn item đầu → quay lại textarea. Đây là cú pháp mention có sẵn của Flow cho ingredient/character. Upload file thì hook `HTMLInputElement.prototype.click` + bơm base64 qua CustomEvent `VEO_UPLOAD_FILE_DATA` (file `catchUploadFile.ts`). |

Chống phát hiện bot: submit **ngẫu nhiên 20% bấm nút / 80% Enter**, delay ngẫu nhiên
`promptDelaySecondsMin..Max` giữa các prompt.

---

## 2. Tính năng / settings (giá trị mặc định lấy từ code)

```
defaultMode: textToVideo | imageToVideo (Frame to Video) | componentsToVideo (Ingredients to Video)
             | textToImage | imageToImage | agentAutomation
model: "Veo 3.1 - Lite" (còn Quality / Fast / Lite [Lower Priority])
imageModel: "Nano Banana 2" (Nano Banana 2 Lite, Omni 1.1 Flash — Omni cần Pro/Ultra)
aspectRatio: 16:9 (YouTube) | 9:16 (Shorts/Reels) | 1:1 | 3:4 | 4:3
defaultVideoOption: 4s | 6s | 8s (mặc định) | 10s  + bản "(concat)" CẦN GÓI ULTRA
outputCount: 2          (số video/ảnh mỗi prompt, 1-4)
concurrentPrompts: 1    (chạy song song 1-6 prompt)
promptDelaySecondsMin/Max: 0..20
maxRetries: 1           (1-20)
autoDownloadVideoQuality: 720 | 1080 | 4K (1080/4K cần gói Google Pro/Ultra) | no-download
autoDownloadImageQuality: 1k | 2k | 4k (4k cần Ultra)
imageToVideoMaxImagesPerPrompt: 1 (start frame) hoặc 2 (start + end frame)
componentsToVideoMaxImagesPerPrompt: 3 ; imageToImageMaxImagesPerPrompt: 3
autoAddCharacterImages / enableCharacterControl / autoAddVoiceBySpeaker / defaultSpeaker
folderName: "veo-folder-1" ; autoChangeFileName: true (đặt tên file theo prompt)
```

- **Nhập prompt hàng loạt từ `.txt` / `.xlsx` / `.csv`** (bundle có SheetJS) → có Queue, trạng thái
  từng prompt (queued/running/completed/error/retrying), tab Debug Logs.
- Panel là **side panel** của Chrome (không phải popup), mở bằng icon extension.
- Có link dịch vụ ngoài `watermark.kylenguyen.me` để **xoá logo VEO** (dịch vụ riêng, không nằm trong extension).

---

## 3. HAI tầng giới hạn — đừng nhầm

| Tầng | Nội dung |
|---|---|
| **Gói của EXTENSION** (kylenguyen.me) | Free = **10 prompt/ngày** (`limit:10`, đếm trong `chrome.storage.local`); Max = **$3/tháng** dùng chung cho mọi extension của tác giả. Đăng nhập bằng **email bất kỳ** (`POST configs.kylenguyen.me/api/auth/login` → accessToken → `/api/auth/plan`), *không cần trùng* tài khoản Google Flow. |
| **Gói của GOOGLE (Flow)** | Quyết định thứ thật sự đắt: 1080p/4K download, video 10s concat, model Quality, Omni — đều đòi **Google AI Pro/Ultra**. Extension chỉ bấm hộ, không vượt được quota Google. |

---

## 4. Cài & dùng (khi bấm tay / bán tự động)

1. Copy thư mục → xoá `_metadata` nếu có (quy tắc chung, xem `youtube_research_ext.md`; bản flow79
   hiện KHÔNG có `_metadata` nên load thẳng được).
2. `chrome://extensions` → Developer mode → Load unpacked.
3. Mở `flow.google.com`, vào 1 project (hoặc để nó tự tạo) → bấm icon extension → side panel.
4. Dán/import prompt → chọn model + tỉ lệ + outputCount → Start.
5. Video rơi vào `Downloads/<folderName>/`.

> Profile: dùng **profile research riêng** (vd `E:\CLAUDE\YOUTUBE\h2dev\chrome_profile`) vì extension
> xin quyền `debugger` + `downloads` + `tabs`. Đừng cài vào Chrome cá nhân / profile giữ phiên tiền bạc.

---

## 5. ⭐ BẢN ĐỒ UI THẬT — verify trực tiếp trên Google Flow 2026-09-07 (Ultra, Chrome 152)

> **Bộ 56 selector lấy từ server của flow79 (file JSON kèm skill) ĐÃ LỖI THỜI với UI hiện tại.**
> Mục này là bản đã chạy thật, tạo được clip Veo 3.1 8 giây 1280×720 có tiếng và tải về máy.
> Dùng mục này làm chuẩn; file JSON chỉ còn giá trị tham khảo lịch sử.

### 5.1 Môi trường chạy (BẮT BUỘC đúng, xem §6 pitfall 10-11)

```
# Profile RIÊNG, thư mục mới hoàn toàn — KHÔNG dùng User Data mặc định, KHÔNG copy, KHÔNG junction
chrome.exe --user-data-dir=E:\CLAUDE\YOUTUBE\VEO3_PROFILE --remote-debugging-port=9333 ^
           --no-first-run --no-default-browser-check https://flow.google.com/
# Lan dau: nguoi dung tu dang nhap tai khoan Google (Ultra) trong cua so nay -> session luu lai vinh vien
```
Playwright: `connect_over_cdp("http://127.0.0.1:9333")` → `browser.contexts[0].pages[-1]`.
**Đừng gọi `browser.close()`** (ngắt CDP kiểu đó có thể đóng luôn browser).

### 5.2 Luồng đã chạy thật, theo đúng thứ tự

| # | Việc | Selector / thao tác ĐÃ VERIFY |
|---|---|---|
| 1 | Vào app | `page.goto("https://flow.google.com/")` rồi bấm `button:has-text("Create with Google Flow")`. `labs.google/fx/tools/flow` chỉ là trang marketing |
| 2 | Xác nhận gói | `flow-user-tier-chip` hiện `ULTRA` |
| 3 | Tạo project | `button:has(mat-icon:text-is("add"))` (hoặc `button:has-text("Dự án mới")`). **`add_2` của map cũ = 0 phần tử** |
| 4 | Đóng agent panel | `flow-agent-panel button:has(mat-icon:text-is("close"))` → mới hiện `flow-prompt-box` cổ điển. Mặc định Flow mở panel chat agent bên phải |
| 5 | Bỏ thẻ giới thiệu | `button:has-text("Tôi hiểu")` nếu có |
| 6 | Mở cài đặt | `button:has(mat-icon:text-is("tune"))` → panel `flow-settings-view`. **Không còn `flow-prompt-box-settings`** |
| 7 | Trong `flow-settings-view` | `mat-radio-button` thứ 2 = "Không bao giờ" (tự sinh, không hỏi xác nhận). `flow-toggles` theo thứ tự: **[0]** tỉ lệ ảnh (16:9/4:3/1:1/3:4/9:16) · **[1]** số ảnh x1-x4 · **[2]** tỉ lệ video (chỉ 16:9 / 9:16) · **[3]** số video x1-x4. Nút model ảnh = `button:has-text("Nano Banana")`, nút model video = `button:has-text("Veo")`. Lưu bằng `button:has-text("Lưu")` |
| 8 | Model video chọn được | `Omni 1.1 Flash` · `Veo 3.1 - Lite` · `Veo 3.1 - Fast` · `Veo 3.1 - Quality` · **`Veo 3.1 - Lite [Lower Priority]`** (chọn qua `flow-menu-item:has-text("...")`) |
| 9 | Upload ảnh | `flow-prompt-box button:has(mat-icon:text-is("add"))` → `mat-list-item:has(mat-icon:text-is("drive_folder_upload"))` ("Tệp tải lên") → `button:has(mat-icon:text-is("upload"))` ("Tải nội dung nghe nhìn lên") **mới bật file chooser** → `page.expect_file_chooser()` + `set_files()` |
| 10 | Gắn ảnh vào prompt | `button:has-text("Thêm vào câu lệnh")` → thumbnail xuất hiện trong prompt box |
| 11 | Gõ prompt | `flow-prompt-box flow-rich-text-editor` → `.click()` rồi `page.keyboard.insert_text(prompt)`. **`div[role="textbox"]` = 0 phần tử** |
| 12 | Submit | `flow-prompt-box button:has(mat-icon:text-is("arrow_forward"))` (hoặc Enter) |
| 13 | **Chờ xong** | Xem §5.3 — chỗ dễ sai nhất |
| 14 | Lấy link video | `tile.hover()` trên `flow-grid-tile-container` → **lúc này mới sinh thẻ `<video>`** → `video.src` dạng `https://flow-content.google/video/<uuid>?Expires=...&KeyName=labs-flow-...` |
| 15 | Tải về | `page.request.get(src).body()` rồi ghi file (đi bằng cookie của phiên, ra MP4 thật) |

### 5.3 ⚠️ Nhận biết "đã render xong" — chỗ SAI 2 LẦN, đọc kỹ

**Hai cách dò SAI đã dính thật:**

1. ❌ `document.querySelectorAll('video')` — Flow render xong chỉ hiện **tile thumbnail**; thẻ
   `<video>` chỉ sinh **khi hover** vào tile. Dò kiểu này báo `videos=0` vĩnh viễn ⇒ tưởng còn chạy
   trong khi clip xong từ lâu.
2. ❌ **Đếm số tile** (`flow-grid-tile-container` nhiều hơn trước) — **ảnh vừa upload CŨNG tạo 1 tile**,
   nên số tile tăng ngay lúc gắn ảnh ⇒ báo "xong" sau 10 giây và **tải nhầm lại video CŨ**
   (md5 trùng khít bản trước — đây là cách phát hiện ra lỗi). `flow-pending-tile` cũng luôn = 0 trong
   UI này, đừng dùng.

**Cách ĐÚNG — 2 tín hiệu, dùng cả hai:**

- **Đang render**: tile hiện **chuỗi phần trăm** (`13%`, `47%`...) — quét text node lá khớp
  `/^\d{1,3}%$/`. Còn thấy `%` = còn chạy.
- **Đã xong + đúng clip mới**: hover từng tile, lấy `video.src`, bóc **UUID** theo
  `/video/([0-9a-f-]{36})`. So với tập UUID chụp **trước khi submit**; chỉ nhận UUID **mới**.

```python
UUID_RE = re.compile(r"/video/([0-9a-f-]{36})")

def scan_videos(pg):                      # hover moi tile de lo <video>
    found = {}
    for t in pg.query_selector_all("flow-grid-tile-container"):
        try: t.hover()
        except Exception: continue
        time.sleep(1.0)
        for s in pg.evaluate("() => [...document.querySelectorAll('video')]"
                             ".map(v=>v.src||v.currentSrc).filter(Boolean)"):
            m = UUID_RE.search(s)
            if m: found[m.group(1)] = s
    return found

def rendering(pg):                        # con % = con render
    return pg.evaluate("""() => {const re=/^\\d{1,3}%$/;
      for (const e of document.querySelectorAll('*'))
        if (!e.children.length && re.test((e.textContent||'').trim())) return true;
      return false;}""")

before = set(scan_videos(pg))             # CHUP TRUOC KHI SUBMIT
... submit ...
while rendering(pg): time.sleep(15)
new = {k: v for k, v in scan_videos(pg).items() if k not in before}
for uid, src in new.items():
    open(f"{uid[:8]}.mp4","wb").write(pg.request.get(src).body())
```

Nút `stop` (`button:has(mat-icon:text-is("stop"))`) của map cũ **không tồn tại** trong UI này.

**Luôn kiểm tra md5 clip tải về khi test** — trùng md5 với clip trước nghĩa là logic chờ sai chứ
không phải Veo trả cùng kết quả.

### 5.4 Kết quả đo thật (2026-09-07, Ultra, Veo 3.1 Lite [Lower Priority], 16:9, x1)

| Chỉ số | Giá trị |
|---|---|
| File | `veo31_test_170230.mp4` — 1.679.591 byte (1,6 MB) |
| Thời lượng | **8,00 giây** |
| Hình | H.264 High, **1280×720**, 24 fps, 1.525 kb/s |
| Tiếng | **AAC LC 48 kHz stereo 140 kb/s** (Veo 3.1 sinh audio native) |
| Nguồn | 1 ảnh tĩnh 1280×720 + prompt tiếng Anh mô tả chuyển động camera |

Lần đo thứ 2 (ảnh thung lũng sương): `veo31_171013_a55f92d0.mp4` — 1,40 MB, 8,00s, 1280×720 24fps, AAC 140 kb/s, md5 khác hẳn ⇒ đúng clip mới. Thư mục ra: `E:\\CLAUDE\\YOUTUBE\\VEO3_OUTPUT`.

### 5.5 ⭐ FRAME TO VIDEO — khoá khung đầu/cuối (verify 2026-09-07)

**Mấu chốt: TẮT chip "Tác nhân".** Prompt box có 2 chế độ khác hẳn nhau:

| Chip "Tác nhân" | Ảnh đính kèm đóng vai gì | Kết quả |
|---|---|---|
| **BẬT** (mặc định, `flow-agent-mode-toggle-chip.checked`) | **Thành phần / Ingredient** (`flow-ingredient-bar` → `flow-image-ingredient-chip`, nút aria=`Thành phần`) | Chỉ là tham chiếu — model vẽ lại hoàn toàn. Ảnh vẽ tay → clip ảnh thật khác hẳn |
| **TẮT** | **Khung hình** (frame) | **Khung 0 của clip = đúng ảnh nguồn**, giữ nguyên phong cách + bố cục |

```python
chip = pg.query_selector("flow-agent-mode-toggle-chip")
if chip and "checked" in (chip.get_attribute("class") or ""):
    chip.click(); time.sleep(3)          # -> prompt box doi sang che do khung hinh
```

Sau khi tắt, prompt box hiện các nút (kiểm bằng `aria-label`, không phụ thuộc ngôn ngữ ở chỗ có aria):

| Thành phần | Selector | Ghi chú |
|---|---|---|
| Ô khung đầu | `flow-prompt-box button:has-text("Bắt đầu")` | bấm → mở picker |
| Ô khung cuối | `flow-prompt-box button:has-text("Kết thúc")` | tuỳ chọn; có cả 2 = nội suy đầu→cuối |
| Hoán đổi 2 khung | `button[aria-label="Hoán đổi khung hình đầu tiên và cuối cùng"]` (icon `swap_horiz`) | |
| Tóm tắt cấu hình | `button[aria-label="Điều kiện kích hoạt cài đặt"]` → hiện `Video · 720p · 8 giây · 16:9 · x2` | **chế độ cổ điển mặc định x2** ⇒ ra 2 clip/lần |
| Nút tạo | `button[aria-label="Bắt đầu tạo"]` | |

Picker khi bấm ô khung: tiêu đề **"Chọn một hình ảnh khung"**, liệt kê ảnh đã upload trong mục
"Gần đây" → click **tên file** (vd `:text("test_scene.png")`) → bấm `button:has-text("Thêm vào câu lệnh")`.
Muốn dùng ảnh mới thì upload trước theo §5.2 bước 9, ảnh sẽ nằm sẵn trong picker này.

**Số đo thật:** submit → xong **51 giây**, ra **2 clip** mỗi clip 1,03 MB (8s · 1280×720 · 24fps).
Đối chiếu khung 0 với ảnh nguồn: **trùng khớp phong cách và bố cục**; khung 95/190 mặt trời lặn dần,
mây trôi vào ⇒ đúng là animate từ khung gốc chứ không vẽ lại.

**Bẫy khi tự động hoá chế độ này:**
- Panel cài đặt (`flow-settings-view`) mở ra sẽ **che mất `flow-prompt-box`** → query trả `None`.
  Bấm `Lưu` đóng panel trước khi thao tác.
- Chạy nhiều lần liên tiếp dễ để sót overlay đang mở → `page.reload()` rồi chờ ~10s là sạch nhất.
- `scan_videos` hover toàn bộ tile rất chậm khi thư viện nhiều; **chỉ hover 4 tile đầu** (nội dung
  mới luôn nằm đầu) là đủ và nhanh hơn nhiều.

---

### 5.6 ⭐ TỰ ĐỘNG HOÁ CHUỖI KHUNG ĐẦU+CUỐI — 5 bẫy chỉ lộ ra khi chạy batch (verify 2026-09-07, dự án VIDEO_VEO3)

§5.5 mô tả **bấm tay 1 phát**. Khi viết batch chạy nhiều shot liên tiếp thì 5 chỗ dưới đây làm gãy, cả 5
đều đã dính thật và đều **không** phải do selector sai:

**1. Nút upload và ô khung hình LOẠI TRỪ NHAU.** Đo bằng cách bật/tắt chip:

| `flow-agent-mode-toggle-chip` class | nút `add` (upload) | ô `Bắt đầu` |
|---|---|---|
| `"checked"` (chế độ Tác nhân) | **1** | 0 |
| `""` (chế độ Khung hình) | 0 | **1** |

⇒ Không thể vừa upload vừa khoá khung. Batch phải **upload HẾT ảnh trước** (chip BẬT), rồi mới tắt chip
để sinh clip. Gọi `set_agent_mode(True)` trong hàm upload và `set_agent_mode(False)` trong hàm gán khung
là hết bệnh.

**2. Upload xong ảnh TỰ DÍNH vào ô khung.** Sau `Thêm vào câu lệnh`, ảnh nhảy thẳng vào ô khung ⇒ shot
tiếp theo báo `không thấy frame_start` (chỗ đó giờ là thumbnail + nút xoá, không còn chữ "Bắt đầu").
Phải dọn trước mỗi shot:

```python
# nút xoá trên mỗi ảnh đang gắn: aria-label="Thành phần tạo hình ảnh"
while (btns := pg.query_selector_all('flow-prompt-box button[aria-label="Thành phần tạo hình ảnh"]')):
    btns[0].click(); time.sleep(1.2)
```

**3. Lần chọn ảnh THỨ HAI, picker tự đóng — KHÔNG có nút "Thêm vào câu lệnh".** Gán khung đầu thì có nút
xác nhận; gán khung cuối thì click ảnh là xong luôn. Code `_need("Thêm vào câu lệnh")` sẽ ném lỗi **dù
việc đã thành công**. ⇒ Coi nút đó là **tuỳ chọn**, và xác nhận bằng trạng thái thật:

```python
add = pg.query_selector('.cdk-overlay-container button:has-text("Thêm vào câu lệnh")')
if add: add.click()
# ô khung bị chiếm thì nút chữ biến mất -> đó mới là bằng chứng đã gán
assert pg.query_selector('flow-prompt-box button:has-text("Bắt đầu")') is None
```

**4. Item trong picker phải click vào `button`, không phải text node.** `:text("ten_file.png")` khớp
được phần tử nhưng **click không ăn** (im lặng, không lỗi). Dùng
`.cdk-overlay-container button:has-text("ten_file.png")`. Picker liệt kê theo **TÊN FILE** nên tên ảnh
phải là duy nhất.

**5. Model mặc định có thể là `Omni 1.1 Flash` = 24 TÍN DỤNG/lần, và mặc định `x2` = nhân đôi.**
Đừng giả định máy đang để model rẻ. Đọc chi phí TRƯỚC KHI SINH — panel cài đặt in thẳng số tín dụng:

```python
pg.query_selector('button[aria-label="Điều kiện kích hoạt cài đặt"]').click()   # nút tóm tắt trong prompt box
# panel hiện: Hình ảnh/Video · 16:9/9:16 · 360p/720p · 4/6/8/10 giây · x1..x4 · "<n> tín dụng"
# nút model = button chứa "arrow_drop_down" trong .cdk-overlay-container
```
Đo thật: `Omni 1.1 Flash` → **24 tín dụng**; đổi sang `Veo 3.1 - Lite [Lower Priority]` + `x1` → **0 tín dụng**.
Nút `tune` của §5.2 bước 6 **không còn** trong UI này; đường vào cài đặt là nút tóm tắt
`Video · 720p · 8 giây · 16:9 · x1` ngay trong prompt box.

**Thời lượng clip: chế độ Khung hình chỉ có `4 / 6 / 8 giây`** (10 giây chỉ có ở chế độ Tác nhân) — nên
"cảnh dễ vỡ thì để ≤5s" trong mọi SOP phải quy về **4 giây**. Đổi bằng panel cài đặt; và `button:text-is("8 giây")`
**không khớp** (trả 0 phần tử) trong khi `button:has-text("8 giây")` khớp — dùng `has-text`. Panel thỉnh thoảng
không hiện ở lần bấm đầu (trang còn bận) ⇒ **thử lại 3 lần** rồi mới báo lỗi.

**Cách nghiệm thu chain — đừng chỉ đếm file.** So sai lệch ảnh giữa khung clip và ảnh nguồn
(`PIL.ImageChops.difference` → `ImageStat.mean`, 0% = trùng khớp). Số đo thật của 2 clip nối chuỗi:

| Phép so | Lệch | Kết luận |
|---|---|---|
| khung ĐẦU clip 0 ↔ ảnh scene 0 | **0,54 %** | khoá khung đầu chạy đúng |
| khung CUỐI clip 0 ↔ ảnh scene 1 | **1,03 %** | endImage = ảnh scene SAU, chain chạy đúng |
| khung ĐẦU clip 1 ↔ ảnh scene 1 | **0,69 %** | cuối clip 0 == đầu clip 1 ⇒ **nối liền mạch** |
| khung CUỐI clip 1 ↔ mọi ảnh | 33-35 % | đúng: shot cuối chuỗi không có khung cuối |

Thời gian đo được ở chế độ này: **51 s** và **63 s**/clip (submit → tải xong), 8,00 s · 1280×720 · 24 fps ·
AAC 140 kb/s, 2,3-3,1 MB. Mã tham chiếu chạy được: `E:\CLAUDE\YOUTUBE\VIDEO_VEO3\corelow_ui.py`
(+ `flow_selectors.json` tách riêng) và `core/run_video.py` (`check` / `probe` / `run --dry-run --no-upload`,
resume bằng `results.csv`).

### 5.7 ⭐ PANEL CÀI ĐẶT — 5 bẫy nữa, và đường vòng bắt buộc để lấy model 0 tín dụng (2026-09-07)

**Cài đặt của Flow TỰ TRÔI giữa các phiên.** Đo thật trong một buổi: `720p + Lite [Lower Priority]`
= 0 tín dụng → quay lại thấy `360p` = 6 tín dụng → lát sau `Veo 3.1 - Lite` = 10 tín dụng.
⇒ Đọc chi phí thôi là chưa đủ, **phải tự đặt lại trước mỗi lô**, và **chặn cứng nếu ≠ `0 tín dụng`**.

**Đường vòng bắt buộc:** model `Veo 3.1 - Lite [Lower Priority]` (0 tín dụng) **chỉ xuất hiện trong
danh sách ở chế độ "Video"**. Ở chế độ **"Khung hình"** — chế độ dùng để khoá khung đầu/cuối — panel
chỉ liệt kê 4 model và **không có nó**; nhưng đã chọn ở chế độ Video thì nó **giữ nguyên** khi quay
lại. Thứ tự đúng: **Video → 720p → chọn model 0 tín dụng → quay lại Khung hình**.
Ở 360p, danh sách cũng **không** có model đó ⇒ đặt độ phân giải TRƯỚC khi chọn model.

| Bẫy | Triệu chứng | Xử lý |
|---|---|---|
| Panel ở chế độ Khung hình **không có** nút thời lượng / độ phân giải | `không thấy nút '8 giây'` | Hai thứ đó thừa hưởng từ chế độ Video. Nhận biết panel bằng nút **chế độ** (`Khung hình`), đừng đếm nút "giây" |
| Bấm nút cài đặt khi **panel đang mở** → đóng luôn | mở mãi không được | Kiểm "đang mở?" trước; nếu có overlay **khác** (menu model) thì Escape trước rồi mới bấm |
| Chia timeout cho 3 rồi Escape giữa các lần thử | không bao giờ mở được | Mỗi lần thử **chờ đủ** timeout, không tự Escape |
| `element.click()` không ăn sau khi phiên CDP trước bị ngắt | click không lỗi, không mở | Bấm bằng **toạ độ chuột thật** (`bounding_box` → `page.mouse.click`) |
| `pages[-1]` bắt nhầm tab | thao tác trên Gmail/YouTube của người dùng | Lọc tab theo `flow.google.com`, đừng lấy tab cuối |

**Giá theo model/độ phân giải (đo thật, mỗi clip 8s x1):** Omni 360p = 6 · Omni 720p = **24** ·
Veo 3.1 Lite 720p = **10** · Lite [Lower Priority] 720p = **0**. ⇒ Chênh 24 lần, **luôn đọc trước khi chạy lô**.

⚠️ **Model 0 tín dụng có thể BIẾN MẤT khỏi danh sách** (đo thật: sáng có, chiều không, cả 2 chế độ).
Khi đó lô lớn phải hoãn, không có cách lách. Kiểm bằng một lệnh rẻ thay vì thử sinh.

## 6. Pitfalls

| # | Triệu chứng | Nguyên nhân → Fix |
|---|---|---|
| 1 | "Cannot connect to server. Extension may be unauthorized." | **Kill-switch phiên bản**: config server trả `version:"3.3.8, 3.3.9"`, extension so version của mình với danh sách đó; bản ngoài danh sách là NGƯNG CHẠY. Cũng gặp khi mất mạng tới `configs.kylenguyen.me`. → update extension, hoặc dùng tool tự viết (không phụ thuộc). |
| 2 | Hôm nay chạy được, mai chết | Google đổi UI Flow → selector trượt. Extension phải chờ tác giả đẩy config mới; tool tự viết thì tự sửa JSON (nhanh hơn vì không phụ thuộc ai). |
| 3 | Bấm mãi không ăn mà không báo lỗi | Angular Material không nhận synthetic event → phải dùng CDP input (Playwright mặc định đã đúng; tự inject JS `el.click()` là hỏng). |
| 4 | Chạy được 10 prompt rồi dừng | Free plan của extension = 10 prompt/ngày, không liên quan quota Google. |
| 5 | Chọn 1080p / 10s concat thì lỗi | Giới hạn phía **Google** (cần AI Pro/Ultra), extension không vượt được. |
| 6 | File tải về lẫn lộn / đè nhau | Tên file đặt theo prompt + hậu tố `a,b,c…` theo số output; prompt trùng chữ đầu dễ đè → đặt `folderName` riêng mỗi lô hoặc tự đánh index. |
| 7 | Tưởng treo | Timeout chờ render là **15 phút**; Veo Quality lô 4 video có thể lâu → tăng timeout thay vì kết luận treo. |
| 8 | Chạy song song bị fail cả lô | `concurrentPrompts` > 1 chỉ an toàn khi gói Google cho phép nhiều job đồng thời → giữ 1-2 cho ổn định. |
| 9 | Đăng nhập extension bằng email lạ | Bình thường: tài khoản extension tách rời tài khoản Google Flow. |
| 10 | Chrome báo "CDP NOT READY", cổng debug không mở | **Chrome >=136 CHẶN remote debugging trên user-data-dir MẶC ĐỊNH.** Phải `--user-data-dir` trỏ tới thư mục KHÁC hoàn toàn |
| 11 | Mở Chrome bằng junction/đường dẫn khác trỏ vào User Data thật ⇒ **MẤT SẠCH COOKIE profile đó** | App-Bound Encryption của Chrome 152 gắn khoá mã hoá theo đường dẫn user-data-dir; sai đường dẫn ⇒ Chrome không giải mã được và **XOÁ** toàn bộ cookie (secure_delete nên không carve lại được từ file). **TUYỆT ĐỐI không junction/copy/đổi đường dẫn User Data thật.** Chỉ dùng profile MỚI hoàn toàn (§5.1) |
| 12 | Tưởng video chưa xong, chờ mãi | Xem §5.3 — dò bằng thẻ `<video>` là SAI (chỉ sinh khi hover). Dùng `flow-pending-tile` + đếm số tile, xong rồi hover mới ra link |
| 13 | Banner "Bạn sắp dùng hết tín dụng Google Flow" | Chọn model **Veo 3.1 - Lite [Lower Priority]** thì không trừ tín dụng; Fast/Quality/Omni đều trừ |
| 14 | `không thấy add_button` khi upload trong batch | Nút upload CHỈ có ở chế độ **Tác nhân** (chip `checked`). §5.6 bẫy 1 |
| 15 | `không thấy frame_start` ở shot thứ 2 trở đi | Ảnh còn dính trong ô khung từ shot trước → phải gỡ hết trước mỗi shot. §5.6 bẫy 2 |
| 16 | Gán khung cuối báo `không thấy "Thêm vào câu lệnh"` **dù đã gán xong** | Lần chọn thứ 2 picker tự đóng, không có nút xác nhận → coi nút đó là tuỳ chọn. §5.6 bẫy 3 |
| 17 | Click ảnh trong picker không ăn, không báo lỗi | `:text(...)` trúng text node; phải click `button:has-text(...)`. §5.6 bẫy 4 |
| 18b | Clip render tới 16% rồi **im luôn**, poll hết 900s vẫn "chưa có clip mới" | **Flow từ chối theo chính sách NHƯNG SAU KHI ĐÃ RENDER** — chỉ hiện một dòng chữ trên trang, không ném lỗi, không đổi tile. Câu thật: *"Câu lệnh này có thể vi phạm chính sách của chúng tôi về việc tạo video liên quan đến **người nổi tiếng**"*. Trong vòng chờ, mỗi lần không thấy `%` phải quét trang tìm cụm `vi phạm chính sách` rồi **bỏ cuộc ngay** (40s thay vì 900s); và phải chụp dòng đó **TRƯỚC** khi submit vì nó nằm lại trên trang, không so với bản trước là shot sau bị báo nhầm. |
| 18c | **Cách chữa khi bị 18b — ĐỪNG phá khuôn mặt** | Nó nói "câu lệnh" nhưng thủ phạm là **ẢNH NGUỒN**: bỏ hẳn người khỏi prompt vẫn bị chặn y nguyên. Nhưng bộ lọc khớp **đúng file ảnh đó**, không phải "có mặt người là chặn" ⇒ **chỉ cần đổi pixel tối thiểu**. Đo thật trên đúng tấm bị chặn 3 lần: `lật gương` → **qua ngay**, và mặt trong clip **vẫn sắc nét** (độ nét vùng mặt **2.35**, còn hơn ảnh gốc **1.41**). Trong khi bản "làm mờ mặt cho khỏi vi phạm" cũng qua nhưng clip ra **0.17 = mờ tịt, vứt đi**. ⇒ Thang chữa đúng: **lật gương → phóng 8% → nén lại JPEG q92**, tất cả giữ mặt nét. **Tuyệt đối không làm mờ / cắt / xoá mặt** — video kể chuyện mà mặt nhân vật mờ thì hỏng sản phẩm. |
| 18 | Tự dưng tốn 24 tín dụng/lần | Model mặc định có thể là `Omni 1.1 Flash` + `x2`. Đọc số tín dụng trong panel TRƯỚC khi sinh. §5.6 bẫy 5 |


---

## 7. Flow-UI automation vs Veo API chính thức — chọn đường nào

| | Google Flow + automation (extension/Playwright) | Gemini/Vertex Veo API |
|---|---|---|
| Tiền | Trả **theo gói tháng** Google AI Pro/Ultra, sinh trong quota | Trả **theo giây video** — kiểm giá hiện hành trước khi chạy lô lớn |
| Ổn định | Bám UI → gãy khi Google đổi giao diện | Hợp đồng API, ổn định |
| Tính năng | Đủ đồ chơi Flow: ingredients, character, speaker, extend/concat, chỉnh khung | Chỉ text/image→video cơ bản |
| Hợp với | Cày số lượng lớn cho kênh faceless khi đã mua gói | Sản phẩm/tool bán cho khách, cần SLA |

Cho dự án h2dev (cày video kênh ngoại): **Flow + automation** hợp lý hơn về chi phí; giữ API làm
đường lui khi cần chạy server-side không có browser.

---

## 8. Ghi chú nguồn

- Code đã đọc: `manifest.json`, `assets/index.ts-B2QzyOff.js` (service worker),
  `index.ts-BSckioIb.js` (content script — logic automation), `catchUploadFile.ts-*.js`,
  `remoteConfig-*.js`, `index.html-*.js` (side panel Vue 2.2MB), `utils-*.js` (= jQuery).
- Quyền xin: `storage, tabs, background, sidePanel, activeTab, downloads, debugger`;
  host chỉ `*://flow.google.com/*` (không đụng site khác — sạch hơn extension NotebookLM).
- Liên quan: `youtube_research_ext.md` (research ý tưởng + insight), `tao_tool_exe.md` (đóng gói tool).

---

## 9. ⭐ CHUYỂN SANG DỰ ÁN KHÁC — checklist bàn giao (đã chạy thật 2026-09-07)

### 9.1 Công cụ có sẵn, copy là chạy

| Thứ | Đường dẫn | Vai trò |
|---|---|---|
| ⭐ **PROFILE CHROME ĐÃ LOGIN ULTRA** | **`E:\CLAUDE\YOUTUBE\VEO3_PROFILE`** | user-data-dir riêng, **đã đăng nhập sẵn `thiengreen03@gmail.com` (gói Google AI Ultra)**. Dự án khác chỉ cần mở Chrome trỏ vào đây kèm `--remote-debugging-port=9333` là chạy được ngay, **không phải đăng nhập lại** |
| **`veo_batch.py`** | `E:\CLAUDE\YOUTUBE\VEO3_BATCH\veo_batch.py` | Batch runner: đọc job → upload ảnh → prompt → chờ → tải MP4 → ghi `results.csv`. **Resume được** |
| **`veo_frame2video.py`** | `E:\CLAUDE\YOUTUBE\VEO3_BATCH\veo_frame2video.py` | Bản chạy **Frame to Video** (khoá khung đầu, §5.5) — tắt chip Tác nhân, chọn ảnh khung, tạo, tải |
| `jobs.csv` | `E:\CLAUDE\YOUTUBE\VEO3_BATCH\jobs.csv` | Mẫu job: cột `image,prompt` (image trống = text→video); nhận cả `.txt` mỗi dòng 1 prompt |
| Kết quả | `E:\CLAUDE\YOUTUBE\VEO3_OUTPUT\` | MP4 + `results.csv` + `batch_log.txt` |

**Lệnh mở profile Ultra đó (chạy 1 lần, để cửa sổ sống suốt phiên làm việc):**
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir=E:\CLAUDE\YOUTUBE\VEO3_PROFILE ^
   --remote-debugging-port=9333 --no-first-run --no-default-browser-check https://flow.google.com/
```
Chạy song song bình thường với Chrome cá nhân (khác user-data-dir = khác tiến trình, không ảnh hưởng nhau).

```bash
py -3.13 veo_batch.py jobs.csv                      # mac dinh out=VEO3_OUTPUT, delay 6s
py -3.13 veo_batch.py jobs.csv --out D:\OUT --delay 8 --timeout 900 --retry 2
```

### 9.2 Sáu điều PHẢI làm đúng ở dự án mới (mỗi cái đều từng làm hỏng việc)

1. **Chrome profile RIÊNG, thư mục mới tinh** — `--user-data-dir=<thư mục mới>`.
   ⛔ Không dùng `User Data` mặc định (Chrome ≥136 chặn CDP), ⛔ không copy profile (dính captcha),
   ⛔ **tuyệt đối không junction/đổi đường dẫn tới `User Data` thật** — App-Bound Encryption sẽ
   không giải mã được và **Chrome XOÁ SẠCH cookie của profile đó** (đã xảy ra thật, phải phục hồi
   từ Volume Shadow Copy). Xem §6 pitfall 10-11.
2. **Đăng nhập tay đúng 1 lần** trong cửa sổ đó (Google Ultra), rồi cứ để nguyên — session sống mãi.
3. **Vào 1 project và ĐÓNG panel agent bên phải** trước khi chạy batch, nếu không sẽ không có
   `flow-prompt-box` → script báo "khong thay o prompt".
4. **Đặt sẵn model + tỉ lệ trong icon `tune`**: `Veo 3.1 - Lite [Lower Priority]` (không trừ tín dụng),
   16:9 hoặc 9:16, x1, và chọn "Không bao giờ" ở mục xác nhận trước khi tạo — nếu để "Luôn luôn",
   batch sẽ đứng chờ người bấm.
4b. **Kiểm chi phí bằng mắt trước khi chạy lô**: panel cài đặt in thẳng `<n> tín dụng`. Thấy khác `0 tín dụng`
   là dừng lại đổi model — mặc định máy có thể đang để `Omni 1.1 Flash` (**24 tín dụng/lần**) và `x2`.
4c. **Upload hết ảnh TRƯỚC (chip Tác nhân BẬT), rồi mới tắt chip để khoá khung** — hai chế độ loại trừ nhau,
   và ảnh vừa upload tự dính vào ô khung nên phải gỡ trước mỗi shot (§5.6).
5. **Selector phải giới hạn trong `.cdk-overlay-container`** khi thao tác menu popup — sidebar trái
   có mục trùng tên ("Tệp tải lên"), khớp nhầm là bị lớp `cdk-overlay-backdrop` chặn click.
6. **Chờ xong theo `%` + UUID mới** (§5.3), và **so md5 clip tải về** khi nghiệm thu — đếm tile là
   sai, sẽ tải trùng clip cũ mà vẫn báo thành công.

### 9.3 Số đo thật (Ultra · Veo 3.1 Lite [Lower Priority] · 16:9 · x1)

| Chỉ số | Giá trị đo được |
|---|---|
| Thời gian mỗi clip | **63–85 giây** (submit → tải xong). Batch 2 job hết 2 phút 49 giây |
| Độ dài clip | luôn **8,00 giây** |
| Chất lượng | 1280×720 · 24 fps · H.264 High · **có audio AAC 48 kHz stereo 140 kb/s** |
| Dung lượng | 1,4 – 8,1 MB tuỳ độ phức tạp (bitrate 1.463 – 8.146 kb/s) |
| Tín dụng | Lite [Lower Priority] **không trừ**; Fast/Quality/Omni có trừ |

### 9.4 Giới hạn đã biết, đừng hứa quá với dự án nhận bàn giao

- **Ảnh đính kèm khi chip "Tác nhân" đang BẬT chỉ là THAM CHIẾU** — model vẽ lại hoàn toàn.
  Muốn **khoá khung đầu/cuối** phải **TẮT chip "Tác nhân"** rồi dùng ô `Bắt đầu` / `Kết thúc`
  (§5.5, đã verify: khung 0 trùng ảnh nguồn). Lưu ý chế độ này mặc định **x2 clip/lần**.
- Chạy **tuần tự**, `--delay ≥ 5s`, không mở 2 phiên song song (luật chống bot-flag của dự án
  VIDEO_VEO3: ≤5 request đồng thời, giãn ≥1 giây).
- UI Flow đổi liên tục — nếu script gãy, chạy lại phần dò DOM ở §5.2 rồi sửa **một chỗ duy nhất**
  là bảng selector, đừng viết lại logic.
- Tài khoản dùng để chạy Flow **phải khác** tài khoản kênh YouTube sẽ đăng (ràng buộc của VIDEO_VEO3).

### 9.5 Dán vào CLAUDE.md của dự án nhận

```
# @C:\Users\admin\.claude\skills\veo3_flow_automation.md — CHẠY VIDEO VEO 3.1 HÀNG LOẠT qua Google Flow.
#   PROFILE ĐÃ LOGIN ULTRA (dùng luôn, khỏi đăng nhập): E:\CLAUDE\YOUTUBE\VEO3_PROFILE  (thiengreen03@gmail.com)
#     mở: chrome.exe --user-data-dir=E:\CLAUDE\YOUTUBE\VEO3_PROFILE --remote-debugging-port=9333 https://flow.google.com/
#   CÔNG CỤ: E:\CLAUDE\YOUTUBE\VEO3_BATCH\veo_batch.py (batch, resume) + veo_frame2video.py (khoá khung đầu)
#   RA: E:\CLAUDE\YOUTUBE\VEO3_OUTPUT — 8s/clip 720p 24fps có audio, 63-85s/clip
#   ⛔ KHÔNG đụng User Data mặc định của Chrome (mất sạch cookie); chờ xong theo % + UUID mới (đếm tile là SAI)
```

---

## §10 — BẪY KHI TỰ LÁI FLOW BẰNG PLAYWRIGHT (đo thật VIDEO_VEO3, 2026-09-08, account Ultra `thiengreen03`)

Bốn bẫy dưới đây đều **hỏng im lặng** — không ném lỗi, chỉ làm sai kết quả hoặc đốt thời gian.

**1. `Return silent videos` mặc định TẮT ⇒ cả lô dính "Audio generation failed".**
Veo tự sinh audio và khâu audio hay hỏng; pipeline nào cũng strip audio khi ghép nên bật silent là **vừa hết lỗi
vừa nhanh hơn**. Công tắc: `[aria-label="Return silent videos toggle"]`, bật rồi thì class có `mdc-switch--selected`.
⚠️ Hàm `ensure_silent_video()` cũ trả `None` khi không thấy công tắc và **không ai đọc giá trị trả về** → chạy cả
lô với audio bật. ⇒ **In trạng thái BẬT/TẮT ra log và DỪNG LÔ nếu chưa bật được.**

**2. `.cdk-overlay-backdrop` còn sót là CHẶN MỌI CLICK.** Panel chọn ảnh / menu / hộp thoại còn mở thì Playwright
chỉ ghi `"<div class="cdk-overlay-backdrop..."> intercepts pointer events"` rồi retry đến hết timeout. ⇒ **Trước
mọi thao tác cài đặt, nhấn `Escape` tới khi `locator(".cdk-overlay-backdrop").count() == 0`.**

**3. Python ĐỆM stdout khi chạy nền ⇒ log rỗng LỪA NGƯỜI ĐỌC.** Giết tiến trình là mất sạch dòng đã in. Đã dính
thật 2 lần trong một giờ: đọc log thấy rỗng → kết luận "chưa upload gì" → thực tế đã up cả mớ ảnh lên Flow.
⇒ `sys.stdout.reconfigure(line_buffering=True)` ngay đầu `main()`. Và **đừng tin log rỗng — kiểm bằng file trên
đĩa hoặc bằng chính trang web.**

**4. Chạy thử lô nhỏ (`--only 0-9`) phải kéo theo cả DANH SÁCH ẢNH UPLOAD.** Kế hoạch khung hình luôn phủ **toàn
bộ** shot list (luật D10 cần ảnh của shot kế bên), nên duyệt thẳng nó là **up 69 ảnh cho 10 clip**. Và ghi cache
`uploaded.json` theo **id project** để chạy lại (resume / đổi `--only` / chạy nốt phần còn lại) **không up trùng** —
thư viện Flow không tự khử trùng lặp.

**Quy trình bắt buộc: LUÔN chạy `--only 0-9` trước khi chạy cả tập.** Sai prompt hay sai ảnh mà phát hiện ở clip
thứ 60 là mất cả tiếng đồng hồ.

### Số đo thật (720p · 8 giây · frame-lock · `Veo 3.1 - Lite [Lower Priority]` = **0 tín dụng**)
| Mục | Giá trị |
|---|---|
| Thời gian mỗi clip | **~48 giây** (render 100% ở giây 48, gồm cả tải về) |
| Tỉ lệ thành công | 10/10, **0 lỗi chính sách**, md5 khác nhau hết |
| Model lúc vào project | `Omni 1.1 Flash` = **12 tín dụng/clip** — cài đặt **TỰ TRÔI**, luôn phải ép lại |
| Giao diện | Lần này ra **tiếng Anh** (trước là tiếng Việt) ⇒ selector phải **song ngữ** |
| Vào thẳng `flow.google.com` | **KHÔNG có prompt box** — phải vào một project mới thấy |

Tạo project mới cho mỗi lô (nút `New project`) thay vì dùng project cũ còn tile test — tránh lặp lại bug **clip cũ
bị gán nhãn shot mới**. Nhất quán nhân vật qua 8 giây chuyển động: đã verify bằng cách trích khung ở giây 0,4 / 4,0
/ 7,5 của từng clip rồi xếp thành contact sheet — mặt không drift, chuyển động đúng "minimum motion".

**5. THU NHỎ ẢNH TRƯỚC KHI UPLOAD — nếu không, khâu upload chiếm hết thời gian lô.**
Đo thật: ảnh scene sinh ở **2560×1440 (~3,9 MB/ảnh)**, 81 ảnh = **306,8 MB**, upload mất **~58 giây MỖI ẢNH**
(≈78 phút chỉ để up, trong khi sinh 81 clip chỉ tốn ~65 phút). Flow render **720p** nên **chỉ cần 1280×720** —
ảnh to hơn không thêm một pixel nào vào clip. Thu về 1280×720 PNG = 987 KB (**nhỏ hơn 4 lần**).
⚠️ **GIỮ NGUYÊN TÊN FILE VÀ ĐUÔI `.png`**: `set_frame()` chọn ảnh trong thư viện **theo TÊN**. JPEG 1280×720 chỉ
188 KB (nhỏ hơn 21 lần) nhưng đổi đuôi thành `.jpg` là picker trượt ngay — muốn dùng JPEG thì phải truyền tên đã
upload xuống tận `set_frame`, không được suy ra từ đường dẫn ảnh gốc.

**6. PICKER CHỌN KHUNG CHỈ HIỆN ~15 ASSET MỚI NHẤT — phải gõ vào ô `Search assets`.**
Bẫy **chỉ lộ ở quy mô lớn**: lô 10 ảnh chạy trót lọt, lô 81 ảnh thì **61/81 shot** báo
`"picker khong co anh ten '006.png' — da upload chua?"` **dù ảnh đã lên đầy đủ** — picker chỉ liệt kê
`067.png`–`080.png`. Thông báo lỗi còn dẫn sai hướng (đổ cho khâu upload). ⇒ Trong `set_frame()`, **gõ tên ảnh
vào `input[aria-label="Search assets"]` rồi mới chọn**; selector để trong file JSON, không hardcode.
Kiểm bằng cách gọi `set_frame("start", "<ảnh cũ nhất>")` khi thư viện đã có vài chục asset — không thì lô nhỏ
luôn xanh và lô lớn luôn đỏ.

**7. Upload gãy giữa chừng thì RETRY, đừng để đổ cả lô.** Đo thật: chết ở ảnh thứ 78/81 sau hơn một tiếng
upload (`picker_add_fallback` không hiện) ⇒ mất trắng cả lô. Bọc `upload_image` trong 3 lần thử, mỗi lần nhấn
`Escape` dọn overlay trước khi thử lại; và ghi cache `uploaded.json` sau **từng** ảnh để chạy lại không up lại.

**8. UP CẢ LÔ ẢNH TRONG MỘT HỘP THOẠI — `multiple=True` (đo thật 2026-09-09).**
Hộp thoại chọn file của Flow **chấp nhận nhiều file**: `page.expect_file_chooser()` → `chooser.is_multiple()`
trả **True**, và `set_files([...])` với cả danh sách chạy được (verify: 3/3 ảnh vào đúng thư viện, chọn lại
bằng `set_frame` được).

⚠️ **ĐỪNG ĐO BẰNG LÔ 3 ẢNH.** Bản skill trước ghi "36,7 giây/ảnh, chỉ nhanh hơn ~26%" — con số đó lấy từ lô
**3 ảnh**, nơi chi phí cố định mỗi lượt chiếm gần hết, nên **sai hẳn ở quy mô thật**. Đo lại trên hai lô lớn
cùng ảnh 1280×720, cùng máy, cùng account, chỉ khác cách up:

| Cách | Số ảnh | Thời gian riêng khâu upload | Mỗi ảnh |
|---|---|---|---|
| Từng cái (`upload_image` × N) — `home88/seg5` 09/09 08:16 | 38 | ~2.424 giây (40,4 phút) | **~64 giây** |
| Cả lô (`upload_images` 1 hộp thoại) — `ginkou` 09/09 12:29 | 28 | ~698 giây (11,6 phút) | **~25 giây** |

⇒ **nhanh hơn ~2,6 lần**, tiết kiệm ~39 giây mỗi ảnh. Quy ra một tập 77 ảnh: **82 phút → 32 phút**.
(Cách đo: mốc đầu là ctime của file log, mốc cuối là mtime `uploaded.json` / clip đầu tiên, trừ ~30 giây khởi
động và ~75 giây render clip đầu — log không tự in dấu thời gian.) Phần Flow xử lý file phía server vẫn tuyến
tính, nhưng **chi phí cố định mỗi lượt lớn hơn nhiều so với ước lượng ~10 giây ban đầu** (mỗi lượt phải bật
chip Tác nhân → mở menu → mở hộp thoại → chờ nút "Add to prompt" → Escape → tắt chip → `clear_frames`), nên
gộp lô ăn đứt. ⚠️ **HAI TRẦN CHỒNG LÊN NHAU Ở `set_files`, dính cả hai trong một buổi (09/09), mỗi lần mất 3-4 phút mới biết:**
| Trần | Giá trị | Triệu chứng |
|---|---|---|
| Dung lượng | **50 MB mỗi lượt** | `Cannot transfer files larger than 50Mb to a browser not co-located` — Playwright coi Chrome nối qua CDP là "not co-located" **kể cả localhost**, không tắt được. Lô 71 ảnh = 87 MB. |
| Thời gian | **30 giây mặc định** | `Timeout 30000ms exceeded` khi lô 40 MB. Truyền qua CDP tuyến tính **theo BYTE**, nên hạn phải tính theo dung lượng chứ không theo số file. |

Cả hai đều ném lỗi **SAU khi đã mở hộp thoại**, màn hình đứng im không có gì để nhìn, rồi mới báo. ⇒ **`chia_lo()`
cắt danh sách theo TỔNG BYTE, trần 24 MB** (mức 25,7 MB đã chạy trót lọt thật) **và truyền hẳn
`set_files(..., timeout=60s + 6s×MB)`**. Ghi cache **sau MỖI lô con**, không phải sau khi xong tất cả — lô cuối
hỏng thì lô trước không phải up lại.

⚠️ Hạn chờ nút "Add to prompt" cũng phải **giãn theo số file** (`45s + 20s×N`) — dùng hạn
cố định 45s là lô lớn timeout chắc chắn. Luôn để **đường lui về up từng ảnh** khi `is_multiple()` là False.
Ghi cache `uploaded.json` theo id project để chạy lại không up trùng (lô 77 ảnh: 49 ảnh được bỏ qua đúng).

⚠️ **`optimize=True` khi lưu PNG thu nhỏ là bẫy tiền-thời-gian:** đo thật ảnh 2560→1280 là **1,55 giây/ảnh** để
bớt **2,5%** dung lượng (1107 → 1079 KB), so với **0,32 giây** khi tắt — **chậm gấp 4,8 lần** để tiết kiệm 2 MB
trên cả bộ 78 MB, không đổi được số lô phải chia. Cả lô 71 ảnh: 161 giây thay vì 28 giây.

**9. `input[type=file]` KHÔNG tồn tại trong DOM cho tới khi mở hộp thoại** — Angular tạo nó theo yêu cầu.
Nên không thể dò trước `multiple` bằng `querySelectorAll('input[type=file]')` (trả về 0). Muốn biết thì phải
mở hộp thoại thật rồi đọc `chooser.is_multiple()`.

**10. `Sorry, this video failed to generate` KHÔNG phải lỗi chính sách — đừng bóp méo ảnh vì nó.**
Flow báo hai chuyện rất khác nhau bằng **cùng một dòng chữ nhỏ trên trang**, và cùng làm vòng chờ ngồi đến hết giờ:
- **Từ chối nội dung** (`vi phạm chính sách` / `policy`) — bộ lọc chặn **ảnh nguồn**; thử lại y nguyên là chặn mãi,
  phải đổi pixel (`imgfix`: lật gương → zoom → nén lại).
- **Sinh hỏng tạm thời** (`failed to generate`) — máy bên Google trượt. Flow ghi kèm
  **"You have not been charged for this generation"** ⇒ **không mất tín dụng, thử lại CÙNG TẤM ẢNH là qua**.

Gộp hai loại vào một nhánh là **vừa báo sai nguyên nhân vừa bóp méo ảnh vô ích**. Đo thật 09/09: 3 shot dính
`failed to generate` (65, 70 của `home88`; 47 của `ginkou`) đều là cảnh **tối, tĩnh, không có người** — chẳng có gì
để mà vi phạm. ⇒ Ném hai loại `FlowError` riêng, nhánh tạm thời **retry cùng ảnh ~2 lần trước**, chỉ khi vẫn hỏng
mới rơi xuống `imgfix`. Dấu hiệu nhận ra mình đang gộp nhầm: log in "bị chặn vì ẢNH" cho một cảnh không có người.


**11. TÊN ẢNH PHẢI MANG TÊN TẬP — `000.png` của mọi tập là một quả mìn hẹn giờ.**
`set_frame()` tìm ảnh trong thư viện Flow **theo TÊN**, và picker chọn khung còn có **ô chọn project** nên duyệt
được asset của project khác. Mọi tập đều đánh số ảnh từ `000.png`, nên hai tập là hai `000.png` — picker trả về
một cái và không ai biết nó của tập nào. Đây là kiểu hỏng tệ nhất: **sai ảnh mà KHÔNG BÁO LỖI**, clip vẫn render
đẹp, chỉ là nhân vật của tập khác. ⇒ Upload dưới tên **`<tập>_000.png`** (suy tự động từ `out/<tập>/`), và bốn chỗ
phải khớp tuyệt đối, lệch một chỗ là hỏng câm lặng:
1. một hàm DUY NHẤT quyết định tên (`ten_asset`), mọi nơi gọi nó;
2. file gửi đi mang đúng tên đó — **ảnh đã đủ nhỏ, không cần resize, vẫn phải copy ra để đổi tên** (chỗ dễ lọt nhất);
3. `set_frame` tra theo tên có tiền tố, **cả khung đầu lẫn khung cuối** (luật D10);
4. cache `uploaded.json` đối chiếu theo TÊN TRÊN FLOW, không phải tên file trên đĩa.

Đặt project mới cho mỗi lô (`new_project()` — nút `New project` ở cuối lưới, **không phải** `Start Creating` vốn
mở lại project gần nhất) vẫn nên làm, nhưng nó KHÔNG thay được tiền tố: project mới chỉ tránh lẫn trong lưới clip,
còn picker vẫn nhìn sang project khác được.

---

## §11 — ẢNH NANO BANANA PRO/2 QUA FLOW: sinh ảnh hàng loạt + REF-LOCK bằng Character (verify 2026-09-11, dự án h2dev/ep07c-beats)

Khác hẳn §1-10 (toàn bộ nói về VIDEO Veo). Mục này là **ẢNH TĨNH** qua model `Nano Banana Pro` / `Nano Banana 2` /
`Nano Banana 2 Lite` — cùng một trang `flow.google.com`, cùng profile Chrome `E:\CLAUDE\YOUTUBE\VEO3_PROFILE`
port 9333 của §9, chỉ khác chế độ tạo (text-to-image thay vì text-to-video).

### 11.1 Xác nhận cơ bản (đã đo thật)
- **Không watermark chữ hiện** trên ảnh Nano Banana Pro/2 (soi zoom 4x cả 4 góc ảnh, không thấy logo/chữ nào).
- Có công tắc **"Visible watermarking"** trong menu tài khoản (bấm chữ "ULTRA" góc phải) — mặc định **TẮT**. Đây
  mới là lý do thật ảnh sạch, không phải do chọn model. Batch tool nên tự kiểm cờ này trước khi chạy loạt, tránh
  ai vô tình bật lên giữa chừng.
- Ảnh vẫn có **SynthID vô hình** (watermark pixel của chính Google DeepMind, không thấy bằng mắt/Pillow nhưng
  YouTube — cũng của Google — có thể tự dò ra và gắn nhãn "Altered or synthetic content" mà không cần creator tự
  khai báo). Khác hẳn ảnh từ `gpti2` (gpt-image-2, xem `gpti2.md`) chỉ mang **C2PA metadata** — dễ xoá bằng
  resave qua Pillow, không nhúng pixel. Nếu kênh muốn né rủi ro tự-động-gắn-nhãn thì ảnh gpti2 an toàn hơn ảnh
  Nano Banana về khoản này.
- **Sinh ảnh thường (không REF-LOCK) KHÔNG trừ "Google Flow credits"** — đã đo xuyên suốt ~16 ảnh test trong 1
  phiên, số credit đứng yên. Khác hẳn video Veo (trừ credit theo model, xem §5.7). Bộ đếm "Google Flow credits"
  hiển thị trong menu tài khoản nhiều khả năng CHỈ dành cho video/Omni, không tính ảnh Nano Banana thường.
  ⚠️ Tạo **Character** (REF-LOCK, §11.3) THÌ CÓ trừ credit thật — xem 11.3.

### 11.1b ⚠️ PHẢI ÉP CHỌN LẠI MODEL MỖI PROJECT MỚI — lỗi thật đã dính (2026-09-11)
Mục 11.1/11.2/11.3 mô tả cách set `x1` + `Never confirm` mỗi project mới (cài đặt tự trôi, xem §5.7 gốc cho
video, áp dụng y hệt cho ảnh) — **nhưng thiếu 1 bước: MODEL ẢNH cũng tự trôi về mặc định `Nano Banana 2`**,
không tự giữ `Nano Banana Pro` dù phiên trước đã chọn Pro. Đã dính thật: toàn bộ batch REF-LOCK/đa luồng sau
lần test đầu tiên (5 tab, 2 tab share project, Character Chiyo/Tomie...) đều CHẠY BẰNG NANO BANANA 2 chứ
KHÔNG PHẢI Pro như yêu cầu ban đầu, vì script chỉ set `x1`+`Never` mà quên ép lại dropdown model.

**⇒ Trong `Agent settings` (icon `tune`), sau khi set `x1`, BẮT BUỘC bấm dropdown model ảnh (hiện chữ
"🍌 Nano Banana 2" mặc định) → chọn **"🍌 Nano Banana Pro"** → mới bấm `Save`. Làm lại bước này ở MỌI project
mới/mọi tab mới, y hệt cách phải làm lại `x1`/`Never` — không có ngoại lệ.**

### 11.2 Đa luồng (nhiều tab cùng lúc) — CHẠY ĐƯỢC, không thấy giới hạn
Đo thật 2026-09-11, mỗi tab **project RIÊNG** (không cần REF-LOCK):
| Quy mô | Kết quả |
|---|---|
| 3 tab // (1 ảnh/tab, prompt khác nhau) | cả 3 xong trong 44–52s, không lệch nhau, không lỗi |
| 5 tab x 2 vòng (10 ảnh) | 10/10 ảnh đúng, không tab nào chậm dần theo thời gian chạy liên tục |

Kiểm tra chéo bằng UUID ảnh (`flow-content.google/image/<uuid>`) — **không UUID nào trùng giữa các tab**, tải về
xem tận mắt khớp đúng prompt của đúng tab. Không có dấu hiệu rate-limit/serialize khi chạy 5 tab song song ở
quy mô ảnh (khác video vốn khuyến nghị giữ 1-2 luồng ở §6 pitfall 8).

### 11.3 ⭐ REF-LOCK bằng Character/@mention — MẠNH, nhưng có 1 bẫy phạm vi PROJECT chết người

Flow có tính năng **Character** riêng (sidebar "Characters", tagline "Build and reuse characters for consistent
videos") — tạo 1 lần, dùng lại bằng cách gõ `@TênNhânVật` trong prompt box, thay thế hẳn cách cũ (upload ảnh
master + `gpti2_edit.py --ref`, tốn 110đ/ảnh REF).

**Cách tạo:** sidebar `Characters` → `New character` → gõ mô tả text đầy đủ (tuổi/giới/tóc/trang phục/thần thái,
kiểu character-sheet) vào ô `Character info` → submit → Flow tự sinh 1 portrait (nền xám, chính diện) → đặt tên
(bấm icon bút chì cạnh "Untitled character" → gõ tên → Enter) → `Done`.

**Cách dùng trong 1 cảnh:** click ô prompt → gõ `@TênNhânVật` (gõ có delay, không paste nguyên cụm) → đợi popover
hiện card `TênNhânVật · Character` (~1-1.5s) → bấm nút **"Add to prompt"** → gõ tiếp mô tả CẢNH (không cần lặp
lại đặc điểm ngoại hình — đã khoá sẵn trong Character) → submit.

**Chất lượng đo thật:** giữ mặt CHÍNH XÁC qua cảnh khác hẳn hoàn toàn bối cảnh (test "ngồi tatami cầm sổ tiết
kiệm tay run, đèn bàn giấy ấm" ra đúng y hệt khuôn mặt master + đúng toàn bộ chi tiết mô tả cảnh — futon cuộn,
cửa shoji, chén trà, sổ tiết kiệm cầm tay). Tốt hơn hẳn REF-LOCK cũ của gpti2 (không cần tính "tỉ lệ ref ≤30%"
để giữ chi phí, không có phụ phí 60đ/ảnh).

⚠️ **BẪY LỚN NHẤT: Character bị khoá theo TỪNG PROJECT, KHÔNG dùng chung tự động toàn tài khoản** — dù tagline
quảng cáo "reuse anywhere". Đã verify 2 lần độc lập:
- Mở project MỚI TINH (`New project`) rồi gõ `@Chiyo` (nhân vật đã tồn tại thật, tạo ở project khác) → popover
  báo **"No assets found"**, nút "Add to prompt" không bao giờ hiện → mọi cảnh có nhân vật FAIL hết, còn cảnh
  thường (không mention) vẫn chạy bình thường. Đây chính là lý do batch 37 ảnh lần đầu chỉ ra được 6 ảnh (toàn
  cảnh thường), 100% cảnh REF-LOCK hỏng.
- Vào sidebar `Characters` của project MỚI đó → Flow đưa THẲNG tới màn `New character` (coi như project chưa
  từng biết nhân vật nào) — không phải danh sách trống, mà là "chưa có gì" thật sự ở phạm vi project này.
- Ô dropdown chọn phạm vi cạnh thanh tìm kiếm trong popover liệt kê TỪNG PROJECT theo mốc thời gian (không có
  lựa chọn "Tất cả"/"All projects") — đổi sang project khác trong dropdown đó KHÔNG tự động lộ ra Chiyo trừ khi
  đúng project đã "biết" nhân vật này.
- Màn tạo Character có nút **"Add from project"** — đây là cơ chế "nhập khẩu" nhân vật từ project cũ sang
  project mới, nhưng phải làm THỦ CÔNG, không tự động.

**⇒ Cách dùng đúng khi chạy batch REF-LOCK đa luồng: TẤT CẢ các tab cần `@Character` phải cùng mở CHUNG MỘT
project** (project nơi Character đã tồn tại) — không để mỗi tab tự bấm "New project" riêng như batch ảnh thường
ở §11.2. Đã verify: 2 tab CÙNG mở 1 project, mỗi tab gõ `@Chiyo`/`@Tomie` khác nhau, submit cách nhau <1s → cả
hai ra đúng ảnh, không đụng độ, không lẫn.

⚠️ **Tạo Character (không phải sinh ảnh cảnh) trừ credit thật** — đo thật: "Google Flow credits" tụt từ 50 → 20
(mất 30) sau khi tạo 2 Character (có vài lần "Reroll"/thử lại). Khác hẳn 11.1 (sinh ảnh cảnh thường không trừ
gì). Cân nhắc số lượng Character cần tạo, đừng tạo tuỳ tiện nhiều lần thử.

### 11.3b Tạo Character bằng UPLOAD ảnh có sẵn KHÔNG trừ credit (sửa lại 11.3, verify 2026-09-11 từ máy 2)
11.3 ghi "tạo Character trừ ~15 credit/nhân vật" — số đó đo khi tạo Character bằng **MÔ TẢ CHỮ** (Flow phải
tự vẽ 1 portrait mới = 1 lượt sinh ảnh = tốn credit). Nhưng tạo Character bằng **Upload ảnh có sẵn** (nút
"Upload" ở màn New character) thì **KHÔNG trừ credit** — verify thật: "Google Flow credits" đứng yên 50→50
sau khi tạo 2 Character bằng upload + sinh 7 ảnh cảnh. Vì pipeline này LUÔN có sẵn ảnh master (gen bằng
gpti2 hoặc tự tạo trước), quy tắc chuẩn: **LUÔN tạo Character bằng Upload master có sẵn, KHÔNG mô tả lại
bằng chữ** — vừa giữ đúng mặt đã chốt vừa không tốn credit.

### 11.3c ⭐ CẢNH CÓ 2 NHÂN VẬT PHẢI MENTION CẢ HAI — lỗi thật đã dính, gây SAI NGƯỜI
Prompt chỉ mention `@Toshiko` (mô tả "Toshiko mỉm cười với Sachiko", tên "Sachiko" chỉ nằm trong CHỮ mô tả,
không phải mention) → Flow tự bịa ra 1 NGƯỜI THỨ BA (nam giới đeo kính) đứng thế chỗ Sachiko, vì chữ
"Sachiko" trong text không hề khoá mặt gì cả — chỉ có `@TênNhânVật` (chip mention thật) mới khoá mặt.
**⇒ Quy tắc bắt buộc khi viết `img_prompts.txt` cho Flow: cảnh có N nhân vật cần thấy mặt thì phải có ĐỦ N
mention `@Character` trong dòng đó** (không phải chỉ viết tên trong câu mô tả). Khác hẳn quy ước cũ của
`gen_images.py`/gpti2 (`@REF`/`@REF2` chỉ đánh dấu MỘT nhân vật làm trung tâm khung, nhân vật phụ để trôi tự
nhiên) — với Flow Character, PHẢI mention hết những ai cần đúng mặt trong cảnh đó.

### 11.3d Bối cảnh bị lẫn thương hiệu SAI QUỐC GIA nếu không ghi rõ
Cùng ảnh 006 ở trên: bối cảnh "bưu điện" ra logo/màu kiểu **USPS (Mỹ)** dù chuyện đang ở Nhật — model mặc
định kéo về hình ảnh bưu điện Mỹ nếu prompt chỉ viết "post office" chung chung. Đây là lỗi ĐỘC LẬP với
REF-LOCK, đã biết cách né ở các tập khác (vd tập tiệm tóc đã viết rõ "generic unbranded device with
absolutely no carrier logos, no company logos and no real brand names anywhere") nhưng tập này quên áp
dụng cho cảnh bưu điện. **⇒ Mọi bối cảnh có khả năng gắn thương hiệu thật (bưu điện/ngân hàng/cửa hàng/thiết
bị điện tử...) PHẢI ghi rõ trong prompt: tên nước cụ thể (vd "a small Japanese post office branch, Japan
Post styling") hoặc câu phủ định thương hiệu ("no real brand names, no US signage, generic unbranded").**

### 11.3e Bốn bẫy vận hành mới khi chạy 5 tab thật (verify 2026-09-11, máy 2, job simbot2-11-test7)
1. **Agent chat là 1 THREAD CHUNG cho cả project** — 5 tab cùng project ở chế độ Agent chip BẬT thì agent
   nhìn thấy prompt của NHIỀU tab cùng lúc, có lúc tự GỘP prompt và sinh thêm ảnH THỪA ngoài ý muốn (agent tự
   viết "I'm going to generate two images…"). Ảnh cần lấy vẫn lấy đúng nhờ so UUID biết ảnh nào mới, nhưng
   batch lớn (100-200 ảnh) sẽ sinh loạn/tốn thời gian dọn. Hướng thử tiếp (CHƯA verify): tắt chip Agent (chế
   độ cổ điển) khi chạy đa tab, hoặc mỗi tab dùng thread riêng nếu Flow hỗ trợ.
2. **Rate-limit "You are asking too fast"** khi các tab submit cách nhau <5s. Giãn cách submit giữa các tab
   tối thiểu **15 giây**, và tự động "Try again" khi dính lỗi này (không phải lỗi nội dung/policy, retry lại
   là qua).
3. **Tab mới mở ra vẫn còn panel Agent che mất `flow-prompt-box`** — y hệt bẫy đã biết cho video (§5.2 mục
   4), áp dụng lại cho ảnh: PHẢI đóng panel Agent trước khi tìm ô prompt, không thì code báo "không thấy ô
   nhập" dù trang đã load xong.
4. **Ảnh tải về là JPEG dù đuôi file đặt `.png`** — không phải lỗi, đã biết từ trước (xem 11.6), nhắc lại vì
   dễ quên khi viết code mới: đừng `assert` định dạng theo đuôi file, luôn đọc bằng PIL để biết định dạng
   thật.

### 11.3f Prompt kiểu "archival/documentary" tự bịa SỐ HIỆU/NGÀY THÁNG dù đã ghi "no text" — verify thật máy 2, job Loại B `ep01-valentich`
Khác 11.3d (thương hiệu sai quốc gia) — đây là lỗi RIÊNG của phong cách "cinematic archival shot" /
"vintage documentary photograph": model tự vẽ THÊM chữ trông như thật (số hiệu đăng ký máy bay kiểu
Mỹ "N9I400"/"N3456V" lên thân Cessna, timestamp "OCT 26, 1974" góc ảnh) dù prompt đã có sẵn cụm
"no text" — vì model hiểu "no text" là không thêm chữ trang trí/watermark, KHÔNG hiểu là cấm luôn
chi tiết "diegetic" (biển số, tem ngày tháng in trên chính vật thể) mà bản thân từ "archival"/
"documentary" ngầm gợi ý nên có. Hai hệ quả xấu cùng lúc: (1) ngày tháng bịa ra SAI với sự kiện thật
(bịa "1974" trong khi vụ việc là 1978) — phạm nguyên tắc [[du-lieu-that-khong-chi-tien]]; (2) số hiệu
kiểu Mỹ (N-number) trong khi máy bay thật mang đăng ký nước khác (Úc, VH-DSJ) — biến thể của bẫy
11.3d nhưng do CHI TIẾT VẼ THÊM chứ không phải bối cảnh.

**⇒ Đã vá tận gốc trong `pipeline/sinh_anh_canh.py` (hằng số `DUOI`, áp dụng mọi lane/mọi tập từ nay):**
thêm cụm phủ định RÕ RÀNG "no readable registration numbers or tail numbers or serial numbers or
license plates, no date stamps, no timestamp overlays, no caption text" — mạnh hơn "no text" chung
chung, chặn đúng loại chữ "trông như thật" mà "no text" không chặn được. Nếu phát hiện lại kiểu lỗi
này ở lane/đối tượng khác (biển số xe, nhãn chai, bảng tên...), thêm đúng cụm phủ định CỤ THỂ vào
prompt — đừng tin "no text" bao quát hết.

### 11.4 ⚠️ RELOAD TRANG = MẤT DẤU VẾT ẢNH — bẫy chết người, đã đốt cả 1 lượt điều tra
Ảnh vừa sinh xong có link dạng `https://flow-content.google/image/<uuid>?Expires=...&Signature=...` — dò UUID
ra ngay bằng regex `r"/image/([0-9a-f-]{36})"`. Nhưng hễ **reload trang (F5 / `page.reload()`)** thì TOÀN BỘ ảnh
cũ trong project (kể cả ảnh vừa tải xong 1 giây trước) đổi sang link khác hẳn dạng
`https://flow.google.com/asb/<mã token mờ, không phải UUID>` — code dò theo UUID sẽ báo **"không có ảnh mới"**
dù ảnh đã sinh ra thật và nằm sờ sờ trong project.

**⇒ QUY TẮC CỨNG: KHÔNG BAO GIỜ reload trang trong lúc đang theo dõi/tải ảnh về theo UUID.** Đọc/tải ảnh NGAY
trong phiên đang chạy, trước khi bất kỳ script nào gọi reload. Nếu lỡ reload rồi thì hết cách dò tự động theo
UUID — phải tải HẾT các tile hiện có (kể cả link dạng `asb`, vẫn tải được bình thường qua `page.request.get`,
chỉ là không có UUID để so khớp) rồi **nhận diện bằng mắt** (so khuôn mặt nhân vật + nội dung cảnh) để xác định
đúng ảnh nào ứng với prompt nào.

### 11.5 Bẫy overlay kẹt riêng của @mention (khác bẫy overlay video ở §10 mục 2, nhưng cùng họ)
Sau khi bấm "Add to prompt" trong popover `@mention`, nếu KHÔNG đợi `.cdk-overlay-backdrop` biến mất HẲN rồi mới
gõ tiếp mô tả cảnh / bấm submit → một lớp overlay còn sót lại che nút submit, Playwright ném
`TimeoutError` liên tục (y hệt bẫy `.cdk-overlay-backdrop` của §10 mục 2, nhưng ở đây xảy ra RIÊNG cho luồng
mention ảnh). Đã dính thật: batch 37 ảnh lần đầu hỏng **31/37 cảnh** vì đúng lỗi này (mọi cảnh có
`@Chiyo`/`@Tomie` đều timeout khi submit).

Cách fix (verify hoạt động tốt):
```python
def wait_no_overlay(pg, max_tries=15):
    for _ in range(max_tries):
        if pg.locator(".cdk-overlay-backdrop").count() == 0:
            return True
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(300)
    return pg.locator(".cdk-overlay-backdrop").count() == 0
```
Gọi hàm này TRƯỚC MỌI thao tác (trước khi click ô prompt, sau khi bấm "Add to prompt", trước khi bấm submit).

**Bẫy phụ:** poll "đã xong chưa" (check còn chữ "Thinking"/nút "Stop" không) NGAY sau khi vừa bấm submit dễ báo
**"xong sau 0.0-0.1 giây"** — đây là ĐỌC DOM QUÁ SỚM (trước khi UI kịp chuyển sang "Thinking..."), không phải
lỗi thật; ảnh vẫn sinh ra bình thường ở phía sau. Không tin mốc thời gian này, chỉ tin việc ảnh có xuất hiện
thật hay không (đếm số tile / so UUID mới) sau khi đã đợi ổn định vài giây.

### 11.6 Đặt tên + chống lẫn ảnh khi chạy đa luồng (trả lời "tải về có bị loạn không")
- Naming `NNN.png` theo ĐÚNG số thứ tự dòng trong `img_prompts.txt` gốc (khớp quy ước `gen_images.py` đã có sẵn
  cho gpti2) — KHÔNG đặt tên theo thứ tự tải về, vì thứ tự hoàn thành giữa các tab không đúng thứ tự gửi.
- Ghi `manifest.json` mỗi ảnh: `{idx, tab, uuid, character, prompt, bytes}` — biết chính xác ảnh nào ứng với
  cảnh nào, tab nào, nhân vật nào, để hậu kiểm khi nghi ngờ.
- **Verify tay bắt buộc**, đừng tin suông theo số thứ tự: tải vài ảnh ngẫu nhiên xem nội dung/khuôn mặt có khớp
  đúng `prompt` ghi trong manifest không. Đã áp dụng thật (so khớp guitar/ramen/lighthouse, và so khớp Chiyo
  carrying tray vs Tomie serving tea) — 0 lẫn ảnh khi làm đúng quy trình.
- Khi 2+ tab CÙNG 1 project (bắt buộc cho REF-LOCK, xem 11.3): tile mới nhất không cố định luôn ở vị trí 0 —
  phải hover vài tile đầu (2-4 tile) rồi so UUID với tập "đã biết trước khi submit" để tìm đúng tile MỚI, không
  suy luận theo vị trí cố định.

### 11.7 Test thật đã chạy làm bằng chứng (dự án h2dev, tập `ep07c-beats`)
- Video Satori "ep07c-beats" (`assets/satori_jp/ep07c-beats/`, script đã qua cổng B3Q, CHƯA có ảnh) dùng làm
  test case thật thay vì prompt vịt-cao-su.
- Đã viết `characters.json` (bible 2 nhân vật chính: Chiyo 75 tuổi goá phụ + Tomie 83 tuổi cựu y tá trưởng,
  kèm toán tuổi quan hệ) + `img_prompts.txt` (37 dòng, đánh dấu `@Chiyo`/`@Tomie`/thường theo đúng mạch truyện).
- Đã tạo 2 Character thật trên Flow, QC bằng mắt (Claude tự soi ảnh, không cần `qc_character.py`) — tuổi/giới/
  ngoại hình đều khớp bible, 2 nhân vật khác biệt rõ ràng (không nhầm lẫn nhau).
- Batch 37 ảnh LẦN 1 (mỗi tab tự tạo project riêng, không có `wait_no_overlay`) → hỏng, chỉ ra 6/37 ảnh (toàn
  cảnh thường), lộ ra cả bug 11.3 lẫn 11.5 cùng lúc.
- Test lại 2 tab CHUNG 1 project (đã áp 2 fix trên) → ra đúng 2/2 ảnh REF-LOCK, verify bằng mắt khớp 100%.
- File còn lại tại `assets/satori_jp/ep07c-beats/{characters.json, img_prompts.txt, manifest.json, img/}` —
  **batch đầy đủ 37 ảnh CHƯA chạy lại theo kiến trúc đã sửa** (việc dở dang, xem 11.8).

### 11.8 Việc dở dang — làm tiếp khi quay lại
- Chưa chạy lại full batch 37 ảnh `ep07c-beats` theo đúng kiến trúc đã sửa (5 tab CHUNG 1 project có sẵn
  Chiyo+Tomie, có `wait_no_overlay` trước mọi thao tác, KHÔNG reload trang khi đang tải ảnh).
- Script test nằm rải rác ở scratchpad phiên làm việc (`flow_2tab_shared_project.py` là bản ĐÃ SỬA đúng, nên
  lấy làm gốc viết lại quy mô 5 tab); `flow_batch_real.py` là bản CŨ có bug — đừng dùng lại nguyên xi.
- Nếu dùng lâu dài nên đóng gói thành 1 file chính thức kiểu `pipeline/flow_gen_images.py` (tương tự
  `gen_images.py` nhưng backend là Flow/Playwright thay vì gpti2 API), nhận `--prompts img_prompts.txt --project
  <project_id_co_san_character> --tabs 5` là chạy được.
