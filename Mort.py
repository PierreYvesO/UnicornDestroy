class Mort():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.sprites = [PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion1.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion2.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion3.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion4.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion5.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion4.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion3.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/Explosion3.gif")]
		self.timer = 0
	def draw(self):
		disp.create_image(self.x, self.y - 25,
		image=self.sprites[self.timer % len(self.sprites)],
		anchor=NW)
		self.timer += 1
		if self.timer >= len(self.sprites):
			self.dead = True
