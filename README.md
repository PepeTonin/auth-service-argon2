## SISTEMA DE AUTENTICAÇÃO

Este projeto é um sistema de autenticação robusto que implementa um algortimo de criptografia muito seguro, o **AES**, para garantir segurança em cada etapa da comunicação entre cliente e servidor.
O sistema utiliza criptografia end-to-end para garantir a confidencialidade dos dados transmitidos e as senhas dos usuários são armazenadas com o algoritmo **Argon2**, considerado um dos mais seguros para armazenamento de senhas.

### Funcionalidades

- **Criptografia end-to-end:** Todos os dados enviados entre o cliente e o servidor são criptografados utilizando o algoritmo **AES**, garantindo que terceiros não possam interceptar ou manipular os dados.
- **Armazenamento seguro de senhas:** As senhas são armazenadas no servidor utilizando **Argon2**, um dos algoritmos mais avançados e seguros para armazenamento de senhas.
- **Atualização de hashes antigas:** Quando um usuário com uma senha armazenada em um formato de hash antigo faz login, o sistema automaticamente atualiza a senha para o formato Argon2.

### Tecnologias Utilizadas

- **FastAPI:** Framework web para criar APIs rápidas e seguras.
- **MySQL:** Banco de dados relacional usado para armazenar informações dos usuários.
- **Argon2:** Algoritmo de hashing de senhas utilizado para garantir a segurança no armazenamento.
  - implementado utilizando a biblioteca [argon2-cffi: Argon2 for Python](https://pypi.org/project/argon2-cffi/)
- **AES:** Algoritmo de criptografia simétrica usado para proteger as comunicações entre cliente e servidor.
  - implementado utilizando a biblioteca [cryptography](https://pypi.org/project/cryptography/)

### Diagrama do sistema

![diagram do sistema](/assets/diagrama-sistema-argon2.jpg)

### Endpoints, payloads e responses

#### `/signup/{hash_type}`

- Tipo: `POST`
- Descrição: Cria um novo usuário no sistema, armazenando a senha utilizando o algoritmo passado no _path paramenter_
- Payload:
  - Payload enviado na requisição:
    ```json
    {
        "body": <corpo da mensagem encriptado em hex>,
        "iv": <iv em texto claro em hex>
    }
    ```
  - Corpo da mensagem antes de encriptar:
    ```json
    {
        "user": {
            "username": <username usario>,
            "password": <senha usuario>
        },
        "metadata": {
            "created_at": <time stamp com a data de criação - formato 'YYYY-MM-DD HH:MM:SS'>
        }
    }
    ```
- Responses:
  - hash type diferente de "argon2" ou "pbkdf2"
    ```
        status_code: 400
    ```
    ```json
    {
      "detail": "Invalid hash type"
    }
    ```
  - problema na conexão com o banco
    ```
        status_code: 500
    ```
    ```json
    {
      "detail": "Failed to connect to the database"
    }
    ```
  - ok
    ```
        status_code: 201
    ```
    ```json
    {
        "message": "User created",
        "id": <user_id>
    }
    ```

#### `/login`

- Tipo: `POST`
- Descrição: Recebe as credenciais do usuário e verifica se estão corretas. Caso a autenticação seja bem sucedida e a senha esteja armazenada em um formato de hash diferente de Argon2, o sistema atualiza automaticamente a hash para o formato Argon2 no banco de dados. Se a senha já estiver no formato Argon2, nenhuma atualização é necessária.
- Payload:
  - Payload enviado na requisição:
    ```json
    {
        "body": <corpo da mensagem encriptado em hex>,
        "iv": <iv em texto claro em hex>
    }
    ```
  - Corpo da mensagem antes de encriptar:
    ```json
    {
        "user": {
            "username": <username usario>,
            "password": <senha usuario>
        },
        "metadata": {
            "created_at": <time stamp com a data da tentativa de login - formato 'YYYY-MM-DD HH:MM:SS'>
        }
    }
    ```
- Responses:
  - email ou senha incorretos
    ```
        status_code: 401
    ```
    ```json
    {
      "detail": "Auth failed"
    }
    ```
  - problema na conexão com o banco
    ```
        status_code: 500
    ```
    ```json
    {
      "detail": "Failed to connect to the database"
    }
    ```
  - ok
    ```
        status_code: 200
    ```
    ```json
    {
        "message": "Login successful",
        "id": <user_id>
    }
    ```

### Como rodar o projeto

1. **Instale as dependências**:

   - No diretório da _view_, execute:
     ```bash
     pip install -r requirements.txt
     ```
   - No diretório do _server_, execute:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configure o banco de dados MySQL**:

   - Certifique-se de que o MySQL esteja instalado e rodando no seu computador.
   - Crie o banco de dados necessário para o projeto.
    - Não é necessário criar tabelas, o server se encarrega disso.

3. **Configure o arquivo `.env`**:

   - No diretório do _server_, crie um arquivo `.env` com as seguintes variáveis:
     ```
     DB_HOST=<seu_host>
     DB_USER=<seu_usuario>
     DB_PASSWORD=<sua_senha>
     DB_NAME=<nome_do_banco_de_dados>
     key=<sua_chave_de_criptografia>
     ```
   - No diretório da _view_, também crie um arquivo `.env` com a variável:
     ```
     key=<sua_chave_de_criptografia>
     ```

4. **Execute o projeto**:
   - No diretório do _server_, execute o FastAPI em modo de desenvolvimento:
     ```bash
     fastapi dev main.py
     ```
     
   - No diretório da _view_, execute:
     ```bash
     python main.py
     ```
