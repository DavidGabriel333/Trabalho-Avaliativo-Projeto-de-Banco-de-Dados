-- ============================================================
-- DML - Inserts para popular o banco e testar o sistema
-- ============================================================

-- Clientes
INSERT INTO cliente (nome, email, telefone, endereco, senha, tipo)
VALUES ('Cliente Teste', 'cliente@email.com', '999999999', 'Rua A, 123', '123', 'CLIENTE');

INSERT INTO cliente (nome, email, telefone, endereco, senha, tipo)
VALUES ('Gerente Loja', 'admin@email.com', '888888888', 'Rua B, 456', '123', 'GERENTE');

-- Produtos
INSERT INTO produto (nome, marca, preco, estoque)
VALUES ('Whey Protein', 'Growth', 120.00, 15);

INSERT INTO produto (nome, marca, preco, estoque)
VALUES ('Creatina', 'Integralmedica', 80.00, 20);

INSERT INTO produto (nome, marca, preco, estoque)
VALUES ('BCAA', 'Max Titanium', 60.00, 10);

-- Pedido de exemplo (útil para testar a View, a Function e a Procedure)
INSERT INTO pedido (id_cliente, status, pagamento)
VALUES (1, 'PENDENTE', 'PIX');

INSERT INTO item_pedido (id_pedido, id_produto, quantidade)
VALUES (1, 1, 2);
