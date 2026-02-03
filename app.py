import os
from flask import Flask, render_template
from database.models import db
from auth.register import register_user

app = Flask(__name__)

# Secret key (later we will move this to env)
app.config["SECRET_KEY"] = "securex-secret-key"

# Cloud-ready DB config
db_url = os.environ.get("DATABASE_URL", "sqlite:///securex.db")

# Fix for Render + Postgres
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return register_user()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)