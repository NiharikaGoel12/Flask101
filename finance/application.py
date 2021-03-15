import os

from cs50 import SQL
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
BASE_DIR = os.path.abspath(os.getcwd())
db_path = os.path.join(BASE_DIR, "finance.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
db_cursor = conn.cursor()
# db = SQL("sqlite:///finance.db")

# db_cursor.execute('''CREATE TABLE if not exists purchase
#              ("id"	INTEGER,
# 	        "symbol"	TEXT NOT NULL,
# 	        "name"	TEXT NOT NULL,
# 	        "qty" INT NOT NULL,
# 	        "purc_time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	        "price" FLOAT NOT NULL,
# 	        "amount" FLOAT NOT NULL)''')
# conn.commit()


# Make sure API key is set
if not os.environ.get("IEX_API_KEY"):
    raise RuntimeError("IEX_API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    rows = db_cursor.execute("SELECT * FROM purchase WHERE id = ?", [user_id])
    current_users = rows.fetchall()
    row_user = db_cursor.execute("SELECT * FROM users WHERE id = ?", [user_id])
    user_cash = row_user.fetchall()
    data = [current_users, user_cash]
    json_data = {
        "user" : user_cash[0],
        "purchases": current_users
    }

    return render_template("index.html",data = json_data )

    # len_user = len(user_info)
    # total_amount = 0
    # for each_stock in range(0, len_user):
    #     stock_id = user_info[each_stock][1]
    #     stock_name = user_info[each_stock][2]
    #     qty = user_info[each_stock][3]
    #     purc_time = user_info[each_stock][4]
    #     stock_price = user_info[each_stock][5]
    #     amount= user_info[each_stock][6]
    #     total_amount += amount
    #
    # balance_amount = total_amount - row_info[0][3]
    # grand_total = balance_amount + total_amount


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        stocks = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        if not request.form.get("symbol"):
            return apology("Enter stock symbol", 403)
        elif stocks < 0:
            return apology("Incorrect shares qty", 403)

        stock_symbol = lookup(symbol)
        if stock_symbol["symbol"] is None:
            return apology("Symbol does not exist", 403)

        stock_price = stock_symbol["price"]
        user_id = session["user_id"]
        rows = db_cursor.execute("SELECT * FROM users WHERE id = ?", [user_id])
        user_info = rows.fetchall()
        if (user_info[0][3] < stock_price * stocks):
            return apology("Insufficient balance", 403)
        else:
            amount = (stock_price * stocks)
            db_cursor.execute("INSERT INTO purchase (id, symbol, name, qty, price, amount) VALUES (?,?,?,?,?,?)",
                              (user_id,symbol, stock_symbol["name"],stocks,stock_price, amount))
            conn.commit()
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = request.form.get("username")
        rows_cursor = db_cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
        rows = rows_cursor.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        user = request.form.get("username")
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password mismatch", 403)

        rows = db_cursor.execute("SELECT * FROM users WHERE username = ?", [user])
        user_info = rows.fetchall()
        print("rows value currently", user_info)
        if len(user_info) !=0:
            return apology("username already exists", 403)

        pass_hash = generate_password_hash(request.form.get("password"))
        db_cursor.execute("INSERT INTO users (username, hash) VALUES (?,?)", (user, pass_hash))
        conn.commit()
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

app.run(debug=True)