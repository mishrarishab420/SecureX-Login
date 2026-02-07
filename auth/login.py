from flask import request, redirect, render_template, session, flash
from database.models import User, LoginLog, db
from auth.crypto import check_password


def login_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        # User not found
        if not user:

            log = LoginLog(
                user_id=0,
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent"),
                status="failed"
            )

            db.session.add(log)
            db.session.commit()

            flash("User not found ❌", "error")
            return redirect("/")


        # Wrong password
        if not check_password(password, user.password.encode()):

            log = LoginLog(
                user_id=user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent"),
                status="failed"
            )

            db.session.add(log)
            db.session.commit()

            flash("Wrong password ❌", "error")
            return redirect("/")


        # Save login session
        session["user_id"] = user.id
        session["username"] = user.username


        # Log success
        log = LoginLog(
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            status="success"
        )

        db.session.add(log)
        db.session.commit()


        flash("Login successful ✅", "success")
        return redirect("/dashboard")


    return render_template("login.html")