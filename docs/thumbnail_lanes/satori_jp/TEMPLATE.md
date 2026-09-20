# THUMBNAIL TEMPLATE — LANE `satori_jp` (profile `satori-jp-obaa`)

**Trạng thái: HARD LOCK.** Chủ kênh duyệt 2026-09-17 trên tập 1 (`simbot2-01-vU5PWT2zLDs`):
"Tôi rất hài lòng với mẫu này." → bản đó là `MASTER_REFERENCE.png` (cùng thư mục).
File này quyết định **QUALITY BAR thị giác** của lane. **CONTENT do TITLE + DESCRIPTION của tập đang làm
quyết định.** `MASTER_REFERENCE.png` và `MASTER_REFERENCE_360.png` chỉ được dùng để học typography,
composition, visual mass và mức impact; tuyệt đối không copy wording, nhân vật, bối cảnh, đạo cụ, ánh sáng
cụ thể hay câu chuyện. Không xem thumbnail tập cũ hoặc Golden khi chưa được chủ kênh chỉ định rõ.

Thứ tự ưu tiên: **CURRENT STORY ACCURACY > LANE QUALITY BAR (file này + designated MASTER) > MODEL PREFERENCE.**

---

## 1. GEOMETRY (cấu trúc khoá, tọa độ không khoá)

| Mục | Giá trị khoá | Đo thật trên MASTER_REFERENCE |
|---|---|---|
| Khung | **16:9**, xuất 1280×720 | 1280×720 |
| Nhân vật chính | **Lớn ở khoảng 1/3 phải và hòa tự nhiên vào cùng scene toàn khung**; giữ REF identity, mặt lớn/rõ, không panel chữ nhật, không cutout halo. | user correction 2026-09-18 |
| Main text | **3 dòng dùng field riêng gần 2/3 trái**, khai thác gần hết safe space nhưng chừa gutter thật trước panel. Tăng context/twist khi yếu; không tăng HERO/banner nếu đã đủ authority. | user correction 2026-09-18 |
| Bottom banner | **BẮT BUỘC** (mục 3), gần full width | cao ≈140px, chữ ≈100px |
| Ảnh nền | **Một khung cảnh current-story liên tục phủ toàn canvas**; chữ đè trực tiếp lên scene. Cấm một bên đen thui/một bên portrait rõ, cấm panel tách đôi. Scene phía trái vẫn phải nhận ra ở 360px. | — |

## 2. TEXT STRUCTURE — HARD PRIORITY

### Quality reference: CONTENT × TYPOGRAPHY

Use `quality_reference/QUALITY_REFERENCE_CONTENT_TYPOGRAPHY_2026-09-19.md` as a reasoning
standard, never a pixel template. Before render, create and score at least three directions from
the current TITLE + DESCRIPTION/SCRIPT: A contradiction, B discovery/shock, C emotional
conflict/secret. Score story accuracy, specificity, stakes, curiosity, title complement, Japanese
naturalness and 1–2 second clarity. Winner must be highest-scoring and exactly match the rendered
rows/banner.

Do not weaken a concrete high-stakes event merely to shorten copy. Solve length with line breaks,
semantic hierarchy, safe BODY/HAND/PROP overlap and typography search. FACE remains hard-safe.
Banner must independently close/add the contradiction; generic labels such as `衝撃の真実`,
`まさかの結末`, `その理由とは？` are forbidden.

**Đơn vị đếm = VISUAL TEXT ROWS** — số hàng chữ **thực tế nhìn thấy** trên thumbnail đã render, KHÔNG phải
semantic block / số câu / số dòng trong `thumb_text.txt`.

```
3+1 PREFERRED = 3 hàng main text NHÌN THẤY + 1 hàng bottom red banner
4+1 FALLBACK  = 4 hàng main text NHÌN THẤY + 1 hàng bottom red banner
```
- Một câu tiếng Nhật về ngữ nghĩa là MỘT câu nhưng phải render thành 2 hàng → **tính là 2 MAIN TEXT ROWS**,
  vì nó chiếm 2 hàng và trực tiếp ảnh hưởng font size / senior readability.
- Mục tiêu cuối không phải "3 semantic blocks" mà là giữ thumbnail ở **3 VISUAL MAIN ROWS + 1 BANNER** để
  chữ có thể lớn nhất.
- **Không được dùng auto-wrap** (`--wrap`) để biến 3 block thành 4–5 visual rows rồi vẫn gọi là "3+1".
  Muốn xuống 3 rows thì phải **rewrite / nén Japanese copy một cách tự nhiên TRƯỚC khi render**.

