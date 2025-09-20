import tkinter as tk
import datetime


from const import *
from tools.event_entry import effacer_indicatif
from tools.est_nombre import est_nombre


class InfosBancaire():
    def __init__(self, canvas, pos_vertical, encien_valeur=None):
        self.canv_fact = canvas
        self.y = pos_vertical
        self.encien_valeur = encien_valeur

        self.info_bancair()

    def info_bancair(self):

        info_banc = tk.Label(self.canv_fact, text="Informations Bancaires ",bg=COULEUR_LABEL,font=(POLICE, 15,"bold"))
        self.canv_fact.create_window(200, (self.y +70) , anchor="n", window=info_banc,tags="infos")

        banque = tk.Label(self.canv_fact, text="Banque : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(100, (self.y +95) , anchor="n", window=banque,tags="banque")
        self.ent_banque = tk.Entry(self.canv_fact,width=30)
        self.canv_fact.create_window(230, (self.y +95) , anchor="n", window=self.ent_banque,tags="ent_banque")
        
   
        rib = tk.Label(self.canv_fact, text="RIB : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(100, (self.y +120) , anchor="n", window=rib,tags="rib")
        self.ent_rib = tk.Entry(self.canv_fact,width=30)
        self.canv_fact.create_window(230, (self.y +120) , anchor="n", window=self.ent_rib,tags="ent_rib")

        iban = tk.Label(self.canv_fact, text="IBAN : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(100, (self.y +145) , anchor="n", window=iban,tags="iban")
        self.ent_iban = tk.Entry(self.canv_fact,width=30)
        self.canv_fact.create_window(230, (self.y +145) , anchor="n", window=self.ent_iban,tags="ent_iban")

        bic = tk.Label(self.canv_fact, text="BIC : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(100, (self.y +170) , anchor="n", window=bic,tags="bic")
        self.ent_bic = tk.Entry(self.canv_fact,width=30)
        self.canv_fact.create_window(230, (self.y +170) , anchor="n", window=self.ent_bic,tags="ent_bic")

        if( self.encien_valeur):
            self.ent_banque.insert(0,self.encien_valeur[0])  
            self.ent_rib.insert(0,self.encien_valeur[1])
            self.ent_iban.insert(0,self.encien_valeur[2])
            self.ent_bic.insert(0, self.encien_valeur[3])

        else:
            self.ent_banque.config(fg="gray")
            self.ent_rib.config(fg="gray")
            self.ent_iban.config(fg="gray")
            self.ent_bic.config(fg="gray")

            self.ent_banque.insert(0,"Nom Banque")
            self.ent_rib.insert(0,"RIB")
            self.ent_iban.insert(0,"IBAN")
            self.ent_bic.insert(0, "BIC")

            self.ent_banque.bind("<FocusIn>", lambda event: effacer_indicatif(self.ent_banque, "Nom Banque" ))
            self.ent_rib.bind("<FocusIn>", lambda event: effacer_indicatif(self.ent_rib, "RIB" ))
            self.ent_iban.bind("<FocusIn>", lambda event: effacer_indicatif( self.ent_iban, "IBAN" ))
            self.ent_bic.bind("<FocusIn>", lambda event: effacer_indicatif(self.ent_bic, "BIC" ))


        self.canv_fact.update_idletasks()  
        self.canv_fact.configure(scrollregion=self.canv_fact.bbox("all"))

    

    def get_info(self):
        banq = self.ent_banque.get()
        rib = self.ent_rib.get()
        iban = self.ent_iban.get()
        bic = self.ent_bic.get()

        return [banq, rib, iban, bic]

    