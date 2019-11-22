from Entite import *
from Heros import *
from Map import *
from pynput.keyboard Key, Listener

class Controleur():
	
	def __init__(mapp,ennemis,hero,difficulte):
		self.map=mapp
		self.ennemis=ennemis
		self.difficulte=difficulte

	def setListEnnemis(listeEnnemis):
		self.ennemis=listeEnnemis

	def getListeEnnemis():
		return ennemis

	def spawnHero():
		hero = Heros("joueur")
		return hero

	def spawnEnnemis():
		listeEnnemis=list()
		for i in range(100):
			listeEnnemis.append(Entite(10,1,10,"mechant",1920,540,10,10,"rouge",1))
		setListEnnemis(listeEnnemis)

	def deplacerEnnemis(self):
		for i in range(self.ennemis):
			self.ennemis[i].set_x(self.ennemis[i].get_x-self.ennemis[i].get_vitesse())
