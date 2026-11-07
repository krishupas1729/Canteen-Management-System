
import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def open_categories(parent):
    window = tk.Toplevel(parent)
    window.title("Category Management")
    window.geometry("750x500")
    window.configure(bg="#eef2f7")

    tk.Label(
        window,
        text="CATEGORY MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="#eef2f7",
        fg="#183153"
    ).pack(pady=15)

    form = tk.Frame(window, bg="#eef2f7")
    form.pack(pady=10)

    tk.Label(form, text="Category Name:", bg="#eef2f7").grid(row=0, column=0, padx=10, pady=8)
    name_entry = tk.Entry(form, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=8)

    tk.Label(form, text="Description:", bg="#eef2f7").grid(row=1, column=0, padx=10, pady=8)
    description_entry = tk.Entry(form, width=30)
    description_entry.grid(row=1, column=1, padx=10, pady=8)

    columns = ("ID", "Category Name", "Description")
    table = ttk.Treeview(window, columns=columns, show="headings", height=12)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=200)

    table.pack(fill="both", expand=True, padx=20, pady=10)

    def load_categories():
        for item in table.get_children():
            table.delete(item)

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT category_id, category_name, description
                FROM categories
                ORDER BY category_id
            """)

            for row in cursor.fetchall():
                table.insert("", "end", values=row)

        except Exception as error:
            messagebox.showerror("Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def clear_fields():
        name_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)

    def select_category(event):
        selected = table.selection()
        if selected:
            values = table.item(selected[0], "values")
            clear_fields()
            name_entry.insert(0, values[1])
            description_entry.insert(0, values[2] or "")

    def save_category():
        name = name_entry.get().strip()
        description = description_entry.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Enter category name.")
            return

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO categories (category_name, description)
                VALUES (%s, %s)
            """, (name, description))

            connection.commit()
            messagebox.showinfo("Success", "Category added successfully!")
            clear_fields()
            load_categories()

        except Exception as error:
            messagebox.showerror("Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def update_category():
        selected = table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a category first.")
            return

        category_id = table.item(selected[0], "values")[0]
        name = name_entry.get().strip()
        description = description_entry.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Enter category name.")
            return

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE categories
                SET category_name=%s, description=%s
                WHERE category_id=%s
            """, (name, description, category_id))

            connection.commit()
            messagebox.showinfo("Success", "Category updated!")
            clear_fields()
            load_categories()

        except Exception as error:
            messagebox.showerror("Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def delete_category():
        selected = table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a category first.")
            return

        category_id = table.item(selected[0], "values")[0]

        if not messagebox.askyesno("Confirm", "Delete this category?"):
            return

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM categories WHERE category_id=%s",
                (category_id,)
            )
            connection.commit()
            messagebox.showinfo("Success", "Category deleted!")
            clear_fields()
            load_categories()

        except Exception:
            connection.rollback()
            messagebox.showerror(
                "Cannot Delete",
                "This category may be linked to existing products."
            )

        finally:
            cursor.close()
            connection.close()

    table.bind("<<TreeviewSelect>>", select_category)

    buttons = tk.Frame(window, bg="#eef2f7")
    buttons.pack(pady=10)

    tk.Button(buttons, text="ADD", width=12, command=save_category).grid(row=0, column=0, padx=5)
    tk.Button(buttons, text="UPDATE", width=12, command=update_category).grid(row=0, column=1, padx=5)
    tk.Button(buttons, text="DELETE", width=12, command=delete_category).grid(row=0, column=2, padx=5)
    tk.Button(buttons, text="CLEAR", width=12, command=clear_fields).grid(row=0, column=3, padx=5)

    load_categories()
