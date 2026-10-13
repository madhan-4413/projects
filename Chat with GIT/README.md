# Chat with GitHub using Google Gemini & RAG!

This project leverages GitIngest to parse any GitHub repository into Markdown format and uses LlamaIndex with Google Gemini for RAG (Retrieval-Augmented Generation) orchestration over the repository.

## Installation and Setup

1. **Install Dependencies**:
   Ensure you have Python 3.9 or later installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**:
   Create or configure the `.env` file in the project directory with your Google API Key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Running the Application**:
   - **Google Gemini App**:
     ```bash
     streamlit run app.py
     ```
   - **Local App (Ollama)**:
     ```bash
     streamlit run app_local.py
     ```
