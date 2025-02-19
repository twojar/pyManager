import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

#constatns
BLOCK_SIZE = 128    # for PKCs7 (in bits)
KEY_SIZE = 32       #32 bytes for AES
ITERATIONS = 100000


#Dervies a key from the master password using PBKDF2
def derive_key(master_password:str, salt:bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        iterations=ITERATIONS,
        salt=salt,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

#encrypts plaintext using AES-256 in CBC mode
def encrypt_data(plaintext: str, key:bytes) -> (bytes,bytes):

    #generate random Initialization Vector
    iv = os.urandom(16)

    #setup cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    #pad the plaintext to be a multiple of block size
    padder = padding.PKCS7(BLOCK_SIZE).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    #Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext

def decrypt_data(iv:bytes, ciphertext:bytes, key:bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    #unpad the decryped data
    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

#main for testing
"""
if __name__ == '__main__':
    master_password = "password"
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    print(key)

    text = "somepassword123"
    iv,ciphertext = encrypt_data(text,key)
    print("Cipher Text:", ciphertext)

    decrypted_text = decrypt_data(iv,ciphertext,key)
    print("Decrypted Text:", decrypted_text)
    """






