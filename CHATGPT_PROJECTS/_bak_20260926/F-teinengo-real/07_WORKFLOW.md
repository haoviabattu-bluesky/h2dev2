# 07 WORKFLOW — F-teinengo-real

> Lane `teinengo-real`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# LANE `teinengo-real` (tab `F-teinengo-real`) — sinh bởi `lane-init` 2026-09-24

**Thumbnail: Trạng thái: PILOT — chưa khoá** — khuôn `config/lanes/teinengo-real.thumb.yaml` sinh từ DNA (`docs/lanes/teinengo-real/thumb/research/thumb_dna.json`), mô-típ ở `docs/lanes/teinengo-real/thumb/TEMPLATE.md`.

**Tiêu đề: ĐÃ CÓ LUẬT (chốt 2026-09-24)** — `title_rules` trong `config/lanes/teinengo-real.json` (file 02_TITLE_RULES của Project ChatGPT). Dòng "chưa có luật" cũ đã lỗi thời.

## 1. Kênh · sheet · thư mục

| | |
|---|---|
| Kênh mẫu | https://www.youtube.com/channel/UCRkP44Mcw-K8IktdTqxC9dg |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep<nn>-<slug>` |
| Giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real\ep<nn>-<slug>` |
| Sheet | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` tab **`F-teinengo-real`** (cột khớp dòng: TODO — xem `sheet_match` lane gần nhất) |
| Config | `config/lanes/teinengo-real.json` + `config/lanes/teinengo-real.thumb.yaml` |

## 2. Lệnh

```bash
py -3.13 -X utf8 cli.py thumb --slug <ep> --profile teinengo-real        # pilot thumbnail (tốn gpti2)
py -3.13 -X utf8 cli.py lane-lock --profile teinengo-real               # sau khi thumb-publish tập pilot
```

## 3. Nhật ký

- 2026-09-24: lane-init từ DNA đo 2026-09-24 (nền `teinengo-tanoshimi`).

---
## BAO_CAO_AP_DUNG_TAI_SAO_2026-09-25.md

# BÁO CÁO — Lane F teinengo-real: làm lại tiêu đề/thumbnail/tags theo VIDEO GỐC (2026-09-25)

Theo `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\GIAO_VIEC_LANE_F_AP_DUNG_TAI_SAO_2026-09-25.md`.

## Video gốc từng tập (từ `VIDEO_GOC.json`, độ chắc `chac_chan`)
| Tập | Video gốc | Nhóm | Đã đọc TAI_SAO.md + our_eps |
|---|---|---|---|
| ep01 | XbwqD2SktC0 【漫画】60歳で定年退職した男…5年後、65歳まで働いた同僚との差に絶望しました | THẮNG ~5.900/ngày | ✅ — lấy khuôn T6 (2 mốc tuổi + so đồng nghiệp + 差 giấu điều gì), H5 (dải đen 2 màu, 2 panel tương phản, mỗi panel 1 nhãn+1 bong bóng); bỏ K3 (không chép nguyên câu 「同僚との差に絶望」→ đổi 愕然, không chép cụm bong bóng của họ) |
| ep02 | e_Zo7Ht5OH8 【漫画】60歳で会社を辞めた元部長…退職金1700万円でも絶望しました | **THUA** ~170/ngày | ✅ — lấy khuôn cấu trúc (tuổi+quyết định+でも+kết cục, dải đen 2 màu, 2 nhãn trước/sau, bong bóng kiêu hãnh↔nhẫn nhịn); **KHÔNG lấy** số 退職金 lớn và vai 元部長 hẹp khán giả (2 nguyên nhân thua chính theo mục "Vì sao thắng/thua") — đổi số tiền lớn → 給料半分 (đúng cốt truyện thật), đổi 元部長 → 俺 chung chung, đổi 1 người trước/sau → 2 người (真壁/日高) vì kịch bản mình thật sự có 2 nhân vật song song |
| ep03 | _VXUim2J9QM 【漫画】60歳で辞めるな！62歳で年金受給が最強な理由 | THẮNG ~1.450/ngày | ✅ — lấy khuôn H5 (dải đen 2 màu, before/after, 2 nhãn tuổi-quyết định/mốc thời gian, bong bóng vui→sốc); **không lấy** "最強な理由" (kịch bản mình là câu chuyện regret khi繰上げ sớm, không phải lời khuyên nên chọn tuổi nào — dùng T6 khác: bí ẩn con số + 本当の代償, giữ tinh thần "vế sau giấu lý do") |

