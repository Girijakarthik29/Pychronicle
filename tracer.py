import sys
import sqlite3
import os

DB_FILE = "trace.db"

# Connect to database
conn = sqlite3.connect(DB_FILE, timeout=30)
cursor = conn.cursor()

# Create table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_number INTEGER,
    variable_name TEXT,
    value TEXT
)
""")

# Remove old trace records
cursor.execute("DELETE FROM variables")
conn.commit()

target_file = ""


def tracer(frame, event, arg):

    if event != "line":
        return tracer

    # Trace only the uploaded Python file
    if os.path.abspath(frame.f_code.co_filename) != os.path.abspath(target_file):
        return tracer

    for var, value in frame.f_locals.items():

        # Ignore Python internal variables
        if var.startswith("__"):
            continue

        try:
            cursor.execute(
                """
                INSERT INTO variables
                (line_number, variable_name, value)
                VALUES (?, ?, ?)
                """,
                (frame.f_lineno, var, str(value))
            )
        except sqlite3.Error as e:
            print("Database error:", e)

    return tracer


# Get uploaded file
if len(sys.argv) > 1:
    target_file = sys.argv[1]
else:
    target_file = "sample.py"

target_file = os.path.abspath(target_file)

print("Tracing:", target_file)

# Start tracing
sys.settrace(tracer)

try:

    with open(target_file, "r", encoding="utf-8") as f:
        source = f.read()

    # Execute uploaded Python program
    exec(
        compile(source, target_file, "exec"),
        {"__name__": "__main__"}
    )

finally:

    # Stop tracing
    sys.settrace(None)

    # Save database changes
    conn.commit()
    conn.close()

print("Tracing Completed Successfully!")