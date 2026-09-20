# TOOL SẢN XUẤT VIDEO — chạy KHÔNG cần Claude Code (trạng thái 2026-09-08)

Tool gọi thẳng LLM qua proxy (ramclouds/ns24) thay 3 bước sáng tạo của Claude. Mọi thứ riêng của
kênh/nhân vật nằm trong **profile**, nên dùng được cho MỌI nhân vật (cụ bà tâm tình → võ tướng ầm vang).

## FILE MỚI

| File | Việc |
|---|---|
| `profiles.py` + `profiles/<id>.json` | hồ sơ nhân vật/kênh — 1 nguồn chân lý cho cả 6 bước |
| `voice_bank.py` | kho 69 giọng OpenSpeaker: tìm theo mô tả tiếng Việt, nghe thử, resolve tên→id |
| `calibrate.py` | ĐO char-rate thật của giọng → ghi vào profile (bắt buộc khi lập kênh mới) |
| `llm_client.py` | gọi LLM: bắt buộc stream, retry, tự đổi model khi output hỏng |
| `ai_steps.py` | B3 kịch bản (2 pass + gate) · B5 prompt ảnh · B7 chữ thumbnail · `measure` |
| `make_video.py` | điều phối B2→B8, có `state.json` (resume) + `--dry-run` |
| `tts.py` (sửa) | `AGE_FILTERS` → `VOICE_FX` (thêm `young/boom/punch`), `--fx`, `--profile` |

## LỆNH HAY DÙNG

```bash
cd e:/CLAUDE/YOUTUBE/h2dev/pipeline

# --- lập kênh/nhân vật mới
py -3.13 voice_bank.py --find "trai tre manh me an to noi lon"     # chọn giọng
py -3.13 voice_bank.py --preview "Ryu - Characters" --fx boom       # nghe thử
# tạo profiles/<id>.json (copy 1 file có sẵn rồi sửa) rồi:
py -3.13 calibrate.py --profile <id>                                # ĐO char-rate, ghi vào profile

# --- làm 1 video
py -3.13 make_video.py --profile satori-jp-obaa --slug ep05 --competitor <video_id> --dry-run
py -3.13 make_video.py --profile satori-jp-obaa --slug ep05 --competitor <video_id>
py -3.13 make_video.py --profile satori-jp-obaa --slug ep05 --from B5     # chạy lại từ B5

# --- chạy lẻ từng bước / kiểm tra
py -3.13 ai_steps.py measure --profile satori-jp-obaa --script <file>    # gate, KHÔNG tốn tiền
py -3.13 llm_client.py --ping                                            # provider còn sống?
py -3.13 profiles.py --list
```

## ⭐ CÔNG THỨC BƯỚC B3 ĐÃ CHỐT (verify end-to-end 2026-09-08)

```
PASS 1  xin bản nháp ≥ 1,3 × target (nói rõ "thiếu thì hỏng, dài thì không sao")
        + khối 【語りのリズム】 bằng TIẾNG NHẬT (nhịp/hội thoại/câu hé tập sau) lấy số từ gate profile
        → nếu vẫn ra ngắn hơn target: viết lại 1 lần xin ≥1,6×, giữ bản dài hơn
PASS 2  trim_chunked: chia 3-4 khúc (đoạn, hoặc CÂU nếu không đủ đoạn), mỗi khúc 1 hạn mức chữ,
        chạy song song 3 luồng. CHỈ NÉN — mục tiêu ≥ bản hiện tại thì tự chuyển "giữ độ dài, sửa nhịp"
GATE    nhận bản mới khi ÍT LỖI HƠN (bằng nhau thì lấy bản gần mục tiêu hơn), tối đa 2 lượt
```

Kết quả chạy thật lần cuối: PASS 1 = 17.150 chữ (85s) → nén 4 khúc → **9.469 chữ = 29,8 phút,
4,2 phẩy/câu, 0% hội thoại, GATE 0 LỖI** (mục tiêu 9.525 → lệch 0,6%). Tổng ~5 phút, ~$0.06.
Nội dung đọc tay: mở cảnh điện ảnh, chi tiết Nhật thật (木枯らし/雨戸/霜月/野沢菜/信州), kết có
mồi comment + câu hé tập sau. Mối nối các khúc liền mạch.

⚠️ **PASS 1 dao động rất mạnh** cùng 1 nguồn: 7.769 / 9.388 / 13.108 / 14.480 / 17.150 chữ.
Vì vậy mới phải xin dài rồi nén — chứ không tin vào 1 lần viết đúng độ dài.

## ĐÃ VERIFY THẬT (2026-09-08)

