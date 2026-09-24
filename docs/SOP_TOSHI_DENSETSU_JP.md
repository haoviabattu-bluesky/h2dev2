# SOP — LANE A: 都市伝説 / 宇宙 / ミステリー (Nhật, kể tài liệu)

> **Đây KHÔNG phải SOP satori.** Hai lane chạy song song trong cùng dự án nhưng khác nhau ở 4 chỗ
> chí mạng. Vào nhầm SOP = bật REF-LOCK cho kênh không có nhân vật (đốt tiền ảnh vô ích) và viết
> văn cụ bà cho giọng dẫn nam. Trước khi làm gì, xác định profile:
>
> | Anh nói | Profile | SOP |
> |---|---|---|
> | "video satori / người già / Nhật kể chuyện đời" | `Lopezzapa68` (satori-jp-obaa) | `SOP_SATORI_JP.md` |
> | "video 都市伝説 / vũ trụ / bí ẩn / Lane A" | **`toshi-densetsu-jp`** | **file này** |

Nguồn nghiên cứu: `docs/laneA_from_research/` (HANDOFF · NICHE_KIT · BLUEPRINT · 63 tiêu đề ·
4 transcript đầy đủ · 190 comment · 12 thumbnail). Mọi con số dưới đây đo thật 2026-09-09/10.

---

## 0. BẢNG DELTA — khác satori chỗ nào (đọc trước khi chạm tay vào lệnh)

| Khâu | Satori JP | **Lane A** |
|---|---|---|
| Người kể | Cụ bà ngôi 1 kể đời mình | Người dẫn tài liệu **ngôi 3**, nam trầm |
| Giọng | George @0.92 · char_rate 285 | **Akira - Calm Deep** `elevenlabs_JKne0OHHjFFwcwWzlGj0` @**1.15** · char_rate **374,9** (đo thật 2026-09-10, mẫu văn tài liệu) |
| Kịch bản 26' | ~7.400 chữ | **9.747 chữ** |
| Cấu trúc | 悟り | **5 chương 第1章…第5章**, chương 4 móc về Nhật |
| Thân video | Ảnh AI 1/6-7s (~290 ảnh, ~20.000đ) | **Clip stock** cắt 12–16 lần/phút (~350 cảnh, **0đ**) |
| Ảnh AI | cả video | **CHỈ thumbnail** |
| REF-LOCK + B5RQ | Bắt buộc | ❌ **BỎ** (`image.ref_lock=false`) |
| B5Q (QC loạt ảnh) | Bắt buộc | ❌ tự bỏ qua (không có loạt ảnh) |
| B8Q chấm "ảnh khớp lời" | Có | ❌ tự tắt — B-roll CỐ Ý không minh hoạ lời |
| QC số học | không | ✅ **bắt buộc** (`gate.check_arithmetic`) |
| Nguồn nội dung | kênh Hàn simbot2 | **kênh Anh ngữ + Wikipedia EN** (`source_lang: "en,ja"`) |

**Định lượng bắt buộc / 1 video** — ⚠️ **ngưỡng đã NẮN LẠI theo phân bố thật của 4 transcript đối
thủ (2026-09-10)**, vì bản đầu chép câu chữ trong tài liệu bàn giao ("しかし mỗi ≤90 giây") và nó
CHẶT HƠN CẢ KÊNH MẪU → đánh trượt oan hai bản kịch bản tốt:

| Chỉ số | Đối thủ đo được | Ngưỡng chốt |
|---|---|---|
| Độ dài 1 câu chuyện | 30,8–46 phút (chuyện đầu của video dài) | **28 phút = 10.497 chữ** |
| Đảo chiều `しかし/だが/ところが` | 0,55–1,01 lần/phút · gap lớn nhất 200–560s · p90 101–222s | **≥0,5/phút VÀ gap ≤300s** |
| Mốc năm / số có đơn vị | 0,87–2,23 /phút | ≥0,8/phút |
| Mẫu câu lá chắn `〜という説がある` | 1,4–5,1 lần/10 phút | **≥2,0 /10 phút** |
| Chương | 5 (video dài = 2 câu chuyện nối) | đủ 第1章…第5章 |

`あなた` CHỈ ở đầu và cuối · **tiêu đề 30–45 ký tự** (45–60 ký tự cho view thấp hơn **2,4 lần**).

> **Bài học chung:** con số trong tài liệu bàn giao là **mô tả cảm giác**, không phải trần kỹ
> thuật. Trước khi biến bất kỳ câu nào thành gate, hãy đo lại chính dữ liệu đối thủ đã có sẵn
> trong `docs/laneA_from_research/data/`.

---

## 0b. CHANNEL ANALYZER — tổng hợp DNA kênh TRƯỚC khi chọn đề tài (mới, 2026-09-16)

Trước đây Claude tự đọc 5-8 transcript thô của kênh mẫu để "cảm" công thức (skill
`youtube-series-builder` P1) — tốn token Claude, không ghi lại thành file, mỗi tab mới lại phải đọc
lại từ đầu. Nay tách 2 việc này ra khỏi Claude, chạy 1 lần/kênh bằng
`pipeline/channel_analyzer.py` + `pipeline/retrieve_videos.py` (chi tiết thiết kế:
`docs/superpowers/specs/2026-09-16-gemini-channel-analyzer-design.md`).

> ⚠️ Đặt tên **K1/K2/K3** cho 2 tool này, KHÔNG dùng B1/B2/B3 — số bước B0-B11 dưới đây đã cố định
> cho pipeline sản xuất 1 TẬP (B3 = KỊCH BẢN, xem §3). Việc ở đây là CẤP KÊNH (1 lần/kênh), dùng
> chung số với B0-B11 sẽ đọc lẫn (đã dính thật 1 lần 2026-09-16, xem CLAUDE.md mục CHANNEL ANALYZER).

**K1+K2 — chạy 1 lần cho 1 kênh mẫu mới** (đã verify thật trên kênh 今夜も都市伝説, đo 2026-09-16:
86-112s cho 8 video, 100% phân tích được, QC DNA "ĐẠT" 11/11 đề mục):
```bash
cd E:\CLAUDE\YOUTUBE\h2dev
py -3.13 pipeline\channel_analyzer.py --channel-url "<URL kênh mẫu>" \
    --out-dir docs\channel_dna\<slug-kenh> --n-candidates 20 --n-select 10 --niche-hint "都市伝説・ミステリー・怖い話"
```
Ra `docs/channel_dna/<slug-kenh>/CHANNEL_DNA.md` (11 đề mục: Audience, Content pillars, Narrative
style, Hook formulas, Story structure, Pacing, Emotional triggers, CTA patterns, Title patterns,
Thumbnail patterns, Rules for writing new videos) + `VIDEO_ANALYSIS/<id>.json` (1 file/video, field
`topics` dùng cho K3 dưới đây). **Đọc `CHANNEL_DNA.md` thay vì tự đọc transcript thô** khi cần nắm
lại công thức kênh (khớp thẳng vào bảng DELTA §0 — nhiều mục trong bảng đó vốn được rút ra thủ công,
nay có thể đối chiếu/cập nhật bằng file này).

**K3 — chạy MỖI LẦN chọn đề tài tập mới** (không cần internet/API key, chạy máy nào cũng được):
```bash
py -3.13 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\<slug-kenh> \
    --topic "<mô tả chủ đề tập sắp viết, tiếng Nhật>" --top-n 8
```
Đọc `CHANNEL_DNA.md` + N file JSON trả về (thay vì đọc thô 3-4 video "top view" như trước) làm input
viết `competitor.txt`/`series_ctx.txt` ở §2 dưới đây — vẫn giữ nguyên 1 transcript đầy của video
"khung kể" gần chủ đề nhất (video top-1 trong kết quả retrieval) để không mất nhịp câu/giọng văn đặc
trưng.

**⭐ TỰ VẬN ĐỘNG — KHÔNG NGỒI CHỜ (user chốt 2026-09-16):** `docs/channel_dna/<slug-kenh>/` thiếu
hoặc chưa có trước khi viết 1 tập → **TỰ chạy K1+K2 ngay tại tab này**, không hỏi/chờ ai giao hộ.
K1+K2 là Python thuần gọi Gemini qua proxy ramcloud CÓ SẴN trong dự án — chạy được ngay tại đây,
không bắt buộc qua máy 2 (máy 2 chỉ là 1 lựa chọn, xem CLAUDE.md mục CHANNEL ANALYZER). Việc này vẫn
nằm trong "Bước 1 — đầu não" (chuẩn bị dữ liệu để viết), không vi phạm luật cấm render/dựng video.

