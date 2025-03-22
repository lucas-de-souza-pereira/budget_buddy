import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox


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



        self.back_button = ctk.CTkButton(self.frame_bottom, text="← Retour au menu", command=self.master.show_main_menu)
        self.back_button.pack(pady=5)

        self.update_transaction_type()


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
        self.data_accounts = self.conn.cursor.fetchall()

        for radiobutton in self.radiobuttons_accounts[:]:  
            radiobutton.destroy()
        self.radiobuttons_accounts.clear()

        for i, account in enumerate(self.data_accounts):
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
        amount = self.montant_var.get()
        description = self.description_var.get()
        transaction_type = self.type_transaction_var.get()
        current_date = datetime.now().strftime("%Y-%m-%d")
        cretited_account = self.entry_compte.get()

        if not amount:
            self.status_label.configure(text="Error: Amount required", text_color="red")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.status_label.configure(text="Error: Invalid amount", text_color="red")
            return
    
        account_id = self.get_selected_account()
        user_id = self.conn.get_user_id()
        reference = f"TR-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        if self.type_transaction_var.get() == "deposit":

            self.querry_depot_it(account_id, reference, description, amount, current_date, transaction_type)
            
        if self.type_transaction_var.get() == "withdrawall":

            self.querry_withdrawall(account_id, reference, description, amount, current_date, transaction_type)

        if self.type_transaction_var.get() == "transfer":

            self.querry_transfer(account_id, reference, description, amount, current_date, transaction_type,cretited_account)


        self.select_account()
        self.afficher_transactions()



        # self.status_label.configure(text="Transaction enregistrée !", text_color="green")
        

    def querry_depot_it(self,account_id, reference, description, amount, current_date, transaction_type):
        try : 
            sql = """INSERT INTO transactions (account_id, reference, description, montant, date, type) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (account_id, reference, description, amount, current_date, transaction_type)

            self.conn.cursor.execute(sql, values)
            self.conn.mydb.commit()
            self.depot_it(amount)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.conn.close_db()


    def depot_it(self,amount):

        for account in self.data_accounts:
            if account[0]== int(self.get_selected_account()):
                balance = float(account[2])
                break

        new_balance = balance + amount

        querry = ("""UPDATE accounts SET balance = %s
                    WHERE id = %s""")

        values = (new_balance,int(self.get_selected_account()))

        self.conn.cursor.execute(querry, values)
        self.conn.mydb.commit()
        


    def querry_withdrawall(self,account_id, reference, description, amount, current_date, transaction_type):
        try : 
            sql = """INSERT INTO transactions (account_id, reference, description, montant, date, type) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (account_id, reference, description, amount, current_date, transaction_type)

            self.conn.cursor.execute(sql, values)
            self.conn.mydb.commit()
            self.withdrawall(amount)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.conn.close_db()

    def withdrawall(self,amount):

        for account in self.data_accounts:
            if account[0]== int(self.get_selected_account()):
                balance = float(account[2])
                break

        new_balance = balance - amount

        querry = ("""UPDATE accounts SET balance = %s
                    WHERE id = %s""")

        values = (new_balance,int(self.get_selected_account()))

        self.conn.cursor.execute(querry, values)
        self.conn.mydb.commit()

    def credited_account_dont_exists(self, credited_account):
        self.conn.cursor.execute("SELECT id FROM accounts WHERE id = %s", (credited_account,))
        id_credited_account = self.conn.cursor.fetchone()
        return id_credited_account is None 


    def querry_transfer(self,account_id, reference, description, amount, current_date, transaction_type,credited_account):
        
        print(f"credited : {credited_account} tr : {transaction_type}")

        if self.credited_account_dont_exists(credited_account):
            messagebox.showinfo("Error", "Credited account dont' exist")
            return

        try : 
            sql = """INSERT INTO transactions (account_id, reference, description, montant, date, type,credited_account_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (account_id, reference, description, amount, current_date, transaction_type,credited_account)

            self.conn.cursor.execute(sql, values)
            self.conn.mydb.commit()
            self.transfer(amount,credited_account)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.conn.close_db()


    def transfer(self,amount,credited_account):

        for account in self.data_accounts:
            if account[0]== int(self.get_selected_account()):
                balance = float(account[2])
                break

        new_balance = balance - amount

        querry = ("""UPDATE accounts SET balance = %s
                    WHERE id = %s""")

        values = (new_balance,int(self.get_selected_account()))

        self.conn.cursor.execute(querry, values)
        self.conn.mydb.commit()


        querry = "SELECT balance FROM accounts WHERE id = %s"
        self.conn.cursor.execute(querry, (credited_account,))
        balance_credited_account = self.conn.cursor.fetchone()

        new_balance = float(balance_credited_account[0]) + amount

        querry = ("""UPDATE accounts SET balance = %s
                    WHERE id = %s""")

        values = (new_balance,credited_account)

        self.conn.cursor.execute(querry, values)
        self.conn.mydb.commit()


    def afficher_transactions(self):
        """ Affiche la liste des transactions """
        self.conn.connect_db()

        querry = """SELECT reference, description, montant, date, type, account_id 
                                FROM transactions 
                                WHERE account_id IN (%s, %s, %s)
                                ORDER BY date DESC"""
        
        account_id_list = []
        for account_id in self.data_accounts:
            account_id_list.append(account_id[0])

        print(f"account_id_list = {account_id_list}")

        self.conn.cursor.execute(querry,(account_id_list))
        transactions = self.conn.cursor.fetchall()

        # self.transaction_listbox.delete("all")
        for transaction in transactions:
            # ref, desc, montant, date, t_type = transaction
            reference = transaction[0]
            desc = transaction[1]
            amount = float(transaction[2])
            date = transaction[3]
            t_type = transaction[4]
            account_id = transaction[5]
            self.transaction_listbox.insert("end", f"Account : {account_id} | {reference} | {date} | {t_type} | {desc} : {amount}€\n")

        self.conn.close_db()

    def show(self):
        """ Afficher la fenêtre des transactions """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Cacher la fenêtre des transactions """
        self.grid_remove()
