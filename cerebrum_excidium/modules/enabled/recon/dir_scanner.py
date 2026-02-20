import requests
from modules.base_module import ReconModule
from core.brain import log_message

class DirScannerModule(ReconModule):
    def __init__(self):
        super().__init__()
        self.name = "Web Directory Scanner"
        self.description = "Brute-forces common web directories (admin, backup, etc)."
        self.common_paths = [
            "admin", "administrator", "login", "wp-admin", "backup", "db", "api", 
            "test", "dev", "staging", "uploads", "images", "js", "css", "robots.txt"
        ]

    def run(self, target_hostname):
        """
        Scans for common directories on the target.
        Returns a dict with found paths.
        """
        found_paths = []
        protocols = ["http", "https"]
        
        log_message("info", f"[{self.name}] Scanning {target_hostname} for {len(self.common_paths)} common paths...")
        
        for proto in protocols:
            base_url = f"{proto}://{target_hostname}"
            try:
                # Check root first to see if reachable
                if requests.get(base_url, timeout=3).status_code not in [200, 403]:
                    continue
            except:
                continue
                
            for path in self.common_paths:
                url = f"{base_url}/{path}/"
                try:
                    res = requests.get(url, timeout=2, allow_redirects=False)
                    if res.status_code in [200, 403, 301, 302]:
                         found_paths.append({"url": url, "status": res.status_code})
                         log_message("success", f"[{self.name}] Found: {url} ({res.status_code})")
                except:
                    pass
        
        if found_paths:
            return {"dir_scan": found_paths}
        return None
