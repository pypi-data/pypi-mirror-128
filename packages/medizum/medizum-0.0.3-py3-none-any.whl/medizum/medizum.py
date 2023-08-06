import pandas as pd
from PIL import Image
from random import randint, uniform
from datetime import date

class diz():

	def __init__(self):
		self.nomes_masc = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/nomes_masculinos.csv')
		self.nomes_fem = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/nomes_femininos.csv')
		self.produtos = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/produtos.csv')
		self.cidades = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/cidades.csv')
		self.estados = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/estados.csv')
		self.paises = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/paises.csv')
		self.signos = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/signos.csv')
		self.cores = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/cores.csv')
		self.meses = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/meses.csv')		
		self.dias = pd.read_csv('https://raw.githubusercontent.com/taotamat/medizum/master/medizum/dados/dias.csv')
		

	def sorteia(self, arq):
		i = randint(0, len(arq)-1)
		retorno = arq.loc[i]
		return retorno


	def nome(self, qnt=1, sexo=None, sobrenome=True):
		if sexo == None:

			retorno = self.nome( qnt=qnt, sexo=self.sexo(), sobrenome=sobrenome )

		else:

			nomes = []

			while(qnt > 0):

				if sexo == 'M':
					aux = self.sorteia(self.nomes_masc)
				else:
					aux = self.sorteia(self.nomes_fem)

				n = aux[0]

				if sobrenome == False:
					sem_sobre = n.split(' ')
					n = sem_sobre[0]

				nomes.append(n)

				qnt -= 1

			if len(nomes) == 1:
				retorno = nomes[0]
			else:
				retorno = nomes

		return retorno


	def sexo(self, qnt=1):
		lista = []
		
		while qnt > 0:
			i = randint(1,2)
			if i == 1:
				lista.append('M')
			else:
				lista.append('F')
			qnt -= 1
		
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista 

		return retorno


	def peso(self, qnt=1, minimo=15.0, maximo=100.0):
		p = []
		while qnt > 0:
			p.append( round( uniform(minimo, maximo), 2 ) )
			qnt -= 1
		if len(p) == 1:
			peso = p[0]
		else:
			peso = p
		return peso


	def pais(self, qnt=1):
		p = []
		while qnt > 0:
			aux = self.sorteia(self.paises)
			pais = aux[3]
			p.append( pais )
			qnt -= 1

		if len(p) == 1:
			retorno = p[0]
		else:
			retorno = p

		return retorno


	def validaUF(self, cod):
		# Retorna True se for válido.
		# Retorna False se não for válido.
		retorno = False
		for i in range( len(self.estados)-1 ):
			if self.estados.loc[i][1] == cod:
				retorno = True
		return retorno


	def estado(self, qnt=1, cod_uf=False):
		lista = []
		while qnt > 0:
			aux = self.sorteia(self.estados)

			if cod_uf == True:
				lista.append([ aux[0], aux[1] ])
			else:
				lista.append(aux[0])
			qnt -= 1
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno


	def uf(self, qnt=1):
		lista = []
		while qnt > 0:
			aux = self.sorteia(self.estados)
			lista.append(aux[1])
			qnt -= 1
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno


	def cidade(self, qnt=1, cod_uf=None):
		
		lista = []

		while qnt > 0:
			if cod_uf == None:
				aux = self.sorteia(self.cidades)
			else:
				if self.validaUF(cod_uf) == True:
					while True:
						aux = self.sorteia(self.cidades)
						if aux[0] == cod_uf:
							break
				else:
					lista.append('ERRO: CODIGO UF NÃO FOI ENCONTRADO!')
					break

			lista.append(aux[1])
			qnt -= 1
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def cpf(self, qnt=1):
		lista = []
		while qnt > 0:
			# 123.456.789-09
			c = ''
			for i in range(14):
				if i in [3, 7]:
					c = c + '.'
				elif i == 11:
					c = c + '-'
				else:
					c = c + str( randint(0,9) )

			lista.append(c)
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def cor(self, qnt=1, hexadecimal=False, rgb=False):
		lista = []
		while qnt > 0:
			cor = []

			aux = self.sorteia(self.cores)

			cor.append(aux[0])

			if hexadecimal == True:
				cor.append(aux[1])

			if rgb == True:
				cor.append( (aux[2], aux[3], aux[4]) )

			lista.append(cor)
			qnt -= 1

		if len(lista) == 1:
			if True in [hexadecimal, rgb]:
				retorno = lista[0]
			else:
				retorno = lista[0][0]
		else:
			retorno = lista		

		return retorno


	def buscaCOR(self, cor):
		ini = 0
		fim = len(self.cores) - 1
		trava = 0
		retorno = None
		while ini <= fim and trava == 0:
			
			meio = ini + (fim - ini)//2


			#print( f'self.cores.loc[meio][0].upper() = {self.cores.loc[meio][0].upper()}')
			#print( f'cor.upper() = {cor.upper()} \n' )

			if self.cores.loc[meio][0].upper() == cor.upper():
				aux = self.cores.loc[meio]
				retorno = [ aux[0], (aux[2], aux[3], aux[4]) ]
				trava = 1
			elif self.cores.loc[meio][0].upper() > cor.upper():
				fim = meio - 1
			elif self.cores.loc[meio][0].upper() < cor.upper():
				ini = meio + 1

		return retorno


	def imagem(self, qnt=1, cor=None, rgb=None, largura=500, altura=500):
		lista = []
		while qnt > 0:
			if rgb == None and cor == None:
				aux = self.cor(rgb=True)
				imagem = Image.new( "RGB", (largura, altura), aux[1])

			elif rgb == None and cor != None:
				aux = self.buscaCOR(cor)
				if aux != None:
					imagem = Image.new( "RGB", (largura, altura), aux[1])
				else:
					imagem = Image.new( "RGB", (largura, altura), 0)

			elif rgb != None and cor == None:
				imagem = Image.new( "RGB", (largura, altura), rgb)

			lista.append(imagem)
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
			#retorno.show()
		else:
			retorno = lista

		return retorno


	def idade(self, qnt=1, minimo=1, maximo=80, crianca=False, adolescente=False, adulto=False, idoso=False):
		lista = []
		while qnt > 0:
			if crianca == True:
				lista.append(randint(1, 12))
			elif adolescente == True:
				lista.append(randint(13, 18))
			elif adulto == True:
				lista.append(randint(18, 59))
			elif idoso == True:
				lista.append(randint(60, 100))
			else:
				lista.append(randint(minimo, maximo))
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def altura(self, qnt=1, minimo=0.5, maximo=1.90):
		lista = []
		while qnt > 0:
			lista.append( round( uniform(minimo, maximo), 2 ) )
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def email(self, qnt=1, nome=''):
		lista = []
		while qnt > 0:

			if nome == '':
				n = self.nome(sobrenome=False)
			else:
				n = nome

			e = (f'{n}{randint(0,9)}{randint(0,9)}{randint(0,9)}')

			i = randint(1,3)

			if i == 1:
				e = e + ('@gmail.com')
			elif i == 2:
				e = e + ('@hotmail.com')
			else:
				e = e + ('@outlook.com')

			lista.append(e)
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def sorteiaCONT(self, arq, linhas):
		for i in range(linhas):

			'''
			1 - nome completo
			2 - nome
			3 - idade
			4 - email
			5 - altura
			6 - cidade
			7 - estado
			8 - pais
			9 - cpf
			10 - cor
			'''

			op = randint(1, 10)

			if op == 1:
				arq.write(f'Nome Completo = {self.nome()}')
			elif op == 2:
				arq.write(f'Nome = {self.nome(sobrenome=False)}')
			elif op == 3:
				arq.write(f'Idade = {self.idade()} anos')
			elif op == 4:
				arq.write(f'Email = {self.email()}')
			elif op == 5:
				arq.write(f'Altura = {self.altura()} m')
			elif op == 6:
				arq.write(f'Cidade = {self.cidade()}')
			elif op == 7:
				arq.write(f'Estado = {self.estado()}')
			elif op == 8:
				arq.write(f'Pais = {self.pais()}')
			elif op == 9:
				arq.write(f'CPF = {self.cpf()}')
			else:
				arq.write(f'Cor = {self.cor()}')

			arq.write('\n')


	def arquivo(self, qnt=1, linhas=50):
		lista = []
		i = 0
		while qnt > 0:
			arq = open(f"arquivo{i}.txt", "w")
			arq = self.sorteiaCONT(arq, linhas)
			lista.append(arq)
			i += 1
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno
	

	def rg(self, qnt=1):
		lista = []
		while qnt > 0:
			c = ''
			for i in range(12):
				if i in [2, 6]:
					c = c + '.'
				elif i == 10:
					c = c + '-'
				elif i == 0:
					c = c + str(randint(1,9))
				else:
					c = c + str(randint(0,9))
			lista.append(c)
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno
	

	def senha(self, qnt=1, numeros = True, minu = True, maiu = True, special = True,maxi = 8):
		l = []
		n = "0123456789"
		mi = "abcdefghijklmnopqrstuvwxyz"
		ma = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		sp = "!@#$%&*()-+.,;?{[}]^><:"
		lista = ''
		if(numeros):
			lista = lista + n
		if(minu):
			lista = lista + mi
		if(maiu):
			lista = lista + ma
		if(special):
			lista = lista + sp
		mix = len(lista)
		while qnt > 0:
			c = ''
			for i in range(maxi):
				x = randint(0,mix-1)
				c = c + lista[x]
			l.append(c)
			qnt -= 1
		if len(lista) == 1:
			retorno = l[0]
		else:
			retorno = l
		return retorno
	

	def telefone(self, qnt=1):
		lista = []
		while qnt > 0:
			c = '89'
			for i in range(9):
				if i < 2:
					c = c + str(randint(8,9))
				else:
					c = c + str(randint(0,9))
			lista.append(c)
			qnt -= 1
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno
	

	def preco(self, qnt= 1,mini = 0.00,maxi = 1000.00):
		lista = []
		while qnt > 0:
			c = uniform(mini,maxi);
			lista.append(c)
			qnt -= 1
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno


	def qnt_dias_mes(self, mes):
		for i in range(len(self.meses)):
			if self.meses.loc[i][0] == mes:
				retorno = self.meses.loc[i][2]
		return retorno


	def dia(self, qnt=1, fds=True, util=True):
		lista = []
		while qnt > 0:

			if fds == True and util == True:
				aux = self.sorteia(self.dias)
			elif util == False:
				aux = []
				n = randint(1, 2)
				if n == 1: 
					aux.append('Domingo')
				else:
					aux.append('Sábado')

			else:
				while True:
					aux = self.sorteia(self.dias)
					if aux[0] != 'Domingo' and aux[0] != 'Sábado':
						break

			lista.append( aux[0] )
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def dia_mes(self, qnt=1, mes=None):

		lista = []

		while qnt > 0:

			if mes == None:
				aux = randint(1,31)
			else:
				aux = randint(1,self.qnt_dias_mes(mes)) # Sorteia sabendo a quantidade exata de dias de um determinado mês.

			lista.append(aux)
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def mes(self, qnt=1):
		lista = []
		while qnt > 0:
			aux = self.sorteia(self.meses)
			lista.append(aux[1])
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def signo(self, qnt=1):
		lista = []
		while qnt > 0:
			aux = self.sorteia(self.signos)
			lista.append(aux[0])
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def data_nascimento(self, qnt=1, crianca=False, adolescente=False, adulto=False, idoso=False, idade=None):
		lista = []
		while qnt > 0:

			if idade != None:
				anos = idade
			elif crianca == True:
				anos = self.idade(crianca=True)
			elif adolescente == True:
				anos = self.idade(adolescente=True)
			elif adulto == True:
				anos = self.idade(adulto=True)
			elif idoso == True:
				anos = self.idade(idoso=True)
			else:
				anos = self.idade()

			aux = str(date.today()).split('-') # Devolve uma lista com ano, mes e dia de hoje.

			ano = int(aux[0]) - anos
			mes = randint(1,12)
			dia = self.dia_mes(mes=mes)

			lista.append(f'{ano}-{mes}-{dia}')
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista

		return retorno


	def produto(self, qnt=1):
		lista = []
		while qnt > 0:
			aux = self.sorteia(self.produtos)
			lista.append(aux[0])
			qnt -= 1
		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno


	def cep(self,qnt=1):
		lista = []
		while qnt > 0:
			c = ''
			for i in range(9):
				if i in [5]:
					c = c + '-'
				elif i == 0:
					c = c + str(randint(1,9))
				else:
					c = c + str(randint(0,9))
			lista.append(c)
			qnt -= 1

		if len(lista) == 1:
			retorno = lista[0]
		else:
			retorno = lista
		return retorno








