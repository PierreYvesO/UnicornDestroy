class Joueur:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pv = 100

    def getPV(self):
        return self.pv

    def setPosX(self, x):
        self.x = x

    def setPosY(self, y):
        self.y = y

    def setPV(self, pv=100):
        self.pv = pv

    def getPosX(self):
        return self.x
