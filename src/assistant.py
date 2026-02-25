import os
import time
from google import genai
from dotenv import load_dotenv
from src.logger import setup_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger(__name__)

class Assistant:
    """
    The AI Assistant wrapper that interacts with the Gemini API.
    Enforces a specific persona based on the Creator's identity.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.creator_name = os.getenv("CREATOR_NAME", "The Creator")
        
        if not self.api_key:
            logger.critical("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("API Key is missing. Please check your .env file.")
            
        try:
            # Initialize the Gemini V2 Client
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = 'gemini-3-flash-preview'
            logger.info(f"Gemini API configured successfully. Persona initialized as: {self.creator_name}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            raise

    def summarize(self, text: str, source_type: str = "text") -> str:
        """
        Generates a summary of the provided text using the Creator's persona.
        Retries on 503 errors (Service Unavailable).
        
        Args:
            text (str): The content to summarize.
            source_type (str): Origin of text ('URL' or 'PDF') for context.
            
        Returns:
            str: The generated summary.
        """
        if not text:
            return "I cannot summarize an empty text."
            
        logger.info(f"Sending summarization request for {source_type} content (Length: {len(text)} chars).")
        
        # Construct the prompt with persona
        prompt = f"""
        You are {self.creator_name}, a Senior Software Engineer and AI Assistant.
        Your personality is professional, helpful, concise, and technically grounded.
        
        Task:
        Please provide a comprehensive yet concise summary of the following text, which was extracted from a {source_type}.
        Focus on the key takeaways and technical details if present.
        
        Text to summarize:
        {text[:30000]}  # Truncate to avoid token limits if extremely large, though Flash context is huge.
        """

        max_retries = 3
        retry_delay = 2  # Start with 2 seconds

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                
                if response.text:
                    logger.info("Summary generated successfully.")
                    return response.text
                else:
                    logger.warning("Gemini returned an empty response.")
                    return "I'm sorry, but I couldn't generate a summary for this content."

            except Exception as e:
                # Check for 503 or overload errors
                error_msg = str(e)
                if ("503" in error_msg or "429" in error_msg) and attempt < max_retries - 1:
                    logger.warning(f"Model overloaded ({error_msg}). Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Error during summarization: {e}")
                    return f"An error occurred while communicating with the AI service: {str(e)}"
        
        return "Failed to generate summary after multiple attempts."
