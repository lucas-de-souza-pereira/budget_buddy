import customtkinter as ctk

from models.connect_db import Connect_db


class Main_menu(ctk.CTkFrame):
    """ Dashboard pour l'utilisateur avec plusieurs blocs """
    def __init__(self, master, show_frame):
        super().__init__(master)

        self.show_frame = show_frame  # Permet de naviguer entre les écrans
        self.conn = Connect_db()


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

        # 💰 Bloc Solde du compte bancaire (à droite)
        self.account_balance_frame = ctk.CTkFrame(self)
        self.account_balance_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Placement

        self.balance_label = ctk.CTkLabel(self.account_balance_frame, text="💰 Solde du Compte", font=("Arial", 16))
        self.balance_label.pack(pady=10)

        self.balance_amount = ctk.CTkLabel(self.account_balance_frame, text="Solde : 1500€")
        self.balance_amount.pack()

        # 🔄 Bouton de Déconnexion en bas
        self.logout_button = ctk.CTkButton(self, text="Déconnexion", command=lambda: self.show_frame(master.login_frame))
        self.logout_button.grid(row=1, column=0, columnspan=2, pady=20, sticky="s")

    def load_user_data(self, user_id):
        """load information for user connected from DB"""
        self.conn.connect_db()

        try : 
            querry = """SELECT last_name,first_name,email
                        FROM users
                        WHERE id = %s
            """
            value = user_id

            self.conn.cursor.execute(querry,(value,))
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

    def show(self):
        """ Afficher le menu principal """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher le menu principal """
        self.grid_remove()
