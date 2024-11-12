from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, QueryOptions, UpsertOptions
from couchbase.auth import PasswordAuthenticator
import couchbase.subdocument as SD
from couchbase.exceptions import CouchbaseException, DocumentExistsException, DocumentNotFoundException, PathExistsException

cluster = Cluster.connect( "couchbase://localhost",
    ClusterOptions(PasswordAuthenticator("Administrator", "password")))
bucket = cluster.bucket("travel-sample")
collection = bucket.scope("inventory").collection("subdoc")

result = collection.lookup_in('customer123', [SD.get('addresses.delivery.country')])
country = result.content_as[str](0)  # 'United Kingdom'
print(f'country : {country}')

result = collection.lookup_in('customer123', [SD.exists('purchases.pending[-1]')])
print(f'Path exists: {result.exists(0)}.')
# Path exists:  False.

result = collection.lookup_in('customer123',[SD.get('addresses.delivery.country'), SD.exists('purchases.complete[-1]')])
print('{0}'.format(result.content_as[str](0)))
print('Path exists: {}.'.format(result.exists(1)))
# path exists: True.

collection.mutate_in('customer123', [SD.upsert('fax','311-555-0151')])

collection.mutate_in('customer123', [SD.insert('purchases.pending', [42, True, 'None'])])

try:
    collection.mutate_in('customer123', [SD.insert('purchases.complete',[42, True, 'None'])])
except PathExistsException:
    print('Path exists, cannot use insert.')

collection.mutate_in('customer123',(SD.remove('addresses.billing'),
                                    SD.replace('email','dougr96@hotmail.com')))
