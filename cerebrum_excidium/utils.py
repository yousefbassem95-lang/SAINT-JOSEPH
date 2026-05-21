# Utility functions for Cerebrum Excidium
import datetime
import re
import socket
import ipaddress

def log_message(level, message):
    """
    Simple logger to print messages with a timestamp and level.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

def is_valid_hostname(hostname):
    """
    Validates if a string is a valid hostname.
    """
    if not hostname:
        return False
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present

    # Check if it looks like an IP address. Hostnames cannot be all numeric segments.
    if re.match(r"^[\d\.]+$", hostname):
        return False

    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def is_valid_ip(ip):
    """
    Validates if a string is a valid IPv4 or IPv6 address.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_target(target):
    """
    Returns True if target is a valid hostname or IP.
    """
    return is_valid_ip(target) or is_valid_hostname(target)

from cryptography.fernet import Fernet
import os

KEY_FILE = os.path.join(os.path.dirname(__file__), ".vault.key")

def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        os.chmod(KEY_FILE, 0o600)
        return key

def encrypt_data(data):
    if not data:
        return data
    key = get_or_create_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(token):
    if not token:
        return token
    try:
        key = get_or_create_key()
        f = Fernet(key)
        return f.decrypt(token.encode()).decode()
    except Exception:
        return "[DECRYPTION_FAILED]"
