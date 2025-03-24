import customtkinter as ctk
from tkinter import messagebox


class Admin_menu(ctk.CTkFrame):
    """Dashboard for the user with multiple sections"""
    def __init__(self, master, show_frame, conn):
        super().__init__(master)

        self.current_mode = ctk.get_appearance_mode()  # Current appearance mode (Light/Dark)
        self.show_frame = show_frame  # Allows navigation between screens
        self.conn = conn  # Database connection

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

        # For radio buttons displaying account numbers
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

        # 🛠️ Edit & Delete Buttons for User and Account
        self.edit_user_button = ctk.CTkButton(self.user_info_frame, text="Edit User", command=self.edit_user)
        self.edit_user_button.pack(pady=10)

        self.delete_user_button = ctk.CTkButton(self.user_info_frame, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=10)

        self.edit_account_button = ctk.CTkButton(self.account_balance_frame, text="Edit Account", command=self.edit_account_balance)
        self.edit_account_button.pack(pady=10)

        self.delete_account_button = ctk.CTkButton(self.account_balance_frame, text="Delete Account", command=self.delete_account)
        self.delete_account_button.pack(pady=10)

        # 🔄 Logout button at the bottom
        self.logout_button = ctk.CTkButton(self, text="Logout", command=lambda: self.show_frame(master.login_frame))
        self.logout_button.grid(row=1, column=0, columnspan=2, padx=20, sticky="e")

        self.theme_button = ctk.CTkButton(self, text="Change Theme", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)

    def load_user_data(self):
        """Load user information from the database"""
        self.conn.connect_db()

        try: 
            user_id = self.conn.get_user_id()
            print(f"🔍 [admin_menu] user_id retrieved: {user_id}")  # Debugging statement

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
        """Open a new window to add an account name"""
        self.create_window = ctk.CTkToplevel(self)
        self.create_window.title("Create an Account")
        self.create_window.geometry("400x200")

        self.account_name_variable = ctk.StringVar(value="Current Account")

        ctk.CTkLabel(self.create_window, text="Account Name:").grid(row=2, column=0, padx=10, pady=5, sticky="n")
        self.account_name_combobox = ctk.CTkComboBox(self.create_window, values=["Current Account", "Livret A", "Savings Account"], variable=self.account_name_variable)
        self.account_name_combobox.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(self.create_window, text="Create Account", command=self.create_account).grid(row=3, column=0, columnspan=2, pady=15)

    def account_exists(self, account_name, user_id):
        """Check if the account already exists"""
        self.conn.cursor.execute("SELECT name FROM accounts WHERE name = %s AND user_id = %s", 
                                (account_name, user_id))
        account = self.conn.cursor.fetchone()
        return account is not None 

    def create_account(self):
        """Create a new account in the database"""
        
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
        """Select an account to display on the dashboard"""
        self.conn.connect_db()

        try: 
            user_id = self.conn.get_user_id()
            print(f"🔍 [admin_menu][select_account] user_id retrieved: {user_id}")  

            query = """SELECT id, name, balance
                       FROM accounts
                       WHERE user_id = %s
            """

            self.conn.cursor.execute(query, (user_id,))
            data_accounts = self.conn.cursor.fetchall()

            for radiobutton in self.radiobuttons_accounts[:]:  # Clear previous radio buttons
                radiobutton.destroy()

            self.radiobuttons_accounts.clear()  # Clear list

            self.variable.set("")  # Reset selected value

            # Create new radio buttons for each account
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
        """Get the selected account value"""
        selected_account = self.variable.get()

        if selected_account:
            print(f"Selected account : {selected_account}")
            return selected_account

    def show(self):
        """Display the admin menu"""
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """Hide the admin menu"""
        self.grid_remove()

    def edit_user(self):
        """Edit user information (name, email, etc.)"""
        user_id = self.conn.get_user_id()  # Get user ID
        self.edit_user_window = ctk.CTkToplevel(self)
        self.edit_user_window.title("Edit User")
        self.edit_user_window.geometry("400x250")

        self.conn.connect_db()
        try:
            query = "SELECT last_name, first_name, email FROM users WHERE id = %s"
            self.conn.cursor.execute(query, (user_id,))
            user_data = self.conn.cursor.fetchone()

            self.last_name_entry = ctk.CTkEntry(self.edit_user_window, placeholder_text="Last Name", textvariable=ctk.StringVar(value=user_data[0]))
            self.last_name_entry.grid(row=0, column=1, padx=10, pady=10)

            self.first_name_entry = ctk.CTkEntry(self.edit_user_window, placeholder_text="First Name", textvariable=ctk.StringVar(value=user_data[1]))
            self.first_name_entry.grid(row=1, column=1, padx=10, pady=10)

            self.email_entry = ctk.CTkEntry(self.edit_user_window, placeholder_text="Email", textvariable=ctk.StringVar(value=user_data[2]))
            self.email_entry.grid(row=2, column=1, padx=10, pady=10)

            # Save button to save changes
            self.save_button = ctk.CTkButton(self.edit_user_window, text="Save Changes", command=self.save_user_changes)
            self.save_button.grid(row=3, column=0, columnspan=2, pady=15)

        except Exception as e:
            print(f"Error retrieving user data: {e}")
        finally:
            self.conn.close_db()

    def save_user_changes(self):
        """Save changes made to the user information"""
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        email = self.email_entry.get()

        try:
            query = """UPDATE users SET last_name = %s, first_name = %s, email = %s WHERE id = %s"""
            self.conn.connect_db()
            self.conn.cursor.execute(query, (last_name, first_name, email, self.conn.get_user_id()))
            self.conn.mydb.commit()

            messagebox.showinfo("User Updated", "User details updated successfully.")
            self.edit_user_window.destroy()

        except Exception as e:
            print(f"Error saving user data: {e}")
            messagebox.showerror("Error", "Error while saving changes.")
        finally:
            self.conn.close_db()

    def delete_user(self):
        """Delete the user from the database"""
        user_id = self.conn.get_user_id()  # Get user ID
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if confirmation:
            try:
                query = "DELETE FROM users WHERE id = %s"
                self.conn.connect_db()
                self.conn.cursor.execute(query, (user_id,))
                self.conn.mydb.commit()

                messagebox.showinfo("User Deleted", "User has been deleted successfully.")
            except Exception as e:
                print(f"Error deleting user: {e}")
                messagebox.showerror("Error", "Error while deleting user.")
            finally:
                self.conn.close_db()

    def delete_account(self):
        """Delete a selected account"""
        selected_account = self.get_selected_account()
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this account?")
        if confirmation:
            try:
                query = "DELETE FROM accounts WHERE id = %s"
                self.conn.connect_db()
                self.conn.cursor.execute(query, (selected_account,))
                self.conn.mydb.commit()

                messagebox.showinfo("Account Deleted", "Account has been deleted successfully.")
            except Exception as e:
                print(f"Error deleting account: {e}")
                messagebox.showerror("Error", "Error while deleting account.")
            finally:
                self.conn.close_db()


    def edit_account_balance(self, account_id):
        """Edit the balance of a selected account"""
        self.edit_account_window = ctk.CTkToplevel(self)
        self.edit_account_window.title("Edit Account Balance")
        self.edit_account_window.geometry("400x200")