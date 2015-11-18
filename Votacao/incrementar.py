from pyparsing import Word, nums, Combine, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
import os


class incrementar():
	def __init__(self):
		self.numero_candidato = Combine(Optional("-") + Optional(Word(nums)))
		self.protocolo = "#" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato + ";" + self.numero_candidato
		self.lista_presidente={}
		self.lista_governador={}
		self.lista_senador1={}
		self.lista_senador2={}
		self.lista_depfederal={}
		self.lista_depestadual={}
		self.lista_prefeito={}
		self.lista_vereador={}
		self.lista_id={}

	#qrcode = "#13;45;151;234;2222;45678;13;33664;152318"
	def incrementar(self, qrcode):
		cedula = self.protocolo.parseString(qrcode)
		votoId = cedula[17]
		if votoId not in self.lista_id:
			self.lista_id[votoId] = 1
			presidente=cedula[1]
			if presidente in self.lista_presidente:
				self.lista_presidente[presidente] += 1
			elif presidente is not '':
				self.lista_presidente[presidente] = 1
			governador=cedula[3]
			if governador in self.lista_governador:
				self.lista_governador[governador] += 1
			elif governador is not '':
				self.lista_governador[governador] = 1
			senador1=cedula[5]
			print senador1
			if senador1 in self.lista_senador1:
				self.lista_senador1[senador1] += 1
			elif senador1 is not '':
				self.lista_senador1[senador1] = 1
			senador2=cedula[7]
			if senador2 in self.lista_senador2:
				self.lista_senador2[senador2] += 1
			elif senador2 is not '':
				self.lista_senador2[senador2] = 1
			depfederal=cedula[9]
			if depfederal in self.lista_depfederal:
				self.lista_depfederal[depfederal] += 1
			elif depfederal is not '':
				self.lista_depfederal[depfederal] = 1
			depestadual=cedula[11]
			if depestadual in self.lista_depestadual:
				self.lista_depestadual[depestadual] += 1
			elif depestadual is not '':
				self.lista_depestadual[depestadual] = 1
			prefeito=cedula[13]
			if prefeito in self.lista_prefeito:
				self.lista_prefeito[prefeito] += 1
			elif prefeito is not '':
				self.lista_prefeito[prefeito] = 1
			vereador=cedula[15]
			if vereador in self.lista_vereador:
				self.lista_vereador[vereador] += 1
			elif vereador is not '':
				self.lista_vereador[vereador] = 1


	def getVotos(self):
		votos = {}
		if len(self.lista_presidente) > 0:
			votos['Presidente'] = self.lista_presidente
		if len(self.lista_governador) > 0:
			votos['Governador'] = self.lista_governador
		if len(self.lista_senador1) > 0:
			votos['Senador1'] = self.lista_senador1
		if len(self.lista_senador2) > 0:
			votos['Senador2'] = self.lista_senador2
		if len(self.lista_depfederal) > 0:
			votos['Deputado Federal'] = self.lista_depfederal
		if len(self.lista_depestadual) > 0:
			votos['Deputado Estadual'] = self.lista_depestadual
		if len(self.lista_prefeito) > 0:
			votos['Prefeito'] = self.lista_prefeito
		if len(self.lista_vereador) > 0:
			votos['Vereador'] = self.lista_vereador
		return votos

	def gerarBoletim(self):
		c = canvas.Canvas('boletim_de_urna.pdf')

		textobject = c.beginText()
		textobject.setTextOrigin(8*cm, 28*cm)
		text_label = 'BOLETIM DE URNA'
		textobject.textOut(text_label)

		if len(self.lista_presidente) > 0:
			text_label = '----------------------------------Presidente---------------------------------------'
			textobject.setTextOrigin(2*cm, 26.5*cm)
			textobject.textOut(text_label)

			linha = 0

			for i in self.lista_presidente:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_presidente[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_presidente[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_presidente[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '---------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_governador) > 0:
			text_label = '----------------------------------Governador-------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

			for i in self.lista_governador:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_governador[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_governador[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_governador[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '----------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_senador1) > 0:
			text_label = '----------------------------------Senador 1----------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)

			linha += 0.5

			for i in  self.lista_senador1:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_senador1[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_senador1[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_senador1[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '----------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_senador2) > 0:
			text_label = '----------------------------------Senador 2----------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)

			linha += 0.5

			for i in self.lista_senador2:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_senador2[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_senador2[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_senador2[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '----------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_depfederal) > 0:
			text_label = '-------------------------------Deputado Federal---------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)

			linha += 0.5

			for i in self.lista_depfederal:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_depfederal[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_depfederal[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_depfederal[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '----------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_depestadual) > 0:
			text_label = '--------------------------------Deputado Estadual-------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)

			linha += 0.5

			for i in self.lista_depestadual:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_depestadual[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_depestadual[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_depestadual[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '----------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_prefeito) > 0:
			text_label = '----------------------------------Prefeito--------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)

			linha += 0.5

			for i in self.lista_prefeito:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_prefeito[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_prefeito[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_prefeito[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

			text_label = '----------------------------------------------------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)
			linha += 0.5

		if len(self.lista_vereador) > 0:
			text_label = '----------------------------------Vereador------------------------------------------'
			textobject.setTextOrigin(2*cm, (26-linha)*cm)
			textobject.textOut(text_label)

			linha += 0.5

			for i in self.lista_vereador:
				if i=='0': text_label = 'Votos Brancos: %2.f' % (self.lista_vereador[i])
				elif i=='-1': text_label = 'Votos Nulos: %2.f' % (self.lista_vereador[i])
				else: text_label = 'Votos Numero %s: %2.f' % (i, self.lista_vereador[i])
				textobject.setTextOrigin(2*cm, (26-linha)*cm)
				textobject.textOut(text_label)
				linha += 0.5

		c.drawText(textobject)
		#c.drawImage('voto.png', 2*cm, 2*cm, 5*cm, 5*cm)
		#os.remove('voto.pdf')
		c.showPage()
		c.save()
