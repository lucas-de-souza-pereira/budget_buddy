import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("config/.env")

class Connect_db():
    def __init__(self):
        self.user_id = ""


    def connect_db(self):

        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = os.getenv("DB_PASSWORD"),
            database = "budget_buddy"
            )
        self.cursor = self.mydb.cursor()

        if self.mydb.is_connected():
            db_info = self.mydb.get_server_info()
            print(db_info)

    def close_db (self):
        self.cursor.close()
        self.mydb.close()

    def set_user_id(self,user_id):
        """define user_id"""
        self.user_id = user_id
        print(f"🔍 [Connect_db] user_id saved : {self.user_id}")

    def get_user_id(self):
        """get user_id"""
        return self.user_id


test = Connect_db()
test.connect_db()