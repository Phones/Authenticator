import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from authenticator import Authenticator

def exec_app():
    app = QApplication(sys.argv)
    app.setFont(QFont("Comic Sans MS"))
    window = Authenticator()
    window.show()
    sys.exit(app.exec_())


# Execução da aplicação
if __name__ == "__main__":
    exec_app()
