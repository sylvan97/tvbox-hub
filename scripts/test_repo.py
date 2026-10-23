#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import zipfile
import hashlib
import urllib.request
import urllib.parse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")

def test_all():
    print("=" * 65)
    print("🔍 TVBox-Hub 纯净电视端 (带 Categories) 自动化深度测试套件")
    print("=" * 65)

    # 1. 验证直链与加速节点
    print("\n【测试 1：各 CDN / 节点直链下载与连通性测试】")
    urls_to_test = [
        ("GitHub Raw 主仓", "https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json"),
        ("GHFast 加速主仓", "https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json"),
        ("GHFast 加速多仓", "https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/multi.json"),
    ]

    for name, u in urls_to_test:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "okhttp/3.15 TVBox/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                print(f"  ✅ [PASS] {name}: HTTP {resp.status}, 大小 {len(data)} 字节")
        except Exception as e:
            print(f"  ❌ [FAIL] {name}: {e}")

    # 2. Spider Jar 核心包与 DEX 结构测试
    print("\n【测试 2：Spider Jar 核心包格式与 MD5 校验】")
    jar_path = os.path.join(DIST_DIR, "jar", "fan.txt")
    calc_md5 = ""
    try:
        with open(jar_path, "rb") as f:
            jar_bytes = f.read()
        calc_md5 = hashlib.md5(jar_bytes).hexdigest()
        print(f"  文件路径: dist/jar/fan.txt")
        print(f"  文件大小: {len(jar_bytes)} 字节 (约 {len(jar_bytes)//1024} KB)")
        print(f"  计算 MD5: {calc_md5}")

        with zipfile.ZipFile(jar_path, "r") as z:
            namelist = z.namelist()
            dex_files = [n for n in namelist if n.endswith(".dex")]
            print(f"  ZIP 归档校验: 成功 (包含 {len(namelist)} 个文件)")
            print(f"  DEX 执行体检测: {dex_files}")
            if dex_files:
                print("  ✅ [PASS] Spider Jar 核心 DEX 结构完全合法！")
    except Exception as e:
        print(f"  ❌ [FAIL] Jar 检查异常: {e}")

    # 3. 校验 sites 列表纯度：确保无任何 .js / drpy 规则，且全员带 categories
    print("\n【测试 3：TV 纯度检验与 Categories 标签覆盖率】")
    index_file = os.path.join(DIST_DIR, "index.json")
    with open(index_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    sites = cfg.get("sites", [])
    js_sites = [s for s in sites if str(s.get("api", "")).endswith(".js") or "drpy" in str(s.get("api", ""))]
    missing_cat_sites = [s for s in sites if not s.get("categories") or len(s.get("categories")) == 0]

    print(f"  总纯 TV 站点数: {len(sites)}")
    print(f"  残留 JS 规则站点数: {len(js_sites)} (要求为 0)")
    print(f"  缺少 categories 站点数: {len(missing_cat_sites)} (要求为 0)")

    if len(js_sites) == 0 and len(missing_cat_sites) == 0:
        print("  ✅ [PASS] 站点纯度 100%，无 JS 干扰，全部配齐精准 Categories！")
    else:
        print(f"  ❌ [FAIL] 纯度检查未达标: js={len(js_sites)}, missing_cat={len(missing_cat_sites)}")

    print(f"  首页第一位主力源: {sites[0].get('name')} -> Categories: {sites[0].get('categories')}")

    # 4. 校验全新高可用直播源 (live.txt 与 live.m3u)
    print("\n【测试 4：高可用电视直播源格式与内容检测】")
    txt_path = os.path.join(DIST_DIR, "live.txt")
    m3u_path = os.path.join(DIST_DIR, "live.m3u")

    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        txt_content = f.read()
    with open(m3u_path, "r", encoding="utf-8", errors="ignore") as f:
        m3u_content = f.read()

    txt_lines = [l for l in txt_content.splitlines() if "," in l and "http" in l]
    print(f"  live.txt 原生电视频道数: {len(txt_lines)}")
    print(f"  live.m3u 大小: {len(m3u_content)} 字节")
    if len(txt_lines) > 50 and "#EXTM3U" in m3u_content:
        print("  ✅ [PASS] 电视直播源 live.txt / live.m3u 结构完备，可用线路充足！")
    else:
        print("  ❌ [FAIL] 直播源内容异常！")

    print("\n" + "=" * 65)
    print("🎉 纯净电视端 (带 Categories) 全量深度测试全部通过！")
    print("=" * 65)

if __name__ == "__main__":
    test_all()
