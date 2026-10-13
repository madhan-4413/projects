import os
import gc
import sys
import tempfile
import uuid
import pandas as pd
from typing import Optional, Dict, Any
import logging

# Ensure UTF-8 for console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from gitingest import ingest
from llama_index.core import Settings, PromptTemplate, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import streamlit as st
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

# Constants
MAX_REPO_SIZE = 250 * 1024 * 1024  # 250MB
SUPPORTED_REPO_TYPES = ['.py', '.md', '.ipynb', '.js', '.ts', '.json']

class GitHubRAGError(Exception):
    """Custom exception for GitHub RAG application errors"""
    pass

def validate_github_url(url: str) -> bool:
    """Validate GitHub repository URL"""
    cleaned = url.strip()
    return cleaned.startswith(('https://github.com/', 'http://github.com/'))

def get_repo_name(url: str) -> str:
    """Extract repository name from URL"""
    try:
        cleaned = url.strip().rstrip('/')
        return cleaned.split('/')[-1].replace('.git', '')
    except Exception as e:
        raise GitHubRAGError(f"Invalid repository URL: {str(e)}")

def reset_chat():
    """Reset chat session and clean up resources"""
    try:
        st.session_state.messages = []
        gc.collect()
        logger.info("Chat session reset successfully")
    except Exception as e:
        logger.error(f"Error resetting chat: {str(e)}")
        raise GitHubRAGError("Failed to reset chat session")

def process_with_gitingest(github_url: str) -> tuple:
    """Process GitHub repository using gitingest"""
    try:
        summary, tree, content = ingest(github_url.strip())
        if not all([summary, tree, content]):
            raise GitHubRAGError("Failed to process repository: Missing data from GitHub")
        return summary, tree, content
    except Exception as e:
        logger.error(f"Error processing repository: {str(e)}")
        raise GitHubRAGError(f"Failed to process repository: {str(e)}")

@st.cache_resource(show_spinner=False)
def get_gemini_models(model_name: str, api_key: str):
    """Cached initialization of Gemini LLM and Embedding models"""
    llm = GoogleGenAI(model=model_name, api_key=api_key)
    embed_model = GoogleGenAIEmbedding(model_name="models/gemini-embedding-001", api_key=api_key)
    return llm, embed_model

def create_query_engine(content_path: str, repo_name: str, tree: str = "") -> Any:
    """Create and configure query engine"""
    try:
        loader = SimpleDirectoryReader(input_dir=content_path)
        docs = loader.load_data()
        node_parser = MarkdownNodeParser()
        index = VectorStoreIndex.from_documents(
            documents=docs, 
            transformations=[node_parser], 
            show_progress=False
        )

        qa_prompt_tmpl_str = """
You are an expert AI assistant specialized in analyzing GitHub repositories.

Repository structure:
{tree}
---------------------

Context information from the repository:
{context_str}
---------------------

Given the repository structure and context above, provide a clear, precise, and helpful answer to the user's question. 
Focus on the repository's content, code structure, patterns, and implementation details. 
If the information is not available in the context, respond with 'I don't have enough information about that aspect in this repository.'

Query: {query_str}
Answer: """
        
        qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str).partial_format(tree=tree)
        query_engine = index.as_query_engine(streaming=True)
        query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
        )
        return query_engine
    except Exception as e:
        logger.error(f"Error creating query engine: {str(e)}")
        raise GitHubRAGError(f"Failed to create query engine: {str(e)}")

# Initialize session state
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}
    st.session_state.messages = []
    st.session_state.current_repo = None
    st.session_state.current_summary = None

session_id = st.session_state.id

