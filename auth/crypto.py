import bcrypt
import re


# Hash password
def hash_password(password):

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password.encode(),
        salt
    )

    return hashed


# Check password
def check_password(password, hashed):

    return bcrypt.checkpw(
        password.encode(),
        hashed
    )


# Password strength
def is_strong_password(password):

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[!@#$%^&*]", password):
        return False

    return True