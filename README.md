# PDF-Summarizer
A ChatBot application built using LangChain using HuggingFace Embeddings and Groq API for fast processing and is hosted using Stremlit


# PDF Summarizer ChatBot

A sophisticated web application that leverages artificial intelligence to generate concise summaries of PDF documents. Built with Streamlit and powered by advanced language models, this tool streamlines document analysis by providing intelligent summarization capabilities.

## Description

The PDF Summarizer ChatBot transforms the way users interact with PDF documents by offering automated summarization functionality. The application utilizes state-of-the-art language models and embedding techniques to process and understand document content, delivering accurate and contextual summaries on demand.

## Key Technologies

The application is built using modern technologies and frameworks:

- **Streamlit**: Powers the interactive web interface
- **LangChain**: Orchestrates the document processing and summarization pipeline
- **Groq**: Provides the large language model capabilities
- **HuggingFace BGE Embeddings**: Enables efficient document embedding and semantic search
- **FAISS**: Manages vector storage and similarity search operations
- **PyPDF2**: Handles PDF document processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-summarizer-chatbot.git
cd pdf-summarizer-chatbot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the application through your web browser (typically at `http://localhost:8501`)

3. Upload a PDF document using the file uploader

4. Click "Generate Summary" to process the document and receive a comprehensive summary

## Project Structure

```
pdf-summarizer-chatbot/
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions for PDF processing
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (create this file)
└── README.md          # Project documentation
```

## Features

- Intuitive web interface for PDF upload
- Advanced text processing with character-level splitting
- High-quality embeddings using BGE models
- Efficient vector similarity search
- Contextual summarization using Mixtral-8x7b model
- Configurable processing parameters

## Technical Implementation

The application follows a structured processing pipeline:

1. **Document Processing**: Extracts text from PDF documents using PyPDF2
2. **Text Chunking**: Splits text into manageable segments with controlled overlap
3. **Embedding Generation**: Creates document embeddings using BGE models
4. **Vector Storage**: Organizes embeddings in FAISS for efficient retrieval
5. **Summary Generation**: Leverages Groq's Mixtral model for coherent summarization

## Configuration

Key parameters can be adjusted in the application:

- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Model temperature: 0.8
- Embedding model: BAAI/bge-small-en

## Environmental Requirements

- Python 3.8 or higher
- Sufficient RAM for document processing (recommended 8GB+)
- Internet connectivity for API access
- CPU with support for modern instruction sets

## Security Notes

- API keys should be stored securely in environment variables
- Uploaded documents are processed in memory and not permanently stored
- User data is not retained between sessions

## Contributing

We welcome contributions to improve the PDF Summarizer ChatBot:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## Future Enhancements

- Support for additional document formats
- Custom summarization parameters
- Batch processing capabilities
- Enhanced error handling and validation
- Multi-language support
- Export functionality for summaries
