import sqlite3
import hashlib
from pathlib import Path

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_new_user(login, password):
    hashed_password = hash_password(password)
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, hashed_password))
        create_user_folder(login)
        cursor.execute('INSERT INTO folders (login, login_folder) VALUES (?, ?)', (login, fr"C:\Users\Silentfeel\easy2notes_folders\Folder_{login}"))
        

def check_login(login):
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()
        return result is not None
    

def login_user(login, password):
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()

        if result is None:
            return False

        stored_hashed_password = result[0]
        input_hashed_password = hash_password(password)

        return stored_hashed_password == input_hashed_password
    

def create_tbl_if_not_exist():
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
    ''')
        
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    login_folder TEXT NOT NULL
    )
    ''')
        

def create_user_folder(login):
    try:
        Path(fr"C:\Users\Silentfeel\easy2notes_folders").mkdir()
    except Exception:
        pass
    Path(fr"C:\Users\Silentfeel\easy2notes_folders\Folder_{login}").mkdir()


def user_get_folder(login):
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT login_folder FROM folders WHERE login = ?", (login,))
        result = cursor.fetchone()
        return result[0]


create_tbl_if_not_exist()

