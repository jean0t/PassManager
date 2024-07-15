import base64
import os
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from hashlib import sha256

def hash256(input: bytes) -> str:
    return sha256(input).hexdigest()

def load_salt() -> bytes:
    with open(".salt", "rb") as file:
        salt = file.read()
    return salt

def save_salt(salt_: bytes) -> bytes:
    with open(".salt", "wb") as file:
        salt = file.write(salt_)
    return salt

def kdf(password: bytes) -> bytes:
    #retrieves the salt and if it doesnt exist creates one
    if Path(".salt").exists():
        salt = load_salt()
    else:
        salt = os.urandom(16)
        save_salt(salt)
    
    kdf_ = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key = base64.urlsafe_b64encode(kdf_.derive(password))
    return key
