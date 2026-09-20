# QUY TRÌNH KỊCH BẢN GỌN (`script.flow = "lean"`) — v2, ĐÃ CODE + TEST 2026-09-20

**Trạng thái:** đã code (`pipeline/lean_script.py` ~520 dòng · `make_video.py::b3_lean/kiem_lock` · `gate_common.ghi_lock/kiem_lock`
· `qc_script_sol.run(extra_note)` · lens `plain` có SÀN MỨC ĐỘ · `ai_steps._pass1_prompt(budget_block)`). Lane G bật `flow="lean"`.
Hồi quy: Lane E (không khai flow) chạy y nguyên; lane cũ không có lock → `kiem_lock` chỉ WARN.

**Test thật nửa sau trên ep01 (bản đã có 7 điểm Sol FIX):**
| Lượt | Diễn biến | Số đo |
|---|---|---|
| chạy 1 (lens plain CHƯA có sàn) | S3 sạch → Sol FIX 7 → Fable patch (đổi 4% đoạn, đúng từng điểm) → S3 sạch → Sol FIX 6 → patch (4%) → Sol FIX 4 → **ESCALATE** đúng luật, `ESCALATION_REPORT.md`, lock state ESCALATE, bench ghi | 7,7' · Fable 2 · Sol 3 · 6.764→7.112 chữ |
| chẩn đoán | Fable patch chuẩn; **Sol không hội tụ**: mỗi lần đọc lại tìm điểm nhỏ hơn, lượt 3 chê chính chữ lượt 2 yêu cầu. Lens plain không có sàn mức độ (đúng memory `cong-llm-phai-dat-duoc`) | — |
| sửa | PLAIN_TMPL thêm **[NẶNG]/[VỪA]/[NHẸ]** + luật: PASS = 0 NẶNG và <3 VỪA; NHẸ → góp ý thêm, không tính | — |
| chạy 2 (có sàn) | S3 sạch → Sol **PASS** lần 1 (0–1 VỪA, 3–4 góp ý) → **LOCK** sha `59d3f6bfc0` | 43s · Sol 1 · 0 patch |
| kiểm khoá | sửa 1 chữ trong script.txt → `kiem_lock` = **FINAL_QC_STALE FAIL**; khôi phục → PASS | — |
Lặp Sol có sàn 3 lần trên cùng bản → PASS cả 3 (điểm VỪA khác nhau mỗi lần nhưng đều <3) → sàn cho hội tụ thật.

