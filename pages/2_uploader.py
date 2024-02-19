import time

import streamlit as st

from src.chroma_client import BaseChroma
from src.utils import create_chunks

st.title("Knowledge Base")
st.divider()

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = None

left, right = st.columns(2)

if st.session_state.openai_api_key is None:
    st.warning("Please enter your OpenAI API key on main page!!!")

else:
    chroma_db = BaseChroma()
    know_option = list(chroma_db.get_knowledge_base_list())
    with left:
        selected_knowledge = st.selectbox(
            "knowledge Base Names", know_option, index=None
        )
        delete_btn = st.button("🗑️", help="Delete knowledge base")
        if selected_knowledge and delete_btn:
            try:
                chroma_db.delete_knowledge_base(selected_knowledge)
                st.success(f"{selected_knowledge} deleted!!!")
                time.sleep(1.5)
                st.rerun()
            except Exception as e:
                st.warning(f"Something went wrong,Please try again!!")

    with right:
        new_option = st.text_input(
            "Create New knowledge",
            placeholder="Name must be 3-63 character and alphanumeric",
        )
        if st.button("➕", help="Create new knowledge base") and new_option:
            if new_option not in know_option:
                chroma_db._create_collection(new_option)
                time.sleep(1.5)
                st.rerun()

    st.divider()
    left1, right1 = st.columns([2, 1])

    with left1:
        with st.form("file-uploader", clear_on_submit=True):
            doc_up = st.file_uploader(
                label="Upload your files here", accept_multiple_files=True, type=["txt"]
            )
            submitted = st.form_submit_button("Create embeddings")
            if submitted and selected_knowledge and doc_up:
                with st.spinner():
                    chunks = create_chunks(doc_up, selected_knowledge)
                    embeddings = chroma_db.create_embeddings(chunks, selected_knowledge)
            elif selected_knowledge and not submitted:
                st.warning("Upload files to create embeddings")
            elif not selected_knowledge:
                st.warning("No knowledge base selected")
            elif submitted and not doc_up:
                st.warning("Please,upload files to create embeddings")

    st.divider()
    st.subheader("File list")
    left2, right2 = st.columns([2, 1])
    with left2:
        if selected_knowledge:
            try:
                files_list = chroma_db.get_file_names(selected_knowledge)
                file_name_list = list(
                    {item["file_name"] for item in files_list.values()}
                )
                selected_file = st.multiselect(
                    f"Files in {selected_knowledge}", file_name_list
                )
                if selected_file and st.button(
                    "🗑️", help="Delete files from knowledge base"
                ):
                    chroma_db.delete_files_from_knowledge_base(
                        selected_knowledge, selected_file
                    )
                    st.rerun()

            except Exception as e:
                st.warning(f"No Collection found!!! {e}")
        else:
            st.warning("Select knowledge base to get files")
