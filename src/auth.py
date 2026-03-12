import hashlib

pepper = "123"  # TODO: Bruk .env

def hash_password(key: str,
                  salt: str) -> str:
    # Step 1: Construct passphrase
    passphrase = f"{salt}{key}{pepper}"
    return hashlib.sha512(passphrase.encode('utf-8')).hexdigest()

def is_correct_password(key: str, salt: str, hashed_password: str) -> bool:
    return hash_password(key, salt) == hashed_password
