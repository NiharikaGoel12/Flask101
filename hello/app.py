from flask import Flask, redirect, render_template, request
import os

import sqlite3
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.getcwd())
db_path = os.path.join(BASE_DIR, "registration.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE student_activity
             ("id"	INTEGER,
	        "name"	TEXT NOT NULL,
	        "sport"	TEXT NOT NULL,
	        PRIMARY KEY("id" AUTOINCREMENT))''')
conn.commit()

SPORTS = ["TT", "CRICKET", "BASEBALL", "FOOSEBALL", "BADMINTON"]

@app.route("/")
def index():
    return render_template("index.html", sports_list= SPORTS)

@app.route("/deregister", methods = ["POST"])
def deregister():
    id = request.form.get("id")
    c.execute("DELETE from student_activity where id = ?", id)
    return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    if not name:
        return render_template("failure.html")

    sport_name = request.form.get("sport")
    if sport_name not in SPORTS:
        return render_template("failure.html")

    c.execute("INSERT INTO student_activity (name, sport) VALUES (?, ?) ", (name, sport_name))
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    result_cursor = c.execute("SELECT * from student_activity")
    registrants = result_cursor.fetchall()
    return render_template("registrants.html", registrants=registrants)


