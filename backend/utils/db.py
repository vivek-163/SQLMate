import os
import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        question TEXT,
        answer TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    conn.close()
    return user[0] if user else None

def save_chat(username, question, answer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_history (username, question, answer) VALUES (%s, %s, %s)",
        (username, question, answer)
    )

    conn.commit()
    conn.close()

def get_user_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer, timestamp FROM chat_history WHERE username = %s ORDER BY timestamp DESC", (username,))
    history = cursor.fetchall()
    conn.close()
    return history



