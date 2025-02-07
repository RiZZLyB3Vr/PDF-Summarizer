from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
import os
import time

load_dotenv()

def process_text(text):
    # Reduced chunk size and overlap to optimize token usage
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,      # Previously 1000; lower to reduce token count per chunk
        chunk_overlap=100,   # Previously 200; lower to reduce redundancy
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
    pdf_reader = PdfReader(pdf)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages])
    if not text.strip():
        raise ValueError("Error: PDF contains no extractable text")
    return process_text(text)

def call_llm_with_retry(chain, input_documents, question, max_retries=3, initial_wait=5):
    """Call the LLM chain with retry logic for rate limit errors."""
    retry_count = 0
    wait_time = initial_wait
    while retry_count < max_retries:
        try:
            return chain.run(input_documents=input_documents, question=question)
        except Exception as e:
            error_message = str(e)
            # Check for rate limit errors (e.g., code 429 or specific error text)
            if "rate_limit_exceeded" in error_message or "429" in error_message:
                print(f"Rate limit exceeded, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retry_count += 1
                wait_time *= 2  # Exponential backoff
            else:
                raise e
    raise Exception("Max retries exceeded due to rate limit issues")

def generate_summary(knowledge_base):
    # Limit retrieval to a few documents to reduce token usage
    docs = knowledge_base.similarity_search(
        "Summarize in 5-10 concise sentences preserving technical details", k=3
    )
    
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.3  # Lower temperature for more deterministic summarization
    )
    chain = load_qa_chain(llm, chain_type="stuff")
    prompt = "Summarize in 5-10 concise sentences preserving technical details"
    return call_llm_with_retry(chain, docs, prompt)

def answer_question(knowledge_base, question):
    # Retrieve only a few relevant chunks to minimize tokens
    docs = knowledge_base.similarity_search(question, k=3)
    
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.3  # Lower temperature for consistency in responses
    )
    chain = load_qa_chain(llm, chain_type="stuff")
    return call_llm_with_retry(chain, docs, question)
