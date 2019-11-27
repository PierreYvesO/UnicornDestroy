class BalleEnnemi(Balle):
	def __init__(self, x, y, xVel, yVel, shotDown):
		super().__init__(x, y, xVel, yVel)
		self.shotDown = shotDown
		if not self.shotDown:
			self.sprites = [PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/AlienBullet1.gif"),
			PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/AlienBullet2.gif"),
			PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/AlienBullet3.gif")]
		elif random.random() < 0.05:
			self.sprites = [PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Coke Can.gif")]
		else:
			self.sprites = [PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Missile1.gif"),
			PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Missile2.gif")]
	def checkCollisions(self):
		if self.shotDown:
			for i in shots:
				if i.x + 15 >= self.x and i.x <= self.x + 15 and i.y + 25 >= self.y \
				and i.y <= self.y + 25:
					self.dead = True
					j.dead = True
					explosions.append(Mort(self.x + 7.5, self.y + 12.5))
