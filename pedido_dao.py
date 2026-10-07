"""
DAO de pedidos — é aqui que a View, a Function e a Procedure do
banco são usadas de verdade pela aplicação.
"""

from dataclasses import dataclass

from src.conexao import conectar


@dataclass
class ItemCarrinho:
    id_produto: int
    quantidade: int


def finalizar_pedido(id_cliente: int, pagamento: str, itens: list[ItemCarrinho]) -> int:
    """
    Finaliza um pedido de forma ATÔMICA:
      1) cria o pedido com status PENDENTE;
      2) adiciona cada item chamando a PROCEDURE sp_adicionar_item_pedido
         (que valida e dá baixa no estoque);
      3) só marca o pedido como FINALIZADO se TODOS os itens forem
         inseridos com sucesso.

    Se qualquer item falhar (ex: estoque insuficiente), a transação
    inteira é desfeita (ROLLBACK) — nada fica gravado pela metade.

    Retorna o id do pedido criado. Lança Exception com mensagem
    amigável em caso de falha.
    """
    if not itens:
        raise ValueError("O carrinho está vazio.")

    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO pedido(id_cliente, status, pagamento) "
                "VALUES (%s, 'PENDENTE', %s) RETURNING id_pedido",
                (id_cliente, pagamento),
            )
            id_pedido = cur.fetchone()[0]

            for item in itens:
                # CALL direto (não "{call ...}"): é a forma correta de
                # chamar uma PROCEDURE (não uma function) no PostgreSQL.
                cur.execute(
                    "CALL sp_adicionar_item_pedido(%s, %s, %s)",
                    (id_pedido, item.id_produto, item.quantidade),
                )

            cur.execute(
                "UPDATE pedido SET status = 'FINALIZADO' WHERE id_pedido = %s",
                (id_pedido,),
            )

        conn.commit()
        return id_pedido

    except Exception as e:
        conn.rollback()
        raise Exception(f"Não foi possível finalizar o pedido: {e}") from e
    finally:
        conn.close()


def calcular_total_pedido(id_pedido: int) -> float:
    """Usa a FUNCTION fn_valor_total_pedido(id_pedido)."""
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT fn_valor_total_pedido(%s)", (id_pedido,))
            return float(cur.fetchone()[0])
    finally:
        conn.close()


def listar_vendas():
    """
    Usa a VIEW vw_relatorio_vendas. Cada linha retornada:
    (id_pedido, cliente, status, pagamento, produto, quantidade, subtotal)
    """
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_pedido, cliente, status, pagamento, produto, quantidade, subtotal "
                "FROM vw_relatorio_vendas ORDER BY id_pedido"
            )
            return cur.fetchall()
    finally:
        conn.close()


def total_faturamento() -> float:
    """Faturamento total, somando a coluna subtotal da VIEW."""
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(SUM(subtotal), 0) FROM vw_relatorio_vendas")
            return float(cur.fetchone()[0])
    finally:
        conn.close()
