from dotenv import load_dotenv
import streamlit as st
from utils import create_knowledge_base, generate_summary, answer_question
import os

# Must be the first Streamlit command
st.set_page_config(page_title="PDF Chatbot", page_icon="📄", layout="centered")
load_dotenv()

# Custom CSS for chat bubbles with dark/light theme support
st.markdown(
    """
    <style>
    :root {
      --user-bg: #DCF8C6;
      --bot-bg: #E8E8E8;
      --user-text: #000000;
      --bot-text: #000000;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --user-bg: #4A6C4A;
        --bot-bg: #2F2F2F;
        --user-text: #FFFFFF;
        --bot-text: #FFFFFF;
      }
    }
    .chat-bubble {
      padding: 10px;
      border-radius: 10px;
      margin: 5px 0;
      max-width: 70%;
      word-wrap: break-word;
    }
    .chat-bubble.user {
      text-align: right;
      margin-left: auto;
      background-color: var(--user-bg);
      color: var(--user-text);
    }
    .chat-bubble.bot {
      text-align: left;
      margin-right: auto;
      background-color: var(--bot-bg);
      color: var(--bot-text);
    }
    </style>
    """,
    unsafe_allow_html=True
)

def display_chat(messages):
    """Display chat messages with styled chat bubbles."""
    for msg in messages:
        if msg["sender"] == "user":
            st.markdown(
                f'<div class="chat-bubble user">{msg["message"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-bubble bot">{msg["message"]}</div>',
                unsafe_allow_html=True
            )

def main():
    st.title("AI-Powered PDF Chatbot")
    st.markdown("---")
    
    # PDF upload section
    pdf = st.file_uploader("Upload PDF Document", type="pdf", help="Maximum file size: 50MB")
    if pdf:
        # Process PDF and build knowledge base only once
        if "knowledge_base" not in st.session_state:
            with st.spinner("Processing document..."):
                try:
                    knowledge_base = create_knowledge_base(pdf)
                    st.session_state.knowledge_base = knowledge_base
                    summary = generate_summary(knowledge_base)
                    st.session_state.summary = summary
                except Exception as e:
                    st.error(f"Processing error: {str(e)}")
        
        if "summary" in st.session_state:
            st.subheader("Document Summary")
            st.markdown(f"```{st.session_state.summary}```")
        
        st.markdown("---")
        st.subheader("Chat with the Document")
        
        # Initialize chat session state variables if not already set
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "previous_queries" not in st.session_state:
            st.session_state.previous_queries = []
        
        # Create a form for input; clear_on_submit resets the input field automatically.
        with st.form("chat_form", clear_on_submit=True):
            user_question = st.text_input("Enter your question about the document")
            submitted = st.form_submit_button("Send")
            if submitted and user_question.strip() != "":
                # Append user's question to chat history and previous queries
                st.session_state.chat_history.append({"sender": "user", "message": user_question})
                st.session_state.previous_queries.append(user_question)
                if "knowledge_base" in st.session_state:
                    with st.spinner("Fetching answer..."):
                        try:
                            answer = answer_question(st.session_state.knowledge_base, user_question)
                            st.session_state.chat_history.append({"sender": "bot", "message": answer})
                        except Exception as e:
                            st.error(f"Chatbot error: {str(e)}")
                else:
                    st.warning("Knowledge base not available.")
        
        # Display updated chat conversation after processing the form
        display_chat(st.session_state.chat_history)
        
        # Display suggested questions based on the last user query
        if st.session_state.previous_queries:
            last_query = st.session_state.previous_queries[-1]
            suggestions = [
                f"Can you explain more about '{last_query}'?",
                f"What are the implications of '{last_query}'?",
                f"How does '{last_query}' affect the overall analysis?",
            ]
            st.subheader("Suggested Questions Based on Your Last Search:")
            for suggestion in suggestions:
                if st.button(suggestion):
                    st.session_state.chat_history.append({"sender": "user", "message": suggestion})
                    with st.spinner("Fetching answer..."):
                        try:
                            answer = answer_question(st.session_state.knowledge_base, suggestion)
                            st.session_state.chat_history.append({"sender": "bot", "message": answer})
                        except Exception as e:
                            st.error(f"Chatbot error: {str(e)}")
                        
if __name__ == "__main__":
    main()
