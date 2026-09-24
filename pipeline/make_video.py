"""make_video.py — chạy 1 video từ link đối thủ đến final.mp4. Có RESUME, có --dry-run.

Mọi thứ riêng của kênh/nhân vật nằm trong profile (`pipeline/profiles/<id>.json`) → đổi kênh chỉ là
đổi `--profile`. Xem `docs/PROFILE_ARCHITECTURE.md` + `docs/SOP_SATORI_JP.md`.

Dùng:
  py -3.13 make_video.py --profile satori-jp-obaa --slug ep05-haka --competitor <video_id|url>
  py -3.13 make_video.py --profile satori-jp-obaa --slug ep05-haka --dry-run      # chỉ phần chữ, KHÔNG tốn tiền ảnh
  py -3.13 make_video.py --profile satori-jp-obaa --slug ep05-haka --from B5      # chạy lại từ bước B5
  py -3.13 make_video.py --profile satori-jp-obaa --slug ep05-haka --only B8

Bước: B2 transcript → B3 script (2 pass + gate) → B4 giọng+SRT → B5 prompt ảnh + gen → B7 thumbnail → B8 ghép.
State ghi `state.json` trong thư mục tập: bước đã xong sẽ được BỎ QUA (chạy lại không mất tiền).
"""
import argparse
import os
import json
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import ai_steps
import gate_common
import profiles
import qc_audio
import qc_facts
import qc_final
import qc_goi_dang  # S1L luật hook + gói đăng (anh chốt 2026-09-24) — chặn cả luồng CŨ, không chỉ lean
import qc_script
import qc_visual

from paths import OUT_ROOT, res
HERE = Path(__file__).resolve().parent
ROOT = OUT_ROOT
# Khi đóng .exe, `sys.executable` LÀ chính exe chứ không phải python.exe, và máy đích có thể
# KHÔNG cài Python. Nên exe tự đóng vai trình chạy: `exe --child <script.py> ...` (xem gui_video).
_FROZEN = getattr(sys, "frozen", False)
PY = sys.executable
_CHILD = ["--child"] if _FROZEN else []


def pycmd(script, *args):
    return [PY] + _CHILD + [script] + [str(a) for a in args]


STEPS = ["B2", "B3", "B3Q", "B3F", "B3S", "B3R", "B3G", "B4", "B4Q", "B5W", "B5P", "B5", "B5K", "B5A", "B5Q",
         "B7", "B8", "B8Q", "B9", "B10", "B11"]


def _mmss(sec):
    """Mốc thời gian kiểu YouTube. Video ≥1 giờ PHẢI ghi h:mm:ss, nếu không chương bị bỏ qua."""
    sec = max(0, int(sec))
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def run(cmd, label, cho_loi=False):
    """cho_loi=True: mã thoát khác 0 KHÔNG dừng pipeline — dành cho cổng CHẤM ĐIỂM, nơi "có lỗi"
    là kết quả cần đọc chứ không phải sự cố. Người gọi tự đọc file kết quả rồi quyết định."""
    print(f"  $ {' '.join(str(c) for c in cmd[:6])} …")
    t0 = time.time()
    # ⚠️ ÉP UTF-8 CHO TIẾN TRÌNH CON. Khi log của make_video bị chuyển hướng ra file (`> build.log`)
    # thì stdout không còn là console, Python quay về bảng mã cp1252 của Windows, và tiến trình con
    # **chết ngay lúc in dòng tiếng Nhật đầu tiên** với UnicodeEncodeError. Đã dính thật: B5 báo
    # "stockfetch lỗi (exit 1)" trong khi chạy tay cùng lệnh đó thì exit 0 — khác nhau đúng ở chỗ
    # có chuyển hướng hay không. Lỗi kiểu này đánh lừa rất lâu vì nó trông y hệt lỗi mạng.
    moi_truong = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    r = subprocess.run([str(c) for c in cmd], cwd=str(HERE), env=moi_truong)
    if r.returncode != 0 and not cho_loi:
        raise SystemExit(f"✗ {label} lỗi (exit {r.returncode})")
    print(f"  ✓ {label} xong ({time.time()-t0:.0f}s)")


