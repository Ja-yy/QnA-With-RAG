import streamlit as st
from langchain.schema import ChatMessage

from src.agents.main_agent import MainAgent
from src.bot_stream_llm import StreamChatOpenAI
from src.chroma_client import BaseChroma

st.title("Chat Interface")
st.divider()
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="How can I help you?")
    ]
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = None

col1, col2 = st.columns([2, 1])

if st.session_state.openai_api_key is None:
    st.warning("Please enter your OpenAI API key on main page!!!")
else:
    chroma_db = BaseChroma()
    with col1:
        know = st.selectbox(
            "select knowledge to chat",
            options=list(chroma_db.get_knowledge_base_list()),
        )

    st.divider()

    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)

    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            streaming_llm = StreamChatOpenAI(st.empty())
            main_agent = MainAgent(streaming_llm, know)
            response = main_agent.run(question=prompt)
            if response:
                st.session_state.messages.append(
                    ChatMessage(role="assistant", content=response)
                )
