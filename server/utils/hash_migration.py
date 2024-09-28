import sys
import os

# Adiciona o caminho do diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from typing import Literal
from utils.hash_argon2 import hash_password_argon2
from db.service import update_password


def verify_hashing_type(hashed_password: str) -> Literal["argon2", "pbkdf2", "other"]:
    if hashed_password.startswith(("$argon2id$", "$argon2i$", "$argon2d$")):
        return "argon2"
    elif hashed_password.startswith("$pbkdf2$"):
        return "pbkdf2"
    else:
        return "other"


def change_hash_type(username: str, plain_password: str):
    argon2_hash_password = hash_password_argon2(plain_password)
    update_password(username, argon2_hash_password)
