#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os
import sys
import zbar
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import eleicoesDB

script_dir = os.path.dirname(__file__)
PRIVATE_KEY = os.path.join(script_dir, "../files/privatekey.pem")
ICON = os.path.join(script_dir, "../files/icon.png")


class mainWidget(QWidget):
    def __init__(self, ui, parent=None):
        super(mainWidget, self).__init__(parent)
        self.ui = ui


class Ui_MainWindow(object):
    def __init__(self, thread):
        self.thread = thread

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        MainWindow.setWindowIcon(QIcon(ICON))

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

        font2 = QFont()
        font2.setFamily("Helvetica")
        font2.setPointSize(20)
        font2.setItalic(False)

        self.lblTitulo = QLabel(self.centralwidget)
        self.lblTitulo.setGeometry(QRect(50, 50, self.screenWidth - 100, 50))
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setText("Seu voto")
        self.lblTitulo.setObjectName("lblTitulo")
        self.lblTitulo.setFont(font)

        font.setPointSize(12)

        self.lblVoto = QLabel(self.centralwidget)
        self.lblVoto.setGeometry(
            QRect(50, self.lblTitulo.pos().y() + self.lblTitulo.height() + 50, self.screenWidth - 100,
                  self.screenHeight - 150 - self.lblTitulo.height()))
        self.lblVoto.setFont(font2)
        self.lblVoto.setAlignment(Qt.AlignHCenter)
        self.lblVoto.setText("")
        self.lblVoto.setObjectName("lblVoto")

        self.btnVerificar = QPushButton(self.centralwidget)
        self.btnVerificar.setGeometry(QRect(self.screenWidth / 2 - 100, self.screenHeight - 100, 200, 50))
        self.btnVerificar.setObjectName("btnVerificar")
        # chamar funcao ao clicar no botao 1
        self.btnVerificar.clicked.connect(self.btnVerificarClicked)
        self.btnVerificar.setStyleSheet('QPushButton{\
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
        self.btnVerificar.setText(QApplication.translate("MainWindow", "VERIFICAR", None, QApplication.UnicodeUTF8))

    def btnVerificarClicked(self):
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
                    self.lblVoto.setText(decodificarString(symbol.data))
                    self.thread.start()
                except ValueError:
                    self.lblVoto.setText(U'Voto inválido. Não pertence a esta seção.')
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


# thread
class MyThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.index = 0

    def run(self):
        while self.exiting == False:
            self.index += 1
            sleep(1)
            if self.index == 6:
                self.exiting = True


class ControlMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        # thread criada para aguardar 5 segundos antes de
        #	reiniciar o programa após um eleitor votar
        self.thread = MyThread()
        self.thread.finished.connect(self.fechar)
        self.ui = Ui_MainWindow(self.thread)
        self.ui.setupUi(self)

    def fechar(self):
        self.ui.lblVoto.setText("")
        self.thread.exiting = False
        self.thread.index = 0


def decrypt(message, f):
    ciphertext = b64decode(message) if not isinstance(message, bytes) else message
    privateKeyFile = f.read()
    rsakey = RSA.importKey(privateKeyFile)
    rsakey = PKCS1_OAEP.new(rsakey)
    decrypted = rsakey.decrypt(b64decode(message))
    return decrypted  # Decrypt messages using own private keys...


def decodificarString(encrypted):
    string = decrypt(encrypted, open(PRIVATE_KEY, 'rb'))

    lstCargos = database.getCargosQtde()
    infoVotos = string[1:].split(';')
    stringVotos = ''
    for indiceCargo in range(len(lstCargos)):
        stringVotos += lstCargos[indiceCargo] + ": "
        voto = infoVotos[indiceCargo]
        if infoVotos[indiceCargo] == "-1":
            voto = "Nulo"
        elif infoVotos[indiceCargo] == "0":
            voto = "Branco"
        stringVotos += voto + "\n\n"

    return stringVotos

def main():
    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySW.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    database = eleicoesDB.DAO()
    main()
