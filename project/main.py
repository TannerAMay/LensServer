from flask import Blueprint, Flask, request, Response, redirect, url_for, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import db

main = Blueprint('main', __name__)

@main.route("/create_user", methods=["POST"])
def create_user():

    if db.create_user(request.form['user'], request.form['pass']):
        return jsonify("{'Success': 'The user was added to core.user.'")

    return jsonify("{'Failure': 'The user was not added to core.user.'")


@main.route("/login", methods=["POST"])
def login():

    if db.login(request.form['user'], request.form['pass']):
        return jsonify("{'Success': 'The user is logged in.'")

    return jsonify("{'Failure': 'The user was not logged in.'")


