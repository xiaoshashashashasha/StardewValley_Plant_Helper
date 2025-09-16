import os
import time
import chromadb
import json
import google.generativeai as genai
import streamlit as st

from typing import List
from sentence_transformers import CrossEncoder
from sentence_transformers import SentenceTransformer

# ---配置加载模型和数据库---
# 配置GeminiAPIKey
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)


# 配置加载Embedding和Cross-Encoder模型
@st.cache_resource
def load_models():
    embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    return embedding_model, cross_encoder


# 连接向量数据库
@st.cache_resource
def load_chromadb():
    chromadb_client = chromadb.PersistentClient("zuowu.db")
    return chromadb_client.get_or_create_collection(name="default")


# ---召回和重排方法---
def retrieve_and_rerank(query: str, top_k1=10, top_k2=4):
    # 获取提问向量值
    query_embedding = embedding.encode(query).tolist()

    # 召回过程，粗略进行数据库向量匹配
    retrieved_info = chromadb_collection.query(query_embeddings=query_embedding, n_results=top_k1)
    retrieved = retrieved_info['documents'][0]

    # 重排过程，对召回片段逐一进行比较打分
    pairs = [(query, chunk) for chunk in retrieved]
    scores = cross_encoder.predict(pairs)

    chunk_with_scores = [(chunk, score) for chunk, score in zip(retrieved, scores)]
    chunk_with_scores.sort(key=lambda pair: pair[1], reverse=True)

    return [chunk for chunk, _ in chunk_with_scores[:top_k2]]


# ---回答方法---
def generate_answer(query: str, chunks: List[str]):
    prompt = f"""你是一位星露谷农作物种植助手，请根据用户问题和下列片段中的有用信息生成准确回答。

    用户问题:{query}

    相关片段:
    {"\n\n".join(chunks)}

    请基于以上内容作答，不要编造信息。"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text


# ---消息持久化---
CHAT_HISTORY = "chat_history.json"


# 历史消息加载方法
def load_chat_history():
    if os.path.exists(CHAT_HISTORY):
        with open(CHAT_HISTORY, "r") as file:
            return json.load(file)
    return []


# 历史消息保存方法
def save_chat_history(messages):
    with open(CHAT_HISTORY, "w") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)


# ---UI界面---
st.set_page_config(page_title="星露谷物语小助手", page_icon="🌱")
st.title("🌱星露谷物语农作物小助手")
st.markdown("输入你的农作物相关问题，我将根据本地知识库为你提供准确的攻略信息。")

# 初始化模型并连接知识库
with st.spinner("正在加载Embedding和Cross-Encoder模型..."):
    embedding, cross_encoder = load_models()

with st.spinner("正在连接知识库..."):
    chromadb_collection = load_chromadb()

# ---页面会话逻辑---
# 初始化会话状态中的聊天记录
if "messages" not in st.session_state:
    with st.spinner("正在加载历史消息..."):
        st.session_state.messages = load_chat_history()

# 遍历并显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # 显示回答所用分片
        if message["role"] == "assistant" and "chunks" in message:
            with st.expander("查看用于生成答案的上下文"):
                for i, chunk in enumerate(message["chunks"]):
                    st.write(f"**分片 {i + 1}:**")
                    st.write(chunk)

# 监听用户输入
if user_query := st.chat_input("在这里输入你的问题..."):
    # 1. 在会话中添加新用户消息
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. 渲染新用户消息
    with st.chat_message("user"):
        st.markdown(user_query)

    # 3. 渲染助手消息
    with st.chat_message("assistant"):
        with st.spinner("正在搜索和生成回答..."):
            retrieved_chunks = retrieve_and_rerank(user_query)
            answer = generate_answer(user_query, retrieved_chunks)

            # 将回答和分片保存到会话
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "chunks": retrieved_chunks
            })

            # 立即保存
            save_chat_history(st.session_state.messages)

        st.rerun()
