#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os
import pyaudio
import pynotify
import subprocess
import sys
import wave
from base64 import b64encode
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

import pyqrcode
from PySide.QtCore import *
from PySide.QtGui import *

import votar

from ..DB import eleicoesDB
from ..Assinatura import assinatura

database = eleicoesDB.DAO()
script_dir = os.path.dirname(__file__)
PRIVATE_KEY = os.path.join(script_dir, "../files/privatekey.pem")
ICON = os.path.join(script_dir, "../files/icon.png")
BEEP = os.path.join(script_dir, "../files/beep_urna.wav")
FIM = os.path.join(script_dir, "../files/fim_urna.wav")
VOTO_PDF = os.path.join(script_dir, "../files/voto.pdf")
VOTO_PNG = os.path.join(script_dir, "../files/voto.png")


class ControlMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def keyPressEvent(self, event):
        if event.text() == '1':
            self.ui.lstCargos.setCurrentRow(0)
            self.ui.btnVotarClicked()
        elif event.text() == '2':
            self.ui.lstCargos.setCurrentRow(1)
            self.ui.btnVotarClicked()
        elif event.text() == '3':
            self.ui.lstCargos.setCurrentRow(2)
            self.ui.btnVotarClicked()
        elif event.text() == '4':
            self.ui.lstCargos.setCurrentRow(3)
            self.ui.btnVotarClicked()
        elif event.text() == '5':
            self.ui.lstCargos.setCurrentRow(4)
            self.ui.btnVotarClicked()
        elif event.text() == '6':
            self.ui.lstCargos.setCurrentRow(5)
            self.ui.btnVotarClicked()
        elif event.text() == '7':
            self.ui.lstCargos.setCurrentRow(6)
            self.ui.btnVotarClicked()
        elif event.text() == '8':
            self.ui.lstCargos.setCurrentRow(7)
            self.ui.btnVotarClicked()
        elif event.text() == '9':
            self.ui.lstCargos.setCurrentRow(8)
            self.ui.btnVotarClicked()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.show()
        MainWindow.showMaximized()
        MainWindow.setWindowIcon(QIcon(ICON))

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
        self.btnVotar.setGeometry(QRect(self.screenWidth / 2 - 100, self.screenHeight - 100, 200, 50))
        self.btnVotar.setObjectName("btnVotar")
        self.btnVotar.clicked.connect(self.btnVotarClicked)
        self.btnVotar.setStyleSheet("QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}")

        self.lstCargos = QListWidget(self.centralwidget)
        self.lstCargos.setGeometry(
            QRect(100, self.lblTitulo.pos().y() + self.lblTitulo.height() + 50, self.screenWidth - 200,
                  self.screenHeight - self.lblTitulo.height() - self.btnVotar.height() - 200))
        self.lstCargos.setObjectName("lstCargos")
        self.lstCargos.setFont(font)
        self.lstCargos.setWordWrap(True)

        # preencher lstCargos com cargos para eleicao
        for cargo in database.getCargos():
            item = QListWidgetItem(cargo)
            self.lstCargos.addItem(item)
        self.lstCargos.setCurrentRow(0)

        font2 = QFont()
        font2.setFamily("Helvetica")
        font2.setPointSize(34)
        font2.setItalic(False)
        self.lblSelecionarCargo = QLabel(self.centralwidget)
        self.lblSelecionarCargo.setGeometry(
            QRect(50, self.lstCargos.pos().y() - 160, 50, self.screenHeight))
        self.lblSelecionarCargo.setObjectName("lblTitulo")
        self.lblSelecionarCargo.setText("1\n2\n3\n4\n5\n6\n7")
        self.lblSelecionarCargo.setFont(font2)

        # label que ira mostrar mensagem "imprimindo voto"
        # ele fica invisivel no inicio e so aparece quando a listview e esvaziada
        # ou seja, quando o eleitor ja votou para todos os cargos possiveis
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
        MainWindow.setWindowTitle(
            QApplication.translate("MainWindow", "Urna Eletronica", None, QApplication.UnicodeUTF8))
        self.btnVotar.setText(QApplication.translate("MainWindow", "VOTAR", None, QApplication.UnicodeUTF8))
        self.lblImprimir.setText(QApplication.translate("MainWindow", "", None, QApplication.UnicodeUTF8))

    # funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
    def btnVotarClicked(self):
        if self.lstCargos.currentItem() is None:
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u"ERRO", u"Nenhum candidato selecionado.")
            notificacao.show()
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
    def __init__(self, ui, parent=None):
        super(mainWidget, self).__init__(parent)
        self.ui = ui
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QEvent.WindowActivate:
            if self.ui.votarWindow is not None:
                if database.getQtdeCargos() == self.ui.votarWindow.getQtdeCargosVotados():
                    som(self, 2)
                    self.ui.lblImprimir.setText("Imprimindo voto")
                    gerarString(self, self.ui.votarWindow.getCargosVotados())
        return False


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

# funcao para gerar string para imprimir QRCode
def gerarString(self, votos):
    c = canvas.Canvas(VOTO_PDF)
    c.setPageSize((6.2 * cm, 10 * cm))
    c.setFont("Helvetica", 10)

    line = 9.5
    textobject = c.beginText()
    textobject.setTextOrigin(0.3 * cm, line * cm)
    textobject.moveCursor(0,15)
    stringQRCode = "#"
    moverLinhas = len(votos)
    for cargo in database.getCargosQtde():
        for voto in votos:
            string = ""
            if cargo == str(voto[0]):
                string += cargo + ": "
                textobject.textOut(string)
                textobject.moveCursor(0, 10)
                string = ""
                if str(voto[1]) == "1":
                    string += "Voto em branco"
                    stringQRCode += "0"
                elif str(voto[2]) == "1":
                    string += "Voto Nulo"
                    stringQRCode += "-1"
                else:
                    string += "Candidato número "+ str(voto[3])
                    stringQRCode += str(voto[3])
                textobject.textOut(string)
                textobject.moveCursor(0,14)
                votos.remove(voto)
        stringQRCode += ";"
    textobject.moveCursor(0, 100 - moverLinhas*24)
    string = "_ _ _ _ _ _ Dobre Aqui _ _ _ _ _ _"
    textobject.textOut(string)

    id_voto = b64encode(os.urandom(16))
    stringQRCode += str(id_voto)
    signature, message = assinatura.sign(stringQRCode, open(PRIVATE_KEY, "rb"))
    sigAndMessage = signature + ":" + message
    url = pyqrcode.create(sigAndMessage, error="L", encoding="utf-8")
    url.png(VOTO_PNG, scale=1)

    c.drawText(textobject)
    c.drawImage(VOTO_PNG, 0.80 * cm, 0.50 * cm, 4.5 * cm, 4.5 * cm)
    os.remove(VOTO_PNG)
    c.showPage()
    c.save()

    subprocess.Popen("lp '{0}'".format(VOTO_PDF), shell=True).wait()
    subprocess.Popen("rm '{0}'".format(VOTO_PDF), shell=True).wait()

    sys.exit()

def main():
    if not os.path.isfile(PRIVATE_KEY):
        pynotify.init(u"Urna Eletrônica")
        notificacao = pynotify.Notification(u"ERRO", u"Chave pública não encontrada.")
        notificacao.show()
        sys.exit()

    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySW.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
