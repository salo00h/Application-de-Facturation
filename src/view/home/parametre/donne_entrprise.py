import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image,ImageTk, ImageDraw

from const import *
from tools.image_size import size_photo

class GereEntrprise():
    def __init__(self,root,canvas, frame_button,BDD,id_utilisateur):
        self.root = root
        self.canvas = canvas
        self.frame_button = frame_button
        self.BDD = BDD
        self.id_utilisateur = id_utilisateur

        self.image_logo = None
        self.chemin_logo= None

        
        self.root.after(10, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)

        
    def initialisation(self):

        x = self.root.winfo_width()
        y = self.root.winfo_height()
        
        
        requt_entrpris = f"SELECT * FROM entreprise WHERE id_utilisateur = '{self.id_utilisateur}' ;"
        tous_ifos = self.BDD.execute_requete(requt_entrpris)
        
        if (len(tous_ifos)!= 0) :

            self.nom_entr = tous_ifos[0][0]
            self.addres = tous_ifos[0][1]
            self.mail = tous_ifos[0][2]
            self.fixe = tous_ifos[0][3]
            self.nb_sr = tous_ifos[0][4]
            self.log = tous_ifos[0][5]
        else:
            self.nom_entr = ""
            self.addres = ""
            self.mail = ""
            self.fixe = ""
            self.nb_sr = ""
            self.log =None
        

        self.fram_infos = tk.Frame(self.canvas,width=450, height=530, bg=COULEUR_LABEL)
        self.canvas.create_window(890,140 , anchor="n", window=self.fram_infos,tags="fram_info")
        self.fram_infos.grid_propagate(False)

        self.canvas_itern = tk.Canvas(self.fram_infos, width=450, height=530,bg=COULEUR_LABEL)
        self.canvas_itern.place(x=0,y=0)

        #frame_logo :
        
        if self.log != "None":
            self.image_logo = size_photo(self.log, 220,150)
            
            # Créer une nouvelle image sur le canevas
            self.frame_logo = self.canvas_itern.create_image(40, 10, anchor='nw', image=self.image_logo, tags="frame_logo")
        else:
            self.frame_logo = tk.Frame(self.canvas_itern,width=220, height=150, bg=COULEUR_PRINCIPALE)
            self.canvas_itern.create_window(130,30 , anchor="n", window=self.frame_logo,tags="frame_logo")
            lab_logo = tk.Label(self.frame_logo, text="+ logo",font=(POLICE, 12),bg=COULEUR_PRINCIPALE)
            lab_logo.place(x=60,y=60)


        choisi_logo = tk.Button(self.canvas_itern, text="Choisir Photo", command=lambda:self.choisir_photo(),
                                        bg=COULEUR_CANVAS,font=(POLICE, 9))
        self.canvas_itern.create_window(355,100 , anchor="n", window=choisi_logo)
        
        nom_en = tk.Label(self.canvas_itern, text="Nom D'entrprise : ",font=(POLICE, 10),bg=COULEUR_LABEL)
        self.canvas_itern.create_window(120,200 , anchor="n", window=nom_en)
        self.entr_nom_en = tk.Entry(self.canvas_itern,width=25, font=(POLICE, 10))
        self.canvas_itern.create_window(290,200 , anchor="n", window=self.entr_nom_en)
        self.entr_nom_en.insert(0,self.nom_entr)

        adr_en = tk.Label(self.canvas_itern, text="Adresse : ",font=(POLICE, 10),bg=COULEUR_LABEL)
        self.canvas_itern.create_window(120,240 , anchor="n", window=adr_en)
        self.entr_adr_en = tk.Text(self.canvas_itern,width=25,height=2, font=(POLICE, 10))
        self.canvas_itern.create_window(290,240 , anchor="n", window=self.entr_adr_en)
        self.entr_adr_en.insert(tk.END, self.addres)

        mail_en = tk.Label(self.canvas_itern, text="Mail : ",font=(POLICE, 10),bg=COULEUR_LABEL)
        self.canvas_itern.create_window(120,300 , anchor="n", window=mail_en)
        self.entr_mail_en = tk.Entry(self.canvas_itern,width=25, font=(POLICE, 10))
        self.canvas_itern.create_window(290,300 , anchor="n", window=self.entr_mail_en)
        self.entr_mail_en.insert(0,self.mail)

        fixe_en = tk.Label(self.canvas_itern, text="Tél. fixe : ",font=(POLICE, 10),bg=COULEUR_LABEL)
        self.canvas_itern.create_window(120,340 , anchor="n", window=fixe_en)
        self.entr_fixe_en = tk.Entry(self.canvas_itern,width=25, font=(POLICE, 10))
        self.canvas_itern.create_window(290,340 , anchor="n", window=self.entr_fixe_en)
        self.entr_fixe_en.insert(0, self.fixe)

        nb_en = tk.Label(self.canvas_itern, text="N° SIREN/SIRET : ",font=(POLICE, 10),bg=COULEUR_LABEL)
        self.canvas_itern.create_window(120,380 , anchor="n", window=nb_en)
        self.entr_nb_en = tk.Entry(self.canvas_itern,width=25, font=(POLICE, 10))
        self.canvas_itern.create_window(290,380 , anchor="n", window=self.entr_nb_en)
        self.entr_nb_en.insert(0, self.nb_sr)

        button_enrgs = tk.Button(self.canvas_itern, text="Enregistrer", command=lambda:self.save(),
                                        bg=COULEUR_BOUTON,fg= COULEUR_TEXT_BOUTON, font=(POLICE, 11))
        self.canvas_itern.create_window(320,475 , anchor="n", window=button_enrgs)

        button_ferm = tk.Button(self.canvas_itern, text="Fermer", command=lambda:self.fermer(),
                                        bg=COULEUR_CANVAS,font=(POLICE, 11))
        self.canvas_itern.create_window(160,475 , anchor="n", window=button_ferm)


    def save(self):
        if ( self.entr_nom_en.get() != self.nom_entr ):
            requt = f"UPDATE entreprise SET nom_entreprise = '{self.entr_nom_en.get()}' WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if ( self.entr_adr_en.get("1.0", "end-1c") != self.addres ):
            requt = f"UPDATE entreprise SET adresse = '{self.entr_adr_en.get("1.0", "end-1c")}' WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if ( self.entr_mail_en.get() != self.mail ):
            requt = f"UPDATE entreprise SET mail = '{self.entr_mail_en.get()}' WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if ( self.entr_fixe_en.get() != self.fixe ):
            requt = f"UPDATE entreprise SET telephone = '{self.entr_fixe_en.get()}' WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if ( self.entr_nb_en.get() != self.nb_sr ):
            requt = f"UPDATE entreprise SET nb_ser = '{self.entr_nb_en.get()}' WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        if( self.chemin_logo != None) and ( self.chemin_logo != self.log ):
            requt = f"UPDATE entreprise SET logo = '{self.chemin_logo}' WHERE id_utilisateur = '{self.id_utilisateur}' ;"
            self.BDD.execute_requete(requt)
        else:
            pass

        self.fram_infos.destroy()


    def fermer(self):
        self.fram_infos.destroy()

    def choisir_photo(self):
        
        self.chemin_logo = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=(("Fichiers PNG", "*.png"), ("Fichiers JPEG", "*.jpg;*.jpeg"), ("Tous les fichiers", "*.*"))
        )
        if self.chemin_logo:
            try:
                # Ouvrir l'image avec PIL
                #origin_image = Image.open(self.chemin_logo)
                #copie_image = origin_image.copy()
                #copie_image.save(f"DATA/logo_{self.id_utilisateur}.png")

                #self.chemin_logo = os.path.join(DATA_DIR, f"logo_{self.id_utilisateur}.png")
                self.image_logo = size_photo(self.chemin_logo, 220,150)
                if self.frame_logo:
                    self.canvas_itern.delete("frame_logo")
                # Créer une nouvelle image sur le canevas
                self.frame_logo = self.canvas_itern.create_image(130, 30, anchor='n', image=self.image_logo, tags="frame_logo")
            
            except Exception as e:
                print("Erreur lors du chargement de l'image :", e)

    
    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            long = self.root.winfo_width()
            haut = self.root.winfo_height()
            self.frame_button.config(width=long, height=(haut // 11.42))
            self.frame_button.place(x=0, y=0)

            self.canvas.config(width=long, height=haut)
            self.canvas.place(x=0, y=(haut // 11.42))