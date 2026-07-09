import sys
import sqlite3

conn = sqlite3.connect("trace.db",timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS variables(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_number INTEGER,
    variable_name TEXT,
    value TEXT
)
""")
cursor.execute("DELETE FROM variables")
conn.commit()


conn.commit()

ignore = {
    "__name__", "__doc__", "__package__", "__loader__", "__spec__",
    "__annotations__", "__builtins__", "__file__", "__cached__"
}

target_file = ""

def tracer(frame, event, arg):

    if event != "line":
        return tracer

    
    if frame.f_code.co_filename != target_file:
        return tracer

    for var, value in frame.f_locals.items():

        if var.startswith("__"):
            continue

        cursor.execute(
            "INSERT INTO variables(line_number, variable_name, value) VALUES(?,?,?)",
            (frame.f_lineno, var, str(value))
        )

    return tracer


if len(sys.argv) > 1:
    target_file = sys.argv[1]
else:
    target_file = "sample.py"

sys.settrace(tracer)

with open(target_file, "r") as f:
    source = f.read()

exec(compile(source, target_file, "exec"), {})

sys.settrace(None)

conn.commit()
conn.close()

print("Tracing Completed Successfully!")