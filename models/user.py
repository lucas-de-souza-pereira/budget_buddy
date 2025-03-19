import customtkinter as ctk
import bcrypt
import sqlite3

from models.connect_db import Connect_db
from tkinter import messagebox



class User(ctk.CTkFrame):
    def __init__(self, master, show_main_menu):
        super().__init__(master)
        self.show_main_menu = show_main_menu  # Permet de naviguer vers le menu principal

        self.conn = Connect_db()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Conteneur centré
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0)


        self.label_title = ctk.CTkLabel(self.container, text="Bienvenue", font=("Arial", 20))
        self.label_title.pack(padx=200,pady=20)

        self.label_nom = ctk.CTkLabel(self.container, text="Nom:")
        self.label_nom.pack(pady=5)
        self.entry_nom = ctk.CTkEntry(self.container)
        self.entry_nom.pack(pady=5)

        self.label_prenom = ctk.CTkLabel(self.container, text="Prénom:")
        self.label_prenom.pack(pady=5)
        self.entry_prenom = ctk.CTkEntry(self.container)
        self.entry_prenom.pack(pady=5)

        self.label_email = ctk.CTkLabel(self.container, text="Email:")
        self.label_email.pack(pady=5)
        self.entry_email = ctk.CTkEntry(self.container)
        self.entry_email.pack(pady=5)

        self.label_password = ctk.CTkLabel(self.container, text="Mot de passe:")
        self.label_password.pack(pady=5)
        self.entry_password = ctk.CTkEntry(self.container, show="*")
        self.entry_password.pack(pady=5)

        self.button_register = ctk.CTkButton(self.container, text="S'inscrire", command=self.create_user)
        self.button_register.pack(pady=10)

        self.button_login = ctk.CTkButton(self.container, text="Se connecter", command=self.sign_in)
        self.button_login.pack(pady=10)

        self.label_message = ctk.CTkLabel(self.container, text="")
        self.label_message.pack(pady=10)


    def user_exists(self,email):

        self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = self.conn.cursor.fetchone()

        return user is not None 
    
    def create_user(self):

        self.conn.connect_db()
        print("connexion ok")

        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        print(f"{nom} {prenom} {email} {password}")

        if self.user_exists(email):
            print("Cet utilisateur existe déjà !")
            messagebox.showinfo("Erreur", "L'utilisateur existe déjà")
            return
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        print(f"{nom} {prenom} {email} {hashed_password}")

        try:
            querry = "INSERT INTO users (last_name, first_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (nom, prenom, email, hashed_password.decode('utf-8'))

            self.conn.cursor.execute(querry,values)
            self.conn.mydb.commit()

            messagebox.showinfo("Succès", "Connexion réussie !")
            print("Inscription réussie !")
            self.show_main_menu() 
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            self.conn.close_db()

    def check_connection(self,email, password):

        self.conn.connect_db()
        print("connexion ok")

        try:
            self.conn.cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone() 
            
            self.conn.cursor.fetchall()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
                return True
        except Exception as e:
            print("Erreur", e)
        finally:
            self.conn.close_db()

        return False


    def sign_in(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if self.check_connection(email, password):
            print("Connexion réussie !")
            messagebox.showinfo("Succès", "Connexion réussie !")
            self.show_main_menu()
        else:
            print("Email ou mot de passe incorrect")


    def show(self):
        """ Afficher l'écran de connexion """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher l'écran de connexion """
        self.grid_remove()
