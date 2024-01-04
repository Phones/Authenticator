from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QListWidgetItem,
)
from token_opt import TokenOPT
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_index = None

        self.setWindowTitle("Autenticação de Dois Fatores")
        self.setStyleSheet(
            """
            QMessageBox {
                background-color: #f0f0f0;
            }
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #2980b9;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #40739e;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            """
        )



        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        font = QFont("Arial", 16, QFont.Bold)
        self.title_label = QLabel("Autenticação de Dois Fatores", self)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)

        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.input_layout = QHBoxLayout()

        font = QFont("Arial", 10)
        self.name_label = QLabel("Nome:", self)
        self.name_label.setFont(font)
        self.input_layout.addWidget(self.name_label)

        self.name_entry = QLineEdit(self)
        self.name_entry.setFont(font)
        self.input_layout.addWidget(self.name_entry)

        self.key_label = QLabel("Chave:", self)
        self.key_label.setFont(font)
        self.input_layout.addWidget(self.key_label)

        self.key_entry = QLineEdit(self)
        self.key_entry.setFont(font)
        self.input_layout.addWidget(self.key_entry)

        self.layout.addLayout(self.input_layout)

        self.button_layout = QHBoxLayout()
        
        font = QFont("Arial", 12)
        self.add_button = QPushButton("Adicionar Chave", self)
        self.add_button.setFont(font)
        self.add_button.setStyleSheet("padding: 8px 16px;")
        self.add_button.clicked.connect(self.add_key)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Deletar Chave", self)
        self.delete_button.setFont(font)
        self.delete_button.setStyleSheet("background-color: #c0392b; color: #ffffff; border: none; border-radius: 4px; padding: 8px 16px;")
        self.delete_button.clicked.connect(self.confirm_delete_key)
        self.button_layout.addWidget(self.delete_button)

        self.mode_button = QPushButton("Modo Escuro", self)
        self.mode_button.setFont(font)
        self.mode_button.setStyleSheet("padding: 8px 16px;")
        self.mode_button.clicked.connect(self.toggle_theme)
        self.button_layout.addWidget(self.mode_button)

        self.layout.addLayout(self.button_layout)

        font = QFont("Arial", 10)
        self.timer_label = QLabel("Próxima atualização em: -", self)
        self.timer_label.setFont(font)
        self.layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_otp_codes)
        self.timer.start(1000)

        # Variáveis para controle do tema
        self.dark_mode = False
        self.toggle_theme()

        self.load_settings()

        # Carrega as chaves do arquivo
        self.keys = []
        self.load_keys_from_file()

        # Popula a lista com as chaves salvas e seus códigos OTP atualizados
        for name, key in self.keys:
            otp = TokenOPT.generate_otp(key)
            item = QListWidgetItem(f"{name}: {otp}")
            font = QFont("Arial", 12, QFont.Bold)
            item.setFont(font)
            self.list_widget.addItem(item)

        # Conecta o sinal itemDoubleClicked ao slot de cópia do OTP
        self.list_widget.itemDoubleClicked.connect(self.copy_otp)

        # Conecta o sinal itemSelectionChanged ao slot de atualização do índice selecionado
        self.list_widget.itemSelectionChanged.connect(self.update_selected_index)


