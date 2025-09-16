# 星露谷物语 RAG 知识助手

这是一个基于检索增强生成（RAG）技术的交互式聊天助手，能够回答关于星露谷物语农作物的问题。

## 功能

- 本地知识库：使用 ChromaDB 存储攻略信息。
- 智能问答：通过 RAG 架构，提供基于上下文的准确回答。
- 交互式 UI：使用 Streamlit 构建的聊天界面。
- 会话持久化：能够保存和加载历史聊天记录。

## 环境准备

- Python 3.8+

## 安装指南

1.  克隆项目仓库：
    `git clone <你的仓库地址>`

2.  进入项目目录：
    `cd <你的项目文件夹>`

3.  创建并激活虚拟环境：
    `uv venv`
    `.\.venv\Scripts\activate` (Windows) 或 `source .venv/bin/activate` (macOS/Linux)

4.  安装所有依赖：
    `uv pip install -r requirements.txt`

## API 密钥配置

在使用应用前，你需要配置 Gemini API 密钥。

1.  访问 Google AI Studio 获取你的密钥。
2.  在终端中设置环境变量：

    - Windows：
      `set GOOGLE_API_KEY="你的API密钥"`
    - macOS / Linux：
      `export GOOGLE_API_KEY="你的API密钥"`

## 运行应用

在终端中，确保虚拟环境已激活，并运行以下命令：

`streamlit run AIHelper_app.py`

应用将在你的默认浏览器中打开。