import time
from core.module_manager import ModuleManager
from core.report_generator import ReportGenerator
import database as db

def log_message(level, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

class Brain:
    def __init__(self, target=None, mode='recon'):
        log_message("info", "Initializing Cerebrum Excidium AI Core...")
        
        self.initial_target = target
        self.mode = mode
        
        # Initialize Database
        db.initialize_db()
        log_message("info", "Database initialized successfully.")
        
        # Load Modules
        self.module_manager = ModuleManager()
        self.module_manager.load_modules()
        
        self.reporter = ReportGenerator()
        
        self.osint_queries_run = set() # Keep track of OSINT queries to avoid repetition
        log_message("info", "Cerebrum Excidium AI Core is waking up. Knowledge Base and Module Manager are online.")

    def run(self):
        log_message("info", "AI Core is now operational. Beginning operational cycles.")
        self.seed_initial_target()

        while self.main_loop():
            log_message("info", "Cycle complete. Pausing for 5 seconds for reflection...")
            time.sleep(5)
            
        log_message("info", "AI Core has concluded its scheduled operational cycles.")

    def seed_initial_target(self):
        """Adds the initial seed target to the database if provided."""
        if self.initial_target and not db.get_target_by_hostname(self.initial_target):
            log_message("info", f"Seeding initial target {self.initial_target} into Knowledge Base.")
            db.add_target(hostname=self.initial_target)

    def main_loop(self):
        log_message("info", "Starting new operational cycle.")
        
        # 1. OSINT Phase
        self.run_osint()
        
        # 2. Reconnaissance Phase
        self.run_reconnaissance()

        # 3. Target Selection
        target = self.select_target()
        if not target:
            log_message("info", "No actionable targets found for this cycle. Standing by.")
            # If there's nothing to attack, we can still continue OSINT and Recon
            return True 
        
        log_message("info", f"Selected '{target['hostname']}' (ID: {target['id']}) as current focus target.")
        
        if self.mode == 'recon':
            log_message("info", "Mode is 'recon'. Concluding cycle after investigation phase.")
            return True

        # 4. Analysis Phase
        self.run_analysis(target)

        # 5. Exploitation Phase
        self.run_exploitation(target)

        return True

    def run_osint(self):
        """Runs OSINT modules to gather intelligence and discover new targets."""
        log_message("info", "Entering OSINT Phase.")
        # Create a query based on the initial target
        if self.initial_target and self.initial_target not in self.osint_queries_run:
            query = f"site:*.{self.initial_target} | site:{self.initial_target}"
            self.module_manager.run_osint_modules(query)
            self.osint_queries_run.add(self.initial_target)
        else:
            log_message("info", "No new OSINT queries to run in this cycle.")

    def run_reconnaissance(self):
        log_message("info", "Entering Reconnaissance Phase.")
        targets_to_scan = db.get_targets_by_status(['new'])
        if not targets_to_scan:
            log_message("info", "No new targets require investigation.")
            return
            
        for target in targets_to_scan:
            log_message("info", f"Investigating new target: {target['hostname']}")
            scan_results = self.module_manager.run_recon_modules(target['hostname'])
            
            if scan_results:
                db.add_port_scan_results(target['id'], scan_results)
                db.update_target_status(target['id'], 'scanned')
                log_message("info", f"Investigation of {target['hostname']} complete. Results stored in KB.")
            else:
                db.update_target_status(target['id'], 'scan_failed')
                log_message("warning", f"Investigation of {target['hostname']} failed.")

    def select_target(self):
        if self.mode == 'recon': return None
        targets = db.get_targets_by_status(['scanned', 'analysis_complete', 'analyzed_clean'])
        return targets[0] if targets else None

    def run_analysis(self, target):
        target_id = target['id']
        hostname = target['hostname']
        log_message("info", f"Entering Analysis Phase for {hostname}.")

        self.module_manager.run_analysis_modules(target_id)
        
        # Check if any vulns were added
        if db.get_potential_vulnerabilities(target_id):
            db.update_target_status(target_id, 'analysis_complete')
            log_message("info", f"Analysis for {hostname} complete. Potential vulnerabilities were found.")
        else:
            db.update_target_status(target_id, 'analyzed_clean')
            log_message("info", f"Analysis for {hostname} complete. No obvious vulnerabilities found.")

    def run_exploitation(self, target):
        target_id = target['id']
        hostname = target['hostname']
        if target['status'] != 'analysis_complete':
            log_message("info", f"Skipping exploitation for {hostname} (Status: {target['status']}).")
            return

        log_message("info", f"Entering Exploitation Phase for {hostname}.")
        exploit_result = self.module_manager.run_exploitation_modules(target_id)
        
        if exploit_result and exploit_result.get("status") == "success":
            log_message("critical", f"Target {hostname} has been COMPROMISED.")
            db.update_target_status(target_id, 'compromised')
        else:
            log_message("warning", f"Exploitation attempt failed on {hostname}.")

    # --- Interactive Methods for SAINT-JOSEPH Chatbot ---

    def interactive_recon(self, target_hostname):
        """Manually triggers a recon scan on a specific target."""
        # Ensure target exists in DB
        existing = db.get_target_by_hostname(target_hostname)
        if not existing:
            db.add_target(hostname=target_hostname)
            existing = db.get_target_by_hostname(target_hostname)
        
        log_message("info", f"Interactive: Launching Recon on {target_hostname}...")
        results_list = self.module_manager.run_recon_modules(target_hostname)
        
        if results_list:
            scan_count = 0
            for results in results_list:
                if 'protocols' in results:
                    # Nmap Result
                    db.add_port_scan_results(existing['id'], results)
                    db.update_target_status(existing['id'], 'scanned')
                    print(f"[+] Port Scan Complete. Open Ports: {len(results.get('protocols', {}).get('tcp', {}))}")
                    scan_count += 1
                
                elif 'dir_scan' in results:
                    # Dir Scanner Result
                    paths = results['dir_scan']
                    print(f"[+] Directory Scan Complete. Found {len(paths)} paths.")
                    for p in paths:
                        print(f"    - {p['url']} ({p['status']})")
                        # Add as vulnerability for tracking
                        db.add_vulnerability(
                            target_id=existing['id'],
                            vuln_type="SENSITIVE_DIR",
                            description=f"Found: {p['url']} ({p['status']})",
                            severity="info"
                        )
                    scan_count += 1

                elif 'uptime_scan' in results:
                    # Uptime Monitor Result
                    up = results['uptime_scan']
                    print(f"[+] Uptime Check: {up['status']} (HTTP {up.get('code','N/A')}) - {up['latency_ms']}ms")
                    scan_count += 1
            
            if scan_count == 0:
                 print("[-] Modules ran but produced no actionable data.")
        else:
            print("[-] Scan produced no results or failed.")

    def interactive_analysis(self, target_id=None):
        """Manually triggers analysis."""
        if not target_id:
            # Auto-select
            targets = db.get_targets_by_status(['scanned'])
            if not targets:
                print("[-] No scanned targets available for analysis.")
                return
            target = targets[0]
        else:
            target = db.get_target_by_id(target_id)
            if not target:
                print(f"[-] Target ID {target_id} not found.")
                return

        print(f"[*] Analyzing {target['hostname']}...")
        self.run_analysis(target)
        print("[+] Analysis run complete.")

    def interactive_exploitation(self, target_id=None):
        """Manually triggers exploitation."""
        if not target_id:
             targets = db.get_targets_by_status(['analysis_complete'])
             if not targets:
                 print("[-] No analyzed targets ready for exploitation.")
                 return
             target = targets[0]
        else:
            target = db.get_target_by_id(target_id)
            
        if not target: 
            print("[-] Invalid target.")
            return

        print(f"[*] ATTACKING {target['hostname']}...")
        self.run_exploitation(target)
        print("[+] Attack sequence finished.")

    def print_status(self):
        """Prints a summary of the Knowledge Base."""
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM targets GROUP BY status")
        stats = cursor.fetchall()
        print("\n--- KNOWLEDGE BASE STATUS ---")
        for row in stats:
            print(f"- {row['status'].upper()}: {row['count']} targets")
        
        cursor.execute("SELECT count(*) as count FROM credentials")
        creds = cursor.fetchone()
        print(f"- LOOT (Credentials): {creds['count']}")
        conn.close()

    def toggle_protection(self):
        """Toggles 'Use Tor' / Self-Protection mode."""
        # In a real implementation, this would update a global config or ModuleManager state
        # For now, we'll set a flag on the instance
        if not hasattr(self, 'use_tor'):
            self.use_tor = False
        
        self.use_tor = not self.use_tor
        log_message("info", f"Self-Protection (Tor) set to: {self.use_tor}")
        return self.use_tor

    def generate_report(self):
        filename = self.reporter.generate_mission_report()
        log_message("success", f"Mission Report Generated: {filename}")
        return filename
