import customtkinter as ctk
from tkinter import PhotoImage
import bcrypt

from tkinter import messagebox



class User(ctk.CTkFrame):
    def __init__(self, master, show_main_menu,conn):
        super().__init__(master)
        self.show_main_menu = show_main_menu  

        self.current_language = "fr"
        self.current_mode = ctk.get_appearance_mode()
        self.conn = conn
        self.flag_image_fr = PhotoImage(file="Assets/flag_france.png")
        self.flag_image_en = PhotoImage(file="Assets/uk_flag.png")

        # Configuration des colonnes et lignes
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Conteneur centré
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0)

        self.label_title = ctk.CTkLabel(self.container, text=self.get_text("label_title"), font=("Arial", 18))
        self.label_title.pack(padx=200,pady=10)

        self.last_name_entry = ctk.CTkEntry(self.container, placeholder_text=self.get_text("placeholder_last_name"))
        self.last_name_entry.pack(pady=5)

        self.first_name_entry = ctk.CTkEntry(self.container, placeholder_text=self.get_text("placeholder_first_name"))
        self.first_name_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.container, placeholder_text=self.get_text("placeholder_password"), show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self.container, text=self.get_text("button_connecter"), command=self.sign_in)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self.container, text=self.get_text("button_inscrire"), command=self.create_user)
        self.register_button.pack(pady=5)

        self.theme_button = ctk.CTkButton(self.container, text=self.get_text("button_theme"), command=self.toggle_theme)
        self.theme_button.pack(side = "right", anchor ="n", padx = 10, pady = 40)

        self.language_button = ctk.CTkButton(self.container, image=self.flag_image_fr, text=self.get_text("button_language"), command=self.toggle_language)
        self.language_button.pack(side = "left", anchor ="n", padx = 10, pady = 40)

        self.label_message = ctk.CTkLabel(self.container, text="")
        self.label_message.pack(pady=10)


    def user_exists(self,email):

        self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = self.conn.cursor.fetchone()

        return user is not None 
    
    def create_user(self):

        self.conn.connect_db()

        nom = self.last_name_entry.get()
        prenom = self.first_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if self.user_exists(email):
            print("Cet utilisateur existe déjà !")
            messagebox.showinfo("Erreur", "L'utilisateur existe déjà")
            return
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            querry = "INSERT INTO users (last_name, first_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (nom, prenom, email, hashed_password.decode('utf-8'))

            self.conn.cursor.execute(querry,values)
            self.conn.mydb.commit()
        
            self.conn.cursor.execute("SELECT id FROM users WHERE email = %s",(email,))

            user = self.conn.cursor.fetchone()
            user_id = user[0]

            messagebox.showinfo("Succès", "Connexion réussie !")
            print("Inscription réussie !")
            self.show_main_menu(user_id) 
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            self.conn.close_db()

    def check_connection(self,email, password):
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

    def get_text(self, key):
        """ Retourne le texte correspondant en fonction de la langue actuelle """
        texts = {
            "fr": {
                "label_title": "Connexion / Inscription",
                "placeholder_last_name": "Nom",
                "placeholder_first_name": "Prénom",
                "placeholder_password": "Mot de passe",
                "button_connecter": "Se connecter",
                "button_inscrire": "Créer un compte",
                "button_theme": "Changer de Thème",
                "button_language": "Passer en Anglais",
                "error_text": "Erreur",
                "error_message": "Nom d'utilisateur ou mot de passe incorrect."
            },
            "en": {
                "label_title": "Login / Register",
                "placeholder_last_name": "Last Name",
                "placeholder_first_name": "First Name",
                "placeholder_password": "Password",
                "button_connecter": "Log In",
                "button_inscrire": "Create Account",
                "button_theme": "Change Theme",
                "button_language": "Switch to French",
                "error_text": "Error",
                "error_message": "Incorrect username or password."
            }
        }
        return texts[self.current_language].get(key, key)

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
        self.label_title.configure(text=self.get_text("label_title"))
        self.last_name_entry.configure(placeholder_text=self.get_text("placeholder_last_name"))
        self.first_name_entry.configure(placeholder_text=self.get_text("placeholder_first_name"))
        self.password_entry.configure(placeholder_text=self.get_text("placeholder_password"))
        self.login_button.configure(text=self.get_text("button_connecter"))
        self.register_button.configure(text=self.get_text("button_inscrire"))
        self.theme_button.configure(text=self.get_text("button_theme"))
        self.language_button.configure(text=self.get_text("button_language"))

    def sign_in(self):

        self.conn.connect_db()

        email = self.email_entry.get()
        password = self.password_entry.get()
        texts = {
            "fr": {
                "error_text": "Erreur",
                "error_message": "Nom d'utilisateur ou mot de passe incorrect.",
                "success_message": "Connexion réussie !",
                "empty_fields": "Veuillez remplir tous les champs."

            },
            "en": {
                "error_text": "Error",
                "error_message": "Incorrect username or password.",
                "success_message": "Login successful !",
                "empty_fields": "Please fill in all fields."
            }
        }

        try : 
            self.conn.cursor.execute("SELECT id FROM users WHERE email = %s",(email,))
            user = self.conn.cursor.fetchone()

            if self.check_connection(email, password):
                print("Connexion réussie !")
                messagebox.showinfo("Succès", "Connexion réussie !")
                
                user_id = user[0]
                self.conn.set_user_id(user_id)  # 🔹 Stocke l'ID utilisateur

                print(f"🔍 [User] user_id transmis à Connect_db : {user_id}")

                self.show_main_menu()
            else:
                messagebox.showinfo("Erreur", "Email ou mot de passe incorrect")
                print("Email ou mot de passe incorrect")

        except Exception as e:
            print("Erreur lors de la connexion :", e)
        finally:
            self.conn.close_db()

        # if not email or not password:
        #     messagebox.showerror(texts[self.current_language]["error_text"], texts[self.current_language]["empty_fields"])

        # elif user:
        #     messagebox.showinfo(texts[self.current_language]["success_message"])
        #     self.show_main_menu()
        # else:
        #     messagebox.showerror(texts[self.current_language]["error_text"], texts[self.current_language]["error_message"])

    def show(self):
        """ Afficher l'écran de connexion """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher l'écran de connexion """
        self.grid_remove()
