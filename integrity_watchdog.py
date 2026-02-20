import os
import hashlib
import json
import sys
from datetime import datetime

# --- THE ARCHITECT'S WATCHDOG ---
# Purpose: Detect unauthorized changes to the codebase (Intrusion Detection).
# Usage: 
#   python integrity_watchdog.py baseline  (To set the normal state)
#   python integrity_watchdog.py check     (To scan for intruders)

DB_FILE = ".watchdog_db.json"
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".idea", ".vscode", "dist", "build"}

def calculate_hash(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def scan_directory(root_dir="."):
    snapshot = {}
    for root, dirs, files in os.walk(root_dir):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file == "integrity_watchdog.py" or file == DB_FILE:
                continue
                
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            if file_hash:
                snapshot[filepath] = file_hash
    return snapshot

def create_baseline():
    print("🛡️  WATCHDOG: Creating new baseline of the fortress...")
    snapshot = scan_directory()
    data = {
        "timestamp": datetime.now().isoformat(),
        "files": snapshot
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Baseline secured. Monitoring {len(snapshot)} files.")

def check_integrity():
    if not os.path.exists(DB_FILE):
        print("❌ WATCHDOG ERROR: No baseline found. Run 'baseline' first.")
        return

    print("👁️  WATCHDOG: Scanning for intruders...")
    with open(DB_FILE, "r") as f:
        baseline_data = json.load(f)
    
    baseline_files = baseline_data["files"]
    current_files = scan_directory()
    
    changes_detected = False
    
    # Check for modified or deleted files
    for filepath, stored_hash in baseline_files.items():
        if filepath not in current_files:
            print(f"🚨 ALERT: File DELETED -> {filepath}")
            changes_detected = True
        elif current_files[filepath] != stored_hash:
            print(f"🚨 ALERT: File MODIFIED -> {filepath}")
            changes_detected = True
            
    # Check for new files (potential malware/backdoors)
    for filepath in current_files:
        if filepath not in baseline_files:
            print(f"⚠️  WARNING: New File Detected -> {filepath}")
            changes_detected = True
            
    if not changes_detected:
        print("✅ SYSTEM SECURE: No unauthorized changes detected.")
    else:
        print("🛑 BREACH DETECTED: The integrity of the fortress is compromised!")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python integrity_watchdog.py [baseline|check]")
    else:
        cmd = sys.argv[1]
        if cmd == "baseline":
            create_baseline()
        elif cmd == "check":
            check_integrity()
