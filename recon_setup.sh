#!/bin/bash

# Professional Recon Setup Script
echo "[*] Updating System & Installing Core Packages..."
sudo apt update && sudo apt install -y git curl wget golang-go whois seclists whatweb ffuf amass gobuster theharvester

# Ensure Go binaries are in your PATH
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin' >> ~/.bashrc
source ~/.bashrc

echo "[*] Installing ProjectDiscovery & Advanced Tools..."
# These are often more up-to-date via 'go install' than apt
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest

echo "[*] Installing Gowitness (Screenshots)..."
go install github.com/sensepost/gowitness@latest

# Finalizing SecLists check
if [ ! -d "/usr/share/wordlists/seclists" ]; then
    echo "[!] SecLists not found in default path. Installing..."
    sudo apt install -y seclists
fi

echo "[+] SETUP COMPLETE!"
echo "[!] Please run 'source ~/.bashrc' or restart your terminal before running the Python script."
