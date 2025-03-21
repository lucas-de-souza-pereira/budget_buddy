import customtkinter as ctk
from datetime import datetime


class TransactionManage(ctk.CTkFrame):
    def __init__(self,master,show_frame,conn):
        super().__init__(master)

        self.current_mode = ctk.get_appearance_mode()
        self.show_frame = show_frame  # Permet de naviguer entre les écrans
        self.conn = conn

        # self.root.title("Elle C'est Elle")
        # self.root.geometry("600x500")

        self.montant_var = ctk.StringVar()
        self.description_var = ctk.StringVar()
        self.type_transaction_var = ctk.StringVar(value="deposit")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frame_transaction = ctk.CTkFrame(self)
        self.frame_transaction.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.frame_transaction, text="Montant :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.frame_transaction, textvariable=self.montant_var).grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.frame_transaction, text="Description :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.frame_transaction, textvariable=self.description_var).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.frame_transaction, text="Type de Transaction :").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        transaction_menu = ctk.CTkComboBox(self.frame_transaction, values=["deposit", "withdrawall", "transfer"], variable=self.type_transaction_var)
        transaction_menu.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkButton(self.frame_transaction, text="Effectuer Transaction", command=self.effectuer_transaction).grid(row=3, column=0, columnspan=2, pady=15)
        
        self.status_label = ctk.CTkLabel(self.frame_transaction, text="", text_color="white")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.transaction_listbox = ctk.CTkTextbox(self.frame_transaction, height=150, width=500)
        self.transaction_listbox.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        ctk.CTkButton(self.frame_transaction, text="Actualiser Transactions", command=self.afficher_transactions).grid(pady=5)

        self.theme_button = ctk.CTkButton(self, text="Changer de thème", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=0, pady=20, sticky="ne")
    
    def toggle_theme(self):
        """ Basculer entre le thème clair et sombre """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)
        
    def effectuer_transaction(self):
        print("effect")
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
        
        
        print("effect3")
        
        self.conn.cursor.execute(sql, values)
        print("effect4")
        self.conn.mydb.commit()
        print("effect5")
        self.status_label.configure(text="Transaction enregistrée !", text_color="green")
        print("effect6")
        self.afficher_transactions()
        self.conn.close_db()
    
    def afficher_transactions(self):
        print("affich")

        self.conn.cursor.execute("SELECT reference, description, montant, date, type FROM transactions ORDER BY date DESC")
        transactions = self.cursor.fetchall()
        
        self.transaction_listbox.delete("all")
        for transaction in transactions:
            ref, desc, montant, date, t_type = transaction
            self.transaction_listbox.insert("end", f"{date} | {t_type.upper()} | {desc} : {montant}€\n")
    
    def close_db (self):
        self.cursor.close()
        self.mydb.close()



    def show(self):
        """ Afficher la fenêtre des transactions """
        self.grid(row=0, column=0, sticky="nsew")  

    def hide(self):
        """ Cacher la fenêtre des transactions """
        self.grid_remove()  

