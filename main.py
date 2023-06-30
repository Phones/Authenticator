import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from GraphicInterface.main_window import MainWindow
from GraphicInterface.confirmation_dialog import ConfirmationDialog

# Execução da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Comic Sans MS"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
