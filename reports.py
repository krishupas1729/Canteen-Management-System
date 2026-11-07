import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import get_connection


def open_reports(parent):
    window = tk.Toplevel(parent)
    window.title("Canteen Reports")
    window.geometry("1150x700")
    window.configure(bg="#eef2f7")

    tk.Label(
        window, text="CANTEEN REPORTS",
        font=("Arial", 22, "bold"),
        bg="#eef2f7", fg="#183153"
    ).pack(pady=15)

    # Date filter
    filter_frame = tk.Frame(window, bg="#eef2f7")
    filter_frame.pack(pady=10)

    today = date.today()

    tk.Label(filter_frame, text="From (YYYY-MM-DD):",
             bg="#eef2f7").pack(side="left", padx=5)

    from_entry = tk.Entry(filter_frame, width=14)
    from_entry.insert(0, today.replace(day=1).isoformat())
    from_entry.pack(side="left", padx=5)

    tk.Label(filter_frame, text="To (YYYY-MM-DD):",
             bg="#eef2f7").pack(side="left", padx=5)

    to_entry = tk.Entry(filter_frame, width=14)
    to_entry.insert(0, today.isoformat())
    to_entry.pack(side="left", padx=5)

    # Summary cards
    summary_frame = tk.Frame(window, bg="#eef2f7")
    summary_frame.pack(fill="x", padx=20, pady=15)

    sales_label = tk.Label(
        summary_frame, text="Sales: Rs. 0.00",
        font=("Arial", 14, "bold"), bg="white", fg="#183153",
        padx=15, pady=15
    )
    sales_label.pack(side="left", expand=True, fill="x", padx=5)

    cost_label = tk.Label(
        summary_frame, text="Product Cost: Rs. 0.00",
        font=("Arial", 14, "bold"), bg="white", fg="#183153",
        padx=15, pady=15
    )
    cost_label.pack(side="left", expand=True, fill="x", padx=5)

    expense_label = tk.Label(
        summary_frame, text="Expenses: Rs. 0.00",
        font=("Arial", 14, "bold"), bg="white", fg="#183153",
        padx=15, pady=15
    )
    expense_label.pack(side="left", expand=True, fill="x", padx=5)

    profit_label = tk.Label(
        summary_frame, text="Estimated Profit: Rs. 0.00",
        font=("Arial", 14, "bold"), bg="white", fg="#087443",
        padx=15, pady=15
    )
    profit_label.pack(side="left", expand=True, fill="x", padx=5)

    # Report tabs
    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", expand=True, padx=20, pady=10)

    best_frame = tk.Frame(notebook, bg="white")
    category_frame = tk.Frame(notebook, bg="white")

    notebook.add(best_frame, text="Best-Selling Products")
    notebook.add(category_frame, text="Category-wise Sales")

    best_columns = ("Product ID", "Product Name", "Quantity Sold", "Sales")
    best_table = ttk.Treeview(
        best_frame, columns=best_columns,
        show="headings", height=15
    )

    for col in best_columns:
        best_table.heading(col, text=col)
        best_table.column(col, width=200, anchor="center")

    best_table.pack(fill="both", expand=True, padx=10, pady=10)

    category_columns = ("Category", "Quantity Sold", "Sales")
    category_table = ttk.Treeview(
        category_frame, columns=category_columns,
        show="headings", height=15
    )

    for col in category_columns:
        category_table.heading(col, text=col)
        category_table.column(col, width=250, anchor="center")

    category_table.pack(fill="both", expand=True, padx=10, pady=10)

    def load_reports():
        start_date = from_entry.get().strip()
        end_date = to_entry.get().strip()

        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)

            if start > end:
                messagebox.showwarning(
                    "Invalid Dates",
                    "From date cannot be after To date."
                )
                return
        except ValueError:
            messagebox.showwarning(
                "Invalid Dates",
                "Enter dates in YYYY-MM-DD format."
            )
            return

        con = get_connection()
        if con is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )
            return

        cur = con.cursor()

        try:
            # Total paid sales
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM payments
                WHERE payment_status = 'Paid'
                AND DATE(payment_date) BETWEEN %s AND %s
            """, (start_date, end_date))
            sales = float(cur.fetchone()[0] or 0)

            # Cost of products sold
            cur.execute("""
                SELECT COALESCE(SUM(oi.quantity * p.cost_price), 0)
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE o.order_status = 'Completed'
                AND DATE(o.order_date) BETWEEN %s AND %s
            """, (start_date, end_date))
            product_cost = float(cur.fetchone()[0] or 0)

            # Expenses
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE DATE(expense_date) BETWEEN %s AND %s
            """, (start_date, end_date))
            expenses = float(cur.fetchone()[0] or 0)

            profit = sales - product_cost - expenses

            sales_label.config(text=f"Sales: Rs. {sales:.2f}")
            cost_label.config(text=f"Product Cost: Rs. {product_cost:.2f}")
            expense_label.config(text=f"Expenses: Rs. {expenses:.2f}")
            profit_label.config(
                text=f"Estimated Profit: Rs. {profit:.2f}",
                fg="#087443" if profit >= 0 else "#c0392b"
            )

            # Best-selling products
            best_table.delete(*best_table.get_children())

            cur.execute("""
                SELECT p.product_id, p.product_name,
                       SUM(oi.quantity) AS quantity_sold,
                       SUM(oi.quantity * oi.unit_price) AS total_sales
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE o.order_status = 'Completed'
                AND DATE(o.order_date) BETWEEN %s AND %s
                GROUP BY p.product_id, p.product_name
                ORDER BY quantity_sold DESC
            """, (start_date, end_date))

            for row in cur.fetchall():
                best_table.insert("", "end", values=(
                    row[0], row[1], row[2],
                    f"Rs. {float(row[3]):.2f}"
                ))

            # Category-wise sales
            category_table.delete(*category_table.get_children())

            cur.execute("""
                SELECT c.category_name,
                       SUM(oi.quantity) AS quantity_sold,
                       SUM(oi.quantity * oi.unit_price) AS total_sales
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                WHERE o.order_status = 'Completed'
                AND DATE(o.order_date) BETWEEN %s AND %s
                GROUP BY c.category_id, c.category_name
                ORDER BY total_sales DESC
            """, (start_date, end_date))

            for row in cur.fetchall():
                category_table.insert("", "end", values=(
                    row[0], row[1], f"Rs. {float(row[2]):.2f}"
                ))

        except Exception as error:
            messagebox.showerror("Report Error", str(error))

        finally:
            cur.close()
            con.close()

    tk.Button(
        filter_frame, text="GENERATE REPORT",
        command=load_reports,
        bg="#183153", fg="white",
        font=("Arial", 10, "bold"),
        padx=12, pady=6
    ).pack(side="left", padx=10)

    tk.Button(
        filter_frame, text="REFRESH",
        command=load_reports,
        bg="#087443", fg="white",
        font=("Arial", 10, "bold"),
        padx=12, pady=6
    ).pack(side="left", padx=5)

    load_reports()