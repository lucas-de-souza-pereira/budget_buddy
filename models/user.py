import customtkinter as ctk
import bcrypt
import tkinter as tk
from tkinter import messagebox

class User(ctk.CTkFrame):
    def __init__(self, master, show_main_menu, conn):
        super().__init__(master)
        self.show_main_menu = show_main_menu  

        self.current_mode = ctk.get_appearance_mode()
        self.conn = conn

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame pour la création de compte
        self.create_account_frame = ctk.CTkFrame(self)
        self.create_account_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.create_tittle = ctk.CTkLabel(self.create_account_frame, text="Créer un compte", font=("Arial", 18))
        self.create_tittle.pack(pady=30)

        # Champs de la création de compte
        self.last_name_entry = ctk.CTkEntry(self.create_account_frame, placeholder_text="Nom")
        self.last_name_entry.pack(pady=10)

        self.first_name_entry = ctk.CTkEntry(self.create_account_frame, placeholder_text="Prénom")
        self.first_name_entry.pack(pady=10)

        self.email_entry_create = ctk.CTkEntry(self.create_account_frame, placeholder_text="Email")
        self.email_entry_create.pack(pady=10)

        self.password_entry_create = ctk.CTkEntry(self.create_account_frame, placeholder_text="Mot de passe", show="*")
        self.password_entry_create.pack(pady=10)

        # Checkbox pour afficher/masquer le mot de passe
        self.show_password_create = ctk.CTkCheckBox(self.create_account_frame, text="Afficher le mot de passe", command=self.toggle_password_create)
        self.show_password_create.pack(pady=10)

        self.register_button = ctk.CTkButton(self.create_account_frame, text="Créer mon compte", command=self.create_user)
        self.register_button.pack(pady=10)

        # Frame pour la connexion
        self.account_connection_frame = ctk.CTkFrame(self)
        self.account_connection_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Champs à remplir pour se connecter
        self.connection_tittle = ctk.CTkLabel(self.account_connection_frame, text="Connexion", font=("Arial", 18))
        self.connection_tittle.pack(pady=30)

        self.email_entry_conn = ctk.CTkEntry(self.account_connection_frame, placeholder_text="Email")
        self.email_entry_conn.pack(pady=10)

        self.password_entry_conn = ctk.CTkEntry(self.account_connection_frame, placeholder_text="Mot de passe", show="*")  
        self.password_entry_conn.pack(pady=10)

        # Checkbox pour afficher/masquer le mot de passe
        self.show_password_conn = ctk.CTkCheckBox(self.account_connection_frame, text="Afficher le mot de passe", command=self.toggle_password_conn)
        self.show_password_conn.pack(pady=10)

        self.login_button = ctk.CTkButton(self.account_connection_frame, text="Se connecter", command=self.sign_in)
        self.login_button.pack(pady=10)

        self.theme_button = ctk.CTkButton(self, text="Changer de thème", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, padx=10, pady=5, columnspan=3)

    def toggle_password_create(self):
        """ Affiche ou masque le mot de passe lors de la création du compte """
        if self.show_password_create.get():
            self.password_entry_create.configure(show="")
        else:
            self.password_entry_create.configure(show="*")

    def toggle_password_conn(self):
        """ Affiche ou masque le mot de passe lors de la connexion """
        if self.show_password_conn.get():
            self.password_entry_conn.configure(show="")
        else:
            self.password_entry_conn.configure(show="*")

    def user_exists(self, email):
        self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = self.conn.cursor.fetchone()
        return user is not None 

    def create_user(self):
        self.conn.connect_db()

        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        email = self.email_entry_create.get()
        password = self.password_entry_create.get()

        if not last_name or not first_name or not email or not password:
            messagebox.showinfo("Erreur", "Vous devez remplir tous les champs.")
            return

        elif self.user_exists(email):
            print("Cet utilisateur existe déjà !")
            messagebox.showinfo("Erreur", "L'utilisateur existe déjà")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            query = "INSERT INTO users (last_name, first_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (last_name, first_name, email, hashed_password.decode('utf-8'))

            self.conn.cursor.execute(query, values)
            self.conn.mydb.commit()

            self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone()
            user_id = user[0]

            messagebox.showinfo("Succès", "Inscription réussie !")
            print("Inscription réussie !")
            self.show_main_menu(user_id)

            self.last_name_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.email_entry_create.delete(0, tk.END)
            self.password_entry_create.delete(0, tk.END)

        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            self.conn.close_db()

    def check_connection(self, email, password):
        """ Vérifie les identifiants et passe au menu si valide """
        try:
            self.conn.cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone() 
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')): 
                return True
        except Exception as e:
            print("Erreur", e)
        finally:
            self.conn.close_db()

        return False

    def toggle_theme(self):
        """ Basculer entre le thème clair et sombre """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)
    
    def sign_in(self):
        self.conn.connect_db()

        email = self.email_entry_conn.get()
        password = self.password_entry_conn.get()
        try: 
            self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone()
            
            if not email or not password:
                messagebox.showinfo("Erreur", "Vous devez remplir tous les champs.")
            elif self.check_connection(email, password):
                print("Connexion réussie !")
                messagebox.showinfo("Succès", "Connexion réussie !")
                
                user_id = user[0]
                self.conn.set_user_id(user_id)

                print(f"🔍 [User] user_id transmis à Connect_db : {user_id}")

                self.show_main_menu()

                self.email_entry_conn.delete(0, tk.END)
                self.password_entry_conn.delete(0, tk.END)
            else:
                messagebox.showinfo("Erreur", "Email ou mot de passe incorrect")
                print("Email ou mot de passe incorrect")

        except Exception as e:
            print("Erreur lors de la connexion :", e)
        finally:
            self.conn.close_db()

    def show(self):
        """ Afficher l'écran de connexion """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher l'écran de connexion """
        self.grid_remove()
