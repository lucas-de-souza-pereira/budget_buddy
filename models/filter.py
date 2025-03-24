import customtkinter as ctk
from tkcalendar import DateEntry

class TransactionApp(ctk.CTkFrame):
    def __init__(self, master, show_frame, conn):
        super().__init__(master)

        self.show_frame = show_frame  
        self.conn = conn
        self.current_mode = ctk.get_appearance_mode()
        
        # Variable pour stocker l'ID du compte sélectionné
        self.account_id = None
        self.radiobuttons_accounts = []
        self.variable = ctk.IntVar()

        # Grid configuration for layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)  # Compte
        self.grid_rowconfigure(1, weight=1)   # Filtres
        self.grid_rowconfigure(2, weight=1)   # Tri
        self.grid_rowconfigure(3, weight=4)   # Résultats

        # Frame pour la sélection du compte
        self.account_frame = ctk.CTkFrame(self)
        self.account_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        
        ctk.CTkLabel(self.account_frame, text="Select Account:").pack(pady=5)
        
        # Bouton pour rafraîchir la liste des comptes
        ctk.CTkButton(self.account_frame, text="Refresh Accounts", command=self.select_account).pack(pady=5)
        
        # Frame pour afficher les radios boutons des comptes
        self.frame_account = ctk.CTkScrollableFrame(self.account_frame, height=100)
        self.frame_account.pack(pady=5, fill="both", expand=True)
        
        # Bouton pour valider la sélection du compte
        ctk.CTkButton(self.account_frame, text="Show Transactions", command=self.show_selected_account_transactions).pack(pady=5)

        # Frame for filters
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        ctk.CTkLabel(self.filter_frame, text="Filters").grid(row=0, column=0, columnspan=3, pady=10)

        # Type filter
        ctk.CTkLabel(self.filter_frame, text="Type:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.type_var = ctk.StringVar(value="deposit")
        self.type_box = ctk.CTkComboBox(self.filter_frame, values=["deposit", "withdrawal", "transfer"], variable=self.type_var)
        self.type_box.grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(self.filter_frame, text="Filter", command=self.filter_by_type).grid(row=1, column=2, padx=10, pady=5)

        # Category filter
        ctk.CTkLabel(self.filter_frame, text="Category:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.category_var = ctk.StringVar(value="leisure")
        self.category_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.category_var, width=120)
        self.category_entry.grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkButton(self.filter_frame, text="Filter", command=self.filter_by_category).grid(row=2, column=2, padx=10, pady=5)

        # Start date filter
        ctk.CTkLabel(self.filter_frame, text="Start Date:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.date_start = DateEntry(self.filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_start.grid(row=3, column=1, padx=10, pady=5)

        # End date filter
        ctk.CTkLabel(self.filter_frame, text="End Date:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.date_end = DateEntry(self.filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_end.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkButton(self.filter_frame, text="Filter by Date", command=self.filter_by_date_range).grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        # Frame for sorting options
        self.sort_frame = ctk.CTkFrame(self)
        self.sort_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        ctk.CTkLabel(self.sort_frame, text="Sort by Amount:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkButton(self.sort_frame, text="↑", width=30, command=lambda: self.sort_transactions("ASC")).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(self.sort_frame, text="↓", width=30, command=lambda: self.sort_transactions("DESC")).grid(row=0, column=2, padx=10, pady=10)

        # Frame for displaying results
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        self.result_box = ctk.CTkTextbox(self.display_frame, height=150, width=450, wrap="none")
        self.result_box.pack(padx=10, pady=2, fill="both", expand=True)

        # Navigation buttons
        self.back_button = ctk.CTkButton(self, text="← Back to Menu", command=self.master.show_main_menu)
        self.back_button.grid(row=0, column=1, padx=20, pady=5, sticky="ne")

        self.theme_button = ctk.CTkButton(self, text="Change Theme", command=self.toggle_theme)
        self.theme_button.grid(row=3, column=1, padx=20, pady=5, sticky="se")

        # Charger les comptes au démarrage
        self.select_account()

    def toggle_theme(self):
        """ Toggle between light and dark theme """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)

    def select_account(self):
        """ Select an account """
        self.conn.connect_db()
        user_id = self.conn.get_user_id()

        query = "SELECT id, name, balance FROM accounts WHERE user_id = %s"
        self.conn.cursor.execute(query, (user_id,))
        self.data_accounts = self.conn.cursor.fetchall()

        # Clear existing radiobuttons
        for widget in self.frame_account.winfo_children():
            widget.destroy()

        # Create new radiobuttons for each account
        for account in self.data_accounts:
            account_text = f"Account N°{account[0]} - {account[1]} - Balance: {account[2]}€"
            radiobutton = ctk.CTkRadioButton(
                self.frame_account, 
                text=account_text,
                variable=self.variable,
                value=account[0]
            )
            radiobutton.pack(pady=3, anchor="w")

        self.conn.close_db()

    def show_selected_account_transactions(self):
        """Show transactions for the selected account"""
        self.account_id = self.variable.get()
        if self.account_id:
            self.show_all_transactions()
        else:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("end", "Please select an account first.\n")

    def fetch_transactions(self, query, params=()):
        """ Execute a query and display results in the textbox """
        if not self.account_id:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("end", "Please select an account first.\n")
            return

        self.conn.connect_db()

        # Ajouter l'account_id aux paramètres si nécessaire
        if "account_id" not in query.lower():
            query += " WHERE account_id = %s"
            params = (self.account_id,) + params

        self.conn.cursor.execute(query, params)
        transactions = self.conn.cursor.fetchall()

        self.conn.close_db()

        self.result_box.delete("0.0", "end")
        if transactions:
            for transaction in transactions:
                formatted_transaction = f"""
                Amount: {transaction[4]} €
                Description: {transaction[3]}
                Type: {transaction[6]}
                Date: {transaction[5]}
                Category: {transaction[7]}
                
                -------------------------------------------------------
                """
                self.result_box.insert("end", formatted_transaction)
        else:
            self.result_box.insert("end", "No transactions found.\n")

    def show_all_transactions(self):
        """ Fetch and display all transactions for the account """
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s", (self.account_id,))

    def filter_by_type(self):
        """ Filter transactions by type (deposit, withdrawal, or transfer) """
        transaction_type = self.type_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE type = %s", (transaction_type,))

    def filter_by_category(self):
        """ Filter transactions by category """
        category = self.category_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE category = %s", (category,))

    def filter_by_date_range(self):
        """ Filter transactions by date range """
        start_date = self.date_start.get_date()
        end_date = self.date_end.get_date()
        self.fetch_transactions("SELECT * FROM transactions WHERE date BETWEEN %s AND %s", (start_date, end_date))

    def sort_transactions(self, order):
        """ Sort transactions by amount in ascending or descending order """
        self.fetch_transactions(f"SELECT * FROM transactions ORDER BY montant {order}")

    def show(self):
        """ Display the search window """
        self.grid(row=0, column=0, sticky="nsew")
        # Rafraîchir la liste des comptes à chaque affichage
        self.select_account()

    def hide(self):
        """ Hide the search window """
        self.grid_remove()