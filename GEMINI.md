# Project: AI Assistant - MEST TechStudio

## Overview
A minimalist AI Assistant built with Python, Streamlit, and Gemini API. It can summarize articles from URLs and PDFs while maintaining a specific personality tied to its creator.

## Creator Identity
- **Name:** MINLEKIBE Jean-Pierre
- **Role:** Senior Software Engineer (Creator)
- **Personality:** Professional, helpful, concise, and technically grounded.

## Tech Stack
- **Language:** Python 3.10+
- **AI Model:** Google Gemini 1.5 Pro/Flash
- **Interface:** Streamlit
- **PDF Processing:** PyMuPDF (fitz) or pdfplumber
- **Web Scraping:** BeautifulSoup4 / requests

## Core Capabilities
1. **URL Summarization:** Extract text content from a provided link and summarize it.
2. **PDF Summarization:** Extract text from uploaded PDF files and summarize it.
3. **Identity:** The assistant must identify itself as being created by or named after the Creator.

## Engineering Standards
- **Logging:** All major operations and errors must be logged using the standard `logging` library.
- **Exceptions:** Use custom exception classes where appropriate and always wrap external API calls in try-except blocks.
- **Documentation:** Every module must have a docstring.
- **Environment:** Secrets (API keys, creator name) must be stored in a `.env` file.

## Project Structure
```text
.
├── .env
├── GEMINI.md
├── README.md
├── requirements.txt
├── app.py
├── src/
│   ├── __init__.py
│   ├── assistant.py
│   ├── processor.py
│   └── logger.py
└── tests/
```
