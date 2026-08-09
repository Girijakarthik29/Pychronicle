import sys
import sqlite3
import os

DB_FILE = "trace.db"


conn = sqlite3.connect(DB_FILE, timeout=30)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_number INTEGER,
    variable_name TEXT,
    value TEXT
)
""")


cursor.execute("DELETE FROM variables")
conn.commit()

target_file = ""


def tracer(frame, event, arg):

    if event != "line":
        return tracer

    
    if os.path.abspath(frame.f_code.co_filename) != os.path.abspath(target_file):
        return tracer

    for var, value in frame.f_locals.items():

        
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



if len(sys.argv) > 1:
    target_file = sys.argv[1]
else:
    target_file = "sample.py"

target_file = os.path.abspath(target_file)

print("Tracing:", target_file)


sys.settrace(tracer)

try:

    with open(target_file, "r", encoding="utf-8") as f:
        source = f.read()


    exec(
        compile(source, target_file, "exec"),
        {"__name__": "__main__"}
    )

finally:

    
    sys.settrace(None)

    
    conn.commit()
    conn.close()

print("Tracing Completed Successfully!")