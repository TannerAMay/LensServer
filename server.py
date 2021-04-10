from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config = {
        'secure_connect_bundle': '<</PATH/TO/>>secure-connect-p2021.zip'
}
auth_provider = PlainTextAuthProvider('<<CLIENT ID>>', '<<CLIENT SECRET>>')

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select * from core.topic").all()
if row:
    print(row)
else:
    print("An error occurred.")
