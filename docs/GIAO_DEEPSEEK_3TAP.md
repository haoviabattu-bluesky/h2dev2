# GIAO VIỆC — dựng video 3 tập (06 · 11 · 19)

Lane `satori-jp-obaa` · tab trang tính `Lopezzapa68` · mọi lệnh chạy ở
`E:\CLAUDE\YOUTUBE\h2dev\pipeline`, luôn dùng `py -3.13`.

Đọc trước: `E:\CLAUDE\YOUTUBE\h2dev\docs\QUY_TRINH_RENDER_VIDEO.md`

## ⛔ BỐN ĐIỀU CẤM

1. **Không render khi số ảnh < số dòng `img_prompts.txt`** — thiếu một tấm là nó tự gen lại toàn
   bộ bằng gpti2, tốn ~8.000đ, im lặng không hỏi.
2. Không thêm cờ `--burn-sub` (video đăng cố ý không cháy phụ đề).
3. Không đăng `review-vi.mp4` — đó là bản duyệt tiếng Việt.
4. Không xoá dòng/cột/dữ liệu trong Google Sheet, chỉ ghi thêm.

---

## VIỆC 1 — Tập 06: ghép lại, neo đã chuẩn bị sẵn

Tập này đã có video nhưng khớp hình–lời chỉ **2,9/5** vì thiếu neo. `img_doan.txt` và `anchors.txt`
đã có sẵn. Chỉ ghép lại, **không tốn lại tiền giọng**.

```bat
del "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM\final.mp4"

py -3.13 render_engine.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM" --profile satori-jp-obaa --quality low --workers 8

py -3.13 giao_hang.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM" --profile satori-jp-obaa --ep 06 --ten oita-onna
```

**Kiểm trong log:** bước `B7.5 neo ảnh↔lời` phải báo `133 neo hop le`, và bước ghép phải ghi
`sync theo NEO NỘI DUNG (--anchors...)`. Nếu ghi `sync theo RANH GIỚI CÂU (SRT)` là neo không ăn →
**dừng, báo lại**.

**So B8Q với mốc cũ 2,9/5** rồi báo con số mới.

---

## VIỆC 2 và 3 — Tập 11 và 19: làm từ đầu, ảnh đã sẵn trên Drive

| Tập | `<SLUG>` | `<EP>` | `<TEN>` |
|---|---|---|---|
| 11 | `simbot2-11-DXXwIxhcfF0` | `11` | `tsucho-ikura` |
| 19 | `simbot2-19-l0p1EnDcXYM` | `19` | `yonin-no-onna` |

Thay `<SLUG>` `<EP>` `<TEN>` rồi chạy tuần tự từng tập:

```bat
py -3.13 drive_handoff.py download-result <SLUG> "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<SLUG>\img"

py -3.13 -c "from pathlib import Path; d=Path(r'E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<SLUG>'); a=len(list((d/'img').glob('*.png'))); b=len([l for l in (d/'img_prompts.txt').read_text(encoding='utf-8').splitlines() if l.strip()]); print(f'anh={a} prompt={b} ->', 'DU' if a>=b else 'THIEU, DUNG LAI')"

py -3.13 sinh_img_doan.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<SLUG>"

py -3.13 render_engine.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<SLUG>" --profile satori-jp-obaa --quality low --workers 8

py -3.13 giao_hang.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\<SLUG>" --profile satori-jp-obaa --ep <EP> --ten <TEN>
```

**Hai chốt bắt buộc:**
- Lệnh đếm phải ra **`DU`** mới được chạy tiếp. Ra `THIEU, DUNG LAI` → dừng, báo thiếu bao nhiêu tấm.
- `sinh_img_doan.py` báo `bu thieu` hoặc `nan nguoc` **trên 15% số dòng** → dừng, báo lại.

⚠️ **KHÔNG chạy `sinh_neo.py` bằng tay cho tập 11 và 19.** Nó cần file phụ đề, mà phụ đề chỉ có
sau khi chạy giọng (TTS). `render_engine.py` tự gọi nó ở **bước B7.5**, đúng sau khâu giọng. Chạy
tay trước sẽ báo `khong co voice_paced.srt`.
(Tập 06 khác: giọng đã làm từ lần trước nên neo đã sinh sẵn rồi.)

---

## GHI TRANG TÍNH (sau mỗi tập)

Cột **G (VIDEO)** = đường dẫn thư mục giao hàng:
`E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep<NN>-<tên>\`

Chỉ ghi ô đó, không đụng ô khác.

---

## BÁO VỀ

- Thời gian từng bước
- **Điểm B8Q khớp hình–lời** của từng tập
- Cảnh báo B5Q: **mở đúng ảnh bị nêu ra nhìn** rồi mới kết luận
  - biển hiệu / biển số / số phòng **bằng tiếng Nhật** → không phải lỗi
  - **chữ tiếng Anh trong bối cảnh Nhật** → lỗi thật
  - **mặt người nhoè bệt** → lỗi nặng nhất
- Đường dẫn thư mục giao hàng

## DỪNG LẠI VÀ BÁO, ĐỪNG TỰ QUYẾT, KHI

- Số ảnh thiếu so với số prompt
- Bước B5 bắt đầu gen ảnh → **Ctrl+C ngay**
- B4Q hoặc B8Q rớt
- Bước ghép chạy chế độ `RANH GIỚI CÂU` thay vì `NEO NỘI DUNG`

---

Ba tập chạy tuần tự khoảng **1 tiếng 15 phút** — tập 06 ~20 phút (bỏ qua khâu giọng), tập 11 và 19
mỗi tập ~27 phút.
