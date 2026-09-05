import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as s

app = Flask(__name__)

def init_db():
    conn = s.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            Sno. INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])

def index():
    conn = s.connect("notes.db")
    c = conn.cursor()

    if request.method == "POST":
        note = request.form["note"]
        if note.strip():
            c.execute("INSERT INTO notes (content) VALUES (?)", (note,))
            conn.commit()

    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()

    return render_template("index.html", notes=notes)

@app.route("/delete/<int:note_id>")
def delete(note_id):
    conn = s.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=False)
