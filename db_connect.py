from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from keys import PATH_TO_ZIP, ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET

def gen_session():
    CLOUD_CONFIG = {'secure_connect_bundle': PATH_TO_ZIP}
    AUTH_PROVIDER = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)

    CLUSTER = Cluster(cloud=CLOUD_CONFIG, auth_provider=AUTH_PROVIDER)
    SESSION = CLUSTER.connect()

    return SESSION

