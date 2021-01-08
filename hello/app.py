from flask import Flask, redirect, render_template, request

app = Flask(__name__)

REGISTRANTS = {}
SPORTS = ["TT", "CRICKET", "BASEBALL", "FOOSEBALL", "BADMINTON"]

@app.route("/")
def index():
    return render_template("index.html", sports_list= SPORTS)

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    if not name:
        return render_template("error.html", message ="Missing name")

    sport_name = request.form.get("sport")
    if sport_name not in SPORTS:
        return render_template("error.html", message = "Incorrect sport selected")

    if not sport_name:
        return render_template("error.html", message= "No sport selected")

    REGISTRANTS[name] = sport_name

    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    return render_template("registrants.html", registrants = REGISTRANTS)


