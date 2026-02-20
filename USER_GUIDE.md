# SAINT-JOSEPH: User Guide

**SAINT-JOSEPH** is a powerful, interactive offensive security bot designed for Reconnaissance, Vulnerability Analysis, and Automated Exploitation. This guide provides step-by-step instructions on how to use its capabilities.

## 1. Getting Started

### Launching the Bot
Open your terminal and navigate to the project directory:
```bash
cd cerebrum_excidium
venv/bin/python saint_joseph.py
```
You will be greeted by the SAINT-JOSEPH banner and the command prompt.

## 2. Command Menu
Type `menu` or `help` to see the available options:
```text
1. Scan Target (Recon)
2. Analyze Target (Vulnerability Check)
3. Attack Target (Exploit)
4. Status Report
5. Toggle Self-Protection (Tor)
6. Generate Mission Report
7. Exit
```

## 3. Operations Guide

### Step 1: Reconnaissance (The Eyes)
Before attacking, you must see. Use Recon to find open ports and hidden directories.
1. Type `1` or `scan`.
2. Enter the **Hostname** or **IP** (e.g., `scanme.nmap.org`).
3. The bot will perform:
    -   **Nmap Scan**: To find open ports (Safe Connect Scan).
    -   **Directory Scan**: To brute-force hidden paths like `/admin`.
    -   **Subdomain Enum**: To find subdomains via certificate logs.
    -   **Uptime Monitor**: To check availability and latency.

### Step 2: Analysis (The Mind)
Once a target is scanned, analyze it for weaknesses.
1. Type `2`.
2. Enter the **Target ID** (or leave empty to analyze all).
3. The bot will run:
    - **WAF Detector**: Identifies Cloudflare, AWS WAF, etc.
    -   **CMS Detector**: Identifies if it's WordPress, Joomla, etc.
    -   **XSS Scanner**: Fuzzes parameters for Reflected XSS.
    -   **LFI Scanner**: Checks for Local File Inclusion flaws.
    - **SQLMap Preparer**: Identifies potential injection points.

### Step 3: Exploitation (The Hand)
If vulnerabilities are confirmed, launch the attack.
1. Type `3`.
2. The bot will attempt to exploit:
    - **SQL Injection**: Using SQLMap to dump database names.
    - **Weak SSH**: Brute-forcing root credentials.
3. Successful loot (credentials) is stored in the database.

### Step 4: Reporting (The Record)
Document your conquest.
1. Type `6`.
2. The bot generates a **Mission Report** in the `reports/` directory.
3. This Markdown file contains all Targets, Open Ports, Vulnerabilities, and Exfiltrated Credentials.

## 4. Self-Protection
Type `5` to toggle **Tor Mode**.
- **ENABLED**: Traffic is routed through Tor (requires local Tor service).
- **DISABLED**: Direct connection (faster, less stealthy).

> [!WARNING]
> Use this tool responsibly. Only test targets you have permission to attack.
