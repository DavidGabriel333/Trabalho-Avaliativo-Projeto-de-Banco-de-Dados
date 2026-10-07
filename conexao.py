"""
Conexão com o banco PostgreSQL.
Equivalente ao Conexao.java original.
"""

import psycopg2

HOST = "localhost"
PORT = 5432
DATABASE = "suplementos"
USER = "postgres"
PASSWORD = "022006"


def conectar():
    """Abre e retorna uma nova conexão com o banco suplementos."""
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DATABASE,
        user=USER,
        password=PASSWORD,
    )
