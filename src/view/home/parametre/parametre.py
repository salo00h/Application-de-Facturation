import tkinter as tk
from tkinter import messagebox

from const import *
from view.home.parametre.gere_compte import GereCompte
from view.home.parametre.donne_entrprise import GereEntrprise

class Parametre():
    def __init__(self,root,frame_button,BDD,id_utilisateur):
        self.root = root
        self.frame_button = frame_button
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur

        self.canvas = None
        self.root.after(10, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)

        
    def initialisation(self):

        x = self.root.winfo_width()
        y = self.root.winfo_height()
        self.canvas = tk.Canvas(self.root, width=x, height=y,bg=COULEUR_PRINCIPALE)
        self.canvas.place(x=0, y=(y//11.42))

        
        self.compte = tk.Button(self.canvas, width=20, height=3,text="MON COMPTE", command=lambda:self.mon_compte() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 12,"bold"))
        self.canvas.create_window(290,60 , anchor="n", window=self.compte,tags="compte")
        
        self.entreprise = tk.Button(self.canvas, width=25, height=3,text="DONNEES ENTREPRISE", command=lambda:self.donnees_entrpris() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(890,60 , anchor="n", window=self.entreprise,tags="entreprise")

        self.retour = tk.Button(self.canvas, width=10, height=2,text="RETOUR", command=lambda:self.retour_arrier() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(580,730 , anchor="n", window=self.retour,tags="retour")

    def mon_compte(self):
        GereCompte(self.root,self.canvas, self.frame_button, self.BDD, self.id_utilisateur)

    def donnees_entrpris(self):
        GereEntrprise(self.root,self.canvas, self.frame_button, self.BDD, self.id_utilisateur)

    def retour_arrier(self):
        self.canvas.destroy()
        self.root.event_generate("<<retour_history_fact>>")

    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))