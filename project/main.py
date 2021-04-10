from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from flask import Blueprint, request, Response, redirect, url_for, jsonify

main = Blueprint('main', __name__)

@main.route("/create_user", methods=["POST"])
def create_user():

    user = request.form['user']
    pwd = request.form['pass']

    # Code to add user to database

    return jsonify("{'test': 'this is test data'}")


@main.route("/login", methods=["POST"])
def login():

    user =  request.form['user']
    pwd = request.form['pass']

    # Check if user exists in db
    # hash(pwd) and check against stored in db
    good = True
    if good:
        pass
        
    return jsonify("    ")

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
