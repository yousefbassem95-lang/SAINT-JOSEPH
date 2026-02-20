import requests
from modules.base_module import AnalysisModule
from core.brain import log_message
import database as db

class WafDetectorModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "WAF Detector"
        self.description = "Identifies Web Application Firewalls (Cloudflare, AWS, etc.)"

    def run(self, target_id):
        target = db.get_target_by_id(target_id)
        if not target:
            return
            
        host = target['hostname']
        log_message("info", f"[{self.name}] Checking {host} for WAF presence...")
        
        waf_signatures = {
            "Cloudflare": ["cf-ray", "__cfduid", "cf-cache-status", "cloudflare-nginx"],
            "AWS WAF": ["x-amz-cf-id", "x-amzn-requestid", "awselb"],
            "Akamai": ["akamai-x-cache", "x-akamai-request-id"],
            "Incapsula": ["incap-ses", "visid_incap"],
            "F5 BIG-IP": ["bigipserver", "x-cnection"],
            "Sucuri": ["sucuri", "x-sucuri-id"]
        }
        
        detected_waf = None
        
        try:
            url = f"http://{host}"
            # Send a request that might trigger a WAF block or reveal headers
            # Using a slightly suspicious User-Agent or payload might help, but standard headers often reveal it too.
            res = requests.get(url, timeout=5)
            headers = str(res.headers).lower()
            
            for waf, sigs in waf_signatures.items():
                for sig in sigs:
                    if sig in headers:
                        detected_waf = waf
                        break
                if detected_waf:
                    break
            
            if detected_waf:
                log_message("success", f"[{self.name}] DETECTED WAF: {detected_waf} on {host}")
                db.add_vulnerability(
                    target_id=target_id,
                    vuln_type="DEFENSE_MECHANISM",
                    description=f"Protected by {detected_waf} WAF.",
                    severity="info"
                )
            else:
                log_message("info", f"[{self.name}] No common WAF signatures found on {host}.")
                
        except Exception as e:
            log_message("error", f"[{self.name}] Failed to check WAF: {e}")
