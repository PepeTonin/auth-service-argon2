import os
import json
import requests

import tkinter as tk
from tkinter import messagebox

from dotenv import load_dotenv
from datetime import datetime

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Carrega as variáveis de ambiente
load_dotenv()


# Função para gerar IV aleatório
def generate_iv():
    return os.urandom(16)


# Função para criptografar dados
def encrypt_data(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
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


# Função para fazer signup
def signup():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Erro", "Preencha todos os campos")
        return

    # Estrutura do JSON que será enviado para a API
    data = {
        "user": {"username": username, "password": password},
        "metadata": {"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    }

    # Cria o body para criptografia
    bytes_body = json.dumps(data).encode("utf-8")
    iv = generate_iv()
    key = os.getenv("key").encode("utf-8")
    encrypted_data = encrypt_data(key, iv, bytes_body)

    # Converte os dados para hexadecimal
    encrypted_data_hex = encrypted_data.hex()
    iv_hex = iv.hex()

    # Cria o payload a ser enviado
    request = {"body": encrypted_data_hex, "iv": iv_hex}

    # Envia os dados para a rota de signup: ARGON2 / PBKDF2
    # url = "http://127.0.0.1:8000/signup/pbkdf2"
    url = "http://127.0.0.1:8000/signup/argon2"
    try:
        response = requests.post(url, json=request)
        # Trata a resposta
        handle_response(response)
    except:
        messagebox.showerror("Erro", "Erro ao se conectar com o servidor")


# Função para fazer login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Erro", "Preencha todos os campos")
        return

    # Estrutura do JSON que será enviado para a API
    data = {
        "user": {"username": username, "password": password},
        "metadata": {"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    }

    # Cria o body para criptografia
    bytes_body = json.dumps(data).encode("utf-8")
    iv = generate_iv()
    key = os.getenv("key").encode("utf-8")
    encrypted_data = encrypt_data(key, iv, bytes_body)

    # Converte os dados para hexadecimal
    encrypted_data_hex = encrypted_data.hex()
    iv_hex = iv.hex()

    # Cria o payload a ser enviado
    request = {"body": encrypted_data_hex, "iv": iv_hex}

    # Envia os dados para a rota de login
    url = "http://127.0.0.1:8000/login"
    try:
        response = requests.post(url, json=request)
        # Trata a resposta
        handle_response(response)
    except:
        messagebox.showerror("Erro", "Erro ao se conectar com o servidor")


# Função para tratar a resposta do servidor
def handle_response(response):
    if response.status_code == 400:
        messagebox.showerror("Erro", "Rota inválida")
    elif response.status_code == 401:
        messagebox.showerror("Erro", "Usuário ou senha inválidos")
    elif response.status_code == 500:
        messagebox.showerror("Erro", "Erro no servidor")
    elif response.status_code == 201:
        user_id = response.json().get("id", "ID não disponível.")
        messagebox.showinfo("Conta criada", f"Usuário criado com sucesso\nUser ID: {user_id}")
    elif response.status_code == 200:
        user_id = response.json().get("id", "ID não disponível.")
        messagebox.showinfo("Sucesso", f"Login efetuado com sucesso\nUser ID: {user_id}")
    else:
        messagebox.showwarning("Alerta", "Resposta não reconhecida do servidor")
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# Criação da interface gráfica
root = tk.Tk()
root.title("Login / Criar conta")

# Labels e campos de entrada
tk.Label(root, text="Nome de usuário:").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Botões de signup e login
signup_button = tk.Button(root, text="Criar Conta", command=signup)
signup_button.grid(row=2, column=0, padx=10, pady=10)

login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=1, padx=10, pady=10)

# Inicia a interface gráfica
root.mainloop()
