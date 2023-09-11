# import boto3
# from elasticsearch import Elasticsearch, RequestsHttpConnection
# from requests_aws4auth import AWS4Auth
# import json
# from elasticsearch.helpers import bulk

# # AWS Credentials and Region
# aws_access_key = 'AKIA2DYBUFSHXLXMLGUX'
# aws_secret_key = 'ecZBSHTyfj5WXH3TJcPmBzkk4ekgwtglaOh+Igd1'
# aws_region = 'us-east-1'  # Change to your region

# # OpenSearch Domain Information
# domain_endpoint = 'https://v74bgsl88xr2s6w46ppe.us-east-1.aoss.amazonaws.com'
# index_name = 'sentencias-index'  # Change to your index name

# # Initialize AWS authentication
# aws_auth = AWS4Auth(aws_access_key, aws_secret_key, aws_region, 'es')

# # Initialize Elasticsearch client
# es = Elasticsearch(
#     hosts=[{'host': domain_endpoint, 'port': 443}],
#     http_auth=aws_auth,
#     use_ssl=True,
#     verify_certs=True,
#     connection_class=RequestsHttpConnection
# )

# # Bulk load documents
# def bulk_load_documents(documents):
#     actions = [
#         {
#             '_op_type': 'index',
#             '_index': index_name,
#             '_source': document
#         }
#         for document in documents
#     ]

#     success, _ = bulk(es, actions=actions)
#     return success

# # Sample documents to bulk load (list of dictionaries)
# sample_documents = [
#     {
#         'id': 1,
#         'title': 'Document 1',
#         'content': 'This is the content of document 1.'
#     },
#     {
#         'id': 2,
#         'title': 'Document 2',
#         'content': 'This is the content of document 2.'
#     }
# ]

# # Bulk load the sample documents
# success_count = bulk_load_documents(sample_documents)

# # Check the number of successfully indexed documents
# print(f"Successfully indexed {success_count} documents.")

import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.helpers import bulk
from requests_aws4auth import AWS4Auth
import boto3


def read_jsonl_file_in_chunks(filename, chunk_size=1000):
    with open(filename, 'r') as jsonl_file:
        chunk = []
        for line in jsonl_file:
            try:
                data = json.loads(line.strip())
                chunk.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line.strip()}")
                continue

            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []

        if chunk:
            yield chunk

    
# https://search-jurisprudencia-e6bo6poynsg5wfdnqggt4xp2uu.us-east-1.es.amazonaws.com/
host = 'search-jurisprudencia-e6bo6poynsg5wfdnqggt4xp2uu.us-east-1.es.amazonaws.com' # e.g. my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Create the client.
client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    http_compress = True, # enables gzip compression for request bodies
    connection_class = RequestsHttpConnection
)

for i, chunk in enumerate(read_jsonl_file_in_chunks('merged_data.jsonl', chunk_size=1000)):
    print(f"Chunk {i + 1}, Number of items: {len(chunk)}")
    response = client.bulk(body=chunk)
    print(response)

# actions = [
#     {"_op_type": "index", "_index": "sentencias-idx", "_id": 1, "_source": {"field1": "value1"}},
#     # {"_op_type": "index", "_index": "test-index", "_id": 2, "_source": {"field1": "value2"}},
#     # {"_op_type": "update", "_index": "test-index", "_id": 1, "doc": {"field1": "updated_value1"}},
#     # {"_op_type": "delete", "_index": "test-index", "_id": 2}
# ]
# Send the request.
# print(search.index(index='sentencias-index', id='2', body=document, refresh=True))
# success, failed = bulk(client, actions)

# print(search.index(index='movies', doc_type='_doc', id='1', body=document, refresh=True))

