import sqlite3
import hashlib
import json
import os
from pathlib import Path

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_base_dir():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    return str(BASE_DIR)


def add_new_user(login, password):
    hashed_password = hash_password(password)
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, hashed_password))
        create_user_folder(login)
        cursor.execute('INSERT INTO folders (login, login_folder) VALUES (?, ?)', (login, f"{get_base_dir()}/easy2notes/Folder_{login}"))
        

def check_login(login):
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()

        if result == None:
            return False
        else:
            return True
    

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

        cursor.execute('''
    CREATE TABLE IF NOT EXISTS face_encodings (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    encoding TEXT NOT NULL,
    FOREIGN KEY (login) REFERENCES users (login)
    )
    ''')
        

def create_user_folder(login):
    try:
        Path(f"{get_base_dir()}/easy2notes").mkdir()
    except Exception:
        pass
    Path(f"{get_base_dir()}/easy2notes/Folder_{login}").mkdir()


def user_get_folder(login):
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT login_folder FROM folders WHERE login = ?", (login,))
        result = cursor.fetchone()
        return result[0]


def store_face_encoding(login, encoding):
    encoding_json = json.dumps(encoding)
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO face_encodings (login, encoding) VALUES (?, ?)', (login, encoding_json))


def get_face_encodings(login):
    with sqlite3.connect("easy2notes_base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT encoding FROM face_encodings WHERE login = ?", (login,))
        results = cursor.fetchall()
        encodings = [json.loads(row[0]) for row in results]
        return encodings
    
create_tbl_if_not_exist()
