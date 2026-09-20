# GIAO VIỆC — Phương án B: sửa neo ảnh↔lời cho tập 11, rồi dùng chính tập 11 làm bài test thật cho `chay_buoc3.py`

File này tự chứa. Đọc hết rồi làm theo ĐÚNG THỨ TỰ, không cần hỏi ai, không cần đọc lịch sử chat.
Mọi lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev\pipeline`, luôn dùng `py -3.13`.

## 0. BỐI CẢNH — ĐỌC KỸ TRƯỚC KHI VIẾT DÒNG CODE NÀO, TRÁNH LẶP LẠI 3 LẦN THẤT BẠI TRƯỚC

`sinh_img_doan.py` (gán ảnh → số đoạn kịch bản) đã bị viết lại 3 lần, LẦN NÀO CŨNG HỎNG THEO KIỂU
KHÁC NHAU. Đọc kỹ để không đi lại đúng ba con đường cụt này:

1. **Hỏi lô 30 ảnh + mục lục 52 đoạn cắt cụt 70 ký tự** → model bão hoà, dồn hết về đoạn CUỐI
   (đo thật: đoạn 52/52 nhận 28 ảnh). Sửa bằng cửa sổ gợi ý theo vị trí — đỡ hơn nhưng vẫn kẹt.
2. **Giữ đề xuất của LLM, nắn nhịp bằng thuật toán cơ học sau đó** (đẩy ảnh dư sang đoạn lân cận
   còn chỗ) → nhịp rất đẹp (0 ảnh <3s, 0 ảnh >30s) nhưng **NỘI DUNG SAI HẲN**: đoạn 46 (chiều
   28/12 rét đậm, chị mang dưa cải đến thăm) bị gán cụm ảnh tiệc đầu năm; đoạn 39 (giữ bí mật số dư
   đến chết, chỉ để lại sổ+con dấu) bị gán cụm ảnh đi thăm nhà bạn mùa đông.
   **BÀI HỌC QUAN TRỌNG NHẤT: SỐ ĐẾM và NỘI DUNG LÀ CÙNG MỘT BIẾN** — ảnh viết đúng thứ tự kịch
   bản, nên đẩy một ảnh đi chữa nhịp là mọi ảnh phía sau trôi theo. KHÔNG được nắn nhịp bằng cách
   dịch chuyển gán ảnh mà không xét lại nội dung.
3. **Đổi cách hỏi: quét từng đoạn, hỏi "mấy ảnh kế tiếp thuộc đoạn này (0..K)"** → LLM luôn trả về
   ĐÚNG SỐ NHỎ NHẤT luật cho phép, bất kể ngân sách gợi ý bao nhiêu. **KẾT LUẬN: model đoán được
   ẢNH NÀY TẢ CẢNH GÌ, nhưng KHÔNG ĐẾM ĐƯỢC bao nhiêu ảnh nên gán cho một đoạn.**

**Hướng đúng (Phương án B), dùng ở việc 2 dưới đây:** đừng bắt LLM đếm hay tự sắp xếp gì cả — chỉ
hỏi nó câu MULTIPLE-CHOICE cực hẹp: "ảnh NÀY khớp đoạn NÀO trong đúng {8-10} đoạn ứng viên quanh vị
trí của nó" (viết đầy đủ, KHÔNG cắt cụt). Việc dồn-đều-theo-sức-chứa giao hẳn cho `can_bang()` —
hàm này ĐÃ VIẾT, ĐÃ TEST 200 CA NGẪU NHIÊN, ĐANG CHẠY ĐÚNG trong `sinh_img_doan.py` hiện tại — TÁI
DÙNG NGUYÊN VẸN, đừng viết lại.

---

## 1. ⛔ CẤM TUYỆT ĐỐI

1. Không đụng lane nào khác ngoài `satori-jp-obaa`.
2. Không xoá dòng/cột/dữ liệu Google Sheet — chỉ được CẬP NHẬT đúng ô đã quy định ở việc 5.
3. Không chạy `render_engine.py` nhiều lần tuỳ ý để "thử" — mỗi lần chạy tốn thời gian máy thật
   (không tốn tiền TTS vì giọng tập 11 đã có sẵn, nhưng B5/B8Q vẫn tốn thời gian thật). Chỉ chạy
   THẬT đúng 1 lần ở việc 5, sau khi đã xác nhận số liệu + nội dung ở việc 4.
4. Không xoá `voice.mp3`, `voice.srt`, `script.txt`, `img_prompts.txt` của tập 11 — chỉ được XOÁ
   và SINH LẠI `img_doan.txt`, `anchors.txt`, `final.mp4` (ba file này là sản phẩm của chính việc
   đang sửa, xoá đi làm lại là đúng việc).
5. Không tự ý sửa `characters.json`, `master_prompts*.txt`.

---

## 2. VIỆC 1 (làm trước, đơn giản, đã có công thức đúng) — sửa cách chọn neo trong `sinh_neo.py`

**Lỗi hiện tại:** hàm `sinh()` chọn neo bằng "cue SỚM NHẤT còn cách neo trước ≥1 giây" — khiến mọi
ảnh trong cùng một đoạn dồn hết về ĐẦU đoạn, để trống hẳn phần sau. Đo thật: cách này cho `max`
45,0s và 17 ảnh <3 giây trên cùng một bộ gán ảnh→đoạn.

**Cách sửa — TRẢI ĐỀU THEO THỜI GIAN trong dải cue của đoạn:**

Tìm đoạn code (khoảng dòng 152-161 hiện tại, tìm theo comment `CHON NEO TUAN TU TOAN CUC`):
```python
chon, cue_truoc = {}, -10.0
for p in anh:
    i, j = dai[m[p.name] - 1]
    k = next((t for t in range(i, j + 1) if cues[t][0] - cue_truoc >= TOI_THIEU_GIAY), None)
    if k is None:
        loi.append(f"doan {m[p.name]} khong con cho cho {p.name} ...")
        break
    chon[p.name] = k
    cue_truoc = cues[k][0]
