# 07 WORKFLOW — Satori-Lopezzapa68 · satori-jp-obaa

> Lane `satori-jp-obaa`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# QUY TRÌNH TIÊU ĐỀ + MÔ TẢ — LANE SATORI (`satori-jp-obaa`)

> 🔴 **CẬP NHẬT 2026-09-23 — đọc TRƯỚC file này:**
> `docs/lanes/satori-jp-obaa/SOP_TIEU_DE_THUMBNAIL_2026-09-23.md` — công thức 2 vế đo từ kênh mẫu Hàn
> 노년의 마음소리, luật viết chữ thumbnail (lời thoại có người nói), trần ký tự, chuỗi lệnh `title-ask →
> lock → thumb-ab → sheet-publish`, 7 bẫy đã trả giá và 7 tập mẫu. Phần dưới là quy trình gốc 2026-09-20,
> vẫn đúng về vai trò/model nhưng LUẬT TIÊU ĐỀ + THUMBNAIL lấy theo SOP mới.

Chốt 2026-09-20 sau 1 ngày thử trên simbot2-01/02. **Chỉ áp dụng cho lane này.** Lane khác (toshi-densetsu, teinengo…) có ngách,
khán giả, kiểu tiêu đề khác → tạo file `docs/lanes/<mã>.md` + `config/lanes/<mã>.json` riêng, không dùng chung luật tiêu đề.

## 1. Kênh · sheet · thư mục
| | |
|---|---|
| Kênh thật | 人生の夕暮れ · `UC9huXCiBIXBfUh11D7ZsFSA` (mới 09/2026, 5 video 1–7 view khi bắt đầu) |
| Kênh mẫu | simbot2 (Hàn) · `docs/channel_dna/simbot2` |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<slug>` |
| Sheet | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` tab **`Lopezzapa68`** (header B ghi "lane satori"). Cột C = đường dẫn tập · **cột E = tiêu đề tool ghi** · cột L = tiêu đề cũ viết chay (giữ để so). |
| Config | `config/lanes/satori-jp-obaa.json` (luật tiêu đề `title_rules`, độ dài, bộ lọc ngách, sheet) |

## 2. Quyền sở hữu (không đổi)
> **Model đang đóng vai Fable: `claude-fable-5-1` (bật lại 2026-09-23, đã ping OK 6s).**
> Cách tạm đổi khi Fable hết quota: thêm `model_writer_override` + `model_picker_override` = `"opus"` vào
> `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\satori-jp-obaa.json`; bật lại = XOÁ hẳn 2 khoá đó (không chỉ đổi giá trị).
> Ảnh hưởng cả S2/S3/S3c/S3b (tiêu đề) lẫn S7 (chữ thumbnail). Vai trò/quyền không đổi, chỉ đổi model đóng vai.
- **Fable 5.1 = tác giả tiêu đề, quyền cuối.** Viết 3 → chọn 1 (context mới) → kiểm 5 bất biến → KHOÁ → phân xử ý kiến thanh tra.
- **Opus = tác giả mô tả, quyền cuối.** Viết → sửa theo mã lỗi (D1, D2…). Không bao giờ chạm tiêu đề.
- **GPT-5.6-sol = thanh tra.** Chỉ chỉ ra vi phạm có mã `T1 | FACTUAL | HIGH | … ⟵ chứng cứ`. Không định hình văn phong. Chấm 2 lượt gộp (Sol không ổn định).
- **Anh = quyết ESCALATE** và phủ quyết bằng `emit --title N`.

## 3. Chuỗi 1 tập (≈12 phút lần đầu, cache từng bước)
```
seeds (Opus) → crawl (yt-dlp, keyless) → mine → S1 Opus tóm tắt → S2 Fable 3 tiêu đề → S3 Fable chọn 1
→ S3c Fable 5 bất biến + KHOÁ (TITLE_LOCK.json) → S4 Opus mô tả → emit → QC1 Sol
→ router: T-objective → Fable 4 nhãn (ACCEPT_FIX / REJECT_STYLE / REJECT_WEAK_EVIDENCE / ESCALATE) · D → Opus sửa · STYLE_ONLY bỏ
→ QC2 → Opus sửa 2 → QC3 nghiệm thu → Fable phân xử cuối (chỉ nếu còn T objective) → emit → sheet cột E
```
Mở khoá tiêu đề CHỈ khi: FACTUAL · MISLEADING · SEMANTIC · UNNATURAL_SEVERE · KEYWORD_MISMATCH · SPOILER · LENGTH.
KHÔNG mở vì "hay hơn / ngắn hơn / cảm xúc hơn / tôi thích từ khác".
Verdict do router tính: FAIL = còn FACTUAL/MISLEADING/KEYWORD HIGH · FIX = còn lỗi ≥ MEDIUM · PASS = còn lại.

