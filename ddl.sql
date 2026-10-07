-- ============================================================
-- DDL - Criação das tabelas do sistema
-- ============================================================

CREATE TABLE cliente (
  id_cliente SERIAL PRIMARY KEY,
  nome VARCHAR,
  email VARCHAR UNIQUE,
  telefone VARCHAR,
  endereco TEXT,
  senha VARCHAR,
  tipo VARCHAR(10) NOT NULL DEFAULT 'CLIENTE' CHECK (tipo IN ('CLIENTE', 'GERENTE'))
);

CREATE TABLE produto (
  id_produto SERIAL PRIMARY KEY,
  nome VARCHAR UNIQUE,
  marca VARCHAR,
  preco DECIMAL,
  estoque INT
);

CREATE TABLE pedido (
  id_pedido SERIAL PRIMARY KEY,
  id_cliente INT REFERENCES cliente(id_cliente),
  data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR,
  pagamento VARCHAR
);

CREATE TABLE item_pedido (
  id_item SERIAL PRIMARY KEY,
  id_pedido INT REFERENCES pedido(id_pedido),
  id_produto INT REFERENCES produto(id_produto),
  quantidade INT
);
