from src.conexao import conectar


def listar_produtos():
    """Retorna lista de tuplas (id_produto, nome, marca, preco, estoque)."""
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_produto, nome, marca, preco, estoque "
                "FROM produto ORDER BY id_produto"
            )
            return cur.fetchall()
    finally:
        conn.close()


def cadastrar_produto(nome: str, marca: str, preco: float, estoque: int) -> None:
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO produto(nome, marca, preco, estoque) VALUES (%s, %s, %s, %s)",
                (nome, marca, preco, estoque),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def excluir_produto(id_produto: int) -> None:
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM produto WHERE id_produto = %s", (id_produto,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
