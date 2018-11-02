# -*- coding:utf-8 -*-

from BlurModel import myBlur
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIcon
import sys

class MainWnd(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowTitle('SmartFitter')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()

if __name__ == "__main__" :
    app = QApplication(sys.argv)

    mainWin = MainWnd()

    sys.exit(app.exec_())