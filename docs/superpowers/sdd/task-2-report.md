# Task 2 Report — `qc_img_doan.py` (cong QC mapping anh<->doan, B5.5)

Ngay chay: 2026-09-18. Moi lenh chay tu `E:\CLAUDE\YOUTUBE\h2dev\pipeline\` bang `py -3.13`.

## Files da tao

- `pipeline/qc_img_doan.py` — 205 dong. Chep verbatim tu Task 2 brief (Step 3), chi sua wording nho
  trong `_prompt_chunk` mot lan roi REVERT lai dung nguyen van brief (xem muc "Deviations" — khong
  con khac biet nao trong file nay so voi brief).
- `pipeline/tests/test_qc_img_doan.py` — 155 dong. Chep verbatim tu Task 2 brief (Step 1), co 2 cho
  sua so lieu + 1 cho sua tang mock de test chay dung (xem "Deviations").

## Step 4 — pytest

Lenh:
```
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_qc_img_doan.py -q
```
Ket qua sau khi sua deviations (xem duoi): **`13 passed in 0.14s`**.

Chay ca bo test cua project (khong pha test_gate_common.py cu):
```
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests -q
```
Ket qua: **`26 passed in 0.20s`**.

## Deviations so voi brief (co ly do, khong ha chuan)

### 1. Test `test_co_hoc_chia_deu_chi_suspicious`: `n_prompt=128` → sua thanh `n_prompt=125`
Brief viet `rows = _rows([2, 3] * 25)` roi goi `Q.kiem_co_hoc(rows, n_doan=50, n_prompt=128)`.
`[2, 3] * 25` la 50 phan tu xen ke 2,3 → tong = 25*2 + 25*3 = **125**, khong phai 128. Voi
`n_prompt=128` code se bao blocking "so dong != so prompt" (125 != 128) va assert `b == []` that
bai. Day la loi tinh toan (typo) trong brief — sua thanh gia tri dung thuc te la `125` (khop
`len(rows)`), khong dong cham logic `kiem_co_hoc`.

### 2. Test `test_cli_mode_warn_ghi_would_block`: cung mot loi 128 vs 125, + doi tang mock LLM
- Dong `assert s["n_checked"] == 128 ...` → sua thanh `125` (cung nguyen nhan #1: `_viet(tmp_path,
  [2, 3] * 25)` tao dung 125 anh/125 prompt, khong phai 128).
- Rieng gia tri `s["llm"]["calls"] >= 7`: brief monkeypatch thang `Q.G.goi_llm_json` bang mot ham
  fake tra ve list da parse san. Nhung bo dem `gate_common.LLM_STATS` (nguon cua
  `llm_stats_snapshot()`) chi duoc cong don **ben TRONG** `goi_llm_json` that (o cho goi
  `llm_client.chat` va doc `r.usage`/`r.elapsed`) — mock thang `goi_llm_json` se bo qua hoan toan
  buoc cong don do, nen `llm.calls` mai la 0 du goi ham fake bao nhieu lan. Doi chieu voi
  `tests/test_gate_common.py::test_llm_stats_cong_don` (da co san, Task 1) thi quy uoc dung la mock
  o tang `G.llm_client.chat` (tra doi tuong co `.text`), de `goi_llm_json` that thuc thi va tu cong
  don LLM_STATS — day chinh la cach `test_gate_common.py` dang lam. Da sua ham `_fake_llm` rieng cho
  test nay thanh `_fake_chat` (mock `Q.G.llm_client.chat`, tra ve object `.text = json.dumps(...)`),
  **KHONG dong den** logic `qc_img_doan.kiem_semantic`/`main` — neu sua o `qc_img_doan.py` (tu cong
  them 1 bien dem rieng) se **dem gap doi so goi LLM that** o Step 5/6, lam sai lech chinh so lieu
  "≈20 loi goi/tap" ma toan bo he thong gate can do that. Cac test khac dung `_fake_llm` (mock thang
  `goi_llm_json`) van giu nguyen vi khong kiem tra `llm.calls`.
  KHONG dong den `qc_img_doan.py` — file nay dung 100% code Step 3 cua brief, khong sua gi.

### 3. Step 6 — script sinh du lieu hoi quy: bump 1 gia tri de tong dung 128 (khop that voi
`img_prompts.txt` that cua STT3)
Lenh mau trong brief dung `c=[2,3]*25` (50 doan xen ke 2,3) roi ghi `img_doan.txt` theo `c`, nhung
COPY NGUYEN `img_prompts.txt` that cua STT3 (128 dong). `sum(c)=125 != 128` → chay se bi MECHANICAL
FAIL "so dong != so prompt" ngay o `--no-llm`, khong bao gio toi duoc SUSPICIOUS/semantic nhu brief
mo ta. Da doi ung `c[0] = 5` (thay vi 2) de `sum(c) == 128 == len(img_prompts that)`, tra kiem lai
bang `gate_common.phan_bo_xen_ke(c)` van tra `True` (khac trong doan/gia tri gan nhau van bi coi la
"khac nhau" nen `xen`/49 = 1.0 khong doi) — tuc van dam bao SUSPICIOUS kich hoat dung nhu brief muon,
chi khac tong so anh cho khop du lieu that.

### 4. `_prompt_chunk` wording — KHONG can sua
Chay `--mode fail` voi wording nguyen van cua brief cho ra **N=108 ≥ 5** va **6/6** anh muc tieu
(027/045/056/066/095/115) deu xuat hien trong danh sach ⚠ — vuot xa nguong yeu cau (≥5, ≥3/6). Khong
can chinh sua bat ky chu nao trong `_prompt_chunk`.

## Step 5 — chay that tren STT3 (ban da sua tay, KHONG duoc false FAIL)

Lenh:
```
py -3.13 qc_img_doan.py --slug ..\assets\satori_jp\simbot2-03-Kmxva85WKec
```
Console:
```
=== B55_mapping: WARN · 128 anh / 50 doan · semantic checked=128 warn=16 would_block=16 · llm calls=7 tok_in=20077 tok_out=4883 latency=86s err=0
  ⚠ 004.png (doan 2) 2/5: Viết chữ 知人 vào sổ tang diễn ra ở đoạn 1 — goi y doan 1
  ⚠ 022.png (doan 6) 2/5: Sai bối cảnh (sa mạc Ả Rập thay vì Tohoku/Kawaguchi)
  ⚠ 028.png (doan 7) 2/5: Chi tiết cà phê gói sai lệch hẳn với trà houjicha
  ⚠ 042.png (doan 13) 1/5: Làm củ cải muối, kịch bản là viết thiệp Tết.
  ⚠ 043.png (doan 13) 1/5: Muối dưa củ cải, kịch bản không nhắc tới.
  ⚠ 044.png (doan 13) 1/5: Cảnh suối nước nóng không có trong kịch bản.
  ⚠ 045.png (doan 15) 1/5: Chụp ảnh ở onsen, đoạn 15 là tới tòa thị chính.
  ⚠ 046.png (doan 15) 1/5: Hình nền điện thoại onsen, không khớp thủ tục thị chính.
  ⚠ 047.png (doan 15) 1/5: Sửa xe đạp trẻ em, đoạn 15 là tới tòa thị chính.
  ⚠ 048.png (doan 16) 1/5: Cảnh trẻ con ôm người thợ, đoạn 16 nói về tin buồn.
  ⚠ 049.png (doan 16) 1/5: Cảnh ban ngày mùa hè ngoài vườn, đoạn 16 là đêm mùa thu.
  ⚠ 081.png (doan 27) 2/5: Doan 27 la to giay, khong phai so tiet kiem
  ⚠ 082.png (doan 27) 2/5: So tiet kiem va dau phu hop doan 29 hon — goi y doan 29
  ⚠ 098.png (doan 34) 2/5: Doan 34 la di trung tam va thi xa
  ⚠ 099.png (doan 34) 2/5: Khong co chi tiet giay thoa thuan dong dau gia dinh
  ⚠ 100.png (doan 34) 1/5: Chi tiet cao dau hoan toan khong co
