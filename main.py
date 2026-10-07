import sys

from PySide6.QtWidgets import QApplication

from src.estilos import ESTILO_APP
from src.telas.tela_login import TelaLogin


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(ESTILO_APP)

    janela = TelaLogin()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
