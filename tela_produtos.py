from PySide6.QtWidgets import (
    QHBoxLayout, QHeaderView, QInputDialog, QMessageBox,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from src.carrinho_estado import adicionar_item
from src.dao.produto_dao import listar_produtos


class TelaProdutos(QWidget):
    def __init__(self, id_cliente: int):
        super().__init__()
        self.id_cliente = id_cliente

        self.setWindowTitle("Produtos")
        self.resize(650, 400)

        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Marca", "Preço", "Estoque"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)

        btn_adicionar = QPushButton("Adicionar ao Carrinho")
        btn_atualizar = QPushButton("Atualizar")
        btn_voltar = QPushButton("Voltar")

        btn_adicionar.clicked.connect(self.adicionar_carrinho)
        btn_atualizar.clicked.connect(self.carregar_produtos)
        btn_voltar.clicked.connect(self.close)

        botoes = QHBoxLayout()
        botoes.addWidget(btn_adicionar)
        botoes.addWidget(btn_atualizar)
        botoes.addWidget(btn_voltar)

        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        layout.addLayout(botoes)
        self.setLayout(layout)

        self.carregar_produtos()

    def carregar_produtos(self):
        self.tabela.setRowCount(0)

        try:
            produtos = listar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os produtos: {e}")
            return

        for linha, (id_produto, nome, marca, preco, estoque) in enumerate(produtos):
            self.tabela.insertRow(linha)
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(id_produto)))
            self.tabela.setItem(linha, 1, QTableWidgetItem(nome))
            self.tabela.setItem(linha, 2, QTableWidgetItem(marca))
            self.tabela.setItem(linha, 3, QTableWidgetItem(f"R$ {float(preco):.2f}"))
            self.tabela.setItem(linha, 4, QTableWidgetItem(str(estoque)))

    def adicionar_carrinho(self):
        linha = self.tabela.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Produtos", "Selecione um produto!")
            return

        id_produto = int(self.tabela.item(linha, 0).text())
        estoque = int(self.tabela.item(linha, 4).text())

        qtd, ok = QInputDialog.getInt(self, "Quantidade", "Quantidade:", 1, 1, 1_000_000)

        if not ok:
            return  # usuário cancelou a caixa de diálogo

        # Checagem só de UX (feedback imediato). A validação definitiva
        # e à prova de concorrência acontece no banco, na PROCEDURE
        # sp_adicionar_item_pedido, quando o pedido é finalizado.
        if qtd > estoque:
            QMessageBox.warning(self, "Produtos", f"Estoque insuficiente! Disponível: {estoque}")
            return

        adicionar_item(id_produto, qtd)
        QMessageBox.information(self, "Produtos", "Produto adicionado ao carrinho!")
