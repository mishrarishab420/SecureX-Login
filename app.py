import os
from flask import Flask, render_template, redirect, session
from database.models import db
from auth.login import login_user
from auth.register import register_user


app = Flask(__name__)


# Secret Key
app.config["SECRET_KEY"] = "securex-secret-key"


# Database (SQLite Local)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(BASE_DIR, "instance", "securex.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Init DB
db.init_app(app)


# ================= ROUTES =================


@app.route("/", methods=["GET", "POST"])
def login():
    return login_user()


@app.route("/register", methods=["GET", "POST"])
def register():
    return register_user()


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# Create tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)