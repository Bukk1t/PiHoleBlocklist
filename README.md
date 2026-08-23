# 🛡️ PiHoleBlocklist

## One blocklist to rule them all.

PiHoleBlocklist is an automatically maintained, deduplicated Pi-hole blocklist combining trusted community-maintained advertising, tracking, malware, phishing, privacy, telemetry, and threat-intelligence lists.

It is rebuilt automatically from the configured sources, so changes made by the original list maintainers are automatically reflected here.

[![Update Blocklist](https://github.com/Bukk1t/PiHoleBlocklist/actions/workflows/update.yml/badge.svg)](https://github.com/Bukk1t/PiHoleBlocklist/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/Bukk1t/PiHoleBlocklist)
![GitHub repo size](https://img.shields.io/github/repo-size/Bukk1t/PiHoleBlocklist)

---

## 📥 Add to Pi-hole

Go to:

**Pi-hole → Lists → Add a new list**

Add:

https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist.txt

Then update Pi-hole Gravity.

---

## 🚀 Features

- Ad blocking
- Tracker blocking
- Malware protection
- Phishing protection
- Privacy protection
- Telemetry blocking
- Threat intelligence
- Cryptomining protection
- Smart TV / IoT protection
- Persian / Iranian protection
- Automatic duplicate removal
- Automatic updates every 3 hours
- Automatic domain validation
- Automatic statistics generation
- Pi-hole compatible

---

## 🔄 How Automatic Updates Work

Every 3 hours, GitHub Actions rebuilds the entire blocklist from the configured sources.

```text
sources.txt
    ↓
Download latest sources
    ↓
Extract valid domains
    ↓
Validate domains
    ↓
Remove duplicates
    ↓
Sort domains
    ↓
Generate Blocklist.txt
    ↓
Generate Stats.txt
    ↓
Commit changes
