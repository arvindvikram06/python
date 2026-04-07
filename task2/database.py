import sqlite3
import os

DB_FILE = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT NOT NULL,
            sender TEXT NOT NULL,
            recipient TEXT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_rooms():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM rooms')
    rooms = [row[0] for row in cursor.fetchall()]
    conn.close()
    return rooms

def create_room(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO rooms (name) VALUES (?)', (name,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def save_message(room, sender, content, recipient=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (room, sender, recipient, content)
        VALUES (?, ?, ?, ?)
    ''', (room, sender, recipient, content))
    conn.commit()
    conn.close()

def get_messages(room):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sender, recipient, content, timestamp 
        FROM messages 
        WHERE room = ? AND recipient IS NULL
        ORDER BY timestamp ASC
    ''', (room,))
    messages = [
        {"sender": r[0], "recipient": r[1], "content": r[2], "timestamp": r[3]}
        for r in cursor.fetchall()
    ]
    conn.close()
    return messages

def get_private_messages(room, user1, user2):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sender, recipient, content, timestamp 
        FROM messages 
        WHERE room = ? AND sender IN (?, ?) AND recipient IN (?, ?)
        ORDER BY timestamp ASC
    ''', (room, user1, user2, user1, user2))
    messages = [
        {"sender": r[0], "recipient": r[1], "content": r[2], "timestamp": r[3]}
        for r in cursor.fetchall()
    ]
    conn.close()
    return messages

if not os.path.exists(DB_FILE):
    init_db()
else:
    init_db()
