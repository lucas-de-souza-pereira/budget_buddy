from models.connect_db import Connect_db
from models.historical import Historical
from models.transaction import Transaction
from models.mainmenu import Main_menu
from models.user import User

import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 500
        self.title("Budget Buddy")
        self.geometry(f"{self.width}x{self.height}")

        # Configurer la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création des écrans
        self.login_frame = User(self, self.show_main_menu)
        self.main_menu_frame = Main_menu(self, self.show_frame)

        # Afficher uniquement la connexion au début
        self.main_menu_frame.hide()
        self.login_frame.show()

    def show_frame(self, frame):
        """ Afficher uniquement le frame sélectionné """
        self.login_frame.hide()
        self.main_menu_frame.hide()

        frame.show()

    def show_main_menu(self,user_id):
        """ Passe au menu principal après connexion """
        self.main_menu_frame.load_user_data(user_id)
        self.show_frame(self.main_menu_frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
