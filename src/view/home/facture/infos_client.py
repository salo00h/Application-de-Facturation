import tkinter as tk
import datetime


from const import *
from tools.event_entry import effacer_indicatif, effacer_Text_indicatif


class InfosClient():
    def __init__(self, canvas, encien_infos=None):
        self.canv_fact = canvas
        self.encien_infos = encien_infos # dans cas modifier facture ou le client deja dans table basse donc on affiche direct ses infos 

        self.info_client()
        

    def info_client(self):
        client = tk.Label(self.canv_fact, text="Adresse De Facturation : ",bg=COULEUR_LABEL,font=(POLICE, 15,"bold"))
        self.canv_fact.create_window(760, 185, anchor="n", window=client)
        # Adresse client
        nom_client_label = tk.Label(self.canv_fact, text="Nom : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(675, 215, anchor="n", window=nom_client_label)
        self.entry_nom_client = tk.Entry(self.canv_fact,width=35,font=(POLICE,9))
        self.canv_fact.create_window(850, 215, anchor="n", window=self.entry_nom_client)

        pren_client_label = tk.Label(self.canv_fact, text="Prénom : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(675, 240, anchor="n", window=pren_client_label)
        self.entry_pren_client = tk.Entry(self.canv_fact,width=35,font=(POLICE,9))
        self.canv_fact.create_window(850, 240, anchor="n", window=self.entry_pren_client)
        
        adresse_client_label = tk.Label(self.canv_fact, text="Adresse : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(675, 283, anchor="n", window=adresse_client_label)
        self.entry_adrs_client = tk.Text(self.canv_fact,width=35,height=3,font=(POLICE,9))
        self.canv_fact.create_window(850, 265, anchor="n", window=self.entry_adrs_client)

        telphon_client_label = tk.Label(self.canv_fact, text="Tél.fixe : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(675, 325, anchor="n", window=telphon_client_label)
        self.entry_tel_client = tk.Entry(self.canv_fact,width=35,font=(POLICE,9))
        self.canv_fact.create_window(850, 325, anchor="n", window=self.entry_tel_client)

        mobil_client_label = tk.Label(self.canv_fact, text="Tél Mobile : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(675, 350, anchor="n", window=mobil_client_label)
        self.entry_mobil_client = tk.Entry(self.canv_fact, width=35, font=(POLICE,9))
        self.canv_fact.create_window(850, 350, anchor="n", window=self.entry_mobil_client)

        if(self.encien_infos):
            self.entry_nom_client.insert(0, self.encien_infos[1])
            self.entry_pren_client.insert(0, self.encien_infos[2])
            self.entry_adrs_client.insert(tk.END, self.encien_infos[3])
            self.entry_tel_client.insert(0, self.encien_infos[4])
            self.entry_mobil_client.insert(0, self.encien_infos[5])

        else:
            self.entry_nom_client.config(fg="gray")
            self.entry_nom_client.insert(0, "Nom Client ")

            self.entry_pren_client.config(fg="gray")
            self.entry_pren_client.insert(0, "Prénom Client ")

            self.entry_adrs_client.config(fg="gray")
            self.entry_adrs_client.insert(tk.END, "Rue ....")

            self.entry_tel_client.config(fg="gray")
            self.entry_tel_client.insert(0, "(123) 456 789")

            self.entry_mobil_client.config(fg="gray")
            self.entry_mobil_client.insert(0, "(123) 456 789")

            self.event_entry_case() # on active l'event juste dans cas nouvelle facture 



    def event_entry_case(self):
        """on active l'event pour case enrty pour quand l'utilisateur tape le case , l'example existe va supprimer 
            par la fonction importée (effacer_indicatif) qui prend le variable Entry et son text indicatif
        """
        self.entry_nom_client.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_nom_client, "Nom Client " ))
        self.entry_pren_client.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_pren_client, "Prénom Client "))
        self.entry_adrs_client.bind("<FocusIn>", lambda event: effacer_Text_indicatif(self.entry_adrs_client, "Rue ...."))
        self.entry_tel_client.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_tel_client, "(123) 456 789"))
        self.entry_mobil_client.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_mobil_client, "(123) 456 789"))



    def get_info(self):
        nom = self.entry_nom_client.get() if (self.entry_nom_client.get() != "Nom Client ") else ""
        prenom = self.entry_pren_client.get() if (self.entry_pren_client.get() != "Prénom Client ") else ""
        adr = self.entry_adrs_client.get("1.0", "end-1c") if (self.entry_adrs_client.get("1.0", "end-1c") != "Rue ....") else ""
        tel = self.entry_tel_client.get() if ( self.entry_tel_client.get() != "(123) 456 789") else ""
        mobil = self.entry_mobil_client.get() if (self.entry_mobil_client.get() != "(123) 456 789") else ""

        return [nom,prenom,adr,tel,mobil]



