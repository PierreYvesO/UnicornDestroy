class Balle():	
	def __init__(self, x, y, xVel, yVel):
		self.x = x
		self.y = y
		self.xVel = xVel
		self.yVel = yVel
		self.sprites = [PhotoImage(file="fire1.gif"),
				PhotoImage(file="fire2.gif")]
		self.timer = 0
		self.tPeriod = 0
		self.period = 5
		self.dead = False
	def draw(self):
		disp.create_image(self.x, self.y - 25,
		image=self.sprites[self.tPeriod],
		anchor=NW)
		self.timer += 1
		self.timer %= self.period
		if self.timer == 0:
			self.tPeriod += 1
			self.tPeriod %= len(self.sprites)
	def checkCollisions(self):
		for i in aliens:
			if i.x + 50 >= self.x and i.x <= self.x + 15 and i.y + 50 >= self.y \
			and i.y <= self.y + 25:
				self.dead = True
				i.hp -= 1
				explosions.append(Mort(self.x + 7.5, self.y))
	def update(self):
		self.draw()
		self.x += self.xVel
		self.y += self.yVel
		# Bouncing off horizontal walls
		if self.x >= disp.winfo_width() or self.x <= 0:
			self.xVel *= -1
		if self.y + 25 >= disp.winfo_height() or self.y <= 0:
			self.dead = True

		self.checkCollisions()
