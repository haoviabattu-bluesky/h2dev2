# CÔNG THỨC WIN — Lane M `teinengo-anaba` (BẮT BUỘC cho MỌI tập mới)

> ⛔⛔ **Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá** (6 thành phần / kiểu A/B/C hook / hook 10 nhịp / câu đầu = thoại / mẫu hook ep05 — tất cả bỏ). File này nay CHỈ là công thức CHỌN ĐỀ (mục 1) + THÂN BÀI (mục 3); hook KHÔNG chấm theo file này. Tập không có xung đột thật thì KHÔNG bịa cảnh bị coi thường; 第7位 (hạng 7) trước phút 4.

> ⛔ **16/10/2026 anh chốt: kịch bản Lane M BUỘC theo công thức này.** Mỗi tập mới: sau B3G, TRƯỚC khi giao máy 3 → chạy máy kiểm (mục 0) + chấm phần "kiểm bằng mắt". Có mục ❌ → vá qua `viec_tay.txt` (patch_model, sửa tại chỗ, KHÔNG viết lại, KHÔNG sửa tay `script.txt`) rồi kiểm lại tới khi ĐẠT. Đề không qua mục 1 → DỪNG, báo anh đổi đề.
> Lịch sử: bản đầu 14/10 (ep05+ep06, báo cáo máy 2 `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_PHAN_TICH_LANE_M_NHOM_WIN_2026-10-14.md`) · cập nhật 16/10 bằng số YouTube Studio 10 tập + đọc 12 kịch bản (mục 0B).
>
> **Đã nạp vào máy** — `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\teinengo-anaba.json`:
> `script.cong_thuc_win` (máy kiểm) · `script.structure_block` (khuôn thân bài)
> · `script.soat_gptweb.rang_buoc` · `script_qc.lane_rules` (Sol bắt FIX).

## 0. KIỂM 1 TẬP (bắt buộc, chạy sau B3G)

```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kiem_cong_thuc_win.py --profile teinengo-anaba --slug <slug tập>
```
In từng mốc ✅ ĐÚNG / ❌ CHƯA + **cách sửa**, rồi danh sách "kiểm bằng mắt". Mã thoát 1 = chưa đạt → không giao máy 3.
Đối chứng đã chạy 16/10: ep05 ĐẠT · ep06 ĐẠT · ep10 CHƯA (4 mốc) · ep12 CHƯA (mở bằng tóm tắt, thiếu nhịp im lặng).

