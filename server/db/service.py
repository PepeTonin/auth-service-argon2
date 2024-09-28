import os
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()


def create_new_user(username: str, password: str, created_at: datetime) -> int:
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password, created_at) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, created_at))
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return user_id


def get_user_by_username(username: str) -> dict | None:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def update_password(username: str, new_password: str) -> bool:
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET password = %s WHERE username = %s"
    cursor.execute(query, (new_password, username))
    connection.commit()
    cursor.close()
    connection.close()
    return True
