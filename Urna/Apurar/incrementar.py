#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pyaudio
import subprocess
import sys
import wave
from os import path
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from ..DB import eleicoesDB

script_dir = os.path.dirname(__file__)
BOLETIM_PDF = os.path.join(script_dir, "../files/boletim_de_urna.pdf")
BOLETIM_CSV = os.path.join(script_dir, "../files/boletim_de_urna.csv")
BEEP = os.path.join(script_dir, "../files/beep_urna.wav")
FIM = os.path.join(script_dir, "../files/fim_urna.wav")

class incrementar():
    def __init__(self):
        database = eleicoesDB.DAO()
        self.cargos = database.getCargosQtde()
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
            som(self, 1)
        else:
            som(self, 2)


    def getVotos(self):
        return self.lista_cargos_votos


    def gerarBoletim(self):
        c = canvas.Canvas(BOLETIM_PDF)

        c.setPageSize((6.2 * cm, 10 * cm))

        textobject = c.beginText()
        textobject.setTextOrigin(0.3 * cm, 9.5 * cm)
        textobject.setFont("Courier", 8)
        text_label = 'BOLETIM DE URNA'
        textobject.textOut(text_label)

        linha = 0
        textobject.setTextOrigin(0.3 * cm, 9.5 * cm)

        for key in self.lista_cargos_votos:
            linha += 0.3
            textobject.setTextOrigin(0.3 * cm, (9.5 - linha) * cm)
            text_label = "-".join(["" for i in range(18 - int(len(key) / 2))])
            text_label += key
            text_label += "-".join(["" for i in range(18 - int(len(key) / 2))])
            textobject.textOut(text_label)
            for k in self.lista_cargos_votos[key]:
                if k == '0':
                    text_label = "Votos Branco: {0}".format(self.lista_cargos_votos[key][k])
                elif k == '-1':
                    text_label = "Votos Nulo: {0}".format(self.lista_cargos_votos[key][k])
                else:
                    text_label = "Votos {0}: {1}".format(k, self.lista_cargos_votos[key][k])
                linha += 0.3
                textobject.setTextOrigin(0.3 * cm, (9.5 - linha) * cm)
                textobject.textOut(text_label)
        c.drawText(textobject)
        c.showPage()
        c.save()
        # subprocess.Popen("lpr -P QL-700 -o PageSize=62x100 '{0}'".format(BOLETIM_PDF), shell=True)
        subprocess.Popen("lp '{0}'".format(BOLETIM_PDF), shell=True)
        subprocess.Popen("rm '{0}'".format(BOLETIM_PDF), shell=True)


    def exportarCSV(self):
        stringCsv = "Cargo,Voto,Qtde\n"
        for key in self.lista_cargos_votos:
            for k in self.lista_cargos_votos[key]:
                stringCsv  += "{0},{1},{2}\n".format(key, k, self.lista_cargos_votos[key][k])
        outfile = open(BOLETIM_CSV, 'w')
        outfile.write(stringCsv)
        outfile.close()

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