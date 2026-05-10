#!/usr/bin/env python3
import subprocess
import json
import re
from colorama import Fore, Style

class NmapWrapper:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def run_port_scan(self, ports="1-1000"):
        """Basic port scan"""
        print(f"{Fore.CYAN}[*] Running Nmap port scan on {self.target}...")
        try:
            cmd = f"nmap -p {ports} -sV -sC -O {self.target} -oN reports/nmap_scan.txt"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            self.results['port_scan'] = result.stdout
            return self.parse_nmap_output(result.stdout)
        except Exception as e:
            print(f"{Fore.RED}[-] Nmap error: {e}")
            return []
    
    def parse_nmap_output(self, output):
        """Parse Nmap output to extract port info"""
        open_ports = []
        pattern = r"(\d+)/tcp\s+open\s+(\w+)\s+(.*)"
        for line in output.split('\n'):
            match = re.search(pattern, line)
            if match:
                open_ports.append({
                    'port': int(match.group(1)),
                    'service': match.group(2),
                    'version': match.group(3).strip()
                })
        return open_ports
    
    def run_vuln_scan(self):
        """Run Nmap vulnerability scripts"""
        print(f"{Fore.CYAN}[*] Running Nmap vulnerability scan...")
        try:
            cmd = f"nmap --script vuln -p- {self.target} -oN reports/nmap_vulns.txt"
            subprocess.run(cmd, shell=True, timeout=600)
            return True
        except:
            return False
    
    def run_udp_scan(self):
        """UDP port scan"""
        print(f"{Fore.CYAN}[*] Running UDP scan...")
        try:
            cmd = f"nmap -sU --top-ports 100 {self.target} -oN reports/nmap_udp.txt"
            subprocess.run(cmd, shell=True, timeout=300)
            return True
        except:
            return False