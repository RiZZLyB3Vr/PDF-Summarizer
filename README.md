# PDF Chatbot

An AI-powered Streamlit application that allows users to upload PDF documents, generate concise summaries, and interact with the document content via a chat interface.

## Description

The PDF Chatbot processes a PDF file to extract its text, generates a summary of the document, and then provides an interactive chat interface where users can ask questions about the content. The chatbot uses a language model (via LangChain and ChatGroq) to answer questions based on the PDF content. It also provides suggested follow-up questions based on the user's previous queries. The app supports both light and dark themes for improved readability.

## Features

- **PDF Upload & Processing:**  
  Upload PDF documents and extract text using PyPDF2. (An OCR fallback can be implemented if needed.)
  
- **Summary Generation:**  
  Generate a concise summary of the PDF content using a language model.

- **Interactive Chat Interface:**  
  Ask questions about the document and receive contextually relevant answers.  
  - The chat interface displays messages in styled chat bubbles that adapt to the user's theme.
  
- **Suggested Questions:**  
  Based on the most recent user query, the app offers suggested questions to help further explore the content.

- **Optimized Token Usage & Retry Logic:**  
  The application minimizes token usage by adjusting chunk sizes and limits the number of context chunks. It also includes retry logic to handle rate limit errors gracefully.

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [pdf2image](https://pypi.org/project/pdf2image/) *(if OCR is needed)*
- [pytesseract](https://pypi.org/project/pytesseract/) *(if OCR is needed)*
- [langchain](https://github.com/hwchase17/langchain)
- [langchain_community](https://github.com/hwchase17/langchain)
- [langchain_groq](https://github.com/yourprovider/langchain_groq) *(or your specific API integration)*
- FAISS (or FAISS-cpu)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/pdf-chatbot.git
   cd pdf-chatbot
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv myvenv
   # Activate the virtual environment:
   # On Windows:
   myvenv\Scripts\activate
   # On macOS/Linux:
   source myvenv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the project root with at least the following content:

   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Usage

1. **Run the application:**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the App:**
   - **Upload a PDF:** Use the file uploader to select and upload your PDF document.
   - **View Summary:** The app will display a concise summary of the document.
   - **Chat Interface:** Type your question in the chat box and click "Send" to get an answer.  
     Suggested questions based on your last query will be displayed below the chat.
   - **Theme Compatibility:** The chat interface automatically adapts to light or dark themes based on your system settings.

## Deployment

- **Streamlit Cloud:**  
  Push your repository to GitHub and deploy it using [Streamlit Cloud](https://streamlit.io/cloud).

- **Other Platforms:**  
  You can also deploy this application using services such as Heroku, AWS, or Docker. Ensure that environment variables (e.g., `GROQ_API_KEY`) are properly set in your chosen deployment environment.

## Future Improvements

- Implement an OCR fallback for image-based PDFs.
- Enhance prompt engineering for more accurate answers.
- Add additional error handling and logging.
- Explore integration with alternative AI models for improved performance.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the developers of Streamlit, LangChain, and the associated libraries that made this project possible.
```

---

Feel free to adjust the content (such as repository links, deployment instructions, or additional features) to fit your specific needs.
