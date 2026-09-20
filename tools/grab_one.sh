#!/bin/bash
# grab_one.sh <needle> <slug_hint> <out_prefix>
# Bọc grab_lesson.py bằng timeout cứng + retry 3x + dọn python treo. Tự chữa hang.
needle="$1"; slug="$2"; out="$3"; wav="${out}.wav"
tools="/e/CLAUDE/YOUTUBE/h2dev/tools"
base=$(basename "$out")
rm -f "$wav"
cd "$tools" || exit 1
for i in 1 2 3; do
  echo "=== grab attempt $i ($base) ==="
  timeout --kill-after=15 340 py -3.13 grab_lesson.py "$needle" "$slug" "$out"
  # dọn python còn treo cho bài này (nếu timeout để sót)
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Where-Object { \$_.CommandLine -like '*${base}*' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" 2>/dev/null
  if [ -f "$wav" ] && [ $(stat -c%s "$wav") -gt 1500000 ]; then echo "GRABBED_OK: $wav ($(stat -c%s "$wav") bytes)"; exit 0; fi; rm -f "$wav"
  echo "attempt $i: no wav, retry"; sleep 3
done
echo "GRAB_FAILED after 3 attempts"; exit 1
