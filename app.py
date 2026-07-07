from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os
import subprocess
import csv

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():

    search = request.args.get("search", "")
    code = ""

    py_files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.endswith(".py")
    ]

    if py_files:
        latest_file = max(
            [os.path.join(UPLOAD_FOLDER, f) for f in py_files],
            key=os.path.getmtime
        )

        with open(latest_file, "r", encoding="utf-8") as f:
            code = f.read()

    conn = sqlite3.connect("trace.db")
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT line_number, variable_name, value
            FROM variables
            WHERE variable_name LIKE ?
        """, ('%' + search + '%',))
    else:
        cursor.execute("""
            SELECT line_number, variable_name, value
            FROM variables
        """)

    data = cursor.fetchall()

    total_records = len(data)
    total_variables = len(set(row[1] for row in data))
    last_line = max((row[0] for row in data), default=0)

    conn.close()

    return render_template(
        "index.html",
        data=data,
        search=search,
        total_records=total_records,
        total_variables=total_variables,
        last_line=last_line,
        code=code
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    subprocess.run(
        ["python", "tracer.py", filepath],
        check=True
    )

    return redirect("/")


@app.route("/download")
def download():

    conn = sqlite3.connect("trace.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT line_number, variable_name, value
        FROM variables
    """)

    data = cursor.fetchall()

    conn.close()

    with open("trace_report.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)
        writer.writerow(["Line Number", "Variable", "Value"])
        writer.writerows(data)

    return send_file(
        "trace_report.csv",
        as_attachment=True
    )
@app.route("/clear")
def clear():

    conn = sqlite3.connect("trace.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM variables")

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)