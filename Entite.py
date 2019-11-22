from math import *

class Entite:

	def __init__(self,pv,vitesse,degats,nom,x,y,hauteur,largeur,couleur,arme,typeDeplacement=0):
		self.pv=pv
		self.vitesse=vitesse
		self.degats=degats
		self.nom=nom
		self.typeDeplacement=typeDeplacement
		self.x=x
		self.y=y
		self.arme=arme
		self.hauteur=hauteur
		self.largeur=largeur
		self.couleur=couleur

	def get_pv(self):
		return self.pv
	
	def get_vitesse(self):
		return self.vitesse

	def get_degats(self):
		return self.degats

	def get_nom(self):
		return self.nom
	
	def get_arme(self):
		return self.arme

	def get_typeDeplacement(self):
		return self.typeDeplacement
	
	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y

	def get_hauteur(self):
		return self.hauteur

	def get_largeur(self):
		return self.largeur

	def get_couleur(self):
		return self.couleur

	def set_pv(self,pv):
		self.pv=pv

	def set_vitesse(self,vitesse):
		self.vitesse=vitesse

	def set_degats(self,degats):
		self.degats=degats

	def set_nom(self,nom):
		self.nom=nom

	def set_typeDeplacement(self,typeDeplacement):
		self.typeDeplacement=typeDeplacement

	def set_arme(self,arme):
		self.arme=arme

	def set_x(self,x):
		self.x=x

	def set_y(self,y):
		self.y=y

	def attaquer(self,Entite):
		Entite.pv-=self.degats

	def deplacer(self,x,y):
		if(typeDeplacement==0):
			self.x=self.x+(x*self.vitesse)
		self.x=self.x+(x*self.vitesse)
		self.y=cos(self.x)

	def mourir(self):
		if(self.pv<=0):
			return True
		return False


