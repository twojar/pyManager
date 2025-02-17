import json
import os
from argon2 import *

#create a PasswordHasher object
ph = PasswordHasher()
HASH_FILE = "master_hash.json"

#create the hashed password
def create_master_hash(master_password: str) -> str:
    return ph.hash(master_password)

#verifiy master password against stored hash
def verify_master_hash(master_password: str, stored_hash: str) -> bool:
    try:
        ph.verify(stored_hash, master_password)
        return True
    except exceptions.VerifyMismatchError:
        return False

#store hashed password in json file "master_hash.json"
def store_master_hash(hash_value: str, filename: str = HASH_FILE):
    data = {"master_hash": hash_value}
    with open(filename, "w") as file:
        json.dump(data, file)
        #set file permission to be read/write for user only
    try:
        os.chmod(filename, 0o600)
    except Exception as e:
        print(f"Unable to set file permissions: {e}")

def load_master_password_hash(filename: str = HASH_FILE) -> str:
    if os.path.exists(filename):
        with open(filename) as file:
            data = json.load(file)
        return data.get("master_hash")
    return None

