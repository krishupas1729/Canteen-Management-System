
import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def open_order_history(parent):
    window = tk.Toplevel(parent)
    window.title("Order History")
    window.geometry("1100x600")
    window.configure(bg="#eef2f7")

    tk.Label(
        window,
        text="ORDER HISTORY",
        font=("Arial", 22, "bold"),
        bg="#eef2f7",
        fg="#183153"
    ).pack(pady=15)

    search_frame = tk.Frame(window, bg="#eef2f7")
    search_frame.pack(pady=10)

    tk.Label(
        search_frame, text="Search Order ID:",
        bg="#eef2f7"
    ).pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side="left", padx=5)

    columns = (
        "Order ID", "Date", "Customer", "Product",
        "Quantity", "Unit Price", "Item Total",
        "Total Bill", "Payment", "Status"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=18
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=105, anchor="center")

    table.pack(fill="both", expand=True, padx=15, pady=10)

    def load_orders():
        table.delete(*table.get_children())

        con = get_connection()
        if con is None:
            return

        cur = con.cursor()

        try:
            search_id = search_entry.get().strip()

            query = """
                SELECT
                    o.order_id,
                    o.order_date,
                    COALESCE(c.customer_name, 'Walk-in'),
                    p.product_name,
                    oi.quantity,
                    oi.unit_price,
                    (oi.quantity * oi.unit_price),
                    pay.amount,
                    pay.payment_method,
                    pay.payment_status
                FROM orders o
                LEFT JOIN customers c
                    ON o.customer_id = c.customer_id
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                JOIN products p
                    ON oi.product_id = p.product_id
                LEFT JOIN payments pay
                    ON o.order_id = pay.order_id
            """

            if search_id:
                if not search_id.isdigit():
                    messagebox.showwarning(
                        "Invalid Search",
                        "Enter a valid numeric Order ID."
                    )
                    return

                query += " WHERE o.order_id = %s"
                cur.execute(
                    query + " ORDER BY o.order_id DESC",
                    (int(search_id),)
                )
            else:
                cur.execute(query + " ORDER BY o.order_id DESC")

            rows = cur.fetchall()

            for row in rows:
                table.insert("", "end", values=row)

            if not rows:
                messagebox.showinfo(
                    "Order History",
                    "No matching orders found."
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            cur.close()
            con.close()

    def clear_search():
        search_entry.delete(0, tk.END)
        load_orders()

    buttons = tk.Frame(window, bg="#eef2f7")
    buttons.pack(pady=10)

    tk.Button(
        buttons, text="SEARCH",
        command=load_orders, width=15
    ).pack(side="left", padx=8)

    tk.Button(
        buttons, text="SHOW ALL",
        command=clear_search, width=15
    ).pack(side="left", padx=8)

    load_orders()
