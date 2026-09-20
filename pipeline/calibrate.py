"""calibrate.py — ĐO char-rate (chữ/phút) thật của 1 giọng rồi ghi vào profile.

Vì sao BẮT BUỘC: "309 chữ/phút" chỉ đúng cho giọng Ado@0.92. Đo thật 2026-09-07:
Ryu-Characters@1.0 = 322,6 · Dominant Man@1.0 = 332,6 · Ryo-maru@1.1 = 427,6 (chênh 39%).
Dùng sai char-rate → kịch bản "30 phút" đọc ra 22 phút. Xem `docs/PROFILE_ARCHITECTURE.md`.

Dùng:
  py -3.13 calibrate.py --profile satori-jp-obaa                 # đo giọng của profile rồi GHI LẠI
  py -3.13 calibrate.py --voice "Ryu - Characters" --speed 1.0 --fx boom     # chỉ đo, không ghi
  py -3.13 calibrate.py --profile samurai-history-jp --no-save

Chi phí: ~250 chữ ≈ 300 credit ≈ 15 giây/lần đo.
"""
import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import profiles
from tts import apply_fx, mp3_seconds, normalize_fx, resolve_voice

# Đoạn mẫu: văn kể chuyện bình thường, mật độ kanji trung bình (kanji đọc lâu hơn kana → sai số ~±3%).
SAMPLE = {
    "ja": ("私が、この村に、戻ってまいりましたのは、去年の、秋のことでございます。"
           "駅前の、古い商店街は、シャッターばかりになり、子どもの声も、聞こえなくなっておりました。"
           "けれど、山裾の、あの栗の木は、昔と同じように、たわわに実をつけて、私を待っていてくれました。"
           "父が植え、母が守り、そして私が、五十年ぶりに、手を触れた木でございます。"
           "人は変わり、町も変わりますが、根を張ったものは、静かに、そこに在り続けるのだと、"
           "私はその日、初めて、身体で分かったような気がいたしました。"),
    "ko": ("제가 이 마을로 돌아온 것은 지난해 가을이었습니다. 역 앞 오래된 상점가는 셔터만 내려져 있고, "
           "아이들 목소리도 들리지 않았습니다. 그러나 산기슭의 그 밤나무는 옛날과 똑같이 열매를 잔뜩 "
           "달고 저를 기다려 주었습니다. 아버지가 심고 어머니가 지키고, 그리고 제가 오십 년 만에 손을 "
           "댄 나무입니다."),
    "en": ("I came back to this village late last autumn. The old shopping street by the station was "
           "all shuttered, and I could not hear a single child's voice. And yet the chestnut tree at "
           "the foot of the mountain was heavy with fruit, just as it had always been, waiting for me. "
           "My father planted it, my mother kept it, and I touched it again after fifty years."),
}


# Mẫu thứ hai: văn KỂ TÀI LIỆU (ngách 都市伝説/vũ trụ). Khác mẫu trên ở đúng chỗ ảnh hưởng tới
# tốc độ đọc: ít dấu phẩy (câu liền hơi), dày kanji + MỐC NĂM + số có đơn vị — mà số đọc thành
# lời rất tốn thời gian ("1957年" = 4 ký tự nhưng đọc "せんきゅうひゃくごじゅうしちねん"). Đo bằng mẫu
# tâm tình rồi đem viết văn tài liệu là tự lệch độ dài ngay từ dòng đầu.
SAMPLE_DOC = {
    "ja": ("1957年10月4日、ソビエト連邦は人類初の人工衛星スプートニク1号の打ち上げに成功しました。"
           "直径わずか58センチ、重さ83.6キログラムの金属球です。しかしこの小さな球体が発した信号音は、"
           "アメリカ全土に衝撃を与えました。当時のアメリカ国防総省は、わずか3か月で対抗計画を承認しています。"
           "ところが公開された記録には、説明のつかない空白の期間が存在するという説があるのです。"
           "1958年2月から11月までの9か月間、関連文書の大半が非公開のままとされています。"
           "この空白の期間に何が起きていたのか。もし本当だったら、私たちが教わってきた宇宙開発の歴史は、"
           "その出発点から書き換えられることになるのかもしれません。"),
}


