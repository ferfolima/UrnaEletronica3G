# -*- coding: utf-8 -*-
import h5py
from sets import Set


class Database:
    h5pyFile = h5py.File('Urna.h5', 'r')
    setupGeral = h5pyFile['Urna/SetupGeral']
    tipoDeCandidato = h5pyFile['Urna/TipoDeCandidato']
    candidatos = h5pyFile['Urna/Candidatos']
    perguntas = h5pyFile['Urna/Perguntas']
    partido = h5pyFile['PreEleicao/Partido']
    fotosCandidatos = h5pyFile['img_candidato']


    def getCargosEleicao(self):
        listIndexCargos = []
        listCargos = []

        for i in self.candidatos:
            if i[0] not in listIndexCargos:
                listIndexCargos.append(i[0])

        for j in range(len(self.tipoDeCandidato)):
            for i in listIndexCargos:
                if j == i and self.tipoDeCandidato[j][0] not in listCargos:
                    listCargos.append(self.tipoDeCandidato[j][0])

        return listCargos

    def getCargos(self):
        return [self.tipoDeCandidato[item][0] for item in range(len(self.tipoDeCandidato))]

    def getQtdeCargos(self):
        return len(Set([self.tipoDeCandidato[indiceCargo[0]][0] for indiceCargo in self.candidatos]))

    def getTipoCandidato(self):
        return self.tipoDeCandidato

    def getCandidatoNumeroPartido(self, numerosDigitados, cargo):
        NUMERO_PARTIDO_CANDIDATO = 1
        NUMERO_CANDIDATO = 2
        NOME_CANDIDATO = 3

        NUMERO_PARTIDO_PARTIDO = 1
        SIGLA_PARTIDO_PARTIDO = 2

        INDICE_CARGO_CANDIDATO = 0
        NOME_CARGO_TIPO_CANDIDATO = 0

        stringDigitos = ''
        for i in numerosDigitados:
            stringDigitos += str(i)

        nomeCandidato = None
        numeroCandidato = None
        numeroPartidoCandidato = None
        siglaPartido = None
        foto = None

        for candidato in self.candidatos:
            if stringDigitos == str(candidato[NUMERO_CANDIDATO]):
                strCargo = ''
                for indiceCargo in range(len(self.tipoDeCandidato)):
                    if indiceCargo == candidato[INDICE_CARGO_CANDIDATO]:
                        strCargo = self.tipoDeCandidato[indiceCargo][NOME_CARGO_TIPO_CANDIDATO]
                        break
                if cargo == str(strCargo):
                    nomeCandidato = candidato[NOME_CANDIDATO]
                    numeroCandidato = candidato[NUMERO_CANDIDATO]
                    numeroPartidoCandidato = candidato[NUMERO_PARTIDO_CANDIDATO]
                    foto = self.fotosCandidatos[cargo.lower().replace(' ', '_')][str(numeroCandidato)]
                    break

        if numeroPartidoCandidato is not None:
            for indexPartido in self.partido:
                if indexPartido[NUMERO_PARTIDO_PARTIDO] == numeroPartidoCandidato:
                    siglaPartido = indexPartido[SIGLA_PARTIDO_PARTIDO]

        return (str(nomeCandidato), str(siglaPartido), str(numeroCandidato), foto)
