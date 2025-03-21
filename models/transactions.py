import customtkinter as ctk
from datetime import datetime


class TransactionManage(ctk.CTkFrame):
    def __init__(self, master, show_frame, conn):
        super().__init__(master)

        self.show_frame = show_frame  
        self.conn = conn

        self.credited_account = ctk.StringVar()
        self.montant_var = ctk.StringVar()
        self.description_var = ctk.StringVar()
        self.type_transaction_var = ctk.StringVar(value="deposit")
        self.variable = ctk.StringVar(value="")
        self.type_transaction_var.trace_add("write", self.update_transaction_type)


        self.grid_columnconfigure((0, 1), weight=1)  
        self.grid_rowconfigure(0, weight=4)  
        self.grid_rowconfigure(1, weight=1)  

        # 🏦 **Bloc 1 : account** (Colonne 0)
        self.frame_account = ctk.CTkFrame(self)
        self.frame_account.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_account.grid_rowconfigure(0, weight=2)

        ctk.CTkLabel(self.frame_account, text="Sélectionner le compte à débiter :").pack(pady=5, anchor="w")

        self.radiobuttons_accounts = []

        # 💳 **Bloc 2 : input transaction** (Colonne 1)
        self.frame_transaction = ctk.CTkFrame(self)
        self.frame_transaction.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.frame_transaction, text="Type de Transaction :").pack(pady=5, anchor="w")
        self.transaction_menu = ctk.CTkComboBox(
            self.frame_transaction, 
            values=["deposit", "withdrawall", "transfer"], 
            variable=self.type_transaction_var
        )
        self.transaction_menu.pack(pady=2, fill="x")


        self.label_montant = ctk.CTkLabel(self.frame_transaction, text="Montant :")
        self.entry_montant = ctk.CTkEntry(self.frame_transaction, textvariable=self.montant_var)

        self.label_description = ctk.CTkLabel(self.frame_transaction, text="Description :")
        self.entry_description = ctk.CTkEntry(self.frame_transaction, textvariable=self.description_var)


        self.label_compte = ctk.CTkLabel(self.frame_transaction, text="Compte à créditer :")
        self.entry_compte = ctk.CTkEntry(self.frame_transaction, textvariable=self.credited_account)


        # 📋 **Bloc 3 : action transaction** (Row 1, Colspan=2)
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, padx=20, pady=0, sticky="nsew")


        self.button_frame = ctk.CTkFrame(self.frame_bottom)
        self.button_frame.pack(pady=10, fill="x")

        self.submit_button = ctk.CTkButton(self.button_frame, text="Effectuer Transaction", command=self.effectuer_transaction)
        self.submit_button.pack(side="left", padx=5, expand=True)

        self.refresh_button = ctk.CTkButton(self.button_frame, text="Actualiser Transactions", command=self.afficher_transactions)
        self.refresh_button.pack(side="left", padx=5, expand=True)


        self.transaction_listbox = ctk.CTkTextbox(self.frame_bottom, height=100, width=500)
        self.transaction_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        self.update_transaction_type()


        self.get_selected_account()

    def update_transaction_type(self, *args):
        """ Met à jour l'affichage en fonction du type de transaction sélectionné """

        self.label_montant.pack_forget()
        self.entry_montant.pack_forget()
        self.label_description.pack_forget()
        self.entry_description.pack_forget()
        self.label_compte.pack_forget()
        self.entry_compte.pack_forget()

        # show montant and decription, reset data if change 
        self.label_montant.pack(pady=2, fill="x")
        self.entry_montant.pack(pady=2, fill="x")
        self.entry_montant.delete(0, "end") 

        self.label_description.pack(pady=2, fill="x")
        self.entry_description.pack(pady=2, fill="x")
        self.entry_description.delete(0, "end")  

        # show credited account , reset data if change 
        if self.type_transaction_var.get() == "transfer":
            self.label_compte.pack(pady=2, fill="x")
            self.entry_compte.pack(pady=2, fill="x")
            self.entry_compte.delete(0, "end") 


    def select_account(self):
        """ Select an account """
        self.conn.connect_db()
        user_id = self.conn.get_user_id()

        querry = "SELECT id, name, balance FROM accounts WHERE user_id = %s"
        self.conn.cursor.execute(querry, (user_id,))
        data_accounts = self.conn.cursor.fetchall()

        for radiobutton in self.radiobuttons_accounts[:]:  
            radiobutton.destroy()
        self.radiobuttons_accounts.clear()

        for i, account in enumerate(data_accounts):
            account_text = f"N° de compte : {account[0]} - {account[1]} - Solde : {account[2]}€"
            radiobutton = ctk.CTkRadioButton(
                self.frame_account, 
                text=account_text,
                variable=self.variable,
                value=account[0]
            )
            radiobutton.pack(pady=3, anchor="w")
            self.radiobuttons_accounts.append(radiobutton) 


        self.conn.close_db()


    def get_selected_account(self):
        """ Retourne l'ID du compte sélectionné """
        selected_account_id = self.variable.get()
        if selected_account_id:
            print(f"✅ Compte sélectionné : {selected_account_id}")
            return selected_account_id
        else:
            print("⚠️ Aucun compte sélectionné.")
            return None

    def effectuer_transaction(self):
        """ Enregistre une transaction dans la base de données """
        
        self.conn.connect_db()
        montant = self.montant_var.get()
        description = self.description_var.get()
        type_transaction = self.type_transaction_var.get()
        date_actuelle = datetime.now().strftime("%Y-%m-%d")

        if not montant:
            self.status_label.configure(text="Erreur : Montant requis", text_color="red")
            return

        try:
            montant = float(montant)
        except ValueError:
            self.status_label.configure(text="Erreur : Montant invalide", text_color="red")
            return
    
        user_id = self.get_selected_account()
        reference = f"TR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        sql = "INSERT INTO transactions (user_id, reference, description, montant, date, type) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (user_id, reference, description, montant, date_actuelle, type_transaction)

        self.conn.cursor.execute(sql, values)
        self.conn.mydb.commit()
        self.status_label.configure(text="Transaction enregistrée !", text_color="green")
        self.afficher_transactions()
        self.conn.close_db()

    def afficher_transactions(self):
        """ Affiche la liste des transactions """
        self.conn.connect_db()
        self.conn.cursor.execute("SELECT reference, description, montant, date, type FROM transactions ORDER BY date DESC")
        transactions = self.conn.cursor.fetchall()

        self.transaction_listbox.delete("all")
        for transaction in transactions:
            ref, desc, montant, date, t_type = transaction
            self.transaction_listbox.insert("end", f"{date} | {t_type.upper()} | {desc} : {montant}€\n")

        self.conn.close_db()

    def show(self):
        """ Afficher la fenêtre des transactions """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher la fenêtre des transactions """
        self.grid_remove()