## Tiêu đề: cũ → mới

| Tập | Tiêu đề CŨ | Tiêu đề MỚI |
|---|---|---|
| ep01 | 【漫画】60歳で退職した俺と働き続けた妻…5年後、夫婦の月収に8万円の差が出た理由 | **【漫画】60歳で退職した男…5年後、65歳まで働いた同僚との差に愕然としました** |
| ep02 | 【漫画】60歳で再雇用に残った俺と断った同期…1年後、多くを失ったのはどっちだったか | **【漫画】60歳で再雇用を選んだ俺…給料ほぼ半分でも1年後に分かった本当の理由** |
| ep03 | 【漫画】63歳で年金を繰り上げた男…減ったのは月2万円だけじゃなかった本当の理由 | **【漫画】63歳で繰り上げた俺…読んでいない注意書きに書かれていた本当の代償** |

Đã khoá qua `s3_lock_title.lock()`, đã qua QC ChatGPT web 1 vòng (sửa: ep02 "給料半分"→"給料ほぼ半分" vì script thật 30万→17万 ≈56,7%, không phải đúng 50%; ep03 sửa quan hệ nghĩa "注意書きが代償になった"→"注意書きに書かれていた代償" vì cái giá thật là lựa chọn tương lai mất đi, không phải tờ giấy). ep01 đổi từ góc VỢ (do research cũ) sang góc ĐỒNG NGHIỆP 日高 — khớp với `hook/hook_locked.txt` đã dựng vào video (繰上げ/日高) và khớp gần như nguyên văn video gốc XbwqD2SktC0.

## Thumbnail

Khuôn engine đã NÂNG CẤP hôm nay: `thumbnail_engine/bands_manga.py` giờ hỗ trợ **2 nhãn (lead_left/lead_right) + 2 bong bóng (quote_left/quote_right)** — trước đây engine chỉ vẽ được 1 nhãn + 1 bong bóng (dùng cho lane G), không đúng mô-típ thật của lane F (mỗi panel có RIÊNG 1 nhãn + 1 bong bóng). Đã đối chiếu trực tiếp ảnh gốc `K8tTrxijqEo/O84L0zOtrxo/ZogHjPo8cX0` (full-res) để chỉnh màu chữ (trắng+vàng viền ĐEN dày, không phải vàng viền trắng nhạt như bản 24/09) + bố cục cận mặt.

| Tập | Link Catbox | Bố cục |
|---|---|---|
| ep01 | https://files.catbox.moe/p4by0v.png | Top「どっちが幸せ」(vàng: 幸せ) · trái 俺 cận mặt cà phê nhãn「60歳で退職」bong bóng「自由を語った」· phải 日高 cận mặt hành lang văn phòng nhãn「65歳まで勤務」bong bóng「税金は？」(NGUYÊN VĂN) |
| ep02 | https://files.catbox.moe/g5bhg5.png | Top「同期は断った」(vàng: 断った) · trái 真壁 mũ vàng cận mặt bong bóng「お願いします」(NGUYÊN VĂN) nhãn「同じ月に定年」· phải 日高 cận mặt thoải mái bong bóng「俺は課長だぞ」(NGUYÊN VĂN) nhãn「自分の形」 |
| ep03 | https://files.catbox.moe/v8cogf.png | Top「2度のはい」(vàng: はい) · trái quầy lương hưu bong bóng「はい」nhãn「一度目は金額」· phải nhân viên chỉ tay vào giấy bong bóng「知らなかった」nhãn「二度目は注意書き」 — bám sát nguyên văn câu mở hook_locked.txt |

