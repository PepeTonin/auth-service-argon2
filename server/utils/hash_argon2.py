from argon2 import PasswordHasher


def hash_password_argon2(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password_argon2(hashed_password: str, plain_password: str) -> bool:
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except:
        return False


# casos de teste
if __name__ == "__main__":

    password_1 = "password123"
    hashed_password_1 = hash_password_argon2(password_1)

    password_2 = "my_secret_pass"
    hashed_password_2 = hash_password_argon2(password_2)

    if verify_password_argon2(hashed_password_1, password_1):
        print("Teste 1: Verificação bem-sucedida")
    else:
        print("Teste 1: Falha na verificação")

    if not verify_password_argon2(hashed_password_1, password_2):
        print("Teste 2: Senha incorreta, verificação falhou como esperado")
    else:
        print("Teste 2: Verificação falhou, a senha incorreta foi aceita")

    if verify_password_argon2(hashed_password_2, password_2):
        print("Teste 3: Verificação bem-sucedida")
    else:
        print("Teste 3: Falha na verificação")

    if not verify_password_argon2(hashed_password_2, password_1):
        print("Teste 4: Senha incorreta, verificação falhou como esperado")
    else:
        print("Teste 4: Verificação falhou, a senha incorreta foi aceita")