Đây là cấu trúc mặc định của Satori vì: target = Japanese seniors · ít hàng hơn ⇒ typography lớn hơn ·
ưu tiên tốc độ đọc.

**Nếu draft ban đầu cần 4 VISUAL MAIN ROWS → BẮT BUỘC thử nén về 3 trước** bằng cách:
- bỏ từ thừa;
- bỏ thông tin title đã nói;
- chuyển emotional payoff xuống banner;
- gộp các ý có thể đọc liền trong MỘT hàng (vẫn phải vừa 1 hàng ở cỡ chữ lớn — 4–9 ký tự CJK);
- giữ strongest information;
- bỏ explanatory copy yếu.
Sau đó **Native Japanese QC lại** bản 3+1.

Nếu 3+1 vẫn giữ được: natural Japanese · meaning · story accuracy · strongest hook · curiosity
→ **PHẢI ưu tiên 3+1.**

**NHƯNG** nếu ép về 3 visual rows làm: Japanese không tự nhiên · sai nghĩa · mất contradiction / thông tin
thiết yếu · mất strongest hook · curiosity yếu đi đáng kể → **CHO PHÉP 4 VISUAL MAIN ROWS + 1 BANNER, và
ghi lý do trong QC** (mục 9, câu 7).

TUYỆT ĐỐI KHÔNG thêm một hàng chỉ để đạt số lượng hàng. Không bao giờ hy sinh CONTENT QUALITY chỉ để đạt
geometry. (Cả 3+1 lẫn 4+1 đều phải qua typography mục 4 — 4 hàng ⇒ chữ nhỏ hơn, đó là cái giá của fallback.)

## 3. BOTTOM RED BANNER — HARD LOCK

**BOTTOM RED BANNER = MANDATORY.** Là visual identity của kênh.
- Model có quyền quyết định **WHAT THE BANNER SAYS**.
- Model KHÔNG có quyền quyết định **WHETHER THE BANNER EXISTS**.
- Banner phải: gần full width · **đỏ mạnh, sạch, saturated** · không đỏ nâu/xỉn · không gradient trang trí
  không cần thiết · không viền màu làm rẻ/yếu khối · **text trắng rất lớn, đậm** · strong contrast.
- Vai trò tuỳ story: emotional payoff / secondary hook / final curiosity trigger. Không lặp ý đã có ở main text.
- **Câu banner draft yếu → VIẾT LẠI BANNER. Không được REMOVE banner.**
- `thumb_text.txt` luôn có dòng `BANNER|…`; thiếu = lỗi format, không phải lựa chọn.

## 4. SENIOR TYPOGRAPHY — HARD LOCK

Target: Japanese senior audience. **"Readable" KHÔNG đồng nghĩa "PASS". Phải so với MASTER_REFERENCE.**
- Main text **cực lớn**; lấp vùng chữ, không "đặt chữ trong vùng trống".
- **Fit từng dòng độc lập** (`--fit-each`): short line ĐƯỢC PHÉP phóng lớn hơn long line. Không dùng một base
  font nhỏ do dòng dài nhất quyết định làm tất cả dòng nhỏ theo.
- Không làm 3 dòng gần bằng nhau chỉ để “cân”; dòng ngắn/trigger quan trọng PHẢI được thử phóng vượt trội.
- Không ưu tiên poster/editorial sạch, nhiều margin, nếu cái giá là typography yếu. Satori ưu tiên impact.
- Khối chữ xếp **SÁT nhau** (trần khoảng dư `--gap-max 0.25`), không dàn đều xuống hết chiều cao.
- Giảm decorative negative space nếu diện tích đó dùng được để tăng chữ. **FONT SIZE > khoảng trống.**
- Banner text cực lớn; **không thu banner để "cân" với main text.**
- Giới hạn: **KHÔNG đè FACE** (mặt/mắt/mũi/miệng — xem phân loại HARD vs CONDITIONAL ở §4B, đây KHÔNG phải
  "không đè cả nhân vật/đạo cụ" như bản cũ — thân/tay/áo/đạo cụ chỉ được bảo vệ CÓ ĐIỀU KIỆN) · không chạm
  mép nguy hiểm · không cắt glyph · không phá câu tiếng Nhật.
- **Final QC phải xem cả full-size lẫn mobile preview (~360px).** Nếu text mới **nhỏ hơn MASTER_REFERENCE
  đáng kể mà vẫn còn diện tích an toàn → FIX.** Không PASS chỉ vì "vẫn đọc được".
