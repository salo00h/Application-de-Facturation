import tkinter as tk
import os


from const import *
from view.login_page.login import Login
from model.basse_donnes import BaseDeDonnee

class Connection():
    def __init__(self,root,BDD):
        self.root = root
        self.BDD =BDD

        self.root.bind("<<retour_login_clicked>>", self.click_retour_login)


    def main_connec(self):
        Login(self.root,self.BDD)

        
    def click_retour_login(self, event=None):
        self.main_connec()