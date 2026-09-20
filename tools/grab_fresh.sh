#!/bin/bash
# grab_fresh.sh <needle> <slug> <out_prefix>
# Restart Chrome (graceful + auto-login) RỒI grab_one. Dùng khi degradation nhanh (mỗi grab 1 lần restart).
needle="$1"; slug="$2"; out="$3"
bash /e/CLAUDE/YOUTUBE/h2dev/tools/restart_login.sh 2>&1 | grep -E "closed|LOGIN_OK|LOGIN_FAIL|CDP"
echo "=== grab after fresh ==="
bash /e/CLAUDE/YOUTUBE/h2dev/tools/grab_one.sh "$needle" "$slug" "$out"
