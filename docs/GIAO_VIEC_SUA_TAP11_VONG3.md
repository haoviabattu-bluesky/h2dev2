# GIAO VIỆC — vòng 3: sửa bug `--ep` + sửa cục bộ các điểm gán sai đã bắt được, rồi chạy lại tập 11

File tự chứa, đọc hết rồi làm theo ĐÚNG THỨ TỰ, không cần hỏi ai, không cần đọc lịch sử chat.
Lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev\pipeline`, luôn dùng `py -3.13`.

## 0. BỐI CẢNH — TÓM TẮT NGẮN, đọc kỹ mục "ĐỪNG LẶP LẠI"

Tập 11 đã qua 2 vòng sửa: vòng 1 sửa cách trải neo theo thời gian (`sinh_neo.py`, ĐÃ ĐÚNG, giữ
nguyên — không đụng file này nữa). Vòng 2 viết lại thuật toán gán ảnh→đoạn bằng cửa sổ hẹp +
multiple-choice (`sinh_img_doan.py`). Đã chạy thật `chay_buoc3.py --dong 11` — video ra được, giao
hàng thật, nhưng đo lại B8Q chỉ **2,9/5** (không cải thiện so với bản CŨ 3,1/5, và thấp hơn hẳn mốc
Lane D từng đạt cho đúng loại sửa neo này: 2,9 → **3,8/5**). Đây là vòng 3: sửa CỤC BỘ đúng những
điểm đã bị bắt lỗi, KHÔNG chạy lại toàn bộ thuật toán từ đầu (rủi ro tạo lỗi mới ở chỗ đang đúng).

**⚠️ ĐỪNG LẶP LẠI 2 SAI LẦM ĐÃ XẢY RA:**
1. Người giao việc (không phải bạn) đã sai khi bảo "không cần truyền `--ep`/`--ten` cho
   `giao_hang.py`, tool tự suy ra" — SAI, dẫn tới thư mục giao hàng sai tên `ep01-...`. Sửa ở VIỆC 1.
2. Vòng 2 kết luận "đoạn 46 thiếu ảnh nguồn" — SAI, ảnh có sẵn (073/074.png) nhưng bị thuật toán gán
   nhầm sang đoạn 31, và **không sửa được bằng cách đổi số trong `img_doan.txt`** vì ảnh hiển thị
   theo đúng thứ tự tên file cố định — đổi số mà không xét ảnh liền trước/sau sẽ phá thứ tự thời
   gian, video sẽ phải "đi lùi". **MỌI SỬA Ở VIỆC 2 DƯỚI ĐÂY PHẢI KIỂM KHẢ THI TRƯỚC KHI ĐỔI SỐ.**

---

## 1. ⛔ CẤM TUYỆT ĐỐI

1. Không đụng lane nào khác ngoài `satori-jp-obaa`.
2. Không xoá dòng/cột/dữ liệu Google Sheet — chỉ cập nhật đúng ô đã quy định.
3. Không sửa `sinh_neo.py` (đã đúng, giữ nguyên). Không sửa `script.txt`/`voice.*`/`img_prompts.txt`.
4. Không gọi lại toàn bộ `main()` của `sinh_img_doan.py` để "chạy lại từ đầu" ở VIỆC 2 — chỉ sửa
   ĐÚNG các dòng đã liệt kê trong bảng ở mục 3.2, giữ nguyên 114/121 dòng còn lại.
5. Không chạy `render_engine.py`/`chay_buoc3.py` nhiều lần tuỳ ý để "thử" — chỉ chạy thật đúng 1
   lần ở VIỆC 4, sau khi đã xong VIỆC 1-3.

---

## 2. VIỆC 1 — sửa bug số tập trong lệnh gọi `giao_hang.py` (nhỏ, làm trước)

**Lỗi:** BƯỚC G trong `chay_buoc3.py` gọi `giao_hang.py --slug ... --profile ...` KHÔNG kèm
`--ep` — trong khi `so_tap()` của `giao_hang.py` chỉ đoán được số tập từ tên thư mục nếu tên có
dạng `epNN-...`; thư mục lane satori là `simbot2-11-DXXwIxhcfF0` (không có "ep"), nên nó rơi vào
mặc định `1`, tạo ra thư mục sai `ep01-simbot2-11-DXXwIxhcfF0`.

**Cách sửa — trong `pipeline/chay_buoc3.py`, tìm đoạn BƯỚC G (`"G. giao hàng (giao_hang)"`):**
```python
ok, lines, lan = chay_lenh(
    "G. giao hàng (giao_hang)",
    ["giao_hang.py", "--slug", str(tap), "--profile", prof["id"], "--ep", str(a.dong)],
    "A", HERE, retry_toi_da=3)
