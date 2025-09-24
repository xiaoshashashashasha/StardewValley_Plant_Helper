import os
import chromadb
import google.generativeai as genai

from typing import List
from sentence_transformers import CrossEncoder
from AI_Helper_Proto.setUp import embed_chunk

chromadb_client = chromadb.PersistentClient("AI_Helper_Proto/zuowu.db")

chromadb_collection = chromadb_client.get_or_create_collection(name="default")

# 提问后召回过程
def retrieve(query: str, top_k: int) -> List[str]:
    query_embedding = embed_chunk(query)
    results = chromadb_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

query = "草莓从种植到成熟要几天？"

retrieved_chunks = retrieve(query,5)
print("召回返回：\n")
for i, chunk in enumerate(retrieved_chunks):
    print(f"[{i}] {chunk}\n")



# 提问后重排过程
def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    chunk_with_score_list = [(chunk, score)
                            for chunk, score in zip(retrieved_chunks, scores)]
    chunk_with_score_list.sort(key=lambda pair: pair[1], reverse=True)

    # 仅返回前几个分片
    return [chunk for chunk, _ in chunk_with_score_list][:top_k]

reranked_chunks = rerank(query, retrieved_chunks, 3)

print("重排返回:\n")
for i, chunk in enumerate(reranked_chunks):
    print(f"[{i}] {chunk}\n")



API_KEY = os.environ.get("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

# 回答方法
def generate(query: str, chunks: List[str]) -> str:
    prompt = f"""你是一位知识助手，亲根据用户的问题和下列片段生成准确的回答。

    用户问题:{query}

    相关片段:
    {"\n\n".join(chunks)}

    请基于以上内容作答，不要编造信息。"""


    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text

answer = generate(query, reranked_chunks)
print(answer)