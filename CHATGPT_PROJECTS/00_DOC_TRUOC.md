# Bộ file tạo ChatGPT Project theo lane (1 lane = 1 Project)

Xuất ngày 2026-09-26. Kiến trúc 3 tầng:

```
GLOBAL   INSTRUCTIONS.txt trong từng thư mục   → dán vào ô "Instructions" của Project (luật chung, đã điền sẵn tên kênh)
PROJECT  file 00→08 (+ 09, 10 ở lane có kho video gốc) → kéo vào "Files/Sources" của Project
EPISODE  kịch bản + facts + ứng viên tiêu đề/thumb → dán trong từng tin nhắn (ưu tiên cao nhất)
```

## Cách tạo 1 Project (làm lần lượt cho từng thư mục)

1. ChatGPT → Projects → **Create project** → tên = nội dung file `_TEN_PROJECT.txt` (hoặc tên thư mục).
2. Chọn **Project-only memory** (KHÔNG dùng Default memory — bộ nhớ tài khoản đang lẫn nhiều thứ không liên quan).
3. Mở Project settings → **Instructions** → dán toàn bộ `INSTRUCTIONS.txt`.
4. **Add files** → kéo TẤT CẢ file `.md` đánh số trong thư mục (`00_…` → `08_…`, lane E/F/G/K/L/Satori có thêm `09_VIDEO_GOC.md` + `10_KENH_GOC_TAI_SAO.md`).
5. Thử: hỏi "Tóm tắt kênh này và 1 luật fact quan trọng nhất" → phải trả đúng tên kênh + luật của file 05.

## Cập nhật 2026-09-26 (Claude bên YT-TITLE-RESEARCH bổ sung — bỏ qua lane A, D)

| Thêm gì | Lane | Vì sao |
|---|---|---|
| `09_VIDEO_GOC.md` (bảng tập ↔ video gốc + bảng THẮNG/THUA kênh gốc + cách dùng) và `10_KENH_GOC_TAI_SAO.md` (toàn văn hồ sơ TẠI SAO mọi video kênh gốc: khuôn T6, chữ thumb C1–C5, hình H5, được/không được chép K2/K3, vì sao thắng/thua, tags + mô tả gốc) | E F G K L Satori | quy trình 25/09 "mỗi tập theo đúng 1 video gốc" — bản xuất cũ không có |
| `04_DESCRIPTION_RULES.md` thêm cấu trúc file đăng BẮT BUỘC có khối Timestamps + luật Tags (chép tags video gốc, thiếu thì đủ 15–20) | tất cả 9 lane | luật 25/09; G/H/I/J bản cũ còn ghi "bỏ Timestamps" |
| `08_CURRENT_LESSONS.md` có bài học thật (trước RỖNG ở E F G K L) | E F G K L Satori H I J | E: thumbnail đủ món + chữ thẳng · K: luật thumbnail tự động cũ SAI · L: nhãn không che mặt · F: ví dụ tránh nguyên nhân thua · G: Timestamps không được bỏ |
| `INSTRUCTIONS.txt` thêm: chữ số, chữ không che mặt, quy tắc video gốc, Timestamps, tags | tất cả 9 lane | — **phải dán lại vào ô Instructions** |
| K: dòng "Thumbnail kênh mẫu" ở 00/03 thay bằng mô tả đúng (2 nhân vật đối mặt, bong bóng xanh/đỏ, dải vàng giữa) | K | dữ liệu đo tự động cũ ghi "không có người" |
| Satori: 01/04 bổ sung khán giả + khuôn mô tả (trước gần rỗng) | Satori | |

