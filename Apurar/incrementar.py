#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

import eleicoesDB

script_dir = os.path.dirname(__file__)
BOLETIM_PDF = os.path.join(script_dir, "../files/boletim_de_urna.pdf")
BOLETIM_CSV = os.path.join(script_dir, "../files/boletim_de_urna.csv")

class incrementar():
    def __init__(self):
        database = eleicoesDB.DAO()
        self.cargos = database.getCargos()
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
        c = canvas.Canvas(BOLETIM_PDF)

        c.setPageSize((6.2*cm,10*cm))

        textobject = c.beginText()
        textobject.setTextOrigin(0.3 * cm, 9.5 * cm)
        textobject.setFont("Courier",8)
        text_label = 'BOLETIM DE URNA'
        textobject.textOut(text_label)

        linha = 0
        textobject.setTextOrigin(0.3 * cm, 9.5 * cm)
        for cargo in self.cargos:
            linha += 0.3
            text_label = "-".join(["" for i in range(18 - int(len(cargo) / 2))])
            text_label += cargo
            text_label += "-".join(["" for i in range(18 - int(len(cargo) / 2))])
            textobject.setTextOrigin(0.3 * cm, (9.5 - linha) * cm)
            textobject.textOut(text_label)
            for i in self.lista_cargos_votos[cargo]:
                if i == '0':
                    text_label = "Votos Branco: {0}".format(self.lista_cargos_votos[cargo][i])
                elif i == '-1':
                    text_label = "Votos Nulo: {0}".format(self.lista_cargos_votos[cargo][i])
                else:
                    text_label = "Votos {0}: {1}".format(i, self.lista_cargos_votos[cargo][i])
                linha += 0.3
                textobject.setTextOrigin(0.3 * cm, (9.5 - linha) * cm)
                textobject.textOut(text_label)

        c.drawText(textobject)
        # c.drawImage('voto.png', 2*cm, 2*cm, 5*cm, 5*cm)
        # os.remove('voto.pdf')
        c.showPage()
        c.save()

    def exportarCSV(self):
        stringCsv = "Cargo,Voto,Qtde\n"
        for key in self.lista_cargos_votos:
            for k in self.lista_cargos_votos[key]:
                stringCsv  += "{0},{1},{2}\n".format(key, k, self.lista_cargos_votos[key][k])
        outfile = open(BOLETIM_CSV, 'w')
        outfile.write(stringCsv)
        outfile.close()
