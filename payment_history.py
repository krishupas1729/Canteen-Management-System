import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


def open_payment_history(parent):

    window = tk.Toplevel(parent)
    window.title("Payment History")
    window.geometry("1100x650")
    window.configure(bg="#eef2f7")

    tk.Label(
        window,
        text="PAYMENT HISTORY",
        font=("Arial", 22, "bold"),
        bg="#eef2f7",
        fg="#183153"
    ).pack(pady=15)

    # SUMMARY
    summary_frame = tk.Frame(window, bg="#eef2f7")
    summary_frame.pack(fill="x", padx=20, pady=10)

    total_label = tk.Label(
        summary_frame,
        text="Total Payments: Rs. 0.00",
        font=("Arial", 15, "bold"),
        bg="#eef2f7",
        fg="#183153"
    )
    total_label.pack(side="left", padx=15)

    count_label = tk.Label(
        summary_frame,
        text="Number of Payments: 0",
        font=("Arial", 15, "bold"),
        bg="#eef2f7",
        fg="#183153"
    )
    count_label.pack(side="left", padx=15)

    # SEARCH
    search_frame = tk.Frame(window, bg="#eef2f7")
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search Order ID:",
        bg="#eef2f7"
    ).pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side="left", padx=5)

    # PAYMENT TABLE
    columns = (
        "Payment ID",
        "Order ID",
        "Amount",
        "Payment Method",
        "Payment Date",
        "Payment Status"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=17
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=165, anchor="center")

    table.pack(fill="both", expand=True, padx=20, pady=10)

    def load_payments(order_id=None):

        table.delete(*table.get_children())

        con = get_connection()

        if con is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )
            return

        cur = con.cursor()

        try:
            query = """
                SELECT
                    payment_id,
                    order_id,
                    amount,
                    payment_method,
                    payment_date,
                    payment_status
                FROM payments
            """

            if order_id:
                query += " WHERE order_id = %s"
                cur.execute(query + " ORDER BY payment_id DESC", (order_id,))
            else:
                cur.execute(query + " ORDER BY payment_id DESC")

            rows = cur.fetchall()

            total = 0
            for row in rows:
                amount = float(row[2])
                total += amount

                table.insert("", "end", values=(
                    row[0],
                    row[1],
                    f"Rs. {amount:.2f}",
                    row[3],
                    row[4],
                    row[5]
                ))

            total_label.config(
                text=f"Total Payments: Rs. {total:.2f}"
            )

            count_label.config(
                text=f"Number of Payments: {len(rows)}"
            )

        except Exception as e:
            messagebox.showerror("Payment Error", str(e))

        finally:
            cur.close()
            con.close()

    def search_payment():

        value = search_entry.get().strip()

        if not value:
            load_payments()
            return

        if not value.isdigit():
            messagebox.showwarning(
                "Invalid Input",
                "Enter a valid Order ID."
            )
            return

        load_payments(int(value))

    def show_all():
        search_entry.delete(0, tk.END)
        load_payments()

    # BUTTONS
    button_frame = tk.Frame(window, bg="#eef2f7")
    button_frame.pack(pady=12)

    tk.Button(
        button_frame,
        text="SEARCH",
        command=search_payment,
        width=15,
        bg="#183153",
        fg="white"
    ).pack(side="left", padx=8)

    tk.Button(
        button_frame,
        text="SHOW ALL",
        command=show_all,
        width=15
    ).pack(side="left", padx=8)

    tk.Button(
        button_frame,
        text="REFRESH",
        command=load_payments,
        width=15
    ).pack(side="left", padx=8)

    load_payments()