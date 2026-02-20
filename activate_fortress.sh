#!/bin/bash

# --- THE ARCHITECT'S ACTIVATION SCRIPT ---
# Usage: ./activate_fortress.sh
# Purpose: Deploys the Fortress Protocol to the current project directory.

echo "🏰 ACTIVATING FORTRESS PROTOCOL..."
echo "Owner: Youssef Bassem (JOJO / JUPITER)"

# 1. Initialize Git
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
else
    echo "Git repository already initialized."
fi

# 2. Configure Identity
echo "Configuring Git Identity..."
git config user.name "Youssef Bassem"
git config user.email "Yousefbassem95@Gmail.com"
git config user.signingkey "61CC6B967A1AF5EB"
git config commit.gpgsign true
git config tag.gpgsign true

# 3. Deploy Guardians (Hooks)
echo "Deploying Guardians..."
mkdir -p .git/hooks
cp templates/hooks/pre-commit .git/hooks/pre-commit
cp templates/hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/pre-commit .git/hooks/commit-msg

# 4. Start Watchdog Baseline
echo "Starting Watchdog Baseline..."
if [ -f "integrity_watchdog.py" ]; then
    python3 integrity_watchdog.py baseline
else
    echo "⚠️  WARNING: integrity_watchdog.py not found. Skipping baseline."
fi

echo "✅ FORTRESS ACTIVATED. The Architect is watching."
