from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = ["TT", "CRICKET", "BASEBALL", "FOOSEBALL", "BADMINTON"]

@app.route("/")
def index():
    return render_template("index.html", sports_list= SPORTS)

@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        # Decline user registration
        return render_template("failure.html")

    # Confirm user registration
    return render_template("success.html")

