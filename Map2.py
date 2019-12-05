import tkinter as tk
import tkinter.font as tkFont
from random import randint
from tkinter.messagebox import askquestion
from tkinter.simpledialog import askstring

from Joueur import *
from Score import *
from Sound import *

pause = False


def ask_name():
    """
    Affiche une fenetre demandant le nom du joueur. Si il n'y a pas de réponse un nom par défaut est donné
    @return: le nom du joueur
    """
    root.config(cursor="heart")
    name = askstring("Name ?", "Enter your name")
    root.config(cursor="None")

    if name is None or name is "":
        return 'Anonymous'
    else:
        return name


def tagged(tag, tp, canvas):
    """
    Verifie si un certain tag est présent dans la liste tp
    @param tag: chaine de caractère correspondant au tag de l'objet tkinter recherché
    @param tp: liste de tuple des tags
    @param canvas: canvas contenant ces tags
    @return: Si le tag est présent dans liste ou non
    """
    listTAGS = list()
    [listTAGS.append(results) for results in [canvas.gettags(i) for i in tp]]
    nb = 0
    for tags in tp:

        if tag in canvas.gettags(tags):
            nb += 1
    if nb != 0:
        return nb
    return False


def getIDfromTag(tag, ids, canvas):
    """
    Retourne l'ID d'un objet tkitner dans le canvas dans la liste ids
    @param tag: chaine de caractère correspondant au tag de l'objet tkinter
    @param ids: liste des id des objets tkinter
    @param canvas: canvas contenant ces tags
    @return: l'id qui correspond au tag
    """
    for id_ in ids:
        if tag in canvas.gettags(id_):
            return id_


