import psycopg2

from PySide6.QtWidgets import (
    QFormLayout, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from src.dao.produto_dao import cadastrar_produto


class TelaCadastroProduto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastrar Produto")
        self.resize(320, 260)

        self.campo_nome = QLineEdit()
        self.campo_marca = QLineEdit()
        self.campo_preco = QLineEdit()
        self.campo_estoque = QLineEdit()

        form = QFormLayout()
        form.addRow("Nome:", self.campo_nome)
        form.addRow("Marca:", self.campo_marca)
        form.addRow("Preço:", self.campo_preco)
        form.addRow("Estoque:", self.campo_estoque)

        btn_salvar = QPushButton("Salvar")
        btn_voltar = QPushButton("Voltar")

        btn_salvar.clicked.connect(self.salvar)
        btn_voltar.clicked.connect(self.close)

        botoes = QHBoxLayout()
        botoes.addWidget(btn_salvar)
        botoes.addWidget(btn_voltar)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(botoes)
        self.setLayout(layout)

    def salvar(self):
        nome = self.campo_nome.text().strip()
        marca = self.campo_marca.text().strip()
        preco_txt = self.campo_preco.text().strip().replace(",", ".")
        estoque_txt = self.campo_estoque.text().strip()

        if not nome or not marca or not preco_txt or not estoque_txt:
            QMessageBox.warning(self, "Cadastro", "Preencha todos os campos!")
            return

        try:
            preco = float(preco_txt)
            estoque = int(estoque_txt)
        except ValueError:
            QMessageBox.warning(self, "Cadastro", "Preço e estoque devem ser números válidos!")
            return

        if preco <= 0:
            QMessageBox.warning(self, "Cadastro", "O preço deve ser maior que zero!")
            return

        if estoque < 0:
            QMessageBox.warning(self, "Cadastro", "O estoque não pode ser negativo!")
            return

        try:
            cadastrar_produto(nome, marca, preco, estoque)
            QMessageBox.information(self, "Cadastro", "Produto cadastrado!")
            self.close()
        except psycopg2.errors.UniqueViolation:
            QMessageBox.warning(self, "Cadastro", "Já existe um produto com esse nome!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar: {e}")
