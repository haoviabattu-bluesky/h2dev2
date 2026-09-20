# SOP — LANE D: 色が語る記憶 (ảnh WW2 thật, AI tô màu, kể 1 người/1 khoảnh khắc cụ thể)

> **Đây KHÔNG phải SOP satori/Lane A/Lane E.** Vào nhầm SOP = tự động bật REF-LOCK cho kênh không
> có nhân vật lặp lại (đốt tiền ảnh vô ích), hoặc lấy ảnh AI sinh mới thay vì ảnh THẬT (phá đúng
> thứ khiến kênh này đáng tin). Trước khi làm gì, xác định profile:
>
> | Anh nói | Profile | SOP |
> |---|---|---|
> | "video satori / người già / Nhật kể chuyện đời" | `satori-jp-obaa` | `SOP_SATORI_JP.md` |
> | "video 都市伝説 / vũ trụ / bí ẩn / Lane A" | `toshi-densetsu-jp` | `SOP_TOSHI_DENSETSU_JP.md` |
> | "video sức khoẻ người già / Lane E / 健康の知恵袋" | `kenko-chiebukuro` | `SOP_LANE_E.md` |
> | "ảnh chiến tranh tô màu / 色が語る記憶 / Lane D" | **`irogatatarukioku`** | **file này** |

Nguồn nghiên cứu gốc: `docs/laneD_from_research/LANE_D_HANDOFF.md` (báo cáo nghiên cứu kênh mẫu,
đã duyệt 2026-09-10 — đọc để hiểu BỐI CẢNH, nhưng ĐỪNG copy lệnh từ đó, dùng file này). Kênh mẫu:
**色でたどる戦争の記録** `https://www.youtube.com/channel/UCaj1dslbibbHEnOAOh0tyYw`.
Kênh của mình: **色が語る記憶** `UCtRuxojb7218QeFBf5TBCQQ`, profile `irogatatarukioku`.

---

## 0. BẢNG DELTA — khác 3 lane kia chỗ nào

