import streamlit as st

st.set_page_config(layout="wide", page_title='QnA with Douments')


st.title("QnA With your Documents")


col1,col2 = st.columns(2)


with col1:
    with st.form("question_form"):
        input = st.text_input("Ask question to the document")

        submitted = st.form_submit_button("Submit")

        if submitted:
             st.write(input)

with col2:
    data = st.file_uploader("Upload your document",
                        type=['txt'],
                        accept_multiple_files=True)
    

    if data:
        for d in data:
            read_f = d.read()
            st.write(read_f)