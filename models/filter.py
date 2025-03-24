import customtkinter as ctk
from datetime import datetime

class TransactionApp(ctk.CTkFrame):
    def __init__(self, master, conn, show_frame):
        super().__init__(master)

        self.current_mode = ctk.get_appearance_mode()
        self.show_frame = show_frame  # Pour naviguer entre les écrans
        self.conn = conn

        # Variables liées aux widgets
        self.type_var = ctk.StringVar(value="deposit")
        self.category_var = ctk.StringVar(value="loisir")
        self.date_start = ctk.StringVar()
        self.date_end = ctk.StringVar()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Cadre principal
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Filtres de type de transaction
        ctk.CTkLabel(self.filter_frame, text="Type :").grid(row=0, column=0, sticky="w")
        self.type_box = ctk.CTkComboBox(self.filter_frame, values=["deposit", "withdrawal", "transfer"], variable=self.type_var)
        self.type_box.grid(row=0, column=1, padx=10, pady=5)
        
        # Catégorie de transaction
        ctk.CTkLabel(self.filter_frame, text="Catégorie :").grid(row=1, column=0, sticky="w")
        self.category_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.category_var)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        # Date de début et fin
        ctk.CTkLabel(self.filter_frame, text="Date début :").grid(row=2, column=0, sticky="w")
        self.date_start_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.date_start)
        self.date_start_entry.grid(row=2, column=1, padx=10, pady=5)
        self.date_start.bind("<KeyRelease>", lambda e: self.format_date_entry(e, self.date_start))

        ctk.CTkLabel(self.filter_frame, text="Date fin :").grid(row=3, column=0, sticky="w")
        self.date_end_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.date_end)
        self.date_end_entry.grid(row=3, column=1, padx=10, pady=5)
        self.date_end.bind("<KeyRelease>", lambda e: self.format_date_entry(e, self.date_end))

        # Bouton pour appliquer le filtre
        ctk.CTkButton(self.filter_frame, text="Filtrer", command=self.filter_transactions).grid(row=4, column=0, columnspan=2, pady=10)

        # Affichage des résultats
        self.result_box = ctk.CTkTextbox(self.filter_frame, height=150, width=450)
        self.result_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Bouton pour rafraîchir les transactions
        ctk.CTkButton(self.filter_frame, text="Afficher toutes les transactions", command=self.show_all_transactions).grid(row=6, column=0, columnspan=2, pady=10)

        # Bouton pour changer de thème
        self.theme_button = ctk.CTkButton(self, text="Changer le thème", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=10, pady=20, sticky="ne")

    def toggle_theme(self):
        """ Basculer entre le mode clair et foncé """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)

    def filter_transactions(self):
        """ Appliquer les filtres et afficher les résultats """
        type_ = self.type_var.get()
        category = self.category_var.get()
        start_date = self.date_start.get()
        end_date = self.date_end.get()

        query = "SELECT * FROM transactions WHERE type = %s AND category = %s"
        params = (type_, category)

        if start_date and end_date:
            start_date = self.format_date_for_sql(start_date)
            end_date = self.format_date_for_sql(end_date)
            query += " AND date BETWEEN %s AND %s"
            params += (start_date, end_date)

        self.fetch_transactions(query, params)

    def fetch_transactions(self, query, params=()):
        """ Exécuter la requête et afficher les résultats """
        self.conn.cursor.execute(query, params)
        transactions = self.conn.cursor.fetchall()

        self.result_box.delete("0.0", "end")
        if transactions:
            for transaction in transactions:
                self.result_box.insert("end", f"{transaction}\n")
        else:
            self.result_box.insert("end", "Aucune transaction trouvée.\n")

    def show_all_transactions(self):
        """ Afficher toutes les transactions """
        query = "SELECT * FROM transactions"
        self.fetch_transactions(query)

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

    def show(self):
        """ Afficher l'écran """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Masquer l'écran """
        self.grid_remove()