| Khâu | Satori | Lane A (toshi) | Lane E (kenko) | **Lane D** |
|---|---|---|---|---|
| Nguồn hình | Ảnh AI sinh mới | Clip stock | Ảnh AI minh hoạ | **Ảnh THẬT lịch sử (PD/CC0), AI chỉ TÔ MÀU — không sinh mới, không vẽ lại** |
| Nhân vật | Cụ bà lặp lại (REF-LOCK) | Không | Ẩn danh mỗi mục | **Người có thật trong ảnh, KHÔNG lặp lại giữa các tập** (`ref_lock=false`) |
| Người kể | Ngôi 1 | Ngôi 3, nam trầm | Ngôi 2 (nói chuyện với khán giả) | **Ngôi 3, nam trung niên, giọng bảo tàng** — mô tả ảnh TRƯỚC khi kể bối cảnh |
| Giọng | George @0.92 | Akira @1.15 · 374,9 chữ/ph | Papa Ji @1.0 · 290,9 chữ/ph | **Koji - Warm Japanese Business Narrator** `elevenlabs_W8wofKLOWnsM57L8hIx2` @**0.85** · **276,3 chữ/ph** (đo thật 2026-09-16; đổi từ Akira "Calm Deep" vì nghe buồn/trầm quá cho giọng lịch sử) |
| Cấu trúc | 悟り 3 tầng | 5 chương 第◯章 | List đếm ngược | **Photo-essay tuyến tính**: mỗi đoạn văn = 1 ảnh (`もう一枚/続く一枚/さらに一枚` + mô tả + bối cảnh), bookend quay lại ảnh mở đầu |
| Độ dài đã làm | 25-30' | 29-30' | 20' mục tiêu | **11-16'** (kênh mẫu 23-29', pipeline Lane D vẫn ở giai đoạn thận trọng — xem §0c) |
| **Sản xuất** | 1 bước (Claude làm hết) | 3 bước (Claude→máy2 vẽ→DeepSeek ghép) | 1 bước | **2 bước: Claude (bước 1: kịch bản→giọng→chuẩn bị đơn ảnh) → DeepSeek/Hermes (bước 2: tô màu ảnh+ghép+QC+giao hàng)** — xem §8 |
| Tô màu ảnh | — | — | — | **`ima2` (miễn phí, quota ChatGPT Plus OAuth)** — KHÔNG dùng gpti2_edit.py trả tiền nữa (profile cũ còn ghi gpti2, đã lỗi thời, xem §6) |
| Thumbnail | Chân dung REF-LOCK | Ảnh vũ trụ, không mặt người | Nền đen + ảnh đồ ăn thật | **Ảnh chân dung DỌC đã tô màu, mặt PHẢI/chữ TRÁI** — `--fit-height --subject-side right` bắt buộc (xem §7) |
| Rủi ro riêng | Thấp | Chính sách trung bình | Y khoa | **Bản quyền ảnh + nhạy cảm lịch sử/chính trị** — xem §7 handoff gốc |

---

## 0b. CHANNEL ANALYZER — bắt buộc trước khi viết bất kỳ tập nào

`docs/channel_dna/irogatatarukioku/CHANNEL_DNA.md` — **đã chạy xong 2026-09-16** (Sonnet tự chạy tại
đây, không qua máy 2). Kênh mẫu có 21 video → lấy đủ 20 làm ứng viên (≤20 thì lấy hết, kênh này vừa
đủ), chọn lọc 10 video tốt nhất đưa vào phân tích. QC DNA 11/11 đề mục ĐẠT.

```bash
cd E:\CLAUDE\YOUTUBE\h2dev
py -3.13 pipeline\channel_analyzer.py --channel-url "https://www.youtube.com/channel/UCaj1dslbibbHEnOAOh0tyYw" \
    --out-dir docs\channel_dna\irogatatarukioku --n-candidates 20 --n-select 10 \
    --niche-hint "WW2史実写真AIカラー化・実在人物の最期を辿る"
```

⚠️ **Đã dính 429 khi crawl transcript (2026-09-16)** — chạy lần 2 (mở rộng ứng viên) bị YouTube chặn
IP hoàn toàn (0/20 video, mọi retry đều 429), khả năng do chạy trùng giờ với 1 tab khác (Lane E) đang
crawl 20 video khác trên cùng máy, cộng dồn hạn ngạch IP. **Fix: thêm `--proxy socks5h://user:pass@host:port`
(SOCKS5)** — verify thật: 20/20 video sạch, 0 lỗi 429, 91s. Proxy đã verify sống (2 dây, IP khác nhau,
khác IP máy thật):
```
socks5h://haonguyen262.hao1:quanghao@154.198.33.150:9093
socks5h://haonguyen262.hao4:quanghao@154.198.33.150:9093
```
Dùng khi thấy log lặp `ERROR: Unable to download video subtitles ... HTTP Error 429` liên tục không
tiến triển (không phải 1-2 lần retry rồi qua — đó là bình thường, cứ để tool tự retry). Cờ `--proxy`
đã có sẵn ở cả `channel_analyzer.py` và `fetch_script.py`.

Dùng khi chọn chủ đề tập mới (không cần internet/API key, chạy máy nào cũng được):
```bash
py -3.13 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\irogatatarukioku \
    --topic "<mô tả chủ đề tập sắp viết, tiếng Nhật>" --top-n 8
```

**⭐ TỰ VẬN ĐỘNG — KHÔNG NGỒI CHỜ:** thiếu/chưa có `docs/channel_dna/irogatatarukioku/` thì TỰ chạy
K1+K2 ngay tại tab, không hỏi/chờ máy 2 giao hộ (máy 2 chỉ là 1 lựa chọn, không bắt buộc). Việc này
vẫn nằm trong "Bước 1 — đầu não", không vi phạm luật cấm render video (§8).

## 0c. ⚠️ ĐỐI CHIẾU CHANNEL_DNA vs 7 TẬP ĐÃ LÀM — 2 lệch cần cân nhắc sửa

CHANNEL_DNA.md phát hiện 2 điểm mà kịch bản ep01-07 (viết TRƯỚC khi có tool này) **chưa khớp đúng
công thức thật** của kênh mẫu:

1. **Tiêu đề kênh mẫu dài 75-95 ký tự**, cấu trúc 3 đoạn nối bằng `——` và `｜`, luôn kết bằng đuôi cố
   định `｜実際の写真をAIフルカラー復元`. `profile.script.gate.title_len` hiện chốt **[30,47]** — NGẮN
   HƠN NHIỀU so với thực tế kênh mẫu. Title đã dùng cho 7 tập (1 câu, không có cấu trúc 3-đoạn/đuôi
   cố định) theo đúng gate cũ nhưng KHÔNG khớp công thức thật.
2. **Cụm ghim thị giác `写真をよく見てほしい`** (nhìn kỹ bức ảnh này) lặp lại 6-12 lần/video, và cụm
   chuyển cảnh `この写真をカラー化してみる` (thử tô màu bức ảnh này) trước mỗi đoạn mô tả màu — kịch
   bản ep01-07 dùng mô-típ khác (`もう一枚/続く一枚/さらに一枚`) chứ không có 2 cụm ghim này.

**Chưa tự ý sửa** — đây là phát hiện MỚI (chỉ vừa có CHANNEL_DNA hôm nay), 7 tập cũ đã QC đạt theo
gate cũ và một số đã đăng/lên lịch. Quyết định áp dụng cho tập MỚI (đổi gate title_len + thêm 2 cụm
ghim) hay giữ nguyên công thức đang dùng — hỏi user trước khi đổi `profile.script.gate`.

**✅ ĐÃ CHỐT 2026-09-20 (user giao toàn quyền, tab YT-TITLE-RESEARCH):** tiêu đề + mô tả lane D từ nay do tool
`E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH` sinh theo CÔNG THỨC KÊNH MẪU (`【sự kiện】hook——hệ quả｜số liệu｜実際の写真をAIカラー化`,
60–90 ký tự chưa tính suffix, 【】+hook trọn 35 ký tự đầu) — luật ở `config/lanes/irogatatarukioku.json`, quy trình ở
`docs/lanes/irogatatarukioku.md` (bên tool). Lệnh: `py -3.13 cli.py run --slug <ep> --profile irogatatarukioku` rồi
`sheet` (cột E) + `deliver` (chép `TIEU_DE_MO_TA.txt` sang CHANEL/<ep>, xoá `listting.txt`). Khuôn file mới: KHÔNG dòng tags
(tags trên sheet cột F), giữ đoạn miễn trừ AI + khối 【映像・画像クレジット】. `profile.script.gate.title_len` [30,47] KHÔNG đổi —
đó là cổng KỊCH BẢN/series_ctx, không phải tiêu đề đăng. 11 tập ep01–11 đã chạy lại 2026-09-20.
Cụm ghim `写真をよく見てほしい` (mục 2) vẫn chưa quyết — ngoài phạm vi tool tiêu đề.

---

## 1. QUY TRÌNH 2 BƯỚC — TỔNG QUAN

**Bước 1 (Claude, tab này)** — nghiên cứu → kịch bản → giọng → chuẩn bị đơn ảnh. **DỪNG CỨNG trước
khi tạo ảnh** (theo chỉ thị 2026-09-16: kể cả tô màu ảnh chính cũng không tự làm nữa — khác ep02-05
trước đó, xem ghi chú trong `BAN_GIAO_BUOC2.txt` của từng tập).

**Bước 2 (DeepSeek/Hermes, agent khác)** — tô màu ảnh (`ima2`) → dựng thumbnail → ghép video → B8Q →
B10 → B11 giao hàng → burn phụ đề Việt → ghi cột G Sheet. Hồ sơ tự chứa: **`docs/GIAO_VIEC_LANE_D_
BUOC2.md`** (quy trình chung, lệnh + cấm + cổng + sổ xử lý lỗi) + `BAN_GIAO_BUOC2.txt` riêng từng tập
(số liệu + ghi chú riêng, Claude viết cuối bước 1).

Không có bước 3/máy 2 nào khác trong luồng sản xuất thường xuyên — chỉ 2 "người": Claude và DeepSeek.

---

## 2. B0 — NGHIỆM THU HỒ SƠ (SPACE_RESEARCH)

```bash
py -3.13 pipeline\qc_hoso.py --folder "E:\CLAUDE\YOUTUBE\SPACE_RESEARCH\output\_READY\d<nn>-<slug>" \
    --profile irogatatarukioku
```

Hợp đồng khai ở `profile.research` — file ảnh PHẢI tên `evidence.json` (KHÔNG `photos.json`), có
`series_ctx.txt` với khối `TIÊU ĐỀ` (≥2 phương án). **2 lỗi định dạng gặp ở CẢ 3 tập gần đây nhất
(ep05/06/07)**, đều tự sửa tại chỗ (đúng quy tắc B0 "tự sửa format, trả lại nội dung"):
- `cp photos.json evidence.json` (đổi tên, không đổi nội dung).
- Thiếu khối `TIÊU ĐỀ` → tự viết 3 phương án (30-47 ký tự theo gate cũ — xem §0c nếu gate đổi) chèn
  trước dòng `TƯ LIỆU SỰ THẬT`.

B0 ĐẠT mới copy `series_ctx.txt` + `evidence.json` + `photos/` vào
`assets/irogatatarukioku/ep<nn>-<slug>/`. B0 TRƯỢT vì **nội dung** (bịa số liệu/nguồn) thì trả lại
SPACE_RESEARCH kèm danh sách, KHÔNG tự sửa hộ dữ kiện.

---

## 3. B2/B3 — VIẾT KỊCH BẢN (việc PHẢI Claude tự làm, không giao subagent)

**Cấu trúc bắt buộc** (`profile.script.structure = "lane_d_photo_essay"`): mỗi đoạn văn (ngăn cách
2 dòng trống) = 1 ảnh trong `evidence.json`, mở bằng cụm neo duy nhất trong toàn script
(`もう一枚、<mô tả ảnh>...`/`続く一枚には...`/`さらに一枚...` — luân phiên tránh lặp máy móc, xem
§0c về 2 cụm ghim thêm nếu đổi công thức). Đoạn cuối `もう一度、最初の写真に戻ろう` quay lại ảnh mở đầu
(bookend) nếu script có câu kết nhắc lại ảnh đầu.

**Luật nội dung** (`ctx_label` trong profile): mọi tên/ngày/số liệu PHẢI lấy đúng từ `series_ctx.txt`
— cấm bịa thêm dù hợp lý đến đâu. Hồ sơ SPACE_RESEARCH có thể tự nó SAI (xem 3 ví dụ thật §4) — phát
hiện qua QC thì SỬA CẢ dossier (bản SPACE_RESEARCH gốc lẫn bản local) kèm ghi chú `h2dev訂正` +
nguồn kiểm chứng độc lập, KHÔNG chỉ sửa script rồi để dossier sai nguyên.

**Độ dài**: không có công thức cố định "X phút = Y chữ" đáng tin — 7 tập đã làm dao động 2.891-4.192
ký tự thô (~11-15 phút thô trước giãn nhịp), tuỳ độ giàu tư liệu của từng dossier. Đếm nhanh:
```bash
py -3.13 -c "t=open('script.txt',encoding='utf-8').read().replace(chr(10),'');print(len(t), round(len(t)/276.3,1),'phut tho')"
```
Dưới ~3.500 ký tự → cân nhắc mở rộng bằng MÔ TẢ THỊ GIÁC thêm cho mỗi ảnh (không phải bịa dữ kiện
mới) trước khi chấp nhận tập ngắn.

**Hedge bắt buộc khi hồ sơ tự mâu thuẫn** (đã gặp ở ep06 — 3 lời khai khác nhau về cách Nagumo chết;
ep07 — ngày nhậm chức 7月 vs 9月, ngày tử trận 20日 vs 25日, câu nói nổi tiếng chỉ có trong nguồn Anh
ngữ): dùng `〜という／〜とされる／複数の証言が残っており、正確な状況は分かっていない`, KHÔNG tự chọn
1 phía khi dossier ghi rõ đang mâu thuẫn.

---

## 4. B3Q + B3F — HAI CỔNG, HAI CÂU HỎI KHÁC NHAU

`qc_script.py` hỏi *"kịch bản tự mâu thuẫn/lặp không"*; `qc_facts.py` hỏi *"chi tiết này ở ĐÂU ra"*.

```bash
py -3.13 pipeline\qc_script.py --profile irogatatarukioku --script <ep>\script.txt
py -3.13 pipeline\qc_facts.py --script <ep>\script.txt --dossier <ep>\series_ctx.txt
```

**Lỗi thật đã bắt được qua 7 tập** (không phải lý thuyết — số đo thật, mỗi lỗi kèm cách sửa):
- **Lặp mô-típ mở đoạn** (もう一枚/続く一枚/さらに一枚 dùng quá đều, 2 đoạn liền kề cùng chủ đề tù
  binh/cảnh hoang tàn không phát triển thêm) → sửa bằng cách VARY động từ mở đoạn + gộp 2 đoạn mỏng
  thành 1 đoạn giàu hơn thay vì 2 đoạn nhạt.
- **Rò từ Latin** (`TBM-1C`, `LVT-2`) → bỏ mã hiệu kỹ thuật, giữ tên chung tiếng Nhật (`アベンジャー
  雷撃機`, `水陸両用装軌車`).
- **Mâu thuẫn thời gian có thật trong DOSSIER GỐC** (ep06): "trận Biển Philippines xảy ra NGAY TRƯỚC
  khi đổ bộ Saipan" — SAI, verify qua Wikipedia thì xảy ra **4 ngày SAU** (19-20/6 so với đổ bộ
  15/6). Sửa cả dossier + script, ghi `h2dev訂正` + nguồn.
