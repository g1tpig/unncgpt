from pymilvus import Collection, connections
from encoder import Encoder
from Search import SearchEngine
import numpy as np
from keywordLLM import KeywordExtractor

TOPK = 5


def combineVectors(k_norm, s_norm, alpha):
    def L2Norm(vector):
        return np.linalg.norm(vector, ord=2, axis=0, keepdims=True)
    combined = np.divide(k_norm, L2Norm(k_norm)) + alpha * np.divide(s_norm, L2Norm(s_norm))
    return combined.tolist()

def getReference(question):
    connections.connect(
        alias='default', 
        uri='https://in01-ac3f552a832e63b.aws-us-west-2.vectordb.zillizcloud.com:19533',
        secure=True,
        token='db_admin:Jhl030108', 
    )

    collection = Collection("Nottingham")      
    collection.load()




    # 生成关键词
    kwd_extractor = KeywordExtractor()
    keywords = kwd_extractor.HanLP(question)
    print(keywords)

    # 过滤停用词、介词...




    # 编码问题、关键词
    encoder = Encoder()
    query_embedding = encoder.encode(question)
    kwd_embeddings = encoder.encode(keywords)
    # 结合问题、关键词
    combined_embeddings = []
    for kwd_embedding in kwd_embeddings:
        combined_embeddings.append(combineVectors(kwd_embedding, query_embedding, 1))
    # 计算相似度得分
    search_engine = SearchEngine()
    num_of_rows = search_engine.NumberOfRows()

    score_dict = {row_id: 0 for row_id in range(1, num_of_rows + 1)}
    search_list = search_engine.bulkSearch(query=combined_embeddings, limit=10)

    for sublist in search_list:
        for item in sublist:
            score_dict[item['id']] += item['distance']

    # 取前topk条数据输出
    sorted_list = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    k_sorted_list = sorted_list[:TOPK]
    i_d_list = [(k_sorted_list[i])[0] for i in range(TOPK)]
    rows_of_ids = collection.query(
        expr = f"id in {i_d_list}",
        offset = 0,
        limit = TOPK, 
        output_fields = ["content"],
    )
    
    reference = ""
    for i, row in enumerate(rows_of_ids):
        content_of_row = row['content']
        reference.join(f"({i}){content_of_row}\n")

    return reference

    
