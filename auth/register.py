from flask import request, redirect, render_template, flash
from database.models import db, User
from auth.crypto import hash_password, is_strong_password

def register_user():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        # Check password strength
        if not is_strong_password(password):
            return "Weak password ❌ Use uppercase, number & special char"

        # Check existing user
        existing = User.query.filter_by(username=username).first()

        if existing:
            return "Username already exists ❌"

        hashed = hash_password(password)

        user = User(
            username=username,
            password=hashed.decode()
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")