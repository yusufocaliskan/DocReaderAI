import streamlit as st
from DocReaderAI import DocReaderAI

st.title("Doc Reader")

question = st.sidebar.text_input("Ask a question?")
if question != "":
    print("question", question)
    answer = DocReaderAI.askQuestion(question)
    st.text(answer["text"])
