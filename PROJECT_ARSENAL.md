# PROJECT ARSENAL: SAINT-JOSEPH

> [!IMPORTANT]
> **OPERATIONAL SECURITY WARNING**: All tools listed here are for authorized testing only. "With great power comes great responsibility." - The Saint.

## Core Capabilities

### 1. SAINT-JOSEPH Bot
The central command interface.
- **Path**: `saint_joseph.py`
- **Usage**: `./saint_joseph.py`
- **Features**: 
    - Interactive Recon/Attack modes.
    - Automated Target Management.
    - Self-Protection Toggles.

### 2. Reconnaissance
#### Nmap Scanner
- **Module**: `modules/enabled/recon/nmap_scanner.py`
- **Type**: Network Scanner
- **Method**: TCP Connect Scan (`-sT`)
- **Evation**: Timing (`-T2`), Decoys (`-D RND:10`), Frag (`-f` in future)
- **Status**: **SAFE** (Non-privileged)

### 3. Exploitation
#### SQLMap Executor
- **Module**: `modules/enabled/exploitation/sqlmap_executor.py`
- **Dependency**: `sqlmap`
- **Trigger**: Runs on targets with `SQL_INJECTION_COMMAND` vulnerability type.
- **Action**: Automatically extracts Database Names and stores as Credentials.

#### SSH Bruteforcer
- **Module**: `modules/enabled/exploitation/ssh_bruteforcer.py`
- **Dependency**: `paramiko`
- **Trigger**: Runs on targets with `WEAK_SSH_CREDENTIALS` vulnerability type.
- **Action**: Brute-forces root/admin accounts.

#### Directory Scanner
- **Module**: `modules/enabled/recon/dir_scanner.py`
- **Type**: Web Fuzzer
- **Action**: Checks for sensitive paths (admin, backup, etc).

### 4. Analysis
#### CMS Detector
- **Module**: `modules/enabled/analysis/cms_detector.py`
- **Type**: Fingerprinting
- **Action**: Identifies WordPress, Joomla, Drupal, Magento.

#### XSS Scanner
- **Module**: `modules/enabled/analysis/xss_scanner.py`
- **Type**: Web Vulnerability Fuzzing
- **Action**: Tests parameters for Reflected XSS.

#### LFI Scanner
- **Module**: `modules/enabled/analysis/lfi_scanner.py`
- **Type**: Web Vulnerability Fuzzing
- **Action**: Tests parameters for Local File Inclusion (reading /etc/passwd).

#### WAF Detector
- **Module**: `modules/enabled/analysis/waf_detector.py`
- **Type**: Defense Identification
- **Action**: Identifies Firewalls (Cloudflare, AWS, Akamai).

### 5. OSINT
#### Subdomain Enumeration
- **Module**: `modules/enabled/osint/subdomain_enum.py`
- **Source**: crt.sh (Certificate Transparency)
- **Action**: Expands attack surface by finding subdomains.

### 6. Monitoring
#### Uptime Monitor
- **Module**: `modules/enabled/recon/uptime_monitor.py`
- **Type**: Availability Check
- **Action**: Verifies target is UP and measures latency.
#### Subdomain Enumeration
- **Module**: `modules/enabled/osint/subdomain_enum.py`
- **Source**: crt.sh (Certificate Transparency)
- **Action**: Expands attack surface by finding subdomains.

## Knowledge Base (Brain)
- **Database**: `cerebrum_excidium/core/knowledge_base.db` (SQLite)
- **Schema**:
    - `targets`: Hostnames, Status.
    - `ports`: Open ports, Services.
    - `vulnerabilities`: Potential flaws.
    - `credentials`: Loot.

## Reference Links
- [SQLMap Wiki](https://github.com/sqlmapproject/sqlmap/wiki)
- [Nmap Reference Guide](https://nmap.org/book/man.html)