Bản trước khi sửa: `_bak_20260926\`. Project đã tạo trên ChatGPT: dán lại INSTRUCTIONS + xoá file cũ rồi kéo file mới (08 và 04 đã đổi ở mọi lane).

## Danh sách thư mục

| Thư mục | Lane | Nguồn |
|---|---|---|
| `A-shinya_shiryoshitsu` | toshi-densetsu-jp (都市伝説 · bí ẩn) | xuất từ YT-TITLE-RESEARCH |
| `D-irogatatarukioku` | irogatatarukioku (ảnh WW2 tô màu) | xuất từ YT-TITLE-RESEARCH |
| `E-70dai-kenko` | kenko-chiebukuro (sức khoẻ người già) | xuất từ YT-TITLE-RESEARCH |
| `F-teinengo-real` | teinengo-real (hưu trí · manga tiền) | xuất từ YT-TITLE-RESEARCH |
| `G-teinengo-tanoshimi` | teinengo-tanoshimi (hưu trí · list vui/rẻ) | xuất từ YT-TITLE-RESEARCH |
| `K-yakkyoku-sukatto` | yakkyoku-sukatto (dược sĩ quả báo) | xuất từ YT-TITLE-RESEARCH |
| `L-shakai-no-naze` | shakai_no_naze (xã hội · số liệu) | xuất từ YT-TITLE-RESEARCH |
| `Satori-Lopezzapa68` | satori-jp-obaa (truyện người già 悟り) | xuất từ YT-TITLE-RESEARCH |
| `H-kokoro-kazoku` | kokoro-kazoku (tâm lý gia đình) | **BẢN NHÁP** — lane chưa có tập, rút từ DNA kênh mẫu |
| `I-sengoku-uragawa` | sengoku-uragawa (lịch sử Chiến quốc) | **BẢN NHÁP** — như trên |
| `J-teinengo-fuufu` | teinengo-fuufu (vợ chồng sau hưu trí) | **BẢN NHÁP** — như trên |
| `M-teinengo-anaba` | teinengo-anaba (việc làm tuổi 60) | **DỰNG TAY 2026-09-26** — lane chưa có trong bộ sinh của YT-TITLE-RESEARCH (`config\lanes\` không có `teinengo-anaba.json`), nên rút tay từ DNA kênh mẫu `otonanomouten` + `profiles\profiles\teinengo-anaba.json` + `docs\SOP_LANE_M.md`. Có đủ 00→10. Khi YT-TITLE thêm lane M thì xuất lại và thay cả thư mục. |
| `O-kaigo-sukatto-script` | kaigo-sukatto (介護スカッと, tên tạm Lane-O) | **DỰNG TAY 2026-10-03** — Project SOÁT KỊCH BẢN (khuôn J/N `-script`: INSTRUCTIONS + 00_KENH, 01_CAU_TRUC_VA_LUAT, 02_BINH_LUAN_THAT, 03_VIDEO_GOC). Rút từ `profiles\profiles\kaigo-sukatto.json` + `docs\SOP_LANE_O.md` + `docs\channel_dna\kaigo-sukatto\COMMENT_INSIGHT.md` + `docs\channel_dna\yakkyoku-sukatto\KENH_GOC_10\`. Tên Project = `Lane-O` (trùng thì `Lane-O-script`). |

## Lưu ý

- **Nguồn chuẩn là repo, không phải ChatGPT.** 8 thư mục đầu được dựng bằng hàm `build()` của
  `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\chatgpt_project.py` (chỉ đọc, không ghi gì vào dự án đó).
  Sửa luật trực tiếp trong ChatGPT thì lần xuất sau sẽ lệch → muốn thêm bài học, ghi vào repo rồi xuất lại
  và thay file `08_CURRENT_LESSONS.md` trong Project.
- Xuất lại bản mới (khi luật lane đổi): chạy lại lệnh trong mục "Xuất lại" dưới đây, rồi thay file trong Project.
- Không nhét kịch bản cũ vào Project — mỗi tập mới dán kịch bản + facts trong tin nhắn.

## Xuất lại (đè thư mục này) — lệnh dưới xuất CẢ 8 lane kể cả A/D; muốn bỏ A/D thì lọc danh sách `cp.lanes()`

```
cd /d E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src
py -3.13 -X utf8 -c "import chatgpt_project as cp;from pathlib import Path;O=Path(r'E:\CLAUDE\YOUTUBE\h2dev\CHATGPT_PROJECTS');exec('for l in cp.lanes():\n n,i,f,h=cp.build(l);t=n.split(\' · \')[0];t=\'D-\'+t if t==\'irogatatarukioku\' else t;d=O/t;d.mkdir(exist_ok=True)\n [(d/k).write_text(v,encoding=\'utf-8\') for k,v in f.items()];(d/\'INSTRUCTIONS.txt\').write_text(i,encoding=\'utf-8\');(d/\'_TEN_PROJECT.txt\').write_text(n,encoding=\'utf-8\');print(l,t)')"
```
