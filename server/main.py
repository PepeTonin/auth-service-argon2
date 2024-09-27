from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os

# Carregar as variáveis do .env
load_dotenv()

app = FastAPI()


# Configurações do banco de dados MySQL obtidas do arquivo .env
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


# Modelo de requisição para a rota de login
class UserLogin(BaseModel):
    username: str
    password: str


# Conecta ao banco de dados MySQL
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


# Inicialização do banco de dados (criando tabela se não existir)
def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Verificar e criar a tabela de usuários
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()


# Função para hashear a senha (to do)
def hash_password(password: str) -> str:
    # TODO: Implementar a lógica para gerar o hash
    pass


# Rota de login
@app.post("/login")
def login(user: UserLogin):
    hashed_password = hash_password(user.password)  # Hash da senha
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Armazenar usuário e hash da senha no banco de dados
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (user.username, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Usuário cadastrado com sucesso"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao se conectar ao banco de dados: {err}")


# Inicializar o banco de dados ao iniciar o aplicativo
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
