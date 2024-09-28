import hashlib
import secrets


def hash_password_pbkdf2(password: str) -> str:
    hash_config = {
        "hash_name": "sha256",
        "salt": secrets.token_bytes(16),
        "iterations": 600_000,
    }

    dk = hashlib.pbkdf2_hmac(**hash_config, password=password.encode("utf-8"))

    hashed_password = (
        f"$pbkdf2"
        + f"${hash_config['hash_name']}"
        + f"${hash_config['salt'].hex()}"
        + f"${hash_config['iterations']}"
        + f"${dk.hex()}"
    )

    return hashed_password


def verify_password_pbkdf2(hashed_password: str, plain_password: str) -> bool:
    hash_params = hashed_password.split("$")

    if len(hash_params) != 6 or hash_params[1] != "pbkdf2":
        return False

    hash_config = {
        "hash_name": hash_params[2],
        "salt": bytes.fromhex(hash_params[3]),
        "iterations": int(hash_params[4]),
    }

    dk = hashlib.pbkdf2_hmac(**hash_config, password=plain_password.encode("utf-8"))

    return dk.hex() == hash_params[5]


# casos de teste
if __name__ == "__main__":

    password_1 = "my_secure_password"
    hashed_password_1 = hash_password_pbkdf2(password_1)

    password_2 = "another_password"
    hashed_password_2 = hash_password_pbkdf2(password_2)

    if verify_password_pbkdf2(hashed_password_1, password_1):
        print("Teste 1: Verificação bem-sucedida")
    else:
        print("Teste 1: Falha na verificação")

    if not verify_password_pbkdf2(hashed_password_1, password_2):
        print("Teste 2: Senha incorreta, verificação falhou como esperado")
    else:
        print("Teste 2: Verificação falhou, a senha incorreta foi aceita")

    if verify_password_pbkdf2(hashed_password_2, password_2):
        print("Teste 3: Verificação bem-sucedida")
    else:
        print("Teste 3: Falha na verificação")

    if not verify_password_pbkdf2(hashed_password_2, password_1):
        print("Teste 4: Verificação falhou como esperado, as senhas não correspondem")
    else:
        print("Teste 4: Falha na verificação, aceitou senha incorreta")
