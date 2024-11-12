from datetime import timedelta

# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

# Update this to your cluster
username = "Administrator"
password = "password"
bucket_name = "travel-sample"
###cert_path = "path/to/certificate"
# User Input ends here.

# Connect options - authentication
auth = PasswordAuthenticator(
    username,
    password,
    # NOTE: If using SSL/TLS, add the certificate path.
    # We strongly reccomend this for production use.
    # cert_path=cert_path
)

# Get a reference to our cluster
# NOTE: For TLS/SSL connection use 'couchbases://<your-ip-address>' instead
cluster = Cluster('couchbase://localhost', ClusterOptions(auth))

# Wait until the cluster is ready for use.
cluster.wait_until_ready(timedelta(seconds=5))

# get a reference to our bucket
cb = cluster.bucket(bucket_name)

cb_coll = cb.scope("inventory").collection("airline")

# Get a reference to the default collection, required for older Couchbase server versions
cb_coll_default = cb.default_collection()

# upsert document function
def upsert_document(doc):
    print("\nUpsert CAS: ")
    try:
        # key will equal: "airline_8091"
        key = doc["type"] + "_" + str(doc["id"])
        result = cb_coll.upsert(key, doc)
        print(result.cas)
    except Exception as e:
        print(e)

# get document function
def get_airline_by_key(key):
    print("\nGet Result: ")
    try:
        result = cb_coll.get(key)
        print(result.content_as[str])
    except Exception as e:
        print(e)

# query for new document by callsign
def lookup_by_callsign(cs):
    print("\nLookup Result: ")
    try:
        sql_query = 'SELECT name FROM `travel-sample`.inventory.airline WHERE callsign = $1'
        row_iter = cluster.query(
            sql_query,
            QueryOptions(positional_parameters=[cs]))
        for row in row_iter:
            print(row)
    except Exception as e:
        print(e)

airline = {
    "type": "airline",
    "id": 8091,
    "callsign": "CBS",
    "iata": None,
    "icao": None,
    "name": "Couchbase Airways",
}

upsert_document(airline)

get_airline_by_key("airline_8091")

lookup_by_callsign("CBS")