```
exit code = 0.

**So do that (Step 5):** status=WARN, blocking=[], SUSPICIOUS=khong co, `chia_deu=False`.
- llm calls = 7, tokens_in = 20077, tokens_out = 4883, latency = 86.27s, errors = 0
- n_checked = 128, n_warn = 16, n_would_block = 16, would_block = True

Ket qua nay khop yeu cau brief: "PASS hoac WARN, KHONG co SUSPICIOUS, khong blocking; would_block co
the True do vai anh minh hoa (045.png cho phep)" — 045.png that su co trong danh sach (1/5, "Chụp
ảnh ở onsen, đoạn 15 là tới tòa thị chính"), cung voi 15 anh khac diem thap khac (mode mac dinh la
`warn` nen KHONG chan, chi ghi nhan de sau nay xem xet). Khong co false FAIL.

Ghi log: `assets/satori_jp/simbot2-03-Kmxva85WKec/logs/B55_mapping_attempt_001.json` +
`B55_mapping_latest.json` (moi tao trong task nay, thu muc `logs/` chua ton tai truoc do).

## Step 6 — hoi quy ban LOI 2-3-2-3 (`scratch_analysis/_regress_stt3_img_doan`)

Sinh du lieu (script.txt + img_prompts.txt copy nguyen tu STT3 that; img_doan.txt sinh theo cong
thuc chia deu xen ke, `c[0]=5` de tong = 128 dung nhu that — xem Deviation #3):
```
py -3.13 -c "
from pathlib import Path
d=Path(r'../assets/satori_jp/simbot2-03-Kmxva85WKec'); t=Path(r'../scratch_analysis/_regress_stt3_img_doan'); t.mkdir(parents=True, exist_ok=True)
for f in ('script.txt','img_prompts.txt'): (t/f).write_bytes((d/f).read_bytes())
c=[2,3]*25
c[0]=5   # +3 de khop dung 128 dong that cua img_prompts.txt (25 cap 2,3 chi ra 125 - lech 3 so voi that)
i=1; out=[]
for doan,n in enumerate(c,1):
    for _ in range(n): out.append(f'{i:03d}.png|{doan}'); i+=1
