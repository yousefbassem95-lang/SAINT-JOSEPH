
import sqlite3
from utils import log_message
import os

DB_NAME = "knowledge_base.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Initializes the database and creates tables if they don't exist."""
    log_message("info", f"Connecting to database at {DB_PATH}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Target Table: Main table for discovered hosts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT UNIQUE NOT NULL,
                ip_address TEXT,
                status TEXT NOT NULL DEFAULT 'new', -- e.g., 'new', 'scanned', 'compromised', 'scan_failed'
                os TEXT,
                state TEXT, -- 'up', 'down'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Ports Table: Stores open ports and services for each target
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER NOT NULL,
                port_number INTEGER NOT NULL,
                protocol TEXT NOT NULL,
                service_name TEXT,
                product TEXT,
                version TEXT,
                state TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id),
                UNIQUE (target_id, port_number, protocol)
            );
        """)

        # Vulnerabilities Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER NOT NULL,
                port_id INTEGER,
                type TEXT NOT NULL, -- e.g., 'SQL_INJECTION_COMMAND', 'WEAK_SSH_CREDENTIALS'
                description TEXT,
                tool TEXT, -- e.g., 'sqlmap', 'nmap'
                command TEXT,
                status TEXT NOT NULL DEFAULT 'potential', -- 'potential', 'confirmed', 'failed'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id),
                FOREIGN KEY (port_id) REFERENCES ports (id)
            );
        """)

        # Credentials Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                service TEXT,
                username TEXT,
                password TEXT NOT NULL,
                type TEXT, -- e.g., 'hash', 'plaintext'
                source TEXT, -- Where it was found, e.g., 'exploitation', 'osint'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            );
        """)
        
        # Intelligence Table: For storing unstructured data, links, notes, etc.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                type TEXT NOT NULL, -- e.g., 'social_media_profile', 'email_address', 'employee_name'
                source TEXT, -- The module or method that found it
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            );
        """)

        # Triggers to update 'updated_at' timestamps
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_targets_updated_at
            AFTER UPDATE ON targets
            FOR EACH ROW
            BEGIN
                UPDATE targets SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)

        conn.commit()
        log_message("info", "Database initialized successfully.")
    except sqlite3.Error as e:
        log_message("error", f"Database initialization failed: {e}")
    finally:
        if conn:
            conn.close()

# --- TARGET MANAGEMENT ---

def add_target(hostname, ip_address=None, status='new'):
    """Adds a new target to the database if it doesn't already exist."""
    sql = "INSERT INTO targets (hostname, ip_address, status) VALUES (?, ?, ?)"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (hostname, ip_address, status))
        conn.commit()
        log_message("info", f"Added new target to KB: {hostname}")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        log_message("debug", f"Target {hostname} already exists in KB.")
        # Get the existing target's ID
        cursor.execute("SELECT id FROM targets WHERE hostname = ?", (hostname,))
        return cursor.fetchone()['id']
    except sqlite3.Error as e:
        log_message("error", f"Failed to add target {hostname}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_target_status(target_id, status):
    """Updates the status of a specific target."""
    sql = "UPDATE targets SET status = ? WHERE id = ?"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (status, target_id))
        conn.commit()
    except sqlite3.Error as e:
        log_message("error", f"Failed to update status for target ID {target_id}: {e}")
    finally:
        if conn:
            conn.close()

def get_target_by_hostname(hostname):
    """Retrieves a target by its hostname."""
    sql = "SELECT * FROM targets WHERE hostname = ?"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (hostname,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        log_message("error", f"Failed to get target {hostname}: {e}")
        return None
    finally:
        if conn:
            conn.close()
            
def get_target_by_id(target_id):
    """Retrieves a target by its ID."""
    sql = "SELECT * FROM targets WHERE id = ?"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (target_id,))
    target = cursor.fetchone()
    conn.close()
    return target

def get_targets_by_status(status_list):
    """Gets all targets with a given status."""
    sql = f"SELECT * FROM targets WHERE status IN ({','.join('?'*len(status_list))})"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, status_list)
    targets = cursor.fetchall()
    conn.close()
    return targets


# --- PORT MANAGEMENT ---

