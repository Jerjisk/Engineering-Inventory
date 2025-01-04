import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Database setup
def initialize_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Database operations
def add_item(id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (id, name, quantity, price) VALUES (?, ?, ?, ?)", (id, name, quantity, price))
    conn.commit()
    conn.close()

def view_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()
    return items

def update_item(item_id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# GUI Functions
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in view_inventory():
        tree.insert("", "end", values=item)

def get_valid_quantity():
    while True:
        quantity = simpledialog.askstring("Input", "Enter item quantity:")
        if quantity is None:  # If the user presses Cancel
            return None
        try:
            quantity = int(quantity)
            return quantity
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be an integer. Please enter again.")

def get_valid_price():
    while True:
        price = simpledialog.askstring("Input", "Enter item price:")
        if price is None:  # If the user presses Cancel
            return None
        try:
            price = float(price)
            return price
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a valid number. Please enter again.")

def get_valid_id():
    while True:
        item_id = simpledialog.askstring("Input", "Enter item ID:")
        if item_id is None:  # If the user presses Cancel
            return None
        try:
            item_id = int(item_id)
            return item_id
        except ValueError:
            messagebox.showerror("Invalid Input", "ID must be an integer. Please enter again.")

def add_item_gui():
    item_id = get_valid_id()
    if item_id is None:
        return
    name = simpledialog.askstring("Add Item", "Enter item name:")
    if name:
        quantity = get_valid_quantity()
        if quantity is None:
            return
        price = get_valid_price()
        if price is None:
            return
        add_item(item_id, name, quantity, price)
        refresh_table()
        messagebox.showinfo("Success", "Item added successfully!")

def update_item_gui():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)["values"]
        item_id = item[0]
        name = simpledialog.askstring("Update Item", "Enter new name:", initialvalue=item[1])
        quantity = get_valid_quantity()
        if quantity is None:
            return
        price = get_valid_price()
        if price is None:
            return
        update_item(item_id, name, quantity, price)
        refresh_table()
        messagebox.showinfo("Success", "Item updated successfully!")
    else:
        messagebox.showerror("Error", "No item selected!")

def delete_item_gui():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)["values"]
        item_id = item[0]
        delete_item(item_id)
        refresh_table()
        messagebox.showinfo("Success", "Item deleted successfully!")
    else:
        messagebox.showerror("Error", "No item selected!")

# Main GUI
initialize_database()

root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x400")

# Table
columns = ("ID", "Name", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=10)

tk.Button(button_frame, text="Add Item", command=add_item_gui).pack(side="left", padx=5)
tk.Button(button_frame, text="Update Item", command=update_item_gui).pack(side="left", padx=5)
tk.Button(button_frame, text="Delete Item", command=delete_item_gui).pack(side="left", padx=5)

# Initial Data Load
refresh_table()

root.mainloop()