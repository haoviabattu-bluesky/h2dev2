# -*- coding: utf-8 -*-
r"""Chạy tools/channel_branding.py trên profile ADSPOWER thay vì GPM (kênh mail nằm trong AdsPower).

KENH.json khai "browser": {"kind": "adspower", "user_id": "<id>"}. Profile đang mở thì nối vào ws sẵn có,
chưa mở thì start. KHÔNG đóng profile khi xong (giữ phiên anh đang dùng).
  py -3.13 tools\channel_branding_ads.py --config assets\...\KENH.json --steps profile,settings --no-sheet
"""
import json
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import channel_branding as cb

ADS = "http://local.adspower.net:50325/api/v1/browser"


def _uid():
    cfg = json.load(open(sys.argv[sys.argv.index("--config") + 1], encoding="utf-8"))
    b = cfg.get("browser") or {}
    if b.get("kind") != "adspower" or not b.get("user_id"):
        raise SystemExit("KENH.json thiếu browser.kind=adspower + user_id")
    return b["user_id"]


def ads_ws(uid):
    j = requests.get(f"{ADS}/active", params={"user_id": uid}, timeout=30).json()
    if j.get("code") == 0 and j["data"].get("status") == "Active":
        return j["data"]["ws"]["puppeteer"]
    j = requests.get(f"{ADS}/start", params={"user_id": uid}, timeout=120).json()
    if j.get("code") != 0:
        raise RuntimeError(f"AdsPower start fail: {j.get('msg')}")
    return j["data"]["ws"]["puppeteer"]


if __name__ == "__main__":
    uid = _uid()
    cb.find_gpm_profile = lambda mail: uid
    cb.safe_gpm_start = ads_ws
    cb.gpm_stop = lambda pid: print("    (AdsPower: giữ profile mở)")
    sys.exit(cb.main())
