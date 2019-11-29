class Alien:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def getXY(self):
        return self.x, self.y
