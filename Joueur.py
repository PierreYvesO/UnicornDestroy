from Balle import *


class Joueur():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.sprites = [PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ship1.gif"),
        # PhotoImage(file="/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ship2.gif")]
        self.timer = 0
        self.tPeriod = 0
        self.period = 3
        self.left = False
        self.right = False
        self.hp = 3
        self.autofire = False
        '''disp.bind("<Left>", self.moveLeft)
		disp.bind("<Right>", self.moveRight)
		disp.bind("<KeyRelease-Left>", self.stopLeft)
		disp.bind("<KeyRelease-Right>", self.stopRight)
		disp.bind("<KeyRelease-space>", self.spawnBullet)
		disp.bind("<KeyRelease-Shift_L>", self.toggleAutoFire)'''



    def setPosX(self, x):
        self.x = x

    def getPosX(self):
        return self.x