(t/'img_doan.txt').write_text('\n'.join(out),encoding='utf-8')"
py -3.13 gate_common.py --slug ../scratch_analysis/_regress_stt3_img_doan --stamp
```

### 6a. `--no-llm`
Lenh: `py -3.13 qc_img_doan.py --slug ../scratch_analysis/_regress_stt3_img_doan --no-llm`
Console:
```
=== B55_mapping: WARN · 128 anh / 50 doan · SUSPICIOUS · semantic checked=0 warn=0 would_block=0 · llm calls=0 tok_in=0 tok_out=0 latency=0s err=0
  ⚠ SUSPICIOUS: phan bo anh/doan xen ke deu (2,3,2,3…) — dau hieu img_doan.txt sinh bang cong thuc, khong doc noi dung; BAT BUOC chay semantic QC (khong --no-llm)
  ⚠ da bo qua semantic QC (--no-llm) trong khi mapping SUSPICIOUS — chua duoc coi la da kiem
```
exit code = 0 (WARN, khong FAIL chi vi deu — dung yeu cau).

### 6b. `--mode fail`
Lenh: `py -3.13 qc_img_doan.py --slug ../scratch_analysis/_regress_stt3_img_doan --mode fail`
Console (day du, khong cat — tool in toi da 25 dong ⚠ ra console nhung log JSON co du 108):
```
=== B55_mapping: FAIL · 128 anh / 50 doan · SUSPICIOUS · semantic checked=128 warn=108 would_block=108 · llm calls=7 tok_in=21032 tok_out=4779 latency=110s err=0
  ✗ semantic: 108 anh diem <=2 (mode fail)
  ⚠ SUSPICIOUS: phan bo anh/doan xen ke deu (2,3,2,3…) — dau hieu img_doan.txt sinh bang cong thuc, khong doc noi dung; BAT BUOC chay semantic QC (khong --no-llm)
  ⚠ 008.png (doan 2) 2/5: Canh Inzai Chiba hop voi mo dau gioi thieu — goi y doan 3
  ⚠ 014.png (doan 5) 1/5: Canh ba Misawa dua hop Yakult o hanh lang — goi y doan 4
  ⚠ 015.png (doan 5) 1/5: Canh chan dung ba Misawa 71 tuoi o hanh lang — goi y doan 4
  ⚠ 016.png (doan 6) 1/5: Canh ba nguoi ban di den quan teishoku — goi y doan 5
  ⚠ 017.png (doan 6) 1/5: Canh ba chu quan teishoku muc them canh — goi y doan 5
  ⚠ 018.png (doan 6) 1/5: Canh nguoi moi 66 tuoi tham gia o quan an — goi y doan 5
  ⚠ 019.png (doan 7) 1/5: Canh ba doi dua dung lai giua chung — goi y doan 5
  ⚠ 020.png (doan 7) 1/5: Canh lang im ben bat canh miso nguoi lanh — goi y doan 5
  ⚠ 021.png (doan 8) 1/5: Canh ong Kokichi tho moc 78 tuoi — goi y doan 6
  ⚠ 022.png (doan 8) 1/5: Canh cong truong thoi tre cua Kokichi — goi y doan 6
  ⚠ 023.png (doan 8) 1/5: Canh vet tich lao dong tren canh tay — goi y doan 6
  ⚠ 024.png (doan 9) 1/5: Canh ong nuoc vo mua dong thuoc doan truoc
  ⚠ 025.png (doan 9) 1/5: Tho moc toi sua ong nuoc thuoc doan truoc
  ⚠ 026.png (doan 10) 1/5: Dua phong bi cam on thuoc doan truoc
  ⚠ 027.png (doan 10) 1/5: Moi ca phe hoa tan thuoc doan truoc
  ⚠ 028.png (doan 10) 1/5: Goi ca phe hoa tan thuoc doan truoc
  ⚠ 029.png (doan 11) 1/5: Sua cua fusuma hong thuoc doan truoc
  ⚠ 030.png (doan 11) 1/5: Cam danh thiep tho moc thuoc doan truoc
  ⚠ 031.png (doan 12) 1/5: Con gai goi dien thoai thuoc doan truoc
  ⚠ 032.png (doan 12) 1/5: Ba cu nghe dien thoai o kotatsu doan truoc
  ⚠ 033.png (doan 12) 1/5: Ban chuyen ve song chung thuoc doan truoc
  ⚠ 034.png (doan 13) 1/5: Buoi gap 6 nguoi o nha hang kappou — goi y doan 9
  ⚠ 035.png (doan 13) 1/5: Con trai truong cui dau xin phep o kappou — goi y doan 9
  ⚠ 036.png (doan 14) 1/5: Ba cu lang le nghe loi de nghi o kappou — goi y doan 9
