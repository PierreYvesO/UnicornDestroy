from Heros import *
from Map import *
class Map:
	def __init__(self,nbEnnemis):
		self.initEnnemis(nbEnnemis)
		self.heros = Entite()
		




	def initEnnemis(self,nb):
		self.listEnnemis = list()
		for i in range(nb):
			self.listEnnemis.append(Entite())
		
		

map = Map(10)
print(map.listEnnemis)
