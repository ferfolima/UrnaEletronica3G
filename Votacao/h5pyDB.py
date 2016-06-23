# -*- coding: utf-8 -*-
import h5py
from sets import Set

class Database:
    h5pyFile = h5py.File('Urna.h5', 'r')
    setupGeral = h5pyFile['Urna/SetupGeral']
    tipoDeCandidato = h5pyFile['Urna/TipoDeCandidato']
    candidatos = h5pyFile['Urna/Candidatos']
    perguntas = h5pyFile['Urna/Perguntas']

    def getCargosEleicao(self):
        listIndexCargos = []
    	listCargos = []
        tipoEleicao = self.setupGeral[0][8]

    	#caso eleicoes
    	if tipoEleicao == '1':
    		for i in self.candidatos:
    			if i[0] not in listIndexCargos:
    				listIndexCargos.append(i[0])

    		for j in range(len(self.tipoDeCandidato)):
    			for i in listIndexCargos:
    				if j == i and self.tipoDeCandidato[j][0] not in listCargos:
    					listCargos.append(self.tipoDeCandidato[j][0])

    	#caso plebiscito
    	# elif tipoEleicao == '0':
    	# 	indexPergunta = 1
    	# 	for i in perguntas:
    	# 		if len(i[0]) > 0:
    	# 			listCargos.append(i[0])
    	# 			indexPergunta += 1

        return listCargos

    def getCargos(self):
        return [self.tipoDeCandidato[item][0] for item in range(len(self.tipoDeCandidato))]

    def getQtdeCargos(self):
        return len(Set([self.tipoDeCandidato[indiceCargo[0]][0] for indiceCargo in self.candidatos]))
