---
name: youtube-image-prompts
description: Sinh loạt PROMPT ẢNH + hệ NHẤT QUÁN NHÂN VẬT cho video YouTube faceless — TỔNG QUÁT cho MỌI ngách/thị trường (phong cách ảnh, sắc tộc, màu/đen-trắng là THAM SỐ). Gồm: character bible + toán tuổi, sinh master face, QC vision, marker @REF/@REF2/@GROK (khoá mặt 2 nhân vật + route cảnh trẻ em), content-policy. Trigger: "prompt ảnh <ngách>", "ảnh cho video YouTube", "image prompts", "nhất quán nhân vật/khuôn mặt", "character consistency", "ảnh người già/WW2/tư liệu". Input: script + niche/market + mô tả nhân vật + số ảnh. Dùng sau youtube-script. Áp dụng mọi dự án YouTube.
---

> **NGÁCH CHỐT CHO PROFILE NÀY:** niche=satori-elderly · market=JP · language=tiếng Nhật · narrator=cụ bà 70-80 ngôi 1, です・ます+ございます. Mọi tham số còn lại lấy từ  (char_rate, gate nhịp, character_sheet, style_suffix).

# YouTube Image Prompts + Character Consistency (tổng quát)

Sinh prompt ảnh theo mạch script + đảm bảo **khuôn mặt nhân vật nhất quán**. Ngách/phong cách/sắc tộc là THAM SỐ.

## INPUT
```
NICHE/STYLE: [satori→cinematic COLOR ấm | ww2→archival B&W documentary | <khác>]
MARKET/ETHNICITY: [Japanese | Korean | Western | ...]   SỐ ẢNH: [~1 ảnh/6-7s; 25-31' ≈ 280-300 ảnh]
NGÂN SÁCH ẢNH: [mặc định 20.000đ/video — gpti2: ảnh @REF 110đ, ảnh thường 50đ
                → n × (50 + 60×tỉ_lệ_ref) ≤ ngân sách; chuẩn 290 ảnh = 87 ref (≤30%) + 203 thường = 19.720đ]
Style tail chung (nhắc trong mọi prompt): "cinematic ultra-realistic <color|B&W>, photorealistic, 8K, <mood> lighting, authentic <market> setting, 16:9, no text"
```

## ⚠️ ĐỒNG BỘ ẢNH ↔ LỜI ĐỌC (verify nenkin-fujinkai 2026-09-08 — lỗi đã dính)
`assemble.py` chia ảnh **ĐỀU theo cue SRT** (ảnh thứ i ↔ khối cue thứ i), KHÔNG biết ảnh nào thuộc câu nào →
để ảnh khớp lời, PHẢI viết prompt với **MẬT ĐỘ ĐỀU theo kịch bản**: số ảnh cho mỗi đoạn ∝ ĐỘ DÀI LỜI của đoạn
đó, đi ĐÚNG THỨ TỰ text. **Đừng dồn nhiều ảnh vào cảnh cao trào và bỏ ít ảnh cho đoạn mở đầu/thiết lập dài** →
ảnh sẽ TRÔI TRỄ so với lời ở khúc giữa video (đo thật: 8:30 ảnh màn LINE trong khi lời đã sang cảnh khác).
**Ảnh QUÁ ĐẶC TẢ** (màn hình điện thoại đọc được, biển hiệu, chữ) chỉ dùng khi chắc vị trí — đặt sai câu là lộ.

⭐ **CÁCH CHẮC NHẤT — dựng STORYBOARD từ SRT (verify 2026-09-08, sửa lệch của nenkin-fujinkai):** parse `voice.srt`
thành M cue, chia thành N khối GIỐNG assemble (`bounds[i]=round(i*M/N)`), in text mỗi khối. Rồi viết prompt #i
BÁM ĐÚNG lời khối #i (đặt cảnh đặc tả — màn LINE/kẻ lông mày/dòng sông ẩn dụ — đúng khối lời nhắc tới). → ảnh #i
luôn khớp đoạn assemble sẽ chiếu. Đây là cách đảm bảo sync tuyệt đối (đo thật: 8:30 & 15:30 khớp nghĩa sau khi làm lại).
```python
# gợi ý: đọc cue, gom N khối, in ra để tự viết prompt theo từng khối
bounds=[round(i*M/N) for i in range(N+1)]; bounds[-1]=M
```

## ⭐ NHẤT QUÁN NHÂN VẬT — BIBLE → MASTER → QC → REF-LOCK (bắt buộc; verify 2026-09)
CHARACTER SHEET bằng chữ CHỈ giữ "cùng kiểu người", KHÔNG giữ KHUÔN MẶT (gpti2 không seed). Phải:

**P0 — HỒ SƠ NHÂN VẬT (bible) TRƯỚC KHI TẠO ẢNH.** Thiết kế tuổi/ngoại hình/tính cách/phong cách HÀI HOÀ +
**toán tuổi quan hệ** rồi mới sinh master. `<slug>/characters.json`:
`{"characters":[{"name","age","gender","role","look","personality","master"}],"relationships":[{"a","b","min_gap","max_gap"}]}`.
Toán tuổi: **con = cha mẹ − (25..35)** → mẹ 73 thì con ~40-50 (KHÔNG để con nhìn 10 tuổi hay ngang tuổi mẹ →
người xem tưởng nhầm); con cả > con sau. Con là TRẺ EM thật → route `@GROK`.

