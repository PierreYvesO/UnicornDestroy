import tkinter as tk
from random import randint
from Alien import *
from Joueur import *

import sys

vague = 5


class Application(tk.Frame):
    def __init__(self, master=None):
        self.pv = 100
        sys.setrecursionlimit(10000)
        self.ennemies = list()
        super().__init__(master)
        self.master = master
        self.pack(fill="both")
        self.create_HPBAR()
        self.create_MAIN()
        self.hero = Joueur(95, 100)
        self.mouvements()
        self.eventTir()

        self.init_ennemyList()
        self.vague(vague)
        self.initEnnemies()
        self.drawEnnemies()
        self.drawJoueur()

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
                self.ennemies.append(Alien(100, 100, 1))
        elif vague == 2:
            for i in range(25):
                self.ennemies.append(Alien(100, 100, 1))
        elif vague == 3:
            for i in range(35):
                self.ennemies.append(Alien(100, 100, 1))
        elif vague == 4:
            for i in range(45):
                self.ennemies.append(Alien(100, 100, 1))
        elif vague == 5:
            for i in range(60):
                self.ennemies.append(Alien(100, 100, 1))

        if len(self.ennemies) == 0:
            vague += 1

    def create_HPBAR(self):
        hp_frame = tk.Frame(self, bg="black", height=50)
        self.hp_canvas = tk.Canvas(hp_frame, width=1920, height=50)
        self.hp_canvas.create_rectangle(0, 0, 1920, 50, fill="green")
        self.hp_canvas.pack()

        hp_frame.pack(side="top", fill="both", expand=False)

    def create_MAIN(self):
        self.canvas = list()
        main_frame = tk.Frame(self, bg="RED", height=1030)
        self.frameHeros = tk.Canvas(main_frame, bg="white", width=200, height=1000)
        self.frameHeros.grid(column=0, row=0, rowspan=5)
        self.canvas.append(tk.Canvas(main_frame, bg="pink", width=1920, height=200))
        self.canvas[0].grid(column=1, row=0)
        self.canvas.append(tk.Canvas(main_frame, bg="blue", width=1920, height=200))
        self.canvas[1].grid(column=1, row=1)
        self.canvas.append(tk.Canvas(main_frame, bg="pink", width=1920, height=200))
        self.canvas[2].grid(column=1, row=2)
        self.canvas.append(tk.Canvas(main_frame, bg="blue", width=1920, height=200))
        self.canvas[3].grid(column=1, row=3)
        self.canvas.append(tk.Canvas(main_frame, bg="pink", width=1920, height=200))
        self.canvas[4].grid(column=1, row=4)
        main_frame.pack(side="bottom", fill="both", expand=True)

    def moveDown(self, event):
        x = self.hero.getPosX() + 200
        if x < 1000:
            self.hero.setPosX(x)
            self.frameHeros.delete("all")
            hero = self.frameHeros.create_image(90, x, image=ship[0])
            self.updategif(hero, self.frameHeros, ship)

    def moveUp(self, event):
        x = self.hero.getPosX() - 200
        if x > 0:
            self.hero.setPosX(x)
            self.frameHeros.delete("all")
            hero = self.frameHeros.create_image(90, x, image=ship[0])
            self.updategif(hero, self.frameHeros, ship)

    def tir(self, event):
        if 0 < self.hero.getPosX() < 210:
            row = 0
        elif self.hero.getPosX() < 420:
            row = 1
        elif self.hero.getPosX() < 630:
            row = 2
        elif self.hero.getPosX() < 840:
            row = 3
        else:
            row = 4

        idballe = self.canvas[row].create_image(100, 100, image=bullet[0])
        self.updategif(idballe, self.canvas[row], bullet)
        self.moveTir(idballe, self.canvas[row])

    def mouvements(self):
        self.master.bind("<Down>", self.moveDown)
        self.master.bind("<Up>", self.moveUp)

    def eventTir(self):
        self.master.bind("<space>", self.tir)

    def initEnnemies(self):
        for ennemy in self.ennemies:
            i = randint(0, 4)
            self.rows[i].append(ennemy)

    def moveTir(self, idt, canvas):
        if len(canvas.find_withtag(idt)) == 1:
            canvas.move(idt, 10, 0)
            x, y = canvas.coords(idt)
            if x > canvas.winfo_width() - 250:
                canvas.delete(idt)
            tpl = canvas.find_overlapping(x, y, x, y + 130)

            if len(tpl) > 1 and 'dead' not in canvas.gettags(tpl[0]):
                if 'uni' in canvas.gettags(tpl[0]):
                    canvas.itemconfig(tpl[1], image=dead, tags="dead")
                    canvas.delete(tpl[0])
                    self.updatePV(1)
                else:
                    canvas.delete(tpl[1])
            else:
                canvas.after(10, lambda: self.moveTir(idt, canvas))

    def drawJoueur(self):
        hero = self.frameHeros.create_image(95, 100, image=ship[0])

        x, y = self.frameHeros.coords(hero)
        self.updategif(hero, self.frameHeros, ship)
        return x, y

    def updategif(self, idimg, canvas, img, img_offset=-1, time=-1):
        if "dead" in canvas.gettags(idimg):
            if time == 10:
                canvas.after(200, lambda: self.updategif(idimg, canvas, dead, time + 1))
            else:
                canvas.delete(idimg)
        elif len(canvas.find_withtag(idimg)) == 1:
            if img_offset == -1:
                img_offset = randint(0, len(img) - 1)
            elif img_offset >= len(img):
                img_offset = 0
            canvas.itemconfig(idimg, image=img[img_offset])
            canvas.after(200, lambda: self.updategif(idimg, canvas, img, img_offset + 1))

    def drawEnnemies(self):
        self.tags = list()
        for row in range(0, 5):
            offset = 20 + randint(0, 10000)
            x = 0
            for ent in self.rows[row]:
                idlic = self.canvas[row].create_image(1920 + offset, 100,tag="uni")
                offset += 500 + randint(0, 5000)
                x += 25
                self.moveEnnemy(idlic, self.canvas[row], ent)
                self.updategif(idlic, self.canvas[row], unicorn)

    def moveEnnemy(self, idlic, canvas, ent, img_offset=-1):
        if len(canvas.find_withtag(idlic)) == 1:
            if self.pv <= 0:
                canvas.delete(idlic)
            else:
                canvas.move(idlic, -30, 0)

                # get current position
                x1, y1 = canvas.coords(idlic)
                ent.setPos(x1, y1)
                if x1 <= unicorn[0].width() / 2 + 20:
                    canvas.delete(idlic)
                    self.updatePV(-10)

                else:
                    canvas.after(75, lambda: self.moveEnnemy(idlic, canvas, ent, img_offset + 1))

    def updatePV(self, pvDIFF):
        if self.pv + pvDIFF < 100:
            self.pv = self.pv + pvDIFF
            pv = self.pv / 100 * 1920
            self.hp_canvas.delete("all")
            self.hp_canvas.create_rectangle(0, 0, pv, 50, fill="green")


root = tk.Tk()
root.geometry("1920x1080")

unicorn = [tk.PhotoImage(file='gif/uni.gif', format='gif -index %i' % i) for i in range(9)]
ship = [tk.PhotoImage(file='gif/vaisseau.gif', format='gif -index %i' % i) for i in range(4)]
bullet = [tk.PhotoImage(file='gif/balle.gif', format='gif -index %i' % i) for i in range(4)]
dead = tk.PhotoImage(file='gif/dead.gif', )
app = Application(master=root)
app.mainloop()
