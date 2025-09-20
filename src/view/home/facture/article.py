import tkinter as tk

from const import *
from tools.event_entry import effacer_indicatif,effacer_Text_indicatif
from tools.est_nombre import est_nombre


class Article():
    def __init__(self,canvas,pos_vertical,nb, parent, encien_art=None):
        self.canv_fact = canvas
        self.y = pos_vertical
        self.nb = nb
        self.parent = parent
        self.encien_art = encien_art #dans cas modifier une facture 
        self.info = []
        
    
        self.init_article()
        

        #on passe event soit FoucusOut soit return ( touche Entre ) pour prend l'entry
        self.entry_prix.bind("<FocusOut>", self.focus_out_event)
        self.entry_qnt.bind("<FocusOut>", self.focus_out_event)
        self.prix_tva.bind("<FocusOut>", self.focus_out_event)

        self.entry_prix.bind("<Return>", self.focus_out_event)
        self.entry_qnt.bind("<Return>", self.focus_out_event)
        self.prix_tva.bind("<Return>", self.focus_out_event)

    def init_article(self): 
        button_suprim = tk.Button(self.canv_fact, width=1, height=1, text="X", command=lambda i=self.nb: self.supprime(i))
        self.id_but = self.canv_fact.create_window(20, self.y, anchor="nw", window=button_suprim,tags=f"supprimer_{self.nb}")
 
        self.entry_des = tk.Text(self.canv_fact, bg="white", width=70, height=6)
        self.id_desc = self.canv_fact.create_window(50, self.y, anchor="nw", window=self.entry_des,tags=f"descrip_{self.nb}")
        

        self.entry_prix = tk.Entry(self.canv_fact, width=10)
        self.id_prix = self.canv_fact.create_window(560, self.y, anchor="nw", window=self.entry_prix,tags=f"prix_{self.nb}")
        

        self.entry_qnt = tk.Entry(self.canv_fact, width=7)
        self.id_qnt = self.canv_fact.create_window(650, self.y, anchor="nw", window=self.entry_qnt,tags=f"qnt_{self.nb}")

        self.prix_tva = tk.Entry(self.canv_fact, width=7)
        self.id_tva = self.canv_fact.create_window(820, self.y, anchor="nw", window=self.prix_tva,tags=f"get_tva_{self.nb}")
        
        

        if( self.encien_art):
            self.entry_des.insert(tk.END, self.encien_art[0])
            self.entry_prix.insert(0,self.encien_art[1])
            self.entry_qnt.insert(0,self.encien_art[2])
            self.prix_tva.insert(0,self.encien_art[3])
        else:
            self.entry_des.config(fg="gray")
            self.entry_des.insert(tk.END, "Description De L'intervention")
            self.entry_prix.config(fg="gray")
            self.entry_prix.insert(0,"0.00")
            self.entry_qnt.config(fg="gray")
            self.entry_qnt.insert(0,"0")
            self.prix_tva.config(fg="gray")
            self.prix_tva.insert(0,"0")

            self.entry_des.bind("<FocusIn>", lambda event: effacer_Text_indicatif(self.entry_des, "Description De L'intervention" ))
            self.entry_prix.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_prix, "0.00" ))
            self.entry_qnt.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_qnt, "0" ))
            self.prix_tva.bind("<FocusIn>", lambda event: effacer_indicatif(self.prix_tva, "0" ))


        prix = self.entry_prix.get() if est_nombre( self.entry_prix.get() ) else "0"
        qnt = self.entry_qnt.get() if est_nombre( self.entry_qnt.get() )  else "0"
        tva = self.prix_tva.get() if est_nombre( self.prix_tva.get() ) else "0"

        self.total_ht = tk.Label(self.canv_fact, text=f"{self.get_total_ht(prix,qnt)} €",bg=COULEUR_LABEL)
        self.id_ht = self.canv_fact.create_window(740, self.y, anchor="nw", window=self.total_ht,tags=f"tot_ht_{self.nb}")
        
        self.total_TC = tk.Label(self.canv_fact, text=f"{self.get_TTC(prix,qnt,tva)} €",bg=COULEUR_LABEL)
        self.id_ttc = self.canv_fact.create_window(900, self.y, anchor="nw", window=self.total_TC,tags=f"get_totC_{self.nb}")
    
    def __getitem__(self, index):
        return self.info[index]

    def update_list_infos(self):
        descrip = self.entry_des.get("1.0", "end-1c")
        prix_unit = self.entry_prix.get() if est_nombre( self.entry_prix.get() ) else "0"
        qnt = self.entry_qnt.get() if est_nombre( self.entry_qnt.get() )  else "0"
        tva = self.prix_tva.get() if est_nombre( self.prix_tva.get() ) else "0"

        prix_ht = self.get_total_ht(prix_unit,qnt)
        prix_ttc = self.get_TTC(prix_unit,qnt,tva)

        self.info = [descrip, prix_unit, qnt, tva, prix_ht, prix_ttc]

    def get_info(self):
        descrip = self.entry_des.get("1.0", "end-1c")
        prix_unit = self.entry_prix.get() if est_nombre( self.entry_prix.get() ) else "0"
        qnt = self.entry_qnt.get() if est_nombre( self.entry_qnt.get() )  else "0"
        tva = self.prix_tva.get() if est_nombre( self.prix_tva.get() ) else "0"

        prix_ht = round(self.get_total_ht(prix_unit,qnt) , 2)
        prix_ttc = round(self.get_TTC(prix_unit,qnt,tva), 2)

        self.update_list_infos()

        return [descrip, prix_unit, qnt, tva, prix_ht, prix_ttc]


    

    def supprime(self,nb):
        self.canv_fact.delete(f"supprimer_{nb}")
        self.canv_fact.delete(f"descrip_{nb}")
        self.canv_fact.delete(f"prix_{nb}")
        self.canv_fact.delete(f"qnt_{nb}")
        self.canv_fact.delete(f"tot_ht_{nb}")
        self.canv_fact.delete(f"get_tva_{nb}")
        self.canv_fact.delete(f"get_totC_{nb}")

        y = self.y #renvois sa postion pour quand mise a jour les suivant 
        for new_nb in range( nb+1, len(self.parent.list_article) ):

            self.mise_jour(new_nb, y)

            self.modif_tags(new_nb, new_nb-1)
            y += 100
        self.parent.supprime_article(nb,y)
        

    def mise_jour(self,nb, y):
        self.y = y
        self.canv_fact.coords(f"supprimer_{nb}", 20, y)
        self.canv_fact.coords(f"descrip_{nb}", 50,y )
        self.canv_fact.coords(f"prix_{nb}", 560,y)
        self.canv_fact.coords(f"qnt_{nb}", 650, y)
        self.canv_fact.coords(f"tot_ht_{nb}", 740, y)
        self.canv_fact.coords(f"get_tva_{nb}", 820, y)
        self.canv_fact.coords(f"get_totC_{nb}", 900, y)

    def modif_tags(self,nb,new_nb):
        self.canv_fact.itemconfigure(f"supprimer_{nb}", tags=f"supprimer_{new_nb}")
        self.canv_fact.itemconfigure(f"descrip_{nb}", tags=f"descrip_{new_nb}")
        self.canv_fact.itemconfigure(f"prix_{nb}", tags=f"prix_{new_nb}")
        self.canv_fact.itemconfigure(f"qnt_{nb}", tags=f"qnt_{new_nb}")
        self.canv_fact.itemconfigure(f"tot_ht_{nb}", tags=f"tot_ht_{new_nb}")
        self.canv_fact.itemconfigure(f"get_tva_{nb}", tags=f"get_tva_{new_nb}")
        self.canv_fact.itemconfigure(f"get_totC_{nb}", tags=f"get_totC_{new_nb}")
        
    def get_total_ht(self,prix,qnt):
        res = float(prix) * int(qnt)
        return res


    def get_TTC(self,prix,qnt,tva):
        ht = self.get_total_ht(prix,qnt)
        
        res = ht + (ht * (float(tva)/100))
        return res

    def focus_out_event(self, event: None):
        # Exécuter le code lorsque l'utilisateur a terminé de saisir des valeurs, on verifier que les valeurs entrees sont bien des nombres
        prix = self.entry_prix.get() if est_nombre( self.entry_prix.get() ) else "0"
        qnt = self.entry_qnt.get() if est_nombre( self.entry_qnt.get() )  else "0"
        tva = self.prix_tva.get() if est_nombre( self.prix_tva.get() ) else "0"

        ht = self.get_total_ht(prix, qnt)
        ttc = self.get_TTC(prix,qnt,tva)

        self.total_ht.config(text=f"{ht} €")
        self.total_TC.config(text=f"{ttc} €")
        
        self.update_list_infos()
        self.parent.modif_element(self.nb, self.info)
        self.parent.calcule_total() #on recalcule le somme total 
