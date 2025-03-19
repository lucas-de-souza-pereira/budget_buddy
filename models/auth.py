import customtkinter as ctk
import bcrypt
from connect_db import Connect_db
from tkinter import PhotoImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

current_language = "fr" 

def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    new_mode = "Dark" if current_mode == "Light" else "Light" 
    window.after(50, lambda: ctk.set_appearance_mode(new_mode))

def toggle_language():
    global current_language
    
    current_language = "fr" if current_language == "en" else "en"
    
    update_texts()
    
    if current_language == "fr":
        flag_image = PhotoImage(file="Assets/flag_france.png")
        button_language.configure(image=flag_image)
        button_language.image = flag_image
    else:
        flag_image = PhotoImage(file="Assets/uk_flag.png")
        button_language.configure(image=flag_image)
        button_language.image = flag_image

def update_texts():
    label_title.configure(text=texts[current_language]["label_title"])
    label_nom.configure(text=texts[current_language]["label_nom"])
    label_prenom.configure(text=texts[current_language]["label_prenom"])
    label_email.configure(text=texts[current_language]["label_email"])
    label_password.configure(text=texts[current_language]["label_mot_de_passe"])
    button_register.configure(text=texts[current_language]["button_inscrire"])
    button_login.configure(text=texts[current_language]["button_connecter"])
    button_theme.configure(text=texts[current_language]["button_theme"])
    button_language.configure(text=texts[current_language]["button_language"])
    check_button.configure(text=texts[current_language]["check_button"])

texts = {
    "fr": {
        "label_title": "Bienvenue sur Budget Buddy",
        "label_nom": "Nom:",
        "label_prenom": "Prénom:",
        "label_email": "Email:",
        "label_mot_de_passe": "Mot de passe:",
        "button_inscrire": "S'inscrire",
        "button_connecter": "Se connecter",
        "button_theme": "Changer de Thème",
        "button_language": "Passer en Anglais",
        "check_button" : "Se souvenir de moi"
    },
    "en": {
        "label_title": "Welcome to Budget Buddy",
        "label_nom": "Last Name:",
        "label_prenom": "First Name:",
        "label_email": "Email:",
        "label_mot_de_passe": "Password:",
        "button_inscrire": "Register",
        "button_connecter": "Login",
        "button_theme": "Change Theme",
        "button_language": " Switch to French",
        "check_button": "Remember me"
    }
}

def utilisateur_existe(email):
    conn = Connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None 

def inscrire_utilisateur():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    email = entry_email.get()
    mot_de_passe = entry_password.get()

    if utilisateur_existe(email):
        print("L'utilisateur existe déjà")
        return
    
    hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())

    conn = Connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (last_name, first_name, email, password) VALUES (%s, %s, %s, %s)",
            (nom, prenom, email, hashed_password.decode('utf-8'))
        )
        conn.commit()
        print("Utilisateur inscrit avec succès.")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        cursor.close()
        conn.close()

def verifier_connexion(email, mot_de_passe):
    conn = Connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone() 
        
        if user and bcrypt.checkpw(mot_de_passe.encode('utf-8'), user[0].encode('utf-8')):
            return True
    except Exception as e:
        print("Erreur lors de la vérification de la connexion:", e)
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

window = ctk.CTk()
window.geometry("1080x720")
window.title("Authentification")

flag_image_fr = PhotoImage(file="Assets/flag_france.png")
flag_image_en = PhotoImage(file="Assets/uk_flag.png")
button_language = ctk.CTkButton(window, image=flag_image_fr, text=texts[current_language]["button_language"], command=toggle_language, corner_radius=10)
button_language.pack(side="left", anchor="n", padx=10, pady=40)

button_theme = ctk.CTkButton(window, text=texts[current_language]["button_theme"], command=toggle_theme, corner_radius=10)
button_theme.pack(side="right", anchor="n", padx=10, pady=40)

label_title = ctk.CTkLabel(window, text=texts[current_language]["label_title"], font=("Arial", 20))
label_title.pack(pady=10)

frame = ctk.CTkFrame(window)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label_nom = ctk.CTkLabel(frame, text=texts[current_language]["label_nom"])
label_nom.pack(pady=5)
entry_nom = ctk.CTkEntry(frame, width=250)
entry_nom.pack(pady=5)

label_prenom = ctk.CTkLabel(frame, text=texts[current_language]["label_prenom"])
label_prenom.pack(pady=5)
entry_prenom = ctk.CTkEntry(frame, width=250)
entry_prenom.pack(pady=5)

label_email = ctk.CTkLabel(frame, text=texts[current_language]["label_email"]) 
label_email.pack(pady=5)
entry_email = ctk.CTkEntry(frame, width=250)
entry_email.pack(pady=5)

label_password = ctk.CTkLabel(frame, text=texts[current_language]["label_mot_de_passe"])
label_password.pack(pady=5)
entry_password = ctk.CTkEntry(frame, show="*", width=250)
entry_password.pack(pady=5)

check_button = ctk.CTkCheckBox(frame, text=texts[current_language]["check_button"])
check_button.pack(pady=5)

button_register = ctk.CTkButton(frame, text=texts[current_language]["button_inscrire"], command=inscrire_utilisateur)
button_register.pack(pady=20)

button_login = ctk.CTkButton(frame, text=texts[current_language]["button_connecter"], command=connexion)
button_login.pack(pady=20)

window.mainloop()