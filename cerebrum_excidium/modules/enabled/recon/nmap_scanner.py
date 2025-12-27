
import nmap
import socket
from utils import log_message
from modules.base_module import ReconModule

class NmapScannerModule(ReconModule):
    def __init__(self):
        super().__init__()
        self.name = "Nmap Port Scanner"
        self.description = "Investigates a target using Nmap to find open ports and services."
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError:
            log_message("error", "Nmap binary not found. NmapScannerModule will be disabled.")
            self.nm = None
        except Exception as e:
            log_message("error", f"Error initializing NmapPortScanner: {e}")
            self.nm = None

    def run(self, target_hostname):
        """
        Investigates a single target using Nmap.
        This is the core logic of the module.
        """
        if not self.nm:
            log_message("warning", f"Skipping Nmap investigation for {target_hostname}: Nmap is not available.")
            return None

        try:
            ip_address = socket.gethostbyname(target_hostname)
            log_message("info", f"Resolved {target_hostname} to {ip_address}.")
        except socket.gaierror:
            log_message("error", f"Could not resolve hostname {target_hostname}. Skipping scan.")
            return None

        log_message("info", f"Starting Evasive Nmap port scan on {ip_address} ({target_hostname})...")
        try:
            # -sS: TCP SYN (Stealth) Scan, -T2: Slow/sneaky timing, --scan-delay: avoid IDS, -D RND:10: use decoys
            evasive_args = '-sS -T2 --scan-delay 1s -D RND:10 -Pn'
            log_message("debug", f"Nmap arguments: {evasive_args}")
            self.nm.scan(hosts=ip_address, arguments=evasive_args)
            
            host_info = self.nm[ip_address] if ip_address in self.nm else None
            if not host_info:
                log_message("warning", f"Host {target_hostname} ({ip_address}) appears down or did not respond to Nmap scan.")
                return None

            scan_results = {
                "host": target_hostname,
                "ip": ip_address,
                "state": host_info.state(),
                "protocols": {}
            }

            for proto in host_info.all_protocols():
                scan_results["protocols"][proto] = {}
                for port_num, port_data in host_info[proto].items():
                    if port_data['state'] == 'open':
                        scan_results["protocols"][proto][port_num] = {
                            "name": port_data.get('name', 'unknown'),
                            "product": port_data.get('product', 'unknown'),
                            "version": port_data.get('version', 'unknown'),
                            "state": port_data.get('state'),
                            "reason": port_data.get('reason', 'unknown')
                        }
            log_message("info", f"Nmap scan of {target_hostname} completed. Status: {host_info.state()}")
            return scan_results

        except Exception as e:
            log_message("error", f"An unexpected error occurred during Nmap scan of {target_hostname}: {e}")
            return None