- Viền chữ mỏng cố định 2px (khoá trong tool) — to = thân chữ to.

Số đo tham chiếu (MASTER_REFERENCE, 3+1): dòng 9 ký tự 78px · dòng 4 ký tự 196px · dòng 7 ký tự 100px ·
banner ≈100px. Tập khác có số ký tự khác ⇒ số px khác — **so VISUAL DENSITY** (tỉ lệ vùng trái được chữ lấp,
cỡ dòng nhỏ nhất ≈ ≥11% H), không so px tuyệt đối.

### 4B. PRE-PASS TYPOGRAPHY OPTIMIZATION — MAXIMUM EFFECTIVE TYPOGRAPHY (bắt buộc, tự chạy, TRƯỚC §9 Final QC)

**Thêm 2026-09-17, patch lại cùng ngày sau human review tập 6.** Bài học cần giữ lại KHÔNG PHẢI một con số
side-width/font-px/toạ độ của tập nào — mọi con số như vậy là kết quả CỦA RIÊNG ảnh tập đó, KHÔNG được lưu
làm chuẩn. Bài học là **QUY TRÌNH TỰ TÌM MAXIMUM EFFECTIVE TYPOGRAPHY cho chính ảnh đang làm**, chạy MỖI
TẬP, hoàn toàn tự động — Claude không được chờ human nói "chữ nhỏ quá" mới tối ưu.

**Mục tiêu:** 3 VISUAL MAIN ROWS phải LỚN NHẤT có thể trong composition thực tế, miễn vẫn giữ: tiếng Nhật
tự nhiên · semantic hierarchy · FACE sạch · subject nhận diện được · scene vẫn kể được câu chuyện · banner
đúng template. **READABLE ≠ OPTIMAL** — mục tiêu là LARGEST EFFECTIVE TEXT, không phải SMALLEST SAFE TEXT.

**Trigger:** ngay sau khi đã có final Japanese copy + background đã PASS nghiệm thu (§7) + đã xác định
bố cục 3+1 hoặc fallback 4+1 (§2) + vị trí subject đã cố định trong ảnh nền — **TRƯỚC KHI** coi Final
Visual QC (§9) là xong. Không được render một lần rồi PASS chỉ vì "đọc được".

#### 4B.1 Phân loại SAFE SUBJECT theo Ý NGHĨA THỊ GIÁC — không phải theo bounding box thô

Không được coi toàn bộ vùng subject là cấm địa cho chữ. Phân 2 loại:

- **A. HARD PROTECTED ZONE** — FACE: mắt, mũi, miệng, các chi tiết nhận dạng/biểu cảm thiết yếu. **Text
  TUYỆT ĐỐI không được xâm phạm vùng này**, ở bất kỳ candidate nào.
- **B. CONDITIONAL PROTECTED ZONE** — tay, thân, quần áo, đạo cụ, đồ nội thất/vật thể nền. **KHÔNG tự động
  là giới hạn của text.** Chỉ bảo vệ khi overlap thực sự: làm mất storytelling · làm một đạo cụ quan trọng
  không còn nhận ra được · làm subject khó nhận diện · hoặc làm bố cục xấu rõ rệt. **Overlap NHẸ lên thân/
  quần áo/tay/đạo cụ mà scene vẫn kể được và đạo cụ vẫn nhận ra → CHO PHÉP**, nếu đổi lại chữ to hơn đáng
  kể. Ví dụ: nhân vật cầm một vật trước ngực KHÔNG có nghĩa mép trái của vật đó tự động thành ranh giới
  phải của toàn bộ khối chữ.

Khi đo (xem `TOOL_NOTES.md` cho kỹ thuật pixel), luôn XÁC ĐỊNH TRƯỚC vùng đang chạm là (A) hay (B) —
chạm (A) ở bất kỳ mức nào = loại ngay; chạm (B) chỉ loại khi xét bằng mắt thấy thật sự phá 1 trong 4 điều
kiện ở trên, không loại chỉ vì "đã chạm bounding box".

#### 4B.2 Quy trình (SEARCH tự động, không áp 1 con số cố định)

1. Render candidate đầu tiên với subject nằm gọn trong tối đa 1/3 phải và `side_width` gần 2/3 trái — đây
   vẫn chỉ là **điểm xuất phát**, không phải kết quả typography cuối.
