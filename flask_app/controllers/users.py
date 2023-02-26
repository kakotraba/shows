from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models import show
from flask import flash



#####################################
#
#   @app.routes
#
#####################################


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/users/register", methods=["POST"])
def register():
    valid_user = User.create_valid_user(request.form)
    if not valid_user:
        print("   *!*!*!*!*!*!*   REGISTRATION FAILED   *!*!*!*!*!*!*   ")
        return redirect("/")
    session["user_id"] = valid_user.id
    print("   *$*$*$*$*$*$*   USER SUCCESSFULLY REGISTERED   *$*$*$*$*$*$*   ")
    print(session['user_id'])
    return redirect("/shows/list")


@app.route("/users/login", methods=["POST"])
def login():
    valid_user = User.authenticated_user_by_input(request.form)
    if not valid_user:
        print("   *!*!*!*!*!*!*   LOGIN FAILED   *!*!*!*!*!*!*   ")
        return redirect("/")
    session["user_id"] = valid_user.id
    print("   *$*$*$*$*$*$*   USER SUCCESSFULLY LOGGED IN   *$*$*$*$*$*$*   ")
    print(session['user_id'])
    return redirect("/shows/list")


@app.route("/users/logout")
def logout():
    print(session['user_id'])
    session.clear()
    if 'user_id' not in session:
        print("   @!@!@!@!@!@!@   SESSION CLEAR - USER LOGGED OUT   @!@!@!@!@!@!@   ")
    return redirect("/")