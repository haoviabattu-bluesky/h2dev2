"""brain_steps.py — BỘ NÃO: gọi `claude` CLI (headless) làm khâu SÁNG TẠO cho 1 video.

Khác tool full-ramcloud (tab a3): tool NÀY dùng CLAUDE làm bộ não. Trên máy CÓ Claude Code, exe gọi
`claude -p "<đề bài>"` ngay trong thư mục dự án (có sẵn CLAUDE.md + skills + docs/SOP) để Claude:
  · đọc competitor.txt (transcript đối thủ) + skill youtube-script/youtube-image-prompts
  · viết script.txt (kịch bản 70/30 bản địa hoá) · characters.json (bible + toán tuổi) ·
    img_prompts.txt (storyboard từ SRT, marker @REF/@REF2/@GROK) · thumb_text.txt
  · TỰ chạy QC (qc_script.py = Gemini) + gen master (gpti2) + QC master, tự sửa tới khi đạt
Sau đó `render_engine.py` lo phần cơ học (giọng ElevenLabs · ảnh gpt-image-2 · ghép ffmpeg · QC Gemini).

Claude ở đây là AI VIẾT — ảnh/giọng/ghép/QC vẫn do gpt-image-2 / ElevenLabs / ffmpeg / Gemini.

Dùng (CLI test):
  py -3.13 brain_steps.py --slug <đường dẫn slug> --profile satori-jp-obaa --minutes 30
Import (GUI/orchestrator): from brain_steps import run_creative
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_std()

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent          # nơi có CLAUDE.md + skills + docs/SOP (Claude auto-discover)


def find_claude():
    """Tìm `claude` CLI. Máy client có thể cài qua npm (…/npm/claude[.cmd])."""
    import shutil
    for name in ("claude", "claude.cmd", "claude.exe"):
        p = shutil.which(name)
        if p:
            return p
    for c in (Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd",
              Path.home() / "AppData" / "Roaming" / "npm" / "claude.cmd"):
        if c.exists():
            return str(c)
    return ""


def creative_prompt(slug_dir, profile_id, minutes, competitor_name="competitor.txt", phase="all"):
    """Đề bài cho Claude — bám docs/SOP_SATORI_JP.md, dừng TRƯỚC khi tiêu tiền ảnh/giọng loạt lớn.

    phase: "all" (như cũ — brain_toshi.py + CLI cũ) · "script" (chỉ B3 + 70/30 + cổng số + B3Q) ·
    "assets" (chỉ characters/img_prompts/img_doan/thumb/TIEU_DE_MO_TA trên script ĐÃ CHỐT, cấm sửa script)."""
    S = Path(slug_dir)
    voice_note = ""
    vj = S / "voice.json"
    if vj.exists():
        try:
            d = json.loads(vj.read_text(encoding="utf-8"))
            voice_note = (f"\n- Giọng người kể của video này ĐÃ được phân tích sẵn: "
                          f"{d.get('gender','?')}·{d.get('age_band','?')} ({d.get('tone','')}). "
                          f"characters.json phải khớp giới tính này.")
        except Exception:
            pass
    # Số chữ MỤC TIÊU theo char_rate của profile → bảo Claude viết ĐÚNG độ dài NGAY, khỏi viết dài
    # gấp rưỡi rồi cắt tay chục lần (đo thật: cắt lặp làm cạn ngân sách trước khi xong các file).
    target, art_style, gate_note, prof_path = 0, "", "", ""
    palette = ("WHITE", "YELLOW", "RED")
    try:
        import profiles
        prof = profiles.load(profile_id)
        # ĐƯỜNG DẪN THẬT của profile, không phải đường đoán: bản cũ ghi cứng "pipeline/profiles/…"
        # trong khi thư mục đó KHÔNG TỒN TẠI (file nằm ở profiles/profiles/). Đo thật 2026-09-10:
        # mỗi lượt chạy tốn 1 lần Read trượt + 3 lần Glob dò (~1-2 phút) chỉ để tìm lại file này.
        try:
            f = profiles._find(profile_id)
            prof_path = str(f) if f else ""
        except Exception:
            prof_path = ""
        target = int(profiles.target_chars(prof, minutes))
        art_style = (prof.get("thumbnail", {}) or {}).get("art_style", "")
        palette = tuple((prof.get("thumbnail", {}) or {}).get("palette") or palette)
        g = profiles.gate(prof)
        br = g.get("chars_per_breath") or [0, 0]
        gate_note = (
            f"\n- ⛔ CỔNG SỐ HỌC (chặn cứng, đo bằng máy — KHÔNG đoán bằng mắt): độ dài {target:,} chữ "
            f"±12% · {g['comma_per_sentence'][0]}-{g['comma_per_sentence'][1]} dấu phẩy/câu · "
            f"{br[0]}-{br[1]} chữ/nhịp thở · hội thoại ≤{g['dialogue_ratio_max']:.0%} tổng số chữ."
            f"\n  ĐO BẰNG LỆNH NÀY (chạy tức thì, KHÔNG tốn tiền, chạy bao nhiêu lần cũng được):"
            f"\n     py -3.13 \"{Path(__file__).with_name('gate_check.py')}\" --profile {profile_id} "
            f"--script {S / 'script.txt'} "
            f"--minutes {minutes}"
            f"\n  BẮT BUỘC chạy tới khi in `CỔNG SỐ HỌC: ĐẠT` rồi mới được sang bước 2. Chạy NÓ TRƯỚC "
            f"qc_script.py (rẻ hơn, sửa hình thức trước rồi mới soi nội dung)."
            f"\n  ĐÓ LÀ TOÀN BỘ cổng chặn — đừng đọc source `ai_steps.py`/`profiles.py` để dò thêm luật. "
            f"(`require_next_ep_teaser` trong profile KHÔNG phải cổng chặn, chỉ là yêu cầu văn: kết bài "
            f"gợi mở tập sau.) Các ngưỡng ngách khác (đảo chiều/mốc sự thật/lá chắn) chỉ áp cho kênh tài "
            f"liệu, kênh này KHÔNG khai nên KHÔNG kiểm."
            f"\n  Mẹo đúng hướng: thiếu phẩy/câu dài hơi = câu văn quá dài liền mạch → chẻ câu, thêm "
            f"nhịp ngắt (、) như lời cụ già kể chậm. Hội thoại vượt trần = bớt đoạn đối thoại trực tiếp, "
            f"chuyển thành lời kể gián tiếp của người dẫn.")
    except Exception:
        target = int(minutes * 300)
    # Trạng thái file → resume: đã có file nào hợp lệ thì GIỮ, chỉ làm file còn thiếu (đỡ tốn budget).
    have = [f for f in ("script.txt", "characters.json", "img_prompts.txt", "thumb_text.txt",
                        "thumb_bg_prompt.txt", "TIEU_DE_MO_TA.txt")
            if (S / f).exists() and (S / f).stat().st_size > 50]
    resume_note = (f"\n- ĐÃ CÓ SẴN (GIỮ NGUYÊN nếu hợp lệ, đừng viết lại từ đầu): {', '.join(have)}. "
                   "Chỉ làm file CÒN THIẾU." if have else "")
    ci = S / "comment_insight.json"
    comment_note = ""
    if ci.exists():
        comment_note = (f"\n- Đã có `comment_insight.json` (điểm chạm cảm xúc + thiếu sót rút từ bình "
                        f"luận thật dưới video gốc) — đọc file này TRƯỚC khi viết B3, dùng để nhấn đúng "
                        f"cảm xúc khán giả kênh này quan tâm nhất, và để gợi ý cho phần 30% sáng tạo thêm.")
    thumb_bg_note = (
        f"  4) THUMBNAIL NỀN RIÊNG: kênh này có `thumbnail.art_style` = \"{art_style}\". Viết thêm "
        f"`thumb_bg_prompt.txt` = ĐÚNG 1 DÒNG prompt tiếng Anh sinh ẢNH NỀN RIÊNG cho thumbnail (KHÁC "
        f"ảnh thân video), BẮT ĐẦU BẰNG marker `@REF ` (có dấu cách sau REF) — THIẾU marker này thì "
        f"máy sẽ KHÔNG khoá mặt theo master, ảnh ra có thể là người lạ, hỏng cả thumbnail.\n"
        f"     ⚠️ BỐ CỤC BẮT BUỘC (đo thật 2026-09-14: 3/3 tập đầu viết \"positioned in the right "
        f"half\" vẫn KHÔNG đủ ép — tóc/trán vẫn lấn vào vùng chữ, phải sửa lại cả 3): PHẢI dùng đúng "
        f"cụm 'her entire face and body positioned tightly in the RIGHT THIRD of the frame only ... "
        f"the LEFT TWO-THIRDS of the frame is completely empty out-of-focus background with "
        f"absolutely no part of her hair body or hands visible there' — nói 'nửa khung' là KHÔNG ĐỦ, "
        f"phải nói rõ MỘT PHẦN BA + 'hoàn toàn không có bộ phận nào của người xuất hiện' ở phần kia.\n"
        f"     Nội dung: nhân vật chính theo character_sheet CỦA CHÍNH TẬP NÀY, đang cầm/gần MỘT vật "
        f"thể gắn với nút thắt của tập (sổ tiết kiệm, lá thư, tấm ảnh cũ... chọn đúng cái khớp cốt "
        f"truyện tập này, đừng dùng chung một vật cho mọi tập), biểu cảm khớp đỉnh điểm cảm xúc của "
        f"tập (sốc, đau buồn lặng lẽ, cảnh báo nghiêm khắc... tự chọn theo nội dung), theo đúng "
        f"art_style trên, kết thúc bằng '16:9, no text'. Ví dụ đúng khuôn: '@REF cinematic portrait "
        f"photo of the elderly Japanese woman, her entire face and body positioned tightly in the "
        f"RIGHT THIRD of the frame only, holding an old bank passbook, stunned heartbroken "
        f"expression, the LEFT TWO-THIRDS of the frame is completely empty out-of-focus dark room "
        f"background with absolutely no part of her hair body or hands visible there, cinematic "
        f"ultra-realistic color, photorealistic, 16:9, no text'\n"
        f"     Sau khi máy sinh xong ảnh nền, MỞ ẢNH LÊN XEM mặt rơi vào bên nào rồi mới chọn "
        f"`thumbnail_text.py --side` khớp bên TRỐNG (gpti2 không theo đúng 100% chỉ dẫn trái/phải "
        f"trong prompt — đừng đoán trước, phải nhìn ảnh thật)."
        if art_style else "")
    # Tach 2 pha (P0 2026-09-18): pha "script" chi viet script.txt + qua cong so/B3Q; pha "assets"
    # viet characters/img_prompts/img_doan/thumb/TIEU_DE_MO_TA tren script DA CHOT. Truoc day viet
    # tat ca trong 1 luot roi vong B3Q sua script.txt SAU -> prompt/img_doan bam ban script cu
    # (bang chung STT3: img_prompts 18:36 < script 20:45, 3 anh mau thuan cot truyen).
    khoa_pha = {
        "script": ("  2) B5:", "  2b) B5", "  3) B7:", thumb_bg_note[:20] if thumb_bg_note else "\x00", "  4) TIÊU ĐỀ"),
        "assets": ("  1) B3:", "⚖️ 70/30", "LÀM ĐÚNG 4 BƯỚC", "   1. Liệt kê 10 nhịp", "   2. Chốt bằng chữ",
                   "   3. Với 7 nhịp", "   💴 CON SỐ TIỀN", "      → PHẢI DÙNG", "   🔎 TIỀN CHỈ", "   ⚠️ NẾU QC",
                   "   4. Mọi lời thoại", "Mục tiêu: ĐẠT B3Q"),
    }.get(phase, ())
    pha_note = {
        "script": "\n- PHA NÀY CHỈ LÀM `script.txt` (B3) tới khi ĐẠT gate_check.py + qc_script.py. KHÔNG viết "
                  "characters/img_prompts/img_doan/thumb/tiêu đề+mô tả đăng tải — pha sau làm. "
                  "KHÔNG tự chạy B3S (`qc_script_sol.py`) dù SOP có nhắc — orchestrator chạy B3S SAU lượt này "
                  "và sẽ gọi lại bạn kèm báo cáo sol nếu cần sửa (đo thật STT10: bộ não tự chạy B3S 2 vòng "
                  "trong lượt viết = 96 lượt tool, gấp 4 lần bình thường, rồi orchestrator vẫn chấm lại). "
                  "Xong in BRAIN_DONE.",
        "assets": "\n- `script.txt` ĐÃ ĐẠT mọi cổng. TUYỆT ĐỐI KHÔNG sửa script.txt lượt này (sửa là lệch "
                  "prompt/img_doan với script — đúng lỗi STT3). Nếu thấy script BUỘC phải sửa: in "
                  "BRAIN_BLOCKED <lý do> và dừng. Chỉ viết các file asset còn thiếu.",
    }.get(phase, "")
    parts = [
        "⚠️ CHẾ ĐỘ TỰ ĐỘNG (HEADLESS) — KHÔNG có người trả lời bạn. TUYỆT ĐỐI KHÔNG hỏi xác nhận, "
        "KHÔNG liệt kê phương án rồi chờ chốt, KHÔNG dừng giữa chừng xin ý kiến. Tự quyết MỌI lựa chọn "
        "và THỰC THI NGAY, chạy một mạch tới khi tạo xong các file. BỎ QUA mọi skill kiểu brainstorming/"
        "hỏi-đáp — vào việc luôn. Nếu phân vân, chọn phương án hợp SOP nhất rồi làm.",
        "",
        f"Bạn đang làm 1 video YouTube faceless. Thư mục làm việc của tập này: {S}",
        f"Profile giọng/kênh: {profile_id} ({prof_path or 'profiles/profiles/' + profile_id + '.json'}). "
        f"Mục tiêu độ dài: {minutes} phút.",
        "",
        f"Trong thư mục đã có `{competitor_name}` = transcript kịch bản đối thủ (nguồn).",
        "Hãy làm ĐÚNG các bước SÁNG TẠO trong docs/SOP_SATORI_JP.md, theo skill youtube-script + "
        "youtube-image-prompts, tuân thủ CLAUDE.md (công thức 70/30, bản địa hoá 100%, REF-LOCK, "
        "giới giọng khớp người kể):",
        f"  1) B3: viết `script.txt` (voiceover-ready, thuần prose) nhắm ĐÚNG ~{target} chữ (không dấu "
        f"cách) NGAY TỪ LƯỢT ĐẦU."
        f"\n     📐 CÔNG THỨC ĐẾM ĐƯỢC (bạn KHÔNG đếm nổi ký tự tiếng Nhật khi đang viết, nhưng đếm được "
        f"ĐOẠN và CÂU — nên bám cấu trúc, đừng bám cảm giác độ dài). Đo từ một kịch bản ĐÃ ĐẠT cổng:"
        f"\n        · **{max(target // 126, 10)} đoạn**, mỗi đoạn **4-5 câu** (~126 ký tự/đoạn)"
        f"\n        · mỗi câu **~26 ký tự**, ngắt **3 dấu 、** trong câu (đây chính là thứ tạo ra nhịp "
        f"thở đúng — cụ già kể chậm, ngắt nhiều)"
        f"\n        · ĐỪNG viết đoạn dài 400+ ký tự với 11 câu/đoạn: bản FAIL đo được đúng kiểu đó."
        f"\n     🛑 CHỐNG VIẾT LỐ — VIẾT LÀM 2 NHỊP, TUYỆT ĐỐI KHÔNG viết một mạch cả bài."
        f"\n        (Đo thật 2026-09-10 hai lượt liên tiếp: bảo \"viết {max(target // 126, 10)} đoạn\" thì "
        f"ra 104 đoạn / 16.014 chữ = GẤP ĐÔI; bảo \"viết 10 đoạn rồi dừng đo\" thì bỏ qua luôn. Lý do: "
        f"khi đang sinh chữ bạn KHÔNG tự theo dõi được số đoạn đã viết. Dàn ý ĐÁNH SỐ thì đếm được.)"
        f"\n        NHỊP 0 — TRA DỮ KIỆN THẾ GIỚI THẬT, LÀM TRƯỚC KHI VIẾT DÀN Ý."
        f"\n           Tách hai loại số, đừng gộp:"
        f"\n             · DỮ KIỆN THẾ GIỚI (giá, phí, mức trợ cấp, thời hạn thủ tục, tên cơ quan/giấy tờ, lịch chi trả) — CÓ THẬT ngoài đời ⇒ BẮT BUỘC TRA, cấm đoán."
        f"\n             · SỐ CỦA NHÂN VẬT (bà cụ để dành bao nhiêu, góp mấy lần) — hư cấu, không tra được ⇒ chỉ cần HỢP LÝ so với dữ kiện thế giới ở trên."
        f"\n           Làm đúng 3 việc:"
        f"\n             1. Liệt kê ra các DỮ KIỆN THẾ GIỚI mà kịch bản này sẽ đụng tới."
        f"\n             2. Tra từng cái: đọc bảng {PROJECT_ROOT / 'docs' / 'SO_LIEU_THAT_JP.md'} TRƯỚC; cái nào bảng chưa có thì "
        f"**WebSearch** lấy số thật."
        f"\n             3. Cái nào vừa tra được mà bảng chưa có thì THÊM MỘT DÒNG vào {PROJECT_ROOT / 'docs' / 'SO_LIEU_THAT_JP.md'} "
        f"kèm nguồn + ngày tra. Tập sau khỏi tra lại, và số liệu thống nhất giữa các tập."
        f"\n           ⚠️ ĐO THẬT 2026-09-12 (tập simbot2-07): bạn CÓ mở bảng nhưng **0 lần "
        f"WebSearch**, bảng KHÔNG dày thêm dòng nào — trong khi tập đó nói về phí tang lễ, thủ tục "
        f"thừa kế, tiền gửi ngân hàng, chẳng khoản nào có trong bảng. Nghĩa là các con số đó là "
        f"ĐOÁN CHO HỢP LÝ. Hết chia tỉ giá thì chuyển sang bịa — vẫn sai y như cũ."
        f"\n           Orchestrator nay ĐO việc này: xong lượt nó in ra bảng có dày thêm dòng nào "
        f"không. Kịch bản đụng hạng mục mới mà bảng đứng yên = bạn đã bỏ qua nhịp này."
        f"\n           Tra không ra thì VIẾT MỜ ĐI hoặc BỎ HẲN chi tiết đó — một chi tiết mơ hồ mà "
        f"đúng còn hơn một chi tiết cụ thể mà sai."
        f"\n        NHỊP 1 — viết `dan_y.txt`: ĐÚNG {max(target // 126, 10)} dòng, đánh số 1.."
        f"{max(target // 126, 10)}, mỗi dòng MỘT câu tóm tắt đoạn đó kể gì."
        f"\n           ✓ ĐẾM BẰNG MÁY, đừng đếm bằng mắt (đo thật: bảo 64 dòng, viết ra 140):"
        f"\n             grep -c . \"{S / 'dan_y.txt'}\""
        f"\n             Ra khác {max(target // 126, 10)} thì GỘP/TÁCH dòng cho đúng rồi đếm lại, "
        f"xong mới sang nhịp 2."
        f"\n        NHỊP 1.5 — TỰ KIỂM BÁM GỐC NGAY TRÊN DÀN Ý (rẻ, vài dòng — làm TRƯỚC khi viết hết "
        f"prose): đối chiếu 64 dòng `dan_y.txt` vừa viết với 10 nhịp sự kiện chính của bản gốc (bạn sẽ "
        f"liệt kê ở bước 1 của mục 70/30 phía dưới — làm bước đó NGAY BÂY GIỜ, trước khi viết script.txt, "
        f"không phải sau). ĐẾM BẰNG SỐ, không cảm tính: dàn ý vừa viết có ĐỦ ít nhất 2-3 nhịp gốc bị "
        f"BỎ HẲN (không xuất hiện dưới bất kỳ hình thức nào) và ít nhất 3-4 nhịp HOÀN TOÀN MỚI (không có "
        f"trong bản gốc, không phải chỉ đổi đạo cụ) hay không? THIẾU MỘT TRONG HAI ĐIỀU KIỆN TRÊN → sửa "
        f"lại `dan_y.txt` NGAY rồi đếm lại — đừng để viết hết ~{target:,} chữ prose rồi mới phát hiện "
        f"bám gốc quá cao (đo thật simbot2-03: viết hết prose ở mức bám gốc 100%, phải xé viết lại, tốn "
        f"hơn 100 phút — sửa 64 dòng dàn ý ngắn rẻ hơn rất nhiều so với sửa lại toàn bộ prose dài)."
        f"\n        NHỊP 2 — viết `script.txt` BÁM SÁT dàn ý: mỗi dòng dàn ý → ĐÚNG 1 đoạn ~126 ký tự "
        f"(4-5 câu). Cấm thêm đoạn ngoài dàn ý, cấm gộp 2 dòng dàn ý vào 1 đoạn, cấm bỏ dòng nào."
        f"\n        NHỊP 3 — GIAO VIỆC CẮT CHO MÁY, TUYỆT ĐỐI KHÔNG TỰ VIẾT LẠI ĐỂ CHỈNH SỐ:"
        f"\n             py -3.13 \"{Path(__file__).with_name('fix_gate.py')}\" "
        f"--script {S / 'script.txt'} --profile {profile_id} --minutes {minutes}"
        f"\n           Lệnh này nén độ dài + thêm/bớt nhịp thở + hạ hội thoại bằng LLM rẻ chạy 3 luồng, "
        f"~1-5 phút, KHÔNG tốn ngân sách của bạn, và nó ghi đè `script.txt` luôn."
        f"\n           ⛔ ĐO THẬT 2026-09-10, đây là lỗi ĐẮT NHẤT của cả pipeline: một lượt tự viết lại "
        f"script 5 LẦN LIÊN TIẾP để ép độ dài = 26 PHÚT + cạn sạch ngân sách, tập FAIL vì không còn "
        f"tiền làm characters.json. Trong khi máy nắn xong trong 4,7 phút. VIỆC CỦA BẠN LÀ VIẾT VĂN "
        f"HAY, việc đếm ký tự là của máy — đừng tranh việc của máy."
        f"\n           Chạy xong mới `gate_check.py` xác nhận. Còn lệch thì chạy `fix_gate.py` LẦN NỮA, "
        f"vẫn KHÔNG tự viết lại."
        f"\n     Cổng số ĐẠT rồi mới chạy `qc_script.py` (B3Q) — cổng này soi NỘI DUNG (logic, văn hoá, "
        f"sao chép 70/30) nên phải TỰ TAY sửa, máy không làm hộ được. Sửa đúng chỗ bị nêu, đừng viết "
        f"lại cả bài (viết lại là lệch số, lại phải nắn lại từ đầu)."
        f"\n     ⚡ SỬA HÀNG LOẠT RỒI MỚI VERIFY LẠI 1 LẦN (đo thật simbot2-03: sửa-từng-câu-rồi-chạy-"
        f"gate_check.py-ngay lặp hàng chục vòng = tốn hơn 100 phút chỉ riêng việc sửa, trong khi mỗi "
        f"vòng chỉ sửa được 1-3 câu). Khi `qc_script.py`/gate liệt kê NHIỀU chỗ cần sửa: đọc HẾT danh "
        f"sách trước, sửa HẾT toàn bộ bằng nhiều lệnh Edit LIÊN TIẾP KHÔNG xen `gate_check.py`/"
        f"`qc_script.py` ở giữa, CHỈ chạy lại 2 lệnh đó SAU KHI đã sửa xong cả danh sách. Ngoại lệ duy "
        f"nhất: sửa xong mà không chắc có phá cổng số học không thì chạy `gate_check.py` (rẻ, tức "
        f"thì) — nhưng vẫn KHÔNG chạy `qc_script.py` (đắt, ~1 phút) sau mỗi câu."
        f"{gate_note}",
        "",
        "⚖️ 70/30 LÀ SỐ ĐO CÓ NGƯỠNG, KHÔNG PHẢI KHẨU HIỆU — cổng B3Q chấm bằng KHUNG SỰ KIỆN (không "
        "so câu chữ): `ty_le_bam_goc` (% nhịp gốc còn giữ) phải rơi vào 60-80%. >90% RỚT (bám sát quá) · "
        "<50% RỚT (lạc đề). Riêng câu dịch sát bản gốc = SAO_CHEP = HỎNG NẶNG, chỉ 1 câu cũng rớt.",
        "LÀM ĐÚNG 4 BƯỚC NÀY TRƯỚC KHI VIẾT PROSE (viết thẳng prose kiểu phóng tác trung thành = chắc "
        "chắn ra ~95% và mất 10+ lượt QC để gỡ):",
        "   1. Liệt kê 10 nhịp sự kiện chính của bản gốc (đánh số, mỗi nhịp 1 dòng).",
        "   2. Chốt bằng chữ: GIỮ 7 nhịp nào · BỎ HẲN 2-3 nhịp nào · THÊM MỚI 3-4 nhịp của riêng mình "
        "(lấy ý từ comment_insight nếu có). Giữ KHUNG CẢM XÚC + cú twist cuối; KHÔNG giữ nguyên tình tiết.",
        "   3. Với 7 nhịp GIỮ: đổi ĐẠO CỤ / BỐI CẢNH / CON SỐ / QUAN HỆ cụ thể (áo đỏ → vật khác, bể bơi "
        "→ chỗ khác…). Giữ CHỨC NĂNG của nhịp, thay VẬT LIỆU của nhịp.",
        "   💴 CON SỐ TIỀN — LỖI HỆ THỐNG, ĐỌC KỸ: TUYỆT ĐỐI KHÔNG quy đổi con số của bản gốc theo "
        "tỉ giá (chia 10, bỏ một số 0…). Đo thật 2026-09-11, một kịch bản dính 7 chỗ liền: 82만원 → "
        "「八万二千円」 · 3.000원 → 「三百円」 · 130만원 → 「十三万円」 · 3000만원 → 「三百万円」 · "
        "500만원 → 「五十万円」. Người bản xứ nhìn con số là biết ngay đây là bản dịch — đây là DẤU "
        "VÂN TAY của việc sao chép, nặng hơn cả dịch sát câu chữ.",
        f"      → PHẢI DÙNG DỮ LIỆU THẬT, không quy đổi mà cũng KHÔNG BỊA số 'cho hợp lý':"
        f"\n        (a) Tra bảng số liệu đã kiểm chứng của dự án TRƯỚC: "
        f"{PROJECT_ROOT / 'docs' / 'SO_LIEU_THAT_JP.md'}"
        f"\n        (b) Không có trong bảng (giá sổ tay, tiền điện, phí tang lễ, tiền thuê…) → dùng "
        f"**WebSearch** tra mức thật, lấy đúng con số đó, rồi THÊM MỘT DÒNG vào bảng kèm nguồn + ngày "
        f"tra để tập sau khỏi tra lại."
        f"\n        (c) Viết xong chạy: py -3.13 \"{Path(__file__).with_name('qc_tien.py')}\" "
        f"--script {S / 'script.txt'} --competitor {S / competitor_name}"
        f"\n        Lệnh này đối chiếu TẤT ĐỊNH từng số tiền với bản gốc (1 giây, 0 đồng) — trùng đúng "
        f"tỉ lệ 1:10 là CHẶN.",
        f"   🔎 TIỀN CHỈ LÀ MỘT LOẠI — MỌI CHI TIẾT ĐỜI THẬT ĐỀU PHẢI ĐÚNG SỰ THẬT (anh chốt 2026-09-11): "
        f"chuyện đời thường nên chi tiết sai hoặc mơ hồ là khán giả bản xứ nhận ra ngay, y như con số "
        f"quy đổi. Danh sách PHẢI TRA, cấm phỏng đoán:"
        f"\n        · Thủ tục hành chính — tên giấy tờ, cơ quan cấp, nộp ở đâu, mất bao lâu "
        f"(介護保険, 生活保護, 年金事務所, 地域包括支援センター, 成年後見, 死亡届…)"
        f"\n        · Y tế — tên bệnh/khoa/thuật ngữ BẢN XỨ, tỉ lệ tự trả theo tuổi, giấy tờ cuối đời "
        f"(事前指示書 chứ không phải bản dịch sát từ tiếng gốc)"
        f"\n        · Lịch & mốc thời gian — lương hưu Nhật trả 2 THÁNG MỘT LẦN, ngày 15 các tháng CHẴN "
        f"(không phải hằng tháng như bản gốc), năm học, mùa, ngày lễ, giờ tàu xe"
        f"\n        · Phong tục & nghi lễ — đám tang, giỗ, quà thăm bệnh, món ăn theo mùa/theo dịp "
        f"(bê nguyên phong tục bản gốc = lỗi DẤU_VẾT_HÀN)"
        f"\n        · Địa danh, phương tiện, giá cả, tên cửa hàng — có thật và hợp vùng miền"
        f"\n      CÁCH LÀM GIỐNG HỆT PHẦN TIỀN: (a) tra bảng dữ liệu dự án trước → (b) không có thì "
        f"**WebSearch** rồi GHI BỔ SUNG vào bảng kèm nguồn + ngày tra → (c) chi tiết nào KHÔNG tra được "
        f"thì VIẾT MỜ ĐI hoặc BỎ HẲN, TUYỆT ĐỐI không bịa cho 'nghe hợp lý'. Một chi tiết mơ hồ mà đúng "
        f"còn hơn một chi tiết cụ thể mà sai.",
        "   ⚠️ NẾU QC CỨ BÁO BÁM SÁT BẢN GỐC (SAO_CHEP / >90%) SAU 2 LƯỢT SỬA: đừng sửa câu chữ nữa, "
        "cũng ĐỪNG DỪNG LẠI BÁO CÁO — hãy BỎ HẲN 2-3 nhịp gốc và THÊM 3-4 nhịp tự nghĩ. Sửa chữ không "
        "bao giờ gỡ được lỗi này vì cổng chấm KHUNG SỰ KIỆN, không chấm câu chữ.",
        "   4. Mọi lời thoại tự đặt bằng tiếng Nhật của mình. CẤM dịch câu bản gốc rồi sửa vài chữ.",
        "Mục tiêu: ĐẠT B3Q trong 1-2 lượt. KHÔNG đọc source code qc_script.py để dò luật — luật đã ghi ở trên.",
        "  2) B5: viết `characters.json` — ⚠️ KHUÔN BẮT BUỘC, render_engine đọc ĐÚNG khoá này, sai "
        "khuôn là nó thấy 0 nhân vật rồi gen cả loạt ảnh KHÔNG khoá mặt mà không báo lỗi gì:\n"
        "     {\"video\": \"<slug>\", \"world\": \"<bối cảnh chung>\",\n"
        "      \"characters\": [ {\"name\":\"Chiyo\", \"age\":73, \"gender\":\"F\",\n"
        "                        \"master\":\"_ref/001.png\", \"look\":\"<mô tả ngoại hình tiếng Anh>\"},\n"
        "                       {\"name\":\"Fusako\",\"age\":73,\"gender\":\"F\",\n"
        "                        \"master\":\"_ref_fusako/001.png\",\"look\":\"…\"} ],\n"
        "      \"supporting\": […], \"relationships\": […], \"notes\": \"toán tuổi…\" }\n"
        "     `characters` PHẢI là MẢNG (không phải các khoá REF/REF2/SIDE_x rời), mỗi nhân vật có "
        "`master` trỏ file ảnh THẬT bạn sẽ gen. Nhân vật nào có `@REF`/`@REF2` trong img_prompts.txt "
        "thì BẮT BUỘC có mặt trong mảng này kèm ảnh master đã gen xong.\n"
        "     → gen + QC master (gpti2 + qc_character/"
        "qc_visual master), tự sửa tới đạt tuổi/giới/trang phục/thời đại → viết `img_prompts.txt` "
        "\n     ⚡ CHẠY SONG SONG (tiết kiệm ~6 phút mỗi tập, đo thật 2026-09-10): lệnh gen ảnh master "
        "mất ~1 phút và QC master mất ~2 phút, trong khi bạn CÓ THỂ vừa chờ vừa viết. Nên: viết xong "
        "`characters.json` + `master.txt` thì BẮN LỆNH GEN MASTER Ở NỀN (Bash với run_in_background), "
        "rồi VIẾT NGAY `img_prompts.txt` trong lúc ảnh đang sinh. Viết xong mới quay lại kiểm QC master "
        "và sửa nếu trượt. ĐỪNG ngồi không chờ ảnh xong rồi mới viết — đó là xếp hàng vô ích."
        "(storyboard theo độ dài script, mỗi ~15s/ảnh, marker @REF/@REF2/@GROK). "
        "voice.srt CHƯA có ở bước này là BÌNH THƯỜNG — cứ rải đều theo mạch kịch bản.",
        "  2b) B5 — CÙNG LÚC viết `img_doan.txt`: MỖI ẢNH MỘT DÒNG `<tên ảnh>|<số đoạn>`, ví dụ\n"
        "     001.png|1  ·  002.png|1  ·  003.png|2 …\n"
        "     `<số đoạn>` = ảnh đó minh hoạ cho ĐOẠN THỨ MẤY của `script.txt` (đoạn = khối chữ cách\n"
        "     nhau bằng dòng trống), đếm từ 1. Nhiều ảnh chung một đoạn là bình thường (~2 ảnh/đoạn).\n"
        "     Số đoạn phải KHÔNG GIẢM theo thứ tự ảnh — ảnh sau không được lùi về đoạn trước.\n"
        "     ⚠️ VÌ SAO BẮT BUỘC: không có file này thì khâu ghép chia ảnh theo SỐ ĐẾM, ảnh TRÔI dần\n"
        "     so với lời và nặng dần về cuối video (đo thật tập simbot2-04: khớp hình–lời chỉ 3,1/5,\n"
        "     3 trong 5 mốc lệch nằm sau phút 26 của video 32 phút). BẠN đang giữ mối nối ảnh↔đoạn\n"
        "     trong đầu lúc viết prompt — chỉ cần ghi con số ra, MÁY tự cắt chuỗi neo chính xác.\n"
        "     CHỈ ghi số, TUYỆT ĐỐI đừng chép trích đoạn — chép sai một ký tự là hỏng cả lượt ghép.",
        "  3) B7: viết `thumb_text.txt` — MỖI DÒNG ĐÚNG KHUÔN `MÀU|chữ` (bắt buộc có dấu `|`, thiếu "
        "dấu này thì máy ghép ảnh BỎ QUA cả dòng, thumbnail ra 0 chữ mà không báo lỗi gì). MÀU là một "
        f"trong {palette} (khớp `thumbnail.palette` của kênh). Dòng cuối bắt đầu `BANNER|` là câu phụ đề dưới cùng — "
        "PHẢI NGẮN (tối đa ~15 ký tự tiếng Nhật), dài hơn sẽ tràn khung. Ví dụ đúng:\n"
        "        WHITE|母さん\n        WHITE|その金は\n        RED|僕でも\n        RED|下ろせない\n"
        "        BANNER|夫が遺した三行の遺言",
        thumb_bg_note,
        "  4) TIÊU ĐỀ + MÔ TẢ ĐĂNG TẢI: viết `TIEU_DE_MO_TA.txt` — ĐÂY LÀ VIỆC CỦA BẠN, KHÔNG PHẢI "
        "việc của bước 2/3 (máy vẽ ảnh + máy ghép video KHÔNG hiểu nội dung, không viết được tiêu đề "
        "hay mô tả tử tế — đã dính thật: 2 tập giao qua nhánh ghép riêng bị lọt tới tay người xem với "
        "tiêu đề trống/mô tả kỹ thuật rỗng vì bước 3 không tự sinh nội dung, chỉ cơ học). Khuôn CỐ ĐỊNH:\n"
        "     Dòng 1: tiêu đề (câu trích/hook mạnh nhất trong script + số liệu/twist cụ thể, không sáo rỗng)\n"
        "     Dòng trống, rồi 1 dòng 5 từ khoá cách nhau dấu phẩy KHÔNG cách\n"
        "     Dòng trống, rồi 3-4 đoạn mô tả (viết bằng giọng nhân vật kể chuyện, kể lại đúng mạch "
        "truyện — không phải tóm tắt khô khan, không bịa chi tiết không có trong script)\n"
        "     Dòng gạch ngang, rồi `Timestamps:`, dòng trống, rồi ĐÚNG 8 dòng mốc chương. VÌ CHƯA CÓ "
        "AUDIO (voice_paced.srt) ở bước này nên KHÔNG được bịa số phút:giây — thay vào đó viết "
        "`[CHƯA CÓ — cần trích từ voice_paced.srt thật sau khi bước 3 chạy TTS, bám đúng câu mở đầu "
        "8 đoạn dưới đây theo thứ tự xuất hiện, KHÔNG chia đều/đoán]` rồi liệt kê 8 câu mở đầu of 8 "
        "đoạn script.txt bạn chọn làm mốc chương (câu chép NGUYÊN VĂN từ script, không diễn giải).\n"
        "     Dòng gạch ngang, 1 câu cảm ơn ngắn, dòng gạch ngang, rồi 1 dòng 6-7 hashtag.\n"
        "     File này CHÉP NGUYÊN VĂN sang `listting.txt` khi giao hàng (bước 3 chỉ tìm-thay mốc "
        "chương thật vào chỗ `[CHƯA CÓ...]`, KHÔNG được viết lại tiêu đề/mô tả/hashtag).",
        voice_note,
        comment_note,
        resume_note,
        "",
        "⏱ ĐỪNG PHÍ THỜI GIAN (đo thật 2026-09-10, mất 2,2 phút vô ích trong 1 lượt): TUYỆT ĐỐI KHÔNG "
        "`sleep`/chờ vu vơ — mọi lệnh ở đây đều chạy ĐỒNG BỘ, lệnh trả về là đã xong. Không đi đọc file "
        "log tạm của phiên khác. Không đọc source `ai_steps.py`/`profiles.py`/`qc_*.py` để dò luật.",
        "",
        "QUAN TRỌNG — DỪNG ĐÚNG RANH GIỚI:",
        "- CHỈ làm phần CHỮ + gen/QC MASTER. TUYỆT ĐỐI KHÔNG chạy gen loạt ảnh đầy đủ, KHÔNG chạy "
        "tts.py, KHÔNG assemble — phần cơ học đó do render_engine.py lo sau (đỡ tốn tiền + tránh trùng).",
        "- Khi xong, in đúng một dòng: BRAIN_DONE <slug> rồi kết thúc.",
        "- Nếu thiếu dữ kiện không thể tiếp, in: BRAIN_BLOCKED <lý do ngắn>.",
    ]
    if khoa_pha:
        parts = [s for s in parts if not any(str(s).startswith(k) for k in khoa_pha)]
    # Lane khai `assets.skip` (vd satori 2026-09-19: tiêu đề/mô tả + thumbnail do dự án khác lo) thì
    # BỎ HẲN khối việc đó khỏi đề bài — nếu chỉ bỏ khỏi danh sách kiểm file mà vẫn để trong prompt,
    # bộ não vẫn ngồi viết (tốn quota) rồi ghi ra file thừa.
    try:
        import profiles as _pf
        _skip = set((_pf.load(profile_id).get("assets") or {}).get("skip") or [])
    except Exception:
        _skip = set()
    khoa_skip = []
    if "thumb_text.txt" in _skip:
        khoa_skip += ["  3) B7:", (thumb_bg_note[:20] if thumb_bg_note else "\x00")]
    if "TIEU_DE_MO_TA.txt" in _skip:
        khoa_skip.append("  4) TIÊU ĐỀ")
    if khoa_skip:
        parts = [s for s in parts if not any(str(s).startswith(k) for k in khoa_skip)]
        if phase in ("assets", "all"):   # pha script vốn đã khoá các khối này, nhắc lại là thừa
            parts.append("\n- LANE NÀY KHÔNG LÀM: " + ", ".join(sorted(_skip)) +
                         " — dự án khác đảm nhận. Đừng viết các file đó, đừng nhắc tới chúng trong báo cáo.")
    if pha_note:
        parts.insert(parts.index("") if "" in parts else 0, pha_note)
    return "\n".join(parts)


# File BẮT BUỘC phải tồn tại sau mỗi pha (kiểm tầng hai — không tin exit code / BRAIN_DONE tự khai).
NEED_BY_PHASE = {
    "script": ["script.txt"],
    "assets": ["characters.json", "img_prompts.txt", "img_doan.txt", "thumb_text.txt", "TIEU_DE_MO_TA.txt"],
    "all": ["script.txt", "characters.json", "img_prompts.txt", "thumb_text.txt", "TIEU_DE_MO_TA.txt"],
}


def run_creative(slug_dir, profile_id="satori-jp-obaa", minutes=30, on_line=None,
                 permission_mode="acceptEdits", budget_usd=0.0, timeout=2400,
                 competitor_name="competitor.txt", extra_prompt="", phase="all"):
    """Gọi `claude -p` headless viết phần sáng tạo cho slug. Trả (ok, dòng_cuối).

    on_line(str): callback nhận từng dòng tiến trình (GUI in ra). permission_mode: 'acceptEdits'
    (tự nhận sửa file, Bash vẫn hỏi → dùng khi có allowlist) hoặc 'bypassPermissions' (tự chủ hẳn —
    cần vì Claude phải chạy qc/gpti2). budget_usd>0 = trần chi phí. Cần máy đã đăng nhập Claude Code."""
    claude = find_claude()
    if not claude:
        msg = "✗ Không tìm thấy `claude` CLI trên máy này — tool NÃO=Claude cần Claude Code đã cài + đăng nhập."
        (on_line or print)(msg)
        return False, msg
    prompt = creative_prompt(slug_dir, profile_id, minutes, competitor_name, phase=phase)
    if extra_prompt:
        prompt += "\n\n" + extra_prompt
    # append-system-prompt: chặn tận gốc thói quen hỏi-lại của Claude khi chạy không người giám sát.
    autonomy = ("Bạn đang chạy KHÔNG người giám sát (headless -p). Không bao giờ hỏi câu hỏi làm rõ, "
                "không chờ xác nhận, không đề xuất phương án rồi dừng. Tự quyết và thực thi liền mạch "
                "tới khi hoàn thành nhiệm vụ được giao.")
    # ĐỀ BÀI đưa qua STDIN, KHÔNG qua argv: truyền prompt dài làm positional sau `-p` không ổn định
    # (đo thật: Claude báo "không có yêu cầu trong turn này" = prompt không tới). `echo prompt | claude -p`
    # là cách headless chuẩn, né luôn giới hạn độ dài/encoding của dòng lệnh.
    # GHIM MODEL: không ghim thì bộ não chạy bằng model MẶC ĐỊNH của CLI (đổi theo phiên bản/máy), và
    # `/model` người dùng chọn trong phiên chat cha KHÔNG truyền xuống tiến trình con này.
    cmd = [claude, "-p", "--permission-mode", permission_mode,
           "--model", os.environ.get("BRAIN_MODEL", "opus"),
           "--append-system-prompt", autonomy,
           "--add-dir", str(PROJECT_ROOT), "--output-format", "stream-json", "--verbose"]
    if budget_usd and budget_usd > 0:
        cmd += ["--max-budget-usd", str(budget_usd)]
    emit = on_line or (lambda s: print(s, flush=True))
    emit(f"🧠 Claude (bộ não) bắt đầu viết — {Path(slug_dir).name} · profile {profile_id} · {minutes}'")
    try:
        # KHÔNG CREATE_NO_WINDOW: nếu có cha là GUI (console ẩn) hay terminal, claude + các shell nó
        # spawn KẾ THỪA console đó → không bật cửa sổ mới. CREATE_NO_WINDOW làm claude mất console →
        # mỗi shell con tự tạo console MỚI HIỆN RA (đúng "đống cmd").
        p = subprocess.Popen(cmd, cwd=str(PROJECT_ROOT), stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                             encoding="utf-8", errors="replace", bufsize=1,
                             env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        p.stdin.write(prompt)
        p.stdin.close()                 # đóng stdin để Claude biết đề bài đã hết → bắt đầu chạy
    except Exception as e:
        emit(f"✗ Không chạy được claude: {type(e).__name__} {e}")
        return False, str(e)
    last = ""
    try:
        for raw in p.stdout:
            line = _readable(raw.rstrip("\n"))
            if line:
                last = line
                emit("  " + line)
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        emit("✗ Claude quá thời gian → dừng.")
        return False, "timeout"
    # KIỂM TẦNG HAI: đừng tin exit code. Claude có thể thoát 0 mà chưa tạo file (vd nó dừng hỏi lại).
    # Thành công = file sáng tạo CỦA PHA NÀY phải TỒN TẠI THẬT (TIEU_DE_MO_TA.txt thêm 2026-09-17 — bước 2/3
    # không tự sinh nội dung tiêu đề/mô tả tử tế được, phải có sẵn từ bước 1). Pha "script" chỉ đòi
    # script.txt (asset chưa viết là ĐÚNG thiết kế); pha "assets" đòi 5 file asset (kể cả img_doan.txt).
    need = NEED_BY_PHASE.get(phase, NEED_BY_PHASE["all"])
    if phase in ("assets", "all"):      # lane khai `assets.skip` thì không đòi file đó nữa
        try:
            import profiles as _pf
            _sk = set((_pf.load(profile_id).get("assets") or {}).get("skip") or [])
            need = [f for f in need if f not in _sk]
        except Exception:
            pass
    missing = [f for f in need if not (Path(slug_dir) / f).exists()]
    ok = (p.returncode == 0) and not missing and ("BRAIN_BLOCKED" not in last)
    if missing:
        emit(f"✗ Claude chưa tạo đủ file (thiếu: {', '.join(missing)}) — nghi nó dừng hỏi thay vì làm.")
        return False, f"thiếu file: {', '.join(missing)}"
    return ok, last


def _readable(raw):
    """stream-json → dòng đọc được cho log (tên tool Claude gọi + text nó nói). Bỏ nhiễu."""
    raw = raw.strip()
    if not raw:
        return ""
    if not raw.startswith("{"):
        return raw                                  # dòng thường (BRAIN_DONE...)
    try:
        o = json.loads(raw)
    except Exception:
        return ""
    t = o.get("type")
    if t == "assistant":
        parts = []
        for b in (o.get("message", {}) or {}).get("content", []) or []:
            if b.get("type") == "text" and b.get("text", "").strip():
                parts.append(b["text"].strip().replace("\n", " ")[:200])
            elif b.get("type") == "tool_use":
                nm = b.get("name", "?")
                inp = b.get("input", {}) or {}
                hint = inp.get("command") or inp.get("file_path") or inp.get("description") or ""
                parts.append(f"⚙ {nm}: {str(hint)[:90]}")
        return " · ".join(parts)
    if t == "result":
        return f"— Claude xong (tốn ${o.get('total_cost_usd', 0):.3f}, {o.get('num_turns','?')} lượt)"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", default="satori-jp-obaa")
    ap.add_argument("--minutes", type=float, default=30)
    ap.add_argument("--permission-mode", default="acceptEdits")
    ap.add_argument("--budget", type=float, default=0.0)
    a = ap.parse_args()
    ok, last = run_creative(a.slug, a.profile, a.minutes, permission_mode=a.permission_mode,
                            budget_usd=a.budget)
    print(f"\n{'✅' if ok else '✗'} brain {'xong' if ok else 'CHƯA xong'}: {last}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
