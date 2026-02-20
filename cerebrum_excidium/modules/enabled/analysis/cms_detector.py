import requests
from modules.base_module import AnalysisModule
from core.brain import log_message
import database as db

class CmsDetectorModule(AnalysisModule):
    def __init__(self):
        super().__init__()
        self.name = "CMS Detector"
        self.description = "Identifies Content Management Systems (WordPress, Joomla, etc)."

    def run(self, target_id):
        # Get target info
        target = db.get_target_by_id(target_id)
        if not target:
            return
            
        host = target['hostname']
        log_message("info", f"[{self.name}] Checking {host} for CMS signatures...")
        
        protocols = ["http", "https"]
        detected_cms = None
        
        for proto in protocols:
            try:
                url = f"{proto}://{host}"
                res = requests.get(url, timeout=5)
                content = res.text.lower()
                headers = str(res.headers).lower()
                
                if "wp-content" in content or "wordpress" in content:
                    detected_cms = "WordPress"
                elif "joomla" in content or "option=com_content" in content:
                    detected_cms = "Joomla"
                elif "drupal" in content or "drupal.org" in content:
                    detected_cms = "Drupal"
                elif "content-generator" in headers and "magento" in headers:
                    detected_cms = "Magento"
                
                if detected_cms:
                    break
            except:
                pass
        
        if detected_cms:
            log_message("success", f"[{self.name}] DETECTED CMS: {detected_cms} on {host}")
            # Identify as a vulnerability/finding
            db.add_vulnerability(
                target_id=target_id,
                vuln_type="TECH_DISCLOSURE",
                description=f"Target is running {detected_cms} CMS.",
                severity="info"
            )
        else:
            log_message("info", f"[{self.name}] No common CMS detected on {host}.")
