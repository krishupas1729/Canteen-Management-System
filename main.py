from db import get_connection

connection = get_connection()

if connection and connection.is_connected():
    print("SUCCESS: Database connected!")
    print("Database: canteen_db")

    connection.close()
else:
    print("Database connection failed!")
