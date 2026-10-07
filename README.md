# Trabalho-Avaliativo-Projeto-de-Banco-de-Dados
Atualização do projeto de banco de dados, inserindo View, Function e Procedure.
# Sistema de Loja de Suplementos (Python + PySide6)

## Vídeo explicativo
Disponível em: https://drive.google.com/file/d/1tuQj6ajpngJzcbm7Ks0UyVMxG5LGkz3k/view?usp=sharing

## Sobre o projeto
Sistema de gerenciamento de uma loja de suplementos, com interface gráfica em **PySide6 (Qt)** e banco de dados **PostgreSQL**. Permite cadastro e controle de estoque de produtos, carrinho de compras, finalização de pedidos e acompanhamento de vendas/faturamento, com acesso separado para **Cliente** e **Gerente**.

Esta é a versão em Python do projeto (a versão original era em Java/Swing). O banco de dados é exatamente o mesmo — só a aplicação mudou de linguagem.

## Tecnologias utilizadas
- Python 3.11+
- PySide6 (Qt) — interface gráfica
- psycopg2 — conexão com o PostgreSQL
- PostgreSQL — banco de dados

## Banco de dados

**SGBD:** PostgreSQL

**Principais tabelas:** `cliente`, `produto`, `pedido`, `item_pedido`

**View criada:** `vw_relatorio_vendas`
Consolida pedido + cliente + produto + item_pedido (com subtotal calculado). Usada na tela de vendas do gerente (`tela_vendas.py`, via `pedido_dao.listar_vendas()`).

**Function criada:** `fn_valor_total_pedido(id_pedido)`
Calcula o valor total de um pedido. Usada ao finalizar um pedido (`carrinho.py`, via `pedido_dao.calcular_total_pedido()`).

**Procedure criada:** `sp_adicionar_item_pedido(id_pedido, id_produto, quantidade)`
Valida estoque, dá baixa e insere o item — tudo em uma operação no banco. Usada ao finalizar o pedido (`pedido_dao.finalizar_pedido()`).

> Ao clicar em "Finalizar Pedido", `pedido_dao.finalizar_pedido()` cria o pedido e chama a Procedure para cada item **dentro de uma única transação**. Se faltar estoque de algum item, a transação inteira é desfeita e uma mensagem de erro é mostrada — nada fica salvo pela metade.

## Estrutura do projeto

```
Projeto_loja/
│
├── src/                        # código-fonte da aplicação (Python + PySide6)
│   ├── conexao.py
│   ├── carrinho_estado.py
│   ├── estilos.py
│   ├── dao/
│   │   ├── login_dao.py
│   │   ├── produto_dao.py
│   │   └── pedido_dao.py       (View, Function e Procedure)
│   └── telas/
│       ├── tela_login.py
│       ├── menu_cliente.py
│       ├── menu_gerente.py
│       ├── tela_produtos.py
│       ├── carrinho.py
│       ├── tela_cadastro_produto.py
│       ├── tela_gerenciar_produtos.py
│       └── tela_vendas.py
│
├── database/
│   ├── tables/
│   │   ├── ddl.sql
│   │   └── migracao_add_tipo.sql
│   ├── views/
│   │   └── vw_relatorio_vendas.sql
│   ├── functions/
│   │   └── fn_valor_total_pedido.sql
│   ├── procedures/
│   │   └── sp_adicionar_item_pedido.sql
│   └── inserts/
│       └── dml.sql
│
├── docs/                        # diagramas e documentação adicional
│
├── main.py
├── requirements.txt
└── README.md
```

## Tipos de usuário (login)

### Cliente
- Visualiza produtos
- Adiciona ao carrinho
- Escolhe quantidade e forma de pagamento (PIX/CARTÃO)
- Finaliza pedidos
- Visualiza valor total da compra

### Gerente
- Cadastra produtos
- Lista e exclui produtos
- Visualiza vendas realizadas
- Acompanha faturamento total

### Dados de login de teste
Já inseridos por `database/inserts/dml.sql`.

- **Cliente:** `cliente@email.com` / senha `123`
- **Gerente:** `admin@email.com` / senha `123`

## Como executar

1. Instalar o PostgreSQL e criar o banco:
   ```sql
   CREATE DATABASE suplementos;
   ```
2. Rodar os scripts, nesta ordem:
   ```
   database/tables/ddl.sql
   database/views/vw_relatorio_vendas.sql
   database/functions/fn_valor_total_pedido.sql
   database/procedures/sp_adicionar_item_pedido.sql
   database/inserts/dml.sql
   ```
3. Instalar o Python (3.11+) e as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Ajustar a conexão em `app/conexao.py` (host, porta, usuário, senha) se necessário.
5. Executar:
   ```bash
   python main.py
   ```
