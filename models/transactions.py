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
        
        self.grid_columnconfigure((0, 1), weight=1)  
        self.grid_rowconfigure(0, weight=4)  
        self.grid_rowconfigure(1, weight=1)  

        # 🏦 **Bloc 1 : account** (Colonne 0)
        self.frame_account = ctk.CTkFrame(self)
        self.frame_account.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_account.grid_rowconfigure(0, weight=2)

        ctk.CTkLabel(self.frame_account, text="Sélectionner le compte à débiter :").pack(pady=5, anchor="w")

        self.radiobuttons_accounts = []

        # 💳 **Bloc 2 : input transaction* (Colonne 1)
        self.frame_transaction = ctk.CTkFrame(self)
        self.frame_transaction.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame_transaction.grid_rowconfigure(0, weight=2)

        ctk.CTkLabel(self.frame_transaction, text="Type de Transaction :").pack(pady=5, anchor="w")
        self.transaction_menu = ctk.CTkComboBox(self.frame_transaction, 
                                                values=["deposit", "withdrawall", "transfer"],
                                                variable=self.type_transaction_var,
                                                command=self.update_transaction_type)
        self.transaction_menu.pack(pady=2, fill="x")

        ctk.CTkLabel(self.frame_transaction, text="Montant :").pack(pady=5, anchor="w")
        self.amount_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.montant_var)
        self.amount_entry.pack(pady=2, fill="x")

        ctk.CTkLabel(self.frame_transaction, text="Description :").pack(pady=5, anchor="w")
        self.description_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.description_var)
        self.description_entry.pack(pady=2, fill="x")



        # 📋 **Bloc 3 : action transaction** (Row 1, Colspan=2)
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, padx=20, pady=0, sticky="nsew")

        # Boutons
        self.button_frame = ctk.CTkFrame(self.frame_bottom)
        self.button_frame.pack(pady=10, fill="x")

        self.submit_button = ctk.CTkButton(self.button_frame, text="Effectuer Transaction", command=self.effectuer_transaction)
        self.submit_button.pack(side="left", padx=5, expand=True)

        self.refresh_button = ctk.CTkButton(self.button_frame, text="Actualiser Transactions", command=self.afficher_transactions)
        self.refresh_button.pack(side="left", padx=5, expand=True)

        # Zone d'affichage des transactions
        self.transaction_listbox = ctk.CTkTextbox(self.frame_bottom, height=100, width=500)
        self.transaction_listbox.pack(pady=10, padx=10, fill="both", expand=True)

    def update_transaction_type(self, event=None):
        """ Met à jour l'affichage en fonction du type de transaction sélectionné """
        

        for widget in self.frame_transaction.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.frame_transaction, text="Type de Transaction :").pack(pady=5, anchor="w")
        self.transaction_menu = ctk.CTkComboBox(
            self.frame_transaction, 
            values=["deposit", "withdrawall", "transfer"], 
            variable=self.type_transaction_var, 
            command=self.update_transaction_type 
        )
        self.transaction_menu.pack(pady=2, fill="x")

        if self.type_transaction_var.get() == "deposit":
            self.show_depot_it()
        elif self.type_transaction_var.get() == "withdrawall":
            self.show_withdrawall()
        elif self.type_transaction_var.get() == "transfer":
            self.show_transfer()

    
    def show_depot_it(self):

        ctk.CTkLabel(self.frame_transaction, text="Montant :").pack(pady=5, anchor="w")
        self.amount_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.montant_var)
        self.amount_entry.pack(pady=2, fill="x")

        ctk.CTkLabel(self.frame_transaction, text="Description :").pack(pady=5, anchor="w")
        self.description_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.description_var)
        self.description_entry.pack(pady=2, fill="x")

    def show_withdrawall(self):

        ctk.CTkLabel(self.frame_transaction, text="Montant :").pack(pady=5, anchor="w")
        self.amount_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.montant_var)
        self.amount_entry.pack(pady=2, fill="x")

        ctk.CTkLabel(self.frame_transaction, text="Description :").pack(pady=5, anchor="w")
        self.description_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.description_var)
        self.description_entry.pack(pady=2, fill="x")

    def show_transfer(self):

        ctk.CTkLabel(self.frame_transaction,text="Compte à créditer").pack(pady=5, anchor="w")
        self.credited_account_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.credited_account)
        self.credited_account_entry.pack(pady=2, fill="x")

        ctk.CTkLabel(self.frame_transaction, text="Montant :").pack(pady=5, anchor="w")
        self.amount_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.montant_var)
        self.amount_entry.pack(pady=2, fill="x")

        ctk.CTkLabel(self.frame_transaction, text="Description :").pack(pady=5, anchor="w")
        self.description_entry = ctk.CTkEntry(self.frame_transaction, textvariable=self.description_var)
        self.description_entry.pack(pady=2, fill="x")





    def select_account(self):
        """ Met à jour la liste des comptes disponibles """
        self.conn.connect_db()
        user_id = self.conn.get_user_id()

        querry = "SELECT id, name, balance FROM accounts WHERE user_id = %s"
        self.conn.cursor.execute(querry, (user_id,))
        data_accounts = self.conn.cursor.fetchall()

        # 🔄 Supprime les anciens boutons radio
        for radiobutton in self.radiobuttons_accounts[:]:  
            radiobutton.destroy()
        self.radiobuttons_accounts.clear()

        # ✅ Ajoute les nouveaux boutons radio
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
    
        user_id = 1
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
