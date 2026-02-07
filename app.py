import os
from flask import Flask, render_template, redirect, session
from database.models import db
from auth.register import register_user
from auth.login import login_user


app = Flask(__name__)


# =========================
# SECRET KEY (for sessions)
# =========================
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "securex-secret-key"
)


# =========================
# DATABASE CONFIG
# =========================

db_url = os.environ.get("DATABASE_URL")

if db_url:

    # Fix Render postgres URL
    if db_url.startswith("postgres://"):
        db_url = db_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

else:
    # Local SQLite fallback
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/securex.db"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize DB
db.init_app(app)


# =========================
# ROUTES
# =========================


# Login Page (Home)
@app.route("/", methods=["GET", "POST"])
def login():

    return login_user()


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():

    return register_user()


# Dashboard (Protected)
@app.route("/dashboard")
def dashboard():

    # If not logged in → redirect to login
    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session.get("username")
    )


# Logout
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# =========================
# CREATE TABLES
# =========================

with app.app_context():
    db.create_all()


# =========================
# RUN APP (LOCAL)
# =========================

if __name__ == "__main__":

    app.run(debug=True)