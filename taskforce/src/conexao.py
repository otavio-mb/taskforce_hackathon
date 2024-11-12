import mysql.connector
from tkinter import messagebox

# Dados de conexão com o banco de dados
DB_CONFIG = {
    'host': "localhost",
    'user': "taskforce",
    'password': "12345678",
    'database': "projeto_hackathon"
}

# Função para conectar ao banco de dados MySQL
def conectar():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
        return None


# Função para criar a tabela no banco de dados (caso não exista)
def criar_tabelas():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                valor DECIMAL(10, 2) NOT NULL,
                categoria VARCHAR(120) NOT NULL,
                data DATE NOT NULL,
                descricao VARCHAR(300)
            )
        """)
        conn.commit()
        conn.close()