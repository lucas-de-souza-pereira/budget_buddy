import customtkinter as ctk
from datetime import datetime
from connect_db import Connect_db

class TransactionManage:
    def __init__(self, root):
        self.conn = Connect_db()
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        print("setup")
        self.root.title("Elle C'est Elle")
        self.root.geometry("600x500")

        self.montant_var = ctk.StringVar()
        self.description_var = ctk.StringVar()
        self.type_transaction_var = ctk.StringVar(value="deposit")

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Montant :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(frame, textvariable=self.montant_var).grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame, text="Description :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(frame, textvariable=self.description_var).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame, text="Type de Transaction :").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        transaction_menu = ctk.CTkComboBox(frame, values=["deposit", "withdrawall", "transfer"], variable=self.type_transaction_var)
        transaction_menu.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkButton(frame, text="Effectuer Transaction", command=self.effectuer_transaction).grid(row=3, column=0, columnspan=2, pady=15)
        
        self.status_label = ctk.CTkLabel(frame, text="", text_color="white")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.transaction_listbox = ctk.CTkTextbox(self.root, height=150, width=500)
        self.transaction_listbox.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkButton(self.root, text="Actualiser Transactions", command=self.afficher_transactions).pack(pady=5)
    
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

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    
    app = ctk.CTk()
    TransactionManage(app)
    app.mainloop()
