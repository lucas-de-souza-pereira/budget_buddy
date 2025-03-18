

class User:
    def __init__(self):
        pass
    
        
        passw = pwinput.pwinput("mot de passe : ")
    def connect_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=passw,
            database="budget_buddy"
        )