```
Thay bằng (dùng lại `nhom` — dict đoạn→danh sách tên ảnh, ĐÃ CÓ SẴN ngay phía trên đoạn này trong
file, đừng xây lại):
```python
import collections
chon, cue_truoc = {}, -10.0
da_dat = collections.Counter()
for p in anh:
    so_doan = m[p.name]
    i, j = dai[so_doan - 1]
    n_trong_doan = len(nhom[so_doan])
    k_thu = da_dat[so_doan]                 # anh nay la anh thu may (0-based) trong doan
    da_dat[so_doan] += 1
    t0 = cues[i][0]
    t1 = cues[j + 1][0] if j + 1 < len(cues) else cues[-1][0] + 1.0
    muc = t0 + (t1 - t0) * k_thu / n_trong_doan       # moc thoi gian mong muon, trai deu
    ung = [t for t in range(i, j + 1) if cues[t][0] - cue_truoc >= TOI_THIEU_GIAY]
    if not ung:
        loi.append(f"doan {so_doan} khong con cho cho {p.name} (cac cue con lai cach neo "
                   f"truoc < {TOI_THIEU_GIAY}s) — bot anh o doan nay trong img_doan.txt")
        break
    k = min(ung, key=lambda t: abs(cues[t][0] - muc))  # cue GAN MOC NHAT trong so con hop le
    chon[p.name] = k
    cue_truoc = cues[k][0]
if loi:
    return [], loi
```
Phần còn lại của hàm (mô phỏng `anchor_durations`, kiểm tra <1s) GIỮ NGUYÊN không đổi.

**Kiểm bằng đo, không phải bằng mắt:** viết một script tạm (không cần commit vào dự án) mô phỏng
đúng phép tính `anchor_durations` trên bộ neo mới sinh cho tập 11 (dùng
`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0`), so sánh với bộ neo CŨ đang nằm
trên đĩa. Phải cải thiện rõ: **số ảnh <3 giây giảm xuống gần 0**, **thời lượng dài nhất giảm** so
với bản cũ (bản cũ: max 45,0s với đề xuất tỉ lệ, hoặc xem số đo trong `anchors.txt` cũ nếu vẫn còn
trên đĩa). Ghi số đo thật vào báo cáo (việc 6).

---

## 3. VIỆC 2 (việc khó, làm sau) — viết lại thuật toán chính trong `sinh_img_doan.py`

**GIỮ NGUYÊN** các hàm sau, KHÔNG viết lại: `doc_doan()`, `doc_prompt()`, `suc_chua()`,
`can_bang()`. Chỉ thay `hoi_mot_lo()` và toàn bộ vòng lặp gọi nó trong `main()`.

### 3.1 Bước 1 — tính "đoạn trung tâm" cho từng ảnh theo TỈ LỆ THỜI GIAN THẬT (không theo index)

```python
def doan_trung_tam(S, doan, N):
    """[so_doan_trung_tam moi anh, 1..N]. Dung TY LE THOI GIAN THAT cua tung doan (khong phai
    tỷ lệ theo SO LUONG doan) — anh thu i (0-based) nam o vi tri i/N trong toan bo audio."""
    import sinh_neo as sn
    f = sn.tim_srt(S)
    P = len(doan)
    if not f:
        # khong co SRT (chua chay TTS) — uoc theo do dai doan, cung tot hon chia deu theo SO LUONG
        do_dai = [len(d) for d in doan]
        tong = sum(do_dai)
        cong = [0]
        for d in do_dai:
            cong.append(cong[-1] + d)
    else:
        cues = sn.parse_srt_cues(f)
        dai = sn.dai_cue_cua_doan(doan, cues)
        het = cues[-1][0]
        tg = []
        for i2, j2 in dai:
            t0 = cues[i2][0]
            t1 = cues[j2 + 1][0] if j2 + 1 < len(cues) else het
            tg.append(max(0.1, t1 - t0))
        tong = sum(tg)
        cong = [0]
        for t in tg:
            cong.append(cong[-1] + t)
    ra = []
    for i in range(N):
        pos = (i + 0.5) / N * tong          # vi tri thoi gian mong muon cua anh thu i
        p = next((k for k in range(1, P + 1) if cong[k] >= pos), P)
        ra.append(p)
    return ra