Opus chấm cả 3 lần (9 ảnh) và chọn biến thể **C** cho cả 3 tập (đọc ảnh trực tiếp, không cache).

## Tags: cũ → mới

| Tập | Số tag cũ | Số tag mới | Cấu trúc |
|---|---|---|---|
| ep01 | 43 tag (tool T v3 tự lấy từ video đối thủ) | **19 tag** | 3 tag gốc kênh (老後,年金,お金) đứng đầu + 16 tag ChatGPT web mở rộng từ tóm tắt kịch bản |
| ep02 | 38 tag | **19 tag** | như trên |
| ep03 | 30 tag | **20 tag** | như trên |

Đã ghi cột F (Sheet). Không dùng lại bước `cli.py tags` (T v3) theo đúng giao việc — tag lấy tay từ 3 tag gốc + ChatGPT mở rộng.

## Đã publish

Sheet tab `F-teinengo-real`: cột E (tiêu đề), F (tags), G (link Catbox), K (trạng thái) — cả 3 dòng đã cập nhật.
`TIEU_DE_MO_TA.txt` + `thumbnail.png` đã chép đè vào `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real\<ep>\`.

## ⚠️ CẦN ANH KIỂM LẠI — ep01 và ep02 CÓ THỂ ĐÃ ĐĂNG
Cột K ghi "CẦN THAY" cho cả ep01 và ep02 (khác "CẦN ĐĂNG" của ep03) — nghĩa là 2 tập này **đã được đặt lịch/đăng trước đó** với tiêu đề và ảnh bìa CŨ (ep01 có ghi chú hôm qua "ĐÃ ĐẶT LỊCH ĐĂNG VÀO 17:30 ngày 24/9"). Tiêu đề/ảnh MỚI hôm nay đã ghi vào Sheet + CHANEL nhưng **KHÔNG tự sửa video đã đăng trên YouTube Studio** — anh cần vào Studio đổi lại tiêu đề + ảnh bìa cho khớp bản mới, hoặc bảo em giữ nguyên bản cũ nếu không muốn đổi video đã lên lịch.

## Việc còn tồn (không thuộc phạm vi giao việc hôm nay)
- Cổng `qc_goi_dang.py` (G1 lời hứa, G3 câu nghi thức) vẫn còn vài cảnh báo — đã ghi `goi_dang_ok.txt` trong từng thư mục tập kèm bằng chứng cụ thể (câu thoại/hook thật chứng minh ý đã giữ, chỉ khác cách diễn đạt ngắn gọn của nhãn/bong bóng so với câu promise dài).
- `hook/hook_locked.txt` ep01/ep02 vẫn thiếu câu nghi thức 「そう思っていた」 của kênh — đã báo từ 24/09, là việc bên h2dev sửa hook, không phải việc tiêu đề/thumb/tags.

---
## PHUONG_AN_TIEU_DE_MO_TA_TAGS_THUMB_2026-09-24.md

# Lane F `teinengo-real` (tab `F-teinengo-real`) — Kiểm hồ sơ + PHƯƠNG ÁN tiêu đề · mô tả · tags · thumbnail

Ngày 2026-09-24 · Chỉ nghiên cứu, CHƯA sửa file nào của h2dev, CHƯA ghi Sheet, CHƯA tốn tiền.
Kênh mình: 定年後のリアル `@teinengo-real` · Kênh mẫu: 老後の暮らし研究所 https://www.youtube.com/channel/UCRkP44Mcw-K8IktdTqxC9dg

## 0. Đã đọc những gì (đường dẫn thật)

| Nguồn | Đường dẫn | Dùng cho |
|---|---|---|
| Cửa vào lane | `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-real.md` | định danh, trạng thái, luật cứng |
| Handoff research (đã duyệt 13/09) | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneF_from_research\LANE_F_HANDOFF.md` | công thức tiêu đề §4, hook §5, 7 chặng §6, tên/tag §12 |
| Ảnh 6 thumbnail top kênh mẫu | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneF_from_research\data\thumb_老後の暮らし研究所.png` | khuôn thumbnail |
| **title_intel (BẮT BUỘC)** | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\teinengo-real.json` | 5 công thức F1–F5, 6 cặp thắng/thua, 8 nguyên tắc, `our_eps` ep01–03 |
| Audit hook/tiêu đề/thumb | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\HOOK_AUDIT_LANE_EFG.md` (phần Lane F, dòng 458–680) | lỗi từng tập |
| Profile h2dev | `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\teinengo-real.json` (`thumbnail`, `publish`, `goi_dang`) | `listing_external:true` = tiêu đề/mô tả/thumb do dự án NÀY làm |
| Hook đã khoá (24/09 08:2x, repair mode) | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep0{1,2,3}-*\hook\hook_locked.txt` + `hook_lock.json` | lời hứa 30 giây đầu |
| Kịch bản + tóm tắt | `...\ep0N-*\script.txt`, `script_tomtat_vi.txt`, `title.txt` | đối chiếu lời hứa |
| Video đã dựng | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\video_render\teinengo-real\ep0{1,2,3}-*\final.mp4` (22–23/09) | trạng thái |
| Mô tả + tags thật 4 video thắng | tải bằng yt-dlp 24/09 (scratchpad `desc.json`) | khuôn mô tả/tags |
| Sheet | tab `F-teinengo-real` A1:K12 | ep01–03 D=Done, I có đường dẫn; E/F/G TRỐNG |

## 1. Hiện trạng — 7 phát hiện (xếp theo mức chặn)

1. **ep01: hook đã khoá KHÔNG khớp tiêu đề nào.** `hook_locked.txt` mở bằng 「六十二歳の秋…年金事務所の窓口で「はい」と二回言った…繰上げ」 +
   「六十歳で会社を出た俺と、六十五歳まで残った日高。どっちが幸せだったのか」 — 0 chữ về VỢ. Tiêu đề hiện tại (và `promise.title` trong
   `hook_lock.json`) nói 「働き続けた妻…夫婦の月収に8万円の差」; 3 tiêu đề research đề xuất (324万 / 妻の手取り / 2冊の通帳) cũng không có trong hook.
   Thêm nữa 「夫婦の月収に8万円の差」 là **sai bản chất** (so lương hưu gộp với lương thực nhận của vợ) — research đã bắt.
2. **ep01 và ep03 có hook gần như TRÙNG:** cả hai mở bằng 「年金事務所の窓口で、はいと二回/二度言った」 + 繰上げ + 「俺と…同期」. Đăng liền nhau người xem
   thấy lặp ngay 10 giây đầu. Một trong hai phải viết lại hook (đề xuất: ep01, vì ep01 còn lệch tiêu đề).
3. **Thumbnail trong profile h2dev ĐI NGƯỢC dữ liệu đo.** `profile.thumbnail.art_style` = ảnh người GẦN THẬT, 1 người cận mặt, nền tối, chữ bên trái,
   tầng đỏ 「絶望/残酷な現実」. Kênh mẫu 14/15 thumbnail = **dải đen trên + 2 panel manga bán thực + bong bóng chữ dọc + nhãn vàng**, không số tiền
   (0/4 video thắng có tiền), và 「残酷な現実」 thuộc nhóm thua. → Không dùng khuôn đó; khuôn thumb của lane phải dựng mới trong dự án này.
4. **Tiêu đề làm việc cả 3 tập dính kiểu thua:** ep02 「残酷な現実」 (chữ sốc trừu tượng, 0/4 thắng) + tiêu đề nói 元部下 còn hook nói 日高;
   ep03 「本当の後悔」 trừu tượng + va chạm video kênh mẫu mới đăng ZogHjPo8cX0 (cũng 繰上げ, cùng khuôn 'NN歳で年金を〜た男…').
5. **Chưa có gì cho lane này bên YT-TITLE-RESEARCH:** thiếu `config\lanes\teinengo-real.json`, `.thumb.yaml`, `docs\lanes\teinengo-real.md`, SOP, và
   `thumb_dna.json` (TRENDING chưa đo thumb kênh này). Chỉ có `title_intel\teinengo-real.json` ✓ → tool sẽ DỪNG nếu chạy ngay.
6. **Giao hàng chưa khớp Sheet:** cột I ghi `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real\ep0N-…\` nhưng thư mục `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real` **không tồn tại** trên máy 1
   (final.mp4 chỉ nằm ở `...\video_render\teinengo-real\`). Và hook clip (khoá 24/09) chưa ghép vào final.mp4 (dựng 22–23/09).
7. Nhỏ: Sheet B3 vẫn ghi 「61歳で再雇用」 trong khi `title.txt` đã sửa 60歳.

## 2. Luật gói đăng lane F (rút từ dữ liệu — tham khảo linh hoạt, không cứng)

**Tiêu đề** — khuôn chung `【漫画】{tuổi}で{quyết định}した{男/俺}…{mốc thời gian}、{ẨN SỐ}`; thân 23–41 ký tự, 1 lời hứa, chữ số (60歳, 2万円).
- Vế sau PHẢI là câu hỏi chưa trả lời: 差 / 本当の理由 / どっちだったのか / N選 đếm thật. Kiểm: che vế đầu, vế sau còn là câu hỏi không? (thắng 4/4, kể-kết-cục ≤200/ngày)
- Số trên tiêu đề = số MẤT nhỏ-vừa của người thường (67万, 2万). CẤM số 退職金 lớn ≥1.500万 (0/4 thắng, 4/4 có đều ≤766/ngày).
- Tránh chữ sốc làm kết: 残酷な現実 / 衝撃の現実 / 末路. Tránh nhóm hẹp: 独身 / 元部長 / 非課税 / 繰下げ70.
- Không chép tiêu đề hit kênh mẫu; khung F1 (so 2 người) không dùng 2 tập liền (hook cả 3 tập đã dùng khung này).
- Ba chỗ cùng một lời hứa: tiêu đề · chữ thumbnail · 30 giây hook đã khoá.

**Mô tả** — khuôn kênh mẫu (4/4 video thắng giống nhau):
1 đoạn 300–450 chữ: câu mở = tiền đề + số nhỏ + loại trừ lời giải dễ → tên/tuổi/nghề nhân vật → chuỗi từ khoá tự nhiên (退職金、年金、再雇用、老後資金、定年後の生活…)
→ 「ぜひ最後までご覧ください」 → câu hỏi mời comment (「あなたなら何歳で…？」) · rồi 「関連動画↓」 + link video của MÌNH (có từ tập 2 trở đi) · rồi 3 hashtag.
Thêm 1 câu minh bạch như mô tả kênh: 「登場人物は架空ですが、数字は実在の制度に基づいています。」 (an toàn chính sách cho nội dung tiền/chế độ).
Hashtag: kênh mẫu `#年金 #老後 #老後資金`; profile đang `#定年 #老後 #年金 #退職 #60代` → đề xuất 3 cái `#年金 #老後 #定年`.

