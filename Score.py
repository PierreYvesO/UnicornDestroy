from os.path import *
import operator


class Score:
    def __init__(self):
        """
        Récupere les données enregistrées si elles existent
        """
        self.scores = dict()
        if exists("score.txt"):
            with open("score.txt", "r") as fichierR:
                for line in fichierR.readlines():
                    if line != "\n":
                        nom, score = line.split(";")
                        self.scores[nom] = int(score)

    def save(self, joueur):
        """
        Enregistre les nouvelles données soit en ajoutant un nouveau joueur soit en mettant à jour son meilleur score
        @param joueur: objet joueur actuel
        @return:
        """
        if joueur.getNom() in self.scores:
            if joueur.getScore() > int(self.scores[joueur.getNom()]):
                self.scores[joueur.getNom()] = joueur.getScore()
        else:
            self.scores[joueur.getNom()] = joueur.getScore()

        with open("score.txt", "w") as fichier:
            for nom, score in self.getSortedScores():
                data = nom + ";" + str(score)
                fichier.write(data + '\n')

    def getSortedScores(self):
        """
        @return: Liste de tuple du dictionnaire des scores trié (ordre decroissant)
        """
        sorted_dict = sorted(self.scores.items(), key=operator.itemgetter(1))
        sorted_dict.reverse()
        return sorted_dict
