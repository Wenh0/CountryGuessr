from tkinter import *
import customtkinter
import random
import math
import csv
import time
from drapeaux import crunch

# fenetre initialisee
customtkinter.set_appearance_mode("System")
root = customtkinter.CTk()
root.title("Devine le pays !")
root.geometry("700x500")
root.resizable(False,False)
root.iconbitmap("flag.ico")

# variables
paysAleatoire = {}
scoreCount = 0
nom_colonnes = []
started = False
pays_joues = []
tours = 0

def csv_toData():
    nom_colonnes = []
    donnee = []
    listePays = []
    with open("donnees.csv", 'r') as f:
        obj = csv.DictReader(f)
        for i in obj:
            donnee.append(i['nom'])
            listePays.append(i['nom'])
            donnee.append(i['x'])
            donnee.append(i['y'])
            nom_colonnes.append(donnee)
            donnee = []
            print(i['nom'], i['x'], i['y'])
    print(listePays)
    print(nom_colonnes)
    commencer(nom_colonnes)
    return listePays, nom_colonnes

# objets de base sur la fenetre
Game = Canvas(root, width=500, height=500, bg="white")
Game.pack(anchor=NE)

image = PhotoImage(file="europemap2.png")
Game.create_image(0, 0, image = image, anchor=NW)

pays = Entry(root, width=20)
pays.place(x=30, y=30)

score = customtkinter.CTkLabel(root, text="0", font=("Arial", 20))
score.place(x=70, y=300)

message = customtkinter.CTkLabel(root, text="Commencez à jouer", font=("Arial",22))
message.place(x=50, y=200)

resultat = customtkinter.CTkLabel(root, text="")
resultat.place(x=50, y=100)

# fonctions
def coord(eventorigin):
    global x0,y0
    x0 = eventorigin.x
    y0 = eventorigin.y
    print(x0,y0)

#Game.bind("<Button 1>",coord)

def commencer(nom_colonnes):
    global Game, paysAleatoire, image, started, tours
    started = True
    paysAleatoire = nom_colonnes[random.randint(0,41)]
    if len(pays_joues) <= 41:
        if paysAleatoire[0] in pays_joues:
            commencer(nom_colonnes)
        else:
            print(paysAleatoire[0])
            pays_joues.append(paysAleatoire[0])
            Game.delete('all')
            Game.create_image(0, 0, image=image, anchor=NW)
            Game.create_rectangle(int(paysAleatoire[1]), int(paysAleatoire[2]), int(paysAleatoire[1])+5, int(paysAleatoire[2])+5, fill='black')
            tours += 1
    else:
        fin()
    return paysAleatoire, nom_colonnes, tours

def fin():
    global scoreCount
    resultat.configure(text=f"Bravo ! votre score est de {(scoreCount/41)*100}%")
    
def isTrue(event):
    global paysAleatoire
    if tours<=40:
        if pays.get() == paysAleatoire[0]:
            print("oui")
            pays.delete(0, END)
            message.configure(text="continuez comme ça !")
            scoreUpdate(1)
        else:
            print("non")
            pays.delete(0, END)
            message.configure(text=f"Faux ! c'était le/la {paysAleatoire[0]}")
            scoreUpdate(-1)        
root.bind("<Return>",isTrue)

def scoreUpdate(ajout):
    global score, scoreCount, nom_colonnes
    scoreCount += ajout
    score.configure(text=str(scoreCount))
    csv_toData()
    return scoreCount

csv_toData()
crunch()
root.mainloop()