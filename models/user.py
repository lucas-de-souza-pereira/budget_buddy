import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class User(ctk.CTkFrame):
    def __init__(self, master, show_main_menu):
        super().__init__(master)
        self.show_main_menu = show_main_menu  # Permet de naviguer vers le menu principal

        

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Conteneur centré
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0)

        self.label = ctk.CTkLabel(self.container, text="Connexion", font=("Arial", 18))
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="Nom d'utilisateur")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.container, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self.container, text="Se connecter", command=self.sign_in)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self.container, text="Créer un compte", command=self.register)
        self.register_button.pack(pady=5)

        self.setup_database()

    def setup_database(self):
        """ Création de la base de données SQLite """
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def sign_in(self):
        """ Vérifie les identifiants et passe au menu si valide """
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Succès", "Connexion réussie !")
            self.show_main_menu()  # Passe au menu principal
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def show(self):
        """ Afficher l'écran de connexion """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher l'écran de connexion """
        self.grid_remove()
