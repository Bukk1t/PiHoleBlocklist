# 🛡️ PiHoleBlocklist

## One text file to rule them all.

A single, automatically updated Pi-hole blocklist combining multiple trusted community-maintained security and privacy lists into one optimized file.

[![Update Blocklist](https://github.com/Bukk1t/PiHoleBlocklist/actions/workflows/update.yml/badge.svg)](https://github.com/Bukk1t/PiHoleBlocklist/actions) ![Domains](https://img.shields.io/badge/domains-900k%2B-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/Bukk1t/PiHoleBlocklist) ![GitHub repo size](https://img.shields.io/github/repo-size/Bukk1t/PiHoleBlocklist)

---

## 🚀 Features

✅ Ads blocking  
✅ Tracker blocking  
✅ Malware domain blocking  
✅ Phishing protection  
✅ Threat intelligence feeds  
✅ Automatic daily updates  
✅ Duplicate removal  
✅ Pi-hole compatible  

---

# 📥 Installation

Add this URL to Pi-hole: https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist.txt

---

## 🔄 Automatic Updates

This blocklist is automatically updated every day (Every 24 hours at 00:00 UTC) using GitHub Actions.

The update system:
- Downloads the latest versions of all included sources
- Removes duplicate entries
- Generates a fresh `Blocklist.txt`
- Publishes the updated list automatically

You do not need to manually download a new version.  
If you use the Pi-hole URL given at the top, your Pi-hole will always receive the latest available list when it updates gravity.