2. Inspect **full-size** rồi **360px**: right edge thực tế của TỪNG main text row · ranh giới HARD zone
   (FACE) · ranh giới CONDITIONAL zone (tay/thân/đạo cụ, ghi nhận nhưng KHÔNG coi là chặn cứng) · khoảng
   trống ngang/dọc chưa dùng.
3. Tự hỏi **NO WASTED SPACE RULE**: *"Có vùng trống ngang hoặc dọc đáng kể mà có thể dùng để tăng MAIN
   TEXT mà không làm hỏng face/story/composition không?"* — **YES → FIX, chưa PASS**, mở rộng
   `--side-width` (bước nhỏ +0.02 đến +0.04), render lại, đo lại, quay lại bước 2.
4. Nếu candidate đang xét CHẠM (B) CONDITIONAL zone: đừng loại ngay — xét bằng mắt xem storytelling/đạo
   cụ/composition có còn ổn không. Còn ổn → vẫn PASS được, tiếp tục thử to hơn nữa. Chỉ dừng optimize khi
   candidate tiếp theo thực sự: chạm (A) HARD zone, HOẶC phá (B) theo 1 trong 4 điều kiện ở 4B.1, HOẶC phá
   hierarchy/tiếng Nhật/banner.
5. Chọn **candidate lớn nhất còn thoả toàn bộ điều kiện** — ngay trước candidate bị loại ở bước 4.

**Banner không đổi:** bottom red banner vẫn HARD LOCK theo §3 — không đổi banner geometry chỉ để nhường chỗ
tăng main text. Search chỉ hoạt động trong vùng phía TRÊN banner.

#### 4B.3 Semantic hierarchy KHÔNG được giết font size của bất kỳ dòng nào

Hierarchy vẫn bắt buộc (§5) nhưng hierarchy **KHÔNG đồng nghĩa** `context = nhỏ, trigger = vừa, hook = lớn`.
Tạo hierarchy bằng **màu · vị trí · tương phản · cách chọn từ · viền · chênh lệch scale VỪA PHẢI** — không
phải bằng cách bóp một dòng xuống quá nhỏ. **Cả 3 MAIN ROWS vẫn phải có visual authority** — nếu một dòng
nhỏ/gầy hẳn so với 2 dòng còn lại khiến thumbnail trông yếu ở 360px → **FIX**, kể cả khi dòng đó đúng vai
"context". `:scale` (≤1) chỉ dùng để CÂN LẠI khi 1 dòng vô tình lấn át do ngắn hơn (bài học tập 2/3/6),
không dùng để chủ động thu nhỏ 1 dòng "vì nó là context".

#### 4B.4 So mật độ với MASTER_REFERENCE — TINH THẦN, không phải pixel

Trước khi chốt, mở **cả 4**: candidate full-size · candidate 360px · `MASTER_REFERENCE.png` ·
`MASTER_REFERENCE_360.png`. Tự hỏi bằng mắt: *"Typography của candidate có cảm giác mạnh, lớn, chiếm
không gian tương đương TINH THẦN của MASTER không?"* — so **mức độ táo bạo · mật độ chữ · khả năng tận
dụng không gian · readability cho senior**, KHÔNG so side-width/font-px tuyệt đối (mỗi ảnh có độ dài chữ,
tư thế, prop khác nhau — pixel khác nhau là bình thường).

#### 4B.5 Tự chạy — không chờ human nhắc, không phô bản thất bại

Đây là việc **Claude tự phát hiện và tự làm**, không phải chờ human nói "cho chữ to hơn"/"mở rộng sang
phải". Được thử nhiều candidate nội bộ trong lúc search; **human không cần xem từng candidate thất bại** —
chỉ giao **candidate tốt nhất** (kèm log ngắn gọn các mốc đã thử để có bằng chứng đã search, không cần mở
từng ảnh thất bại cho human).

#### 4B.6 FINAL GATE — 6 câu hỏi, PASS chỉ khi cả 6 đều đúng chiều

```
A. Có thể tăng MAIN TEXT thêm đáng kể mà FACE vẫn sạch không?                → phải NO
B. Có unused horizontal/vertical space đáng kể không?                        → phải NO
C. Có dòng main nào trông nhỏ/gầy rõ rệt so với các dòng còn lại không?       → phải NO
D. Có đang bảo vệ BODY/HAND/PROP một cách không cần thiết khiến chữ nhỏ không? → phải NO
E. Ở 360px typography có đạt visual impact gần tinh thần MASTER_REFERENCE không? → phải YES
F. Banner có đỏ mạnh, sạch, đủ lớn và có visual weight gần MASTER không?          → phải YES
```
A=YES hoặc B=YES hoặc C=YES hoặc D=YES hoặc E/F=NO → **chưa được PASS, optimize tiếp.** Chỉ khi cả 6 câu
đều đúng chiều (A-D = NO, E-F = YES) → Final Visual QC (§9) mới được PASS.

