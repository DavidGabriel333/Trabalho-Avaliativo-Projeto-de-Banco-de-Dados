from PySide6.QtWidgets import (
    QHBoxLayout, QHeaderView, QMessageBox, QPushButton,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from src.dao.produto_dao import excluir_produto, listar_produtos


class TelaGerenciarProdutos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Produtos")
        self.resize(600, 400)

        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Marca", "Preço", "Estoque"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)

        btn_excluir = QPushButton("Excluir Produto")
        btn_excluir.setObjectName("botaoPerigo")
        btn_atualizar = QPushButton("Atualizar")
        btn_voltar = QPushButton("Voltar")

        btn_excluir.clicked.connect(self.excluir)
        btn_atualizar.clicked.connect(self.carregar)
        btn_voltar.clicked.connect(self.close)

        botoes = QHBoxLayout()
        botoes.addWidget(btn_excluir)
        botoes.addWidget(btn_atualizar)
        botoes.addWidget(btn_voltar)

        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        layout.addLayout(botoes)
        self.setLayout(layout)

        self.carregar()

    def carregar(self):
        self.tabela.setRowCount(0)

        try:
            produtos = listar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar: {e}")
            return

        for linha, (id_produto, nome, marca, preco, estoque) in enumerate(produtos):
            self.tabela.insertRow(linha)
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(id_produto)))
            self.tabela.setItem(linha, 1, QTableWidgetItem(nome))
            self.tabela.setItem(linha, 2, QTableWidgetItem(marca))
            self.tabela.setItem(linha, 3, QTableWidgetItem(f"R$ {float(preco):.2f}"))
            self.tabela.setItem(linha, 4, QTableWidgetItem(str(estoque)))

    def excluir(self):
        linha = self.tabela.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Gerenciar Produtos", "Selecione um produto!")
            return

        id_produto = int(self.tabela.item(linha, 0).text())

        try:
            excluir_produto(id_produto)
            QMessageBox.information(self, "Gerenciar Produtos", "Produto excluído!")
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir: {e}")
