from database import get_connection

MAX_MEMORY = 10  # limit messages per session

def get_memory(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM conversation_memory
        WHERE session_id = ?
        ORDER BY timestamp ASC
        LIMIT ?
    """, (session_id, MAX_MEMORY))

    rows = cursor.fetchall()
    conn.close()

    return [{"role": role, "content": content} for role, content in rows]

def update_memory(session_id: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversation_memory (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    # 🔹 Keep memory bounded
    cursor.execute("""
        DELETE FROM conversation_memory
        WHERE id NOT IN (
            SELECT id FROM conversation_memory
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ) AND session_id = ?
    """, (session_id, MAX_MEMORY, session_id))

    conn.commit()
    conn.close()
