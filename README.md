# 🛡️ PiHoleBlocklist

## One blocklist to rule them all.

A single, automatically updated Pi-hole blocklist that combines multiple trusted community-maintained security, privacy, and malware blocklists into one optimized file.

[![Update Blocklist](https://github.com/Bukk1t/PiHoleBlocklist/actions/workflows/update.yml/badge.svg)](https://github.com/Bukk1t/PiHoleBlocklist/actions) ![Domains](https://img.shields.io/badge/domains-900k%2B-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/Bukk1t/PiHoleBlocklist) ![GitHub repo size](https://img.shields.io/github/repo-size/Bukk1t/PiHoleBlocklist)

---

## 🚀 Features

* ✅ Ad blocking
* ✅ Tracker blocking
* ✅ Malware domain blocking
* ✅ Phishing protection
* ✅ Threat intelligence feeds
* ✅ Automatic updates every 3 hours
* ✅ Duplicate removal
* ✅ Pi-hole compatible

---

## 📥 Installation

Add the following URL to your Pi-hole **Blocklist**:

```text
https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist.txt
```

Then update Pi-hole Gravity to download the latest version.

---

## 🔄 Automatic Updates

This blocklist is automatically rebuilt and published **every 3 hours** using GitHub Actions.

Each update:

* Downloads the latest versions of all included source lists
* Merges them into a single blocklist
* Removes duplicate entries
* Generates a fresh `Blocklist.txt`
* Automatically publishes the updated file to GitHub

As long as your Pi-hole is configured to use the URL above, it will always receive the latest version the next time Gravity is updated.

---

## 📊 Statistics

The repository also includes a `Stats.txt` file containing information about the latest build, including the total number of unique domains after deduplication.
