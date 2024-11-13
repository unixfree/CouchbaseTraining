from datetime import timedelta
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.bucket import Bucket
from couchbase.exceptions import CouchbaseException
from couchbase.kv_range_scan import RangeScan, PrefixScan
import time
import json

def couchbase_range_scan_example():
    # Couchbase 클러스터에 연결
    endpoint = "couchbase://localhost" 
    username = "Administrator" 
    password = "password" 

    auth = PasswordAuthenticator( username, password ) 
    cluster = Cluster(endpoint, ClusterOptions(auth)) 
    cluster.wait_until_ready(timedelta(seconds=10))

    # 버킷 참조 얻기
    bucket = cluster.bucket("travel-sample")
    collection = bucket.scope("inventory").collection("hotel")

    # 범위 스캔 설정 (예: hotel_00001부터 hotel_20000까지)
#    range_scan = RangeScan("hotel_00001", "hotel_20000")
    range_scan = PrefixScan("hotel_100")

    # Range Scan 실행 및 결과 처리
    count = 0
    try:
        # scan() 메서드로 범위 스캔 수행
        for result in collection.scan(range_scan):
            doc_id = result.id
            doc_content = result.content_as[str]
        
            print("Document ID:", doc_id)
            print("Document Content:", doc_content)
        
            count += 1

    except Exception as e:
        print("Error during range scan:", e)

    print("Total number of documents scanned:", count)


# 함수 실행
if __name__ == "__main__":
    couchbase_range_scan_example()
