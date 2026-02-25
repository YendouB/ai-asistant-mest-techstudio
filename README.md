# AI Assistant - MEST TechStudio

An AI Assistant built with **Python**, **Streamlit**, and  **Google Gemini** model.

This tool is designed to summarize content from web URLs and PDF documents and it's tied to its creator, **MINLEKIBE Jean-Pierre**.

## Capabilities

- **URL Summarization:** Paste a link to an article, and the assistant will fetch, clean, and summarize the content.
- **PDF Summarization:** Upload a PDF document to receive a concise summary of its contents.


## Tech Stack

- **Python 3.10+**
- **Streamlit** (User Interface)
- **Google GenAI SDK (V2)** (Latest SDK for Gemini models)
- **PyMuPDF (fitz)** (PDF Text Extraction)
- **BeautifulSoup4** (Web Content Cleaning)

## Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed and also python3-venv installed(for linux users).


### 2. Set Up the Virtual Environment


```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
With the virtual environment activated, install the required libraries:
```bash
pip install -r requirements.txt
```

### 4. Configuration
1.  Create a `.env` file in the project root; Copy `.env.example` to `.env` 
2.  Add your Google Gemini API Key and (optionally) your name.

```ini
GEMINI_API_KEY=your_actual_api_key_here
CREATOR_NAME=MINLEKIBE Jean-Pierre
LOG_LEVEL=INFO
```

### Logging Configuration
The `LOG_LEVEL` setting in your `.env` file controls the verbosity of the application logs.

| Level | Description | Use Case |
| :--- | :--- | :--- |
| **DEBUG** | Logs detailed information, including variables and internal states. | Use during development or when troubleshooting complex bugs. |
| **INFO** | Logs standard operational events (e.g., "App started", "PDF processed"). | **Recommended default** for normal usage. |
| **WARNING** | Logs unexpected events that didn't crash the app (e.g., "Empty PDF page"). | useful for monitoring potential issues. |
| **ERROR** | Logs only critical failures and exceptions. | Use in production environments to minimize log size. |


> **Note:** You can get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).

## Running the Application

To start the interface, run the following command:

```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.



## Project Structure

```text
.
├── .env                # API keys 
├── README.md           # Documentation
├── requirements.txt    # Project dependencies
├── app.py              # Main Streamlit application
├── logs/               # Application execution logs
└── src/
    ├── __init__.py
    ├── assistant.py    # AI interaction logic (Gemini V2 Client)
    ├── processor.py    # URL and PDF text extraction
    └── logger.py       # Centralized logging module
```

---
**Creator:** MINLEKIBE Jean-Pierre  

