#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TVBox-Hub 自动化同步与探活脚本
功能：
1. 拉取上游优质开源配置与直播源
2. 镜像并本地化核心爬虫 Spider Jar 包，生成 MD5 校验
3. 生成自建聚合单仓 index.json 与极速版 lite.json
4. 生成多仓合集 multi.json
5. 执行多仓探活并生成状态报告 upstream_status.json
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DIST_DIR = os.path.join(BASE_DIR, "dist")
JAR_DIR = os.path.join(DIST_DIR, "jar")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 TVBox/1.0"

def clean_idn_url(url: str) -> str:
    """将包含中文字符的域名转化为 Punycode 格式"""
    try:
        parts = urllib.parse.urlsplit(url)
        netloc = parts.netloc.encode("idna").decode("ascii")
        return urllib.parse.urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))
    except Exception:
        return url

def fetch_content(url: str, timeout: int = 12) -> bytes:
    """带重试与 UA 的通用内容下载"""
    target_url = clean_idn_url(url)
    req = urllib.request.Request(target_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def test_url_health(name: str, url: str) -> dict:
    """检测 URL 连通性与响应时间"""
    clean_url = clean_idn_url(url)
    start_time = time.time()
    try:
        req = urllib.request.Request(clean_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=8) as resp:
            latency_ms = int((time.time() - start_time) * 1000)
            status_code = resp.status
            return {
                "name": name,
                "url": url,
                "status": "online" if status_code < 400 else "warning",
                "code": status_code,
                "latency_ms": latency_ms,
                "check_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "name": name,
            "url": url,
            "status": "offline",
            "error": str(e),
            "latency_ms": latency_ms,
            "check_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

def sync():
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(JAR_DIR, exist_ok=True)

    upstream_file = os.path.join(DATA_DIR, "upstream.json")
    if not os.path.exists(upstream_file):
        print(f"[!] 找不到配置文件: {upstream_file}")
        sys.exit(1)

    with open(upstream_file, "r", encoding="utf-8") as f:
        upstream_data = json.load(f)

    print("=" * 60)
    print("▶ 1. 开始同步上游配置与核心 Spider Jar...")
    print("=" * 60)

    # 1. 下载 Spider Jar
    jar_target_path = os.path.join(JAR_DIR, "fan.txt")
    jar_downloaded = False
    jar_md5 = ""

    for source in upstream_data.get("upstream_single_sources", []):
        jar_url = source.get("jar_url")
        if not jar_url:
            continue
        try:
            print(f"[*] 正在拉取 Spider Jar: {jar_url}")
            jar_bytes = fetch_content(jar_url, timeout=20)
            if len(jar_bytes) > 100000:  # 大于 100KB 则视为有效 jar
                with open(jar_target_path, "wb") as f:
                    f.write(jar_bytes)
                jar_md5 = hashlib.md5(jar_bytes).hexdigest()
                print(f"[+] 成功更新 Spider Jar: 大小 {len(jar_bytes)} 字节, MD5: {jar_md5}")
                jar_downloaded = True
                break
        except Exception as e:
            print(f"[-] 拉取 Jar 失败 ({jar_url}): {e}")

    if not jar_downloaded and os.path.exists(jar_target_path):
        with open(jar_target_path, "rb") as f:
            jar_md5 = hashlib.md5(f.read()).hexdigest()
        print(f"[!] 使用本地已有 Jar, MD5: {jar_md5}")

    # 2. 拉取主源并构建 index.json
    base_config = None
    for source in upstream_data.get("upstream_single_sources", []):
        src_url = source.get("url")
        try:
            print(f"[*] 正在拉取上游主配置: {source.get('name')} ({src_url})")
            raw_data = fetch_content(src_url, timeout=15).decode("utf-8")
            parsed = json.loads(raw_data)
            if "sites" in parsed and len(parsed["sites"]) > 0:
                base_config = parsed
                print(f"[+] 成功获取主配置! 包含 {len(base_config['sites'])} 个站点")
                break
        except Exception as e:
            print(f"[-] 拉取主配置失败: {e}")

    if not base_config:
        print("[!] 无法从上游拉取主配置，生成保底配置模板")
        base_config = {
            "spider": f"./jar/fan.txt;md5;{jar_md5}" if jar_md5 else "./jar/fan.txt",
            "wallpaper": "https://bing.img.run/rand.php",
            "sites": [],
            "lives": [],
            "parses": [],
            "rules": []
        }
    else:
        # 重写 spider 引用为本仓库的本地相对路径 (TVBox / 蜂蜜支持相对路径自动解析)
        if jar_md5:
            base_config["spider"] = f"./jar/fan.txt;md5;{jar_md5}"
        else:
            base_config["spider"] = "./jar/fan.txt"

        base_config["wallpaper"] = "https://bing.img.run/rand.php"
        base_config["warningText"] = "TVBox-Hub 自动维护节点，仅供学习交流使用"

    # 3. 写入 dist/index.json
    index_file = os.path.join(DIST_DIR, "index.json")
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(base_config, f, ensure_ascii=False, indent=2)
    print(f"[+] 生成综合主仓配置: {index_file}")

    # 4. 生成极速精简版 dist/lite.json (保留搜索和前 30 个核心站点)
    lite_config = dict(base_config)
    if "sites" in base_config:
        lite_config["sites"] = base_config["sites"][:30]
    lite_file = os.path.join(DIST_DIR, "lite.json")
    with open(lite_file, "w", encoding="utf-8") as f:
        json.dump(lite_config, f, ensure_ascii=False, indent=2)
    print(f"[+] 生成极速精简配置: {lite_file} (保留 {len(lite_config.get('sites', []))} 个站点)")

    # 5. 同步直播源 dist/live.m3u
    print("\n" + "=" * 60)
    print("▶ 2. 同步与校验直播源...")
    print("=" * 60)
    live_downloaded = False
    for live_src in upstream_data.get("live_sources", []):
        url = live_src.get("url")
        try:
            print(f"[*] 正在拉取直播源: {live_src.get('name')} ({url})")
            live_bytes = fetch_content(url, timeout=12)
            if b"#EXTM3U" in live_bytes:
                live_file = os.path.join(DIST_DIR, "live.m3u")
                with open(live_file, "wb") as f:
                    f.write(live_bytes)
                print(f"[+] 成功更新直播源: {live_file} ({len(live_bytes)} 字节)")
                live_downloaded = True
                break
        except Exception as e:
            print(f"[-] 拉取直播源失败: {e}")

    # 6. 生成多仓索引 dist/multi.json 并进行多仓探活
    print("\n" + "=" * 60)
    print("▶ 3. 构建多仓索引并进行健康探活...")
    print("=" * 60)

    multi_urls = []
    health_results = []
    raw_warehouses = upstream_data.get("multi_warehouses", [])

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_map = {
            executor.submit(test_url_health, item["name"], item.get("puny_url") or item["url"]): item
            for item in raw_warehouses
        }
        for future in as_completed(future_map):
            item = future_map[future]
            try:
                res = future.result()
                health_results.append(res)
                status_icon = "🟢" if res["status"] == "online" else "🔴"
                print(f"  {status_icon} [{res['status'].upper()}] {item['name']} - {res.get('latency_ms', 0)}ms")
            except Exception as e:
                health_results.append({"name": item["name"], "url": item["url"], "status": "offline", "error": str(e)})

    # 构建 multi.json (TVBox 多仓标准 urls 列表)
    for item in raw_warehouses:
        multi_urls.append({
            "url": item["url"],
            "name": item["name"]
        })
        # 如果有加速镜像，额外追加一条免翻镜像备用
        if "mirror" in item:
            multi_urls.append({
                "url": item["mirror"],
                "name": f"{item['name']} (加速节点)"
            })

    multi_file = os.path.join(DIST_DIR, "multi.json")
    with open(multi_file, "w", encoding="utf-8") as f:
        json.dump({"urls": multi_urls}, f, ensure_ascii=False, indent=2)
    print(f"\n[+] 生成多仓配置: {multi_file} (共 {len(multi_urls)} 条线路)")

    # 写入健康探活状态 upstream_status.json
    status_file = os.path.join(DIST_DIR, "upstream_status.json")
    with open(status_file, "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "total": len(health_results),
            "results": sorted(health_results, key=lambda x: (x.get("status") != "online", x.get("latency_ms", 99999)))
        }, f, ensure_ascii=False, indent=2)
    print(f"[+] 生成健康探活报告: {status_file}")

    print("\n" + "=" * 60)
    print("✅ 全部同步与生成完毕！")
    print("=" * 60)

if __name__ == "__main__":
    sync()
