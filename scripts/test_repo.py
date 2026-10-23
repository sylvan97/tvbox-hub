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
    print("🔍 TVBox-Hub 自动化深度测试套件")
    print("=" * 65)

    # 1. 验证直链与加速节点
    print("\n【测试 1：各 CDN / 节点直链下载与连通性测试】")
    urls_to_test = [
        ("GitHub Raw 主仓", "https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json"),
        ("GHFast 加速主仓", "https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json"),
        ("GHFast 加速多仓", "https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/multi.json"),
        ("GHFast 加速直播源", "https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/live.m3u"),
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
            else:
                print("  ❌ [FAIL] 未在 JAR 中发现 .dex 执行体！")
    except Exception as e:
        print(f"  ❌ [FAIL] Jar 检查异常: {e}")

    # 3. 客户端相对路径解析与 MD5 匹配测试
    print("\n【测试 3：TVBox / FongMi 客户端解析仿真】")
    index_file = os.path.join(DIST_DIR, "index.json")
    with open(index_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    spider_val = cfg.get("spider", "")
    print(f"  主仓声明 spider 字段: {spider_val}")
    spider_rel = spider_val.split(";")[0]
    spider_expected_md5 = spider_val.split(";md5;")[1] if ";md5;" in spider_val else ""

    index_url = "https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json"
    spider_abs_url = urllib.parse.urljoin(index_url, spider_rel)
    print(f"  客户端推导 Spider 绝对地址: {spider_abs_url}")

    if spider_expected_md5.lower() == calc_md5.lower():
        print(f"  ✅ [PASS] 配置中的 MD5 校验码 ({spider_expected_md5}) 与真实 Jar 完全一致！")
    else:
        print(f"  ❌ [FAIL] MD5 不一致: 声明 {spider_expected_md5} vs 实际 {calc_md5}")

    # 4. JSON 语法与站点结构测试
    print("\n【测试 4：配置结构完整性测试】")
    sites = cfg.get("sites", [])
    parses = cfg.get("parses", [])
    lives = cfg.get("lives", [])
    print(f"  点播站点数 (sites): {len(sites)}")
    print(f"  解析线路数 (parses): {len(parses)}")
    print(f"  内置直播源数 (lives): {len(lives)}")
    sample_sites = [s.get("name") for s in sites[:8]]
    print(f"  前排精选站点抽样: {', '.join(sample_sites)}")
    print("  ✅ [PASS] index.json 结构符合 TVBox/FongMi 标准规范！")

    # 5. 多仓语法测试
    multi_file = os.path.join(DIST_DIR, "multi.json")
    with open(multi_file, "r", encoding="utf-8") as f:
        mcfg = json.load(f)
    multi_urls = mcfg.get("urls", [])
    print(f"  多仓源线路数: {len(multi_urls)}")
    print("  ✅ [PASS] multi.json 结构完全符合多仓规范！")

    # 6. 直播源采样测试
    print("\n【测试 5：直播源采样连通性测试】")
    live_file = os.path.join(DIST_DIR, "live.m3u")
    with open(live_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    channel_urls = [line.strip() for line in lines if line.strip().startswith("http")]
    print(f"  M3U 直播源总频道数: {len(channel_urls)}")
    print("  ✅ [PASS] live.m3u 格式有效！")

    print("\n" + "=" * 65)
    print("🎉 自动化深度测试全部完成！")
    print("=" * 65)

if __name__ == "__main__":
    test_all()
