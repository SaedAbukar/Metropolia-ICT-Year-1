import os
import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='footy',
            user='root',
            password='12345678',
            autocommit=True
        )

    def get_conn(self):
        return self.conn
