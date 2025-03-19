import customtkinter as ctk
from tkinter import PhotoImage
import sqlite3
from tkinter import messagebox

class User(ctk.CTkFrame):
    def __init__(self, master, show_main_menu):
        super().__init__(master)
        self.show_main_menu = show_main_menu  

        self.current_language = "fr"
        self.current_mode = ctk.get_appearance_mode()

        self.flag_image_fr = PhotoImage(file="Assets/flag_france.png")
        self.flag_image_en = PhotoImage(file="Assets/uk_flag.png")

        # Configuration des colonnes et lignes
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Conteneur centré
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0)

        self.label = ctk.CTkLabel(self.container, text=self.get_text("label_title"), font=("Arial", 18))
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.container, placeholder_text=self.get_text("placeholder_username"))
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.container, placeholder_text=self.get_text("placeholder_password"), show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self.container, text=self.get_text("button_connecter"), command=self.sign_in)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self.container, text=self.get_text("button_inscrire"), command=self.register)
        self.register_button.pack(pady=5)

        self.theme_button = ctk.CTkButton(self.container, text=self.get_text("button_theme"), command=self.toggle_theme)
        self.theme_button.pack(side = "right", anchor ="n", padx = 10, pady = 40)

        # Bouton pour changer la langue, avec l'image initiale en français
        self.language_button = ctk.CTkButton(self.container, image=self.flag_image_fr, text=self.get_text("button_language"), command=self.toggle_language)
        self.language_button.pack(side = "left", anchor ="n", padx = 10, pady = 40)

        self.setup_database()

    def get_text(self, key):
        """ Retourne le texte correspondant en fonction de la langue actuelle """
        texts = {
            "fr": {
                "label_title": "Connexion",
                "placeholder_username": "Nom d'utilisateur",
                "placeholder_password": "Mot de passe",
                "button_connecter": "Se connecter",
                "button_inscrire": "Créer un compte",
                "button_theme": "Changer de Thème",
                "button_language": "Passer en Anglais",
            },
            "en": {
                "label_title": "Login",
                "placeholder_username": "Username",
                "placeholder_password": "Password",
                "button_connecter": "Log In",
                "button_inscrire": "Create Account",
                "button_theme": "Change Theme",
                "button_language": "Switch to French",
            }
        }
        return texts[self.current_language].get(key, key)  # Renvoie le texte correspondant ou la clé par défaut

    def toggle_theme(self):
        """ Basculer entre le thème clair et sombre """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)
    

    def toggle_language(self):
        """ Basculer entre les langues (Français / Anglais) """
        self.current_language = "fr" if self.current_language == "en" else "en"
        
        self.update_texts()

        if self.current_language == "fr":
            self.language_button.configure(image=self.flag_image_fr)
        else:
            self.language_button.configure(image=self.flag_image_en)

    def update_texts(self):
        """ Met à jour les textes des éléments de l'interface selon la langue actuelle """
        self.label.configure(text=self.get_text("label_title"))
        self.username_entry.configure(placeholder_text=self.get_text("placeholder_username"))
        self.password_entry.configure(placeholder_text=self.get_text("placeholder_password"))
        self.login_button.configure(text=self.get_text("button_connecter"))
        self.register_button.configure(text=self.get_text("button_inscrire"))
        self.theme_button.configure(text=self.get_text("button_theme"))
        self.language_button.configure(text=self.get_text("button_language"))

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
            self.show_main_menu()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def show(self):
        """ Afficher l'écran de connexion """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher l'écran de connexion """
        self.grid_remove()