# Page configuration
st.set_page_config(
    page_title="Chat with Git",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Read API key and model from environment (not exposed in UI)
google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
model_choice = "gemini-3.5-flash-lite"

# Sidebar
with st.sidebar:
    st.title("💬 Chat with Git")
    st.caption("Ask questions about any GitHub repository using AI")

    st.subheader("Load Repository")
    
    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        help="Enter the full URL of the public GitHub repository"
    )
    
    load_repo = st.button("🚀 Load Repository", type="primary", use_container_width=True)

    if load_repo:
        if not google_api_key:
            st.error("Google API Key not found. Please set GOOGLE_API_KEY in your .env file.")
            st.stop()

        if not github_url or not validate_github_url(github_url):
            st.error("Please enter a valid GitHub repository URL (e.g., https://github.com/pallets/flask).")
            st.stop()

        repo_name = get_repo_name(github_url)
        file_key = f"{session_id}-{repo_name}"
        
        # Configure Gemini models in Settings
        try:
            llm, embed_model = get_gemini_models(model_choice, google_api_key)
            Settings.llm = llm
            Settings.embed_model = embed_model
        except Exception as e:
            st.error(f"Error initializing Google Gemini: {str(e)}")
            st.stop()

        if file_key not in st.session_state.file_cache:
            with st.spinner(f"Ingesting repository '{repo_name}' with GitIngest & building vector index..."):
                with tempfile.TemporaryDirectory() as temp_dir:
                    try:
                        summary, tree, content = process_with_gitingest(github_url)
                        
                        # Save content markdown
                        content_path = os.path.join(temp_dir, f"{repo_name}_content.md")
                        with open(content_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        
                        # Create and cache query engine
                        query_engine = create_query_engine(temp_dir, repo_name, tree=tree)
                        st.session_state.file_cache[file_key] = query_engine
                        st.session_state.current_repo = repo_name
                        st.session_state.current_summary = summary
                        
                        st.success(f"Loaded '{repo_name}'! Ready to chat.")
                        logger.info(f"Successfully processed and indexed repository: {repo_name}")
                        
                    except GitHubRAGError as e:
                        st.error(str(e))
                        st.stop()
                    except Exception as e:
                        st.error(f"Unexpected error: {str(e)}")
                        st.stop()
        else:
            st.session_state.current_repo = repo_name
            st.info(f"Repository '{repo_name}' is already loaded and ready.")

    if st.session_state.current_repo:
        st.markdown("---")
        st.success(f"**Active Repo:** `{st.session_state.current_repo}`")

# Apply configured models globally if key is available
if google_api_key:
    try:
        llm, embed_model = get_gemini_models(model_choice, google_api_key)
        Settings.llm = llm
        Settings.embed_model = embed_model
    except Exception as e:
        logger.warning(f"Could not initialize Gemini models: {e}")

# Main content
col_title, col_actions = st.columns([5, 1])

with col_title:
    if st.session_state.current_repo:
        st.title(f"💬 Chat with Git — `{st.session_state.current_repo}`")
        st.caption("Powered by Google Gemini & GitIngest")
    else:
        st.title("💬 Chat with Git")
        st.caption("Load a GitHub repository from the sidebar to start asking questions.")

with col_actions:
    st.write("")
    if st.button("Clear Chat ↺", on_click=reset_chat, help="Clear chat history and reset session"):
        st.rerun()

# Display current chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick question suggestions if repo is loaded and no messages yet
if st.session_state.current_repo and len(st.session_state.messages) == 0:
    st.markdown("##### 💡 Suggested Questions:")
    q_cols = st.columns(3)
    suggestions = [
        "What is the main purpose of this repository?",
        "Explain the project architecture and file structure.",
        "What are the main entry points and key dependencies?"
    ]
    for i, suggestion in enumerate(suggestions):
        with q_cols[i]:
            if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                st.session_state.pending_prompt = suggestion
                st.rerun()

# Check for pending prompt from suggestion buttons
pending_prompt = st.session_state.pop("pending_prompt", None)
user_prompt = st.chat_input("Ask a question about the repository...") or pending_prompt

if user_prompt:
    # Append and show user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            active_repo = st.session_state.current_repo
            if not active_repo and github_url:
                try:
                    active_repo = get_repo_name(github_url)
                except Exception:
                    pass
            
            if not active_repo:
                raise GitHubRAGError("Please enter a GitHub repository URL and click 'Load Repository' in the sidebar first.")
            
            file_key = f"{session_id}-{active_repo}"
            query_engine = st.session_state.file_cache.get(file_key)
            
            if query_engine is None:
                raise GitHubRAGError("The repository index is not ready. Please click 'Load Repository' in the sidebar.")
            
            response = query_engine.query(user_prompt)
            
            if hasattr(response, 'response_gen'):
                for chunk in response.response_gen:
                    if isinstance(chunk, str):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
            else:
                full_response = str(response)
                message_placeholder.markdown(full_response)
                
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except GitHubRAGError as e:
            st.error(str(e))
            logger.error(f"Error in chat processing: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred while generating response: {str(e)}")
            logger.error(f"Unexpected error in chat: {str(e)}")