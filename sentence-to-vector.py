from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
result = []
contents = []

with open("content/nottingham_cn.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for entry in data:
        if 'title' in entry:
            content = entry["title"] + ": " + entry["content"]
        else:
            content = entry["content"]
        contents.append(content)

print("Begin encoding")
content_embeddings = model.encode(contents)
print("Finish encoding")
for i, content in enumerate(contents):
    item = data[i]
    content_embedding = content_embeddings[i].tolist()
    result.append({"content": content, "vector": content_embedding, "id": item["id"], "title": item["title"], "publish_time": item["publish_time"], "images": item["images"]})
# 处理图片





with open('content/embeddings.json', 'a') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)