import tkinter as tk
from tkinter import messagebox

from const import *
from tools.event_entry import effacer_indicatif

from view.home.facture.cree_fact import Facture
from view.home.facture.touts_facture import ToutesFacture

class HistoryFacture:
    def __init__(self, root,frame_button,BDD, id_utilisateur):
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

        self.lis_button_fact = [] # on mettre les button dans une liste pour appliquer le chnagement de couleur de phase active.
        self.button_active = 0

        self.tout_fact = tk.Button(self.canvas, width=20, height=3,text="Toutes les factures", command=lambda:self.touts_facture() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 10,"bold"))
        self.tout_fact.place(x=(x//30), y=(y//32))
        self.lis_button_fact.append(self.tout_fact)

        self.fact_payee = tk.Button(self.canvas, width=20, height=3,text="Factures payées", command=lambda:self.facture_payee() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 10,"bold"))
        self.fact_payee.place(x=(x//5.33), y=(y//32))
        self.lis_button_fact.append(self.fact_payee)

        self.fact_non_payee = tk.Button(self.canvas, width=20, height=3,text="Factures non payées", command=lambda:self.facture_non_payee() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 10,"bold"))
        self.fact_non_payee.place(x=(x//3), y=(y//32))
        self.lis_button_fact.append(self.fact_non_payee)


        self.nouvel_fact = tk.Button(self.canvas, width=20, height=2,text="Nouvelle facture", command=lambda:self.nouvelle_facture() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 10,"bold"))
        self.canvas.create_window(1150, (y//22.85) , anchor="ne", window=self.nouvel_fact,tags="nouvl_fact")

        self.recherhe_fact = tk.Entry(self.canvas,width=22,fg="gray")
        self.canvas.create_window(960, (y//14.54) , anchor="ne", window=self.recherhe_fact,tags="rech_fact")
        self.recherhe_fact.insert(0, "Recherche")

        self.recherhe_fact.bind("<FocusIn>", lambda event: effacer_indicatif(self.recherhe_fact, "Recherche" ))

        

        fact = tk.Label(self.canvas, text="Facture",bg=COULEUR_PRINCIPALE, font=(POLICE,12,"bold"))
        self.canvas.create_window(140, 160 , anchor="n", window=fact,tags="fact")
        client = tk.Label(self.canvas, text="Client",bg=COULEUR_PRINCIPALE, font=(POLICE,12,"bold"))
        self.canvas.create_window(380, 160 , anchor="n", window=client,tags="client")
        date = tk.Label(self.canvas, text="Date",bg=COULEUR_PRINCIPALE, font=(POLICE,12,"bold"))
        self.canvas.create_window(600, 160 , anchor="n", window=date,tags="date")
        solde = tk.Label(self.canvas, text="Solde Dû ",bg=COULEUR_PRINCIPALE, font=(POLICE,12,"bold"))
        self.canvas.create_window(850,160 , anchor="n", window=solde,tags="solde")
        

        # Création de la listebox
        self.listbox = tk.Listbox(self.canvas, selectmode=tk.SINGLE,  width=650, height=400,font=(POLICE,10))
        self.canvas.create_window(500, 200, width=950, height=400, anchor="n", window=self.listbox, tags="listbox")

        
        self.modf = tk.Button(self.canvas, width=10, height=2,text="Modifier", command=lambda:self.modf_fact() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(420,610 , anchor="n", window=self.modf,tags="lire")
        
        self.supprim = tk.Button(self.canvas, width=10, height=2,text="Supprimer", command=lambda:self.supprim_fact() ,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"))
        self.canvas.create_window(630,610 , anchor="n", window=self.supprim,tags="lire")
        


        self.touts_facture() #on ititialse le page pour tous facture


        self.recherhe_fact.bind("<Return>",lambda event: self.cherche_facture())
        



    def touts_facture(self):
        self.lis_button_fact[self.button_active].config(bg=COULEUR_PRINCIPALE)
        self.lis_button_fact[0].config(bg=COULEUR_CANVAS)
        self.button_active = 0

        self.requet_tous_fact = f"""SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du
                        FROM client
                        INNER JOIN facture ON client.num = facture.ref_client
                        WHERE  facture.id_utilisateur = {self.id_utilisateur}"""
        self.requet_tous_fact = self.BDD.execute_requete(self.requet_tous_fact)

        
        self.listbox.delete(0, tk.END)
        for fact in self.requet_tous_fact:
            nom_client = f"{fact[1]} {fact[2]}"

            format_info = f"{'':<10}{fact[0]:<60}{nom_client[0:15]:<45}{fact[3]:<50}{fact[4]:>20}"
            self.listbox.insert(tk.END, format_info)

        
    def facture_payee(self):
        self.lis_button_fact[self.button_active].config(bg=COULEUR_PRINCIPALE)
        self.lis_button_fact[1].config(bg=COULEUR_CANVAS)
        self.button_active = 1

        self.requt_fact_pay = f"SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du FROM client, facture WHERE client.num = facture.ref_client AND facture.id_utilisateur = {self.id_utilisateur} AND facture.solde_du = 0"
        self.requt_fact_pay = self.BDD.execute_requete(self.requt_fact_pay)
        
        self.listbox.delete(0, tk.END)
        for fact in self.requt_fact_pay:
            nom_client = f"{fact[1]} {fact[2]}"

            format_info = f"{'':<10}{fact[0]:<60}{nom_client[0:15]:<53}{fact[3]:<60}{fact[4]:>20}"
            self.listbox.insert(tk.END, format_info)

    def facture_non_payee(self):
        self.lis_button_fact[self.button_active].config(bg=COULEUR_PRINCIPALE)
        self.lis_button_fact[2].config(bg=COULEUR_CANVAS)
        self.button_active = 2
        
        self.requt_fact_non_pay = f"SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du FROM client, facture WHERE client.num = facture.ref_client AND facture.id_utilisateur = {self.id_utilisateur} AND facture.solde_du <> 0"
        self.requt_fact_non_pay = self.BDD.execute_requete(self.requt_fact_non_pay)

        self.listbox.delete(0, tk.END)
        for fact in self.requt_fact_non_pay:
            nom_client = f"{fact[1]} {fact[2]}"

            format_info = f"{'':<10}{fact[0]:<60}{nom_client[0:15]:<45}{fact[3]:<50}{fact[4]:>20}"
            self.listbox.insert(tk.END, format_info)

    def nouvelle_facture(self):
        self.canvas.destroy()
        Facture(self.root,self.frame_button,self.BDD, self.id_utilisateur) #defini dans  (cree_fact.py)


    def cherche_facture(self, event=None):

        if ( self.button_active ==0 ):

            requete_cherche = f"""
                        SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du
                        FROM client
                        INNER JOIN facture ON client.num = facture.ref_client
                        WHERE 
                        facture.id_utilisateur = '{self.id_utilisateur}' AND (
                        facture.num = '{self.recherhe_fact.get()}' OR
                        client.nom = '{self.recherhe_fact.get()}' OR
                        client.prenom = '{self.recherhe_fact.get()}' OR
                        facture.date_fac = '{self.recherhe_fact.get()}'
                    )
                    """
            resultat_recherche = self.BDD.execute_requete(requete_cherche)

            
        elif( self.button_active == 1):
            requete_cherche = f"""
                        SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du
                        FROM client
                        INNER JOIN facture ON client.num = facture.ref_client
                        WHERE facture.solde_du = 0 
                        AND facture.id_utilisateur = '{self.id_utilisateur}' AND (
                        facture.num = '{self.recherhe_fact.get()}' OR
                        client.nom = '{self.recherhe_fact.get()}' OR
                        client.prenom = '{self.recherhe_fact.get()}' OR
                        facture.date_fac = '{self.recherhe_fact.get()}'
                    )
                    """
            resultat_recherche = self.BDD.execute_requete(requete_cherche)

            
        else:
            requete_cherche = f"""
                        SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du
                        FROM client
                        INNER JOIN facture ON client.num = facture.ref_client
                        WHERE facture.solde_du <> 0 
                        AND facture.id_utilisateur = '{self.id_utilisateur}' AND (
                        facture.num = '{self.recherhe_fact.get()}' OR
                        client.nom = '{self.recherhe_fact.get()}' OR
                        client.prenom = '{self.recherhe_fact.get()}' OR
                        facture.date_fac = '{self.recherhe_fact.get()}'
                    )
                    """
            resultat_recherche = self.BDD.execute_requete(requete_cherche)

        self.listbox.delete(0, tk.END)
        for fact in resultat_recherche:
            nom_client = f"{fact[1]} {fact[2]}"

            format_info = f"{'':<10}{fact[0]:<60}{nom_client[0:15]:<45}{fact[3]:<50}{fact[4]:>20}"
            self.listbox.insert(tk.END, format_info)


    def lire_fact(self):
        pass

    def modf_fact(self):
        indice_fact = self.listbox.curselection()
        if indice_fact:
            format_box =self.listbox.get(indice_fact)
            num_fact = format_box.split()[0]
            requet_fact = f"SELECT * FROM facture WHERE num = '{num_fact}' AND id_utilisateur = '{self.id_utilisateur}';"
            requet_fact = self.BDD.execute_requete(requet_fact)[0]
            
            self.canvas.destroy()
            Facture(self.root,self.frame_button,self.BDD, self.id_utilisateur,requet_fact) #defini dans  (cree_fact.py)

        else:
            messagebox.showerror("Erreur", "Vous devez sélectionner une facture.") 
        

        

    def supprim_fact(self):
        indice_fact = self.listbox.curselection()
        if indice_fact:
            format_box =self.listbox.get(indice_fact)
            num_fact = format_box.split()[0]
            suprime_fact = f"DELETE FROM facture WHERE num = '{num_fact}' AND id_utilisateur = '{self.id_utilisateur}';"
            self.BDD.execute_requete(suprime_fact)

            if(self.button_active == 0):
                list_fact = f"SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du FROM client, facture WHERE client.num = facture.ref_client AND facture.id_utilisateur = {self.id_utilisateur}"
                list_fact = self.BDD.execute_requete(list_fact)

            elif(self.button_active == 1):
                list_fact =f"SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du FROM client, facture WHERE client.num = facture.ref_client AND facture.id_utilisateur = {self.id_utilisateur} AND facture.solde_du = 0"
                list_fact = self.BDD.execute_requete(list_fact)

            else:
                list_fact = f"SELECT facture.num, client.nom, client.prenom, facture.date_fac, facture.solde_du FROM client, facture WHERE client.num = facture.ref_client AND facture.id_utilisateur = {self.id_utilisateur} AND facture.solde_du <> 0"
                list_fact = self.BDD.execute_requete(list_fact )

            self.listbox.delete(0, tk.END)
            for fact in list_fact:
                nom_client = f"{fact[1]}   {fact[2]}"

                format_info = f"{'':<10}{fact[0]:<60}{nom_client[0:15]:<45}{fact[3]:<50}{fact[4]:>20}"
                self.listbox.insert(tk.END, format_info)
        else:
            messagebox.showerror("Erreur", "Vous devez sélectionner une facture.") 
        
    
    
    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))

