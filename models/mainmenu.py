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

        self.create_account_button = ctk.CTkButton(self.user_info_frame,text= "Créer un compte",command=self.open_create_account_window)
        self.create_account_button.pack(pady=50)


        # for radiobutton
        self.values = ["Account N° :"]
        self.radiobuttons_accounts = []
        self.variable = ctk.StringVar(value="")

        for i, value in enumerate(self.values):
            self.radiobutton = ctk.CTkRadioButton(self.user_info_frame, text=value)
            self.radiobutton.pack(pady=5)
            self.radiobuttons_accounts.append(self.radiobutton)


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

            self.user_name.configure(text= f"Name : {user_conneted[0]} {user_conneted[1]}")
            self.user_email.configure(text= f"Email : {user_conneted[2]}")

        except Exception as e:
            print("Erreur lors du chargement des infos utilisateur :", e)
        finally :
            self.conn.close_db()


    def open_create_account_window(self):
        """open new window to add name account"""
        self.create_window = ctk.CTkToplevel(self)
        self.create_window.title("Create an account")
        self.create_window.geometry("400x200")

        self.account_name_variable = ctk.StringVar(value="Compte courant")

        ctk.CTkLabel(self.create_window, text="Nom du compte :").grid(row=2, column=0, padx=10, pady=5, sticky="n")
        self.account_name_combobox = ctk.CTkComboBox(self.create_window, values=["Compte courant","Livret A", "Livret Epargne"], variable=self.account_name_variable)
        self.account_name_combobox.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkButton(self.create_window, text="Créer le compte", command=self.create_account).grid(row=3, column=0, columnspan=2, pady=15)


    def account_exists(self,account_name,user_id):

        self.conn.cursor.execute("SELECT name FROM accounts WHERE name = %s AND user_id = %s" , 
                                (account_name,user_id))
        account = self.conn.cursor.fetchone()

        return account is not None 
    

    def create_account(self):
        """create an account"""
        
        self.conn.connect_db()
        user_id = self.conn.get_user_id()
        account_name = self.account_name_variable.get()

        print(f"[creat_account] {account_name}")

        if self.account_exists(account_name,user_id):
            messagebox.showinfo("Erreur", "Le compte banquaire existe déjà")
            self.create_window.destroy()
            self.open_create_account_window()
            return
        try:
                        
            querry = """INSERT INTO accounts (name,balance,user_id)
                        VALUES (%s,%s,%s)
                    """
            values = (account_name,0,user_id)

            self.conn.cursor.execute(querry,values)
            self.conn.mydb.commit()

            messagebox.showinfo("Création de compte", "Création de compte effectué")
            self.select_account()
            self.create_window.destroy()            

        except Exception as e:
            print("Erreur lors de la connexion :", e)

        finally:
            self.conn.close_db()



    def select_account(self):
        """Fonction to select account on dashboard"""
        self.conn.connect_db()

        try : 

            user_id = self.conn.get_user_id() 
            print(f"🔍 [Main_menu][select_account] user_id récupéré : {user_id}")  

            querry = """SELECT id,name,balance
                        FROM accounts
                        WHERE user_id = %s
            """

            self.conn.cursor.execute(querry,(user_id,))
            data_accounts = self.conn.cursor.fetchall()


            for radiobutton in self.radiobuttons_accounts[:]:  
                radiobutton.destroy()

            self.radiobuttons_accounts.clear() 


            self.variable.set("") 

            for i, account in enumerate(data_accounts):
                account_text = f"Account N° : {account[0]} - Name : {account[1]} - Solde : {account[2]}€"
                radiobutton = ctk.CTkRadioButton(
                    self.user_info_frame, 
                    text=account_text,
                    variable=self.variable,
                    value=account[0])
                radiobutton.pack(pady=3, padx=50,anchor="w", fill="x")
                self.radiobuttons_accounts.append(radiobutton) 

        except Exception as e:
            print("Erreur lors du chargement des infos utilisateur :", e)
        finally :
            self.conn.close_db()

    def get_select_account(self):
        """get value selected account"""
        select_account = self.variable.get()

        if select_account:
            print(f"selected account : {select_account}")
            return select_account




    def show(self):
        """ Print main menu"""
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Hide main menu """
        self.grid_remove()
