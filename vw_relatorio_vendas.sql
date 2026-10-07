-- ============================================================
-- VIEW: vw_relatorio_vendas
-- Finalidade: consolidar em uma única consulta os dados de
-- pedido + cliente + produto + item_pedido, já calculando o
-- subtotal de cada item. Usada na tela de vendas do gerente
-- (TelaVendas), substituindo o JOIN que antes era feito
-- manualmente dentro do PedidoDAO.
-- ============================================================

CREATE OR REPLACE VIEW vw_relatorio_vendas AS
SELECT
    p.id_pedido,
    c.nome        AS cliente,
    p.data_pedido,
    p.status,
    p.pagamento,
    pr.nome       AS produto,
    i.quantidade,
    pr.preco,
    (i.quantidade * pr.preco) AS subtotal
FROM pedido p
JOIN cliente c       ON p.id_cliente  = c.id_cliente
JOIN item_pedido i   ON p.id_pedido   = i.id_pedido
JOIN produto pr      ON i.id_produto  = pr.id_produto;

-- Exemplo de uso:
-- SELECT * FROM vw_relatorio_vendas ORDER BY id_pedido;
