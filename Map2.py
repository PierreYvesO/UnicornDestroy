import sys
import tkinter as tk
import tkinter.font as tkFont
from random import randint
from tkinter.messagebox import askquestion
from Sound import *


from Joueur import *

vague = 1
pause = False


class Application(tk.Frame):
    def __init__(self, master=None):

        sys.setrecursionlimit(10000)

        super().__init__(master)
        self.master = master
        self.pack(fill="both")

        self.create_HPBAR()
        self.create_MAIN()

        self.hero = Joueur()
        self.init_game(fullreset=True)
        self.pause()
        self.drawJoueur()

        self.init_sound()
        self.init_touch_binding()

    def create_HPBAR(self):
        hp_frame = tk.Frame(self, bg="black", height=50)
        self.hp_canvas = tk.Canvas(hp_frame, width=1920, height=50, bg="black")
        self.hp_canvas.create_rectangle(0, 0, 1920, 50, fill="green")
        self.hp_canvas.pack()

        hp_frame.pack(side="top", fill="both", expand=False)

    def create_MAIN(self):
        self.canvas = list()
        self.main_frame = tk.Frame(self, bg="black")
        self.frameHeros = tk.Canvas(self.main_frame, bg='black', bd=0, highlightthickness=0, width=ship[0].width())
        self.frameHeros.grid(column=0, row=0, rowspan=5, sticky="NS")

        for i in range(5):
            self.canvas.append(tk.Canvas(self.main_frame, bd=0, bg='black', highlightthickness=0))
            self.canvas[i].create_image(0, 0, tag="bg")
            self.canvas[i].grid(column=1, row=i, sticky="WE")
            self.create_background(self.canvas[i])
            tk.Grid.rowconfigure(self.main_frame, i, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 1, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 0, weight=0)

        self.main_frame.pack(side="bottom", fill="both", expand=True)

    def init_game(self, fullreset=False):
        global vague
        if fullreset:
            vague = 1
            self.hero.setPV()
            self.resetPV()
            self.hero.setScore(0)
        
        self.init_ennemyList()
        self.vague()
        self.initEnnemies()
        self.drawEnnemies()
        self.printWave()
        self.printScore()
        if fullreset:
            self.displayCommands()

    def drawJoueur(self):

        hero = self.frameHeros.create_image(ship[0].width() / 2, ship[0].height() / 2, image=ship[0])
        x, y = self.frameHeros.coords(hero)
        self.hero.setPosX(x)
        self.hero.setPosY(y)
        self.updategif(hero, self.frameHeros, ship)

    def init_ennemyList(self):
        self.rows = [0, 0, 0, 0, 0]

    def vague(self):
        self.ennemies = vague * 5

    def init_sound(self):
        self.music = Sound("testjeu.mp3")
        self.music.start()
        
    def create_background(self, canvas):
        canvas.update()
        for i in range(randint(50, 50)):
            x = randint(0, canvas.winfo_width() * 10)
            y = randint(0, canvas.winfo_height() - 60 * 2)
            w = randint(1, 5)

            canvas.create_oval(x, y, x + w, y + w, width=w, outline='white', tag="bg_star")

        colors = ["DodgerBlue4", "MediumOrchid4", "firebrick4", "goldenrod"]
        for i in range(randint(0, 2)):
            color = colors[randint(0, len(colors) - 1)]
            x = randint(0, canvas.winfo_width() * 3)
            y = 0
            w = randint(30, 50)
            s = w / 5
            canvas.create_oval(x, y, x + w, y + w, width=1, fill=color, tag="bg_planet")
            canvas.create_oval(x - w / 2, y + w / 2 - s, x + w * 1.50, y + w / 2 + s, width=2, outline=color,
                               tag="bg_planet_circle")

        self.update_background(canvas)

    def printWave(self):
        font = tkFont.Font(family='Helvetica', size=36, weight='bold')

        text = "Wave {}".format(vague)
        if len(self.canvas[0].find_withtag("wave")) == 0:
            self.canvas[0].create_text(self.canvas[0].winfo_width() / 2, 36,
                                       text=text, fill="RED", font=font, tag="wave")
        else:
            self.canvas[0].itemconfigure(self.canvas[0].find_withtag("wave"), text=text)
            
    def printScore(self):
        font = tkFont.Font(family='Helvetica', size=36, weight='bold')

        text = "Score {}".format(self.hero.getScore())
        if len(self.canvas[0].find_withtag("score")) == 0:
            self.canvas[0].create_text(self.canvas[0].winfo_width() -200, 36,
                                       text=text, fill="WHITE", font=font, tag="score")
        else:
            self.canvas[0].itemconfigure(self.canvas[0].find_withtag("score"), text=text)

    def moveDown(self, event=None):
        x = self.hero.getPosX() + self.frameHeros.winfo_height() / 5
        if x < self.main_frame.winfo_height():
            self.hero.setPosX(x)
            self.frameHeros.delete("all")
            hero = self.frameHeros.create_image(90, x)
            self.updategif(hero, self.frameHeros, ship)

    def moveUp(self, event=None):
        x = self.hero.getPosX() - self.frameHeros.winfo_height() / 5
        if x > 0:
            self.hero.setPosX(x)
            self.frameHeros.delete("all")
            hero = self.frameHeros.create_image(90, x)
            self.updategif(hero, self.frameHeros, ship)

    def tir(self, event=None):
        offset = self.main_frame.winfo_height() / 5
        if 0 < self.hero.getPosX() < offset:
            row = 0
        elif self.hero.getPosX() < offset * 2:
            row = 1
        elif self.hero.getPosX() < offset * 3:
            row = 2
        elif self.hero.getPosX() < offset * 4:
            row = 3
        else:
            row = 4
        idballe = self.canvas[row].create_image(0, self.canvas[row].winfo_height() / 2,
                                                tag="bullet")
        self.updategif(idballe, self.canvas[row], bullet, img_offset=0, noloop=True)
        self.moveTir(idballe, self.canvas[row])

    def mouvements(self, activate):
        if activate:
            self.master.bind("<Down>", self.moveDown)
            self.master.bind("<Up>", self.moveUp)
        else:
            self.master.unbind("<Down>")
            self.master.unbind("<Up>")

    def init_touch_binding(self):
        self.master.bind("<h>", self.help)
        self.master.bind("<Escape>", self.end)
        self.master.bind("<Return>", self.pause)

    def eventTir(self, activate):
        if activate:
            self.master.bind("<KeyRelease-space>", self.tir)
        else:
            self.master.unbind("<KeyRelease-space>")

    def initEnnemies(self):
        for ennemy in range(self.ennemies):
            i = randint(0, 4)
            self.rows[i] += 1

    def moveTir(self, idt, canvas):
        global vague
        if pause:
            canvas.after(10, lambda: self.moveTir(idt, canvas))
        else:
            if len(canvas.find_withtag(idt)) == 1:
                canvas.move(idt, 10, 0)
                x, y = canvas.coords(idt)
                if x > canvas.winfo_width() - 250:
                    canvas.delete(idt)
                tpl = canvas.find_overlapping(x, y, x, y + 130)

                if self.tagged("bullet", tpl, canvas) and self.tagged("uni", tpl, canvas):
                    #playsound("deaduni2.mp3", False)
                    canvas.itemconfig(self.getIDfromTag("uni", tpl, canvas), image=dead, tags="dead")
                    canvas.delete(self.getIDfromTag("bullet", tpl, canvas))
                    self.updatePV(1)
                    self.ennemies -= 1
                    self.hero.setScore(self.hero.getScore()+vague)
                    self.printScore()
                    if self.ennemies <= 0:
                        vague += 1
                        self.init_game()

                else:
                    canvas.after(10, lambda: self.moveTir(idt, canvas))

    def updategif(self, idimg, canvas, img, img_offset=-1, time=-1, looptime=200, noloop=False):
        if pause:
            canvas.after(75,
                         lambda: self.updategif(idimg, canvas, img, img_offset=img_offset, time=time, looptime=looptime,
                                                noloop=noloop))
        else:
            if "dead" in canvas.gettags(idimg):
                if time == 10:
                    canvas.after(looptime, lambda: self.updategif(idimg, canvas, dead, time + 1))
                else:
                    canvas.delete(idimg)
            elif len(canvas.find_withtag(idimg)) != 0:
                if img_offset == -1:
                    img_offset = randint(0, len(img) - 1)

                elif img_offset >= len(img) and noloop:
                    img_offset = img_offset - 1

                elif img_offset >= len(img):
                    img_offset = 0
                canvas.itemconfig(idimg, image=img[img_offset])

                if not noloop:
                    canvas.after(looptime,
                                 lambda: self.updategif(idimg, canvas, img, img_offset + 1, looptime=looptime))
                else:
                    bulletsound = Sound("bulletsound.mp3",stop=True).start()
                    canvas.after(looptime,
                                 lambda: self.updategif(idimg, canvas, img, img_offset + 1, looptime=looptime,
                                                        noloop=True))

    def drawEnnemies(self):
        for row in range(0, 5):
            self.canvas[row].delete("uni")
            offset = 20 + randint(0, 1000)
            x = 0
            self.master.update()
            for ent in range(self.rows[row]):
                idlic = self.canvas[row].create_image(1920 + offset, self.canvas[row].winfo_height() / 2, tag="uni")
                offset += 500 + randint(0, 2000)
                x += 25
                self.moveEnnemy(idlic, self.canvas[row])
                self.updategif(idlic, self.canvas[row], unicorn, looptime=50)

    def moveEnnemy(self, idlic, canvas, img_offset=-1):
        global vague
        if pause:
            canvas.after(75, lambda: self.moveEnnemy(idlic, canvas, img_offset))
        else:
            if len(canvas.find_withtag(idlic)) == 1:
                if self.hero.getPV() == 0:

                    canvas.delete(idlic)

                else:
                    canvas.move(idlic, -30-vague*10, 0)

                    # get current position
                    x1, y = canvas.coords(idlic)
                    if x1 <= unicorn[0].width() / 2 + 20:
                        canvas.delete(idlic)
                        self.updatePV(-10)
                        dead = Sound("deaduni.mp3",stop=True).start()
                        self.ennemies -= 1
                        if self.ennemies == 0:
                            vague += 1
                            self.init_game()

                    else:
                        canvas.after(75, lambda: self.moveEnnemy(idlic, canvas, img_offset + 1))

    def updatePV(self, pvDIFF):
        self.hero.setPV(self.hero.getPV() + pvDIFF)
        pv = self.hero.getPV()
        pvscale = pv / 100 * self.hp_canvas.winfo_width()
        self.hp_canvas.delete("all")
        self.hp_canvas.create_rectangle(0, 0, pvscale, 50, fill="green")
        if pv <= 0:
            self.pause()
            root.config(cursor="heart")
            answer = askquestion("LOOSER !", "TRY AGAIN?")
            if answer == "yes":
                root.config(cursor="none")
                self.init_game(fullreset=True)
            else:
                self.end()

    def resetPV(self):
        self.hp_canvas.delete("all")
        self.hp_canvas.create_rectangle(0, 0, self.hp_canvas.winfo_width(), 50, fill="green")

    def tagged(self, tag, tp, canvas):
        listTAGS = list()
        [listTAGS.append(results) for results in [canvas.gettags(i) for i in tp]]
        nb = 0
        for tags in tp:

            if tag in canvas.gettags(tags):
                nb += 1
        if nb != 0:
            return nb
        return False

    def update_background(self, canvas):
        global vague
        if pause:
            canvas.after(50, lambda: self.update_background(canvas))
        else:

            canvas.move('bg_star', -20-vague*5, 0)
            canvas.move('bg_planet', -2-vague*2, 0)
            canvas.move('bg_planet_circle', -2-vague*2, 0)
            for star in canvas.find_withtag('bg_star'):
                x = canvas.coords(star)
                if x[0] < 0:
                    canvas.delete(star)
                    x = canvas.winfo_width()
                    y = randint(0, canvas.winfo_height())
                    w = randint(1, 5)

                    canvas.create_oval(x, y, x + w, y + w, width=w, outline='white', tag="bg_star")
            canvas.tag_lower("bg_star")

            for circle in canvas.find_withtag('bg_planet_circle'):
                x = canvas.coords(circle)
                if x[0] < 0:
                    canvas.delete(circle)
            canvas.tag_lower("bg_planet_circle")

            colors = ["DodgerBlue4", "MediumOrchid4", "firebrick4", "goldenrod"]
            for planet in canvas.find_withtag('bg_planet'):
                i = 0
                if i % 2 == 0:
                    x = canvas.coords(planet)
                    if x[0] < 0:
                        canvas.delete(planet)
                        rand = randint(0, 1)
                        color = colors[randint(0, len(colors) - 1)]
                        x = canvas.winfo_width()
                        y = randint(60, canvas.winfo_height() - 60)
                        w = randint(10, 50)
                        s = w / 5
                        canvas.create_oval(x, y, x + w, y + w, width=1, fill=color, tag="bg_planet")
                        if rand % 2 == 0:
                            canvas.create_oval(x - w / 2, y + w / 2 - s, x + w * 1.50, y + w / 2 + s, width=2,
                                               outline=color,
                                               tag="bg_planet_circle")
                    i += 1
            canvas.tag_lower("bg_planet")

            canvas.after(50-vague*5, lambda: self.update_background(canvas))

    def getIDfromTag(self, tag, ids, canvas):
        for tags in ids:
            if tag in canvas.gettags(tags):
                return tags

    def end(self, event=None):
        self.music.stop()
        self.music.join()
        self.master.destroy()

        exit(0)

    def pause(self, event=None):
        global pause
        if pause:
            self.mouvements(True)
            self.eventTir(True)
            pause = False
        else:
            self.mouvements(False)
            self.eventTir(False)
            pause = True

    def help(self, event=None):
        if len(self.canvas[0].find_withtag("help")) == 1:
            self.removeCommands()
        else:
            self.displayCommands()

    def displayCommands(self):
        font = tkFont.Font(family='Helvetica', size=36, weight='bold')

        texts = ["Press Enter to Start/Pause/UnPause", "Press ↑ or ↓ to Move", "Press Space to Attack",
                 "Press Escape to Stop", "Press H to display this"]
        for i in range(5):
            self.canvas[i].create_text(self.canvas[0].winfo_width() / 2, self.canvas[0].winfo_height() / 2,
                                       text=texts[i], fill="Yellow", font=font, tag="help")

    def removeCommands(self):
        for canvas in self.canvas:
            canvas.delete(canvas.find_withtag("help")[0])



root = tk.Tk()

unicorn = [tk.PhotoImage(file='gif/unireact.gif', format='gif -index %i' % i) for i in range(9)]
ship = [tk.PhotoImage(file='gif/vaisseau.gif', format='gif -index %i' % i) for i in range(4)]
bullet = [tk.PhotoImage(file='gif/bullet.gif', format='gif -index %i' % i) for i in range(12)]
dead = tk.PhotoImage(file='gif/dead.gif')

root.attributes("-fullscreen", True)
root.config(cursor="none")
app = Application(master=root)
app.mainloop()
