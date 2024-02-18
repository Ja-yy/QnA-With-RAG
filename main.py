from pathlib import Path

import streamlit as st

from config import openai_config

intro_message = Path("MAIN.md").read_text()

st.markdown(intro_message, unsafe_allow_html=True)

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = None

with st.sidebar:
    openai_key = st.text_input(label="Enter your OpenAI key here", type="password")
    if openai_key and st.session_state.openai_api_key is None:
        st.session_state["openai_api_key"] = openai_key
        openai_config.OPENAI_API_KEY = openai_key
    elif st.session_state.openai_api_key is None:
        st.warning("Please enter your OpenAI API key!!!")
