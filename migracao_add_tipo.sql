-- ============================================================
-- MIGRAÇÃO: use este script SOMENTE SE a tabela "cliente" já
-- existir no seu banco SEM a coluna "tipo" (ex: banco criado
-- antes desta correção). Se você está criando o banco do zero,
-- ignore este arquivo — o ddl.sql já inclui a coluna "tipo".
-- ============================================================

ALTER TABLE cliente
  ADD COLUMN IF NOT EXISTS tipo VARCHAR(10) NOT NULL DEFAULT 'CLIENTE'
  CHECK (tipo IN ('CLIENTE', 'GERENTE'));

-- Se você já tinha um usuário gerente inserido manualmente, marque-o:
-- UPDATE cliente SET tipo = 'GERENTE' WHERE email = 'admin@email.com';
