	# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'votar.ui'
#
# Created: Wed Nov 19 01:44:36 2014
#	  by: Fernando Teodoro de Lima
#
# WARNING! All changes made in this file will be lost!

from PySide.QtGui import *
from PySide.QtCore import *
import h5py
import gtk
from scipy import misc
import os
import main

#Importacao do banco de dados votacao
#file = h5py.File("votacao.h5","r")
#Importacao da tabela de candidatos
#matrizCandidatos = file["matrizCandidatos"]

h5pyFile = h5py.File('Urna.h5', 'r')
candidatos = h5pyFile['Urna/Candidatos']
perguntas = h5pyFile['Urna/Perguntas']
setupGeral = h5pyFile['Urna/SetupGeral']
tipoDeCandidato = h5pyFile['Urna/TipoDeCandidato']
partido = h5pyFile['PreEleicao/Partido']
tipoEleicao = setupGeral[0][8]

fotosPartido = h5pyFile['img_partidos']
fotosCandidatos = h5pyFile['img_candidato']

cargos2Dig = ['Governador', 'Presidente', 'Prefeito']
cargos3Dig = ['Senador']
cargos4Dig = ['Deputado Federal']
cargos5Dig = ['Deputado Estadual', 'Vereador']
cargosLegenda = ['Deputado Federal', 'Deputado Estadual', 'Vereador']

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui

	def keyPressEvent(self, event):
		print event.text()
		self.ui.acoesTecladoNumerico2(event)

#o nulo
#n nao
#s sim
#b branco
#c corrige
#a confirma