- **Số liệu thiếu breakdown, đọc nhầm là tổng** (ep07): dossier ghi "17 tù binh sống sót (đa số lao
  công Triều Tiên)" — 17 CHỈ là lính Nhật, tổng thật (Wikipedia xác nhận) là **146 = 17 lính Nhật +
  129 lao công Triều Tiên**. Sửa cả dossier + script (2 chỗ).
- **Claim không nguồn tự thêm** ("サイパン島の中心都市", "わずか数キロ四方") → B3F bắt được vì không
  có trong `series_ctx.txt` dù đúng về mặt lịch sử — XOÁ, không tự tin dùng kiến thức nền ngoài
  dossier.

⚠️ **Khi QC (LLM) mâu thuẫn với dossier**: verify độc lập qua WebFetch/WebSearch trước khi quyết định
sửa cái nào. Có lúc QC đúng (ép06 Philippine Sea, ep07 tù binh), có lúc QC sai/dùng kiến thức ngoài
phạm vi nguồn được cấp (vd flag "17 lính Nhật ≠ 146 tổng" ban đầu tưởng vô lý nhưng verify ra QC
ĐÚNG; ngược lại có flag về "casualty breakdown ep06" hoá ra chỉ là cách phân loại mơ hồ của nguồn,
không phải lỗi cần sửa). Đừng sửa mù theo QC, cũng đừng phớt lờ mù — luôn kiểm tra.

