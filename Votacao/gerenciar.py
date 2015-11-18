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
import incrementar
import zbar
import gtk
import generateKey

h5pyFile = h5py.File('Urna.h5', 'r')
candidatos = h5pyFile['Urna/Candidatos']
perguntas = h5pyFile['Urna/Perguntas']
setupGeral = h5pyFile['Urna/SetupGeral']
tipoDeCandidato = h5pyFile['Urna/TipoDeCandidato']
tipoEleicao = setupGeral[0][8]

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui

	def keyPressEvent(self, event):
		if event.text() == '.':
			self.ui.button2Clicked()
		elif event.text() == '\n':
			print('deu certo')

class Ui_MainWindow(object):
	def __init__(self, thread):
		self.thread = thread

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		self.apurarWindow = incrementar.incrementar()

		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		MainWindow.showFullScreen()

		self.centralwidget = mainWidget(self, MainWindow)

		self.centralwidget.setObjectName("centralwidget")

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)

		self.table1 = QTableWidget(self.centralwidget)
		self.table1.setGeometry(QRect(50, 50, self.screenWidth - 100, 500))
		self.table1.setObjectName('label')
		self.table1.setRowCount(1000000)
		self.table1.setColumnCount(3)
		self.table1.setColumnWidth(0,(self.screenWidth - 185)/3)
		self.table1.setColumnWidth(1,(self.screenWidth - 185)/3)
		self.table1.setColumnWidth(2,(self.screenWidth - 185)/3)
		self.table1.setEnabled(False);
		horHeader = []
		horHeader.append('Cargo')
		horHeader.append('Voto')
		horHeader.append('# Votos')
		self.table1.setHorizontalHeaderLabels(horHeader)

		self.pushButton1 = QPushButton(self.centralwidget)
		self.pushButton1.setGeometry(QRect(self.screenWidth/2 + 200, self.screenHeight - 100, 200, 50))
		self.pushButton1.setObjectName("pushButton1")
		#chamar funcao ao clicar no botao 1
		self.pushButton1.clicked.connect(self.buttonClicked)
		self.pushButton1.setStyleSheet('QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		self.pushButton2 = QPushButton(self.centralwidget)
		self.pushButton2.setGeometry(QRect(self.screenWidth/2 - 125, self.screenHeight - 100, 200, 50))
		self.pushButton2.setObjectName("pushButton2")
		#chamar funcao ao clicar no botao 1
		self.pushButton2.clicked.connect(self.button2Clicked)
		#self.pushButton2.setStyle('cleanlooks')
		self.pushButton2.setStyleSheet('QPushButton{\
					border: 2px solid #ee7543;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		self.pushButton3 = QPushButton(self.centralwidget)
		self.pushButton3.setGeometry(QRect(self.screenWidth/2 - 450, self.screenHeight - 100, 200, 50))
		self.pushButton3.setObjectName("pushButton3")
        #chamar funcao ao clicar no botao 1
		self.pushButton3.clicked.connect(self.button3Clicked)
		#self.pushButton2.setStyle('cleanlooks')
		self.pushButton3.setStyleSheet('QPushButton{\
                    border: 2px solid #ee7543;\
                    border-radius: 6px;\
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                    min-width: 80px;}')
		if (os.path.isfile('./privatekey.pem') and os.path.isfile('./publickey.pem')):
			#print('se do dois arquivos existem, o botao deve ser inativado')
			self.pushButton3.setEnabled(False)

		self.label = QLineEdit(self.centralwidget)
		self.label.setGeometry(QRect(50, 50, self.screenWidth - 100, self.screenHeight - 100))
		self.label.setFont(font)
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setObjectName("label")
		self.label.setEnabled(False)
		self.label.setVisible(False)

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
		self.pushButton1.setText(QApplication.translate("MainWindow", "GERAR BOLETIM", None, QApplication.UnicodeUTF8))
		self.pushButton2.setText(QApplication.translate("MainWindow", "LER CODIGO", None, QApplication.UnicodeUTF8))
		self.pushButton3.setText(QApplication.translate("MainWindow", "GERAR CHAVES", None, QApplication.UnicodeUTF8))

	#funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
	def buttonClicked(self):
		self.apurarWindow.gerarBoletim()
		sys.exit()

	def button2Clicked(self):
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
					self.apurarWindow.incrementar(generateKey.decrypt(symbol.data, open('./privatekey.pem','rb')))
				except ValueError:
					self.label.setVisible(True)
					self.label.setText(U'Voto inválido. Não pertence a esta seção.')
					self.thread.start()


		proc.set_data_handler(my_handler)

		# enable the preview window
		proc.visible = True

		# initiate scanning
		proc.active = True
		try:
			# keep scanning until user provides key/mouse input
			proc.process_one()
		except zbar.WindowClosed as e:
			pass

		votos = self.apurarWindow.getVotos()
		i = 0
		for key in votos:
			for k in votos[key]:
				self.table1.setItem(i,0,QTableWidgetItem(key))
				if k == "-1":
					self.table1.setItem(i,1,QTableWidgetItem('Nulo'))
				elif k == "0":
					self.table1.setItem(i,1,QTableWidgetItem('Branco'))
				else:
					self.table1.setItem(i,1,QTableWidgetItem(k))
				self.table1.setItem(i,2,QTableWidgetItem(str(votos[key][k])))
				i = i + 1
		# self.table1.resizeColumnsToContents()
		# self.table1.resizeRowsToContents()

	def button3Clicked(self):
		generateKey.generate_RSA()
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
		self.ui.label.setVisible(False)
		self.thread.exiting=False
		self.thread.index=0

def main():
	app = QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	mySW.raise_()
	sys.exit(app.exec_())

def decodificarString(string):
	informacoes1 = string.split("|")[0]
	informacoes2 = informacoes1.split(",")
	informacoes = []
	for informacao in informacoes2: informacoes.append(informacao.split("."))

	votos1 = string.split("|")[1]
	votos2 = votos1.split(";")
	votos3 = []
	for cargo in votos2: votos3.append(cargo.split(":"))
	votos4 = []
	for voto in votos3: votos4.append([voto[0], voto[1].split(",")])
	votos = []
	for voto in votos4:
		test = []
		for voto2 in voto[1]:
			test.append(voto2.split("."))
		votos.append((voto[0], test))
	return votos
if __name__ == "__main__":
	main()
