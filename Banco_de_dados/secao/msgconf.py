# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msgconf.ui'
#
# Created: Tue Dec 02 17:16:41 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
import cadastrosecao, msgerro, msgfinal
import h5py

arquivo = h5py.File("Banco_de_dados/Urna.h5","r+")
secoes = arquivo["PreEleicao/Secao"]

class Ui_msg1(object):
    def setupUi(self, msg1):
        msg1.setObjectName("msg1")
        msg1.resize(680, 440)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        msg1.setPalette(palette)
        msg1.setAutoFillBackground(False)
        self.label = QtGui.QLabel(msg1)
        self.label.setGeometry(QtCore.QRect(230, 110, 251, 61))
        self.label.setObjectName("label")
        self.pushButton = QtGui.QPushButton(msg1)
        self.pushButton.setGeometry(QtCore.QRect(120, 260, 151, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(msg1)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 260, 151, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(msg1)
        QtCore.QMetaObject.connectSlotsByName(msg1)
        
        #self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton_2.clicked.connect(self.buttonClicked2)

    def retranslateUi(self, msg1):
        msg1.setWindowTitle(QtGui.QApplication.translate("msg1", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("msg1", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#ffff7f;\">Deseja gravar a seção?</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("msg1", "Sim", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("msg1", "Não", None, QtGui.QApplication.UnicodeUTF8))
    
    def buttonClicked2(self): 
        self.msgconf = ControlMainWindow()
        self.msgconf.destroy(destroyWindow=True)
    
    #def buttonClicked(self):
    #    for i in range(len(secoes)):
    #        for j in range(len(secoes[i])):
    #            if secoes[1][j] == cadastrosecao.Ui_MainWindow.setupUi(spinBox_2, None):
    #                erroWindow = msgerro.ControlMainWindow()
    #                erroWindow.show()       
        #finalWindow = msgfinal.ControlMainWindow()
        #finalWindow.show()
        

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_msg1()
        self.ui.setupUi(self)
        
def main():
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
    mySW.raise_()

if __name__ == "__main__":
    main()