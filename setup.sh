#!/bin/bash

# PortHunter - Advanced Pentest Suite
# Setup Script - Creates complete directory structure

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

echo -e "${GREEN}[+] Creating PortHunter directory structure...${NC}"

# Create main directories
directories=(
    "core"
    "modules"
    "utils"
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

# Create __init__.py files
echo -e "${GREEN}[+] Creating Python package files...${NC}"
for dir in core modules utils ai; do
    touch "$dir/__init__.py"
    echo -e "${GREEN}  ✓ Created: $dir/__init__.py${NC}"
done

# Create main.py
echo -e "${GREEN}[+] Creating main.py...${NC}"
cat > main.py << 'MAINEOF'
#!/usr/bin/env python3
import sys
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════════════╗
║     🚀 PortHunter - Advanced Pentest Suite v2.0                 ║
║          For Authorized Security Testing Only                   ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """)

def main():
    banner()
    parser = argparse.ArgumentParser(description='PortHunter - Advanced Security Scanner')
    parser.add_argument('target', help='Target IP or domain')
    parser.add_argument('-p', '--ports', default='1-1000', help='Port range')
    parser.add_argument('-s', '--scan-type', choices=['quick', 'full', 'vuln'], default='quick')
    args = parser.parse_args()
    
    print(f"{Fore.GREEN}[+] Target: {args.target}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Ports: {args.ports}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Scan Type: {args.scan_type}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
MAINEOF
chmod +x main.py

# Create core/nmap_wrapper.py
echo -e "${GREEN}[+] Creating core/nmap_wrapper.py...${NC}"
cat > core/nmap_wrapper.py << 'NMAPEOF'
#!/usr/bin/env python3
import subprocess
import re
from colorama import Fore

class NmapWrapper:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def run_port_scan(self, ports="1-1000"):
        print(f"{Fore.CYAN}[*] Running Nmap scan on {self.target}...{Fore.RESET}")
        open_ports = []
        try:
            cmd = f"nmap -p {ports} -sV --open {self.target} -oN reports/nmap_scan.txt"
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
NMAPEOF

# Create core/nuclei_wrapper.py
echo -e "${GREEN}[+] Creating core/nuclei_wrapper.py...${NC}"
cat > core/nuclei_wrapper.py << 'NUCLEIEOF'
#!/usr/bin/env python3
import subprocess
from colorama import Fore

class NucleiWrapper:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
    
    def run_scan(self):
        print(f"{Fore.CYAN}[*] Running Nuclei scan...{Fore.RESET}")
        try:
            cmd = f"nuclei -u {self.target} -severity critical,high -o reports/nuclei_results.txt"
            subprocess.run(cmd, shell=True, timeout=600)
            print(f"{Fore.GREEN}[+] Nuclei scan completed{Fore.RESET}")
            return self.vulnerabilities
        except Exception as e:
            print(f"{Fore.RED}[-] Nuclei error: {e}{Fore.RESET}")
            return []
NUCLEIEOF

# Create core/msf_suggestions.py
echo -e "${GREEN}[+] Creating core/msf_suggestions.py...${NC}"
cat > core/msf_suggestions.py << 'MSFEOF'
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
MSFEOF

# Create core/report_engine.py
echo -e "${GREEN}[+] Creating core/report_engine.py...${NC}"
cat > core/report_engine.py << 'REPORTEOF'
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
<head><title>PortHunter Report</title>
<style>
body {{font-family: Arial; background:#f0f2f5;}}
.container {{max-width:1200px; margin:auto; background:white;}}
.header {{background:#667eea; color:white; padding:20px;}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>🔍 PortHunter Report</h1><p>{self.target}</p></div>
</div>
</body>
</html>"""
        with open(filename, 'w') as f:
            f.write(html)
        print(f"{Fore.GREEN}[+] Report saved: {filename}{Fore.RESET}")
        return filename
REPORTEOF

# Create config/settings.json
echo -e "${GREEN}[+] Creating config/settings.json...${NC}"
cat > config/settings.json << 'CONFIGEOF'
{
    "threads": 100,
    "timeout": 3,
    "aggressive_mode": false,
    "ai_suggestions": true,
    "max_ports": 65535
}
CONFIGEOF

# Create requirements.txt
echo -e "${GREEN}[+] Creating requirements.txt...${NC}"
cat > requirements.txt << 'REQEOF'
colorama==0.4.6
python-nmap==0.7.1
requests==2.31.0
beautifulsoup4==4.12.2
tabulate==0.9.0
jinja2==3.1.2
tqdm==4.66.1
REQEOF

# Create .gitignore
echo -e "${GREEN}[+] Creating .gitignore...${NC}"
cat > .gitignore << 'GITEOF'
__pycache__/
*.pyc
reports/*.html
reports/*.txt
reports/*.json
logs/*.log
*.pyc
.DS_Store
venv/
env/
GITEOF

# Create README.md
echo -e "${GREEN}[+] Creating README.md...${NC}"
cat > README.md << 'READMEEOF'
# 🔍 PortHunter - Advanced Pentest Suite

## Quick Start
```bash
chmod +x setup.sh
./setup.sh
python3 main.py scanme.nmap.org -p 1-1000
