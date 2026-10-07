"""
Folha de estilo (QSS) aplicada em todo o app, para um visual mais
moderno do que o Swing padrão da versão em Java.
"""

ESTILO_APP = """
QWidget {
    background-color: #1e1e2f;
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

QLabel#titulo {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    padding: 8px 0px;
}

QPushButton {
    background-color: #4f6df5;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #3d57d6;
}

QPushButton:pressed {
    background-color: #2d42ad;
}

QPushButton#botaoPerigo {
    background-color: #e5484d;
}

QPushButton#botaoPerigo:hover {
    background-color: #c53d41;
}

QLineEdit, QComboBox {
    background-color: #2a2a3d;
    border: 1px solid #44445c;
    border-radius: 6px;
    padding: 6px;
    color: #f0f0f0;
}

QTableWidget {
    background-color: #25253a;
    gridline-color: #3a3a52;
    border-radius: 6px;
    selection-background-color: #4f6df5;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #2a2a3d;
    color: #ffffff;
    padding: 6px;
    border: none;
    font-weight: bold;
}

QMessageBox {
    background-color: #25253a;
}
"""
