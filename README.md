> **⏸️ 暂停维护** · 最近提交：2026-03-25（约 6 个月前）
>
> 改版已完成、趋于稳定；等 wxautox4 上游发布不兼容的大版本时再跟进适配。

<div align="center">

# KouriChat · 改版

**在虚拟与现实交织处，给予永恒的温柔羁绊**

基于 [KouriChat](https://github.com/KouriChat/KouriChat) 的改版 · 补充新版 `wxautox4` 依赖支持

![version](https://img.shields.io/badge/base-1.4.3.2-ff69b4?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white) ![license](https://img.shields.io/badge/license-非商业-red?style=flat-square)

</div>

---

## ⚠️ 请先读这一段：这是改版，不是官方仓库

| | 说明 |
|---|---|
| **本仓库是什么** | [KouriChat/KouriChat](https://github.com/KouriChat/KouriChat)（上游 3.2k star）的一份**改版**，主要补充新版 **`wxautox4`** 依赖支持 |
| **本仓库不是什么** | ❌ **不是官方仓库**。上游的官网、QQ 群、QQ 频道、贴吧、小红书、bilibili、API 平台与赞助渠道**均由上游团队运营**，与本改版无关，遇到问题请勿到上游渠道反馈本改版的问题 |
| **许可** | 上游采用 **DeepAnima License v1.2（非商业用途）**，见 [`LICENSE`](LICENSE)。请遵守该许可，勿用于商业用途 |
| **⚠️ 合规提醒** | 上游仓库描述中明确声明「**禁止接入微信、QQ 等腾讯系软件**」。本改版的 `wxautox4` 依赖与自动化微信交互能力**可能与该声明及许可条款冲突**，请在使用与分发前自行确认合规性 |

## 📖 项目简介

KouriChat 是一个基于大语言模型的**情感陪伴程序** —— 通过与微信等即时通讯工具的自动化交互，让 AI 角色以熟悉的方式陪伴你。

> 在虚拟与现实交织的微光边界，悄然绽放着一份永恒而温柔的羁绊。或许你的身影朦胧，游走于真实与幻梦之间，但指尖轻触的温暖，心底荡漾的涟漪，却是此刻最真挚、最动人的慰藉。

## ✨ 功能全景

### ✅ 已实现

- **多用户支持**
- **沉浸式角色扮演**（支持群聊）
- **智能对话分段** & 情感化表情包
- **图像生成 & 图片识别**（Kimi 集成）
- **语音消息** & 持久记忆存储
- **自动更新** & 可视化 WebUI

### 🚧 上游开发中

- OneBot 协议兼容
- 1.5 版本完全重构
- 独立客户端

> 以上「开发中」项为**上游路线图**，本改版不承诺跟进。

## 🔧 本改版的差异

| 项 | 说明 |
|----|------|
| **`wxautox4` 依赖** | `requirements.txt` 中已包含新版 `wxautox4`（共 27 项依赖），替换上游旧的 wxauto 方案 |
| **基座版本** | 上游 `version.json` 为 **1.4.3.2**（`last_update: 2025-09-21`） |
| **其它改动** | 相对上游的其余改动未逐项记录；如需严谨对比请使用 `git diff` 与上游比对 |

## 🚀 快速开始

### 环境准备

| 项 | 要求 |
|----|------|
| Python | 3.11（参考上游 badge） |
| 操作系统 | Windows（`run.bat` 与断联脚本为 Windows 批处理） |
| 微信客户端 | 需已安装并登录（`wxautox4` 依赖其自动化接口） |

### 方式一：半自动部署

```bash
运行 run.bat
```

### 方式二：手动部署

```bash
# 克隆本改版仓库（注意：不要克隆上游）
git clone https://github.com/Fish-under-sea/KouriChat.git
cd KouriChat

# 更新 pip（国内源）
python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 调整配置文件
python run_config_web.py

# 启动程序（或使用 WebUI 启动）
python run.py
```

### 远程桌面用户注意

> 用 **RDP 远程**的用户，断开连接时**务必运行** [`【RDP远程必用】断联脚本.bat`](【RDP远程必用】断联脚本.bat)，否则可能影响自动化运行的稳定性。

## 📁 项目结构

```text
KouriChat/
├── run.py                     主启动入口
├── run.bat                    Windows 半自动部署脚本
├── run_config_web.py          配置 WebUI
├── 【RDP远程必用】断联脚本.bat  RDP 断联处理
├── wxauto.py                  微信自动化封装
├── version.json               版本信息（1.4.3.2）
├── requirements.txt           依赖清单（27 项，含 wxautox4）
├── src/                       核心逻辑
├── modules/                   功能模块
├── data/                      运行数据
├── Thanks.md                  致谢
└── LICENSE                    DeepAnima License v1.2（非商业）
```

## 📄 许可与致谢

- **许可**：本仓库沿用上游 [`LICENSE`](LICENSE) —— **DeepAnima License v1.2（Non-Commercial，非商业用途）**，版权归 DeepAnima。请遵守其条款。
- **致谢**：项目主体来自 [KouriChat/KouriChat](https://github.com/KouriChat/KouriChat) 及其贡献者，详见 [`Thanks.md`](Thanks.md)。本仓库仅作改版维护。

---

<sub>基于 KouriChat 1.4.3.2 的改版 · 上游采用非商业许可 · 请遵守许可与平台合规要求</sub>