**Chống overfit (bắt buộc đọc trước khi ghi log):** TUYỆT ĐỐI không lưu side-width/font-px/toạ độ/khoảng
cách pixel/wording/vị trí nhân vật của MỘT TẬP CỤ THỂ làm chuẩn cho tập khác. Cái được lưu là QUY TRÌNH
QUYẾT ĐỊNH (4B.1-4B.6), không phải con số. Mỗi tập tự tìm lại geometry riêng từ đầu.

## 5. HIERARCHY & MÀU — guideline, KHÔNG mapping cứng theo số dòng

Mỗi dòng có một vai trò; màu và cỡ phục vụ hierarchy của **CURRENT STORY**:
- **HOOK chính** (hành động / phát hiện mạnh nhất) — thường ĐỎ, tận dụng gần hết bề ngang cột.
- **Information trigger** (con số / mốc thời gian / danh từ gây sốc) — thường VÀNG; dòng ngắn nên thường to
  nhất về px, điều này ĐƯỢC PHÉP.
- **Context / thiết lập nghịch lý** — thường TRẮNG; vẫn phải lớn, không trông như phụ đề.
- **Banner** = payoff / chốt hạ, không lặp ý.
- **KHÔNG hard-code** `Line 1 = WHITE, Line 2 = YELLOW, Line 3 = RED`. Thứ tự màu đổi theo vị trí của hook /
  trigger / context trong câu của tập đó. Chỉ tránh 2 dòng đỏ kề nhau làm hook mất nổi bật.
- Luồng đọc mục tiêu ≤ 2 giây: hook/trigger → context → banner → mặt nhân vật.

## 6. LỆNH RENDER (điểm xuất phát, không phải geometry toàn lane)

`profile.thumbnail` chỉ cung cấp điểm xuất phát. Lane Satori khóa `--side left --subject-side right`, còn
`side_width`/font vẫn phải search theo ảnh thật; ví dụ dưới đây KHÔNG phải geometry tuyệt đối cho mọi tập:
```
py -3.13 pipeline/thumbnail_text.py --bg <slug>/_thumb/001.png --text <slug>/thumb_text.txt --out <slug>/thumbnail_final.png --side left --side-width 0.60 --subject-side right --fit-height --fit-each --max-size 200
```
`thumb_text.txt`: 3 (hoặc 4 khi fallback) dòng `MÀU|text` + `BANNER|text`. Không dùng `:scale` >1 (fit-each tự
tính); `:0.x` chỉ để ghìm 1 dòng khi thật cần, KHÔNG dùng để bóp một dòng xuống mất "visual authority" (§4B
mục Hierarchy). Kỹ thuật tool: skill global → `TOOL_NOTES.md`.

> `side_width: 0.60` trong ví dụ là **điểm xuất phát**, KHÔNG phải giá trị
> chạy production cuối cùng cho mọi tập. Mỗi tập PHẢI chạy §4B (MAXIMUM SAFE TYPOGRAPHY SEARCH) trước khi
> coi bất kỳ `side_width` nào là "xong" — xem lý do đầy đủ ở đó.

## 7. ẢNH NỀN — khoá cấu trúc, KHÔNG khoá nội dung

- Dùng **một scene liên tục trên toàn khung** phù hợp câu chuyện; subject REF lớn ở khoảng 1/3 phải và hòa
  vào scene, không panel chữ nhật/cutout halo. Ba dòng đè lên scene bên trái; ưu tiên stroke/shadow, chỉ dùng
  contrast veil rất nhẹ khi thật cần, không biến scene thành mảng đen/xám phẳng.
- Blur nhẹ scene dưới vùng chữ (mặc định Gaussian 3px), feather rộng khoảng 12% canvas trước vùng subject;
  vùng phải/mặt giữ pixel-sharp. Scene trái vẫn phải nhận ra ở preview 360px.
