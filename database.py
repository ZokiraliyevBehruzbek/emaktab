import sqlite3
from datetime import datetime

DB_PATH = 'users.db'

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            last_active DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, first_name, last_name, username, last_active):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, first_name, last_name, username, last_active)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, first_name, last_name, username, last_active))
    conn.commit()
    conn.close()

def get_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_count():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_bot_start_time():
    # O'zgartirilgan start vaqtini olish funksiyasini qo'shing
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

create_table()
