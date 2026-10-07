import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget


class MenuCliente(QWidget):
    def __init__(self, id_cliente: int):
        super().__init__()
        self.id_cliente = id_cliente

        self.setWindowTitle("Área do Cliente")
        self.resize(380, 300)

        titulo = QLabel("MENU DO CLIENTE")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        btn_produtos = QPushButton("Ver Produtos")
        btn_carrinho = QPushButton("Carrinho")
        btn_sair = QPushButton("Sair / Logout")
        btn_sair.setObjectName("botaoPerigo")

        btn_produtos.clicked.connect(self.abrir_produtos)
        btn_carrinho.clicked.connect(self.abrir_carrinho)
        btn_sair.clicked.connect(self.logout)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(btn_produtos)
        layout.addWidget(btn_carrinho)
        layout.addWidget(btn_sair)
        layout.addStretch()
        self.setLayout(layout)

    def abrir_produtos(self):
        from src.telas.tela_produtos import TelaProdutos
        self._tela_produtos = TelaProdutos(self.id_cliente)
        self._tela_produtos.show()

    def abrir_carrinho(self):
        from src.telas.carrinho import TelaCarrinho
        self._tela_carrinho = TelaCarrinho(self.id_cliente)
        self._tela_carrinho.show()

    def logout(self):
        resposta = QMessageBox.question(self, "Logout", "Deseja voltar para o login?")
        if resposta == QMessageBox.Yes:
            from src.telas.tela_login import TelaLogin
            self.close()
            self._login_tela = TelaLogin()
            self._login_tela.show()
        else:
            sys.exit(0)
