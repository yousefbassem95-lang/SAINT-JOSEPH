
class BaseModule:
    """
    Base class for all modules.
    Provides a name and description for each module.
    """
    def __init__(self):
        self.name = "Unnamed Module"
        self.description = "No description provided."

    def run(self, **kwargs):
        """
        The main method for the module. This must be implemented by subclasses.
        """
        raise NotImplementedError("The 'run' method must be implemented by the module.")


class ReconModule(BaseModule):
    """
    Base class for all reconnaissance modules.
    """
    def __init__(self):
        super().__init__()
        self.module_type = "recon"

    def run(self, target_hostname):
        """
        Runs the reconnaissance module against a given hostname.
        It should return a results dictionary or None.
        """
        raise NotImplementedError("Recon modules must implement the 'run' method.")


class AnalysisModule(BaseModule):
    """
    Base class for all vulnerability analysis modules.
    """
    def __init__(self):
        super().__init__()
        self.module_type = "analysis"

    def run(self, target_id):
        """
        Runs the analysis module against a target identified by its database ID.
        It should add any findings directly to the database.
        """
        raise NotImplementedError("Analysis modules must implement the 'run' method.")


class ExploitationModule(BaseModule):
    """
    Base class for all exploitation modules.
    """
    def __init__(self):
        super().__init__()
        self.module_type = "exploitation"

    def run(self, target_id):
        """
        Runs the exploitation module against a target identified by its database ID.
        It should return a dictionary with a 'status' key ('success' or 'failure').
        """
        raise NotImplementedError("Exploitation modules must implement the 'run' method.")


class OSINTModule(BaseModule):
    """
    Base class for all Open Source Intelligence modules.
    """
    def __init__(self):
        super().__init__()
        self.module_type = "osint"

    def run(self, query):
        """
        Runs the OSINT module with a given query string.
        It should add any findings directly to the database.
        """
        raise NotImplementedError("OSINT modules must implement the 'run' method.")
