# 🛡️ SECURE CODING STANDARDS: THE ARCHITECT'S COMMANDMENTS
**Owner:** Youssef Bassem (JOJO / JUPITER)

> **DIRECTIVE:** Every line of code written in this project MUST adhere to these commandments. Failure is not an option.

---

## 1. INPUT VALIDATION (The First Wall)
*   **Rule:** NEVER trust user input. Validate everything.
*   **Action:**
    *   Use parameterized queries (e.g., `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))`) to prevent SQL Injection.
    *   Sanitize HTML input (e.g., `DOMPurify` or `bleach`) to prevent XSS.
    *   Validate file uploads (MIME type + extension + content analysis).
    *   Limit input length and character set (e.g., allow only alphanumeric for usernames).

## 2. AUTHENTICATION & SESSION MANAGEMENT (The Gatekeeper)
*   **Rule:** Use proven libraries. Do not reinvent the wheel.
*   **Action:**
    *   Use bcrypt or Argon2 for password hashing (min work factor 12).
    *   Implement Multi-Factor Authentication (MFA) for admin access.
    *   Use HTTPOnly and Secure flags for session cookies.
    *   Implement account lockout policies after 5 failed attempts.

## 3. ACCESS CONTROL (The Throne Room)
*   **Rule:** Least Privilege Principle.
*   **Action:**
    *   Grant only necessary permissions to users/roles.
    *   Verify authorization on EVERY request (backend enforcement, not just UI hiding).
    *   Use UUIDs instead of sequential IDs (e.g., `123e4567-e89b...` instead of `101`) to prevent ID enumeration.

## 4. DATA PROTECTION (The Vault)
*   **Rule:** Encrypt sensitive data at rest and in transit.
*   **Action:**
    *   Use TLS 1.2+ for all communication (HTTPS everywhere).
    *   Encrypt sensitive database columns (PII, tokens) using AES-256 (GCM mode).
    *   Never log sensitive data (passwords, tokens, PII).
    *   Use environment variables for secrets (`.env`), NEVER hardcode them.

## 5. ERROR HANDLING & LOGGING (The Watchtower)
*   **Rule:** Fail securely. Do not leak information.
*   **Action:**
    *   Display generic error messages to users ("Something went wrong"), log detailed errors internally.
    *   Log security events (failed logins, access denied, sensitive actions).
    *   Protect log files from unauthorized access.

## 6. SYSTEM CONFIGURATION (The Fortress Walls)
*   **Rule:** Keep software up-to-date and harden the OS.
*   **Action:**
    *   Remove default accounts and sample files.
    *   Disable directory listing on web servers.
    *   Set strict file permissions (chmod 600 for config/keys).
    *   Regularly patch OS and libraries.

## 7. DEPENDENCY MANAGEMENT (Supply Chain)
*   **Rule:** Trust but verify.
*   **Action:**
    *   Use `npm audit` or `pip-audit` to check dependencies for vulnerabilities.
    *   Pin dependency versions in `package.json` or `requirements.txt`.
    *   Avoid using abandoned or unmaintained libraries.

---

## ✅ ARCHITECT'S CHECKLIST (Before Release)
- [ ] Watchdog Baseline created?
- [ ] Secrets scanned (gitleaks)?
- [ ] Dependencies audited?
- [ ] Input validation verified?
- [ ] Error messages checked for leaks?
