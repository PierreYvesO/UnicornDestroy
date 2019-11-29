import random


class Alien():
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.upgrad = False
        if self.t == 1:
            self.sprites = ["/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/1HitAlien1.gif",
                            "/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/1HitAlien2.gif"]
            self.period = 15
            self.moveSpeed = 3
            self.hp = 1
        if self.t == 2:
            self.sprites = [("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/MultiHitAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/MultiHitAlien2.gif")]
            self.period = 12
            self.moveSpeed = 3
            self.hp = 3
        if self.t == 3:
            self.sprites = [("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ShooterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ShooterAlien2.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ShooterAlien3.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ShooterAlien4.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/ShooterAlien5.gif")]
            self.period = 6
            self.moveSpeed = 3
            self.hp = 1
        if not self.upgrad:
            self.t = 4
            self.moveSpeed = 3.5
            self.upgrad = True
        if self.t == 4:
            self.sprites = [("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien2.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien3.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien2.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien1.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien4.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien5.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien6.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien7.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/BlasterAlien7.gif")]
            self.period = 7
            self.moveSpeed = 2
            self.hp = 3
        if not self.upgrad:
            self.t = 5
        if self.t == 5:
            self.sprites = [("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/UFOBoss.gif"),
                            ("/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/UFOBoss.gif")]
            self.period = 2
            self.moveSpeed = 2
            self.hp = 10
            self.xVel = self.moveSpeed
            self.timer = 0
            self.tPeriod = 0
            self.moveDownTimer = 0
            self.moveNext = True

    def draw(self):
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)

    def update(self):
        self.draw()
        self.x += self.xVel
        if self.x <= 0 or self.x + 50 >= disp.winfo_width():
            # Speed up, move down
            self.xVel *= -1.15
            self.y += 50
        if self.hp <= 0:
            self.dead = True
        if self.t == 3 and self.tPeriod == len(self.sprites) - 1 \
                and self.timer == self.period - 1 \
                and random.random() < 0.3:
            enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                False))
        if self.t == 4 and self.tPeriod == len(self.sprites) - 1 and \
                self.timer == 0:
            if random.random() < 0.3:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    True))
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, -1, 7,
                                                    True))
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                    True))
            elif random.random() < 0.7:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                    True))
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 25, 0, 7,
                                                    True))
            else:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                    False))
        if self.t == 5 and self.tPeriod == 0 and self.timer == 0 and \
                random.random() < 0.5:
            if random.random() < 0.1:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    False))
            else:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    True))

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def getXY(self):
        return self.x, self.y
