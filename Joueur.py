class Joueur:
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.pv = 100
        self.score = 0
        self.nom = name

    def getPV(self):
        return self.pv

    def setPosY(self, y):
        self.y = y

    def setPV(self, pv=100):
        """
        Mise à jour des pv du joeur. Si aucun parametre lui rend toute sa vie
        @param pv: nouvelle valeur des pv
        @return:
        """
        # limite à 100 pv
        if pv > 100:
            self.pv = 100
        else:
            self.pv = pv

    def getPosY(self):
        return self.y
        
    def getScore(self):
        return self.score
    
    def setScore(self, score):
        self.score = score

    def getNom(self):
        return self.nom
