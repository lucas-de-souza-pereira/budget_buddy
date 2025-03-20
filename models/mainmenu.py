import customtkinter as ctk
from tkinter import messagebox

from models.connect_db import Connect_db


class Main_menu(ctk.CTkFrame):
    """ Dashboard pour l'utilisateur avec plusieurs blocs """
    def __init__(self, master, show_frame,conn):
        super().__init__(master)

        self.current_mode = ctk.get_appearance_mode()
        self.show_frame = show_frame  # Permet de naviguer entre les écrans
        self.conn = conn

        # 📌 Configuration de la grille
        self.grid_columnconfigure(0, weight=1)  # Colonne gauche
        self.grid_columnconfigure(1, weight=1)  # Colonne droite
        self.grid_rowconfigure(0, weight=1)  # Espacement vertical

        # 🏠 Bloc Informations utilisateur (à gauche)
        self.user_info_frame = ctk.CTkFrame(self)
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")  # Placement

        self.user_label = ctk.CTkLabel(self.user_info_frame, text="👤 Informations Utilisateur", font=("Arial", 16))
        self.user_label.pack(pady=10)

        self.user_name = ctk.CTkLabel(self.user_info_frame, text="Name : ")
        self.user_name.pack()

        self.user_email = ctk.CTkLabel(self.user_info_frame, text="Email : lucas@example.com")
        self.user_email.pack()

        self.create_account_button = ctk.CTkButton(self.user_info_frame,text= "Créer un compte",command=self.create_account)
        self.create_account_button.pack(pady=50)

        # 💰 Bloc Solde du compte bancaire (à droite)
        self.account_balance_frame = ctk.CTkFrame(self)
        self.account_balance_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Placement

        self.balance_label = ctk.CTkLabel(self.account_balance_frame, text="💰 Solde du Compte", font=("Arial", 16))
        self.balance_label.pack(pady=10)

        self.balance_amount = ctk.CTkLabel(self.account_balance_frame, text="Solde : 1500€")
        self.balance_amount.pack()

        # 🔄 Bouton de Déconnexion en bas
        self.logout_button = ctk.CTkButton(self, text="Déconnexion", command=lambda: self.show_frame(master.login_frame))
        self.logout_button.grid(row=1, column=0, columnspan=2, pady=20, sticky="e")

        self.theme_button = ctk.CTkButton(self, text="Changer de thème", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, padx=10, pady=5, sticky="w" )

    def toggle_theme(self):
        """ Basculer entre le thème clair et sombre """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)

    def load_user_data(self):
        """load information for user connected from DB"""
        self.conn.connect_db()

        try : 

            user_id = self.conn.get_user_id() 
            print(f"🔍 [Main_menu] user_id récupéré : {user_id}")  # Debug

            querry = """SELECT last_name,first_name,email
                        FROM users
                        WHERE id = %s
            """

            self.conn.cursor.execute(querry,(user_id,))
            user_conneted = self.conn.cursor.fetchone()

            # user_conneted = {
            #     "last_name" : user_conneted[0],
            #     "first_name" : user_conneted[1],
            #     "email" : user_conneted[2]
            # }
            
            self.user_name.configure(text= f"Name : {user_conneted[0]} {user_conneted[1]}")
            self.user_email.configure(text= f"Email : {user_conneted[2]}")

        except Exception as e:
            print("Erreur lors du chargement des infos utilisateur :", e)
        finally :
            self.conn.close_db()

    def create_account(self):
        """create an account"""
        
        self.conn.connect_db()

        try:

            user_id = self.conn.get_user_id()
            
            querry = """INSERT INTO accounts (balance,user_id)
                        VALUES (%s,%s)
                    """
            values = (0,user_id)

            self.conn.cursor.execute(querry,values)
            self.conn.mydb.commit()

            messagebox.showinfo("Création de compte", "Création de compte effectué")
            

        except Exception as e:
            print("Erreur lors de la connexion :", e)

        finally:
            self.conn.close_db()

    def show(self):
        """ Afficher le menu principal """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher le menu principal """
        self.grid_remove()
