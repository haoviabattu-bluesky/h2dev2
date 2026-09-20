# SYNCTHING LAN — THAY GOOGLE DRIVE LÀM TRUNG GIAN 2 MÁY (DỰ THẢO 2026-09-14)

> Trạng thái: **ĐANG TRIỂN KHAI** — máy 1 đã cài + sinh device ID + cấu hình 4 folder qua REST API
> (đã verify thành công). Còn thiếu: máy 2 chạy SETUP + gửi device ID → chạy CAU_HINH cả 2 máy →
> bật serve cả 2 → kiểm tra sync. Drive vẫn chạy song song tới khi Syncthing ổn định.

## 0. Thông tin thực tế (đã xác minh 2026-09-14)

| | Máy 1 | Máy 2 |
|---|---|---|
| Tên máy | `DESKTOP-MRQD8T5` | **`PC-MANTO`** (đã scan LAN tìm thấy) |
| IP LAN | `192.168.1.7` (Ethernet) · `192.168.2.220` (Wi-Fi) | **`192.168.1.19`** (Ethernet, cùng mạng `.1.x` với máy 1) |
| Device ID | `UIMW6PL-JJATL7Z-MBYH4TX-L7XAWAB-EWRKBBZ-MYXEX3B-BMCUZ4O-XG6NIQ5` | chờ SETUP |
| Config dir | `E:\CLAUDE\YOUTUBE\h2dev\tools\syncthing\config-may1` | `...\syncthing\config` (do SETUP_MAY2.bat tạo) |

Công cụ đặt tại `E:\CLAUDE\YOUTUBE\h2dev\tools\syncthing\`: `syncthing-windows-amd64-v2.1.5\`
(binary), `SETUP_MAY2.bat` + `START_SYNCTHING.bat` (chạy trên máy 2), `START_SYNCTHING_MAY1.bat`
(máy 1), `CAU_HINH_MAY1.py` + `CAU_HINH_MAY2.py` (cấu hình qua REST API).

⚠️ Device ID = **63 ký tự** (không phải 52) — script check 52-63.

## 1. Vì sao

Google Drive làm trung gian tốn **~1 GB/tập** ảnh (quota 16 GB cạn sau ~2 tập — đã đo thật 2026-09-14,
đã thêm bước D+ tự dọn). Syncthing đồng bộ **trực tiếp qua LAN chung router**, 0 quota, tốc độ ~100 MB/s
(1 tập ~1 GB ⇒ ~1 phút), và **mỗi máy giữ bản local đầy đủ** — máy 1 tắt vẫn không ảnh hưởng máy 2
(Syncthing ≠ SMB share: không phải "máy 2 nhìn vào máy 1" mà là "cả 2 có bản sao riêng").

## 2. Sơ đồ luồng dữ liệu + folder types (BẮT BUỘC đúng — sai type là conflict)

| Thư mục | Máy 1 (sản xuất) | Máy 2 | Chiều |
|---|---|---|---|
| `FlowHandoff/jobs/` | **Send Only** (gửi hồ sơ prompt) | **Receive Only** | 1 → 2 |
| `FlowHandoff/results/` | **Receive Only** (nhận ảnh) | **Send Only** (gửi ảnh) | 2 → 1 |
| `FlowHandoff/shared/` | **Send & Receive** (skill/tài liệu chung) | **Send & Receive** | ↔ |
| `CHANEL/<kênh>/` (video giao hàng) | **Send Only** (gửi video để upload) | **Receive Only** | 1 → 2 |

Quy tắc: **send-only chặn mọi thay đổi từ phía kia** (máy nhận không sửa được dữ liệu gửi tới),
receive-only chặn thay đổi local lan sang máy kia. Dùng 2 chiều tùy tiện = file xung đột `.sync-conflict-*`.
Khoá kết nối = **device ID** (52 ký tự, như số tài khoản) — không có password, ai có device ID mới
ghép được.

## 3. Đã làm trên máy 1 (xong)

- Tải + giải nén **Syncthing v2.1.5** Windows amd64 (12 MB):
  `E:\CLAUDE\YOUTUBE\h2dev\tools\syncthing\syncthing-windows-amd64-v2.1.5\syncthing.exe`
- Sinh config + key: `syncthing.exe generate --home="E:\CLAUDE\YOUTUBE\h2dev\tools\syncthing\config-may1"`
  → `config.xml` + `cert.pem` + `key.pem`
- **Device ID máy 1: `UIMW6PL-JJATL7Z-MBYH4TX-L7XAWAB-EWRKBBZ-MYXEX3B-BMCUZ4O-XG6NIQ5`**
- Máy 1: Windows, hostname `DESKTOP-MRQD8T5`, IP LAN `192.168.2.220` (Wi-Fi, chung router với máy 2)
- GUI quản trị mặc định: `http://127.0.0.1:8384` (API key trong `config.xml`)

