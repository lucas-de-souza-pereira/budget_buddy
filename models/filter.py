import customtkinter as ctk
from database import connect_db
from tkcalendar import DateEntry

class TransactionApp:
    def __init__(self, root, account_id):
        self.root = root
        self.account_id = account_id
        self.root.title("Elle C'est Elle")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Filtres
        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        ctk.CTkLabel(filter_frame, text="Filtres").grid(row=0, columnspan=2, pady=10)

        # Type
        ctk.CTkLabel(filter_frame, text="Type :").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.type_var = ctk.StringVar(value="deposit")
        self.type_box = ctk.CTkComboBox(filter_frame, values=["deposit", "withdrawal", "transfer"], variable=self.type_var)
        self.type_box.grid(row=1, column=1, padx=2, pady=2)
        ctk.CTkButton(filter_frame, text="Filtrer", command=self.filter_by_type).grid(row=1, column=2, padx=2, pady=2)

        # Catégorie
        ctk.CTkLabel(filter_frame, text="Catégorie :").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.category_var = ctk.StringVar(value="loisir")
        self.category_entry = ctk.CTkEntry(filter_frame, textvariable=self.category_var, width=120)
        self.category_entry.grid(row=2, column=1, padx=2, pady=2)
        ctk.CTkButton(filter_frame, text="Filtrer", command=self.filter_by_category).grid(row=2, column=2, padx=2, pady=2)

        # Dates
        ctk.CTkLabel(filter_frame, text="Date début :").grid(row=3, column=0, sticky="w", padx=2, pady=2)
        self.date_start = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_start.grid(row=3, column=1, padx=2, pady=2)

        ctk.CTkLabel(filter_frame, text="Date fin :").grid(row=4, column=0, sticky="w", padx=2, pady=2)
        self.date_end = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_end.grid(row=4, column=1, padx=2, pady=2)

        ctk.CTkButton(filter_frame, text="Filtrer par Date", command=self.filter_by_date_range).grid(row=3, column=2, rowspan=2, padx=2, pady=2)

        # Montant
        sort_frame = ctk.CTkFrame(self.root)
        sort_frame.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        ctk.CTkLabel(sort_frame, text="Trier par Montant :").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ctk.CTkButton(sort_frame, text="↑", width=30, command=lambda: self.sort_transactions("ASC")).grid(row=0, column=1, padx=2, pady=2)
        ctk.CTkButton(sort_frame, text="↓", width=30, command=lambda: self.sort_transactions("DESC")).grid(row=0, column=2, padx=2, pady=2)

        display_frame = ctk.CTkFrame(self.root)
        display_frame.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        self.result_box = ctk.CTkTextbox(display_frame, height=150, width=450, wrap="none")
        self.result_box.pack(padx=2, pady=2)

        ctk.CTkButton(display_frame, text="Afficher toutes les transactions", command=self.show_all_transactions).pack(padx=2, pady=2)

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
        else:
            self.result_box.insert("end", "Aucune transaction trouvée.\n")

    def show_all_transactions(self):
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s", (self.account_id,))

    def filter_by_type(self):
        transaction_type = self.type_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND type = %s", (self.account_id, transaction_type))

    def filter_by_category(self):
        category = self.category_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND category = %s", (self.account_id, category))

    def filter_by_date_range(self):
        start_date = self.date_start.get_date()
        end_date = self.date_end.get_date()
        self.fetch_transactions("SELECT * FROM transactions WHERE account_id = %s AND date BETWEEN %s AND %s", (self.account_id, start_date, end_date))

    def sort_transactions(self, order):
        self.fetch_transactions(f"SELECT * FROM transactions WHERE account_id = %s ORDER BY montant {order}", (self.account_id,))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    
    account_id = 1
    app = TransactionApp(root, account_id)
    
    root.mainloop()