⚠️ **Ranh giới — KHÔNG áp dụng cho hồ sơ SPACE_RESEARCH (B0):** nguyên tắc "tự vận động" ở trên chỉ
áp dụng cho CHANNEL_DNA (công thức/giọng văn kênh mẫu, không cần dẫn nguồn chính xác). Hồ sơ
NGHIÊN CỨU ĐỀ TÀI (dữ kiện/tư liệu 1 tập cụ thể, cổng B0 `qc_hoso.py`, đọc `docs/GIAO_VIEC_SPACE_
RESEARCH.md`) thì KHÁC — đó là dữ kiện có thật cần nguồn kiểm chứng, Gemini không thay thế được,
KHÔNG được tự bịa/tự tổng hợp khi SPACE_RESEARCH chưa giao kịp. Thiếu hồ sơ đề tài → báo user, chờ
đúng theo `docs/GIAO_VIEC_SPACE_RESEARCH.md`, không tự chế dữ kiện (xem memory "dữ liệu thật không
chỉ tiền").

**Giới hạn đã biết** (đo thật khi build, không phải suy đoán): retrieval so khớp SUBSTRING chứ không
hiểu ngữ nghĩa — có thể xếp hạng chưa tối ưu 100% khi câu hỏi dùng từ đồng nghĩa thay vì đúng từ
khoá trong `topics[]`; và `CHANNEL_DNA.md` mạnh về mô tả ĐỊNH TÍNH (hook/cấu trúc/CTA, có trích dẫn
thật) nhưng yếu hơn về so sánh ĐỊNH LƯỢNG kiểu "độ dài tiêu đề nào thắng" (cần cả catalog kèm video
kém thành công để so sánh, không chỉ N video top-view) — vẫn cần bảng ĐỊNH LƯỢNG thủ công ở §0 cho
những con số cần độ chính xác cao (gate số học B3Q).

**Gói bàn giao máy 2** (chạy hoàn toàn không cần Claude, dùng khi muốn giao máy khác phân tích kênh):
`handoff_may2_channel_analyzer.zip` ở gốc dự án — tự chứa `HUONG_DAN.md` + 6 file `.py` cần thiết,
không phụ thuộc phần còn lại của `pipeline/`.

---

⚠️ Hook 20–30s bắt buộc trước S2 — xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.

## 1. LỆNH CHẠY (một dòng cho cả tập)

```bash
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 -X utf8 make_video.py --profile toshi-densetsu-jp --slug ep01-tagen-uchu \
    --competitor <video_id_kênh_mẫu_hoặc_kênh_Anh_ngữ>
```

Bước chạy: `B2 tư liệu → B3 kịch bản (2 pass + gate) → B3Q QC nội dung + SỐ HỌC → B4 giọng + SRT
→ B4Q QC nghe → B5 kho clip stock → B7 thumbnail → B8 ghép clip stock → B8Q → B9`.

Chạy khô (không tốn tiền hình/tiếng): thêm `--dry-run`. Chạy lại từ một bước: `--from B5`.

---

## 2. B2 — TƯ LIỆU (khác satori: nguồn TIẾNG ANH)

7/8 đề tài của kênh mẫu là chuyện gốc phương Tây, cung tiếng Nhật chỉ **0–8 video/tháng**. Mô hình
kinh doanh của lane này = **dịch & kể lại chuyện đã nổi bằng tiếng Anh sang tiếng Nhật, rồi móc về
Nhật Bản**.

Hai file vào thư mục tập, KHÁC VAI TRÒ nhau — đừng gộp:
- `competitor.txt` = **KHUNG KỂ**. Lấy transcript một video của kênh mẫu (hoặc kênh Anh ngữ cùng
  đề tài). Đây là thứ dạy nhịp và thứ tự dẫn dắt.
- `series_ctx.txt` = **TƯ LIỆU SỰ THẬT**. Dữ kiện có thật của đề tài (Wikipedia EN, hồ sơ giải mật)
  + 12 mục checklist của video. `profile.script.ctx_label` đã đổi nhãn khối này thành
  "TƯ LIỆU GỐC — mọi tên/ngày/số liệu PHẢI lấy đúng từ đây, cấm bịa thêm".

Chọn đề tài bằng `topic_gap.py` (đã copy sang `pipeline/`) — ưu tiên đề tài **cung tiếng Nhật ≤2
video/tháng** mà view vẫn cao.

## 3. B3 — KỊCH BẢN

`profile.script.mode = "documentary"` đổi hẳn hai khối trong prompt so với satori:
- Nhiệm vụ: kể chuyện **CÓ THẬT**, mọi tên/ngày/số **lấy đúng từ tư liệu** (satori thì ngược lại:
  tự nghĩ ra hết).
- Luật chống trùng: **CẤM đổi tên người/ngày/địa danh/số liệu** để né trùng (satori được phép và
  bắt buộc đổi). Khác biệt tạo bằng THỨ TỰ kể, GÓC NHÌN, dữ kiện thêm, và chương móc về Nhật.

`profile.script.structure = "chapters5"` bơm khung 5 chương + hook 30 giây vào prompt.

Gate máy đo (`ai_steps._gate_ngach`) chặn ngay ở B3, không cần chờ QC tốn tiền:
`THIẾU CHƯƠNG` · `ĐỨT NHỊP ĐẢO CHIỀU` (khoảng >90s không có しかし) · `THIẾU MỐC SỰ THẬT` ·
`THIẾU MẪU CÂU LÁ CHẮN`.

## 4. B3Q — QC NỘI DUNG + ⭐ CỔNG SỐ HỌC

Ngách này **soi số rất kỹ**. Một comment 44👍 dưới video kênh mẫu bắt lỗi phép nhân của họ
(`東京ドームの60倍が日本列島より大きい？200mの60倍は12kmだろが！`) — một phép tính sai xoá sạch cái uy
"đã nghiên cứu kỹ" mà cả video xây lên, và nó nằm ở comment nổi nhất ai vào cũng đọc.

Hai tầng, đã dựng:
1. **`qc_numbers.py`** (máy, miễn phí, tất định): khoảng năm · khoảng tháng · tuổi theo năm sinh ·
   phép nhân có đơn vị · hằng số quen thuộc (光年, 富士山, đường kính Trái Đất, khoảng cách Mặt
   Trăng/Mặt Trời) · phần trăm cộng quá 100. Verify 2026-09-10: bắt 5/5 lỗi cài sẵn, 0 báo động giả.
   Chạy riêng: `py -3.13 qc_numbers.py --script <file>`.
2. **Tầng LLM** trong `qc_script.py`: mục `so_hoc` — tự tính lại mọi phép, mọi quy đổi, mọi so sánh
   "gấp N lần <vật quen thuộc>". Có lỗi mức `cao` ⇒ verdict **HỎNG** (viết lại), mức nào cũng ⇒ ít
   nhất **SỬA**.

### ⭐ CỔNG MỞ ĐẦU (thêm 2026-09-11 — `qc_script.mo_dau()`)

Trước đó `script.gate` **không có một dòng nào về mở đầu** — chỗ quyết định người xem ở lại hay
bỏ đi lại là chỗ không cổng nào chạm tới. Tập 3 lọt một mở đầu 486 chữ trong đó 11/13 câu không
chứa lấy một chi tiết nào ("vì sao suốt bao năm vẫn thu hút lòng người", "anh cũng từng một lần
tin"). Chủ dự án xem là thấy lan man ngay; máy báo ĐẠT.

Đo **neo dữ kiện** = con số + danh từ riêng katakana trên 1.000 chữ. Đếm được, và phân biệt đúng
thứ cần phân biệt: câu có năm tháng/tên trường/tên nguyên tố là câu kể được một việc; câu không
có gì là câu nói suông.

Ngưỡng lấy từ **4 transcript đối thủ của chính lane này**, xếp theo lượt xem:

| view | chữ | neo/1000 chữ |
|---|---|---|
| 145.972 | 696 | **24,4** |
| 124.915 | 1.068 | **21,5** |
| 98.898 | 681 | **20,6** |
| 99.312 | 766 | 7,8 ← nhạt hẳn |

Chốt: `hook_chars [650, 1150]` · `hook_anchor_per_1000 = 18`. Mở đầu cũ ep03 = 12,3 → **trượt**;
bản viết lại 715 chữ / 23,8 → **đạt**. (Đã thử ngược cả hai bản.)

⚠️ **Mở đầu nhắc lại chủ đề của chương 1 KHÔNG phải lỗi** — cả 4 đối thủ đều làm vậy (bài Cayce
kết mở đầu bằng 「彼は地球の人間ではなかった」 rồi 第1章 lặp đúng câu đó). Đó là format của ngách:
mở đầu **nêu**, chương 1 **kể kỹ**. Lỗi thật là mở đầu **rỗng**, không phải mở đầu **lặp**.

## 4b. B3F — ⭐ CỔNG KIỂM DỮ KIỆN (chi tiết này ở ĐÂU ra?)

B3Q hỏi *"kịch bản có tự mâu thuẫn không"*. B3F hỏi câu khác hẳn: **"chi tiết này lấy từ đâu?"**

Đo thật 2026-09-10 trên video 1: kịch bản viết 「1989年、日本の**埼玉県**にある日立製作所の研究所で…」
trong khi tư liệu **không hề nói phòng thí nghiệm ở đâu**. Tra lại: Wikipedia ghi Tonomura ở
*Hitachi Central Research Laboratory*, Physics World ghi *"Advanced Research Laboratory in Hitachi,
**Tokyo**"* — không nguồn nào nói Saitama. Bản nháp đầu còn điền **hai kiểu khác nhau** ở hai chương;
B3Q bắt được mâu thuẫn rồi "sửa" bằng cách chọn một cái cho nhất quán — **và chọn phải cái sai**.

> **B3Q làm cho NHẤT QUÁN. B3F làm cho ĐÚNG NGUỒN.**
> Trong máy không có cách nào biết "chi tiết này có thật không" — nên cổng này chỉ hỏi một câu trả
> lời được: **có trong `series_ctx.txt` không?** Không có ⇒ không được lên hình.

Hai tầng, đều tất định và miễn phí (`pipeline/qc_facts.py`):

| Tầng | Bắt gì |
|---|---|
| A. Kịch bản ⟶ tư liệu | mốc năm · tỉnh/thành/quận · cơ quan (大学/研究所/省/庁…) · tên riêng katakana · số có đơn vị — cái nào không có trong tư liệu ⇒ **mức nặng, DỪNG** |
| B. Tư liệu tự nó | dòng dữ kiện không kèm `〔出典: …〕`/URL ⇒ cảnh báo + báo tỉ lệ `có nguồn / tổng` |

Ba luật đã phải tinh chỉnh để cổng không kêu oan (**cổng kêu oan là cổng bị tắt**):
1. **Tách mốc năm khỏi khoảng thời gian** — 「1000年以上前」「180年以上が経過」 là độ dài, không phải năm.
2. **Tên riêng katakana chỉ bắt thứ CHẮC là tên người** (có dấu `・` ngăn họ-tên, hoặc đi kèm
   博士/教授/氏/三世). Quét mọi chuỗi katakana thì báo oan cả コーヒーカップ・ベッド・サイコロ・レンズ.
3. **Tên cơ quan phải cắt dần đầu chuỗi rồi mới kết luận** — regex tham ăn nuốt cả 「名門」 nên
   「名門プリンストン大学」 bị báo là bịa dù プリンストン大学 có trong tư liệu.

Số đo thật trên video 1: trước khi sửa **3 lỗi nặng** (`埼玉県` · `26歳` · `100パーセント`), sau khi bỏ
tên tỉnh + bổ sung nguồn vào tư liệu còn **0 lỗi nặng**, nguồn 4/35 dòng.

⚠️ **B3F là DỪNG HẲN, không được nối vào nhánh viết lại kịch bản.** Cái sai nằm ở TƯ LIỆU — viết lại
kịch bản chỉ đẻ ra đúng chỗ bịa đó lần nữa. Tệ hơn: nhánh viết lại **xoá `script.txt` + `voice.mp3` +
`voice.srt`** (đã dính thật khi nối nhầm, mất cả ba file, phải trích lại tiếng từ `final.mp4`).

## 5. B4 — GIỌNG

`elevenlabs_JKne0OHHjFFwcwWzlGj0` (Akira - Calm Deep Japanese Male), **speed 1.15**, fx `none`,
`pace: false` (KHÔNG giãn nhịp — giãn nhịp là thủ thuật của giọng cụ già; ở đây nhịp phải chặt vì
khán giả **xem chủ động**: 0/190 comment nhắc "nghe khi ngủ").

Hai thứ ở B4Q đã phải sửa vì là **luật satori ẩn**:
- `qc_audio(..., doi_nghi=False)` khi `voice.pace=false` — cổng cũ đòi "≥1 chỗ nghỉ rõ mỗi phút"
  và báo lỗi "nghi CHƯA chạy giãn nhịp" cho đúng thứ mình cố ý làm.
- **`tts.chuan_muc()` nay chạy cho MỌI lượt đọc**: file thô ElevenLabs đo được đỉnh **−0,1 dBFS**
  (chạm trần, có thể vỡ tiếng). Kênh satori vô tình thoát vì preset FX làm-già có sẵn `loudnorm`;
  kênh để `fx=none` thì đi thẳng ra video. Nay chuẩn về −16 LUFS / trần −1,5 dBTP, không đổi thời
  lượng nên SRT vẫn khớp. Đã chuẩn hoá file có sẵn: đỉnh −0,1 → **−1,8 dB**, dài y nguyên 1770,3s.

⚠️ Đo char-rate lại **mỗi khi đổi giọng hoặc đổi tốc độ**:
`py -3.13 calibrate.py --profile toshi-densetsu-jp` — profile đã khai `voice.calib_style: "doc"`
nên mẫu đo là văn tài liệu (dày kanji + mốc năm), không phải mẫu tâm tình của satori. Đo thật:
cùng giọng, @1.0 = 317,4 chữ/phút · @1.15 = **374,9** (đúng dải đối thủ 356–383).

## 6. B5 — KHO CLIP STOCK (thay cho gen ảnh AI)

`make_video.py` tự rẽ nhánh theo `profile.body.mode = "stock_clips"`: **không gen ảnh AI nào**,
chỉ bảo đảm kho tư liệu đủ sức chứa.

1. Viết `stock_queries.txt` trong thư mục tập — mỗi dòng một **từ khoá TIẾNG ANH**. B5 tự chạy
   `stockfetch.py` cho từng dòng.
2. Kho dùng chung mọi tập: `assets/stock/` + sổ giấy phép `manifest.jsonl`.
3. **Sức chứa** = Σ trần dùng lại mỗi file; clip dài cho nhiều đoạn khác nhau hơn nên trần cao hơn
   (~1 lần dùng / 15 giây nguồn, tối đa 4× `reuse_max`). Thiếu ⇒ B5 DỪNG, không dựng bằng kho mỏng.

**⚠️ Checklist BẮT BUỘC trước khi chốt `stock_queries.txt` — tập có tên tôn giáo/quốc gia/tổ chức cụ
thể trong `series_ctx.txt` (chốt 2026-09-17, sau vụ ep08 Fátima-Akita):** đọc lại danh sách tên riêng
đã kiểm chứng trong `series_ctx.txt`/`evidence.json`, nếu có tôn giáo/dân tộc/quốc gia/tổ chức cụ thể
(Công giáo, Chính thống giáo, Phật giáo, Nhật/Nga/Ấn Độ, Vatican...) thì **PHẢI ghi rõ tên đó vào
từng dòng từ khoá liên quan**, không được để chung chung. `soi_kho.py` chỉ chấm được "clip có đúng với
TỪ KHOÁ đã tải nó không" — nó KHÔNG chấm được "từ khoá đó có đúng với câu chuyện không", nên từ khoá
chung chung vẫn qua được `soi_kho.py` trót lọt rồi lộ ra muộn ở B8Q (tốn cả vòng B5-B7-B8-B8Q mới
biết). Đo thật ep08: `"wooden statue religious carving"` → Pexels trả tượng Phật/thần Ganesha/võ
tướng Nhật (đều "đúng" với từ khoá, sai với câu chuyện Công giáo) · `"bishop clergy religious
ceremony"` → linh mục Chính thống giáo Nga (sai với bối cảnh Công giáo Nhật) · `"crowd gathering
outdoor vintage"` → đám đông hội chợ có đu quay (sai với đám đông hành hương tôn giáo 1917). Sửa
bằng cách thêm hẳn tên vào từ khoá: `"catholic church statue mary closeup"`, `"japanese catholic
bishop ceremony"`, `"religious pilgrimage crowd praying outdoor"`. Việc này MIỄN PHÍ (chỉ là viết
cẩn thận hơn lúc soạn từ khoá), không cần thêm cổng QC/công cụ nào mới.

**Bản quyền — 3 luật cứng:**
1. File không có trong `manifest.jsonl` thì `stock_cut.py` **bỏ**, không đoán. Internet Archive tìm
   "apollo" trả về cả bản ghi CSPAN/FOXNEWS **CÓ BẢN QUYỀN** → bộ lọc `licenseurl` trong
   `stock_sources.py` là bắt buộc, đừng gỡ.
2. **Có giấy phép ≠ dùng được.** `body.license_policy` mặc định `permissive` = PD + CC BY, **loại
   CC BY-SA / NC / ND**: SA kéo cả video 30 phút vào ràng buộc share-alike, NC cấm bật kiếm tiền,
   ND cấm cắt ghép. Ảnh **bằng chứng** siết chặt hơn nữa — `evidence_license_policy: "pd"`, vì đó
   là tấm mình chủ động khoe ra và cháy chú thích lên hình.
   Đo thật kho hiện tại: `pd` 653 cảnh · `permissive` 671 · `all` 701 → siết chặt gần như không mất gì.
3. Nguồn: **NASA** (public domain, nhanh) + **Wikimedia Commons** (giấy phép từng file).
   Internet Archive ~2,5 MB/phút — quá chậm.
4. **Nguồn thứ tư — PHIM TƯ LIỆU YouTube Creative Commons** (`pipeline/yt_stock.py`, 2026-09-23):
   NASA/Wikimedia/Pexels không có phim thời sự 1940s–1970s, YouTube thì nhiều. Cách dùng + bẫy:
   **`docs/HUONG_DAN_YT_STOCK.md`**. Chỉ tải video `license` đúng chuỗi CC BY (máy kiểm, không
   phải khuyến nghị), bắt buộc ghi nguồn, và luôn `--crop-bottom` vì clip YouTube hay có chữ ở đáy.

⚠️ **Wikimedia trả 429 khi tải dồn** (đo thật: một lượt B5 tải về **0 file** mà không báo hỏng —
kho vẫn "đủ" nhờ file cũ nên lỗi này âm thầm làm nghèo kho qua từng tập). `stockfetch.py` nay có
User-Agent mô tả được + nghỉ 0,5s/file + thử lại 3 lần theo `Retry-After` cho **cả HEAD lẫn GET**
(vá HEAD không thôi vẫn mất 1/3 file).

## 6a. ⭐ B5K + B5A — KHỚP HÌNH VỚI LỜI, VÀ VẼ BÙ CHỖ KHO KHÔNG CÓ (dựng 2026-09-11)

Chuỗi làm hình có **3 khâu**, hỏng khâu nào cũng ra "hình một đằng lời một nẻo":

| Khâu | Hỏng thế nào | Chữa bằng |
|---|---|---|
| từ khoá → clip | Pexels là kho đời thường: tìm thứ nó không có, nó vẫn trả về thứ gì đó | `soi_kho.py` cấm file lạc · **B5A** vẽ bù |
| clip → câu | `chon_nguon()` chọn theo "ít dùng nhất + đủ dài" — **nội dung clip không tham gia quyết định** | **B5K** (`khop_hinh.py`) |
| cảnh → ghép | — | `stock_cut.gan_anh_ai()` |

**Đo thật tập 3 trước khi có 2 bước này: 43/141 cảnh (30%) lạc hẳn lời**, mà B8Q báo 0 vấn đề.
`area 51 sign nevada` → phố Las Vegas · `japan military base fence gate` → cổng torii đền thờ ·
`polygraph test machine` không có tấm nào đúng. Chấm lại cả kho bằng vision: **32% file lạc đề tài**.

- **B5K** gom cue thành đoạn ~15 giây, mỗi đoạn một từ khoá hình, kèm nhãn `CU_THE` / `KHONG_KHI`
  và prompt tiếng Anh. Ghim theo **mốc thời gian**, không theo chỉ số cảnh → dựng lại vẫn dùng được.
- **B5A** (`sinh_anh_canh.py`) **chỉ vẽ đoạn `CU_THE`**. Đoạn `KHONG_KHI` (sa mạc, trời đêm,
  đường vắng) để kho lo — clip thật bao giờ cũng hơn ảnh vẽ vì có chuyển động. Vẽ tất là đốt tiền
  để đổi lấy hình xấu hơn. `--theo-qc` chỉ vẽ đoạn ĐÃ CHỨNG MINH là hỏng; `--uoc-tinh` báo tiền
  trước; chạy bù không vẽ lại ảnh đã có.
- **Mọi ảnh AI mang nhãn 「イメージ（再現）」.** Ảnh vẽ trông như ảnh chụp thật mà nội dung là lời
  khai chính tập này bác bỏ — bỏ nhãn là đúng thứ chính sách "nội dung không trung thực" 2026
  nhắm tới. Dán cho MỌI ảnh AI, không chọn lọc từng cảnh. Ảnh **bằng chứng** không bị đụng tới.
- Tiền đo thật: 88 ảnh cho 10 phút = **4.400đ** (gpti2 low, prompt tiếng Anh).

⚠️ **Bug đã vá — dẫn nhập bị bỏ sót:** vòng lặp chương lấy `t_dau = bien[ch+1]` mà `bien[0]` mới
là mốc dẫn nhập → khoảng `[0 → 第1章)` không thuộc chương nào, **81 giây mở đầu chưa bao giờ được
khớp hình** nên rơi xuống tầng bốc theo chương. Đã thêm hàng rào: đoạn khớp đầu tiên nằm sau giây
20 thì in cảnh báo.

## 6b. ⚠️ CHẤT LƯỢNG B-ROLL — thứ bộ lọc giấy phép KHÔNG bắt được

B-roll của ngách này **được phép không minh hoạ lời** (kênh mẫu cũng vậy), nhưng **không được mang
CHỮ của một câu chuyện khác**. Đo thật ở tập 1: một cảnh rơi trúng **biểu đồ El Niño của NOAA** có
dòng *"to produce a forecast for the next 9 months"* nằm giữa video kể về đa vũ trụ; và một tấm
biển đường **"Everett Square, Massachusetts"** lọt vào chỉ vì trùng chữ "Everett" với tên nhà vật lý.

Nguồn của lỗi: thư viện NASA lẫn rất nhiều video **dạng chương trình** (NASA Science Live, bản tin
tuần, họp báo, giới thiệu sứ mệnh) — người nói + đồ hoạ + chữ tiếng Anh cháy sẵn.

Đã dựng: `stock_cut.CAM_TIEU_DE` (chặn dạng chương trình) + `body.title_blocklist` của profile
(chặn biển hiệu/biểu đồ/giấy chứng nhận). Đo thật: loại 15 file, sức chứa vẫn dư.

**Giới hạn phải biết:** bộ lọc này chỉ đọc TIÊU ĐỀ. Thứ có chữ mà tiêu đề không nói ra thì vẫn lọt.
Muốn chắc thì cần một lượt **soi ảnh bằng vision cho cả kho MỘT LẦN** (mỗi file 1 khung, chấm
"có chữ / đồ hoạ / người nói không", ghi vào sổ) — làm một lần dùng cho mọi tập sau.

## 6c. ĐỘ NÉT & SẠCH HÌNH — 4 bộ lọc kho tư liệu (đo thật 2026-09-10)

Anh xem bản đầu và nói *"ảnh hơi cũ mờ"*. Truy ra **không phải tại nguồn cũ — tại chính tool tải**:
`stock_sources.nasa()` xếp hạng ưu tiên bản **NHỎ NHẤT** (`mobile`) để né tải nhầm bản `~orig` 5,4 GB.
NASA `~mobile` = **320×180**. Phóng lên 1920×1080 là **upscale 6×**. Đo thật: **73% thời lượng video**
dựng từ clip 320×180.

→ Đổi ưu tiên thành `large > medium > small > mobile` (`~orig` vẫn xếp cuối; trần dung lượng + chốt
tốc độ ở `stockfetch.py` đã đủ chặn file khổng lồ). Tải lại: clip mới ra **1920×1080 / 1280×720**.

Bốn bộ lọc trong `stock_cut.nap_kho()` — mỗi cái sinh ra từ một lỗi đã thấy trên bản dựng:

| Bộ lọc | Ngưỡng | Sinh ra từ |
|---|---|---|
| `min_height` | video ≥720p · ảnh ≥540p | clip 320×180 phóng 6× ⇒ nhoè, không AI nào cứu |
| `min_luma` | ≥20/255 | B8Q báo "KHUNG ĐEN 964s" — hoá ra là clip **nguyệt thực**, nội dung thật nhưng 4,6 giây gần như đen. Đo 11 clip: tối nhất 13,6–14,0 · kế tiếp đã 27,5 ⇒ khoảng trống rõ, chọn 20 |
| `title_blocklist` | tên dạng chương trình/biển hiệu | biểu đồ El Niño của NOAA có chữ tiếng Anh; biển đường "Everett Square" |
| `BIEN_DAU/BIEN_DUOI` | cắt 6s đầu · **9s đuôi** | clip NASA gắn **thẻ thương hiệu** (logo NASA + "GODDARD SPACE FLIGHT CENTER" + URL) ở CUỐI. Đo thật: một cảnh rơi vào giây 115,8 của clip dài 119,9s ⇒ lên hình nguyên tấm thẻ. Sau khi sửa: cảnh rơi vào 6 giây đầu clip **32 → 4** |

> **Logo của đài khác nằm trong video mình còn tệ hơn cả nhoè** — vừa lạc đề vừa trông như ăn cắp.

### ❌ KHÔNG dùng AI làm nét
Hỏi đúng thì câu trả lời là **sửa nguồn, không phải sửa ảnh**:
- 320×180 phóng 6× thì AI chỉ **bịa** chi tiết chứ không khôi phục — mà kênh này bán chữ *bằng chứng*.
- **Tuyệt đối không AI-upscale ẢNH BẰNG CHỨNG.** Đưa ra một tấm ảnh đã bị máy vẽ thêm rồi nói
  "đây là ảnh NASA" là tự tay phá đúng thứ mình đang xây.
- Tải đúng bản `~large` là **miễn phí và có chi tiết THẬT**. Đó mới là cách làm nét.

## 6d. ⛔ MÁY 2 VẼ ẢNH BẰNG GOOGLE FLOW — CHẠY `--den B5K` RỒI DỪNG (từ 2026-09-12)

Lane này không gọi gpti2 nữa; máy 2 vẽ bằng Google Flow, 0đ. Nhưng `b5a_anh_canh()` vẫn tự gọi
`sinh_anh_canh.py` **có tính tiền** nếu để pipeline chạy thẳng — một tập ~300 ảnh × 50đ, tiêu tiền
cho đúng thứ bên kia đang vẽ miễn phí, mà chạy xong mới biết. Nên mỗi tập chạy hai chặng:
```
py -3.13 pipeline\make_video.py --profile toshi-densetsu-jp --slug ep<nn>-<slug> --den B5K
py -3.13 pipeline\tim_anh_that.py --slug <thư mục tập>                   (đổi CU_THE→clip thật, xem dưới)
py -3.13 pipeline\sinh_anh_canh.py --slug <thư mục tập> --chi-don        (ra đơn, không vẽ)
py -3.13 pipeline\qc_can_anh.py --folder "<thư mục tập>"                 (cổng trước khi giao)
py -3.13 pipeline\drive_handoff.py upload-job ep<nn>-<slug> "<thư mục tập>\img_ai"
py -3.13 pipeline\ghi_don_buoc3.py --tab A-shinya_shiryoshitsu --dong <nn>   ← ĐƠN BƯỚC 3 vào cột H
   … máy 2 vẽ ảnh, đổi cột F thành "Img done" …
   … agent bước 3 đọc cột H rồi tự làm nốt — tab này KHÔNG chạy `--from B8` nữa …
```

**`tim_anh_that.py` (mới 2026-09-16, chạy NGAY SAU `--den B5K`, TRƯỚC `sinh_anh_canh.py`).** B5K
gắn nhãn `CU_THE` THUẦN NGỮ NGHĨA — không hề thử tìm kho thật trước khi kết luận "phải vẽ AI". Đo
thật ep05/ep06: 63% đoạn `CU_THE` (vd "tượng Pikachu", "ảnh báo cũ", "màn hình tivi nhiễu") thật ra
Pexels có sẵn, chỉ là chưa ai tìm. Tool này tự tìm Pexels cho từng `query` của đoạn CU_THE, chấm
điểm liên quan bằng **gemini-3.8-flash qua ramclouds** (`soi_kho.cham()` — **BẮT BUỘC dùng model
này, Claude không tự phán xét liên quan**), khớp thì tải về `stock/` + ghi `manifest.jsonl` + đổi
`loai` đoạn đó thành `CU_THE_DA_TIM_DUOC` (để `sinh_anh_canh.py` bỏ qua, không vẽ AI nữa). Tự sao
lưu `khop_hinh.json`+`manifest.jsonl` vào `_truoc_khi_sua/` trước khi sửa. Verify thật ep06: 254→60
ảnh AI (giảm 76%). Không có `--thu` (dry-run) thì chạy thật luôn; muốn xem trước thêm `--thu`.

⚠️ Nếu tool này chạy SAU KHI đã có đơn `img_ai/img_meta.json` cũ (vd đã ra đơn trước khi nhớ chạy
tool này) — `sinh_anh_canh.py --chi-don` sau đó sẽ KHÔNG tự rút gọn đơn cũ (nó chỉ cộng thêm đoạn
thiếu, không bỏ đoạn thừa). Phải xoá `img_ai/img_meta.json` (đặt lại `[]`) + `img_ai/prompts.txt`
rồi chạy lại `--chi-don` từ đầu để đơn khớp đúng danh sách CU_THE đã rút gọn (đã dính thật ở ep06:
đơn cũ 254 ảnh cho 64 đoạn còn giữ nguyên dù `khop_hinh.json` đã rút xuống 15 đoạn).

`upload-job` nhận **`<thư mục tập>\img_ai`**, KHÔNG nhận thư mục tập — nó đi đệ quy cả cây nên trỏ
sai cấp là đẩy luôn kho clip vài GB lên Drive, âm thầm (đã dính thật, xem `docs/GIAO_VIEC_MAY2_ANH.md`
mục 4).

**⭐ LANE NÀY LUÔN DÙNG gpti2 CHO BƯỚC 2, KHÔNG CẦN MÁY 2/FLOW NỮA (anh chốt 2026-09-17, thay quy
tắc ngưỡng 50 ảnh cùng ngày).** Lane A **không có REF-LOCK** (`image.ref_lock: false`, không nhân
vật lặp lại) — đây là lý do gpti2 luôn rẻ ở đây (~50đ/ảnh, không cộng phụ phí ref 60đ/ảnh như lane
REF-LOCK), nên **không còn lý do phải chờ người vẽ tay bằng Google Flow**, kể cả khi số ảnh cao.
Áp dụng **từ tập SAU trở đi** (tập nào đã giao máy 2 theo quy trình cũ trước mốc này thì giữ nguyên,
không rút lại). Máy 2 giờ CHỈ còn vai trò chạy tool tự động (bước 2+3 gộp, xem §8f) — không còn thao
tác Flow bằng tay cho lane này nữa.

⚠️ Bẫy tiền đã bịt 2026-09-12: `--from B8` không xoá B5A khỏi state, nhưng tập nào dừng ở
`--den B5K` thì state **chưa từng có** B5A ⇒ `skip()` trả False và B5A lặng lẽ vẽ lại ~300 tấm máy 2
vừa vẽ xong (~15.000đ/tập). Nay `b5a_anh_canh()` đọc ĐĨA làm nguồn chân lý: đủ ảnh theo
`img_meta.json` thì ghi state và bỏ qua; thiếu ảnh thì **dừng hẳn**, không vẽ bù.

## 7. B7 — THUMBNAIL (chỗ DUY NHẤT dùng ảnh AI)

### ⭐ MÔ-TÍP KHOÁ CHO CẢ KÊNH (user chốt 2026-09-10)
Thumbnail của một kênh phải nhận ra được ngay từ xa: **cùng bố cục, cùng bảng màu, cùng số tầng
chữ — mỗi tập CHỈ đổi ẢNH và CHỮ.** Thả cho AI tự chọn thì mỗi tập một kiểu, lướt trang kênh trông
như 20 người khác nhau cùng đăng.

Khoá trong `profile.thumbnail`:

| Field | Vai trò |
|---|---|
| `art_style` | phong cách nền CỐ ĐỊNH, ghép vào prompt của mọi tập |
| `template.tiers` | đúng 2 tầng: `YELLOW` = tiền đề (≤12 ký tự) · `RED` = cú sốc (≤14 ký tự) |
| `template.side_width` `wrap` `max_font` | bố cục: chữ dồn TRÁI 68% khung, ngắt dòng cân đối, trần 150px |
| `require_face: false` | ngách này 11/12 thumbnail top KHÔNG có mặt người |

Mỗi tập chỉ cần **`thumb_bg_subject.txt`** — MỘT DÒNG tả chủ thể (vd *"two identical human
silhouettes seen from behind across a mirrored cosmic divide"*). B7 tự ghép
`art_style + chủ thể + câu chừa chỗ cho chữ`. Muốn phá lệ cho một tập thì viết tay
`thumb_bg_prompt.txt`, B7 sẽ giữ nguyên file đó.

`ai_steps.write_thumb_text` cũng đọc `template.tiers` để ra ĐÚNG số dòng và ĐÚNG màu — không còn
tự đẻ thêm dòng BANNER.

9 quy tắc rút từ 12 thumbnail top: **2 tầng chữ** (trên nhỏ vàng = tiền đề · dưới TO NHẤT đỏ viền
đen dày = cú sốc) · chữ chiếm **30–50% khung** · nền **tối** · chỉ **đỏ + vàng + trắng** · ảnh AI
cinematic **không mặt người thật** · `●●` che đáp án hoặc `「」` trích lời · mũi tên đỏ nếu cần chỉ.
Chữ overlay bằng `thumbnail_text.py` (PIL) — **KHÔNG nhờ model render chữ**.

Ba thứ đã sửa để B7 chạy đúng cho lane này (đừng gỡ):
- **`thumb_bg_prompt.txt` viết tay được** — B7 giữ nguyên nếu file đã có. Ngách này không có nhân
  vật để chụp chân dung; nền là một CẢNH, mỗi tập một cảnh, không sinh máy móc từ profile được.
- **`thumbnail.require_face: false`** — cổng QC cũ đòi "phải thấy mặt người có cảm xúc", tức là
  đánh trượt đúng công thức của ngách (11/12 thumbnail top KHÔNG có mặt người).
- **`thumbnail.wrap: true` + `max_font: 150`** — luật ngách là chữ phủ **30–50% khung**. Chế độ cũ
  ép cả câu vào MỘT hàng nên tự thu nhỏ còn 48px ≈ **8% khung**: làm ngược công thức mà không cổng
  nào bắt, vì chữ vẫn "đọc được". Ngắt dòng **cân đối** (không phải tham lam) để khỏi đẻ ra hàng
  mồ côi một ký tự như 「物理学者が認め / た」.
- Chữ do AI viết phải **soi lại**: bản đầu tự đẻ ra `抹殺された天才物理学者` (nhà vật lý bị thủ tiêu)
  trong khi kịch bản nói rõ Everett chết vì nhồi máu cơ tim. Nay `ai_steps._thumb_rang_buoc()` cấm
  thêm cái chết bí ẩn / âm mưu không có trong kịch bản — nhưng vẫn phải đọc lại bằng mắt.

Prompt nền (gpti2, landscape 3:2 — **đừng xin 16:9**, xem `dl_img_pa3.md`: khung lệch tỉ lệ làm
model kéo giãn chủ thể):
```
Cinematic dark space scene, dramatic volumetric lighting, deep navy and black background with
subtle nebula glow, high contrast, photorealistic, 8k, [CHỦ THỂ], empty space on upper-left and
lower-half for text overlay, no text, no watermark, no people's faces in focus
```

## 8. B8 — GHÉP (`stock_cut.py`)

Tự chạy khi `body.mode = "stock_clips"`. Ba việc nó làm mà ghép tay không làm nổi:
1. **Mốc cắt hút về ranh giới câu SRT** (±1,2s) — cắt tuỳ tiện giữa câu làm hình và lời lệch pha.
2. **Không lặp hình lộ liễu**: trần dùng lại theo độ dài file · cấm lặp trong 25 cảnh gần nhau ·
   mỗi lần dùng lại lấy **đoạn khác** bên trong file (chọn điểm vào xa các điểm đã dùng nhất).
3. **`credits.txt` + `scenes.json`**: sổ nguồn từng file để dán mô tả video và truy ngược khi bị
   khiếu nại.

Verify 2026-09-10: 29,1 phút → **403 cảnh = 13,9 cắt/phút** (mục tiêu 12–16), dài TB 4,3s, 53 file;
render 60 giây thử = 14 cảnh trong 4 giây, ra 1920×1080 h264 + AAC, khớp đúng độ dài tiếng.

### ⭐ ẢNH BẰNG CHỨNG — chỗ thắng kênh mẫu
Hai comment nhiều like nhất trong nhóm phản biện của kênh mẫu đều **đòi tấm ảnh mà video đã hứa**
(`その写真をアップロードしてください` 86👍 · `提供出来ないなら、番組とは呼べない` 55👍). Họ nói mà không
đưa được bằng chứng hình.

→ Đặt `evidence.json` trong thư mục tập:
```json
[{"at": "12:30", "sec": 8, "file": "nasa_PIA17449.jpg",
  "caption": "出典: NASA/JPL-Caltech（パブリックドメイン）"}]
```
`stock_cut.py` ghim đúng file đó vào đúng giây, cháy dòng chú thích nguồn lên đầu khung. Mỗi video
nên có **2–4 mốc** như vậy, đặt ngay sau câu vừa nêu bằng chứng.

Ba luật của ảnh bằng chứng:
1. **Chỉ Public Domain** (`evidence_license_policy: "pd"`) — tool tự từ chối file SA/NC/ND và file
   không có trong `manifest.jsonl`.
2. **Chú thích phải đúng sự thật.** Nếu chỉ có ảnh minh hoạ chứ không phải ảnh gốc thì ghi rõ
   「イメージ図」. Đưa ảnh minh hoạ mà nói như ảnh gốc là tự tay đưa cho nhóm phản biện thứ họ đang
   tìm — tệ hơn cả không đưa ảnh.
3. Tìm mốc bằng SRT: `grep` từ khoá (tên người, năm, địa danh) trong `voice.srt` rồi lấy timestamp.

⚠️ **KHÔNG dùng `drawtext` của ffmpeg để ghi chú thích.** Đường dẫn Windows chứa dấu `:` của ổ đĩa,
trùng dấu ngăn tham số của ffmpeg; mọi kiểu escape đều ra `Error parsing a filter description`
(exit −22) và nó **giết cả lượt render 409 cảnh vì một dòng chữ**. `stock_cut.anh_caption()` vẽ dải
chú thích bằng PIL rồi `overlay` — không escape, không phụ thuộc fontconfig. Máy này **không có**
`meiryo.ttc`; font thật là `YuGothB.ttc` / `msgothic.ttc`.

## 8a. ⭐ B8Q — CHẤM TỪNG CẢNH (`qc_canh.py`), KHÔNG LẤY MẪU

**Bài học đắt nhất của lane này.** `b8q_qc()` từng có đoạn code ghi rõ: *"lane clip stock: hình
là B-roll trang trí, CỐ Ý không minh hoạ lời đang đọc → chấm khớp lời là chấm sai đề"*, rồi
truyền `srt=None`. Giả định đó sai, và vì nó **nằm trong cổng** nên không cổng nào bắt được: tập
3 đi hết pipeline với **43/141 cảnh (30%) lạc hẳn lời**, B8Q báo 0 vấn đề.

Hai tầng lỗi độc lập:
1. Giả định sai được viết thành code kèm chú thích nghe rất thuyết phục ("đo thật ở kênh mẫu")
   mà **không có số liệu kèm theo**. Chú thích càng tự tin càng khó nghi ngờ.
2. Lấy mẫu **12/400 mốc = 3%**. Cổng lấy mẫu trả lời được *"video có hỏng toàn tập không"*,
   KHÔNG trả lời được *"cảnh nào hỏng"*.

Nay lane stock chấm bằng `qc_canh.py`: soi **100% số cảnh**, mỗi cảnh một khung hình + đúng câu
đang đọc lúc đó. Trần lạc ở `profile.assemble.lac_toi_da` (0.03 — đo được sau 4 vòng sửa ở tập 3;
đặt 0 thì không bao giờ dừng vì bộ chấm cũng chặt tay ở vài cảnh đúng).

**Vòng phản hồi:** `--cam-file-lac` đẩy file đã chứng minh là lạc ngược vào `soi_kho.json` của
kho, lần dựng sau không bốc lại. Cấm dè dặt: **lạc ≥1 lần VÀ chưa từng được chấm đúng**.

⚠️ **Thang chấm phải bắt model chỉ ra BẰNG CHỨNG.** Bản đầu hỏi "hình có khớp không" kèm 3 bậc tả
bằng tính từ → **140/141 cảnh rơi vào bậc giữa**, kể cả 24 cảnh dùng ảnh vẽ từ chính câu đó; và
`soi_kho.py` cũng dính y hệt (243/248 file cùng một bậc). Chữa: bắt điền `khop_voi` = từ nào trong
câu ứng với thứ nhìn thấy, rồi **code tự hạ bậc** nếu ô đó trống. Luôn giữ một **nhóm đối chứng**
đã biết trước đáp án (ảnh vẽ từ chính câu đó phải sạch) — không sạch nghĩa là thang vẫn hỏng.

## 8b. SỔ SẢN XUẤT VIDEO 1 — số đo thật (2026-09-10)

Tập `ep01-tagen-uchu` (多元宇宙), đã dựng xong end-to-end:

| | |
|---|---|
| Kịch bản | **11.315 chữ**, 5 chương, gate ĐẠT, 0 lỗi số học |
| Giọng | 29:30 (1770,3s) · đỉnh sau chuẩn hoá −1,8 dB · SRT 517 cue, phủ 100% kịch bản |
| Hình | **408 cảnh · 13,8 cắt/phút · 73 file khác nhau · 9 cảnh bằng chứng** |
| Video | 1920×1080 h264 + AAC · 768 MB · B8Q ĐẠT (0 vấn đề) |
| Chi phí hình | **0đ** (NASA + Commons) + 1 ảnh AI cho thumbnail |
| Thời gian | B3 ~6' · B3Q ~2' · B4 ~1,5' · B5 ~7' (tải tư liệu) · B7 ~1' · **B8 ~10'** → **~28 phút máy** |

Nguồn tư liệu của tập: `competitor.txt` = câu chuyện 1 của video 98.898 view (`HqaY3BLROJU`,
cắt tại mốc 1851s nơi 第1章 khởi động lại) làm KHUNG KỂ · `series_ctx.txt` = dữ kiện thật về
多世界解釈 (Young 1801 · Tonomura/日立 1989 · Everett 1957 · DeWitt 1970 · 華厳/唯識).

**QC đã bắt được một lỗi bịa thật:** model tự đặt phòng thí nghiệm Tonomura ở hai nơi khác nhau
(埼玉県 ở chương 1, 東京の西 ở chương 4) vì `series_ctx.txt` không ghi địa điểm. → Tư liệu thiếu chỗ
nào, model sẽ tự điền chỗ đó. Viết tư liệu càng kín, càng ít phải sửa.

## 8c. B9 — HAI FILE ĐĂNG TẢI

| File | Dùng để làm gì |
|---|---|
| **`TIEU_DE_MO_TA.txt`** | **DÁN THẲNG** vào form YouTube. Quy cách cố định: tiêu đề → 5 từ khoá SEO (nối bằng dấu phẩy, KHÔNG cách) → mô tả ngắn → gạch ngang → `Timestamps:` → gạch ngang → câu cảm ơn → gạch ngang → hashtag |
| `DANG-TAI.txt` | phần còn lại: 3 tiêu đề gợi ý, thẻ đầy đủ, danh mục, bình luận ghim, checklist form |

Hai luật đã phải vá sau tập 1:
1. **`title.txt` thắng AI.** Tiêu đề đã chốt tay (đúng công thức 30–45 ký tự + khối tag SEO) đặt ở
   `title.txt` trong thư mục tập; B9 đẩy nó lên đầu. Không có file thì AI tự đặt — và nó sẽ bỏ mất
   khối `【都市伝説 ミステリー 怖い話】`.
2. **Mốc chương bám LỜI ĐỌC, không chia đều thời lượng.** Bản chia đều ra 7 mốc và AI đặt tên
   第1章…第7章 — trong khi video chỉ có 5 chương và nói 第4章 ở **19:31**, mô tả lại ghi 12:39.
   Người xem bấm vào là thấy sai ngay, mà đó đúng là nhóm khán giả soi kỹ nhất của ngách.
   Nay `_chuong_theo_marker()` dò `第◯章` trong SRT rồi lấy tên chương đầy đủ từ kịch bản.

## 8d. B10 — ⭐ NGHIỆM THU TOÀN TẬP (`qc_final.py`)

B8Q chỉ hỏi *"bản ghép có ổn không"*. B10 hỏi **"bộ này đăng lên được chưa"** — soi GÓI GIAO, tất
định và miễn phí. Bảy thứ nó bắt mà mọi cổng trước đều mù:

| Kiểm | Vì sao chết người |
|---|---|
| Ảnh bìa ≤ **2 MB**, ≥1280×720, đúng 16:9 | vượt 2 MB là YouTube **không nhận**, phát hiện lúc đang đăng |
| Tiêu đề trong dải `gate.title_len` + ≤100 ký tự | lệch dải 30–45 ⇒ view thấp hơn **2,4 lần** (số đo ngách) |
| Mô tả ≤5.000 · chuỗi thẻ ≤500 | vượt là YouTube **cắt cụt lặng lẽ** |
| Mốc chương: mở bằng **0:00** · ≥3 chương · cách nhau ≥10s · không vượt độ dài | sai một điều là YouTube **bỏ TOÀN BỘ chương**, không báo gì |
| Phụ đề đã **CHÁY** vào hình chưa | quên burn-in là lỗi câm hoàn hảo: mp4 vẫn chạy, B8Q vẫn ĐẠT |
| `credits.txt` phủ hết file đã dùng | thiếu là không truy ngược được khi bị khiếu nại |
| B3F còn lỗi nặng không, **và kết quả B3F có còn mới không** | xem dưới |

> ⚠️ **Kết quả QC cũ hơn kịch bản = số ảo.** Ngay lần chạy đầu, B10 báo *"B3F còn 3 chi tiết không
> có trong tư liệu (vd 埼玉県)"* — trong khi kịch bản đã bỏ chữ đó từ lâu, chỉ là `qc_facts.json`
> còn nằm đó từ lượt cũ. Nay B10 so `mtime` của `script.txt` với `qc_facts.json`; cũ hơn thì báo
> **nặng** và bắt chạy lại, chứ không đọc số cũ rồi tưởng là hiện trạng.

Cách kiểm phụ đề: lấy mốc GIỮA cue (lúc chắc chắn đang có lời), đo dải 25% đáy khung, đếm điểm ảnh
>235. Chữ trắng viền đen nên ngưỡng đó tách sạch khỏi nền.

**Đã thử chiều ngược lại** (cổng phải bắt được lỗi, không chỉ đóng dấu): 6/6 gói hỏng bị chặn đúng
— chương đầu ≠0:00 · hai chương cách 5s · chương vượt độ dài · tiêu đề 105 ký tự · chỉ 2 chương ·
thiếu từ khoá SEO. Gói đúng: 0 phát hiện.

Chạy riêng: `py -3.13 qc_final.py --slug <thư mục tập> --profile <id>`

## 8e. LANE NÀY CHIA 3 BƯỚC — BƯỚC 3 GIAO CHO AGENT KHÁC (anh chốt 2026-09-12/16)

**⚠️ Đã có ngoại lệ mới — đọc §8f trước khi áp dụng nguyên văn mục này.** §8e mô tả mô hình CŨ (giao
máy 2/agent khác). Từ 2026-09-21 anh đã cho phép tab Lane A **tự làm luôn bước 2+3** (xem §8f) — mô
hình giao việc dưới đây vẫn là LỰA CHỌN HỢP LỆ (vd khi muốn chạy song song, tách khỏi máy 1), không
phải đã lỗi thời, nhưng không còn là ĐƯỜNG DUY NHẤT nữa.

**Bước 1** (tab này): tư liệu → kịch bản → giọng → khớp hình → ra đơn ảnh, dừng ở `--den B5K`.
**Bước 2**: máy 2 vẽ ảnh qua Google Flow. **Bước 3**: agent riêng (hiện là deepseek) tải ảnh về,
ghép, chấm cảnh, giao hàng, ghi cột G. Hồ sơ giao việc bước 3 — tự chứa, có lệnh copy-paste, sổ xử
lý khi rớt cổng, checklist: **`docs/GIAO_VIEC_BUOC3_AGENT.md`**. Tab này **không làm bước 3 nữa**
trừ khi anh bảo; nhưng vẫn là nơi sửa code/pipeline khi bước 3 báo lỗi hạ tầng.

⚠️ Nguyên tắc "Claude chỉ làm Bước 1, cấm render/ghép video" nay là **luật TOÀN DỰ ÁN** — xem
`CLAUDE.md` mục "⛔ CẤM TUYỆT ĐỐI" để có văn bản đầy đủ (mốc dừng chính xác, hình phạt vi phạm cụ
thể). Phần dưới đây chỉ là bổ sung RIÊNG cho lane này — phân việc nào giao được subagent Haiku:

- **Có thể giao cho subagent (đã verify 2026-09-16, xem memory `phan-tang-model-haiku-buoc1`):**
  B4 (TTS)/B4Q/B5 (tải+soi kho)/B5K (khớp mốc chương), và đoạn giao việc B5A-đơn → cổng
  `qc_can_anh.py` → `drive_handoff.py upload-job` → `ghi_don_buoc3.py` — đây là việc CƠ KHÍ (chạy
  lệnh → đọc số liệu → đi tiếp), Haiku làm tốt khi có lệnh rõ ràng, dặn thêm "dùng
  `TaskOutput(block=true)` đợi lệnh nền xong, đừng coi bắn lệnh nền là xong việc".
- **PHẢI giữ ở tầng người/Sonnet-Opus, không giao Haiku:** B2 (đọc hồ sơ, sửa lỗi định dạng) · B3
  (viết kịch bản) · B3Q (QC nội dung, sửa lặp ý/logic) · B3F (kiểm dữ kiện, quyết định bỏ/sửa chi
  tiết không nguồn) · B7 (duyệt/soát thumbnail) — đây là chỗ cần phán xét đúng/sai, không phải chạy
  lệnh đọc số.
- **B5A (`sinh_anh_canh.py` không có `--chi-don`) và mọi lệnh sinh ảnh AI trả tiền: KHÔNG BAO GIỜ
  chạy trong lane này** kể cả bằng subagent — máy 2 vẽ ảnh 0đ, xem hàng rào tiền đã dựng ở §6d.

### Bàn giao qua 1 file txt + cột H trỏ tới nó

Anh không ngồi giao việc thủ công. Xong bước 1 chạy:
```
py -3.13 pipeline\ghi_don_buoc3.py --tab A-shinya_shiryoshitsu --dong <nn>
```
Nó làm 2 việc: (1) dựng **`CLAUDE-DEEPSEEK.TXT`** ở gốc dự án — PHẦN 1 việc phải làm ngay (thư mục
tập, số ảnh, 5 lệnh, ngưỡng cổng, danh sách CẤM) + PHẦN 2 toàn văn `docs/GIAO_VIEC_BUOC3_AGENT.md`;
(2) ghi **cột H** đúng một dòng: `Claude trả lời Deepseek <hh:mm>: vào kiểm tra câu trả lời tại
<đường dẫn>`. Anh chỉ báo Deepseek đọc cột H. **Ô trang tính chỉ là biển chỉ đường, nội dung nằm
trong file** — dán cả đơn vào ô thì phải kéo mới đọc hết và không copy lệnh ra được.

Thân file lấy THẲNG từ file `.md` (một nguồn chân lý, sửa `.md` rồi chạy lại tool), mọi con số tra
từ profile + đĩa chứ không gõ tay. Tool chỉ ghi được **đúng cột H**, tự bỏ qua dòng đã giao video
hoặc bước 1 chưa xong, làm mới tự do ô do chính nó ghi nhưng **không đè ghi chú của người** trừ
`--ghi-de`. Cặp tool ghi sheet có rào chắn: `ghi_don_buoc3.py` (cột H) · `ghi_cot_video.py` (cột G)
— **đừng ghi tay bằng MCP nữa**, rào nằm trong tool chứ không nằm trong trí nhớ.

### Số tập lấy từ trang tính, KHÔNG đếm theo thứ tự làm (anh chốt 2026-09-11)

Hồ sơ nghiên cứu nằm ở `_READY\<nn>-<slug>`, `<nn>` chính là **STT dòng** trong tab kênh của trang
tính → thư mục tập trong `assets/` và thư mục giao hàng đều phải là `ep<nn>-<slug>`. Đã lệch một
lần: `01-valentich` (STT 1) bị đặt thành `ep02-valentich` vì nó là tập thứ HAI được dựng, còn `ep01`
đã bị một đề tài ngoài danh sách chiếm chỗ — nhìn thư mục không truy ngược được dòng nào nữa. Đề tài
**không có trong trang tính** (tập thử trước khi có quy trình nghiên cứu) đánh số `ep00`. **Tên thư
mục giao hàng dùng slug CHỮ LATIN** (`ep03-bob-lazar`), không dùng tên tiếng Nhật — anh gõ đường
dẫn tay để vào lấy file. Tên tiếng Nhật vẫn nằm trong `listting.txt`/`tomtat.txt`.

**Dựng xong một tập = luôn làm đủ hai việc, không đợi anh nhắc (anh chốt 2026-09-12):**
1. **Ghi đường dẫn thư mục giao hàng vào cột `G` (VIDEO)** đúng dòng STT của tập đó.
2. **Đưa anh đường dẫn thư mục đó** trong câu trả lời, để anh mở ra listing lên YouTube.

⚠️ Cột đã đổi chỗ: tab kênh nay là `A STT · B ĐỀ TÀI · C NỘI DUNG · D TÌNH TRẠNG · E FOLDER ·
**F STATUS-IMG** · **G VIDEO**`. Trước 2026-09-12 cột VIDEO nằm ở F — **đọc lại header trước khi
ghi**, đừng ghi theo trí nhớ, kẻo đè lên trạng thái ảnh của máy 2. Chỉ ghi khi **B11 đã giao xong
thật** (file trong thư mục kênh mới hơn `final.mp4` của thư mục tập); chưa giao mà ghi là chỉ anh
vào thư mục rỗng hoặc bản cũ.

### Giao hàng (B11, tự động sau B10)

Mỗi tập xong, `pipeline/giao_hang.py` chép **đúng 3 file** sang
`E:\CLAUDE\YOUTUBE\CHANEL\<kênh>\ep<N>-<tên tập>\` — `final.mp4` · `thumbnail.png` · `listting.txt`
(tiêu đề + mô tả + mốc chương + hashtag + **khối ghi nguồn rút gọn**). Thư mục tập trong `assets/`
giữ nguyên mọi thứ khác (kịch bản, SRT, JSON QC, kho clip vài GB) — chỗ đó để dựng lại, chỗ kia để
đăng. Kênh khai ở `profile.publish.upload_channel`, nơi lưu ở `publish.upload_dir` — **đổi kênh là
sửa JSON, không sửa code**. Chạy sau B10 chứ không phải trước: thư mục giao hàng chỉ được chứa bản
ĐÃ NGHIỆM THU.

⚠️ `credits.txt` đầy đủ (36 KB / 241 nguồn) KHÔNG nhét vừa ô mô tả 5.000 ký tự của YouTube →
`listting.txt` chỉ chứa bản rút gọn theo đúng thứ luật đòi: **CC BY liệt kê từng tác giả** (3–6
file/tập), PD/NASA/CC0 và Pexels gộp mỗi loại một dòng. Sổ đầy đủ vẫn nằm trong thư mục tập.

## 8f. ⭐ NGOẠI LỆ TỰ RENDER — anh chốt 2026-09-21 (vụ sửa "rung giật")

Sau khi phát hiện + vá xong 2 lỗi thật (zoom hardcode phớt lờ `profile.assemble.zoom`, nhịp cắt
100% "cut" không đệm gây cảm giác giật) và bật `burn_subs=true`, anh yêu cầu Claude Code tự chạy
render thử tập 1 để kiểm — việc này đụng đúng luật cấm ở `CLAUDE.md`. Claude Code đã DỪNG lại hỏi
lại thay vì tự chạy, và anh xác nhận rõ 2 lần: **"với lane A này thì anh cho phép em được quyền tự
tải, tạo ảnh bằng gpti2 và chạy render video nhé, anh cho phép."**

**Phạm vi ngoại lệ (đọc kỹ trước khi dùng):**
- Chỉ áp dụng cho **lane `toshi-densetsu-jp` (Lane A)**, tab này. KHÔNG tự suy diễn sang lane khác —
  lane khác vẫn theo đúng luật CẤM ở `CLAUDE.md`, muốn xin ngoại lệ tương tự phải hỏi lại đúng tab đó.
- Được phép: `stockfetch.py`/`soi_kho.py` (tải+soi kho, vốn dĩ vẫn chạy trong Bước 1 từ trước) ·
  `sinh_anh_canh.py` (vẽ ảnh gpti2, KHÔNG cần `--chi-don` ra đơn cho máy 2 nữa) ·
  `make_video.py --from B8` trở đi (ghép, chấm cảnh, sinh gói đăng, nghiệm thu, giao hàng) — tức là
  TOÀN BỘ 3 bước giờ chạy được trong 1 tab.
- Đường máy 2 (§6d, §8e, `goi_buoc2_3.py`) **vẫn dùng được** — không phải đã gỡ bỏ, chỉ không còn là
  đường bắt buộc. Chọn đường nào tuỳ tình huống (máy 2 rảnh/máy 1 rảnh, muốn chạy song song nhiều tập).
- Tiền vẽ ảnh gpti2 (~50đ/ảnh) vẫn là TIỀN THẬT dù chạy trong tab này — vẫn áp đúng thói quen cũ:
  báo số ảnh + giá trước khi bấm vẽ loạt lớn, vẽ thử vài ảnh trước khi vẽ cả lô (xem memory
  `ve-thu-5-anh-truoc-khi-ve-loat`).
- Render xong 1 tập vẫn phải qua đủ B8Q/B10 như cũ — ngoại lệ chỉ bỏ rào "ai được BẤM nút chạy",
  không bỏ rào "phải qua cổng QC nào".

## 9. CHỈ SỐ CẦN ĐẠT (video 1)
≥5.000 view / 7 ngày · giữ chân 30 giây đầu ≥60% · ≥15 comment.
Retention của **đối thủ KHÔNG lấy được** (đã thử 4 client InnerTube + phiên Chrome đăng nhập) —
chỉ có retention video của chính mình trong Studio sau khi đăng. Mọi con số trong SOP này là
**quan sát tương quan**, chỉ sau 5 video đầu mới biết công thức nào thật sự có tác dụng.

## 10. 4 VIDEO TIẾP THEO (đã nghiên cứu sẵn)
1. `ヴァレンティッチ失踪` (cung 1 video/tháng · 7.382 view) — móc Nhật: 日航1628便 (1986)
2. `トラヴィス・ウォルトン` (trần đã chứng minh **111.873**) — móc Nhật: 神隠し
3. `ボブ・ラザー / エリア51` (27 video nhưng median **16.085** — cầu lớn nhất) — móc Nhật: 相模原
4. Video "日本だけが知っていた" tự tạo — dạng này của kênh mẫu đạt **101k**

## HOOK 20–30 GIÂY ĐẦU — CÁCH CỦA RIÊNG LANE NÀY

> ⚠️ Mỗi lane một kiểu hook khác nhau. **Đừng mượn cách của lane khác.**

| | |
|---|---|
| Kiểu mở (`script.hook.patterns`) | H42 H24 H25 H26 H39 |
| Câu khoá (`script.hook.closer`) | K13 |
| Cách dựng hình (`script.hook.visual`) | `tu_lieu_that` |
| Nguồn hình | **100% tư liệu thật** trong `stock\` của tập (clip Pexels/NASA + ảnh public domain) + 2 băng chữ vàng/đỏ lấy nguyên văn `thumb_text.txt`. CẤM ảnh AI, CẤM clip AI |
| Công tắc (`script.hook.enabled`) | **đang BẬT** |

Runbook dựng đầy đủ (7 bước + 4 phép kiểm trước khi ghép): `docs\QUY_TAC_VIDEO_HOOK.md`, bảng so sánh
cách dựng của mọi lane ở §5b. Nguyên tắc nội dung hook: `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

Viết hook: `py -3.13 pipeline\hook_stage.py --profile toshi-densetsu-jp --slug <tập> --mode repair`