```
(chỉ thêm `"--ep", str(a.dong)` — STT đã biết sẵn từ tham số dòng lệnh, không cần đoán từ tên thư
mục nữa). KHÔNG sửa gì trong `giao_hang.py`.

**Dọn thư mục giao hàng sai của tập 11 (đã tạo ở vòng trước):** xoá
`E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep01-simbot2-11-DXXwIxhcfF0\` (thư mục NÀY, không phải file
gốc trong `assets\`) — thư mục đúng sẽ được tạo lại ở VIỆC 4 sau khi có `--ep`.

**Kiểm:** chạy thử `py -3.13 giao_hang.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0" --profile satori-jp-obaa --ep 11` (chạy tay, không qua `chay_buoc3.py`) — thư mục
tạo ra phải tên **`ep11-...`** (không phải `ep01-...`). Ghi kết quả vào báo cáo. Sau bước kiểm
này thì XOÁ thư mục vừa tạo thử (sẽ tạo lại chính thức ở VIỆC 4, tránh có 2 bản trùng).

---

## 3. VIỆC 2 — sửa CỤC BỘ 7 điểm đã bắt được lỗi, không viết lại thuật toán

### 3.1 Nguyên tắc: "MỞ RỘNG PHẠM VI KHẢ THI, KHÔNG ÉP SỐ"

Với mỗi ảnh nghi vấn (tên `ten`), hiện đang gán đoạn `p_hien`:
```python
import sinh_neo as sn
anh_sorted = sorted((S / "img").glob("*.png"))          # S = thu muc tap
idx = anh_sorted.index(S / "img" / ten)
m = sn.doc_img_doan(S / "img_doan.txt")
p_truoc = m[anh_sorted[idx - 1].name] if idx > 0 else 1
p_sau = m[anh_sorted[idx + 1].name] if idx + 1 < len(anh_sorted) else len(doan)
# PHAM VI KHA THI = [p_truoc, p_sau] — doi so ngoai khoang nay se pha thu tu khong giam
```
Đọc TOÀN VĂN từng đoạn trong `[p_truoc, p_sau]` (không cắt cụt) + TOÀN VĂN prompt của `ten`, hỏi
LLM một câu duy nhất: "trong các đoạn số {p_truoc}..{p_sau}, đoạn nào khớp nội dung ảnh này nhất?"
— PHẠM VI THẬT (không phải cửa sổ ±4 cứng như thuật toán chính) vì cửa sổ hẹp trước đó đã LOẠI
MẤT đáp án đúng ở ít nhất 1 trường hợp đã biết (xem 3.2, dòng đoạn 46).

- Nếu `p_truoc == p_sau` (phạm vi chỉ có 1 lựa chọn) → không cần hỏi, không đổi được gì, ghi nhận
  "không có phạm vi để sửa, giữ nguyên", giải thích trong báo cáo.
- Nếu LLM chọn ra một đoạn KHÁC `p_hien` và nằm trong phạm vi khả thi → **cập nhật đúng dòng đó**
  trong `img_doan.txt` bằng chỉnh sửa văn bản trực tiếp (không chạy lại `main()`).
