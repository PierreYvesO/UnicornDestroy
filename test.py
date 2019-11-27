from tkinter import *

Box = Tk()
Frame = Canvas(Box, height = 500, width = 500, bg = "darkblue")

d = "R"

Enemy = Frame.create_rectangle(10, 60, 50, 80, fill = "red", tag = "e1")
Enemy2 = Frame.create_rectangle(60, 60, 100, 80, fill = "red", tag = "e2")
Enemy3 = Frame.create_rectangle(110, 60, 150, 80, fill = "red", tag = "e3")
Enemy4 = Frame.create_rectangle(160, 60, 200, 80, fill = "red", tag = "e4")
Enemy5 = Frame.create_rectangle(210, 60, 250, 80, fill = "red", tag = "e5")
Enemy6 = Frame.create_rectangle(260, 60, 300, 80, fill = "red", tag = "e6")
Enemy7 = Frame.create_rectangle(310, 60, 350, 80, fill = "red", tag = "e7")
Enemy8 = Frame.create_rectangle(360, 60, 400, 80, fill = "red", tag = "e8")

Bullet = Frame.create_oval(10, 400, 20, 410, fill = "green", tag = "bullet")

Player = Frame.create_rectangle(230, 400, 270, 430, fill = "black", tag = "player")

Alive = [Enemy, Enemy2, Enemy3, Enemy4, Enemy5, Enemy6, Enemy7, Enemy8]
Dead = []

def enemy_move():
    global d
    side = "middle"
    #x1, y1, x2, y2
    for i in Alive:
        if Frame.coords(i)[2] >= 500:
            side = "right"
            #for a in Alive:
             #   Frame.move(a, -1, 15)
            d = "L"
        elif Frame.coords(i)[0] <= 0:
            side = "left"
            #for a in Alive:
            #    Frame.move(a, 1, 15)
            d = "R"
        else:
            side == "middle"
            #if d == "L":
             #   for a in Alive:
              #      Frame.move(a, -1, 0)
            #elif d == "R":
             #   for a in Alive:
              #      Frame.move(a, 1, 0)
    if side == "middle":
        for i in Alive:
            if d == "L":Frame.move(i, -10, 0)
            elif d == "R":Frame.move(i, 10, 0)
    elif side == "right":
        for i in Alive:Frame.move(i, -10, 15)
    elif side == "left":
        for i in Alive:Frame.move(i, 10, 15)
    Frame.after(100, enemy_move)

def gameOver():
    Frame.configure(background = "black")
    for i in Alive:Frame.itemconfig(i, fill = "black")
    for i in Dead:Frame.itemconfig(i, fill = "black")
    Frame.itemconfig(Bullet, fill = "black")

def kill():
    for i in Alive:
        if Frame.coords(i)[0] <= Frame.coords(Bullet)[0] and Frame.coords(i)[1] <= Frame.coords(Bullet)[1] and Frame.coords(i)[2] >= Frame.coords(Bullet)[2] and Frame.coords(i)[3] >= Frame.coords(Bullet)[3]:
            Alive.remove(i)
            Frame.itemconfig(i, fill = "yellow")
            Dead.append(i)
            print(Frame.find_overlapping(Frame.coords(i)[0],Frame.coords(i)[1],Frame.coords(i)[2],Frame.coords(i)[3]))
    Frame.after(1, kill)

#def death():
 #   for i in Alive:
  #      if Frame.find_overlapping(Frame.coords(i)) 
        #if Frame.coords(i)[0]<= Frame.coords(Player)[0] and Frame.coords(i)[2] >= Frame.coords(Player)[0] and Frame.coords(i)[0]<= Frame.coords(Player)[2] and Frame.coords(i)[2] >= Frame.coords(Player)[2] and Frame.coords(i)[0]<= Frame.coords(Player)[1] and Frame.coords(i)[3] >= Frame.coords(Player)[1] and Frame.coords(i)[1]<= Frame.coords(Player)[3] and Frame.coords(i)[3] >= Frame.coords(Player)[3]:
         #   gameOver()
   # Frame.after(1, death)
#x1,y1,x2,y2

def up(event):Frame.move(Bullet, 0, -20)
def down(event):Frame.move(Bullet, 0, 20)
def right(event):Frame.move(Bullet, 20, 0)
def left(event):Frame.move(Bullet, -20, 0)

Frame.bind('<Right>', right)
Frame.bind('<Left>', left)
Frame.bind('<Up>', up)
Frame.bind('<Down>', down)

      

Frame.after(1000,enemy_move)
Frame.after(1000, kill)
#Frame.after(1000, death)
Frame.focus_set()
Frame.pack()
Box.mainloop()
