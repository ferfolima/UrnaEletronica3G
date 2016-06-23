from PySide.QtGui import *
from PySide.QtCore import *
from time import sleep
import sys
import os
import zbar
import gtk
import incrementar
import generateKey

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui

	def keyPressEvent(self, event):
		if event.text() == '.':
			self.ui.btnLerCodigoClicked()
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

		self.tblVotos = QTableWidget(self.centralwidget)
		self.tblVotos.setGeometry(QRect(50, 50, self.screenWidth - 100, 500))
		self.tblVotos.setObjectName('tblVotos')
		self.tblVotos.setRowCount(1000000)
		self.tblVotos.setColumnCount(3)
		self.tblVotos.setColumnWidth(0,(self.screenWidth - 185)/3)
		self.tblVotos.setColumnWidth(1,(self.screenWidth - 185)/3)
		self.tblVotos.setColumnWidth(2,(self.screenWidth - 185)/3)
		self.tblVotos.setEnabled(False);
		horHeader = []
		horHeader.append('Cargo')
		horHeader.append('Voto')
		horHeader.append('# Votos')
		self.tblVotos.setHorizontalHeaderLabels(horHeader)

		self.btnGerarChaves = QPushButton(self.centralwidget)
		self.btnGerarChaves.setGeometry(QRect(self.screenWidth/2 - 450, self.screenHeight - 100, 200, 50))
		self.btnGerarChaves.setObjectName("btnGerarChaves")
        #chamar funcao ao clicar no botao 1
		self.btnGerarChaves.clicked.connect(self.btnGerarChavesClicked)
		#self.btnLerCodigo.setStyle('cleanlooks')
		self.btnGerarChaves.setStyleSheet('QPushButton{\
                    border: 2px solid #ee7543;\
                    border-radius: 6px;\
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                    min-width: 80px;}')

		self.btnLerCodigo = QPushButton(self.centralwidget)
		self.btnLerCodigo.setGeometry(QRect(self.screenWidth/2 - 125, self.screenHeight - 100, 200, 50))
		self.btnLerCodigo.setObjectName("btnLerCodigo")
		self.btnLerCodigo.clicked.connect(self.btnLerCodigoClicked)
		self.btnLerCodigo.setStyleSheet('QPushButton{\
					border: 2px solid #ee7543;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		self.btnGerarBoletim = QPushButton(self.centralwidget)
		self.btnGerarBoletim.setGeometry(QRect(self.screenWidth/2 + 200, self.screenHeight - 100, 200, 50))
		self.btnGerarBoletim.setObjectName("btnGerarBoletim")
		self.btnGerarBoletim.clicked.connect(self.btnGerarBoletimClicked)
		self.btnGerarBoletim.setStyleSheet('QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		if (os.path.isfile('./privatekey.pem') and os.path.isfile('./publickey.pem')):
			#print('se do dois arquivos existem, o botao deve ser inativado')
			self.btnGerarChaves.setEnabled(False)

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
		self.btnGerarChaves.setText(QApplication.translate("MainWindow", "GERAR CHAVES", None, QApplication.UnicodeUTF8))

	def btnGerarBoletimClicked(self):
		self.apurarWindow.gerarBoletim()
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
					self.apurarWindow.incrementar(generateKey.decrypt(symbol.data, open('./privatekey.pem','rb')))
				except ValueError:
					self.lblMensagem.setVisible(True)
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

	def btnGerarChavesClicked(self):
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
	main()