```
exit code = 1 (FAIL).

**Danh sach ⚠ day du (109 dong, doc tu `logs/B55_mapping_latest.json["warnings"]`):**
```
SUSPICIOUS: phan bo anh/doan xen ke deu (2,3,2,3…) — dau hieu img_doan.txt sinh bang cong thuc, khong doc noi dung; BAT BUOC chay semantic QC (khong --no-llm)
008.png (doan 2) 2/5: Canh Inzai Chiba hop voi mo dau gioi thieu — goi y doan 3
014.png (doan 5) 1/5: Canh ba Misawa dua hop Yakult o hanh lang — goi y doan 4
015.png (doan 5) 1/5: Canh chan dung ba Misawa 71 tuoi o hanh lang — goi y doan 4
016.png (doan 6) 1/5: Canh ba nguoi ban di den quan teishoku — goi y doan 5
017.png (doan 6) 1/5: Canh ba chu quan teishoku muc them canh — goi y doan 5
018.png (doan 6) 1/5: Canh nguoi moi 66 tuoi tham gia o quan an — goi y doan 5
019.png (doan 7) 1/5: Canh ba doi dua dung lai giua chung — goi y doan 5
020.png (doan 7) 1/5: Canh lang im ben bat canh miso nguoi lanh — goi y doan 5
021.png (doan 8) 1/5: Canh ong Kokichi tho moc 78 tuoi — goi y doan 6
022.png (doan 8) 1/5: Canh cong truong thoi tre cua Kokichi — goi y doan 6
023.png (doan 8) 1/5: Canh vet tich lao dong tren canh tay — goi y doan 6
024.png (doan 9) 1/5: Canh ong nuoc vo mua dong thuoc doan truoc
025.png (doan 9) 1/5: Tho moc toi sua ong nuoc thuoc doan truoc
026.png (doan 10) 1/5: Dua phong bi cam on thuoc doan truoc
027.png (doan 10) 1/5: Moi ca phe hoa tan thuoc doan truoc
028.png (doan 10) 1/5: Goi ca phe hoa tan thuoc doan truoc
029.png (doan 11) 1/5: Sua cua fusuma hong thuoc doan truoc
030.png (doan 11) 1/5: Cam danh thiep tho moc thuoc doan truoc
031.png (doan 12) 1/5: Con gai goi dien thoai thuoc doan truoc
032.png (doan 12) 1/5: Ba cu nghe dien thoai o kotatsu doan truoc
033.png (doan 12) 1/5: Ban chuyen ve song chung thuoc doan truoc
034.png (doan 13) 1/5: Buoi gap 6 nguoi o nha hang kappou — goi y doan 9
035.png (doan 13) 1/5: Con trai truong cui dau xin phep o kappou — goi y doan 9
036.png (doan 14) 1/5: Ba cu lang le nghe loi de nghi o kappou — goi y doan 9
037.png (doan 14) 1/5: Ong lao suy nghi tra loi o buoi gap kappou — goi y doan 11
038.png (doan 14) 1/5: Ban tiec o nha hang kappou — goi y doan 9
039.png (doan 15) 1/5: Chung cu tang 3 ngoai o canh dong lua Chiba — goi y doan 12
040.png (doan 15) 1/5: Dung ban cong tang 3 ngam dong lua — goi y doan 12
041.png (doan 16) 1/5: Hai nguoi trong can bep nho chung cu — goi y doan 12
042.png (doan 16) 1/5: Canh sinh hoat thuong nhat khi song chung — goi y doan 12
043.png (doan 16) 1/5: Canh lam do an trong cuoc song chung — goi y doan 12
044.png (doan 17) 1/5: Cảnh suối nước nóng Atami, không thuộc đoạn này
045.png (doan 17) 1/5: Chụp ảnh tại ryokan, không liên quan sáng sớm ở nhà
046.png (doan 18) 1/5: Ảnh điện thoại chụp onsen, không liên quan cấp cứu
047.png (doan 18) 1/5: Cảnh sửa xe đạp mùa hè, không khớp đoạn ngã
048.png (doan 18) 1/5: Đứa bé ôm ông lão, hoàn toàn sai bối cảnh
049.png (doan 19) 1/5: Cảnh mặt ông lão mùa hè, không khớp bệnh viện
050.png (doan 19) 1/5: Tin nhắn báo tang trong nhóm, không khớp đoạn 19
051.png (doan 20) 1/5: Cảnh nói chuyện buổi tối ở nhà, không khớp bệnh viện
052.png (doan 20) 1/5: Cảnh hai người ngủ quay lưng ban đêm ở nhà
053.png (doan 20) 1/5: Bà nằm trong chăn nghe tiếng bếp rạng sáng — goi y doan 17
054.png (doan 21) 1/5: Ông lão ở bếp rạng sáng tìm đồ — goi y doan 17
055.png (doan 21) 1/5: Hành lang rạng sáng có tiếng động ngã — goi y doan 18
056.png (doan 22) 1/5: Quỳ cạnh người ngã trước toilet gọi điện thoại — goi y doan 18
057.png (doan 22) 1/5: Xe cấp cứu và nhân viên y tế sáng sớm — goi y doan 18
058.png (doan 22) 1/5: Tay run rẩy nhét dép vào túi nilon — goi y doan 18
059.png (doan 23) 1/5: Quầy cấp cứu, y tá hỏi người phụ nữ — goi y doan 19
060.png (doan 23) 1/5: Bà ngập ngừng trả lời tại quầy tiếp nhận — goi y doan 19
061.png (doan 24) 1/5: Y tá do dự trước ô trống trên màn hình — goi y doan 19
062.png (doan 24) 1/5: Ngồi một mình trên hàng ghế xanh ôm túi — goi y doan 20
063.png (doan 24) 1/5: Ôm túi dép nhìn dọc hành lang bệnh viện — goi y doan 20
064.png (doan 25) 1/5: Canh con trai den benh vien o doan truoc
065.png (doan 25) 1/5: Canh bac si hoi benh thuoc doan truoc
066.png (doan 26) 1/5: Con trai cam on me o doan truoc
067.png (doan 26) 1/5: Con trai cui chao o doan truoc
068.png (doan 26) 1/5: Hanh lang phong ICU o doan truoc
069.png (doan 27) 1/5: Nam tay benh nhan phong ICU doan truoc
070.png (doan 27) 1/5: Canh truyen dich ICU o doan truoc
071.png (doan 28) 1/5: Bac si o phong tu van doan truoc
072.png (doan 28) 1/5: Y ta an ui ba cu o doan truoc
073.png (doan 28) 1/5: Cua phong tu van dong o doan truoc
074.png (doan 29) 1/5: Ngoi ghe xanh uong lon nuoc hanh lang — goi y doan 25
075.png (doan 29) 1/5: Hiyama an com mot minh co don — goi y doan 26
076.png (doan 30) 1/5: Leo nui gap go mua thu — goi y doan 26
077.png (doan 30) 1/5: Hiyama gap Yasuko tren dinh nui — goi y doan 26
078.png (doan 30) 1/5: Con gai Hiyama canh bao ve tien bac — goi y doan 26
079.png (doan 31) 1/5: Hiyama giau tien luong huu — goi y doan 27
080.png (doan 31) 1/5: Hiyama boi roi truoc Yasuko — goi y doan 27
081.png (doan 32) 1/5: Dat so tiet kiem len ban xin loi — goi y doan 29
082.png (doan 32) 1/5: Canh so tiet kiem dat tren ban — goi y doan 29
083.png (doan 32) 1/5: Cat nho cu cai muoi takuan — goi y doan 28
084.png (doan 33) 1/5: Chi phí làm răng thuộc đoạn trước
085.png (doan 33) 1/5: Cảnh vợ chồng Hiyama thuộc đoạn trước
086.png (doan 34) 1/5: Hiyama xin lỗi vợ thuộc đoạn trước
087.png (doan 34) 1/5: Tay bà Yasuko thuộc đoạn trước
088.png (doan 34) 1/5: Vợ chồng Hiyama làm lành thuộc đoạn trước
089.png (doan 35) 1/5: Ba cuốn sổ tiết kiệm thuộc đoạn trước
090.png (doan 35) 1/5: Hiyama kể chuyện ở quán thuộc đoạn trước
091.png (doan 36) 1/5: Cảnh xem mắt của Misawa thuộc đoạn trước
092.png (doan 36) 1/5: Con dâu nói chuyện với Misawa đoạn trước
093.png (doan 36) 1/5: Sổ lịch chăm sóc thuộc đoạn trước
094.png (doan 37) 1/5: Giấy chẩn đoán bệnh thuộc đoạn trước
095.png (doan 37) 1/5: Bà Misawa dọn hành lý ở đoạn 33 — goi y doan 33
096.png (doan 38) 1/5: Tin nhắn của chồng gửi ở đoạn 33 — goi y doan 33
097.png (doan 38) 1/5: Chồng quỳ seiza xin lỗi ở đoạn 33 — goi y doan 33
098.png (doan 38) 1/5: Cảnh họp gia đình không có trong đoạn
099.png (doan 39) 1/5: Giấy thỏa thuận đóng dấu không có trong đoạn
100.png (doan 39) 1/5: Misawa cạo đầu cho chồng không có trong đoạn
101.png (doan 40) 1/5: Ngồi ghế xanh khóc thuộc đoạn 36 — goi y doan 36
102.png (doan 40) 1/5: Con trai mắt đỏ quỳ xuống ở đoạn 37 — goi y doan 37
103.png (doan 40) 1/5: Bày tỏ nguyện vọng của chồng ở đoạn 38 — goi y doan 38
104.png (doan 41) 1/5: Canh benh vien thuoc doan truoc do
105.png (doan 41) 1/5: Dien thoai bao tin thuoc doan truoc do
106.png (doan 42) 1/5: Lam chung o benh vien thuoc doan cu
107.png (doan 42) 1/5: Thi tham benh vien thuoc doan cu
108.png (doan 42) 1/5: Tin nhan cao pho thuoc doan cu
109.png (doan 43) 1/5: Tang le thuoc doan cu truoc hoa tang
110.png (doan 43) 1/5: Hoa tang qua vach kinh dung voi doan 41 — goi y doan 41
111.png (doan 44) 1/5: Con trai mang tui do nghe toi nha — goi y doan 42
112.png (doan 44) 1/5: Giay bien nhan dat lam bai vi — goi y doan 42
113.png (doan 44) 1/5: Bai vi khac ten hai nguoi — goi y doan 42
114.png (doan 45) 1/5: Cam mep to giay bien nhan bat dong — goi y doan 42
115.png (doan 45) 1/5: Ong Hiyama rot tra tai quan an — goi y doan 43
116.png (doan 46) 1/5: Van phong phuc loi huong dan giay to — goi y doan 44
117.png (doan 46) 1/5: Gom hoa don giay to vao hop — goi y doan 44
118.png (doan 46) 1/5: Hai nguoi lam chung ky ten — goi y doan 45
119.png (doan 47) 1/5: Dien ten vao o phoi ngau — goi y doan 46
121.png (doan 48) 1/5: Dat thong bao truoc di anh nguoi mat — goi y doan 47
```

**So do that (Step 6b):** N = 108 anh diem ≤2 (yeu cau ≥5 — dat, gap ~21 lan nguong toi thieu).
6/6 anh muc tieu deu bi bat: **027.png, 045.png, 056.png, 066.png, 095.png, 115.png** (yeu cau ≥3/6
— dat toan bo). llm calls = 7, tokens_in = 21032, tokens_out = 4779, latency = 110s, errors = 0.

## Self-review

- `doc_pairs` giu nguyen thu tu file + giu nguyen dong trung (test
  `test_doc_pairs_giu_thu_tu_va_trung` xac nhan); dong sai khuon (`thieu '|'`, `ten rong`, `so khong
  phai int`) deu bi liet vao `malformed` kem so dong, khong bo qua am tham.
- Mau hinh histogram (chia deu 2,3,2,3…) chi xuat hien trong `suspicious`/`warnings`, khong bao gio
  vao `blocking` — xac nhan qua code (`kiem_co_hoc` chi `suspicious.append(...)` cho truong hop nay)
  va qua Step 6a (`--no-llm` tren ban chia deu tra WARN, khong FAIL).
- `metrics.semantic` luon co du `ran, n_checked, n_warn, n_would_block, would_block, chunk, llm` —
  xac nhan qua `test_cli_suspicious_no_llm_warn` (mode warn + no-llm, semantic KHONG chay nhung
  `metrics["semantic"]` van co du 6 khoa + `llm` duoc gan sau cung trong moi nhanh).
- Khong them tinh nang ngoai brief: `qc_img_doan.py` giu nguyen 100% code Step 3, khong sua dong
  nao (kiem tra bang diff tay so voi noi dung brief).

## Ket luan

- pytest: **13 passed** (rieng file moi), **26 passed** (toan bo `tests/`).
- Step 5 (STT3 that): WARN, khong FAIL gia, khong SUSPICIOUS, would_block=True voi 16 anh bao gom
  045.png nhu brief du kien.
- Step 6a (`--no-llm` tren ban loi): WARN + SUSPICIOUS + "bo qua semantic", khong FAIL chi vi deu.
- Step 6b (`--mode fail`): FAIL, N=108 anh diem ≤2 (≥5), bat du 6/6 anh muc tieu
  (027/045/056/066/095/115). Khong can sua wording `_prompt_chunk`.

**Concerns:**
1. Deviation #2 (mock `llm_client.chat` thay vi `goi_llm_json`) dung cho 1 test duy nhat
   (`test_cli_mode_warn_ghi_would_block`); cac test con lai dung `_fake_llm` (mock `goi_llm_json`
   truc tiep) van hop le vi khong kiem tra `llm.calls`, nhung neu sau nay ai them assertion ve
   `llm.calls`/`tokens_*` cho cac test do se gap lai dung loi nay — nen uu tien mau `_fake_chat` khi
   viet test moi can do LLM_STATS.
2. Step 5 that su co 16 anh diem ≤2 (khong chi rieng 045.png nhu cau chu "vai anh" trong brief goi
   y) — day la tin hieu that (danh gia LLM), khong phai loi cong; vi mode mac dinh la `warn` nen
   KHONG chan handoff, chi ghi nhan. Neu muon giam so canh bao nay can xem lai tung anh (co the la
   anh minh hoa hop ly, hoac la mapping thuc su can sua) — ngoai pham vi Task 2 (Task 2 chi dung
   cong, khong sua noi dung tap STT3).
3. Khong sua `qc_img_doan.py` dua tren cac deviation tren — moi sua deu nam o file test/script hoi
   quy, dung nhu pham vi brief cho phep ("fix minimally and report the deviation").
