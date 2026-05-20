from utils import log_message
import database as db
from modules.base_module import AnalysisModule
import re

class SqlmapPreparerModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "SQLmap Command Preparer"
        self.description = "Analyzes web ports and prepares sqlmap commands based on discovered paths."

    def run(self, target_id):
        """
        Analyzes a target for potential web vulnerabilities and records them in the database.
        """
        target = db.get_target_by_id(target_id)
        if not target:
            log_message("error", f"[{self.name}] Analysis failed: Could not find target with ID {target_id} in KB.")
            return

        host = target['hostname']
        log_message("info", f"[{self.name}] Starting analysis for {host} (ID: {target_id}).")

        open_ports = db.get_open_ports_for_target(target_id)
        if not open_ports:
            log_message("info", f"[{self.name}] No open ports found for {host} in KB. Skipping.")
            return

        self._check_for_web_vulns(target, open_ports)

    def _check_for_web_vulns(self, target, open_ports):
        """Checks for web-related vulnerabilities."""
        host = target['hostname']
        target_id = target['id']
        web_ports_of_interest = {80, 443, 8000, 8080}
        
        found_web_ports = [port for port in open_ports if port['port_number'] in web_ports_of_interest]

        if not found_web_ports:
            log_message("info", f"[{self.name}] No common web ports open on {host}. Skipping web vulnerability scan.")
            return

        # Look for paths discovered by DirScannerModule in vulnerabilities table (stored as SENSITIVE_DIR)
        vulns = db.get_vulnerabilities(target_id)
        discovered_paths = [v['description'].split('Found: ')[1].split(' (')[0] for v in vulns if v['type'] == "SENSITIVE_DIR"]

        # Also check for standard interesting extensions if no paths found
        if not discovered_paths:
            discovered_paths = [f"http://{host}/index.php?id=1"] # Fallback

        for port_info in found_web_ports:
            port_id = port_info['id']
            port_num = port_info['port_number']
            log_message("info", f"[{self.name}] Web port {port_num} detected on {host}. Analyzing paths.")
            
            for path in discovered_paths:
                # Basic check to see if path might be injectable (e.g. has parameters)
                if '?' in path:
                    target_url = path
                else:
                    target_url = f"{path.rstrip('/')}/index.php?id=1"

                sqlmap_command = f"sqlmap -u '{target_url}' --batch --risk=1 --level=2 --random-agent"

                db.add_vulnerability(
                    target_id=target_id,
                    port_id=port_id,
                    vuln_type="SQL_INJECTION_COMMAND",
                    tool="sqlmap",
                    command=sqlmap_command,
                    description=f"Potential SQL Injection vulnerability at {target_url}"
                )
