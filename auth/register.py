from flask import request, redirect, render_template, flash
from database.models import db, User
from auth.crypto import hash_password, is_strong_password


def register_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        # Password strength
        if not is_strong_password(password):

            flash(
                "Weak password ❌ Use uppercase, number & special char",
                "error"
            )
            return redirect("/register")


        # Existing user
        existing = User.query.filter_by(username=username).first()

        if existing:

            flash("Username already exists ❌", "error")
            return redirect("/register")


        hashed = hash_password(password)

        user = User(
            username=username,
            password=hashed.decode()
        )

        db.session.add(user)
        db.session.commit()


        flash("Registration successful ✅ Please login", "success")

        return redirect("/")


    return render_template("register.html")