# -*- coding: utf-8 -*-
import gtk
import sys
from PySide.QtCore import *
from PySide.QtGui import *

from Urna.urnadao import eleicoesDB


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
        MainWindow.showFullScreen()
        MainWindow.setWindowIcon(QIcon('../../files/icon.png'))

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
        self.lblTitulo.setText("Cadastro de Candidato")
        self.lblTitulo.setFont(font)
        self.lblTitulo.setAlignment(Qt.AlignCenter)

        # nesse elemento será carregada a foto do candidato/simbolo do partido
        self.lblFoto = QLabel(self.centralwidget)
        self.lblFoto.setGeometry(QRect(100, self.lblTitulo.pos().y() + 100, 100, 100))
        self.lblFoto.setObjectName("lblFoto")
        self.lblFoto.setVisible(True)
        self.lblFoto.setScaledContents(True)
        self.lblFoto.setWordWrap(False)
        pixmap = QPixmap('../../files/icon.png')
        self.lblFoto.setPixmap(pixmap)

        self.btnFoto = QPushButton(self.centralwidget)
        self.btnFoto.setGeometry(QRect(100, self.lblFoto.pos().y() + 120, 100, 50))
        self.btnFoto.setObjectName("btnFoto")
        self.btnFoto.clicked.connect(self.btnFotoClicked)
        self.btnFoto.setStyleSheet("QPushButton{\
            					border: 2px solid #2d2dff;\
            					border-radius: 6px;\
            					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
            					min-width: 80px;}")

        # nesse elemento será carregada a foto do candidato/simbolo do partido
        self.lblFotoName = QLabel(self.centralwidget)
        self.lblFotoName.setGeometry(QRect(50, self.lblFoto.pos().y() + 100, self.screenWidth - 100, 100))
        self.lblFotoName.setObjectName("lblFotoName")
        self.lblFotoName.setVisible(False)
        self.lblFotoName.setScaledContents(True)
        self.lblFotoName.setWordWrap(False)
        self.lblFotoName.setText('../../files/icon.png')

        self.lblNomeCandidato = QLabel(self.centralwidget)
        self.lblNomeCandidato.setObjectName("lblNomeCandidato")
        self.lblNomeCandidato.setText("Nome do Candidato")
        self.lblNomeCandidato.setGeometry(QRect(250, self.lblTitulo.pos().y() + 50, 200, 50))

        self.txtNomeCandidato = QLineEdit(self.centralwidget)
        self.txtNomeCandidato.setGeometry(QRect(250, self.lblNomeCandidato.pos().y() + 40, self.screenWidth - 300, 40))
        self.txtNomeCandidato.setObjectName("txtNomeCandidato")

        self.lblNumeroCandidato = QLabel(self.centralwidget)
        self.lblNumeroCandidato.setObjectName("lblNumeroCandidato")
        self.lblNumeroCandidato.setText("Numero do Candidato")
        self.lblNumeroCandidato.setGeometry(QRect(250, self.txtNomeCandidato.pos().y() + 40, 200, 50))

        self.txtNumeroCandidato = QLineEdit(self.centralwidget)
        self.txtNumeroCandidato.setGeometry(QRect(250, self.lblNumeroCandidato.pos().y() + 40, self.screenWidth - 300, 40))
        self.txtNumeroCandidato.setObjectName("txtNumeroCandidato")

        self.lblTituloCandidato = QLabel(self.centralwidget)
        self.lblTituloCandidato.setObjectName("lblTituloCandidato")
        self.lblTituloCandidato.setText("Titulo do Candidato")
        self.lblTituloCandidato.setGeometry(QRect(250, self.txtNumeroCandidato.pos().y() + 40, 200, 50))

        self.txtTituloCandidato = QLineEdit(self.centralwidget)
        self.txtTituloCandidato.setGeometry(QRect(250, self.lblTituloCandidato.pos().y() + 40, self.screenWidth - 300, 40))
        self.txtTituloCandidato.setObjectName("txtTituloCandidato")

        self.lblCargoCandidato = QLabel(self.centralwidget)
        self.lblCargoCandidato.setObjectName("lblCargoCandidato")
        self.lblCargoCandidato.setText("Cargo")
        self.lblCargoCandidato.setGeometry(QRect(250, self.txtTituloCandidato.pos().y() + 40, 200, 50))

        self.comboCargoCandidato = QComboBox(self.centralwidget)
        self.comboCargoCandidato.addItem('')
        cargos = database.getCargos()
        for cargo in cargos:
            self.comboCargoCandidato.addItem(cargo[0])
        self.comboCargoCandidato.setGeometry(QRect(250, self.lblCargoCandidato.pos().y() + 40, self.screenWidth - 300, 40))

        self.lblPartidoCandidato = QLabel(self.centralwidget)
        self.lblPartidoCandidato.setObjectName("lblPartidoCandidato")
        self.lblPartidoCandidato.setText("Partido")
        self.lblPartidoCandidato.setGeometry(QRect(250, self.comboCargoCandidato.pos().y() + 120, 200, 50))

        # nesse elemento será carregada a foto do candidato/simbolo do partido
        self.lblFotoPartido = QLabel(self.centralwidget)
        self.lblFotoPartido.setGeometry(QRect(100, self.lblPartidoCandidato.pos().y(), 100, 100))
        self.lblFotoPartido.setObjectName("lblFotoPartido")
        self.lblFotoPartido.setVisible(True)
        self.lblFotoPartido.setScaledContents(True)
        self.lblFotoPartido.setWordWrap(False)
        pixmap = QPixmap('../../files/icon.png')
        self.lblFotoPartido.setPixmap(pixmap)


        self.comboPartidoCandidato = QComboBox(self.centralwidget)
        partidos = database.getSiglas()
        self.comboPartidoCandidato.addItem('')
        for partido in partidos:
            self.comboPartidoCandidato.addItem(partido[0])
        self.comboPartidoCandidato.setGeometry(QRect(250, self.lblPartidoCandidato.pos().y() + 40, self.screenWidth - 300, 40))
        self.comboPartidoCandidato.activated[str].connect(self.alterarFotoPartido)

        self.btnCadastrar = QPushButton(self.centralwidget)
        self.btnCadastrar.setGeometry(QRect(self.screenWidth / 2 - 100, self.screenHeight - 100, 200, 50))
        self.btnCadastrar.setObjectName("btnCadastrar")
        self.btnCadastrar.clicked.connect(self.btnCadastrarClicked)
        self.btnCadastrar.setStyleSheet("QPushButton{\
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

    def alterarFotoPartido(self, text):
        foto = database.getFotoPartido(text)
        qimg = QImage.fromData(foto)
        pixmap = QPixmap.fromImage(qimg)
        self.lblFotoPartido.setPixmap(pixmap)


    def btnFotoClicked(self):
        fname = QFileDialog.getOpenFileName()
        pixmap = QPixmap(fname[0])
        self.lblFoto.setPixmap(pixmap)
        self.lblFotoName.setText(fname[0])

    # funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
    def btnCadastrarClicked(self):
        fin = open(self.lblFotoName.text())
        img = fin.read()
        idCargo = database.getCargoId(self.comboCargoCandidato.currentText())
        idPartido = database.getPartidoId(self.comboPartidoCandidato.currentText())
        database.inserirCandidato(idCargo, idPartido, self.txtNumeroCandidato.text(), self.txtNomeCandidato.text(), self.txtTituloCandidato.text(), img)
        pixmap = QPixmap('../../files/icon.png')
        self.lblFoto.setPixmap(pixmap)
        self.lblFotoName.setText("")
        self.txtTituloCandidato.setText("")
        self.txtNomeCandidato.setText("")
        self.txtNumeroCandidato.setText("")


def main():
    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySW.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    database = eleicoesDB.DAO()
    main()