## 4. Luật tiêu đề satori (bản gốc ở `config/lanes/satori-jp-obaa.json` → `title_rules`, prompt đọc từ đó)
1. Động từ CÓ SỰ CỐ (漏らした・笑われた・外された・解散・消えた…) thay 言った/口にした. Đúng kịch bản.
2. Hậu quả CỤ THỂ (40年の会が解散, LINE誤送信の一行). Cấm kết 目が変わった/後悔/真実 một mình.
3. Đúng 1 mảnh bị giấu (理由/なぜ/一行/… trước mảnh giấu). Không lộ twist.
4. Nhân vật có vai + cược con số (73歳の元惣菜屋 · 年金25万 · 3年).
5. 30–40 ký tự Nhật (điện thoại 2 dòng ≈ 40), tối đa 48, móc trọn trong 28 ký tự đầu.
   Đo 154 tiêu đề ngách: 31–40 ký tự gmean 20K · 41–50 → 9K · 61–80 → 5K.
6. Mẫu XẤU đã loại: 「年金「月25万円」と口にした途端、40年来の仲間の目が変わった…73歳の後悔」 (trung tính, mơ hồ, chung chung).
   Mẫu ĐẠT: 「年金「月25万」を漏らした73歳…40年の仲間の会が解散、LINE誤送信の一行」 (39).

## 5. Lệnh
```bash
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
py -3.13 cli.py run   --slug E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<slug> --profile satori-jp-obaa   # cả chuỗi
py -3.13 cli.py view  --slug <dir>                       # XEM.html: tóm tắt · tiêu đề (khung điện thoại) · 3 ứng viên · mô tả · QC · ESCALATE
py -3.13 cli.py sheet --profile satori-jp-obaa           # ghi tiêu đề TOOL lên cột E (chỉ tập có TITLE_LOCK); --report xem trạng thái file
py -3.13 cli.py emit  --slug <dir> --title 2 && py -3.13 cli.py run --slug <dir> --from lock --force   # phủ quyết: ép ứng viên 2 rồi khoá + mô tả lại
py -3.13 cli.py all   --profile satori-jp-obaa --only simbot2-03,simbot2-04                          # batch
```
Chạy SAU khi `script.txt` đạt QC; tool giữ nguyên khối Timestamps nếu bước 3 đã điền. Bản cũ luôn có `.bak`.

## 5b. Khuôn file + giao hàng (anh chốt 2026-09-20, chỉ lane này)
- `TIEU_DE_MO_TA.txt` KHÔNG còn dòng 5 keyword (tags đã có trên sheet cột F): dòng 1 tiêu đề · trống · mô tả · vạch · Timestamps
  (giữ nguyên) · vạch · cảm ơn · vạch · hashtag. Config `tieu_de_keywords_line: false`.
- `cli.py deliver --slug <dir>` chép file vào thư mục giao hàng `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\<ep-…>` (lấy từ cột I sheet,
  không có thì dò theo id video) và XOÁ `listting.txt` cũ ở đó cho khỏi loạn. Đã test ep01 17:19.
- Lưu ý: `h2dev/pipeline/ghi_cot_video.py` đếm listting.txt là 1/3 file "đã giao" — tập đã ghi cột VIDEO rồi thì không ảnh hưởng.

## 6. Khi nào can thiệp tay
- XEM.html mục 5 có **ESCALATE** → anh đọc lý do 2 bên, giữ hoặc `emit --title N`.
- Sol `SKIPPED` (9router + ns24 đều chết) → file vẫn hợp lệ nhưng chưa có thanh tra; chạy lại `qc-sol` sau.
- Tập chưa có `TIEU_DE_MO_TA.txt` (cột E ghi `[CHƯA CÓ FILE]`) → chạy `run`, tool tạo mới với placeholder Timestamps.

