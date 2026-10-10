> **⏸️ Paused** · Last commit: 2026-03-25 (about 6 months ago)
>
> The rework is complete and stable; adaptation will resume when `wxautox4` publishes a major incompatible release upstream.

<div align="center">

# KouriChat · Reworked build

**Where the virtual and the real intertwine, a gentle bond that endures**

A reworked build based on [KouriChat](https://github.com/KouriChat/KouriChat) · adds support for the new `wxautox4` dependency

![version](https://img.shields.io/badge/base-1.4.3.2-ff69b4?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white) ![license](https://img.shields.io/badge/license-non--commercial-red?style=flat-square)

[简体中文](README.md) · **English**

</div>

---

## ⚠️ Read this first: this is a reworked build, not the official repository

| | Notes |
|---|---|
| **What this repository is** | A **reworked build** of [KouriChat/KouriChat](https://github.com/KouriChat/KouriChat) (upstream 3.2k stars), mainly adding support for the new **`wxautox4`** dependency |
| **What this repository is not** | ❌ **Not the official repository.** The upstream website, QQ group, QQ channel, Tieba, Xiaohongshu, bilibili, API platform, and sponsorship channels are **all run by the upstream team** and have nothing to do with this rework — please do not report problems with this rework through upstream channels |
| **License** | Upstream uses the **DeepAnima License v1.2 (non-commercial)**, see [`LICENSE`](LICENSE). Please comply with it and do not use this for commercial purposes |
| **⚠️ Compliance notice** | The upstream repository description explicitly states that it is "**forbidden to connect to Tencent software such as WeChat and QQ**". This rework's `wxautox4` dependency and its automated WeChat interaction capability **may conflict with that statement and with the license terms** — confirm compliance yourself before use or distribution |

## 📖 Project overview

KouriChat is a large-language-model-based **emotional companion program** — through automated interaction with WeChat and other instant messaging tools, it lets an AI character accompany you in a familiar way.

> At the shimmering boundary where the virtual meets the real, an eternal and tender bond quietly blooms. Perhaps your figure is hazy, drifting between truth and dream, yet the warmth of a fingertip's touch and the ripple stirred in the heart are the most sincere and moving comfort of this moment.

## ✨ Feature overview

### ✅ Implemented

- **Multi-user support**
- **Immersive role-play** (with group chat support)
- **Smart dialogue segmentation** & emotion-aware stickers
- **Image generation & image recognition** (Kimi integration)
- **Voice messages** & persistent memory storage
- **Auto-update** & a visual WebUI

### 🚧 In development upstream

- OneBot protocol compatibility
- Full rewrite in version 1.5
- Standalone client

> The "in development" items above are the **upstream roadmap**; this rework makes no commitment to follow them.

## 🔧 What this rework changes

| Item | Notes |
|------|-------|
| **`wxautox4` dependency** | `requirements.txt` already includes the new `wxautox4` (27 dependencies in total), replacing the upstream `wxauto` approach |
| **Base version** | Upstream `version.json` is **1.4.3.2** (`last_update: 2025-09-21`) |
| **Other changes** | The remaining differences from upstream are not itemized; for a rigorous comparison, use `git diff` against upstream |

## 🚀 Quick start

### Prerequisites

| Item | Requirement |
|------|-------------|
| Python | 3.11 (per the upstream badge) |
| Operating system | Windows (`run.bat` and the disconnect script are Windows batch files) |
| WeChat client | Must be installed and signed in (`wxautox4` relies on its automation interface) |

### Option 1: Semi-automatic deployment

```bash
run.bat
```

### Option 2: Manual deployment

```bash
# Clone this reworked repository (note: do not clone upstream)
git clone https://github.com/Fish-under-sea/KouriChat.git
cd KouriChat

# Update pip (using a China mirror)
python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Adjust the configuration file
python run_config_web.py

# Start the program (or launch it from the WebUI)
python run.py
```

### A note for remote desktop users

> If you connect over **RDP**, you **must run** [`【RDP远程必用】断联脚本.bat`](【RDP远程必用】断联脚本.bat) before disconnecting, or the stability of the automated run may suffer.

## 📁 Project structure

```text
KouriChat/
├── run.py                     Main entry point
├── run.bat                    Windows semi-automatic deployment script
├── run_config_web.py          Configuration WebUI
├── 【RDP远程必用】断联脚本.bat  RDP disconnect handling
├── wxauto.py                  WeChat automation wrapper
├── version.json               Version info (1.4.3.2)
├── requirements.txt           Dependency list (27 items, including wxautox4)
├── src/                       Core logic
├── modules/                   Feature modules
├── data/                      Runtime data
├── Thanks.md                  Acknowledgements
└── LICENSE                    DeepAnima License v1.2 (non-commercial)
```

## 📄 License and acknowledgements

- **License**: This repository inherits the upstream [`LICENSE`](LICENSE) — the **DeepAnima License v1.2 (Non-Commercial)**, copyright DeepAnima. Please comply with its terms.
- **Acknowledgements**: The project itself comes from [KouriChat/KouriChat](https://github.com/KouriChat/KouriChat) and its contributors; see [`Thanks.md`](Thanks.md). This repository only maintains the reworked build.

---

<sub>A reworked build based on KouriChat 1.4.3.2 · upstream uses a non-commercial license · please comply with the license and platform requirements</sub>