**Tags** — kênh mẫu chỉ gắn 3 tag chung 老後/年金/お金 (không có tín hiệu) → chạy **bước T TAG v3** như các lane khác (lấy từ video đối thủ thật qua InnerTube/Data API),
nguồn cấu hình `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\teinengo-real\lane_profile.yaml` (đang `draft:true` — anh cần duyệt 1 lần).
Seed từ profile: 定年退職, 老後 生活, 年金 生活, 退職金, 60代 貯金, 再雇用, 孤独 老後, 老後 お金, 漫画 + từ khoá riêng tập (繰上げ受給, 再雇用 給料…).
Category: kênh mẫu để **Entertainment** (handoff ghi People & Blogs) — đề xuất theo kênh mẫu.

**Thumbnail** — khuôn đo từ ảnh thật:
- Dải đen trên cùng, 1 dòng 4–9 chữ: cụm người xem tự áp vào mình (「65歳で定年退職」「貧乏になるお金の使い方」), 1 từ khoá vàng/đỏ + phần trắng. Không chép nguyên tiêu đề, thêm 1 góc khác tiêu đề.
- Dưới: 2 panel manga bán thực (trước/sau cùng 1 người, HOẶC 2 lựa chọn song song), mỗi panel 1 ông 60+ + bong bóng oval trắng chữ DỌC ≤5 chữ (lời nội tâm)
  + nhãn vàng viền đen ở đáy (tuổi / lựa chọn / N年後…).