## 7. Đo sau khi đăng
`cli.py track --profile satori-jp-obaa --deep` mỗi ngày → `data/track.csv`. So CTR Home/Suggested trong Studio sau 7 ngày
(docx §14). Kênh mới, subscriber 0 → views thấp không chỉ do tiêu đề.

## 8. Nhật ký quyết định
| Ngày | Quyết định |
|---|---|
| 2026-09-20 | Chuỗi Opus tóm tắt → Fable viết 3 → Fable chọn 1 → Opus mô tả (anh chốt). |
| 2026-09-20 | Độ dài 40/48/28 từ dữ liệu; loại tiêu đề 57 ký tự. |
| 2026-09-20 | Luật tò mò 4 điểm (anh loại bản 「口にした途端…」). |
| 2026-09-20 | Kiến trúc QC: Fable sở hữu tiêu đề + 4 nhãn phân xử + 5 bất biến + khoá; Opus sở hữu mô tả; Sol thanh tra lỗi có mã; Sol chấm 2 lượt gộp. |
| 2026-09-20 | Cột E sheet = tiêu đề tool; cột L giữ tiêu đề cũ. |
| 2026-09-22 | Fable hết quota → Opus tạm thay mọi vai Fable của lane (override trong config lane; xoá khoá để bật lại). |
| 2026-09-23 | Fable có quota lại → XOÁ 2 khoá override, lane quay về `claude-fable-5-1` cho S2/S3/S3c/S3b + S7 (ping OK 6s). |
| 2026-09-20 | Bỏ dòng keyword trong TIEU_DE_MO_TA.txt; `deliver` chép sang CHANEL/<ep> + xoá listting.txt (test ep01). |

## Thumbnail (S7, gộp 2026-09-22)
Phong cách khoá của lane ở `config/lanes/satori-jp-obaa.thumb.yaml` (mẫu kênh / TEMPLATE ở `docs/lanes/satori-jp-obaa/thumb/`). `run` tự chạy sau
`deliver`; ảnh chọn `<slug>/thumbnail_final.png`, 3 ảnh + điểm Fable/Opus trong `research/XEM.html` mục 7. DỪNG chờ anh →
`py -3.13 cli.py thumb-publish --slug <dir> --profile satori-jp-obaa [--choose B]` mới ghi Sheet G + CHANEL. Chi tiết `docs/thumbnail.md`.

## 2026-09-23 — sửa gói packaging ep01 sau khi CTR 2,3 %
- Sol (S8 `sol-check`) chấm gói CŨ: tiêu đề **4/10**, thumbnail **5,5/10**. Lỗi nặng nhất: tiêu đề bán
  `年金25万 → LINE誤送信 → 40年の会が解散` còn thumbnail LIVE bán `親友が3年前に引っ越した` — hai câu chuyện khác nhau.
  Thêm: `月25万` là lương hưu của HAI vợ chồng (`夫婦二人を合わせ、月に二十五万円ほど`) nhưng tiêu đề để hiểu thành của riêng bà;
  payoff (LINE, giải tán) nằm sâu trong video trong khi cold open là chuyện Mitsue → AVD 1:04/31:25.
- Gói MỚI (đồng bộ về đúng cold open):
  - Tiêu đề (Fable khoá, 36 ký tự): `「3年前に越されましたよ」毎週会っていた50年の親友が住所を隠していた理由`
    (seed từ đề xuất số 1 của Sol, bỏ tên riêng theo `name_policy`; Fable đổi đuôi vì trùng nguyên văn banner thumbnail).
  - Mô tả: Opus viết lại, mở bằng đúng cảnh cold open.
  - Thumbnail: **dùng `thumbnail_final.png` đã render sẵn từ 2026-09-17** (nền tối hành lang, mặt sững sờ,
    `毎週会っていたのに / 3年前に / 引っ越していた / 私だけ知らなかった`) — kể đúng câu chuyện của tiêu đề mới, KHÔNG tốn gpti2.
    Bản đang chạy trên YouTube là biến thể cũ nền bờ sông sáng (`消えた親友と…`) — chính là bản Sol chê chữ trắng không tách nền.

