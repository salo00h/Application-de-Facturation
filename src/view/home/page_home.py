import os
import tkinter as tk

from const import *
from view.home.facture.history_fact import HistoryFacture
from view.home.devis.history_devis import Devis
from view.home.client.client import Client
from view.home.parametre.parametre import Parametre

"""
"""
class Home:
    def __init__(self, root,BDD, id_utilisateur):
        self.root = root
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur

        self.list_button = []

        self.root.after(10, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)
        self.root.bind("<<retour_history_fact>>", lambda event: self.retour_history_fact())
        self.root.bind("<<retour_page_client>>", lambda event: self.retour_page_client())
        self.root.bind("<<retour_page_devis>>", lambda event: self.retour_page_devis())



    def initialisation(self):
        long = self.root.winfo_width()
        haut = self.root.winfo_height()
        
        self.frame_button = tk.Frame(self.root, width=long, height=(haut // 11.42), bg=COULEUR_BOUTON)
        self.frame_button.grid_propagate(False)  # Empêcher le frame de redimensionner ses cellules
        self.frame_button.place(x=0, y=0)
        for i in range(5) :
            button = tk.Button(self.frame_button, width=20, height=3,bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON, font=(POLICE, 10,"bold"),anchor="center")
            if(i==0):
                button.grid(row=0, column=i,padx=(190,5), pady=(6,4), sticky="w")
            else:
                button.grid(row=0, column=i,padx=(5,5), pady=(6,4), sticky="w")
            self.list_button.append(button)
        #preciser les noms et commandes des button
        self.list_button[0].config(text="Facture", command=lambda:self.facture() )
        self.list_button[1].config(text="Devis", command=lambda: self.devis())
        self.list_button[2].config(text="Clients", command=lambda:self.client())
        self.list_button[3].config(text="Paramètres", command=lambda: self.parametre())
        self.list_button[4].config(text="Se Déconnecter", command=lambda: self.deconnecter())

        self.button_active = 0 #on utilise ce variable pour visualiser au utilisateur quel page est ouvert ( puisque on a 5 pages )

        # Créer un Canvas( ce canvas va placer en sous du frame qui contien les button des pages )
        self.canvas_home = tk.Canvas(self.root, width=long, height=haut,bg=COULEUR_PRINCIPALE)
        self.canvas_home.place(x=0, y=(haut // 11.42))


        
    def on_configure(self, event):
        if (self.canvas_home) and (self.frame_button):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()

            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)
            self.canvas_home.config(width=long, height=haut)
            self.canvas_home.place(x=0, y=(haut // 11.42))


    # ici on a tous les fonction des page chage fonction s'occupe le changment du page , et le page ouvert le couleur de button sera orange

    def facture(self):
        """on change le couluer de button active juste pour montrer que c'est lui activé """
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[0].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 0 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button 
        self.canvas_home.destroy()
        HistoryFacture(self.root,self.frame_button,self.BDD, self.id_utilisateur) #defini dans fichier(history_fact.py) qu'est dans repertoire [facture]
        

    def devis(self):
        """on change le couluer de button active juste pour montrer que c'est lui activé """
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[1].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 1 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button
        
        self.canvas_home.destroy()
        Devis(self.root,self.frame_button,self.BDD, self.id_utilisateur)

    def client(self):
        """on change le couluer de button active juste pour montrer que c'est lui activé """
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[2].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 2 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button
        self.canvas_home.destroy()
        Client(self.root,self.frame_button,self.BDD, self.id_utilisateur) #defini dans fichier client , qui existe dans repertoir client 

        
    def parametre(self):
        """on change le couluer de button active juste pour montrer que c'est lui activé """
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[3].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 3 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button
        self.canvas_home.destroy()
        Parametre(self.root,self.frame_button,self.BDD, self.id_utilisateur) #defini dans gere_compte.py

    def deconnecter(self):
        reponse = tk.messagebox.askquestion("Question", "Voulez-vous déconnecter ? ?")
        if reponse == 'yes':
            self.canvas_home.destroy()
            self.frame_button.destroy
            self.root.event_generate("<<retour_login_clicked>>")
        


    #fonctions des event de retour arier 
    def retour_history_fact(self,event=None):
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[0].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 0 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button 
        self.canvas_home.destroy()
        HistoryFacture(self.root,self.frame_button,self.BDD, self.id_utilisateur) #defini dans fichier(history_fact.py) qu'est dans repertoire [facture]
        
    def retour_page_client(self, event=None):
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[2].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 2 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button
        self.canvas_home.destroy()
        Client(self.root,self.frame_button,self.BDD, self.id_utilisateur) #defini dans fichier client , qui existe dans repertoir client 

    def retour_page_devis(self, event=None):
        self.list_button[self.button_active].config(bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON)
        self.list_button[1].config(bg=COULEUR_TEXT_BOUTON,fg=COULEUR_BOUTON)
        self.button_active = 1 # garde le num de button active acutule , pour que si on change le page , on retour la couleur de ce button
        
        self.canvas_home.destroy()
        Devis(self.root,self.frame_button,self.BDD, self.id_utilisateur)