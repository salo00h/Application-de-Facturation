import tkinter as tk
from tkinter import messagebox
import json

from PIL import Image,ImageTk, ImageDraw
from tkinter import filedialog
import datetime


from const import *
from tools.event_entry import effacer_indicatif, effacer_Text_indicatif
from tools.convert_pdf import convert_pdf

from view.home.facture.infos_client import InfosClient
from view.home.facture.infos_entrprise import InfosEntreprise
from view.home.facture.table_article import TableArticle
from view.home.facture.prix_info_pay import InfosBancaire
from view.home.facture.singature import SignatureFrame


class Facture:
    def __init__(self, root,frame_button,BDD, id_utilisateur, encien_facture=None):
        self.root = root
        self.frame_button = frame_button
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur
        self.encien_facture = encien_facture #dans cas juste modifier une facture 

        self.deja_enregist = 0 #on a besoin pour savoir si la facture deja enregistrer ou pas 
        self.avoir_signature = 0
        
        self.root.after(10, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)
        
        
    def initialisation(self):

        self.x = self.root.winfo_width()
        self.y = self.root.winfo_height()

        self.canvas = tk.Canvas(self.root, width=self.x, height=self.y,bg=COULEUR_PRINCIPALE)
        self.canvas.place(x=0, y=(self.y //11.42))

        self.frame_fact = tk.Frame(self.canvas, width=(self.x//1.2), height=(self.y//1.176), bg=COULEUR_LABEL)
        self.frame_fact.grid_propagate(False)  # Empêcher le frame de redimensionner ses cellules
        self.frame_fact.place(x=100, y=0)

        # Création du canevas avec la barre de défilement
        self.canv_fact = tk.Canvas(self.frame_fact,width=(self.x//1.2), height=(self.y//1.176), yscrollincrement=8, bg=COULEUR_LABEL)
        self.canv_fact.grid_propagate(False)
        self.scrol_fact = tk.Scrollbar(self.frame_fact, command=self.canv_fact.yview, orient="vertical", bg=COULEUR_PRINCIPALE)
        self.scrol_fact.pack(side="right", fill="y")
        self.canv_fact.configure(yscrollcommand=self.scrol_fact.set)
        self.canv_fact.pack(side=tk.TOP, expand=True, fill=tk.BOTH)  # Remplir le canevas avec tout l'espace disponible
       

        self.cree_facture()


        bouton_retour = tk.Button(self.canvas, text="Retour",height=1,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"), command=lambda: self.retour())
        self.canvas.create_window(370, 685, anchor="n", window=bouton_retour,tags="bouton_retour")
        
        bouton_enregs = tk.Button(self.canvas, text="Enregistrer",height=1,bg=COULEUR_BOUTON,fg=COULEUR_TEXT_BOUTON,font=(POLICE, 11,"bold"), command=lambda: self.enregistrer())
        self.canvas.create_window(570, 685, anchor="n", window=bouton_enregs,tags="bouton_enregs")

        bouton_pdf = tk.Button(self.canvas, text="Enregistrer en PDF",height=1,bg=COULEUR_PRINCIPALE,font=(POLICE, 11,"bold"), command=lambda: self.convert_pdf())
        self.canvas.create_window(820, 685, anchor="n", window=bouton_pdf,tags="bouton_pdf")
 
 
        #on on prend l'event soit par taper Entre ou FoucusOut pour sorris
        self.entry_num_fact.bind("<Return>",lambda event: self.get_num_facture()) #si l'utilisature change le numero par defut pour facture
        self.entry_num_fact.bind("<FocusOut>",lambda event: self.get_num_facture())
        self.entry_ref_cleint.bind("<Return>",lambda event: self.get_num_client())#si l'utilisature utilse un client deja dans basse donne ,on va dircte importer ces inofs ou dans cas change le numero par defut pour client
        self.entry_ref_cleint.bind("<FocusOut>",lambda event: self.get_num_client())
        

    
            

    
    def cree_facture(self):
        if self.encien_facture is None:
            # NOUVELLE FACTURE
            self.nouvel_fact()

        else:
            self.modifier_facture()
        
        self.canv_fact.update_idletasks()  
        self.canv_fact.configure(scrollregion=self.canv_fact.bbox("all"))


    def nouvel_fact(self):
        self.info_facture()
        self.info_entrprise = InfosEntreprise(self.canv_fact,self.BDD, self.id_utilisateur)
        self.info_client = InfosClient(self.canv_fact)
        self.info_table_articles = TableArticle(self.canv_fact,425)
        self.info_bancaires = InfosBancaire(self.canv_fact,540 )
        self.infos_supplem(540)

    def modifier_facture(self):
        list_infos_fact = [self.encien_facture[0], self.encien_facture[1] , self.encien_facture[9]]# [num_fact, date , ref_client ]
        self.info_facture(list_infos_fact)

        #on cherche des inofs de cleint apartir de son ref, defini dans encien facture 
        requet_cl = f"SELECT * FROM client WHERE num = '{self.encien_facture[9]}' AND id_utilisateur = '{self.id_utilisateur}';"
        requet_cl = self.BDD.execute_requete(requet_cl)[0]
        self.info_client = InfosClient(self.canv_fact,requet_cl)

        self.info_entrprise = InfosEntreprise(self.canv_fact,self.BDD, self.id_utilisateur)
        
        table = json.loads(self.encien_facture[2]) #parce que les donne ont entre dans table basse de mode json.dump , donc on doite desactive 
        info_pay = json.loads(self.encien_facture[5])
        self.info_table_articles = TableArticle(self.canv_fact,425, table ,info_pay )  

        
        position_suiv_tabla = ( 540 + ((len(table)-1) * 100))
        info_banc = json.loads(self.encien_facture[6])
        self.info_bancaires = InfosBancaire(self.canv_fact,position_suiv_tabla , info_banc )

        self.infos_supplem(position_suiv_tabla,self.encien_facture[3])

    def remplir_client(self):
        if (self.tous_infos_client):
            self.info_client = InfosClient(self.canv_fact, self.tous_infos_client)
        else:
            pass


    def info_facture(self, infos_fact=None): # infos_fact : une liste[num facture, date , ref client]
        facture_label = tk.Label(self.canv_fact, text="FACTURE",bg=COULEUR_LABEL,font=(POLICE, 20,"bold"))
        self.canv_fact.create_window(500, 40, anchor="n", window=facture_label)
        # Num facture
        self.num_fact = int(self.BDD.execute_requete(f"SELECT COUNT(*) AS nombre_de_lignes FROM facture;")[0][0])
        num_facture_label = tk.Label(self.canv_fact, text="Numbre facture : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(797, 70, anchor="n", window=num_facture_label)
        self.entry_num_fact = tk.Entry(self.canv_fact)
        self.canv_fact.create_window(925, 70, anchor="n", window=self.entry_num_fact)
        # Date facture
        date_facture_label = tk.Label(self.canv_fact, text="Date facture : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(805,100, anchor="n", window=date_facture_label)
        self.entry_date_fact = tk.Entry(self.canv_fact)
        self.canv_fact.create_window(925, 100, anchor="n", window=self.entry_date_fact)
        #Ref client 
        self.num_client = int(self.BDD.execute_requete(f"SELECT COUNT(*) AS nombre_de_lignes FROM client;")[0][0])
        ref_cleint_label = tk.Label(self.canv_fact, text="Ref Client : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(810,130, anchor="n", window=ref_cleint_label)
        self.entry_ref_cleint = tk.Entry(self.canv_fact)
        self.canv_fact.create_window(925, 130, anchor="n", window=self.entry_ref_cleint)

        if(infos_fact):
            self.entry_num_fact.insert(0, infos_fact[0])
            self.entry_date_fact.insert(0,infos_fact[1])
            self.entry_ref_cleint.insert(0,infos_fact[2])
        else:
            self.entry_num_fact.insert(0, f"FAC000{self.num_fact +1 }")
            self.entry_date_fact.insert(0,datetime.datetime.now().date()) #afficheer la date actule par defut
            self.entry_ref_cleint.insert(0,f"CL000{self.num_client + 1}") 
    
    
    def infos_supplem(self,y, remarqu=None):
        self.y = y
        lab_remarq = tk.Label(self.canv_fact, text="Remarque : ",bg=COULEUR_LABEL,font=(POLICE, 15,"bold"))
        self.canv_fact.create_window(100, (self.y +300) , anchor="n", window=lab_remarq,tags="remarq")
        self.text_remarq = tk.Text(self.canv_fact, bg="white", width=100,height=9)
        self.canv_fact.create_window(10, (self.y +330) , anchor="nw", window=self.text_remarq,tags="text_remarq")

        if(remarqu):
            self.text_remarq.insert(tk.END,remarqu)
        else:
            self.text_remarq.config(fg="gray")
            self.text_remarq.insert(tk.END,"Ajouter des remarques")
            self.text_remarq.bind("<FocusIn>", lambda event: effacer_Text_indicatif(self.text_remarq, "Ajouter des remarques" ))

        sing = tk.Label(self.canv_fact, text="Singature ",bg=COULEUR_LABEL,font=(POLICE, 15,"bold"))
        self.canv_fact.create_window(870, (self.y +320) , anchor="n", window=sing,tags="sing")
        bouton_sing = tk.Button(self.canv_fact, text="+",bg="black",fg="white", command=lambda: self.ajoute_singature())
        self.canv_fact.create_window(950, self.y + 320, anchor="n", window=bouton_sing,tags="ajoute_sing")

        self.canv_fact.update_idletasks()  
        self.canv_fact.configure(scrollregion=self.canv_fact.bbox("all"))


        
    def ajoute_singature(self):
        self.avoir_signature = 1
        x, y = self.canv_fact.coords("sing")
        frame_sing = tk.Frame(self.canv_fact, width=250, height=130, bg=COULEUR_LABEL)
        self.canv_fact.create_window(850, y + 30, anchor="n", window=frame_sing,tags="frame_sing")
        self.sign = SignatureFrame(self.canv_fact,frame_sing,self.id_utilisateur) 
        
        # on done l'id pour singateur car on relier chaque singeur avec l'utilsature actuel ,, 
        # il paux modifer comme il veux, par contre la fois qu'il singe pas on prend son dernier signature 


    def enregistrer(self):
        #on s'assore des format d'infos avant enregestrer
        num_fact = self.entry_num_fact.get() if (self.entry_num_fact.get()[0:6] =="FAC000") else f"FAC000{self.num_fact +1 }"
        date_fact = self.entry_date_fact.get()
        ref_client = self.entry_ref_cleint.get() if(self.entry_ref_cleint.get()[0:5] == "CL000") else f"CL000{self.num_client + 1}"

        donnees_client = self.info_client.get_info()
        donnees_entrpris = self.info_entrprise.get_info()
        doonees_banque = json.dumps(self.info_bancaires.get_info())
        
        
        donnees_articles = json.dumps(self.info_table_articles.get_info()[0]) #une liste qui contiens des liste ( chaque article represnter dans une liste)
        donnees_payee = json.dumps(self.info_table_articles.get_info()[1:]) #[total_ht, total_ttc,remis,net, etat, mode, date_echan]

        solde = self.info_table_articles.get_info()[6]

        remarque = self.text_remarq.get("1.0", "end-1c") if ( self.text_remarq.get("1.0", "end-1c") != "Ajouter des remarques") else ""
        
        if(self.avoir_signature):
            self.signature = self.sign.get_bien_singe()
        else:
            self.signature = 0
        

        #requet de checher d'abord si la client deaje dans BDD , sinon on va l'ajouter
        requet_cl = f"SELECT num FROM client WHERE num = '{ref_client}' AND id_utilisateur = '{self.id_utilisateur}';"
        requet_cl = self.BDD.execute_requete(requet_cl)
        if (len(requet_cl) == 0 ):
            #si le client n'est pas encore dans table client , on va l'ajouter
            requet_cl = "INSERT INTO client (num, nom, prenom, adresse, tel_fax, mobil, coment,id_utilisateur) \
                    VALUES(?, ?, ?, ?, ?, ?, ?, ? )" 

            valeurs = (ref_client, donnees_client[0], donnees_client[1], donnees_client[2], donnees_client[3], donnees_client[4] ,"", self.id_utilisateur ) #on mettre comentaire vide pour q'il prend pas valeur None

            self.BDD.execute_requete(requet_cl,valeurs)
        else:
            pass #si deja existe 

        #on chereche si les info d'entreprise deja exite dans BDD , sinon on vas l'ajouter , et relier avec l'utilisateur 
        requet_entrprise = f"SELECT * FROM entreprise WHERE id_utilisateur = '{self.id_utilisateur}';"
        requet_entrprise = self.BDD.execute_requete(requet_entrprise)
        print(requet_entrprise)
        if (len(requet_entrprise) == 0 ):
            #on ajoute les infos en reliant avec l'tilisateu , pour que la prochin fois , pas obliger de sissir tous infos
            requet_entrprise = "INSERT INTO entreprise (nom_entreprise, adresse, mail, telephone, nb_ser, logo, id_utilisateur) \
                    VALUES(?, ?, ?, ?, ?, ?, ? )"
            valeurs = (donnees_entrpris[0], donnees_entrpris[1], donnees_entrpris[2], donnees_entrpris[3], donnees_entrpris[4], donnees_entrpris[5], self.id_utilisateur)

            requet_entrprise = self.BDD.execute_requete(requet_entrprise, valeurs)
            print(donnees_entrpris[5])
        else:
            pass #si deja existe

        #on cherche la facture par son num , si il existe deja ( pour juste modifier l'infos ) sinon on cree une nouvelle
        requet_fact = f"SELECT num FROM facture WHERE num = '{num_fact}' AND id_utilisateur = '{self.id_utilisateur}';"
        requet_fact = self.BDD.execute_requete(requet_fact)
        if ( len(requet_fact) == 0 ):
            # si elle n'existe pas ou on la cree
            requet_fact = "INSERT INTO facture (num, date_fac, intervens, remarque, solde_du , info_pay, infos_banque, signatur, id_utilisateur, ref_client) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            valeurs = (num_fact, date_fact, donnees_articles, remarque, solde, donnees_payee, doonees_banque, self.signature, self.id_utilisateur, ref_client)
            resultat = self.BDD.execute_requete(requet_fact, valeurs)

        else:
            #ici au liux de parcourir chaque infos pour update , s'il y'a des modification on va supprimer l'encien facture et on ajoute la nouvelle modifiee
            encien_val = f"DELETE FROM facture WHERE num = '{num_fact}' AND id_utilisateur = '{self.id_utilisateur}';"
            sup_encien = self.BDD.execute_requete(encien_val)

            #on ajoute la nouvelle 
            requet_fact = "INSERT INTO facture (num, date_fac, intervens, remarque, solde_du , info_pay, infos_banque, signatur, id_utilisateur, ref_client) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            valeurs = (num_fact, date_fact, donnees_articles, remarque, solde, donnees_payee, doonees_banque, self.signature, self.id_utilisateur, ref_client)
            resultat = self.BDD.execute_requete(requet_fact, valeurs)

        messagebox.showinfo("Information", "La facture a été correctement enregistrée.")

        self.deja_enregist = 1


    def convert_pdf(self):
        num_fact = self.entry_num_fact.get() if (self.entry_num_fact.get()[0:6] =="FAC000") else f"FAC000{self.num_fact +1 }"
        date_fact = self.entry_date_fact.get()
        self.num_client = int(self.BDD.execute_requete(f"SELECT COUNT(*) AS nombre_de_lignes FROM client;")[0][0])
        ref_client = self.entry_ref_cleint.get() if(self.entry_ref_cleint.get()[0:5] == "CL000") else f"CL000{self.num_client + 1}"
        infos_facture = [num_fact, date_fact, ref_client]

        donnees_client = self.info_client.get_info()
        donnees_entrpris = self.info_entrprise.get_info()
        doonees_banque = self.info_bancaires.get_info()

        donnees_articles = self.info_table_articles.get_info()[0] #une liste qui contiens des liste ( chaque article represnter dans une liste)
        

        donnees_payee = self.info_table_articles.get_info()[1:] #[total_ht, total_ttc,remis,net, etat, mode, date_echan]
        solde = self.info_table_articles.get_info()[5]
        remarque = self.text_remarq.get("1.0", "end-1c")
        if(self.avoir_signature):
            self.signature = self.sign.get_bien_singe()
        else:
            self.signature = 0

        info_supplem = [donnees_payee, remarque, self.signature, doonees_banque ]
        convert_pdf(self.id_utilisateur, infos_facture, donnees_entrpris, donnees_client, donnees_articles, info_supplem, 0) # 0:  sinifie une facture 

        #apres la conertir en pdf , on l'ajoute en table basse donne
        #requet de checher d'abord si la client deaje dans BDD , sinon on va l'ajouter
        requet_cl = f"SELECT num FROM client WHERE num = '{ref_client}' AND id_utilisateur = '{self.id_utilisateur}';"
        requet_cl = self.BDD.execute_requete(requet_cl)
        if (len(requet_cl) == 0 ):
            #si le client n'est pas encore dans table client , on va l'ajouter
            requet_cl = "INSERT INTO client (num, nom, prenom, adresse, tel_fax, mobil, id_utilisateur) \
                    VALUES(?, ?, ?, ?, ?, ?, ? )" 

            valeurs = (ref_client, donnees_client[0], donnees_client[1], donnees_client[2], donnees_client[3], donnees_client[4] , self.id_utilisateur )

            self.BDD.execute_requete(requet_cl,valeurs)
        else:
            pass #si deja existe 
        #on ajoute dans table facture 

        #on cherche la facture par son num , si il existe deja ( pour juste modifier l'infos ) sinon on cree une nouvelle
        requet_fact = f"SELECT num FROM facture WHERE num = '{num_fact}' AND id_utilisateur = '{self.id_utilisateur}';"
        requet_fact = self.BDD.execute_requete(requet_fact)
        if ( len(requet_fact) == 0 ):
            # si elle n'existe pas ou on la cree
            requet_fact = "INSERT INTO facture (num, date_fac, intervens, remarque, solde_du , info_pay, infos_banque, signatur, id_utilisateur, ref_client) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            #ici on transmet les liste avec json.dumps , pour ajouter en basse donne 
            valeurs = (num_fact, date_fact, json.dumps(donnees_articles), remarque, solde, json.dumps(donnees_payee), json.dumps(doonees_banque), self.signature, self.id_utilisateur, ref_client)
            resultat = self.BDD.execute_requete(requet_fact, valeurs)

        else:
            #ici au liux de parcourir chaque infos pour update , s'il y'a des modification on va supprimer l'encien facture et on ajoute la nouvelle modifiee
            encien_val = f"DELETE FROM facture WHERE num = '{num_fact}' AND id_utilisateur = '{self.id_utilisateur}';"
            sup_encien = self.BDD.execute_requete(encien_val)

            #on ajoute la nouvelle 
            requet_fact = "INSERT INTO facture (num, date_fac, intervens, remarque, solde_du , info_pay, infos_banque, signatur, id_utilisateur, ref_client) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            valeurs = (num_fact, date_fact, json.dumps(donnees_articles), remarque, solde, json.dumps(donnees_payee), json.dumps(doonees_banque), self.signature, self.id_utilisateur, ref_client)
            resultat = self.BDD.execute_requete(requet_fact, valeurs)

        

        messagebox.showinfo("Information", f"La facture a été  enregistré dans fichier {f"DATA/{num_fact}_ID_{self.id_utilisateur}"}.pdf")
        self.deja_enregist = 1




    def get_num_facture(self,event=None):
        if(self.entry_num_fact.get() != f"FAC000{self.num_fact +1 }"): 
            #on cherche la facture par son num , si il existe deja ( pour juste modifier l'infos ) sinon on cree une nouvelle
            #aussii on test la valeur entrer pour num facture , il faut que le num comence par FAC000.....
            if(self.entry_num_fact.get()[0:6] =="FAC000"):
                requet_fact = f"SELECT * FROM facture WHERE num = '{self.entry_num_fact.get()}' AND id_utilisateur = '{self.id_utilisateur}';"
                requet_fact = self.BDD.execute_requete(requet_fact)
                if ( len(requet_fact) != 0 ):
                    self.encien_facture = requet_fact[0]
                    self.canv_fact.delete("all")
                    self.cree_facture()
            else:
                messagebox.showerror("Erreur", "Le numéro de facture est invalide. Il doit commencer par FAC000.")


    def get_num_client(self,event=None):
        if(self.entry_ref_cleint.get() != f"CL000{self.num_client + 1}" ) :
            #on cherche si le ref de cleitn deja existe pour qu'on remplir direct les infos de cleint ;
            #en plus on test si le reference valide (commenc par CL000)
            if (self.entry_ref_cleint.get()[0:5] == "CL000"):
                #requet de checher d'abord si la client deaje dans BDD , sinon on va l'ajouter
                requet_cl = f"SELECT * FROM client WHERE num = '{self.entry_ref_cleint.get()}' AND id_utilisateur = '{self.id_utilisateur}';"
                requet_cl = self.BDD.execute_requete(requet_cl)
                if (len(requet_cl) != 0 ):
                    self.tous_infos_client = requet_cl[0]
                    self.remplir_client()

            else:
                messagebox.showerror("Erreur", "Le numéro de client est invalide. Il doit commencer par CL000.")


    def retour(self):
        if self.deja_enregist != 1:
            reponse = tk.messagebox.askquestion("Question", "Voulez-vous sauvegarder les modifications ?")
            if reponse == 'yes':
                self.enregistrer()

        self.frame_fact.destroy()
        self.canv_fact.destroy()
        self.root.event_generate("<<retour_history_fact>>")


    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            x = self.root.winfo_width()
            y = self.root.winfo_height()

            self.frame_button.config(width=x, height=(y // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=x, height=y)
            self.canvas.place(x=0, y=(y //11.42))

            self.frame_fact.config(width=1000, height=(y//1.176))
            self.frame_fact.place(x=(x-1000)//2, y=10)
            self.canv_fact.config(width=1000,height=(y//1.176))
