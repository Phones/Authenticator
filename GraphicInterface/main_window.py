import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
    QDialog,
)
from token_opt import TokenOPT
from confirmation_dialog import ConfirmationDialog
from PyQt5.QtCore import QTimer, QSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
            
    # Função para adicionar uma nova chave
    def add_key(self):
        name = self.name_entry.text().strip()
        key = self.key_entry.text().strip()
        if name and key:
            self.keys.append((name, key))
            otp = TokenOPT.generate_otp(key)
            self.list_widget.addItem(f"{name}: {otp}")
            self.name_entry.clear()
            self.key_entry.clear()
            self.save_keys_to_file()  # Salva as chaves no arquivo
        else:
            QMessageBox.warning(self, "Aviso", "Digite um nome e uma chave válida.")

    # Função para confirmar a exclusão da chave selecionada
    def confirm_delete_key(self):
        if selected_index is not None:
            dialog = ConfirmationDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                self.delete_key()

    # Função para deletar a chave selecionada
    def delete_key(self):
        if selected_index is not None:
            del self.keys[selected_index]
            self.list_widget.takeItem(selected_index)
            self.save_keys_to_file()  # Salva as chaves no arquivo

    # Função para alternar entre os temas
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    # Função para copiar o código OTP do item selecionado
    def copy_otp(self, item):
        otp = item.text().split(":")[-1].strip()
        clipboard = QApplication.clipboard()
        clipboard.setText(otp)
        QMessageBox.information(
            self, "Sucesso", "O código MFA foi copiado para a área de transferência."
        )

    # Função para salvar as chaves no arquivo
    def save_keys_to_file(self):
        with open("Keys/.keys.txt", "w") as file:
            for name, key in self.keys:
                file.write(f"{name},{key}\n")

    # Função para carregar as chaves do arquivo
    def load_keys_from_file(self):
        if os.path.exists("Keys/.keys.txt"):
            with open("Keys/.keys.txt", "r") as file:
                for line in file:
                    name, key = line.strip().split(",")
                    self.keys.append((name, key))

    # Função para atualizar o índice selecionado
    def update_selected_index(self):
        global selected_index
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_index = self.list_widget.row(selected_items[0])
        else:
            selected_index = None

    # Função para atualizar os códigos OTP
    def update_otp_codes(self):
        remaining_time = TokenOPT.calculate_remaining_time()
        self.timer_label.setText(f"Próxima atualização em: {remaining_time} segundos")
        if remaining_time == 0:
            for i in range(self.list_widget.count()):
                name, key = self.keys[i]
                otp = TokenOPT.generate_otp(key)
                item = self.list_widget.item(i)
                item.setText(f"{name}: {otp}")

    def load_settings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)

        theme = settings.value("theme", "light")
        if theme == "dark":
            self.dark_mode = True
        else:
            self.dark_mode = False

        self.update_theme()

    # Função para salvar as configurações
    def save_settings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)

        if self.dark_mode:
            settings.setValue("theme", "dark")
        else:
            settings.setValue("theme", "light")

    # Função para lidar com o evento de fechamento do programa
    def closeEvent(self, event):
        self.save_settings()  # Salva as configurações antes de fechar o programa
        event.accept()
