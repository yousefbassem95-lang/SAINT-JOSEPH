
import re
from urllib.parse import urlparse
from utils import log_message
import database as db
from modules.base_module import OSINTModule

# The 'google_web_search' tool is assumed to be available in the global scope
# where this code will be executed.

class GoogleSearchModule(OSINTModule):
    def __init__(self):
        super().__init__()
        self.name = "Google Search"
        self.description = "Uses Google to search for information about a target, such as subdomains and related websites."

    def run(self, query):
        """
        Runs a Google search and parses the results for new hostnames.
        """
        log_message("info", f"[{self.name}] Running Google search for query: '{query}'")

        try:
            # The tool is called directly. The environment handles the execution.
            search_results = google_web_search(query=query)
        except NameError:
            log_message("error", f"[{self.name}] The 'google_web_search' tool is not available in the current environment.")
            return
        except Exception as e:
            log_message("error", f"[{self.name}] Google search failed: {e}")
            return

        if not search_results:
            log_message("info", f"[{self.name}] No search results found for query.")
            return

        hostnames = self._parse_for_hostnames(search_results)
        log_message("info", f"[{self.name}] Found {len(hostnames)} unique potential hostnames from search.")

        for hostname in hostnames:
            if not db.get_target_by_hostname(hostname):
                log_message("info", f"[{self.name}] Discovered new potential target via OSINT: {hostname}")
                db.add_target(hostname=hostname, status='new')

    def _parse_for_hostnames(self, search_results):
        """
        Parses the output from the google_web_search tool to extract unique hostnames.
        """
        found_hostnames = set()
        # The tool returns a list of dictionaries, each with a 'link' key.
        for result in search_results:
            try:
                link = result.get('link')
                if link:
                    parsed_url = urlparse(link)
                    # Add the main domain and any subdomains
                    if parsed_url.hostname:
                        found_hostnames.add(parsed_url.hostname)
            except Exception as e:
                log_message("debug", f"[{self.name}] Could not parse URL from search result: {link} - {e}")
        
        return list(found_hostnames)
