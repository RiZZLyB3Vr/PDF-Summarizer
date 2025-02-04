from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
import os

load_dotenv()

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    return FAISS.from_texts(chunks, embeddings)

def create_knowledge_base(pdf):
    """Extracts text from PDF and builds a FAISS knowledge base."""
    pdf_reader = PdfReader(pdf)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages])
    if not text.strip():
        raise ValueError("Error: PDF contains no extractable text")
    return process_text(text)

def generate_summary(knowledge_base):
    """Uses the knowledge base to generate a summary."""
    # Retrieve relevant chunks for summarization
    docs = knowledge_base.similarity_search(
        "Provide a concise summary in 5-10 sentences of the document below, preserving all key technical details"
    )
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.3
    )
    chain = load_qa_chain(llm, chain_type="refine")
    summary = chain.run(
        input_documents=docs,
        question="Provide a concise summary in 5-10 sentences of the document below, preserving all key technical details"
    )
    return summary

def answer_question(knowledge_base, question):
    """Answers a user question based on the knowledge base."""
    docs = knowledge_base.similarity_search(question)
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.3
    )
    chain = load_qa_chain(llm, chain_type="refine")
    return chain.run(input_documents=docs, question=question)
