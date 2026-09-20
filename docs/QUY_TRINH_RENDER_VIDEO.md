# QUY TRÌNH RENDER VIDEO (BƯỚC 3) — nhận ảnh từ máy 2 → ra video hoàn chỉnh

> **Giao cho AI nào cũng chạy được.** File này tự chứa: không cần đọc lịch sử chat, không cần biết
> bước 1 và bước 2 làm gì. Chỉ cần máy có Python 3.13 + ffmpeg + quyền đọc Google Sheet của dự án.
>
> **Dây chuyền 3 bước của dự án:**
> | Bước | Ai làm | Việc |
> |---|---|---|
> | 1 | Máy 1 (Claude Code) | Viết kịch bản + tạo ảnh master REF-LOCK → giao việc |
> | 2 | Máy 2 (Flow) | Sinh ảnh hàng loạt → trả về |
> | 3 | **AI nào cũng được ← FILE NÀY** | Nhận ảnh → kiểm → render ra video |
>
> Bước 3 **không cần AI thông minh** — chỉ chạy lệnh theo thứ tự và đọc kết quả. Tách ra để máy 1
> đỡ tốn quota.

**Lane áp dụng:** `satori-jp-obaa` (clone kênh simbot2) · thư mục tập nằm trong
`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\` · tab trang tính tên `Lopezzapa68`.

⚠️ **Tab `shinya_shiryoshitsu` (lane `toshi-densetsu-jp`) KHÔNG dùng file này** — lane đó dựng thân
video bằng clip stock và ghép bằng `make_video.py --from B8`, không phải `render_engine.py`.
Runbook bước 3 của lane đó: **`docs/GIAO_VIEC_BUOC3_AGENT.md`**.

---

## ⛔ BỐN ĐIỀU CẤM — đọc trước khi gõ lệnh đầu tiên

1. **KHÔNG chạy render khi số ảnh chưa đủ.** `render_engine.py` bỏ qua bước sinh ảnh **chỉ khi**
   số file `.png` trong `img/` **≥** số dòng prompt. Thiếu dù một tấm là nó **tự gen lại toàn bộ
   bằng gpti2 ≈ 8.000đ**, im lặng, không hỏi. Mục 2 bên dưới bắt buộc phải làm.
2. **KHÔNG thêm cờ `--burn-sub`.** Video đăng lên YouTube **cố ý không cháy phụ đề** (YouTube tự bật
   CC). Mặc định đã đúng — đừng thêm gì.
3. **KHÔNG đăng `final_vi.mp4`.** Đó là bản phụ đề tiếng Việt chỉ để chủ dự án soi nội dung.
   Bản đăng là `final.mp4`.
4. **KHÔNG xoá dòng/cột/dữ liệu trong Google Sheet.** Chỉ được ghi thêm hoặc cập nhật ô.

---

## 1. TÌM TẬP CẦN RENDER

Mở trang tính, tab `Lopezzapa68`, nhìn cột **F (STATUS-IMG)**. Tập nào ghi:

```
Img done - <n>/<m> ảnh (<ngày giờ>)
```

là máy 2 đã trả ảnh xong, sẵn sàng render. `n` phải **bằng** `m`; lệch thì xem mục 6.

Cột **E (FOLDER)** của chính dòng đó là đường dẫn thư mục tập. **Đoạn cuối đường dẫn là `slug`** —
ví dụ `E:\...\assets\satori_jp\simbot2-07-TISOm_7M_vM\` thì slug là `simbot2-07-TISOm_7M_vM`.

Hoặc để máy tra hộ:
```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 quet_dong_can_anh.py --tab Lopezzapa68 --dong 1-25
```

---

## 2. TẢI ẢNH VỀ + ĐẾM (bắt buộc, đây là chốt chặn tiền)

```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 drive_handoff.py download-result <slug> "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<slug>\img"
```

Rồi **đếm và đối chiếu**:

```bat
py -3.13 -c "from pathlib import Path; d=Path(r'E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<slug>'); a=len(list((d/'img').glob('*.png'))); b=len([l for l in (d/'img_prompts.txt').read_text(encoding='utf-8').splitlines() if l.strip()]); print(f'anh={a} prompt={b} ->', 'DU, render duoc' if a>=b else 'THIEU, DUNG LAI')"
```

- Ra **`DU, render duoc`** → sang mục 3.
- Ra **`THIEU, DUNG LAI`** → **dừng**, báo chủ dự án. Chạy tiếp là đốt ~8.000đ gen lại ảnh.

---

## 3. RENDER

```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 render_engine.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<slug>" --profile satori-jp-obaa --quality low --workers 8
```

Chạy 12 bước, **~25–30 phút** cho video 30 phút. Số đo thật (tập `simbot2-07`, 128 ảnh, 32,5 phút):

| Bước | Việc | Phút |
|---|---|---|
| 1 | B4 giọng (TTS) — **khâu tốn tiền duy nhất, ~1.500đ** | 2,8 |
| 2–4 | Sửa phụ đề khớp script · giãn nhịp · QC giọng+nghe | ~0,1 |
| 5 | B5 gen ảnh — **phải hiện `⏭ skip`** | 0 |
| 6 | B5Q QC ảnh | 1,0 |
| 7 | B7 thumbnail | 0,0 |
| 8 | B8 ghép video — **nặng nhất** | 15,4 |
| 9 | B8Q QC video | 0,6 |
| 10 | B8V bản phụ đề tiếng Việt | 7,3 |
| 11–12 | B9 gói đăng tải · B10 nghiệm thu | 0,1 |

⚠️ **Nhìn bước 5:** phải là `⏭ skip`. Nếu nó bắt đầu gen ảnh → **Ctrl+C ngay**, quay lại mục 2.

---

## 4. ĐỌC KẾT QUẢ

Cuối log có bảng `=== TÓM TẮT ===`. Ba dòng cần đọc kỹ:

**`B4Q QC giọng+phụ đề+nghe`** — phải `ĐẠT`. Rớt = giọng đọc có chỗ đứt từ hoặc nghỉ sai chỗ → báo
chủ dự án, đừng tự sửa.

**`B8Q QC video`** — phải `ĐẠT`.

**`B5Q QC ảnh`** — hay báo `N/20 ảnh mẫu có vấn đề`. **ĐỪNG hoảng, phần lớn là báo động giả.**
Cổng cấm "chữ đọc được" để chặn chú thích AI bịa, nhưng nó **bắt nhầm cả chữ có thật trong cảnh**:
biển số xe, chữ trên thân xe cứu thương, biển hiệu cửa hàng. Đo thật ở tập 07: báo 9/20, mở ra xem
thì ảnh đẹp, "chữ" chỉ là biển số xe hợp cảnh.

Cách xử đúng: **mở đúng những tấm bị nêu tên ra nhìn.**
- Chữ là biển hiệu/biển số/chữ trên xe → **bỏ qua, không phải lỗi.**
- Chữ là dòng chú thích lơ lửng, watermark, chữ nguệch ngoạc chồng lên hình → **lỗi thật.**
- **Mặt người bị nhoè bệt thành mảng** → **lỗi thật, nặng nhất** (đã gặp ở tập 07, tấm 061).

---

## 5. GIAO HÀNG

Trong thư mục tập sẽ có:

| File | Dùng làm gì |
|---|---|
| **`final.mp4`** | **BẢN ĐĂNG** — 1920×1080, không cháy phụ đề |
| **`voice_paced.srt`** | Up lên YouTube làm **CC** cho bản đăng |
| **`thumb_final.png`** | Thumbnail 1280×720 |
| **`TIEU_DE_MO_TA.txt`** · **`DANG-TAI.txt`** | Tiêu đề + mô tả + hashtag để dán khi đăng — **file này BƯỚC 1 (máy 1) đã viết sẵn, KHÔNG được tự viết lại/tự sinh nội dung mới ở bước 3** (chốt 2026-09-17 sau sự cố thật: 2 tập đi qua nhánh ghép riêng bị lọt tới người xem với `listting.txt` chỉ là placeholder rỗng vì bước 3 tưởng phải tự viết mà công cụ bước 3 không hiểu nội dung). Nếu `TIEU_DE_MO_TA.txt` có đoạn `[CHƯA CÓ — trích từ voice_paced.srt thật]` ở mục Timestamps, việc DUY NHẤT cần làm là tìm 8 câu mở đầu đoạn (in kèm sẵn) trong `voice_paced.srt`/`voice.srt` rồi thay bằng mốc `phút:giây` thật (grep/tìm chuỗi, không cần viết lại câu nào) — rồi **chép NGUYÊN VĂN cả file** sang `listting.txt` khi giao hàng. Thiếu file này ở bước 1 → **dừng lại, báo chủ dự án**, đừng tự bịa tiêu đề/mô tả. |
| `final_vi.mp4` | **CHỈ để chủ dự án soi nội dung — KHÔNG ĐĂNG** |
| `voice_vi.srt` | Phụ đề Việt (đi kèm bản duyệt) |

Xong thì **cập nhật cột G (VIDEO)** đúng dòng STT đó = đường dẫn thư mục tập. Không đụng cột khác.

---

## 6. KHI NÀO DỪNG LẠI VÀ BÁO, THAY VÌ TỰ QUYẾT

Ghi rõ **số đo thật** (n/m, tên file, thông báo lỗi nguyên văn) chứ đừng ghi "có vấn đề":

| Tình huống | Làm gì |
|---|---|
| Số ảnh < số prompt | **Dừng.** Báo thiếu bao nhiêu tấm, tên file nào thiếu |
| Cột F ghi `LỖI: ...` | **Dừng.** Máy 2 đã gặp vấn đề, chưa render được |
| Bước 5 bắt đầu gen ảnh | **Ctrl+C ngay.** Báo liền |
| B4Q hoặc B8Q rớt | **Dừng.** Chép nguyên dòng lỗi |
| Có tấm nhoè mặt / chữ bịa chồng hình | Render vẫn xong được — **báo kèm số thứ tự tấm** để chủ dự án quyết vá hay bỏ qua |
| ffmpeg lỗi giữa chừng | Chạy lại đúng lệnh mục 3 — nó tự bỏ qua các bước đã xong. Vẫn lỗi thì dừng, chép log |

---

## 7. GHI CHÚ KỸ THUẬT

- **Luôn dùng `py -3.13`.** Gõ `python` trơn có thể ra bản Python khác thiếu thư viện ffmpeg,
  lỗi rất khó hiểu.
- Render **chạy lại được nhiều lần**: bước nào có sẵn kết quả thì nó bỏ qua. Nên đứt giữa chừng
  cứ chạy lại đúng lệnh cũ, không mất gì.
- Muốn dựng lại video từ đầu (vd đổi nhạc nền) thì **xoá `final.mp4`** rồi chạy lại — đừng xoá
  thư mục `img/`, xoá là mất ảnh máy 2 gửi và lần chạy sau sẽ gen lại tốn tiền.
- Chi phí một tập ở bước 3: **~1.500đ TTS**, không có khoản nào khác (ảnh đã do máy 2 làm bằng
  quota Flow, không mất tiền mặt).
