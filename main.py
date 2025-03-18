from models.connect_db import Connect_db
from models.historical import Historical
from models.transaction import Transaction
from models.user import User

import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 500
        self.title("Budget Buddy")
        self.geometry(f"{self.width}x{self.height}")


        self.login_frame = User(self)


        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        """ Affiche uniquement le frame sélectionné """
        frame.tkraise() 



    # def button_callback():
    #     print("button pressed")

    #     button = ctk.CTkButton(self, text="my button", command=button_callback)
    #     button.grid(row=0, column=0, padx=20, pady=20)

    #     self.grid_columnconfigure(0,weight=1)



app = App()
app.mainloop()