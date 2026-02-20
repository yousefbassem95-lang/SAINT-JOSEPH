import database as db
import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.output_dir = "reports"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_mission_report(self):
        """
        Generates a full report of all targets and findings in the database.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.output_dir}/mission_report_{timestamp}.md"
        
        targets = db.get_all_targets()
        
        with open(filename, "w") as f:
            f.write(f"# SAINT-JOSEPH Mission Report\n")
            f.write(f"**Date**: {timestamp}\n")
            f.write(f"**Total Targets**: {len(targets)}\n")
            f.write("\n---\n")
            
            for target in targets:
                t_id = target['id']
                host = target['hostname']
                ip = target['ip_address'] or "N/A"
                status = target['status']
                
                f.write(f"## Target: {host} ({ip})\n")
                f.write(f"- **Status**: {status}\n")
                
                # Ports
                ports = db.get_ports_by_target(t_id)
                if ports:
                    f.write(f"### Open Ports\n")
                    f.write("| Port | Protocol | Service | Product | Version |\n")
                    f.write("|---|---|---|---|---|\n")
                    for p in ports:
                        f.write(f"| {p['port_number']} | {p['protocol']} | {p['service_name']} | {p['product'] or '-'} | {p['version'] or '-'} |\n")
                    f.write("\n")
                else:
                    f.write("- No open ports found.\n\n")
                
                # Vulnerabilities
                vulns = db.get_vulnerabilities(t_id)
                if vulns:
                    f.write(f"### Vulnerabilities\n")
                    for v in vulns:
                        f.write(f"> [!WARNING] **{v['vuln_type']}** ({v['severity']})\n")
                        f.write(f"> {v['description']}\n>\n")
                    f.write("\n")
                
                # Credentials
                creds = db.get_credentials(t_id)
                if creds:
                    f.write(f"### EXFILTRATED CREDENTIALS\n")
                    f.write("```\n")
                    for c in creds:
                         f.write(f"Service: {c['service']}\n")
                         f.write(f"User: {c['username']}\n")
                         f.write(f"Pass: {c['password']}\n")
                         f.write("---\n")
                    f.write("```\n")
                
                f.write("\n---\n")
        
        return filename
