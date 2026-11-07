
import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def open_orders(parent):
    window = tk.Toplevel(parent)
    window.title("Order Management")
    window.geometry("1000x700")
    window.configure(bg="#eef2f7")

    cart = []
    product_map = {}
    customer_map = {}

    tk.Label(
        window, text="CREATE NEW ORDER",
        font=("Arial", 22, "bold"),
        bg="#eef2f7", fg="#183153"
    ).pack(pady=12)

    # CUSTOMER
    top = tk.Frame(window, bg="#eef2f7")
    top.pack(pady=8)

    tk.Label(top, text="Customer:", bg="#eef2f7").grid(row=0, column=0, padx=8)

    customer_box = ttk.Combobox(top, width=35, state="readonly")
    customer_box.grid(row=0, column=1, padx=8)

    # PRODUCT SELECTION
    product_frame = tk.LabelFrame(
        window, text="Add Products",
        bg="#eef2f7", padx=10, pady=10
    )
    product_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(product_frame, text="Product:", bg="#eef2f7").grid(row=0, column=0)
    product_box = ttk.Combobox(product_frame, width=35, state="readonly")
    product_box.grid(row=0, column=1, padx=8)

    tk.Label(product_frame, text="Quantity:", bg="#eef2f7").grid(row=0, column=2)
    quantity_entry = tk.Entry(product_frame, width=10)
    quantity_entry.grid(row=0, column=3, padx=8)
    quantity_entry.insert(0, "1")

    # CART TABLE
    columns = ("Product ID", "Product", "Quantity", "Price", "Total")

    table = ttk.Treeview(
        window, columns=columns,
        show="headings", height=12
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=150)

    table.pack(fill="both", expand=True, padx=20, pady=10)

    total_label = tk.Label(
        window, text="Total: Rs. 0.00",
        font=("Arial", 18, "bold"),
        bg="#eef2f7", fg="#183153"
    )
    total_label.pack(pady=8)

    # PAYMENT
    payment_frame = tk.Frame(window, bg="#eef2f7")
    payment_frame.pack(pady=8)

    tk.Label(
        payment_frame, text="Payment Method:",
        bg="#eef2f7"
    ).grid(row=0, column=0, padx=8)

    payment_box = ttk.Combobox(
        payment_frame,
        values=["Cash", "UPI", "Card"],
        state="readonly",
        width=15
    )
    payment_box.grid(row=0, column=1, padx=8)
    payment_box.set("Cash")

    def load_data():
        con = get_connection()
        if con is None:
            return

        cur = con.cursor()

        try:
            cur.execute("""
                SELECT product_id, product_name, selling_price
                FROM products
                WHERE is_available = 1
                ORDER BY product_name
            """)

            product_map.clear()

            product_names = []

            for pid, name, price in cur.fetchall():
                label = f"{pid} - {name}"
                product_map[label] = (pid, name, float(price))
                product_names.append(label)

            product_box["values"] = product_names

            cur.execute("""
                SELECT customer_id, customer_name
                FROM customers
                ORDER BY customer_name
            """)

            customer_map.clear()
            customer_names = ["Walk-in Customer"]

            for cid, name in cur.fetchall():
                label = f"{cid} - {name}"
                customer_map[label] = cid
                customer_names.append(label)

            customer_box["values"] = customer_names
            customer_box.set("Walk-in Customer")

        except Exception as e:
            messagebox.showerror("Loading Error", str(e))

        finally:
            cur.close()
            con.close()

    def update_total():
        total = sum(item["quantity"] * item["price"] for item in cart)
        total_label.config(text=f"Total: Rs. {total:.2f}")

    def refresh_table():
        table.delete(*table.get_children())

        for item in cart:
            total = item["quantity"] * item["price"]

            table.insert("", "end", values=(
                item["product_id"],
                item["name"],
                item["quantity"],
                f"{item['price']:.2f}",
                f"{total:.2f}"
            ))

        update_total()

    def add_product():
        selected = product_box.get()

        if selected not in product_map:
            messagebox.showwarning("Warning", "Select a product.")
            return

        try:
            quantity = int(quantity_entry.get())

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

        except ValueError as e:
            messagebox.showwarning("Invalid Quantity", str(e))
            return

        pid, name, price = product_map[selected]

        existing = next(
            (item for item in cart if item["product_id"] == pid),
            None
        )

        if existing:
            existing["quantity"] += quantity
        else:
            cart.append({
                "product_id": pid,
                "name": name,
                "quantity": quantity,
                "price": price
            })

        refresh_table()
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, "1")

    def remove_product():
        selected = table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a cart item.")
            return

        pid = int(table.item(selected[0], "values")[0])

        cart[:] = [
            item for item in cart
            if item["product_id"] != pid
        ]

        refresh_table()

    def place_order():
        print("PLACE ORDER BUTTON CLICKED")
        if not cart:
            messagebox.showwarning("Warning", "Add products first.")
            return

        method = payment_box.get()

        if not method:
            messagebox.showwarning("Warning", "Select payment method.")
            return

        customer = customer_box.get()
        customer_id = customer_map.get(customer)

        total = sum(
            item["quantity"] * item["price"]
            for item in cart
        )

        con = get_connection()
        print("DATABASE CONNECTION:", con)

        if con is None:
            return

        cur = con.cursor()

        try:
            # Find admin user
            cur.execute("""
                SELECT user_id FROM users
                WHERE username='admin' AND is_active=1
                LIMIT 1
            """)

            user = cur.fetchone()

            if not user:
                raise Exception("Active admin user not found.")

            user_id = user[0]

            # Check stock before creating order
            for item in cart:
                cur.execute("""
                    SELECT quantity_available
                    FROM inventory
                    WHERE product_id=%s
                    FOR UPDATE
                """, (item["product_id"],))

                stock = cur.fetchone()

                if stock is None:
                    raise Exception(
                        f"Inventory not created for {item['name']}."
                    )

                if stock[0] < item["quantity"]:
                    raise Exception(
                        f"Insufficient stock for {item['name']}. "
                        f"Available: {stock[0]}"
                    )

            # Create order
            cur.execute("""
                INSERT INTO orders
                (customer_id, user_id, order_date, order_status)
                VALUES(%s, %s, NOW(), 'Completed')
            """, (customer_id, user_id))

            order_id = cur.lastrowid

            # Save order items and reduce inventory
            for item in cart:

                cur.execute("""
                    INSERT INTO order_items
                    (order_id, product_id, quantity, unit_price)
                    VALUES(%s, %s, %s, %s)
                """, (
                    order_id,
                    item["product_id"],
                    item["quantity"],
                    item["price"]
                ))

                cur.execute("""
                    UPDATE inventory
                    SET quantity_available = quantity_available - %s,
                        last_updated = NOW()
                    WHERE product_id = %s
                      AND quantity_available >= %s
                """, (
                    item["quantity"],
                    item["product_id"],
                    item["quantity"]
                ))

                if cur.rowcount != 1:
                    raise Exception(
                        f"Stock update failed for {item['name']}."
                    )

            # Save payment
            cur.execute("""
                INSERT INTO payments
                (order_id, amount, payment_method,
                 payment_date, payment_status)
                VALUES(%s, %s, %s, NOW(), 'Paid')
            """, (order_id, total, method))

            con.commit()
            print("ORDER SAVED SUCCESSFULLY")
            print("ORDER ID:", order_id)
            print("TOTAL:", total)

            messagebox.showinfo(
                "Order Successful",
                f"Order ID: {order_id}\n"
                f"Total: Rs. {total:.2f}\n"
                f"Payment: {method}\n\n"
                "Order placed successfully!"
            )

            cart.clear()
            refresh_table()
            load_data()

        except Exception as e:
            con.rollback()
            messagebox.showerror("Order Failed", str(e))

        finally:
            cur.close()
            con.close()

    # BUTTONS
    buttons = tk.Frame(window, bg="#eef2f7")
    buttons.pack(pady=12)

    tk.Button(
        buttons, text="ADD PRODUCT",
        command=add_product, width=17
    ).grid(row=0, column=0, padx=8)

    tk.Button(
        buttons, text="REMOVE ITEM",
        command=remove_product, width=17
    ).grid(row=0, column=1, padx=8)

    tk.Button(
        buttons, text="PLACE ORDER",
        command=place_order, width=17,
        bg="#183153", fg="white"
    ).grid(row=0, column=2, padx=8)

    tk.Button(
        buttons, text="CLEAR CART",
        command=lambda: (cart.clear(), refresh_table()),
        width=17
    ).grid(row=0, column=3, padx=8)

    load_data()
