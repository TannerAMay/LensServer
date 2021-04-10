from flask import Blueprint, Flask, request, Response, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user

import db_astra

from .models import User

main = Blueprint('main', __name__)


@main.route("/create_user", methods=["POST"])
def create_user():
    """Add user data to database.

    JSON Expectation:
    {
        'user': '<username>',
        'pass': '<hashed password>',
        'bio': '<bio>'
    }

    Codes: Code-level: 1
        100: User successfully added to both core.userdata and auth.users.
        101: Failed to add to auth.user table.
        102: Failed to add to core.userdata table.

    return: JSON object describing result of command.
    """
    createResult = db_astra.create_user(request.form['user'], request.form['pass'])

    if createResult[0] and createResult[1]:
        return jsonify("{'100': 'Success! The user was added to core.user and auth.user.'")

    if createResult[0]:
        return jsonify("{'101': 'Failure! The user was not added to auth.user.'")

    return jsonify("{'102': 'Failure! The user was not added to core.user.'")


@main.route("/login", methods=["POST"])
def login():
    """Log in a user.

    JSON Expectation:
    {
        'user': '<username>',
        'pass': '<hashed password>'
    }

    Codes: Code-level: 2
        200: User was found in auth.users and successfully logged in.
        201: Failed to find user in user.auth.

    return:  JSON object describing result of command.
    """

    remember = True if request.form.get('remember') else False

    # Checks for valid login
    if db_astra.login(request.form['user'], request.form['pass']):
        user_to_test = User()
        user_to_test.username = request.form['user']
        user_to_test.password = request.form['pass']  # Might not need
        login_user(user_to_test, remember=remember)

        return jsonify("{'200': 'Success! The user is logged in.'")
        #return redirect(url_for('main.profile'))

    return jsonify("{'201': 'Failure! The user was not found in auth.users and could not be logged in.'")
    

@main.route('/profile')
@login_required
def profile():
    return current_user.username


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return "logged out"
