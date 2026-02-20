import requests
import json
from modules.base_module import OSINTModule
from core.brain import log_message
import database as db

class SubdomainEnumModule(OSINTModule):
    def __init__(self):
        super().__init__()
        self.name = "Subdomain Enumeration (crt.sh)"
        self.description = "Finds subdomains using Certificate Transparency logs."

    def run(self, query):
        """
        Query is a domain name (e.g., example.com).
        """
        log_message("info", f"[{self.name}] Searching for subdomains of: {query}")
        
        try:
            url = f"https://crt.sh/?q=%25.{query}&output=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                subdomains = set()
                
                for entry in data:
                    name_value = entry['name_value']
                    # Handle multi-line names
                    for sub in name_value.split('\n'):
                        if query in sub and '*' not in sub:
                            subdomains.add(sub.strip().lower())
                
                log_message("success", f"[{self.name}] Found {len(subdomains)} unique subdomains.")
                
                # Add found subdomains to DB
                for sub in subdomains:
                    existing = db.get_target_by_hostname(sub)
                    if not existing:
                        db.add_target(hostname=sub)
                        log_message("info", f"[{self.name}] Added new target: {sub}")
            else:
                log_message("error", f"[{self.name}] Failed to fetch data: HTTP {response.status_code}")
                
        except Exception as e:
            log_message("error", f"[{self.name}] Error: {str(e)}")
