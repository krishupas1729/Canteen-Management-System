import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="canteen_db",
            port=3306
        )

        return connection

    except Error as error:
        print("Database connection error:", error)
        return None