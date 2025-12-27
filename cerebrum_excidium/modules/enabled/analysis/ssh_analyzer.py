
from utils import log_message
import database as db
from modules.base_module import AnalysisModule

class SshAnalyzerModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "SSH Analyzer"
        self.description = "Checks for open SSH ports and flags them for brute-force analysis."
        self.ssh_port = 22

    def run(self, target_id):
        """
        Checks if port 22 is open for a target and adds a 'WEAK_SSH_CREDENTIALS'
        vulnerability if it is.
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

        ssh_port_open = next((port for port in open_ports if port['port_number'] == self.ssh_port), None)

        if ssh_port_open:
            port_id = ssh_port_open['id']
            log_message("warning", f"[{self.name}] Port {self.ssh_port} (SSH) is open on {host}. Flagging for bruteforce.")

            # This vulnerability is just a flag for the next module, it has no 'command'.
            db.add_vulnerability(
                target_id=target_id,
                port_id=port_id,
                vuln_type="WEAK_SSH_CREDENTIALS",
                tool="ssh_bruteforcer",
                command=None, # No command needed, the exploiter knows what to do
                description=f"Port {self.ssh_port} is open, making it a potential target for SSH credential stuffing."
            )
        else:
            log_message("info", f"[{self.name}] Port {self.ssh_port} is not open on {host}. Skipping.")