- **Đạo cụ (nếu có) cầm CAO** ngang ngực — banner che ~22% đáy khung; đáy 20% là nền phẳng.
- REF-LOCK master của tập (`_ref/001.png`), `no text`, style suffix của profile.
- Nghiệm thu nền trước khi overlay: khớp REF · không chữ AI · vùng chữ sạch · tay/mặt không artifact.
- Hình + chữ **bổ sung** nhau (hình kể cảnh title hứa, chữ kể điều title giấu). Không minh hoạ lại chữ.
- Nhân vật, biểu cảm, đạo cụ, bối cảnh **mới theo script từng tập** — không lấy từ master.

## 8. MASTER REFERENCE POLICY

**MASTER_REFERENCE = HUMAN APPROVED VISUAL TARGET.** Mở ra NHÌN mỗi lần làm thumbnail lane này.

| COPY (học) | DO NOT COPY |
|---|---|
| structure (subject một phía / text đối diện / banner) | wording |
| approximate text dominance (chữ chiếm bao nhiêu vùng trái) | character |
| visual density | clothing |
| text/subject balance | prop |
| face scale | background |
| banner geometry | story / hook |
| spacing philosophy (khối sát, không dàn đều) | facial expression |
| hierarchy philosophy (1 hook + 1 trigger + 1 context + payoff) | **exact colors assigned to line number** |
| quality bar ở full + 360 | exact lighting / exact crop / subject identity cụ thể |

## 9. FINAL QC — bắt buộc so với MASTER_REFERENCE

**Điều kiện tiên quyết:** §4B (PRE-PASS TYPOGRAPHY OPTIMIZATION) phải đã chạy xong với FINAL GATE (§4B.6)
trả lời đúng chiều cả 6 câu (A-D = NO, E-F = YES). Chưa chạy §4B hoặc còn 1 câu sai chiều → KHÔNG được vào
bước dưới đây với kết luận PASS.

Mở candidate full + 360 và designated MASTER full + 360, rồi trả lời trên ảnh THẬT:
1. Typography có táo bạo tương đương MASTER không?
2. Không gian hữu ích có được khai thác mạnh tương đương MASTER không?
3. Ở 360px impact có tương đương MASTER không, không chỉ “đọc được”?
4. Có dòng nào rõ ràng có thể phóng lớn thêm mà FACE vẫn sạch và story không hỏng không? (phải NO)
5. Vùng text được chữ lấp tương đương master? (không có khoảng trống chết)
6. Banner gần full width, đỏ sạch/bão hòa, chữ trắng lớn và nặng như master?
7. **SUBJECT + SCENE** — Subject có lớn/rõ ở khoảng 1/3 phải và hòa tự nhiên vào scene toàn khung không?
   Có panel chữ nhật, halo cutout hoặc nền bị chia đôi đen/sáng không? Scene phía sau chữ có còn nhận ra ở
   360px không? Main text không được đè FACE.
8. Tiếng Nhật 100% đúng glyph? Không spoil? Không lặp title vô ích? Không bịa? (kèm dịch Việt từng dòng)
9. Nếu 4+1: ghi rõ vì sao 3+1 không giữ được.
Mục nào kém master → FIX typography/bố cục trước, không hạ chuẩn. Tối đa 2 vòng sửa.

## 10. HUMAN APPROVAL RULE

- `FINAL QC = PASS` (AI) **chưa đủ**.
- Chỉ thumbnail **FINAL QC PASS + HUMAN APPROVED** (chủ kênh nói rõ) mới được: (a) thêm `golden/GOLDEN_<nnn>_<slug>.md`,
  (b) thay `MASTER_REFERENCE.png`. Thay master là quyết định của chủ kênh; model chỉ đề xuất.
- Golden = học **cách tư duy** (why final worked · generalizable principles · case-specific decisions ·
  anti-overfitting). Không copy wording. Chỉ load golden liên quan.

## 11. FILE PHẢI LOAD khi làm thumbnail lane satori

1. Skill global `~/.claude/skills/youtube-thumbnail/SKILL.md` (+ `TOOL_NOTES.md` khi render)
2. `docs/thumbnail_lanes/satori_jp/TEMPLATE.md` (file này)
3. `docs/thumbnail_lanes/satori_jp/MASTER_REFERENCE.png` + `MASTER_REFERENCE_360.png` — mở ra nhìn
4. TITLE + DESCRIPTION hiện tại + đúng MỘT approved character REF của tập.

**Cấm mặc định:** không mở `golden/`, thumbnail/candidate tập cũ, prompt cũ hoặc render parameters cũ.
Chỉ được mở thêm khi chủ kênh chỉ định rõ file nào.

