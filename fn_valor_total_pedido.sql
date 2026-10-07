-- ============================================================
-- FUNCTION: fn_valor_total_pedido
-- Finalidade: calcular o valor total de um pedido somando
-- (preço x quantidade) de todos os itens vinculados a ele.
-- Usada na tela do cliente ao finalizar o pedido e ao listar
-- seus pedidos (CarrinhoTela / MenuClienteTela).
-- ============================================================

CREATE OR REPLACE FUNCTION fn_valor_total_pedido(p_id_pedido INT)
RETURNS NUMERIC AS $$
DECLARE
    v_total NUMERIC;
BEGIN
    SELECT COALESCE(SUM(pr.preco * i.quantidade), 0)
    INTO v_total
    FROM item_pedido i
    JOIN produto pr ON i.id_produto = pr.id_produto
    WHERE i.id_pedido = p_id_pedido;

    RETURN v_total;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso:
-- SELECT fn_valor_total_pedido(1);
