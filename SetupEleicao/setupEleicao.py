#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os
import subprocess
import sys
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

import cadastroCandidato
import cadastroCargo
import cadastroPartido
import eleicoesDB

script_dir = os.path.dirname(__file__)
ICON = os.path.join(script_dir, "../files/icon.png")
DB = os.path.join(script_dir, "../files/db.sql")


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
        MainWindow.showMaximized()

        self.MainWindow = MainWindow

        self.screenWidth = gtk.gdk.screen_width()
        self.screenHeight = gtk.gdk.screen_height()

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
        self.lblTitulo.setObjectName("lblTitulo")
        self.lblTitulo.setText(u"Setup de Eleição")
        self.lblTitulo.setFont(font)
        self.lblTitulo.setAlignment(Qt.AlignCenter)

        self.lblProgresso = QLabel(self.centralwidget)
        self.lblProgresso.setGeometry(QRect(300, self.lblTitulo.pos().y() + 100, self.screenWidth - 400, self.screenHeight - 200))
        self.lblProgresso.setObjectName("lblTitulo")
        self.lblProgresso.setFont(font2)
        self.lblProgresso.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.lblProgresso.setStyleSheet('QLabel{\
            border: 2px solid #000;\
            border-radius: 6px;}')


        self.btnCriarTabelas = QPushButton(self.centralwidget)
        self.btnCriarTabelas.setGeometry(QRect(50, self.lblTitulo.pos().y() + 100, 200, 50))
        self.btnCriarTabelas.setObjectName("btnCriarTabelas")
        self.btnCriarTabelas.clicked.connect(self.btnCriarTabelasClicked)
        self.btnCriarTabelas.setStyleSheet('QPushButton{\
                            border: 2px solid #ee7543;\
                            border-radius: 6px;\
                            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                            min-width: 80px;}')

        self.btnCadastrarPartido = QPushButton(self.centralwidget)
        self.btnCadastrarPartido.setGeometry(QRect(50, self.btnCriarTabelas.pos().y() + 100, 200, 50))
        self.btnCadastrarPartido.setObjectName("btnCadastrarPartido")
        self.btnCadastrarPartido.clicked.connect(self.btnCadastrarPartidoClicked)
        self.btnCadastrarPartido.setStyleSheet('QPushButton{\
                    border: 2px solid #ee7543;\
                    border-radius: 6px;\
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                    min-width: 80px;}')

        self.btnCadastrarCargo = QPushButton(self.centralwidget)
        self.btnCadastrarCargo.setGeometry(QRect(50, self.btnCadastrarPartido.pos().y() + 100, 200, 50))
        self.btnCadastrarCargo.setObjectName("btnCadastrarCargo")
        self.btnCadastrarCargo.clicked.connect(self.btnCadastrarCargoClicked)
        self.btnCadastrarCargo.setStyleSheet('QPushButton{\
                        border: 2px solid #ee7543;\
                        border-radius: 6px;\
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                        min-width: 80px;}')

        self.btnCadastrarCandidato = QPushButton(self.centralwidget)
        self.btnCadastrarCandidato.setGeometry(QRect(50, self.btnCadastrarCargo.pos().y() + 100, 200, 50))
        self.btnCadastrarCandidato.setObjectName("btnCadastrarCargos")
        self.btnCadastrarCandidato.clicked.connect(self.btnCadastrarCandidatoClicked)
        self.btnCadastrarCandidato.setStyleSheet('QPushButton{\
                            border: 2px solid #ee7543;\
                            border-radius: 6px;\
                            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
                            min-width: 80px;}')

        self.btnSair = QPushButton(self.centralwidget)
        self.btnSair.setGeometry(QRect(50, self.screenHeight - 100, 200, 50))
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
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
        self.btnCriarTabelas.setText(QApplication.translate("MainWindow", "APAGAR ELEIÇÃO", None, QApplication.UnicodeUTF8))
        self.btnCadastrarPartido.setText(QApplication.translate("MainWindow", "CADASTRAR PARTIDO", None, QApplication.UnicodeUTF8))
        self.btnCadastrarCargo.setText(QApplication.translate("MainWindow", "CADASTRAR CARGO", None, QApplication.UnicodeUTF8))
        self.btnCadastrarCandidato.setText(QApplication.translate("MainWindow", "CADASTRAR CANDIDATO", None, QApplication.UnicodeUTF8))
        self.btnSair.setText(QApplication.translate("MainWindow", "SAIR", None, QApplication.UnicodeUTF8))

    def btnSairClicked(self):
        self.MainWindow.close()

    def btnCriarTabelasClicked(self):
        database.apagarDados()
        self.lblProgresso.setText(self.lblProgresso.text() + "\nDados apagados com sucesso")

    def btnCadastrarPartidoClicked(self):
        cadastroPartido.ControlMainWindow()
        self.lblProgresso.setText(self.lblProgresso.text() + "\nPartidos cadastrados com sucesso")

    def btnCadastrarCargoClicked(self):
        cadastroCargo.ControlMainWindow()
        self.lblProgresso.setText(self.lblProgresso.text() + "\nCargos cadastrados com sucesso")

    def btnCadastrarCandidatoClicked(self):
        cadastroCandidato.ControlMainWindow()
        self.lblProgresso.setText(self.lblProgresso.text() + "\nCandidatos cadastrados com sucesso")

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
        self.thread = MyThread()
        self.thread.finished.connect(self.fechar)
        self.ui = Ui_MainWindow(self.thread)
        self.ui.setupUi(self)

    def fechar(self):
        self.ui.lblMensagem.setVisible(False)
        self.thread.exiting = False
        self.thread.index = 0


def main():
    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySW.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    database = eleicoesDB.DAO()
    main()