---

## 5. B4 — GIỌNG + GIÃN NHỊP + B4Q

```bash
py -3.13 pipeline\tts.py --script <ep>\script.txt --out <ep>\voice.mp3 --provider openspeaker --profile irogatatarukioku
py -3.13 pipeline\srt_from_script.py --srt <ep>\voice.srt --script <ep>\script.txt
py -3.13 pipeline\pace_audio.py --audio <ep>\voice.mp3 --srt <ep>\voice.srt --script <ep>\script.txt \
    --out-audio <ep>\voice_paced.wav --out-srt <ep>\voice_paced.srt
py -3.13 pipeline\qc_audio.py --audio <ep>\voice_paced.wav --srt <ep>\voice_paced.srt
```

Giọng nạp tự động từ `--profile irogatatarukioku` (Koji, speed 0.85). Đo thật giãn nhịp: +8-15% thời
lượng, tỉ lệ nói 76-87%. `qc_audio.py` ĐẠT chuẩn: `pause_misplaced=0`, `dropouts=0`, `peak_db` dưới
-1dB, `srt_drift` ~0.

⚠️ Đổi giọng/tốc độ → BẮT BUỘC đo lại: `py -3.13 pipeline\calibrate.py --profile irogatatarukioku
--style doc`. Đã đổi từ Akira (Calm Deep — "buồn/trầm quá cho giọng lịch sử") sang Koji 2026-09-16,
đo lại char_rate gần như không đổi (276.0→276.3), không cần tính lại độ dài kịch bản.

