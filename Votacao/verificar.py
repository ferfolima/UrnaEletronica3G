 #-*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue Nov 18 15:42:23 2014
#	  by: Fernando Teodoro de Lima
#
# WARNING! All changes made in this file will be lost!

from PySide.QtGui import *
from PySide.QtCore import *
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from time import sleep
import h5py
import sys
import random
import os
import pyqrcode
import votar
import zbar
import gtk
from time import gmtime, strftime
from PIL import Image
import subprocess
import generateKey
import ast

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui

class Ui_MainWindow(object):
	def __init__(self, thread):
		self.thread = thread

	def setupUi(self, MainWindow):
		self.MainWindow = MainWindow
		MainWindow.setObjectName("MainWindow")

		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		MainWindow.showFullScreen()

		self.centralwidget = mainWidget(self, MainWindow)

		self.centralwidget.setObjectName("centralwidget")

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)

		self.label_0 = QLabel(self.centralwidget)
		self.label_0.setGeometry(QRect(50, 50, self.screenWidth - 100, 50))
		#self.label_0.setStyleSheet("border: 2px solid");
		self.label_0.setAlignment(Qt.AlignCenter)
		self.label_0.setText("Seu voto")
		self.label_0.setObjectName("label_0")
		self.label_0.setFont(font)

		font.setPointSize(12)
		self.label_1 = QLabel(self.centralwidget)
		self.label_1.setGeometry(QRect(50, self.label_0.pos().y() + self.label_0.height() + 50, self.screenWidth - 100, self.screenHeight - 150 - self.label_0.height()))
		#self.label_1.setStyleSheet("border: 2px solid");
		self.label_1.setAlignment(Qt.AlignHCenter)
		self.label_1.setText("")
		self.label_1.setObjectName("label_1")


		self.pushButton1 = QPushButton(self.centralwidget)
		self.pushButton1.setGeometry(QRect(self.screenWidth/2 - 100, self.screenHeight - 100, 200, 50))
		self.pushButton1.setObjectName("pushButton1")
		#chamar funcao ao clicar no botao 1
		self.pushButton1.clicked.connect(self.buttonClicked)
		self.pushButton1.setStyleSheet('QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		font.setPointSize(35)

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
		self.pushButton1.setText(QApplication.translate("MainWindow", "VERIFICAR", None, QApplication.UnicodeUTF8))

	def buttonClicked(self):
		# create a Processor
		proc = zbar.Processor()

		# configure the Processor
		proc.parse_config('enable')

		# initialize the Processor
		device = '/dev/video0'
		proc.init(device)

		# setup a callback
		def my_handler(proc, image, closure):
			# extract results
			for symbol in image.symbols:
			# do something useful with results
				try:
					self.label_1.setText(decodificarString(symbol.data))
					self.thread.start()
				except ValueError:
					self.label_1.setText(U'Voto inválido. Não pertence a esta seção.')
					self.thread.start()

		proc.set_data_handler(my_handler)

		# enable the preview window
		proc.visible = True

		# initiate scanning
		proc.active = True
		try:
			# keep scanning until user provides key/mouse input
			proc.process_one()
		except zbar.WindowClosed, e:
			pass
#thread
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
		#thread criada para aguardar 5 segundos antes de
		#	reiniciar o programa após um eleitor votar
		self.thread = MyThread()
		self.thread.finished.connect(self.fechar)
		self.ui = Ui_MainWindow(self.thread)
		self.ui.setupUi(self)

	def fechar(self):
		self.ui.label_1.setText("")
		self.thread.exiting=False
		self.thread.index=0

def main():
	app = QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	mySW.raise_()
	sys.exit(app.exec_())

def decodificarString(encrypted):
	string = generateKey.decrypt(encrypted, open('./privatekey.pem','rb'))
	#pres, gov, sen1, sen2, depf, depe, pref, ver
	info = string[1:].split(';')
	string = ''
	if info[0] is not '':
		string += 'Presidente: '
		if info[0] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[0] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[0] + '\n\n'
	if info[1] is not '':
		string += 'Governador: '
		if info[1] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[1] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[1] + '\n\n'
	if info[2] is not '':
		string += 'Senador 1: '
		if info[2] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[2] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[2] + '\n\n'
	if info[3] is not '':
		string += 'Senador 2: '
		if info[3] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[3] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[3] + '\n\n'
	if info[4] is not '':
		string += 'Deputado Federal: '
		if info[4] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[4] == '-1':
			string +='Voto nulo' + '\n\n'
		elif len(info[4]) == 2:
			string += 'Legenda' + info[4] + '\n\n'
		else:
			string += 'Numero: ' + info[4] + '\n\n'
	if info[5] is not '':
		string += 'Deputado Estadual: '
		if info[5] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[5] == '-1':
			string +='Voto nulo' + '\n\n'
		elif len(info[5]) == 2:
			string += 'Legenda' + info[5] + '\n\n'
		else:
			string += 'Numero: ' + info[5] + '\n\n'
	if info[6] is not '':
		string += 'Prefeito: '
		if info[6] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[6] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[6] + '\n\n'
	if info[7] is not '':
		string += 'Vereador: '
		if info[7] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[7] == '-1':
			string +='Voto nulo' + '\n\n'
		elif len(info[7]) == 2:
			string += 'Legenda' + info[7] + '\n\n'
		else:
			string += 'Numero: ' + info[7] + '\n\n'
	return string
if __name__ == "__main__":
	main()
