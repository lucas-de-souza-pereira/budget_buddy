
import customtkinter as ctk

class User(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
    
        self.label = ctk.CTkLabel(self,text="Connexion", font=("Arial",18))
        self.label.pack(pady = 10)

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20)

        self.grid_columnconfigure(0,weight=1)

    def button_callback(self):
        print("button pressed")


    def sign_in(self):
        pass
