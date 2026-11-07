
import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def create_window(parent, title, columns, fields):
    window = tk.Toplevel(parent)
    window.title(title)
    window.geometry("900x600")
    window.configure(bg="#eef2f7")

    tk.Label(
        window, text=title.upper(),
        font=("Arial", 20, "bold"),
        bg="#eef2f7", fg="#183153"
    ).pack(pady=15)

    form = tk.Frame(window, bg="#eef2f7")
    form.pack(pady=10)

    entries = {}

    for i, field in enumerate(fields):
        tk.Label(form, text=field + ":", bg="#eef2f7").grid(
            row=i, column=0, padx=10, pady=5, sticky="e"
        )
        entry = tk.Entry(form, width=35)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry

    table = ttk.Treeview(window, columns=columns, show="headings", height=12)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=150)

    table.pack(fill="both", expand=True, padx=20, pady=10)

    def clear():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def selected_id():
        selected = table.selection()
        if not selected:
            return None
        return table.item(selected[0], "values")[0]

    def fill_fields(event):
        selected = table.selection()
        if selected:
            values = table.item(selected[0], "values")
            clear()
            for i, field in enumerate(fields):
                entries[field].insert(0, values[i + 1] or "")

    table.bind("<<TreeviewSelect>>", fill_fields)

    return window, entries, table, clear, selected_id


# ---------------- CUSTOMERS ----------------

def open_customers(parent):
    window, entries, table, clear, selected_id = create_window(
        parent, "Customer Management",
        ("ID", "Name", "Phone", "Type"),
        ("Customer Name", "Phone", "Customer Type")
    )

    def load():
        table.delete(*table.get_children())
        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        cur.execute("""
            SELECT customer_id, customer_name, phone, customer_type
            FROM customers ORDER BY customer_id DESC
        """)
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        cur.close()
        con.close()

    def save():
        name = entries["Customer Name"].get().strip()
        phone = entries["Phone"].get().strip() or None
        ctype = entries["Customer Type"].get().strip() or "Student"

        if not name:
            messagebox.showwarning("Warning", "Enter customer name.")
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO customers(customer_name, phone, customer_type)
                VALUES(%s, %s, %s)
            """, (name, phone, ctype))
            con.commit()
            messagebox.showinfo("Success", "Customer added.")
            clear()
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    def update():
        cid = selected_id()
        if not cid:
            messagebox.showwarning("Warning", "Select a customer.")
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE customers
                SET customer_name=%s, phone=%s, customer_type=%s
                WHERE customer_id=%s
            """, (
                entries["Customer Name"].get().strip(),
                entries["Phone"].get().strip() or None,
                entries["Customer Type"].get().strip() or "Student",
                cid
            ))
            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Customer updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    def delete():
        cid = selected_id()
        if not cid:
            messagebox.showwarning("Warning", "Select a customer.")
            return
        if not messagebox.askyesno("Confirm", "Delete this customer?"):
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM customers WHERE customer_id=%s", (cid,))
            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Customer deleted.")
        except Exception:
            con.rollback()
            messagebox.showerror(
                "Cannot Delete",
                "This customer may have existing orders."
            )
        finally:
            cur.close()
            con.close()

    tk.Button(window, text="ADD CUSTOMER", command=save, width=16).pack(side="left", padx=25, pady=10)
    tk.Button(window, text="UPDATE", command=update, width=16).pack(side="left", padx=5)
    tk.Button(window, text="DELETE", command=delete, width=16).pack(side="left", padx=5)
    tk.Button(window, text="CLEAR", command=clear, width=16).pack(side="left", padx=5)

    load()


# ---------------- INVENTORY ----------------

def open_inventory(parent):
    window, entries, table, clear, selected_id = create_window(
        parent, "Inventory Management",
        ("Inventory ID", "Product ID", "Product", "Quantity", "Reorder Level"),
        ("Product ID", "Quantity", "Reorder Level")
    )

    def load():
        table.delete(*table.get_children())
        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        cur.execute("""
            SELECT i.inventory_id, p.product_id, p.product_name,
                   i.quantity_available, i.reorder_level
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            ORDER BY i.inventory_id
        """)
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        cur.close()
        con.close()

    def save():
        try:
            pid = int(entries["Product ID"].get())
            qty = int(entries["Quantity"].get())
            reorder = int(entries["Reorder Level"].get())
            if qty < 0 or reorder < 0:
                raise ValueError("Values cannot be negative.")
        except ValueError as e:
            messagebox.showwarning("Invalid Input", str(e))
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO inventory(product_id, quantity_available, reorder_level)
                VALUES(%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                quantity_available=%s, reorder_level=%s
            """, (pid, qty, reorder, qty, reorder))
            con.commit()
            messagebox.showinfo("Success", "Inventory saved.")
            clear()
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    def update():
        iid = selected_id()
        if not iid:
            messagebox.showwarning("Warning", "Select an inventory row.")
            return

        try:
            qty = int(entries["Quantity"].get())
            reorder = int(entries["Reorder Level"].get())
            if qty < 0 or reorder < 0:
                raise ValueError("Values cannot be negative.")
        except ValueError as e:
            messagebox.showwarning("Invalid Input", str(e))
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE inventory
                SET quantity_available=%s, reorder_level=%s
                WHERE inventory_id=%s
            """, (qty, reorder, iid))
            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Inventory updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    def low_stock():
        for item in table.get_children():
            values = table.item(item, "values")
            if int(values[3]) <= int(values[4]):
                table.selection_set(item)
                table.focus(item)
                table.see(item)
                return
        messagebox.showinfo("Stock", "No low-stock products found.")

    tk.Button(window, text="SAVE STOCK", command=save, width=16).pack(side="left", padx=25, pady=10)
    tk.Button(window, text="UPDATE STOCK", command=update, width=16).pack(side="left", padx=5)
    tk.Button(window, text="LOW STOCK", command=low_stock, width=16).pack(side="left", padx=5)
    tk.Button(window, text="REFRESH", command=load, width=16).pack(side="left", padx=5)

    load()