---
## SOP_TIEU_DE_THUMBNAIL_2026-09-23.md

# SOP TIÊU ĐỀ + THUMBNAIL — LANE SATORI (`satori-jp-obaa`) · chốt 2026-09-23

> 🔴 **BƯỚC 0 BẮT BUỘC (anh chốt 2026-09-24, mọi tập):** đọc `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\satori-jp-obaa.json`
> (luật kênh mẫu + mục `our_eps` của đúng tập) trước khi viết tiêu đề/chữ thumbnail. Đọc bắt buộc, áp dụng LINH HOẠT: chỉ lấy điểm hợp với tập, không phải luật cứng. Tool tự bơm vào prompt, còn `sheet-publish`/`thumb-publish`
> chặn tập chưa đọc. Xem mục "LUẬT BẮT BUỘC" trong `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\CLAUDE.md`.

> ⚠ **CHỈ DÙNG CHO LANE NÀY.** Mỗi lane một phong cách: lane A (都市伝説), lane D (ảnh WW2), lane G (定年後)
> có kênh mẫu khác, khán giả khác, khuôn thumbnail khác → mỗi lane phải có file SOP riêng trong
> `docs/lanes/<mã>/`. Gọi nhầm SOP của lane khác là ra tiêu đề sai ngách.
>
> Sinh ra sau khi 8 tập đầu của lane đều có CTR < 2,5 % (tập tốt nhất 7,0 %). Nguyên nhân gốc đo được:
> tiêu đề **thiếu nửa công thức của kênh mẫu**, và chữ thumbnail **kể lại đúng cái tiêu đề đã nói**.

## 1. Kênh mẫu của lane này

| | |
|---|---|
| Kênh mẫu | **노년의 마음소리** · `UCfB0fkB_giLFFZsmQmWgBWw` (Hàn, 31.300 sub, 26 video) |
| Dữ liệu tiêu đề đã kéo | `data/simbot2_source_titles.json` (tên file theo `dna_slug` của lane) |
| Công thức đã đo | `docs/lanes/satori-jp-obaa/CONG_THUC_TIEU_DE_KENH_GOC.md` |
| Đo lại | `py -3.13 -X utf8 tools/title_formula_kenh_goc.py --channel UCfB0fkB_giLFFZsmQmWgBWw --skip-newest 6 --out docs/lanes/satori-jp-obaa/CONG_THUC_TIEU_DE_KENH_GOC.md` |

**Bẫy khi đo:** yt_dlp trả video mới → cũ. Video mới nhất chưa đủ tuổi để có view, để nguyên là đo nhầm
"tuổi video" thành "chất lượng tiêu đề" → luôn `--skip-newest 6` (hoặc số video đăng trong 2 tuần gần nhất).

## 2. Công thức TIÊU ĐỀ của lane satori — 2 VẾ

```
VẾ 1: biến cố / nghịch lý / câu hỏi CỤ THỂ, có con số hoặc mốc tuổi
   …
VẾ 2: LỜI HỨA NGƯỜI XEM HỌC ĐƯỢC GÌ  (N điều cấm · lý do thật · sự thật bị giấu)
```

Đòn bẩy đo được trên 20 tiêu đề (đã bỏ 6 video mới):

| Đặc trưng | Lift | Ghi chú |
|---|---|---|
| câu hỏi / từ để hỏi (なぜ・いつ・どこ・いくら) | **2,99** | mạnh nhất |
| lệnh cấm tuyệt đối (絶対に〜てはいけない) | **2,70** | |
| dấu `…` cắt giữa câu | 1,32 | nối 2 vế |
| tuổi cụ thể | 1,00 | trung tính |
| **"N つのこと" đứng một mình** | **0,34** | ❌ chỉ mạnh khi ở VẾ 2 sau một vế 1 có nghịch lý |

**Luật cứng của lane:**
1. Tiêu đề chỉ có vế 1 (kể chuyện) = mới xong một nửa → phải thêm vế 2.
2. Số N ở vế 2 **phải có thật trong kịch bản** — grep `三つ/四つ/一つ目/N가지`. Tập 4 từng bịa `四文字の言葉`
   + `虐待` + `元看護婦` (0 lần trong kịch bản) vì dịch thẳng tiêu đề bản Hàn → cấm tuyệt đối.
