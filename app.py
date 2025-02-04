from dotenv import load_dotenv
import streamlit as st
from utils import create_knowledge_base, generate_summary, answer_question
import os

load_dotenv()

def main():
    st.set_page_config(
        page_title="PDF Chatbot",
        page_icon="📄",
        layout="centered"
    )
    
    st.title("AI-Powered PDF Chatbot")
    st.markdown("---")
    
    pdf = st.file_uploader(
        "Upload PDF Document",
        type="pdf",
        help="Maximum file size: 50MB"
    )
    
    if pdf:
        with st.spinner("Processing document..."):
            try:
                # Build the knowledge base and store it in session_state
                knowledge_base = create_knowledge_base(pdf)
                st.session_state.knowledge_base = knowledge_base
                
                # Generate and display the summary
                summary = generate_summary(knowledge_base)
                st.subheader("Document Summary")
                st.markdown(f"```{summary}```")
            except Exception as e:
                st.error(f"Processing error: {str(e)}")
        
        st.markdown("---")
        st.subheader("Chat with the Document")
        user_question = st.text_input("Enter your question about the document:")
        
        if st.button("Ask"):
            if user_question and "knowledge_base" in st.session_state:
                with st.spinner("Fetching answer..."):
                    try:
                        answer = answer_question(st.session_state.knowledge_base, user_question)
                        st.markdown(f"**Answer:** {answer}")
                    except Exception as e:
                        st.error(f"Chatbot error: {str(e)}")
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
