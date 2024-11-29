#-*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *

pygame.init()
visor = pygame.display.set_mode((560,560))
pygame.display.set_caption("ajedrez")

casilla=[0,0,70,140,210,280,350,420,490,560,999]

ocupadas=[
[0,0,0,0,0,0,0,0,0],#esta linia y el 0 de mas es para kitar el 0 de los indices
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]
cocupadas=[#color de las ocupadas
[0,0,0,0,0,0,0,0,0],#esta linia y el 0 de mas es para kitar el 0 de los indices
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]

class metapieza():
	def __init__(self,x,y,color):
		self.movida = 0
		self.casx=x
		self.casy=y
		self.pos=(casilla[x],casilla[y])
		self.color=color
		self.casposibles=[]
		if self.casx < 9 and self.casy < 9:
			ocupadas[self.casy][self.casx] = self
			cocupadas[self.casy][self.casx] = self.color
	def cambiasilla(self,x,y):
		ocupadas[self.casy][self.casx]=cocupadas[self.casy][self.casx] = 0
		self.__init__(x,y)
		self.movida = 1
	def casillaocupada(self):
		return self.casy,self.casx
	def movlineal(self,movmax=8):
		casi = 0
		oriz = ordr = vrab = vrar = True
		while casi < movmax:
			casi+=1
			if 0 < self.casy <= 8 and 0 < self.casx-casi <= 8 and oriz:
				oriz = cocupadas[self.casy][self.casx-casi] != self.color
				if oriz:
					self.casposibles.append((self.casx-casi,self.casy))
					oriz = cocupadas[self.casy][self.casx-casi] != 3-self.color
			if 0 < self.casy <= 8 and 0 < self.casx+casi <= 8 and ordr:
				ordr = cocupadas[self.casy][self.casx+casi] != self.color
				if ordr:
					self.casposibles.append((self.casx+casi,self.casy))
					ordr = cocupadas[self.casy][self.casx+casi] != 3-self.color				
			if 0 < self.casy-casi <= 8 and 0 < self.casx <= 8 and vrab:		
				vrab = cocupadas[self.casy-casi][self.casx] != self.color
				if vrab:
					self.casposibles.append((self.casx,self.casy-casi))
					vrab = cocupadas[self.casy-casi][self.casx] != 3-self.color
			if 0 < self.casy+casi <= 8 and 0 < self.casx <= 8 and vrar:		
				vrar = cocupadas[self.casy+casi][self.casx] != self.color
				if vrar:
					self.casposibles.append((self.casx,self.casy+casi))
					vrar = cocupadas[self.casy+casi][self.casx] != 3-self.color
		return self.casposibles
		
	def movdiagonal(self,movmax=8):
		casi = 0
		ariz = abdr = ardr = abiz = True
		while casi < movmax:
			casi+=1
			if 0 < self.casy-casi <= 8 and 0 < self.casx-casi <= 8 and ariz:		
				ariz = cocupadas[self.casy-casi][self.casx-casi] != self.color
				if ariz:
					self.casposibles.append((self.casx-casi,self.casy-casi))
					ariz = cocupadas[self.casy-casi][self.casx-casi] != 3-self.color
			if 0 < self.casy+casi <= 8 and 0 < self.casx+casi <= 8 and abdr:		
				abdr = cocupadas[self.casy+casi][self.casx+casi] != self.color
				if abdr:
					self.casposibles.append((self.casx+casi,self.casy+casi))
					abdr = cocupadas[self.casy+casi][self.casx+casi] != 3-self.color
			if 0 < self.casy-casi <= 8 and 0 < self.casx+casi <= 8 and ardr:		
				ardr = cocupadas[self.casy-casi][self.casx+casi] != self.color
				if ardr:
					self.casposibles.append((self.casx+casi,self.casy-casi))
					ardr = cocupadas[self.casy-casi][self.casx+casi] != 3-self.color
			if 0 < self.casy+casi <= 8 and 0 < self.casx-casi <= 8 and abiz:		
				abiz = cocupadas[self.casy+casi][self.casx-casi] != self.color
				if abiz:
					self.casposibles.append((self.casx-casi,self.casy+casi))
					abiz = cocupadas[self.casy+casi][self.casx-casi] != 3-self.color
		return self.casposibles

class metaballo(metapieza):
	def movcaballo(self):
		for x in [-2,-1,1,2]:
			for y in [-(3-abs(x)),3-abs(x)]:
				if 0 < self.casy+y <= 8 and 0 < self.casx+x <= 8:
					if cocupadas[self.casy+y][self.casx+x] == 0 or \
					cocupadas[self.casy+y][self.casx+x] == 3-self.color:
						self.casposibles.append((self.casx+x,self.casy+y))
		return self.casposibles

