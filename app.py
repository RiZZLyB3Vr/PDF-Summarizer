from dotenv import load_dotenv
import streamlit as st
import time
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings  # Changed to BGE embeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
from utils import *
import os

def main():
    st.set_page_config(page_title="PDF Summarizer")
    st.header("Ask About Your PDF 🤷‍♀️💬")
    st.divider()
    
    pdf = st.file_uploader("Upload your PDF File and Ask Questions", type="pdf")
    submit = st.button("Generate Summary")
    
    os.environ["GROQ_API_KEY"] = "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"
    
    if submit:
        response = summarizer(pdf)
        st.subheader("Summary of your file is :")
        st.write(response)

if __name__ == "__main__":
    main()