- `llm_client --ping`: ramclouds gemini-3.8-flash 7,0s · ns24 gemini-3.8-flash 1,4s · ramclouds gpt-5.6-luna 4,2s.
- `voice_bank --find "trai tre manh me an to noi lon"` → top 1 = **Ryu-Characters** (samurai deep powerful).
- `calibrate --profile satori-jp-obaa` → 313,7 chữ/phút (hôm qua 317,5 → lệch 1,2%, đo lại ổn định).
- `calibrate --profile samurai-history-jp` → 317,5 chữ/phút, đã ghi vào profile.
- `tts.py --profile satori-jp-obaa` → chạy đúng giọng/fx/speed của profile.
- Gate (`ai_steps measure`): **ĐẠT** với bản Claude đã lên video + bản nén tốt hôm qua; **BẮT ĐÚNG** mọi bản
  lỗi hôm qua (dài 51,4' · marker `SCRIPT COMPLETED` · cắt giữa câu · hội thoại 29%).
- B5: 30/30 prompt, 63% có CHARACTER SHEET (khi truyền `--sheet` của tập) → đánh dấu `@REF ` để
  `gen_images.py` khoá mặt 110đ/ảnh, còn lại 50đ.
- B7: ra 4 dòng chuẩn kiểu simbot2 (WHITE/YELLOW/RED + BANNER).

## TỐC ĐỘ GEN ẢNH — 24 LUỒNG (đo thật 2026-09-08)

3 key gpti2 xoay round-robin theo chỉ số ảnh (`API_KEYS[i % 3]`) nên 24 luồng = **8 luồng/key**.

| Luồng | Kết quả | Giây/ảnh | 123 ảnh mất |
|---|---|---|---|
| 5 (cũ) | 123 ảnh / 969s / 0 lỗi | 7,9 | 16 phút |
| **24 (mới)** | **24 ảnh / 42s / 0 lỗi** | **1,75** | **~3,6 phút** |

→ `gen_images.py --workers` mặc định 24; đổi riêng từng kênh qua `image.workers` trong profile.
Đừng để 5 luồng: chậm 4,5 lần mà không rẻ hơn đồng nào.

## TỐC ĐỘ GHÉP VIDEO B8 (đo thật 2026-09-08, 123 ảnh · 30'39" · 1080p)

| Bản | Render clip | Nối + mux | TỔNG B8 |
|---|---|---|---|
| gốc: tuần tự · nội suy 3840×2160 · preset medium | ~11-12 ph | ~6-7 ph | **18,4 ph** |
| +8 luồng song song (vẫn nội suy 4K) | ~11-12 ph | — | không đổi (CPU đã 99,7%) |
| +bỏ nội suy (2400×1350) + veryfast | 2,9 ph (172s) | ~6-7 ph | ~9-10 ph |
| **+gộp xfade vào lệnh mux (1 lần encode)** | **1,6 ph** (96s) | **5,4 ph** (324s) | **7,0 ph** |

Bản cuối verify thật: 30'39" · 1920×1080 h264 · AAC 192k · phụ đề Nhật cháy sẵn · 702MB.
**Nhanh 2,6 lần** so với bản gốc, chất lượng bản giao KHÔNG đổi (lần encode cuối vẫn `medium/crf20`).

3 chỗ từng phí công, đã sửa hết:
1. **Nội suy ảnh lên 3840×2160 rồi mới zoom** — ảnh gốc gpti2 chỉ 2560×1440, khung ra 1080p, zoom 1,12
   chỉ cần ~2.150px. Nội suy KHÔNG thêm chi tiết nào mà nhân 2,5× số pixel mỗi frame. Nay dùng
   `W×(zoom+0,13)` = 2400×1350.
2. **Clip trung gian encode preset medium** — chúng đằng nào cũng bị encode LẠI ở bước sau ⇒ dùng
   `veryfast/crf18` (crf thấp để lần encode cuối không cộng dồn mất nét).
3. **Encode cả video 30 phút HAI LẦN**: xfade ra `silent.mp4` (encode 1) rồi burn phụ đề + trộn tiếng
   (encode 2). Nay chuỗi xfade được nhét thẳng vào `filter_complex` của lệnh mux ⇒ **chỉ còn 1 lần
   encode** (`xfade_chain()` chỉ trả về chuỗi filter, không encode).

## TỈ LỆ KHUNG ẢNH — `--fit` (2026-09-08)

Ảnh không đúng 16:9 (nano-banana luôn vuông 2048×2048, ảnh dọc…) trước đây bị **cắt câm lặng** mất 44%
bề ngang. Nay `check_aspect()` cảnh báo trước khi render, và có 4 cách xử:

| `--fit` | Làm gì | Dùng khi |
|---|---|---|
| `cover` (mặc định) | giữ tỉ lệ, phóng cho phủ kín rồi cắt viền dư | ảnh 16:9 (gpti2 2560×1440) → mất 0% |
| `blur` | ảnh vừa khung, nền là chính nó phóng to làm mờ | ảnh **vuông/dọc** — không méo, không viền đen |
| `pad` | thêm viền đen 2 bên | khi buộc phải giữ trọn khung hình |
| `stretch` | kéo cạnh cho vừa | CHỈ khi lệch <3%; lệch nhiều thì **mặt người bè ra** |

Kéo 2048×2048 (1,000) về 16:9 (1,778) = giãn ngang 78% ⇒ cấm dùng `stretch` cho ảnh vuông.

## ⭐ B3Q — QC NỘI DUNG (thêm 2026-09-08, user chốt: phải kiểm logic TRƯỚC khi tạo ảnh)

Gate của B3 chỉ đo **nhịp + độ dài + độ sạch**. Kịch bản mâu thuẫn (75 tuổi → 80 tuổi), gieo 伏線
không trả, hai khúc kể trùng một cảnh, hoặc **dịch sát bản gốc** đều qua gate "0 lỗi" như thường.
`qc_script.py` chạy giữa B3 và B4, **chặn trước khi tiêu tiền giọng + ảnh**.

**Tầng A — máy móc (miễn phí, tin 100%):** sót chữ Hàn · câu lặp nguyên văn · **câu lặp Ý** ·
mốc tuổi lệch · đoạn quá dài/vụn.
**Tầng B — LLM (2 lượt):** bảng dữ kiện nhân vật · 伏線 gieo↔trả · đoạn trùng ý · dấu vết văn hoá
nguồn · điểm từng mối nối khúc · chất lượng văn 1-5 · **so NHỊP SỰ KIỆN với bản gốc (đo 70/30)**.

| verdict | tool làm gì |
|---|---|
| `DAT` | chạy tiếp |
| `SUA` | cảnh báo, chạy tiếp |
| `HONG` | **DỪNG** (mâu thuẫn nặng / sao chép gốc) |
| `KHONG_KIEM_DUOC` | **DỪNG** — QC chết thì "0 lỗi" là SỐ ẢO (bẫy 503 đã dính ở dự án thẻ) |

Cờ: `--skip-qc` (tắt hẳn) · `--force-qc` (biết mà vẫn chạy).

**Bắt được ngay lần chạy đầu (ep07-tsuucho):**
1. Lặp Ý ở mối nối khúc: 「…静かに告白を、いたしました。恵は、涙を流しながら、告白いたしました。」
   ⚠️ **So chuỗi ký tự KHÔNG bắt được** cặp này (bigram chỉ trùng 0,38 vì hai câu kể cùng việc bằng
   chữ khác) → phải dò bằng **TỪ NỘI DUNG dùng chung giữa 2 câu sát nhau** (≥3 từ, cách ≤3 câu).
   Đo thật: 1-4 nghi vấn/kịch bản = đủ sạch.
2. **Bám gốc 100% → SAO_CHEP.** PASS 1 cũ chỉ "dịch + Nhật hoá" chứ không remake: ba nguyên tắc của
   cuốn sổ, câu dặn báo tang bằng giọng người… đều dịch sát. Rủi ro lỗi "sử dụng lại nội dung".
   → PASS 1 nay có ràng buộc số 6: đổi TÊN/NGHỀ/VÙNG/VẬT TRUNG TÂM · cấm dịch sát câu biểu tượng ·
   thêm ≥3 tình tiết mới · bỏ/gộp ≥2 tình tiết gốc. Giữ nguyên khung cảm xúc + bài học.


### ⚠️ BÀI HỌC LỚN NHẤT: cấm bằng PROMPT không ăn — phải GIẤU BẢN GỐC (đo 3 lần)

| Lần | Cách làm | Bám gốc | Kết luận |
|---|---|---|---|
| 1 | PASS 1 nhận NGUYÊN VĂN transcript, prompt ghi "remake 70/30" | 100% | **SAO_CHEP** (3 câu dịch sát) |
| 2 | thêm 4 ràng buộc cấm: đổi tên/nghề/vùng/vật · cấm dịch sát · thêm ≥3 tình tiết mới | **vẫn 100%** | **vẫn SAO_CHEP** |
| 3 | **PASS 0**: bóc khung chức năng rồi **GIẤU transcript khỏi PASS 1** | **67-73%** | **ĐẠT, 0 câu sao chép** |

Model **neo vào văn bản nó nhìn thấy**; cấm bao nhiêu cũng vô ích. `extract_beats()` chỉ trả về
8-12 nhịp mô tả CHỨC NĂNG + cảm xúc, **cấm chép thoại / tên riêng / con số / vật-tục lệ đặc trưng**;
PASS 1 viết từ khung đó, tự nghĩ ra mọi chi tiết. Khung lưu ra `beats.txt` để soi bằng mắt.
Tắt bằng `script.use_raw_source=true` nếu kênh nào cần bám sát bản gốc.

Giá phải trả: khung chỉ ~2.100 ký tự (vs transcript 15.700) nên PASS 1 viết NGẮN hơn (8.209 chữ) —
lượt sửa nhịp `keep_length` kéo lại được 9.212 chữ, gate ĐẠT.

### TỰ SỬA LỖI QC (`ai_steps.repair_script` + `issues_of`)

QC xong, gom lỗi NỘI DUNG thành danh sách rồi bắt model sửa TẠI CHỖ, giữ nguyên độ dài + giọng văn
(lệnh sửa viết bằng **ngôn ngữ đích**, danh sách lỗi để tiếng Việt cho người đọc).
**Chỉ nhận bản sửa khi gate KHÔNG tệ đi VÀ số lỗi QC giảm** — kẻo "sửa" chỗ này hỏng chỗ kia.
Bản cũ lưu `script.pre_fix.txt`. Tắt bằng `--no-fix`.

Đo thật (ep07c-beats): 4 lỗi → 1 · gate 0→0 · 9.212→9.204 chữ · **HONG → DAT** · văn 4/5 → 5/5 ·
tốn 1,6 phút. Lỗi được sửa: mâu thuẫn mốc thời gian (đoạn 1 nói chồng mất 10 năm, đoạn 5/8 nói
12 năm trước đã dùng tiền tử tuất của chồng).

### CHIA KHÚC THÍCH NGHI

Dư càng ÍT phải chia càng NHỎ: `over<1,35` → khúc 2.200 chữ · `<2,0` → 3.200 · còn lại 4.500.
Đo thật: dư 17% mà chia 2 khúc to (5.744+5.357) thì mỗi khúc chỉ phải cắt 15% → model làm ngơ →
bản mới ĐỨNG YÊN ở 11.101 chữ, gate trượt.

## ⭐ WORLD LOCK — ảnh phải CÙNG MỘT THẾ GIỚI (user chốt 2026-09-08)

REF-LOCK chỉ khoá **KHUÔN MẶT**, KHÔNG khoá bối cảnh. Đã thấy ở dự án khác: cùng 1 video mà cảnh này
nhà hiện đại, cảnh kia đám cưới cổ trang samurai, cảnh khác xe tải Thế chiến 2 → xem như 3 phim.

`ai_steps.world_lock(prof, script)` đọc kịch bản, suy ra 1 câu khoá thế giới (thời đại · vùng · mùa ·
kiểu nhà · trang phục · công nghệ + "no period costume, no historical or wartime elements"), rồi
**dán bằng CODE vào mọi prompt** — không nhờ model tự nhớ, vì nó quên từ dòng ~20 trở đi.
Ghi đè cứng bằng `image.world_lock` trong profile khi cần.

`ai_steps.era_violations()` quét danh sách từ phá thời đại (samurai/feudal/WWII/1940s/steam train…)
TRƯỚC khi gen; dòng nào lạc thì nhờ model viết lại, giữ nguyên bố cục cảnh.
Ví dụ world lock suy ra cho ep07: *contemporary 2020s, suburban Japan, winter; aging danchi apartment
with tatami and kotatsu; knit sweaters, domestic aprons; smartphones, flip phone, ATM, compact car*.

## BẪY ĐÃ DÍNH (đừng lặp)

1. **Prompt phải viết bằng NGÔN NGỮ ĐÍCH.** Prompt nén viết tiếng Việt làm gemini **phình** 13.108 →
   16.907 chữ (ngược mục tiêu); cùng nội dung viết tiếng Nhật thì nén 13.108 → 11.953. (Cùng họ với lỗi
   `gpt-5.6-sol` trả lời tiếng Việt khi đọc SKILL.md tiếng Việt.)
2. **Gemini nén được ~1 lượt rồi dừng**: lượt 2 trên cùng bản 11.953 → 12.052 (đứng yên). Đừng lặp vô ích.
   ⇒ **Cách ép độ dài DUY NHẤT ăn: nén THEO KHÚC có hạn mức chữ từng khúc** (`ai_steps.trim_chunked`).
   Đo thật cùng 1 bản nháp 13.108 chữ, mục tiêu 9.525:
   | Cách | Kết quả | Gate |
   |---|---|---|
   | nén cả bản, prompt tiếng Việt | 16.907 chữ (phình ra) | ✗ |
   | nén cả bản, prompt tiếng Nhật | 11.953 chữ (+25%) | ✗ |
   | nén cả bản lượt 2 | 12.052 chữ (đứng) | ✗ |
   | **nén 3 khúc, mỗi khúc 1 hạn mức** | **9.975 chữ (31,4')** | **✓ ĐẠT** |
   Mối nối 3 khúc đọc liền mạch, 0 đoạn trùng (đã soi tay). Chạy song song 3 khúc ≈ 90s.
3. **`続けて`/`停止` là từ Nhật bình thường** (「続けてきた」) → chỉ tính là marker khi trong 「」 hoặc đứng
   một mình cả dòng. Không có luật này thì gate báo sai mọi kịch bản tốt.
4. **Đo nhịp bằng `chars_per_breath`** (chữ giữa 2 lần ngắt hơi) chứ không phải chữ/câu: bản Claude 5,6 ·
   bản nén tốt 7,4 · bản dài lê thê 14,5. Dùng chữ/câu sẽ báo sai bản nén tốt (41,9 chữ/câu mà nhịp đúng).
5. **Phát hiện dòng có nhân vật phải so TOKEN, không so cả cụm**: sheet trong prompt luôn bị chèn dấu
   phẩy/đổi thứ tự → so cả cụm luôn trượt (đã dính: báo 0/30 dù prompt nào cũng có sheet).
6. **Kịch bản kể về người khác HOST** (ep3 kể về giám đốc tang lễ + cụ Hanae) → model chỉ giữ sheet ở
   4/30 prompt. Phải truyền `--sheet` CHARACTER SHEET của tập + ép tỉ lệ tối thiểu (`face_share`).
7. **Ép nhịp "ngắt hơi 7-9 chữ" làm model xuống dòng sau MỖI cụm** → 193 "đoạn" rời rạc.
   Phải `normalize_paragraphs()`: dòng nào không kết bằng 。！？」 thì nối với dòng sau.
8. **Bộ chia khúc phải có nhánh chia theo CÂU**: sau `normalize_paragraphs` bản nháp không còn dòng
   trắng → chia theo đoạn ra 1 khúc khổng lồ + 1 khúc RỖNG → model trả rỗng → `LLMError`.
9. **Độ dài đạt mà nhịp sai thì ĐỪNG đòi nén** — phải chế độ `keep_length` (giữ số chữ, chỉ sửa nhịp),
   và guard nhận bản mới theo SỐ LỖI GATE chứ không theo độ dài, kẻo nhịp không bao giờ được sửa.

## 📦 BẢN .EXE (2026-09-08) — `pipeline\dist_new\SatoriVideoTool\`

3 file mới: `new_profile.py` (wizard lập kênh) · `gui_video.py` (PySide6) · `build_exe.bat` ·
kèm `paths.py` (nguồn chân lý về đường dẫn).

| Lệnh | Việc |
|---|---|
| `SatoriVideoTool.exe` | mở giao diện (2 tab: Làm video · Lập kênh mới) |
| `... --selftest` | ghi `selftest.log` CẠNH exe: BASE, frozen, import, profile, skills, kho giọng |
| `... --selftest --ping` | kiểm cả kết nối LLM |
| `... --make-video <args>` | chạy pipeline không cần giao diện |
| `... --child <script.py> <args>` | exe tự đóng vai Python chạy script con |

**Đo thật:** exe 21MB / thư mục 257MB · selftest thấy 3 profile + 69 giọng + skills + ffmpeg ·
chạy trọn phần chữ (B3 → B3Q → B5 prompt → B7) trong **7,2 phút**, bám gốc 70%, KHÔNG dùng Python
của máy.

### 4 lỗi CHỈ lộ ra khi đóng gói (chạy bằng Python không bao giờ thấy)

| # | Lỗi | Vá |
|---|---|---|
| 1 | Script con không chạy được: khi frozen `sys.executable` LÀ exe, máy đích có thể không có Python | exe tự đóng vai trình chạy qua `--child`; 11 chỗ đổi sang `pycmd()` |
| 2 | `fetch_script` gọi `sys.executable -m yt_dlp` → `-m` không chạy khi frozen | dùng thẳng API Python của yt-dlp |
| 3 | Mất `skills/` + `assets/voice_bank.json`: `__file__` nằm trong `_internal` nên gốc dự án sai | `paths.py`: `DATA_DIR` (ghi) · `res()` (đọc bundle) · `OUT_ROOT` (video ra) |
| 4 | Thông báo lỗi tiếng Việt in thành `ần` | đặt UTF-8 cho **cả** stdout và stderr trước khi dispatch |

**Bẫy phát hiện nhân đó (không liên quan exe):** phụ đề tự động YouTube là kiểu CUỘN — cue sau chép
lại dòng của cue trước. Bộ đọc VTT cũ chỉ bỏ trùng cả khối → text **nhân ba** (37.998 ký tự cho video
27 phút). Sửa thành bỏ trùng TỪNG DÒNG → 12.679 ký tự.

**Bẫy build Windows:** không thể xoá/đổi tên thư mục đang là CWD của tiến trình khác — chỉ cần 1 cửa
sổ cmd/bash đứng trong `dist\SatoriVideoTool` là PyInstaller báo `WinError 32`, và lỗi đó nằm lẫn
giữa hàng trăm dòng log. `build_exe.bat` nay tự chuyển sang `dist_new`.

### CÒN LẠI KHI QUAY LẠI
- [ ] Anh mở thử giao diện, chốt bố cục/nhãn.
- [ ] Chạy 1 video ĐẦY ĐỦ bằng exe (có tiền ảnh) để nghiệm thu bản đóng gói.
- [ ] Dọn (CHỜ ANH DUYỆT vì là ảnh đã tốn tiền): `assets/satori_jp/ep07-tsuucho` **1,2 GB** ·
      `ep07b-remake` 93 KB · `ep07c-beats` 109 KB · `profiles/samurai-test.json` ·
      `pipeline/dist` (rỗng, chỉ còn vỏ). `assets/satori_jp/exetest` đã không còn.
- [x] `keys.json` để đổi key không cần build lại — XONG 2026-09-09, xem mục dưới.

## ✅ NGHIỆM THU BẢN ĐÓNG GÓI — 1 VIDEO ĐẦY ĐỦ BẰNG EXE (2026-09-09)

`simbot2-vU5PWT2zLDs` · profile `satori-jp-obaa` · bật `--auto-voice` · chạy **hoàn toàn trong exe**,
không dùng Python của máy. **27,6 phút · 9.140đ tiền ảnh · 7/7 cổng QC ĐẠT.**

| Bước | Kết quả |
|---|---|
| B3 kịch bản | PASS 0→3 + nén khúc + hạ hội thoại → gate ĐẠT: 8.388 chữ ≈ 30,2' · 4,6 phẩy/câu · hội thoại **2%** |
| B3Q nội dung | lượt 1 **HỎNG** → tool **tự sửa 7 lỗi** → **ĐẠT**, văn **5/5**, bám gốc 80% |
| B4V giọng | nhận ra người kể là **bà Lee Jeong-suk 73 tuổi** → Ado (nữ/già) `old-med` 0.92 |
| B4/B4Q | giọng + SRT ĐẠT · char_rate tự hiệu chỉnh 277,7 → **275,8** |
| B5 | 124 ảnh (49 khoá mặt @REF + 75 cảnh vật) · **B5Q-prompt sửa 16 prompt, 14 khối suýt vẽ nhầm người** |
| B5.0Q / B5Q / B7Q | ĐẠT hết |
| B8Q | **sync 4,0 · 0 lỗi** |

Sản phẩm: `final.mp4` **31:06**, 1920×1080 h264, audio AAC stereo, 661 MB (đã chuyển ra
`assets/satori_jp/simbot2-vU5PWT2zLDs`).

### 🐛 3 LỖI CHỈ CÓ Ở BẢN ĐÓNG GÓI — phát hiện trong nghiệm thu này
1. **`sys.stdout` là `None` trong bản `--windowed`** (LỖI NẶNG NHẤT, tốn gần 1 tiếng truy sai hướng).
   Cả **23 module** của pipeline mở đầu bằng `sys.stdout.reconfigure(...)` ở CẤP MODULE → vừa import
   là nổ `'NoneType' object has no attribute 'reconfigure'`, và PyInstaller dựng **hộp thoại modal**
   đứng chờ click mà tiến trình con thì không ai thấy. Triệu chứng: con **0% CPU, không log, không
   mạng**, cha báo "B2 transcript lỗi (exit 1)" — nhìn y hệt **treo mạng**. Chạy chính lệnh đó một
   mình từ cmd lại OK (cmd cấp console hợp lệ) nên càng dễ kết luận nhầm.
   Vá ở **một chỗ**: `_ensure_std()` chạy đầu `main()`, trước mọi import. Thêm lưới an toàn: mọi lỗi
   ngoài dự kiến ghi `crash.log` cạnh exe rồi `return 3`, KHÔNG để bật hộp thoại nữa.
   Verify 2 chiều: bản cũ treo 90s không ra file · bản vá **xong 2 giây, ra đủ 31.554 byte**.
   ⚠️ Di chứng: tiến trình kẹt kiểu này thành **zombie không giết được** (`tasklist` thấy,
   `taskkill` bảo không tồn tại) và khoá luôn thư mục `dist` — chỉ khởi động lại máy mới xoá được.
2. **ffmpeg bật cửa sổ đen liên tục.** ffmpeg là chương trình console, một video 30' gọi nó hàng
   trăm lượt → màn hình nháy suốt buổi. Vá bằng `_hide_child_windows()`: bọc `subprocess.Popen` tại
   cửa vào (mọi `run/call/check_output` đều đi qua đó) → che hết **12 chỗ gọi trong 6 file** bằng
   một sửa đổi, và **giữ nguyên** `creationflags` riêng của nút DỪNG.
3. **Profile ghi vào `_internal/` → mất mỗi lần build.** `profiles.DIR` trỏ vào thư mục module, khi
   đóng gói là `_internal` (bị xoá sạch khi build lại) và ở Program Files thì không ghi được. Hậu quả
   thật: exe học được char_rate 275,8 nhưng nằm trong bundle. Nay tách `BUNDLED` (chỉ đọc) khỏi
   `DIR` (ghi, CẠNH exe, trùng tên thì thắng); chạy từ mã nguồn hai đường là một nên không đổi hành vi.

`--selftest` nay kiểm luôn 3 điều này (`selftest_extra.py`) — đo thật trên bản cuối:
`noi ghi profile : OK - canh exe` · `an cua so con : OK`.

## ⭐ CHẠY TỪ ĐẦU: KÊNH → DANH SÁCH VIDEO → CẢ LÔ (2026-09-09)

Trước đây tool bắt đầu từ chỗ **đã có** video_id + tên tập, tức anh phải tự vào kênh, tự chọn video,
tự đặt tên. Nay Tab 1 làm từ đầu:

| Anh làm | Tool làm |
|---|---|
| Gõ `simbot2` (hoặc URL kênh) → bấm **Quét video** | Bảng: tên video · số view · thời lượng · ô tích · tên tập tự sinh |
| Tích vài dòng → **Chạy các video ĐÃ TÍCH** | Chạy lần lượt từng tập |
| Hoặc **Chạy TẤT CẢ video** | Cả kênh, tuần tự |
| Bấm **Tạo profile từ kênh này** | Điền sẵn Tab 3 với **ID kênh** làm id profile (`simbot2`) |

Đo thật: quét 6 video mất **0,6s**. Chạy tuần tự chứ không song song — mỗi video đã dùng nhiều
luồng khi gen ảnh và encode, chạy 2 tập cùng lúc chỉ tranh CPU và tranh hạn mức key ảnh.
**Một tập lỗi KHÔNG dừng cả lô** (bấm chạy 10 tập rồi đi ngủ mà tập số 2 gãy là mất cả đêm).

**Tên tập** = `<handle>-<video_id>`, vd `simbot2-vU5PWT2zLDs`. Dùng video_id nên tên KHÔNG đổi khi
kênh đăng thêm video mới → chạy lại là nhận ra tập cũ và bỏ qua các bước đã xong. Sửa được tại cột
cuối của bảng.

### 🎙️ GIỌNG RIÊNG THEO TỪNG VIDEO
simbot2 là kênh **rời rạc**: mỗi video một người kể khác nhau, nên dùng chung một giọng của profile
là sai người kể. Bật ô "Giọng riêng theo từng video" (hoặc `--auto-voice`) thì trước bước B4 tool
đọc transcript đối thủ, đoán giới/tuổi/sắc thái người kể rồi chọn giọng khớp trong kho 69 giọng,
kèm `fx` + `speed` theo độ tuổi. Kết quả ghi vào `state.json` mục **B4V** nên chạy lại KHÔNG gọi
LLM lần nữa.

Đo thật trên 4 transcript đã có (3–8s mỗi tập):

| Tập | Người kể tool đoán | Giọng chọn |
|---|---|---|
| ep08-nanajuu | nam / già · trầm ấm chậm rãi trải đời | Papa Ji – Deep Wise · fx `old-med` · 0.92 |
| ep13-ginkou | nữ / già · trầm lắng điềm đạm | Ado – Mature & Soothing · `old-med` · 0.92 |
| ep14-kaimono | nữ / già · chậm rãi mộc mạc | Ado – Mature & Soothing · `old-med` · 0.92 |
| ep3-sougi | nam / **trung niên** · trầm ấm sâu lắng | George – Warm · `none` · 0.98 |

ep3 đúng là **giám đốc nhà tang lễ** (nam trung niên) — tool phân biệt được, không gán bừa giọng cụ bà.

Ép tay khi cần: `--voice <id|tên>` `--voice-fx <none|old-med|boom…>` `--voice-speed 0.92`.

### 🎧 WHISPER NAY ĐÃ NẰM TRONG EXE (anh chốt "kèm cho chắc")
Đường bóc transcript trong exe đủ **cả 3 tầng**: api → yt-dlp subs → **nghe lại bằng whisper**.
Model `faster-whisper-base` (142 MB) bundle sẵn nên **chạy offline hoàn toàn** — verify bằng cách
đặt `HF_HUB_OFFLINE=1` và trỏ `HF_HOME` vào thư mục không tồn tại, vẫn chạy.

Đo thật **trong exe**: nạp model 0,3s · nghe 12s audio 0,6s · bóc trọn video 28 phút tiếng Hàn ra
552 đoạn / 12.739 ký tự (đường api cho 12.881 — khớp nhau).

⚠️ **Bẫy dung lượng đã dính:** PyInstaller kéo về **1.009 MB DLL GPU vô ích** — `cublasLt64_12.dll`
638 MB + `cufft64_11.dll` 274 MB + `cublas64_12.dll` 98 MB ở gốc `_internal`, cộng 306 MB provider
CUDA của onnxruntime — làm thư mục gửi đi phồng lên **1,8 GB**. Tool chạy `device="cpu"` nên không
dùng một DLL GPU nào. `build_exe.bat` nay xoá hết sau khi build → **575 MB**. Kèm 2 điều chỉnh:
dùng `--collect-binaries` (KHÔNG `--collect-all`) cho ctranslate2/onnxruntime, và
`--exclude-module numba llvmlite pyarrow` (llvmlite 102 MB + pyarrow 78 MB bị `--collect-all` kéo theo).
**Cắt DLL xong PHẢI nghe thật một lần** — bước `[5b/5]` của build script tự chạy
`exe --child selftest_extra.py --audio _selftest_audio.mp3` để không cắt lố mà không biết.

### 🔑 ĐỔI API KEY Ở MÁY KHÁC — KHÔNG BUILD LẠI (2026-09-09)
Trước đây chỉ key LLM đọc được từ `keys.json`; key ẢNH (gpti2 3 key), Grok và OpenSpeaker nằm CỨNG
trong code — nghĩa là một key gpti2 hết tiền (402) ở máy khách là phải build lại exe. Nay mọi key
đi qua `keys.py` với thứ tự tra: **biến môi trường → `keys.json` CẠNH exe → `keys.txt` CẠNH exe →
`keys.json` gốc dự án → mặc định trong code**.

`build_exe.bat` tự đặt sẵn `keys.json` cạnh exe (lấy từ `keys.sample.json` nếu chưa có bản thật).
Khoá: `ramclouds` · `ns24` · `gpti2` (nhận **danh sách** nhiều key, hoặc 1 chuỗi cách nhau bằng `,`
hay `;` — RPM tính theo TỪNG key nên tool luân phiên) · `grok` · `openspeaker`.
Bỏ trống hoặc xoá một khoá = dùng lại mặc định trong code, KHÔNG phải lỗi.

`selftest_extra.py` in ra nguồn từng key (chỉ 6 ký tự đầu, không bao giờ in cả key), số key thật
tới được từng module provider, và số extractor `yt_dlp`. Ba thứ này hay chết ÂM THẦM trong bản
frozen. Gắn vào `--selftest` bằng đúng một dòng: `import selftest_extra; out += selftest_extra.lines()`.

### 🐛 3 LỖI CHỈ CÓ Ở BẢN EXE — đã vá 2026-09-09
1. **ID YouTube bắt đầu bằng `-`** (vd `-Gt6QYEFS38`): argparse coi là tham số →
   `fetch_script.py -Gt6QYEFS38` chết "required: url", `--competitor -Gt6...` chết "expected one
   argument". Không phải lỗi gõ: bộ chữ id là base64url nên ~1/64 video bị, quét 8 video trên kênh
   nguồn đã gặp 1 cái. `_fix_dash_id()` đổi thành URL đầy đủ trước khi argparse chạy.
2. **yt-dlp không thấy ffmpeg**: postprocessor `FFmpegExtractAudio` gọi ffmpeg trên PATH, máy khách
   thường không có, còn bản bundle của `imageio_ffmpeg` nằm trong `_internal`. Phải truyền
   `ffmpeg_location` bằng tay.
3. **Thiếu faster-whisper báo lỗi muộn**: code cũ tải xong ~30 MB audio mới báo
   `ModuleNotFoundError` — trông như tool hỏng. Nay chặn TRƯỚC khi tải và chỉ đúng cách xử lý.
   (Bản exe hiện ĐÃ kèm whisper — xem mục trên — nhưng vẫn giữ cửa chặn này cho máy chạy từ mã nguồn
   chưa `pip install faster-whisper`.)
4. `--collect-submodules yt_dlp`: thiếu cờ này bản frozen báo "no suitable extractor" dù
   `import yt_dlp` vẫn OK (extractor nạp động). Máy dev có 1751 extractor — bản đóng gói phải kiểm lại.

## ✅ NGHIỆM THU TRƯỚC KHI ĐÓNG EXE (2026-09-08)

5 video chạy bằng **1 lệnh**, mỗi video từ 1 nguồn YouTube khác nhau của cùng kênh đối thủ:

| Tập | Kết quả | Thời gian | Tiền ảnh | Tool TỰ gỡ |
|---|---|---|---|---|
| ep10-saigo | ✅ 7/7 cổng ngay lượt đầu | 25,2 ph | 8.580đ | — |
| ep11-saikon | ✅ (sau 3 lần em vá code) · sync 4,0 | 27,6 ph | 9.320đ | hội thoại 15→8% · 2 ảnh hỏng |
| ep12-yokin (code cũ) | ✗ **gãy** ở gate nhịp 6,92 phẩy/câu | 3,7 ph | 0đ | — |
| **ep12-yokin (code mới)** | ✅ qua sạch | 32,1 ph | ~10.000đ | **gate hỏng → viết lại kịch bản** · QC SUA → **tự sửa thành DAT** · 5 ảnh méo → 3 |
| ep13-ginkou | ✅ 7/7 · sync **4,0** | 24,2 ph | 9.870đ | 2 ảnh hỏng → **0** |
| ep14-kaimono | ✅ · sync **4,0** · 136 ảnh 0 lỗi | 26,1 ph | 11.900đ | — |

**Trung bình 1 video ≈ 27 phút · ~10.000đ tiền ảnh.**

### 8 loại lỗi tool TỰ SỬA (đã chạy thật, không cần người)
độ dài kịch bản (nén theo khúc, hạn mức từng khúc) · **nhịp** (`reduce_commas` tách câu dài) ·
**hội thoại** (`reduce_dialogue`, đo thật 21%→5% và 15%→8%) · lỗi logic (`repair_script`) ·
**kịch bản hỏng nặng → viết lại bản khác** (`--tries`) · ảnh master sai (vẽ lại) ·
**ảnh hỏng** (vẽ lại 2 lượt, lượt 2 sửa luôn prompt bỏ cận cảnh bàn tay) ·
**ảnh lệch lời sau khi ghép** (`fix_weak_images` → ghép lại).
Cộng thêm: YouTube chặn (3 đường) · model chết (chuỗi dự phòng) · key ảnh hết tiền (đổi key) ·
cảnh trẻ em (`CHILD` → `@GROK`).

### 4 lỗi CUỐI phát hiện trong nghiệm thu
1. **Gate B3 hỏng không kích hoạt viết lại** (chỉ bắt B3Q/B4Q) → ep12 dừng hẳn. Nay B3→B3Q→B4→B4Q
   nằm chung MỘT vòng, hỏng ở đâu cũng viết lại.
2. **Không có bộ chuyên trị NHỊP** — cùng căn bệnh với hội thoại: chế độ giữ-độ-dài chia 2 khúc to
   nên model làm ngơ ⇒ `reduce_commas` tách câu dài, khúc 2.500 chữ.
3. **Vẽ lại ảnh 1 lượt là chưa đủ** (ep12: 5 → 3) ⇒ 2 lượt, lượt 2 sửa prompt (`CLOSE-UP`→`MEDIUM`,
   bỏ cụm tả bàn tay — thủ phạm gần như luôn là cận cảnh ngón tay).
4. **B8Q báo "thiếu phụ đề" OAN** — giãn nhịp tạo ~16% thời lượng khoảng lặng, mốc lấy mẫu cách đều
   rơi vào đó thì đương nhiên không có phụ đề (ep14: 6/12 mốc, cả 6 đều trong khoảng lặng, video
   hoàn toàn đúng) ⇒ **hút mẫu vào GIỮA cue**.

## 🎧 GIÃN NHỊP (`pace_audio.py`) — bắt buộc cho giọng người già (2026-09-08)

TTS đọc gần liền mạch (khe tự nhiên chỉ **0,11s**/cue) → khán giả già không kịp nghe/nghĩ/nhớ.
`pace_audio.py` CẮT mp3 tại ranh cue, CHÈN im lặng, dựng lại SRT từ độ dài đo được —
**không dùng `atempo` nên KHÔNG trôi phụ đề**. Chạy trong B4 (`voice.pace`, mặc định bật).

| Luật nghỉ | mặc định | ep10 (×1,32) | ep11 (×1,19) |
|---|---|---|---|
| hết câu | 0,65s | 0,86s | 0,77s |
| giữa câu | 0,20s | 0,26s | 0,24s |
| chuyển đoạn | 1,50s | 1,98s | 1,78s |

2 lỗi phải vá khi chạy thật:
1. **0/11 ranh đoạn được nhận ra** — hàm dò cuối đoạn so offset ký tự TUYỆT ĐỐI, mà `voice.srt` do
   STT sinh nên ngắn hơn kịch bản **8,8%** (7.614 vs 8.353) → trôi 3-12 ký tự, dung sai 2 không bao
   giờ khớp ⇒ mất sạch khoảng nghỉ chuyển cảnh. Sửa: so **theo TỈ LỆ**.
2. **Không đạt dải tỉ lệ nói** — mức mặc định chỉ về 90% (mục tiêu 82-87%) vì khe TTS đã 0,11s và
   chỉ 46% cue kết bằng dấu câu ⇒ thêm **tự dò hệ số nghỉ** (bisection) để rơi đúng dải.

Kiểm chứng sync bằng số: audio khớp cue cuối **lệch 0,00s** · RMS trong cue 4.211 · RMS vùng im chèn
**trung vị 0,0** · khoảng nghỉ 0,11s → tối thiểu 0,26s.

⚠️ **Hệ quả dây chuyền: giãn nhịp làm video dài thêm ~15%** nên `char_rate` phải đo trên bản ĐÃ GIÃN
(313,1 → **277,9**). Trung bình động 70/30 quá chậm cho thay đổi hệ thống (bò tới 302,5 trong khi
thật 277,9 → tập nào cũng bị B4Q chặn) ⇒ **hiệu chỉnh thích nghi**: lệch ≤8% nhích nhẹ (0,3),
lệch >8% bám số đo (0,8).

## 🏁 ep11-saikon (2026-09-08) — 1 lệnh, 27,6 phút, 9.320đ

| Cổng | Kết quả |
|---|---|
| B3 gate | ĐẠT — 7.932 chữ, 4,64 phẩy/câu, hội thoại **15% → 8%** (`reduce_dialogue` tự vào cuộc) |
| **B3Q** | **DAT SẠCH, 0 ghi chú** · bám gốc 64% |
| B4 + **B4Q** | 1.523s → **1.681s** sau giãn nhịp · phủ 99,8% · 0 lỗi |
| **B5Q-prompt** | soi 112/112 · sửa 7 prompt · **cứu 4 khối suýt vẽ nhầm người** |
| **B5Q** | 2 ảnh hỏng → **tự vẽ lại** → còn 1 (lỗi nhẹ) |
| **B8Q** | **ĐẠT · khớp ảnh–lời 4,0/5** (cao nhất từ trước tới nay) |

3 lỗi lượt này phơi ra, đã vá: **B8Q so state thay vì đo file tiếng** (báo lệch 170s dù video đúng) ·
**sửa tại chỗ bó tay thì tool bắt người vào cuộc** → thêm tự VIẾT LẠI bản khác (`--tries`, mặc định 2) ·
**char_rate hiệu chỉnh quá chậm** khi có thay đổi hệ thống.

## 🏁 CHẠY SẠCH 1 LỆNH — ep10-saigo (2026-09-08): 7/7 CỔNG QC ĐẠT NGAY LƯỢT ĐẦU

`py -3.13 make_video.py --profile satori-jp-obaa --slug ep10-saigo --competitor 66weQbaUZuk`
KHÔNG can thiệp bước nào. **25,2 phút · 8.580đ tiền ảnh.**

| Bước | Thời gian | Kết quả |
|---|---|---|
| B2 | **1s** | đường nhanh sống lại (429 tự hết) → khỏi whisper |
| B3 | 3 ph | PASS 0 khung 1.677 ký tự · gate ĐẠT (8.353 chữ, 5,28 phẩy/câu, hội thoại 0%) |
| **B3Q** | 1 ph | **DAT ngay lượt đầu, không cần tự sửa** · bám gốc **65%** |
| B4 + **B4Q** | 125s | SRT phủ **98,5%** · 0 lỗi |
| **B5.0Q** | — | master ĐẠT |
| **B5Q-prompt** | 1 ph | soi 108/108 khối, sửa 2 prompt · 0 khối sai cờ |
| B5 | 223s | 108 ảnh = 52 text-only + 53 REF + **3 GROK (trẻ em)** · 0 lỗi |
| **B5Q** | 2 ph | **ĐẠT** — 0 ảnh hỏng, 0 ảnh lệch prompt |
| **B7Q** | 1 ph | **ĐẠT 0 vấn đề** — thumbnail sạch hoàn toàn lần đầu tiên |
| B8 | 362s | 26:52 · 1080p |
| **B8Q** | 1 ph | **ĐẠT · khớp ảnh–lời 3,92/5** |

### 7 lỗi ep09 phơi ra → đã vá hết (ep10 không lặp lại lỗi nào)

| # | Lỗi | Cách vá |
|---|---|---|
| 1 | `skills/` của dự án biến mất → B3 chạy không có skill | copy skill **vào trong dự án** (exe tự chứa) |
| 2 | gate B3 hỏng vẫn chạy tiếp, tiêu tiền giọng+ảnh | gate hỏng = **DỪNG** (`--force-qc` để vượt) |
| 3 | không hạ được tỉ lệ hội thoại (21% đứng yên) | `reduce_dialogue()` — đo thật **21% → 5%**, giữ nguyên độ dài |
| 4 | `SCENE` bị hiểu là "cảnh không người" → khối kể 2 người con ra cảnh trống | lời nói về người khác thì **phải vẽ đúng người đó** |
| 5 | bộ chấm B8Q quá chữ nghĩa (soi tay: 3/4 mốc bị trừ oan) | ghi rõ tiêu chí công bằng cho lời nhắn khán giả / cảnh quay người kể |
| 6 | QC prompt viết lại thành cảnh trẻ em → Azure từ chối | **cờ thứ 3 `CHILD` → `@GROK`** (grok-imagine-image-2.0), và bộ lọc bỏ qua dòng CHILD |
| 7 | thumbnail luôn bị chấm "mặt hơi mất nét" | chỉ làm mờ **nửa bên chữ**, banner to hơn (0,62→0,74) |

## ⭐ 10 BƯỚC · 7 CỔNG QC (user chốt 2026-09-08: "QC sau mỗi bước, đầu ra phải hoàn hảo")

`B2 → B3 → **B3Q** → B4 → **B4Q** → B5 → **B5Q** → B7 → B8 → **B8Q**` (thêm **B5.0Q** cho ảnh master)

| Cổng | File | Kiểm gì | Không đạt |
|---|---|---|---|
| **B3Q** kịch bản | `qc_script.py` | logic · mâu thuẫn dữ kiện · 伏線 gieo–trả · lặp ý · sót văn hoá nguồn · mạch nối khúc · văn 1-5 · **bám gốc 70/30** | tự sửa 1 lượt → vẫn hỏng thì DỪNG |
| **B4Q** giọng | `qc_visual.qc_voice` | SRT phủ bao nhiêu % kịch bản (bắt TTS đọc thiếu/cắt — **lỗi câm lặng**) · cue tăng dần · đuôi audio · thời lượng | DỪNG trước khi tiêu tiền ảnh |
| **B5.0Q** master | `qc_visual.qc_master` | tuổi · giới · **trang phục · thời đại · phong cách** · mặt có rõ để khoá | vẽ lại master rồi QC lại |
| **B5Q** loạt ảnh | `qc_visual.qc_images` | thiếu/hỏng/quá tối/phẳng/**trùng nhau** (dHash, toàn bộ) + vision soi mẫu: khớp prompt · đúng thời đại · méo mó · lọt chữ | lỗi nặng → DỪNG trước khi dựng |
| **B7Q** thumbnail | `qc_visual.qc_thumb` | có thấy MẶT không · **chữ có đè lên mặt không** · chữ đọc được ở cỡ nhỏ · tương phản · có cảm xúc | thử nền khác, lấy nền ít lỗi nhất |
| **B8Q** video | `qc_visual.qc_video` | luồng · thời lượng vs giọng · khung đen · phụ đề có cháy · **ẢNH CÓ KHỚP LỜI ĐANG ĐỌC** (chấm 1-5 tại 12 mốc) | báo từng mốc lệch |

Cờ: `--skip-qc` · `--no-fix` (QC nhưng không tự sửa) · `--force-qc` (biết mà vẫn chạy).
Mọi cổng tách `infra` (mạng/model chết) khỏi lỗi nội dung — QC không chạy được thì **KHÔNG PASS**,
vì "0 lỗi" lúc đó là số ảo (bẫy 503 đã dính ở dự án thẻ).


### B5Q-prompt — QC PROMPT ↔ LỜI bằng CHỮ, trước khi tiêu tiền (2026-09-08)

`ai_steps.qc_prompts()` — cùng model `gemini-3.8-flash`, nhưng **không cần vision** nên rẻ nhất trong
cả chuỗi: 126 khối chia 6-7 lô, chạy song song, ~1 phút. Kiểm 2 việc cho từng khối:
(a) prompt có tả đúng việc LỜI đang kể không · (b) cờ `REF`/`SCENE` có đúng không.
Sai cờ REF là lỗi nặng nhất: khối kể về người khác mà gắn REF thì ảnh **vẽ ra nhầm người**.
Sai thì model viết lại luôn prompt + sửa cờ, rồi mới gen ảnh.

Kinh tế của việc đặt QC sớm: soi ảnh sau khi gen thì tiền đã mất (9.060đ) · chấm khung hình sau khi
dựng thì mất thêm 7 phút encode · ở đây chỉ là văn bản.

Đo thật trên 126 prompt của ep08 (vốn đã qua storyboard): **sửa 3 prompt, đổi 1 cờ REF→SCENE**
(khối 25 lời kể là *con gái quát mắng* mà lại gắn REF → sẽ vẽ ra bà cụ thay vì người con).

⚠️ **BẪY VÁ FILE (mất 40 phút mới tìm ra):** vá bằng heredoc python làm `` trong regex biến thành
**ký tự backspace thật ``**, nên regex không bao giờ khớp → QC báo "soi 0/126 khối" mà KHÔNG lỗi
gì. Cùng họ với việc `
` biến thành xuống dòng thật làm vỡ chuỗi. ⇒ **regex/chuỗi có escape phải
sửa bằng công cụ Edit, đừng qua heredoc**; và đã thêm cảnh báo tường minh khi một lô QC không đọc
được dòng nào (im lặng ở đó chính là "0 lỗi ảo").

### B7Q — 3 lỗi thumbnail chỉ lộ ra khi có cổng QC (ep08, 2026-09-08)

1. **Chữ đè lên mặt.** Chữ chiếm nửa trên khung, mà MỌI ảnh chân dung đều để mặt ở giữa → thử 5 nền
   khác nhau đều hỏng y hệt. Không phải lỗi chọn nền mà lỗi BỐ CỤC.
   → sinh **1 ảnh nền RIÊNG** cho thumbnail (chủ thể dồn 1/3 phải, nửa trái là khoảng tối trống,
   ~110đ) + `thumbnail_text.py --side left` dồn chữ sang trái.
2. **Chữ đỏ viền đen trên nền tối chìm nghỉm.** → chữ đỏ đổi sang viền TRẮNG, và đỏ sáng hơn
   (255,45,45 → 255,78,66). Trắng/vàng giữ viền đen như cũ.
3. **Không có cổng QC nào cho B7** — bản cũ dùng ảnh phố vắng không mặt người, không ai phát hiện.

## ⭐ STORYBOARD TỪ SRT — cách DUY NHẤT để ảnh khớp lời

`assemble.py` chia ảnh ĐỀU theo cue (`bounds[i]=round(i*M/N)`): ảnh #i luôn được chiếu đúng lúc đọc
khối cue #i. Nó KHÔNG biết ảnh nào thuộc câu nào. Cách cũ (đưa cả kịch bản, bảo model "rải đều")
để model tự quyết mật độ → ảnh trôi lệch lời.

`storyboard.py` cắt cue thành N khối GIỐNG HỆT assemble, rồi `ai_steps.write_storyboard_prompts()`
viết prompt #i bám đúng lời khối #i (6 lô × 25, chạy song song).

**Mỗi khối được model gắn cờ `REF` hay `SCENE` THEO LỜI KỂ**, không theo hạn ngạch. Đây mới là gốc
của lỗi lệch: bản cũ ép cứng 60% prompt phải có nhân vật chính, nên khối kể về NGƯỜI KHÁC (ông
Tatsuo lau dầu máy) hay NƠI KHÁC (đầu giường bệnh) cũng bị gắn `@REF` — mà `@REF` thì luôn vẽ ra
nhân vật chính → sai hẳn người.

Kèm 1 vá nữa: `@REF` đi qua chế độ EDIT của gpti2 nên nó bê luôn **BỐI CẢNH** ảnh master, không chỉ
khuôn mặt (đo thật: prompt `waiting in hospital` vẫn ra căn nhà của master). Mọi dòng `@REF` nay được
gắn đuôi *"same face, but a COMPLETELY NEW scene — do not reuse the background/room/furniture"*.

| | cách cũ (rải đều) | **storyboard + cờ theo lời** |
|---|---|---|
| khớp ảnh–lời (B8Q, 8-12 mốc) | **2,2/5** | **3,58/5 ĐẠT** |
| ảnh mẫu lệch prompt (B5Q) | 3/12 | **0/12** |
| tỉ lệ `@REF` | 87/126 ép cứng | 46/126 theo lời kể |
| tiền ảnh | 11.520đ | **9.060đ** |

⚠️ **Vá bằng phép thay chuỗi PHẢI có `assert`.** Bản vá truyền `voice.srt` vào B5 trượt âm thầm →
cả một lượt chạy vẫn đi đường cũ, tốn 8.700đ tiền ảnh mới phát hiện. Dấu hiệu nhận ra: nhật ký
KHÔNG có dòng `[B5] STORYBOARD` và chỉ có MỘT lượt gọi model lớn thay vì 6 lô. Nay B5 in cảnh báo
tường minh khi không dùng được storyboard.

## ✅ BẢN DÙNG ĐƯỢC ĐẦU TIÊN — ep08-nanajuu (2026-09-08, chuỗi ĐÃ VÁ)

Nguồn `sYRr33eHYSM` (388k view, 36'). Chạy 1 lệnh, KHÔNG can thiệp bước nào.

| Bước | Thời gian | Kết quả |
|---|---|---|
| B2 | 441s | api ✗ · yt-dlp ✗ · **whisper ✓** 16.546 chữ |
| B3 | 3 ph | PASS 0 khung 1.758 ký tự (giấu bản gốc) → **gate ĐẠT lượt đầu** 9.478 chữ / 29,9' / 0% hội thoại |
| **B3Q** | 2 ph | QC **8 lỗi** → tự sửa → **2 lỗi** · **HONG → DAT** · bám gốc **73% → 75%**, 0 câu sao chép |
| B4 | 190s | 31,5 phút |
| B5 | 7 ph | WORLD LOCK tự suy: *late 20th century 1980s–90s, suburban Kanto, winter, aged wooden bungalow* · 126 ảnh, 87 khoá mặt · **11.520đ** |
| B7 | 11s | nền = ảnh CÓ MẶT (052.png) |
| B8 | 436s | 31:28 · 1080p · phụ đề + nhạc nền |
| **B8Q** | 1,4 ph | **khớp ảnh–lời 3,58/5 · ĐẠT** · phụ đề hiện đủ 12/12 mốc |
| **TỔNG** | **29 phút** | (20 phút nếu đã có sẵn transcript) |

8 lỗi QC bắt được ở bản đầu — toàn loại gate cũ **mù hoàn toàn**: vợ nhân vật mất "vài năm trước"
ở đoạn 1 nhưng "30 năm trước" ở đoạn 5 · chỗ giấu chìa khoá đổi giữa chừng (giao ước để dưới chân
đèn đá, lúc cứu lại đào chỗ khác) · tờ giấy giao ước gieo ở đoạn 3 rồi bỏ lửng · một câu còn dấu vết
đại từ dịch từ tiếng Hàn.

Nhất quán ảnh: ảnh 020 và 105 (cách 85 cảnh) cùng khuôn mặt, cùng căn nhà, cùng đồng hồ treo tường
và điện thoại quay số đen.

## CHẠY THẬT TỪ SỐ 0 — ep07-tsuucho (2026-09-08)

Video đối thủ MỚI (`DXXwIxhcfF0`, 506k view), không mượn file cũ nào.

| Bước | Thời gian | Ghi chú |
|---|---|---|
| B2 transcript | 9 ph | API + yt-dlp đều bị YouTube chặn IP → **tự tụt xuống whisper** (15.729 chữ) |
| B3 kịch bản | 5 ph | PASS1 27.548 chữ (2,9× mục tiêu!) → nén 6 khúc → 9.963 chữ · gate ĐẠT lượt đầu |
| B4 giọng + SRT | 142s | 32,3 phút · char_rate thật 308,9 (profile ghi 317,5 → lệch 2,8%) |
| B5 ảnh | 269s | 129 ảnh, 80 khoá mặt · 0 lỗi · **11.250đ** |
| B7 thumbnail | 11s | |
| B8 ghép | 426s | 32:15 · 1080p · 630MB |
| **TỔNG (không kể B2)** | **20,4 phút** | |

Sửa từ lần chạy này: `char_rate` **tự hiệu chỉnh** sau mỗi B4 bằng số đo cả video (trung bình động
70/30) — mẫu 230 chữ của `calibrate.py` không có quãng nghỉ giữa đoạn nên luôn đo nhanh hơn thật ·
nền thumbnail chọn ảnh **có mặt người** (@REF) thay vì ảnh thứ n/3 (trúng phố vắng) ·
lọc ký tự Nhật lọt vào prompt tiếng Anh (`old惣菜deli counter`).

## ⚡ B2 NHANH — 3 đường + whisper đã tối ưu (2026-09-08)

| Đường | Thời gian | Khi nào dùng được |
|---|---|---|
| `youtube-transcript-api` | ~2s | YouTube cho phép IP |
| `yt-dlp` phụ đề ASR | ~5-10s | cùng endpoint timedtext ⇒ **429 thì chết cùng lúc với đường 1** |
| **`yt-dlp` audio + faster-whisper** | **62s** (video 31') | KHÔNG bao giờ bị chặn |

**Whisper tăng tốc 7 lần** (441s → 62s cho video 31 phút) nhờ nhận ra: bản nghe này **chỉ để PASS 0
rút thành ~10 nhịp chức năng**, mọi tên/số/câu chữ đều bị vứt đi ⇒ không cần chính xác từng chữ.

| | cũ | mới |
|---|---|---|
| model | `small` | **`base`** |
| beam | 5 | **1 (greedy)** |
| cpu_threads | mặc định (~4) | **16** (máy 24 nhân) |
| condition_on_previous_text | True | **False** (tránh lải nhải, nhanh hơn) |

Khi 429 kéo dài: `--method whisper` để khỏi chờ retry; hoặc lấy lại đường vài-giây bằng
**xoay IP (Deeper DPN, skill `deeper.md`)** hoặc **cookies** (`YTDLP_COOKIES` /
`YTDLP_COOKIES_BROWSER`, đã hỗ trợ sẵn trong `fetch_script.py`).

## B2 BỊ YOUTUBE CHẶN — 3 ĐƯỜNG DỰ PHÒNG

Đo thật 2026-09-08: endpoint phụ đề `/api/timedtext` chặn 429 theo IP, chặn **cả** khi gọi từ trong
trình duyệt thật và khi bấm nút "Show transcript" → **mọi extension transcript đều vô dụng** trên IP
này (chúng dùng chung endpoint đó). Nên `fetch_script.py` có 3 đường tự tụt:

| # | Cách | Tốc độ | Chặn được không |
|---|---|---|---|
| 1 | `youtube-transcript-api` | ~2s | có |
| 2 | `yt-dlp` tải file phụ đề | ~10s | có |
| 3 | **`yt-dlp` tải TIẾNG + `faster-whisper`** | ~9 ph / video 34' | **KHÔNG** — và chạy được cả video KHÔNG có phụ đề |

`--method whisper` để ép đường 3; `--whisper-model tiny/base/small/medium`.

## CÒN LẠI

- [x] ~~Chốt cách ép độ dài~~ → xong: `trim_chunked` (xem §CÔNG THỨC B3).
- [ ] `new_profile.py` — wizard lập kênh mới (gợi ý giọng → nghe thử → calibrate → LLM sinh gate/sheet).
- [ ] GUI PySide6 + `build_exe.bat` (theo skill `tao_tool_exe.md`: `--selftest`, taskkill /F /T, font Nhật bundle).
- [x] ~~Chạy end-to-end 1 video hoàn chỉnh~~ → `assets/satori_jp/ep3b-auto/final.mp4` (30'39", 1080p,
      680MB): tự chạy B3→B8 hết **41 phút**, tiền ảnh ~14.000đ (123 ảnh).