- Không số tiền. Mặt nhân vật lấy từ master REF của tập (`...\ep0N-*\_ref\`, `_ref2\`) để khớp nhân vật trong video.

## 3. Phương án từng tập (đã đọc our_eps ep01–03: lấy gì, bỏ gì, vì sao)

> **Bản sửa 24/09 chiều sau khi đọc tài liệu hook h2dev gửi + chạy thử cổng `qc_goi_dang.py` (xem §6).** Bảng dưới đã thay bảng đầu.
>
> **✅ CHỐT ep01 = phương án B (góc vợ)** — anh giao Claude quyết 24/09. Hook sửa từ ứng viên 2 (154 chữ) qua cổng 0 chặn;
> phiếu việc gửi h2dev: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\GIAO_VIEC_HOOK_EP01_LANE_F_2026-09-24.md`. Thứ tự đăng: ep02 → ep03 → ep01.

| Tập | Tiêu đề (đã qua cổng thử) | promise.txt (1 câu) | Chữ thumbnail (thumb_text) | Cổng qc_goi_dang (thử trong scratchpad) |
|---|---|---|---|---|
| **ep02** `ep02-saikoyou-hanbun` | 【漫画】60歳で再雇用に残った俺と断った同期…1年後、多くを失ったのはどっちだったか | 再雇用に残った俺と断った同期、1年後にどっちが多くを失っていたのか。 | 再雇用か、断るか / 1年後 / どっちが失った？ / 再雇用に残る / 断った同期 | còn 1 chặn: hook thiếu câu nghi thức 「そう思っていた」 (việc của h2dev) |
| **ep03** `ep03-kuriage-koukai` | 【漫画】63歳で年金を繰り上げた男…減ったのは月2万円だけじゃなかった本当の理由 | 減ったのは月2万円だけだと思っていた繰り上げの「はい」が、何を手放したのか。 | 繰り上げの「はい」 / 減ったのは月2万円だけ？ / 読んでない… / 63歳で繰上げ / 半年後… | **0 chặn** (WARN) |
| **ep01** `ep01-fuufu-nenkin-sa` — phương án A (giữ hook đã khoá, 0 đồng) | 【漫画】60歳で会社を出た俺と65歳まで残った同期…5年後、どっちが幸せだったのか | 60歳で会社を出た俺と65歳まで残った同期、5年後にどっちが幸せだったのか。 | 60歳か65歳か / 税金は？ / もう自由だ / 60歳で会社を出た俺 / 65歳まで残った同期 | còn 1 chặn: thiếu 「そう思っていた」 (h2dev) |
| ep01 — phương án B (góc VỢ, cần h2dev khoá lại hook) | 【漫画】60歳で辞めた俺と働き続けた妻…2年半後、並べた2冊の通帳の差に後悔しました | 60歳で辞めた俺と働き続けた妻、並べた2冊の通帳の差に俺は後悔した。 | 2冊の通帳の差 / もう自由だ / 決めた / 60歳で辞めた俺 / 働き続けた妻 | Với hook ứng viên 2 (đã có sẵn): 3 chặn — lời hứa chỉ nói 35% trong 45s, câu mâu thuẫn ở giây 236, thiếu 「そう思っていた」. Với hook đang khoá: lời hứa 16% trong 45s. |

Đã bỏ (cổng chặn): ep03 「…月2万円より高くついた本当の理由を病院で知った」 (hook không nói 「高くついた」 trong 45s đầu), ep03 「…減額率の下の1行…」 và
「…注意書きで失った本当のもの」 (G5: không treo ẩn số hoặc lõi >44), ep01 「…1年で通帳から324万円消えた本当の理由」 (324万 chỉ nói tới giây ~165), ep02 「…本当に負けていたのは…」 (lõi 46).

**ep01 — cân nhắc A và B:** A qua cổng và không tốn gì, nhưng: (1) ep01 và ep02 cùng khung F1 「俺と同期…どっち」 và cùng tên 同期 日高; (2) hook ep01 vẫn
trùng cảnh mở của ep03 (quầy 年金事務所, 「はい」 hai lần); (3) gần cơ chế tiêu đề hit XbwqD (khác chữ — G8 cho phép). B đúng cảnh mạnh nhất tập và góc riêng của kênh,
nhưng h2dev phải khoá lại hook (TTS ≈25–32đ + clip Grok 0đ + 1–3 lượt Sol).
Thứ tự đăng nếu chọn A: ep02 → ep03 → (một tập khác) → ep01, để F1 không liền nhau và hai hook trùng không đứng cạnh nhau.

**ep04–ep10 (chưa viết kịch bản) — sửa đề tài TRƯỚC khi viết, rẻ nhất lúc này:** ep08 「退職金1500万円が3年で消えた」 và ep10 「割増退職金2000万円…2年後の現実」 dính 2 kiểu thua cùng lúc
(số 退職金 lớn + kể kết cục/chữ trừu tượng); ep07 「独身」 và ep05 「妻を亡くした」 là nhóm hẹp; ep04 「98万円消えた」 kể kết cục → đổi sang 「…消えた本当の理由」.
Đây là việc bên h2dev (tên tập ở Sheet cột B) — chỉ báo, không sửa.

## 4. Kế hoạch dựng lane trong YT-TITLE-RESEARCH (5 bước)

| # | Việc | Lệnh / file | Chi phí |
|---|---|---|---|
| 1 | Config lane: sao `teinengo-tanoshimi.json`, `sheet_tab=F-teinengo-real`, `sheet_match` theo cột C (đường dẫn tập), `slug_root=E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real`, `deliver_root=E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real`, `title_rules` = mục 2 ở trên, thân 23–41, bắt buộc 【漫画】 | `e:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\config\lanes\teinengo-real.json` + `docs\lanes\teinengo-real.md` + SOP `docs\lanes\teinengo-real\SOP_TIEU_DE_THUMBNAIL_2026-09-24.md` | 0 |
| 2 | Thumb DNA: nhờ TRENDING đo máy kênh mẫu (hoặc `--dna-draft` từ mục 2, bị `lane-lock` chặn tới khi đo thật) | `py -3.13 -X utf8 e:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\cli.py lane-init --profile teinengo-real --dna <thumb_dna.json> --from-lane teinengo-tanoshimi` | 0 LLM |
| 3 | Pilot 1 tập (ep02): tiêu đề + mô tả + tags + 3 ảnh thumb, xem XEM.html | `py -3.13 -X utf8 e:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\cli.py lane-pilot --profile teinengo-real --slug E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep02-saikoyou-hanbun` | Fable/Opus (quota) + gpti2 ~3–6 ảnh |
| 4 | Anh chọn → publish + khoá khuôn | `cli.py thumb-publish` / `sheet-publish` (E/G/K) / `tags --write` rồi `cli.py lane-lock --profile teinengo-real` | Catbox 0 |
| 5 | ep03 chạy `run`; ep01 chờ h2dev làm lại hook | `py -3.13 -X utf8 e:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\cli.py run --slug E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep03-kuriage-koukai --profile teinengo-real` | như bước 3 |

Tiêu đề chốt phải đưa ngược sang h2dev (`title.txt` + `promise.title` của `hook_lock.json`) để cổng 3 chiều hook↔title↔thumb của `qc_final.py` không báo lệch.

## 5. Cần anh quyết

1. ep01: đồng ý **làm lại hook** theo góc 2 cuốn sổ của vợ (đề xuất), hay giữ hook 日高 và đổi tiêu đề theo hook (nhưng sẽ trùng ep03 và gần tiêu đề hit XbwqD)?
2. Thumbnail: bỏ khuôn "ảnh gần thật 1 người" trong profile h2dev, theo khuôn 2 panel manga của kênh mẫu — đồng ý?
3. Cho làm bước 1 (config + SOP, 0 đồng) ngay; bước 3 pilot ep02 (tốn quota + gpti2) chờ anh gõ.
4. Việc máy 2: thư mục `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real` chưa có dù cột I đã ghi — kiểm lại giao hàng.

## 6. Bổ sung 24/09 — tài liệu hook h2dev gửi và cách đã áp vào tiêu đề

**h2dev gửi gì liên quan lane F** (không có file riêng gửi YT-TITLE-RESEARCH; lane F chưa có `HOOK_TAP.md`/`promise.txt` như kenko ep01):
| File | Nội dung dùng cho tiêu đề |
|---|---|
| `E:\CLAUDE\YOUTUBE\h2dev\docs\QUY_TAC_GOI_DANG.md` | Luật G1–G8: 1 lời hứa (`promise.txt`) phải có ở tiêu đề · chữ thumbnail · câu đầu mô tả · 45 giây đầu lời đọc; vế tiêu đề/thumbnail phải có trong script; tiêu đề treo ẩn số, lõi 26–44 ký tự (đo từ kênh mẫu lane F) |
| `E:\CLAUDE\YOUTUBE\h2dev\pipeline\qc_goi_dang.py` + `profile.goi_dang` của `teinengo-real` | cổng máy 0 đồng: `contradiction_max_s 17`, `title_core_max_s 30`, `promise_window_s 45`, nghi thức 「そう思っていた」, `title_core_len [26,44]` |
| `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_H2DEV_HOOK_2026-09-23.md` | lane F: 11 phát hiện gói đăng; `script.hook.enabled` + cổng S1L (tập mới phải có `promise.txt`) |
| `E:\CLAUDE\YOUTUBE\h2dev\docs\QUY_TAC_VIDEO_HOOK.md` + `...\shared\GIAO_VIEC_MAY2_ep01_HOOK_2026-09-24.md` | hook là clip Grok đè HÌNH 0–35s, giữ tiếng — lời hook là lời 30s đầu thật của video |
| `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep0{1,2,3}-*\hook\hook_candidates.txt` + `hook_sol_report_*.txt` | 3 ứng viên hook/tập. ep01 **ứng viên 2 chính là cảnh 2 cuốn sổ của vợ** (có sẵn, chưa khoá); hook 1 ep01 được khoá dù Sol FIX×3 (“coi như PASS”) và Sol ghi rõ nó không khoá lời hứa tiêu đề |

**Cách đã áp:** dựng bản sao từng tập trong scratchpad (`script.txt` + `hook_locked.txt` thật, `title.txt`/`promise.txt`/`thumb_text.txt` thử), chạy
`py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\qc_goi_dang.py --slug <bản sao> --profile teinengo-real --no-log`, 5 vòng, 20 phương án.
Không sửa file nào trong `E:\CLAUDE\YOUTUBE\h2dev\`. Kết quả ở bảng mục 3.

**Bài học đưa vào công cụ lane F:**
1. Tiêu đề phải dùng lại CHỮ của 30s hook đã khoá (cổng đo phủ bigram trong 45s) → S2/S3 phải được đưa `hook_locked.txt`, không chỉ script.
2. Thumbnail phải có ≥40% chữ của lời hứa → thêm 1 dòng câu hỏi (「どっちが失った？」「減ったのは月2万円だけ？」), không chỉ bong bóng lời nội tâm.
3. Sau S3c chạy `qc_goi_dang.py` như một cổng (0 đồng); chặn → quay lại S3.

**Việc trả về h2dev (chỉ báo, không tự sửa):** ghi `promise.txt` (3 câu ở mục 3) · thêm 「そう思っていた」 vào hook ep01/ep02 (hook ep03 đã có) ·
cập nhật `promise.title` trong `hook_lock.json` khi tiêu đề chốt · ep01 quyết A/B.

<!-- export 7761cd709107 · 2026-09-26 -->
