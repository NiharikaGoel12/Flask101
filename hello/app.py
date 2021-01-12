import mail as mail
import sys
from flask import Flask, redirect, render_template, request
from flask_mail import Message
from flask_mail_sendgrid import MailSendGrid

import os
import re

import sqlite3
app = Flask(__name__)

app.config['MAIL_SENDGRID_API_KEY'] = os.getenv("MAIL_SENDGRID_API_KEY")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
mail= MailSendGrid(app)

# BASE_DIR = os.path.abspath(os.getcwd())
# db_path = os.path.join(BASE_DIR, "registration.db")
# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute('''CREATE TABLE student_activity
#              ("id"	INTEGER,
# 	        "name"	TEXT NOT NULL,
# 	        "sport"	TEXT NOT NULL,
# 	        PRIMARY KEY("id" AUTOINCREMENT))''')
# conn.commit()

SPORTS = ["TT", "CRICKET", "BASEBALL", "FOOSEBALL", "BADMINTON"]

@app.route("/")
def index():
    return render_template("index.html", sports_list= SPORTS)

# @app.route("/deregister", methods = ["POST"])
# def deregister():
#     id = request.form.get("id")
#     c.execute("DELETE from student_activity where id = ?", id)
#     return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    email = request.form.get("email")
    sport_name = request.form.get("sport")
    if not name or not email or sport_name not in SPORTS:
        return render_template("failure.html")

    message = Message("You are registered", sender=MAIL_DEFAULT_SENDER, recipients= [email])
    content = "Your selected sport <b>{sport_name} </b> is registered!".format(sport_name = sport_name)
    message.body= content
    message.html = content
    try:
        mail.send(message)
    except :
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return render_template("success.html")

    # c.execute("INSERT INTO student_activity (name, sport) VALUES (?, ?) ", (name, sport_name))
    # return redirect("/registrants")


# @app.route("/registrants")
# def registrants():
#     result_cursor = c.execute("SELECT * from student_activity")
#     registrants = result_cursor.fetchall()
#     return render_template("registrants.html", registrants=registrants)


app.run(debug=True)