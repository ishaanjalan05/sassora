import os
from flask import Flask, redirect, render_template, request, session
import sqlite3
from flask_session import Session
from flask_mail import Mail, Message
from helpers import login_required,apology
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['MAIL_USERNAME']= "lallupallu78@gmail.com"
app.config["MAIL_DEFAULT_SENDER"] = "lallupallu78@gmail.com"
app.config["MAIL_PASSWORD"] = "ishaanvi28"
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
mail = Mail(app)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

conn = sqlite3.connect('/home/sassora/mysite/final.db')
db = conn.cursor()
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else :
        l = []
        e = []
        for row in db.execute("SELECT * FROM users"):
            l.append(row[2])
            e.append(row[3])
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if request.form.get("username") in l :
            return apology("username already exists", 400)
        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match ", 400)
        if not request.form.get("email") :
            return apology("must provide email", 400)
        if request.form.get("email") in e :
            return apology("email already exists", 400)
        db.execute("INSERT INTO users (username,hash,email) VALUES (?,?,?)", (request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8),request.form.get("email")))
        return redirect("/login")

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
        db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = db.fetchall()
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

@app.route("/shop", methods =["GET", "POST"] )
@login_required
def shop():
    if request.method == "GET" :
        return render_template("shop.html")
    else:
        i = request.form.get("id")
        db.execute("SELECT * FROM products where id = ?", i)
        rows = db.fetchall()
        product = rows[0][1]
        db.execute("SELECT * FROM cart where product =  ? and user_id = ?" , (product, str(session["user_id"])) )
        cart = db.fetchall()
        if len(cart) == 0 :
            quantity = 1
            subtotal = rows[0][2]
            db.execute("INSERT INTO cart (user_id,product,price,quantity,subtotal,product_id) VALUES (?,?,?,?,?,?)", (str(session["user_id"]), product, rows[0][2], quantity ,subtotal,i))
        else :
            quantity = cart[0][3] + 1
            subtotal = quantity * rows[0][2]
            db.execute("UPDATE cart SET quantity = ?, subtotal = ? WHERE  product =  ? and user_id = ?" , (quantity , subtotal , product, str(session["user_id"])) )
        db.execute("SELECT * FROM cart where user_id = ?" , str(session["user_id"]))
        row = db.fetchall()
        total = 0
        for r in row :
            total = total + r[4]
        return render_template("cart.html" , row = row , total = total )

@app.route("/cart")
@login_required
def cart():
        db.execute("SELECT * FROM cart where user_id = ?" , str(session["user_id"]) )
        row = db.fetchall()
        total = 0
        for r in row :
            total = total + r[4]
        return render_template("cart.html" , row = row , total = total )

@app.route("/checkout",methods =["POST"])
@login_required
def checkout():
    if request.method == "POST":
        return render_template("checkout.html")

@app.route("/success", methods = ["POST"])
@login_required
def success():

    db.execute("SELECT * from users where id = ?", str(session["user_id"]) )
    rows = db.fetchall()
    email = rows[0][3]
    message = Message(subject = "Sassora order confirmation ", body = "Your order has been placed ", recipients=[email])
    mail.send(message)
    return ("Your order has been placed ")

@app.route("/edit",methods = ["POST"])
@login_required
def edit():

   if request.form.get("plus"):
       product_id = request.form.get("plus")
       db.execute('SELECT * FROM cart where product_id = ? and user_id = ?' , (product_id , str(session["user_id"])))
       row = db.fetchall()
       quantity = row[0][3] + 1
       subtotal = quantity * row[0][2]
       db.execute("UPDATE cart SET quantity = ?, subtotal = ? WHERE  product_id =  ? and user_id = ?" , ( quantity , subtotal , product_id, str(session["user_id"])))

   else :
       product_id = request.form.get("minus")
       db.execute('SELECT * FROM cart where product_id = ? and user_id = ?' , (product_id , str(session["user_id"])))
       row = db.fetchall()
       quantity = row[0][3] - 1
       subtotal = quantity * row[0][2]
       db.execute("UPDATE cart SET quantity = ?, subtotal = ? WHERE  product_id =  ? and user_id = ?" , ( quantity , subtotal , product_id, str(session["user_id"])))
       if quantity == 0 :
           db.execute("DELETE from cart where user_id = ? and product_id = ? ", (str(session["user_id"])  , product_id ))
   return redirect("/cart")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

