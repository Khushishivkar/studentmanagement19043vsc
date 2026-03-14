from flask import Flask, render_template, request, redirect, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "attendance_secret"

def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    attendance = conn.execute("SELECT * FROM attendance").fetchall()
    conn.close()
    return render_template("index.html", students=students, attendance=attendance)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name")

    # Validation
    if not name or name.strip() == "":
        flash("Student name is required!")
        return redirect("/")

    conn = get_db()
    conn.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/mark/<int:id>/<status>")
def mark_attendance(id, status):
    today = date.today()

    conn = get_db()
    conn.execute(
        "INSERT INTO attendance (student_id, status, date) VALUES (?, ?, ?)",
        (id, status, today),
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    conn = sqlite3.connect("attendance.db")

    conn.execute(
        "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)"
    )

    conn.execute(
        """CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        status TEXT,
        date TEXT
        )"""
    )

    conn.close()

    app.run(debug=True)
