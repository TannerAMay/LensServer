from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from flask import Blueprint, request, Response, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route("/create_user", methods=["POST"])
def create_user():

    user = request.form['user']
    pwd = request.form['pass']

    # Code to add user to database

    return jsonify("{'test': 'this is test data'}")


@main.route("/login", methods=["POST"])
def login():

    user = request.form['user']
    pwd = request.form['pass']
    remember = False

    print(user)
    user_to_test = User()
    user_to_test.username = user
    user_to_test.password = pwd

    # Check if user exists in db
    # hash(pwd) and check against stored in db
    good = True
    
    print("cum:", pwd, pwd == "test")
    if user == "bruhman" and pwd == "test":
        print("/\/\/\/\/\/\/\/\WE GOOD", user_to_test.username)
        login_user(user_to_test, remember=remember)
        
    return redirect(url_for('main.profile'))

@main.route('/profile')
@login_required
def profile():
    print("EMEME")
    return current_user.username

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return "logged out"

# if __name__ == '__main__':
#     app.run(debug=True)

# cloud_config = {
#         'secure_connect_bundle': '<</PATH/TO/>>secure-connect-p2021.zip'
# }
# auth_provider = PlainTextAuthProvider('<<CLIENT ID>>', '<<CLIENT SECRET>>')

# cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
# session = cluster.connect()

# row = session.execute("select * from core.topic").all()
# if row:
#     print(row)
# else:
#     print("An error occurred.")
