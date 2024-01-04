from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
)

class ConfirmationDialog(QDialog):
    def __init__(self, parent=None, dialog_dark_mode=True):
        super().__init__(parent)
        self.dialog_dark_mode = dialog_dark_mode
        self.update_dialog_theme()

        self.setWindowTitle("Confirmação")
        self.setWindowModality(Qt.ApplicationModal)

        self.layout = QVBoxLayout(self)

        message_label = QLabel("Tem certeza de que deseja deletar a chave selecionada?")
        self.layout.addWidget(message_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)

    def update_dialog_theme(self) -> None:
        if self.dialog_dark_mode:
            self.setStyleSheet("background-color: #222222;") 
        else:
            self.setStyleSheet("background-color: #f0f0f0;") 
        