import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("../.env")

class Connect_db:

    def connect_db(self):
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = os.getenv("DB_PASSWORD"),
            database = "xxxx"
            )
        self.cursor = self.mydb.cursor()

    def close_db (self):
        self.cursor.close()
        self.mydb.close()