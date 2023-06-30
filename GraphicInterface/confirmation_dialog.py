from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
)

class ConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Confirmação")
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)

        message_label = QLabel("Tem certeza de que deseja deletar a chave selecionada?")
        layout.addWidget(message_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)