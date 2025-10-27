import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_tbl_if_not_exist():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
    ''')
        

def add_new_user(login, password):
    hashed_password = hash_password(password)
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, hashed_password))
        

def check_login(login):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()
        return result is not None
    

def login_user(login, password):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()

        if result is None:
            return False

        stored_hashed_password = result[0]
        input_hashed_password = hash_password(password)

        return stored_hashed_password == input_hashed_password
    

create_tbl_if_not_exist()