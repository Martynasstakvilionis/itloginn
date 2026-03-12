from dataclasses import dataclass
from auth import hash_password, is_correct_password

import sqlite3

DATABASE = "test.db"

@dataclass
class User:
    username: str
    password: str

    fornavn: str
    etternavn: str

    _load_from_db: bool = False

    def __post_init__(self):
        if self._load_from_db:
            return
        self.username = self.username.lower()
        self.password = hash_password(self.password, self.username)
        self.save_to_db()

    def save_to_db(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO users (
            username,
            password,
            fornavn,
            etternavn
        ) VALUES (:username, 
                  :password, 
                  :fornavn, 
                  :etternavn)""", self.__dict__)
        conn.commit()
        conn.close()

    def check_password(self, password: str) -> bool:
        return is_correct_password(password, self.username, self.password)

    @property
    def fullt_navn(self):
        return f"{self.fornavn} {self.etternavn}"

def get_all() -> dict[str, User]:
    data = {}

    # SQL (tullball)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

    for row in cursor.fetchall():
        # 0 = username, 1 = pass, 2 = fornavn, 3 = etternavn
        data[row[0]] = User(*row, _load_from_db=True)

    # Ferdig med SQL
    conn.close()
    return data

def get(username: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

    data = User(*cursor.fetchone(), _load_from_db=True)

    conn.close()
    return data

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        fornavn TEXT,
        etternavn TEXT,
        UNIQUE(username)
    )
    """)
    conn.commit()
    conn.close()

init_db()
