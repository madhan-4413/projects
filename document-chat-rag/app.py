import os
import base64
import gc
import tempfile
import uuid
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings for clean output
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()

# pyrefly: ignore [missing-import]
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.core import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

import streamlit as st

# Streamlit Page Setup
st.set_page_config(
    page_title="Chat with Docs — Google Gemini RAG",
    page_icon="📄",
    layout="wide"
)

if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.id


@st.cache_resource
def load_llm():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ `GOOGLE_API_KEY` not found in `.env` file. Please configure your API key.")
        st.stop()
    # Initialize Google Gemini model
    llm = Gemini(model="models/gemini-2.5-flash", api_key=api_key)
    return llm


def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()


def display_pdf(file):
    st.markdown("### 📄 PDF Preview")
    file.seek(0)
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")

    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"
                        style="height:80vh; width:100%; border-radius: 8px; border: 1px solid #e0e0e0;"
                    >
                    </iframe>"""
    st.markdown(pdf_display, unsafe_allow_html=True)


# Sidebar controls
with st.sidebar:
    st.header("📄 Add your documents")
    
    uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")

    if uploaded_file:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                file_key = f"{session_id}-{uploaded_file.name}"

                if file_key not in st.session_state.get('file_cache', {}):
                    with st.spinner("Indexing your document..."):
                        if os.path.exists(temp_dir):
                            loader = SimpleDirectoryReader(
                                input_dir=temp_dir,
                                required_exts=[".pdf"],
                                recursive=True
                            )
                        else:    
                            st.error('Could not find uploaded file, please try again.')
                            st.stop()
                        
                        docs = loader.load_data()

                        # Setup LLM & Embedding Model
                        llm = load_llm()
                        embed_model = HuggingFaceEmbedding(
                            model_name="BAAI/bge-large-en-v1.5",
                            trust_remote_code=True
                        )
                        
                        # Creating an index over loaded data
                        Settings.embed_model = embed_model
                        Settings.llm = llm
                        index = VectorStoreIndex.from_documents(docs, show_progress=True)

                        # Create the query engine with streaming
                        query_engine = index.as_query_engine(streaming=True)

                        # ====== Customise prompt template ======
                        qa_prompt_tmpl_str = (
                            "Context information is below.\n"
                            "---------------------\n"
                            "{context_str}\n"
                            "---------------------\n"
                            "Given the context information above I want you to think step by step to answer the query in a crisp manner, in case you don't know the answer say 'I don't know!'.\n"
                            "Query: {query_str}\n"
                            "Answer: "
                        )
                        qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

                        query_engine.update_prompts(
                            {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                        )
                        
                        st.session_state.file_cache[file_key] = query_engine

                # Display preview and ready badge
                st.success("✅ Ready to Chat!")
                display_pdf(uploaded_file)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()     

# Main Header
col1, col2 = st.columns([6, 1])

with col1:
    st.header("💬 Chat with Docs using Google Gemini")

with col2:
    st.button("Clear ↺", on_click=reset_chat)

# Initialize chat history
if "messages" not in st.session_state:
    reset_chat()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Guard: ensure a document has been uploaded and indexed first
        if "file_cache" not in st.session_state or not st.session_state.file_cache:
            message_placeholder.warning("⚠️ Please upload a PDF document first using the sidebar before asking questions.")
        else:
            # Get the most recently cached query engine
            query_engine = list(st.session_state.file_cache.values())[-1]

            # Stream response from the query engine
            streaming_response = query_engine.query(prompt)
            
            for chunk in streaming_response.response_gen:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})