from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from app.ui.uilib.window import WindowContainer
from app.app import Application
import sys
import os

def main():
    if not os.path.exists("conf"):
        os.makedirs("conf")
    app = QApplication(sys.argv)
    app.setFont(QFont("JetBrains Mono"))
    wcon = WindowContainer(window=Application)
    wcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()