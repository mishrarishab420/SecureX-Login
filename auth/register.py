from flask import request, render_template, redirect, flash
from database.models import User, db
from auth.crypto import hash_password, is_strong_password


def register_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        # Password check
        if not is_strong_password(password):

            flash("Weak password ❌ Use Upper, Number, Special Char")
            return redirect("/register")


        # Check user exists
        existing = User.query.filter_by(
            username=username
        ).first()

        if existing:

            flash("Username already exists ❌")
            return redirect("/register")


        hashed = hash_password(password)


        user = User(
            username=username,
            password=hashed.decode()
        )

        db.session.add(user)
        db.session.commit()


        flash("Registration successful ✅ Login now")

        return redirect("/")


    return render_template("register.html")