from typing import List
from sentence_transformers import SentenceTransformer

import chromadb


# 分片方法
def split_into_chunks(doc_file: str) -> List[str]:
    with open(doc_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return [chunk for chunk in content.split("\n\n")]


chunks = split_into_chunks("./zuowu.txt")

# 导入emdding模型
embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")


# 片段向量转化方法
def embed_chunk(chunk: str) -> List[float]:
    embedding = embedding_model.encode(chunk)
    return embedding.tolist()


embeddings = [embed_chunk(chunk) for chunk in chunks]

# 建立向量知识库
chromadb_client = chromadb.PersistentClient("zuowu.db")
# 在chromadb中创建collection表
chromadb_collection = chromadb_client.get_or_create_collection(name="default")


# 1次性创建本地向量数据库
def save_embeddings(chunks: List[str], embeddings: List[List[float]]) -> None:
    ids = [str(i) for i in range(len(chunks))]
    chromadb_collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )


save_embeddings(chunks, embeddings)
