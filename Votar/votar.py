#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk

from PySide.QtCore import *
from PySide.QtGui import *

import pyaudio
import wave
import pynotify
import os
import eleicoesDB

script_dir = os.path.dirname(__file__)
BEEP = os.path.join(script_dir, "../files/beep_urna.wav")
FIM = os.path.join(script_dir, "../files/fim_urna.wav")

database = eleicoesDB.DAO()

class mainWidget(QWidget):
    def __init__(self, ui, parent=None):
        super(mainWidget, self).__init__(parent)
        self.ui = ui

    def keyPressEvent(self, event):
        self.ui.acoesTecladoNumerico(event.text())

# n nulo
# b branco
# c corrige
# a confirma

class Ui_MainWindow(object):
    cargos = []
    cargoVotado = []
    numerosDigitados = []
    cargo = ""
    MainWindow = None
    branco = False
    nulo = False
    leg = False

    def setupUi(self, MainWindow, cargo):
        self.screenWidth = gtk.gdk.screen_width()
        self.screenHeight = gtk.gdk.screen_height()

        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(32)
        font.setItalic(False)
        self.qtdeVotosNecessarios = database.getQtdeVotosCargo(cargo)
        self.cargo = cargo
        self.qtdeVotos = 0
        self.candidatoVotado = []
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.showMaximized()

        self.centralwidget = mainWidget(self, MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lblCargo = QLabel(self.centralwidget)
        self.lblCargo.setGeometry(QRect(50, 50, self.screenWidth - 100, 100))
        self.lblCargo.setAlignment(Qt.AlignCenter)
        self.lblCargo.setText(self.cargo)
        self.lblCargo.setObjectName("lblCargo")
        self.lblCargo.setFont(font)
        self.lblCargo.setWordWrap(True)

        self.txtQuadrado1 = QTextEdit(self.centralwidget)
        self.txtQuadrado1.setGeometry(QRect(50, self.lblCargo.pos().y() + self.lblCargo.height(), 100, 100))
        self.txtQuadrado1.setFont(font)
        self.txtQuadrado1.setObjectName("txtQuadrado1")
        self.txtQuadrado1.setCursorWidth(0)
        self.txtQuadrado1.textChanged.connect(self.txtQuadrado1Action)

        self.txtQuadrado2 = QTextEdit(self.centralwidget)
        self.txtQuadrado2.setGeometry(
            QRect(self.txtQuadrado1.pos().x() + self.txtQuadrado1.width() + 50, self.txtQuadrado1.pos().y(), 100, 100))
        self.txtQuadrado2.setFont(font)
        self.txtQuadrado2.setObjectName("txtQuadrado2")
        self.txtQuadrado2.setCursorWidth(0)
        self.txtQuadrado2.textChanged.connect(self.txtQuadrado2Action)

        self.txtQuadrado3 = QTextEdit(self.centralwidget)
        self.txtQuadrado3.setGeometry(
            QRect(self.txtQuadrado2.pos().x() + self.txtQuadrado2.width() + 50, self.txtQuadrado1.pos().y(), 100, 100))
        self.txtQuadrado3.setFont(font)
        self.txtQuadrado3.setObjectName("txtQuadrado3")
        self.txtQuadrado3.setCursorWidth(0)
        self.txtQuadrado3.textChanged.connect(self.txtQuadrado3Action)

        self.txtQuadrado4 = QTextEdit(self.centralwidget)
        self.txtQuadrado4.setGeometry(
            QRect(self.txtQuadrado3.pos().x() + self.txtQuadrado3.width() + 50, self.txtQuadrado1.pos().y(), 100, 100))
        self.txtQuadrado4.setFont(font)
        self.txtQuadrado4.setObjectName("txtQuadrado4")
        self.txtQuadrado4.setCursorWidth(0)
        self.txtQuadrado4.textChanged.connect(self.txtQuadrado4Action)

        self.txtQuadrado5 = QTextEdit(self.centralwidget)
        self.txtQuadrado5.setGeometry(
            QRect(self.txtQuadrado4.pos().x() + self.txtQuadrado4.width() + 50, self.txtQuadrado1.pos().y(), 100, 100))
        self.txtQuadrado5.setFont(font)
        self.txtQuadrado5.setObjectName("txtQuadrado5")
        self.txtQuadrado5.setCursorWidth(0)
        self.txtQuadrado5.textChanged.connect(self.txtQuadrado5Action)

        # nesse elemento será carregada a foto do candidato/simbolo do partido
        self.lblFoto = QLabel(self.centralwidget)
        self.lblFoto.setGeometry(QRect(50, self.txtQuadrado1.pos().y() + self.txtQuadrado1.height() + 50, 262.5, 350))
        self.lblFoto.setObjectName("lblFoto")
        self.lblFoto.setVisible(True)
        self.lblFoto.setScaledContents(True)
        self.lblFoto.setWordWrap(False)

        self.lblNomeCandidato = QLabel(self.centralwidget)
        self.lblNomeCandidato.setGeometry(QRect(self.lblFoto.pos().x() + self.lblFoto.width() + 50,
                                                self.txtQuadrado1.pos().y() + self.txtQuadrado1.height() + 50,
                                                self.screenWidth - (
                                                self.lblFoto.pos().x() + self.lblFoto.width() + 100), 50))
        self.lblNomeCandidato.setText("")
        self.lblNomeCandidato.setObjectName("lblNomeCandidato")
        self.lblNomeCandidato.setFont(font)

        self.lblNomePartido = QLabel(self.centralwidget)
        self.lblNomePartido.setGeometry(QRect(self.lblNomeCandidato.pos().x(),
                                              self.lblNomeCandidato.pos().y() + self.lblNomeCandidato.height() + 50,
                                              self.lblNomeCandidato.width(), 50))
        self.lblNomePartido.setText("")
        self.lblNomePartido.setObjectName("lblNomePartido")
        self.lblNomePartido.setFont(font)

        self.lblNumeroLegenda = QLabel(self.centralwidget)
        self.lblNumeroLegenda.setGeometry(
            QRect(self.lblNomeCandidato.pos().x(), self.lblNomePartido.pos().y() + self.lblNomePartido.height() + 50,
                  self.lblNomeCandidato.width(), 50))
        self.lblNumeroLegenda.setText("")
        self.lblNumeroLegenda.setObjectName("lblNumeroLegenda")
        self.lblNumeroLegenda.setFont(font)

        self.lblOpcao1 = QLabel(self.centralwidget)
        self.lblOpcao1.setGeometry(QRect(self.lblFoto.pos().x() + self.lblFoto.width() + 50,
                                         self.txtQuadrado1.pos().y() + self.txtQuadrado1.height() + 50,
                                         self.screenWidth - (self.lblFoto.pos().x() + self.lblFoto.width() + 100), 100))
        self.lblOpcao1.setText("")
        self.lblOpcao1.setObjectName("lblOpcao1")
        self.lblOpcao1.setFont(font)
        self.lblOpcao1.setWordWrap(True)

        self.lblOpcao2 = QLabel(self.centralwidget)
        self.lblOpcao2.setGeometry(
            QRect(self.lblNomeCandidato.pos().x(), self.lblNomePartido.pos().y() + self.lblNomePartido.height() + 50,
                  self.lblNomeCandidato.width(), 100))
        self.lblOpcao2.setText("")
        self.lblOpcao2.setObjectName("lblOpcao2")
        self.lblOpcao2.setFont(font)
        self.lblOpcao2.setWordWrap(True)

        self.btnBranco = QPushButton(self.centralwidget)
        self.btnBranco.setGeometry(QRect(50, self.screenHeight - 100, 200, 50))
        self.btnBranco.setStyleSheet("QPushButton{\
					border: 2px solid #ffffff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}")
        self.btnBranco.setObjectName("btnBranco")
        self.btnBranco.clicked.connect(self.btnBrancoClicked)

        self.btnCorrige = QPushButton(self.centralwidget)
        self.btnCorrige.setGeometry(QRect(self.screenWidth / 2 - 100, self.screenHeight - 100, 200, 50))
        self.btnCorrige.setStyleSheet("QPushButton{\
					border: 2px solid #ffc800;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}")
        self.btnCorrige.setObjectName("btnCorrige")
        self.btnCorrige.clicked.connect(self.btnCorrigeClicked)

        self.btnConfirma = QPushButton(self.centralwidget)
        self.btnConfirma.setGeometry(QRect(self.screenWidth - 250, self.screenHeight - 100, 200, 50))
        self.btnConfirma.setStyleSheet("QPushButton{\
					border: 2px solid #00ff00;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}")
        self.btnConfirma.setObjectName("btnConfirma")
        self.btnConfirma.clicked.connect(self.btnConfirmaClicked)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self.MainWindow)

        # Função é chamada para limpar qualquer info que esteja nos quadrados
        self.btnCorrigeClicked()

    def retranslateUi(self):
        self.MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Votar", None, QApplication.UnicodeUTF8))
        self.btnBranco.setText(QApplication.translate("MainWindow", "BRANCO", None, QApplication.UnicodeUTF8))
        self.btnCorrige.setText(QApplication.translate("MainWindow", "CORRIGE", None, QApplication.UnicodeUTF8))
        self.btnConfirma.setText(QApplication.translate("MainWindow", "CONFIRMA", None, QApplication.UnicodeUTF8))

    def acoesTecladoNumerico(self, text):
        if text == "n":  # nulo
            self.btnNuloClicked()
        elif text == "b":  # branco
            self.btnBrancoClicked()
        elif text == "c":  # corrige
            self.btnCorrigeClicked()
        elif text == "a":  # confirma
            self.btnConfirmaClicked()

    # quando texto é modificado: verifica se entrada é numerica
    # foca no proximo textedit caso a entrada seja correta
    # desabilita o textEdit caso a entrada seja correta
    def txtQuadrado1Action(self):
        if len(self.txtQuadrado1.toPlainText()) > 0:
            try:
                number = int(self.txtQuadrado1.toPlainText())
                self.txtQuadrado2.setFocus()
                self.txtQuadrado1.setReadOnly(True)
                self.numerosDigitados.append(number)
            except ValueError:
                self.acoesTecladoNumerico(self.txtQuadrado1.toPlainText())
                self.txtQuadrado1.setText("")
        self.onChange()

    def txtQuadrado2Action(self):
        if len(self.txtQuadrado2.toPlainText()) > 0:
            try:
                number = int(self.txtQuadrado2.toPlainText())
                self.txtQuadrado3.setFocus()
                self.txtQuadrado2.setReadOnly(True)
                self.numerosDigitados.append(number)
            except ValueError:
                self.acoesTecladoNumerico(self.txtQuadrado2.toPlainText())
                self.txtQuadrado2.setText("")
        self.onChange()

    def txtQuadrado3Action(self):
        if len(self.txtQuadrado3.toPlainText()) > 0:
            try:
                number = int(self.txtQuadrado3.toPlainText())
                self.txtQuadrado4.setFocus()
                self.txtQuadrado3.setReadOnly(True)
                self.numerosDigitados.append(number)
            except ValueError:
                self.acoesTecladoNumerico(self.txtQuadrado3.toPlainText())
                self.txtQuadrado3.setText("")
        self.onChange()

    def txtQuadrado4Action(self):
        if len(self.txtQuadrado4.toPlainText()) > 0:
            try:
                number = int(self.txtQuadrado4.toPlainText())
                self.txtQuadrado5.setFocus()
                self.txtQuadrado4.setReadOnly(True)
                self.numerosDigitados.append(number)
            except ValueError:
                self.acoesTecladoNumerico(self.txtQuadrado4.toPlainText())
                self.txtQuadrado4.setText("")
        self.onChange()

    def txtQuadrado5Action(self):
        if len(self.txtQuadrado5.toPlainText()) > 0:
            try:
                number = int(self.txtQuadrado5.toPlainText())
                self.txtQuadrado5.setReadOnly(True)
                self.numerosDigitados.append(number)
            except ValueError:
                self.acoesTecladoNumerico(self.txtQuadrado5.toPlainText())
                self.txtQuadrado5.setText("")
        self.onChange()

    def onChange(self):
        self.limparTela()
        self.preencherTela()

    def preencherTela(self):
        if len(self.numerosDigitados) > 0:
            nome, numero, partido, foto = database.getCandidatoNumeroPartido(self.numerosDigitados, self.cargo)
            if nome is not None and partido is not None and numero is not None and foto is not None:
                qimg = QImage.fromData(foto)
                pixmap = QPixmap.fromImage(qimg)
                self.lblFoto.setPixmap(pixmap)
                self.nulo = False
                self.lblNomeCandidato.setText(nome)
                self.lblNomePartido.setText(partido)
                self.lblNumeroLegenda.setText(str(numero))

    # limpar as informacoes da tela toda vez que ela é iniciada e quando botao corrige é clicado
    def limparTela(self):
        self.nulo = True
        self.leg = False
        self.lblNomeCandidato.setText("")
        self.lblNomePartido.setText("")
        self.lblNumeroLegenda.setText("")
        self.lblFoto.setPixmap("")


    # zerar todos os textEdit quando botao corrige é clicado
    # dar foco ao textEdit1
    def btnCorrigeClicked(self):
        while len(self.numerosDigitados) > 0:
            self.numerosDigitados.pop()
        self.txtQuadrado1.setReadOnly(False)
        self.txtQuadrado2.setReadOnly(False)
        self.txtQuadrado3.setReadOnly(False)
        self.txtQuadrado4.setReadOnly(False)
        self.txtQuadrado5.setReadOnly(False)
        self.lblFoto.setPixmap("")
        self.txtQuadrado1.setText("")
        self.txtQuadrado2.setText("")
        self.txtQuadrado3.setText("")
        self.txtQuadrado4.setText("")
        self.txtQuadrado5.setText("")
        self.txtQuadrado1.setFocus()
        self.limparTela()


    # acao quando botao branco é clicado
    def btnBrancoClicked(self):
        self.branco = True
        self.btnCorrigeClicked()
        self.lblNomeCandidato.setText("Branco")


    def btnNuloClicked(self):
        self.cargoVotado = []
        self.cargoVotado.append(self.cargo)
        self.cargoVotado.append(0)  # branco
        self.cargoVotado.append(1)  # nulo
        self.cargoVotado.append(0)  # legenda
        self.cargoVotado.append("00000")  # numero
        if (self.lblNumeroLegenda.text() not in self.candidatoVotado or self.lblNumeroLegenda.text() == ""):
            self.cargos.append(self.cargoVotado)
            self.candidatoVotado.append(self.lblNumeroLegenda.text())
            self.qtdeVotos += 1
            if (self.qtdeVotos == int(self.qtdeVotosNecessarios)):
                self.MainWindow.close()
            else:
                self.btnCorrigeClicked()


    # acao quando botao confirma é clicado
    def btnConfirmaClicked(self):
        if(self.branco):
            self.branco = False
            self.cargoVotado = []
            self.cargoVotado.append(self.cargo)
            self.cargoVotado.append(1)  # branco
            self.cargoVotado.append(0)  # nulo
            self.cargoVotado.append(0)  # legenda
            self.cargoVotado.append("00000")  # numero
            if (self.lblNumeroLegenda.text() not in self.candidatoVotado or self.lblNumeroLegenda.text() == ""):
                som(self,1)
                self.cargos.append(self.cargoVotado)
                self.candidatoVotado.append(self.lblNumeroLegenda.text())
                self.qtdeVotos += 1
                if (self.qtdeVotos == int(self.qtdeVotosNecessarios)):
                    self.MainWindow.close()
                else:
                    self.btnCorrigeClicked()
        else:
            stringDigitos = ""
            for i in self.numerosDigitados:
                stringDigitos += str(i)
            self.cargoVotado = []
            self.cargoVotado.append(self.cargo)
            self.cargoVotado.append(0)  # branco
            self.cargoVotado.append(1) if self.nulo == True else self.cargoVotado.append(0)  # nulo
            self.cargoVotado.append(1) if self.leg == True  else self.cargoVotado.append(0)  # legenda
            self.cargoVotado.append(stringDigitos)  # numero
            if (self.lblNumeroLegenda.text() not in self.candidatoVotado and self.txtQuadrado1.toPlainText() != ""):
                som(self,1)
                self.cargos.append(self.cargoVotado)
                self.candidatoVotado.append(self.lblNumeroLegenda.text())
                self.qtdeVotos += 1
                if (self.qtdeVotos == int(self.qtdeVotosNecessarios)):
                    self.MainWindow.close()
                else:
                    self.btnCorrigeClicked()
            elif (self.lblNumeroLegenda.text() in self.candidatoVotado and self.nulo):
                som(self,1)
                self.cargos.append(self.cargoVotado)
                self.candidatoVotado.append(self.lblNumeroLegenda.text())
                self.qtdeVotos += 1
                if (self.qtdeVotos == int(self.qtdeVotosNecessarios)):
                    self.MainWindow.close()
                else:
                    self.btnCorrigeClicked()
            else:
                self.btnCorrigeClicked()

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

class ControlMainWindow(QMainWindow):
    def __init__(self, cargo, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, cargo)

    def getCargosVotados(self):
        return self.ui.cargos

    def getQtdeCargosVotados(self):
        return len(self.ui.cargos)
