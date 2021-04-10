from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from flask import Flask, request, Response, redirect, url_for, jsonify


app = Flask(__name__)

@app.route("/create_user", methods=["POST"])
def create_user():

    print(request.form['user'])
    return jsonify("{'test': 'this is test data'}")

def login():

    return jsonify("    ")

if __name__ == '__main__':
    app.run(debug=True)

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