class metapeon(metapieza):
	def movpeon(self):
		lpeon=[0,-1,1,5,4]
		if 0 < self.casy+lpeon[self.color] <= 8 and 0 < self.casx <= 8:
			if cocupadas[self.casy+lpeon[self.color]][self.casx] == 0:	
				self.casposibles.append((self.casx,self.casy+lpeon[self.color]))
				if self.movida == 0 and cocupadas[lpeon[self.color+2]][self.casx] == 0:
					self.casposibles.append((self.casx,lpeon[self.color+2]))
		if 0 < self.casy+lpeon[self.color] <= 8 and 0 < self.casx+1 <= 8:
			if cocupadas[self.casy+lpeon[self.color]][self.casx+1] == 3-self.color:
				self.casposibles.append((self.casx+1,self.casy+lpeon[self.color]))
		if 0 < self.casy+lpeon[self.color] <= 8 and 0 < self.casx-1 <= 8:
			if cocupadas[self.casy+lpeon[self.color]][self.casx-1] == 3-self.color:
				self.casposibles.append((self.casx-1,self.casy+lpeon[self.color]))
		return self.casposibles

enroke = 0
class metarey(metapieza):
	def movrey(self):
		posimov=[]
		posimov+=metapieza.movlineal(self,1)
		posimov+=metapieza.movdiagonal(self,1)
		global enroke
		if self.movida == 0:
			if (torrenegra[2].movida == 0 or torreblanca[2].movida == 0) and \
			cocupadas[self.casy][self.casx+2] == 0 and cocupadas[self.casy][self.casx+1] == 0:
				self.casposibles.append((self.casx+2,self.casy))
				enroke = 1
			if (torrenegra[1].movida == 0 or torreblanca[1].movida == 0) and \
			cocupadas[self.casy][self.casx-3] == 0 and cocupadas[self.casy][self.casx-2] == 0 \
			and cocupadas[self.casy][self.casx-1] == 0:
				self.casposibles.append((self.casx-2,self.casy))
				enroke = 2
			posimov+=self.casposibles
		return posimov
		
class Peonegro(metapeon):
	def __init__(self,x,y=2):
		self.foto = pygame.image.load('peonegro.png')
		metapieza.__init__(self,x,y,2)
	def puedemovera(self):
		return metapeon.movpeon(self)

class Peonblanco(metapeon):
	def __init__(self,x,y=7):
		self.foto = pygame.image.load('peonblanco.png')
		metapieza.__init__(self,x,y,1)
	def puedemovera(self):
		return metapeon.movpeon(self)

class Caballonegro(metaballo):
	def __init__(self,x,y=1):
		self.foto = pygame.image.load('caballonegro.png')
		metapieza.__init__(self,x,y,2)
	def puedemovera(self):
		return metaballo.movcaballo(self)

class Caballoblanco(metaballo):
	def __init__(self,x,y=8):
		self.foto = pygame.image.load('caballoblanco.png')
		metapieza.__init__(self,x,y,1)
	def puedemovera(self):
		return metaballo.movcaballo(self)

class Torrenegra(metapieza):
	def __init__(self,x,y=1):
		self.foto = pygame.image.load('torrenegra.png')
		metapieza.__init__(self,x,y,2)
	def puedemovera(self):
		return metapieza.movlineal(self)			

class Torreblanca(metapieza):
	def __init__(self,x,y=8):
		self.foto = pygame.image.load('torreblanca.png')
		metapieza.__init__(self,x,y,1)
	def puedemovera(self):
		return metapieza.movlineal(self)	

class Alfilnegro(metapieza):
	def __init__(self,x,y=1):
		self.foto = pygame.image.load('alfilnegro.png')
		metapieza.__init__(self,x,y,2)
	def puedemovera(self):
		return metapieza.movdiagonal(self)	

class Alfilblanco(metapieza):
	def __init__(self,x,y=8):
		self.foto = pygame.image.load('alfilblanco.png')
		metapieza.__init__(self,x,y,1)
	def puedemovera(self):
		return metapieza.movdiagonal(self)
		
class Reynegro(metarey):
	def __init__(self,x=5,y=1):
		self.foto = pygame.image.load('reynegro.png')
		metapieza.__init__(self,x,y,2)
	def puedemovera(self):
		return metarey.movrey(self)

class Reyblanco(metarey):
	def __init__(self,x=5,y=8):
		self.foto = pygame.image.load('reyblanco.png')
		metapieza.__init__(self,x,y,1)
	def puedemovera(self):
		return metarey.movrey(self)

class Reinanegra(metapieza):
	def __init__(self,x=4,y=1):
		self.foto = pygame.image.load('reinanegra.png')
		metapieza.__init__(self,x,y,2)
	def puedemovera(self):
		posimov=[]
		posimov+=metapieza.movlineal(self)
		posimov+=metapieza.movdiagonal(self)
		return posimov

class Reinablanca(metapieza):
	def __init__(self,x=4,y=8):
		self.foto = pygame.image.load('reinablanca.png')
		metapieza.__init__(self,x,y,1)
	def puedemovera(self):
		posimov=[]
		posimov+=metapieza.movlineal(self)
		posimov+=metapieza.movdiagonal(self)
		return posimov

