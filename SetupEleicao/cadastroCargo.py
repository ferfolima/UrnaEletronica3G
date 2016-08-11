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
        self.lblTitulo.setText("Cadastro de Cargos")
        self.lblTitulo.setFont(font)
        self.lblTitulo.setAlignment(Qt.AlignCenter)

        self.lblNomeCargo = QLabel(self.centralwidget)
        self.lblNomeCargo.setObjectName("lblNomeCargo")
        self.lblNomeCargo.setText("Nome do Cargo")
        self.lblNomeCargo.setGeometry(QRect(50, self.lblTitulo.pos().y() + 50, 200, 50))

        self.txtNomeCargo = QLineEdit(self.centralwidget)
        self.txtNomeCargo.setGeometry(QRect(50, self.lblNomeCargo.pos().y() + 40, self.screenWidth - 200, 40))
        self.txtNomeCargo.setObjectName("txtNomeCargo")

        self.lblQtdeVotos = QLabel(self.centralwidget)
        self.lblQtdeVotos.setObjectName("lblQtdeVotos")
        self.lblQtdeVotos.setText("Quantidade de vezes a ser votado")
        self.lblQtdeVotos.setGeometry(QRect(50, self.txtNomeCargo.pos().y() + 50, 200, 50))

        self.txtQtdeVotos = QLineEdit(self.centralwidget)
        self.txtQtdeVotos.setGeometry(QRect(50, self.lblQtdeVotos.pos().y() + 40, self.screenWidth - 200, 40))
        self.txtQtdeVotos.setObjectName("txtQtdeVotos")
        self.txtQtdeVotos.setText("1")

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
        self.btnSair.setText(QApplication.translate("MainWindow", "SAIR", None, QApplication.UnicodeUTF8))
        self.txtNomeCargo.setFocus()

    # funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
    def btnCadastrarClicked(self):
        if self.txtNomeCargo.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de inserir o nome')
            notificacao.show()
        elif self.txtQtdeVotos.text() == "":
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u'Oops', u'Você esqueceu de inserir a quantidade de votos')
            notificacao.show()
        else:
            database.inserirCargo(self.txtNomeCargo.text(), self.txtQtdeVotos.text())
            pynotify.init(u"Urna Eletrônica")
            notificacao = pynotify.Notification(u"OK", u"Cargo cadastrado com sucesso.")
            notificacao.show()
            self.txtNomeCargo.setText("")
            self.txtQtdeVotos.setText("1")
            self.txtNomeCargo.setFocus()

    def btnSairClicked(self):
        self.MainWindow.close()


def main():
    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySW.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
