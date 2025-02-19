from src.core import auth
from src.core import gui

#only run if there's no master password hash yet
def setup_master_password():
    stored_hash = auth.load_master_password_hash()
    print(stored_hash)
    if stored_hash is None:
        master_password = input("Set Master Password: ")
        hash_value = auth.create_master_hash(master_password)
        auth.store_master_hash(hash_value)
        print("Master Password Set.")
    else:
        print("Master Password is already set..")
def login() -> bool:
    stored_hash = auth.load_master_password_hash()
    if stored_hash is None:
        print("No Master Password set. Set it up first.")
        return True
    master_password = input("Enter your master password: ")
    if auth.verify_master_hash(master_password, stored_hash):
        print("Login Successful.")
        return True
    else:
        print("Incorrect Master Password.")
    return False

if __name__ == "__main__":
    setup_master_password()
    if login():
        gui.main()