```

### 3.2 Bước 2 — cửa sổ ứng viên quanh đoạn trung tâm, TỰ NỚI RỘNG nếu không xếp vừa

```python
def cua_so(trung_tam, P, K):
    return [max(1, trung_tam - K), min(P, trung_tam + K)]
```
`K` bắt đầu = 4 (cửa sổ ~9 đoạn). Nếu sau khi chạy xong `can_bang()` vẫn báo `None` (không xếp
vừa), THỬ LẠI với `K = 6` rồi `K = 9`, tối đa 3 lần. Vẫn `None` ở K=9 → dừng thật, báo lỗi rõ ràng
(kịch bản quá ngắn so với số ảnh) — đừng đoán bừa, đừng hạ ngưỡng capacity.

### 3.3 Bước 3 — hỏi LLM, MULTIPLE-CHOICE trong cửa sổ, KHÔNG cắt cụt nội dung đoạn

Hỏi theo LÔ (ví dụ 20 ảnh/lô, giữ `--lo` như cũ), nhưng MỖI ảnh trong lô liệt kê ĐÚNG cửa sổ CỦA
RIÊNG NÓ (không dùng chung một cửa sổ cho cả lô — các ảnh trong cùng lô có thể có cửa sổ khác
nhau vì vị trí trung tâm khác nhau):

```python
def hoi_mot_lo(doan, lo, trung_tam_lo, K):
    """lo: [(ten_anh, prompt)]. trung_tam_lo: {ten_anh: so_doan_trung_tam}.
    Tra {ten_anh: so_doan} — MOI ANH mot lua chon, LAY TU CUA SO RIENG cua no."""
    cau = []
    for ten, txt in lo:
        tt = trung_tam_lo[ten]
        lo_min, lo_max = cua_so(tt, len(doan), K)
        ds_doan = "\n".join(f"    {p}. {doan[p-1][:200]}" for p in range(lo_min, lo_max + 1))
        cau.append(f"ANH {ten}: {txt[:180]}\n  CAC DOAN UNG VIEN (chon DUNG MOT so trong day):\n{ds_doan}")
    ask = ("Voi MOI anh duoi day, chon DUNG MOT doan trong danh sach ung vien rieng cua no — "
           "doan nao ta dung noi dung/canh vat/hanh dong ma anh do the hien nhat. KHONG duoc chon "
           "so ngoai danh sach ung vien cua chinh anh do.\n\n" + "\n\n".join(cau) +
           "\n\nTra ve DUNG moi dong mot cho moi anh, dinh dang `<ten anh>|<so doan>`, "
           "khong giai thich, khong markdown.")
    kq = chat(ask, task="short", max_tokens=4000, temperature=0.1, verbose=False)
    kq = getattr(kq, "text", kq) or ""
    ra = {}
    for ln in kq.splitlines():
        m = re.match(r"\s*([0-9]{3}\.png)\s*\|\s*(\d+)", ln.strip())
        if m:
            ra[m.group(1)] = int(m.group(2))
    return ra
