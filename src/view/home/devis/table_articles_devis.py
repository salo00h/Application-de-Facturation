import tkinter as tk
import json
import datetime

from const import *
from tools.event_entry import effacer_indicatif,effacer_Text_indicatif
from tools.est_nombre import est_nombre
from view.home.facture.article import Article



class TableArticleDevis():
    def __init__(self,canvas,pos_vertical, encien_valeur=None):

        self.canv_devis = canvas
        self.y = pos_vertical
        self.encien_valeur = encien_valeur

    
        if(self.encien_valeur):
            self.total_ht = self.encien_valeur[1]
            self.total_ttc = self.encien_valeur[2]
        else:
            self.total_ht = 0.0
            self.total_ttc = 0.0

        self.info_table_articles()
        self.inite_prix_total()


    def info_table_articles(self):
        ligne_1 = self.canv_devis.create_line(15, 380, 990, 380, fill="black")

        # Entête du tableau
        inter = tk.Label(self.canv_devis, text="Intervention",bg=COULEUR_LABEL)
        self.canv_devis.create_window(200, 385, anchor="n", window=inter)
        prix = tk.Label(self.canv_devis, text="Prix Unit HT",bg=COULEUR_LABEL)
        self.canv_devis.create_window(600, 385, anchor="n", window=prix)
        qunt = tk.Label(self.canv_devis, text="Quantité",bg=COULEUR_LABEL)
        self.canv_devis.create_window(680, 385, anchor="n", window=qunt)

        tout_ht = tk.Label(self.canv_devis, text="Total HT",bg=COULEUR_LABEL)
        self.toutht_id = self.canv_devis.create_window(760, 385, anchor="n", window=tout_ht)

        tva = tk.Label(self.canv_devis, text="TVA  %",bg=COULEUR_LABEL)
        self.canv_devis.create_window(840, 385, anchor="n", window=tva)

        total_ttc = tk.Label(self.canv_devis, text="Total TTC",bg=COULEUR_LABEL)
        self.canv_devis.create_window(920, 385, anchor="n", window=total_ttc)

        ligne_2 = self.canv_devis.create_line(15,415, 990, 415, fill="black")
        self.nb = 0 #pour conter numbre des article

        if(self.encien_valeur):
            self.list_article = self.encien_valeur[0].copy()
            for encien_art in self.list_article:
                Article(self.canv_devis, self.y, self.nb,self, encien_art)
                self.y += 100
                self.nb += 1 #pour conter numbre des article

        else:
            self.list_article = []
            self.ajoute_article()

        bouton_ajout = tk.Button(self.canv_devis, text="+",bg="black",fg="white", command=lambda: self.ajoute_article())
        self.canv_devis.create_window(20, self.y, anchor="nw", window=bouton_ajout,tags="ajoute")

        ligne_3 = self.canv_devis.create_line(15,self.y +40 , 990,self.y+40,tags="linge_3", fill="black")

        
        
        
    
    def inite_prix_total(self):
        # Total HT, TVA, Total TTC, etc.
        self.total_ht_label = tk.Label(self.canv_devis, bg=COULEUR_LABEL)
        self.canv_devis.create_window(860, (self.y +85) , anchor="n", window=self.total_ht_label,tags="Total_HT")
        self.total_ht_label.config(text=f"   Total HT :   {self.total_ht } € ")

        self.total_ttc_label = tk.Label(self.canv_devis,bg=COULEUR_LABEL)
        self.canv_devis.create_window(860, (self.y +110) , anchor="n", window=self.total_ttc_label,tags="Total_TTC")
        self.total_ttc_label.config(text=f"   Total TTC :  {self.total_ht } €")
            
    
    def ajoute_article(self):
        new_article = Article(self.canv_devis, self.y, self.nb, self)
        self.list_article.append(new_article)
        self.nb += 1

        """ on mise a jour la postion de button ajoute ,, et tous les position suivant a lui """
        self.y += 100
        #Nouvelles coordonnées pour le bouton
        self.canv_devis.coords("ajoute", 20, self.y)
        self.canv_devis.coords("linge_3",15,self.y +40 , 990,self.y+40)
        self.update_places(self.y)

        self.canv_devis.update_idletasks()  
        self.canv_devis.configure(scrollregion=self.canv_devis.bbox("all"))


    def modif_element(self, nb, new_info):
        """ cette fonction pour modifier un element dans liste article """
        self.list_article[nb] = new_info


    def supprime_article(self, indx, new_y):
        self.y = new_y
        self.list_article.pop(indx)
        self.nb -= 1

        self.canv_devis.coords("ajoute", 20, self.y)
        self.canv_devis.coords("linge_3",15,self.y +40 , 990,self.y+40)
        self.update_places(self.y)

        self.canv_devis.update_idletasks()  
        self.canv_devis.configure(scrollregion=self.canv_devis.bbox("all"))

    


    def get_info(self):
        articles = []
        total_ht = 0
        total_ttc = 0
        for artcl in self.list_article:
            if not isinstance(artcl, list): #on fait ce test parceque les articles deja  existe sont representer de type list par contre nouvelle article sont de type objet Article
                articles.append(artcl.get_info())
                total_ht += artcl.get_info()[4]
                total_ttc += artcl.get_info()[5]
            else:
                articles.append(artcl)
                total_ht += artcl[4]
                total_ttc += artcl[5]


        return [articles, round(total_ht,2), round(total_ttc,2)]

    def calcule_total(self):
        self.total_ht = 0
        self.total_ttc = 0
        
        for artcl in self.list_article:
            if not isinstance(artcl, list): #on fait ce test parceque les articles deja  existe sont representer de type list par contre nouvelle article sont de type objet Article
                self.total_ht += artcl.get_info()[4]
                self.total_ttc += artcl.get_info()[5]
            else:
                self.total_ht += artcl[4]
                self.total_ttc += artcl[5]

        self.total_ht_label.config(text=f"   Total HT :   {self.total_ht } € ")
        self.total_ttc_label.config(text=f"   Total TTC :  {self.total_ttc } €")

        
    
    
    def update_places(self,y):
        """ on vas recalculer les position des tous wedjet qu'existe apres table article,, car ces postiones chnage selon d'ajouter des articles
        on appel chaque wedjit par son tags
        """
        #position des infos paiment 
        self.canv_devis.coords("Total_HT",860, y+70)
        self.canv_devis.coords("Total_TTC", 860, y+95)
        self.canv_devis.coords("remarq", 100, y+125)
        self.canv_devis.coords("text_remarq", 10, y+150)
        self.canv_devis.coords("sing", 870, y+150)
        self.canv_devis.coords("ajoute_sing", 950, y+150)
        


