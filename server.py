from flask import Flask, request, Response, redirect, url_for, jsonify

import db


app = Flask(__name__)


@app.route("/create_user", methods=["POST"])
def create_user():
    print(request.form['user'])

    if db.create_user(request.form['user'], request.form['pass']):
        return jsonify("{'Success': 'The user was added to core.user.'")

    return jsonify("{'Failure': 'The user was not added to core.user.'")


@app.route("/login", methods=["POST"])
def login():
    if db.login(request.form['user'], request.form['pass']):
        return jsonify("{'Success': 'The user is logged in.'")

    return jsonify("{'Failure': 'The user was not logged in.'")


if __name__ == '__main__':
    app.run(debug=True)
