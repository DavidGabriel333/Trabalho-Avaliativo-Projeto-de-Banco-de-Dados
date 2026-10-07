from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from src.dao.login_dao import login


class TelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Loja de Suplementos")
        self.resize(380, 260)

        titulo = QLabel("LOGIN DO SISTEMA")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        self.campo_email = QLineEdit()
        self.campo_email.setPlaceholderText("seu@email.com")

        self.campo_senha = QLineEdit()
        self.campo_senha.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("Email:", self.campo_email)
        form.addRow("Senha:", self.campo_senha)

        btn_entrar = QPushButton("Entrar")
        btn_entrar.clicked.connect(self.fazer_login)
        self.campo_senha.returnPressed.connect(self.fazer_login)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addLayout(form)
        layout.addWidget(btn_entrar)
        layout.addStretch()
        self.setLayout(layout)

    def fazer_login(self):
        email = self.campo_email.text().strip()
        senha = self.campo_senha.text()

        try:
            resultado = login(email, senha)
        except Exception as e:
            QMessageBox.critical(self, "Erro de conexão", str(e))
            return

        if resultado == 0:
            QMessageBox.warning(self, "Login", "Login inválido!")
            return

        self.close()

        if resultado == -1:
            from src.telas.menu_gerente import MenuGerente
            self._proxima = MenuGerente()
        else:
            from src.telas.menu_cliente import MenuCliente
            self._proxima = MenuCliente(resultado)

        self._proxima.show()
