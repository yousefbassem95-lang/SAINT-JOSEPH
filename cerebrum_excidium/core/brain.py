
import time
from utils import log_message
import database as db
from core.module_manager import ModuleManager

class Brain:
    def __init__(self, target=None, mode='recon'):
        self.initial_target = target
        self.mode = mode
        db.initialize_db()
        self.module_manager = ModuleManager()
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