## 4. Làm trên máy 2 (cần user hoặc truy cập máy 2)

### 4a. Cài Syncthing (Windows)
```powershell
# Tải bản windows-amd64 mới nhất: https://github.com/syncthing/syncthing/releases/latest
# Giải nén, chạy 1 lần để sinh config:
syncthing.exe generate --home="C:\syncthing\config"
# Lấy device ID:
syncthing.exe device-id --home="C:\syncthing\config"
```
(Linux/macOS: tải bản tương ứng, `syncthing generate --home=...`; macOS có thể dùng `brew install syncthing`.)

### 4b. Ghép nối (2 chiều — làm cả 2 máy)
- Máy 1 GUI → Actions → Show ID → copy device ID máy 1 → dán vào máy 2 "Add Remote Device"
- Máy 2 copy device ID của nó → dán vào máy 1 "Add Remote Device"
- (Hoặc sửa `config.xml` trực tiếp: thêm `<device id="..." name="...">` vào `<device id="mình">...</device>`)
- Kiểm tra: GUI máy 1 thấy thiết bị máy 2 sáng xanh (connected) — cùng LAN, không cần mở NAT/relay.

### 4c. Tạo 4 folder đúng type (bảng mục 2)
- GUI → Add Folder: điền `Folder ID` (vd `jobs`, `results`, `shared`, `chanel`), `Folder Path`, **Folder Type** theo bảng, tick đúng thiết bị ở mục Sharing.
- `CHANEL/<kênh>`: tạo thư mục `E:\CLAUDE\YOUTUBE\CHANEL\` trên máy 2 nếu chưa có (hoặc đường dẫn tương đương), sync cả cây.
- **Cách tự động (khuyên dùng — không cần GUI): chạy script CAU_HINH (xem mục 8)**

### 4d. Firewall (2 máy)
Mở 2 cổng cho syncthing.exe: **TCP 22000** (truyền dữ liệu) + **UDP 21027** (tìm thiết bị LAN).
Windows sẽ hỏi khi chạy lần đầu (tick Private networks) — nếu lỡ chặn:
```powershell
New-NetFirewallRule -DisplayName "Syncthing" -Direction Inbound -Program "C:\syncthing\syncthing.exe" -Action Allow -Profile Private
```

### 4e. Tự chạy khi khởi động (cả 2 máy)
- Windows: `Win+R` → `shell:startup` → tạo shortcut trỏ `syncthing.exe serve --home="<thư mục config>"`
  (hoặc cài service: `sc.exe create Syncthing ...` / dùng NSSM).
- Linux: systemd unit sample trong thư mục `etc/` của bản cài.
- LƯU Ý chạy nền: log ra file riêng (`--logfile`), GUI chỉ mở khi cần.

## 5. Chỉnh workflow sau khi Syncthing OK (chưa làm — chờ user duyệt cắt Drive)

- `drive_handoff.py` hiện up/download qua Drive API. Khi chuyển hẳn sang Syncthing:
  - `upload-job` → chép local vào `FlowHandoff/jobs/<slug>/` (Syncthing tự gửi) — có thể bỏ hẳn Drive.
  - `download-result` → đọc `FlowHandoff/results/<slug>/` local (máy 2 gửi sang tự động).
  - Bước D+ dọn Drive → **không cần nữa** (chỉ cần giữ bản local; có thể giữ thêm `clean-job` vô hại).
- Video giao hàng: `CHANEL/` đã ở trong sync → máy 2 (auto list) đọc local, không cần kéo qua Drive.
- Giữ Drive làm **fallback** 1-2 tập đầu song song, so kết quả rồi mới cắt.

## 6. Kiểm tra / số đo sau khi nối (điền sau khi chạy thật)
- [ ] Cả 2 máy connected trong GUI
- [ ] Sync 1 job mẫu (`jobs/`) — máy 2 nhận đủ file, không conflict
- [ ] Sync 1 batch ảnh ~300 tấm (`results/`) — đo thời gian, so với Drive
- [ ] Sync `CHANEL/ep19-...` (943 MB) — đo thời gian + xác nhận máy 2 có file đủ
- [ ] Tắt máy 1 thử: máy 2 vẫn có file + upload được
- [ ] Quota Drive giảm hẳn sau khi bỏ dùng

## 7. Rủi ro / lưu ý
- **Không bao giờ đặt `results/` send-receive 2 chiều** → máy 1 sửa ảnh sẽ quay ngược máy 2, conflict.
- `shared/` 2 chiều: nếu 2 máy sửa cùng file cùng lúc → file `.sync-conflict-*` — đọc kỹ trước khi xoá.
- Syncthing lần đầu phải scan toàn bộ ổ (thư mục lớn) — mặc định `rescanIntervalS=3600` (1 giờ), có
  fsWatcher nên file mới thấy ngay; nếu muốn scan nhanh hơn giảm rescanIntervalS.
- Device ID công khai như username — không phải mật khẩu; an toàn trong LAN riêng.

## 8. QUY TRÌNH TRIỂN KHAI BẰNG SCRIPT (đã verify phần máy 1 — 2026-09-14)

Thư mục công cụ: `E:\CLAUDE\YOUTUBE\h2dev\tools\syncthing\` (máy 1). Copy CẢ thư mục `syncthing\`
sang máy 2 (USB hoặc qua mạng) giữ nguyên cấu trúc.

**Bước 1 — trên máy 2:** chạy `SETUP_MAY2.bat` (tự giải nén zip + sinh config + in device ID).
Gửi device ID máy 2 (63 ký tự) cho máy 1.

**Bước 2 — trên máy 1 (agent h2dev làm được):** với serve đang chạy, chạy:
```
py -3.13 CAU_HINH_MAY1.py <device-id-may2>
```
→ thêm device máy 2 + cập nhật 4 folder (jobs/results/shared/chanel) kèm máy 2 vào Sharing.

**Bước 3 — trên máy 2:** chạy:
```
py -3.13 CAU_HINH_MAY2.py <device-id-may1>
```
(device-id-may1 = `UIMW6PL-JJATL7Z-MBYH4TX-L7XAWAB-EWRKBBZ-MYXEX3B-BMCUZ4O-XG6NIQ5`;
tham số 2 tuỳ chọn = gốc thư mục, mặc định `E:\CLAUDE\YOUTUBE` → tạo `FlowHandoff_local/` +
`CHANEL/` trên máy 2).

**Bước 4 — bật serve cả 2 máy:**
- Máy 1: `START_SYNCTHING_MAY1.bat` (hoặc em chạy nền)
- Máy 2: `START_SYNCTHING.bat`
- Lần đầu Windows hỏi firewall → tick **Private networks** (hoặc chạy lệnh PowerShell mục 4d).

**Bước 5 — kiểm tra:** GUI `http://127.0.0.1:8384` mỗi máy thấy thiết bị kia xanh; đợi sync lần đầu
(CHANEL 8,7 GB — vài phút LAN). Điền kết quả vào checklist mục 6.

**Ghi chú cấu hình máy 1 hiện tại (đã ghi qua REST API):**
| Folder | Type | Path máy 1 |
|---|---|---|
| jobs | sendonly | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs` |
| results | receiveonly | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results` |
| shared | sendreceive | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared` |
| chanel | sendonly | `E:\CLAUDE\YOUTUBE\CHANEL` |