import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import mysql.connector
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_database_if_not_exists():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
    )

    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS pharmacy_db")
    cursor.execute("USE pharmacy_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price FLOAT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(15),
            medicine_id INT NOT NULL,
            quantity INT NOT NULL,
            total_price FLOAT NOT NULL,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()

create_database_if_not_exists()

db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="pharmacy_db"
)
cursor = db.cursor()

class PharmacyManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.style = Style(theme="superhero")  # Modern theme

        self.sales_list = []

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.create_dashboard_tab()
        self.create_medicine_tab()
        self.create_sales_tab()

    def create_dashboard_tab(self):
        dashboard_tab = ttk.Frame(self.tabs)
        self.tabs.add(dashboard_tab, text="Dashboard")

        ttk.Label(dashboard_tab, text="Sales Dashboard", font=("Helvetica", 16)).pack(pady=10)

        self.plot_sales_chart(dashboard_tab)

    def plot_sales_chart(self, tab):
        cursor.execute("SELECT m.name, SUM(s.quantity) FROM sales s JOIN medicines m ON s.medicine_id = m.id GROUP BY m.id")
        data = cursor.fetchall()

        medicine_names = [row[0] for row in data]
        quantities = [row[1] for row in data]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(medicine_names, quantities, color='blue')
        ax.set_title("Medicine Sales")
        ax.set_ylabel("Quantity Sold")
        ax.set_xlabel("Medicines")

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.get_tk_widget().pack()

    def create_medicine_tab(self):
        medicine_tab = ttk.Frame(self.tabs)
        self.tabs.add(medicine_tab, text="Medicine")

        ttk.Label(medicine_tab, text="Medicine Management", font=("Helvetica", 14)).pack(pady=10)
        ttk.Button(medicine_tab, text="Add Medicine", command=self.add_medicine).pack(pady=5)
        ttk.Button(medicine_tab, text="View Medicines", command=self.view_medicines).pack(pady=5)

    def create_sales_tab(self):
        sales_tab = ttk.Frame(self.tabs)
        self.tabs.add(sales_tab, text="Sales")

        ttk.Label(sales_tab, text="Sales Management", font=("Helvetica", 14)).pack(pady=10)
        ttk.Button(sales_tab, text="Make Sale", command=self.make_sale).pack(pady=5)
        ttk.Button(sales_tab, text="View Temporary Sales", command=self.view_temporary_sales).pack(pady=5)

    def add_medicine(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Medicine")

        ttk.Label(add_window, text="Medicine Name:").grid(row=0, column=0, padx=10, pady=5)
        medicine_name_entry = ttk.Entry(add_window)
        medicine_name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(add_window, text="Price:").grid(row=1, column=0, padx=10, pady=5)
        price_entry = ttk.Entry(add_window)
        price_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_medicine():
            name = medicine_name_entry.get()
            price = float(price_entry.get())
            try:
                cursor.execute("INSERT INTO medicines (name, price) VALUES (%s, %s)", (name, price))
                db.commit()
                messagebox.showinfo("Success", "Medicine added successfully")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

        ttk.Button(add_window, text="Save", command=save_medicine).grid(row=2, column=0, columnspan=2, pady=10)

    def view_medicines(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Medicines")

        tree = ttk.Treeview(view_window, columns=("ID", "Name", "Price"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Price", text="Price")

        cursor.execute("SELECT * FROM medicines")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

        tree.pack(padx=10, pady=10)

    def make_sale(self):
        make_sale_window = tk.Toplevel(self.root)
        make_sale_window.title("Make Sale")

        ttk.Label(make_sale_window, text="Customer Name:").grid(row=0, column=0, padx=10, pady=5)
        customer_name_entry = ttk.Entry(make_sale_window)
        customer_name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(make_sale_window, text="Phone Number:").grid(row=1, column=0, padx=10, pady=5)
        phone_number_entry = ttk.Entry(make_sale_window)
        phone_number_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(make_sale_window, text="Medicine:").grid(row=2, column=0, padx=10, pady=5)
        cursor.execute("SELECT id, name FROM medicines")
        medicine_data = cursor.fetchall()
        medicine_name_combo = ttk.Combobox(make_sale_window, values=[med[1] for med in medicine_data])
        medicine_name_combo.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(make_sale_window, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
        quantity_entry = ttk.Entry(make_sale_window)
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        def generate_bill():
            customer_name = customer_name_entry.get()
            phone_number = phone_number_entry.get()
            medicine_name = medicine_name_combo.get()
            quantity = quantity_entry.get()

            if not medicine_name or not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Error", "Please select a valid medicine and quantity.")
                return

            selected_index = [med[1] for med in medicine_data].index(medicine_name)
            medicine_id = medicine_data[selected_index][0]
            quantity = int(quantity)

            cursor.execute("SELECT price FROM medicines WHERE id = %s", (medicine_id,))
            price = cursor.fetchone()[0]
            total_price = price * quantity

            cursor.execute(
                "INSERT INTO sales (customer_name, phone_number, medicine_id, quantity, total_price) VALUES (%s, %s, %s, %s, %s)",
                (customer_name, phone_number, medicine_id, quantity, total_price),
            )
            db.commit()

            messagebox.showinfo("Bill Generated", f"Total Bill: ${total_price:.2f}")
            self.plot_sales_chart(self.tabs.winfo_children()[0])  # Update the sales chart
            make_sale_window.destroy()

        ttk.Button(make_sale_window, text="Generate Bill", command=generate_bill).grid(row=4, column=0, columnspan=2, pady=10)

    def view_temporary_sales(self): 
        view_window = tk.Toplevel(self.root)
        view_window.title("View Temporary Sales")

        tree = ttk.Treeview(view_window, columns=("Customer", "Phone", "Medicine", "Quantity", "Total"), show='headings')
        tree.heading("Customer", text="Customer")
        tree.heading("Phone", text="Phone")
        tree.heading("Medicine", text="Medicine")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Total", text="Total")

        # Fetch sales data from the database
        cursor.execute("""
            SELECT s.customer_name, s.phone_number, m.name, s.quantity, s.total_price
            FROM sales s
            JOIN medicines m ON s.medicine_id = m.id
        """)
        sales_data = cursor.fetchall()

        # Insert fetched data into the Treeview
        for sale in sales_data:
            tree.insert("", "end", values=sale)

        tree.pack(padx=10, pady=10)

    def plot_sales_chart(self, tab):
        # Clear the existing plot (if any)
        for widget in tab.winfo_children():
            widget.destroy()

        cursor.execute("SELECT m.name, SUM(s.quantity) FROM sales s JOIN medicines m ON s.medicine_id = m.id GROUP BY m.id")
        data = cursor.fetchall()

        medicine_names = [row[0] for row in data]
        quantities = [row[1] for row in data]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(medicine_names, quantities, color='blue')
        ax.set_title("Medicine Sales")
        ax.set_ylabel("Quantity Sold")
        ax.set_xlabel("Medicines")

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.get_tk_widget().pack()

    def generate_bill(self, customer_name, phone_number, medicine_id, quantity, total_price):
        cursor.execute(
            "INSERT INTO sales (customer_name, phone_number, medicine_id, quantity, total_price) VALUES (%s, %s, %s, %s, %s)",
            (customer_name, phone_number, medicine_id, quantity, total_price),
        )
        db.commit()
        messagebox.showinfo("Bill Generated", f"Total Bill: ${total_price:.2f}")
        self.plot_sales_chart(self.tabs.winfo_children()[0])  # Update the sales chart


root = tk.Tk()
app = PharmacyManagementApp(root)
root.geometry("900x700")
root.mainloop()
