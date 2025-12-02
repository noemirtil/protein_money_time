from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from app.db.connection import get_db
from app.forms.auth_forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash
from app.models.user import User
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@auth_bp.route("/test")
def test():
    return "<h2>Auth blueprint is working! ✅</h2>"


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    db = get_db()
    cur = db.cursor()

    if form.validate_on_submit():
        try:
            username = form.username.data.strip().lower()
            email = form.email.data.strip().lower()
            # Method for posix systems (without scrypt):
            hashed_password = generate_password_hash(
                form.password.data, method="pbkdf2:sha256"
            )

            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password),
            )
            db.commit()

            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            user_dict = cur.fetchone()

            if user_dict:
                user_obj = User(user_dict)
                login_user(user_obj)
                flash("Welcome! Your account has been successfully created.", "success")
                return redirect(url_for("main.index"))

        except Exception as e:
            db.rollback()
            print(f"❌ ERROR: {e}")
            print(f"Error type: {type(e)}")

            if "unique" in str(e).lower():
                flash("E-mail or username already exists.", "error")
            else:
                flash("E-mail or username already exists.", "error")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    db = get_db()
    cur = db.cursor()

    if form.validate_on_submit():
        username_email = form.username_email.data.strip().lower()
        password = form.password.data

        try:
            cur.execute(
                "SELECT * FROM users WHERE (username=%s or email=%s)",
                (
                    username_email,
                    username_email,
                ),
            )
            user_dict = cur.fetchone()
            if user_dict:
                user_obj = User(user_dict)
                if user_obj.is_password_correct(password):
                    login_user(user_obj)
                    flash(f"Welcome, {user_obj.username}!", "success")
                    return redirect(url_for("main.index"))
                else:
                    flash("Invalid credentials. Try again.", "error")
                    return redirect(url_for("auth.login"))
            else:
                flash("Invalid credentials. Try again.", "error")
                return redirect(url_for("auth.login"))
        except Exception as e:
            print(f"❌ ERROR: {e}")
            print(f"Error type: {type(e)}")

            flash("Error logging in. Try again.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully. See you again soon!.", "success")
    return redirect(url_for("main.index"))


@auth_bp.route("/check-username", methods=["GET", "POST"])
def check_username():

    username = request.args.get("username", "").strip().lower()

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    user = cur.fetchone()

    return jsonify({"available": user is None})


@auth_bp.route("/check-email", methods=["GET", "POST"])
def check_email():

    email = request.args.get("email", "").strip().lower()

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    return jsonify({"available": user is None})
