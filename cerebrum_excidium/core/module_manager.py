
import os
import importlib
import inspect
from utils import log_message
from modules.base_module import ReconModule, AnalysisModule, ExploitationModule, OSINTModule

class ModuleManager:
    def __init__(self, module_path='modules.enabled'):
        self.module_path = module_path
        self.recon_modules = []
        self.analysis_modules = []
        self.exploitation_modules = []
        self.osint_modules = []
        self.load_modules()

    def load_modules(self):
        """
        Dynamically discovers and loads all modules from the enabled modules directory.
        """
        log_message("info", "Module Manager is discovering and loading all enabled modules...")
        base_path = self.module_path.replace('.', '/')
        
        if not os.path.exists(base_path):
            log_message("warning", f"Module directory not found at '{base_path}'. No modules will be loaded.")
            return

        for module_type in ['recon', 'analysis', 'exploitation', 'osint']:
            module_dir = os.path.join(base_path, module_type)
            try:
                for filename in os.listdir(module_dir):
                    if filename.endswith('.py') and not filename.startswith('__'):
                        module_name = f"{self.module_path}.{module_type}.{filename[:-3]}"
                        self._load_and_instantiate(module_name, module_type)
            except FileNotFoundError:
                log_message("debug", f"No '{module_type}' modules found or directory is missing.")

        log_message("info", f"Loaded {len(self.recon_modules)} recon, {len(self.analysis_modules)} analysis, "
                            f"{len(self.exploitation_modules)} exploitation, and {len(self.osint_modules)} OSINT module(s).")

    def _load_and_instantiate(self, module_name, module_type):
        try:
            module = importlib.import_module(module_name)
            base_classes = {ReconModule, AnalysisModule, ExploitationModule, OSINTModule}
            
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls in base_classes: continue # Skip the base classes themselves

                if module_type == 'recon' and issubclass(cls, ReconModule):
                    instance = cls()
                    self.recon_modules.append(instance)
                    log_message("info", f"Successfully loaded Recon module: {instance.name}")
                elif module_type == 'analysis' and issubclass(cls, AnalysisModule):
                    instance = cls()
                    self.analysis_modules.append(instance)
                    log_message("info", f"Successfully loaded Analysis module: {instance.name}")
                elif module_type == 'exploitation' and issubclass(cls, ExploitationModule):
                    instance = cls()
                    self.exploitation_modules.append(instance)
                    log_message("info", f"Successfully loaded Exploitation module: {instance.name}")
                elif module_type == 'osint' and issubclass(cls, OSINTModule):
                    instance = cls()
                    self.osint_modules.append(instance)
                    log_message("info", f"Successfully loaded OSINT module: {instance.name}")
        except Exception as e:
            log_message("error", f"Failed to load module {module_name}: {e}")

    def run_osint_modules(self, query):
        """
        Runs all loaded OSINT modules with a given query.
        """
        log_message("info", f"Running {len(self.osint_modules)} OSINT module(s) for query: '{query}'.")
        for module in self.osint_modules:
            try:
                module.run(query=query)
            except Exception as e:
                log_message("error", f"Error running OSINT module {module.name}: {e}")

    def run_recon_modules(self, target_hostname):
        all_results = []
        log_message("info", f"Running {len(self.recon_modules)} recon module(s) against {target_hostname}.")
        for module in self.recon_modules:
            try:
                result = module.run(target_hostname=target_hostname)
                if result:
                    all_results.append(result)
            except Exception as e:
                log_message("error", f"Error running recon module {module.name}: {e}")
        return all_results[0] if all_results else None

    def run_analysis_modules(self, target_id):
        log_message("info", f"Running {len(self.analysis_modules)} analysis module(s) against target ID {target_id}.")
        for module in self.analysis_modules:
            try:
                module.run(target_id=target_id)
            except Exception as e:
                log_message("error", f"Error running analysis module {module.name}: {e}")

    def run_exploitation_modules(self, target_id):
        log_message("info", f"Running {len(self.exploitation_modules)} exploitation module(s) against target ID {target_id}.")
        for module in self.exploitation_modules:
            try:
                result = module.run(target_id=target_id)
                if result and result.get("status") == "success":
                    log_message("critical", f"Exploitation module {module.name} reported SUCCESS.")
                    return result
            except Exception as e:
                log_message("error", f"Error running exploitation module {module.name}: {e}")
        return {"status": "failure", "reason": "all_modules_failed"}