> Lịch sử: mẫu này thay thế quy tắc "4+1 dòng cho mọi tập satori" từng nằm trong skill global (đã gỡ
> 2026-09-17). 4+1 chỉ còn là fallback theo mục 2.

## 12. TITLE ↔ THUMBNAIL FINAL SYNC (thêm 2026-09-17 — thumbnail được làm trước title chính thức)

Pipeline satori sinh title chính thức ở **B9** (`TIEU_DE_MO_TA.txt` / `listting.txt`), CHẠY SAU bước
thumbnail (B7). Mục này giải quyết đúng khoảng trống đó: thumbnail không phải chờ title, nhưng title thật
xuất hiện thì bắt buộc đối chiếu lại.

**Thứ tự pipeline đầy đủ (bổ sung, không đổi thứ tự cũ):**
```
FULL SCRIPT
  → WORKING TITLE (nếu chưa có title chính thức)
  → THUMBNAIL STRATEGY → THUMBNAIL PRODUCTION → FINAL VISUAL QC → HUMAN APPROVAL
  → B9 sinh FINAL TITLE
  → TITLE ↔ THUMBNAIL FINAL SYNC (mục này)
  → KEEP / FIX COPY / REMAKE
  → FINAL ASSETS → GOLDEN UPDATE
```

### 12.1 Working Title
Chưa có title chính thức lúc làm thumbnail → được phép tự đề xuất WORKING TITLE từ full script, chỉ để
định hướng chiến lược (không phải title đăng thật). Đánh dấu rõ **TITLE_STATUS = WORKING** trong Golden
Example của tập đó (mục "Working title (chưa có title chính thức lúc làm thumbnail)"). Thumbnail
Strategist vẫn làm đủ §1 skill global khi dùng working title: đọc full script, hiểu story, xác định title
đang hứa gì, tìm thông tin nên bổ sung, tránh lặp, giữ curiosity gap.

### 12.2 Trigger
Ngay sau khi B9 tạo `TIEU_DE_MO_TA.txt`/`listting.txt` (FINAL TITLE) cho một tập đã có thumbnail (dù đã
HUMAN APPROVED hay chưa) → chạy REVIEW này. Input: FINAL TITLE (dòng tiêu đề đầu tiên, KHÔNG phải toàn bộ
mô tả) · full script · `thumbnail_final.png` · `thumb_text.txt` · file này · `MASTER_REFERENCE.png`.
**Không redesign ngay — chỉ REVIEW trước.**

### 12.3 Review 6 điểm
- **A. REPETITION — KHÔNG tự động = ISSUE (patch 2026-09-17 sau human review tập 2).** Trùng với title
  không tự nó là lỗi; phải phân biệt 2 loại:
  - **REDUNDANT REPETITION → FIX.** Thumbnail lặp thông tin title nhưng: không tăng emotional impact ·
    không phải core hook · không cần thiết để thumbnail tự hoạt động · đang chiếm chỗ có thể dùng cho
    thông tin mạnh hơn.
  - **STRATEGIC REPETITION → KEEP được phép.** Phần lặp là **CORE HOOK của story** · có sức mạnh cảm
    xúc/sốc rất cao · cần thiết để thumbnail **tự hoạt động khi viewer chỉ nhìn thumbnail, chưa đọc
    title** · khi kết hợp với các dòng còn lại vẫn tạo thêm curiosity (không phải đọc lại nguyên khối).
  - **Phép thử bắt buộc trước khi FLAG:** *"Nếu bỏ phần lặp này, thumbnail đứng một mình có yếu đi đáng
    kể không?"* — **CÓ** → đây là STRATEGIC, không được FIX chỉ vì lặp title. **KHÔNG** → có thể thay
    bằng thông tin bổ sung mạnh hơn (REDUNDANT thật).
  - **Nguyên tắc ưu tiên: SPECIFIC HIGH-IMPACT HOOK > GENERIC NON-REPETITIVE COPY.** Không rewrite một
    câu cụ thể/mạnh thành một câu mơ hồ chỉ để đạt "0% lặp title" — câu mơ hồ generic, không mang đủ
    information value khi đứng độc lập, là lỗi NẶNG HƠN việc lặp một phần title có chủ đích.
  - Đặc biệt soi: thumbnail có paraphrase gần sát một cụm mà title trích dẫn nguyên văn trong 「…」 không —
    nhưng nếu cụm đó chính là core emotional hook thì áp phép thử ở trên trước khi kết luận ISSUE.
