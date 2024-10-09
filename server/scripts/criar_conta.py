# import das libs de criptografia
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import json

from dotenv import load_dotenv
import os

import requests
from datetime import datetime

import random
import string


def generate_random_username(length=8):
    # Combina letras minúsculas, letras maiúsculas e dígitos
    characters = string.ascii_letters + string.digits
    # Gera um nome de usuário aleatório de um comprimento especificado
    username = "".join(random.choice(characters) for _ in range(length))
    return username


def encrypt_aes(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """
    Criptografa o texto usando AES no modo CBC.
    :param key: Chave de criptografia de 16, 24 ou 32 bytes.
    :param iv: Vetor de inicialização de 16 bytes.
    :param plaintext: Texto em claro a ser criptografado.
    :return: Texto cifrado.
    """
    # Criação do cifrador AES no modo CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Criando o objeto de criptografia
    encryptor = cipher.encryptor()

    # Preenchimento do texto em claro para ajustar ao tamanho do bloco
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Criptografando o texto em claro
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext


# carrega as variaveis de ambientes que estão no .env
load_dotenv()

# captura elas
key = os.getenv("key").encode("utf-8")

n = 10
for i in range(n):
    # cria o iv --> aqui você usa uma função de true random
    iv = os.urandom(16)

    # cria um dicionário com os dados do usuario
    username = generate_random_username(random.randint(3, 6))
    user = {"username": username, "password": "123"}

    # metadados
    metadata = {"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # body que será enviado
    body = {"user": user, "metadata": metadata}

    # passa ele pra json string (json dumps) e depois pra bytes (encode)
    byte_body = json.dumps(body).encode("utf-8")

    # criptografa o byte_data com a chave e o iv
    encrypted_body = encrypt_aes(key, iv, byte_body)

    # fiz os testes e não da pra transformar bytes em json, entao passa tudo rpa string antes de fazer o json
    encrypted_body = encrypted_body.hex()
    iv = iv.hex()

    # gera o request dict
    request = {"body": encrypted_body, "iv": iv}

    # envia o request
    hash_types = ["argon2", "pbkdf2"]
    url = f"http://127.0.0.1:8000/signup/{random.choice(hash_types)}"
    response = requests.post(url, json=request)

    # mostra o response
    print("response: ", response)
    print("status code: ", response.status_code)
    print("mensagem: ", response.text)
