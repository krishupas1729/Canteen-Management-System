import tkinter as tk
from tkinter import messagebox
from db import get_connection
def login_user():
    username = username_entry.get().strip()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Input Error", "Enter username and password.")
        return
    connection = get_connection()
    if connection is None:
        messagebox.showerror("Database Error", "Could not connect to database.")
        return
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_id, full_name, username, password_hash, role
            FROM users
            WHERE username = %s AND is_active = 1
        """
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user and user["password_hash"] == password:
            if user["role"].lower() != "admin":
                messagebox.showerror("Access Denied", "Only administrators can log in.")
            else:
                messagebox.showinfo("Login Successful", f"Welcome, {user['full_name']}!")
                root.destroy()
                import dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except Exception as error:
        messagebox.showerror("Error", str(error))
    finally:
        cursor.close()
        connection.close()
root = tk.Tk()
root.title("Canteen Management System - Admin Login")
root.geometry("450x350")
root.resizable(False, False)
root.configure(bg="#eef2f7")
title = tk.Label(
    root,
    text="CANTEEN MANAGEMENT SYSTEM",
    font=("Arial", 16, "bold"),
    bg="#eef2f7",
    fg="#183153"
)
title.pack(pady=(35, 10))

subtitle = tk.Label(
    root,
    text="Administrator Login",
    font=("Arial", 12),
    bg="#eef2f7"
)
subtitle.pack(pady=5)
tk.Label(root, text="Username", bg="#eef2f7", font=("Arial", 11)).pack(pady=(20, 5))
username_entry = tk.Entry(root, font=("Arial", 12), width=28)
username_entry.pack()
tk.Label(root, text="Password", bg="#eef2f7", font=("Arial", 11)).pack(pady=(15, 5))
password_entry = tk.Entry(root, font=("Arial", 12), width=28, show="*")
password_entry.pack()
login_button = tk.Button(
    root,
    text="LOGIN",
    font=("Arial", 11, "bold"),
    bg="#183153",
    fg="white",
    width=20,
    command=login_user
)
login_button.pack(pady=25)

root.mainloop()
