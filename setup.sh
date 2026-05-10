#!/bin/bash

# PortHunter - Advanced Pentest Suite
# Setup Script - Creates complete directory structure

set -e  # Stop on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     ██████╗  ██████╗ ██████╗ ████████╗██╗  ██╗██╗   ██╗      ║"
echo "║     ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██║   ██║      ║"
echo "║     ██████╔╝██████╔╝██████╔╝   ██║   ███████║██║   ██║      ║"
echo "║     ██╔═══╝ ██╔══██╗██╔══██╗   ██║   ██╔══██║██║   ██║      ║"
echo "║     ██║     ██║  ██║██║  ██║   ██║   ██║  ██║╚██████╔╝      ║"
echo "║     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝       ║"
echo "║                                                               ║"
echo "║              Advanced Pentest Suite v2.0                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}[!] Running as root...${NC}"
fi

# Create main directory structure
echo -e "${GREEN}[+] Creating PortHunter directory structure...${NC}"

# Create main project directory if not exists
PROJECT_DIR="PortHunter"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create all directories
directories=(
    "core"
    "modules"
    "utils"
    "config"
    "config/wordlists"
    "reports"
    "templates"
    "logs"
    "ai"
    "lib"
    "docs"
    "tests"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    echo -e "${GREEN}  ✓ Created: $dir${NC}"
done

# Create __init__.py files for Python packages
echo -e "${GREEN}[+] Creating Python package files...${NC}"
for dir in core modules utils ai; do
    touch "$dir/__init__.py"
    echo -e "${GREEN}  ✓ Created: $dir/__init__.py${NC}"
done

# Create main Python files
echo -e "${GREEN}[+] Creating main Python files...${NC}"

# main.py
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
PortHunter - Advanced Pentest Suite
Main entry point
"""

import sys
import os
import argparse
from colorama import Fore, Style, init
from core.nmap_wrapper import NmapWrapper
from core.nuclei_wrapper import NucleiWrapper
from core.msf_suggestions import MetasploitSuggester
from core.report_engine import ReportEngine

init(autoreset=True)

def banner():
    print(f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════════════╗
║     🚀 PortHunter - Advanced Pentest Suite v2.0                 ║
║          For Authorized Security Testing Only                   ║
║        Integrated: Nmap | Nuclei | Metasploit                   ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """)

def main():
    banner()
    print(f"{Fore.YELLOW}[!] Use -h for help{Style.RESET_ALL}\n")
    
if __name__ == "__main__":
    main()
EOF
chmod +x main.py

# core/nmap_wrapper.py
cat > core/nmap_wrapper.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import re
from colorama import Fore

class NmapWrapper:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def run_port_scan(self, ports="1-1000"):
        print(f"{Fore.CYAN}[*] Running Nmap port scan on {self.target}...{Fore.RESET}")
        open_ports = []
        try:
            cmd = f"nmap -p {ports} -sV -sC -O {self.target} -oN reports/nmap_scan.txt"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            pattern = r"(\d+)/tcp\s+open\s+(\w+)\s+(.*)"
            for line in result.stdout.split('\n'):
                match = re.search(pattern, line)
                if match:
                    open_ports.append({
                        'port': int(match.group(1)),
                        'service': match.group(2),
                        'version': match.group(3).strip()
                    })
            print(f"{Fore.GREEN}[+] Found {len(open_ports)} open ports{Fore.RESET}")
            return open_ports
        except Exception as e:
            print(f"{Fore.RED}[-] Nmap error: {e}{Fore.RESET}")
            return []
EOF

# core/nuclei_wrapper.py
cat > core/nuclei_wrapper.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
from colorama import Fore