def add_port_scan_results(target_id, nmap_results):
    """Adds port scan results from an Nmap scan to the database."""
    if not nmap_results or 'protocols' not in nmap_results:
        return

    # Update target main info
    sql_update_target = "UPDATE targets SET ip_address = ?, state = ? WHERE id = ?"
    conn = get_db_connection()
    try:
        with conn: # Using 'with' handles commit/rollback
            conn.execute(sql_update_target, (nmap_results.get('ip'), nmap_results.get('state'), target_id))
            
            sql_insert_port = """
                INSERT OR IGNORE INTO ports (target_id, port_number, protocol, service_name, product, version, state) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            for proto, ports in nmap_results['protocols'].items():
                for port_num, port_data in ports.items():
                    if port_data['state'] == 'open':
                        conn.execute(sql_insert_port, (
                            target_id,
                            port_num,
                            proto,
                            port_data.get('name'),
                            port_data.get('product'),
                            port_data.get('version'),
                            port_data.get('state')
                        ))
        log_message("info", f"Updated port information for target ID {target_id}.")
    except sqlite3.Error as e:
        log_message("error", f"Failed to add port scan results for target ID {target_id}: {e}")
    finally:
        if conn:
            conn.close()
            
def get_open_ports_for_target(target_id):
    """Retrieves all open ports for a specific target."""
    sql = "SELECT * FROM ports WHERE target_id = ? AND state = 'open'"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (target_id,))
    ports = cursor.fetchall()
    conn.close()
    return ports

# --- VULNERABILITY MANAGEMENT ---
def add_vulnerability(target_id, vuln_type, tool, command, port_id=None, description=None):
    sql = """
        INSERT INTO vulnerabilities (target_id, port_id, type, description, tool, command)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(sql, (target_id, port_id, vuln_type, description, tool, command))
        log_message("info", f"Added new potential vulnerability '{vuln_type}' for target ID {target_id}")
    except sqlite3.Error as e:
        log_message("error", f"Failed to add vulnerability for target ID {target_id}: {e}")
    finally:
        if conn:
            conn.close()

def get_potential_vulnerabilities(target_id):
    sql = "SELECT * FROM vulnerabilities WHERE target_id = ? AND status = 'potential'"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (target_id,))
    vulns = cursor.fetchall()
    conn.close()
    return vulns
    
def update_vulnerability_status(vuln_id, status):
    """Updates the status of a specific vulnerability."""
    sql = "UPDATE vulnerabilities SET status = ? WHERE id = ?"
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(sql, (status, vuln_id))
    except sqlite3.Error as e:
        log_message("error", f"Failed to update status for vulnerability ID {vuln_id}: {e}")
    finally:
        if conn:
            conn.close()

# --- CREDENTIALS MANAGEMENT ---
def add_credentials(password, target_id=None, service=None, username=None, cred_type='plaintext', source='exploitation'):
    sql = """
        INSERT INTO credentials (target_id, service, username, password, type, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(sql, (target_id, service, username, password, cred_type, source))
        log_message("critical", f"New credentials captured and stored in KB.")
    except sqlite3.Error as e:
        log_message("error", f"Failed to store credentials in KB: {e}")
    finally:
        if conn:
            conn.close()

# --- INTELLIGENCE MANAGEMENT ---
def add_intelligence(content, intel_type, source, target_id=None):
    """Adds a piece of intelligence to the database, ensuring no duplicates."""
    # First, check if this exact piece of intel already exists
    check_sql = "SELECT id FROM intelligence WHERE content = ? AND type = ?"
    insert_sql = """
        INSERT INTO intelligence (target_id, type, source, content)
        VALUES (?, ?, ?, ?)
    """
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(check_sql, (content, intel_type))
            if cursor.fetchone():
                log_message("debug", f"Intelligence '{content[:50]}...' already exists in KB.")
                return

            cursor.execute(insert_sql, (target_id, intel_type, source, content))
            log_message("info", f"New intelligence stored: {intel_type} - '{content[:50]}...'")
    except sqlite3.Error as e:
        log_message("error", f"Failed to store intelligence in KB: {e}")
    finally:
        if conn:
            conn.close()