- Nếu phạm vi khả thi KHÔNG chứa đoạn đúng về nội dung (như trường hợp 073/074.png — nội dung
  đúng là đoạn 46 nhưng phạm vi khả thi chỉ 30-32) → **đây là giới hạn cấu trúc** (ảnh được viết
  sai vị trí trong `img_prompts.txt` từ bước 1, ngoài khả năng sửa ở tầng gán ảnh→đoạn) → GIỮ
  NGUYÊN, ghi rõ vào báo cáo là "không sửa được do giới hạn thứ tự file, cần bước 1 viết lại vị trí
  ảnh này nếu muốn sửa triệt để" — KHÔNG ép chọn bừa một đáp án tệ hơn trong phạm vi khả thi.

### 3.2 Danh sách 7 điểm cần xem lại (đã xác định từ B8Q + kiểm tay trước đó)

| # | Ảnh | Đang gán đoạn | Vấn đề đã ghi nhận |
|---|---|---|---|
| 1 | `022.png` | 9 | B8Q flag @319s: ảnh tả cảnh đêm/ngồi cạnh ngăn kéo mở, lời đang tả mùi bếp/hơi ấm |
| 2 | `031.png` | 14 | B8Q flag @444s: ảnh tả toà nhà trung tâm hỗ trợ cộng đồng, lời đang tả tiếng nước nhỏ giọt trong bếp |
| 3 | `057.png` | 24 | B8Q flag @824s: ảnh tả tiệm văn phòng phẩm, lời đang tả "lần đầu ghé trung tâm hỗ trợ cộng đồng" — **CHÚ Ý: nội dung này khớp với ảnh #2 (031.png) hơn — kiểm xem có phải 2 ảnh này bị đổi chỗ cho nhau không, nếu phạm vi khả thi của CẢ HAI đều cho phép hoán đổi** |
| 4 | `065.png` | 27 | B8Q flag @952s: ảnh tả mặt tiền viện dưỡng lão, lời đang tả "một người thanh lịch như vậy" |
| 5 | `103.png` | 47 | B8Q flag @1588s: ảnh tả hai người ăn cơm không có sổ tay, lời đang tả "lặng lẽ lấy sổ tay ra" |
| 6 | `027.png`, `028.png` | 12 | Đã xác định trước: lệch đoạn 11 (027, cụm chợ Kamata) và bối cảnh ngân hàng không khớp bữa ăn tang lễ (028) |
| 7 | `073.png`, `074.png` | 31 | Đã xác định trước: nội dung đúng là đoạn 46 (dưa cải + kotatsu), nhưng phạm vi khả thi hẹp — SIÊU NHIỀU KHẢ NĂNG rơi vào nhóm "giới hạn cấu trúc, không sửa được" — vẫn phải KIỂM (đừng giả định), vì biết đâu phạm vi khả thi rộng hơn em tưởng |

Với mục #3, thử đặc biệt: hỏi riêng một câu "057.png và 031.png, ảnh nào khớp đoạn 14 hơn, ảnh nào
khớp đoạn 24 hơn" — nếu câu trả lời gợi ý nên HOÁN ĐỔI hai ảnh này cho nhau, kiểm phạm vi khả thi
của CẢ HAI trước khi đổi (mỗi ảnh phải nằm trong phạm vi khả thi của VỊ TRÍ MỚI).

### 3.3 Sau khi sửa xong — kiểm tra `img_doan.txt` vẫn hợp lệ

