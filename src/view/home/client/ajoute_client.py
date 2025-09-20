import tkinter as tk
from tkinter import messagebox

from const import *
from tools.event_entry import effacer_indicatif, effacer_Text_indicatif



class AjouteClient():
    def __init__(self, root,canvas, frame_button, BDD, id_utilisateur,nuplet_client=None):
        self.root = root
        self.canvas = canvas
        self.frame_button = frame_button
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur
        self.nuplet_client = nuplet_client # contien tous infos de client qu'est danr table basse donnes ,,
        #on utilse cela juste dans cas modifier client.

        
        self.root.bind("<Configure>", self.on_configure)
        
        self.ajoute_infos()
        
        
    def ajoute_infos(self):
        num = tk.Label(self.canvas, text="Numéro ",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 80 , anchor="n", window=num,tags="num")
        self.entr_num = tk.Entry(self.canvas,font=(POLICE, 10),width=30)
        self.canvas.create_window(350, 80 , anchor="n", window=self.entr_num,tags="entr_num")
        

        nom = tk.Label(self.canvas, text="Nom ",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 120 , anchor="n", window=nom,tags="nom")
        self.entr_nom = tk.Entry(self.canvas,font=(POLICE, 10),width=30)
        self.canvas.create_window(350, 120 , anchor="n", window=self.entr_nom,tags="entr_nom")
        

        prenom = tk.Label(self.canvas, text="Nom ",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 160 , anchor="n", window=prenom,tags="prenom")
        self.entr_prenom = tk.Entry(self.canvas,font=(POLICE, 10), width=30)
        self.canvas.create_window(350, 160 , anchor="n", window=self.entr_prenom,tags="entr_prenom")
        

        adres = tk.Label(self.canvas, text="Adresse ",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 200 , anchor="n", window=adres,tags="adres")
        self.entr_adres = tk.Text(self.canvas,width=50,height=3, font=(POLICE, 10))
        self.canvas.create_window(430, 200 , anchor="n", window=self.entr_adres,tags="entr_adres")
        

        fixe = tk.Label(self.canvas, text="Tél. fixe",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 290 , anchor="n", window=fixe,tags="fixe")
        self.entr_fixe = tk.Entry(self.canvas,width=30,font=(POLICE, 10))
        self.canvas.create_window(350, 290 , anchor="n", window=self.entr_fixe,tags="entr_fixe")
        

        mobile = tk.Label(self.canvas, text="Mobile ",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 330 , anchor="n", window=mobile,tags="mobile")
        self.entr_mobil = tk.Entry(self.canvas,width=30,font=(POLICE, 10))
        self.canvas.create_window(350, 330 , anchor="n", window=self.entr_mobil,tags="entr_mobil")
        

        comentair = tk.Label(self.canvas, text="Comentaire ",font=(POLICE, 10),bg=COULEUR_PRINCIPALE)
        self.canvas.create_window(150, 370 , anchor="n", window=comentair,tags="nom")
        self.entr_comentair = tk.Text(self.canvas,width=50,height=5, font=(POLICE, 10))
        self.canvas.create_window(430, 370 , anchor="n", window=self.entr_comentair,tags="entr_comentair")
        
        
        
        self.button_ensrigst = tk.Button(self.canvas, text="Enregistrer", command=lambda: self.save(),
                                        bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON,font=(POLICE, 13))
        self.canvas.create_window(450, 520 , anchor="n", window=self.button_ensrigst,tags="button_ensrigst")

        self.button_anul = tk.Button(self.canvas, text="Annuler", command=lambda:self.annule(),
                                        bg=COULEUR_PRINCIPALE,fg=COULEUR_BOUTON,font=(POLICE, 13))
        self.canvas.create_window(320, 520 , anchor="n", window=self.button_anul,tags="button_anul")


        self.num_client = int(self.BDD.execute_requete(f"SELECT COUNT(*) AS nombre_de_lignes FROM client;")[0][0])

        if( self.nuplet_client != None):
            #dans cas modifier , on affiche l'encien infos
            num_cl = self.nuplet_client[0]
            nom_cl = self.nuplet_client[1]
            pren_cl = self.nuplet_client[2]
            adr = self.nuplet_client[3]
            fix = self.nuplet_client[4]
            mob = self.nuplet_client[5]
            coment = self.nuplet_client[6]

            self.entr_num.insert(0, num_cl)
            self.entr_nom.insert(0, nom_cl)
            self.entr_prenom.insert(0, pren_cl)
            self.entr_adres.insert(tk.END, adr)
            self.entr_fixe.insert(0, fix)
            self.entr_mobil.insert(0, mob)
            self.entr_comentair.insert(tk.END, coment)
            

        else:

            self.entr_num.insert(0, f"CL000{self.num_client + 1}")

            self.entr_nom.config(fg="gray")
            self.entr_nom.insert(0, "Nom")
            self.entr_nom.bind("<FocusIn>", lambda event: effacer_indicatif(self.entr_nom,"Nom"))

            self.entr_prenom.config(fg="gray")
            self.entr_prenom.insert(0, "Prénom")
            self.entr_prenom.bind("<FocusIn>", lambda event: effacer_indicatif(self.entr_prenom,"Prénom"))

            self.entr_adres.config(fg="gray")
            self.entr_adres.insert(tk.END, "Rue ....")
            self.entr_adres.bind("<FocusIn>", lambda event: effacer_Text_indicatif(self.entr_adres,"Rue ...."))

            
            self.entr_fixe.config(fg="gray")
            self.entr_fixe.insert(0, "(123) 456 789")
            self.entr_fixe.bind("<FocusIn>", lambda event: effacer_indicatif(self.entr_fixe,"(123) 456 789"))

            self.entr_mobil.config(fg="gray")
            self.entr_mobil.insert(0, "(123) 456 789")
            self.entr_mobil.bind("<FocusIn>", lambda event: effacer_indicatif(self.entr_mobil,"(123) 456 789"))

            
            self.entr_comentair.config(fg="gray")
            self.entr_comentair.insert(tk.END, "Ajoute comentair")
            self.entr_comentair.bind("<FocusIn>", lambda event: effacer_Text_indicatif(self.entr_comentair,"Ajoute comentair"))


        
    
    def save(self):
        #on controle les infos entre par utilisateur 
        num_client = self.entr_num .get() if (self.entr_num .get() != f"CL000{self.num_client + 1}") else f"CL000{self.num_client + 1}"
        nom_client = self.entr_nom.get() if  (self.entr_nom.get() != "Nom") else ""
        prenom = self.entr_prenom.get()  if ( self.entr_prenom.get() != "Prénom") else ""
        adresse = self.entr_adres.get("1.0", "end-1c") if ( self.entr_adres.get("1.0", "end-1c") != "Rue ....") else ""
        tel_fixe = self.entr_fixe.get() if ( self.entr_fixe.get() !=  "(123) 456 789" ) else ""
        mobil = self.entr_mobil.get()  if ( self.entr_mobil.get() !=  "(123) 456 789") else ""
        comet = self.entr_comentair.get("1.0", "end-1c") if self.entr_comentair.get("1.0", "end-1c") != "Ajoute comentair" else ""

        if( self.nuplet_client != None):
            #on mise a jour les infos qui sont chnagees 
            if (num_client != self.nuplet_client[0]):
                #on verifier d'abord que ce num n'est pas a quelqun autre
                requete = f"SELECT * FROM client WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                deja_exist = self.BDD.execute_requete(requete)
                if(len(deja_exist)!=0 ):
                    messagebox.showerror("Erreur", "Nous sommes désolés, vous ne pouvez pas attribuer ce numéro à ce client car ce numéro existe déjà.") 
                else:
                    requt = f"UPDATE client SET num ='{num_client}' WHERE num = '{self.nuplet_client[0]}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                    self.BDD.execute_requete(requt)
            else:
                pass
            
            if (nom_client != self.nuplet_client[1]):
                requt = f"UPDATE client SET nom = '{nom_client}' WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(requt)
            else:
                pass

            if (prenom != self.nuplet_client[2]):
                requt = f"UPDATE client SET prenom = '{prenom}' WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(requt)
            else:
                pass

            if (adresse != self.nuplet_client[3]):
                requt = f"UPDATE client SET adresse = '{adresse}' WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(requt)
            else:
                pass

            if (tel_fixe != self.nuplet_client[4]):
                requt = f"UPDATE client SET tel_fax = '{tel_fixe}' WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(requt)
            else:
                pass

            if (mobil != self.nuplet_client[5]):
                requt = f"UPDATE client SET mobil = '{mobil}'WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(requt)
            else:
                pass

            if (comet != self.nuplet_client[6]):
                requt = f"UPDATE client SET coment = '{comet}' WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(requt)
            else:
                pass

            
        #dans cas nouveux cleint
        else:
            
            requete = f"SELECT * FROM client WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
            deja_exist = self.BDD.execute_requete(requete)

            if(len(deja_exist)!=0 ):
                messagebox.showerror("Erreur", "Désolé, ce client existe déjà.")
            else:
                requet_cl = "INSERT INTO client (num, nom, prenom, adresse, tel_fax, mobil, coment, id_utilisateur) \
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?);" 

                valeurs = (num_client, nom_client, prenom, adresse, tel_fixe, mobil ,comet, self.id_utilisateur )

                self.BDD.execute_requete(requet_cl,valeurs)


                
        self.canvas.delete("all")
        self.root.event_generate("<<retour_page_client>>")

        


    def annule(self):
        self.canvas.delete("all")
        self.root.event_generate("<<retour_page_client>>")
    

    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))