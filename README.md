# 👁️ ARGUS
**The All-Seeing Automated Reconnaissance Suite**

Argus is a high-performance wrapper designed to automate the initial phases of infrastructure discovery and vulnerability mapping. It weaves together industry-standard tools into a single, cohesive pipeline, moving from DNS resolution to OSINT, subdomain discovery, web probing, and automated vulnerability scanning.



---

## 🚀 Features
* **Phase 0: DNS Baseline** – Deep DNS query via `dig` to establish the target's footprint.
* **Phase 1: OSINT** – Aggregates metadata using `theHarvester` and `whois`.
* **Phase 2: Subdomain Discovery** – Combines passive (Amass, Subfinder) and active (FFUF) methods.
* **Phase 3: Web Analysis** – Probes for live hosts via `httpx`, fingerprints tech stacks with `WhatWeb`, and captures visual evidence with `GoWitness`.
* **Phase 4: Vulnerability & Content** – Automated template-based scanning with `Nuclei` and spidering with `Katana`.

---

## 🛠️ Prerequisites & Installation

### 1. System Requirements
Argus-Eye is designed to run on **Kali Linux**. Ensure you have `golang` and `python3` installed.

### 2. Automatic Setup
Run the provided setup script to install all dependencies:
```bash
chmod +x recon_setup.sh
./recon_setup.sh
source ~/.bashrc

```

### 3. API Key Configuration (CRITICAL)

To unlock the full power of Argus-Eye, you must configure your **Shodan** and **Censys** keys:

* **Subfinder:** Add keys to `~/.config/subfinder/provider-config.yaml`
* **Amass:** Add keys to `~/.config/amass/config.ini`
* **theHarvester:** Add keys to `/etc/theHarvester/api-keys.yaml`

---

## 🚦 Usage

Run a standard scan against a target domain:

```bash
python3 argus.py -d target.com

```

### Arguments:

* `-d`, `--domain`: The target domain to scan (Required).
* `-o`, `--output`: The base directory for results (Default: `results/`).

---

## 📂 Output Structure

Argus-Eye creates a timestamped folder for every scan:

```text
results/target.com_YYYYMMDD_HHMMSS/
├── dns_records.txt       # Raw DNS answers
├── all_subdomains.txt    # De-duplicated list of all found subs
├── live_hosts.txt        # Verified web servers (with status codes)
├── tech_stack.txt        # Fingerprinting results
├── nuclei_findings.txt   # Critical/High vulnerabilities
└── screenshots/          # Visual captures of the web surface

```

---

## ⚖️ License & Warning

**Disclaimer:** Argus-Eye is intended for authorized security auditing and bug bounty research only. The author is not responsible for any misuse or damage caused by this tool. Always obtain written permission before scanning a target.

```
