import streamlit as st

from langchain.schema import ChatMessage
from src.bot_stream_llm import StreamChatOpenAI
from src.agents.main_agent import MainAgent
from src.chroma_client import chroma_db


st.title("Chat Interface")
st.divider()
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="How can I help you?")
    ]
col1, col2 = st.columns([2, 1])
with col1:
    know = st.selectbox("select knowledge to chat", options=list(
        chroma_db.get_knowledge_base_list()))


st.divider()

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(
        ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        streaming_llm = StreamChatOpenAI(st.empty())
        main_agent = MainAgent(streaming_llm, know)
        response = main_agent.run(question=prompt)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response)
        )
