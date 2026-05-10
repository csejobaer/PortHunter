#!/usr/bin/env python3
import subprocess
import json
from colorama import Fore

class NucleiWrapper:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
    
    def run_scan(self, template_type="all"):
        """Run Nuclei vulnerability scan"""
        print(f"{Fore.CYAN}[*] Running Nuclei scan on {self.target}...")
        
        templates = {
            "critical": "-tags critical",
            "high": "-severity high",
            "medium": "-severity medium",
            "all": "-severity critical,high,medium,low"
        }
        
        cmd = f"nuclei -u {self.target} {templates.get(template_type, '')} -json -o reports/nuclei_results.json"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
            
            # Parse JSON results
            for line in result.stdout.split('\n'):
                if line.strip():
                    try:
                        data = json.loads(line)
                        self.vulnerabilities.append({
                            'template': data.get('template-id', 'Unknown'),
                            'name': data.get('info', {}).get('name', 'Unknown'),
                            'severity': data.get('info', {}).get('severity', 'unknown'),
                            'matched_at': data.get('matched-at', ''),
                            'description': data.get('info', {}).get('description', '')
                        })
                    except:
                        pass
            
            print(f"{Fore.GREEN}[+] Found {len(self.vulnerabilities)} potential vulnerabilities")
            return self.vulnerabilities
        
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}[-] Nuclei scan timeout")
            return []
        except Exception as e:
            print(f"{Fore.RED}[-] Nuclei error: {e}")
            return []