---

## 6. CHUẨN BỊ ĐƠN ẢNH — anchors.txt + colorize_map.txt (Claude làm, KHÔNG tự tô màu)

**Mốc chương thật**: định vị từng câu neo trong `voice_paced.srt` bằng offset ký tự (KHÔNG chia đều
thời lượng — `sync_durations()` mặc định của `assemble.py` làm mất khớp hình/lời, xem
`profile.body.assemble_note`). Kỹ thuật: nối toàn bộ text các cue theo thứ tự, `str.find()` câu neo
trong chuỗi nối, map offset về cue chứa nó, lấy timestamp cue đó.

**`anchors.txt`** — mỗi dòng `<slot>.png|<câu neo nguyên văn, xuất hiện ĐÚNG 1 LẦN trong script.txt>`.
Verify uniqueness trước khi ghi file:
```bash
grep -o -F "<câu neo>" <ep>\script.txt | wc -l    # phải ra đúng 1
```

**`colorize_map.txt`** — mỗi dòng `<slot>.png|<ảnh nguồn trong photos/>|<size ima2>`. Quy tắc kích
thước theo tỉ lệ khung ảnh gốc (đo `PIL.Image.size`, `w/h`):
| Tỉ lệ w/h | Size ima2 |
|---|---|
| ≥1.15 (ngang) | `1536x1024` |
| ≤0.87 (dọc) | `1024x1536` |
| còn lại (vuông-ish) | `1280x1280` |

