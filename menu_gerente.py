import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from src.dao.pedido_dao import total_faturamento


class MenuGerente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerente")
        self.resize(350, 360)

        titulo = QLabel("MENU DO GERENTE")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        btn_cadastrar = QPushButton("Cadastrar Produto")
        btn_gerenciar = QPushButton("Gerenciar Produtos")
        btn_vendas = QPushButton("Ver Vendas")
        btn_faturamento = QPushButton("Faturamento")
        btn_sair = QPushButton("Sair / Logout")
        btn_sair.setObjectName("botaoPerigo")

        btn_cadastrar.clicked.connect(self.abrir_cadastro)
        btn_gerenciar.clicked.connect(self.abrir_gerenciar)
        btn_vendas.clicked.connect(self.abrir_vendas)
        btn_faturamento.clicked.connect(self.ver_faturamento)
        btn_sair.clicked.connect(self.logout)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        for botao in (btn_cadastrar, btn_gerenciar, btn_vendas, btn_faturamento, btn_sair):
            layout.addWidget(botao)
        layout.addStretch()
        self.setLayout(layout)

    def abrir_cadastro(self):
        from src.telas.tela_cadastro_produto import TelaCadastroProduto
        self._tela_cadastro = TelaCadastroProduto()
        self._tela_cadastro.show()

    def abrir_gerenciar(self):
        from src.telas.tela_gerenciar_produtos import TelaGerenciarProdutos
        self._tela_gerenciar = TelaGerenciarProdutos()
        self._tela_gerenciar.show()

    def abrir_vendas(self):
        from src.telas.tela_vendas import TelaVendas
        self._tela_vendas = TelaVendas()
        self._tela_vendas.show()

    def ver_faturamento(self):
        try:
            total = total_faturamento()
            QMessageBox.information(self, "Faturamento", f"Faturamento: R$ {total:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular faturamento: {e}")

    def logout(self):
        resposta = QMessageBox.question(self, "Logout", "Deseja voltar para o login?")
        if resposta == QMessageBox.Yes:
            from src.telas.tela_login import TelaLogin
            self.close()
            self._login_tela = TelaLogin()
            self._login_tela.show()
        else:
            sys.exit(0)
