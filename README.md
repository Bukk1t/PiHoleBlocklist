# 🛡️ PiHoleBlocklist

## One blocklist to rule them all.

A single, automatically updated Pi-hole blocklist combining trusted community-maintained **ad, tracker, malware, phishing, privacy, and threat-intelligence lists** into one deduplicated collection.

[![Update Blocklist](https://github.com/Bukk1t/PiHoleBlocklist/actions/workflows/update.yml/badge.svg)](https://github.com/Bukk1t/PiHoleBlocklist/actions)
![Domains](https://img.shields.io/badge/domains-16M%2B-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/Bukk1t/PiHoleBlocklist)
![GitHub repo size](https://img.shields.io/github/repo-size/Bukk1t/PiHoleBlocklist)

---

## 🚀 Features

- ✅ Ad blocking
- ✅ Tracker blocking
- ✅ Malware protection
- ✅ Phishing protection
- ✅ Threat intelligence
- ✅ Privacy protection
- ✅ Newly registered domain blocking
- ✅ DGA domain blocking
- ✅ Duplicate removal
- ✅ Automatic updates every 3 hours
- ✅ Pi-hole compatible
- ✅ Automatically split into GitHub-safe files
- ✅ Automatically removes obsolete blocklist parts

---

## 📥 Installation

Because GitHub has a **100 MB per-file limit**, the blocklist is automatically split into multiple files.

Add the following URLs to your Pi-hole blocklists:

<!-- BLOCKLIST_START -->

The blocklist parts are generated automatically.

<!-- BLOCKLIST_END -->

Then update **Pi-hole Gravity** to download the latest lists.

> **You do not need to manually update the URLs.**
>
> When the blocklist changes, the generated parts and this section are automatically updated.

---

## 🔄 Automatic Updates

PiHoleBlocklist is automatically rebuilt and published **every 3 hours** using GitHub Actions.

Each update:

1. Downloads the latest versions of all configured source lists.
2. Extracts valid domains.
3. Validates domains.
4. Removes duplicates.
5. Sorts the final domain list.
6. Splits the list into GitHub-safe parts.
7. Removes obsolete parts from previous builds.
8. Automatically updates the blocklist URLs in this README.
9. Generates updated statistics.
10. Commits the new files to the repository.

If a source removes false positives, those domains will disappear from PiHoleBlocklist during the next successful build.

Likewise, if the total list becomes smaller and fewer parts are required, unused `Blocklist-XX.txt` files are automatically deleted.

If the list grows, new parts are automatically created and added to this README.

---

## 📊 Statistics

The repository includes [`Stats.txt`](Stats.txt), containing information about the latest successful build.

Statistics include:

- Total number of sources
- Total unique domains
- Number of generated blocklist parts
- Domains in each part
- Size of each part
- Domains found in each source
- Last update time

---

## 📦 Blocklist Parts

The blocklist is stored as:

```text
Blocklist-01.txt
Blocklist-02.txt
Blocklist-03.txt
...
