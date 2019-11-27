import tkinter as tk
from random import randint
class Application(tk.Frame):
	def __init__(self, master=None):
		self.ennemies=list()
		self.ennemies.append(100)
		self.ennemies.append(100)
		self.ennemies.append(100)
		super().__init__(master)
		self.master = master
		self.pack(fill="both")
		self.create_HPBAR()
		self.create_MAIN()
		self.init_ennemyList()
		self.initEnnemies()
		self.drawEnnemies()

	def init_ennemyList(self):
		self.rows = list()
		self.rows.append(list())
		self.rows.append(list())
		self.rows.append(list())
		self.rows.append(list())
		self.rows.append(list())


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
		self.canvas.append(tk.Canvas(main_frame,bg="pink",width=19200,height=200))
		self.canvas[0].grid(column=1,row=0)
		self.canvas.append(tk.Canvas(main_frame,bg="blue",width=19200,height=200))
		self.canvas[1].grid(column=1,row=1)	
		self.canvas.append(tk.Canvas(main_frame,bg="pink",width=19200,height=200))
		self.canvas[2].grid(column=1,row=2)
		self.canvas.append(tk.Canvas(main_frame,bg="blue",width=19200,height=200))
		self.canvas[3].grid(column=1,row=3)
		self.canvas.append(tk.Canvas(main_frame,bg="pink",width=19200,height=200))
		self.canvas[4].grid(column=1,row=4)
		main_frame.pack(side="bottom",fill="both",expand=True)


	def initEnnemies(self):
		for ennemy in self.ennemies:
			i = randint(0, 4)
			print(i)
			self.rows[i].append(ennemy)
		
	def drawEnnemies(self):
		
		for row in range(0,5) :
			offset = 20
			x=0
			for ent in self.rows[row] :

				self.canvas[row].create_rectangle(0+offset+x,20,300+offset+x,180)
				offset += 300
				x+=25
				
		

	def drawHero(self):
		return 0
	
     
root = tk.Tk()
root.geometry("1920x1080")
app = Application(master=root)
app.mainloop()
