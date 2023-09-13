import base64
import os
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from hashlib import sha256

def hash256(input: str):
    return sha256(input.encode("utf-8")).hexdigest()

def load_salt() -> str:
    with open(".salt", "r") as file:
        salt = file.read()
    return salt

def save_salt(salt_: bytes) -> bytes:
    with open(".salt", "w") as file:
        salt = file.write(salt_.decode("utf-8"))
    return salt

def kdf(password: str) -> str:
    #retrieves the salt and if it doesnt exist creates one
    if Path(".salt").exists():
        salt = load_salt().encode("utf-8")
    else:
        salt = os.urandom(16)
        save_salt(salt)
    
    kdf_ = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key = base64.urlsafe_b64encode(kdf_.derive(password))
    
    return key

