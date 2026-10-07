"""
Estado do carrinho, compartilhado entre TelaProdutos e TelaCarrinho.
Equivalente à lista estática que existia dentro de CarrinhoTela.java
no projeto original em Java.
"""

itens: list[tuple[int, int]] = []  # cada item: (id_produto, quantidade)


def adicionar_item(id_produto: int, quantidade: int) -> None:
    itens.append((id_produto, quantidade))


def limpar() -> None:
    itens.clear()
