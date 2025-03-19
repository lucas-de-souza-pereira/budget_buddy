import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("config/.env")

class Connect_db():

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


test = Connect_db()
test.connect_db()