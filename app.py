from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os
import subprocess
import csv
from datetime import datetime
 

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/")


def index():

    search = request.args.get("search", "")
    code = ""
    filename = ""
    explanation = "Upload a Python file to view AI explanation."

    
    py_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".py")]

    if py_files:
        latest_file = max(
            [os.path.join(UPLOAD_FOLDER, f) for f in py_files],
            key=os.path.getmtime
        )

        filename = os.path.basename(latest_file)

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

    conn.close()

    total_records = len(data)
    total_variables = len(set(row[1] for row in data)) if data else 0
    last_line = max((row[0] for row in data), default=0)
#to add graph labels and values 
    graph_labels = []
    graph_values = []
    for row in data:
        graph_labels.append(row[1])   

    try:
        graph_values.append(float(row[2]))   
    except:
        graph_values.append(0)               

    if code:
        lines = code.split("\n")

        explanation = f"""
🤖 AI Code Summary

📄 File Name : {filename}
📅 Analysis Date : {datetime.now().strftime("%d-%m-%Y %H:%M")}
📏 Total Lines : {len(lines)}
🔢 Variables Found : {total_variables}

✅ Variable tracing completed successfully.
"""

    return render_template(
        "index.html",
        data=data,
        search=search,
        total_records=total_records,
        total_variables=total_variables,
        last_line=last_line,
        code=code,
        explanation=explanation,
        graph_labels=graph_labels,
        graph_values=graph_values
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    import time
    time.sleep(2)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)
    import gc
    gc.collect()

    subprocess.run(["python", "tracer.py", filepath],check=True)

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
    app.run(debug=True,use_reloader=False)