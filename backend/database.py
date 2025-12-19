import sqlite3

DB_NAME = "interactions.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            query TEXT,
            agent TEXT,
            response TEXT,
            latency_ms REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def log_interaction(session_id, query, agent, response, latency_ms):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interactions (session_id, query, agent, response, latency_ms)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, query, agent, response, latency_ms))

    conn.commit()
    conn.close()

def get_analytics_summary():
    conn = get_connection()
    cursor = conn.cursor()

    # Agent usage
    cursor.execute("""
        SELECT agent, COUNT(*) 
        FROM interactions 
        GROUP BY agent 
        ORDER BY COUNT(*) DESC
    """)
    agent_counts = cursor.fetchall()

    # Avg latency per agent
    cursor.execute("""
        SELECT agent, ROUND(AVG(latency_ms), 2)
        FROM interactions
        GROUP BY agent
    """)
    latency_data = cursor.fetchall()

    # Peak hour
    cursor.execute("""
        SELECT strftime('%H', timestamp), COUNT(*) 
        FROM interactions 
        GROUP BY strftime('%H', timestamp)
        ORDER BY COUNT(*) DESC 
        LIMIT 1
    """)
    peak_hour = cursor.fetchone()

    conn.close()

    return {
        "agent_usage": {a: c for a, c in agent_counts},
        "average_latency_ms": {a: l for a, l in latency_data},
        "most_used_agent": agent_counts[0][0] if agent_counts else None,
        "peak_usage_hour": peak_hour[0] if peak_hour else None
    }
