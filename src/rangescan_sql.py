from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from datetime import timedelta

# Couchbase 클러스터 연결 설정
cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('Administrator', 'password')
))
cluster.wait_until_ready(timedelta(seconds=10))

bucket = cluster.bucket('travel-sample')
collection = bucket.default_collection()

# N1QL 쿼리를 사용하여 키 범위 검색
start_key = "hotel_00001"
end_key = "hotel_20000"

query = f"""
SELECT META().id, title, name, city, country, type
FROM `travel-sample`
WHERE META().id BETWEEN '{start_key}' AND '{end_key}'
"""

try:
    # 쿼리 실행 및 결과 처리
    result = cluster.query(query)
    count = 0

    for row in result:
        print("Document ID:", row['id'])
        print("Document Content:", row)
        count += 1

    print("Total number of documents scanned:", count)

except Exception as e:
    print("Error during range scan:", e)
