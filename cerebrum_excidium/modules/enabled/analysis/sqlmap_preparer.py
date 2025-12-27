
from utils import log_message
import database as db
from modules.base_module import AnalysisModule

class SqlmapPreparerModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "SQLmap Command Preparer"
        self.description = "Analyzes web ports and prepares a basic sqlmap command if a web server is suspected."

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
        
        found_web_port = next((port for port in open_ports if port['port_number'] in web_ports_of_interest), None)

        if found_web_port:
            port_id = found_web_port['id']
            log_message("info", f"[{self.name}] Web port {found_web_port['port_number']} detected on {host}. Crafting SQLMap command.")
            
            protocol = 'https' if found_web_port['port_number'] == 443 else 'http'
            target_url = f"{protocol}://{host}/index.php?id=1" # Simplistic assumption
            
            sqlmap_command = f"sqlmap -u '{target_url}' --batch --risk=1 --level=2 --random-agent"

            db.add_vulnerability(
                target_id=target_id,
                port_id=port_id,
                vuln_type="SQL_INJECTION_COMMAND",
                tool="sqlmap",
                command=sqlmap_command,
                description=f"Potential SQL Injection vulnerability at {target_url}"
            )
        else:
            log_message("info", f"[{self.name}] No common web ports open on {host}. Skipping web vulnerability scan.")
