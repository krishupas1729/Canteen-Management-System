import tkinter as tk
from tkinter import messagebox
from db import get_connection
def get_stats():
    stats = {
        "products": 0,
        "orders": 0,
        "sales": 0,
        "total_sales": 0,
        "expenses": 0,
        "low_stock": 0
    }
    connection = get_connection()
    if connection is None:
        return stats
    cursor = connection.cursor()
    queries = {
        "products": """
            SELECT COUNT(*)
            FROM products
            WHERE is_available = 1
        """,
        "orders": """
            SELECT COUNT(*)
            FROM orders
        """,
        "sales": """
            SELECT COALESCE(SUM(amount), 0)
            FROM payments
            WHERE payment_status = 'Paid'
            AND DATE(payment_date) = CURDATE()
        """,
        "total_sales": """
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE payment_status = 'Paid'
    """,
        "expenses": """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE DATE(expense_date) = CURDATE()
        """,
        "low_stock": """
            SELECT COUNT(*)
            FROM inventory
            WHERE quantity_available <= reorder_level
        """
    }
    for key, query in queries.items():
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                stats[key] = result[0]
        except Exception as error:
            print(f"Error loading {key}: {error}")
    cursor.close()
    connection.close()
    return stats
dashboard = tk.Tk()
dashboard.title("Canteen Management System")
dashboard.geometry("1100x750")
dashboard.minsize(950, 650)
dashboard.configure(bg="#eef2f7")
header = tk.Frame(
    dashboard,
    bg="#183153",
    height=85
)
header.pack(fill="x")
tk.Label(
    header,
    text="CANTEEN MANAGEMENT SYSTEM",
    font=("Arial", 23, "bold"),
    bg="#183153",
    fg="white"
).pack(pady=22)
tk.Label(
    dashboard,
    text="ADMIN DASHBOARD",
    font=("Arial", 20, "bold"),
    bg="#eef2f7",
    fg="#183153"
).pack(pady=20)
stats_frame = tk.Frame(
    dashboard,
    bg="#eef2f7"
)
stats_frame.pack(pady=10)
def display_stats():
    stats = get_stats()

    for widget in stats_frame.winfo_children():
        widget.destroy()
    cards = [
        ("TOTAL PRODUCTS", stats["products"]),
        ("TOTAL ORDERS", stats["orders"]),
        ("TODAY'S SALES", f"Rs. {float(stats['sales']):.2f}"),
        ("TOTAL SALES", f"Rs. {float(stats['total_sales']):.2f}"),
        ("TODAY'S EXPENSES", f"Rs. {float(stats['expenses']):.2f}"),
        ("LOW STOCK ITEMS", stats["low_stock"])
    ]
    for i, (title, value) in enumerate(cards):
        card = tk.Frame(
            stats_frame,
            bg="white",
            width=190,
            height=100,
            highlightbackground="#cccccc",
            highlightthickness=1
        )
        card.grid(
            row=i // 3,
            column=i % 3,
            padx=12,
            pady=12
        )
        card.pack_propagate(False)
        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#555555"
        ).pack(pady=(18, 5))
        tk.Label(
            card,
            text=str(value),
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#183153"
        ).pack()
display_stats()
tk.Label(
    dashboard,
    text="MANAGEMENT MODULES",
    font=("Arial", 16, "bold"),
    bg="#eef2f7",
    fg="#183153"
).pack(pady=15)
modules = [
    "Products",
    "Categories",
    "Customers",
    "Orders",
    "Order History",
    "Payments",
    "Inventory",
    "Suppliers",
    "Purchases",
    "Expenses",
    "Reports"
]
def open_module(module_name):
    try:
        if module_name == "Products":
            from products import open_products
            open_products(dashboard)
        elif module_name == "Categories":
            from categories import open_categories
            open_categories(dashboard)
        elif module_name == "Customers":
            from operations import open_customers
            open_customers(dashboard)
        elif module_name == "Inventory":
            from operations import open_inventory
            open_inventory(dashboard)
        elif module_name == "Suppliers":
            from operations import open_suppliers
            open_suppliers(dashboard)
        elif module_name == "Purchases":
            from purchases import open_purchases
            open_purchases(dashboard)
        elif module_name == "Expenses":
            from operations import open_expenses
            open_expenses(dashboard)
        elif module_name == "Orders":
            from orders import open_orders
            open_orders(dashboard)
        elif module_name == "Order History":
            from order_history import open_order_history
            open_order_history(dashboard)
        elif module_name == "Payments":
            from payment_history import open_payment_history
            open_payment_history(dashboard)
        elif module_name == "Reports":
            from reports import open_reports
            open_reports(dashboard)
        else:
            messagebox.showinfo("Coming Next", module_name + " module will be connected next.")
    except Exception as error:
        messagebox.showerror("Module Error", str(error))
buttons = tk.Frame(
    dashboard,
    bg="#eef2f7"
)
buttons.pack(pady=10)
for i, module in enumerate(modules):
    tk.Button(
        buttons,
        text=module,
        font=("Arial", 12, "bold"),
        width=19,
        height=2,
        bg="#183153",
        fg="white",
        activebackground="#2874a6",
        activeforeground="white",
        cursor="hand2",
        command=lambda name=module: open_module(name)
    ).grid(
        row=i // 5,
        column=i % 5,
        padx=10,
        pady=10
    )
def refresh_dashboard():
    display_stats()
    messagebox.showinfo(
        "Dashboard",
        "Dashboard refreshed successfully!"
    )
tk.Button(
    dashboard,
    text="REFRESH DASHBOARD",
    font=("Arial", 11, "bold"),
    bg="#2874a6",
    fg="white",
    width=22,
    command=refresh_dashboard
).pack(pady=12)
def logout():
    confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )
    if confirm:
        dashboard.destroy()
        import login
tk.Button(
    dashboard,
    text="LOGOUT",
    font=("Arial", 12, "bold"),
    bg="#c0392b",
    fg="white",
    width=18,
    height=2,
    command=logout
).pack(pady=15)
dashboard.mainloop()