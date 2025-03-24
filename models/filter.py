
import customtkinter as ctk
from tkcalendar import DateEntry

class TransactionApp(ctk.CTkFrame):
    def __init__(self, master, show_frame, conn):
        super().__init__(master)

        self.show_frame = show_frame  
        self.conn = conn

        self.current_mode = ctk.get_appearance_mode()

        # self.grid_columnconfigure((0, 1), weight=1)
        # self.grid_rowconfigure(0, weight=4)
        # self.grid_rowconfigure(1, weight=1)

        # Block 1: Filters
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        ctk.CTkLabel(self.filter_frame, text="Filtres").grid(row=0, column=0, columnspan=2, pady=10)

        # Type
        ctk.CTkLabel(self.filter_frame, text="Type :").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.type_var = ctk.StringVar(value="deposit")
        self.type_box = ctk.CTkComboBox(self.filter_frame, values=["deposit", "withdrawal", "transfer"], variable=self.type_var)
        self.type_box.grid(row=1, column=1, padx=2, pady=2)
        ctk.CTkButton(self.filter_frame, text="Filtrer", command=self.filter_by_type).grid(row=1, column=2, padx=2, pady=2)

        # Category
        ctk.CTkLabel(self.filter_frame, text="Catégorie :").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.category_var = ctk.StringVar(value="loisir")
        self.category_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.category_var, width=120)
        self.category_entry.grid(row=2, column=1, padx=2, pady=2)
        ctk.CTkButton(self.filter_frame, text="Filtrer", command=self.filter_by_category).grid(row=2, column=2, padx=2, pady=2)

        # Dates
        ctk.CTkLabel(self.filter_frame, text="Date début :").grid(row=3, column=0, sticky="w", padx=2, pady=2)
        self.date_start = DateEntry(self.filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_start.grid(row=3, column=1, padx=2, pady=2)

        ctk.CTkLabel(self.filter_frame, text="Date fin :").grid(row=4, column=0, sticky="w", padx=2, pady=2)
        self.date_end = DateEntry(self.filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_end.grid(row=4, column=1, padx=2, pady=2)

        ctk.CTkButton(self.filter_frame, text="Filtrer par Date", command=self.filter_by_date_range).grid(row=5, column=0, columnspan=3, padx=2, pady=2)

        # Block 2: Sort by Amount
        self.sort_frame = ctk.CTkFrame(self)
        self.sort_frame.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        ctk.CTkLabel(self.sort_frame, text="Trier par Montant :").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ctk.CTkButton(self.sort_frame, text="↑", width=30, command=lambda: self.sort_transactions("ASC")).grid(row=0, column=1, padx=2, pady=2)
        ctk.CTkButton(self.sort_frame, text="↓", width=30, command=lambda: self.sort_transactions("DESC")).grid(row=0, column=2, padx=2, pady=2)

        # Block 3: Display Results
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        self.result_box = ctk.CTkTextbox(self.display_frame, height=150, width=450, wrap="none")
        self.result_box.pack(padx=2, pady=2)

        # Block 4: Action Buttons (Optional)
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self.frame_bottom)
        self.button_frame.pack(pady=10, fill="x")




        self.transaction_listbox = ctk.CTkTextbox(self.frame_bottom, height=100, width=500)
        self.transaction_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        self.back_button = ctk.CTkButton(self.frame_bottom, text="← Back to Menu", command=self.master.show_main_menu)
        self.back_button.pack(pady=5)    

    def fetch_transactions(self, query, params=()):
        """ Exécute une requête et affiche les résultats """
        self.cursor.execute(query, params)
        transactions = self.cursor.fetchall()

        self.result_box.delete("0.0", "end")
        if transactions:
            for transaction in transactions:
                formatted_transaction = f"""
                Montant : {transaction[4]} €
                Description : {transaction[3]}
                Type : {transaction[6]}
                Date : {transaction[5]}
                Categorie : {transaction[7]}
                
                -------------------------------------------------------
                """
                self.result_box.insert("end", formatted_transaction)
                formatted_transaction = f"""
                Montant : {transaction[4]} €
                Description : {transaction[3]}
                Type : {transaction[6]}
                Date : {transaction[5]}
                Categorie : {transaction[7]}
                
                -------------------------------------------------------
                """
                self.result_box.insert("end", formatted_transaction)
        else:
            self.result_box.insert("end", "Aucune transaction trouvée.\n")

    def show_all_transactions(self):
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s", (self.account_id,))
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s", (self.account_id,))

    def filter_by_type(self):
        transaction_type = self.type_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND type = %s", (self.account_id, transaction_type))
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND type = %s", (self.account_id, transaction_type))

    def filter_by_category(self):
        category = self.category_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND category = %s", (self.account_id, category))
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND category = %s", (self.account_id, category))

    def filter_by_date_range(self):
        start_date = self.date_start.get_date()
        end_date = self.date_end.get_date()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND date BETWEEN %s AND %s", (self.account_id, start_date, end_date))
        start_date = self.date_start.get_date()
        end_date = self.date_end.get_date()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND date BETWEEN %s AND %s", (self.account_id, start_date, end_date))

    def sort_transactions(self, order):
        self.fetch_transactions(f"SELECT * FROM transactions WHERE account_id = %s ORDER BY montant {order}", (self.account_id,))
    
    def show(self):
        """ Afficher la fenêtre des recherches """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher la fenêtre des recherches """
        self.grid_remove()