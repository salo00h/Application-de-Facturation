import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk, ImageDraw
import datetime


from const import *
from tools.event_entry import effacer_indicatif, effacer_Text_indicatif
from tools.image_size import size_photo



class InfosEntreprise():
    def __init__(self,canvas,BDD, id_utilisateur ):
        self.canv_fact = canvas
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur  #pour chercher si ces infos deaj existe dans basse et aussi pour relier nom d'image logo per son id 

    
        self.infos_entr = None
        self.chemin_logo = None # ici le logo qu'on' retenu
        self.image_logo = None #ici pour faire referance de l'image pour son affichage 
        

        self.cherche_infos_entr() #on voir table basse donne si avoir l'infos de l'entrprise 

        self.info_entrprise()
        

        self.canv_fact.tag_bind(self.logo, "<Button-1>", self.choisir_photo)


    def info_entrprise(self):
        expredature = tk.Label(self.canv_fact, text="De : ",bg=COULEUR_LABEL,font=(POLICE, 15,"bold"))
        self.canv_fact.create_window(50, 185, anchor="n", window=expredature)
        
        # Nom entreprise
        nom_entreprise_label = tk.Label(self.canv_fact, text="Nom : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(60, 215, anchor="n", window=nom_entreprise_label)
        self.entry_nom = tk.Entry(self.canv_fact,width=35,font=(POLICE,9))
        self.canv_fact.create_window(225, 215, anchor="n", window=self.entry_nom)
        # Adresse entreprise
        adresse_entreprise_label = tk.Label(self.canv_fact, text="Adresse:",bg=COULEUR_LABEL)
        self.canv_fact.create_window(53, 261, anchor="n", window=adresse_entreprise_label)
        self.entry_adrs_entr = tk.Text(self.canv_fact,width=35,height=3,font=(POLICE,9))
        self.canv_fact.create_window(225, 240, anchor="n", window=self.entry_adrs_entr)

        mail_entreprise_label = tk.Label(self.canv_fact, text="Mail : ",bg=COULEUR_LABEL)
        self.canv_fact.create_window(60, 300, anchor="n", window=mail_entreprise_label)
        self.entry_mail_entr = tk.Entry(self.canv_fact,width=35,font=(POLICE,9))
        self.canv_fact.create_window(225, 300, anchor="n", window=self.entry_mail_entr)

        telphon_entreprise_label = tk.Label(self.canv_fact, text="Tél.fixe:",bg=COULEUR_LABEL)
        self.canv_fact.create_window(53, 325, anchor="n", window=telphon_entreprise_label)
        self.entry_tel_entr =tk.Entry(self.canv_fact,width=35,font=(POLICE,9))
        self.canv_fact.create_window(225, 325, anchor="n", window=self.entry_tel_entr)

        N_siren_label = tk.Label(self.canv_fact, text="N° SIREN/SIRET",bg=COULEUR_LABEL)
        self.canv_fact.create_window(67, 350, anchor="n", window=N_siren_label)
        self.entry_siren_entr = tk.Entry(self.canv_fact,width=31,font=(POLICE,9))
        self.canv_fact.create_window(240, 350, anchor="n", window=self.entry_siren_entr)

        if (self.infos_entr):
            self.entry_nom.insert(0, self.infos_entr[0])
            self.entry_adrs_entr.insert(tk.END, self.infos_entr[1])
            self.entry_mail_entr.insert(0, self.infos_entr[2])
            self.entry_tel_entr.insert(0, self.infos_entr[3])
            self.entry_siren_entr.insert(0, self.infos_entr[4])

            self.chemin_logo = self.infos_entr[5]
            self.image_logo = size_photo(self.chemin_logo, 220,150)
            self.logo = self.canv_fact.create_image(20, 30, anchor='nw', image=self.image_logo, tags="logo")
            
        else:
            #on voir si y'a le logo 
            if(self.chemin_logo ):
                self.image_logo = size_photo(self.chemin_logo, 220,150)
                self.logo = self.canv_fact.create_image(20, 30, anchor='nw', image=self.image_logo, tags="logo")

            else:
                # Logo entreprise
                self.logo = self.canv_fact.create_rectangle(15, 20, 270, 170, fill=COULEUR_PRINCIPALE,tags="logo")
                # Ajout d'un label sur le rectangle
                self.label_logo = self.canv_fact.create_text(140, 95, text="Ajoute Logo", font=("Arial", 10),tags="click")
        
            self.entry_nom.config(fg="gray")
            self.entry_nom.insert(0, "Nom Entreprise")
            self.entry_adrs_entr.config(fg="gray")
            self.entry_adrs_entr.insert(tk.END, "Rue ....")
            self.entry_mail_entr.config(fg="gray")
            self.entry_mail_entr.insert(0, "contacte@nom.fr")
            self.entry_tel_entr.config(fg="gray")
            self.entry_tel_entr.insert(0, "(123) 456 789")
            self.entry_siren_entr.config(fg="gray")
            self.entry_siren_entr.insert(0, "Gt; 123-45-6789")

            self.event_entry_case()


    def cherche_infos_entr(self):
        requt = f"SELECT * FROM entreprise WHERE id_utilisateur = '{self.id_utilisateur}';"
        list_info = self.BDD.execute_requete(requt)
        
        if (len(list_info) == 0):
            #si l'infos d'entrprise n'existe pas dans table 
            self.infos_entr = None
        else:
            
            #on verifeir les 3 infos princibal : nom,adresse et mail ; sans les 3 infos on peux pas afficher l'infos existe dans table 
            if (list_info[0][0] != "") and (list_info[0][1] != "") and (list_info[0][2] != ""):
                self.infos_entr = list_info[0]
            
            if(list_info[0][5] != ""):
                #dans cas y'a le logo mais le nom et adre et mail n'existe pas 
                self.chemin_logo = list_info[0][5]
                
                

    def event_entry_case(self):
        """on active l'event pour case enrty pour quand l'utilisateur tape le case , l'example existe va supprimer 
            par la fonction importée (effacer_indicatif) qui prend le variable Entry et son text indicatif
        """
        self.entry_nom.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_nom,"Nom Entreprise"))
        self.entry_adrs_entr.bind("<FocusIn>", lambda event: effacer_Text_indicatif(self.entry_adrs_entr,"Rue ...."))
        self.entry_mail_entr.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_mail_entr,  "contacte@nom.fr"))
        self.entry_tel_entr.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_tel_entr, "(123) 456 789"))
        self.entry_siren_entr.bind("<FocusIn>", lambda event: effacer_indicatif(self.entry_siren_entr, "Gt; 123-45-6789"))

    def get_info(self):
        nom = self.entry_nom.get() if ( self.entry_nom.get() != "Nom Entreprise") else ""
        adr = self.entry_adrs_entr.get("1.0", "end-1c") if ( self.entry_adrs_entr.get("1.0", "end-1c") != "Rue ....")  else ""
        mail = self.entry_mail_entr.get() if (self.entry_mail_entr.get()!= "contacte@nom.fr") else ""
        tel = self.entry_tel_entr.get() if ( self.entry_tel_entr.get() != "(123) 456 789" ) else ""
        nb_ser = self.entry_siren_entr.get() if ( self.entry_siren_entr.get() !=  "Gt; 123-45-6789") else ""

        logo = self.chemin_logo

        return [nom, adr, mail, tel, nb_ser, logo]

    def choisir_photo(self, event=None):
        #self.canv_fact.delete("click")
        self.chemin_logo = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=(("Fichiers PNG", "*.png"), ("Fichiers JPEG", "*.jpg;*.jpeg"), ("Tous les fichiers", "*.*"))
        )
        if self.chemin_logo:
            try:
                # Supprimer l'image existante s'il y en a une
                #if os.path.exists(os.path.join(DATA_DIR, f"logo_{self.id_utilisateur}.png")):
                    #os.remove(os.path.join(DATA_DIR, f"logo_{self.id_utilisateur}.png"))
            
                #origin_image = Image.open(self.chemin_logo)
                #copie_image = origin_image.copy() #on crre un copie pour mettre dans donner de logiciel
                #copie_image.save(f"DATA/logo_{self.id_utilisateur}.png")

                #self.chemin_logo = os.path.join(DATA_DIR, f"logo_{self.id_utilisateur}.png")
                self.image_logo = size_photo(self.chemin_logo, 220,150)
                
                if self.logo:
                    self.canv_fact.delete("logo")
                self.canv_fact.delete("click")
                # Créer une nouvelle image sur le canevas
                self.logo = self.canv_fact.create_image(20, 30, anchor='nw', image=self.image_logo, tags="logo")
            
            except Exception as e:
                print("Erreur lors du chargement de l'image :", e)