class NucleiWrapper:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
    
    def run_scan(self, template_type="all"):
        print(f"{Fore.CYAN}[*] Running Nuclei scan on {self.target}...{Fore.RESET}")
        try:
            cmd = f"nuclei -u {self.target} -severity critical,high,medium -json -o reports/nuclei_results.json"
            subprocess.run(cmd, shell=True, timeout=600)
            print(f"{Fore.GREEN}[+] Nuclei scan completed{Fore.RESET}")
            return self.vulnerabilities
        except Exception as e:
            print(f"{Fore.RED}[-] Nuclei error: {e}{Fore.RESET}")
            return []
EOF

# core/msf_suggestions.py
cat > core/msf_suggestions.py << 'EOF'
#!/usr/bin/env python3
from colorama import Fore

class MetasploitSuggester:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports
        self.suggestions = []
    
    def suggest_exploits(self):
        print(f"{Fore.CYAN}[*] Generating exploit suggestions...{Fore.RESET}")
        exploit_db = {
            21: {'exploits': ['vsftpd_234_backdoor'], 'commands': ['use exploit/unix/ftp/vsftpd_234_backdoor']},
            22: {'exploits': ['ssh_login'], 'commands': ['use auxiliary/scanner/ssh/ssh_login']},
            445: {'exploits': ['ms17_010_eternalblue'], 'commands': ['use exploit/windows/smb/ms17_010_eternalblue']},
        }
        for port, service in self.ports:
            if port in exploit_db:
                self.suggestions.append({'port': port, 'service': service, **exploit_db[port]})
        print(f"{Fore.GREEN}[+] Found {len(self.suggestions)} exploit suggestions{Fore.RESET}")
        return self.suggestions
    
    def generate_msf_script(self):
        script = "# Metasploit Resource Script\n"
        for s in self.suggestions:
            script += f"\n# Exploit for port {s['port']}\n"
            for cmd in s['commands']:
                script += f"{cmd}\n"
        with open('reports/msf_commands.rc', 'w') as f:
            f.write(script)
        return "reports/msf_commands.rc"
EOF

# core/report_engine.py
cat > core/report_engine.py << 'EOF'
#!/usr/bin/env python3
from datetime import datetime
from colorama import Fore

class ReportEngine:
    def __init__(self, target, scan_data):
        self.target = target
        self.scan_data = scan_data
    
    def generate_html_report(self):
        filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html = f"""<!DOCTYPE html>
<html>
<head><title>PortHunter Report - {self.target}</title>
<style>
body {{font-family: Arial; background:#f0f2f5; margin:20px;}}
.container {{max-width:1200px; margin:auto; background:white; border-radius:10px;}}
.header {{background:linear-gradient(135deg,#667eea,#764ba2); color:white; padding:30px; text-align:center;}}
table {{width:100%; border-collapse:collapse;}}
th,td {{padding:12px; text-align:left; border-bottom:1px solid #ddd;}}
th {{background:#667eea; color:white;}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>🔍 PortHunter Report</h1><p>{self.target} | {datetime.now()}</p></div>
<div style="padding:20px;"><h2>Scan Results</h2><p>Report generated successfully.</p></div>
</div>
</body>
</html>"""
        with open(filename, 'w') as f:
            f.write(html)
        print(f"{Fore.GREEN}[+] Report saved: {filename}{Fore.RESET}")
        return filename
EOF

# Create config/settings.json
cat > config/settings.json << 'EOF'
{
    "threads": 100,
    "timeout": 3,
    "aggressive_mode": false,
    "generate_pdf": false,
    "ai_suggestions": true,
    "max_ports": 65535,
    "common_ports_only": false
}
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
colorama==0.4.6
python-nmap==0.7.1
requests==2.31.0
beautifulsoup4==4.12.2
tabulate==0.9.0
jinja2==3.1.2
tqdm==4.66.1
EOF

# Create README.md
cat > README.md << 'EOF'
# 🔍 PortHunter - Advanced Pentest Suite

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/yourusername/porthunter)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)

## Quick Start

```bash
# Install
chmod +x setup.sh
./setup.sh

# Run
python3 main.py <target> -p 1-1000
