import os
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QDialog,
)
from token_opt import TokenOPT
from create_logging import get_logger
from graphic_interface.main_window import MainWindow
from graphic_interface.confirmation_dialog import ConfirmationDialog

class Authenticator(MainWindow):
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)

    def update_otp_codes(self):
        remaining_time = TokenOPT.calculate_remaining_time()
        self.timer_label.setText(f"Próxima atualização em: {remaining_time} segundos")
        for i in range(self.list_widget.count()):
            name, key = self.keys[i]
            otp = TokenOPT.generate_otp(key)
            item = self.list_widget.item(i)
            item.setText(f"{name}: {otp}")

    # Função para adicionar uma nova chave
    def add_key(self):
        name = self.name_entry.text().strip()
        key = self.key_entry.text().strip()
        if name and key:
            try:
                otp = TokenOPT.generate_otp(key)
                self.keys.append((name, key))
                self.list_widget.addItem(f"{name}: {otp}")
                self.name_entry.clear()
                self.key_entry.clear()
                self.save_keys_to_file()  # Salva as chaves no arquivo
            except Exception as error:
                self.logger.error(f":\n--------------------------\n{error}\n--------------------------\n")
                QMessageBox.warning(self, "Aviso", f"Error: {error}")
        else:
            QMessageBox.warning(self, "Aviso", "Digite um nome e uma chave válida.")

    # Função para confirmar a exclusão da chave selecionada
    def confirm_delete_key(self):
        if self.selected_index is not None:
            dialog = ConfirmationDialog(self, dialog_dark_mode=self.dark_mode)
            if dialog.exec_() == QDialog.Accepted:
                self.delete_key()

    # Função para deletar a chave selecionada
    def delete_key(self):
        if self.selected_index is not None:
            del self.keys[self.selected_index]
            self.list_widget.takeItem(self.selected_index)
            self.save_keys_to_file()  # Salva as chaves no arquivo

    # Função para atualizar o tema
    def update_theme(self):
        if self.dark_mode:
            self.setStyleSheet(
                """
                QMessageBox {
                    background-color: #222222;
                }
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
            self.mode_button.setText("Modo Escuro")

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
        with open("src/keys/.keys.txt", "w") as file:
            for name, key in self.keys:
                file.write(f"{name},{key}\n")

    # Função para carregar as chaves do arquivo
    def load_keys_from_file(self):
        if os.path.exists("src/keys/.keys.txt"):
            with open("src/keys/.keys.txt", "r") as file:
                for line in file:
                    name, key = line.strip().split(",")
                    self.keys.append((name, key))

    # Função para atualizar o índice selecionado
    def update_selected_index(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            self.selected_index = self.list_widget.row(selected_items[0])
        else:
            self.selected_index = None

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

