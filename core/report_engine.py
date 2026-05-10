cat > core/report_engine.py << 'REPORTEOF'
#!/usr/bin/env python3
import os
from datetime import datetime
from colorama import Fore

class ReportEngine:
    def __init__(self, target, scan_data):
        self.target = target
        self.scan_data = scan_data
    
    def generate_html_report(self):
        """Generate professional HTML report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/porthunter_report_{timestamp}.html"
        
        # Count vulnerabilities by severity
        vuln_critical = sum(1 for v in self.scan_data.get('vulnerabilities', []) if 'critical' in str(v).lower())
        vuln_high = sum(1 for v in self.scan_data.get('vulnerabilities', []) if 'high' in str(v).lower())
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PortHunter Report - {self.target}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1300px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{ color: #667eea; margin-bottom: 10px; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #333; }}
        .risk-critical {{ color: #dc3545; }}
        .risk-high {{ color: #fd7e14; }}
        .risk-medium {{ color: #ffc107; }}
        .risk-low {{ color: #28a745; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #667eea;
            color: white;
            position: sticky;
            top: 0;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
        }}
        .badge-critical {{ background: #dc3545; color: white; }}
        .badge-high {{ background: #fd7e14; color: white; }}
        .badge-medium {{ background: #ffc107; color: #333; }}
        .badge-low {{ background: #28a745; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 PortHunter Security Report</h1>
            <p>Target: {self.target} | Scan Time: {self.scan_data.get('scan_time', 'N/A')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>🌐 Target</h3>
                <div class="stat-number">{self.target}</div>
            </div>
            <div class="stat-card">
                <h3>🔓 Open Ports</h3>
                <div class="stat-number">{len(self.scan_data.get('open_ports', []))}</div>
            </div>
            <div class="stat-card">
                <h3>⚠️ Vulnerabilities</h3>
                <div class="stat-number">{len(self.scan_data.get('vulnerabilities', []))}</div>
            </div>
            <div class="stat-card">
                <h3>💣 Exploits</h3>
                <div class="stat-number">{len(self.scan_data.get('exploits', []))}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📡 Open Ports & Services</h2>
            <table>
                <thead>
                    <tr><th>Port</th><th>Service</th><th>Version</th><th>Risk Level</th></tr>
                </thead>
                <tbody>
'''
        
        for port in self.scan_data.get('open_ports', []):
            risk = "High" if port['port'] in [21,22,23,445,3389,3306,1433] else "Medium" if port['port'] in [80,443,8080,8443] else "Low"
            html_content += f'<tr><td>{port["port"]}</td><td>{port["service"]}</td><td>{port["version"]}</td><td class="risk-{risk.lower()}">{risk}</td></tr>'
        
        html_content += '''
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>💣 Exploit Suggestions</h2>
'''
        
        if self.scan_data.get('exploits'):
            for exp in self.scan_data.get('exploits', []):
                html_content += f'''
            <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #fd7e14;">
                <h3>🎯 Port {exp.get('port', 'N/A')} - {exp.get('service', 'Unknown')}</h3>
                <p><strong>Metasploit Module:</strong> <code>{exp.get('exploits', ['N/A'])[0]}</code></p>
                <p><strong>Command:</strong> <code>msfconsole -q -x "use {exp.get('exploits', [''])[0]}; set RHOST {self.target}; run"</code></p>
            </div>
'''
        else:
            html_content += '<p>No exploit suggestions available.</p>'
        
        html_content += f'''
        </div>
        
        <div class="footer">
            <p>⚠️ This report is for authorized security testing only</p>
            <p>Generated by PortHunter v2.0 | Advanced Pentest Suite</p>
        </div>
    </div>
</body>
</html>
'''
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"{Fore.GREEN}[+] HTML Report generated: {filename}{Fore.RESET}")
        return filename
REPORTEOF
