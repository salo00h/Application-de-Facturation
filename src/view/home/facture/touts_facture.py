import tkinter as tk


from PIL import Image,ImageTk, ImageDraw
from tkinter import filedialog


from const import *
from tools.event_entry import effacer_indicatif



class ToutesFacture():
    def __init__(self, root, canvas, frame_button, recherhe_fact, BDD, id_utilisateur):
        self.root = root
        self.canvas = canvas
        self.frame_button = frame_button
        self.recherhe_fact = recherhe_fact  #pour checher dans factures

        self.BDD = BDD
        self.id_utilisateur = id_utilisateur
        
        
        self.root.after(10, self.initialisation)
        self.root.bind("<Configure>", self.on_configure)
        
        

        
    def initialisation(self):

        self.x = self.root.winfo_width()
        self.y = self.root.winfo_height()

        #si il existe deja le frame dans canvas on va le supprimer 
        if( self.canvas.find_withtag("frame_list")):
            self.canvas.delete("frame_list")


        self.frame_list = tk.Frame(self.canvas, width=(self.x//1.2), height=(self.y//1.6), bg=COULEUR_LABEL)
        self.frame_list.grid_propagate(False)  # Empêcher le frame de redimensionner ses cellules
        self.canvas.create_window(600, (self.y // 6) , anchor="n", window=self.frame_list,tags="frame_list")

        fact = tk.Label(self.canvas, text="Facture",bg=COULEUR_LABEL)
        self.canvas.create_window(600, (self.y // 8) , anchor="n", window=fact,tags="fact")
        client = tk.Label(self.canvas, text="Client",bg=COULEUR_LABEL)
        self.canvas.create_window(700, (self.y // 8) , anchor="n", window=client,tags="client")
        date = tk.Label(self.canvas, text="Date",bg=COULEUR_LABEL)
        self.canvas.create_window(800, (self.y // 8) , anchor="n", window=date,tags="date")
        solde = tk.Label(self.canvas, text="Solde Dû ",bg=COULEUR_LABEL)
        self.canvas.create_window(900, (self.y // 8) , anchor="n", window=solde,tags="solde")
        

        # Création de la listebox
        self.listbox = tk.Listbox(self.frame_list, selectmode=tk.SINGLE, width=int(self.x//1.2), height=int (self.y//2))
        self.listbox.pack(expand=True, fill=tk.BOTH)
        

    def on_configure(self, event):
        if (self.canvas):
            # Recalculer les dimensions de la fenêtre
            x = self.root.winfo_width()
            y = self.root.winfo_height()

            self.canvas.config(width=x, height=y)

            self.frame_button.config(width=x, height=(y // 11.42))
            self.frame_button.place(x=0, y=0)

            #self.frame_list.config(width=1000, height=(y//1.6))
            #self.canvas.coords("frame_list",600, y//6)
            
