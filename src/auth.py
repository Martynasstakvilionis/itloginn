import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

pepper = os.getenv("PEPPER")
if not pepper:
    raise RuntimeError("PEPPER is not set. Create a .env file with PEPPER=<secret>.")

def hash_password(key: str,
                  salt: str) -> str:
    passphrase = f"{salt}{key}{pepper}"
    return hashlib.sha512(passphrase.encode('utf-8')).hexdigest()

def is_correct_password(key: str, salt: str, hashed_password: str) -> bool:
    return hash_password(key, salt) == hashed_password
