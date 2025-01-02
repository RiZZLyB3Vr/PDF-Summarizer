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

def process_text(text):
    # split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # Use BGE embeddings (free and high quality)
    model_name = "BAAI/bge-small-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    
    return knowledge_base

def summarizer(pdf):
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        knowledge_base = process_text(text)
        
        query = "Summarize the contents of the PDF file in approximately 5-10 sentences"
        
        if query:
            docs = knowledge_base.similarity_search(query)
            
            llm = ChatGroq(
                api_key="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",
                model_name="mixtral-8x7b-32768",
                temperature=0.8
            )
            
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=query)
            
            return response