def sample_text(lang, style="story"):
    if style == "doc" and lang in SAMPLE_DOC:
        return SAMPLE_DOC[lang]
    return SAMPLE.get(lang, SAMPLE["ja"])


def count_chars(text):
    return len(text.replace("\n", "").replace(" ", "").replace("　", ""))


def measure(voice, speed, fx, lang="ja", text=None, keep=True, style="story"):
    """Trả (char_rate, duration, n_chars, file). Gọi TTS thật 1 lần."""
    import openspeaker_tts as osp
    text = text or sample_text(lang, style)
    n = count_chars(text)
    vid = resolve_voice(voice)
    fx = normalize_fx(fx)
    outdir = Path(__file__).resolve().parent.parent / "assets" / "_voice_test"
    outdir.mkdir(parents=True, exist_ok=True)
    p = outdir / f"calib_{vid[-8:]}_{str(speed).replace('.', '')}_{fx}_{style}.mp3"
    print(f"[calibrate] voice={vid} speed={speed} fx={fx} · mẫu {n} chữ ({lang}/{style}) …")
    audio, _ = osp.synthesize(text, voice_id=vid, speed=speed, with_transcript=False,
                              file_name=p.stem)
    p.write_bytes(audio)
    apply_fx(p, fx)
    dur = mp3_seconds(p)
    rate = n / (dur / 60.0)
    print(f"  → {dur:.1f}s ⇒ char_rate = {rate:.1f} chữ/phút "
          f"(script 30' cần {int(rate*30):,} chữ · 25' cần {int(rate*25):,})")
    print(f"  → nghe thử: {p}")
    if not keep:
        p.unlink(missing_ok=True)
    return rate, dur, n, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="", help="id profile → đo giọng của nó và GHI char_rate vào file")
    ap.add_argument("--voice", default="", help="voice_id / tên giọng (bỏ qua profile)")
    ap.add_argument("--speed", type=float, default=0.0)
    ap.add_argument("--fx", default="")
    ap.add_argument("--lang", default="", help="ja/ko/en (mặc định theo profile)")
    ap.add_argument("--no-save", action="store_true", help="chỉ đo, không ghi vào profile")
    ap.add_argument("--style", default="", choices=["", "story", "doc"],
                    help="kiểu văn của mẫu đo: story = tâm tình (mặc định) · doc = kể tài liệu "
                         "(dày kanji + mốc năm). Mặc định lấy theo profile.voice.calib_style.")
    args = ap.parse_args()

    prof = None
    voice, speed, fx, lang = args.voice, args.speed, args.fx, args.lang
    if args.profile:
        prof = profiles.load(args.profile)
        pv, pfx, psp = profiles.voice_conf(prof)
        voice = voice or pv
        speed = speed or psp
        fx = fx or pfx
        lang = lang or prof.get("language", "ja")
    if not voice:
        raise SystemExit("Cần --profile hoặc --voice.")
    speed = speed or 1.0
    fx = fx or "none"
    lang = lang or "ja"

    style = args.style or ((prof or {}).get("voice", {}) or {}).get("calib_style") or "story"
    rate, dur, n, _ = measure(voice, speed, fx, lang, style=style)

    if prof and not args.no_save:
        old = (prof.get("voice", {}) or {}).get("char_rate")
        prof.setdefault("voice", {})["char_rate"] = round(rate, 1)
        prof["voice"]["char_rate_measured_at"] = __import__("datetime").date.today().isoformat()
        prof["voice"]["char_rate_note"] = f"đo thật {n} chữ ({style}) → {dur:.1f}s"
        prof["voice"]["char_rate_speed"] = speed
        profiles.save(prof)
        tgt = profiles.target_chars(prof)
        print(f"  char_rate: {old or '(chưa có)'} → {round(rate,1)} · "
              f"target {profiles.target_minutes(prof)}' = {tgt:,} chữ")


if __name__ == "__main__":
    main()
