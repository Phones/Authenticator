from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QHBoxLayout,
)
from token_opt import TokenOPT
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_index = None

        self.setWindowTitle("Autenticação de Dois Fatores")
        self.setStyleSheet(
            """
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

        self.title_label = QLabel("Autenticação de Dois Fatores", self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.input_layout = QHBoxLayout()

        self.name_label = QLabel("Nome:", self)
        self.name_label.setStyleSheet("font-size: 16px;")
        self.input_layout.addWidget(self.name_label)

        self.name_entry = QLineEdit(self)
        self.name_entry.setStyleSheet("font-size: 16px;")
        self.input_layout.addWidget(self.name_entry)

        self.key_label = QLabel("Chave:", self)
        self.key_label.setStyleSheet("font-size: 16px;")
        self.input_layout.addWidget(self.key_label)

        self.key_entry = QLineEdit(self)
        self.key_entry.setStyleSheet("font-size: 16px;")
        self.input_layout.addWidget(self.key_entry)

        self.layout.addLayout(self.input_layout)

        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("Adicionar Chave", self)
        self.add_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        self.add_button.clicked.connect(self.add_key)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Deletar Chave", self)
        self.delete_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        self.delete_button.clicked.connect(self.confirm_delete_key)
        self.button_layout.addWidget(self.delete_button)

        self.mode_button = QPushButton("Modo Escuro", self)
        self.mode_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        self.mode_button.clicked.connect(self.toggle_theme)
        self.button_layout.addWidget(self.mode_button)

        self.layout.addLayout(self.button_layout)

        self.timer_label = QLabel("Próxima atualização em: -", self)
        self.timer_label.setStyleSheet("font-size: 16px;")
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
            self.list_widget.addItem(f"{name}: {otp}")

        # Conecta o sinal itemDoubleClicked ao slot de cópia do OTP
        self.list_widget.itemDoubleClicked.connect(self.copy_otp)

        # Conecta o sinal itemSelectionChanged ao slot de atualização do índice selecionado
        self.list_widget.itemSelectionChanged.connect(self.update_selected_index)


    # Função para atualizar o tema
    def update_theme(self):
        if self.dark_mode:
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #222222;
                }
                QLabel {
                    color: #ffffff;
                }
                QLineEdit {
                    background-color: #333333;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 5px;
                    color: #ffffff;
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
                    background-color: #333333;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 5px;
                    color: #ffffff;
                }
                """
            )
            self.mode_button.setText("Modo Claro")
        else:
            self.setStyleSheet(
                """
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
            self.mode_button.setText("Modo Escuro")


