import tkinter as tk
import os


from const import *
from tkinter import messagebox
from view.login_page.creer_compt import CreeCompte
from model.basse_donnes import BaseDeDonnee
from view.home.page_home import Home

class Login:
    def __init__(self, root,BDD):
        self.root = root
        self.BDD = BDD
        
        self.canvas = None
        
        self.root.after(100, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)


    def initialisation(self):
        # Maintenant, récupérez les dimensions de la fenêtre après qu'elle ait été affichée
        self.largeur = self.root.winfo_width()
        self.hauteur = self.root.winfo_height()
        #on calcule les coordonne de centre canvas pour mettre le frame 
        x = int((self.largeur ) / 2)
        y = int((self.hauteur) / 2)
        # Création du canvas et du frame avec les dimensions récupérées
        self.cree_canvas()
        self.cree_frame(x,y)


    def cree_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.largeur, height=self.hauteur)
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def cree_frame(self,x,y):
        self.frame_login = tk.Frame(self.canvas, bg=COULEUR_CANVAS)
        self.canvas.create_window(x, y, window=self.frame_login, anchor="center")
        # Création des widgets
        self.label_username = tk.Label(self.frame_login, text=" Email :",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.entry_username = tk.Entry(self.frame_login)
        self.label_password = tk.Label(self.frame_login, text="Mot de passe :",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.entry_password = tk.Entry(self.frame_login, show="*")
        self.button_login = tk.Button(self.frame_login, text="Se connecter", command=self.login,width=30, height=2,
                                        bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON,font=(POLICE, 11))
        self.button_create_account = tk.Button(self.frame_login, text="Créer un compte", command=self.create_account,width=30, height=2,
                                        bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON,font=(POLICE, 11))

        # Placement des widgets dans le frame
        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.button_login.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.button_create_account.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")


    def on_configure(self, event):
        if self.canvas and str(self.canvas.winfo_exists()) == "1":
            # Recalculer les dimensions de la fenêtre
            self.largeur = self.root.winfo_width()
            self.hauteur = self.root.winfo_height()

            self.canvas.config(width=self.largeur, height=self.hauteur)

            if self.frame_login and str(self.frame_login.winfo_exists()) == "1":
                x = int(self.root.winfo_width() / 2.7)
                y = int(self.root.winfo_height() / 2.8)
            self.frame_login.place(x=x, y=y)


    def login(self):
        # Méthode à exécuter lorsque le bouton "Se connecter" est cliqué
        username = self.entry_username.get()
        password = self.entry_password.get()
        requete = f"SELECT nom_utilisateur,mot_passe FROM utilisateur WHERE nom_utilisateur = '{username}';"
        verifie_compt = self.BDD.execute_requete(requete)
    
        if(len(verifie_compt) == 0):
            messagebox.showerror("Erreur", "Désolé, ce nom d'utilisateur n'existe pas. Vous devez créer un compte.")
        elif(str(password) != str(verifie_compt[0][1])):
            messagebox.showerror("Erreur", "Mot de passe incorrect")
        else:
            self.canvas.destroy()
            id_utilisateur = int(self.BDD.execute_requete(f"SELECT ID FROM utilisateur WHERE nom_utilisateur = '{username}';")[0][0])
            #on prend l'ID d'utilisatuer pour relier tous les traveil dans avec ce ID 
            Home(self.root,self.BDD, id_utilisateur) #defini dans fichier (page_home.py)
        
    def create_account(self):
        self.frame_login.destroy()
        CreeCompte(self.root,self.canvas,self.BDD) #defini dans fichier ( cree_compt.py )


