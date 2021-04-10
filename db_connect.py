from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

CLOUD_CONFIG = {'secure_connect_bundle': '<<PATH TO ZIP>>/secure-connect-p2021.zip'}
AUTH_PROVIDER = PlainTextAuthProvider('<<CLIENT ID>>',
                                          '<<CLIENT SECRET')

CLUSTER = Cluster(cloud=CLOUD_CONFIG, auth_provider=AUTH_PROVIDER)
SESSION = CLUSTER.connect()
