# Utility functions for Cerebrum Excidium
import datetime

def log_message(level, message):
    """
    Simple logger to print messages with a timestamp and level.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")
