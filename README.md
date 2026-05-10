
<div align="center">

# 🔍 PortHunter - Advanced Pentest Suite

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/yourusername/porthunter)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![Nmap](https://img.shields.io/badge/nmap-integrated-brightgreen.svg)](https://nmap.org)
[![Metasploit](https://img.shields.io/badge/metasploit-ready-orange.svg)](https://metasploit.com)
[![Nuclei](https://img.shields.io/badge/nuclei-enabled-yellow.svg)](https://nuclei.projectdiscovery.io)

```
╔═══════════════════════════════════════════════════════════════╗
║                    🔍 PORT HUNTER v2.0                        ║
║         Advanced Port Scanner & Vulnerability Hunter          ║
║                 For Authorized Security Testing               ║
╚═══════════════════════════════════════════════════════════════╝
```

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=25&duration=3000&pause=500&color=38C2FF&center=true&vCenter=true&width=600&lines=PortHunter+is+ready!;Scanning+for+vulnerabilities...;Hunting+open+ports...;Generating+professional+reports...;Metasploit+integration+active!)](https://git.io/typing-svg)

</div>

---

## 🎯 Features

| Feature | Status | Description |
|---------|--------|-------------|
| 🔌 **Port Scanning** | ✅ | Fast multi-threaded TCP port scanner |
| 🎯 **Service Detection** | ✅ | Identifies services & versions |
| 🛡️ **Vulnerability Scanning** | ✅ | Nuclei + Nmap vuln scripts |
| 💣 **Exploit Suggestions** | ✅ | Metasploit command generator |
| 📊 **Professional Reports** | ✅ | HTML + PDF reports with CVSS scoring |
| 🤖 **AI Suggestions** | ✅ | Smart vulnerability recommendations |
| 🚀 **Auto Exploit Scripts** | ✅ | Generates ready-to-run commands |
| 🌐 **Web Scanning** | ✅ | Directory & file enumeration |

## 📸 Screenshots

<div align="center">
  
| Scan Report | Vulnerability Details |
|-------------|----------------------|
| ![Report](https://via.placeholder.com/400x250?text=HTML+Report+Preview) | ![Vulns](https://via.placeholder.com/400x250?text=Vulnerability+Details) |

</div>

## 🚀 Quick Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/porthunter.git
cd porthunter

# Make installer executable
chmod +x setup.sh

# Run automatic installation
./setup.sh

# Or manual installation
pip3 install -r requirements.txt
sudo apt-get install -y nmap nuclei metasploit-framework
```

## 💻 Usage Examples

```bash
# Basic scan
python3 main.py 192.168.1.1

# Quick scan on common ports
python3 main.py example.com -p 1-1000 -s quick

# Full vulnerability assessment
python3 main.py target.com -p 1-65535 -s full

# Vulnerability only scan
python3 main.py 10.0.0.1 -p 80,443,8080 -s vuln

# With custom output directory
python3 main.py scanme.org -p 1-10000 -o ./my_reports
```

## 📁 Output Structure

```
reports/
├── pentest_report_20240101_120000.html    # Main HTML report
├── commands_20240101_120000.sh            # Exploit commands script
├── msf_commands.rc                        # Metasploit resource file
├── nmap_scan.txt                          # Nmap scan results
├── nmap_vulns.txt                         # Vulnerability scan results
└── nuclei_results.json                    # Nuclei findings
```

## 🎬 Demo

```bash
$ python3 main.py scanme.nmap.org -p 1-1000 -s quick

╔══════════════════════════════════════════════════════════════════╗
║     🚀 Advanced Pentest Suite - Professional Edition v2.0       ║
║          For Authorized Security Testing Only                   ║
╚══════════════════════════════════════════════════════════════════╝

[+] Target set to: scanme.nmap.org
[+] Port range: 1-1000
[*] Running Nmap port scan...
[+] Port 22 open - SSH
[+] Port 80 open - HTTP
[+] Port 443 open - HTTPS
[*] Running Nuclei scan...
[+] Found 3 potential vulnerabilities
[✓] Scan completed successfully!
[✓] Report: reports/pentest_report_20240101_120000.html
[✓] Open ports found: 3
[✓] Vulnerabilities found: 3
[✓] Exploits suggested: 2
```

## 📋 Sample Report Preview

The generated HTML report includes:

- 📊 **Executive Summary** - Risk score and critical findings
- 🔓 **Open Ports Table** - All discovered services
- ⚠️ **Vulnerability List** - CVSS scores and descriptions
- 💣 **Exploit Directions** - Ready-to-use Metasploit commands
- 💡 **Remediation Suggestions** - Fix recommendations
- 📈 **Visual Charts** - Risk distribution graphs

## 🛠️ Requirements

- **Python**: 3.8 or higher
- **OS**: Linux (Kali Linux / Parrot OS / Ubuntu recommended)
- **RAM**: Minimum 2GB
- **Disk**: 500MB free space

### Required Tools
```bash
# Install all dependencies automatically
sudo apt-get update
sudo apt-get install -y nmap nuclei metasploit-framework
pip3 install -r requirements.txt
```

## ⚙️ Configuration

Edit `config/settings.json` to customize:

```json
{
    "threads": 100,
    "timeout": 3,
    "aggressive_mode": false,
    "generate_pdf": true,
    "ai_suggestions": true,
    "max_ports": 65535
}
```

## 🎯 Supported Services & Exploits

| Service | Port | Exploit Availability |
|---------|------|---------------------|
| FTP | 21 | ✅ vsftpd backdoor |
| SSH | 22 | ✅ Brute force, Auth bypass |
| SMB | 445 | ✅ EternalBlue (MS17-010) |
| RDP | 3389 | ✅ BlueKeep (CVE-2019-0708) |
| MySQL | 3306 | ✅ UDF injection |
| HTTP/HTTPS | 80,443 | ✅ 100+ Nuclei templates |

## 📚 Commands Cheat Sheet

```bash
# Run with custom port range
python3 main.py target.com -p 22,80,443,3306

# Full scan with all features
python3 main.py target.com -p 1-65535 -s full

# Quick reconnaissance
python3 main.py target.com -s quick

# Generate only report from existing scans
python3 main.py target.com --report-only
```

## 🔒 Legal Disclaimer

> ⚠️ **IMPORTANT**: This tool is for **authorized security testing only**!
>
> - Only use on systems you **own** or have **written permission** to test
> - Unauthorized scanning may violate laws like:
>   - Computer Fraud and Abuse Act (CFAA) - USA
>   - Computer Misuse Act - UK
>   - Similar laws worldwide
> - The author assumes **no liability** for misuse
>
> **By using this tool, you agree to these terms.**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support
- 🐛 Issues: [GitHub Issues](https://github.com/csejobaer/porthunter/issues)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=csejobaer/porthunter&type=Date)](https://star-history.com/#yourusername/porthunter&Date)


<div align="center">
  
**Made with 🔍 by Security Researchers**

[⬆ Back to Top](#-porthunter---advanced-pentest-suite)

</div>
```
