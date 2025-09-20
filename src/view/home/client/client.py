import tkinter as tk
from tkinter import messagebox

from const import *
from tools.event_entry import effacer_indicatif
from view.home.client.ajoute_client import AjouteClient
from view.home.client.voir_client import VoirClient


class Client():
    def __init__(self, root, frame_button, BDD, id_utilisateur):
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



        self.recherhe_client = tk.Entry(self.canvas,width=35,fg="gray")
        self.canvas.create_window(730, (y//26.66) , anchor="ne", window=self.recherhe_client,tags="rech_client")
        self.recherhe_client.insert(0, "Recherche")

        self.recherhe_client.bind("<FocusIn>", lambda event: effacer_indicatif(self.recherhe_client,"Recherche"))
        
        self.recherhe_client.bind("<Return>",lambda event: self.cherche_client())
        
        
        num_client = tk.Label(self.canvas, text="Num",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(100, 70 , anchor="n", window=num_client,tags="num_client")
        nom_client = tk.Label(self.canvas, text="Nom",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(200, 70 , anchor="n", window=nom_client,tags="nom_client")
        prenom_client = tk.Label(self.canvas, text="Prénom",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(350, 70 , anchor="n", window=prenom_client,tags="prenom_client")
        adr = tk.Label(self.canvas, text="Adresse",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(530,70 , anchor="n", window=adr,tags="adr")
        tel_fax = tk.Label(self.canvas, text="Tél. Fixe",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(725,70 , anchor="n", window=tel_fax,tags="tel_fax")
        mob = tk.Label(self.canvas, text="Mobile",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(860,70 , anchor="n", window=mob,tags="mob")
        coment = tk.Label(self.canvas, text="Commentaires",bg=COULEUR_PRINCIPALE, font=(POLICE,11,"bold"))
        self.canvas.create_window(1000,70 , anchor="n", window=coment,tags="coment")
        

        # Création de la listebox
        self.listbox = tk.Listbox(self.canvas, selectmode=tk.SINGLE,  width=1130, height=550, font=(POLICE,10))
        self.canvas.create_window(600, 100, width=1130, height=550, anchor="n", window=self.listbox, tags="listbox")

        self.requet_client = f"SELECT * FROM client WHERE id_utilisateur = {self.id_utilisateur}"
        self.requet_client  = self.BDD.execute_requete( self.requet_client )
        
        for clien in self.requet_client:
            if (clien[6] is not None ):
                comentair = clien[6]
            else:
                comentair = ""
            

           
            format_info = f"{'':<9}{(clien[0] + (len(clien[0])%8)*" ")[0:8] :<18}{(clien[1] + (len(clien[1])%10)*" ")[0:10]:<26}{(clien[2] + (len(clien[2])%10)*" ")[0:10]:<32}{(clien[3] + (len(clien[3])%15)*" ")[0:15]:<37}{(clien[4] + (len(clien[4])%8)*" ")[0:8]:27}{(clien[5] + (len(clien[5])%8)*" ")[0:8]:25}{(comentair + (len(comentair)%8)*" ")[0:10]:>5}"
            self.listbox.insert(tk.END, format_info)


        self.ajoute = tk.Button(self.canvas, width=10, height=2,text="Ajouter", command=lambda:self.ajoute_client() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(380,660 , anchor="n", window=self.ajoute,tags="ajoute")
        
        self.modf = tk.Button(self.canvas, width=10, height=2,text="Modifier", command=lambda:self.modf_client() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(500,660 , anchor="n", window=self.modf,tags="lire")

        self.voir = tk.Button(self.canvas, width=10, height=2,text="Afficher", command=lambda:self.voir_client() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(630,660 , anchor="n", window=self.voir,tags="voir")
        
        self.supprim = tk.Button(self.canvas, width=10, height=2,text="Supprimer", command=lambda:self.supprim_client() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(770,660 , anchor="n", window=self.supprim,tags="supr")
        
        

    def ajoute_client(self):
        self.canvas.delete("all")
        AjouteClient(self.root,self.canvas, self.frame_button, self.BDD, self.id_utilisateur)
        
    def modf_client(self):
        index_client = self.listbox.curselection() #recuperer l'indice d'elemrnt choisi
        if index_client:
            client_info = self.listbox.get(index_client[0])
            num_client = client_info.split()[0]

            requet_tous_info = f"SELECT * FROM client WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
            nuplet_client = self.BDD.execute_requete(requet_tous_info)[0]

            self.canvas.delete("all")
            AjouteClient(self.root,self.canvas, self.frame_button, self.BDD, self.id_utilisateur,nuplet_client)
        else:
            messagebox.showerror("Erreur", "Vous devez sélectionner un client.") 
            


    def voir_client(self):
        index_client = self.listbox.curselection() #recuperer l'indice d'elemrnt choisi
        if index_client:
            client_info = self.listbox.get(index_client[0])
            num_client = client_info.split()[0]

            requet_tous_info = f"SELECT * FROM client WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
            nuplet_client = self.BDD.execute_requete(requet_tous_info)[0]

            self.canvas.delete("all")
            VoirClient(self.root,self.canvas, self.frame_button, self.BDD, self.id_utilisateur,nuplet_client)
        else:
            messagebox.showerror("Erreur", "Vous devez sélectionner un client.") 
            

    def supprim_client(self):
        index_client = self.listbox.curselection() #recuperer l'indice d'elemrnt choisi
        if index_client:
            client_info = self.listbox.get(index_client[0])
            num_client = client_info.split()[0]


            #on regarde d'aborde si y'a des facture ou devis relier a ce cleint , s'y existe on peux pas supprimer 
            if( self.BDD.execute_requete(f"SELECT * FROM facture WHERE ref_client = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;")):
                messagebox.showerror("Erreur", "Vous ne pouvez pas supprimer ce client car il y a des factures liées à lui.") 

            elif( self.BDD.execute_requete(f"SELECT * FROM devis WHERE ref_client = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;")):
                messagebox.showerror("Erreur", "Vous ne pouvez pas supprimer ce client car il y a des devis liées à lui.") 

            else:

                suprime_client = f"DELETE FROM client WHERE num = '{num_client}' AND id_utilisateur = '{self.id_utilisateur}' ;"
                self.BDD.execute_requete(suprime_client)

                #on mise a jour l'affichage
                self.listbox.delete(0, tk.END)
                self.requet_client = f"SELECT * FROM client WHERE id_utilisateur = {self.id_utilisateur}"
                self.requet_client  = self.BDD.execute_requete( self.requet_client )
        
                for clien in self.requet_client:
                    if (clien[6] is not None ):
                        comentair = clien[6]
                    else:
                        comentair = ""
            
                    format_info = f"{'':<9}{(clien[0] + (len(clien[0])%8)*" ")[0:8] :<18}{(clien[1] + (len(clien[1])%10)*" ")[0:10]:<26}{(clien[2] + (len(clien[2])%10)*" ")[0:10]:<32}{(clien[3] + (len(clien[3])%15)*" ")[0:15]:<37}{(clien[4] + (len(clien[4])%8)*" ")[0:8]:27}{(clien[5] + (len(clien[5])%8)*" ")[0:8]:25}{(comentair + (len(comentair)%8)*" ")[0:10]:>5}"
                    self.listbox.insert(tk.END, format_info)
        else:
            messagebox.showerror("Erreur", "Vous devez sélectionner un client.") 
            

    def cherche_client(self, event=None):

        requete_cherche = f"""SELECT * FROM client WHERE id_utilisateur = {self.id_utilisateur}
                            AND(num = '{self.recherhe_client.get()}' OR
                                nom = '{self.recherhe_client.get()}' OR
                                prenom = '{self.recherhe_client.get()}')"""
        
        
        resultat_recherche = self.BDD.execute_requete(requete_cherche)

        self.listbox.delete(0, tk.END)
        for clien in resultat_recherche:
            if (clien[6] is not None ):
                comentair = clien[6]
            else:
                comentair = ""
            
            format_info = f"{'':<9}{(clien[0] + (len(clien[0])%8)*" ")[0:8] :<18}{(clien[1] + (len(clien[1])%10)*" ")[0:10]:<26}{(clien[2] + (len(clien[2])%10)*" ")[0:10]:<32}{(clien[3] + (len(clien[3])%15)*" ")[0:15]:<37}{(clien[4] + (len(clien[4])%8)*" ")[0:8]:27}{(clien[5] + (len(clien[5])%8)*" ")[0:8]:25}{(comentair + (len(comentair)%8)*" ")[0:10]:>5}"
            self.listbox.insert(tk.END, format_info)


    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))

            
