# model/basse_donnes.py
import sqlite3
import os
from const import DATA_DIR

class BaseDeDonnee:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(DATA_DIR, "factur.db")  # Fichier SQLite portable
        self.db_path = db_path
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def execute_requete(self, requete: str, valeurs: tuple = None):
        """
        Exécute une requête SQL (SELECT/INSERT/UPDATE/DELETE).

        Args:
            requete: La requête SQL à exécuter.
            valeurs: Les paramètres optionnels pour la requête.

        Returns:
            Résultat pour SELECT, sinon None.
        """
        self.connect()
        if valeurs:
            self.cur.execute(requete, valeurs)
        else:
            self.cur.execute(requete)

        if requete.strip().upper().startswith("SELECT"):
            result = self.cur.fetchall()
            self.disconnect()
            return result
        else:
            self.conn.commit()
            self.disconnect()
            return None

    def init_table(self):
        """Initialise les tables à partir d'un fichier SQL"""
        fichier_basse = os.path.join(DATA_DIR, "cree_table.sql")
        self.connect()
        with open(fichier_basse, 'r') as f:
            self.cur.executescript(f.read())  # executescript pour plusieurs requêtes
        self.conn.commit()
        self.disconnect()
