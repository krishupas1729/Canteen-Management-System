import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def open_purchases(parent):
    window = tk.Toplevel(parent)
    window.title("Purchase Management")
    window.geometry("1150x720")
    window.configure(bg="#eef2f7")

    tk.Label(
        window, text="PURCHASE MANAGEMENT",
        font=("Arial", 22, "bold"),
        bg="#eef2f7", fg="#183153"
    ).pack(pady=12)

    # Purchase details
    details = tk.Frame(window, bg="#eef2f7")
    details.pack(fill="x", padx=20, pady=8)

    tk.Label(details, text="Supplier:", bg="#eef2f7").grid(
        row=0, column=0, padx=5, pady=8
    )
    supplier_combo = ttk.Combobox(details, width=30, state="readonly")
    supplier_combo.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(details, text="Invoice Number:", bg="#eef2f7").grid(
        row=0, column=2, padx=5, pady=8
    )
    invoice_entry = tk.Entry(details, width=25)
    invoice_entry.grid(row=0, column=3, padx=5, pady=8)

    # Product selection
    product_frame = tk.LabelFrame(
        window, text="Add Products",
        font=("Arial", 12, "bold"),
        bg="#eef2f7", padx=10, pady=10
    )
    product_frame.pack(fill="x", padx=20, pady=8)

    tk.Label(product_frame, text="Product:", bg="#eef2f7").grid(
        row=0, column=0, padx=5, pady=8
    )
    product_combo = ttk.Combobox(
        product_frame, width=30, state="readonly"
    )
    product_combo.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(product_frame, text="Quantity:", bg="#eef2f7").grid(
        row=0, column=2, padx=5, pady=8
    )
    quantity_entry = tk.Entry(product_frame, width=12)
    quantity_entry.grid(row=0, column=3, padx=5, pady=8)

    tk.Label(product_frame, text="Unit Cost (Rs.):", bg="#eef2f7").grid(
        row=0, column=4, padx=5, pady=8
    )
    cost_entry = tk.Entry(product_frame, width=12)
    cost_entry.grid(row=0, column=5, padx=5, pady=8)

    # Cart
    columns = ("Product ID", "Product", "Quantity", "Unit Cost", "Subtotal")
    cart_table = ttk.Treeview(
        window, columns=columns, show="headings", height=8
    )

    for col in columns:
        cart_table.heading(col, text=col)
        cart_table.column(col, width=180, anchor="center")

    cart_table.pack(fill="x", padx=20, pady=10)

    cart = {}

    total_label = tk.Label(
        window, text="Purchase Total: Rs. 0.00",
        font=("Arial", 16, "bold"),
        bg="#eef2f7", fg="#183153"
    )
    total_label.pack(pady=5)

    # Purchase history
    tk.Label(
        window, text="PURCHASE HISTORY",
        font=("Arial", 15, "bold"),
        bg="#eef2f7", fg="#183153"
    ).pack(pady=8)

    history_columns = (
        "Purchase ID", "Supplier", "Purchase Date",
        "Invoice Number", "Total Amount"
    )

    history_table = ttk.Treeview(
        window, columns=history_columns,
        show="headings", height=7
    )

    for col in history_columns:
        history_table.heading(col, text=col)
        history_table.column(col, width=200, anchor="center")

    history_table.pack(fill="both", expand=True, padx=20, pady=8)

    supplier_map = {}
    product_map = {}

    def load_dropdowns():
        con = get_connection()
        if con is None:
            messagebox.showerror("Database Error", "Connection failed.")
            return

        cur = con.cursor()

        try:
            cur.execute("""
                SELECT supplier_id, supplier_name
                FROM suppliers
                ORDER BY supplier_name
            """)
            suppliers = cur.fetchall()

            supplier_map.clear()
            supplier_combo["values"] = []

            supplier_values = []
            for supplier_id, supplier_name in suppliers:
                display = f"{supplier_id} - {supplier_name}"
                supplier_values.append(display)
                supplier_map[display] = supplier_id

            supplier_combo["values"] = supplier_values

            cur.execute("""
                SELECT product_id, product_name
                FROM products
                WHERE is_available = 1
                ORDER BY product_name
            """)
            products = cur.fetchall()

            product_map.clear()
            product_combo["values"] = []

            product_values = []
            for product_id, product_name in products:
                display = f"{product_id} - {product_name}"
                product_values.append(display)
                product_map[display] = product_id

            product_combo["values"] = product_values

        except Exception as error:
            messagebox.showerror("Loading Error", str(error))

        finally:
            cur.close()
            con.close()

    def update_cart_table():
        cart_table.delete(*cart_table.get_children())

        total = 0

        for product_id, item in cart.items():
            subtotal = item["quantity"] * item["unit_cost"]
            total += subtotal

            cart_table.insert("", "end", values=(
                product_id,
                item["name"],
                item["quantity"],
                f"Rs. {item['unit_cost']:.2f}",
                f"Rs. {subtotal:.2f}"
            ))

        total_label.config(text=f"Purchase Total: Rs. {total:.2f}")

    def add_product():
        selected = product_combo.get()

        if selected not in product_map:
            messagebox.showwarning("Select Product", "Select a product.")
            return

        try:
            product_id = product_map[selected]
            quantity = int(quantity_entry.get())
            unit_cost = float(cost_entry.get())

            if quantity <= 0 or unit_cost <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Enter a positive whole quantity and a positive unit cost."
            )
            return

        product_name = selected.split(" - ", 1)[1]

        if product_id in cart:
            old = cart[product_id]

            # Combine duplicate product lines using weighted average cost.
            new_quantity = old["quantity"] + quantity
            new_cost = (
                old["quantity"] * old["unit_cost"] +
                quantity * unit_cost
            ) / new_quantity

            old["quantity"] = new_quantity
            old["unit_cost"] = new_cost

        else:
            cart[product_id] = {
                "name": product_name,
                "quantity": quantity,
                "unit_cost": unit_cost
            }

        update_cart_table()

        quantity_entry.delete(0, tk.END)
        cost_entry.delete(0, tk.END)

    def remove_product():
        selected = cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Product", "Select a cart row to remove."
            )
            return

        values = cart_table.item(selected[0], "values")
        product_id = int(values[0])

        cart.pop(product_id, None)
        update_cart_table()

    def load_history():
        history_table.delete(*history_table.get_children())

        con = get_connection()
        if con is None:
            return

        cur = con.cursor()

        try:
            cur.execute("""
                SELECT pu.purchase_id, s.supplier_name,
                       pu.purchase_date, pu.invoice_number,
                       COALESCE(SUM(pi.quantity * pi.unit_cost), 0)
                FROM purchases pu
                JOIN suppliers s ON pu.supplier_id = s.supplier_id
                LEFT JOIN purchase_items pi
                    ON pu.purchase_id = pi.purchase_id
                GROUP BY pu.purchase_id, s.supplier_name,
                         pu.purchase_date, pu.invoice_number
                ORDER BY pu.purchase_id DESC
            """)

            for row in cur.fetchall():
                history_table.insert("", "end", values=(
                    row[0], row[1], row[2],
                    row[3] if row[3] else "-",
                    f"Rs. {float(row[4]):.2f}"
                ))

        except Exception as error:
            messagebox.showerror("History Error", str(error))

        finally:
            cur.close()
            con.close()

    def save_purchase():
        supplier_display = supplier_combo.get()

        if supplier_display not in supplier_map:
            messagebox.showwarning(
                "Select Supplier", "Please select a supplier."
            )
            return

        if not cart:
            messagebox.showwarning(
                "Empty Purchase", "Add at least one product."
            )
            return

        invoice_number = invoice_entry.get().strip() or None
        con = get_connection()

        if con is None:
            messagebox.showerror("Database Error", "Connection failed.")
            return

        cur = con.cursor()

        try:
            cur.execute("""
                SELECT user_id
                FROM users
                WHERE username = 'admin' AND is_active = 1
                LIMIT 1
            """)
            user = cur.fetchone()

            if not user:
                raise Exception("Active admin user not found.")

            user_id = user[0]
            supplier_id = supplier_map[supplier_display]

            # Create purchase record.
            cur.execute("""
                INSERT INTO purchases
                (supplier_id, user_id, purchase_date, invoice_number)
                VALUES (%s, %s, CURDATE(), %s)
            """, (supplier_id, user_id, invoice_number))

            purchase_id = cur.lastrowid

            # Save items and increase inventory.
            for product_id, item in cart.items():
                cur.execute("""
                    INSERT INTO purchase_items
                    (purchase_id, product_id, quantity, unit_cost)
                    VALUES (%s, %s, %s, %s)
                """, (
                    purchase_id,
                    product_id,
                    item["quantity"],
                    item["unit_cost"]
                ))

                cur.execute("""
                    INSERT INTO inventory
                    (product_id, quantity_available, reorder_level)
                    VALUES (%s, %s, 5)
                    ON DUPLICATE KEY UPDATE
                    quantity_available =
                        quantity_available + VALUES(quantity_available),
                    last_updated = CURRENT_TIMESTAMP
                """, (product_id, item["quantity"]))

            con.commit()

            messagebox.showinfo(
                "Success",
                f"Purchase #{purchase_id} saved successfully.\n"
                "Inventory has been updated."
            )

            cart.clear()
            invoice_entry.delete(0, tk.END)
            update_cart_table()
            load_history()

        except Exception as error:
            con.rollback()
            messagebox.showerror("Purchase Error", str(error))

        finally:
            cur.close()
            con.close()

    # Buttons
    button_frame = tk.Frame(window, bg="#eef2f7")
    button_frame.pack(pady=10)

    tk.Button(
        product_frame, text="ADD TO PURCHASE",
        command=add_product,
        bg="#183153", fg="white",
        font=("Arial", 10, "bold"), padx=12, pady=6
    ).grid(row=1, column=1, pady=8)

    tk.Button(
        button_frame, text="REMOVE SELECTED",
        command=remove_product,
        bg="#c0392b", fg="white",
        font=("Arial", 10, "bold"), padx=12, pady=7
    ).pack(side="left", padx=8)

    tk.Button(
        button_frame, text="SAVE PURCHASE",
        command=save_purchase,
        bg="#087443", fg="white",
        font=("Arial", 10, "bold"), padx=15, pady=7
    ).pack(side="left", padx=8)

    tk.Button(
        button_frame, text="REFRESH HISTORY",
        command=load_history,
        bg="#555555", fg="white",
        font=("Arial", 10, "bold"), padx=12, pady=7
    ).pack(side="left", padx=8)

    load_dropdowns()
    load_history()