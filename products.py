
import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def open_products(parent):
    window = tk.Toplevel(parent)
    window.title("Product Management")
    window.geometry("1050x650")
    window.configure(bg="#eef2f7")

    selected_id = None
    category_map = {}

    tk.Label(
        window, text="PRODUCT MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="#183153", fg="white", pady=15
    ).pack(fill="x")

    form = tk.Frame(window, bg="#eef2f7")
    form.pack(pady=15)

    fields = [
        "Product Name", "Description",
        "Selling Price", "Cost Price"
    ]

    entries = {}

    for i, field in enumerate(fields):
        tk.Label(form, text=field, bg="#eef2f7").grid(
            row=i // 2, column=(i % 2) * 2,
            padx=8, pady=8, sticky="w"
        )

        entry = tk.Entry(form, width=25)
        entry.grid(
            row=i // 2, column=(i % 2) * 2 + 1,
            padx=8, pady=8
        )
        entries[field] = entry

    tk.Label(form, text="Category", bg="#eef2f7").grid(
        row=2, column=0, padx=8, pady=8
    )

    category_box = ttk.Combobox(form, width=23, state="readonly")
    category_box.grid(row=2, column=1, padx=8, pady=8)

    def load_categories():
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        cursor.execute(
            "SELECT category_id, category_name FROM categories"
        )

        rows = cursor.fetchall()
        connection.close()

        category_map.clear()
        for category_id, name in rows:
            category_map[name] = category_id

        category_box["values"] = list(category_map.keys())

    columns = ("ID", "Name", "Category", "Selling Price",
               "Cost Price", "Available")

    table = ttk.Treeview(
        window, columns=columns, show="headings", height=12
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=145, anchor="center")

    table.pack(fill="both", expand=True, padx=15, pady=10)

    def load_products():
        for item in table.get_children():
            table.delete(item)

        connection = get_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT p.product_id, p.product_name, c.category_name,
                       p.selling_price, p.cost_price, p.is_available
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.is_available = 1
                ORDER BY p.product_id
            """)

            for row in cursor.fetchall():
                table.insert("", "end", values=row)

        except Exception as error:
            messagebox.showerror("Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def clear_fields():
        nonlocal selected_id
        selected_id = None

        for entry in entries.values():
            entry.delete(0, tk.END)

        category_box.set("")

    def select_product(event):
        nonlocal selected_id

        selected = table.focus()
        if not selected:
            return

        values = table.item(selected, "values")
        selected_id = int(values[0])

        entries["Product Name"].delete(0, tk.END)
        entries["Product Name"].insert(0, values[1])

        entries["Selling Price"].delete(0, tk.END)
        entries["Selling Price"].insert(0, values[3])

        entries["Cost Price"].delete(0, tk.END)
        entries["Cost Price"].insert(0, values[4])

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        cursor.execute(
            "SELECT description, category_id FROM products WHERE product_id=%s",
            (selected_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        entries["Description"].delete(0, tk.END)
        entries["Description"].insert(0, result[0] or "")

        for name, category_id in category_map.items():
            if category_id == result[1]:
                category_box.set(name)
                break

    def save_product():
        name = entries["Product Name"].get().strip()
        description = entries["Description"].get().strip()
        selling = entries["Selling Price"].get().strip()
        cost = entries["Cost Price"].get().strip()
        category = category_box.get()

        if not name or not selling or not cost or not category:
            messagebox.showwarning(
                "Missing Details", "Fill all required fields."
            )
            return

        try:
            selling = float(selling)
            cost = float(cost)

            if selling <= 0 or cost < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Price",
                "Selling price must be positive and cost price cannot be negative."
            )
            return

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        try:
            if selected_id is None:
                cursor.execute("""
                    INSERT INTO products
                    (category_id, product_name, description,
                     selling_price, cost_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    category_map[category], name, description,
                    selling, cost
                ))
            else:
                cursor.execute("""
                    UPDATE products
                    SET category_id=%s, product_name=%s,
                        description=%s, selling_price=%s,
                        cost_price=%s
                    WHERE product_id=%s
                """, (
                    category_map[category], name, description,
                    selling, cost, selected_id
                ))

            connection.commit()
            messagebox.showinfo("Success", "Product saved successfully.")
            clear_fields()
            load_products()

        except Exception as error:
            connection.rollback()
            messagebox.showerror("Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def deactivate_product():
        if selected_id is None:
            messagebox.showwarning(
                "Select Product", "Select a product first."
            )
            return

        if not messagebox.askyesno(
            "Confirm", "Deactivate this product?"
        ):
            return

        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                "UPDATE products SET is_available=0 WHERE product_id=%s",
                (selected_id,)
            )
            connection.commit()
            messagebox.showinfo("Success", "Product deactivated.")
            clear_fields()
            load_products()

        except Exception as error:
            connection.rollback()
            messagebox.showerror("Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def search_product():
        search_text = search_entry.get().strip()

        for item in table.get_children():
            table.delete(item)

        connection = get_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT p.product_id, p.product_name, c.category_name,
                       p.selling_price, p.cost_price, p.is_available
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.product_name LIKE %s
                  AND p.is_available = 1
                ORDER BY p.product_id
            """, ("%" + search_text + "%",))

            for row in cursor.fetchall():
                table.insert("", "end", values=row)

        except Exception as error:
            messagebox.showerror("Search Error", str(error))

        finally:
            cursor.close()
            connection.close()

    table.bind("<<TreeviewSelect>>", select_product)

    buttons = tk.Frame(window, bg="#eef2f7")
    buttons.pack(pady=10)

    tk.Button(
        buttons, text="SAVE / UPDATE",
        command=save_product, bg="#183153", fg="white",
        width=16
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons, text="DEACTIVATE",
        command=deactivate_product, bg="#c0392b", fg="white",
        width=16
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        buttons, text="CLEAR",
        command=clear_fields, width=12
    ).grid(row=0, column=2, padx=5)

    search_frame = tk.Frame(window, bg="#eef2f7")
    search_frame.pack(pady=10)

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)

    tk.Button(
        search_frame, text="SEARCH",
        command=search_product
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame, text="SHOW ALL",
        command=load_products
    ).pack(side="left", padx=5)

    load_categories()
    load_products()
