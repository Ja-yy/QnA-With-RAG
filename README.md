# QnA-With-RAG

![python](https://img.shields.io/badge/python-3.10-green)

### Project Description:

A full-stack application that enables you to turn any document or piece of content into context that any LLM can use as references during chatting. This application allows you to add and delete documents and can create multiple knowledge bases.

### Purpose and Achievement:

This project is more than just a chatbot. I want to learn how to code a production-ready chatbot using the OpenAI API. Through my research, I found my way to accomplish this goal. Additionally, I've been learning about VectorDB and Langsmith, which I have extensively incorporated into this project.

### Technologies and Frameworks Utilized

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-black?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Langchain](https://img.shields.io/badge/%F0%9F%A6%9C%EF%B8%8F%F0%9F%94%97%20LangChain-black?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

### Features

- Chat with text files
- Chat <u>streaming</u> 
- Upload <u>multiple</u> Text file
- <u>Maintainable</u> vector DB (add, delete files)
- Static API Token Authentication for ChromaDB
- Create <u>more than one</u> knowledge base

### Future Development and Features

For future development, I would like to use React.js for the frontend and enhance the functionality of ChromDB. This includes features such as filtering data, deleting files through search, and most importantly, adding memory capabilities for the chatbot.

## Run

Clone the repository

```bash
git clone git@github.com:Ja-yy/QnA-With-RAG.git
```

Set up this environment variable in `.env` file

```bash

OPENAI_API_KEY='<open_ai_key>'
EMBEDDING_MODEL='text-embedding-ada-002'
CHAT_MODEL='gpt-3.5-turbo'
TEMPERATURE=0
MAX_RETRIES=2
REQUEST_TIMEOUT=15

CHROMADB_HOST="chromadb"
CHROMADB_PORT="8000"

CHROMA_SERVER_AUTH_CREDENTIALS="<test-token>"
CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER="chromadb.auth.token.TokenConfigServerAuthCredentialsProvider"
CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.token.TokenAuthServerProvider"
CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER="AUTHORIZATION"

```


Build and run docker image

```bash
docker-compose  up -d --build
```

Now, go to [localhost:8501](http://localhost:8501/)

Enjoy the app :) 
