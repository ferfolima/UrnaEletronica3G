# -*- coding: utf-8 -*-
import gtk
import os
import pyaudio
import random
import sys
import wave
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from time import sleep

import pyqrcode
from PySide.QtCore import *
from PySide.QtGui import *

import votar
from Urna.apuracao import generateKey
from Urna.urnadao import eleicoesDB

PUBLIC_KEY = "../../files/publickey.pem"

class ControlMainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)

		#thread criada para aguardar 5 segundos antes de reiniciar o programa apos um eleitor votar
		self.thread = MyThread()
		self.thread.finished.connect(self.fechar)

		self.ui =  Ui_MainWindow(self.thread)
		self.ui.setupUi(self)

	def fechar(self):
		sys.exit()

		# Reexecutar o programa ao sair?
		python = sys.executable
		os.execl(python, python, * sys.argv)

class Ui_MainWindow(object):
	def __init__(self, thread):
		self.thread = thread

	def eventFilter(self, object, event):
		if event.type() == QEvent.WindowActivate:
			if self.ui.votarWindow is not None:
				if database.getQtdeCargos() == self.ui.votarWindow.getQtdeCargosVotados():
					if self.ui.thread.isRunning():
						self.ui.thread.exiting = True
					else:
						self.ui.lblImprimir.setText("Imprimindo voto")
						self.ui.thread.start()
						gerarString(self, self.ui.votarWindow.getCargosVotados())

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.showFullScreen()
		MainWindow.setWindowIcon(QIcon('../../files/icon.png'))

		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		self.centralwidget = mainWidget(self, MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.centralwidget.installEventFilter(self.centralwidget)

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)

		self.lblTitulo = QLabel(self.centralwidget)
		self.lblTitulo.setGeometry(QRect(50, 50, self.screenWidth - 100, 50))
		self.lblTitulo.setObjectName("lblTitulo")
		self.lblTitulo.setText("Selecione um cargo para votar")
		self.lblTitulo.setFont(font)
		self.lblTitulo.setAlignment(Qt.AlignCenter)

		self.btnVotar = QPushButton(self.centralwidget)
		self.btnVotar.setGeometry(QRect(self.screenWidth/2 - 100, self.screenHeight - 100, 200, 50))
		self.btnVotar.setObjectName("btnVotar")
		self.btnVotar.clicked.connect(self.btnVotarClicked)
		self.btnVotar.setStyleSheet("QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}")

		self.lstCargos = QListWidget(self.centralwidget)
		self.lstCargos.setGeometry(QRect(100, self.lblTitulo.pos().y() + self.lblTitulo.height() + 50, self.screenWidth - 200, self.screenHeight - self.lblTitulo.height() - self.btnVotar.height() - 200))
		self.lstCargos.setObjectName("lstCargos")
		self.lstCargos.setFont(font)
		self.lstCargos.setWordWrap(True)

		#preencher lstCargos com cargos para eleicao
		for cargo in database.getCargos():
			item = QListWidgetItem(cargo[0])

			#item.setTextAlignment(Qt.AlignHCenter)
			self.lstCargos.addItem(item)
		self.lstCargos.setCurrentRow(0)

		#label que ira mostrar mensagem "imprimindo voto"
		#ele fica invisivel no inicio e so aparece quando a listview e esvaziada
		#ou seja, quando o eleitor ja votou para todos os cargos possiveis
		self.lblImprimir = QLineEdit(self.centralwidget)
		self.lblImprimir.setGeometry(QRect(50, 50, self.screenWidth - 100, self.screenHeight - 100))
		self.lblImprimir.setFont(font)
		self.lblImprimir.setAlignment(Qt.AlignCenter)
		self.lblImprimir.setObjectName("lblImprimir")
		self.lblImprimir.setVisible(False)

		# Variavel onde sera inicializada a classe de votacao
		self.votarWindow = None

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Urna Eletronica", None, QApplication.UnicodeUTF8))
		self.btnVotar.setText(QApplication.translate("MainWindow", "VOTAR", None, QApplication.UnicodeUTF8))
		self.lblImprimir.setText(QApplication.translate("MainWindow", "", None, QApplication.UnicodeUTF8))

	#funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
	def btnVotarClicked(self):
		if self.lstCargos.currentItem() is None:
			 print("Nenhum candidato selecionado")
		else:
			votarCargo = self.lstCargos.currentItem()
			self.votarWindow = votar.ControlMainWindow(votarCargo.text())
			self.lstCargos.takeItem(self.lstCargos.row(votarCargo))
			if self.lstCargos.count() == 0:
				self.lblImprimir.setText("Imprimindo Voto")
				self.lblImprimir.setEnabled(False)
				self.lblImprimir.setVisible(True)
				self.btnVotar.setVisible(False)

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui
		self.installEventFilter(self)

	def eventFilter(self, object, event):
		if event.type() == QEvent.WindowActivate:
			if self.ui.votarWindow is not None:
				if database.getQtdeCargos() == self.ui.votarWindow.getQtdeCargosVotados():
					if self.ui.thread.isRunning():
						self.ui.thread.exiting = True
					else:
						self.ui.lblImprimir.setText("Imprimindo voto")
						self.ui.thread.start()
						gerarString(self, self.ui.votarWindow.getCargosVotados())
		return False

		def keyPressEvent(self, event):
			if event.text() == "v":
				self.ui.btnVotarClicked()
			elif event.text() == "a":
				self.ui.btnVotarClicked()
			elif event.text() == "1":
				self.ui.lstCargos.setCurrentRow(0)
				self.ui.btnVotarClicked()
			elif event.text() == "2":
				self.ui.lstCargos.setCurrentRow(1)
				self.ui.btnVotarClicked()
			elif event.text() == "3":
				self.ui.lstCargos.setCurrentRow(2)
				self.ui.btnVotarClicked()
			elif event.text() == "4":
				self.ui.lstCargos.setCurrentRow(3)
				self.ui.btnVotarClicked()
			elif event.text() == "5":
				self.ui.lstCargos.setCurrentRow(4)
				self.ui.btnVotarClicked()
			elif event.text() == "6":
				self.ui.lstCargos.setCurrentRow(5)
				self.ui.btnVotarClicked()
			elif event.text() == "7":
				self.ui.lstCargos.setCurrentRow(6)
				self.ui.btnVotarClicked()
			elif event.text() == "8":
				self.ui.lstCargos.setCurrentRow(7)
				self.ui.btnVotarClicked()
			elif event.text() == "9":
				self.ui.lstCargos.setCurrentRow(8)
				self.ui.btnVotarClicked()

