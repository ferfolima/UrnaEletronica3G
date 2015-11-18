# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'locais.ui'
#
# Created: Sun Nov 30 22:21:43 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class Ui_Locais(object):
    def setupUi(self, Locais):
        Locais.setObjectName("Locais")
        Locais.resize(680, 440)
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
        Locais.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        Locais.setFont(font)
        self.label = QtGui.QLabel(Locais)
        self.label.setGeometry(QtCore.QRect(210, 40, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setUnderline(True)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Locais)
        self.label_2.setGeometry(QtCore.QRect(140, 160, 111, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Locais)
        self.label_3.setGeometry(QtCore.QRect(140, 210, 141, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Locais)
        self.label_4.setGeometry(QtCore.QRect(140, 260, 131, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtGui.QLineEdit(Locais)
        self.lineEdit.setGeometry(QtCore.QRect(260, 160, 71, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtGui.QLineEdit(Locais)
        self.lineEdit_2.setGeometry(QtCore.QRect(260, 210, 261, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtGui.QLineEdit(Locais)
        self.lineEdit_3.setGeometry(QtCore.QRect(260, 260, 31, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtGui.QPushButton(Locais)
        self.pushButton.setGeometry(QtCore.QRect(500, 330, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Locais)
        QtCore.QMetaObject.connectSlotsByName(Locais)

    def retranslateUi(self, Locais):
        Locais.setWindowTitle(QtGui.QApplication.translate("Locais", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Locais", "Cadastro de Locais", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Locais", "Código do Município*:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Locais", "Nome do Município*:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Locais", "Sigla do Estado*:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Locais", "Salvar", None, QtGui.QApplication.UnicodeUTF8))

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_Locais()
        self.ui.setupUi(self)
		
def main():
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
    mySW.raise_()

if __name__ == "__main__":
    main()