```
py -3.13 -c "
import sys; sys.path.insert(0, r'E:\CLAUDE\YOUTUBE\h2dev\pipeline')
import sinh_neo as sn
S = r'E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0'
sn.sinh(S)
" 
```
(hoặc chạy thẳng `py -3.13 sinh_neo.py --slug "<thư mục tập>" --kiem` — nếu báo lỗi "so doan GIAM
(neo lui)" nghĩa là một chỗ sửa đã phá thứ tự không giảm — QUAY LẠI, chỗ đó thuộc nhóm "giới hạn
cấu trúc", không sửa được, trả lại giá trị cũ.

---

## 4. VIỆC 3 — sinh lại neo + chạy lại thật, đo lại B8Q

1. Xoá `anchors.txt`, `final.mp4` trong thư mục tập 11 (bản cũ đã sai, không dùng lại được).
2. `py -3.13 sinh_neo.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0"`
   — phải báo `121 neo hop le`, không lỗi.
3. Đảm bảo VIỆC 1 đã xong (chay_buoc3.py có `--ep`) trước khi chạy bước dưới.
4. `py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 11` — chạy thật. Không tốn tiền giọng.
5. Đọc điểm B8Q trong log/báo cáo `chay_buoc3.py` tự ghi.

---

## 5. TIÊU CHUẨN ĐẠT — không được tự hạ thấp ngưỡng để báo "xong"

- B8Q **phải ≥ 3,5/5** (giữa mốc cũ 3,1 và mốc Lane D 3,8 — không đòi hỏi bằng Lane D vì nội dung
  khác nhau, nhưng phải rõ ràng CẢI THIỆN so với mọi lần trước, không được bằng hoặc thấp hơn 2,9).
- Không còn điểm nào trong 5 điểm B8Q cũ (mục 3.2 #1-5) bị lặp lại NGUYÊN VĂN ở lần đo mới (có thể
  xuất hiện điểm MỚI khác, đó là bình thường, nhưng đừng để đúng 5 điểm cũ vẫn còn nguyên).
- Nếu chạy xong vẫn dưới 3,5/5: KHÔNG tự ý chạy thêm vòng nữa. Dừng, báo cáo trung thực, liệt kê
  đã thử gì, để người giao việc quyết bước tiếp — đừng lặp vòng lặp vô tận.

---

## 6. BÁO CÁO HOÀN THÀNH — file mới

`E:\CLAUDE\YOUTUBE\h2dev\docs\BAO_CAO_HOAN_THANH_TAP11_VONG3.md`:

```markdown
# BÁO CÁO — vòng 3 sửa tập 11

Ngày: <...> · Model: <...> · Thời gian: <tổng phút>

## 1. VIỆC 1 — bug --ep
Trước/sau + kết quả lệnh kiểm (tên thư mục ra đúng ep11-... chưa, dán nguyên văn)

## 2. VIỆC 2 — 7 điểm đã xem lại
Với MỖI điểm (1-7): đoạn cũ → đoạn mới (hoặc "GIỮ NGUYÊN — giới hạn cấu trúc" kèm lý do cụ thể),
phạm vi khả thi đã tính, có hoán đổi 031/057 không (và tại sao)

## 3. Kết quả kiểm img_doan.txt sau sửa
Dán nguyên văn output `sinh_neo.py --kiem`

## 4. Kết quả chạy thật (VIỆC 3-4)
- B8Q mới: <điểm>/5, so với 2,9 (vòng 2) và 3,1 (bản gốc không neo)
- Danh sách mốc lệch mới (nếu còn) — so với 5 mốc cũ, còn trùng mốc nào không
- Tên thư mục giao hàng (phải là ep11-..., không phải ep01-...)
- Cột G, H sau khi ghi (dán nguyên văn từ sheet)

## 5. Đạt tiêu chuẩn mục 5 chưa? (có/không, kèm số liệu)

## 6. Câu hỏi (nếu có)
```

## 7. Tài liệu liên quan

- `pipeline/sinh_img_doan.py`, `pipeline/chay_buoc3.py` — 2 file đang sửa
- `docs/BAO_CAO_HOAN_THANH_PHUONG_AN_B.md`, `docs/BAO_CAO_HOAN_THANH_CHAY_THAT_TAP11.md` — lịch sử
  2 vòng trước, đọc nếu cần đối chiếu chi tiết (không bắt buộc đọc lại từ đầu, mục 0 đã tóm tắt đủ)
