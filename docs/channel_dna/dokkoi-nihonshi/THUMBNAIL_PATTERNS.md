# THUMBNAIL PATTERNS — どっこい日本史 (kênh mẫu Lane I `sengoku-uragawa`)

> Lấp mục "Thumbnail patterns" mà `CHANNEL_DNA.md` tự khai **"không đủ dữ liệu"** (Channel Analyzer
> chỉ đọc transcript, không xem ảnh). Nguồn: **21/21 thumbnail thật** tải ngày 2026-09-23 về
> `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\_raw\thumbs\`
> (đặt tên `<hạng view>_<view>_<video_id>.jpg`), xem bằng mắt + đo dải màu bằng Pillow/NumPy.
> Mọi con số dưới đây là ĐO, không suy luận.

## 1. Phát hiện quan trọng nhất — KHÔNG PHẢI "chibi"
Tài liệu giao việc cũ (`FlowHandoff_local\shared\GIAO_VIEC_LANE_I.md`) và cửa vào
`docs\BAT_DAU_LANE\sengoku-uragawa.md` đều ghi format là **"manga chibi (nhân vật lịch sử dễ thương)"**.
Ảnh thật cho thấy **sai**: kênh dùng **manga seinen / anime lịch sử nghiêm túc** — mặt người lớn tỉ lệ
thật, nếp nhăn, lông mày rậm, nét viền dày, tô màu cel-shading đậm. Không hề có đầu to thân nhỏ,
không hề dễ thương. Biểu cảm luôn NẶNG: trừng mắt, nghiến răng, kinh hoàng toát mồ hôi, cam chịu.

→ **Phải sửa `image.style_suffix` và `thumbnail` trong profile theo mô tả này**, đừng viết "chibi
cute" — vẽ ra chibi là lệch hẳn nhận diện kênh mẫu ngay từ tập 1.

## 2. Template cố định (21/21 video đều theo, kể cả video 3,3k view)
```
┌─────────────────────────────────────────────┐
│  DÒNG 1 — CHỮ VÀNG viền đen, cao ~20% khung │  ← câu NGHỊCH LÝ / câu hỏi
│                                             │
│     [ MẶT NHÂN VẬT CHÍNH, cận, lệch phải ]  │  ← nền = bối cảnh (mưa bão/lửa/thành/tuyết)
│                                             │
│  DÒNG 2 — CHỮ ĐỎ viền trắng, cao ~27% khung │  ← TÊN riêng + 「の最期/の真実」
└─────────────────────────────────────────────┘
```
Số đo thật (chuẩn hoá về khung 640×360, % tính theo chiều cao):
| Thành phần | Mép trên | Mép dưới | Ghi chú |
|---|---|---|---|
| Chữ vàng dòng trên | **2–3 %** | ~22–25 % | 21/21 video có; dính sát mép trên |
| Chữ đỏ dòng dưới | ~70–74 % | **95–97 %** | 18/21 nằm đúng dải này; dính sát mép dưới |

- **Màu chữ**: vàng `#FFD400`-ish viền đen dày ở trên · đỏ `#E1001A`-ish viền TRẮNG dày ở dưới.
  Không có banner nền chữ (khác hẳn template satori) — chữ nằm thẳng trên ảnh, sống nhờ viền dày.
- **Font**: gothic đậm (kiểu 貂明朝/ゴシック極太), 100 % chữ Nhật, KHÔNG chữ Latin, KHÔNG số hiệu tập.
- **Độ dài chữ (đếm thật)**: dòng vàng **6–10 ký tự**, dòng đỏ **4–9 ký tự**. Không bao giờ quá 10.
- **Nhân vật**: 1 mặt cận chiếm ~35–45 % khung, mắt nằm ở khoảng 1/3 trên. Bố cục mặt thường lệch
  PHẢI (7/21) hoặc giữa; nhân vật phụ nhỏ hơn đặt lệch trái để tạo thế đối đầu.