**Master + QC + Gen (1 lượt):**
1. Sinh 1 MASTER portrait mỗi nhân vật (`--quality medium`, nền xám trơn, chính diện, đặc điểm độc nhất
   nốt ruồi/kính, KÈM TUỔI): `gen_images.py --prompts master.txt --out <slug>/_ref --quality medium`.
2. ⭐ **QC master bằng AI vision TRƯỚC khi gen loạt:** `qc_character.py --bible <slug>/characters.json`
   (model **gemini-3.8-flash** + grok-4.6, trung bình) → ước lượng tuổi/giới + chênh tuổi quan hệ; FLAG (lệch
   >±12 tuổi / sai giới / nhìn trẻ con / quan hệ vô lý) → sửa master rồi QC lại, ĐỪNG gen loạt khi master còn sai.
3. Đánh dấu `img_prompts.txt`: **`@REF`** (mặt NV1, `--ref`) · **`@REF2`** (mặt NV2, `--ref2`) · **`@GROK`**
   (cảnh trẻ em) · dòng thường (cảnh vật/tay/người xa/nhân vật ở nhiều độ tuổi = biến thiên tự nhiên). Prompt @REF
   nên có "the SAME person from the reference image, identical face, in a completely NEW scene".
   ⭐ **CẢNH 2 NGƯỜI có nhân vật khoá → VẪN phải @REF/@REF2 (đừng để plain).** Ref là nhân vật khoá, mô tả người
   kia ("her middle-aged son pleading across from her") là phụ — model giữ mặt khoá, người phụ tự do. Đo thật
   (yokin-basho 029/060): để plain vì "có thêm con trai" → BÀ MẸ (Yasuko) bị vẽ thành người khác (tóc/áo khác) =
   trôi mặt. QC bằng mắt luôn soi riêng các cảnh 2 người này.
   💰 **GIỮ TỈ LỆ @REF/@REF2 ≤ 30% tổng số dòng** — mỗi marker ref là +60đ (110đ vs 50đ), nên đây là đòn bẩy
   chi phí LỚN NHẤT: đo thật bản simbot2 cũ 49/124 dòng ref (40%) = **59% tổng tiền cho 40% số ảnh**. Hạ 40%→30%
   mua thêm ~20 ảnh trong cùng ngân sách. Chỉ đánh ref khi khung THẬT SỰ thấy rõ mặt; over-shoulder, người quay
   lưng, tay/đồ vật, người ở xa, cảnh vật → để dòng thường. Đếm lại tỉ lệ trước khi gen (`grep -c "@REF"`).
4. Gen: `gen_images.py --prompts img_prompts.txt --out <slug>/img --ref _ref/001.png --ref2 _refB/001.png --quality low`
   (routing tự động). Tối đa 8 ảnh/`--ref`, ảnh đầu ưu tiên. Chi phí: text-only **50đ** · REF-LOCK low **110đ** ·
   Grok (trẻ em) ~1280×720. Dùng **low** (giữ mặt ngang medium, rẻ ~4 lần); chỉ MASTER dùng medium.

## ⚠️ CONTENT-POLICY (đo thật 2026-09-08)
- **TRẺ EM/EM BÉ:** gpti2/Azure **CHẶN TUYỆT ĐỐI mọi minor** (kể cả lành mạnh/silhouette/"học sinh"; trigger theo
  từ child/kid/baby/infant/toddler/students/số tuổi). → **cảnh trẻ em đánh `@GROK`** (route Grok Imagine, cho phép
  ảnh trẻ em lành mạnh). Không muốn trẻ em thật → VẬT tượng trưng (không người) hoặc "bundle" ôm từ sau không gọi tên.
- **Tắm/sento/khoả thân** → "mặc kín, khăn/yukata, modest and fully covered". Bạo lực/máu → biểu tượng. Tránh tên
  người thật/bản quyền. 1 prompt gpti2 reject → resume chạy tiếp → sửa prompt/retry ≤3, quá → chuyển `@GROK`/bỏ cảnh.

## HỒ SƠ NICHE (style)
- **satori-elderly:** cinematic ultra-realistic COLOR, warm emotional lighting, người già + đời thường (縁側/仏壇/
  bệnh viện/phố/gia đình). **ww2-history:** archival B&W documentary (LIFE Magazine/Signal Corps), realistic grounded, 1940s.

Bộ pipeline ở `pipeline/` của dự án (impl: e:\CLAUDE\YOUTUBE\h2dev\pipeline: gen_images.py · gpti2_edit.py ·
grok_gen.py · qc_character.py). Chi tiết + bẫy: memory [[khoa-nhat-quan-nhan-vat-ref-lock]], [[content-policy-tre-em-grok]].
