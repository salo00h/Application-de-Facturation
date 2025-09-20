import tkinter as tk
import webbrowser #pour visualiser l'addres postal de client sur google maps
from tkinter import messagebox

from const import *
from tools.event_entry import effacer_indicatif


class VoirClient():
    def __init__(self, root,canvas, frame_button, BDD, id_utilisateur,nuplet_client):
        self.root = root
        self.canvas = canvas
        self.frame_button = frame_button
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur
        self.nuplet_client = nuplet_client # contien tous infos de client qu'est danr table basse donnes ,,

        
        self.root.bind("<Configure>", self.on_configure)
        
        self.voir_infos()
        self.lien_google_maps.bind("<Button-1>",lambda event: self.ouvrir_google_maps(self.adr))
        
    def voir_infos(self):
        num_cl = self.nuplet_client[0]
        num = tk.Label(self.canvas, text=f"Numéro :       {num_cl}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(350, 80 , anchor="n", window=num,tags="num")

        nom_cl = self.nuplet_client[1]
        nom = tk.Label(self.canvas, text=f"Nom :       {nom_cl}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(350, 120 , anchor="n", window=nom,tags="nom")

        pren_cl = self.nuplet_client[2]
        prenom = tk.Label(self.canvas, text=f"Prénom :       {pren_cl}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(350, 160 , anchor="n", window=prenom,tags="prenom")
        
        self.adr = self.nuplet_client[3]
        adres = tk.Label(self.canvas, text=f"Adresse :       {self.adr}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(500, 200 , anchor="n", window=adres,tags="adres")
        self.lien_google_maps = tk.Label(self.canvas, text="Voir sur Google Maps",bg=COULEUR_PRINCIPALE, fg="blue")
        self.canvas.create_window(570, 220 , anchor="n", window=self.lien_google_maps,tags="lien_adres")
        
        
        fix = self.nuplet_client[4]
        fixe = tk.Label(self.canvas, text=f"Tél. fixe  :       {fix}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(350, 240 , anchor="n", window=fixe,tags="fixe")
        
        mob = self.nuplet_client[5]
        mobile = tk.Label(self.canvas, text=f"Mobile  :       {mob}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(350, 280 , anchor="n", window=mobile,tags="mobile")
        
        coment = self.nuplet_client[6]
        comentair = tk.Label(self.canvas, text=f"Comentaire  :       {coment}",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(350, 370 , anchor="n", window=comentair,tags="nom")
        
        self.button_anul = tk.Button(self.canvas, text="OK", command=lambda:self.annule(),
                                        bg=COULEUR_PRINCIPALE,fg=COULEUR_BOUTON,font=(POLICE, 13))
        self.canvas.create_window(500, 420 , anchor="n", window=self.button_anul,tags="button_anul")


        
    
    def annule(self):
        self.canvas.delete("all")
        self.root.event_generate("<<retour_page_client>>")
    
    def ouvrir_google_maps(self, adresse,event=None):
        lien_google_maps = f"https://www.google.com/maps/search/?api=1&query={adresse}"
        webbrowser.open(lien_google_maps)


    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))