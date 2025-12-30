# SAINT-JOSEPH
<img width="704" height="842" alt="Screenshot from 2025-12-30 17-24-03" src="https://github.com/user-attachments/assets/7782f43c-603f-4c44-8d43-04291a2e121d" />

Project SAINT-JOSEPH: Advanced Offensive AI
Executive Summary
SAINT-JOSEPH is a sophisticated, command-line based Offensive Security Intelligence & Exploitation Bot. Designed for red team operations, it integrates modular tools for reconnaissance, vulnerability analysis, and automated exploitation into a cohesive, interactive AI-driven system.

IMPORTANT

Operational Security: This tool includes self-protection mechanisms (Tor routing) and stealth features. Use authorized channels only.

System Architecture
The core system, Cerebrum Excidium, orchestrates a modular arsenal through a central 
Brain
:

Commands
Manages
Stores
User / Operator
Interactive CLI
AI Brain Core
Module Manager
Knowledge Base / SQLite
Recon Modules
Analysis Modules
Exploit Modules
OSINT Modules
Target System
Core Capabilities
1. Global Reconnaissance (The Eyes)
Port Scanning: Non-privileged TCP Connect scans (Nmap) to map the attack surface.
Subdomain Enumeration: Leveraging OSINT (Certificate Transparency) to find hidden infrastructure.
Directory Fuzzing: Brute-forcing web paths to discover admin panels and backups.
Uptime Monitoring: Real-time availability and latency checks.
2. Deep Analysis (The Mind)
WAF Detection: Identifying defensive layers (Cloudflare, AWS WAF, Akamai).
CMS Fingerprinting: Detecting technologies like WordPress, Joomla, and Drupal.
Vulnerability Scanning:
Reflected XSS: Fuzzing parameters for Cross-Site Scripting.
LFI Scanner: Probing for Critical Local File Inclusion flaws.
SQL Injection: Preparing automated injection maps.
3. Automated Exploitation (The Hand)
SQL Injection: Auto-executing SQLMap to extract database schemas and credentials.
SSH Brute-force: Dictionary attacks on weak administrative credentials.
Credential Exfiltration: Automatically storing "loot" in the Knowledge Base.
4. Mission Reporting (The Record)
Report Generation: Compiling comprehensive Mission Reports (
.md
) detailing all findings, vulnerabilities, and exfiltrated data for post-operation analysis.
Operational Workflow
Initialize: Launch the bot venv/bin/python saint_joseph.py.
Protect: Enable Tor Mode (Option 5) for anonymity.
Scan: Engage Recon modules (Option 1) to map the target.
Analyze: Run Analysis checks (Option 2) to identify weaknesses and WAFs.
Exploit: Launch authorized attacks (Option 3) on confirmed vulnerabilities.
Report: Generate a Mission Report (Option 6) to document the operation.
Installation & Setup
Ensure dependencies are met within the virtual environment:

# Clone and Enter Directory
cd cerebrum_excidium
# Install Dependencies
pip install -r requirements.txt
# Launch SAINT-JOSEPH
venv/bin/python saint_joseph.py
Note: External tools nmap, 
sqlmap
, and 
tor
 service must be installed on the host system.

Step-by-Step Usage Tutorial
Phase 1: Initiation
Start the system and ensure stealth.

$ venv/bin/python saint_joseph.py
... [Banner] ...
SAINT-JOSEPH> 5
[*] Self-Protection Mode: ENABLED (Tor)
Phase 2: Target Acquisition (Recon)
Identify the target's attack surface.

SAINT-JOSEPH> 1
Target Hostname/IP: scanme.nmap.org
[*] Initiating Recon on scanme.nmap.org...
[+] Port Scan Complete. Open Ports: 4
[+] Directory Scan Complete. Found 2 paths.
[+] Uptime Check: UP (HTTP 200) - 120ms
Phase 3: Vulnerability Assessment (Analysis)
Probing for specific weaknesses.

SAINT-JOSEPH> 2
Target ID to Analyze (leave empty for auto): 1
[*] Starting Analysis...
[+] DETECTED WAF: Cloudflare
[+] CMS DETECTED: WordPress
[!] POTENTIAL XSS FOUND at http://scanme.../?q=<script>...
Phase 4: Exploitation (Attack)
Launching authorized exploits on confirmed flaws.

SAINT-JOSEPH> 3
Target ID to Attack (leave empty for auto): 1
[*] AUTHORIZED. Launching Exploitation...
[+] SQLMAP: VULNERABLE.
[+] SSH: Brute-force SUCCESS. Credentials stored.
Phase 5: Exfiltration & Reporting
Generating the final mission dossier.

SAINT-JOSEPH> 6
[SUCCESS] Mission Report Generated: reports/mission_report_2025-12-30_15-30.md
Open the generated markdown file to view the full intelligence report.
