import tkinter as tk
from tkinter import ttk
import sqlite3


conn = sqlite3.connect("trace.db")
cursor = conn.cursor()


root = tk.Tk()
root.title("Python Variable Tracer")
root.geometry("600x400")


tree = ttk.Treeview(root)
tree["columns"] = ("Line", "Variable", "Value")

tree.column("#0", width=0, stretch=False)
tree.column("Line", width=100)
tree.column("Variable", width=180)
tree.column("Value", width=180)

tree.heading("#0", text="")
tree.heading("Line", text="Line Number")
tree.heading("Variable", text="Variable Name")
tree.heading("Value", text="Value")


cursor.execute("SELECT line_number, variable_name, value FROM variables")

for row in cursor.fetchall():
    tree.insert("", tk.END, values=row)

tree.pack(fill="both", expand=True)

conn.close()

root.mainloop()