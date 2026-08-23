# 🛡️ PiHoleBlocklist

## One blocklist to rule them all.

PiHoleBlocklist is an automatically maintained, deduplicated Pi-hole blocklist combining trusted community-maintained advertising, tracking, malware, phishing, privacy, telemetry, and threat-intelligence lists.

It is rebuilt automatically from the original sources, so changes made by the original list maintainers are automatically reflected here.

[![Update Blocklist](https://github.com/Bukk1t/PiHoleBlocklist/actions/workflows/update.yml/badge.svg)](https://github.com/Bukk1t/PiHoleBlocklist/actions)
![Domains](https://img.shields.io/badge/domains-16M%2B-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/Bukk1t/PiHoleBlocklist)
![GitHub repo size](https://img.shields.io/github/repo-size/Bukk1t/PiHoleBlocklist)

---

## 📥 Add to Pi-hole

The blocklist is automatically divided into multiple files because GitHub has a 100 MB per-file limit.

### Copy these URLs into Pi-hole

Go to:

Pi-hole → Lists → Add a new list

<!-- BLOCKLIST_START -->
https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist-01.txt
<!-- BLOCKLIST_END -->

These URLs are automatically generated and maintained.

Do not manually add Blocklist-02.txt, Blocklist-03.txt, etc.

If more parts are required, they will automatically appear here.

If parts are no longer required, their URLs will automatically disappear.

After adding the URLs, update Pi-hole Gravity.

---

## 🚀 Features

- Ad blocking
- Tracker blocking
- Malware protection
- Phishing protection
- Privacy protection
- Telemetry blocking
- Threat intelligence
- Newly registered domain blocking
- DGA domain blocking
- Cryptomining protection
- Smart TV / IoT protection
- Persian / Iranian blocklists
- Automatic duplicate removal
- Automatic updates every 3 hours
- Automatic GitHub-safe splitting
- Automatic removal of obsolete parts
- Automatic Pi-hole URL generation
- Automatic statistics generation
- Pi-hole compatible

---

## 🔄 How Automatic Updates Work

Every 3 hours, GitHub Actions rebuilds the entire blocklist from the configured sources.

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
Split into GitHub-safe files
↓
Remove obsolete files
↓
Generate Pi-hole raw URLs
↓
Update README.md
↓
Generate Stats.txt
↓
Commit changes

---

## 🧹 Source Changes Are Automatically Applied

PiHoleBlocklist does not permanently store domains from previous builds.

Every build starts from the current contents of the configured source lists.

That means:

- If a source adds a domain, it can appear in the next build.
- If a source removes a domain, it can disappear in the next build.
- If a source removes a false positive, that domain can disappear automatically.
- If the blocklist becomes smaller, unnecessary parts are automatically deleted.
- If the blocklist grows, additional parts are automatically created.

There is no need to manually edit generated blocklist files.

---

## 📦 Blocklist Parts

Because the complete blocklist can exceed GitHub's 100 MB file limit, it is automatically split into numbered parts.

Example:

Blocklist-01.txt
Blocklist-02.txt
Blocklist-03.txt
Blocklist-04.txt

If a later build only requires three parts:

Blocklist-01.txt
Blocklist-02.txt
Blocklist-03.txt

Blocklist-04.txt is automatically removed.

The README is updated at the same time so that only the currently existing raw URLs are displayed.

---

## 🔗 Raw Blocklist Files

Every generated part is directly compatible with Pi-hole.

Example:

https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist-01.txt

Additional parts follow the same format:

https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist-02.txt
https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist-03.txt
https://raw.githubusercontent.com/Bukk1t/PiHoleBlocklist/main/Blocklist-04.txt

The Add to Pi-hole section above always contains the current list of files.

---

## 📊 Statistics

Stats.txt contains information about the latest successful build.

It includes:

- Last update time
- Number of sources
- Total unique domains
- Number of generated parts
- Size of each part
- Domains contained in each part
- Domains found in each source
- Source-by-source statistics

---

## 🗂️ Sources

All source URLs are maintained in:

sources.txt

The project combines lists covering areas such as:

- Advertising
- Tracking
- Telemetry
- Malware
- Phishing
- Fraud
- Scam domains
- Privacy
- Cryptomining
- Newly registered domains
- DGA domains
- Smart TVs
- IoT devices
- Regional threats
- Other security and nuisance domains

The generated blocklist is a deduplicated aggregation of these sources.

---

## ⚙️ GitHub Actions

The repository uses GitHub Actions to automatically rebuild the blocklist every 3 hours.

The generated files, README URL section, and statistics are updated automatically.

You do not need to run the builder manually.

---

## ⚠️ Generated Files

The following files are generated automatically:

Blocklist-01.txt
Blocklist-02.txt
Blocklist-03.txt
...
Stats.txt

Do not manually edit generated blocklist files.

Changes will be overwritten by the next successful build.

To change what is included in the blocklist, modify:

sources.txt

---

## 📄 Third-Party Sources

PiHoleBlocklist aggregates third-party blocklists maintained by their respective authors.

The original sources retain their respective licenses and terms.

Please refer to sources.txt for the complete list of included sources.

---

## ⭐ Support

If PiHoleBlocklist is useful to you, consider giving the repository a ⭐.

Every star helps the project gain visibility.

---

Automatically built. Automatically updated. Automatically maintained. 