| # | Phải có | Máy đo? | Chưa có thì sửa thế nào |
|---|---|---|---|
| 1 | ~~(16/10 bỏ bắt buộc — nay: nỗi đau dẫn về VIỆC LÀM sau 60)~~ **ĐỀ**: chính 田島 bị công ty HẠ GIÁ VÌ TUỔI bằng 1 con số bị mất (tái tuyển 再雇用 bị hạ điều kiện · bị cắt ca 18→11 ngày · mất tiền vì hiểu sai luật lương hưu) | mắt | Đổi đề, hoặc bọc: người có quyền với 田島 nói câu hạ giá + con số. Không bọc được → báo anh đổi đề |
| 2–5 | ~~(17/10 XOÁ — luật viết hook cũ: câu đầu = thoại, số trong 3 câu đầu, cấm mở kiểu…, hook 10 nhịp)~~ Hook (21/10) bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`, không chấm ở bảng này | — | — |
| 6 | **Cấp trên TRẺ HƠN**, chỉ nhìn tablet/màn hình; cuối tập lộ ra bị tổng công ty ép rồi **xin lỗi** | mắt | Thêm 1 cảnh cuối (~85–92%) cấp trên nói thật + xin lỗi; lạnh, không ác, không パワハラ (bắt nạt nơi làm việc) |
| 7 | **1 người CÙNG TUỔI chọn NGƯỢC** 田島 (ở lại / chịu đựng) | mắt | Dùng 小野寺 (Onodera) hoặc đồng nghiệp cũ, 「正解は、ひとつじゃない」 (không có một đáp án đúng duy nhất) |
| 8 | **So kè đủ 3 cặp**: ở lại vs ra đi · số trước vs sau · chữ trên giấy tờ vs thực tế | mắt | Thêm cảnh giấy tờ (労働条件通知書 – giấy báo điều kiện lao động, 「シフトによる」 tuỳ theo ca) đối với thực tế |
| 9 | **Cung cảm xúc**: nhục → lo (tiền, 春江 + 家計簿 sổ chi tiêu) → ~38–40% bị gọi QUAY LẠI → ~55–60% từ chối BÌNH TĨNH → 第1位 (hạng 1) được trân trọng | máy (mốc) + mắt | Thiếu nút giữa bài → thêm cuộc gọi 「今年だけ戻っていただけませんか」 (năm nay thôi ông quay lại được không) |
| 10 | A/B/C + コメント ở 40–50% + hứa 「俺の答えは、最後に言う」 (tôi sẽ nói câu trả lời ở cuối); 第1位 72–82%; trả lời A/B/C ≥88% | máy | Dời mốc theo dòng "sửa" máy in |
| 11 | **Kết cân bằng**: không ai thắng, VẪN CÒN 1 mất mát thật (tiền/ngày không lấy lại được) | mắt | Thêm 1 câu con số không lấy lại được ở 90–95% (vd 「戻らない5万8千円」 5,8 vạn yên không về lại) |
| 12 | Gói đăng (khi anh mở lại title): chuyện TIỀN lên title/thumbnail; chữ/số trên thumbnail PHẢI có trong kịch bản | mắt | Lỗi đã gặp: ep09 thumbnail 「5つ」 (5 cái) trong khi kịch bản 7 việc; ep07 có chữ không có trong kịch bản |

## 0B. SỐ STUDIO 16/10 (10 tập đã đăng — cơ sở của công thức)

| Tập | View | CTR | Kết luận |
|---|---|---|---|
| ep05 từ chối gia hạn tái tuyển (再雇用) | 9.600 | 4,4% | Thắng #1, 191 giờ xem |
| ep06 bị cắt ca, thu nhập bấp bênh | 3.900 | 3,5% | Thắng #2, có ngày 14.255 lần hiển thị |
| ep09 hiểu sai luật lương hưu → cắt ca người khác | 1.600 (55 giờ) | 7,4% | Đang lên, chưa có số giữ chân |
| ep02, ep03, ep04 (buổi sáng, ít giao tiếp, dậy sớm) | thấp | — | Thua: đề sở thích/tính cách, không ai lấy mất gì của nhân vật; ep02 CTR 24h 2,4% |

Ngách thắng: **người 60+ bị công ty hạ giá vì tuổi bằng một con số bị mất, rồi chọn giữ phẩm giá.**
Bình luận gần như không có (cả kênh ~10) → "tương tác" đo bằng like, giữ chân, thời gian xem. 10 tập = xu hướng mạnh, chưa phải luật tuyệt đối → **đo lại khi kênh có ~15 tập**.
Báo cáo gốc 16/10 (máy phân tích Studio): `BAO_CAO_WIN_LANE_M_2026-10-16.md` — chưa đồng bộ về máy 1 lúc ghi file này; nội dung chính đã chép vào đây.

## 1. CHỌN ĐỀ (kiểm TRƯỚC khi lập hồ sơ tập)

### LUẬT 3 YẾU TỐ (14/10/2026) — ⚠️ 16/10 hạ thành ƯU TIÊN: thiếu yếu tố 1 → vẫn làm đề nếu nỗi đau dẫn về việc làm sau 60, KHÔNG bịa cảnh bị coi thường

| # | Yếu tố | Mức | Ví dụ win |
|---|---|---|---|
| 1 | **Bị KHINH THƯỜNG**: chính 田島 bị công ty/nơi làm việc coi nhẹ — bị thay bằng người trẻ/hệ thống, bị cắt ca/lương, bị dời chỗ, kinh nghiệm bị gạt | **BẮT BUỘC** — thiếu = KHÔNG làm đề này | dời chỗ ra cạnh phòng tài liệu (ep05) · nhường ngày cho 牧 28 tuổi (ep06) · 38 năm chỉ được tô vàng dòng bằng lái (ep08) |
| 2 | **Quyết định có TỰ TRỌNG**: lặng lẽ, không giận, không đắc thắng | Ưu tiên (phải có trong kịch bản) | 「更新は、しません」 (tôi không gia hạn) · gấp tờ lịch làm lại |
| 3 | **Mất mát bằng CON SỐ** | Ưu tiên (phải có trong kịch bản) | lương giảm · 18→11 ngày · 年金まで2年 (còn 2 năm mới có lương hưu) |

Cách kiểm: đọc tựa + hồ sơ đề → chấm 3 yếu tố. Yếu tố 1 ❌ → DỪNG, báo anh đổi đề hoặc bọc lại (người khinh thường phải là người có quyền với 田島, KHÔNG phải nhân vật phụ; kịch bản KHÔNG được tự gỡ kiểu 「嫌われたのかと思った。違った。」 (tưởng bị ghét, hoá ra không phải)). Yếu tố 2/3 thiếu → bổ sung trong hồ sơ `promise.txt`/`series_ctx.txt` trước khi chạy B3G.

`Người 60–65 bị nơi làm việc COI NHẸ` + `1 MẤT MÁT đo bằng con số` + `1 QUYẾT ĐỊNH có tự trọng` → `7 việc ngoài kia`

| Ưu tiên | Đề |
|---|---|
| ✅ Win | lương/quyền lợi/chỗ ngồi bị cắt sau 再雇用 (tái tuyển dụng) · bị người trẻ/hệ thống thay · kinh nghiệm không được công nhận ngoài công ty · công ty cũ quay lại nhờ mà không trả vị trí · ở lại hay rời đi (A/B/C) |
| ⚠️ Gần win | "bẫy tiền" (thu nhập không ổn định, tiền đi lại) — CHỈ win khi có NGƯỜI gây bất công; chỉ là phép tính = rơi về trung bình |
| ❌ Loại | danh sách lọc theo 1 điều kiện lịch/thể chất không xung đột: 週3日・午前だけ (3 buổi sáng), 接客少なめ (ít tiếp khách), 朝2時間/早起き (dậy sớm), 座って働ける (ngồi làm) thuần. Chỉ quay lại khi bọc trong cảnh bị coi nhẹ |

## 2. HOOK — Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.
(Hook 10 nhịp ep05 / kiểu A/B/C / mẫu `docs\hook_mau\teinengo-anaba_ep05_win.txt` không còn là luật.)

## 3. THÂN BÀI — 7 mục đan với mạch truyện song song (mốc = % số chữ kịch bản)

| Mốc | Nút bắt buộc | ep05 |
|---|---|---|
| ~8–12% | Cảnh 春江 (Harue) + 家計簿 (sổ chi tiêu) + giới thiệu 緑のノート (sổ xanh) | 「全部、見せて」 |
| ~38–40% | Người gây bất công QUAY LẠI / biến cố mới → vòng treo | Sudo gọi: 「今年だけ戻っていただけませんか」 điều kiện 「前と同じで」 |
| ~42–47% | Câu A/B/C + 「コメントで教えてください」 + 「俺の答えは、最後に言う」 (tôi sẽ nói câu trả lời ở cuối) | A ở lại / B ra ngoài dùng kinh nghiệm / C việc mới |
| ~55–60% | Cao trào cảm xúc: quyết định tự trọng, không trả thù | gọi lại từ chối, để sổ hướng dẫn ở 「三段目の引き出し」 (ngăn kéo thứ ba) |
| ~76–80% | 第1位 TRẢ ĐÚNG lời nhá ở hook | 「待ってたの」 |
| ~95% | Trả lời A/B/C + hỏi lại khán giả + cảm ơn + outro | 「俺は、Bだった」 |

Mỗi mục = 1 thẻ cố định trong sổ xanh: tên việc · thời gian/điều kiện có nguồn · thể lực · ưu điểm · cạm bẫy · ai hợp/không hợp — **và 1 cảnh thật** (đi xem chỗ làm, 1 câu thoại của người ở đó).
Nhân vật phụ theo chức năng: 柳瀬 (Yanase, quầy tư vấn — câu hỏi xoay chuyển 「守りたいのは、席ですか。仕事ですか」 ông muốn giữ chỗ ngồi hay công việc) · 小野寺 (Onodera, đồng nghiệp ở lại — 「正解は、ひとつじゃない」 không có một đáp án đúng duy nhất).

## 4. BẢNG KIỂM NHANH 1 TẬP (máy đo vị trí — chạy sau B3G)

Đếm % số chữ của: `第7位` lần đầu (≤8–9%) · câu A/B/C (42–47%) · `最後に言う/話す` (đi kèm A/B/C) · `第1位` (76–80%) · trả lời A/B/C (≥90%).
Script đo mẫu đã dùng 14/10: tìm regex `第(7|七)位`, `第(1|一)位`, `最後に(言う|話す)`, `コメント` trong `script.txt`, chia vị trí cho tổng số chữ.
