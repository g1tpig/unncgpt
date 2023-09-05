from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
from pymilvus import Collection, connections

"""
client = MilvusClient(
            uri="https://in03-1912facb2a3d6d9.api.gcp-us-west1.zillizcloud.com", # Cluster endpoint obtained from the console
            token="ea2b50d3aa8e8e66a03fb19979580b5eefd86ecaab9149ad2b5ce63086bab4ce7bddd5d3b9aa83c3289b906fbeef7c6add811a0c"
        )
"""

client = MilvusClient(
    uri = "https://in01-ac3f552a832e63b.aws-us-west-2.vectordb.zillizcloud.com:19533",
    token = "db_admin:Jhl030108"
)

connections.connect(
  alias='default', 
  #  Public endpoint obtained from Zilliz Cloud
  uri='https://in01-ac3f552a832e63b.aws-us-west-2.vectordb.zillizcloud.com:19533',
  secure=True,
  token='db_admin:Jhl030108', # Username and password specified when you created this cluster
    # Or continue using legacy method `user` and `password` to replace `token`:
    # user='',
    # password='' 
)

class SearchEngine:
    def __init__(self, model_name="distiluse-base-multilingual-cased-v1"):
        self.model_name = model_name
    
    def singleSearch(self, query, limit):
        model = SentenceTransformer(self.model_name)
        vector = model.encode(query)

        res = client.search(
            collection_name="Nottingham",
            data=[vector],
            output_fields=["content"],
            limit=limit
        )
        
        return res
    
    def bulkSearch(self, query, limit=5):   
        res = client.search(
            collection_name="Nottingham",
            data=query,
            output_fields=["content"],
            limit=limit
        )
        
        return res

    def NumberOfRows(self):
        return client.num_entities(collection_name='Nottingham')
    
    def hybridSearch(query, model_name="distiluse-base-multilingual-cased-v1"):
        model = SentenceTransformer(model_name)
        vectors = model.encode(query)
        collection = Collection("Nottingham")      
        collection.load()

        search_param = {
            "data": [vectors.tolist()],
            "anns_field": "vector",
            "param": {"metric_type": "IP", "params": {"nprobe": 10}},
            "limit": 16384,
            "output_fields": ["content"]
        }
        res = collection.search(**search_param)
        return res