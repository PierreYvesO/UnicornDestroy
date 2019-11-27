class player():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.sprites = [PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ship1.gif"),
				PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ship2.gif")]
		self.timer = 0
		self.tPeriod = 0
		self.period = 3
		self.left = False
		self.right = False
		self.hp = 3
		self.autofire = False
		disp.bind("<Left>", self.moveLeft)
		disp.bind("<Right>", self.moveRight)
		disp.bind("<KeyRelease-Left>", self.stopLeft)
		disp.bind("<KeyRelease-Right>", self.stopRight)
		disp.bind("<KeyRelease-space>", self.spawnBullet)
		disp.bind("<KeyRelease-Shift_L>", self.toggleAutoFire)
	def draw(self):
		disp.create_image(self.x, self.y,
		image=self.sprites[self.tPeriod],
		anchor=NW)
		self.timer += 1
		self.timer %= self.period
		if self.timer == 0:
			self.tPeriod += 1
			self.tPeriod %= len(self.sprites)
			disp.create_text(self.x + 25, self.y - 20, text="HP: " + str(self.hp),
			fill="white", font=otherFont)
	def update(self):
		global dead
		if self.hp > 0:
			if self.left and self.x >= 0:
				self.x -= 10
			if self.x < 0:
				self.x = 0
			if self.right and self.x + 50 <= disp.winfo_width():
				self.x += 10
			if self.x + 50 > disp.winfo_width():
				self.x = disp.winfo_width() - 50
				self.draw()
			if self.tPeriod == 1 and self.timer == 1 and self.autofire:
				self.spawnBullet(False)
		else:
			dead = True
			for i in aliens:
				if i.x + 50 >= self.x and i.x <= self.x + 50 and i.y + 50 >= self.y \
				and i.y <= self.y + 50:
					self.hp = -1
			for j in enemyProjectiles:
				if j.x + 15 >= self.x and j.x <= self.x + 50 and j.y + 25 >= self.y \
				and j.y <= self.y + 50:
					self.hp -= 1
					j.dead = True
				if self.hp > 0:
					j.yVel *= -1.25
					j.y -= 50
				if self.hp > -1:
					explosions.append(Mort(j.x + 7.5, self.y))
	def moveLeft(self, event):
		self.left = True
	def moveRight(self, event):
		self.right = True
	def stopLeft(self, event):
		self.left = False
	def stopRight(self, event):
		self.right = False
	def spawnBullet(self, event):
		if self.hp > 0:
			global shots
			shots.append(bullet(self.x + 25, self.y, 0, -20))
		if opAttack:
			shots.append(bullet(self.x + 25, self.y, -3, -20))
			shots.append(bullet(self.x + 25, self.y, 3, -20))
		if otherOPAttack:
			shots.append(bullet(self.x + 25, self.y + 25, 0, -20))
			shots.append(bullet(self.x + 25, self.y - 25, 0, -20))
			shots.append(bullet(self.x + 25, self.y - 50, 0, -20))
			shots.append(bullet(self.x + 25, self.y - 75, 0, -20))
	def toggleAutoFire(self, event):
		self.autofire = not self.autofire
		print(self.autofire)

