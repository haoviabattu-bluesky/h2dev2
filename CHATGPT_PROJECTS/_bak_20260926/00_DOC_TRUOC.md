# Bộ file tạo ChatGPT Project theo lane (1 lane = 1 Project)

Xuất ngày 2026-09-26. Kiến trúc 3 tầng:

```
GLOBAL   INSTRUCTIONS.txt trong từng thư mục   → dán vào ô "Instructions" của Project (luật chung, đã điền sẵn tên kênh)
PROJECT  9 file 00→08                           → kéo vào "Files/Sources" của Project
EPISODE  kịch bản + facts + ứng viên tiêu đề/thumb → dán trong từng tin nhắn (ưu tiên cao nhất)
```

## Cách tạo 1 Project (làm lần lượt cho từng thư mục)

1. ChatGPT → Projects → **Create project** → tên = nội dung file `_TEN_PROJECT.txt` (hoặc tên thư mục).
2. Chọn **Project-only memory** (KHÔNG dùng Default memory — bộ nhớ tài khoản đang lẫn nhiều thứ không liên quan).
3. Mở Project settings → **Instructions** → dán toàn bộ `INSTRUCTIONS.txt`.
4. **Add files** → kéo đủ 9 file `00_…` → `08_…`.
5. Thử: hỏi "Tóm tắt kênh này và 1 luật fact quan trọng nhất" → phải trả đúng tên kênh + luật của file 05.

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

## Lưu ý

- **Nguồn chuẩn là repo, không phải ChatGPT.** 8 thư mục đầu được dựng bằng hàm `build()` của
  `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\chatgpt_project.py` (chỉ đọc, không ghi gì vào dự án đó).
  Sửa luật trực tiếp trong ChatGPT thì lần xuất sau sẽ lệch → muốn thêm bài học, ghi vào repo rồi xuất lại
  và thay file `08_CURRENT_LESSONS.md` trong Project.
- Xuất lại bản mới (khi luật lane đổi): chạy lại lệnh trong mục "Xuất lại" dưới đây, rồi thay file trong Project.
- Không nhét kịch bản cũ vào Project — mỗi tập mới dán kịch bản + facts trong tin nhắn.

## Xuất lại 8 lane (đè thư mục này)

```
cd /d E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src
py -3.13 -X utf8 -c "import chatgpt_project as cp;from pathlib import Path;O=Path(r'E:\CLAUDE\YOUTUBE\h2dev\CHATGPT_PROJECTS');exec('for l in cp.lanes():\n n,i,f,h=cp.build(l);t=n.split(\' · \')[0];t=\'D-\'+t if t==\'irogatatarukioku\' else t;d=O/t;d.mkdir(exist_ok=True)\n [(d/k).write_text(v,encoding=\'utf-8\') for k,v in f.items()];(d/\'INSTRUCTIONS.txt\').write_text(i,encoding=\'utf-8\');(d/\'_TEN_PROJECT.txt\').write_text(n,encoding=\'utf-8\');print(l,t)')"
```
