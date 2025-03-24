import customtkinter as ctk
import bcrypt
import tkinter as tk
from tkinter import messagebox
import re

class User(ctk.CTkFrame):
    def __init__(self, master, show_main_menu, show_admin_menu, conn):
        super().__init__(master)
        self.show_main_menu = show_main_menu  
        self.show_admin_menu = show_admin_menu

        self.current_mode = ctk.get_appearance_mode()
        self.conn = conn

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame for account creation
        self.create_account_frame = ctk.CTkFrame(self)
        self.create_account_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.create_tittle = ctk.CTkLabel(self.create_account_frame, text="Create an Account", font=("Arial", 18))
        self.create_tittle.pack(pady=30)

        # Account creation fields
        self.last_name_entry = ctk.CTkEntry(self.create_account_frame, placeholder_text="Last Name")
        self.last_name_entry.pack(pady=10)

        self.first_name_entry = ctk.CTkEntry(self.create_account_frame, placeholder_text="First Name")
        self.first_name_entry.pack(pady=10)

        self.email_entry_create = ctk.CTkEntry(self.create_account_frame, placeholder_text="Email")
        self.email_entry_create.pack(pady=10)

        self.password_entry_create = ctk.CTkEntry(self.create_account_frame, placeholder_text="Password", show="*")
        self.password_entry_create.pack(pady=10)

        # Checkbox to show/hide the password
        self.show_password_create = ctk.CTkCheckBox(self.create_account_frame, text="Show password", command=self.toggle_password_create)
        self.show_password_create.pack(pady=10)

        self.register_button = ctk.CTkButton(self.create_account_frame, text="Create My Account", command=self.create_user)
        self.register_button.pack(pady=10)

        # Frame for login
        self.account_connection_frame = ctk.CTkFrame(self)
        self.account_connection_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Fields to fill in for login
        self.connection_tittle = ctk.CTkLabel(self.account_connection_frame, text="Login", font=("Arial", 18))
        self.connection_tittle.pack(pady=30)

        self.email_entry_conn = ctk.CTkEntry(self.account_connection_frame, placeholder_text="Email")
        self.email_entry_conn.pack(pady=10)

        self.password_entry_conn = ctk.CTkEntry(self.account_connection_frame, placeholder_text="Password", show="*")  
        self.password_entry_conn.pack(pady=10)

        # Checkbox to show/hide the password
        self.show_password_conn = ctk.CTkCheckBox(self.account_connection_frame, text="Show password", command=self.toggle_password_conn)
        self.show_password_conn.pack(pady=10)

        self.login_button = ctk.CTkButton(self.account_connection_frame, text="Login", command=self.sign_in)
        self.login_button.pack(pady=10)

        self.theme_button = ctk.CTkButton(self, text="Change Theme", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, padx=10, pady=5, columnspan=3)

    def toggle_password_create(self):
        """ Show or hide the password during account creation """
        if self.show_password_create.get():
            self.password_entry_create.configure(show="")
        else:
            self.password_entry_create.configure(show="*")

    def toggle_password_conn(self):
        """ Show or hide the password during login """
        if self.show_password_conn.get():
            self.password_entry_conn.configure(show="")
        else:
            self.password_entry_conn.configure(show="*")

    def user_exists(self, email):
        self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = self.conn.cursor.fetchone()
        return user is not None 

    def create_user(self):
        self.conn.connect_db()

        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        email = self.email_entry_create.get()
        password = self.password_entry_create.get()

        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w])[A-Za-z\d\W]{10,}$"

        if not last_name or not first_name or not email or not password:
            messagebox.showinfo("Error", "All fields must be filled out.")
            return

        if self.user_exists(email):
            messagebox.showinfo("Error", "User already exists")
            return

        if not re.match(regex, password):
            error_message = "Invalid password! It must contain:\n"
            if not re.search(r"[a-z]", password):
                error_message += "- At least one lowercase letter\n"
            if not re.search(r"[A-Z]", password):
                error_message += "- At least one uppercase letter\n"
            if not re.search(r"\d", password):
                error_message += "- At least one digit\n"
            if not re.search(r"[^\w_]", password):
                error_message += "- At least one special character (!@#$%^&* etc.)\n"
            if len(password) < 10:
                error_message += "- Minimum 10 characters\n"

            messagebox.showinfo("Error", error_message)
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            query = "INSERT INTO users (last_name, first_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (last_name, first_name, email, hashed_password.decode('utf-8'))

            self.conn.cursor.execute(query, values)
            self.conn.mydb.commit()

            self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone()
            user_id = user[0]
            self.conn.set_user_id(user_id)

            messagebox.showinfo("Success", "Registration successful!")
            self.show_main_menu()

            self.last_name_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.email_entry_create.delete(0, tk.END)
            self.password_entry_create.delete(0, tk.END)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.conn.close_db()


    def check_connection(self, email, password):
        """ Check credentials and move to the menu if valid """
        try:
            self.conn.cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone() 
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')): 
                return True
        except Exception as e:
            print("Error", e)
        finally:
            self.conn.close_db()

        return False

    def toggle_theme(self):
        """ Toggle between light and dark theme """
        new_mode = "Dark" if self.current_mode == "Light" else "Light"
        self.current_mode = new_mode
        ctk.set_appearance_mode(new_mode)
        
    def sign_in(self):
        self.conn.connect_db()

        email = self.email_entry_conn.get()
        password = self.password_entry_conn.get()

        try: 
            self.conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = self.conn.cursor.fetchone()
            
            if not email or not password:
                messagebox.showinfo("Error", "All fields must be filled out.")
            
            elif self.check_connection(email, password):
                print("Login successful!")
                messagebox.showinfo("Success", "Login successful!")

                user_id = user[0]
                self.conn.set_user_id(user_id)

                print(f"🔍 [User] user_id passed to Connect_db: {user_id}")

                # Vérification email admin
                if email == "admin@mail.com":  
                    self.show_admin_menu(user_id)  # ✅ Passe l'ID utilisateur
                else:
                    self.show_main_menu(user_id)  # ✅ Passe l'ID utilisateur


                self.email_entry_conn.delete(0, tk.END)
                self.password_entry_conn.delete(0, tk.END)

            else:
                messagebox.showinfo("Error", "Incorrect email or password")
                print("Incorrect email or password")

        except Exception as e:
            print("Error during login:", e)
        finally:
            self.conn.close_db()



    def show(self):
        """ Show the login screen """
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """ Hide the login screen """
        self.grid_remove()
