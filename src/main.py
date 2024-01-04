import sys
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication
from authenticator import Authenticator

def exec_app():
    app = QApplication(sys.argv)
    app.setFont(QFont("Comic Sans MS"))
    app.setWindowIcon(QIcon('icons/cadeado64.ico')) 
    window = Authenticator()
    window.setWindowIcon(QIcon('icons/cadeado64.ico')) 
    window.show()
    sys.exit(app.exec_())


# Execução da aplicação
if __name__ == "__main__":
    exec_app()
