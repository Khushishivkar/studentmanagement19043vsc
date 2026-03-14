from flask import Flask, render_template, request, redirect, flash
import sqlite3
from datetime import date

app = Flask(**name**)
app.secret_key = "attendance_secret"

def get_db():
conn = sqlite3.connect("attendance.db")
conn.row_factory = sqlite3.Row
return conn

@app.route("/")
def index():
conn = get_db()

```
# student list
students = conn.execute("SELECT * FROM students").fetchall()

# attendance records with student name
attendance = conn.execute("""
SELECT attendance.id,
       students.id AS student_id,
       students.name,
       attendance.status,
       attendance.date
FROM attendance
JOIN students
ON attendance.student_id = students.id
ORDER BY attendance.date DESC
""").fetchall()

conn.close()

return render_template("index.html", students=students, attendance=attendance)
```

@app.route("/add", methods=["POST"])
def add_student():

```
name = request.form.get("name")

if not name or name.strip() == "":
    flash("Student name is required!")
    return redirect("/")

conn = get_db()

conn.execute(
    "INSERT INTO students (name) VALUES (?)",
    (name,)
)

conn.commit()
conn.close()

return redirect("/")
```

@app.route("/mark/[int:id](int:id)/<status>")
def mark_attendance(id, status):

```
today = date.today()

conn = get_db()

conn.execute(
    "INSERT INTO attendance (student_id, status, date) VALUES (?, ?, ?)",
    (id, status, today)
)

conn.commit()
conn.close()

return redirect("/")
```

@app.route("/delete/[int:id](int:id)")
def delete(id):

```
conn = get_db()

# delete attendance records first
conn.execute(
    "DELETE FROM attendance WHERE student_id=?",
    (id,)
)

# delete student
conn.execute(
    "DELETE FROM students WHERE id=?",
    (id,)
)

conn.commit()
conn.close()

return redirect("/")
```

if **name** == "**main**":

```
conn = sqlite3.connect("attendance.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    status TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()

app.run(debug=True)
```
