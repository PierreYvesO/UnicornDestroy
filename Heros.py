class Heros(Entite):
	def __init__(self,nom)
		super().__init__(100,0,0,nom,100,100,"bleu",1)
	
	def changerArme(self,score):
		if score>=500 and score<=1000:
			self.degats+=5
		elif score>1000:
			self.degats+=10


