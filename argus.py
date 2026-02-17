import subprocess
import os
import argparse
from datetime import datetime

# --- CONFIGURATION ---
TOOLS = {
    "dig": "dig",
    "amass": "amass",
    "subfinder": "subfinder",
    "ffuf": "ffuf",
    "theHarvester": "theHarvester",
    "whois": "whois",
    "whatweb": "whatweb",
    "httpx": "httpx",
    "gowitness": "gowitness",
    "katana": "katana",
    "nuclei": "nuclei",
    "gobuster": "gobuster"
}

WORDLISTS = {
    "subs": "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt",
    "dirs": "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"
}

def run(cmd, desc):
    print(f"\n[*] Starting: {desc}")
    try:
        # timeout 3600 ensures no single tool hangs your system for more than an hour
        subprocess.run(f"timeout 3600 {cmd}", shell=True, check=False)
    except Exception as e:
        print(f"[!] Error during {desc}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Professional Recon Automation")
    parser.add_argument("-d", "--domain", help="Target domain", required=True)
    parser.add_argument("-o", "--output", help="Output directory", default="results")
    args = parser.parse_args()

    target = args.domain
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = f"{args.output}/{target}_{timestamp}"
    os.makedirs(out_dir, exist_ok=True)

    # --- PHASE 0: DNS BASELINE ---
    print(f"\n--- PHASE 0: DNS Resolution (dig) ---")
    run(f"{TOOLS['dig']} {target} ANY +noall +answer > {out_dir}/dns_records.txt", "Querying DNS Records")
    run(f"{TOOLS['dig']} {target} A +short > {out_dir}/root_ips.txt", "Extracting Root IPs")

    # --- PHASE 1: OSINT ---
    print(f"\n--- PHASE 1: OSINT & Metadata ---")
    run(f"{TOOLS['whois']} {target} > {out_dir}/whois.txt 2>/dev/null", "Whois Lookup")
    # Using -b censys,otx,crtsh to use your keys and avoid search engine bans
    run(f"{TOOLS['theHarvester']} -d {target} -l 200 -b censys,otx,crtsh -f {out_dir}/harvester", "theHarvester")

    # --- PHASE 2: SUBDOMAINS ---
    print(f"\n--- PHASE 2: Subdomain Discovery ---")
    run(f"{TOOLS['amass']} enum -passive -d {target} -o {out_dir}/amass_subs.txt", "Amass Passive")
    run(f"{TOOLS['subfinder']} -d {target} -all -silent -o {out_dir}/subfinder_subs.txt", "Subfinder Passive")
    run(f"{TOOLS['ffuf']} -w {WORDLISTS['subs']} -u http://FUZZ.{target} -s -of csv -o {out_dir}/ffuf_subs.csv", "FFUF DNS Brute")

    # --- CONSOLIDATION ---
    print("\n[*] Consolidating subdomains...")
    merge_cmd = f"""
    cat {out_dir}/*.txt 2>/dev/null > {out_dir}/temp_all.txt
    if [ -f {out_dir}/ffuf_subs.csv ]; then 
        tail -n +2 {out_dir}/ffuf_subs.csv | cut -d',' -f2 >> {out_dir}/temp_all.txt
    fi
    cat {out_dir}/temp_all.txt | grep -E '([a-z0-9]+(-[a-z0-9]+)*\\.)+[a-z]{{2,}}' | \
    sed 's/http:\\/\\///g; s/https:\\/\\///g' | sort -u > {out_dir}/all_subdomains.txt
    rm {out_dir}/temp_all.txt
    """
    subprocess.run(merge_cmd, shell=True)

    # --- PHASE 3: LIVE HOSTS & SCREENSHOTS ---
    subs_path = f"{out_dir}/all_subdomains.txt"
    if os.path.exists(subs_path) and os.path.getsize(subs_path) > 0:
        print(f"\n--- PHASE 3: Web Probing ---")
        run(f"cat {subs_path} | {TOOLS['httpx']} -silent -sc -td -title -o {out_dir}/live_hosts.txt", "HTTPX Probing")
        
        live_path = f"{out_dir}/live_hosts.txt"
        if os.path.exists(live_path) and os.path.getsize(live_path) > 0:
            run(f"{TOOLS['whatweb']} -i {live_path} > {out_dir}/tech_stack.txt", "WhatWeb Fingerprinting")
            run(f"{TOOLS['gowitness']} file -f {live_path} --destination {out_dir}/screenshots", "GoWitness Screenshots")
            
            # --- PHASE 4: VULNS & CRAWLING ---
            print(f"\n--- PHASE 4: Vulnerability Scanning ---")
            run(f"{TOOLS['nuclei']} -l {live_path} -severity critical,high -o {out_dir}/nuclei_findings.txt", "Nuclei Scan")
            run(f"{TOOLS['katana']} -list {live_path} -jc -o {out_dir}/endpoints.txt", "Katana Crawling")
    else:
        print("\n[!] No subdomains found for the next phases.")

    print(f"\n--- RECON COMPLETE ---")
    print(f"Results saved to: {out_dir}")

if __name__ == "__main__":
    main()