Slot cuối thường COPY slot đầu (bookend, không gọi ima2 lại — ghi rõ `COPY of 000.png (bookend,
không gọi ima2 lại)|-`). File `.tif` trong nguồn (gặp ở ep07) → ghi chú cảnh báo cho bước 2 convert
trước nếu ima2 không nhận thẳng.

⚠️ **Từ 2026-09-16, Claude KHÔNG tự chạy `ima2` nữa** (kể cả ảnh chính cho thumbnail) — dừng hẳn ở
việc CHUẨN BỊ đơn (`colorize_map.txt`), bước 2 tự tô màu slot 000 trước rồi mới dựng thumbnail. Nếu
sau này user yêu cầu quay lại tự tô ảnh chính: dùng `ima2 edit <src> --prompt "colorize, keep
composition 100% identical, natural 1940s color estimate" --model gpt-5.6-luna --quality high --size
<theo bảng trên> -o <out> --json`, gọi qua đường dẫn tuyệt đối
`C:\Users\admin\AppData\Roaming\npm\ima2.cmd` (Python subprocess không tự resolve `.cmd` shim).

---

## 7. THUMBNAIL — CHỈ CHUẨN BỊ THEO ĐÚNG QUY TẮC, KHÔNG TỰ DỰNG

`thumb_text.txt` (4 dòng `MÀU|nội dung` + `BANNER|...`, giống format các lane khác) — Claude viết,
bước 2 dựng bằng lệnh cố định trong `profile.thumbnail.template.command`:
```
py -3.13 pipeline\thumbnail_text.py --bg <ep>\img\000.png --text <ep>\thumb_text.txt \
    --out <ep>\thumbnail_final.png --side left --wrap --fit-height --subject-side right
```

**Vì sao bắt buộc `--fit-height --subject-side right`** (chốt 2026-09-16, dính lỗi thật ở ep02-05):
ảnh `000.png` luôn là chân dung DỌC (1024x1536/1536x2048). Cover-crop mặc định của `thumbnail_text.py`
ép khung ngang 1280x720 lên ảnh dọc bằng cách scale theo CHIỀU RỘNG — sau đó không còn biên ngang dư
nào để đẩy mặt sang một bên, nên mặt LUÔN kẹt ở giữa khung bất kể `--side left/right`, đúng ngay vào
ranh giới vùng chữ. `--fit-height` scale theo CHIỀU CAO (giữ trọn khổ dọc), ghim khối mặt hẳn sang
`--subject-side right`, phần trống bên trái lấp bằng chính ảnh đó phóng to làm nền mờ — chữ và mặt
không bao giờ tranh chỗ. Chi tiết: memory `lane-d-thumbnail-fit-height`.

**Ngoại lệ duy nhất**: ảnh NHÓM nhiều người dàn ngang (như ep01, sĩ quan trong hang) → GIỮ cover-crop
mặc định (bỏ `--fit-height`), `--fit-height` sẽ ghim theo góc và cắt mất người khác trong nhóm.
Kiểm nhanh trước khi áp dụng: `000.png` là chân dung 1 người hay cảnh nhóm/rộng?

---

## 8. BÀN GIAO BƯỚC 2

