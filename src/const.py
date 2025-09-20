import os

# Définissez vos variables globales ici
LONGUEUR = 1200  # Longueur de la fenêtre
HAUTEUR = 1000  # Largeur de la fenêtre
COULEUR_PRINCIPALE = "#E2E2E2"  # Couleur principale de lapplication (coulur light orange)
COULEUR_CANVAS = "#BBBBBB"
COULEUR_BOUTON = "#001F5A"
COULEUR_TEXT_BOUTON = "#F3890B"
COULEUR_ENTRY = "gray"
COULEUR_LABEL = "lightgray"
POLICE = "Palatino Linotype"  # Police principale de l'application

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJ_DIR, "DATA")
