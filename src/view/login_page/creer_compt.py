import tkinter as tk
import os


from const import *
from tools.event_entry import effacer_indicatif , reste_indicatif
from model.basse_donnes import BaseDeDonnee
from tkinter import messagebox


class CreeCompte():
    def __init__(self,root,canvas,BDD):
        self.root = root
        self.canvas = canvas
        self.BDD = BDD

        
        self.root.bind("<Configure>", self.on_configure)
        
        self.mini_page()
        
        #ajoute les event <Foucs In> pour les entry 
        self.prenom.bind("<FocusIn>", lambda event: effacer_indicatif(self.prenom,"Prénom"))
        self.nom.bind("<FocusIn>", lambda event: effacer_indicatif(self.nom, "Nom") )
        self.username.bind("<FocusIn>", lambda event: effacer_indicatif(self.username,"@gmail.com") )
        self.tel.bind("<FocusIn>", lambda event: effacer_indicatif(self.tel,"+33"))

        
    def mini_page(self):
        self.compt_frame = tk.Frame(self.root,width=350, height=750, bg=COULEUR_CANVAS)
        
        x = ((self.root.winfo_width() - 350) // 2)# Coordonnée x de la fenêtre fille
        y = ((self.root.winfo_height() - 750) // 2)

        self.compt_frame.place(x=x//2, y=y//2)


        self.new_canvas = tk.Canvas(self.compt_frame, width=350, height=750, bg=COULEUR_CANVAS)
        self.new_canvas.pack()


        # Création des widgets[ label ]
        self.nom = tk.Label(self.new_canvas, text="Nom ",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.nom.grid(row=0, column=0,padx=(20, 0), pady=(30, 0),sticky="w")
        self.user = tk.Label(self.new_canvas, text="Choisissez votre nom d'utilisateur ",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.user.grid(row=2, column=0, columnspan=2,padx=(20, 0), pady=(30, 0), sticky="w")
        self.passe = tk.Label(self.new_canvas, text="Créez un mot de passe ",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.passe.grid(row=4, column=0,columnspan=2,padx=(20, 0), pady=(30, 0), sticky="w")
        self.passe_conf = tk.Label(self.new_canvas, text="Confirmez votre mot de passe  ",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.passe_conf.grid(row=6, column=0,columnspan=2,padx=(20, 0), pady=(30, 0),sticky="w")
        self.telephone = tk.Label(self.new_canvas, text="Numéro de telephone mobile  ",font=(POLICE, 10),bg=COULEUR_CANVAS)
        self.telephone.grid(row=8, column=0,columnspan=2,padx=(20, 0), pady=(30, 0),sticky="w")

        self.entry_info()
        
        
        self.button_ensrigst = tk.Button(self.new_canvas, text="Enregistrer", command=lambda: self.save(),
                                        bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON,font=(POLICE, 11))
        self.button_ensrigst.grid(row=10, column=1,padx=(20, 10), pady=(20, 10), sticky="e")

        self.button_anul = tk.Button(self.new_canvas, text="Annuler", command=lambda:self.annule(),
                                        bg=COULEUR_PRINCIPALE,fg=COULEUR_BOUTON,font=(POLICE, 11))
        self.button_anul.grid(row=10, column=0,padx=(20, 10), pady=(20, 10), sticky="w")

        
    def entry_info(self):
        self.prenom = tk.Entry(self.new_canvas,fg="gray")
        self.prenom.grid(row=1, column=0, padx=(20, 0), pady=(0, 30),sticky="w")
        self.prenom.insert(0, "Prénom")
        

        self.nom = tk.Entry(self.new_canvas,fg="gray")
        self.nom.grid(row=1, column=1,padx=(15,20), pady=(0, 30), sticky="w")
        self.nom.insert(0, "Nom")

        self.username = tk.Entry(self.new_canvas,width=30,fg="gray")
        self.username.grid(row=3, column=0,columnspan=2,padx=(20, 0), pady=(0, 30), sticky="w")
        self.username.insert(1, "@gmail.com")

        self.mot_de_passe = tk.Entry(self.new_canvas,width=30, fg=COULEUR_BOUTON ,show="*")
        self.mot_de_passe.grid(row=5, column=0,columnspan=2, padx=(20, 0), pady=(0, 30), sticky="w")

        self.confirm_passe = tk.Entry(self.new_canvas, width=30,fg=COULEUR_BOUTON,show="*")
        self.confirm_passe.grid(row=7, column=0,columnspan=2,padx=(20, 0), pady=(0, 30), sticky="w")

        self.tel = tk.Entry(self.new_canvas,width=30,fg="gray")
        self.tel.grid(row=9, column=0,columnspan=2,padx=(20, 0), pady=(0, 60), sticky="w")
        self.tel.insert(0, "+33")



    

    def save(self):
        
        """on verifie d'abord que l'utilisature bien entrer tous les ionfos necissaire"""
        prenom_text = self.prenom.get()  # Obtenir le texte du champ Prénom et supprimer les espaces
        nom_text = self.nom.get()  # Obtenir le texte du champ Nom et supprimer les espaces
        username_text = self.username.get() # Obtenir le texte du champ Nom d'utilisateur et supprimer les espaces
        mot_de_passe_text = self.mot_de_passe.get()  # Obtenir le texte du champ Mot de passe et supprimer les espaces
        confirm_passe_text = self.confirm_passe.get()  # Obtenir le texte du champ Confirmation de mot de passe et supprimer les espaces
        tel_text = self.tel.get()  # Obtenir le texte du champ Téléphone et supprimer les espaces


        if prenom_text and nom_text and username_text and mot_de_passe_text and confirm_passe_text and tel_text:
            requete = f"SELECT nom_utilisateur FROM utilisateur WHERE nom_utilisateur = '{username_text}';"
            deja_exist = self.BDD.execute_requete(requete)

            if(len(deja_exist)!=0 ):
                messagebox.showerror("Erreur", "Désolé, ce nom d'utilisateur existe déjà.")

            elif( mot_de_passe_text != confirm_passe_text) :
                """on verifie bein qu'il a bien creer le mot de passe , sinon on affiche message ereure"""
                
                messagebox.showerror("Erreur", "Le mot de passe de confirmation est différent du mot de passe initial.")
            else:
                requete = f"INSERT INTO utilisateur (prenom, nom, nom_utilisateur, mot_passe, tel) \
                            VALUES ('{prenom_text}','{nom_text}','{username_text}','{mot_de_passe_text}','{tel_text}')"
                self.BDD.execute_requete(requete)
                self.compt_frame.destroy()
                self.root.event_generate("<<retour_login_clicked>>")

        else:
            messagebox.showerror("Erreur","Attention, il est obligatoire de remplir correctement toutes les cases.")


        



    def annule(self):
        self.compt_frame.destroy()
        self.root.event_generate("<<retour_login_clicked>>")
    

    def on_configure(self, event):
        if self.compt_frame:

            self.canvas.config(width=self.root.winfo_width(), height=self.root.winfo_height())
            
            x = int(self.root.winfo_width() / 2.7)
            y = int(self.root.winfo_height() / 5.8)
            self.compt_frame.place(x=x, y=y)