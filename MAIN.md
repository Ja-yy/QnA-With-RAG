# Q&A with Documents using RAG

Welcome to our Streamlit application designed for Q&A with documents powered by RAG (Retriever-Reader-Generator).

This full-stack application enables you to transform any text document or piece of content into contextual references that any language model can utilize during conversations. With this application, you can seamlessly add and delete documents and even create multiple knowledge bases to organize your information effectively.

### Powered by

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Langchain](https://img.shields.io/badge/%F0%9F%A6%9C%EF%B8%8F%F0%9F%94%97%20LangChain-black?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-black?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

### Key Features

- Chat with text documents
- Real-time chat streaming
- Upload multiple text files simultaneously
- Maintainable vector database (add and delete files)
- Static API Token Authentication for ChromaDB
- Create and manage multiple knowledge bases

### How to Use?

1. **Set Up Your OpenAI API Key**: Past your OpenAI API key in the designated section in the sidebar. It's crucial for accessing OpenAI's language models. Please note that the application does not store this key anywhere else and solely uses it for calling APIs.
2. **Prepare Your Knowledge**: Compile your knowledge into text files.
3. **Create a Knowledge Base**: Use the "Uploader" page to create a new knowledge base with an appropriate name.
4. **Upload Your Knowledge**: Add your text files containing knowledge to the newly created knowledge base.
5. **Access the Chat Interface**: Navigate to the "Chat Interface" page.
6. **Select Your Knowledge Base**: Choose the desired knowledge base you created earlier.
7. **Start Chatting**: Initiate conversations and interact with the system using the selected knowledge base.

#### Want to Run Locally?

- Follow the instructions outlined on [GitHub](https://github.com/Ja-yy/QnA-With-RAG).

**NOTE:** The current knowledge base will persist even after refreshing or closing the window. Remember to delete your data before leaving the page. Happy chatting!