def comepieza(pieza):
	pieza.cambiasilla(9,9)

def	sacapieza(casx,casy):
	return ocupadas[casy][casx]
		
def sacasilla(posraton):
	for i in range(9):
		if casilla[i] < posraton[0] <= casilla[i+1]:
			x = i
		if casilla[i] < posraton[1] <= casilla[i+1]:
			y = i
	return x,y

ud7 = [0,2,7]

tablero = pygame.image.load('tablero-ajedrez.png')			
puntoazul = pygame.image.load('puntoazul.png')
gblancas = pygame.image.load('gblancas.png')
gnegras = pygame.image.load('gnegras.png')

peonegro = [0]
peonblanco = [0]
caballonegro = [0]
caballoblanco = [0]
torrenegra = [0]
torreblanca = [0]
alfilnegro = [0]
alfilblanco = [0]

for p in range(1,9):#1-8
	peonegro.append(Peonegro(p))
	peonblanco.append(Peonblanco(p))

for c in (1,2):
	caballonegro.append(Caballonegro(ud7[c]))
	caballoblanco.append(Caballoblanco(ud7[c]))
	torrenegra.append(Torrenegra(pow(c,3)))
	torreblanca.append(Torreblanca(pow(c,3)))
	alfilnegro.append(Alfilnegro(c*3))
	alfilblanco.append(Alfilblanco(c*3))

reynegro = Reynegro()
reyblanco = Reyblanco()

reinanegra = Reinanegra()
reinablanca = Reinablanca()

click=[]

fichamover=""
turno="blancas"
print ("empiezan las blancas")

while True:
	for evento in pygame.event.get():
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()
		if evento.type == MOUSEBUTTONDOWN:
			click.append(pygame.mouse.get_pos())

	visor.blit(tablero,(0,0))

	if len(click) == 1:#primer click
		posraton = click[0]
		casillax,casillay=sacasilla(posraton)
		fichamover=sacapieza(casillax,casillay)
		if (fichamover == 0) or (fichamover.color == 1 and turno == "negras") \
		or (fichamover.color == 2 and turno == "blancas"):
			fichamover=""#anula movimientos del otro turno
		else:
			posimov = fichamover.puedemovera()
		if fichamover=="":
			click=[]

	if len(click) == 2:#segundo click
		posraton = click[1]
		nuevacasillax,nuevacasillay = sacasilla(posraton)
		if (nuevacasillax,nuevacasillay) in posimov:
			if ocupadas[nuevacasillay][nuevacasillax] != 0:
				comepieza(sacapieza(nuevacasillax,nuevacasillay))
			fichamover.cambiasilla(nuevacasillax,nuevacasillay)
			if fichamover == reynegro or fichamover == reyblanco:
				if fichamover == reynegro:
					if enroke == 1 and (nuevacasillax,nuevacasillay) == (7,1):
						torrenegra[2].cambiasilla(6,1)
					if enroke == 2 and (nuevacasillax,nuevacasillay) == (3,1):
						torrenegra[1].cambiasilla(4,1)
				if fichamover == reyblanco:
					if enroke == 1 and (nuevacasillax,nuevacasillay) == (7,8):
						torreblanca[2].cambiasilla(6,8)
					if enroke == 2 and (nuevacasillax,nuevacasillay) == (3,8):
						torreblanca[1].cambiasilla(4,8)
				enroke = 0
			if fichamover.color == 1:
				turno = "negras"
			else:
				turno = "blancas"

	#refrescos y representaciones
	if reynegro.casx < 9 and reyblanco.casx < 9:
		for d in range(1,9):
			visor.blit(peonblanco[d].foto,peonblanco[d].pos)
			visor.blit(peonegro[d].foto,peonegro[d].pos)
			
		for e in (1,2):
			visor.blit(torrenegra[e].foto,torrenegra[e].pos)
			visor.blit(torreblanca[e].foto,torreblanca[e].pos)
			
			visor.blit(alfilnegro[e].foto,alfilnegro[e].pos)
			visor.blit(alfilblanco[e].foto,alfilblanco[e].pos)
			
			visor.blit(caballoblanco[e].foto,caballoblanco[e].pos)
			visor.blit(caballonegro[e].foto,caballonegro[e].pos)
		
		visor.blit(reynegro.foto,reynegro.pos)
		visor.blit(reyblanco.foto,reyblanco.pos)
		
		visor.blit(reinanegra.foto,reinanegra.pos)
		visor.blit(reinablanca.foto,reinablanca.pos)
	
	if len(click) > 1:
		click=[]
		fichamover=""
	if len(click) > 0:
		for pos in posimov:
			visor.blit(puntoazul,(casilla[pos[0]],casilla[pos[1]]))
	
	if reynegro.casx > 8:
		visor.blit(gblancas,(0,0))
	elif reyblanco.casx > 8:
		visor.blit(gnegras,(0,0))

	pygame.display.update()
	
	pygame.time.wait(20)#limita a 50 fps para ahorrar cpu
