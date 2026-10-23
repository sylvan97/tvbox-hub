import urllib.request
import json
import re

urls = [
    ("饭太硬1", "http://xn--sss604efuw.top/tv"),
    ("饭太硬2", "https://raw.liucn.cc/box/m.json"),
    ("肥猫", "http://xn--z7x900a.live"),
    ("摸鱼", "http://xn--070az07b.xn--fiq52l96f.top"),
    ("运输车", "https://weixine.net/ysc.json"),
    ("OKJack", "https://jihulab.com/okcaptain/kko/raw/main/ok.txt"),
]

for name, u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "okhttp/3.15 TVBox/1.0"})
        with urllib.request.urlopen(req, timeout=6) as r:
            body = r.read()
            print(f"{name} -> 200, length: {len(body)}")
            text = body.decode("utf-8", errors="ignore")[:300]
            print(f"  preview: {text.strip()[:100]}")
    except Exception as e:
        print(f"{name} -> Error: {e}")
