import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from io import BytesIO
from typing import Optional
from src.logger import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

class ContentProcessor:
    """
    Handles extraction of text from various sources (URL, PDF).
    """

    @staticmethod
    def extract_text_from_url(url: str) -> Optional[str]:
        """
        Fetches the content from a URL and extracts the main text.
        
        Args:
            url (str): The URL of the article to process.
            
        Returns:
            str: The extracted text content, or None if extraction fails.
        """
        try:
            logger.info(f"Attempting to fetch content from URL: {url}")
            
            # Use a generic user-agent to prevent 403 Forbidden errors
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
                
            # specific cleanup for common article layouts
            # (can be expanded based on target sites)
            article_body = soup.find('article')
            if article_body:
                text = article_body.get_text()
            else:
                # Fallback to body content if no article tag found
                text = soup.body.get_text() if soup.body else ""

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            if not clean_text:
                logger.warning(f"No text extracted from URL: {url}")
                return None
                
            logger.info(f"Successfully extracted {len(clean_text)} characters from URL.")
            return clean_text

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing URL {url}: {e}")
            return None

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
        """
        Extracts text from a PDF file provided as bytes.
        
        Args:
            file_bytes (bytes): The raw bytes of the uploaded PDF file.
            
        Returns:
            str: The extracted text content, or None if extraction fails.
        """
        try:
            logger.info("Attempting to extract text from PDF file.")
            
            # Open the PDF from bytes
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            full_text = []

            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text:
                    full_text.append(text)
                else:
                    logger.warning(f"Page {page_num} of PDF contains no extractable text (might be an image).")

            doc.close()
            
            combined_text = '\n'.join(full_text)
            
            if not combined_text.strip():
                logger.warning("PDF extraction resulted in empty text.")
                return None
                
            logger.info(f"Successfully extracted {len(combined_text)} characters from PDF.")
            return combined_text

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return None