class Ui_MainWindow(object):
	cargos = []
	cargoVotado = []
	numerosDigitados = []
	cargo = ""
	MainWindow = None
	nulo = False
	leg = False

	def setupUi(self, MainWindow, cargo):
		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)
		self.cargo = cargo
		self.MainWindow = MainWindow
		self.MainWindow.setObjectName("MainWindow")
		#self.MainWindow.resize(self.screenWidth, self.screenHeight)
		self.MainWindow.showFullScreen()
		self.centralwidget = mainWidget(self, MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.label_0 = QLabel(self.centralwidget)
		self.label_0.setGeometry(QRect(50, 50, self.screenWidth - 100, 100))
		#self.label_0.setStyleSheet("border: 2px solid");
		self.label_0.setAlignment(Qt.AlignCenter)
		self.label_0.setText(self.cargo)
		self.label_0.setObjectName("label_0")
		self.label_0.setFont(font)
		self.label_0.setWordWrap(True)

		self.textEdit_1 = QTextEdit(self.centralwidget)
		self.textEdit_1.setGeometry(QRect(50, self.label_0.pos().y() + self.label_0.height(), 100, 100))
		self.textEdit_1.setFont(font)
		self.textEdit_1.setObjectName("textEdit_1")
		#chamar funcao quando texto é modificado
		self.textEdit_1.textChanged.connect(self.textEdit_1Action)

		self.textEdit_2 = QTextEdit(self.centralwidget)
		self.textEdit_2.setGeometry(QRect(self.textEdit_1.pos().x() + self.textEdit_1.width() + 50, self.textEdit_1.pos().y(), 100, 100))
		self.textEdit_2.setFont(font)
		self.textEdit_2.setObjectName("textEdit_2")
		#chamar funcao quando texto é modificado
		self.textEdit_2.textChanged.connect(self.textEdit_2Action)

		self.textEdit_3 = QTextEdit(self.centralwidget)
		self.textEdit_3.setGeometry(QRect(self.textEdit_2.pos().x() + self.textEdit_2.width() + 50, self.textEdit_1.pos().y(), 100, 100))
		self.textEdit_3.setFont(font)
		self.textEdit_3.setObjectName("textEdit_3")
		#chamar funcao quando texto é modificado
		self.textEdit_3.textChanged.connect(self.textEdit_3Action)

		self.textEdit_4 = QTextEdit(self.centralwidget)
		self.textEdit_4.setGeometry(QRect(self.textEdit_3.pos().x() + self.textEdit_3.width() + 50, self.textEdit_1.pos().y(), 100, 100))
		self.textEdit_4.setFont(font)
		self.textEdit_4.setObjectName("textEdit_4")
		#chamar funcao quando texto é modificado
		self.textEdit_4.textChanged.connect(self.textEdit_4Action)

		self.textEdit_5 = QTextEdit(self.centralwidget)
		self.textEdit_5.setGeometry(QRect(self.textEdit_3.pos().x() + self.textEdit_4.width() + 50, self.textEdit_1.pos().y(), 100, 100))
		self.textEdit_5.setFont(font)
		self.textEdit_5.setObjectName("textEdit_5")
		#chamar funcao quando texto é modificado
		self.textEdit_5.textChanged.connect(self.textEdit_5Action)

		#nesse elemento será carregada a foto do candidato/simbolo do partido
		'''self.graphicsView = QGraphicsView(self.centralwidget)
		self.graphicsView.setGeometry(QRect(50, self.textEdit_1.pos().y() + self.textEdit_1.height() + 50, 262.5, 350))
		self.graphicsView.setObjectName("graphicsView")
		self.graphicsView.setVisible(True)'''

		self.labelFigura = QLabel(self.centralwidget)
		self.labelFigura.setGeometry(QRect(50, self.textEdit_1.pos().y() + self.textEdit_1.height() + 50, 262.5, 350))
		self.labelFigura.setObjectName("labelFigura")
		self.labelFigura.setVisible(True)
		#self.labelFigura.setPixmap(QPixmap('voto.png'))
		self.labelFigura.setScaledContents(True)
		self.labelFigura.setWordWrap(False)


		self.label_1 = QLabel(self.centralwidget)
		self.label_1.setGeometry(QRect(self.labelFigura.pos().x() + self.labelFigura.width() + 50, self.textEdit_1.pos().y() + self.textEdit_1.height() + 50, self.screenWidth - (self.labelFigura.pos().x() + self.labelFigura.width() + 100), 50))
		#self.label_1.setStyleSheet("border: 2px solid");
		self.label_1.setText("")
		self.label_1.setObjectName("label_1")
		self.label_1.setFont(font)

		self.label_2 = QLabel(self.centralwidget)
		self.label_2.setGeometry(QRect(self.label_1.pos().x(), self.label_1.pos().y() + self.label_1.height() + 50, self.label_1.width(), 50))
		#self.label_2.setStyleSheet("border: 2px solid");
		self.label_2.setText("")
		self.label_2.setObjectName("label_2")
		self.label_2.setFont(font)

		self.label_3 = QLabel(self.centralwidget)
		self.label_3.setGeometry(QRect(self.label_1.pos().x(), self.label_2.pos().y() + self.label_2.height() + 50, self.label_1.width(), 50))
		#self.label_3.setStyleSheet("border: 2px solid");
		self.label_3.setText("")
		self.label_3.setObjectName("label_3")
		self.label_3.setFont(font)

		self.label_4 = QLabel(self.centralwidget)
		self.label_4.setGeometry(QRect(self.labelFigura.pos().x() + self.labelFigura.width() + 50, self.textEdit_1.pos().y() + self.textEdit_1.height() + 50, self.screenWidth - (self.labelFigura.pos().x() + self.labelFigura.width() + 100), 100))
		#self.label_4.setStyleSheet("border: 2px solid");
		self.label_4.setText("")
		self.label_4.setObjectName("label_1")
		self.label_4.setFont(font)
		self.label_4.setWordWrap(True)

		self.label_5 = QLabel(self.centralwidget)
		self.label_5.setGeometry(QRect(self.label_1.pos().x(), self.label_2.pos().y() + self.label_2.height() + 50, self.label_1.width(), 100))
		#self.label_2.setStyleSheet("border: 2px solid");
		self.label_5.setText("")
		self.label_5.setObjectName("label_2")
		self.label_5.setFont(font)
		self.label_5.setWordWrap(True)

		self.pushButton_1 = QPushButton(self.centralwidget)
		self.pushButton_1.setGeometry(QRect(50, self.screenHeight - 100, 200, 50))
		self.pushButton_1.setStyleSheet('QPushButton{\
					border: 2px solid #ffffff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')
		self.pushButton_1.setObjectName("pushButton_1")
		#chamar funcao ao clicar no botao 1
		self.pushButton_1.clicked.connect(self.brancoButton)

		self.pushButton_2 = QPushButton(self.centralwidget)
		self.pushButton_2.setGeometry(QRect(self.screenWidth/2 - 100, self.screenHeight - 100, 200, 50))
		self.pushButton_2.setStyleSheet('QPushButton{\
					border: 2px solid #ffc800;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')
		self.pushButton_2.setObjectName("pushButton_2")
		#chamar funcao ao clicar no botao 2
		self.pushButton_2.clicked.connect(self.corrigeButton)

		self.pushButton_3 = QPushButton(self.centralwidget)
		self.pushButton_3.setGeometry(QRect(self.screenWidth - 250, self.screenHeight - 100, 200, 50))
		self.pushButton_3.setStyleSheet('QPushButton{\
					border: 2px solid #00ff00;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')
		self.pushButton_3.setObjectName("pushButton_3")
		#chamar funcao ao clicar no botao 3
		self.pushButton_3.clicked.connect(self.confirmaButton)

		#altera o layout de acordo com o cargo
		#modificando a quantidade de digitos que o eleitor pode digitar
		if tipoEleicao == '0':
			self.label_4.setText('1 - ' + perguntas[0][1])
			self.label_5.setText('0 - ' + perguntas[0][2])
			self.label_1.setVisible(False)
			self.label_2.setVisible(False)
			self.label_3.setVisible(False)
			self.textEdit_2.setVisible(False)
			self.textEdit_3.setVisible(False)
			self.textEdit_4.setVisible(False)
			self.textEdit_5.setVisible(False)
		elif tipoEleicao == '1':
			if self.cargo in cargos2Dig:
				self.textEdit_3.setVisible(False)
				self.textEdit_4.setVisible(False)
				self.textEdit_5.setVisible(False)
				self.label_4.setVisible(False)
				self.label_5.setVisible(False)
			elif self.cargo in cargos3Dig:
				self.textEdit_4.setVisible(False)
				self.textEdit_5.setVisible(False)
				self.label_4.setVisible(False)
				self.label_5.setVisible(False)
			elif self.cargo in cargos4Dig:
				self.textEdit_5.setVisible(False)
				self.label_4.setVisible(False)
				self.label_5.setVisible(False)
			else:
				self.label_4.setVisible(False)
				self.label_5.setVisible(False)

		self.MainWindow.setCentralWidget(self.centralwidget)
		self.retranslateUi()
		QMetaObject.connectSlotsByName(self.MainWindow)
		self.corrigeButton()

	def retranslateUi(self):
		self.MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Votar", None, QApplication.UnicodeUTF8))
		self.pushButton_1.setText(QApplication.translate("MainWindow", "BRANCO", None, QApplication.UnicodeUTF8))
		self.pushButton_2.setText(QApplication.translate("MainWindow", "CORRIGE", None, QApplication.UnicodeUTF8))
		self.pushButton_3.setText(QApplication.translate("MainWindow", "CONFIRMA", None, QApplication.UnicodeUTF8))


	def acoesTecladoNumerico2(self, obj):
		if obj.text() == 'o':	#nulo
			self.nuloButton()
		elif obj.text() == 'n':	#nao
			print 'sem acao'
		elif obj.text() == 's':	#sim
			print 'sem acao'
		elif obj.text() == 'b':	#branco
			self.brancoButton()
		elif obj.text() == 'c':	#corrige
			self.corrigeButton()
		elif obj.text() == 'a':	#confirma
			self.confirmaButton()

	def acoesTecladoNumerico(self, obj):
		if obj.toPlainText() == 'o':	#nulo
			self.nuloButton()
		elif obj.toPlainText() == 'n':	#nao
			print 'sem acao'
		elif obj.toPlainText() == 's':	#sim
			print 'sem acao'
		elif obj.toPlainText() == 'b':	#branco
			self.brancoButton()
		elif obj.toPlainText() == 'c':	#corrige
			self.corrigeButton()
		elif obj.toPlainText() == 'a':	#confirma
			self.confirmaButton()

	#quando texto é modificado: verifica se entrada é numerica
	#foca no proximo textedit caso a entrada seja correta
	#desabilita o textEdit caso a entrada seja correta
	def textEdit_1Action(self):
		if len(self.textEdit_1.toPlainText()) > 0:
			try:
				number = int(self.textEdit_1.toPlainText())
				self.textEdit_2.setFocus()
				self.textEdit_1.setReadOnly(True)
				self.numerosDigitados.append(number)
			except ValueError:
				self.acoesTecladoNumerico(self.textEdit_1)
				self.textEdit_1.setText("")
		self.onChange()

	#quando texto é modificado: verifica se entrada é numerica
	#foca no proximo textedit caso a entrada seja correta
	#desabilita o textEdit caso a entrada seja correta
	def textEdit_2Action(self):
		if len(self.textEdit_2.toPlainText()) > 0:
			try:
				number = int(self.textEdit_2.toPlainText())
				self.textEdit_3.setFocus()
				self.textEdit_2.setReadOnly(True)
				self.numerosDigitados.append(number)
			except ValueError:
				self.acoesTecladoNumerico(self.textEdit_2)
				self.textEdit_2.setText("")
		self.onChange()

	#quando texto é modificado: verifica se entrada é numerica
	#foca no proximo textedit caso a entrada seja correta
	#desabilita o textEdit caso a entrada seja correta
	def textEdit_3Action(self):
		if len(self.textEdit_3.toPlainText()) > 0:
			try:
				number = int(self.textEdit_3.toPlainText())
				self.textEdit_4.setFocus()
				self.textEdit_3.setReadOnly(True)
				self.numerosDigitados.append(number)
			except ValueError:
				self.acoesTecladoNumerico(self.textEdit_3)
				self.textEdit_3.setText("")
		self.onChange()

	#quando texto é modificado: verifica se entrada é numerica
	#foca no proximo textedit caso a entrada seja correta
	#desabilita o textEdit caso a entrada seja correta
	def textEdit_4Action(self):
		if len(self.textEdit_4.toPlainText()) > 0:
			try:
				number = int(self.textEdit_4.toPlainText())
				self.textEdit_5.setFocus()
				self.textEdit_4.setReadOnly(True)
				self.numerosDigitados.append(number)
			except ValueError:
				self.acoesTecladoNumerico(self.textEdit_4)
				self.textEdit_4.setText("")
		self.onChange()

	#quando texto é modificado: verifica se entrada é numerica
	#foca no proximo textedit caso a entrada seja correta
	#desabilita o textEdit caso a entrada seja correta
	def textEdit_5Action(self):
		if len(self.textEdit_5.toPlainText()) > 0:
			try:
				number = int(self.textEdit_5.toPlainText())
				self.textEdit_5.setReadOnly(True)
				self.numerosDigitados.append(number)
			except ValueError:
				self.acoesTecladoNumerico(self.textEdit_5)
				self.textEdit_5.setText("")
		self.onChange()

	#define se o numero digitado corresponde a:
	# - voto nulo
	# - voto legenda
	# - voto candidato
	def onChange(self):
		self.limparTela()
		tamanho = len(self.numerosDigitados)
		index = None
		foto = None
		if tipoEleicao == '0':
			index = self.pergunta()
			self.nulo = True if index == None else False
		elif tipoEleicao == '1':
			if self.cargo in cargos2Dig:
				if tamanho == 2:
					index = self.candidato()
					self.nulo = True if index == None else False
				else: self.nulo = True

			elif self.cargo in cargos3Dig:
				if tamanho == 3:
					index = self.candidato()
					self.nulo = True if index == None else False
				else: self.nulo = True

			else:
				if self.cargo in cargosLegenda:
					if tamanho == 2:
						index = self.legenda()
						if index is not None:
							foto = fotosPartido[str(index[2])]
							misc.imsave('foto.png', foto)
							self.labelFigura.setPixmap(QPixmap('foto.png'))
							os.remove('foto.png')
						self.leg = False if index == None else True
						self.nulo = True if index == None else False
					else:
						index = self.candidato()
						self.labelFigura.setPixmap('')
						self.nulo = True if index == None else False
				else:
					index = self.candidato()
					self.labelFigura.setPixmap('')
					self.nulo = True if index == None else False

			if index is not None and foto == None:
				strCargo = self.cargo.lower().replace(' ', '_')
				foto = fotosCandidatos[strCargo][str(index[2])]
				misc.imsave('foto.png', foto)
				self.labelFigura.setPixmap(QPixmap('foto.png'))
				os.remove('foto.png')

		self.preencherTela(index, foto)

	#preenche as labels com as informacoes de acordo com o numero digitado
	#cargo: cargoLegenda = 0
	#legenda: cargoLegenda = 1
	def preencherTela(self, index, foto):
		if index is not None and tipoEleicao == '1':
			self.label_1.setText(index[0])
			self.label_2.setText(index[1])
			self.label_3.setText(index[2])

	#limpar as informacoes da tela toda vez que ela é iniciada e quando botao corrige é clicado
	def limparTela(self):
		self.nulo = True
		self.leg = False
		self.label_1.setText("")
		self.label_2.setText("")
		self.label_3.setText("")


	def pergunta(self):
		stringDigitos = ''
		for i in self.numerosDigitados:
			stringDigitos += str(i)

		#Sim
		if stringDigitos == '1':
			return ('Voto', '', 'Sim')
		#Nao
		elif stringDigitos == '0':
			return ('Voto', '', 'Nao')
		return None


	#buscar informacoes quando voto é para a legenda
	def legenda(self):
		stringDigitos = ''
		for i in self.numerosDigitados:
			stringDigitos += str(i)

		indexCandidato = None
		for i in candidatos:
			if stringDigitos == str(i[1]):
				cargo = ''
				for j in range(len(tipoDeCandidato)):
					if j == i[0]:
						cargo = tipoDeCandidato[j][0]
						break
				if self.cargo == cargo:
					indexCandidato = i

		if indexCandidato is not None:
			for indexPartido in partido:
				if indexPartido[1] == indexCandidato[1]:
					return ('Voto na legenda', str(indexPartido[2]), str(indexCandidato[1]))
		#print 'legenda nula'
		return indexCandidato

	#buscar informacoes quando voto é para o candidato
	def candidato(self):
		stringDigitos = ''
		for i in self.numerosDigitados:
			stringDigitos += str(i)

		indexCandidato = None
		for i in candidatos:
			if stringDigitos == str(i[2]):
				cargo = ''
				for j in range(len(tipoDeCandidato)):
					if j == i[0]:
						cargo = tipoDeCandidato[j][0]
						break
				if self.cargo == cargo:
					indexCandidato = i
					break

		if indexCandidato is not None:
			for indexPartido in partido:
				if indexPartido[1] == indexCandidato[1]:
					return (str(indexCandidato[3]), str(indexPartido[2]), str(indexCandidato[2]))
		#print 'candidato nulo'
		return indexCandidato

	#zerar todos os textEdit quando botao corrige é clicado
	#dar foco ao textEdit1
	def corrigeButton(self):
		while len(self.numerosDigitados) > 0:
			self.numerosDigitados.pop()
		self.textEdit_1.setReadOnly(False)
		self.textEdit_2.setReadOnly(False)
		self.textEdit_3.setReadOnly(False)
		self.textEdit_4.setReadOnly(False)
		self.textEdit_5.setReadOnly(False)
		self.labelFigura.setPixmap('')
		self.textEdit_1.setText("")
		self.textEdit_2.setText("")
		self.textEdit_3.setText("")
		self.textEdit_4.setText("")
		self.textEdit_5.setText("")
		self.textEdit_1.setFocus()
		self.limparTela()

	#acao quando botao branco é clicado
	def brancoButton(self):
		self.cargoVotado = []
		self.cargoVotado.append(self.cargo)
		self.cargoVotado.append(1)		  #branco
		self.cargoVotado.append(0)		  #nulo
		self.cargoVotado.append(0)		  #legenda
		self.cargoVotado.append('00000')	#numero
		self.cargos.append(self.cargoVotado)
		self.MainWindow.close()

	def nuloButton(self):
		self.cargoVotado = []
		self.cargoVotado.append(self.cargo)
		self.cargoVotado.append(0)		  #branco
		self.cargoVotado.append(1)		  #nulo
		self.cargoVotado.append(0)		  #legenda
		self.cargoVotado.append('00000')	#numero
		self.cargos.append(self.cargoVotado)
		self.MainWindow.close()

	#acao quando botao confirma é clicado
	def confirmaButton(self):
		stringDigitos = ''
		for i in self.numerosDigitados:
			stringDigitos += str(i)
		self.cargoVotado = []
		self.cargoVotado.append(self.cargo)
		self.cargoVotado.append(0)							#branco
		self.cargoVotado.append(1) if self.nulo == True else self.cargoVotado.append(0)	#nulo
		self.cargoVotado.append(1) if self.leg == True  else self.cargoVotado.append(0)	#legenda
		self.cargoVotado.append(stringDigitos)						#numero
		self.cargos.append(self.cargoVotado)
		main.som(self,1)
		self.MainWindow.close()


class ControlMainWindow(QMainWindow):
	def __init__(self, cargo):
		super(ControlMainWindow, self).__init__(None)
		self.ui =  Ui_MainWindow()
		self.ui.setupUi(self, cargo)
		self.show()
		self.raise_()

	def getCargosVotados(self):
	 	return self.ui.cargos

	def getQtdeCargosVotados(self):
		return len(self.ui.cargos)
