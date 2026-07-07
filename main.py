import ast
import sqlite3

# Read sample.py
with open("sample.py", "r") as file:
    code = file.read()

# Convert to AST
tree = ast.parse(code)

# Connect to Database
conn = sqlite3.connect("trace.db")
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_number INTEGER,
    variable_name TEXT,
    value TEXT
)
""")


for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                line = node.lineno
                name = target.id
                value = ast.unparse(node.value)

                cursor.execute(
                    "INSERT INTO variables (line_number, variable_name, value) VALUES (?, ?, ?)",
                    (line, name, value)
                )

conn.commit()

print("Data Saved Successfully!")
conn.commit()

print("Data Saved Successfully!")

print("\nSaved Data:\n")

cursor.execute("SELECT * FROM variables")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

conn.close()