```

### 3.4 `main()` — ráp lại vòng lặp

```python
N = len(prompts)
K = 4
for lan_thu in range(3):
    trung_tam = dict(zip((t for t, _ in prompts), doan_trung_tam(S, doan, N)))
    chua = suc_chua(S, doan)                 # GIU NGUYEN ham cu
    ket = {}
    for i in range(0, N, a.lo):
        lo = prompts[i:i + a.lo]
        tra = hoi_mot_lo(doan, lo, trung_tam, K)
        # KEP CUNG vao cua so rieng cua TUNG anh — LLM co the lo mo chon ngoai du da dan
        for ten, _ in lo:
            if ten in tra:
                lo_min, lo_max = cua_so(trung_tam[ten], len(doan), K)
                tra[ten] = max(lo_min, min(tra[ten], lo_max))
        ket.update(tra)
        print(f"  lo {i//a.lo + 1}: {len(tra)}/{len(lo)} anh (K={K})")

    so_bu = sum(1 for ten, _ in prompts if ten not in ket)
    truoc, de_xuat = 1, []
    for ten, _ in prompts:
        v = max(1, min(ket.get(ten, truoc), len(doan)))
        de_xuat.append(v)
        truoc = v
    cuoi = can_bang(de_xuat, chua)            # GIU NGUYEN ham cu, da test 200 ca
    if cuoi is not None:
        break
    print(f"  K={K} khong xep vua, noi rong cua so...")
    K += 2 if K < 8 else 5                    # 4 -> 6 -> 9 (lan thu 3 het )
else:
    print(f"✗ khong xep vua sau 3 lan noi cua so (K toi da {K}): kich ban qua ngan so voi so anh.")
    return 1

so_doi = sum(1 for x, y in zip(de_xuat, cuoi) if x != y)
ra = [(ten, v) for (ten, _), v in zip(prompts, cuoi)]
# ... phan ghi file + in bao cao GIU NGUYEN nhu code cu (dong_nhat, canh bao >15%...)
```

**Ghi chú quan trọng:** đoạn code trên là KHUNG THAM KHẢO, không phải chép y nguyên bắt buộc — có
thể chỉnh biến/tên hàm cho khớp phong cách phần còn lại của file, MIỄN GIỮ ĐÚNG 3 Ý: (1) trung tâm
tính theo tỉ lệ THỜI GIAN thật, (2) cửa sổ hẹp riêng từng ảnh không cắt cụt nội dung đoạn,
(3) `can_bang()` giữ nguyên làm lưới an toàn cuối, tự nới cửa sổ nếu không xếp vừa.

---

## 4. TEST BẮT BUỘC trên CHÍNH tập 11 — số liệu VÀ nội dung, không được chỉ đo một chiều

Thư mục: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-11-DXXwIxhcfF0`

1. **Xoá** `img_doan.txt`, `anchors.txt` cũ trong thư mục đó (đã sai, không dùng lại được).
2. Chạy: `py -3.13 sinh_img_doan.py --slug "<thư mục trên>"` rồi `py -3.13 sinh_neo.py --slug "<thư mục trên>"`.
3. **Đo bằng số** — mô phỏng lại `anchor_durations` (viết script tạm, không cần commit) trên
   `anchors.txt` MỚI sinh ra. So với các ngưỡng đã biết từ các lần thử trước:
   - Số ảnh <3 giây: phải **thấp hơn hẳn** 17 (con số của bản neo-sớm-nhất cũ).
   - Thời lượng dài nhất: phải **thấp hơn hẳn** 282 giây (con số của bản render đang có trên đĩa).
   - `can bang doi` (số dòng bị `can_bang()` sửa): càng THẤP càng tốt, mục tiêu dưới 15% (121 ảnh
     → dưới ~18 dòng bị đổi). Đây là số đo TRỰC TIẾP cho biết cửa sổ mới có sát vị trí thật không.
4. **Kiểm NỘI DUNG bằng tay — KHÔNG được bỏ qua bước này dù số liệu đẹp.** Mở `script.txt`, đọc
   nguyên văn đoạn số **12, 30, 39, 46** (đây là 4 đoạn đã biết CÁC HƯỚNG TRƯỚC ĐÃ SAI). Với mỗi
   đoạn, in ra: (a) nguyên văn đoạn kịch bản, (b) tên + nội dung prompt của các ảnh MỚI được gán
   cho đoạn đó. Tự đọc và tự đánh giá bằng lý lẽ (không có đáp án đúng cho sẵn ở đây, phải tự phán
   đoán như một người đọc thật): ảnh có tả đúng cảnh trong đoạn không? Nếu có đoạn nào rõ ràng
   không khớp (ví dụ đoạn tả "trời rét đậm tháng 12" mà ảnh tả "tiệc mừng năm mới ấm cúng" — hai
   bối cảnh khác hẳn), GHI RÕ vào báo cáo, ĐỪNG che giấu, kể cả khi số liệu tổng thể đẹp.