3. Luật số: mọi lượng viết bằng CHỮ SỐ (`40年` `25万` `73歳` `3年前`), không `四十年`. Thành ngữ (`一言`) giữ nguyên.
4. Độ dài 30–40 ký tự, tối đa 48; móc trọn trong 28 ký tự đầu.
5. Không dùng tên riêng nhân vật.
6. Không bê nguyên con số của bản Hàn (`310만원` → `310万円/tháng` là vô lý ở Nhật; đổi sang `25万`).

## 3. Công thức CHỮ THUMBNAIL của lane satori

**Nguyên tắc số 1 (anh chốt): chữ thumbnail là MỘT CÂU CÓ NGƯỜI NÓI RA, không phải câu tường thuật.**
Ưu tiên trích nguyên văn lời thoại trong kịch bản, đặt trong 「」.

**Nguyên tắc số 2: phải có AI / Ở ĐÂU / CHUYỆN GÌ trước, rồi mới tới bí ẩn.** Câu triết lý kiểu
`入る門より出る門を訊きなさい` chỉ hiểu được sau khi xem xong video → hỏng. Người lướt phải dựng được cảnh
trong 1 giây.

**Nguyên tắc số 3: không nói lại thứ tiêu đề đã nói.** Tiêu đề và thumbnail cùng MỘT xung đột nhưng
chia vai: tiêu đề nêu biến cố + lời hứa, thumbnail đưa **một mảnh khác** (lời thoại, chi tiết lạ, con số).
Nếu tiêu đề đã ôm `なぜ` thì thumbnail không được hỏi `なぜ` nữa — và ngược lại.

**6 khuôn hook** (rút từ `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\patterns.json`, bơm vào prompt bằng `src/hook_brief.py`):
câu hỏi thẳng · con số có bí mật · kết quả ngược kỳ vọng · mâu thuẫn A-nhưng-B · bí mật chưa nói · lời thoại sốc.

**Khuôn 3 dòng + banner, trần ký tự CỨNG của lane** (vượt là engine từ chối render, mất tiền ảnh):

| Vai (màu) | Trần | Vai trò |
|---|---|---|
| `WHITE` → context (trắng) | 7 | ai / ở đâu / bối cảnh |
| `YELLOW` → hero (vàng, to nhất) | **5** | mảnh sốc nhất |
| `TRIGGER` (vàng, ≤7) | 7 | dùng khi dòng vàng cần > 5 ký tự |
| `RED` → twist / hook (đỏ) | 7 | hậu quả / vế lật |
| `BANNER` (băng đỏ dưới) | 12 | thêm nghĩa ĐỘC LẬP, không lặp 3 dòng trên |

File chữ: `<slug>/research/thumb_rows.txt`, mỗi dòng `MÀU|nội dung`.

## 4. Chuỗi lệnh 1 tập (lane satori)

```bash
# B1. Soi kịch bản trước khi viết gì: tiêu đề cũ có bịa không, có N-list thật không
#     grep 三つ/四つ/一つ目 trong <slug>/script.txt · đối chiếu từng danh từ của tiêu đề với script

# B2. Hỏi Sol chọn tiêu đề (BẮT BUỘC — không tự chốt, không hỏi anh khi chưa hỏi Sol)
py -3.13 -X utf8 cli.py title-ask --slug <slug> --profile satori-jp-obaa --candidates <file 3 dòng> \
    [--current "<tiêu đề đang dùng>"] [--source "<tiêu đề bản gốc Hàn>"]

# B3. Khoá tiêu đề qua Fable (6 bất biến, tự sửa luật số)
py -3.13 -X utf8 cli.py lock --slug <slug> --profile satori-jp-obaa --force

# B4. Ghi tiêu đề vào TIEU_DE_MO_TA.txt (giữ nguyên mô tả) + chép sang CHANEL

# B5. Chữ thumbnail → dựng ảnh (nền cache theo prompt; REF khoá mặt nhân vật của tập)
py -3.13 -X utf8 cli.py thumb-ab --slug <slug> --profile satori-jp-obaa --rows <thumb_rows.txt> --scene "<prompt cảnh>"
#     hoặc để Sol + Fable cùng đề xuất rồi so 2 ảnh:  thumb-ab --advisor both  (bỏ --rows)

# B6. Chép ảnh vào <slug>/thumbnail_final.png + CHANEL/<ep>/thumbnail.png

# B7. Ghi Sheet: E = tiêu đề · G = link Catbox · K = "TIÊU ĐỀ + THUMB ĐÃ XONG dd/m - CẦN THAY" (ghi đè)
py -3.13 -X utf8 cli.py sheet-publish --slug <slug> --profile satori-jp-obaa
```

