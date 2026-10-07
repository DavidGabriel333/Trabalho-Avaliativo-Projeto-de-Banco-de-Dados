from src.conexao import conectar


def login(email: str, senha: str) -> int:
    """
    Retorna:
       0  -> login inválido
      -1  -> é gerente
      id_cliente (> 0) -> é cliente comum
    """
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_cliente, tipo FROM cliente WHERE email = %s AND senha = %s",
                (email, senha),
            )
            linha = cur.fetchone()

            if linha is None:
                return 0

            id_cliente, tipo = linha
            return -1 if tipo == "GERENTE" else id_cliente
    finally:
        conn.close()