5. Nếu bước 4 phát hiện nội dung sai rõ ràng ở ≥2 trong 4 đoạn kiểm — coi như CHƯA ĐẠT, quay lại
   việc 2 chỉnh `K` (cửa sổ) hoặc cách hỏi, KHÔNG được nộp báo cáo nói "đạt" khi nội dung sai.

---

## 5. SAU KHI ĐẠT (số liệu + nội dung) — chạy thật, gỡ khoá, dùng chính tập 11 làm bài test `chay_buoc3.py`

1. Xoá `final.mp4` cũ trong thư mục tập 11 (bản KHÔNG neo, điểm 3,1/5, không dùng được nữa).
2. Cập nhật cột H dòng 11 của tab `Lopezzapa68` (spreadsheet ID
   `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`) — dùng MCP `gsheets`, chỉ đọc rồi GHI ĐÈ đúng ô
   H12 (STT 11 nằm ở dòng sheet 12), **giữ nguyên phần "Deepseek trả lời Claude..." phía trước**,
   chỉ thay đoạn `TẠM DỪNG — chờ sửa neo ảnh, KHÔNG chạy bước 3` thành:
   `HẾT TẠM DỪNG — đã sửa neo ảnh (đo: <điền số liệu thật>), sẵn sàng chạy bước 3`
3. Chạy THẬT (không phải `--thu`):
   ```
   py -3.13 chay_buoc3.py --tab Lopezzapa68 --dong 11
   ```
   Đây KHÔNG tốn tiền TTS (giọng đã có sẵn từ trước, `render_engine.py` tự resume bỏ qua bước B4).
   Sẽ tốn thời gian máy thật cho B5Q/B7.5/B8/B8Q/giao hàng — để nó chạy hết, đừng Ctrl+C giữa
   chừng trừ khi thấy nó đi vào B5 (gen ảnh mới, KHÔNG nên xảy ra vì ảnh tập 11 đã đủ 121/121 —
   nếu thấy B5 chạy thật, DỪNG NGAY, đó là dấu hiệu đếm ảnh sai).
4. Đọc log/report do `chay_buoc3.py` tự ghi (file trong `BAO_CAO_BUOC3\` + cột H nó tự cập nhật) —
   không cần tự viết báo cáo riêng cho bước này, `chay_buoc3.py` đã tự làm.

---

## 6. BÁO CÁO HOÀN THÀNH — file MỚI, không nối vào các báo cáo trước (việc khác hẳn)

`E:\CLAUDE\YOUTUBE\h2dev\docs\BAO_CAO_HOAN_THANH_PHUONG_AN_B.md`, đúng khuôn:

```markdown
# BÁO CÁO HOÀN THÀNH — Phương án B (neo ảnh tập 11)

Ngày làm: <...> · Model: <...> · Thời gian: <tổng phút>

## 1. VIỆC 1 — sửa sinh_neo.py
Trước/sau (trích đoạn code) + số đo (max/`<3s`/`<1s` trước và sau)

## 2. VIỆC 2 — thuật toán mới sinh_img_doan.py
Trước/sau + số lần K phải nới rộng (nếu có) + số đo cuối (can bang doi bao nhiêu %, dong nhat bao nhiêu anh)

## 3. Kiểm nội dung tay — đoạn 12, 30, 39, 46
Với MỖI đoạn: nguyên văn đoạn + ảnh được gán + tên/prompt ảnh đó + TỰ NHẬN XÉT khớp hay không
(thành thật — có sai thì ghi sai, đừng tô hồng)

## 4. Kết quả chạy thật chay_buoc3.py --dong 11
- Đường dẫn báo cáo BAO_CAO_BUOC3 nó tự ghi
- B8Q điểm bao nhiêu (so với 3,1/5 cũ)
- Đường dẫn giao hàng cuối cùng (nếu ĐẠT)
- Nếu KHÔNG đạt: dừng ở đâu, log gì

## 5. Rủi ro / việc chưa làm

## 6. Câu hỏi
```

## 7. Tài liệu nên đọc

- `pipeline/sinh_img_doan.py`, `pipeline/sinh_neo.py` — 2 file đang sửa, đọc docstring đầu file
- `pipeline/chay_buoc3.py` — công cụ sẽ dùng ở việc 5, KHÔNG sửa file này
- `CLAUDE-DEEPSEEK-satori.TXT` — bối cảnh đầy đủ vụ tập 11 (không bắt buộc đọc lại nếu đã hiểu mục 0)
