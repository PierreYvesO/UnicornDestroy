import tkinter as tk
from random import randint
from Balle import *
from BalleEnnemi import *
from Mort import *
from Alien import *
from Joueur import *

vague=1




class Application(tk.Frame):
	def __init__(self, master=None):
		self.ennemies=list()
		super().__init__(master)
		self.master = master
		self.pack(fill="both")
		self.create_HPBAR()
		self.create_MAIN()
		self.init_ennemyList()
		self.vague(vague)
		self.initEnnemies()
		self.drawEnnemies()
		

	def init_ennemyList(self):
		self.rows = list()
		self.rows.append(list())
		self.rows.append(list())
		self.rows.append(list())
		self.rows.append(list())
		self.rows.append(list())

	def vague(self, vague=1):
		if vague == 1:
			for i in range(20):
				self.ennemies.append(Alien(100,100,1))
		elif vague == 2 :
			for i in range(25):
				self.ennemies.append(Alien(100,100,1))
		elif vague == 3 :
			for i in range(35):
				self.ennemies.append(Alien(100,100,1))
		elif vague == 4 :
			for i in range(45):
				self.ennemies.append(Alien(100,100,1))
		elif vague == 5 :
			for i in range(60):
				self.ennemies.append(Alien(100,100,1))
		
		if len(self.ennemies)==0:
			vague +=1


	def create_HPBAR(self):
		hp_frame = tk.Frame(self,bg="black",height=50)
		self.hp_canvas = tk.Canvas(hp_frame,width=1920, height=50)
		self.hp_canvas.create_rectangle(0, 0, 1920, 50, fill="green")
		self.hp_canvas.pack()

		hp_frame.pack(side="top",fill="both",expand=False)


	def create_MAIN(self):
		self.canvas = list()
		main_frame = tk.Frame(self,bg="RED",height=1030)
		frameHeros = tk.Canvas(main_frame,bg="white",width=200,height=1000)
		frameHeros.grid(column=0,row=0,rowspan=5)
		self.canvas.append(tk.Canvas(main_frame,bg="pink",width=1920,height=200))
		self.canvas[0].grid(column=1,row=0)
		self.canvas.append(tk.Canvas(main_frame,bg="blue",width=1920,height=200))
		self.canvas[1].grid(column=1,row=1)	
		self.canvas.append(tk.Canvas(main_frame,bg="pink",width=1920,height=200))
		self.canvas[2].grid(column=1,row=2)
		self.canvas.append(tk.Canvas(main_frame,bg="blue",width=1920,height=200))
		self.canvas[3].grid(column=1,row=3)
		self.canvas.append(tk.Canvas(main_frame,bg="pink",width=1920,height=200))
		self.canvas[4].grid(column=1,row=4)
		main_frame.pack(side="bottom",fill="both",expand=True)


	def initEnnemies(self):
		for ennemy in self.ennemies:
			i = randint(0, 4)
			self.rows[i].append(ennemy)
		
	def drawEnnemies(self):
		for row in range(0,5) :
			offset = 20
			x=0
			for ent in self.rows[row] :

				self.canvas[row].create_image(100+offset,100,image=img)
				offset += 75
				x+=25

	def drawHero(self):
		return 0
	
     
root = tk.Tk()
root.geometry("1920x1080")
img = tk.PhotoImage(file='/user/miollanr/Téléchargements/TKINTER-Space-Invaders-master/UFOBoss.gif')
app = Application(master=root)
app.mainloop()
