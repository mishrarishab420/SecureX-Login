import os
from flask import Flask, render_template
from database.models import db
from auth.register import register_user
from auth.login import login_user
from flask import session, redirect

app = Flask(__name__)

# Secret key (from env for stability on Render)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "securex-secret-key")

# Cloud-ready DB config (Render PostgreSQL + Local SQLite fallback)

db_url = os.environ.get("DATABASE_URL")

if db_url:
    # Fix for Render postgres URL
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    # Local fallback
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/securex.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)



@app.route("/register", methods=["GET", "POST"])
def register():
    return register_user()

@app.route("/", methods=["GET", "POST"])
def login():
    return login_user()

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


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)