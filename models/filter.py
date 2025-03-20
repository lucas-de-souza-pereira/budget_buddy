import customtkinter as ctk
from models.connect_db import Connect_db

class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Elle C'est Elle")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.conn = Connect_db()
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
        self.date_start = ctk.CTkEntry(filter_frame, width=100)
        self.date_start.grid(row=3, column=1, padx=2, pady=2)
        self.date_start.bind("<KeyRelease>", lambda e: self.format_date_entry(e, self.date_start))


        ctk.CTkLabel(filter_frame, text="Date fin :").grid(row=4, column=0, sticky="w", padx=2, pady=2)
        self.date_end = ctk.CTkEntry(filter_frame, width=100)
        self.date_end.grid(row=4, column=1, padx=2, pady=2)
        self.date_end.bind("<KeyRelease>", lambda e: self.format_date_entry(e, self.date_end))

        ctk.CTkButton(filter_frame, text="Filtrer par Date", command=self.filter_by_date_range).grid(row=3, column=2, rowspan=2, padx=2, pady=2)

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
        self.fetch_transactions("SELECT * FROM transactions")

    def filter_by_type(self):
        transaction_type = self.type_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE type = %s", (transaction_type,))

    def filter_by_category(self):
        category = self.category_var.get()
        self.fetch_transactions("SELECT * FROM transactions WHERE category = %s", (category,))

    def filter_by_date_range(self):
        start_date = self.format_date_for_sql(self.date_start.get())
        end_date = self.format_date_for_sql(self.date_end.get())
        self.fetch_transactions("SELECT * FROM transactions WHERE date BETWEEN %s AND %s", (start_date, end_date))

    def sort_transactions(self, order):
        self.fetch_transactions(f"SELECT * FROM transactions ORDER BY montant {order}")

    def format_date_for_sql(self, date_str):
        """ Convertit YYYY/MM/DD en YYYY-MM-DD pour SQL """
        return date_str.replace("/", "-")

    def format_date_entry(self, event, entry: ctk.CTkEntry):
        """ Reformate la date en YYYY/MM/DD au fur et à mesure de la saisie """
        raw_date = entry.get().replace("/", "")

        if len(raw_date) > 8:
            raw_date = raw_date[:8]

        if raw_date.isdigit():
            formatted_date = raw_date
            if len(raw_date) > 4:
                formatted_date = raw_date[:4] + "/" + raw_date[4:]
            if len(raw_date) > 6:
                formatted_date = raw_date[:4] + "/" + raw_date[4:6] + "/" + raw_date[6:]

            entry.delete(0, "end")
            entry.insert(0, formatted_date)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = TransactionApp(root)
    root.mainloop()
