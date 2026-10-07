from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QHeaderView, QLabel, QMessageBox,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from src import carrinho_estado
from src.conexao import conectar
from src.dao.pedido_dao import ItemCarrinho, calcular_total_pedido, finalizar_pedido


class TelaCarrinho(QWidget):
    def __init__(self, id_cliente: int):
        super().__init__()
        self.id_cliente = id_cliente

        self.setWindowTitle("Carrinho")
        self.resize(600, 440)

        self.total_label = QLabel("Total: R$ 0,00")
        self.total_label.setObjectName("titulo")

        self.tabela = QTableWidget(0, 4)
        self.tabela.setHorizontalHeaderLabels(["Produto", "Preço", "Qtd", "Subtotal"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)

        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(["PIX", "CARTAO"])

        btn_finalizar = QPushButton("Finalizar Pedido")
        btn_voltar = QPushButton("Voltar")

        btn_finalizar.clicked.connect(self.finalizar)
        btn_voltar.clicked.connect(self.close)

        pagamento_layout = QHBoxLayout()
        pagamento_layout.addWidget(QLabel("Forma de pagamento:"))
        pagamento_layout.addWidget(self.combo_pagamento)

        botoes = QHBoxLayout()
        botoes.addWidget(btn_finalizar)
        botoes.addWidget(btn_voltar)

        layout = QVBoxLayout()
        layout.addWidget(self.total_label)
        layout.addWidget(self.tabela)
        layout.addLayout(pagamento_layout)
        layout.addLayout(botoes)
        self.setLayout(layout)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.tabela.setRowCount(0)
        total = 0.0

        conn = conectar()
        try:
            with conn.cursor() as cur:
                for linha, (id_produto, qtd) in enumerate(carrinho_estado.itens):
                    cur.execute(
                        "SELECT nome, preco FROM produto WHERE id_produto = %s",
                        (id_produto,),
                    )
                    resultado = cur.fetchone()
                    if resultado is None:
                        continue

                    nome, preco = resultado
                    preco = float(preco)
                    subtotal = preco * qtd
                    total += subtotal

                    self.tabela.insertRow(linha)
                    self.tabela.setItem(linha, 0, QTableWidgetItem(nome))
                    self.tabela.setItem(linha, 1, QTableWidgetItem(f"R$ {preco:.2f}"))
                    self.tabela.setItem(linha, 2, QTableWidgetItem(str(qtd)))
                    self.tabela.setItem(linha, 3, QTableWidgetItem(f"R$ {subtotal:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar o carrinho: {e}")
        finally:
            conn.close()

        self.total_label.setText(f"Total: R$ {total:.2f}")

    def finalizar(self):
        if not carrinho_estado.itens:
            QMessageBox.warning(self, "Carrinho", "Seu carrinho está vazio!")
            return

        pagamento = self.combo_pagamento.currentText()
        itens = [ItemCarrinho(id_produto, qtd) for id_produto, qtd in carrinho_estado.itens]

        try:
            id_pedido = finalizar_pedido(self.id_cliente, pagamento, itens)
            total = calcular_total_pedido(id_pedido)

            carrinho_estado.limpar()

            QMessageBox.information(
                self, "Pedido realizado",
                f"Pedido #{id_pedido} realizado!\nTotal: R$ {total:.2f}",
            )
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erro ao finalizar pedido", str(e))