## 5. Bẫy đã trả giá (lane này)

| Bẫy | Hậu quả thật | Cách tránh |
|---|---|---|
| Sửa nhầm thư mục nháp | `roujin-home` (người kể 佐藤静子) vs tập thật `simbot2-04-Fgc8IQvQVj8` (người kể 花) | Dò cột C của Sheet trước khi sửa |
| Dịch thẳng tiêu đề bản Hàn | Tập 4 bịa `虐待` `元看護婦` `四文字` — 0 lần trong kịch bản | Mọi danh từ trong tiêu đề phải grep ra trong `script.txt` |
| Không bơm trần ký tự vào prompt hỏi Sol/Fable | Cả hai viết dòng 8–9 ký tự → engine ném `readability hard gate` SAU KHI đã trả tiền ảnh | `thumb_advice.lane_limits()` lấy số từ chính contract engine |
| `79歳の夫が突然` tưởng 7 ký tự | Thật ra **8** (số 79 là 2 ký tự) | Luôn `len()` bằng máy, đừng đếm mắt |
| Cảnh tả nhân vật CÚI MẶT | gpti2 sinh 3 lần đều `no face detected`, mất 3 ảnh | Viết rõ `FACE IS FULLY VISIBLE, three-quarter angle` |
| Tập cũ không có REF nhân vật | `gpti2 (image edit) requires an approved REF` | `thumb_ab` tự chuyển sang `gpti2_text` |
| Chạy 3 job render song song bằng `&` trong 1 lệnh | 1 job chết câm, log rỗng | Chạy nền từng job hoặc kiểm log từng file |

## 6. 7 tập đã làm theo SOP này (2026-09-23) — dùng làm mẫu

| Tập | Tiêu đề (vế 1 … vế 2) | Chữ thumbnail (lời thoại / mảnh khác) |
|---|---|---|
| 1 | 年金25万を漏らした後、40年の会が解散…**老後に絶対言ってはいけない4つ** | 静ちゃんには / 言わないでね / 届いた誤送信 · `年金額は絶対に秘密` |
| 2 | 倒れたのは80歳の母ではなく娘…**共倒れを防ぐため絶対忘れてはいけない3つのこと** | 通帳は見せない… → 娘が先に倒れた / 親孝行を / 禁じました · `介護する家族を守るために` |
| 3 | 7年暮らしても、なぜ葬儀では「知人」なのか…**事実婚で備える3つのこと** | 7年の伴侶 / 芳名帳では / ただの「知人」 · `事実婚の落とし穴` |
| 4 | 74歳、老人ホームを88日で出ました…**入る前に施設へ訊くべきだった3つのこと** | 施設の本当の顔 / 夜にある / 88日で出た · `74歳が見た夜勤の数` |
| 6 | 70歳を過ぎた女性が男を探す本当の理由…**78歳の私を救った3つの条件** | 71歳の条件は / 恋ではない / 朝7時半の電話 · `生きてる証を確かめ合う` |
| 11 | 通帳の残高は絶対に教えてはいけません…**81歳に教わった「うちの地図」の中身** | 通帳は見せない / 息子が泣いた / 母が渡したもの · `73歳 元惣菜屋の決断` |
| 19 | 山歩きサークルは猟場でした…**60を過ぎた男が絶対に近づいてはいけない4つの型** | 「いい猟場よ」 / 鏡越しに / 聞いた言葉 · `兄は850万円を失った` |

<!-- export a3cda1862e52 · 2026-09-26 -->
