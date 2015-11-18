# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'partidos6.ui'
#
# Created: Sun Nov 30 20:24:37 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class Ui_partidos8(object):
    def setupUi(self, partidos8):
        partidos8.setObjectName("partidos8")
        partidos8.resize(680, 400)
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
        partidos8.setPalette(palette)
        self.pushButton_2 = QtGui.QPushButton(partidos8)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 130, 231, 81))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(partidos8)
        QtCore.QMetaObject.connectSlotsByName(partidos8)
        self.pushButton_2.clicked.connect(self.buttonClicked2)
        
    def buttonClicked2(self): 
        self.partidos6Window = ControlMainWindow()
        self.partidos6Window.destroy(destroyWindow=True)
                                                 
    
    def retranslateUi(self, partidos8):
        partidos8.setWindowTitle(QtGui.QApplication.translate("partidos8", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("partidos8", "Operação Cancelada!", None, QtGui.QApplication.UnicodeUTF8))

    
    
class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_partidos8()
        self.ui.setupUi(self)
       
def main():
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
    mySW.raise_()

if __name__ == "__main__":
    main()