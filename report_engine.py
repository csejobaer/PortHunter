#!/usr/bin/env python3
import os
import json
from datetime import datetime
from jinja2 import Template
from colorama import Fore

class ReportEngine:
    def __init__(self, target, scan_data):
        self.target = target
        self.scan_data = scan_data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_html_report(self):
        """Generate comprehensive HTML report"""
        
        template = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pentest Report - {{ target }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .summary-card h3 { color: #667eea; margin-bottom: 10px; }
        .summary-card .number { font-size: 2em; font-weight: bold; color: #333; }
        .risk-critical { color: #dc3545; }
        .risk-high { color: #fd7e14; }
        .risk-medium { color: #ffc107; }
        .risk-low { color: #28a745; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        th {
            background: #667eea;
            color: white;
            position: sticky;
            top: 0;
        }
        .vulnerability {
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 20px;
            border-radius: 8px;
        }
        .vulnerability.critical { background: #f8d7da; border-left-color: #dc3545; }
        .vulnerability.high { background: #fde2e4; border-left-color: #fd7e14; }
        .exploit-section {
            background: #1a1a2e;
            color: #eee;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin-top: 15px;
        }
        .exploit-section pre {
            background: #16213e;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .suggestions {
            background: #d1ecf1;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
        }
        @media (max-width: 768px) {
            table, thead, tbody, th, td, tr { display: block; }
            th { position: relative; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Professional Pentest Report</h1>
            <p>{{ target }} | {{ timestamp }}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>🌐 Target</h3>
                <p>{{ target }}</p>
            </div>
            <div class="summary-card">
                <h3>🔓 Open Ports</h3>
                <div class="number">{{ open_ports|length }}</div>
            </div>
            <div class="summary-card">
                <h3>⚠️ Vulnerabilities</h3>
                <div class="number">{{ vulnerabilities|length }}</div>
            </div>
            <div class="summary-card">
                <h3>💣 Exploits Suggested</h3>
                <div class="number">{{ exploits|length }}</div>
            </div>
        </div>
        
        <div style="padding: 30px;">
            <h2>📡 Open Ports & Services</h2>
            <table>
                <thead>
                    <tr><th>Port</th><th>Service</th><th>Version</th><th>Risk Level</th></tr>
                </thead>
                <tbody>
                    {% for port in open_ports %}
                    <tr>
                        <td>{{ port.port }}</td>
                        <td>{{ port.service }}</td>
                        <td>{{ port.version }}</td>
                        <td class="risk-{{ port.risk|lower }}">{{ port.risk }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <h2>💣 Exploit Suggestions</h2>
            {% for exploit in exploits %}
            <div class="vulnerability {{ exploit.severity|lower }}">
                <h3>🎯 {{ exploit.name }}</h3>
                <p><strong>Port:</strong> {{ exploit.port }} | <strong>Service:</strong> {{ exploit.service }}</p>
                <p><strong>Severity:</strong> <span class="risk-{{ exploit.severity|lower }}">{{ exploit.severity }}</span></p>
                <p><strong>Description:</strong> {{ exploit.description }}</p>
                
                <div class="exploit-section">
                    <strong>🔧 Metasploit Commands:</strong>
                    <pre>{% for cmd in exploit.msf_commands %}{{ cmd }}
{% endfor %}</pre>
                </div>
                
                <div class="suggestions">
                    <strong>💡 Remediation Suggestions:</strong>
                    <ul>
                        {% for suggestion in exploit.suggestions %}
                        <li>{{ suggestion }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            {% endfor %}
            
            <h2>⚠️ Detected Vulnerabilities (Nuclei)</h2>
            {% for vuln in vulnerabilities %}
            <div class="vulnerability {{ vuln.severity|lower }}">
                <h3>{{ vuln.name }}</h3>
                <p><strong>Template:</strong> {{ vuln.template }}</p>
                <p><strong>Severity:</strong> {{ vuln.severity }}</p>
                <p><strong>URL:</strong> {{ vuln.matched_at }}</p>
                <p><strong>Description:</strong> {{ vuln.description }}</p>
            </div>
            {% endfor %}
        </div>
        
        <div class="footer">
            <p>⚠️ This report is generated for authorized security testing only</p>
            <p>Generated by Advanced Pentest Suite | Professional Edition</p>
        </div>
    </div>
</body>
</html>
        ''')
        
        html_output = template.render(
            target=self.target,
            timestamp=self.timestamp,
            open_ports=self.scan_data.get('open_ports', []),
            vulnerabilities=self.scan_data.get('vulnerabilities', []),
            exploits=self.scan_data.get('exploits', [])
        )
        
        filename = f"reports/pentest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w') as f:
            f.write(html_output)
        
        print(f"{Fore.GREEN}[+] HTML Report generated: {filename}")
        return filename
    
    def generate_commands_file(self):
        """Generate executable commands file"""
        cmd_file = f"reports/commands_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sh"
        with open(cmd_file, 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write(f"# Exploitation commands for {self.target}\n")
            f.write(f"# Generated on {self.timestamp}\n\n")
            
            for exploit in self.scan_data.get('exploits', []):
                f.write(f"echo '[+] Trying exploit for {exploit[\"service\"]} on port {exploit[\"port\"]}'\n")
                for cmd in exploit.get('msf_commands', []):
                    if cmd.startswith('use'):
                        f.write(f"msfconsole -q -x \"{cmd}; run; exit\"\n")
        
        os.chmod(cmd_file, 0o755)
        print(f"{Fore.GREEN}[+] Commands script generated: {cmd_file}")
        return cmd_file