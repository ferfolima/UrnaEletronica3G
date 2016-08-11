#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os
import sys
import zbar
import pyaudio
import wave
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

import incrementar
from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

script_dir = os.path.dirname(__file__)
BEEP = os.path.join(script_dir, "../files/beep_urna.wav")
FIM = os.path.join(script_dir, "../files/fim_urna.wav")
PRIVATE_KEY = os.path.join(script_dir, "../files/privatekey.pem")
ICON = os.path.join(script_dir, "../files/icon.png")

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui

	def keyPressEvent(self, event):
		if event.text() == '.':
			self.ui.btnLerCodigoClicked()
		# elif event.text() == '\n':
		# 	print('deu certo')

class Ui_MainWindow(object):
	def __init__(self, thread):
		self.thread = thread

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setWindowIcon(QIcon(ICON))
		self.apurarWindow = incrementar.incrementar()

		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		MainWindow.show()
		MainWindow.showMaximized()

		self.centralwidget = mainWidget(self, MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)

		self.lblTitulo = QLabel(self.centralwidget)
		self.lblTitulo.setGeometry(QRect(50, 50, self.screenWidth - 100, 50))
		self.lblTitulo.setObjectName("lblTitulo")
		self.lblTitulo.setText(u"Apuração")
		self.lblTitulo.setFont(font)
		self.lblTitulo.setAlignment(Qt.AlignCenter)

		self.tblVotos = QTableWidget(self.centralwidget)
		self.tblVotos.setGeometry(QRect(50, self.lblTitulo.pos().y() + 100, self.screenWidth - 100, 500))
		self.tblVotos.setObjectName('tblVotos')
		self.tblVotos.setRowCount(1000000)
		self.tblVotos.setColumnCount(3)
		self.tblVotos.setColumnWidth(0,(self.screenWidth - 185)/3)
		self.tblVotos.setColumnWidth(1,(self.screenWidth - 185)/3)
		self.tblVotos.setColumnWidth(2,(self.screenWidth - 185)/3)
		self.tblVotos.setEnabled(False)
		horHeader = []
		horHeader.append('Cargo')
		horHeader.append('Voto')
		horHeader.append('# Votos')
		self.tblVotos.setHorizontalHeaderLabels(horHeader)

		self.btnLerCodigo = QPushButton(self.centralwidget)
		self.btnLerCodigo.setGeometry(QRect(self.screenWidth/2 - 300, self.screenHeight - 100, 200, 50))
		self.btnLerCodigo.setObjectName("btnLerCodigo")
		self.btnLerCodigo.clicked.connect(self.btnLerCodigoClicked)
		self.btnLerCodigo.setStyleSheet('QPushButton{\
					border: 2px solid #ee7543;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		self.btnGerarBoletim = QPushButton(self.centralwidget)
		self.btnGerarBoletim.setGeometry(QRect(self.screenWidth/2 + 150, self.screenHeight - 100, 200, 50))
		self.btnGerarBoletim.setObjectName("btnGerarBoletim")
		self.btnGerarBoletim.clicked.connect(self.btnGerarBoletimClicked)
		self.btnGerarBoletim.setStyleSheet('QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		self.lblMensagem = QLineEdit(self.centralwidget)
		self.lblMensagem.setGeometry(QRect(50, 50, self.screenWidth - 100, self.screenHeight - 100))
		self.lblMensagem.setFont(font)
		self.lblMensagem.setAlignment(Qt.AlignCenter)
		self.lblMensagem.setObjectName("lblMensagem")
		self.lblMensagem.setEnabled(False)
		self.lblMensagem.setVisible(False)

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
		self.btnGerarBoletim.setText(QApplication.translate("MainWindow", "GERAR BOLETIM", None, QApplication.UnicodeUTF8))
		self.btnLerCodigo.setText(QApplication.translate("MainWindow", "LER CODIGO", None, QApplication.UnicodeUTF8))

	def btnGerarBoletimClicked(self):
		som(self, 2)
		self.apurarWindow.gerarBoletim()
		self.apurarWindow.exportarCSV()
		sys.exit()

	def btnLerCodigoClicked(self):
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
					self.apurarWindow.incrementar(self.decrypt(symbol.data, open(PRIVATE_KEY, 'rb')))
				except ValueError:
					self.lblMensagem.setVisible(True)
					som(self, 2)
					self.lblMensagem.setText(U'Voto inválido. Não pertence a esta seção.')
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
				self.tblVotos.setItem(i,0,QTableWidgetItem(key))
				if k == "-1":
					self.tblVotos.setItem(i,1,QTableWidgetItem('Nulo'))
				elif k == "0":
					self.tblVotos.setItem(i,1,QTableWidgetItem('Branco'))
				else:
					self.tblVotos.setItem(i,1,QTableWidgetItem(k))
				self.tblVotos.setItem(i,2,QTableWidgetItem(str(votos[key][k])))
				i = i + 1
		# self.tblVotos.resizeColumnsToContents()
		# self.tblVotos.resizeRowsToContents()

	def decrypt(self, message, f):
		ciphertext = b64decode(message) if not isinstance(message, bytes) else message
		privateKeyFile = f.read()
		rsakey = RSA.importKey(privateKeyFile)
		rsakey = PKCS1_OAEP.new(rsakey)
		decrypted = rsakey.decrypt(b64decode(message))
		return decrypted  # Decrypt messages using own private keys...

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

def som(self, tipo):
    # define stream chunk
    chunk = 1024

    # open a wav format music
    if tipo == 1:
        f = wave.open(BEEP, "rb")
    elif tipo == 2:
        f = wave.open(FIM, "rb")
    else:
        return
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data != "":
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

def main():
	app = QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	mySW.raise_()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
