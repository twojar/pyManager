import sqlite3
from src.core import encryption
from src.core.encryption import decrypt_data

DATABASE_FILE = "passwords.db"

#Create connection to SQL database
def create_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    return conn

#create the tables if they don't exist
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY,
    site TEXT NOT NULL,
    username TEXT,
    iv BLOB NOT NULL,
    ciphertext BLOB NOT NULL,
    '''
    )
    conn.commit()
    conn.close()
    return

def add_password(site: str, username: str, iv: str, ciphertext: str):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO passwords (site, username, iv, ciphertext) VALUES (?, ?, ?, ?) ''', (site, username, iv, ciphertext))
    conn.commit()
    conn.close()
    return

def get_all_passwords(key:bytes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT site, username, iv, ciphertext FROM passwords''')
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        record_id, site, username, iv, ciphertext = row
        password = decrypt_data(iv,ciphertext,key)
        results.append({
            'id': record_id,
            'site': site,
            'username': username,
            'password': password
        })
    return results
    







