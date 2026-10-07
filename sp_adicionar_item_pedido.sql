-- ============================================================
-- PROCEDURE: sp_adicionar_item_pedido
-- Finalidade: registrar a operação de "adicionar item ao
-- carrinho/pedido" como um processo único no banco: valida o
-- estoque, dá baixa no estoque e insere o item_pedido. Antes
-- essas 3 etapas eram feitas em statements separados dentro do
-- Java (ItemPedidoDAO); agora ficam garantidas no banco.
-- Usada na tela CarrinhoTela (ação do cliente).
-- ============================================================

CREATE OR REPLACE PROCEDURE sp_adicionar_item_pedido(
    p_id_pedido  INT,
    p_id_produto INT,
    p_quantidade INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_estoque INT;
BEGIN
    SELECT estoque INTO v_estoque
    FROM produto
    WHERE id_produto = p_id_produto;

    IF v_estoque IS NULL THEN
        RAISE EXCEPTION 'Produto não encontrado (id_produto=%)', p_id_produto;
    END IF;

    IF p_quantidade > v_estoque THEN
        RAISE EXCEPTION 'Estoque insuficiente. Disponível: %', v_estoque;
    END IF;

    UPDATE produto
    SET estoque = estoque - p_quantidade
    WHERE id_produto = p_id_produto;

    INSERT INTO item_pedido (id_pedido, id_produto, quantidade)
    VALUES (p_id_pedido, p_id_produto, p_quantidade);
END;
$$;

-- Exemplo de uso:
-- CALL sp_adicionar_item_pedido(1, 2, 3);
