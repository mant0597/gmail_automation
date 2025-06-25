import sqlite3

DB_NAME = 'emails.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            snippet TEXT,
            received_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO emails (id, sender, subject, snippet, received_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (email['id'], email['sender'], email['subject'], email['snippet'], email['received_at']))
    conn.commit()
    conn.close()

def get_all_emails():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emails')
    return cursor.fetchall()
