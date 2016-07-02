# -*- coding: utf-8 -*-
import gtk
import os
import sys
import zbar
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

from Urna.urnadao import eleicoesDB
import Urna.gerenciar.generateKey

PUBLIC_KEY = "../../files/publickey.pem"
PRIVATE_KEY = "../../files/privatekey.pem"
class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui

class Ui_MainWindow(object):
	def __init__(self, thread):
		self.thread = thread

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setWindowIcon(QIcon('../../files/icon.png'))

		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		MainWindow.showFullScreen()

		self.centralwidget = mainWidget(self, MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)

		self.btnGerarChaves = QPushButton(self.centralwidget)
		self.btnGerarChaves.setGeometry(QRect(self.screenWidth/2 - 300, self.screenHeight - 150, 200, 50))
		self.btnGerarChaves.setObjectName("btnGerarChaves")
        #chamar funcao ao clicar no botao 1
		self.btnGerarChaves.clicked.connect(self.btnGerarChavesClicked)
		#self.btnCriarTabelas.setStyle('cleanlooks')
		self.btnGerarChaves.setStyleSheet('QPushButton{\
                    border: 2px solid #ee7543;\
                    border-radius: 6px;\
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                    min-width: 80px;}')

		self.btnCriarTabelas = QPushButton(self.centralwidget)
		self.btnCriarTabelas.setGeometry(QRect(self.screenWidth/2 + 150, self.screenHeight - 150, 200, 50))
		self.btnCriarTabelas.setObjectName("btnCriarTabelas")
		self.btnCriarTabelas.clicked.connect(self.btnCriarTabelasClicked)
		self.btnCriarTabelas.setStyleSheet('QPushButton{\
					border: 2px solid #ee7543;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		if (os.path.isfile(PUBLIC_KEY) and os.path.isfile(PRIVATE_KEY)):
			#print('se do dois arquivos existem, o botao deve ser inativado')
			self.btnGerarChaves.setEnabled(False)

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
		self.btnCriarTabelas.setText(QApplication.translate("MainWindow", "CRIAR TABELAS", None, QApplication.UnicodeUTF8))
		self.btnGerarChaves.setText(QApplication.translate("MainWindow", "GERAR CHAVES", None, QApplication.UnicodeUTF8))


	def btnCriarTabelasClicked(self):
		database.criarTabelas()

	def btnGerarChavesClicked(self):
		Urna.gerenciar.generateKey.generate_RSA()
		sys.exit()


class MyThread(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.exiting = False
		self.index = 0

	def run(self):
		while self.exiting==False:
			self.index += 1
			sleep(1)
			if self.index == 6:
				self.exiting = True

class ControlMainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.thread = MyThread()
		self.thread.finished.connect(self.fechar)
		self.ui =  Ui_MainWindow(self.thread)
		self.ui.setupUi(self)

	def fechar(self):
		self.ui.lblMensagem.setVisible(False)
		self.thread.exiting=False
		self.thread.index=0

def main():
	app = QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	mySW.raise_()
	sys.exit(app.exec_())

if __name__ == "__main__":
	database = eleicoesDB.DAO()
	main()