Cuối bước 1, viết `<ep>/BAN_GIAO_BUOC2.txt` (mẫu: xem `assets/irogatatarukioku/ep06-nagumo-saipan/
BAN_GIAO_BUOC2.txt` hoặc `ep07-shibasaki-tarawa/BAN_GIAO_BUOC2.txt`) — số liệu + ghi chú RIÊNG tập
đó, KHÔNG lặp lại lệnh (lệnh nằm hết trong `docs/GIAO_VIEC_LANE_D_BUOC2.md`, sửa ở đó thì mọi tập
tự động theo bản mới). Câu lệnh đưa cho Hermes:
```
Đọc kỹ 2 file sau rồi làm THEO ĐÚNG THỨ TỰ:
1) E:\CLAUDE\YOUTUBE\h2dev\docs\GIAO_VIEC_LANE_D_BUOC2.md
2) E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\<ep>\BAN_GIAO_BUOC2.txt

Thư mục làm việc: E:\CLAUDE\YOUTUBE\h2dev\assets\irogatatarukioku\<ep>
Sheet tab: irogatatarukioku, dòng: <STT>

Xong báo lại: đường dẫn CHANEL, thời lượng final.mp4, kết quả B8Q/B10, phụ đề Việt có đè chữ Nhật
không (trích 1 khung hình giữa video để kiểm).
```

Bước 2 làm: tô màu ảnh (ima2) → thumbnail thật → `assemble.py --anchors --fit blur --burn-sub` →
B8Q (`--srt` BẮT BUỘC, KHÔNG `--script` — bug đã dính ep01-04, xem `docs/GIAO_VIEC_LANE_D_BUOC2.md`
§5.1) → B10 → B11 giao hàng → phụ đề Việt → `ghi_cot_video.py --tab irogatatarukioku --dong <STT>`
→ chuyển dossier SPACE_RESEARCH sang `_DONE\`.

**Sau khi bước 2 báo xong, LUÔN verify độc lập, không tin mù**: đã bắt được 1 báo cáo sai thật (ep05
— DeepSeek báo "burn phụ đề Việt không đè chữ" nhưng trích khung hình thật thì THẤY đè — xem §9 lỗi
chưa sửa).

---

## 9. SỔ SẢN XUẤT THẬT (cập nhật 2026-09-16)

| Tập | STT | Nhân vật/Trận | Bước 1 | Bước 2 | Giao hàng |
|---|--:|---|---|---|---|
| ep01-ushijima-mitsuru | 1 | 牛島満, Okinawa | ✅ | ✅ | ✅ đã lên lịch/đăng |
| ep02-kuribayashi-iwojima | 2 | 栗林忠道, Iwo Jima | ✅ | ✅ | ✅ ĐÃ ĐĂNG |
| ep03-nakagawa-peleliu | 3 | 中川州男, Peleliu | ✅ | ✅ | ✅ đã lên lịch |
| ep04-aruga-yamato | 4 | 有賀幸作, chiến hạm Yamato | ✅ | ✅ | ✅ đã lên lịch |
| ep05-yamazaki-attu | 5 | 山崎保代, Attu | ✅ | ✅ (DeepSeek) | ✅ giao (phụ đề Việt còn lỗi đè chữ, chưa sửa) |
| ep06-nagumo-saipan | 6 | 南雲忠一, Saipan | ✅ (giọng Koji, sửa lỗi Philippine Sea) | ⏳ đã bàn giao, chưa có báo cáo | — |
| ep07-shibasaki-tarawa | 7 | 柴崎恵次, Tarawa/Betio | ✅ (sửa lỗi 17/146 tù binh) | ⏳ đã bàn giao, chưa có báo cáo | — |

Tất cả 5 tập ep01-05 hiện dùng thumbnail bố cục **cũ** (`--side left/right` không `--fit-height`) đã
được **regenerate lại đúng chuẩn mới** (§7) và redeliver 2026-09-16.

---

## 10. LỖI CHƯA SỬA — biết trước khi hỏi lại

**Phụ đề Việt đè chữ Nhật** (ảnh hưởng CẢ 5 tập đã giao, kể cả bước 2 của DeepSeek lẫn của Claude
trước đây): `assemble.py`'s phụ đề Nhật burn-in dùng style `Alignment=2, MarginV=45`; lệnh burn phụ
đề Việt riêng dùng `Alignment=2, MarginV=40` — gần như cùng vị trí, 2 lớp phụ đề chồng nhau ở
`final_vi_phude.mp4`. Đã báo user, **chưa quyết định thời điểm sửa**.

**Gate title_len + thiếu 2 cụm ghim thị giác** — xem §0c, chưa quyết định có đổi công thức cho tập
mới hay không.

**`profile.body.colorize.tool` còn ghi `gpti2_edit.py` (trả tiền)** — đã lỗi thời, thực tế dùng
`ima2` (miễn phí) từ ep04 trở đi. Cần cập nhật field này (và dòng tương ứng trong bảng router ở
CLAUDE.md gốc dự án) lần tới sửa profile.
