import customtkinter as ctk
from tkinter import messagebox

from models.connect_db import Connect_db


class Main_menu(ctk.CTkFrame):
    """ Dashboard pour l'utilisateur avec plusieurs blocs """
    def __init__(self, master, show_frame,conn):
        super().__init__(master)

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


        # for checkbox
        self.values = ["Account N° :"]
        self.checkboxes = []

        for i, value in enumerate(self.values):
            self.checkbox = ctk.CTkCheckBox(self.user_info_frame, text=value)
            self.checkbox.pack(pady=5)
            self.checkboxes.append(self.checkbox)


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

    def select_account(self):

        self.conn.connect_db()

        try : 

            user_id = self.conn.get_user_id() 
            print(f"🔍 [Main_menu][select_account] user_id récupéré : {user_id}")  

            querry = """SELECT id,balance
                        FROM accounts
                        WHERE user_id = %s
            """

            self.conn.cursor.execute(querry,(user_id,))
            data_accounts = self.conn.cursor.fetchall()
            print(f"data account {data_accounts}")

            for checkbox in self.checkboxes:
                checkbox.destroy()
                self.checkboxes.clear()

            for i, account in enumerate(data_accounts):
                account_text = f"Account N° : {account[0]} - Solde : {account[1]}€"
                checkbox = ctk.CTkCheckBox(self.user_info_frame, text=account_text)
                checkbox.pack(pady=5)
                self.checkboxes.append(checkbox) 

        except Exception as e:
            print("Erreur lors du chargement des infos utilisateur :", e)
        finally :
            self.conn.close_db()



    def get(self):
        """get information to checkbox (example : click on 1, click on 2....)"""
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


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
