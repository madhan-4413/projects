import os
import base64
import gc
import tempfile
import uuid
import warnings
import google.generativeai as genai
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
    page_title="single-model RAG",
    page_icon="📄",
    layout="wide"
)

if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

# Store full document text separately for summarization
if "doc_full_text" not in st.session_state:
    st.session_state.doc_full_text = {}

session_id = st.session_state.id

# ── Keyword detection for summary requests ──────────────────────────────────
SUMMARY_KEYWORDS = [
    "summary", "summarize", "summarise", "summarization",
    "overview", "outline", "gist", "brief", "describe the pdf",
    "what is this pdf", "what is this document", "what does this pdf",
    "what does this document", "explain the pdf", "explain the document",
    "full summary", "entire pdf", "whole document", "entire document",
    "key points", "main points", "key takeaways", "highlights",
]

def is_summary_request(query: str) -> bool:
    q = query.lower().strip()
    return any(kw in q for kw in SUMMARY_KEYWORDS)


@st.cache_resource
def load_llm():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ `GOOGLE_API_KEY` not found in `.env` file. Please configure your API key.")
        st.stop()
    llm = Gemini(model="models/gemini-2.5-flash", api_key=api_key)
    return llm


def get_api_key():
    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def summarize_full_document(full_text: str, user_query: str) -> str:
    """Send the FULL document text directly to Gemini for a comprehensive summary."""
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    prompt = (
        f"You are an expert document analyst. The user has uploaded a PDF document. "
        f"Below is the COMPLETE text extracted from the entire document.\n\n"
        f"USER REQUEST: {user_query}\n\n"
        f"FULL DOCUMENT TEXT:\n"
        f"{'─'*60}\n"
        f"{full_text}\n"
        f"{'─'*60}\n\n"
        f"Please provide a thorough, well-structured summary of the ENTIRE document above. "
        f"Include:\n"
        f"- 📌 Main topic and purpose of the document\n"
        f"- 🔑 Key concepts, sections, and important points\n"
        f"- 📊 Any important data, findings, or conclusions\n"
        f"- 💡 Key takeaways\n\n"
        f"Be comprehensive and cover the full document."
    )

    response = model.generate_content(prompt)
    return response.text


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


# ── Sidebar ───────────────────────────────────────────────────────────────────
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

                if file_key not in st.session_state.get("file_cache", {}):
                    with st.spinner("Indexing your document..."):
                        if os.path.exists(temp_dir):
                            loader = SimpleDirectoryReader(
                                input_dir=temp_dir,
                                required_exts=[".pdf"],
                                recursive=True
                            )
                        else:
                            st.error("Could not find uploaded file, please try again.")
                            st.stop()

                        docs = loader.load_data()

                        # ── Store full concatenated text for summarization ──
                        full_text = "\n\n".join(
                            [doc.get_content() for doc in docs]
                        )
                        st.session_state.doc_full_text[file_key] = full_text

                        # ── Setup LLM & Embedding Model ──
                        llm = load_llm()
                        embed_model = HuggingFaceEmbedding(
                            model_name="BAAI/bge-large-en-v1.5",
                            trust_remote_code=True
                        )

                        Settings.embed_model = embed_model
                        Settings.llm = llm
                        index = VectorStoreIndex.from_documents(docs, show_progress=True)

                        # ── Query Engine (for specific Q&A) ──
                        query_engine = index.as_query_engine(streaming=True)

                        qa_prompt_tmpl_str = (
                            "Context information is below.\n"
                            "---------------------\n"
                            "{context_str}\n"
                            "---------------------\n"
                            "Given the context information above, think step by step to answer the query "
                            "in a crisp and complete manner. If you cannot find the answer in the context, "
                            "say 'I don't know!'.\n"
                            "Query: {query_str}\n"
                            "Answer: "
                        )
                        qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
                        query_engine.update_prompts(
                            {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                        )

                        st.session_state.file_cache[file_key] = query_engine

                st.success("✅ Ready to Chat!")
                display_pdf(uploaded_file)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()


# ── Main Header ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([6, 1])

with col1:
    st.header("💬 single-model RAG")

with col2:
    st.button("Clear ↺", on_click=reset_chat)

# Initialize chat history
if "messages" not in st.session_state:
    reset_chat()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat Input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question or request a summary of your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if "file_cache" not in st.session_state or not st.session_state.file_cache:
            message_placeholder.warning("⚠️ Please upload a PDF document first using the sidebar.")
        else:
            # Get the most recent file key
            latest_key = list(st.session_state.file_cache.keys())[-1]
            query_engine = st.session_state.file_cache[latest_key]

            # ── Route: Full Summary vs. Specific Q&A ──────────────────────
            if is_summary_request(prompt):
                # Use full document text → send directly to Gemini
                message_placeholder.markdown("🔍 *Reading the entire document and generating summary...*")
                try:
                    full_text = st.session_state.doc_full_text.get(latest_key, "")
                    if not full_text:
                        full_response = "⚠️ Could not retrieve full document text. Please re-upload the PDF."
                    else:
                        full_response = summarize_full_document(full_text, prompt)
                except Exception as e:
                    full_response = f"⚠️ Error generating summary: {e}"
                message_placeholder.markdown(full_response)

            else:
                # Use RAG for specific Q&A with streaming
                try:
                    streaming_response = query_engine.query(prompt)
                    for chunk in streaming_response.response_gen:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"⚠️ Error: {e}"
                    message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})