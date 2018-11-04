# -*- coding:utf-8 -*-

from BlurModel import myBlur
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, qApp, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.srcImg = None
        self.dstImg = None
        self.Model_No = 0
        self.initUI()

    def CreateMenu(self):
        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit SmartFitter')
        self.exitAction.triggered.connect(qApp.quit)

        self.openAction = QAction('&Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open File')
        self.openAction.triggered.connect(self.OpenImage)

        self.section_1 = QAction('&Comic Fitter', self, checkable=True)
        self.section_1.setStatusTip("fuck1")
        self.section_1.setChecked(True)
        self.section_1.triggered.connect(self.AdpModel_1)

        self.section_2 = QAction('&Simple Stroke Fitter', self, checkable=True)
        self.section_2.setStatusTip("fuck2")
        self.section_2.setChecked(False)
        self.section_2.triggered.connect(self.AdpModel_2)

        self.section_3 = QAction('&Portrait Fitter', self, checkable=True)
        self.section_3.setStatusTip("fuck3")
        self.section_3.setChecked(False)
        self.section_3.triggered.connect(self.AdpModel_3)
        self.statusbar = self.statusBar()

        """self.Trans = QAction('Transform', self)
        self.Trans.setShortcut('Ctrl+B')
        self.Trans.setStatusTip('Trans')
        self.Trans.triggered.connect(self.Run)"""
        button = QPushButton("Transform", self)
        button.setToolTip("Pic Transform")
        """按钮坐标x = 100, y = 70"""
        button.move(780, 350)
        """按钮与鼠标点击事件相关联"""
        button.clicked.connect(self.Run)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        sectionMenu = menubar.addMenu('&Fitter')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)
        sectionMenu.addAction(self.section_1)
        sectionMenu.addAction(self.section_2)
        sectionMenu.addAction(self.section_3)

    def AdpModel_1(self):
        self.section_1.setChecked(True)
        self.section_2.setChecked(False)
        self.section_3.setChecked(False)
        self.Model_No = 0

    def AdpModel_2(self):
        self.section_1.setChecked(False)
        self.section_2.setChecked(True)
        self.section_3.setChecked(False)
        self.Model_No = 1

    def AdpModel_3(self):
        self.section_1.setChecked(False)
        self.section_2.setChecked(False)
        self.section_3.setChecked(True)
        self.Model_No = 2

    def OpenImage(self):
        self.srcImg = QFileDialog.getOpenFileName(self, "Open File", "", "*.jpg;;*.png;;All Files(*)")[0]
        self.Label_ori.setScaledContents(True)
        self.Label_ori.setFrameShadow(QFrame.Raised)
        self.Label_ori.setPixmap(QPixmap(self.srcImg))

    def Run(self):
        if self.Model_No == 0:
            self.dstImg = myBlur(self.srcImg, 0)
            self.dstImg.applyModel()
            self.Label_new.setScaledContents(True)
            self.Label_new.setFrameShadow(QFrame.Raised)
            self.Label_new.setPixmap(QPixmap("dstImg.jpg"))
        elif self.Model_No == 1:
            pass
        elif self.Model_No == 2:
            pass


    def initUI(self):
        self.CreateMenu()

        self.Label_ori = QLabel(self)
        self.Label_new = QLabel(self)

        self.Label_ori.setFixedSize(700, 600)
        self.Label_ori.move(50, 50)
        self.Label_ori.setText("            显示原图片")
        self.Label_ori.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:40px;font-weight:bold;font-family:宋体;}"
                                 )

        self.Label_new.setFixedSize(700, 600)
        self.Label_new.move(900, 50)
        self.Label_new.setText("          显示处理后图片")
        self.Label_new.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:40px;font-weight:bold;font-family:宋体;}"
                                 )

        self.statusBar().showMessage('Ready')
        self.setGeometry(200, 200, 1650, 750)
        self.setWindowTitle('SmartFitter')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()


if __name__ == "__main__" :
    app = QApplication(sys.argv)

    mainWin = MainWnd()

    sys.exit(app.exec_())