class Application(tk.Frame):

    def __init__(self, master=None):
        """
        Constructeur de l'application
        Initialise tous les éléments visuels, sonores et touches
        @param master: Fenetre mère tkinter
        """

        self.canvas = None
        self.main_frame = None
        self.hp_canvas = None
        self.frameHeros = None
        self.rows = None
        self.ennemies = None
        self.vague = 1

        super().__init__(master)
        self.master = master
        self.pack(fill="both")
        self.score = Score()
        self.create_HPBAR()
        self.create_MAIN()
        self.hero = Joueur(ask_name())
        self.drawJoueur()
        self.init_game(fullreset=True)
        self.pause()
        self.init_sound()
        self.init_touch_binding()

    def create_HPBAR(self):
        """
        Créé une frame qui contiendra le canvas de la barre de vie et l'initialise
        @return:
        """
        hp_frame = tk.Frame(self, bg="black", height=50)
        self.hp_canvas = tk.Canvas(hp_frame, width=self.master.winfo_screenwidth(), height=50, bg="black")
        self.hp_canvas.create_rectangle(0, 0, self.master.winfo_screenwidth(), 50, fill="green")
        self.hp_canvas.pack()
        hp_frame.pack(side="top", fill="both", expand=False)

    def create_MAIN(self):
        """
        Créé une frame qui contiendra le heros et un autre les ennemis
        @return:
        """
        self.canvas = list()
        self.main_frame = tk.Frame(self, bg="black")

        # Creation du canvas où le joueur se déplacera
        self.frameHeros = tk.Canvas(self.main_frame, bg='black', bd=0, highlightthickness=0, width=ship[0].width())
        # le canvas prend toute la premiere colone
        self.frameHeros.grid(column=0, row=0, rowspan=5, sticky="NS")

        # Creation de 5 canvas. Chacun represente une ligne d'ennemi
        for i in range(5):
            self.canvas.append(tk.Canvas(self.main_frame, bd=0, bg='black', highlightthickness=0))
            self.canvas[i].create_image(0, 0, tag="bg")
            self.canvas[i].grid(column=1, row=i, sticky="WE")
            self.create_background(self.canvas[i])
            # le canvas es postionné sur la ligne correspondante avec un poid de 1 pour s'etendre en longueur
            tk.Grid.rowconfigure(self.main_frame, i, weight=1)

        # La 2eme colone a un poid supérieur donc s'etend par rapport à la premiere
        tk.Grid.columnconfigure(self.main_frame, 1, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 0, weight=0)

        self.main_frame.pack(side="bottom", fill="both", expand=True)

    def init_game(self, fullreset=False):
        """
        Initialise tous ce qui concerne l'ajout des images, des ennemis et leur positionnement
        @param fullreset: Mise à jour totale des éléments (vague, pv et le score)
                            Affiche l'aide pour les commandes
        @return:
        """
        if fullreset:
            self.vague = 1
            self.hero.setPV()
            self.resetPV_bar()
            self.hero.setScore(0)

        self.init_ennemyList()
        self.init_ennemies()
        self.initEnnemies()
        self.drawEnnemies()
        self.printWave()
        self.printScore()
        if fullreset:
            self.displayCommands()

    def drawJoueur(self):
        """
        Dessine l'image du joueur
        @return:
        """

        # Creation de l'image du joueur avec un tag
        hero = self.frameHeros.create_image(ship[0].width() / 2, self.frameHeros.winfo_height() / 10, tag="hero")

        # Mise à jour du gif du vaisseau
        self.updategif(hero, self.frameHeros, ship)

        # Récupéreation et mise à jour des coordonnées du joueur
        x, y = self.frameHeros.coords(hero)
        self.hero.setPosY(y)

    def init_ennemyList(self):
        """
        Initialisation à 0 du nombre d'ennemis dans chanque ligne
        @return:
        """
        self.rows = [0, 0, 0, 0, 0]

    def init_ennemies(self):
        """
        Defini le nombre d'ennemi par vague
        @return:
        """
        self.ennemies = self.vague * 5

    def init_sound(self):
        """
        Lance le thread de la musique de fond
        @return:
        """
        Sound("testjeu.mp3").start()

    def create_background(self, canvas):
        """
        Créé le fond d'ecran sur un canvas
        @param canvas: canvas sur lequel on va dessiner
        @return:
        """
        # Mise à jour du canvas pour récuperer les bonnes données de taille
        canvas.update()

        # 1-- Dessin des etoiles
        # Chaque ligne aura entre 30 et 50 etoiles
        for i in range(randint(30, 50)):
            # position et epaisseur aléatoires sur le canvas
            x = randint(0, canvas.winfo_width() * 10)
            y = randint(0, canvas.winfo_height() - 60 * 2)
            w = randint(1, 5)

            # Creation sur le canvas avec le tag
            canvas.create_oval(x, y, x + w, y + w, width=w, outline='white', tag="bg_star")

        colors = ["DodgerBlue4", "MediumOrchid4", "firebrick4", "goldenrod"]
        # 1-- Dessin des planetes
        # Chaque ligne aura entre 0 et 2 planetes
        for i in range(randint(0, 2)):
            # couleur, position et epaisseur aléatoires sur le canvas
            color = colors[randint(0, len(colors) - 1)]
            x = randint(0, canvas.winfo_width() * 3)
            y = 0
            w = randint(30, 50)
            s = w / 5

            # Creation sur le canvas avec le tag
            canvas.create_oval(x, y, x + w, y + w, width=1, fill=color, tag="bg_planet")
            canvas.create_oval(x - w / 2, y + w / 2 - s, x + w * 1.50, y + w / 2 + s, width=2, outline=color,
                               tag="bg_planet_circle")

        # Lance le thread de mise à jour du fond
        self.update_background(canvas)

    def printWave(self):
        """
        Affiche la vague actuelle à l'écran
        @return:
        """
        font = tkFont.Font(family='Helvetica', size=36, weight='bold')

        text = "Wave {}".format(self.vague)

        # Si le texte est deja presnet sur l'image on le modifie sinon on le créé
        if len(self.canvas[0].find_withtag("wave")) == 0:
            self.canvas[0].create_text(self.canvas[0].winfo_width() / 2, 36,
                                       text=text, fill="RED", font=font, tag="wave")
        else:
            self.canvas[0].itemconfigure(self.canvas[0].find_withtag("wave"), text=text)

    def printScore(self):
        """
        Affiche le score actuel à l'écran
        @return:
        """
        font = tkFont.Font(family='Helvetica', size=36, weight='bold')
        text_2 = "Score {}".format(self.hero.getScore())

        # Si le texte est deja present sur l'image on le modifie sinon on le créé
        if len(self.canvas[0].find_withtag("score")) == 0:
            self.canvas[0].create_text(self.canvas[0].winfo_width() - 200, 36,
                                       text=text_2, fill="WHITE", font=font, tag="score")
        else:
            self.canvas[0].itemconfigure(self.canvas[0].find_withtag("score"), text=text)

    def moveDown(self, event=None):
        """
        Deplacement du joueur vers le bas
        @param event:
        @return:
        """
        # Recupere la valeurs stockees
        y = self.hero.getPosY()
        # y_offset correspond a la distance de décalage
        y_offset = self.frameHeros.winfo_height() / 5
        # Vérifie le nom dépassement de la zone
        if y + y_offset < self.main_frame.winfo_height():
            # Met a jour la donnée stockée
            self.hero.setPosY(y + y_offset)
            # Déplace l'image
            self.frameHeros.move("hero", 0, y_offset)

    def moveUp(self, event=None):
        """
        Deplacement du joueur vers le haut
        @param event:
        @return:
        """
        # Recupere la valeurs stockees
        y = self.hero.getPosY()
        # y_offset correspond a la distance de décalage
        y_offset = -self.frameHeros.winfo_height() / 5
        # Vérifie le nom dépassement de la zone
        if y + y_offset > 0:
            # Met a jour la donnée stockée
            self.hero.setPosY(y + y_offset)
            # Déplace l'image
            self.frameHeros.move("hero", 0, y_offset)

    def tir(self, event=None):
        """
        Envoi un projectile selon la position du joueur
        @param event: 
        @return: 
        """
        # offset correspond a la distance de décalage
        offset = self.main_frame.winfo_height() / 5

        if 0 < self.hero.getPosY() < offset:
            row = 0
        elif self.hero.getPosY() < offset * 2:
            row = 1
        elif self.hero.getPosY() < offset * 3:
            row = 2
        elif self.hero.getPosY() < offset * 4:
            row = 3
        else:
            row = 4

        # Création de l'image dans le canvas avec le tag bullet
        idballe = self.canvas[row].create_image(0, self.canvas[row].winfo_height() / 2,
                                                tag="bullet")
        # lancement du Thread de mise à jour du gif
        self.updategif(idballe, self.canvas[row], bullet, img_offset=0, noloop=True)
        # Lancement du thread de déplacement
        self.moveTir(idballe, self.canvas[row])

    def mouvements(self, activate):
        """
        Définition des touches de deplacement
        @param activate: Si True, les touche ne sont plus liées à une action
        @return:
        """
        if activate:
            self.master.bind("<Down>", self.moveDown)
            self.master.bind("<Up>", self.moveUp)
        else:
            self.master.unbind("<Down>")
            self.master.unbind("<Up>")

    def init_touch_binding(self):
        """
        Définition des touches liées à des actions
        @return:
        """
        self.master.bind("<h>", self.help)
        self.master.bind("<Escape>", self.end)
        self.master.bind("<Return>", self.pause)
        self.master.bind("<Tab>", self.displayScores)

    def eventTir(self, activate):
        """
        Définition de la touche de tir
        @param activate: Si True, la touche n'est plus liée à une action
        @return:
        """
        if activate:
            self.master.bind("<KeyRelease-space>", self.tir)
        else:
            self.master.unbind("<KeyRelease-space>")

    def initEnnemies(self):
        """
        Rempli la liste des lignes par le nombre d'ennemi qui apparaitront dessus
        """
        for ennemy in range(self.ennemies):
            i = randint(0, 4)
            self.rows[i] += 1

    def moveTir(self, idt, canvas):
        """
        Boucle threadée du deplacement du tir
        Gere aussi l'evenement de collision

        @param idt: id tkinter de l'image
        @param canvas: canvas contenant l'image
        """
        # La pause arrete tout déplacement
        if pause:
            canvas.after(10, lambda: self.moveTir(idt, canvas))
        else:
            # Si l'élément est toujours dans le canvas on continue le traitement sinon le thread se ferme
            if len(canvas.find_withtag(idt)) == 1:
                # Déplacement de l'objet
                canvas.move(idt, 10 + self.vague * 5, 0)
                # Récupération des coordonnées de l'image
                x, y = canvas.coords(idt)
                # Suppression de l'image a partir d'un point
                if x > canvas.winfo_width() - 250:
                    canvas.delete(idt)
                # tpl contient la liste de tous les éléments en collision dans le rectangle x,y/x,y+130
                tpl = canvas.find_overlapping(x, y, x, y + 130)

                # Vérifie si dans cette liste on retrouve un projectile et un ennemi
                if tagged("bullet", tpl, canvas) and tagged("uni", tpl, canvas):
                    # Actionnement du son d'un ennemi qui meurt
                    Sound("deaduni2.mp3", True).start()
                    # Change le tag de l'ennemi pour eviter d'autre collision
                    canvas.itemconfig(getIDfromTag("uni", tpl, canvas), image=dead, tags="dead")
                    # Suppression du projectile
                    canvas.delete(getIDfromTag("bullet", tpl, canvas))
                    # Mise à jour des PV
                    self.updatePV(1)
                    # Augmentation du score
                    self.hero.setScore(self.hero.getScore() + self.vague)
                    # Affichage du score
                    self.printScore()
                    # Mise à jour du nombre d'ennemis
                    self.updateEnnemies()

                else:
                    # Relance la fonction dans un thread toutes les 10ms
                    canvas.after(10, lambda: self.moveTir(idt, canvas))

    def updategif(self, idimg, canvas, img, img_offset=-1, time=-1, looptime=200, noloop=False):
        """
        Animation des gifs

        @param idimg: id tkinter de l'image
        @param canvas: canvas contenant l'image
        @param img: PhotoImage
        @param img_offset: image de dpart de l'animation
        @param time: si > 0 defini le nombre de boucle avant la destruction de l'image
        @param looptime: temps avant de realancer la boucle
        @param noloop: pas de boucle sur les image, l'image la plus "grande" est la derniere
        """
        # La pause bloque l'animation des gifs
        if pause:
            canvas.after(75, lambda: self.updategif(idimg, canvas, img, img_offset=img_offset, time=time,
                                                    looptime=looptime, noloop=noloop))
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
                    Sound("bulletsound.mp3", stop=True).start()
                    canvas.after(looptime,
                                 lambda: self.updategif(idimg, canvas, img, img_offset + 1, looptime=looptime,
                                                        noloop=True))

    def drawEnnemies(self):
        """
        Dessine l'image des ennemis sur les canvas
        @return:
        """
        # Pour chaque ligne/canvas
        for row in range(0, 5):
            # Décalage de l'image pour des postionnements pseudo-aléatoires
            offset = 20 + randint(0, 1000)
            # Supprime les reliquats
            self.canvas[row].delete("uni")

            # Creation des ennemis selon le nombre associé dans la liste rows
            for ent in range(self.rows[row]):
                idlic = self.canvas[row].create_image(self.canvas[row].winfo_width() + offset,
                                                      self.canvas[row].winfo_height() / 2, tag="uni")

                # Décalage suplémentaire à chaque itération d'un minimum de la taille de l'image
                offset += unicorn[0].width() + randint(0, 2000)

                # Lance le thread de déplacement des ennemis
                self.moveEnnemy(idlic, self.canvas[row])

                # Mise à jour du gif de l'ennemi
                self.updategif(idlic, self.canvas[row], unicorn, looptime=50)

    def moveEnnemy(self, idlic, canvas):
        """
        Boucle threadée déplaçant les ennemis
        @param idlic: id de l'objet tkinter
        @param canvas: canvas contenant l'objet tkinter
        @return:
        """
        # La pause arrete tout déplacement
        if pause:
            canvas.after(75, lambda: self.moveEnnemy(idlic, canvas))
        else:
            # Vérifie si le canvas contient toujours l'élémént sinon le thread se ferme
            if len(canvas.find_withtag(idlic)) == 1:
                # Si le joueur est mort, les enemis sont tués
                if self.hero.getPV() == 0:
                    canvas.delete(idlic)
                else:
                    # Déplacement selon la vague. Qaund la vague augmente le deplacement aussi
                    canvas.move(idlic, -30 - self.vague * 10, 0)

                    # Verifie si l'ennemi à dépassé la limite
                    x1, y = canvas.coords(idlic)
                    if x1 <= unicorn[0].width() / 2 + 20:
                        # Suppression de l'élément
                        canvas.delete(idlic)
                        # Mise à jour des PV
                        self.updatePV(-10)
                        # Activation du son d'un ennemi mort mais vainqueur
                        Sound("deaduni.mp3", stop=True).start()
                        # Mise à jour du compteur d'ennemis
                        self.updateEnnemies()

                    else:
                        # Commence le thread
                        canvas.after(75, lambda: self.moveEnnemy(idlic, canvas))

    def updatePV(self, pvDIFF):
        """
        Met à jour les point de vie du joueur
        @param pvDIFF: différence par rapport à sa vie actuelle
        @return:
        """
        # Mise à jour des pv de l'objet joueur
        self.hero.setPV(self.hero.getPV() + pvDIFF)
        pv = self.hero.getPV()

        # Mise à l'echelle suivant la taille de la barre de vie
        # 100 pv  =  barre de vie pleine
        pvscale = pv / 100 * self.hp_canvas.winfo_width()
        self.hp_canvas.delete("all")
        self.hp_canvas.create_rectangle(0, 0, pvscale, 50, fill="green")

        # En cas de défaite
        if pv <= 0:
            # pause du jeu
            self.pause()
            # Activation du curseur
            root.config(cursor="heart")
            # Apparition d'un dialogue demandant si le joeur veut recommencer ou non
            answer = askquestion("LOOSER !", "TRY AGAIN?")

            if answer == "yes":
                # Sauvegarde du score
                self.score.save(self.hero)
                # Disparition du curseur
                root.config(cursor="none")
                # C'est reparti
                self.init_game(fullreset=True)
            else:
                # Fin :(
                self.end()

    def resetPV_bar(self):
        """
        Remet à 0 la barre de vie
        @return:
        """
        self.hp_canvas.delete("all")
        self.hp_canvas.create_rectangle(0, 0, self.hp_canvas.winfo_width(), 50, fill="green")

    def update_background(self, canvas):
        """
        Mise à jour du fond
        @param canvas: canvas contenant le fond
        @return:
        """
        # La pause arrete tout déplacement
        if pause:
            canvas.after(50, lambda: self.update_background(canvas))
        else:
            # Deplace les éléments avec les tags star, planet et planet_cricle
            canvas.move('bg_star', -20 - self.vague * 5, 0)
            canvas.move('bg_planet', -2 - self.vague * 2, 0)
            canvas.move('bg_planet_circle', -2 - self.vague * 2, 0)

            # On récupere toutes les étoiles du canvas
            for star in canvas.find_withtag('bg_star'):
                x = canvas.coords(star)
                # Verifie le dépassement du canvas et les repositionne en bout du canvas
                if x[0] < 0:
                    canvas.delete(star)
                    x = canvas.winfo_width()
                    y = randint(0, canvas.winfo_height())
                    w = randint(1, 5)

                    canvas.create_oval(x, y, x + w, y + w, width=w, outline='white', tag="bg_star")

            # positionne les éléments en fond d'ecran
            canvas.tag_lower("bg_star")

            # On récupere tous les cercles de planete du canvas et on les détruits s'ils dépassent
            for circle in canvas.find_withtag('bg_planet_circle'):
                x = canvas.coords(circle)
                if x[0] < 0:
                    canvas.delete(circle)

            # Couleurs des planetes
            colors = ["DodgerBlue4", "MediumOrchid4", "firebrick4", "goldenrod"]

            # On récupere tous les  planete du canvas et on repositionnent aléatoirement celles qui dépassent du canvas
            for planet in canvas.find_withtag('bg_planet'):
                i = 0
                # 50% des planetes disparaissent
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
                        # ajout aléatoire d'un anneau ou non sur la planete
                        if rand % 2 == 0:
                            canvas.create_oval(x - w / 2, y + w / 2 - s, x + w * 1.50, y + w / 2 + s, width=2,
                                               outline=color,
                                               tag="bg_planet_circle")
                    i += 1

            # positionne les éléments en fond d'ecran
            canvas.tag_lower("bg_planet")
            canvas.tag_lower("bg_planet_circle")
            canvas.after(50, lambda: self.update_background(canvas))

    def end(self, event=None):
        """
        Quitte le programme
        @param event:
        @return:
        """
        # Pause
        self.pause()
        # Sauvegarde le score
        self.score.save(self.hero)
        exit(0)

    def pause(self, event=None, only=False):
        """
        Active/Desactive la pause et les liens de touches spécifiques
        @param event:
        @param only: Can only triffer pause but cannot unpause
        @return:
        """
        global pause
        if pause and not only:
            self.mouvements(True)
            self.eventTir(True)
            pause = False
        else:
            self.mouvements(False)
            self.eventTir(False)
            pause = True

    def help(self, event=None):
        """
        Active déactive l'aide des touches
        @param event:
        @return:
        """
        if len(self.canvas[0].find_withtag("help")) == 1:
            self.removeCommands()
        else:
            self.displayCommands()

    def displayCommands(self):
        """
        Affiche les commandes à l'écran
        @return:
        """
        font = tkFont.Font(family='Helvetica', size=36, weight='bold')

        texts = ["Press Enter to Start/Pause/UnPause", "Press ↑ or ↓ to Move", "Press Space to Attack",
                 "Press Escape to Quit", "Press H to display this", "Press Tab for highscores"]
        for i in range(5):
            self.canvas[i].create_text(self.canvas[0].winfo_width() / 2, self.canvas[0].winfo_height() / 2,
                                       text=texts[i], fill="Yellow", font=font, tag="help")
        self.canvas[0].create_text(self.canvas[0].winfo_width() / 2, self.canvas[0].winfo_height() -36,
                                   text=texts[5], fill="Yellow", font=font, tag="help")

    def removeCommands(self):
        """
        Supprime les commandes à l'ecran
        @return:
        """
        for canvas in self.canvas:
            canvas.delete(canvas.find_withtag("help")[0])

    def updateEnnemies(self):
        """
        Mise à jour du nombre d'ennemis restant et gère l'incrémentation des vagues
        @return:
        """
        self.ennemies -= 1
        if self.ennemies <= 0:
            self.vague += 1
            self.init_game()

    def displayScores(self, event=None):
        """
        Affiche les meilleurs scores
        @param event:
        @return:
        """
        # pause si besoin
        self.pause(only=True)
        # Creation et configuration de la fenetre au niveau supérieur
        higscores = tk.Toplevel(self.master)
        x = self.master.winfo_screenwidth()
        y = self.master.winfo_screenheight()
        root.config(cursor="heart")
        higscores.geometry("{}x{}+{}+{}".format(int(x / 3), int(y / 3), int(x / 2 - x / 6), int(y / 2 - y / 6)))
        higscores.overrideredirect(1)
        higscores.focus_set()

        # Ajout de lien avec les touches pour fermer la fenetre
        higscores.bind("<FocusOut>", lambda event: self.destroyHS(higscores))
        higscores.bind("<Escape>", lambda event: self.destroyHS(higscores))
        higscores.bind("<Tab>", lambda event: self.destroyHS(higscores))

        # Ecriture des informations
        tk.Label(higscores, image=bullet[10]).grid(row=0, column=0, sticky='W')
        tk.Label(higscores, image=bullet[10]).grid(row=0, column=1, sticky='E')

        font_title = tkFont.Font(family='Helvetica', size=36, weight='bold')

        title = tk.Label(higscores, text="Highscores", font=font_title, fg='white', bg="red")
        title.grid(row=0, column=0, columnspan=2)

        font_scores = tkFont.Font(family='Helvetica', size=15, weight='bold')
        scores = self.score.getSortedScores()
        for joueur, score in scores:
            label_joueur = tk.Label(higscores, text=joueur, font=font_scores, fg="blue", bd=1, relief="solid")
            label_score = tk.Label(higscores, text=score, font=font_scores, bd=1, relief="solid")
            label_joueur.grid(row=scores.index((joueur, score)) + 1, column=0, sticky="EW")
            label_score.grid(row=scores.index((joueur, score)) + 1, column=1, sticky="EW")

        tk.Grid.columnconfigure(higscores, 0, weight=1)
        tk.Grid.columnconfigure(higscores, 1, weight=1)

    def destroyHS(self, hs, event=None):
        """
        Destruction de la fenetre
        @param hs:
        @param event:
        @return:
        """
        hs.destroy()
        root.config(cursor="none")


root = tk.Tk()

# Gifs utilisés dans le jeu
unicorn = [tk.PhotoImage(file='gif/unireact.gif', format='gif -index %i' % i) for i in range(9)]
ship = [tk.PhotoImage(file='gif/vaisseau.gif', format='gif -index %i' % i) for i in range(4)]
bullet = [tk.PhotoImage(file='gif/bullet.gif', format='gif -index %i' % i) for i in range(12)]
dead = tk.PhotoImage(file='gif/dead.gif')

# Activation du mode Fullscreen
root.attributes("-fullscreen", True)

# Désactivation du curseur
root.config(cursor="none")

app = Application(master=root)
app.mainloop()