- **B. COMPLEMENT** — Title + thumbnail đọc cùng nhau có tạo thêm câu hỏi mới trong đầu người xem không?
  Mục tiêu: TITLE cho một phần thông tin + THUMBNAIL cho phần khác = curiosity gap MẠNH HƠN từng phần riêng.
- **C. CONTRADICTION** — Thumbnail có vô tình mâu thuẫn với FINAL TITLE không? Phân biệt GOOD (nghịch lý có
  thật trong story, tăng curiosity — giữ) và BAD (title/thumbnail khiến hiểu 2 sự kiện không tương thích do
  wording sai/misleading — phải sửa).
- **D. SPOILER** — Ghép FINAL TITLE + thumbnail lại có vô tình lộ payoff/bí mật chính mà từng phần riêng lẻ
  chưa lộ không?
- **E. STORY ACCURACY** — Title + thumbnail có cùng phản ánh đúng full script không? Không bịa fact/quote,
  không phóng đại sai bản chất, không tạo quan hệ nhân quả không có trong story.
- **F. CURIOSITY/CTR** — Sau khi có FINAL TITLE thật, thumbnail hiện tại còn là hook tốt nhất không? KHÔNG
  đổi chỉ vì tồn tại wording khác — chỉ FIX khi title mới thực sự làm thumbnail bị lặp / curiosity giảm
  đáng kể / spoil / misleading / mâu thuẫn / hook không còn hiệu quả.

### 12.4 Quy tắc quyết định
- Title khác working title nhưng thumbnail vẫn accurate + complementary + non-spoiler + curiosity mạnh, và
  phần trùng title (nếu có) là **STRATEGIC REPETITION** (qua được phép thử "đứng một mình có yếu đi không")
  → **KEEP THUMBNAIL**. Không sửa chỉ vì title đổi chữ, và không sửa chỉ để đạt 0% trùng chữ với title.
- Phát hiện vấn đề THẬT (REDUNDANT repetition thật sự — không đổi thumbnail thành copy chung chung để né
  trùng — hoặc spoil/mâu thuẫn/curiosity giảm mà không do đánh đổi lấy tính mơ hồ) → **FIX COPY FIRST**, ưu
  tiên chỉ sửa `thumb_text.txt`. KHÔNG gen lại nền nếu nhân vật/scene/cảm xúc/bố cục vẫn phù hợp story và
  FINAL TITLE. Chỉ **REMAKE IMAGE** khi FINAL TITLE làm thay đổi bản chất hook đến mức visual concept hiện
  tại không còn đúng.

### 12.5 Sau khi FIX COPY (bắt buộc đủ, không được PASS chỉ dựa trên text file)
Japanese Native QC (skill global §2) → dịch Việt từng dòng mới → giữ **3 VISUAL MAIN ROWS + 1 BANNER** nếu
có thể (§2 của file này), 4+1 chỉ fallback đúng luật §2 → giữ bottom red banner mandatory (§3) → senior
typography (§4) → **render lại PNG thật** → QC full-size → QC 360px → **so với MASTER_REFERENCE** (§9).

### 12.6 Golden Sync
Thumbnail đã HUMAN APPROVED trước khi có FINAL TITLE → **KHÔNG huỷ HUMAN APPROVAL** chỉ vì title đổi. Sau
review:
- **KEEP** → cập nhật FINAL TITLE vào Golden tương ứng, giữ nguyên thumbnail/copy đã duyệt.
- **FIX COPY** → thumbnail mới **phải HUMAN APPROVED lại** trước khi cập nhật copy vào Golden.
- **REMAKE** → thumbnail mới bắt buộc FINAL VISUAL QC PASS + HUMAN APPROVED trước khi thay Golden/Master.
Golden luôn lưu FINAL TITLE, không để WORKING TITLE giả làm title chính thức.

### 12.7 Output chuẩn (dùng đúng format mỗi lần chạy sync)
```
TITLE STATUS: FINAL
FINAL TITLE: [日本語] → [Dịch Việt]
THUMBNAIL TEXT: [từng dòng] → [dịch Việt] ... BANNER: [...] → [...]
TITLE ↔ THUMBNAIL: PASS / FIX / REMAKE
REPETITION / COMPLEMENT / SPOILER / STORY ACCURACY / CURIOSITY: PASS / ISSUE (từng mục)
ACTION: KEEP / FIX COPY / REMAKE
REASON: (tiếng Việt, ngắn gọn)
```
