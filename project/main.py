from flask import Blueprint, Flask, request, Response, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user

import db_astra

from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route("/create_user", methods=["POST"])
def create_user():

    if db_astra.create_user(request.form['user'], request.form['pass']):
        return jsonify("{'Success': 'The user was added to core.user.'")

    return jsonify("{'Failure': 'The user was not added to core.user.'")


@main.route("/login", methods=["POST"])
def login():

    remember = remember = True if request.form.get('remember') else False

    # Checks for valid login
    if db_astra.login(request.form['user'], request.form['pass']):
        user_to_test = User()
        user_to_test.username = request.form['user']
        user_to_test.password = request.form['pass'] # Might not need
        login_user(user_to_test, remember=remember)

        return jsonify("{'Success': 'The user is logged in.'")
        #return redirect(url_for('main.profile'))

    return jsonify("{'Failure': 'The user was not logged in.'")
    

@main.route('/profile')
@login_required
def profile():
    return current_user.username

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return "logged out"
