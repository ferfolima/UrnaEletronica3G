# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menuentrada.ui'
#
# Created: Sun Nov 30 22:22:03 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
from Partidos.partidos1 import ControlMainWindow as windowmain
from Main_Window.mainwindow import ControlMainWindow as windowmain2
from Candidatos.locais import ControlMainWindow as windowmain3
from secao.cadastrosecao import ControlMainWindow as windowmain4

class Ui_MenuEntrada(object):
    def setupUi(self, MenuEntrada):
        MenuEntrada.setObjectName("MenuEntrada")
        MenuEntrada.resize(680, 440)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MenuEntrada.setPalette(palette)
        self.label = QtGui.QLabel(MenuEntrada)
        self.label.setGeometry(QtCore.QRect(140, 80, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setUnderline(True)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtGui.QPushButton(MenuEntrada)
        self.pushButton.setGeometry(QtCore.QRect(210, 160, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(MenuEntrada)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 200, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtGui.QPushButton(MenuEntrada)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 240, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtGui.QPushButton(MenuEntrada)
        self.pushButton_4.setGeometry(QtCore.QRect(210, 280, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton_2.clicked.connect(self.buttonClicked2)
        self.pushButton_3.clicked.connect(self.buttonClicked3)
        self.pushButton_4.clicked.connect(self.buttonClicked4)
        

        self.retranslateUi(MenuEntrada)
        QtCore.QMetaObject.connectSlotsByName(MenuEntrada)

    def retranslateUi(self, MenuEntrada):
        MenuEntrada.setWindowTitle(QtGui.QApplication.translate("MenuEntrada", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MenuEntrada", "Preparação de Urna Eletrônica 3.0", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MenuEntrada", "Cadastramento de Locais", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MenuEntrada", "Cadastramento de Partidos", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MenuEntrada", "Cadastramento de Seções", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MenuEntrada", "Setup de Urna", None, QtGui.QApplication.UnicodeUTF8))

    def buttonClicked2(self): 
        self.partidos1Window = windowmain()
        self.partidos1Window.show()
    def buttonClicked(self): 
        self.locaisWindow = windowmain3()
        self.locaisWindow.show()
    def buttonClicked3(self): 
        self.secaoWindow = windowmain4()
        self.secaoWindow.show()
    def buttonClicked4(self): 
        self.setupWindow = windowmain2()
        self.setupWindow.show()

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_MenuEntrada()
        self.ui.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
    mySW.raise_()

if __name__ == "__main__":
    main()