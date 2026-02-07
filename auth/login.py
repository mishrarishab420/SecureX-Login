from flask import request, render_template, redirect, session, flash
from database.models import User, LoginLog, db
from auth.crypto import check_password


def login_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()


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

            flash("User does not exist ❌")
            return redirect("/")


        # Wrong password
        if not check_password(
            password,
            user.password.encode()
        ):

            log = LoginLog(
                user_id=user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent"),
                status="failed"
            )

            db.session.add(log)
            db.session.commit()

            flash("Wrong password ❌")
            return redirect("/")


        # Login success
        session["user_id"] = user.id
        session["username"] = user.username


        log = LoginLog(
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            status="success"
        )

        db.session.add(log)
        db.session.commit()


        return redirect("/dashboard")


    return render_template("login.html")