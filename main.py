cat > main.py << 'MAINEOF'
#!/usr/bin/env python3
import sys
import os
import argparse
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Import modules
from core.nmap_wrapper import NmapWrapper
from core.nuclei_wrapper import NucleiWrapper
from core.msf_suggestions import MetasploitSuggester
from core.report_engine import ReportEngine

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
    
    parser = argparse.ArgumentParser(description='PortHunter - Advanced Security Scanner')
    parser.add_argument('target', help='Target IP or domain')
    parser.add_argument('-p', '--ports', default='1-1000', help='Port range (default: 1-1000)')
    parser.add_argument('-s', '--scan-type', choices=['quick', 'full', 'vuln'], default='quick', 
                        help='Scan type: quick(1-1000), full(1-65535), vuln(vulnerability scan)')
    parser.add_argument('-o', '--output', help='Output directory', default='reports')
    parser.add_argument('--no-nuclei', action='store_true', help='Skip Nuclei scan')
    parser.add_argument('--no-msf', action='store_true', help='Skip Metasploit suggestions')
    
    args = parser.parse_args()
    
    # Set port range based on scan type
    if args.scan_type == 'full':
        ports = '1-65535'
    elif args.scan_type == 'vuln':
        ports = '20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443'
    else:
        ports = args.ports
    
    print(f"{Fore.GREEN}[+] Target: {args.target}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Ports: {ports}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Scan Type: {args.scan_type}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print("")
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    
    # Step 1: Nmap Port Scan
    print(f"{Fore.YELLOW}[1/4] Starting Nmap port scan...{Style.RESET_ALL}")
    nmap = NmapWrapper(args.target)
    open_ports = nmap.run_port_scan(ports)
    
    if not open_ports:
        print(f"{Fore.RED}[-] No open ports found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Trying quick scan on common ports...{Style.RESET_ALL}")
        open_ports = nmap.run_port_scan('20,21,22,23,25,53,80,443,8080')
        
        if not open_ports:
            print(f"{Fore.RED}[-] Target seems down or filtered. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
    
    print(f"{Fore.GREEN}[+] Found {len(open_ports)} open ports{Style.RESET_ALL}")
    print("")
    
    # Display open ports
    print(f"{Fore.CYAN}Open Ports:{Style.RESET_ALL}")
    for p in open_ports:
        print(f"  📡 Port {p['port']}: {p['service']} - {p['version']}")
    print("")
    
    # Step 2: Vulnerability Scan (Nuclei)
    vulnerabilities = []
    if not args.no_nuclei and args.scan_type in ['full', 'vuln']:
        print(f"{Fore.YELLOW}[2/4] Running Nuclei vulnerability scan...{Style.RESET_ALL}")
        nuclei = NucleiWrapper(args.target)
        vulnerabilities = nuclei.run_scan()
        print(f"{Fore.GREEN}[+] Found {len(vulnerabilities)} potential vulnerabilities{Style.RESET_ALL}")
        print("")
    else:
        print(f"{Fore.YELLOW}[2/4] Skipping Nuclei scan{Style.RESET_ALL}")
        print("")
    
    # Step 3: Metasploit Exploit Suggestions
    exploits = []
    if not args.no_msf:
        print(f"{Fore.YELLOW}[3/4] Generating exploit suggestions...{Style.RESET_ALL}")
        msf = MetasploitSuggester(args.target, [(p['port'], p['service']) for p in open_ports])
        exploits = msf.suggest_exploits()
        msf.generate_msf_script()
        print(f"{Fore.GREEN}[+] Generated {len(exploits)} exploit suggestions{Style.RESET_ALL}")
        print("")
    else:
        print(f"{Fore.YELLOW}[3/4] Skipping Metasploit suggestions{Style.RESET_ALL}")
        print("")
    
    # Step 4: Generate Report
    print(f"{Fore.YELLOW}[4/4] Generating HTML report...{Style.RESET_ALL}")
    
    scan_data = {
        'target': args.target,
        'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'open_ports': open_ports,
        'vulnerabilities': vulnerabilities,
        'exploits': exploits,
        'scan_type': args.scan_type
    }
    
    report_engine = ReportEngine(args.target, scan_data)
    report_file = report_engine.generate_html_report()
    
    # Final summary
    print("")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ SCAN COMPLETED!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Summary:{Style.RESET_ALL}")
    print(f"  🎯 Target: {args.target}")
    print(f"  🔓 Open Ports: {len(open_ports)}")
    print(f"  ⚠️  Vulnerabilities: {len(vulnerabilities)}")
    print(f"  💣 Exploits: {len(exploits)}")
    print(f"  📄 Report: {report_file}")
    print("")
    print(f"{Fore.YELLOW}💡 Next Steps:{Style.RESET_ALL}")
    print(f"  1. Open the HTML report: firefox {report_file}")
    print(f"  2. Check Metasploit commands: cat reports/msf_commands.rc")
    print(f"  3. Run additional scans: nmap -sV -sC -A {args.target}")
    print("")
    print(f"{Fore.RED}⚠️  Legal: Only test systems you own or have permission!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
MAINEOF
