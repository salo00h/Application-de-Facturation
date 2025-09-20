from PIL import Image, ImageTk

def size_photo(image, x, y):
    if image == "None" or image is None:
        return None
    else:
        try:
            # Ouvrir l'image depuis le chemin du fichier
            lire_photo = Image.open(image)
            image_modf = ImageTk.PhotoImage(lire_photo.resize((x, y)))  # Redimensionner l'image
            return image_modf
        except Exception as e:
            print(f"Erreur lors de l'ouverture de l'image: {e}")
            return None
