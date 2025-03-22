from models.connect_db import Connect_db
from models.historical import Historical

from models.mainmenu import Main_menu
from models.adminmenu import Admin_menu
from models.user import User
from models.transactions import TransactionManage


import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 500
        self.title("Budget Buddy")
        self.geometry(f"{self.width}x{self.height}")

        self.conn = Connect_db()

        # Configurer la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création des écrans
        self.login_frame = User(self, self.show_main_menu, self.show_admin_menu, self.conn)
        self.main_menu_frame = Main_menu(self, self.show_frame,self.conn)
        self.admin_menu_frame = Admin_menu(self, self.show_frame,self.conn)
        self.transaction_frame = TransactionManage(self,self.show_frame, self.conn)

        # Afficher uniquement la connexion au début
        self.main_menu_frame.hide()
        self.admin_menu_frame.hide()
        self.transaction_frame.hide()
        self.login_frame.show()

    def show_frame(self, frame):
        """ Afficher uniquement le frame sélectionné """
        self.login_frame.hide()
        self.main_menu_frame.hide()
        self.admin_menu_frame.hide()
        self.transaction_frame.hide()

        frame.show()

    def show_main_menu(self, user_id):
        """ Passe au menu principal après connexion """
        self.main_menu_frame.select_account()
        self.main_menu_frame.load_user_data()
        self.show_frame(self.main_menu_frame)

        
    def show_admin_menu(self, email):
        """ Passe au menu admin après connexion """
        self.admin_menu_frame.select_account()
        self.admin_menu_frame.load_user_data()
        self.show_frame(self.admin_menu_frame)


    def show_transaction_page(self):
        self.show_frame(self.transaction_frame)
        self.transaction_frame.select_account()


if __name__ == "__main__":
    app = App()
    app.mainloop()
