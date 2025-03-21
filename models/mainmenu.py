import customtkinter as ctk
from tkinter import messagebox


class Main_menu(ctk.CTkFrame):
    """ Dashboard for the user with multiple sections """
    def __init__(self, master, show_frame, conn):
        super().__init__(master)

        self.current_mode = ctk.get_appearance_mode()
        self.show_frame = show_frame  # Allows navigation between screens
        self.conn = conn

        # 📌 Grid configuration
        self.grid_columnconfigure(0, weight=1)  # Left column
        self.grid_columnconfigure(1, weight=1)  # Right column
        self.grid_rowconfigure(0, weight=1)  # Vertical spacing

        # 🏠 User Information Section (on the left)
        self.user_info_frame = ctk.CTkFrame(self)
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")  # Placement

        self.user_label = ctk.CTkLabel(self.user_info_frame, text="👤 User Information", font=("Arial", 16))
        self.user_label.pack(pady=10)

        self.user_name = ctk.CTkLabel(self.user_info_frame, text="Name : ")
        self.user_name.pack()

        self.user_email = ctk.CTkLabel(self.user_info_frame, text="Email : lucas@example.com")
        self.user_email.pack()

        self.create_account_button = ctk.CTkButton(self.user_info_frame, text="Create Account", command=self.open_create_account_window)
        self.create_account_button.pack(pady=50)


        # for radio buttons
        self.values = ["Account N° :"]
        self.radiobuttons_accounts = []
        self.variable = ctk.StringVar(value="")

        for i, value in enumerate(self.values):
            self.radiobutton = ctk.CTkRadioButton(self.user_info_frame, text=value)
            self.radiobutton.pack(pady=5)
            self.radiobuttons_accounts.append(self.radiobutton)


        # 💰 Bank Account Balance Section (on the right)
        self.account_balance_frame = ctk.CTkFrame(self)
        self.account_balance_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Placement

        self.balance_label = ctk.CTkLabel(self.account_balance_frame, text="💰 Account Balance", font=("Arial", 16))
        self.balance_label.pack(pady=10)

        self.balance_amount = ctk.CTkLabel(self.account_balance_frame, text="Balance : 1500€")
        self.balance_amount.pack()

        self.research_button = ctk.CTkButton(self.account_balance_frame, text="Search")
        self.research_button.pack()

        self.transaction_button = ctk.CTkButton(self.account_balance_frame, text="Transaction", command=self.master.show_transaction_page)
        self.transaction_button.pack(pady=10)

        # 🔄 Logout button at the bottom
        self.logout_button = ctk.CTkButton(self, text="Logout", command=lambda: self.show_frame(master.login_frame))
        self.logout_button.grid(row=1, column=0, columnspan=2, padx=20, sticky="e")

        self.theme_button = ctk.CTkButton(self, text="Change Theme", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, padx=20, pady=5, sticky="w" )

    def toggle_theme(self):
        """ Toggle between light and dark theme """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)

    def load_user_data(self):
        """ Load user information from DB """
        self.conn.connect_db()

        try: 
            user_id = self.conn.get_user_id() 
            print(f"🔍 [Main_menu] user_id retrieved: {user_id}")  # Debug

            query = """SELECT last_name, first_name, email
                       FROM users
                       WHERE id = %s
            """

            self.conn.cursor.execute(query, (user_id,))
            user_connected = self.conn.cursor.fetchone()

            self.user_name.configure(text=f"Name : {user_connected[0]} {user_connected[1]}")
            self.user_email.configure(text=f"Email : {user_connected[2]}")

        except Exception as e:
            print("Error while loading user info:", e)
        finally:
            self.conn.close_db()

    def open_create_account_window(self):
        """ Open a new window to add an account name """
        self.create_window = ctk.CTkToplevel(self)
        self.create_window.title("Create an Account")
        self.create_window.geometry("400x200")

        self.account_name_variable = ctk.StringVar(value="Current Account")

        ctk.CTkLabel(self.create_window, text="Account Name:").grid(row=2, column=0, padx=10, pady=5, sticky="n")
        self.account_name_combobox = ctk.CTkComboBox(self.create_window, values=["Current Account", "Livret A", "Savings Account"], variable=self.account_name_variable)
        self.account_name_combobox.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkButton(self.create_window, text="Create Account", command=self.create_account).grid(row=3, column=0, columnspan=2, pady=15)

    def account_exists(self, account_name, user_id):
        self.conn.cursor.execute("SELECT name FROM accounts WHERE name = %s AND user_id = %s", 
                                (account_name, user_id))
        account = self.conn.cursor.fetchone()
        return account is not None 

    def create_account(self):
        """ Create an account """
        
        self.conn.connect_db()
        user_id = self.conn.get_user_id()
        account_name = self.account_name_variable.get()

        print(f"[create_account] {account_name}")

        if self.account_exists(account_name, user_id):
            messagebox.showinfo("Error", "The bank account already exists")
            self.create_window.destroy()
            self.open_create_account_window()
            return

        try:
            query = """INSERT INTO accounts (name, balance, user_id)
                       VALUES (%s, %s, %s)
                    """
            values = (account_name, 0, user_id)

            self.conn.cursor.execute(query, values)
            self.conn.mydb.commit()

            messagebox.showinfo("Account Creation", "Account created successfully")
            self.select_account()
            self.create_window.destroy()            

        except Exception as e:
            print("Error during connection:", e)

        finally:
            self.conn.close_db()

    def select_account(self):
        """ Function to select account on dashboard """
        self.conn.connect_db()

        try: 
            user_id = self.conn.get_user_id() 
            print(f"🔍 [Main_menu][select_account] user_id retrieved: {user_id}")  

            query = """SELECT id, name, balance
                       FROM accounts
                       WHERE user_id = %s
            """

            self.conn.cursor.execute(query, (user_id,))
            data_accounts = self.conn.cursor.fetchall()

            for radiobutton in self.radiobuttons_accounts[:]:  
                radiobutton.destroy()

            self.radiobuttons_accounts.clear() 

            self.variable.set("") 

            for i, account in enumerate(data_accounts):
                account_text = f"Account N° : {account[0]} - Name : {account[1]} - Balance : {account[2]}€"
                radiobutton = ctk.CTkRadioButton(
                    self.user_info_frame, 
                    text=account_text,
                    variable=self.variable,
                    value=account[0])
                radiobutton.pack(pady=3, padx=50, anchor="w", fill="x")
                self.radiobuttons_accounts.append(radiobutton) 

        except Exception as e:
            print("Error while loading account data:", e)
        finally:
            self.conn.close_db()

    def get_selected_account(self):
        """ Get the selected account value """
        selected_account = self.variable.get()

        if selected_account:
            print(f"Selected account : {selected_account}")
            return selected_account

    def show(self):
        """ Print main menu """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Hide main menu """
        self.grid_remove()
