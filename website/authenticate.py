# Imports modules from packages
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Creates a Blueprint named 'authenticate'
authenticate = Blueprint("authenticate", __name__)
# Route for the login page using GET and POST methods
@authenticate.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            # Checks if the provided password matches the hashed password in the database
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)  # Logs in the user and remembers the session
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)

# Route for the logout functionality (requires login)
@authenticate.route("/logout")
@login_required
def logout():
    logout_user()  # Logs out the current user
    return redirect(url_for("authenticate.login"))

# Route for the sign-up page using GET and POST method
@authenticate.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif password != confirmpassword:
            flash("Passwords don't match.", category="error")
        elif len(password) < 5:
            flash("Password must be at least 5 characters.", category="error")
        else:
            # Creates a new user, hash the password, and add to the database
            new_user = User(email=email, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Logs in the new user after creating
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)