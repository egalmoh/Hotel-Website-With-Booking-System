import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import login_required, error

# Configure application
app = Flask(__name__)
app.secret_key = os.getenv("SECURITY_KEY")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookings.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """Home page"""

    # POST
    if request.method == "POST":

        # check if the user signed in before booking
        if session.get("user_id") is None:
            flash("Please login first!")
            return redirect("/")

        # geting users checkin time
        checkin = request.form.get("checkin")
        if not checkin:
            return error("Please add checkin date", 403)

        # getting users checkout time
        checkout = request.form.get("checkout")
        if not checkout:
            return error("Please add checkout date", 403)

        # getting how many adults with the user
        adults = request.form.get("adults")
        if not adults:
            return error("Please include number of adults", 403)

        # getting number of rooms the user wants
        rooms = request.form.get("rooms")
        if not rooms:
            return error("Please include number of rooms", 403)

        time = datetime.now()

        db.execute("INSERT INTO reservations (user_id, check_in, check_out, adults, rooms, time) VALUES (?, ?, ?, ?, ?, ?)",
                   session.get("user_id"), checkin, checkout, adults, rooms, time)

        flash("Here are our available rooms!😊")
        return redirect("/rooms")

    # GET
    else:
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""

    # POST
    if request.method == "POST":

        # get the username
        username = request.form.get("username")
        if not username:
            return error("Please provide the username", 403)

        # get the password
        password = request.form.get("password")
        if not password:
            return error("Please provide the password", 403)

        # get the confirmation
        confirmation = request.form.get("confirmation")
        if not confirmation or password != confirmation:
            return error("Password confirmation aren't matching", 403)

        # get the time that the username registered
        time = datetime.now()

        # Check if the username exist
        try:
            hashed_pass = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash, time) VALUES (?, ?, ?)",
                       username, hashed_pass, time)
        except:
            return error("pick another username")

        # Store the new username id into the session
        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ?", username)[0]["id"]

        # redirect to the home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Allow login for the registered users"""

    # POST
    if request.method == "POST":

        # get the username
        username = request.form.get("username")
        if not username:
            return error("Please provide the username", 403)

        # get the password
        password = request.form.get("password")
        if not password:
            return error("Please provide the password", 403)

        # get the current username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # check if the username and password exist
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return error("username and password aren't exist", 403)

        # store the username session
        session["user_id"] = rows[0]["id"]

        # back to home
        return redirect("/")

    # GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out and clear session"""

    # Log out
    session.clear()

    return redirect("/")


@app.route("/rooms", methods=["GET", "POST"])
@login_required
def rooms():
    """Let the user book a room"""

    # POST
    if request.method == 'POST':

        # current user
        c_user = session["user_id"]

        # current user's reservation information
        res_info = db.execute("SELECT * FROM reservations WHERE user_id = ?", c_user)
        if not res_info:
            return error("Please reserve the hotel first")
        for r_info in res_info:
            reservation = r_info

        # getting user's booked room number
        room_no = request.form.get("room_no")
        if not room_no:
            return error("Invalid room number", 403)

        # room's information
        room_info = db.execute("SELECT * FROM rooms WHERE room_no = ?", room_no)
        if not room_info:
            return error("Room doesn't exist or unavailable")

        # current room's price
        room_price = room_info[0]["price"]

        # current user's information
        user_info = db.execute("SELECT * FROM users WHERE id = ?", c_user)
        if not user_info:
            return error("User doesn't exist")

        # book the room if the user haven't booked
        try:
            db.execute("INSERT INTO booked_rooms (user_id, room_no, room_type, price) VALUES (?, ?, ?, ?)",
                       c_user, room_no, room_info[0]["room_type"], room_price)
        except:
            return error("You already booked a room")

        # Setting the current room unavailable
        db.execute("UPDATE rooms SET is_available = ? WHERE room_no = ?", "no", room_no)

        # buying the room and updating user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", int(room_price), c_user)

        current_date = datetime.now().date()

        # Setting the current room available when the date is reached
        if str(reservation["check_out"]) == str(current_date):
            # Update room availability
            db.execute("UPDATE rooms SET is_available = ? WHERE room_no = ?", "yes", room_no)
            # Delete the reservation
            db.execute("DELETE FROM reservations WHERE user_id = ?", c_user)
            # Delete the booked room for the current user when check_out reached
            db.execute("DELETE FROM booked_rooms WHERE user_id = ?", c_user)

        flash("You have successfully booked!")
        return redirect("/rooms")

    # GET
    else:

        # current user
        c_user = session["user_id"]

        # current user's reservation information
        # silent these errors when the user haven't reserved and the user just visits the page
        try:
            reservation = db.execute("SELECT * FROM reservations WHERE user_id = ?", c_user)
        except:
            pass

        current_date = datetime.now().date()

        # Setting the current room available when the date is reached
        # silent these errors when the user haven't reserved and the user just visits the page
        try:
            if str(reservation[0]["check_out"]) == str(current_date):
                # Update room availability
                db.execute("UPDATE rooms SET is_available = ? WHERE room_no = ?", "yes", room_no)
                # Delete the reservation
                db.execute("DELETE FROM reservations WHERE user_id = ?", c_user)
                # Delete the booked room for the current user when check_out reached
                db.execute("DELETE FROM booked_rooms WHERE user_id = ?", c_user)
        except:
            pass

        # get the standard rooms
        standard_room = db.execute("SELECT * FROM rooms WHERE room_type == ?", "Standard Room")

        # get the deluxe rooms
        deluxe_rooms = db.execute("SELECT * FROM rooms WHERE room_type == ?", "Deluxe Room")

        # get suite
        suite = db.execute("SELECT * FROM rooms WHERE room_type == ?", "Suite")

        return render_template("rooms.html", standard=standard_room, deluxe=deluxe_rooms, suite=suite)


@app.route("/about")
def about():
    """Show only the about page"""

    # return only the about page
    return render_template("about.html")


@app.route("/contact")
@login_required
def contact():
    """Show only the contact page"""

    # return only the contact page
    return render_template("contact.html")


@app.route("/reservation")
@login_required
def reservation():
    """User reservations"""

    # show table of the user's reservations
    c_user = session["user_id"]

    reservations = db.execute("SELECT * FROM reservations WHERE user_id = ?", c_user)

    return render_template("reservation.html", reservations=reservations)


@app.route("/gallery")
@login_required
def gallery():
    """Hotel gallery"""

    # return only the gallery page
    return render_template("gallery.html")