**Bench (bench.jsonl):** ep01 nửa sau: `patch_count 2 · sol_calls 3 · ESCALATE` (trước sàn) → `sol_calls 1 · PASS · 43s` (sau sàn).
**Tập 2 `ep02-1000yen-shumi` — chạy TRỌN từ S1 (đo S2 viết đúng ngân sách):**
| Mốc | Kết quả |
|---|---|
| S2 Fable viết đúng ngân sách | **6.580 chữ / mục tiêu 6.474 = +1,6%** (luồng cũ: +36% rồi nén) · 426s · thoại 27% · S3 sạch, 0 patch máy |
| Vòng Sol lần chạy 1 | FIX 2 NẶNG (hạng 1 phá điều kiện mentor · hạng 1 không phải "sở thích" vs tiêu đề) → patch → FIX 2 NẶNG mới (radio/TV đạo cụ · title chưa trả) → patch → FIX 1 NẶNG (110×4=600円) → **ESCALATE** đúng luật, 15,6' |
| Lỗ hổng máy lộ ra | phép CỘNG tổng tiền không ai bắt (qc_numbers chỉ có phép nhân) → thêm `_tong_tien` (Σ khoản 円 trong đoạn vs 総額/合計, lệch >15%) — test bắt được 600 và cả lỗi 440 của em |
| Lớp 3 đọc ESCALATE | sửa tay 3 điểm Sol lần 3 (lock state ESCALATE → được phép) → chạy lại: S3 bắt 440円 không có trong SỐ ĐƯỢC PHÉP → patch máy → Sol **PASS** → LOCK (2'34) |
| Lớp 3 đọc bản khoá | phát hiện 2 lỗi LANE Sol không thể biết: CTA bị Sol dời xuống cuối (luật §3.6 giữa video) · 1 câu mentor bám gốc 73% bigram → **S3 nay coi CTA giữa 40–65% là VIỆC** (không phải warn), Sol được báo luật lane trong extra_note; thêm kênh `viec_tay.txt` để lớp 3 đưa việc vào vòng patch thay vì sửa tay |
| Chạy lại | mở lock (ESCALATE có lý do) → S3 2 việc → 1 patch (đổi 4% đoạn: điều kiện thành ẩn dụ 工程表, CTA @49%) → Sol PASS (1 VỪA) → **LOCK sha 84beda216e** · 7.185 chữ (+11%) · 3'03 |
Quan sát: mỗi patch Fable +100–300 chữ → sau 3 patch tổng lệch +11% (vẫn trong 12% của gate cũ, vượt 8% budget). Cân nhắc S3 báo DÀI theo budget tol.
Tổng máy tập 2: ~21' (3 lần chạy) + S1 tra tư liệu ~12'. Bench 3 dòng ở `ep02/bench.jsonl`.

**BENCHMARK 10/10 TẬP Lane G — xong 2026-09-20 tối (tất cả LOCK PASS, sheet D = `Done`):**
| Tập | Chữ | Lệch % | Lần chạy | ESCALATE | Fable | Sol | Patch | Phút máy |
|---|---|---|---|---|---|---|---|---|
| ep01 | 7.112 | +9,9 | 2 | 1 | 2 | 4 | 2 | 8 |
| ep02 | 7.185 | +11,0 | 3 | 1 | 6 | 5 | 4 | 21 |
| ep03 城下町 | 6.673 | +3,1 | 4 | 3 | 9 | 7 | 7 | 31 |
| ep04 夕方の習慣 | 6.575 | +1,6 | 2 | 1 | 5 | 4 | 3 | 16 |
| ep05 夫婦 | 6.131 | −5,3 | 2 (viết lại 1) | 1 | 8 | 4 | 4 | 23 |
| ep06 散歩道 | 6.933 | +7,1 | 5 (viết lại 1) | 4 | 13 | 6 | 9 | 42 |
| ep07 台所 | 6.427 | −0,7 | 3 | 1 | 5 | 4 | 3 | 18 |
| ep08 歩き方 | 6.528 | +0,8 | 1 | 0 | 4 | 2 | 2 | 13 |
| ep09 図書館 | 6.100 | −5,8 | 1 | 0 | 4 | 3 | 2 | 14 |
| ep10 日帰り温泉 | 6.915 | +6,8 | 1 | 0 | 4 | 3 | 2 | 20 |
Tổng 206' máy (chạy 2–3 tập song song → ~2h đồng hồ) · 60 lượt Fable · 42 lượt Sol · S1 tra tư liệu tay ~8×10'.
So tiêu chí §8: PASS 0–1 patch ở lần chạy đầu = 3/10 (ep08/09/10 — 3 tập cuối sau khi vá) → CHƯA đạt 80%; |lệch| ≤8% = 8/10 ✓; 0 STALE ✓; median phút máy/tập 19' ✓.
**Vá trong ngày làm 3 tập cuối chạy 1 lần PASS:** (a) trần patch = max(1,05×, trần ngân sách) — ep03 2 patch tốt bị từ chối oan vì 6.585 > 6.561; (b) máy tự xoá câu lặp nguyên văn (ep03 tốn 1 patch chỉ để xoá 1 câu); (c) S3 kiểm theo budget ±8% (ep07 lock −11,5% lọt vì gate cũ 12%); (d) prompt viết: "viết NGẮN cũng là lỗi" + mỗi mục ≥0,9×moi_muc (3/6 bản đầu thiếu 11–26%); (e) `script_qc.lane_rules` cho Sol biết quy ước tiêu đề「0円/1円も使わず」 của kênh (ep06 3 vòng Sol chê vì logic thuần); (f) viec_tay.done rename trùng tên (Windows) → đánh số; (g) bridge báo cả stdout khi exit≠0 (cảnh báo settings.json che mất lỗi).
**Bài học S1 (hồ sơ) — nguồn ESCALATE lớn nhất:** ctx viết "gợi ý" thì Fable đi hướng khác tiêu đề (ep05 3/5 mục không phải vợ chồng; ep06 第1位 = 川沿い không có tên) → phải ghi **BẮT BUỘC** 5 mục khớp tiêu đề; tiêu đề hứa gì (夫婦/若返る/1円) thì ctx phải nói cách trả. Fable trong patch có thể đưa địa danh MỚI kèm số trùng SỐ ĐƯỢC PHÉP (ep10 城崎 800円) → máy không bắt được, lớp 3 phải soi địa danh lạ và bổ nguồn.



> v1 (sáng 20/09) ra sau khi test tập 1 Lane G: 12 lượt LLM, 4 lớp QC xen kẽ, lỗi cuối sinh SAU khi sol
> chấm. v2 (chiều 20/09) tiếp thu bản phản biện anh gửi — **đồng ý toàn bộ 4 điểm khoá** và thêm 1 rủi ro
> thứ 3. Nguyên tắc chốt một câu:
>
> **Fable viết → máy bắt lỗi cơ học → Sol bắt lỗi nội dung → Fable patch tối đa 2 lần → mọi patch đều chạy
> lại máy + Sol → Sol PASS cuối cùng → khoá SHA256 → tuyệt đối không ai sửa script nữa.**
>
> Phần A (quy trình cũ đo thật) giữ nguyên ở cuối file để đối chiếu.

---

## 0. Bốn điểm khoá từ phản biện — em nhận gì, sửa gì

| # | Phản biện | Nhận? | Đưa vào thiết kế thế nào |
|---|---|---|---|
| 1 | **Sau Sol chỉ ra lỗi → Fable sửa → PHẢI quay lại máy + S3 + Sol lần nữa**; không có "Sol FAIL → sửa → S3 PASS → DONE" | ✅ Đây là lỗi thật của v1 (S5 viết "FIX → S4 → S3 → sol lần 2" nhưng chưa nói rõ *mọi* patch, và chưa có khoá sau PASS) | §2 vòng PATCH: mỗi patch = Fable sửa → FACT+S3 → Sol re-QC. Không có nhánh tắt. |
| 2 | **Không cho Fable "tự cắt địa văn" tự do** → compression pass có ràng buộc (MUST PRESERVE / PREFER CUTTING / không viết lại toàn bài) | ✅ v1 viết "Fable tự cắt địa văn" là nới quá — nén cũng là chỗ sinh lỗi (Gemini đã chứng minh) | §3 prompt nén ràng buộc, có số chữ phải cắt tính từ S3, danh sách bảo toàn, danh sách ưu tiên cắt, trần/sàn bridge |
| 3 | **Máy kiểm thứ máy kiểm được; Sol chỉ kiểm thứ máy mù** — không tốn Sol hỏi "đủ 8.000 chữ chưa" | ✅ Trùng hướng S3, nhưng v1 chưa kê rạch ròi | §4 bảng phân công máy ↔ Sol; prompt Sol nói rõ "độ dài/số mục/số liệu máy đã kiểm — đừng lặp" |
| 4 | **DỪNG phải có trạng thái**: PASS / ESCALATE / BLOCK; ESCALATE sinh `ESCALATION_REPORT.md`, pha asset bị chặn; không "chạy tiếp" | ✅ v1 chỉ nói "DỪNG báo người" — chưa đủ để máy sau không lấy nhầm bản | §5 trạng thái + `script.lock.json`; B5W/B5/B7… đọc trạng thái này, không phải `script.txt` tồn tại là chạy |
| + | Rủi ro thứ 3: **patch sửa lỗi Sol chỉ ra nhưng sinh lỗi mới chỗ khác** → Sol pass cuối vẫn bắt buộc | ✅ Chính vì vậy #1 là bắt buộc, không phải tối ưu | §2, §7 |
| + | Gemini không bỏ khỏi hệ thống, chỉ **cấm chạm master script**; giữ cho việc phụ rẻ (phụ đề, map ảnh↔câu, phân loại, dịch) | ✅ Đúng — B5 prompt ảnh/thumbnail/analyzer vẫn Gemini | §4 |
| + | Bigram chỉ là gate phụ, không đo chất văn | ✅ | S3 xếp bigram là WARN → dòng việc cho Sol tham khảo, không tự chặn |
| + | 12–18' chưa là fact → benchmark 10 tập với bộ số đo cố định | ✅ | §8 |

Một chỗ em **giữ ý khác** nhẹ: phản biện đặt FACT GATE trước S3 như 2 khối; trong code em gộp làm **một hàm
đo tất định** chạy một lần (cùng đầu vào, không LLM, thứ tự không ảnh hưởng kết quả) — nhưng **báo cáo tách 2
mục** FACT / LENGTH-STRUCTURE để người đọc thấy rõ. Không khác về bản chất.

---

## 1. SƠ ĐỒ LUỒNG v2

```
S1  HỒ SƠ            Claude Code tab: competitor.txt + series_ctx.txt (SỐ ĐƯỢC PHÉP + URL)      0 LLM
S1Q HỒ SƠ ĐỦ CHƯA    máy: series_ctx có ≥1 [Dn] + URL mỗi dòng · SỐ ĐƯỢC PHÉP có · competitor ≥3.000 chữ
                      · cùng dạng đếm với tập → thiếu = BLOCK ngay, chưa tốn Fable                  0 LLM
S2  VIẾT              Fable: khung (giấu gốc) → viết ĐÚNG NGÂN SÁCH từng phần                        2 LLM
S3  ĐO TẤT ĐỊNH       máy: [FACT] số/địa danh/năm ↔ tư liệu · nhất quán tên/tuổi/tiền trong bài
                      [LENGTH-STRUCTURE] chữ · phẩy · hơi · thoại · 、(tự gỡ) · N mục · outro (tự thay)
                      · CTA vị trí · đoạn trùng · mở đầu · bigram(WARN)                              0 LLM
      └─ trượt → PATCH(n) ── n<2 ──┐            n≥2 → ESCALATE
S4  SOL QC            sol, lens theo lane; prompt nói rõ máy đã kiểm gì                              1 LLM
      ├─ PASS → LOCK: script.lock.json {sha256, sol_pass_at, patches, metrics} → xong
      ├─ FIX  → PATCH(n) ── n<2 ──→ S3 → S4 (Sol re-QC, BẮT BUỘC) ──→ PASS → LOCK │ FIX/REMAKE → …
      └─ REMAKE lần 1 → ESCALATE ngay
PATCH(n) = Fable sửa ĐÚNG danh sách (S3 hoặc Sol), ràng buộc §3, trần 1,05×; ghi script.pre_patch{n}.txt
ESCALATE = ghi ESCALATION_REPORT.md + script.lock.json{state:"ESCALATE"} + BLOCK pha asset; không "chạy tiếp"
```

Đếm: điển hình 3–4 lượt LLM (khung · viết · Sol; +1 patch +1 Sol nếu FIX); xấu nhất 7 (khung · viết · 2 patch
· 3 Sol). Thứ tự bất biến: **mọi lần văn bản đổi → S3 → Sol**. Sau LOCK không bước nào ghi `script.txt`.

---

## 2. VÒNG PATCH — quy tắc cứng
1. Patch chỉ nhận **danh sách việc có vị trí** (trích câu / số đoạn) từ S3 hoặc từ Sol. Không nhận "làm hay hơn".
2. Sau MỌI patch: S3 lại (0đ) → còn lỗi cơ học → patch tiếp (tính lượt) hoặc ESCALATE; sạch → **Sol re-QC**
   (tốn 1 lượt, chấp nhận — đây là giá của "Sol là lời cuối").
3. Tối đa **2 patch** cho cả vòng (không phải 2 cho S3 + 2 cho Sol). Patch thứ 3 = ESCALATE.
4. Fable patch phải trả **toàn văn** (để S3 đo được) nhưng bị ép "chỉ đổi những chỗ nêu": bridge đo thêm
   **tỉ lệ đoạn thay đổi** (diff theo đoạn) — >40% đoạn đổi ở patch "sửa 3 câu" = từ chối bản patch, giữ
   bản trước, ghi lỗi `patch_qua_tay`.
5. Sau Sol PASS: ghi `script.lock.json` = `{state:"PASS", sha256, at, sol_report, patches:n, metrics}`.
   `NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS` — mọi bước sau (B5W prompt ảnh, B5P, B7, drive_handoff…) gọi
   `gate_common.kiem_lock(slug)`: sha256(`script.txt`) ≠ lock → `FINAL_QC_STALE = FAIL`, dừng. Tái dùng
   `gate_common.sha256_file` + cơ chế `artifact_meta.json` đã có (memory `p0-buoc1-gates`), chỉ thêm 1 file lock
   + 1 hàm kiểm.

---

## 3. PROMPT NÉN/PATCH CÓ RÀNG BUỘC (thay "Fable tự cắt")
Sinh từ số đo S3, ví dụ S3 báo `ACTUAL 7.120 / TARGET 6.474 ±8% → OVER 646`:

```
NHIỆM VỤ: rút ngắn 650–800 chữ (không tính xuống dòng). KHÔNG viết lại toàn bài — chỉ cắt/gọn tại chỗ.
PHẢI GIỮ NGUYÊN: mọi con số/địa điểm/thông tin thực tế · trình tự thời gian · quan hệ nhân–quả · các bước ngoặt
cảm xúc · mục cuối (cú lật) và kết/payoff · câu thoại ngắn đối đáp · câu CTA · câu outro nguyên văn.
ƯU TIÊN CẮT THEO THỨ TỰ: (1) giải thích lặp lại · (2) cảm xúc tả hai lần · (3) câu chuyển đoạn dư · (4) tả cảnh
trang trí · (5) câu tu từ lặp. Cắt đều — không xoá trọn 1 mục.
OUTPUT: toàn văn kịch bản sau khi cắt, không giải thích.
```
Ràng buộc máy đi kèm: `min_chars 0,90× · max_chars 1,05×` (hoặc đúng khoảng mục tiêu khi nén) · đoạn đổi ≤40%
(nén thì ≤70%) · FACT gate phải **không mất** số nào so với bản trước (so tập hợp số/địa danh trước–sau).
Cùng khuôn cho patch theo Sol: "SỬA ĐÚNG các điểm sau (trích câu) — mọi thứ khác giữ nguyên".

---

## 4. PHÂN CÔNG MÁY ↔ SOL ↔ FABLE ↔ GEMINI

| Việc | Ai | Ghi chú |
|---|---|---|
| Độ dài · phẩy/câu · chữ/hơi · thoại % · 、cắt cụm (tự gỡ) · outro nguyên văn (tự thay) · N mục đủ/đúng thứ tự · CTA trong 40–65% · đoạn trùng · bigram lặp/bám gốc (WARN) · sót Hàn/Latin · marker lọt · kết bằng dấu câu · mở đầu dài/suông | **Máy** | tái dùng `ai_steps.check/go_cat_cum`, `qc_script.mechanical/_bigrams/mo_dau` |
| Số có đơn vị · mốc năm · địa danh hành chính ↔ `SỐ ĐƯỢC PHÉP`/series_ctx · **tên nhân vật/tuổi/số tiền cá nhân nhất quán trong bài** (cùng tên → cùng tuổi; số tiền không đổi giữa đoạn) · nguồn [Dn] đủ URL | **Máy** | tái dùng `qc_facts.chi_tiet_thieu_nguon` (bỏ katakana) + hàm nhỏ mới `nhat_quan_noi_bo` (regex tuổi/tiền theo tên) |
| Fingerprint · lock SHA256 · stale | **Máy** | `gate_common` |
| Logic chuyện · nhân–quả · động cơ nhân vật · tình tiết vô lý · mâu thuẫn ngầm (dòng thời gian kể vs kể lại) · pacing · tone theo lane · câu tiếng Nhật không tự nhiên · diễn giải dữ kiện sai ý · ending/payoff trả đúng lời hứa tiêu đề · nguy hiểm mà máy mù | **Sol** (`lens` theo lane: E `medical` · F/G `plain`) | prompt mở đầu: "Máy đã kiểm độ dài/số mục/số liệu khớp tư liệu — đừng lặp; tập trung vào tính hợp lý." Đo thật ep01 lens plain: 7 điểm logic thật, 0 điểm ảo |
| Viết · nén có ràng buộc · patch tại chỗ | **Fable** (duy nhất chạm master) | `claude -p --tools ""` CLI ≥2.1.251 |
| Prompt ảnh (B5W) · map ảnh↔câu · phụ đề · phân loại · dịch · channel_analyzer | **Gemini** (ngoài luồng master) | **cấm ghi `script.txt`**; đọc thì được |

---

## 5. TRẠNG THÁI KẾT THÚC — 3 giá trị, ghi `script.lock.json`

| state | Khi nào | Hệ quả |
|---|---|---|
| `PASS` | Sol PASS (lần 1, hoặc sau patch ≤2) và S3 sạch ở cùng bản | sha256 khoá; pha asset được chạy; sheet D = `script-qc` |
| `ESCALATE` | patch 2 vẫn FIX · Sol REMAKE · S3 không nắn được sau 2 patch · patch bị từ chối 2 lần | ghi `ESCALATION_REPORT.md` (bản nào, lỗi gì còn, 2 patch đã thử gì, gợi ý người quyết); **pha asset BLOCK**; sheet D = `escalate` + K lý do; Claude Code báo anh |
| `BLOCK` | S1Q trượt (hồ sơ thiếu) · hạ tầng (Sol/Fable lỗi mạng, JSON hỏng) | không tốn lượt viết; báo đúng thứ thiếu |

Không có trạng thái thứ 4 kiểu "PASS có điều kiện / chạy tiếp". `make_video.py` pha asset (B5W…) mở đầu bằng
`kiem_lock()`: không có lock hoặc state ≠ PASS hoặc sha lệch → dừng với lý do.

---

## 6. NGÂN SÁCH VIẾT (S2) — đo từ kênh mẫu, khai trong profile
`script.budget = {"mo_dau": 0.22, "ket": 0.08}` (phần còn lại chia đều N mục). Với 6.474 chữ: Hồi 1+2 ≈ 1.420 ·
5 mục ≈ 800/mục · kết ≈ 520 · dung sai ±8%. Prompt ghi từng số tiếng Nhật + "không có bước cắt phía sau — viết đúng
độ dài". Lệch >8% → PATCH nén/nới có ràng buộc (§3), tính là 1 patch.
Giả thuyết cần đo: Fable viết đúng ±8% được bao nhiêu % tập. Nếu <50% thì sửa prompt writer (thêm ví dụ đếm
đoạn), **không đưa Gemini nén trở lại**.

---

## 7. RỦI RO — 3 cái, cách đo
1. Fable không tự ra đúng độ dài → đo `final_char_deviation` + `patch_count` (§8). 
2. Bigram thô → chỉ WARN, Sol đọc kèm; nếu 10 tập không có ca "bám gốc" nào bị Sol/anh bắt mà bigram im → bỏ.
3. **Patch sinh lỗi mới chỗ khác** → chính là lý do Sol re-QC sau mọi patch + diff đoạn ≤40% + FACT so trước–sau.

---

## 8. BENCHMARK 10 TẬP — ghi `bench.jsonl` mỗi tập, 1 dòng
`slug · total_time_s · fable_calls · sol_calls · patch_count · s3_fail_count · sol_fail_count ·
final_char_deviation (%) · final_state · manual_intervention (bool + ghi chú) · cost_vnd (sol) · lens`.
Tiêu chí thắng: ≥80% tập PASS với 0–1 patch; median total_time ≤20'; |deviation| ≤8% ở ≥70% tập; 0 ca
FINAL_QC_STALE. Không đạt → sửa prompt writer/patch, không thêm model.

---

## 9. ĐƯA VÀO CODE (hàng rào #2 — lane khác không đổi hành vi)
- Profile khai `script.flow="lean"` (+ `script.budget`); không khai = luồng cũ y nguyên. Lane G thử trước, Lane F
  sau khi đạt, Lane E chờ anh (giữ `lens=medical`, `sol_qc` không tắt).
- File mới `pipeline/lean_script.py` (~300 dòng): `s1q_ho_so()` · `ngan_sach()` · `viet()` · `do_tat_dinh() → (metrics,
  viec_fact[], viec_len[])` · `patch(text, viec, kieu)` (nén/sửa, ràng buộc §3, diff đoạn) · `sol_qc()` · `lock()` /
  `escalate()`. Trong `make_video.py`: `b3_script` rẽ nhánh khi `flow==lean`; các bước cũ B3Q/B3F/B3S/B3R/B3G ghi
  `skipped:"lean_flow"`; **B5W trở đi thêm `kiem_lock()`** (áp cho MỌI lane: lane cũ không có lock → chỉ WARN để
  không gãy; lane lean → FAIL).
- `gate_common.py` thêm `ghi_lock()/kiem_lock()` (20 dòng, dùng `sha256_file` sẵn).
- Test hồi quy: 1 tập Lane E cũ `--den B3G --dry-run` không khai flow → log/state y hệt.
- Thử thật: **tập 1 Lane G chạy nửa sau** (bản hiện tại đã có Sol plain FIX 7 điểm → PATCH → S3 → Sol re-QC → LOCK
  hoặc ESCALATE) để kiểm vòng patch; rồi **tập 2** chạy trọn từ S1 để kiểm S2 ngân sách. Ghi 2 dòng `bench.jsonl` đầu.

---

## A. QUY TRÌNH CŨ — đúng như `make_video.py` đang chạy (đo thật ep01, giữ để đối chiếu)

| # | Bước | Model | Chạm văn bản | Đo thật ep01 |
|---|---|---|---|---|
| A0 | Hồ sơ | Claude Code + K3 + WebSearch | — | ~10' |
| A2 | B3 PASS 0 khung | Fable | — | 72s |
| A3 | B3 PASS 1 viết, xin ≥1,3× | Fable | VIẾT | 8.830 chữ (+36%) |
| A4 | B3 PASS 2–3 nén khúc | Gemini | SỬA | 6.954; lượt 1 xoá thoại 26→8% |
| A5–6 | tách câu / hạ thoại | Gemini | SỬA | — |
| A7 | GATE | máy | — | lượt 1 trượt vì 1 dấu 、 → viết lại từ đầu |
| A8 | B3Q chấm + sửa | Gemini | SỬA | 3 lỗi vừa |
| A9 | B3F | máy | — | bỏ qua (mode=story) |
| A10 | B3S sol ×2 + Fable sửa | sol/Fable | SỬA | lens medical nhầm → +1.100 chữ y tế, rơi dữ kiện |
| A11 | B3R Fable ×3 | Fable | SỬA | 「再会」nêu không sửa |
| A12 | B3G nén + hạ thoại | Gemini | SỬA ×2 | **đảo nghĩa 6000/8000歩 SAU sol** |
| A13 | đọc tay | Claude Code | 2 câu | bắt lỗi A12 |

12 lượt LLM · 6 sửa toàn văn đổi tay · 4 lớp QC · không lời cuối · ~31' máy. Lỗi sinh ở A4, A10, A12.
