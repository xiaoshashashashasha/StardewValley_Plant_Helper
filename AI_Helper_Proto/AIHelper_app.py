import os
import tools
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


# ---函数调用---
def call_tool(tool_call):
    function_name = tool_call.name
    args = {k: v for k, v in tool_call.args.items()}

    # 函数名到实际函数的映射
    available_functions = {
        "get_crops_by_sellprice": tools.get_crops_by_sellprice,
        "get_crops_by_dailyrevenue": tools.get_crops_by_dailyrevenue,
        "get_crops_by_seedprice": tools.get_crops_by_seedprice,
        "get_crops_by_growtime": tools.get_crops_by_growtime,
    }

    if function_name in available_functions:
        return available_functions[function_name](**args)


# ---回答方法---
def generate_answer(query: str):
    prompt = f"""你是一位星露谷农作物种植助手，请根据用户问题和提供片段中的有用信息生成准确回答。回答格式请尽量简洁，美观。
    不要编造信息，请从工具库中选择合适的工具来获取信息。若无需其他信息，则直接回答。若所获信息无法解决问题，则直接说明无法解决。"""

    # 构造第一轮消息
    messages = [
        {"role": "user", "parts": [{"text": prompt}]},
        {"role": "user", "parts": [{"text": f"用户问题: {query}\n\n"}]}
    ]

    # 获取响应
    model = genai.GenerativeModel("gemini-2.5-flash", tools=tools.TOOLS_LIST)
    response = model.generate_content(messages)

    # 检查响应是否包含函数调用
    try:
        tool_call = response.candidates[0].content.parts[0].function_call

        # 若为函数调用
        if tool_call:
            print("get function calling\n")

            # 若为RAG检索请求
            if tool_call.name == "RAGCalling":
                print("RAG Search\n")

                # 执行召回、重排过程
                retrieved_chunks = retrieve_and_rerank(user_query)
                messages.append({"role": "user", "parts": [{"text": f"可用片段如下:{retrieved_chunks}"}]})

                print("生成回答，相关分片为:\n")
                i = 0
                for chunk in retrieved_chunks:
                    print(f"分片{i}:{chunk}\n")
                    i += 1

                # 根据RAG片段生成最终回答
                final_response = model.generate_content(messages)
                return final_response.text

            # 若为正常函数调用
            else:
                print("Function Search\n")

                # 执行函数并获取结果
                tool_output = call_tool(tool_call)

                # 构造函数响应消息格式
                function_response_part = {
                    "function_response": {
                        "name": tool_call.name,
                        "response": {
                            "content": tool_output
                        }
                    }
                }
                messages.append({"role": "function", "parts": [function_response_part]})

                # 将函数结果传给模型生成最终回答
                final_response = model.generate_content(messages)
                return final_response.text

        # 若无需额外信息来源
        else:
            # 直接返回回答
            print(response.text)
            return response.text
    except (AttributeError, IndexError):
        if response.text:
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
col1, col2 = st.columns([4,1])
with col1:
    st.markdown("输入你的农作物相关问题，我将根据本地知识库为你提供准确的攻略信息。")

with col2:
    # 添加清空历史的按钮
    if st.button("清空历史消息"):
        st.session_state.messages = []
        save_chat_history([])
        st.rerun()

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

# 监听用户输入
if user_query := st.chat_input("在这里输入你的问题..."):
    # 在会话中添加新用户消息
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 渲染新用户消息
    with st.chat_message("user"):
        st.markdown(user_query)

    # 渲染助手消息
    with st.chat_message("assistant"):
        with st.spinner("正在搜索和生成回答..."):
            # 调用回答方法
            answer = generate_answer(user_query)

            # 将回答保存到会话
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

            # 立即保存
            save_chat_history(st.session_state.messages)

        st.rerun()

