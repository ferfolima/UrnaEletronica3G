# -*- coding: utf-8 -*-
"""
Criado em 31 Out 2014
Modificado em 07 Nov de 2014
	   por Fernando Teodoro de Lima

@author: Fernando Teodoro de Lima
	 Paulo Tofanello
	 Thainara Miyashiro
"""

"""
Metodos: 
tipoEntrada
    	Analise se é a entrada é um comando ou um número 
	Retorna tipo de entrada
	Variaveis: entrada

candidato
	Analisa se o numero entrada pertence a um candidato
	Retorna Nome do candidato ou string vazia
    	Variaveis: entrada - É o numero do candidato

legenda
	Analisa se o numero entrada pertence a um partido
	Retorna Nome do partido ou string vazia
    	Variaveis: entrada - É o numero do partido

"""
from math import *
import numpy
import h5py
import random

#Nome, Partido, Numero, Cargo, Legenda
arrayUrna = ['2014','01','SP','Osasco','1234','1324','4321']

matrizCandidatos = [	['Fernando', 'PdE', '23', 'Presidente', '23'],
			['Aecio', 'PSDB', '45', 'Presidente', '45'],
		  	['Dilma', 'PT', '13', 'Presidente', '13'],
			['Tiririca', 'PdR', '2222', 'Deputado Federal', '22'],
		  	['Eduardo Suplicy', 'PT', '131', 'Senador', '13']]

cargos2Dig = ['Governador', 'Presidente', 'Prefeito']
cargos3Dig = ['Senador']
cargos4Dig = ['Deputado Federal']
cargos5Dig = ['Deputado Estadual', 'Vereador']
cargosLegenda = ['Deputado Federal', 'Deputado Estadual', 'Vereador']

def tipoEntrada(entrada):
	if isinstance(entrada, str):
		if entrada == '&branco':
			return 'branco'
		elif entrada == '&corrige':
			return 'corrige'
		elif entrada == '&confirma':
			return 'confirma'
	elif isinstance(entrada, (int, float, long)):	
		return entrada
	else:
		return 'incorreto'

def legenda(digitos):
	stringDigitos = ''
	for i in digitos[:2]:
		stringDigitos += str(i)
	for i in matrizCandidatos:
		if stringDigitos == i[4]:
			return i[1]
	return -1

def candidato(entrada):
	stringDigitos = ''
	for i in digitos:
		stringDigitos += str(i)
	for i in matrizCandidatos:
		if stringDigitos == i[2]:
			return i[0]
	return -1

def gerarString(votos):
	print 'Imprimindo voto'
	stringQRCode = ''
	rng = random.SystemRandom()
	ids = [i for i in range(2000)]
	id_voto = ids[rng.randint(0, len(ids))]
	ids.remove(id_voto)
	stringQRCode += 'ID.' 			+ str(id_voto) + ','
	stringQRCode += 'ANO.' 			+ str(arrayUrna[0]) + ','
	stringQRCode += 'TURNO.' 		+ str(arrayUrna[1]) + ','
	stringQRCode += 'UF.' 			+ str(arrayUrna[2]) + ','
	stringQRCode += 'MUNICIPIO.' 		+ str(arrayUrna[3]) + ','
	stringQRCode += 'ZONA ELEITORAL.' 	+ str(arrayUrna[4]) + ','
	stringQRCode += 'LOCAL VOTACAO.' 	+ str(arrayUrna[5]) + ','
	stringQRCode += 'SECAO ELEITORAL.' 	+ str(arrayUrna[6]) + '|'	
	for voto in votos:
		stringQRCode += 		str(voto[0]) + ':'
		stringQRCode += 'BRANCO.' + 	str(voto[1]) + ','
		stringQRCode += 'NULO.' + 	str(voto[2]) + ','
		stringQRCode += 'LEGENDA.' + 	str(voto[3]) + ','
		stringQRCode += 'NUMERO.' + 	str(voto[4]) + ';'
	stringQRCode = stringQRCode.upper()
	print stringQRCode 

cargos = []
for i in matrizCandidatos:
	if i[3] not in cargos:
		cargos.append(i[3])
votos = []
while len(cargos) > 0:
	confirmaVoto = False
	cargoVotado = []

	for string in cargos:
		print string

	cargo = input('Insira cargo para o qual deseja votar\n')
	cargoVotado.append(cargo)

	digitos = numpy.zeros((2,), dtype=numpy.int)
	if cargo in cargos3Dig:
		digitos = numpy.zeros((3,), dtype=numpy.int)
	elif cargo in cargos4Dig:
		digitos = numpy.zeros((4,), dtype=numpy.int)
	elif cargo in cargos5Dig:
		digitos = numpy.zeros((5,), dtype=numpy.int)

	digitos[:] = -1
	numeroDigitos = len(digitos)

	contadorDigitos = 0
	while contadorDigitos < numeroDigitos or not confirmaVoto:
		nulo = True
		leg = False

		print digitos[:contadorDigitos]

		if contadorDigitos == numeroDigitos:
			if candidato(digitos) == -1:
				nulo = True
				leg = False
			else:
				nulo = False
				leg = False
				print candidato(digitos)
		if cargo in cargosLegenda and contadorDigitos == 2:
			if legenda(digitos) == -1:
				nulo = True
				leg = False
			else:
				nulo = False
				leg = True
			print legenda(digitos)

		entrada = input("Aguardando entrada\n")
		tipoEntradaStr = tipoEntrada(entrada)	
	
		if tipoEntradaStr == 'branco':
			cargoVotado.append(1)		#branco
			cargoVotado.append(0)		#nulo 
			cargoVotado.append(0)		#legenda
			cargoVotado.append(digitos)	#numero
			contadorDigitos = numeroDigitos
			confirmaVoto = True
		elif tipoEntradaStr == 'confirma':
			cargoVotado.append(0)							#branco
			cargoVotado.append(1) if nulo == True else cargoVotado.append(0)	#nulo 
			cargoVotado.append(1) if leg == True  else cargoVotado.append(0) 	#legenda
			cargoVotado.append(digitos)						#numero
			contadorDigitos = numeroDigitos
			confirmaVoto = True
		elif tipoEntradaStr == 'corrige':
			digitos[:] = -1
			contadorDigitos = 0
		elif tipoEntradaStr == 'incorreto':
			print tipoEntradaStr
		else: #caso o usuario esteja entrando com numeros
			if contadorDigitos < numeroDigitos:
				digitos[contadorDigitos] = entrada
				contadorDigitos += 1
	votos.append(cargoVotado)
	cargos.remove(cargo)
gerarString(votos)
