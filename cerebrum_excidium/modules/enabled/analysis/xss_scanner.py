import requests
import urllib.parse
from modules.base_module import AnalysisModule
from core.brain import log_message
import database as db

class XssScannerModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "XSS Scanner (Reflected)"
        self.description = "Tests for Reflected Cross-Site Scripting vulnerabilities."
        self.payloads = [
            "<script>alert('XSS')</script>",
            "\" ><script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "' onmouseover='alert(1)",
            "\"><img src=x onerror=alert('Sawyer')>"
        ]
        self.test_params = ["q", "s", "search", "id", "page", "query", "url"]

    def run(self, target_id):
        target = db.get_target_by_id(target_id)
        if not target:
            return
            
        host = target['hostname']
        log_message("info", f"[{self.name}] Scanning {host} for Reflected XSS...")
        
        # Determine protocol (simple check)
        # Determine protocol (Try both HTTP and HTTPS)
        base_urls = [f"http://{host}", f"https://{host}"]
        
        vulnerable_urls = []

        for url in base_urls:
            try:
                # 1. Quick connectivity check
                if requests.get(url, timeout=3).status_code not in [200, 403]:
                    continue
                    
                # 2. Fuzz common parameters
                for param in self.test_params:
                    for payload in self.payloads:
                        # Construct URL: http://host/?param=payload
                        # We must encode the payload for the request, but look for reflected unfiltered output
                        fuzzed_url = f"{url}/?{param}={urllib.parse.quote(payload)}"
                        
                        try:
                            res = requests.get(fuzzed_url, timeout=3)
                            # Check if payload is reflected in response body
                            if payload in res.text:
                                log_message("critical", f"[{self.name}] POTENTIAL XSS FOUND at {fuzzed_url}")
                                vulnerable_urls.append(fuzzed_url)
                                
                                db.add_vulnerability(
                                    target_id=target_id,
                                    vuln_type="REFLECTED_XSS",
                                    description=f"Payload reflected in parameter '{param}': {payload}",
                                    severity="high"
                                )
                                break # Stop fuzzing this param if vulnerable
                        except:
                            pass
            except:
                pass
        
        if vulnerable_urls:
            log_message("success", f"[{self.name}] Scan completed. Found {len(vulnerable_urls)} potential XSS vectors.")
        else:
            log_message("info", f"[{self.name}] No XSS found on common parameters.")
