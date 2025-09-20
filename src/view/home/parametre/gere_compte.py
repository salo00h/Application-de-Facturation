import tkinter as tk
from tkinter import messagebox

from const import *


class GereCompte():
    def __init__(self,root,canvas, frame_button,BDD,id_utilisateur):
        self.root = root
        self.canvas = canvas
        self.frame_button = frame_button
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur

        
        self.root.after(10, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)

        
    def initialisation(self):

        x = self.root.winfo_width()
        y = self.root.winfo_height()
        
        
        requt_compt = f"SELECT * FROM utilisateur WHERE ID = '{self.id_utilisateur}' ;"
        infos_compt =self.BDD.execute_requete(requt_compt)[0]
        self.votre_prenom = infos_compt[1]
        self.votre_nom = infos_compt[2]
        self.nom_utilisateur = infos_compt[3]
        self.mot_passe = infos_compt[4]
        self.teleph = infos_compt[5]
        

        self.fram_compte = tk.Frame(self.canvas,width=350, height=750, bg=COULEUR_LABEL)
        self.canvas.create_window(275,140 , anchor="n", window=self.fram_compte,tags="fram_compte")
        

        nom = tk.Label(self.fram_compte, text="Nom :",font=(POLICE, 10),bg=COULEUR_LABEL)
        nom.grid(row=0, column=0,padx=(15, 15), pady=(30, 10),sticky="w")
        self.entr_nom = tk.Entry(self.fram_compte,width=25, font=(POLICE, 10))
        self.entr_nom.grid(row=0, column=1, padx=(15, 15), pady=(30, 10),sticky="w")
        self.entr_nom.insert(0, self.votre_nom)

        prenom = tk.Label(self.fram_compte, text="Prénom :",font=(POLICE, 10),bg=COULEUR_LABEL)
        prenom.grid(row=1, column=0,padx=(15, 15), pady=(10, 10),sticky="w")
        self.entr_prenom = tk.Entry(self.fram_compte,width=25,font=(POLICE, 10))
        self.entr_prenom.grid(row=1, column=1, padx=(15, 15), pady=(10, 10),sticky="w")
        self.entr_prenom.insert(0, self.votre_prenom )

        user = tk.Label(self.fram_compte, text="Nom d'utilisateur ",font=(POLICE, 10),bg=COULEUR_LABEL)
        user.grid(row=2, column=0, padx=(15, 15), pady=(10, 10), sticky="w")
        self.username = tk.Entry(self.fram_compte,width=25,font=(POLICE, 10))
        self.username.grid(row=2, column=1, padx=(15, 15), pady=(10, 10), sticky="w")
        self.username.insert(0, self.nom_utilisateur )

        passe = tk.Label(self.fram_compte, text="Mot de passe ",font=(POLICE, 10),bg=COULEUR_LABEL)
        passe.grid(row=3, column=0,padx=(15, 15), pady=(10, 10), sticky="w")
        self.mot_de_passe = tk.Entry(self.fram_compte,width=25, font=(POLICE, 10))
        self.mot_de_passe.grid(row=3, column=1, padx=(15, 15), pady=(10,0), sticky="w")
        self.mot_de_passe.insert(0, self.mot_passe)

        """
        lab_show = tk.Label(self.fram_compte, text="voir ",font=(POLICE, 10),bg=COULEUR_LABEL)
        lab_show.grid(row=4, column=1,padx=(15, 40), pady=(0, 15), sticky="e")
        self.val_show = tk.IntVar()
        self.show = tk.Checkbutton(self.fram_compte, variable=self.val_show)
        self.show.grid(row=4, column=1, padx=(10, 15), pady=(0, 15), sticky="e")
        
        
        if (self.val_show.get()== 0):
            
            self.mot_de_passe.config(show="*")
            self.mot_de_passe.insert(0, "*" * len(self.mot_passe))
        else:
            self.mot_de_passe.config(show="")
            self.mot_de_passe.delete(0, tk.END)
            self.mot_de_passe.insert(0, self.mot_passe)
        """
        telephone = tk.Label(self.fram_compte, text="Numéro de telephone :",font=(POLICE, 10),bg=COULEUR_LABEL)
        telephone.grid(row=5, column=0,padx=(15, 15), pady=(10, 60),sticky="w")
        self.tel = tk.Entry(self.fram_compte,width=25, font=(POLICE, 10))
        self.tel.grid(row=5, column=1,padx=(15, 15), pady=(5, 60), sticky="w")
        self.tel.insert(0, self.teleph)

        #self.show.bind("<Button-1>",lambda event: self.show_motpassa())
        self.button_anul = tk.Button(self.fram_compte, text="Fermer", command=lambda:self.fermer(),
                                        bg=COULEUR_PRINCIPALE,font=(POLICE, 11))
        self.button_anul.grid(row=6, column=0,padx=(210, 0), pady=(10, 20), sticky="w")

        self.button_supprim = tk.Button(self.fram_compte, text="Supprimer Compte", command=lambda:self.supprime(),
                                        bg=COULEUR_CANVAS,font=(POLICE, 11))
        self.button_supprim.grid(row=6, column=0,padx=(10, 10), pady=(10, 20), sticky="w")

        self.button_ensrigst = tk.Button(self.fram_compte, text="Enregistrer", command=lambda: self.save(),
                                        bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON,font=(POLICE, 11))
        self.button_ensrigst.grid(row=6, column=1,padx=(0, 15), pady=(10, 20), sticky="e")

        

        


    def save(self):
        if ( self.entr_prenom.get() != self.votre_prenom ):
            requt = f"UPDATE utilisateur SET prenom = '{self.entr_prenom.get()}' WHERE ID = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if (self.entr_nom.get() != self.votre_nom ):
            requt = f"UPDATE utilisateur SET nom = '{self.entr_nom.get()}' WHERE ID = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if (self.username.get() != self.nom_utilisateur):
            requt = f"UPDATE utilisateur SET nom_utilisateur = '{self.username.get()}' WHERE ID = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if (self.mot_de_passe.get() != self.mot_passe):
            requt = f"UPDATE utilisateur SET mot_passe = '{self.mot_de_passe.get()}' WHERE ID = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if (self.tel.get() != self.teleph):
            requt = f"UPDATE utilisateur SET tel = '{self.tel.get()}' WHERE ID = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        self.fram_compte.destroy()

    def supprime(self):
        reponse = tk.messagebox.askquestion("Question", "Êtes-vous sûr de vouloir supprimer votre compte ?")
        if reponse == 'yes':
            delet_fact_compt = f"DELETE FROM facture WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(delet_fact_compt)

            delet_client_compt = f"DELETE FROM client WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(delet_client_compt)

            delete_entrpeise_compt = f"DELETE FROM  entreprise WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(delete_entrpeise_compt)

            delet_compte = f"DELETE FROM utilisateur WHERE ID = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(delet_compte)

        

        self.fram_compte.destroy()
        self.canvas.destroy()
        self.frame_button.destroy
        self.root.event_generate("<<retour_login_clicked>>")

    def fermer(self):
        self.fram_compte.destroy()
    """
    def show_motpassa(self, event=None):
        if (self.val_show.get()== 0):
            print(self.val_show)
            #self.mot_de_passe.config(show="*")
            self.mot_de_passe.insert(0, "*" * len(self.mot_passe))
        else:
            self.mot_de_passe.config(show="")
            self.mot_de_passe.delete(0, tk.END)  # Supprime tout le texte
            self.mot_de_passe.insert(0, self.mot_passe)  # Insère le contenu de self.mot_passe
    """

        
    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))