
from urllib.parse import urlparse
from utils import log_message
import database as db
from modules.base_module import OSINTModule

# The 'google_web_search' tool is assumed to be available in the global scope.

class SocialMediaSearchModule(OSINTModule):
    def __init__(self):
        super().__init__()
        self.name = "Social Media Search"
        self.description = "Uses Google to find social media profiles related to a target."
        self.social_sites = ["linkedin.com", "twitter.com", "facebook.com", "github.com"]

    def run(self, query):
        """
        Runs Google searches for social media profiles related to the query.
        """
        log_message("info", f"[{self.name}] Searching for social media profiles related to '{query}'")

        target_id = db.get_target_by_hostname(query)['id'] if db.get_target_by_hostname(query) else None

        for site in self.social_sites:
            search_query = f'site:{site} "{query}"'
            log_message("info", f"[{self.name}] Running search: {search_query}")
            
            try:
                search_results = google_web_search(query=search_query)
            except NameError:
                log_message("error", f"[{self.name}] The 'google_web_search' tool is not available.")
                continue # Skip this site
            except Exception as e:
                log_message("error", f"[{self.name}] Google search failed for site {site}: {e}")
                continue

            if not search_results:
                continue

            for result in search_results:
                link = result.get('link')
                if link:
                    # We found a potential profile, let's store it.
                    db.add_intelligence(
                        target_id=target_id,
                        intel_type='social_media_profile',
                        source=self.name,
                        content=link
                    )
