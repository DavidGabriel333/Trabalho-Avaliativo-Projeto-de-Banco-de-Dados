from PySide6.QtWidgets import (
    QHBoxLayout, QHeaderView, QMessageBox, QPushButton,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from src.dao.pedido_dao import listar_vendas


class TelaVendas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vendas")
        self.resize(750, 400)

        self.tabela = QTableWidget(0, 7)
        self.tabela.setHorizontalHeaderLabels(
            ["Pedido", "Cliente", "Produto", "Qtd", "Subtotal", "Status", "Pagamento"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.close)

        botoes = QHBoxLayout()
        botoes.addWidget(btn_voltar)

        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        layout.addLayout(botoes)
        self.setLayout(layout)

        self.carregar()

    def carregar(self):
        # Usa a VIEW vw_relatorio_vendas (via PedidoDAO), em vez de
        # montar o JOIN na mão dentro da tela.
        try:
            linhas = listar_vendas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar vendas: {e}")
            return

        self.tabela.setRowCount(0)
        for i, (id_pedido, cliente, status, pagamento, produto, qtd, subtotal) in enumerate(linhas):
            self.tabela.insertRow(i)
            self.tabela.setItem(i, 0, QTableWidgetItem(str(id_pedido)))
            self.tabela.setItem(i, 1, QTableWidgetItem(cliente))
            self.tabela.setItem(i, 2, QTableWidgetItem(produto))
            self.tabela.setItem(i, 3, QTableWidgetItem(str(qtd)))
            self.tabela.setItem(i, 4, QTableWidgetItem(f"R$ {float(subtotal):.2f}"))
            self.tabela.setItem(i, 5, QTableWidgetItem(status))
            self.tabela.setItem(i, 6, QTableWidgetItem(pagamento))
