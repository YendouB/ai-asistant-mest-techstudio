import streamlit as st
import os
from src.assistant import Assistant
from src.processor import ContentProcessor
from src.logger import setup_logger

# Initialize Logger
logger = setup_logger("streamlit_app")

# Page Configuration
st.set_page_config(
    page_title="AI Assistant - MEST TechStudio",
    layout="wide"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .sidebar .sidebar-content {
        background: #ffffff
    }
    h1 {
        color: #0E1117;
    }
    .stButton>button {
        color: white;
        background-color: #FF4B4B;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """
    Main Streamlit Application Logic
    """
    
    # --- Sidebar ---
    st.sidebar.title("Configuration")
    
    # Creator Identity (Read-Only from Env)
    creator_name = os.getenv("CREATOR_NAME", "Unknown Creator")
    st.sidebar.info(f"Identity: **{creator_name}**")
    st.sidebar.markdown("---")
    st.sidebar.write("This tool uses Google Gemini API to summarize content from URLs and PDFs.")

    # --- Main Content ---
    st.title(f"🤖 AI Assistant ({creator_name})")
    st.markdown("### Intelligent Summarization & Analysis")

    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["🔗 Summarize URL", "📄 Summarize PDF"])

    # Initialize Assistant
    try:
        assistant = Assistant()
    except Exception as e:
        st.error(f"❌ Failed to initialize AI Assistant: {e}")
        st.warning("Please check your .env file and ensure GEMINI_API_KEY is set correctly.")
        return

    # --- Tab 1: URL Summarization ---
    with tab1:
        st.header("Paste an Article Link")
        url_input = st.text_input("Enter URL here:", placeholder="https://example.com/article")
        
        if st.button("Summarize URL"):
            if not url_input:
                st.warning("Please enter a valid URL.")
            else:
                with st.spinner("Fetching and summarizing content..."):
                    try:
                        # 1. Fetch Content
                        text_content = ContentProcessor.extract_text_from_url(url_input)
                        
                        if text_content:
                            st.success("Content fetched successfully!")
                            
                            # 2. Generate Summary
                            summary = assistant.summarize(text_content, source_type="URL")
                            
                            st.subheader("Summary:")
                            st.markdown(summary)
                        else:
                            st.error("Failed to extract text from the URL. The website might be blocking access.")
                            
                    except Exception as e:
                        logger.error(f"Error in URL tab: {e}")
                        st.error(f"An unexpected error occurred: {e}")

    # --- Tab 2: PDF Summarization ---
    with tab2:
        st.header("Upload a PDF Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            if st.button("Summarize PDF"):
                with st.spinner("Processing PDF and generating summary..."):
                    try:
                        # 1. Read File Bytes
                        file_bytes = uploaded_file.read()
                        
                        # 2. Extract Text
                        text_content = ContentProcessor.extract_text_from_pdf(file_bytes)
                        
                        if text_content:
                            st.success(f"PDF processed successfully! ({len(text_content)} characters extracted)")
                            
                            # 3. Generate Summary
                            summary = assistant.summarize(text_content, source_type="PDF")
                            
                            st.subheader("Summary:")
                            st.markdown(summary)
                        else:
                            st.error("Could not extract text from this PDF. It might be scanned or encrypted.")
                            
                    except Exception as e:
                        logger.error(f"Error in PDF tab: {e}")
                        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