class Job:
    def __init__(self, prof, slug, minutes=None, force_from=None, only=None, dry=False,
                 voice="", voice_fx="", voice_speed=0.0, auto_voice=False, minutes_auto=False,
                 img_workers=0, asm_jobs=0, den=None):
        self.p = prof
        self.slug = slug
        # Giọng THEO TỪNG TẬP. Kênh rời rạc (mỗi video một người kể khác nhau: cụ bà 75, giám đốc
        # nhà tang lễ, y tá...) thì dùng chung một giọng của profile là sai người kể. `--auto-voice`
        # đọc transcript đối thủ, đoán giới/tuổi/sắc thái rồi chọn giọng khớp trong kho.
        self.voice, self.voice_fx, self.voice_speed = voice, voice_fx, voice_speed
        self.auto_voice = auto_voice
        self.ep_speed = 0.0        # tốc độ đọc THẬT của tập, chốt ở B4V
        # Hạn mức tài nguyên khi chạy NHIỀU VIDEO CÙNG LÚC (0 = tự do, dùng mặc định).
        # Chạy song song mà mỗi tập vẫn xin 24 luồng ảnh + 8 luồng ffmpeg là tự bóp nhau:
        # gpti2 chỉ có 3 key nên >24 lượt gọi cùng lúc là dính 429, còn ffmpeg thì tranh CPU.
        self.img_workers = int(img_workers or 0)
        self.asm_jobs = int(asm_jobs or 0)
        self.rate_fixed = False    # B4 vừa hiệu chỉnh char_rate đáng kể?
        self.minutes = minutes or profiles.target_minutes(prof)
        self.minutes_auto = minutes_auto and not minutes
        self.dir = ROOT / (prof.get("slug_dir") or "assets/out") / slug
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_f = self.dir / "state.json"
        self.state = json.loads(self.state_f.read_text(encoding="utf-8")) if self.state_f.exists() else {}
        self.only = only
        # DỪNG SAU MỘT BƯỚC. Có vì khâu ảnh nay do MÁY 2 vẽ (Google Flow, 0đ): máy 1 chạy tới B5K
        # rồi ra đơn, chờ ảnh về mới chạy tiếp. Không có chốt này thì B5A tự gọi gpti2 — mỗi tập
        # ~300 ảnh × 50đ, tiêu tiền cho thứ bên kia đang vẽ miễn phí, mà chạy xong mới biết.
        self.den = den
        self.dry = dry
        self.anh_mau = 0        # --anh-mau N: B5 chỉ vẽ N ảnh đầu rồi DỪNG chờ người xem (không ghi state B5)
        self.sample_only = False  # --sample-only: lane có image.sample_gate LUÔN dừng sau mẫu dù QC vision PASS (C2)
        if force_from:
            i = STEPS.index(force_from)
            # `--den` giới hạn CHẠY tới đâu — trạng thái các bước SAU `den` không hề bị đụng tới
            # trong lượt này nên KHÔNG ĐƯỢC xoá theo (bài học 2026-09-17: `--from B7 --den B7` sửa
            # thumbnail xoá sạch B8-B11 dù final.mp4/voice.mp3 không đổi 1 byte, khiến lần chạy
            # tiếp theo tưởng "chưa xong" rồi ghép lại video từ đầu, dù chỉ ảnh thumbnail đổi).
            j = STEPS.index(self.den) + 1 if self.den and self.den in STEPS else len(STEPS)
            for s in STEPS[i:j]:
                self.state.pop(s, None)

    # ---------- state
    def done(self, step, **info):
        self.state[step] = {"at": time.strftime("%Y-%m-%d %H:%M"), **info}
        self.state_f.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")

    def skip(self, step, f=None):
        if self.only and step != self.only:
            return True
        if self.den and step in STEPS and STEPS.index(step) > STEPS.index(self.den):
            return True
        if step in self.state and (f is None or Path(f).exists()):
            print(f"[{step}] bỏ qua (đã xong {self.state[step]['at']})")
            return True
        return False

    def f(self, name):
        return self.dir / name

    def voice_audio(self):
        """Bản đã giãn nhịp nếu có — đó mới là tiếng thật của video."""
        p = self.f("voice_paced.wav")
        return p if p.exists() else self.f("voice.mp3")

    def voice_srt(self):
        p = self.f("voice_paced.srt")
        return p if p.exists() else self.f("voice.srt")

    # ---------- các bước
    # Giới hạn an toàn cho độ dài bám theo video gốc. Kênh nào cũng có lẫn Shorts 1 phút và
    # video tổng hợp 2-3 tiếng; bám mù là hoặc ra bài cụt, hoặc đốt vài trăm nghìn tiền ảnh.
    MIN_PHUT, MAX_PHUT = 8.0, 60.0

    def resolve_minutes(self, source):
        """Chốt độ dài tập: bám theo THỜI LƯỢNG VIDEO GỐC nếu bật --minutes-from-source.

        Ép cứng một con số cho cả kênh là sai — cùng một kênh có bài 28 phút lẫn 44 phút.
        Đo một lần rồi ghi vào state, chạy lại không hỏi mạng nữa.
        """
        if not self.minutes_auto:
            return
        old = (self.state.get("B0") or {}).get("minutes")
        if old:
            self.minutes = float(old)
            print(f"[B0] độ dài theo video gốc (đã đo trước): {self.minutes} phút")
            return
        if not source:
            print("[B0] không có link video gốc → giữ độ dài theo hồ sơ kênh "
                  f"({self.minutes} phút)")
            return
        from fetch_script import video_minutes
        m = video_minutes(source)
        if not m:
            print(f"[B0] không đo được → giữ theo hồ sơ kênh ({self.minutes} phút)")
            return
        got = max(self.MIN_PHUT, min(self.MAX_PHUT, m))
        if got != m:
            print(f"[B0] video gốc {m} phút — ngoài khoảng an toàn, kẹp về {got} phút")
        self.minutes = got
        print(f"[B0] độ dài bám video gốc: {m} phút → làm {self.minutes} phút")
        self.done("B0", minutes=self.minutes, source_minutes=m)

    def ensure_char_rate(self):
        """Hồ sơ CHƯA ĐO tốc độ đọc thì đo ngay, TRƯỚC khi viết kịch bản.

        char_rate quyết định viết bao nhiêu chữ cho đủ số phút. Hồ sơ mới lập mang số tạm 300 kèm
        nhãn "CHƯA ĐO"; sai 20% là kịch bản dài ra 8 phút và B4Q chặn — mất trắng một lượt B3 + một
        lượt đọc TTS cả 9.000 chữ (~1.400đ). Đo trước chỉ tốn một câu ~230 chữ (~300 credit) và
        20 giây, nên luôn đáng.
        """
        v = self.p.get("voice", {}) or {}
        # Đã đo rồi thì THÔI. Số đo từ một video THẬT (có giãn nhịp, có quãng nghỉ) chính xác hơn
        # hẳn mẫu ngắn của calibrate — đo lại là thay số tốt bằng số thô.
        if v.get("char_rate_measured_at"):
            return
        # CHƯA ĐO mà cũng không mang nhãn "CHƯA ĐO": hồ sơ viết tay của kênh mới. Trước đây rơi
        # thẳng vào char_rate mặc định 309 (nhịp cụ bà satori) mà không kêu một tiếng — từ khi dự
        # án chạy nhiều ngách, đây là đường ngắn nhất để viết kịch bản dài/ngắn sai 20%.
        if not str(v.get("char_rate_note", "")).upper().replace("Ư", "U").replace("Đ", "D") \
               .startswith("CHUA DO"):
            if not profiles.rate_measured(self.p):
                print(f"[B1] hồ sơ '{self.p['id']}' chưa có char_rate đo thật "
                      f"(đang có: {v.get('char_rate') or 'không có'}) → đo ngay")
                run(pycmd("calibrate.py", "--profile", self.p["id"]), "B1 đo tốc độ đọc")
                self.p = profiles.load(self.p["id"])
                if self.ep_speed:
                    self.p.setdefault("voice", {})["ep_speed"] = self.ep_speed
                if not profiles.rate_measured(self.p):
                    raise SystemExit(
                        f"✗ B1: không đo được tốc độ đọc cho '{self.p['id']}'. DỪNG — chạy tiếp sẽ "
                        f"mượn char_rate {profiles.DEFAULT_CHAR_RATE} của kênh khác và viết sai độ dài.")
                print(f"[B1] char_rate = {profiles.char_rate(self.p)} "
                      f"(đo ở tốc độ {profiles.char_rate_speed(self.p)})")
            return
        print(f"[B1] hồ sơ '{self.p['id']}' CHƯA ĐO tốc độ đọc (đang tạm {v.get('char_rate')}) "
              f"→ đo thật trước khi viết kịch bản")
        try:
            run(pycmd("calibrate.py", "--profile", self.p["id"]), "B1 đo tốc độ đọc")
            self.p = profiles.load(self.p["id"])
            if self.ep_speed:
                self.p.setdefault("voice", {})["ep_speed"] = self.ep_speed
            print(f"[B1] char_rate = {profiles.char_rate(self.p)} "
                  f"(đo ở tốc độ {profiles.char_rate_speed(self.p)})")
        except SystemExit as e:
            print(f"[B1] đo không được ({e}) → chạy tiếp bằng số tạm, B4Q có thể chặn vì lệch dài")

    def b2_competitor(self, source):
        out = self.f("competitor.txt")
        if self.skip("B2", out):
            return
        if out.exists() and out.stat().st_size > 500:
            print(f"[B2] đã có {out.name} ({out.stat().st_size:,} byte) → dùng luôn")
            self.done("B2", chars=len(out.read_text(encoding="utf-8")), source="file có sẵn")
            return
        # KHUNG NHỊP DÙNG CHUNG CẢ LANE.
        #
        # competitor.txt dạy NHỊP và thứ tự dẫn dắt, KHÔNG dạy nội dung — mà nhịp là thuộc tính
        # của ĐỊNH DẠNG KÊNH, không phải của đề tài. Bắt bên nghiên cứu tìm lại một transcript
        # dài đúng đề tài cho từng tập là đặt ra một việc vừa khó vừa vô ích: đề tài hiếm thì
        # video cùng đề tài chỉ có bản 8–10 phút, và họ đành giao bản ngắn — đã trượt cổng B0 hai
        # lần liên tiếp đúng ở mục này (01-valentich 9,6′ · 02-walton 10,8′ cho video 28′).
        # Nên: lane giữ MỘT khung nhịp chuẩn, tập nào không có bản riêng thì mượn.
        chung = ROOT / self.p.get("slug_dir", "assets") / "_khung_nhip.txt"
        if chung.exists() and chung.stat().st_size > 500:
            out.write_text(chung.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"[B2] mượn khung nhịp chung của lane: {chung.name} "
                  f"({chung.stat().st_size:,} byte)")
            self.done("B2", chars=len(out.read_text(encoding="utf-8")),
                      source="khung nhịp chung của lane")
            return
        if not source:
            raise SystemExit("Cần --competitor (video_id/URL) hoặc sẵn file competitor.txt")
        lang = {"ja": "ja", "ko": "ko"}.get(self.p.get("language", "ja"), "en")
        # Thứ tự thử phụ đề THEO KÊNH, không đóng đinh nữa: satori bóc kênh Hàn nên "ko" đứng đầu,
        # còn ngách 都市伝説 lấy tư liệu từ kênh ANH NGỮ nên phải là "en". Khai ở profile.source_lang.
        order = str(self.p.get("source_lang") or f"ko,{lang},en")
        run(pycmd("fetch_script.py", source, "--lang", order, "--out", out), "B2 transcript")
        self.done("B2", chars=len(out.read_text(encoding="utf-8")))

    def b2b_comments(self, source):
        """Đọc BÌNH LUẬN THẬT (công khai, miễn phí) dưới video gốc → điểm chạm cảm xúc (nhấn ở
        cao trào bản mới) + thiếu sót (gợi ý cho phần 30% sáng tạo thêm). User chốt 2026-09-10.

        Vì sao không dùng biểu đồ giữ chân (Audience Retention) như hỏi ban đầu: đó là dữ liệu
        RIÊNG TƯ trong YouTube Studio, không có API lấy được của kênh đối thủ. Bình luận là tín
        hiệu công khai gần nhất.

        BỔ TRỢ — KHÔNG BAO GIỜ chặn tập. Video tắt bình luận / lỗi mạng / quá ít bình luận đều chỉ
        bỏ qua, kịch bản vẫn viết bình thường (không có gợi ý thêm, như trước đây)."""
        if self.skip("B2b", None):
            return
        try:
            from fetch_script import video_id
            # video_id() ném SystemExit khi không nhận ra id — SystemExit KHÔNG kế thừa Exception
            # nên `except Exception` không bắt được, làm chết cả tập chỉ vì bước BỔ TRỢ này. Bọc
            # riêng, dò được thì tiếp tục, không thì coi như "không có video nguồn".
            try:
                vid = video_id(source) if source else ""
            except SystemExit:
                vid = ""
            if not vid:
                self.done("B2b", note="không có video nguồn để đọc bình luận")
                return
            from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
            dl = YoutubeCommentDownloader()
            cmts, gen = [], dl.get_comments_from_url(
                f"https://www.youtube.com/watch?v={vid}", sort_by=SORT_BY_POPULAR)
            for c in gen:
                t = (c.get("text") or "").strip()
                if t:
                    cmts.append(t)
                if len(cmts) >= 80:
                    break
        except Exception as e:
            print(f"  (B2b: không tải được bình luận — {type(e).__name__} {e} → bỏ qua, không "
                  f"chặn tập)")
            self.done("B2b", loi=f"{type(e).__name__}: {e}"[:200])
            return
        if len(cmts) < 5:
            print(f"  (B2b: chỉ {len(cmts)} bình luận — quá ít để rút tín hiệu đáng tin → bỏ qua)")
            self.done("B2b", so_binh_luan=len(cmts), note="quá ít bình luận")
            return
        comp = self.f("competitor.txt").read_text(encoding="utf-8")
        d = ai_steps.analyze_comments(self.p, comp, cmts)
        if d:
            self.f("comment_insight.json").write_text(
                json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        self.done("B2b", so_binh_luan=len(cmts), co_ket_qua=bool(d))

    def comment_insight(self):
        """Đọc lại kết quả B2b nếu có — None nếu chưa chạy/không có gì đáng dùng."""
        f = self.f("comment_insight.json")
        if not f.exists():
            return None
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return None

    def b3_script(self, sheet_note="", force=False):
        out = self.f("script.txt")
        if self.skip("B3", out):
            return
        # Hàng rào ĐA KÊNH: ngưỡng nhịp văn phải là của CHÍNH kênh này. Mượn DEFAULT_GATE
        # (nhịp tâm tình của cụ bà satori) cho một kênh kể tài liệu giọng nam = gate gật đầu
        # cho đúng thứ văn mình không muốn, mà không báo gì.
        if not profiles.gate_declared(self.p) and not force:
            raise SystemExit(
                f"✗ B3: hồ sơ '{self.p['id']}' chưa khai `script.gate` riêng → sẽ mượn nhịp văn "
                f"của kênh satori. DỪNG. Thêm gate vào profiles/{self.p['id']}.json "
                f"(mẫu: docs/PROFILE_ARCHITECTURE.md §5) rồi chạy lại.")
        # S1L — LUẬT HOOK + GÓI ĐĂNG, đặt Ở ĐÂY để luồng CŨ (`flow != "lean"`) không đi cửa sau.
        # Cổng chính nằm ở lean_script.run(); 6 lane đang sản xuất đều lean nên nhánh này hiện không
        # ai đi qua — nhưng hễ mở 1 lane không khai `flow` (mặc định = luồng cũ) là luật lại bị bỏ
        # lọt y như trước. Bài học memory `soi-pham-vi-moi-file-dung-chung`: vá 1 nhánh thì phải soi
        # nhánh còn lại của CÙNG một việc.
        loi_luat = qc_goi_dang.cong_truoc_khi_viet(self.dir, self.p)
        if loi_luat and not force:
            raise SystemExit("✗ B3/S1L: chưa đủ điều kiện luật hook + gói đăng → DỪNG "
                             "(chưa tốn lượt viết nào)\n   - " + "\n   - ".join(loi_luat))
        comp = self.f("competitor.txt").read_text(encoding="utf-8")
        series_f = self.f("series_ctx.txt")
        ctx = series_f.read_text(encoding="utf-8") if series_f.exists() else ""
        insight = self.comment_insight()
        if insight:
            print(f"  [B2b] dùng {len(insight.get('diem_cham') or [])} điểm chạm + "
                  f"{len(insight.get('thieu_sot') or [])} thiếu sót từ bình luận thật")
        res = ai_steps.write_script(self.p, comp, self.minutes, ctx, comment_insight=insight)
        out.write_text(res["text"], encoding="utf-8")
        if res.get("beats"):        # khung PASS 0 — để soi bằng mắt xem có lọt tên/thoại gốc không
            self.f("beats.txt").write_text(res["beats"], encoding="utf-8")
        if res.get("pass1_raw"):    # bản nháp THÔ trước nén — để khôi phục khi nén/gate làm hỏng (bài học Lane G ep01)
            self.f("script_pass1_raw.txt").write_text(res["pass1_raw"], encoding="utf-8")
        # ⚠️ CHỈ đánh dấu XONG khi gate ĐẠT. Bản cũ ghi `done("B3")` trước rồi mới xét gate ⇒ lượt
        # chạy sau thấy B3 "đã xong" nên BỎ QUA hẳn, đi thẳng sang B3Q với đúng cái kịch bản vừa bị
        # từ chối. Đo thật ep03: sửa xong lỗi trong ai_steps rồi chạy lại, tưởng đang kiểm bản vá
        # mà thật ra B3 không hề chạy lần nào — bản 9.026 chữ (NGẮN −12%) đi tiếp như không có gì.
        # Nói cách khác: "sửa code rồi chạy lại" IM LẶNG không chạy lại.
        # Vẫn ghi vết thất bại (`B3_truot`) để lượt sau đọc được đã hỏng ở đâu.
        if res["gate_problems"]:
            self.state["B3_truot"] = {"at": time.strftime("%Y-%m-%d %H:%M"),
                                      "chars": res["metrics"]["chars"],
                                      "passes": res["passes"], "gate": res["gate_problems"]}
            self.state_f.write_text(json.dumps(self.state, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
        else:
            self.done("B3", chars=res["metrics"]["chars"], minutes=res["metrics"]["minutes"],
                      passes=res["passes"], gate=res["gate_problems"])
        if res["gate_problems"]:
            # Trước đây chỉ CẢNH BÁO rồi chạy tiếp → tiêu tiền giọng + ảnh cho kịch bản đã biết là
            # lỗi (đo thật ep09: hội thoại 21%). Gate hỏng = DỪNG.
            print("  ✗ GATE KHÔNG ĐẠT:")
            for b in res["gate_problems"]:
                print("     -", b)
            print("  Sửa: chạy lại '--from B3' (viết bản khác), sửa tay script.txt, "
                  "hoặc --force-qc nếu chấp nhận.")
            if not force:
                raise SystemExit("✗ B3: kịch bản chưa qua gate → DỪNG trước khi tiêu tiền.")

    def b3q_qc(self, force=False, fix=True):
        """QC NỘI DUNG — chặn TRƯỚC khi tiêu tiền giọng + ảnh (user chốt 2026-09-08).

        Gate của B3 chỉ đo nhịp/độ dài/độ sạch; kịch bản mâu thuẫn hoặc dịch sát bản gốc vẫn qua.
        Ở đây mới kiểm logic, 伏線, lặp ý, và tỉ lệ bám gốc 70/30."""
        outf = self.f("qc.json")
        if self.skip("B3Q", outf):
            return
        sf = self.f("script.txt")
        script = sf.read_text(encoding="utf-8")
        comp_f = self.f("competitor.txt")
        comp = comp_f.read_text(encoding="utf-8") if comp_f.exists() else ""
        res = qc_script.run(self.p, script, comp)
        qc_script.report(res)
        # TỰ SỬA 1 lượt: đưa đúng danh sách lỗi QC chỉ ra, bắt sửa tại chỗ, giữ độ dài.
        # Chỉ nhận bản sửa khi gate KHÔNG tệ đi VÀ QC ít lỗi hơn — kẻo "sửa" thành hỏng chỗ khác.
        if res["verdict"] in ("SUA", "HONG") and not res["infra_errors"] and fix:
            issues = ai_steps.issues_of(res)
            if issues:
                print(f"[B3Q] tự sửa {len(issues)} lỗi …")
                old_gate, _ = ai_steps.check(self.p, script, self.minutes)
                try:
                    fixed = ai_steps.repair_script(self.p, script, issues, self.minutes)
                except Exception as e:
                    fixed = None
                    print(f"  (sửa thất bại: {type(e).__name__} {e})")
                if fixed:
                    new_gate, _ = ai_steps.check(self.p, fixed, self.minutes)
                    res2 = qc_script.run(self.p, fixed, comp)
                    n1, n2 = len(ai_steps.issues_of(res)), len(ai_steps.issues_of(res2))
                    ok = (len(new_gate) <= len(old_gate) and not res2["infra_errors"] and n2 < n1)
                    print(f"  [sửa] gate {len(old_gate)}→{len(new_gate)} lỗi · QC {n1}→{n2} lỗi · "
                          f"{'NHẬN' if ok else 'BỎ (không tốt hơn)'}")
                    if ok:
                        sf.with_suffix(".pre_fix.txt").write_text(script, encoding="utf-8")
                        sf.write_text(fixed, encoding="utf-8")
                        script, res = fixed, res2
                        qc_script.report(res)
        outf.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        v = res["verdict"]
        self.done("B3Q", verdict=v, infra_errors=len(res["infra_errors"]),
                  bam_goc=(res.get("beats") or {}).get("ty_le_bam_goc"))
        if force:
            print("[B3Q] --force-qc: bỏ qua kết luận, chạy tiếp.")
            return
        if v == "KHONG_KIEM_DUOC":
            print("  'không thấy lỗi' lúc này là SỐ ẢO — QC không chạy được, không phải nội dung sạch.")
            print("  Chạy lại, hoặc --force-qc nếu chấp nhận rủi ro.")
            raise SystemExit("✗ B3Q: QC KHÔNG chạy được (lỗi hạ tầng) → DỪNG trước khi tiêu tiền.")
        if v == "HONG":
            print(f"  Chi tiết: {outf}")
            print("  Sửa: chạy lại '--from B3' để viết bản khác, hoặc sửa tay script.txt.")
            raise SystemExit("✗ B3Q: kịch bản HỎNG (mâu thuẫn nặng hoặc sao chép bản gốc) → DỪNG.")
        if v == "SUA":
            print("[B3Q] ⚠️ còn lỗi VỪA — chạy tiếp, nhưng nên soi lại các mục ✗ ở trên.")

    # Tuổi người kể → hiệu ứng giọng + tốc độ đọc. Bám THEO SỐ TUỔI khi nhận được, vì chia thô
    # 3 mức thì ông 60 và ông 45 bị xử lý y hệt nhau — mà hai người đó nghe khác hẳn.
    # Thang: (tuổi tối thiểu, fx, tốc độ) — dò từ già xuống trẻ.
    _THANG_TUOI = [
        (75, "old-frail", 0.90),   # rất già: run giọng, đọc chậm hẳn
        (68, "old-med", 0.92),     # già rõ  — mức chuẩn của ngách Satori
        (58, "old-mild", 0.94),    # chớm già: chỉ trầm nhẹ
        (45, "none", 0.96),        # trung niên: giữ giọng gốc, hơi chậm cho dễ nghe
        (30, "none", 0.98),
        (0, "young", 1.0),
    ]
    # Không nhận được số tuổi thì lùi về nhóm tuổi thô.
    _FX_BY_AGE = {"old": "old-med", "middle_aged": "none", "young": "young"}
    _SPEED_BY_AGE = {"old": 0.92, "middle_aged": 0.98, "young": 1.0}

    @classmethod
    def fx_speed_cho(cls, det):
        """(fx, tốc độ) khớp người kể của tập — ưu tiên SỐ TUỔI, không có thì theo nhóm tuổi."""
        try:
            tuoi = int(re.sub(r"\D", "", str(det.get("age") or ""))[:3])
        except Exception:
            tuoi = 0
        if tuoi:
            for moc, fx, sp in cls._THANG_TUOI:
                if tuoi >= moc:
                    return fx, sp, f"{tuoi} tuổi"
        band = det.get("age_band") or "middle_aged"
        return (cls._FX_BY_AGE.get(band, "none"), cls._SPEED_BY_AGE.get(band, 0.98),
                f"nhóm {band}")

    def detect_narrator(self):
        """NGƯỜI KỂ CỦA RIÊNG TẬP NÀY — chạy sau B2, TRƯỚC B3.

        Một kênh có nhiều video, mỗi video một người kể khác nhau (bà mẹ / ông chồng / y tá /
        giám đốc nhà tang lễ). Hồ sơ kênh chỉ giữ được MỘT người, nên phải nhận ra theo từng
        video, nếu không kịch bản viết sai ngôi kể và ảnh vẽ sai mặt nhân vật chính — trong khi
        giọng đọc lại đúng, thành ra lệch hẳn nhau.

        Kết quả ghi vào state (B2N) và nuôi CẢ BA: kịch bản, ảnh, giọng.
        """
        if not self.auto_voice:
            return None
        old = self.state.get("B2N") or {}
        if old.get("persona"):
            print(f"[B2N] người kể (đã nhận trước): {old.get('persona')}")
            self.p = ai_steps.apply_narrator(self.p, old)
            return old
        src = self.f("competitor.txt")
        if not src.exists():
            return None
        det = ai_steps.detect_narrator(src.read_text(encoding="utf-8"),
                                       self.p.get("language", ""), self.p.get("market", ""))
        if not det:
            print("[B2N] không nhận ra người kể → giữ người kể của hồ sơ kênh")
            return None
        print(f"[B2N] người kể tập này: {det.get('persona')}")
        print(f"      {det.get('gender')}/{det.get('age_band')} · vai {det.get('role')} "
              f"· giọng {det.get('tone')} (tin cậy {det.get('confidence')})")
        if det.get("character_sheet"):
            print(f"      mặt nhân vật trong ảnh: {det['character_sheet'][:90]}")
        self.done("B2N", **det)
        self.p = ai_steps.apply_narrator(self.p, det)
        return det

    def pick_voice(self):
        """Chốt giọng cho TẬP NÀY → (voice_id, fx, speed); rỗng = để tts.py lấy theo profile.

        Dùng CHÍNH kết quả nhận người kể ở B2N, nên giọng đọc luôn khớp với kịch bản và với mặt
        nhân vật trong ảnh. Trước đây voice tự đoán riêng một lần nữa → có thể ra người khác hẳn.
        """
        if self.voice or self.voice_fx or self.voice_speed:
            return self.voice, self.voice_fx, self.voice_speed
        if not self.auto_voice:
            return "", "", 0.0
        old = self.state.get("B4V") or {}
        if old.get("voice_id"):
            print(f"[B4V] dùng lại giọng đã chọn: {old.get('voice_name')} ({old['voice_id']}) "
                  f"fx={old.get('fx')} speed={old.get('speed')}")
            self.ep_speed = float(old.get("speed") or 0)
            if self.ep_speed:
                self.p.setdefault("voice", {})["ep_speed"] = self.ep_speed
            return old["voice_id"], old.get("fx") or "", float(old.get("speed") or 0)
        det = self.state.get("B2N") or {}
        if not det.get("gender"):
            print("[B4V] chưa nhận được người kể → giữ giọng theo hồ sơ kênh")
            return "", "", 0.0
        try:
            import voice_bank
            # Kho giọng dò theo TỪ KHOÁ tiếng Việt (bảng PERSONA_KEYWORDS). Câu tả sắc thái không
            # có chữ "cụ bà"/"cụ ông" nên phải thêm vào, nếu không mất hẳn nhóm giọng già ấm và
            # vớ phải giọng thuyết trình (đo thật: ra "Alice - Clear, Engaging Educator" cho một
            # cụ bà 74 tuổi, trong khi đúng phải là "Ado - Mature & Soothing").
            band = det.get("age_band") or "middle_aged"
            them = ""
            if band == "old":
                them = "cu ba ke chuyen tam tinh" if det["gender"] == "female" else "cu ong ke chuyen"
            elif band == "young":
                them = "tre"
            q = f"{det.get('tone') or ''} {them}".strip() or "ke chuyen"
            hits = voice_bank.suggest(q, gender=det["gender"], limit=5)
            if not hits:
                hits = voice_bank.suggest("ke chuyen", limit=5)
        except Exception as e:
            print(f"[B4V] không tra được kho giọng ({type(e).__name__} {e}) → theo hồ sơ kênh")
            return "", "", 0.0
        if not hits:
            print("[B4V] không có giọng nào khớp → giữ giọng theo hồ sơ kênh")
            return "", "", 0.0
        v = hits[0][1]
        band = det.get("age_band") or "middle_aged"
        fx, speed, cancu = self.fx_speed_cho(det)
        print(f"[B4V] giọng khớp người kể: {v.get('name')} ({v.get('voice_id')}) "
              f"fx={fx} speed={speed}  ← theo {cancu}")
        self.ep_speed = float(speed)
        # Gắn vào BẢN SAO hồ sơ → target_chars() tự quy đổi số chữ theo tốc độ đọc của tập này.
        self.p.setdefault("voice", {})["ep_speed"] = self.ep_speed
        self.done("B4V", voice_id=v.get("voice_id"), voice_name=v.get("name"),
                  fx=fx, speed=speed, gender=det.get("gender"), age_band=band,
                  age=det.get("age"), tone=det.get("tone"))
        return v.get("voice_id"), fx, float(speed)

    def b3f_facts(self, force=False):
        """B3F — CHI TIẾT NÀO TRONG KỊCH BẢN KHÔNG CÓ TRONG TƯ LIỆU?

        Cổng này bắt đúng thứ mọi cổng khác mù. B3Q hỏi "kịch bản có tự mâu thuẫn không";
        cổng này hỏi **"chi tiết này ở ĐÂU ra"**.

        Đo thật 2026-09-10: kịch bản viết「1989年、日本の埼玉県にある日立製作所の研究所で…」trong khi
        tư liệu KHÔNG hề nói phòng thí nghiệm ở đâu. Tra lại: Wikipedia ghi Tonomura ở Hitachi
        Central Research Laboratory, Physics World ghi "Advanced Research Laboratory in Hitachi,
        Tokyo" — không nguồn nào nói Saitama. Bản nháp đầu còn điền HAI kiểu khác nhau ở hai
        chương; B3Q bắt được mâu thuẫn rồi "sửa" bằng cách chọn một cái cho nhất quán — và chọn
        phải cái sai. **B3Q làm cho NHẤT QUÁN, B3F làm cho ĐÚNG NGUỒN.**
        """
        if self.skip("B3F", None):
            return
        if ((self.p.get("script", {}) or {}).get("mode") or "").lower() not in ("documentary", "fiction_facts"):
            print("[B3F] kênh không ở chế độ documentary/fiction_facts → bỏ qua kiểm dữ kiện")
            self.done("B3F", skipped="not_documentary")
            return
        ho_so = self.f("series_ctx.txt")
        if not ho_so.exists():
            print("[B3F] ⚠️ KHÔNG có series_ctx.txt — kịch bản tài liệu mà không có tư liệu nguồn "
                  "thì mọi chi tiết đều là do mô hình tự nghĩ. Nên dừng lại và viết hồ sơ đề tài.")
            if not force:
                raise SystemExit("✗ B3F: thiếu tư liệu (series_ctx.txt) → DỪNG.")
            return
        kq = qc_facts.kiem(self.f("script.txt").read_text(encoding="utf-8"),
                           ho_so.read_text(encoding="utf-8"))
        n = qc_facts.bao_cao(kq)
        self.f("qc_facts.json").write_text(
            json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
        tong = kq["nguon_tong"]
        if tong and kq["nguon_co"] / tong < 0.5:
            print(f"  ⚠️ chỉ {kq['nguon_co']}/{tong} dòng tư liệu có nguồn tra lại được. "
                  f"Hồ sơ đề tài cần ghi 〔nguồn: …〕 cho từng dòng (xem docs/KHUON_HO_SO_DE_TAI.md).")
        self.done("B3F", findings=n, heavy=len(kq["nang"]),
                  sources=f"{kq['nguon_co']}/{tong}")
        if kq["nang"] and not force:
            print("  Sửa: bổ sung dữ kiện vào series_ctx.txt (kèm nguồn) rồi '--from B3', "
                  "hoặc sửa tay script.txt bỏ chi tiết không có nguồn, hoặc --force-qc.")
            raise SystemExit(f"✗ B3F: {len(kq['nang'])} chi tiết KHÔNG có trong tư liệu → DỪNG "
                             f"trước khi tiêu tiền giọng + hình.")

    def b3_lean(self, force=False):
        """B3 theo LUỒNG GỌN (`script.flow="lean"`) — xem lean_script.py + docs/QUY_TRINH_KICH_BAN_GON.md v2.
        Thay trọn B3→B3G của luồng cũ bằng: S1Q hồ sơ → S2 Fable viết đúng ngân sách → S3 đo tất định →
        S5 Sol (lens lane) → patch ≤2 (mỗi patch: máy + Sol lại) → PASS khoá sha256 | ESCALATE | BLOCK."""
        out = self.f("script.txt")
        if self.only and self.only != "B3":
            return
        if self.den and STEPS.index("B3") > STEPS.index(self.den):
            return
        ok, msg, level = gate_common.kiem_lock(self.dir)
        if level == "PASS" and not force:
            print(f"[B3] bỏ qua — {msg}")
            return
        if not profiles.gate_declared(self.p) and not force:
            raise SystemExit(f"✗ B3: hồ sơ '{self.p['id']}' chưa khai `script.gate` riêng → DỪNG.")
        sys.path.insert(0, str(HERE))
        import lean_script
        lean_script.run(self, force=force)

    def kiem_lock(self, buoc):
        """NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS — gọi ở đầu mọi bước pha asset. Lane flow=lean: sha lệch/chưa PASS
        → DỪNG. Lane luồng cũ (chưa có lock) → chỉ WARN, không gãy."""
        ok, msg, level = gate_common.kiem_lock(self.dir)
        lean = ((self.p.get("script", {}) or {}).get("flow") or "").lower() == "lean"
        if level == "FAIL":
            print(f"[{buoc}] ✗ LOCK: {msg}")
            raise SystemExit(f"✗ {buoc}: {msg}")
        if level == "WARN" and lean:
            raise SystemExit(f"✗ {buoc}: lane flow=lean nhưng {msg} → chạy B3 (lean) trước.")
        print(f"[{buoc}] lock: {msg}")
        # 2026-09-23 (Task 10): hook 20-30s là artifact THƯỢNG NGUỒN — hook lệch tiêu đề/thumbnail/
        # lời hứa (HOOK_STALE) thì mọi ảnh/giọng/ghép dựng tiếp theo đều dựng trên nền sai, cấm đi tiếp.
        # Tập cũ (trước tính năng hook) chưa có hook_lock.json thì chỉ NHẮC, không chặn — không hồi tố.
        # 2026-09-23 (Việc 2, vá review cuối): kênh CHƯA khai `script.hook.enabled=true` thì bỏ qua
        # HẲN phép kiểm này — hook_stage.is_enabled() là ngã rẽ DUY NHẤT, không suy luận theo lane.
        import hook_stage
        if hook_stage.is_enabled(self.p):
            stale, ly_do = hook_stage.kiem_stale(self.dir)
            if stale:
                raise SystemExit(f"✗ {buoc}: HOOK_STALE — " + " · ".join(ly_do))
            if ly_do:   # ["chưa có hook lock"]
                print(f"[{buoc}] ⚠️ {ly_do[0]} — tập cũ: chạy hook_stage.py --mode repair trước khi giao")

    def b3s_sol(self, force=False):
        """B3S — QC ĐỘC LẬP bằng GPT-5.6-sol (khác hãng hẳn với Gemini/Claude đang viết+B3Q/B3F),
        xem qc_script_sol.py. CHỈ chạy khi lane khai `profile.script.sol_qc = true`.

        Bài học 2026-09-18 (kenko-chiebukuro ep01/ep02, xem docs/SOP_LANE_E.md §B3S): B3Q/B3F
        cùng "họ suy luận" với người viết (Gemini QC văn Gemini/Claude viết) nên để lọt lỗi AN
        TOÀN/KHÁI NIỆM mà B3S bắt được ngay lượt đầu — dù CẢ HAI TẬP đều đã "PASS" B3Q/B3F và ĐÃ
        GIAO HÀNG THẬT trước khi phát hiện (ep02: câu chuyện yếu tay ĐỘT NGỘT bị kể như tuổi già
        bình thường, đúng dấu hiệu đột quỵ; ep01: hàng loạt lỗ an toàn — warfarin, phơi nắng, cá
        hóc, chấn thương đầu). Nhưng B3S áp chuẩn học thuật nghiêm nên KHÔNG BAO GIỜ tự chấm PASS
        tuyệt đối cho văn phổ thông (đo thật ep01: FIX lặp lại 3 vòng liền, cùng loại góp ý "có
        thể hedging thêm") — CẤM lặp vô hạn đợi PASS. Chính sách: sửa headless ĐÚNG 1 lần (không
        phải nhiều lần dò brief tay như lúc test — máy chạy mù không phán đoán SAI/CHƯA HAY được,
        thử nhiều lần chỉ tốn thời gian/tiền), chấm lại ĐÚNG 1 lần, rồi DỪNG:
          - PASS/FIX (dù vòng 1 hay sau khi sửa) → cho qua, ghi log, KHÔNG chặn B4.
          - REMAKE (kể cả sau khi đã thử sửa) → CHẶN HẲN trước B4. Đây là tín hiệu lỗi THIẾT KẾ/
            PHẠM VI (vd tiêu đề hứa hẹn vượt nội dung thật), không phải câu chữ — máy không tự
            quyết được, cần Claude thật đọc lại (giống cách B3F chặn khi thiếu tư liệu nguồn).
        """
        if self.skip("B3S", None):
            return
        if not ((self.p.get("script", {}) or {}).get("sol_qc")):
            return  # lane không bật cờ này → bỏ qua êm, không phải lỗi
        sys.path.insert(0, str(HERE))
        import qc_script_sol
        sf = self.f("script.txt")
        script = sf.read_text(encoding="utf-8")
        title = ""
        lf = self.f("listting.txt")
        if lf.exists():
            lines = lf.read_text(encoding="utf-8").splitlines()
            title = next((l.strip() for l in lines if l.strip()), "")
        print("[B3S] QC độc lập bằng GPT-5.6-sol …")
        verdict, text = qc_script_sol.run(script, title, profile_id=self.p["id"],
                                          out=self.f("qc_sol_report.txt"))
        fixed_ap_dung = False
        # `script.sol_fix_headless = false` (Lane F, 2026-09-20): TẮT lượt sửa headless — đo thật ep01: mỗi lượt
        # Fable sửa mù lại chèn thêm dữ kiện mới (điều kiện 扶養, "thuế trả thừa") và +150–300 chữ, sol lượt 2
        # lại bắt đúng những câu vừa chèn. Với lane này Claude trong tab đọc báo cáo rồi sửa tay. Lane khác không đổi.
        if verdict == "FIX" and (self.p.get("script", {}) or {}).get("sol_fix_headless", True) is False:
            print("[B3S] FIX — lane tắt sửa headless (script.sol_fix_headless=false) → chỉ ghi báo cáo, Claude sửa tay.")
        elif verdict == "FIX":
            print("[B3S] FIX — thử sửa 1 lần bằng claude -p headless …")
            fixed = None
            try:
                import claude_p_bridge
                brief = (
                    "Đây là báo cáo QC ĐỘC LẬP (GPT-5.6-sol) cho kịch bản dưới đây. Hãy sửa TẠI "
                    "CHỖ (không viết lại từ đầu, giữ nguyên văn phong và độ dài) đúng những lỗi "
                    "THẬT/NGUY HIỂM mà báo cáo chỉ ra — an toàn vật lý, cảnh báo cấp cứu, tương "
                    "tác thuốc, chuẩn tham chiếu sai đối tượng, mâu thuẫn logic, lỗi ngữ pháp "
                    "thật. KHÔNG cần sửa hết các góp ý chỉ mang tính học thuật/diễn đạt thận "
                    "trọng hơn nếu nội dung đã đủ an toàn và đúng — phân biệt rõ SAI (bắt buộc "
                    "sửa) và CHƯA HAY (bỏ qua được). Output CHỈ kịch bản hoàn chỉnh, không kèm "
                    f"giải thích.\n\n=== BÁO CÁO QC ===\n{text}\n\n=== KỊCH BẢN ===\n{script}")
                # SỬA tại chỗ = việc của patch_model (Opus), không phải model viết (Fable) — quy tắc 2026-09-22
                r = claude_p_bridge.ask(brief, timeout=1500, min_chars=int(len(script) * 0.7),
                                        require_sentence_end=True, max_chars=int(len(script) * 1.08),
                                        model=claude_p_bridge.patch_model_of(self.p))
                fixed = r.text
            except Exception as e:
                print(f"  (sửa thất bại: {type(e).__name__} {e}) — giữ bản gốc, chạy tiếp.")
            if fixed:
                sf.with_suffix(".pre_b3s.txt").write_text(script, encoding="utf-8")
                sf.write_text(fixed, encoding="utf-8")
                script = fixed
                fixed_ap_dung = True
                verdict, text = qc_script_sol.run(script, title, profile_id=self.p["id"],
                                                  out=self.f("qc_sol_report_2.txt"))
        self.done("B3S", verdict=verdict, fixed=fixed_ap_dung)
        if verdict == "REMAKE":
            outf = self.f("qc_sol_report_2.txt" if fixed_ap_dung else "qc_sol_report.txt")
            print(f"  Chi tiết: {outf}")
            print("  Đây là lỗi THIẾT KẾ/PHẠM VI (không phải câu chữ) — cần Claude đọc và quyết "
                  "định lại phạm vi/tiêu đề trước khi tiếp tục, máy không tự quyết được.")
            if not force:
                raise SystemExit("✗ B3S: GPT-5.6-sol vẫn REMAKE sau khi thử sửa → DỪNG trước B4.")
        elif verdict == "FIX":
            print("[B3S] ⚠️ vẫn còn FIX sau khi đã thử sửa 1 lần (thường là góp ý diễn đạt thận "
                  "trọng hơn chứ không phải lỗi nguy hiểm) — chạy tiếp, xem báo cáo nếu muốn soi.")
        else:
            print("[B3S] ✓ PASS")

    def b3r_final_review(self, force=False):
        """B3R — NGHIỆM THU CUỐI kịch bản bằng model Claude do lane khai (`script.final_review_model`,
        Lane G: Fable 5.1 — anh chốt 2026-09-20 "nghiệm thu cuối cũng dùng Fable").

        Khác B3S (GPT-5.6-sol, KHÁC HÃNG, chấm chuẩn học thuật/an toàn) — B3R đọc như một BIÊN TẬP
        VIÊN tiếng Nhật của chính kênh: đủ 5 hồi/N mục chưa, thoại có tự nhiên không, cú lật hướng nội
        ở mục cuối, CTA giữa video, outro nguyên văn, địa điểm/giá có bịa ngoài series_ctx không, câu
        nào TTS đọc sẽ gãy. Đây là lớp thay cho việc "Claude Code trong tab đọc lại bằng mắt" (SOP_LANE_G
        §1c dòng 11) — kết quả ghi file để anh soi, không nằm trong đầu tab.
        Cùng họ với model viết (Fable viết – Fable chấm) nên KHÔNG thay được B3S; chỉ là lớp cuối.
        Chính sách như B3S: FIX → sửa TẠI CHỖ 1 lần rồi chấm lại; REMAKE → DỪNG; lane không khai → bỏ qua."""
        if self.skip("B3R", None):
            return
        model = ((self.p.get("script", {}) or {}).get("final_review_model") or "").strip()
        if not model:
            return
        sys.path.insert(0, str(HERE))
        import claude_p_bridge
        sf = self.f("script.txt")
        script = sf.read_text(encoding="utf-8")
        ctxf = self.f("series_ctx.txt")
        ctx = ctxf.read_text(encoding="utf-8") if ctxf.exists() else ""
        g = profiles.gate(self.p)
        n_items = g.get("list_item_count") or 5
        outro = (self.p.get("script", {}) or {}).get("outro_line") or ""

        # Tiêu chí nghiệm thu: lane khai `script.final_review_criteria` (văn bản tự do, đánh số) thì dùng
        # nguyên văn; không khai → khối mặc định bên dưới (viết cho Lane G, 2026-09-20). Hàng rào #2:
        # lane khác (F...) KHÔNG thêm nhánh if ở đây, khai tiêu chí trong profile.
        tieu_chi_rieng = ((self.p.get("script", {}) or {}).get("final_review_criteria") or "").strip()

        def _review(text):
            brief = (
                "Bạn là BIÊN TẬP VIÊN kịch bản tiếng Nhật của kênh YouTube manga story cho khán giả 60+. "
                "Đọc TOÀN BỘ kịch bản dưới đây và nghiệm thu theo đúng các tiêu chí, trả về DUY NHẤT một JSON "
                "(không markdown, không giải thích ngoài JSON) dạng:\n"
                '{"verdict":"PASS|FIX|REMAKE","issues":[{"muc":"<tiêu chí>","muc_do":"nang|vua|nhe","vi_tri":"<trích 15-30 chữ>","loi":"<mô tả ngắn>","sua":"<gợi ý sửa tại chỗ>"}],"tom_tat":"<2 câu tiếng Việt>"}\n'
                "Tiêu chí:\n"
            ) + (tieu_chi_rieng + "\n" if tieu_chi_rieng else (
                f"1) Cấu trúc 5 hồi: hook nghịch lý ở câu đầu (không chào hỏi) → nhân vật tên/tuổi/nghề → mentor → đúng {n_items} mục đếm đủ, đều nhau → mục cuối là cú lật HƯỚNG NỘI → sáng hôm sau khép cảnh đầu.\n"
                "2) Mỗi mục đủ: tên cụ thể · đối thoại 2 người · nhân vật TỰ THỬ · mini-chốt + câu hỏi dẫn.\n"
                "3) Có 1 câu CTA mời bình luận ở khoảng giữa video.\n"
                f"4) Câu cuối nguyên văn:「{outro}」\n"
                "5) DỮ KIỆN: địa điểm / giá tiền / số liệu / tên tổ chức được GIỚI THIỆU CHO NGƯỜI XEM như thông tin thật "
                "(nơi nên đi, vé bao nhiêu, dịch vụ gì, nghiên cứu nào) PHẢI có trong TƯ LIỆU kèm dưới; cái nào KHÔNG có → "
                "issue muc_do 'nang' (bịa). KHÔNG tính: tên/tuổi/nghề/quê quán/nơi ở của nhân vật hư cấu, số tiền cá nhân "
                "của nhân vật (lương hưu, tiền tiêu vặt) — đó là hư cấu được phép.\n"
                "6) Thoại「」tự nhiên như người Nhật nói, không văn dịch; giọng「俺」nam 60–67 nhất quán; không lên lớp.\n"
                "7) Hướng VUI/RẺ giữ trọn — không trượt sang kịch tính mất tiền/bi kịch.\n"
                "8) Claim sức khoẻ/若返る không tuyệt đối (không '必ず治る/100%'); không xúc phạm nhóm người nào.\n"
                "9) Câu nào TTS đọc sẽ gãy (quá dài không ngắt, ký hiệu lạ, chữ Latin/Hàn, marker, ngoặc vuông) → nêu.\n"
            )) + (
                "Quy ước verdict: REMAKE chỉ khi lỗi THIẾT KẾ (sai cấu trúc/sai hướng/thiếu mục) không sửa tại chỗ được; "
                "FIX khi có lỗi 'nang' hoặc ≥3 lỗi 'vua' sửa tại chỗ được; còn lại PASS. Phân biệt SAI (phải sửa) với CHƯA HAY (không tính).\n\n"
                f"=== TƯ LIỆU (series_ctx.txt) ===\n{ctx or '(không có — mọi địa điểm/giá cụ thể đều là bịa)'}\n\n=== KỊCH BẢN ===\n{text}")
            r = claude_p_bridge.ask(brief, model=model, timeout=900, min_chars=20)
            raw = r.text.strip()
            raw = raw[raw.find("{"): raw.rfind("}") + 1] if "{" in raw and "}" in raw else raw
            try:
                j = json.loads(raw)
            except Exception:
                raise SystemExit(f"✗ B3R: {model} không trả JSON hợp lệ → DỪNG (không PASS ảo). Raw: {raw[:200]}")
            v = str(j.get("verdict", "")).upper()
            if v not in ("PASS", "FIX", "REMAKE"):
                raise SystemExit(f"✗ B3R: verdict lạ {v!r} → DỪNG.")
            return v, j, r

        print(f"[B3R] nghiệm thu cuối bằng {model} …")
        v, j, r = _review(script)
        rep = self.f("qc_final_review.txt")
        rep.write_text(f"model={model} · {r.elapsed:.0f}s · verdict={v}\n" + json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → {v} · {len(j.get('issues') or [])} issue · {r.elapsed:.0f}s · {rep.name}")
        fixed_ap_dung = False
        if v == "FIX":
            pm = claude_p_bridge.patch_model_of(self.p)   # chấm = final_review_model; SỬA = patch_model (quy tắc 2026-09-22)
            print(f"[B3R] FIX — sửa TẠI CHỖ 1 lần bằng {pm} …")
            brief = ("Sửa TẠI CHỖ kịch bản tiếng Nhật dưới đây đúng những issue trong báo cáo (giữ văn phong, độ dài ±5%, "
                     "KHÔNG viết lại từ đầu, KHÔNG thêm dữ kiện ngoài TƯ LIỆU). Output CHỈ kịch bản hoàn chỉnh.\n\n"
                     f"=== BÁO CÁO ===\n{json.dumps(j, ensure_ascii=False)}\n\n=== TƯ LIỆU ===\n{ctx}\n\n=== KỊCH BẢN ===\n{script}")
            try:
                r2 = claude_p_bridge.ask(brief, model=pm, timeout=1500, min_chars=int(len(script) * 0.85),
                                         require_sentence_end=True, max_chars=int(len(script) * 1.08))
                sf.with_suffix(".pre_b3r.txt").write_text(script, encoding="utf-8")
                sf.write_text(r2.text, encoding="utf-8")
                script = r2.text
                fixed_ap_dung = True
                v, j, r = _review(script)
                self.f("qc_final_review_2.txt").write_text(
                    f"model={model} · {r.elapsed:.0f}s · verdict={v}\n" + json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
                print(f"  → sau sửa: {v} · {len(j.get('issues') or [])} issue")
            except Exception as e:
                print(f"  (sửa thất bại: {type(e).__name__} {e}) — giữ bản gốc, chạy tiếp.")
        self.done("B3R", verdict=v, model=model, fixed=fixed_ap_dung)
        if v == "REMAKE":
            print(f"  Chi tiết: {rep}")
            if not force:
                raise SystemExit(f"✗ B3R: {model} kết luận REMAKE (lỗi thiết kế) → DỪNG. Anh/Claude đọc báo cáo rồi quyết.")
        elif v == "FIX":
            print("[B3R] ⚠️ vẫn còn FIX sau 1 lần sửa — chạy tiếp, soi qc_final_review_2.txt.")
        else:
            print("[B3R] ✓ PASS")

    def b3g_regate(self, force=False):
        """B3G — ĐO LẠI GATE SỐ sau mọi lượt sửa LLM (B3Q tự sửa · B3S FIX · B3R FIX).

        Lỗ hổng đo thật Lane G ep01 2026-09-20: gate số chỉ chạy TRONG B3. Sau đó B3S FIX (Fable) thêm
        1.100 chữ cảnh báo y tế theo yêu cầu sol, B3R FIX thêm câu dẫn → bản cuối 7.811 chữ (+21%),
        thoại 43% (>40%), 1 dấu 、 cắt cụm — nhưng state ghi PASS vì không ai đo lại. Bước này:
        (1) gỡ 、 tất định, (2) DÀI → nén khúc về target (cùng trim_chunked của B3), (3) đo lại; còn
        lỗi → DỪNG như B3 (gate hỏng = dừng), --force-qc mới đi tiếp. Không sửa nội dung, chỉ số."""
        if self.skip("B3G", None):
            return
        sf = self.f("script.txt")
        text = sf.read_text(encoding="utf-8")
        goc = text
        text = ai_steps._go_cat_neu_ja(self.p, text)
        target = profiles.target_chars(self.p, self.minutes)
        bad, m = ai_steps.check(self.p, text, self.minutes)
        print(f"[B3G] đo lại sau sửa: {m['chars']:,} chữ ≈ {m['minutes']}' · phẩy/câu {m['comma_per_sentence']} · "
              f"thoại {m['dialogue_ratio']:.0%} · " + ("ĐẠT" if not bad else " | ".join(bad)))
        nen = False
        if any(b.startswith("DÀI") for b in bad):
            print(f"[B3G] DÀI → nén khúc về {target:,} chữ (giữ thoại, chỉ nén địa văn) …")
            try:
                new = ai_steps._go_cat_neu_ja(self.p, ai_steps.trim_chunked(self.p, text, target, self.minutes))
                nb, nm = ai_steps.check(self.p, new, self.minutes)
                if len(nb) <= len(bad) and nm["chars"] >= target * 0.88:
                    text, bad, m, nen = new, nb, nm, True
                    print(f"  → nhận bản nén: {nm['chars']:,} chữ, còn {len(nb)} lỗi")
                else:
                    print(f"  ⚠️ bản nén {nm['chars']:,} chữ / {len(nb)} lỗi không tốt hơn → giữ bản trước")
            except Exception as e:
                print(f"  ⚠️ nén hỏng ({type(e).__name__}: {e}) → giữ bản trước")
        if any(b.startswith("HỘI THOẠI") for b in bad):
            print(f"[B3G] HỘI THOẠI {m['dialogue_ratio']:.0%} → hạ về ≤{profiles.gate(self.p)['dialogue_ratio_max']:.0%} "
                  f"(reduce_dialogue: đổi thoại phụ sang địa văn, giữ câu đắt) …")
            try:
                new = ai_steps._go_cat_neu_ja(self.p, ai_steps.reduce_dialogue(self.p, text))
                nb, nm = ai_steps.check(self.p, new, self.minutes)
                if len(nb) < len(bad) or (len(nb) == len(bad) and nm["dialogue_ratio"] < m["dialogue_ratio"]):
                    text, bad, m = new, nb, nm
                    print(f"  → nhận bản hạ thoại: {nm['dialogue_ratio']:.0%}, {nm['chars']:,} chữ, còn {len(nb)} lỗi")
                else:
                    print(f"  ⚠️ hạ thoại không cải thiện ({nm['dialogue_ratio']:.0%}, {len(nb)} lỗi) → giữ bản trước")
            except Exception as e:
                print(f"  ⚠️ hạ thoại hỏng ({type(e).__name__}: {e}) → giữ bản trước")
        if text != goc:
            if not sf.with_suffix(".pre_b3g.txt").exists():   # giữ bản TRƯỚC B3G lần đầu, không ghi đè khi chạy lại
                sf.with_suffix(".pre_b3g.txt").write_text(goc, encoding="utf-8")
            sf.write_text(text, encoding="utf-8")
        self.done("B3G", chars=m["chars"], minutes=m["minutes"], gate=bad, nen=nen)
        if bad:
            print("  ✗ B3G GATE KHÔNG ĐẠT sau sửa:")
            for b in bad:
                print("     -", b)
            if not force:
                raise SystemExit("✗ B3G: kịch bản sau các lượt sửa QC không qua gate số → DỪNG (sửa tay hoặc --force-qc).")
        print("[B3G] ✓ ĐẠT")

    def b4_voice(self):
        out = self.f("voice.mp3")
        if self.skip("B4", out):
            return
        self.kiem_lock("B4")    # đọc giọng cho đúng bản script đã khoá (máy 2 chạy B4 sau máy 1 nhiều ngày)
        # Lane ĐA GIỌNG (voice.provider="voicevox", Lane K 2026-09-24): mỗi câu đọc bằng giọng của vai trong
        # vai.txt; SRT ghi thẳng từ độ dài thật từng câu (chữ = script) nên KHÔNG qua B4a nắn phụ đề.
        da_giong = profiles.da_giong(self.p)     # voicevox (Lane K) | ai33 (Lane L)
        if da_giong:
            cmd = pycmd("tts_voicevox.py", "--script", self.f("script.txt"), "--profile", self.p["id"],
                        "--out", out, "--vai", self.f("vai.txt"), "--chars", self.f("characters.json"))
        else:
            cmd = pycmd("tts.py", "--script", self.f("script.txt"), "--profile", self.p["id"],
                        "--out", out)
            vid, vfx, vsp = self.pick_voice()
            if vid:
                cmd += ["--voice", vid]
            if vfx:
                cmd += ["--fx", vfx]
            if vsp:
                cmd += ["--speed", str(vsp)]
        run(cmd, "B4 giọng + SRT")
        from tts import mp3_seconds
        sec = round(mp3_seconds(out), 1)
        # SỬA PHỤ ĐỀ CHO KHỚP KỊCH BẢN — phải làm TRƯỚC khi giãn nhịp, vì pace_audio dựng
        # voice_paced.srt từ chính voice.srt này.
        # Vì sao bắt buộc: voice.srt do server STT NGHE LẠI audio, không phải chữ gốc. Giọng đọc
        # đúng (đọc từ script) nhưng phụ đề cháy vào video thì sai. Đo thật tập
        # simbot2-vU5PWT2zLDs: 70 chỗ sai chữ + 517 dấu phẩy bị mất — trong đó
        # 終の棲家 (nơi an nghỉ cuối đời) thành 衆の成果, 冷たい澱 thành 冷たいヒレ.
        # Đây là lỗi CÂM: ảnh vẫn đẹp, tiếng vẫn hay, chỉ khán giả Nhật đọc phụ đề mới thấy sai.
        if self.f("voice.srt").exists() and self.f("script.txt").exists() and not da_giong:
            try:
                run(pycmd("srt_from_script.py", "--srt", self.f("voice.srt"),
                          "--script", self.f("script.txt")), "B4a phụ đề bám kịch bản")
            except SystemExit as e:
                # Không chặn cả tập vì phụ đề: giọng và ảnh vẫn dùng được, chỉ chữ kém chuẩn.
                print(f"  ! B4a không chạy được ({e}) → phụ đề giữ nguyên chữ STT")
        # GIÃN NHỊP cho giọng người già: chèn khoảng nghỉ sau mỗi câu + nghỉ dài khi chuyển đoạn,
        # dựng lại SRT từ độ dài đo được (KHÔNG atempo nên KHÔNG trôi phụ đề).
        v = self.p.get("voice", {}) or {}
        if v.get("pace", True):
            cmd = pycmd("pace_audio.py", "--audio", out, "--srt", self.f("voice.srt"),
                   "--script", self.f("script.txt"))
            for k, flag in (("pace_sentence", "--sentence"), ("pace_mid", "--mid"),
                            ("pace_para", "--para"), ("pace_target_hi", "--target-hi")):
                if v.get(k) is not None:
                    cmd += [flag, str(v[k])]
            run(cmd, "B4b giãn nhịp")
            pw = self.f("voice_paced.wav")
            if pw.exists():
                from qc_visual import probe
                sec = round(probe(pw).get("duration") or sec, 1)
        self.done("B4", seconds=sec, seconds_raw=round(mp3_seconds(out), 1),
                  paced=self.f("voice_paced.wav").exists())
        # char_rate trong profile đo bằng MẪU NGẮN (~230 chữ) nên hơi nhanh hơn thật: mẫu không có
        # quãng nghỉ giữa đoạn. Đo lại bằng CẢ video rồi kéo profile về phía số thật (trung bình động
        # 70/30) → càng chạy càng đúng, các tập sau ước lượng độ dài sát hơn.
        raw = self.f("script.txt").read_text(encoding="utf-8")
        chars = len("".join(raw.split()))
        real = chars / (sec / 60)
        # Quy số đo về TỐC ĐỘ CHUẨN của hồ sơ trước khi ghi lại. Tập này có thể đọc 0.90 (cụ già)
        # hay 1.00 (người trẻ); ghi thẳng số đo vào hồ sơ là để tốc độ của MỘT tập kéo lệch số
        # đo chung của cả kênh, các tập sau ước lượng sai độ dài theo.
        goc = profiles.char_rate_speed(self.p)
        if self.ep_speed and goc and abs(self.ep_speed - goc) > 1e-6:
            quy_doi = real * goc / self.ep_speed
            print(f"  [char_rate] tập này đọc {self.ep_speed} (hồ sơ chuẩn {goc}) → "
                  f"quy đổi {real:.1f} về {quy_doi:.1f}")
            real = quy_doi
        cur = profiles.char_rate(self.p)
        if sec > 300 and abs(real - cur) / cur > 0.015:
            # Lệch NHỎ = nhiễu giữa các tập → nhích nhẹ (70/30). Lệch LỚN (>8%) = thay đổi HỆ THỐNG
            # (vd bật giãn nhịp làm video dài thêm 15%) → phải bám số đo, không thì bò mất mấy tập
            # mới tới nơi mà tập nào cũng bị B4Q chặn (đo thật ep11: 313,1 → 302,5 trong khi thật 277,9).
            w = 0.3 if abs(real - cur) / cur <= 0.08 else 0.8
            new_rate = round(cur * (1 - w) + real * w, 1)
            print(f"  [char_rate] đo thật {real:.1f} vs profile {cur} → cập nhật {new_rate}")
            self.p.setdefault("voice", {})["char_rate"] = new_rate
            # Ghi rõ số này đo Ở TỐC ĐỘ NÀO, để tập sau đọc tốc độ khác còn quy đổi được.
            self.p["voice"]["char_rate_speed"] = goc or self.ep_speed or 0.95
            self.p["voice"].pop("char_rate_note", None)     # đã đo thật, bỏ nhãn "CHƯA ĐO"
            self.p["voice"]["char_rate_measured_at"] = time.strftime("%Y-%m-%d")
            self.p["voice"]["char_rate_from"] = f"video thật {self.slug}"
            # Cho vòng ngoài biết char_rate vừa đổi → đáng viết lại kịch bản một lượt nữa.
            self.rate_fixed = abs(new_rate - cur) / cur > 0.05
            try:
                profiles.save(self.p)
            except Exception as e:
                print(f"  (không ghi được profile: {e})")

    def b4q_qc(self, force=False):
        """QC GIỌNG, hai tầng:

        1. SRT (server sinh từ chính file mp3) có phủ hết kịch bản không — bắt lỗi TTS đọc
           thiếu/bị cắt, thứ CÂM LẶNG vì mp3 vẫn có và nghe vẫn xuôi.
        2. Soi thẳng SÓNG ÂM (`qc_audio`) — bắt lỗi về NHỊP mà tầng 1 mù hoàn toàn: nghỉ đặt
           giữa câu, chết tiếng, rụng đoạn, vỡ tiếng, phụ đề lệch. Tập simbot2-vU5PWT2zLDs có
           52 chỗ nghỉ giữa câu mà vẫn phủ 95% kịch bản → mọi cổng cũ đều báo ĐẠT.
        """
        if self.skip("B4Q", None):
            return
        sec = (self.state.get("B4", {}) or {}).get("seconds") or 0
        r = qc_visual.qc_voice(self.f("script.txt"), self.voice_srt(), sec, self.minutes)
        try:
            # Kênh KHÔNG giãn nhịp (voice.pace=false) thì đừng đòi "≥1 chỗ nghỉ rõ mỗi phút" —
            # đó là luật của giọng cụ già, không phải luật chung.
            ra = qc_audio.qc_audio(self.voice_audio(), self.voice_srt(),
                                   doi_nghi=bool((self.p.get("voice", {}) or {}).get("pace", True)))
            r["problems"] += ra.get("problems", [])
            r["infra"] += ra.get("infra", [])
            r["nghe"] = {k: v for k, v in ra.items() if k not in ("problems", "infra")}
        except Exception as e:
            # QC không chạy được KHÁC với QC sạch — phải nói ra, đừng để "0 vấn đề" thành số ảo.
            r["infra"].append(f"qc_audio không chạy được: {type(e).__name__} {e}")
        n = qc_visual.report("B4Q GIỌNG + SRT + NGHE", r)
        if r.get("nghe"):
            g = r["nghe"]
            print(f"  nghe: nói {g.get('speak_ratio', 0):.0%} · {g.get('pauses', 0)} chỗ nghỉ "
                  f"({g.get('pauses_per_min', 0)}/phút) · nghỉ sai chỗ {g.get('pause_misplaced', 0)} "
                  f"· rụng đoạn {g.get('dropouts', 0)} · đỉnh {g.get('peak_db')} dB")
        self.done("B4Q", coverage=r.get("coverage"), cues=r.get("cues"), problems=n,
                  nghe=r.get("nghe"))
        if n and not force:
            print("  Sửa: chạy lại '--from B4' (đọc lại), hoặc --force-qc nếu chấp nhận.")
            raise SystemExit("✗ B4Q: giọng/SRT có vấn đề → DỪNG trước khi tiêu tiền ảnh.")

    def b5q_qc(self, force=False, fix=True):
        """QC LOẠT ẢNH trước khi dựng: thiếu/hỏng/đen/trùng (máy) + soi mẫu bằng vision."""
        if self.body_mode() == "stock_clips":
            # Không có loạt ảnh AI để chấm. Kho tư liệu đã được kiểm số lượng ở B5, còn chất lượng
            # từng cảnh do stock_cut.py bảo đảm (bỏ file <2s, cấm lặp gần, cắt tránh viền đen).
            print("[B5Q] lane clip stock → không có ảnh AI để chấm, bỏ qua")
            self.done("B5Q", skipped="stock_clips")
            return
        if self.skip("B5Q", None):
            return
        pf = self.f("img_prompts.txt")
        prompts = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]             if pf.exists() else []
        wf = self.f("world.txt")
        world = wf.read_text(encoding="utf-8") if wf.exists() else ""
        sample = int((self.p.get("image", {}) or {}).get("qc_sample", 12))
        r = qc_visual.qc_images(self.f("img"), prompts, world, sample)
        n = qc_visual.report("B5Q LOẠT ẢNH", r)
        # Ảnh mẫu nào hỏng (không khớp prompt / tay chân dị dạng) → XOÁ rồi gen lại đúng những
        # ảnh đó (gen_images tự bỏ qua ảnh đã có), sau đó QC lại chính chúng. Chỉ 1 lượt.
        # Vẽ lại tối đa 2 LƯỢT: méo tay/mặt là ngẫu nhiên theo từng lần sinh nên lượt 2 thường gỡ
        # được phần còn lại (đo thật ep12: 5 → 3 sau 1 lượt). Ảnh nào vẫn méo sau lượt 1 thì sửa
        # luôn PROMPT — thủ phạm hầu như luôn là tả cận cảnh bàn tay/ngón tay.
        for rnd in (1, 2):
            bad = [nm for nm, _, _ in (r.get("vision_bad") or [])]
            if not (bad and fix and not r["infra"]):
                break
            print(f"[B5Q] vẽ lại {len(bad)} ảnh hỏng (lượt {rnd}/2): {', '.join(bad)}")
            if rnd == 2:
                prompts = self._soften_hands(prompts, bad)
            for nm in bad:
                (self.f("img") / nm).unlink(missing_ok=True)
            n_face = sum(1 for l in prompts if l.lower().lstrip().startswith(("@ref", "@cast:")))
            run(self.gen_cmd(self.f("img_prompts.txt"), self.f("img"), n_face), "B5Q vẽ lại ảnh")
            r2 = qc_visual.qc_images(self.f("img"), prompts, world, sample)
            n2 = qc_visual.report(f"B5Q LOẠT ẢNH (sau khi vẽ lại lượt {rnd})", r2)
            print(f"  [vẽ lại] ảnh hỏng {len(bad)} → {len(r2.get('vision_bad') or [])}")
            r, n = r2, n2
        self.f("qc_images.json").write_text(json.dumps(r, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
        self.done("B5Q", images=r.get("n"), problems=n, vision_bad=len(r.get("vision_bad") or []))
        hard = [p for p in r["problems"] if "thiếu" in p or "HỎNG" in p or "TRÙNG" in p]
        if (hard or r["infra"]) and not force:
            raise SystemExit("✗ B5Q: loạt ảnh có lỗi nặng → DỪNG trước khi dựng video.")

    # ---------- B9: gói đăng tải
    def _chuong_theo_marker(self, cues):
        """Mốc chương lấy từ CHÍNH LỜI ĐỌC, không chia đều theo thời gian.

        Kênh nào đọc rõ "第1章…第5章" thì mốc chương trong mô tả PHẢI trùng với lúc người dẫn
        nói ra. Bản chia đều đo thật ở tập này ra 7 mốc và LLM đặt tên 第1章…第7章 — nghĩa là mô tả
        ghi 第4章 ở 12:39 trong khi video nói 第4章 ở 19:31. Người xem bấm vào là thấy sai ngay,
        và đó đúng là nhóm khán giả soi kỹ nhất của ngách này.

        Trả [(giây, tên chương thật)] — tên lấy nguyên dòng tiêu đề chương trong kịch bản.
        """
        marks = (profiles.gate(self.p).get("chapter_markers") or [])
        if not marks or not cues:
            return []
        # Tên chương đầy đủ lấy từ kịch bản (SRT bị cắt vụn nên tên hay mất chữ).
        ten = {}
        for dong in self.f("script.txt").read_text(encoding="utf-8").splitlines():
            d = dong.strip()
            for m in marks:
                if d.startswith(m):
                    ten[m] = d[:60]
        out = []
        for m in marks:
            cue = next((c for c in cues if m in c[2].replace(" ", "")), None)
            if cue:
                out.append((cue[0], ten.get(m, m)))
        if not out:
            return []
        # Chương đầu của YouTube BẮT BUỘC ở 0:00 → thêm phần mở đầu (hook) làm chương 0.
        if out[0][0] > 10:
            out.insert(0, (0.0, "導入" if self.p.get("language") == "ja" else "Mở đầu"))
        else:
            out[0] = (0.0, out[0][1])
        return out if len(out) >= 3 else []

    def _chuong(self, cues, so_chuong):
        """[(giây, lời mẫu)] chia đều theo THỜI GIAN THẬT của bản đọc.

        Luật chương của YouTube: mốc ĐẦU phải là 0:00, phải có ÍT NHẤT 3 chương, mỗi chương dài
        tối thiểu 10 giây. Sai một điều là YouTube bỏ qua TOÀN BỘ chương chứ không báo lỗi.
        """
        if not cues:
            return []
        tong = cues[-1][1]
        buoc = tong / so_chuong
        out, moc = [], 0
        for i in range(so_chuong):
            t = 0.0 if i == 0 else i * buoc
            phan = [c for c in cues if t <= c[0] < t + buoc]
            if not phan:
                continue
            if out and phan[0][0] - out[-1][0] < 10:      # quá sát chương trước → gộp vào
                continue
            out.append((0.0 if i == 0 else phan[0][0], " ".join(c[2] for c in phan[:6])))
        if out:
            out[0] = (0.0, out[0][1])                     # ép chương đầu về 0:00
        return out if len(out) >= 3 else []

    def _kiem_thumb(self):
        """Ảnh bìa có đúng chuẩn YouTube không: ≥1280×720, tỉ lệ 16:9, dưới 2 MB."""
        p = self.f("thumbnail_final.png")
        if not p.exists():
            return "CHƯA CÓ ảnh bìa"
        mb = p.stat().st_size / 1e6
        try:
            from PIL import Image
            w, h = Image.open(p).size
        except Exception:
            return f"{p.name} ({mb:.1f} MB) — không đọc được kích thước"
        loi = []
        if w < 1280 or h < 720:
            loi.append(f"nhỏ hơn 1280x720 (đang {w}x{h})")
        if abs(w / h - 16 / 9) > 0.02:
            loi.append(f"không phải 16:9 (đang {w}x{h})")
        if mb > 2:
            loi.append(f"nặng hơn 2 MB ({mb:.1f} MB) — YouTube sẽ từ chối")
        return f"{p.name} — {w}x{h}, {mb:.1f} MB" + (" · ⚠ " + "; ".join(loi) if loi else " · ĐẠT")

    def _b9_short_desc(self, titles, tags, dong_ch, hashtags, kit):
        """Sinh TIEU_DE_MO_TA.txt — đúng quy cách user chốt 2026-09-10: 1 khối DÁN THẲNG vào ô
        mô tả YouTube, KHÔNG chia mục/checklist như DANG-TAI.txt (file đó vẫn giữ nguyên cho phần
        còn lại — tags đầy đủ/danh mục/ngôn ngữ/việc phải tự chọn trong form).

        Thứ tự cố định: Tiêu đề → 5 từ khoá SEO (nối bằng dấu phẩy, KHÔNG cách) → mô tả ngắn →
        gạch ngang → "Timestamps:" + mốc thời gian → gạch ngang → câu cảm ơn → gạch ngang →
        hashtag. Không tuỳ biến theo profile — đây là 1 quy cách CỐ ĐỊNH áp cho mọi kênh/ngôn ngữ,
        chỉ nội dung bên trong đổi theo ngôn ngữ đích của kênh."""
        if not titles:
            return
        GACH = "-" * 100
        tu_khoa = ",".join((tags or [])[:5])
        mo_ta = (kit.get("description") or "").strip()
        cam_on = (kit.get("loi_cam_on") or "").strip()
        L = [titles[0], "", tu_khoa, "", mo_ta, "", GACH, "Timestamps:", "", "\n".join(dong_ch),
             GACH, "", cam_on, "", GACH, " ".join(hashtags)]
        self.f("TIEU_DE_MO_TA.txt").write_text("\n".join(L), encoding="utf-8")

    def b10_nghiem_thu(self, force=False):
        """B10 — NGHIỆM THU TOÀN TẬP: soi GÓI GIAO, không chỉ file MP4.

        B8Q chỉ hỏi "bản ghép có ổn không". B10 hỏi "**bộ này đăng lên được chưa**": ảnh bìa có
        vượt trần 2 MB của YouTube không · tiêu đề có nằm trong dải đã đo của ngách không · mô tả
        và thẻ có vượt trần không · mốc chương có đúng luật không (sai là YouTube **bỏ hết chương**
        mà không báo) · phụ đề đã CHÁY vào hình chưa · sổ nguồn có đủ file đã dùng không · B3F còn
        lỗi nặng không.

        Tất cả tất định, miễn phí. Chạy CUỐI CÙNG vì nó cần mọi thứ đã có mặt.
        """
        if self.skip("B10", None):
            return
        kq = qc_final.kiem(self.dir, self.p["id"])
        n = qc_final.bao_cao(kq)
        self.f("qc_final.json").write_text(
            json.dumps(kq, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        self.done("B10", findings=n, heavy=len(kq["nang"]))
        if kq["nang"] and not force:
            raise SystemExit(f"✗ B10: {len(kq['nang'])} vấn đề NẶNG ở gói giao → chưa đăng được.")

    def b11_giao_hang(self):
        """B11 — gom ĐÚNG 3 file cần để đăng vào thư mục của kênh.

        Chạy SAU B10, không phải trước: thư mục giao hàng là nơi anh vào lấy để đăng, nên chỉ được
        có mặt bản ĐÃ NGHIỆM THU. B10 trượt thì SystemExit ở trên đã chặn, B11 không chạy tới.

        Lane nào không khai `publish.upload_channel` thì bỏ qua êm — không phải kênh nào cũng cần
        thư mục giao hàng riêng.
        """
        # B11 là bước DUY NHẤT không gọi `skip()` (cố ý: dựng lại video thì phải giao lại). Nhưng
        # vì vậy `--den` không với tới đây — chạy `--den B5K` xong nó vẫn nhảy vào dựng bản xem thử
        # rồi chết vì chưa có final.mp4, báo "exit 1" cho một lượt chạy thực ra đã xong việc.
        if self.den and STEPS.index("B11") > STEPS.index(self.den):
            return
        if self.only and self.only != "B11":       # `--only B7` cũng từng lọt xuống đây
            return
        pub = self.p.get("publish", {}) or {}
        if not pub.get("upload_channel"):
            return
        if self.dry:
            return
        # Bản xem thử tiếng Việt dựng TRƯỚC khi giao, vì giao hàng sẽ chép nó sang thư mục kênh.
        # Dựng lại khi nó CŨ HƠN final.mp4 — không thì dựng lại video xong vẫn giao kèm bản xem
        # của lần dựng trước, mà đây đúng là file dùng để soi "hình có khớp lời không".
        rv = self.f("review_vi.mp4")
        mp4 = self.f("final.mp4")
        cu = rv.exists() and mp4.exists() and rv.stat().st_mtime < mp4.stat().st_mtime - 1
        if pub.get("review_vi") and (not rv.exists() or cu):
            if cu:
                print("  ⚠️ review_vi.mp4 cũ hơn final.mp4 → dựng lại bản xem thử")
            run(pycmd("ban_xem_viet.py", "--slug", self.f(""), "--profile", self.p["id"]),
                "B11a bản xem thử tiếng Việt")
        run(pycmd("giao_hang.py", "--slug", self.f(""), "--profile", self.p["id"]),
            "B11 giao hàng")
        # Ghi sổ — thiếu dòng này thì `--from` và bảng tổng kết cuối luôn báo "B11 chưa chạy"
        # dù đã giao xong, và lần chạy sau giao lại từ đầu.
        goc = Path(pub.get("upload_dir") or "") / str(pub.get("upload_channel"))
        self.done("B11", kenh=pub.get("upload_channel"), noi=str(goc))

    def b9_publish(self):
        """Sinh DANG-TAI.txt + TIEU_DE_MO_TA.txt — GIAO cho `publish_kit.py` (bản DÙNG CHUNG).

        `publish_kit.py` do lượt audit 2026-09-10 tách ra để tool não-Claude (`render_engine.py`)
        cũng sinh được gói đăng tải. Nó chép nguyên logic của make_video (kể cả `title.txt` thắng
        tiêu đề AI và mốc chương bám lời đọc). Giữ HAI BẢN chạy song song là mời drift: sửa một
        bên, bên kia âm thầm khác đi. Nên chỗ này gọi thẳng bản chung; các hàm `_chuong*`,
        `_b9_short_desc`, `_kiem_thumb` bên dưới CHỈ còn là dự phòng khi bản chung lỗi.
        """
        out = self.f("DANG-TAI.txt")
        if self.listing_external():
            if (self.only and self.only != "B9") or (self.den and STEPS.index("B9") > STEPS.index(self.den)):
                return
            if "B9" not in self.state:
                print("[B9] bỏ qua — publish.listing_external: tiêu đề/mô tả do dự án khác lo")
                self.done("B9", skipped="listing_external")
            return
        if self.skip("B9", out):
            return
        try:
            import publish_kit
            if publish_kit.build(self.dir, self.p["id"], self.minutes):
                self.done("B9", by="publish_kit")
                return
        except Exception as e:
            print(f"  ! publish_kit lỗi ({type(e).__name__} {e}) → dùng nhánh dự phòng trong file này")
        script_f, srt_f = self.f("script.txt"), self.voice_srt()
        if not script_f.exists():
            print("[B9] chưa có kịch bản → bỏ qua")
            return
        script = script_f.read_text(encoding="utf-8")
        cues = []
        if Path(srt_f).exists():
            import storyboard
            cues = storyboard.parse_cues(srt_f)
        # Ưu tiên mốc chương THẬT trong lời đọc; không có thì mới chia đều theo thời gian.
        ten_that = self._chuong_theo_marker(cues)
        if ten_that:
            secs = [(t, n) for t, n in ten_that]
            print(f"[B9] mốc chương lấy theo lời đọc: "
                  + " · ".join(f"{_mmss(t)} {n[:14]}" for t, n in ten_that))
        else:
            so = max(4, min(10, round((cues[-1][1] / 60 if cues else self.minutes) / 4)))
            secs = self._chuong(cues, so)
        kit = ai_steps.publish_kit(self.p, script, [(t, s) for t, s in secs] or
                                   [(0.0, script[:400])])
        if not kit:
            print("[B9] không sinh được gói đăng tải → bỏ qua (chạy lại: --only B9)")
            return
        titles = [t for t in (kit.get("titles") or []) if t][:3]
        # Tiêu đề đã chốt tay cho tập này (đúng công thức ngách: độ dài + khối tag SEO) thắng
        # mọi gợi ý của LLM. Không có file thì giữ nguyên như cũ.
        tf = self.f("title.txt")
        if tf.exists() and tf.read_text(encoding="utf-8").strip():
            chot = tf.read_text(encoding="utf-8").strip().splitlines()[0].strip()
            titles = [chot] + [t for t in titles if t != chot]
            print(f"[B9] tiêu đề CHỐT theo title.txt ({len(chot)} ký tự): {chot[:50]}")
        tags = [t for t in (kit.get("tags") or []) if t]
        # Thẻ YouTube tính TỔNG 500 ký tự (đã gồm dấu phẩy) — vượt là bị cắt cụt lặng lẽ.
        gon, do_dai = [], 0
        for t in tags:
            if do_dai + len(t) + 2 > 480:
                break
            gon.append(t)
            do_dai += len(t) + 2
        hashtags = [h if h.startswith("#") else "#" + h for h in (kit.get("hashtags") or [])][:8]
        # Có mốc chương thật thì DÙNG TÊN THẬT, đừng để LLM đặt lại — nó sẽ đánh số 第◯章 lệch
        # với số mà người dẫn đọc trong video.
        if ten_that:
            dong_ch = [f"{_mmss(t)} {n}" for t, n in ten_that]
        else:
            ten_ch = kit.get("chapters") or []
            dong_ch = [f"{_mmss(t)} {ten_ch[i] if i < len(ten_ch) else f'Phần {i+1}'}"
                       for i, (t, _) in enumerate(secs)]
        self._b9_short_desc(titles, tags, dong_ch, hashtags, kit)
        mo_ta = (kit.get("description") or "").strip()
        if dong_ch:
            mo_ta += "\n\n" + "\n".join(dong_ch)
        if hashtags:
            mo_ta += "\n\n" + " ".join(hashtags)
        srt_ten = Path(srt_f).name if Path(srt_f).exists() else "(chưa có)"
        L = [
            "=" * 78, f"GÓI ĐĂNG TẢI — {self.slug}", "=" * 78,
            "Copy từng khối bên dưới dán thẳng vào form tải lên của YouTube.", "",
            "-" * 78, "1) TIÊU ĐỀ  (chọn 1 — tối đa 100 ký tự)", "-" * 78,
        ]
        for i, t in enumerate(titles, 1):
            canh = "" if len(t) <= 100 else f"   ⚠ DÀI {len(t)} ký tự, phải cắt bớt"
            L.append(f"[{i}] {t}   ({len(t)} ký tự){canh}")
        L += ["", "-" * 78, "2) MÔ TẢ  (dán nguyên khối — đã gồm mốc chương + hashtag)", "-" * 78,
              mo_ta, "", f"   → {len(mo_ta)} ký tự" + (" ⚠ VƯỢT 5.000, phải cắt"
                                                       if len(mo_ta) > 5000 else " (tối đa 5.000)"),
              "", "-" * 78, "3) THẺ / TAGS  (dán cả dòng)", "-" * 78,
              ", ".join(gon), "", f"   → {len(', '.join(gon))} ký tự (tối đa 500)"
              + (f" · đã bỏ bớt {len(tags) - len(gon)} thẻ cho vừa" if len(gon) < len(tags) else ""),
              "", "-" * 78, "4) ẢNH BÌA", "-" * 78, "   " + self._kiem_thumb(),
              "", "-" * 78, "5) BÌNH LUẬN GHIM  (đăng xong thì dán rồi ghim lên đầu)", "-" * 78,
              (kit.get("pinned_comment") or "").strip(),
              "", "-" * 78, "6) CÁC MỤC PHẢI TỰ CHỌN TRONG FORM", "-" * 78,
              f"   Danh mục            : {kit.get('category') or 'People & Blogs'}",
              f"   Ngôn ngữ video      : {ai_steps.LANG_NAME.get(self.p.get('language','ja'), '')}",
              f"   Phụ đề              : tải file {srt_ten} lên (cùng thư mục này)",
              "   Dành cho trẻ em     : KHÔNG  ← bắt buộc trả lời, chọn sai là bị tắt bình luận",
              "   Nội dung do AI tạo  : CÓ — khai ở mục 'Nội dung tổng hợp/đã chỉnh sửa'.",
              "                         Giọng đọc là AI nên PHẢI khai; giấu là rủi ro gậy bản quyền.",
              "   Giới hạn độ tuổi    : không",
              "   Bình luận           : bật, sắp xếp theo 'Mới nhất'",
              "   Danh sách phát      : thêm vào playlist của kênh",
              "   Màn hình kết thúc   : gắn 1 video liên quan + nút đăng ký",
              "", "-" * 78, "7) TỰ KIỂM TRƯỚC KHI BẤM ĐĂNG", "-" * 78,
              "   [ ] Nghe lại 30 giây đầu — hỏng phần mở là mất hết lượt xem",
              "   [ ] Xem thumbnail ở cỡ NHỎ, chữ còn đọc được không",
              "   [ ] Tiêu đề khớp nội dung (câu view lố bị hạ đề xuất)",
              "   [ ] Đã khai nội dung AI",
              "   [ ] Đặt lịch đăng vào khung giờ khán giả của kênh online", "",
        ]
        out.write_text("\n".join(L), encoding="utf-8")
        print(f"[B9] gói đăng tải → {out.name} · {len(titles)} tiêu đề · {len(gon)} thẻ · "
              f"{len(dong_ch)} chương")
        print(f"      tiêu đề gợi ý: {titles[0] if titles else '(không có)'}")
        self.done("B9", titles=len(titles), tags=len(gon), chapters=len(dong_ch),
                  title=titles[0] if titles else "")

    def b8q_qc(self, force=False):
        """QC BẢN GHÉP: luồng/thời lượng/khung đen + ẢNH CÓ KHỚP LỜI ĐANG ĐỌC không."""
        if self.skip("B8Q", None):
            return
        # ĐO THẲNG file tiếng đang dùng, đừng tin số trong state: chạy lại '--from B8' sau khi
        # giãn nhịp thì state B4 còn giá trị CŨ → B8Q báo lệch 170s dù video hoàn toàn đúng.
        sec = qc_visual.probe(self.voice_audio()).get("duration") or             (self.state.get("B4", {}) or {}).get("seconds") or 0
        srt = self.voice_srt()
        sample = int((self.p.get("assemble", {}) or {}).get("qc_sample", 12))
        # ⚠️ CHỖ NÀY TỪNG CỐ Ý BỎ QUA PHÉP KIỂM QUAN TRỌNG NHẤT — ĐỪNG KHÔI PHỤC.
        # Bản cũ ghi: "lane clip stock: hình là B-roll trang trí, CỐ Ý không minh hoạ lời đang
        # đọc → chấm khớp lời là chấm sai đề", rồi truyền srt=None. Giả định đó SAI, và vì nó nằm
        # trong cổng nên không ai phát hiện: tập 3 đi hết pipeline với **43/141 cảnh (30%) lạc
        # hẳn lời**, B8Q báo 0 vấn đề, chủ dự án xem 5 phút là thấy. Kênh mẫu dùng b-roll không
        # khớp TỪNG CHỮ, nhưng không bao giờ để cảnh phụ nữ gõ máy tính văn phòng lên đoạn kể vụ
        # bắt giữ năm 1990.
        # Lane stock nay chấm bằng `qc_canh.py` — soi TỪNG cảnh chứ không lấy mẫu 12 mốc (12/400
        # mốc = 3%, một video hỏng 30% vẫn có ~2% khả năng qua sạch… và nó đã qua sạch thật).
        if self.body_mode() == "stock_clips":
            return self.b8q_qc_canh(force)
        # want_sub theo ĐÚNG assemble.burn_subs của profile — video KHÔNG cháy phụ đề (mặc định dự
        # án từ 2026-09-11, .srt giao riêng làm CC) thì đừng chấm "thiếu phụ đề" oan. `qc_visual.py`
        # CLI đã có `--no-sub` từ trước nhưng lệnh gọi thư viện này quên truyền, nên 1 lane ai_images
        # đầu tiên dùng burn_subs=false (kenko-chiebukuro) mới lộ ra — không lane nào khác dính vì
        # satori/toshi trước đó không đi qua đúng nhánh này với burn_subs=false.
        r = qc_visual.qc_video(self.f("final.mp4"), srt if srt.exists() else None, sec, sample,
                               want_sub=self.chay_phu_de(), voice=self.voice_audio())
        n = qc_visual.report("B8Q VIDEO HOÀN CHỈNH", r)
        self.f("qc_video.json").write_text(json.dumps(r, ensure_ascii=False, indent=1),
                                           encoding="utf-8")
        self.done("B8Q", sync_score=r.get("sync_score"), problems=n)
        if n and not force:
            print(f"  Chi tiết: {self.f('qc_video.json')}")
            raise SystemExit("✗ B8Q: bản ghép có vấn đề (xem danh sách trên).")

    def b8q_qc_canh(self, force=False):
        """B8Q của lane stock: soi TỪNG CẢNH — hình có thuộc về khoảnh khắc này của lời không.

        Ngưỡng `assemble.lac_toi_da` là TỈ LỆ cảnh được phép lạc. Đặt 0 thì mỗi lần dựng lại là
        một vòng cấm file + vẽ ảnh, không bao giờ dừng — vì bộ chấm cũng chặt tay ở vài cảnh đúng
        (sân trường có người đi bộ trong đoạn kể học bạ). 3% là mức đo được sau 4 vòng sửa ở tập 3.
        """
        import qc_canh
        sc = self.f("scenes.json")
        srt = self.voice_srt()
        if not sc.exists():
            print("[B8Q] chưa có scenes.json → bỏ qua chấm từng cảnh")
            return
        run(pycmd("qc_canh.py", "--video", self.f("final.mp4"), "--scenes", sc,
                  "--srt", srt, "--cam-file-lac", self.kho_stock()), "B8Q chấm từng cảnh",
            cho_loi=True)
        ds = json.loads(self.f("qc_canh.json").read_text(encoding="utf-8"))
        cham = [x for x in ds if x.get("muc") is not None]
        ha_tang = [x for x in ds if x.get("loi_ha_tang")]
        lac = [x for x in cham if x["muc"] == 0]
        ty = len(lac) / max(len(cham), 1)
        toi_da = float((self.p.get("assemble", {}) or {}).get("lac_toi_da", 0.03))
        print(f"[B8Q] {len(cham)}/{len(ds)} cảnh chấm được · lạc {len(lac)} ({ty:.1%}, "
              f"trần {toi_da:.0%})" + (f" · ⚠️ {len(ha_tang)} lỗi hạ tầng" if ha_tang else ""))
        for x in lac[:10]:
            print(f"    {x['t0']:7.1f}s {x['file'][:30]:30s} {x.get('ta', '')[:34]}")
        self.done("B8Q", canh=len(ds), lac=len(lac), ty_le_lac=round(ty, 4),
                  infra=len(ha_tang))
        # "0 lỗi" khi QC không chạy được là SỐ ẢO — hạ tầng hỏng thì KHÔNG được coi là đạt.
        if (ty > toi_da or ha_tang) and not force:
            raise SystemExit(f"✗ B8Q: {len(lac)} cảnh lạc lời ({ty:.1%} > {toi_da:.0%}). "
                             f"Cấm file đã ghi vào soi_kho.json — chạy lại B5A rồi B8.")

    def gen_cmd(self, pf, imgdir, n_face, sheet=""):
        """Lệnh gen ảnh — dùng chung cho B5 (gen lần đầu) và B5Q (vẽ lại ảnh hỏng).
        3 key gpti2 xoay round-robin theo chỉ số ảnh → 8 luồng/key = 24 luồng."""
        img = self.p.get("image", {}) or {}
        cmd = pycmd("gen_images.py", "--prompts", pf, "--out", imgdir,
               "--quality", img.get("ref_quality", "low"),
               "--workers", str(self.img_workers or int(img.get("workers", 24))))
        if n_face and img.get("ref_lock"):
            if self.characters_from_bible() and self.cast_mode():
                self.masters_from_bible()                 # vẽ đủ _ref_<id>/001.png cho mọi nhân vật ref:true
                cmd += ["--cast-root", self.dir]
            elif self.characters_from_bible():
                m1, m2 = self.masters_from_bible()
                cmd += ["--ref", m1]
                if m2:
                    cmd += ["--ref2", m2]
            else:
                cmd += ["--ref", self.master_portrait(sheet or img.get("character_sheet", ""))]
        return cmd

    def masters_from_bible(self):
        """Master REF-LOCK của TỪNG nhân vật trong characters.json (khuôn qc_character.py:
        {"characters":[{name, age, gender:"M"/"F", look, ref_marker:"@REF"/"@REF2", master:"_ref/001.png"}]}).
        Thiếu ảnh master → vẽ (gpti2 medium, nền xám trơn, style của lane) → QC tuổi/giới bằng vision
        (qc_character.py --img) tối đa 2 lượt. @REF và @REF2 ĐỘC LẬP (khác thư mục, khác prompt) →
        vẽ+QC SONG SONG (2 luồng) thay vì lần lượt — đo thật 2026-09-21: 6 master (3 tập) tuần tự mất
        ~3,5' dù gpti2 cho 24 luồng, vì mỗi lượt `run()` chỉ gửi ĐÚNG 1 ảnh (workers=24 vô dụng khi có
        1 ảnh/lượt gọi) — sự lãng phí nằm ở việc GỌI TUẦN TỰ, không phải ở worker count. Trả
        (master_@REF, master_@REF2 | None)."""
        cf = self.f("characters.json")
        if not cf.exists():
            raise SystemExit("✗ image.characters_from_bible=true nhưng thiếu characters.json (lớp 1 viết trước B5W)")
        data = json.loads(cf.read_text(encoding="utf-8"))
        chars = data.get("characters") or []
        cast = self.cast_mode()
        # Lane K (2026-09-24): hồ sơ kiểu mới {id, ref:true} → mỗi nhân vật 1 thư mục _ref_<id>, số lượng tuỳ tập.
        can_ve = ([c for c in chars if c.get("ref")] if cast
                  else [c for c in chars if c.get("ref_marker") in ("@REF", "@REF2")])

        def _lam(c):
            mk = c["id"] if cast else c["ref_marker"]
            sub = f"_ref_{c['id']}" if cast else ("_ref" if mk == "@REF" else "_ref2")
            master = self.f(c.get("master") or f"{sub}/001.png")
            if master.exists():
                return mk, master
            # Lane L (2026-09-24): nhân vật XUYÊN TẬP (Sakura) khoá bằng 1 ảnh gốc CỦA LANE — image.fixed_refs
            # {id: đường dẫn từ gốc dự án}. Chép vào _ref_<id>/001.png của tập → mọi bước sau (gen_images
            # --cast-root, đóng gói máy 2, Flow Tool) chạy y như master của tập, không vẽ mặt mới.
            goc = ((self.p.get("image") or {}).get("fixed_refs") or {}).get(c.get("id"))
            if cast and goc:
                src = HERE.parent / goc
                if not src.exists():
                    raise SystemExit(f"✗ image.fixed_refs[{c['id']}] trỏ tới {src} nhưng không có file")
                master.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, master)
                c["master"] = str(master.relative_to(self.dir)).replace("\\", "/")
                print(f"  ✓ master {c['id']}: ảnh gốc của lane ({goc})")
                return mk, master
            mp = self.f(f"master_prompt_{c['id']}.txt" if cast else f"master_prompt{'' if mk == '@REF' else '2'}.txt")
            # ⚠️ KHÔNG dùng chữ "character reference sheet": gpti2 vẽ ra BẢNG NHIỀU Ô (front/side/biểu cảm), rồi mọi ảnh
            # @REF edit từ master đó cũng thành trang manga nhiều ô (đo thật ep01 Lane G 2026-09-21: 6/14 ảnh mẫu là collage).
            # ⚠️ style_suffix của lane thường có cụm "everyday Japanese settings: living room, bank
            # counter…" (cho ẢNH CẢNH) — nếu chỉ nối vào cuối, model gpti2 đọc thấy mô tả PHÒNG cụ
            # thể ở gần cuối prompt nên VẼ THEO ĐÓ thay vì "plain grey background" đã dặn phía trước
            # (đo thật 2026-09-21: 4/6 master của Lane F dính nền phòng khách dù prompt có "plain
            # light-grey studio background"). Thêm câu ĐÈ LẠI sau cùng — model ưu tiên chỉ dẫn gần
            # cuối, nên câu chốt phải là câu MẠNH NHẤT, không phải câu nêu bối cảnh chung của lane.
            mp.write_text(
                f"ONE single full-frame picture, exactly ONE person, medium bust portrait: {c.get('look')}. Neutral calm "
                f"expression, facing camera, even soft lighting, plain light-grey studio background, no text, no panels, "
                f"no grid, no multiple views. "
                f"{(self.p.get('image') or {}).get('style_suffix', '')} "
                f"IMPORTANT override for THIS portrait only: IGNORE any specific room/scene/setting mentioned above — "
                f"the background MUST stay a single flat plain light-grey studio backdrop, no furniture, no windows, "
                f"no room details of any kind.", encoding="utf-8")
            for k in range(2):
                run(pycmd("gen_images.py", "--prompts", mp, "--out", master.parent, "--quality", "medium"),
                    f"B5.0 master {c.get('name')} ({mk})")
                if self.dry or self._master_ok(master, c):
                    break
                if k == 0:
                    print(f"  ↻ master {c.get('name')} lệch tuổi/giới → vẽ lại 1 lần")
                    master.unlink(missing_ok=True)
            c["master"] = str(master.relative_to(self.dir)).replace("\\", "/")
            return mk, master

        out = {}
        with ThreadPoolExecutor(max_workers=max(1, len(can_ve))) as ex:
            for mk, master in ex.map(_lam, can_ve):
                out[mk] = master
        cf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        if cast:
            if not out:
                raise SystemExit("✗ characters.json không có nhân vật nào ref:true")
            return out
        if "@REF" not in out:
            raise SystemExit("✗ characters.json không có nhân vật ref_marker=\"@REF\"")
        return out["@REF"], out.get("@REF2")

    def _master_ok(self, master, c):
        """QC 1 ảnh master bằng qc_character (vision, ramclouds). Lỗi hạ tầng → coi là đạt tạm, có in cảnh báo."""
        try:
            r = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "qc_character.py"), "--img", str(master),
                                "--age", str(int(c.get("age") or 0)), "--gender", str(c.get("gender") or "M")[:1].upper()],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300,
                               env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            if r.returncode not in (0, 2):
                print(f"  (QC master crash exit {r.returncode}: {(r.stderr or '')[-200:]!r} → dùng tạm, KHÔNG coi là đạt)")
                return True
            print(("  " + (r.stdout or "").strip().replace("\n", "\n  "))[:600])
            if r.returncode != 0:
                print(f"  ⚠️ master {c.get('name')}: QC báo lệch (exit {r.returncode})")
                return False
            return True
        except Exception as e:
            print(f"  (QC master không chạy được: {type(e).__name__} {e} → dùng tạm, KHÔNG coi là đạt)")
            return True

    # ---------- 4 field mới (Lane G, anh duyệt 2026-09-20 — docs/PHUONG_AN_LANE_G_BUOC2_3.md C1–C4).
    # Lane không khai → mọi hàm trả False → nhánh cũ y nguyên (hàng rào #2: khác biệt CHỈ qua field profile).
    def prompts_by_fable_doan(self):
        """image.prompts_by == "fable_doan": Fable viết prompt theo ĐOẠN + img_doan.txt (prompt_doan.py)."""
        return ((self.p.get("image", {}) or {}).get("prompts_by") or "").lower() == "fable_doan"

    def cast_mode(self):
        """characters.json kiểu MỚI (Lane K 2026-09-24): nhân vật có `id` + `ref` (không `ref_marker`) → khoá mặt
        N nhân vật/tập, prompt ảnh dùng @CAST:id1,id2. File kiểu cũ (@REF/@REF2) → False, nhánh cũ y nguyên."""
        cf = self.f("characters.json")
        if not cf.exists():
            return False
        try:
            chars = json.loads(cf.read_text(encoding="utf-8")).get("characters") or []
        except Exception:
            return False
        return bool(chars) and all("id" in c and "ref" in c and not c.get("ref_marker") for c in chars)

    def characters_from_bible(self):
        """image.characters_from_bible: master REF-LOCK lấy từ characters.json (nhiều nhân vật/tập)."""
        return bool((self.p.get("image", {}) or {}).get("characters_from_bible"))

    def sync_anchors(self):
        """assemble.sync == "anchors": B8 neo ảnh theo câu (sinh_neo.py → anchors.txt) thay vì chia theo số đếm."""
        return ((self.p.get("assemble", {}) or {}).get("sync") or "").lower() == "anchors"

    def listing_external(self):
        """publish.listing_external: tiêu đề/mô tả/thumbnail do DỰ ÁN KHÁC lo → bỏ B7/B9, B10/B11 không đòi."""
        return bool((self.p.get("publish", {}) or {}).get("listing_external"))

    def sample_gate(self):
        """image.sample_gate=N (C2, docs/PHUONG_AN_LANE_F_BUOC2_3.md): trước khi vẽ cả loạt, vẽ N
        ảnh mẫu rồi QC vision (khớp prompt + KHÔNG collage/nhiều ô) — bắt lỗi KIỂU ẢNH hệ thống
        sớm. 0/thiếu = tắt (nhánh B5 cũ y nguyên)."""
        return int((self.p.get("image", {}) or {}).get("sample_gate") or 0)

    def body_mode(self):
        """Thân video dựng bằng gì: 'ai_images' (satori) hay 'stock_clips' (ngách kể tài liệu).

        Khai ở profile.body.mode. Đây là NGÃ RẼ DUY NHẤT giữa hai lane — mọi khác biệt còn lại
        (số ảnh, REF-LOCK, nhịp cắt) đã nằm trong profile, nên đừng thêm `if profile_id ==` ở
        bất cứ đâu khác.
        """
        return (self.p.get("body", {}) or {}).get("mode") or "ai_images"

    def chay_phu_de(self):
        """Có CHÁY phụ đề vào hình không. Mặc định KHÔNG (anh chốt 2026-09-11).

        Lý do: YouTube tự bật phụ đề khi người xem cần, và mình vẫn giao file .srt để tải lên làm
        CC — người xem bấm nút CC là có, đúng phụ đề của mình chứ không phải bản máy nghe. Khán giả
        Nhật nghe hiểu nên chữ cháy vào hình chỉ che mất hình.
        Cháy phụ đề là **không gỡ được**: muốn bỏ phải dựng lại cả video. Để nó ngoài file là giữ
        được quyền đổi.
        Bật lại cho một lane: `assemble.burn_subs = true` trong profile.
        """
        return bool((self.p.get("assemble", {}) or {}).get("burn_subs", False))

    def kho_stock(self):
        """Thư mục kho tư liệu cho TẬP NÀY.

        `body.stock_per_episode: true` ⇒ mỗi tập một kho riêng trong thư mục tập.
        Vì sao cần: `stock_cut.chon_nguon()` chọn clip theo "ít dùng nhất + ngẫu nhiên", KHÔNG hề
        đối chiếu nội dung clip với lời đọc. Kho dùng chung mà lẫn đề tài là cảnh thiên hà chạy
        dưới đoạn kể về một chiếc Cessna mất tích — sai mà pipeline không có cách nào biết.
        Kênh này mỗi tập một đề tài rời (vũ trụ, hàng không, biển) nên phải tách; lane nào các tập
        cùng một thế giới hình ảnh thì để `false` cho đỡ tải lại.
        """
        body = self.p.get("body", {}) or {}
        chung = ROOT / (body.get("stock_dir") or "assets/stock")
        if body.get("stock_per_episode"):
            rieng = self.f("stock")
            # Tập LÀM TRƯỚC khi bật `stock_per_episode` không có kho riêng — dựng lại nó mà cứ
            # trỏ vào thư mục rỗng là chết ở "không thấy kho tư liệu". Thiếu kho riêng thì lùi về
            # kho chung, đúng nơi tập đó vốn lấy hình.
            return rieng if rieng.exists() else chung
        return chung

    def b5_stock(self):
        """B5 của lane STOCK: bảo đảm kho tư liệu đủ dùng — KHÔNG gen ảnh AI nào.

        Ảnh AI ở lane này chỉ dùng cho THUMBNAIL (B7). Thân video là clip công cộng, chi phí ~0.
        """
        if self.skip("B5", None):
            return
        body = self.p.get("body", {}) or {}
        cuts = body.get("cuts_per_min") or [12, 16]
        n_canh = int(self.minutes * (sum(cuts) / 2))
        reuse = int(body.get("reuse_max") or 6)
        stock = self.kho_stock()
        qf = self.f("stock_queries.txt")
        if qf.exists():
            qs = [q.strip() for q in qf.read_text(encoding="utf-8").splitlines()
                  if q.strip() and not q.startswith("#")]
            print(f"[B5] tải tư liệu theo {len(qs)} từ khoá trong stock_queries.txt …")
            for q in qs:
                # Một truy vấn hỏng KHÔNG được giết cả lượt chạy: nguồn ngoài chập chờn là
                # chuyện thường (Pexels 429, Wikimedia chặn IP), mà 1/29 truy vấn lỗi thì kho
                # vẫn thừa sức dùng. Cổng thật nằm ngay dưới — `suc_chua()` đo kho có gánh nổi
                # số cảnh không; đó mới là câu hỏi đáng dừng lại.
                run(pycmd("stockfetch.py", "--q", q, "--n", "5",
                          "--sources", body.get("stock_sources") or "nasa,commons",
                          "--out", stock), f"B5 stock: {q[:40]}", cho_loi=True)
        # Kho vừa có file MỚI thì phải soi nội dung trước khi dựng, nếu không file lạc đề tài lại
        # lọt vào video đúng như tập 3. `soi_kho.py` bỏ qua file đã chấm nên chỉ trả tiền cho phần
        # mới.
        if stock.exists() and (stock / "manifest.jsonl").exists():
            run(pycmd("soi_kho.py", "--stock", stock), "B5 soi nội dung kho", cho_loi=True)
        import stock_cut
        vids, stills = stock_cut.nap_kho(stock) if stock.exists() else ([], [])
        co = len(vids) + len(stills)
        chua = stock_cut.suc_chua(vids, stills, reuse)
        print(f"[B5/stock] cần ~{n_canh} cảnh · kho {co} file ({len(vids)} clip + {len(stills)} ảnh) "
              f"gánh được {chua} cảnh")
        if chua < n_canh:
            print(f"  Thiếu sức chứa {n_canh - chua} cảnh. Bổ sung: py -3.13 stockfetch.py "
                  f"--q \"<từ khoá EN>\" --n 6 --out {stock}")
            if not self.dry:
                raise SystemExit("✗ B5: kho tư liệu chưa đủ → DỪNG (dựng bằng kho mỏng sẽ lặp hình).")
        self.done("B5", mode="stock_clips", files=co, videos=len(vids), stills=len(stills),
                  scenes_planned=n_canh, capacity=chua, cost_vnd=0)

    def b5k_khop_hinh(self):
        """B5K — nối LỜI ĐỌC với TỪ KHOÁ HÌNH theo từng đoạn ~15 giây.

        Không có bước này thì `stock_cut.chon_nguon()` chọn clip theo "file nào ít dùng nhất, đủ
        dài, chưa dùng gần đây" — **nội dung clip không tham gia vào quyết định**. Đo thật tập 3
        trước khi có B5K: 43/141 cảnh (30%) lạc hẳn lời đang đọc.
        Chạy sau B4a (đã có .srt bám kịch bản) và trước B5A: B5A cần biết đoạn nào nói tới vật thể
        cụ thể thì mới biết phải vẽ gì.
        """
        if self.body_mode() != "stock_clips" or self.skip("B5K", self.f("khop_hinh.json")):
            return
        run(pycmd("khop_hinh.py", "--slug", self.dir, "--profile", self.p["id"]), "B5K khớp hình")
        ds = json.loads(self.f("khop_hinh.json").read_text(encoding="utf-8"))
        cu_the = sum(1 for x in ds if x.get("loai") == "CU_THE" and x.get("prompt"))
        self.done("B5K", doan=len(ds), cu_the=cu_the,
                  bat_dau_giay=round(ds[0]["t0"], 1) if ds else None)

    def b5a_anh_canh(self):
        """B5A — VẼ ẢNH cho những đoạn lời mà kho stock không phục vụ được.

        VÌ SAO KHÔNG THỂ CHỈ DỰA VÀO KHO
        ----------------------------------------------------------------------------------------
        Pexels là kho ảnh ĐỜI THƯỜNG. Tìm thứ nó không có thì nó vẫn trả về thứ gì đó, mình vẫn
        tải, vẫn ghi sổ, rồi B5K ghép **hoàn hảo vào một clip sai**. Đo thật tập 3: `area 51 sign
        nevada` ra phố Las Vegas, `japan military base fence gate` ra cổng torii đền thờ,
        `polygraph test machine` không có tấm nào đúng. Chấm lại cả kho bằng vision: 32% số file
        lạc hẳn đề tài.
        Chỉ vẽ đoạn `CU_THE` (có vật/nơi xác định). Đoạn `KHONG_KHI` để kho lo — clip thật bao giờ
        cũng hơn ảnh vẽ vì có chuyển động.
        Mọi ảnh vẽ đều mang nhãn 「イメージ（再現）」 (xem `stock_cut.gan_anh_ai`).
        """
        body = self.p.get("body", {}) or {}
        if self.body_mode() != "stock_clips" or not body.get("ai_fill_images", True):
            return
        if self.dry or self.skip("B5A", None):
            return
        # ẢNH ĐÃ NẰM SẴN TRONG THƯ MỤC THÌ KHÔNG VẼ LẠI — kể cả khi state chưa ghi B5A.
        # Đây là bẫy tiền thật của quy trình 3 bước (máy 2 vẽ ảnh, bước 3 chỉ ghép): bước 3 chạy
        # `--from B8`, mà B8 nằm SAU B5A nên `--from` không xoá B5A khỏi state — nhưng nếu state
        # chưa từng có B5A (vì máy 1 dừng ở `--den B5K` rồi ra đơn) thì `skip()` trả False và
        # bước này lặng lẽ gọi nhà cung cấp vẽ lại TOÀN BỘ ~300 tấm mà máy 2 vừa vẽ xong miễn phí
        # (~15.000đ/tập). Không có cổng nào kêu, vì xét theo state thì nó đang làm đúng việc.
        # Nguồn chân lý là ĐĨA, không phải state: có đủ file theo `img_meta.json` ⇒ đã có ảnh.
        meta = self.f("img_ai/img_meta.json")
        if meta.exists():
            try:
                ds = json.loads(meta.read_text(encoding="utf-8"))
            except Exception:
                ds = []
            ten = [r.get("file") for r in ds if r.get("file")]
            co = [t for t in ten if (self.f("img_ai") / t).exists()]
            if ten and len(co) == len(ten):
                print(f"[B5A] đã có đủ {len(co)}/{len(ten)} ảnh trong img_ai/ → KHÔNG vẽ lại")
                self.done("B5A", anh=len(co), nguon="co san tren dia", cost_vnd=0)
                return
            if ten and co:
                print(f"  ⚠️ img_ai/ mới có {len(co)}/{len(ten)} ảnh — THIẾU {len(ten)-len(co)} tấm. "
                      f"Đây là việc của bên vẽ ảnh, KHÔNG tự vẽ bù ở đây.")
                raise SystemExit("✗ B5A: thiếu ảnh so với img_meta.json → dừng, đòi đủ ảnh trước.")
        run(pycmd("sinh_anh_canh.py", "--slug", self.dir,
                  "--quality", body.get("ai_fill_quality") or "low"), "B5A vẽ ảnh theo cảnh")
        d = self.f("img_ai/img_meta.json")
        n = len(json.loads(d.read_text(encoding="utf-8"))) if d.exists() else 0
        self.done("B5A", anh=n, cost_vnd=n * 50)

    def b5w_write_prompts(self, sheet=""):
        """B5W — viết img_prompts.txt (NỘI DUNG + số lượng ảnh, do LLM quyết định ở Bước 1),
        KHÔNG gọi gen ảnh thật (không tốn tiền — đó là việc của B5 phía sau). Tách khỏi B5 để
        lane "chỉ làm kịch bản" dừng được đúng chỗ (`--den B5P`) mà vẫn có nội dung ảnh, đúng luật
        "cấm để bước 2/3 tự sinh nội dung, Bước 1 phải viết xong để lại thành file" (CLAUDE.md).

        2026-09-23 (vá review cuối, Việc 1+2 — nối hook_storyboard vào luồng bình thường): sau khi
        ghi xong tài sản của bước này, gọi thêm `self._sinh_hook_storyboard_neu_can()` — xem
        docstring của hàm đó để biết lý do đặt ĐÚNG ở đây (characters.json đã có ở điểm này) và các
        ràng buộc an toàn (không phá B5W nếu hook lỗi).
        """
        self._b5w_ghi_prompt(sheet)
        self._sinh_hook_storyboard_neu_can()

    def _sinh_hook_storyboard_neu_can(self):
        """2026-09-23 (vá review cuối, Việc 1+2): gọi `hook_storyboard.sinh()` ngay sau bước ghi
        tài sản (characters.json + prompt ảnh) để MỌI tập chạy luồng bình thường (lean_script.run →
        make_video.py) đều có đủ 5 file mà `docs/GIAO_VIEC_BUOC3_AGENT.md` mục 9 đòi hỏi ở khâu
        bước 3 (`hook_locked.txt`, `hook_lock.json`, `hook_storyboard.json`, `flow_prompts\\shot_NN.txt`,
        `grok_jobs.csv`) — trước bản vá này, storyboard CHỈ sinh khi gọi tay `hook_stage.py`, nên mọi
        tập chạy luồng bình thường bị giao thiếu 2/5 file, khâu bước 3 buộc phải DỪNG theo đúng
        luật của chính tài liệu đó.

        ĐẶT Ở ĐÂY (cuối `b5w_write_prompts`, KHÔNG đặt ở `hook_stage.khoa()` lúc khoá hook) vì
        `hook_storyboard.sinh()` đọc `characters.json` để giữ continuity khuôn mặt nhân vật
        (@REF/@REF2), mà hook bị khoá TRƯỚC KHI viết thân — lúc đó `characters.json` CHƯA TỒN TẠI
        (nó là tài sản sinh CÙNG ĐỢT với `img_prompts.txt`/`img_doan.txt`/`thumb_text.txt`, xem
        `masters_from_bible()` ở trên: "characters.json (lớp 1 viết trước B5W)" — tức đã có sẵn
        trên đĩa ngay khi `b5w_write_prompts` bắt đầu chạy, do Claude Code/bộ não viết TRƯỚC khi
        gọi tiếp make_video.py). Sinh storyboard sớm hơn mốc này sẽ chạy với ghi chú "(chưa có
        characters.json)" của chính `hook_storyboard.sinh()` mà vẫn gắn nhãn REF/REF2 cho các
        shot — tức trỏ tới ảnh gốc nhân vật CHƯA TỒN TẠI, trái luật dự án "phải tạo ảnh master
        nhân vật TRƯỚC khi giao khâu vẽ ảnh" (memory `ref-lock-tao-truoc-khi-giao-may2`).

        Điều kiện chạy (bỏ qua ÊM, không in gì, cho ~90% tập chưa dùng tính năng hook):
        - `hook_stage.is_enabled(self.p)` — công tắc BẬT/TẮT THEO TỪNG KÊNH, mặc định TẮT.
        - `hook_stage.doc_lock(self.dir)` khác None — tập phải có hook ĐÃ KHOÁ (H1–H4 xong).
        Không rẽ theo `body_mode()`/`id` kênh — hook độc lập với AI-images hay stock-clips
        (hàng rào #2 CLAUDE.md: khác biệt lane chỉ qua field profile).

        Idempotent, KHÔNG tốn thêm lượt model khi gọi lại nhiều lần (đã đọc lại code xác nhận):
        `hook_storyboard.sinh()` mở `hook_storyboard.json` đã có, so `hook_sha256` với
        `hook_lock.json["sha256"]`, khớp thì `return sb` NGAY — dòng này nằm TRƯỚC lệnh gọi
        `ai_steps._writer_chat()` trong hàm đó, nên B5W chạy lại (resume, hoặc bị skip rồi gọi lại
        do sửa code) không sinh thêm request nào tới model.

        Lỗi khi sinh storyboard (model trả JSON hỏng cả 3 lần, mạng đứt, hạ tầng...) KHÔNG được
        làm hỏng bước ghi tài sản — B5W (viết ảnh/characters) là việc CHÍNH, storyboard hook chỉ là
        việc PHỤ đi kèm. Bắt cả `Exception` lẫn `SystemExit` (hook_storyboard.sinh ném SystemExit
        khi thiếu hook khoá hoặc storyboard không hợp lệ sau 3 lần — SystemExit không phải
        subclass của Exception nên phải bắt riêng), in cảnh báo kèm lệnh chạy tay để vá sau, rồi
        đi tiếp bình thường.
        """
        import hook_stage
        if not hook_stage.is_enabled(self.p) or not hook_stage.doc_lock(self.dir):
            return
        try:
            import hook_storyboard
            hook_storyboard.sinh(self.dir, self.p)
        except (Exception, SystemExit) as e:
            print(f"  ⚠️ hook_storyboard.sinh() lỗi ({type(e).__name__}: {str(e)[:200]}) — bỏ qua, "
                  f"KHÔNG chặn B5W. Chạy tay lại khi cần: "
                  f"py -3.13 hook_storyboard.py --profile {self.p.get('id')} --slug {self.slug}")

    def _b5w_ghi_prompt(self, sheet=""):
        """Thân cũ của B5W (tách ra 2026-09-23 để `b5w_write_prompts` gọi thêm
        `_sinh_hook_storyboard_neu_can()` sau khi hàm này ghi xong tài sản — xem docstring 2 hàm
        trên). Nội dung/hành vi giữ NGUYÊN, không đổi 1 dòng logic viết prompt.

        Stamp fingerprint (gate_common) ngay sau khi viết — lần sau resume (kể cả sau khi script
        bị sửa lại vì REMAKE) còn biết prompt có bám đúng script hiện tại hay không.
        """
        if self.body_mode() == "stock_clips":
            return
        pf = self.f("img_prompts.txt")
        if pf.exists():
            b_stale, _ = gate_common.kiem_stale(self.dir)
            if b_stale:
                print("[B5W] img_prompts.txt bám bản script CŨ (script đã sửa lại sau đó) → viết lại")
                for x in b_stale:
                    print("   ✗", x)
                pf.unlink()
                self.state.pop("B5W", None)
        if self.skip("B5W", pf):
            return
        self.kiem_lock("B5W")   # NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS — sau skip, trước khi tốn tiền
        if self.prompts_by_fable_doan():
            # Fable viết prompt THEO ĐOẠN (không cần voice.srt → giọng có thể để cuối), ra luôn img_doan.txt
            # cho sinh_neo. B55 (qc_img_doan) chấm mapping ngay sau — lỗi cơ học/STALE là dừng.
            import prompt_doan
            n, tk = prompt_doan.viet(self.p, self.dir)
            run(pycmd("qc_img_doan.py", "--slug", self.dir, "--mode", "warn"), "B55 mapping ảnh↔đoạn", cho_loi=True)
            logf = self.dir / "logs" / "B55_mapping_latest.json"
            kq = json.loads(logf.read_text(encoding="utf-8")) if logf.exists() else {}
            if kq.get("status") == "FAIL":
                raise SystemExit("✗ B55: mapping ảnh↔đoạn lỗi cơ học/STALE → DỪNG (đọc logs/B55_mapping_latest.json).")
            self.done("B5W", prompts=n, by="fable_doan", tags=tk, b55=kq.get("status", "?"))
            return
        dur = (self.state.get("B4", {}) or {}).get("seconds") or self.minutes * 60
        res = ai_steps.write_img_prompts(self.p, self.f("script.txt").read_text(encoding="utf-8"),
                                         duration_sec=dur, sheet=sheet or None, srt=self.voice_srt())
        pf.write_text("\n".join(res["prompts"]), encoding="utf-8")
        if res.get("world"):
            self.f("world.txt").write_text(res["world"], encoding="utf-8")
        if not res.get("storyboard"):
            print("  ⚠️ KHÔNG dùng được storyboard (thiếu/lỗi voice.srt) → ảnh chỉ rải đều theo "
                  "thời lượng, chưa bám mốc lời đọc.")
        gate_common.ghi_fingerprint(self.dir)
        self.done("B5W", prompts=len(res["prompts"]))

    def b5p_qc(self, force=False):
        """B5P — prompt ảnh có MÂU THUẪN CỐT TRUYỆN không (module dùng chung gate_common.py +
        qc_prompt_consistency.py, P0 2026-09-18 — trước đây chỉ satori-jp-obaa/brain_channel.py
        dùng; ở đây lắp lại y nguyên cho não-ramcloud, KHÔNG import brain_channel.py, đúng luật
        "cấm gộp/cấm bundle chéo hai nhánh" — chỉ dùng chung phần hạ tầng gate_common vốn viết
        pipeline-agnostic). CHỈ chạy khi lane khai `profile.image.b5p_qc = true`.

        Mode WARN cố định cho lane này lúc mới bật (chưa đủ số liệu false-positive để chuyển FAIL,
        đúng cách satori làm ở "2 tập đầu"): chỉ DỪNG khi lỗi CƠ HỌC/STALE/hạ tầng (không phải vì
        mâu thuẫn semantic — cái đó chỉ cảnh báo, đọc log mà soi).
        """
        if self.body_mode() == "stock_clips" or not self.f("img_prompts.txt").exists():
            return
        if not ((self.p.get("image", {}) or {}).get("b5p_qc")):
            return  # lane không bật cờ này → bỏ qua êm, không phải lỗi
        if self.skip("B5P", None):
            return
        print("[B5P] prompt ảnh ↔ cốt truyện (gate_common/qc_prompt_consistency) …")
        run(pycmd("qc_prompt_consistency.py", "--slug", self.dir, "--mode", "warn"),
            "B5P prompt↔truyện", cho_loi=True)
        logf = self.dir / "logs" / "B5P_latest.json"
        kq = json.loads(logf.read_text(encoding="utf-8")) if logf.exists() else {}
        status = kq.get("status", "?")
        sem = (kq.get("metrics", {}) or {}).get("semantic", {}) or {}
        self.done("B5P", status=status, blocking=kq.get("blocking_issues"),
                  n_would_block=sem.get("n_would_block"), n_ambiguous=sem.get("n_ambiguous"))
        if status == "FAIL" and not force:
            print("  Sửa: đọc logs/B5P_latest.json, sửa img_prompts.txt (hoặc series_ctx.txt nếu "
                  "thiếu dữ kiện) rồi chạy lại, hoặc --force-qc nếu chấp nhận.")
            raise SystemExit("✗ B5P: lỗi cơ học/STALE/hạ tầng ở prompt ảnh → DỪNG.")

    def b5_images(self, sheet=""):
        """1 file img_prompts.txt có marker '@REF ' cho cảnh thấy mặt → gen_images.py tự chia
        REF-LOCK (110đ) vs text-only (50đ). Không tách 2 file (gen_images đã hỗ trợ marker)."""
        if self.body_mode() == "stock_clips":
            return self.b5_stock()
        pf = self.f("img_prompts.txt")
        imgdir = self.f("img")
        if self.skip("B5", None if self.dry else imgdir / "001.png"):
            return
        dur = (self.state.get("B4", {}) or {}).get("seconds") or self.minutes * 60
        img = self.p.get("image", {}) or {}
        if not pf.exists():
            res = ai_steps.write_img_prompts(self.p, self.f("script.txt").read_text(encoding="utf-8"),
                                             duration_sec=dur, sheet=sheet or None,
                                             srt=self.voice_srt())
            pf.write_text("\n".join(res["prompts"]), encoding="utf-8")
            if res.get("world"):
                self.f("world.txt").write_text(res["world"], encoding="utf-8")
            if not res.get("storyboard"):
                print("  ⚠️ KHÔNG dùng được storyboard (thiếu/lỗi voice.srt) → ảnh chỉ rải đều, "
                      "sẽ lệch lời ở khúc giữa. Nên chạy lại B5 sau khi có SRT.")
        lines = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
        n_face = sum(1 for l in lines if l.lower().lstrip().startswith(("@ref", "@cast:")))
        n_scene = len(lines) - n_face
        cost = n_scene * 50 + n_face * (110 if img.get("ref_lock") else 50)
        print(f"[B5] {len(lines)} ảnh: {n_face} khoá mặt (@REF) + {n_scene} cảnh vật ≈ {cost:,}đ")
        if self.dry:
            print("[B5] --dry-run: DỪNG trước khi gen ảnh (chưa tốn tiền).")
            return
        imgdir.mkdir(exist_ok=True)
        sg = self.sample_gate()
        sample_status = (self.state.get("B5S") or {}).get("status")
        # C2 (docs/PHUONG_AN_LANE_F_BUOC2_3.md): lane khai image.sample_gate=N và ĐANG vẽ mẻ đầu
        # (chưa có ảnh nào) → tự đặt số mẫu = N, KỂ CẢ khi không truyền tay --anh-mau. Đã có
        # logs/B5S_sample.json PASS từ lượt trước (hoặc lane không khai sample_gate) thì bỏ qua,
        # vẽ thẳng cả loạt như cũ.
        n_mau = self.anh_mau or (sg if sg and sample_status != "PASS" and not any(imgdir.glob("*.png")) else 0)
        if n_mau:
            # VẼ MẪU TRƯỚC (bài học ep01 Lane G 2026-09-21: 40% ảnh ra trang manga nhiều ô, phát hiện sau khi đã vẽ
            # cả 94 ảnh → đốt 15.800đ thay vì 8.700đ). Vẽ master + N ảnh đầu rồi QUYẾT ĐỊNH tiếp theo.
            run(self.gen_cmd(pf, imgdir, n_face, sheet) + ["--limit", str(n_mau)], f"B5 vẽ {n_mau} ảnh MẪU")
            co = sorted(imgdir.glob("*.png"))
            if not sg:
                # Nhánh CŨ (--anh-mau tay, lane không khai sample_gate): LUÔN dừng, người tự xem
                # rồi tự chạy lại lệnh thường — giữ nguyên hành vi, không đổi cho lane khác.
                print(f"[B5] --anh-mau: đã vẽ {len(co)} ảnh mẫu → XEM {imgdir}\\001.png … {co[-1].name if co else ''} "
                      f"(+ master _ref/_ref2). Ảnh ra nhiều ô/collage, sai tuổi, sai phong cách → sửa img_prompts.txt / "
                      f"characters.json, xoá ảnh hỏng rồi chạy lại. Đạt → chạy lại lệnh thường (không --anh-mau) để vẽ nốt.")
                return
            # Nhánh MỚI (sample_gate khai trong profile): QC vision tự động (khớp prompt + KHÔNG
            # collage/nhiều ô — field single_scene mới trong qc_visual.IMG_SCHEMA).
            wf = self.f("world.txt")
            world = wf.read_text(encoding="utf-8") if wf.exists() else ""
            mau_prompts = lines[:n_mau]
            r = qc_visual.qc_images(imgdir, mau_prompts, world, sample=len(mau_prompts))
            n_van_de = qc_visual.report("B5S ẢNH MẪU", r)
            hard = [x for x in r["problems"] if "thiếu" in x or "HỎNG" in x or "TRÙNG" in x]
            dat = not (hard or r["infra"] or r.get("vision_bad"))
            self.f("logs").mkdir(exist_ok=True)
            (self.f("logs") / "B5S_sample.json").write_text(
                json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
            self.done("B5S", status="PASS" if dat else "FAIL", n=len(mau_prompts),
                      vision_bad=len(r.get("vision_bad") or []), problems=n_van_de)
            if self.sample_only or not dat:
                ly_do = "cờ --sample-only (dừng lại chờ người xem, đúng thiết kế)" if dat else \
                        f"{n_van_de} vấn đề — đọc logs/B5S_sample.json hoặc report ở trên"
                print(f"[B5S] DỪNG trước khi vẽ cả loạt ({ly_do}). Sửa xong (nếu có lỗi) thì xoá "
                      f"ảnh mẫu hỏng + chạy lại lệnh thường (không --sample-only) để vẽ nốt.")
                return
            print(f"[B5S] {len(mau_prompts)} ảnh mẫu ĐẠT (khớp prompt, không collage) → vẽ tiếp cả loạt luôn trong lượt này")
        # 3 key gpti2 xoay round-robin theo chỉ số ảnh → 8 luồng/key = 24 luồng.
        # Đo thật: 123 ảnh với 5 luồng = 969s (0 lỗi). Skill gpti2: 20 luồng × 39 ảnh = 211s, không 429.
        run(self.gen_cmd(pf, imgdir, n_face, sheet), "B5 gen ảnh")
        self.done("B5", images=len(list(imgdir.glob("*.png"))), ref_lock=n_face, cost_vnd=cost)

    def master_portrait(self, sheet):
        """1 ảnh master/nhân vật để khoá mặt cả video (CHARACTER SHEET bằng chữ KHÔNG giữ được mặt)."""
        master = self.f("_ref") / "001.png"
        if master.exists():
            # QC cả master CÓ SẴN: trước đây chỉ QC master mới vẽ → chạy lại B5 là bỏ qua QC.
            if not self.state.get("B5.0Q"):
                self.qc_master(master, sheet or (self.p.get("image") or {}).get("character_sheet", ""))
            return master
        mp = self.f("master_prompt.txt")
        mp.write_text(
            f"Character reference sheet portrait: {sheet}. Neutral calm expression, facing camera, "
            f"even lighting, plain grey background. "
            f"{(self.p.get('image') or {}).get('style_suffix','')}", encoding="utf-8")
        run(pycmd("gen_images.py", "--prompts", mp, "--out", self.f("_ref"), "--quality", "medium"),
            "B5.0 ảnh master (khoá mặt)")
        self.qc_master(master, sheet)
        return master

    def qc_master(self, master, sheet, tries=2):
        """QC ảnh master TRƯỚC khi gen loạt: tuổi · giới · trang phục · thời đại · phong cách.
        Master sai thì mọi ảnh khoá mặt theo nó đều sai — sửa ở đây rẻ hơn cả trăm lần."""
        n0 = self.p.get("narrator", {}) or {}
        band = str(n0.get("age_band", "")).split("-")
        age = int(band[0]) + 5 if band and band[0].isdigit() else 0
        spec = {"age": age, "gender": (n0.get("gender") or "")[:1].upper(), "look": sheet}
        wf = self.f("world.txt")
        world = wf.read_text(encoding="utf-8") if wf.exists() else ""
        for k in range(tries):
            r = qc_visual.qc_master(master, spec, world)
            n = qc_visual.report("B5.0Q ẢNH MASTER", r)
            if r["infra"]:
                print("  (QC master không chạy được → bỏ qua, KHÔNG coi là đạt)")
                return
            if not n:
                self.done("B5.0Q", ok=True, age=r.get("apparent_age"))
                return
            if k == tries - 1:
                print("  ⚠️ master vẫn chưa đạt sau khi vẽ lại → dùng tạm, ảnh khoá mặt sẽ kém.")
                return
            print("  ↻ vẽ lại ảnh master rồi QC lần nữa …")
            master.unlink(missing_ok=True)
            run(pycmd("gen_images.py", "--prompts", self.f("master_prompt.txt"),
                 "--out", self.f("_ref"), "--quality", "medium"), "B5.0 vẽ lại master")

    def _soften_hands(self, prompts, bad_names):
        """Ảnh vẫn méo sau lượt vẽ lại đầu → sửa PROMPT: bỏ cận cảnh bàn tay/ngón tay.
        Đó gần như luôn là thủ phạm của 'méo mó/dị dạng' ở ảnh AI."""
        pf = self.f("img_prompts.txt")
        imgs = {p.name: i for i, p in enumerate(sorted(self.f("img").glob("*.png")))}
        lines = list(prompts)
        hit = 0
        for nm in bad_names:
            i = imgs.get(nm)
            if i is None or i >= len(lines):
                continue
            l = lines[i]
            new = re.sub(r"\b(CLOSE-UP|DETAIL)\b", "MEDIUM", l, flags=re.I)
            new = re.sub(r"[^,]*\b(hands?|fingers?|palms?)\b[^,]*,\s*", "", new, flags=re.I)
            if new != l:
                lines[i] = new.strip().rstrip(",") + ", hands out of frame or relaxed and unfocused"
                hit += 1
        if hit:
            pf.write_text("\n".join(lines), encoding="utf-8")
            print(f"  [prompt] bỏ cận cảnh bàn tay ở {hit} dòng (thủ phạm hay gây méo)")
        return lines

    def fix_weak_images(self):
        """B8Q chỉ ra mốc thời gian nào ảnh lệch lời → quy ra ĐÚNG ảnh đó, xoá và vẽ lại.
        Trả True nếu có vẽ lại được ảnh nào."""
        qf, pf = self.f("qc_video.json"), self.f("img_prompts.txt")
        if not (qf.exists() and pf.exists()):
            return False
        try:
            weak = (json.loads(qf.read_text(encoding="utf-8")) or {}).get("weak") or []
        except Exception:
            return False
        srt = self.voice_srt()
        imgs = sorted(self.f("img").glob("*.png"))
        if not (weak and srt.exists() and imgs):
            return False
        import storyboard as sb
        prompts = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
        idx = set()
        anc = self.f("anchors.txt")
        if self.sync_anchors() and anc.exists():
            # Lane neo theo câu: ảnh nào ĐANG HIỆN ở mốc t phải tra theo anchors (chia đều sb.blocks trỏ SAI ảnh —
            # đo thật ep01 Lane G: B8Q chê 203s/472s/608s, chia đều trỏ 014/034/045 trong khi ảnh thật là 017/034/043).
            import assemble
            ims = sorted(self.f("img").glob("[0-9]*.png"))
            segs = assemble.anchor_durations(assemble.load_anchors(anc), ims, assemble.media_seconds(self.voice_audio()),
                                             assemble.parse_srt_cues(srt))
            t0 = 0.0
            spans = []
            for im, sg in zip(ims, segs):
                spans.append((t0, t0 + sg)); t0 += sg
            for w in weak:
                tt = w.get("t") or 0
                idx.add(next((i for i, (a_, b_) in enumerate(spans) if a_ <= tt < b_), len(spans) - 1))
        else:
            bl = sb.blocks(sb.parse_cues(srt), len(imgs))
            for w in weak:
                tt = w.get("t") or 0
                idx.add(min(range(len(bl)), key=lambda i: abs((bl[i][1] + bl[i][2]) / 2 - tt)))
        idx = {i for i in idx if i < len(imgs)}
        if not idx:
            return False
        print(f"[B8Q] vẽ lại {len(idx)} ảnh ở mốc lệch: "
              f"{', '.join(imgs[i].name for i in sorted(idx))}")
        for i in sorted(idx):
            imgs[i].unlink(missing_ok=True)
        n_face = sum(1 for l in prompts if l.lower().lstrip().startswith(("@ref", "@cast:")))
        run(self.gen_cmd(pf, self.f("img"), n_face), "B8Q vẽ lại ảnh lệch")
        return True

    def _thumb_flags(self, bg):
        """Cờ dựng chữ thumbnail theo hồ sơ kênh.

        `wrap` + `max_font`: ngách kể tài liệu đòi CHỮ PHỦ 30-50% khung (đo 12/12 thumbnail top).
        Chế độ cũ ép câu dài vào MỘT hàng nên tự thu nhỏ còn 48px ≈ 8% khung — làm ngược công thức
        mà không cổng nào bắt, vì chữ vẫn "đọc được". Kênh nào không khai thì giữ nguyên như cũ.
        """
        th = self.p.get("thumbnail", {}) or {}
        # nền RIÊNG dựng sẵn chủ thể lệch phải → chữ dồn sang TRÁI cho khỏi đè mặt
        cmd = ["--side", "left"] if bg.parent.name == "_thumb" else []
        if th.get("side_width"):
            cmd += ["--side-width", str(th["side_width"])]
        if th.get("wrap"):
            cmd += ["--wrap"]
        if th.get("max_font"):
            cmd += ["--max-size", str(int(th["max_font"]))]
        if th.get("flat_bg") and bg.parent.name == "_thumb":
            # ảnh nền RIÊNG đã tự chừa đúng bố cục (đen/ảnh thật) ngay từ prompt — bỏ hẳn
            # blend mờ/vignette/co ảnh, dùng nguyên vẹn (xem _flat_bg_note trong profile).
            cmd += ["--flat-bg"]
        elif th.get("photo_scale"):
            cmd += ["--photo-scale", str(th["photo_scale"])]
        # cờ thêm theo lane (vd satori: --fit-height --fit-each = SENIOR TYPOGRAPHY, user khoá
        # 2026-09-17) — khai trong profile, KHÔNG if theo profile_id ở đây.
        cmd += [str(x) for x in (th.get("extra_flags") or [])]
        return cmd

    def _ensure_face_json(self, bg):
        """`thumbnail_text.py` bắt buộc `face.json` cạnh `bg` (gate 2026-09-18) nhưng không tự
        sinh — thiếu bước gọi `face_box.py` này làm B7 chết ngay lần đầu chạy lại sau khi thêm gate
        (đo thật ep08-fatima-akita, Lane A không có mặt người trong nền). Chỉ chạy khi CHƯA có sẵn
        (không phá `face_debug.png` một tập đã duyệt tay). Cờ layout PHẢI khớp cờ dựng chữ thật —
        chỉ lấy đúng tập con face_box.py hiểu, KHÔNG truyền nguyên `_thumb_flags()` (--wrap/--max-size
        làm face_box.py lỗi argparse).
        """
        fj = bg.parent / "face.json"
        if fj.exists():
            return
        th = self.p.get("thumbnail", {}) or {}
        extra = [str(x) for x in (th.get("extra_flags") or [])]
        cmd = ["--side", "left" if bg.parent.name == "_thumb" else "center"]
        if th.get("side_width"):
            cmd += ["--side-width", str(th["side_width"])]
        if "--fit-height" in extra:
            cmd += ["--fit-height"]
        if "--subject-side" in extra:
            i = extra.index("--subject-side")
            if i + 1 < len(extra):
                cmd += ["--subject-side", extra[i + 1]]
        flat = bool(th.get("flat_bg")) and bg.parent.name == "_thumb"
        if flat or "--flat-bg" in extra:
            cmd += ["--flat-bg"]
        elif th.get("photo_scale"):
            cmd += ["--photo-scale", str(th["photo_scale"])]
        if not th.get("require_face", True):
            cmd += ["--allow-no-face"]
        run(pycmd("face_box.py", bg) + cmd, f"B7 face_box ({bg.parent.name}/{bg.name})")

    def b7_thumb(self):
        if self.listing_external():
            if (self.only and self.only != "B7") or (self.den and STEPS.index("B7") > STEPS.index(self.den)):
                return
            if "B7" not in self.state:
                print("[B7] bỏ qua — publish.listing_external: thumbnail do dự án khác lo")
                self.done("B7", skipped="listing_external")
            return
        out = self.f("thumbnail_final.png")
        tf = self.f("thumb_text.txt")
        if self.skip("B7", out if not self.dry else tf):
            return
        if not tf.exists():
            th_cfg = self.p.get("thumbnail", {}) or {}
            if th_cfg.get("text_engine") == "opus_dual_qc":
                # THAY THẾ ai_steps.write_thumb_text() (1 lượt Gemini, không QC) bằng 2 lượt Opus
                # ĐỘC LẬP (viết 3 phương án → context Opus MỚI QC tiếng Nhật + sự thật, chọn PASS).
                # Verify thật 2026-09-17 (satori ep01): bắt được lỗi suy diễn/gán sai trách nhiệm
                # mà 1 lượt Gemini cũ không tự soi ra. Bật per-lane qua field này, KHÔNG đổi mặc
                # định cho lane chưa verify — xem docs/QC_THUMBNAIL_GPT_SOL.md.
                import write_thumb_text_opus
                script_txt = self.f("script.txt").read_text(encoding="utf-8")[:6000]
                lines, vi_lines = write_thumb_text_opus.run(title="", summary=script_txt,
                                                            profile_id=self.p["id"])
                tf.write_text("\n".join(lines) + "\n", encoding="utf-8")
                # Bản dịch tiếng Việt CẠNH thumb_text.txt — user không đọc được tiếng Nhật, cần
                # hiểu ngay thumbnail đang nói gì (quy ước "_vi" như voice_vi.srt/tomtat_vi.txt).
                if vi_lines:
                    self.f("thumb_text_vi.txt").write_text(
                        "\n".join(vi_lines) + "\n", encoding="utf-8")
            else:
                tf.write_text(ai_steps.write_thumb_text(
                    self.p, self.f("script.txt").read_text(encoding="utf-8")), encoding="utf-8")
        print(f"[B7] chữ thumbnail:\n{tf.read_text(encoding='utf-8')}")
        if self.dry:
            return
        # Lane clip stock KHÔNG có thư mục img/ (thân video là clip công cộng). Trước đây thiếu
        # img/ là bỏ luôn thumbnail — mà thumbnail lại chính là chỗ DUY NHẤT lane đó dùng ảnh AI.
        imgs = sorted(self.f("img").glob("*.png"))
        # Nền phải là ảnh CÓ MẶT NGƯỜI (kiểu simbot2). Nhưng chữ chiếm NỬA TRÊN khung, nên ảnh
        # nào mặt nằm giữa khung sẽ bị chữ đè lên mặt — mất cả mặt lẫn chữ (đo thật ep08, B7Q bắt).
        # → thử vài nền, render rồi CHẤM bằng B7Q, lấy nền đầu tiên đạt (hoặc ít lỗi nhất).
        # ⭐ Nền RIÊNG cho thumbnail: mọi ảnh trong img/ đều để mặt ở GIỮA khung, mà chữ cũng chiếm
        # nửa trên → thử 5 nền đều hỏng như nhau (đo thật ep08). Sinh 1 ảnh dành riêng, bố cục chừa
        # chỗ cho chữ: chủ thể dồn về 1/3 PHẢI, nửa trái là khoảng tối trống. Tốn thêm ~110đ.
        pf = self.f("img_prompts.txt")
        cands = []
        th = self.p.get("thumbnail", {}) or {}
        if th.get("dedicated_bg", True):
            tb = self.f("_thumb") / "001.png"
            if not tb.exists():
                wf = self.f("world.txt")
                world = wf.read_text(encoding="utf-8") if wf.exists() else ""
                sheet = (self.p.get("image") or {}).get("character_sheet", "")
                tp = self.f("thumb_bg_prompt.txt")
                if tp.exists() and tp.stat().st_size > 40:
                    # Prompt nền viết tay của tập này — GIỮ NGUYÊN. Ngách kể tài liệu không có
                    # nhân vật để chụp chân dung; nền là một CẢNH (vd hai bóng người soi gương qua
                    # vực vũ trụ), mỗi tập một cảnh khác, không sinh máy móc được từ profile.
                    print(f"[B7.0] dùng prompt nền viết sẵn: {tp.name}")
                else:
                    # Phong cách NỀN cố định cho cả kênh (user chốt 2026-09-10: "mỗi kênh 1 phong
                    # cách thumbnail, chỉ thay ảnh và text"). Trống = giữ nguyên photoreal điện ảnh
                    # cũ — kênh đang chạy (Satori JP) không bị đổi diện mạo giữa chừng.
                    phong_cach = th.get("art_style") or "cinematic ultra-realistic color, photorealistic, 8K"
                    if not sheet:
                        # CHỦ THỂ của riêng tập này — 1 dòng trong `thumb_bg_subject.txt`.
                        # Đây là thứ DUY NHẤT đổi giữa các tập; phong cách + bố cục + chỗ chừa chữ
                        # đều lấy từ hồ sơ kênh, nên loạt thumbnail nhìn là biết cùng một kênh.
                        sf = self.f("thumb_bg_subject.txt")
                        chu_the = sf.read_text(encoding="utf-8").strip() if sf.exists() else ""
                        if chu_the:
                            print(f"[B7.0] chủ thể của tập: {chu_the[:70]}")
                        tp.write_text(
                            f"{phong_cach}. Dark scene for a documentary thumbnail. "
                            f"{chu_the or world}. Deep "
                            f"navy and black background with subtle glow, dramatic lighting, high "
                            f"contrast. Main subject in the RIGHT third of the frame; the LEFT half "
                            f"and the LOWER half are empty dark negative space reserved for large "
                            f"text. No text, no watermark, no recognizable real person's face.",
                            encoding="utf-8")
                    else:
                        tp.write_text(
                            f"{phong_cach}. CLOSE-UP portrait of {sheet}, strong emotion on the "
                            f"face, eyes visible, positioned in the RIGHT third of the frame and "
                            f"looking toward the left; the LEFT half is empty dark shadowed "
                            f"background with deep negative space, no objects and no text there. "
                            f"{world}. dramatic side lighting, 16:9, no text", encoding="utf-8")
                cmd = pycmd("gen_images.py", "--prompts", tp, "--out", self.f("_thumb"),
                       "--quality", "medium")
                # BUG THẬT đã vá 2026-09-17 (satori ep01, anh chỉ ra): kênh có REF-LOCK
                # (`image.ref_lock=true`, có ảnh master ở `_ref/001.png`) mà prompt nền thumbnail
                # đánh dấu @REF/@REF2 thì PHẢI khoá đúng khuôn mặt nhân vật đó — trước đây gọi
                # gen_images.py KHÔNG truyền --ref nên marker @REF bị bỏ qua câm lặng (parse_prompts
                # tag='ref' nhưng route rơi về 'plain' vì thiếu --ref, xem gen_images.py dòng ~123),
                # ảnh nền thumbnail ra một khuôn mặt NGẪU NHIÊN không phải nhân vật chính của tập.
                # Quy tắc: mọi kênh có ref_lock → LUÔN thử khoá mặt cho ảnh thumbnail giống hệt thân
                # video, không chỉ khi "cần" — vì marker @REF/@REF2 do B3/B5 tự viết vào
                # thumb_bg_prompt.txt, không phải Claude tự đoán khi nào cần.
                first_tag = tp.read_text(encoding="utf-8").strip().split(None, 1)[:1]
                first_tag = first_tag[0].lower() if first_tag else ""
                img_cfg = self.p.get("image", {}) or {}
                if img_cfg.get("ref_lock") and self.f("_ref").joinpath("001.png").exists():
                    if first_tag == "@ref2":
                        # Nhân vật PHỤ trong thumbnail (hiếm) — chưa có quy ước đặt tên thư mục
                        # chuẩn cho "master nhân vật phụ" như `_ref` của nhân vật chính, nên dò
                        # thư mục `_ref_*` đầu tiên tìm được trong tập làm --ref2 (heuristic, KHÔNG
                        # phải quy tắc cứng — tập nào có ≥2 nhân vật phụ dùng chung kiểu tên `_ref_*`
                        # thì tự chỉ định tay bằng cách đổi thumb_bg_prompt.txt cho khớp).
                        alt = sorted(p_ for p_ in self.dir.glob("_ref_*/001.png"))
                        if alt:
                            cmd += ["--ref2", alt[0]]
                    elif first_tag == "@ref":
                        cmd += ["--ref", self.f("_ref") / "001.png"]
                run(cmd, "B7.0 ảnh nền thumbnail")
            if tb.exists():
                cands.append(tb)   # ưu tiên số 1; các ảnh trong img/ chỉ là dự phòng
        if pf.exists():
            lines = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
            face = [i for i, l in enumerate(lines)
                    if l.lower().lstrip().startswith("@ref") and i < len(imgs)]
            if face:
                k = max(1, len(face) // 4)
                cands += [imgs[i] for i in face[::k]][:4]
        if not cands and imgs:
            cands = [imgs[len(imgs) // 3]]
        if not cands:
            print("[B7] không có ảnh nền nào (thiếu cả _thumb/ lẫn img/) → bỏ qua thumbnail")
            return
        txt = tf.read_text(encoding="utf-8")
        best = None
        for bg in cands:
            # nền RIÊNG dựng sẵn chủ thể lệch phải → chữ dồn sang TRÁI cho khỏi đè mặt
            self._ensure_face_json(bg)
            run(pycmd("thumbnail_text.py", "--bg", bg, "--text", tf, "--out", out)
                + self._thumb_flags(bg), f"B7 thumb ({bg.parent.name}/{bg.name})")
            # Kênh không dùng mặt người làm nền thumbnail (ngách kể tài liệu) thì đừng đòi mặt.
            r = qc_visual.qc_thumb(out, txt, doi_mat=bool(th.get("require_face", True)))
            n = len(r["problems"])
            print(f"[B7Q] nền {bg.name}: {'ĐẠT' if not n and not r['infra'] else str(n) + ' vấn đề'}"
                  + ("" if not n else " — " + "; ".join(p[:60] for p in r["problems"][:2])))
            if r["infra"]:
                print("  (QC thumbnail không chạy được → giữ nền này)")
                best = (0, bg)
                break
            if not n:
                best = (0, bg)
                break
            if best is None or n < best[0]:
                best = (n, bg)
            # Nền RIÊNG (`_thumb`, dedicated_bg) LUÔN được nhận sau đúng 1 lần thử, KHÔNG so
            # điểm với ảnh thân video dự phòng — đúng nghĩa "ưu tiên số 1, img/ chỉ là dự
            # phòng" đã ghi ở chỗ dựng `cands`. Trước đây so bằng SỐ VẤN ĐỀ thô: nền riêng bị
            # QC vision chê cảm tính "hơi vô cảm, không gợi tò mò" (3 vấn đề) thua ảnh thân
            # video tình cờ ít vấn đề hơn (2), code CŨ chọn ảnh thân video — ảnh đó SAI HẲN
            # khuôn thumbnail dự án (không nền đen, không chừa chỗ chữ) dù điểm số thấp hơn.
            # Đã dính thật ep01 Lane E (2026-09-16) — sửa tại gốc thay vì ghi đè tay từng tập.
            if bg.parent.name == "_thumb":
                print("  (nền riêng — dùng luôn, không đổi sang ảnh thân video dự phòng)")
                break
        nbad, bg = best
        if nbad:
            print(f"[B7] không nền nào đạt hẳn → dùng {bg.name} ({nbad} vấn đề)")
            self._ensure_face_json(bg)
            run(pycmd("thumbnail_text.py", "--bg", bg, "--text", tf, "--out", out)
                + self._thumb_flags(bg), "B7 thumbnail")
        print(f"[B7] nền: {bg.name}")
        self.done("B7", bg=bg.name, qc_problems=nbad)

    def b8_assemble(self):
        out = self.f("final.mp4")
        if self.skip("B8", out) or self.dry:
            return
        a = self.p.get("assemble", {}) or {}
        if self.body_mode() == "stock_clips":
            body = self.p.get("body", {}) or {}
            cmd = pycmd("stock_cut.py", "--profile", self.p["id"], "--slug", self.dir,
                        "--audio", self.voice_audio(), "--out", out,
                        "--stock", self.kho_stock(),
                        "--size", "1920x1080")
            srt0 = self.voice_srt()
            if srt0.exists():
                # Vẫn đưa .srt vào để stock_cut hút mốc cắt về ranh giới câu; chỉ chặn riêng
                # khâu CHÁY CHỮ. Hai việc khác nhau, đừng gộp (xem chú thích trong stock_cut.py).
                cmd += ["--srt", srt0]
                if not self.chay_phu_de():
                    cmd += ["--khong-chay-phu-de"]
            # Kiểu phụ đề cháy theo hồ sơ kênh (xem chú thích trong stock_cut.py).
            for khoa, co in (("sub_font", "--font"), ("sub_size", "--sub-size"),
                             ("sub_margin", "--sub-margin"), ("sub_outline", "--sub-outline")):
                if a.get(khoa) is not None:
                    cmd += [co, str(a[khoa])]
            ev = self.f("evidence.json")
            if ev.exists():
                cmd += ["--evidence", ev]
            if self.asm_jobs:
                cmd += ["--jobs", str(self.asm_jobs)]
            if a.get("bgm") and (ROOT / a["bgm"]).exists():
                cmd += ["--bgm", ROOT / a["bgm"], "--bgm-volume", a.get("bgm_volume", 0.09)]
            run(cmd, "B8 ghép clip stock")
            self.done("B8", mp4=out.name, mode="stock_clips")
            return
        cmd = pycmd("assemble.py", "--img", self.f("img"), "--audio", self.voice_audio(),
               "--out", out, "--zoom", a.get("zoom", 1.12),
               "--transition", a.get("transition", "xfade"), "--xfade", a.get("xfade", 0.6),
               "--size", "1920x1080", "--zoom-dir", a.get("zoom_dir", "alt"))
        if self.asm_jobs:
            cmd += ["--jobs", str(self.asm_jobs)]
        srt = self.voice_srt()
        if self.sync_anchors():
            # NEO THEO CÂU (satori: img_doan.txt → sinh_neo.py → anchors.txt). Cần SRT đã bám kịch bản (B4a).
            # Không sinh được neo → sinh_neo exit 1 → DỪNG (không âm thầm quay về chia đều — ảnh sẽ trôi).
            if not srt.exists():
                raise SystemExit("✗ B8: assemble.sync=anchors cần voice.srt (chạy B4 trước)")
            if not self.f("img_doan.txt").exists():
                raise SystemExit("✗ B8: assemble.sync=anchors cần img_doan.txt (B5W nhánh fable_doan sinh ra) — chưa có")
            anc = self.f("anchors.txt")
            cu = anc.exists() and anc.stat().st_mtime < max(self.f("img_doan.txt").stat().st_mtime, srt.stat().st_mtime)
            if not anc.exists() or cu:
                run(pycmd("sinh_neo.py", "--slug", self.dir), "B8a đặt neo ảnh↔câu")
            cmd += ["--srt", srt, "--anchors", anc]
            if self.chay_phu_de():
                cmd += ["--burn-sub"]
                if a.get("sub_font"):
                    cmd += ["--font", str(a["sub_font"])]
        elif srt.exists() and self.chay_phu_de():
            cmd += ["--srt", srt]
        tt = a.get("tate", {}) or {}
        if tt.get("enabled"):
            # C4 (docs/PHUONG_AN_LANE_F_BUOC2_3.md): hộp chữ dọc 縦書き thay phụ đề ngang. Cần SRT
            # bám kịch bản (B4a) — nhánh sync=anchors ở trên đã thêm --srt vào cmd; nhánh khác thì
            # tự thêm ở đây nếu có file.
            if "--srt" not in cmd and srt.exists():
                cmd += ["--srt", srt]
            if "--srt" not in cmd:
                raise SystemExit("✗ B8: assemble.tate.enabled cần voice.srt (chạy B4 trước)")
            cmd += ["--tate", "--tate-side", str(tt.get("side", "left"))]
            for khoa, co in (("font_narration", "--tate-font-narration"), ("font_dialogue", "--tate-font-dialogue"),
                             ("font_size", "--tate-size"), ("max_chars_per_col", "--tate-max-chars"),
                             ("max_cols", "--tate-max-cols")):
                if tt.get(khoa) is not None:
                    cmd += [co, str(tt[khoa])]
        bb = a.get("bubble", {}) or {}
        if bb.get("enabled"):
            # Lane K (2026-09-24): mọi câu hiện trên hình — hộp lời kể + bóng thoại có đuôi (bong_thoai.py).
            # Cần voice_roles.json (tts_voicevox ghi ở B4) + img_faces.json (định vị mặt, vision, chạy 1 lần).
            roles = self.f("voice_roles.json")
            if not roles.exists():
                raise SystemExit("✗ B8: assemble.bubble cần voice_roles.json (B4 lồng tiếng đa giọng chưa chạy)")
            if "--srt" not in cmd and srt.exists():
                cmd += ["--srt", srt]
            import bong_thoai
            bong_thoai.do_mat(self.dir)
            cmd += ["--bubble-roles", roles, "--bubble-faces", self.f("img_faces.json"),
                    "--bubble-cfg", json.dumps(bb, ensure_ascii=False)]
        if a.get("bgm") and (ROOT / a["bgm"]).exists():
            cmd += ["--bgm", ROOT / a["bgm"], "--bgm-volume", a.get("bgm_volume", 0.09)]
            if a.get("bgm_keep_voice"):
                cmd += ["--bgm-keep-voice"]
        run(cmd, "B8 ghép video")
        # Lane L 2026-09-24: hiệu ứng âm thanh THÂN video (assemble.sfx) — sfx_plan.txt do máy 1 chọn theo nội dung,
        # ở đây chỉ sinh kho (nếu thiếu) rồi trộn vào final.mp4 vừa dựng (video giữ nguyên, mỗi lần B8 dựng lại từ đầu).
        if ((a.get("sfx") or {}).get("enabled")):
            if not self.f("sfx_plan.txt").exists():
                raise SystemExit("✗ B8: assemble.sfx bật nhưng thiếu sfx_plan.txt (máy 1: sfx_than.py --plan)")
            run(pycmd("sfx_than.py", "--profile", self.p["id"], "--slug", self.dir, "--kho"), "B8s kho hiệu ứng âm thanh")
            run(pycmd("sfx_than.py", "--profile", self.p["id"], "--slug", self.dir, "--tron"), "B8s trộn hiệu ứng âm thanh")
        self.done("B8", mp4=out.name)


def main():
    # ID YouTube được phép bắt đầu bằng '-' (vd -Gt6QYEFS38) → argparse tưởng là tham số và chết
    # với "expected one argument". Đổi sang URL đầy đủ trước khi phân tích dòng lệnh.
    from fetch_script import _fix_dash_id
    sys.argv[1:] = _fix_dash_id(sys.argv[1:])
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--competitor", default="", help="video_id/URL kênh đối thủ (bỏ nếu đã có competitor.txt)")
    ap.add_argument("--minutes", type=float, default=0)
    ap.add_argument("--sheet", default="", help="CHARACTER SHEET nhân vật chính của TẬP này")
    ap.add_argument("--from", dest="from_step", default="", choices=[""] + STEPS,
                    help="chạy lại từ bước này (xoá state các bước sau)")
    ap.add_argument("--only", default="", choices=[""] + STEPS)
    ap.add_argument("--den", default="", choices=[""] + STEPS,
                    help="chạy TỚI bước này rồi dừng (ảnh do máy 2 vẽ: --den B5K rồi ra đơn)")
    ap.add_argument("--skip-qc", action="store_true", help="bỏ hẳn bước QC nội dung B3Q")
    ap.add_argument("--no-fix", action="store_true", help="QC xong KHÔNG tự sửa, chỉ báo lỗi")
    ap.add_argument("--force-qc", action="store_true", help="vẫn chạy tiếp dù QC kết luận HỎNG")
    ap.add_argument("--tries", type=int, default=2,
                    help="số lượt viết lại kịch bản khi QC kết luận HỎNG")
    ap.add_argument("--dry-run", action="store_true", help="chỉ làm phần CHỮ + báo tiền, KHÔNG gen ảnh/video")
    # Giọng THEO TẬP — kênh rời rạc thì mỗi video một người kể khác nhau, dùng chung 1 giọng là sai.
    # Tên cờ giữ nguyên cho lệnh cũ không vỡ, nhưng nay nó làm nhiều hơn giọng: nhận NGƯỜI KỂ của
    # tập rồi dùng cho cả kịch bản, ảnh và giọng.
    ap.add_argument("--auto-voice", "--auto-narrator", dest="auto_voice", action="store_true",
                    help="đọc lời video gốc, nhận NGƯỜI KỂ của tập này rồi dùng cho kịch bản + "
                         "mặt nhân vật trong ảnh + giọng đọc")
    ap.add_argument("--voice", default="", help="ép giọng cho tập này (voice_id hoặc tên trong kho)")
    ap.add_argument("--voice-fx", default="", help="ép hiệu ứng giọng (none/old-med/boom/...)")
    ap.add_argument("--voice-speed", type=float, default=0.0, help="ép tốc độ đọc (0.5-1.5)")
    ap.add_argument("--img-workers", type=int, default=0,
                    help="số luồng vẽ ảnh (0 = theo hồ sơ). Giảm khi chạy nhiều video cùng lúc")
    ap.add_argument("--assemble-jobs", type=int, default=0,
                    help="số luồng ffmpeg khi ghép (0 = tự tính theo CPU). Giảm khi chạy song song")
    ap.add_argument("--redo-voice", action="store_true",
                    help="ĐỔI GIỌNG SAU KHI XEM (Lane G, anh chốt 2026-09-20 'giọng là bước cuối'): xoá voice.*/anchors/"
                         "final rồi chạy lại B4→B4Q→neo→B8→B8Q→B10→B11; GIỮ img_prompts/img_doan/ảnh (không gọi Fable/gpti2 lại). "
                         "Dùng kèm --voice/--voice-speed để đổi giọng.")
    ap.add_argument("--anh-mau", type=int, default=0, metavar="N",
                    help="B5 chỉ vẽ master + N ảnh đầu rồi DỪNG để người xem (luật 'vẽ 5 ảnh mẫu trước khi vẽ loạt', "
                         "Lane G 2026-09-21). Đạt → chạy lại không có cờ này, gen_images tự vẽ nốt phần còn thiếu.")
    ap.add_argument("--sample-only", action="store_true",
                    help="lane khai image.sample_gate (C2, Lane F): B5 vẽ mẫu + QC vision tự động rồi LUÔN DỪNG "
                         "(dù QC PASS) để người xem — dùng cho tập đầu của lane mới. Bỏ cờ này từ tập sau: QC PASS "
                         "thì tự vẽ tiếp cả loạt trong cùng lượt chạy, không cần mắt người.")
    ap.add_argument("--minutes-from-source", action="store_true",
                    help="độ dài tập BÁM THEO video gốc (bỏ qua nếu đã truyền --minutes)")
    args = ap.parse_args()

    prof = profiles.load(args.profile)
    job = Job(prof, args.slug, args.minutes or None, args.from_step or None, args.only or None,
              args.dry_run, voice=args.voice, voice_fx=args.voice_fx,
              voice_speed=args.voice_speed, auto_voice=args.auto_voice,
              minutes_auto=args.minutes_from_source,
              img_workers=args.img_workers, asm_jobs=args.assemble_jobs,
              den=args.den or None)
    job.anh_mau = max(0, int(args.anh_mau or 0))
    job.sample_only = bool(args.sample_only)
    if args.redo_voice:
        # Khác --from B4: KHÔNG pop B5W/B5P/B5/B5Q → prompt/ảnh giữ nguyên, chỉ giọng + những gì phụ thuộc giọng làm lại.
        xoa = ["voice.mp3", "voice.srt", "voice.stt.srt", "voice_paced.wav", "voice_paced.srt", "anchors.txt",
               "final.mp4", "review_vi.mp4", "qc_video.json", "qc_final.json"]
        for f_ in xoa:
            if job.f(f_).exists():
                job.f(f_).unlink()
        for s_ in ("B4", "B4Q", "B8", "B8Q", "B10", "B11"):
            job.state.pop(s_, None)
        job.state_f.write_text(json.dumps(job.state, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[--redo-voice] đã xoá giọng/neo/video cũ; giữ prompt + ảnh → chạy lại B4 → neo → B8 → QC → giao")
    job.resolve_minutes(args.competitor)     # PHẢI trước khi in dòng mục tiêu và trước B3
    print(f"=== {args.slug} · profile {prof['id']} · {profiles.narrator_line(prof)}")
    print(f"    mục tiêu {job.minutes}' = {profiles.target_chars(prof, job.minutes):,} chữ "
          f"(char_rate {profiles.char_rate(prof)}) · thư mục {job.dir}")
    t0 = time.time()
    job.b2_competitor(args.competitor)
    job.b2b_comments(args.competitor)       # bổ trợ, không chặn — xem docstring b2b_comments
    # PHẢI đứng giữa B2 và B3: cần transcript để nhận người kể, và phải xong TRƯỚC khi viết
    # kịch bản vì kịch bản + prompt ảnh đều lấy người kể từ hồ sơ.
    job.detect_narrator()
    # Chốt giọng NGAY tại đây (tra kho giọng, không gọi LLM, ~0s) thay vì đợi tới B4. Nhờ vậy
    # `--only B2` đủ để XEM TRƯỚC người kể + giọng của cả loạt video mà chưa tiêu một đồng nào.
    job.pick_voice()
    job.ensure_char_rate()          # hồ sơ mới chưa đo → đo ngay, kẻo cháy cả lượt B3+B4
    # Sửa tại chỗ không phải lúc nào cũng gỡ được (đo thật ep11: mâu thuẫn mốc thời gian, sửa 1 lượt
    # vẫn 3 lỗi → bị loại đúng luật). Khi đó VIẾT LẠI bản khác còn hơn bắt người vào cuộc — PASS 1
    # dao động rất mạnh nên bản sau thường khác hẳn. Tối đa `--tries` lượt.
    # B3 → B3Q → B4 → B4Q trong MỘT vòng: hỏng ở bất kỳ đâu trong bốn bước này đều quy về
    # "kịch bản chưa dùng được" → viết lại bản khác rồi làm lại.
    #  · gate B3 hỏng (đo thật ep12: nhịp 6,92 phẩy/câu) — trước đây dừng hẳn vì chưa bắt nhánh này
    #  · B3Q kết luận HỎNG (mâu thuẫn nặng / sao chép)
    #  · B4Q hỏng vì thời lượng — đó cũng là lỗi kịch bản, và char_rate vừa được B4 hiệu chỉnh nên
    #    bản viết lại sẽ nhắm đúng hơn.
    # LƯỢT THƯỞNG: khi B4Q chặn vì thời lượng NGAY SAU lúc char_rate vừa được hiệu chỉnh mạnh,
    # viết lại gần như chắc chắn đúng (bản trước nhắm bằng con số sai). Lượt này KHÔNG tính vào
    # `--tries`, nếu không thì các lượt viết lại vì nhịp/hội thoại ăn hết ngân sách và tập nào
    # dùng hồ sơ mới cũng gãy — đo thật trên hồ sơ Lopezzapa68: char_rate 300 (chưa đo) vs 249 thật.
    lean = ((prof.get("script", {}) or {}).get("flow") or "").lower() == "lean"
    thuong, luot, tries = 1, 0, max(1, args.tries)
    while True:
        luot += 1
        attempt = luot
        again = False
        if lean:
            # flow=lean (docs/QUY_TRINH_KICH_BAN_GON.md v2): Fable viết đúng ngân sách → máy đo → Sol lời cuối
            # → khoá SHA256. B3Q/B3F/B3S/B3R/B3G KHÔNG chạy (state ghi skipped=lean_flow). Không có vòng
            # viết-lại --tries: trượt = ESCALATE/BLOCK (SystemExit), người quyết.
            job.b3_lean(force=args.force_qc)
        else:
            try:
                job.b3_script(force=args.force_qc)
            except SystemExit:
                if attempt >= args.tries:
                    raise
                again = True
            if not again and not args.skip_qc:
                try:
                    job.b3q_qc(force=args.force_qc, fix=not args.no_fix)
                except SystemExit:
                    if attempt >= args.tries or \
                            (job.state.get("B3Q", {}) or {}).get("verdict") != "HONG":
                        raise
                    again = True
            if not again and not args.skip_qc:
                # B3F DỪNG HẲN, KHÔNG cho viết lại kịch bản. Lý do: B3F báo "chi tiết này không có
                # trong tư liệu" — cái sai nằm ở TƯ LIỆU, viết lại kịch bản chỉ đẻ ra đúng chỗ bịa đó
                # lần nữa. Tệ hơn: nhánh viết lại XOÁ script.txt + voice.mp3 + voice.srt, nên nối B3F
                # vào đó là tự xoá bản đang dùng được (đã dính thật 2026-09-10, mất cả 3 file).
                job.b3f_facts(force=args.force_qc)
            if not again and not args.skip_qc:
                job.b3s_sol(force=args.force_qc)
            if not again and not args.skip_qc:
                job.b3r_final_review(force=args.force_qc)
            if not again and not args.skip_qc:
                job.b3g_regate(force=args.force_qc)
        if not again and not args.dry_run:
            job.b4_voice()
            if not args.skip_qc:
                try:
                    job.b4q_qc(force=args.force_qc)
                except SystemExit:
                    # C3 (docs/PHUONG_AN_LANE_F_BUOC2_3.md, bảo vệ script khi B4 chạy Ở MÁY 2):
                    # lane flow=lean đã có script.lock.json (PASS/ESCALATE) từ máy 1 — KHÔNG được
                    # rơi vào nhánh "viết lại kịch bản" bên dưới (nó xoá script.txt rồi gọi lại B3,
                    # mà máy 2 thường không có claude -p/Fable để viết lại, và dù có thì cũng ghi
                    # đè bản đã Sol PASS). B4Q hỏng ở đây luôn là lỗi GIỌNG (credit/độ dài/nghỉ sai
                    # chỗ), không phải lỗi kịch bản → dừng ngay, báo lại máy 1, không tự sửa.
                    if lean:
                        raise
                    if job.rate_fixed and thuong > 0:
                        thuong -= 1
                        luot -= 1          # lượt này KHÔNG tính vào ngân sách
                        job.rate_fixed = False
                        print("\n↻ char_rate vừa được hiệu chỉnh — bản trước nhắm bằng số sai, "
                              "viết lại một lượt (không tính vào --tries)")
                        again = True
                    elif luot >= tries:
                        raise
                    else:
                        again = True
        if not again:
            break
        print(f"\n↻ viết lại kịch bản (lượt {luot+1}/{tries})\n")
        for s_ in ("B3", "B3Q", "B4", "B4Q"):
            job.state.pop(s_, None)
        # ⚠️ CHÉP RA TRƯỚC KHI XOÁ — nhánh này đã làm mất kịch bản viết tay một lần (2026-09-11).
        # Kịch bản có phần mở đầu sửa tay bị nhánh này xoá sạch vì B4Q báo đúng 1 vấn đề; may là
        # còn bản nháp rời nên dựng lại được. `--tries` mặc định là 2, nghĩa là chỉ cần một cổng
        # phía sau kêu lên là công viết tay bay mất mà không hỏi ai. Xoá thì vẫn xoá (vòng viết
        # lại cần thư mục sạch), nhưng phải để lại đường lùi.
        bak = job.dir / "_truoc_khi_viet_lai"
        bak.mkdir(exist_ok=True)
        for f_ in ("script.txt", "voice.mp3", "voice.srt", "voice_paced.wav", "voice_paced.srt"):
            p_ = job.f(f_)
            if p_.exists():
                shutil.copy2(p_, bak / f_)
                p_.unlink()
        print(f"  (bản cũ đã chép sang {bak.name}/ — muốn giữ kịch bản viết tay thì chạy lại "
              f"với --tries 1)")
    if not args.dry_run:
        job.b5w_write_prompts(args.sheet)
        if not args.skip_qc:
            job.b5p_qc(force=args.force_qc)
    job.b5_images(args.sheet)
    # B5K trước B5A: phải biết đoạn nào nói tới vật thể cụ thể rồi mới biết vẽ gì.
    job.b5k_khop_hinh()
    job.b5a_anh_canh()
    if not args.dry_run and not args.skip_qc:
        job.b5q_qc(force=args.force_qc, fix=not args.no_fix)
    job.b7_thumb()
    # B8Q chỉ ra ĐÚNG mốc thời gian nào ảnh lệch lời → vẽ lại đúng những ảnh đó rồi ghép lại.
    # Trước đây chỉ báo rồi dừng, bắt người vào cuộc.
    for a2 in range(1, 3):
        job.b8_assemble()
        if args.dry_run or args.skip_qc:
            break
        try:
            job.b8q_qc(force=args.force_qc)
            break
        except SystemExit:
            if a2 >= 2 or args.no_fix or not job.fix_weak_images():
                raise
            print("\n↻ đã vẽ lại ảnh ở các mốc lệch → ghép lại rồi chấm lần nữa\n")
            for s_ in ("B8", "B8Q"):
                job.state.pop(s_, None)
            job.f("final.mp4").unlink(missing_ok=True)
    job.b9_publish()
    if not args.skip_qc:
        job.b10_nghiem_thu(force=args.force_qc)
        job.b11_giao_hang()
    print(f"\n=== XONG {args.slug} sau {(time.time()-t0)/60:.1f} phút")
    for s in STEPS:
        st = job.state.get(s)
        print(f"  {s}: {json.dumps(st, ensure_ascii=False)[:110] if st else '(chưa chạy)'}")


if __name__ == "__main__":
    main()
