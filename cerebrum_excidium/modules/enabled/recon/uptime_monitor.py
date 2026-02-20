import requests
import time
from modules.base_module import ReconModule
from core.brain import log_message

class UptimeMonitorModule(ReconModule):
    def __init__(self):
        super().__init__()
        self.name = "Uptime Monitor"
        self.description = "Checks target availability and response latency."

    def run(self, target_hostname):
        """
        Checks if the target is up and measures latency.
        Returns a dict compatible with Recon results.
        """
        log_message("info", f"[{self.name}] Pinging {target_hostname} (HTTP)...")
        
        protocols = ["https", "http"]
        result = None
        
        for proto in protocols:
            url = f"{proto}://{target_hostname}"
            try:
                start_time = time.time()
                res = requests.get(url, timeout=5)
                latency = (time.time() - start_time) * 1000 # ms
                
                status = "UP" if res.status_code < 500 else "DOWN"
                color = "success" if status == "UP" else "error"
                
                log_message(color, f"[{self.name}] Target {target_hostname} is {status} ({res.status_code}). Latency: {latency:.2f}ms")
                
                result = {
                    "uptime_scan": {
                        "status": status,
                        "code": res.status_code,
                        "latency_ms": round(latency, 2),
                        "url": url
                    }
                }
                break # Stop if we got a response
            except Exception:
                continue
        
        if not result:
            log_message("warning", f"[{self.name}] Target {target_hostname} seems DOWN or unreachable.")
            return {"uptime_scan": {"status": "DOWN", "latency_ms": 0}}
            
        return result
