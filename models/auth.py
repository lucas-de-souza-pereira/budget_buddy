import customtkinter as ctk
import bcrypt
from connect_db import Connect_db

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def utilisateur_existe(email):
    conn = Connect_db()
    conn.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = conn.cursor.fetchone()
    conn.close_db()
    return user is not None 

def inscrire_utilisateur():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    email = entry_email.get()
    mot_de_passe = entry_password.get()

    if utilisateur_existe(email):
        print("Cet utilisateur existe déjà !")
        return
    
    hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (last_name, first_name, email, password) VALUES (%s, %s, %s, %s)",
            (nom, prenom, email, hashed_password.decode('utf-8'))
        )
        conn.commit()
        print("Inscription réussie !")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        cursor.close()
        conn.close()

def verifier_connexion(email, mot_de_passe):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone() 
        
        cursor.fetchall()
        
        if user and bcrypt.checkpw(mot_de_passe.encode('utf-8'), user[0].encode('utf-8')):
            return True
    except Exception as e:
        print("Erreur", e)
    finally:
        cursor.close()
        conn.close()

    return False

def connexion():
    email = entry_email.get()
    password = entry_password.get()

    if verifier_connexion(email, password):
        print("Connexion réussie !")
    else:
        print("Email ou mot de passe incorrect")

app = ctk.CTk()
app.geometry("400x500")
app.title("Authentification")

label_title = ctk.CTkLabel(app, text="Bienvenue", font=("Arial", 20))
label_title.pack(pady=20)

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label_nom = ctk.CTkLabel(frame, text="Nom:")
label_nom.pack(pady=5)
entry_nom = ctk.CTkEntry(frame)
entry_nom.pack(pady=5)

label_prenom = ctk.CTkLabel(frame, text="Prénom:")
label_prenom.pack(pady=5)
entry_prenom = ctk.CTkEntry(frame)
entry_prenom.pack(pady=5)

label_email = ctk.CTkLabel(frame, text="Email:")
label_email.pack(pady=5)
entry_email = ctk.CTkEntry(frame)
entry_email.pack(pady=5)

label_password = ctk.CTkLabel(frame, text="Mot de passe:")
label_password.pack(pady=5)
entry_password = ctk.CTkEntry(frame, show="*")
entry_password.pack(pady=5)

button_register = ctk.CTkButton(frame, text="S'inscrire", command=inscrire_utilisateur)
button_register.pack(pady=10)

button_login = ctk.CTkButton(frame, text="Se connecter", command=connexion)
button_login.pack(pady=10)

label_message = ctk.CTkLabel(frame, text="")
label_message.pack(pady=10)

app.mainloop()
