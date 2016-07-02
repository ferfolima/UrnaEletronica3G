# -*- coding: utf-8 -*-
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from Urna.urnadao import eleicoesDB


class incrementar():
    def __init__(self):
        database = eleicoesDB.DAO()
        self.cargos = [x[0] for x in database.getCargos()]
        self.lstVotoId = {}
        self.lista_cargos_votos = {}
        for cargo in self.cargos:
            self.lista_cargos_votos[cargo] = {}

    def incrementar(self, qrcode):
        cedula = qrcode[1:].split(';')
        votoId = cedula[len(cedula) - 1]
        if votoId not in self.lstVotoId:
            self.lstVotoId[votoId] = 1
            for indexCargos in range(len(self.cargos)):
                voto = cedula[indexCargos]
                if voto in self.lista_cargos_votos[self.cargos[indexCargos]]:
                    self.lista_cargos_votos[self.cargos[indexCargos]][voto] += 1
                elif voto is not '':
                    self.lista_cargos_votos[self.cargos[indexCargos]][voto] = 1


    def getVotos(self):
        return self.lista_cargos_votos


    def gerarBoletim(self):
        c = canvas.Canvas('../../files/boletim_de_urna.pdf')

        textobject = c.beginText()
        textobject.setTextOrigin(8 * cm, 28 * cm)
        text_label = 'BOLETIM DE URNA'
        textobject.textOut(text_label)

        linha = 0
        textobject.setTextOrigin(2 * cm, 26.5 * cm)
        for cargo in self.cargos:
            linha += 0.5
            text_label = "----------------------------------{0}---------------------------------------".format(cargo)
            textobject.setTextOrigin(2 * cm, (26 - linha) * cm)
            textobject.textOut(text_label)
            for i in self.lista_cargos_votos[cargo]:
                if i == '0':
                    text_label = "Votos Brancos: {0}".format(self.lista_cargos_votos[cargo][i])
                elif i == '-1':
                    text_label = "Votos Nulos: {0}".format(self.lista_cargos_votos[cargo][i])
                else:
                    text_label = "Votos Numero {0}: {1}".format(i, self.lista_cargos_votos[cargo][i])
                linha += 0.5
                textobject.setTextOrigin(2 * cm, (26 - linha) * cm)
                textobject.textOut(text_label)

        c.drawText(textobject)
        # c.drawImage('voto.png', 2*cm, 2*cm, 5*cm, 5*cm)
        # os.remove('voto.pdf')
        c.showPage()
        c.save()
