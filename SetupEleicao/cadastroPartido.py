#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

import eleicoesDB
import pynotify

script_dir = os.path.dirname(__file__)
ICON = os.path.join(script_dir, "../files/icon.png")
database = eleicoesDB.DAO()
class ControlMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow(self.thread)
        self.ui.setupUi(self)

    def fechar(self):
        sys.exit()


class Ui_MainWindow(object):
    def __init__(self, thread):
        self.thread = thread

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.showMaximized()
        MainWindow.setWindowIcon(QIcon(ICON))

        self.MainWindow = MainWindow

        self.screenWidth = gtk.gdk.screen_width()
        self.screenHeight = gtk.gdk.screen_height()

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.installEventFilter(self.centralwidget)

        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(32)
        font.setItalic(False)

        self.lblTitulo = QLabel(self.centralwidget)
        self.lblTitulo.setGeometry(QRect(50, 50, self.screenWidth - 100, 50))
        self.lblTitulo.setObjectName("lblTitulo")
        self.lblTitulo.setText("Cadastro de Partido")
        self.lblTitulo.setFont(font)
        self.lblTitulo.setAlignment(Qt.AlignCenter)

        self.lblNomePartido = QLabel(self.centralwidget)
        self.lblNomePartido.setObjectName("lblNomePartido")
        self.lblNomePartido.setText("Nome do Partido")
        self.lblNomePartido.setGeometry(QRect(50, self.lblTitulo.pos().y() + 50, 200, 50))
        # self.lblNomePartido.setFont(font)
        # self.lblNomePartido.setAlignment(Qt.AlignCenter)

        self.txtNomePartido = QLineEdit(self.centralwidget)
        self.txtNomePartido.setGeometry(QRect(50, self.lblNomePartido.pos().y() + 40, self.screenWidth - 200, 40))
        # self.txtNomePartido.setFont(font)
        self.txtNomePartido.setObjectName("txtNomePartido")

        self.lblSiglaPartido = QLabel(self.centralwidget)
        self.lblSiglaPartido.setObjectName("lblSiglaPartido")
        self.lblSiglaPartido.setText("Sigla do Partido")
        self.lblSiglaPartido.setGeometry(QRect(50, self.lblNomePartido.pos().y() + 100, 200, 50))
        # self.lblNomePartido.setFont(font)
        # self.lblNomePartido.setAlignment(Qt.AlignCenter)

        self.txtSiglaPartido = QLineEdit(self.centralwidget)
        self.txtSiglaPartido.setGeometry(QRect(50, self.lblSiglaPartido.pos().y() + 40, self.screenWidth - 200, 40))
        # self.txtNomePartido.setFont(font)
        self.txtSiglaPartido.setObjectName("txtSiglaPartido")

        self.lblNumeroPartido = QLabel(self.centralwidget)
        self.lblNumeroPartido.setObjectName("lblNumeroPartido")
        self.lblNumeroPartido.setText("Numero do Partido")
        self.lblNumeroPartido.setGeometry(QRect(50, self.lblSiglaPartido.pos().y() + 100, 200, 50))
        # self.lblNomePartido.setFont(font)
        # self.lblNomePartido.setAlignment(Qt.AlignCenter)

        self.txtNumeroPartido = QLineEdit(self.centralwidget)
        self.txtNumeroPartido.setGeometry(QRect(50, self.lblNumeroPartido.pos().y() + 40, self.screenWidth - 200, 40))
        # self.txtNomePartido.setFont(font)
        self.txtNumeroPartido.setObjectName("txtNumeroPartido")

        self.lblPresidentePartido = QLabel(self.centralwidget)
        self.lblPresidentePartido.setObjectName("lblPresidentePartido")
        self.lblPresidentePartido.setText("Presidente do Partido")
        self.lblPresidentePartido.setGeometry(QRect(50, self.lblNumeroPartido.pos().y() + 100, 200, 50))
        # self.lblNomePartido.setFont(font)
        # self.lblNomePartido.setAlignment(Qt.AlignCenter)

        self.txtPresidentePartido = QLineEdit(self.centralwidget)
        self.txtPresidentePartido.setGeometry(QRect(50, self.lblPresidentePartido.pos().y() + 40, self.screenWidth - 200, 40))
        # self.txtNomePartido.setFont(font)
        self.txtPresidentePartido.setObjectName("txtPresidentePartido")

        # nesse elemento será carregada a foto do candidato/simbolo do partido
        self.lblFoto = QLabel(self.centralwidget)
        self.lblFoto.setGeometry(QRect(50, self.txtPresidentePartido.pos().y() + 100, 100, 100))
        self.lblFoto.setObjectName("lblFoto")
        self.lblFoto.setVisible(True)
        self.lblFoto.setScaledContents(True)
        self.lblFoto.setWordWrap(False)
        pixmap = QPixmap(ICON)
        self.lblFoto.setPixmap(pixmap)

        # nesse elemento será carregada a foto do candidato/simbolo do partido
        self.lblFotoName = QLabel(self.centralwidget)
        self.lblFotoName.setGeometry(QRect(50, self.lblFoto.pos().y() + 100, self.screenWidth - 100, 100))
        self.lblFotoName.setObjectName("lblFotoName")
        self.lblFotoName.setVisible(False)
        self.lblFotoName.setScaledContents(True)
        self.lblFotoName.setWordWrap(False)
        self.lblFotoName.setText(ICON)

        self.btnFoto = QPushButton(self.centralwidget)
        self.btnFoto.setGeometry(QRect(200 , self.lblFoto.pos().y() + self.lblFoto.height()/2 - 25, 200, 50))
        self.btnFoto.setObjectName("btnFoto")
        self.btnFoto.clicked.connect(self.btnFotoClicked)
        self.btnFoto.setStyleSheet("QPushButton{\
        					border: 2px solid #2d2dff;\
        					border-radius: 6px;\
        					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
        					min-width: 80px;}")


        self.btnCadastrar = QPushButton(self.centralwidget)
        self.btnCadastrar.setGeometry(QRect(self.screenWidth / 2 - 100, self.screenHeight - 100, 200, 50))
        self.btnCadastrar.setObjectName("btnCadastrar")
        self.btnCadastrar.clicked.connect(self.btnCadastrarClicked)
        self.btnCadastrar.setStyleSheet("QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}")

        self.btnSair = QPushButton(self.centralwidget)
        self.btnSair.setGeometry(QRect(self.screenWidth - 300, self.screenHeight - 100, 200, 50))
        self.btnSair.setObjectName("btnSair")
        self.btnSair.clicked.connect(self.btnSairClicked)
        self.btnSair.setStyleSheet("QPushButton{\
            					border: 2px solid #2d2dff;\
            					border-radius: 6px;\
            					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
            					min-width: 80px;}")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Urna Eletronica", None, QApplication.UnicodeUTF8))
        self.btnCadastrar.setText(QApplication.translate("MainWindow", "CADASTRAR", None, QApplication.UnicodeUTF8))
        self.btnFoto.setText(QApplication.translate("MainWindow", "INSERIR FOTO", None, QApplication.UnicodeUTF8))
        self.btnSair.setText(QApplication.translate("MainWindow", "SAIR", None, QApplication.UnicodeUTF8))
        self.txtNomePartido.setFocus()

    def btnFotoClicked(self):
        fname = QFileDialog.getOpenFileName()
        pixmap = QPixmap(fname[0])
        self.lblFoto.setPixmap(pixmap)
        self.lblFotoName.setText(fname[0])

    def btnSairClicked(self):
        self.MainWindow.close()

    # funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
    def btnCadastrarClicked(self):
        if self.txtNomePartido.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de inserir o nome')
            notificacao.show()
        elif self.txtSiglaPartido.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de inserir a sigla')
            notificacao.show()
        elif self.txtNumeroPartido.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de inserir o número')
            notificacao.show()
        elif self.txtPresidentePartido.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de inserir o presidente')
            notificacao.show()
        elif self.lblFotoName.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de selecionar uma foto')
            notificacao.show()
        else:
            fin = open(self.lblFotoName.text())
            img = fin.read()
            database.inserirPartido(self.txtNumeroPartido.text(), self.txtNomePartido.text(), self.txtSiglaPartido.text(), self.txtPresidentePartido.text(), img)
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u"OK", u"Partido cadastrado com sucesso.")
            notificacao.show()
            pixmap = QPixmap(ICON)
            self.lblFoto.setPixmap(pixmap)
            self.lblFotoName.setText(ICON)
            self.txtNumeroPartido.setText("")
            self.txtNomePartido.setText("")
            self.txtSiglaPartido.setText("")
            self.txtPresidentePartido.setText("")
            self.txtNomePartido.setFocus()


def main():
    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySW.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