- **Nền**: luôn là bối cảnh kịch tính có màu chủ đạo mạnh — mưa+sét xanh lạnh, lửa+khói cam đỏ,
  tuyết xanh đêm, vách vàng kim của thành. Không bao giờ nền phẳng.

## 3. Biến thể — và nó nói gì về view
| Kiểu | Video | View | Kết luận |
|---|---|---|---|
| 1 mặt cận + 2 dòng chữ | 01 前田慶次 · 02 柴田勝家 · 06 今川義元 · 07 千利休 · 09 今川氏真 | 771k · 466k · 91k · 60k · 27k | **Kiểu chuẩn.** Dùng ở cả hit lẫn video thường |
| 2 nhân vật đối đầu | 04 徳川家康 (213k) · 21 備中高松城 (3,3k) | trải rộng | Không quyết định view |
| ≥3 nhân vật, không có mặt cận | 03 清須会議 (219k) · 14 春日局 (10k) | trải rộng | Rối hơn nhưng vẫn ăn nếu nhân vật nổi |
| Thiếu dòng chữ vàng trên | 21 備中高松城 (3,3k — video cũ nhất) | 3,3k | Video đầu kênh, template chưa chốt |

**Kết luận thẳng:** thumbnail của video 27k (今川氏真) và video 771k (前田慶次) **giống hệt nhau về
template** — khác biệt view KHÔNG nằm ở thumbnail mà ở **độ nổi tiếng của nhân vật**. Đúng y luật
cứng #1 của lane (LUÔN chọn nhân vật có game/anime). Đừng đổ công tối ưu thumbnail để cứu một nhân
vật không ai biết.

## 4. Công thức copy chữ thumbnail (rút từ 21 mẫu)
```
DÒNG VÀNG (6–10 chữ) = nghịch lý rút gọn, KHÔNG có tên nhân vật
DÒNG ĐỎ  (4–9 chữ)  = TÊN NHÂN VẬT + đuôi 「の最期」「の真実」 hoặc tên trận đánh
```
Mẫu thật:
| Dòng vàng | Dòng đỏ | Video |
|---|---|---|
| 作られた傾奇者 | 前田慶次の最期 | 771k |
| 勝っていたのに総崩れ | 賤ヶ岳の戦い | 466k |
| 織田家崩壊の始まり | 清須会議 | 219k |
| 勝ったのに頭を下げた | 徳川家康 | 213k |
| 正しかったのに負けた | 今川義元の最期 | 91k |
| 秀吉に何をした？ | 千利休の最期 | 60k |
| 9年で国を失った | 今川氏真の真実 | 27k |
| 逆臣の娘から | 大奥の頂点へ | 10k |

Quy luật: **dòng vàng mở mâu thuẫn — dòng đỏ trả lời "của AI"**. Hai dòng đọc liền nhau thành 1 câu.
Tuyệt đối không nhồi cả tiêu đề video vào thumbnail (tiêu đề dài 29–47 ký tự, thumbnail chỉ 10–19).

## 5. Việc phải làm khi khai `profile.thumbnail` cho Lane I
1. `art_style`: manga/anime lịch sử seinen, nét viền dày, cel-shading, mặt người lớn tỉ lệ thật —
   **cấm chữ "chibi"/"cute"**.
2. 2 khối chữ: trên vàng viền đen (6–10 chữ), dưới đỏ viền TRẮNG (4–9 chữ), không banner nền.
3. Chữ dính mép: mép trên ~3 %, mép dưới ~96 % chiều cao.
4. Mặt nhân vật chính cận cảnh, biểu cảm nặng, lệch phải; nền bối cảnh kịch tính 1 màu chủ đạo.
5. QC bằng `pipeline\qc_thumbnail_sol.py` với form riêng lane (xem `docs\QC_THUMBNAIL_GPT_SOL.md`).
