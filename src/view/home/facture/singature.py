import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageDraw


from const import DATA_DIR , COULEUR_LABEL
from tools.image_size import size_photo

class SignatureFrame():
    def __init__(self,canvas,frame,id_utilisateur):
        self.canv_fact = canvas
        self.frame = frame
        self.id_utilisateur = id_utilisateur
        self.image_sing = None
        self.bien_singee = 0 #variable pour indique si la facture ou devis contien un signature 

        self.canvas = tk.Canvas(self.frame, width=250, height=130, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.trace_signature)

        self.clear_button = tk.Button(self.frame, text="Effacer", command=self.clear_signature)
        self.clear_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.frame, text="Enregistrer", command=self.save_signature)
        self.save_button.pack(side=tk.RIGHT)

        self.signature_image = Image.new("RGBA", (250, 130), (255, 255, 255, 0) )
        self.draw = ImageDraw.Draw(self.signature_image)

        self.canv_fact.update_idletasks()  
        self.canv_fact.config(scrollregion=self.canv_fact.bbox("all"))

    def trace_signature(self, event):
        x, y = event.x, event.y
        r = 1
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
        self.draw.ellipse([x-r, y-r, x+r, y+r], fill="black")

    def clear_signature(self):
        self.canvas.delete("all")
        self.signature_image = Image.new("RGBA", (250, 130), (255, 255, 255, 0) )
        self.draw = ImageDraw.Draw(self.signature_image)

    def save_signature(self):
        filename = os.path.join(DATA_DIR, f"signature_{self.id_utilisateur}.png")
        self.signature_image.save(filename)
        
        # Ouvrir l'image avec PIL
        image = os.path.join(DATA_DIR, f"signature_{self.id_utilisateur}.png")
        self.image_sing = size_photo(image, 220 , 150)
        
        if self.frame : 
            # on change le frame par l'image
            self.canv_fact.delete("frame_sing")
            x, y = self.canv_fact.coords("sing") #on cherche la possition de singateur pour metter la photo 
            self.frame = self.canv_fact.create_image( x+110 , y+40, anchor='ne', image=self.image_sing, tags="imag_sing")
            self.bien_singee = 1
            
        
    def get_bien_singe(self):
        return self.bien_singee
