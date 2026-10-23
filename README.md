# 📺 TVBox-Hub 壳源分离订阅中心

<p align="center">
  <img src="https://img.shields.io/badge/TVBox-壳源分离-blue?style=flat-square" alt="TVBox">
  <img src="https://img.shields.io/badge/FongMi-原生支持-green?style=flat-square" alt="FongMi">
  <img src="https://img.shields.io/badge/自动维护-GitHub%20Actions-orange?style=flat-square" alt="Actions">
  <img src="https://img.shields.io/badge/状态-每日探活-brightgreen?style=flat-square" alt="Status">
</p>

> 本项目为 **TVBox / 影视仓 / FongMi（蜂蜜）** 等多平台播放器提供高可用、纯净无广告的“壳源分离”订阅合集。
> 依托 **GitHub Actions 每日自动化流水线**，定时同步上游优质源、探活健康状态，并将核心 Spider Jar 镜像缓存至本仓库，杜绝接口失效与上游删库风险。

---

## 🚀 订阅接口地址（开箱即用）

> 💡 **使用提示**：在电视盒子或手机 APP 设置中的「配置地址 / 接口」填入以下任一链接即可。如果直连网络不稳定，请优先使用 **加速节点**。

### 1. 🌟 综合精选主仓（全端通用，电视首选）
*已内置完整爬虫依赖包、豆瓣热榜、优质磁力解析、网盘检索与高清直播*
* **国内极速加速节点 1 (GHFast)**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json
  ```
* **jsDelivr CDN 加速**：
  ```text
  https://cdn.jsdelivr.net/gh/sylvan97/tvbox-hub@main/dist/index.json
  ```
* **GitHub 直连**：
  ```text
  https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json
  ```

---

### 2. 🖥️ PC 电脑桌面专用仓（FreeBox / 电脑端推荐，杜绝弹错）
*针对 Windows / Mac 原生桌面播放器（如 FreeBox、ZY-Player）特别优化，剔除 Android Dalvik 专属的 `csp_` 爬虫，精选 44 个高性能 CMS 影视站与通用 JS 规则，秒开无弹错*
* **国内极速加速节点**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/pc.json
  ```
* **GitHub 直连**：
  ```text
  https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/pc.json
  ```

---

### 3. 🗂️ 聚合多仓（一键切换全网知名源）
*聚合自建仓、饭太硬、肥猫、运输车、摸鱼儿、Qist 等全网顶级源，支持在播放器内随时切换*
* **GitHub 直连**：
  ```text
  https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/multi.json
  ```
* **国内极速加速节点**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/multi.json
  ```

---

### 3. ⚡ 极速精简仓（老旧电视/低配盒子首选）
*仅保留前 30 个响应极快的高质量站点，秒开加载，内存占用极小*
* **加速订阅地址**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/lite.json
  ```

---

### 4. 📡 高清 IPTV 直播源（央视 / 卫视 / 地方台 IPv6）
*精校高清电视台直链，支持各类 IPTV 播放器（如 TiviMate、APTV、PotPlayer、Kodi）*
* **M3U 直播源直连**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/live.m3u
  ```

---

## 📱 常用优质“播放器壳”推荐

> “壳源分离”架构下，播放器本身仅为无内容的纯播放引擎，请前往其官方开源仓库下载：

| 客户端 | 适用平台 | 特点说明 | 官方发布页 |
| :--- | :--- | :--- | :--- |
| **FongMi (蜂蜜)** | Android / Android TV | 原生 Android TV 架构，无任何多余弹窗与广告，极其丝滑流利 | [FongMi/Release](https://github.com/FongMi/Release) |
| **TVBox (Takagen99 版)** | Android / TV | 最成熟的开源 TVBox 分支之一，兼容性极佳，UI 支持高度自定义 | [takagen99/Box](https://github.com/takagen99/Box) |
| **OK影视 / OKPlayer** | Android / TV | 优化解码能力，内置丰富解码内核支持 | [OKCaptain](https://jihulab.com/okcaptain) |
| **影视仓** | Android / TV | 国内广为流传的分支，支持多仓多接口快速切换与远程推流 | 开源社区各版本 |

---

## 🛠️ 配置使用教程

### 在 FongMi（蜂蜜）中配置：
1. 安装并打开 **FongMi**。
2. 点击右上角 **「设置」⚙️ ->「点播」**。
3. 输入上述的 **综合精选单仓** 或 **聚合多仓** 地址，点击确定。
4. 返回首页即可自动加载最新影视分类与站点列表。

### 在 TVBox / 影视仓中配置：
1. 打开 **TVBox**，进入 **「设置」->「配置地址」**。
2. 点击输入框，粘贴复制的订阅 URL（若支持手机扫码推送，可直接扫码粘贴）。
3. 点击 **「确定」** 并返回主界面，配置将自动解析并生效。

---

## 🤖 自动化与维护架构

```text
tvbox-hub/
├── .github/workflows/
│   └── sync.yml              # 每天凌晨 04:00 自动执行同步与健康探活
├── data/
│   └── upstream.json         # 跟踪的上游官方源清单与备选源
├── scripts/
│   └── sync.py               # 核心清洗、探活、Jar 本地化与构建脚本
└── dist/
    ├── index.json            # 核心综合主仓 (本地化 Spider Jar，防失效)
    ├── multi.json            # 聚合多仓 (集成全网顶级主力源)
    ├── lite.json             # 极速精简仓
    ├── live.m3u              # 央卫视高清直播列表
    ├── upstream_status.json  # 每日定时探活健康报告
    └── jar/
        └── fan.txt           # 核心爬虫 Jar 包镜像缓存 (防上游删库)
```

1. **自动探活**：每日自动对所有上游接口进行并发 HTTP 连通性测试与延迟探测，淘汰死链。
2. **Jar 包镜像本地化**：自动抓取主流最新 Spider Jar（如 `fan.txt`）存入本仓库的 `dist/jar/`，并计算实时 MD5 绑定，哪怕原作者接口挂掉也不影响使用。
3. **Punycode 域名兼容**：自动兼容处理如 `饭太硬.top`、`肥猫.live` 等中文域名的 IDN 转码，保证在低版本 Android WebView 下亦可正常请求。

---

## ⚠️ 免责声明

1. 本项目所有配置、规则与数据均由开源社区及网络公开资源整理抓取而来，**仓库本身不存储、不制作、不传播任何视音频内容**。
2. 本项目脚本及生成的配置文件仅供个人学习网络爬虫、JSON 解析、GitHub Actions 自动化流水线之用。
3. 请勿将本项目用于任何商业用途。若任何内容存在版权争议，请联系上游源站点或提交 Issue 予以移除。
