# 📺 TVBox-Hub 纯净电视端订阅中心 (TV Dedicated)

<p align="center">
  <img src="https://img.shields.io/badge/TVBox-大屏原生-blue?style=flat-square" alt="TVBox">
  <img src="https://img.shields.io/badge/FongMi-官方适配-green?style=flat-square" alt="FongMi">
  <img src="https://img.shields.io/badge/特性-全站带Categories-brightgreen?style=flat-square" alt="Categories">
  <img src="https://img.shields.io/badge/直播-高可用IPv4%2Fv6-orange?style=flat-square" alt="IPTV">
  <img src="https://img.shields.io/badge/维护-每日Actions自动更新-blueviolet?style=flat-square" alt="Actions">
</p>

> **专注电视大屏体验**：专为 **TVBox / 影视仓 / FongMi（蜂蜜）** 定制。
> 彻底移除所有杂乱无章的 JS / drpy 干扰规则，纯享原生 Spider Jar（`fan.txt`）高速解析。
> **全站自带标准化大屏分类（Categories）**，换台与筛选极度丝滑；每日自动同步高可用央卫视直播源。

---

## 🚀 电视端订阅接口（开箱即用）

> 💡 **使用提示**：在电视盒子或手机 APP 设置中的「配置地址 / 接口」填入以下任一链接即可。

### 1. 🌟 纯净电视精选主仓（强烈推荐，主力首选）
*已内置完整爬虫依赖、玩偶哥哥 4K 弹幕、厂长资源、低端外剧、夸克/阿里网盘、全站带精选 Categories，并自带国内高可用央卫视直播*
* **国内极速加速节点 (GHFast)**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json
  ```
* **jsDelivr CDN 节点**：
  ```text
  https://cdn.jsdelivr.net/gh/sylvan97/tvbox-hub@main/dist/index.json
  ```
* **GitHub 原生直链**：
  ```text
  https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/index.json
  ```

---

### 2. 🗂️ 聚合多仓（一键切换全网知名源）
*聚合自建仓、饭太硬、肥猫、高天流云、Qist、运输车等顶级电视源，支持在播放器内一键下拉切换*
* **国内极速加速节点**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/multi.json
  ```
* **GitHub 原生直链**：
  ```text
  https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/multi.json
  ```

---

### 3. ⚡ 极速精简仓（老人房 / 低配盒子首选）
*仅精选前 20 个响应极快的高质量站点，全站带 Categories 结构，秒开加载*
* **加速订阅地址**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/lite.json
  ```

---

### 4. 📡 电视高可用直播源（每日自动探活）
*自动测试可用性，央视、卫视、地方台及超清 4K，兼容普通 IPv4 与 IPv6 宽带网络*
* **TVBox 原生 TXT 直播源（换台秒切首选）**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/live.txt
  ```
* **通用 M3U 播放列表（TiviMate / APTV / PotPlayer 等）**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/sylvan97/tvbox-hub/main/dist/live.m3u
  ```

---

## ✨ 纯电视端优化特色

1. **专注 TV 原生，彻底剔除 JS 规则**：
   * 移除了导致报错的外部 `.js` 与 `drpy` 干扰源，所有站点均由原汁原味的 Android Spider Jar（`dist/jar/fan.txt`，已缓存至本仓库并绑定 MD5）驱动，纯净高速。
2. **全站配备结构化 Categories（分类标签）**：
   * 每个影视站点均规范配置了大屏专用的 `categories` 标签（如 `4K专区`、`电影`、`电视剧`、`国产剧`、`欧美剧`、`动漫`、`综艺` 等），电视遥控器左右切分类直观清晰，告别杂乱冗余的原始标签。
3. **真实高可用直播源**：
   * 采用每日自动测速探活源，淘汰已失效源，同时提供电视盒子原生支持的 `live.txt` 与标准流媒体 `live.m3u`。

---

## 📱 推荐“播放器壳”

| 客户端 | 适用平台 | 特点说明 | 官方发布页 |
| :--- | :--- | :--- | :--- |
| **FongMi (蜂蜜)** | Android / Android TV | 原生大屏 Leanback 架构，最丝滑纯净无广告 | [FongMi/Release](https://github.com/FongMi/Release) |
| **TVBox (Takagen99 版)** | Android / TV | 最成熟的开源电视分支，兼容性极佳 | [takagen99/Box](https://github.com/takagen99/Box) |
| **影视仓** | Android / TV | 国内大屏流行分支，支持多仓与手机推送 | 开源社区各版本 |

---

## 🛠️ 配置使用教程

### 在 FongMi（蜂蜜）中配置：
1. 打开 **FongMi** -> 点击右上角 **「设置」⚙️ ->「点播」**。
2. 粘贴上述 **纯净电视精选主仓** 链接，点击确定。
3. 返回主页即可看到精选分类及 4K 影视内容。
4. 在「直播」中自动加载内置的探活直播源。

### 在 TVBox / 影视仓中配置：
1. 打开 **TVBox** -> 进入 **「设置」->「配置地址」**。
2. 粘贴上述订阅链接 -> 点击 **「确定」** 即可。

---

## ⚠️ 免责声明

1. 本项目所有数据及规则均来源于开源社区及网络公开资源，**仓库本身不制作、不存储任何音视频文件**。
2. 仓库仅供个人学习开源播放器协议及 GitHub Actions 流水线之用，请勿用于任何商业用途。