#thread
class MyThread(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.exiting = False
		self.index = 0

	def run(self):
		som(self,2)
		while self.exiting==False:
			self.index += 1
			sleep(1)
			if self.index == 6:
				self.exiting = True

def som(self, tipo):
	#define stream chunk
	chunk = 1024

	#open a wav format music
	if tipo == 1:
		f = wave.open(r"../../files/beep_urna.wav","rb")
	elif tipo == 2:
		f = wave.open(r"../../files/fim_urna.wav","rb")
	else:
		return
	#instantiate PyAudio
	p = pyaudio.PyAudio()
	#open stream
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
					channels = f.getnchannels(),
					rate = f.getframerate(),
					output = True)
	#read data
	data = f.readframes(chunk)

	#play stream
	while data != "":
		stream.write(data)
		data = f.readframes(chunk)

	#stop stream
	stream.stop_stream()
	stream.close()

	#close PyAudio
	p.terminate()

#funcao para gerar string para imprimir QRCode
def gerarString(self, votos):
	c = canvas.Canvas("../../files/voto.pdf")
	c.setPageSize((6.2*cm,10*cm))
	c.setFont("Helvetica",10)

	textobject = c.beginText()
	textobject.setTextOrigin(0.3*cm, 6.2*cm)
	textobject.moveCursor(0,-50)

	stringQRCode = "#"
	for cargo in database.getCargos():
		for voto in votos:
			string = ""
			if cargo == str(voto[0]):
				string += cargo + ": "
				if str(voto[1]) == "1":
					string += "Voto em branco"
					stringQRCode += "0"
				elif str(voto[2]) == "1":
					string += "Voto Nulo"
					stringQRCode += "-1"
				else:
					string += str(voto[4])
					stringQRCode += str(voto[4])
				textobject.textOut(string)
				textobject.moveCursor(0,14)
				votos.remove(voto)
		stringQRCode += ";"

	rng = random.SystemRandom()
	id_voto = rng.randint(0, 1000000000)
	stringQRCode += str(id_voto)

	encryptedMessage = generateKey.encrypt(stringQRCode, open(PUBLIC_KEY, "rb"))
	url = pyqrcode.create(encryptedMessage, error="L", encoding="utf-8")
	url.png("../../files/voto.png", scale=1)

	c.drawText(textobject)
	c.drawImage("../../files/voto.png", 0.05*cm, 0.05*cm, 6.1*cm, 6.1*cm)
	os.remove("../../files/voto.png")
	c.showPage()
	c.save()
	# subprocess.call(["lp","../files/voto.pdf"])
	# os.remove("../files/voto.pdf")

def main():
	if not os.path.isfile(PUBLIC_KEY):
		print("votacao nao pode ser iniciada")
		print("chave publica faltando")
		sys.exit()

	app = QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	mySW.raise_()
	sys.exit(app.exec_())

if __name__ == "__main__":
	database = eleicoesDB.DAO()
	main()
