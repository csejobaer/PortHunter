#!/usr/bin/env python3
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
║     🚀 Advanced Pentest Suite - Professional Edition v2.0       ║
║          For Authorized Security Testing Only                   ║
║        Integrated: Nmap | Nuclei | Metasploit | Burp            ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """)

def check_dependencies():
    """Check if required tools are installed"""
    tools = ['nmap', 'nuclei', 'msfconsole']
    missing = []
    
    for tool in tools:
        if os.system(f"which {tool} > /dev/null 2>&1") != 0:
            missing.append(tool)
    
    if missing:
        print(f"{Fore.YELLOW}[!] Missing tools: {', '.join(missing)}")
        print(f"{Fore.YELLOW}[!] Install with: sudo apt-get install {' '.join(missing)}")
        return False
    return True

def main():
    banner()
    
    parser = argparse.ArgumentParser(description='Advanced Pentest Suite')
    parser.add_argument('target', help='Target IP or domain')
    parser.add_argument('-p', '--ports', default='1-1000', help='Port range (default: 1-1000)')
    parser.add_argument('-s', '--scan-type', choices=['quick', 'full', 'vuln'], default='quick')
    parser.add_argument('-o', '--output', help='Output directory')
    args = parser.parse_args()
    
    target = args.target
    ports = args.ports
    
    print(f"{Fore.GREEN}[+] Target set to: {target}")
    print(f"{Fore.GREEN}[+] Port range: {ports}")
    
    # Create directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Step 1: Nmap scan
    nmap = NmapWrapper(target)
    open_ports = nmap.run_port_scan(ports)
    
    if not open_ports:
        print(f"{Fore.RED}[-] No open ports found. Exiting.")
        sys.exit(1)
    
    # Step 2: Run vulnerability scan if needed
    if args.scan_type == 'vuln' or args.scan_type == 'full':
        nmap.run_vuln_scan()
    
    # Step 3: Nuclei scan
    nuclei = NucleiWrapper(target)
    vulnerabilities = nuclei.run_scan()
    
    # Step 4: Metasploit suggestions
    msf = MetasploitSuggester(target, [(p['port'], p['service']) for p in open_ports])
    exploits = msf.suggest_exploits()
    msf.generate_msf_script()
    
    # Step 5: Prepare scan data
    scan_data = {
        'open_ports': [{'port': p['port'], 'service': p['service'], 'version': p['version'], 'risk': 'High' if p['port'] in [21,22,23,445,3389,3306] else 'Medium'} for p in open_ports],
        'vulnerabilities': vulnerabilities,
        'exploits': [{
            'port': e['port'],
            'service': e['service'],
            'name': f"Exploit for {e['service']}",
            'severity': 'Critical' if e['port'] in [445,3389] else 'High',
            'description': f"Multiple exploits available for {e['service']} on port {e['port']}",
            'msf_commands': e['msf_commands'],
            'suggestions': [
                f"Upgrade {e['service']} to latest version",
                "Apply security patches",
                f"Restrict access to port {e['port']}",
                "Monitor for suspicious activities"
            ]
        } for e in exploits]
    }
    
    # Step 6: Generate report
    report = ReportEngine(target, scan_data)
    html_report = report.generate_html_report()
    commands_file = report.generate_commands_file()
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}[✓] Scan completed successfully!")
    print(f"{Fore.GREEN}[✓] Report: {html_report}")
    print(f"{Fore.GREEN}[✓] Commands: {commands_file}")
    print(f"{Fore.GREEN}[✓] Open ports found: {len(open_ports)}")
    print(f"{Fore.GREEN}[✓] Vulnerabilities found: {len(vulnerabilities)}")
    print(f"{Fore.GREEN}[✓] Exploits suggested: {len(exploits)}")
    print(f"{Fore.GREEN}{'='*60}\n")
    
    print(f"{Fore.YELLOW}[!] Legal Disclaimer: Only use this tool on systems you own or have written permission to test{Style.RESET_ALL}")

if __name__ == "__main__":
    main()