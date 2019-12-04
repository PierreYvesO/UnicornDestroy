from os.path import *

class Score():
    def __init__(self):
        self.scores = dict()
        if not exists("score.txt"):
            open("score.txt", "w")
            
        else:
            fichierR = open("score.txt","r")
            for line in fichierR.readlines():
                if line!="\n":
                    nom,score = line.split(";")
                    self.scores[nom] = score
            fichierR.close()

    def save(self,joueur):
        print(self.scores)
        if joueur.getNom() in self.scores:
            if joueur.getScore() > int(self.scores[joueur.getNom()]):
                self.scores[joueur.getNom()] = joueur.getScore()
        else:
            self.scores[joueur.getNom()] = joueur.getScore()
        #self.scores = sorted(self.scores.items(), key = lambda x : x[1])
        fichier = open("score.txt","w")
        data = ""
        for nom, score in self.scores.items():
            data += nom+";"+str(score)+"\n"

        fichier.write(data)
        fichier.close()