# ---------------- SUPPLIERS ----------------

def open_suppliers(parent):
    window, entries, table, clear, selected_id = create_window(
        parent, "Supplier Management",
        ("ID", "Supplier Name", "Phone", "Email", "Address"),
        ("Supplier Name", "Phone", "Email", "Address")
    )

    def load():
        table.delete(*table.get_children())
        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        cur.execute("""
            SELECT supplier_id, supplier_name, phone, email, address
            FROM suppliers ORDER BY supplier_id DESC
        """)
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        cur.close()
        con.close()

    def save():
        name = entries["Supplier Name"].get().strip()
        if not name:
            messagebox.showwarning("Warning", "Enter supplier name.")
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO suppliers(supplier_name, phone, email, address)
                VALUES(%s, %s, %s, %s)
            """, (
                name,
                entries["Phone"].get().strip() or None,
                entries["Email"].get().strip() or None,
                entries["Address"].get().strip()
            ))
            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Supplier added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    def update():
        sid = selected_id()
        if not sid:
            messagebox.showwarning("Warning", "Select a supplier.")
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE suppliers
                SET supplier_name=%s, phone=%s, email=%s, address=%s
                WHERE supplier_id=%s
            """, (
                entries["Supplier Name"].get().strip(),
                entries["Phone"].get().strip() or None,
                entries["Email"].get().strip() or None,
                entries["Address"].get().strip(),
                sid
            ))
            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Supplier updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    def delete():
        sid = selected_id()
        if not sid:
            messagebox.showwarning("Warning", "Select a supplier.")
            return
        if not messagebox.askyesno("Confirm", "Delete this supplier?"):
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM suppliers WHERE supplier_id=%s", (sid,))
            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Supplier deleted.")
        except Exception:
            con.rollback()
            messagebox.showerror(
                "Cannot Delete",
                "This supplier may be linked to existing purchases."
            )
        finally:
            cur.close()
            con.close()

    tk.Button(window, text="ADD SUPPLIER", command=save, width=16).pack(side="left", padx=25, pady=10)
    tk.Button(window, text="UPDATE", command=update, width=16).pack(side="left", padx=5)
    tk.Button(window, text="DELETE", command=delete, width=16).pack(side="left", padx=5)
    tk.Button(window, text="CLEAR", command=clear, width=16).pack(side="left", padx=5)

    load()


# ---------------- EXPENSES ----------------

def open_expenses(parent):
    window, entries, table, clear, selected_id = create_window(
        parent, "Expense Management",
        ("ID", "Category", "Amount", "Date", "Description"),
        ("Expense Category", "Amount", "Description")
    )

    def load():
        table.delete(*table.get_children())
        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        cur.execute("""
            SELECT expense_id, expense_category, amount,
                   expense_date, description
            FROM expenses ORDER BY expense_date DESC, expense_id DESC
        """)
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        cur.close()
        con.close()

    def save():
        category = entries["Expense Category"].get().strip()
        description = entries["Description"].get().strip()

        try:
            amount = float(entries["Amount"].get())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError as e:
            messagebox.showwarning("Invalid Amount", str(e))
            return

        if not category:
            messagebox.showwarning("Warning", "Enter expense category.")
            return

        con = get_connection()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("SELECT user_id FROM users WHERE username='admin' LIMIT 1")
            user = cur.fetchone()

            if not user:
                raise Exception("Admin user not found.")

            cur.execute("""
                INSERT INTO expenses
                (user_id, expense_category, amount, expense_date, description)
                VALUES(%s, %s, %s, CURDATE(), %s)
            """, (user[0], category, amount, description))

            con.commit()
            clear()
            load()
            messagebox.showinfo("Success", "Expense recorded.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            con.close()

    tk.Button(window, text="ADD EXPENSE", command=save, width=18).pack(side="left", padx=30, pady=10)
    tk.Button(window, text="REFRESH", command=load, width=18).pack(side="left", padx=10)
    tk.Button(window, text="CLEAR", command=clear, width=18).pack(side="left", padx=10)

    load()
