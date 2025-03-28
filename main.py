from models.connect_db import Connect_db
from models.filter import TransactionApp
from models.mainmenu import Main_menu
from models.user import User
from models.transactions import TransactionManage
from models.adminmenu import Admin_menu

import customtkinter as ctk
import sys

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 500
        self.title("Budget Buddy")
        self.geometry(f"{self.width}x{self.height}")

        self.conn = Connect_db()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure the main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create the screens
        self.login_frame = User(self, self.show_main_menu, self.show_admin_menu, self.conn)
        self.main_menu_frame = Main_menu(self, self.show_frame, self.conn)
        self.transaction_frame = TransactionManage(self, self.show_frame, self.conn)
        self.search_frame = TransactionApp(self, self.show_frame, self.conn)
        self.admin_menu_frame = Admin_menu(self, self.show_frame, self.conn)

        # Show only the login screen initially
        self.main_menu_frame.hide()
        self.transaction_frame.hide()
        self.search_frame.hide()
        self.admin_menu_frame.hide()
        self.login_frame.show()

    def show_frame(self, frame):
        """ Show only the selected frame """
        self.login_frame.hide()
        self.main_menu_frame.hide()
        self.transaction_frame.hide()
        self.search_frame.hide()
        self.admin_menu_frame.hide()

        frame.show()

    def show_main_menu(self):
        """ Go to the main menu after login """
        self.main_menu_frame.select_account()
        self.main_menu_frame.load_user_data()
        self.show_frame(self.main_menu_frame)

    def show_transaction_page(self):
        """Show transaction frame"""
        self.show_frame(self.transaction_frame)
        self.transaction_frame.select_account()

    def show_search_frame(self):
        """Show filter frame"""
        self.show_frame(self.search_frame)   

    def show_admin_menu(self):
        self.show_frame(self.admin_menu_frame)

    def on_closing(self):
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
