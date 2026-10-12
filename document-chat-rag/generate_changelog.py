from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
)
from reportlab.lib.units import inch

OUTPUT = "changeslog.pdf"

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = colors.HexColor("#1E3A8A")   # Deep blue
ACCENT    = colors.HexColor("#2563EB")   # Bright blue
TEAL      = colors.HexColor("#0D9488")   # Teal (additions)
AMBER     = colors.HexColor("#D97706")   # Amber (why)
SLATE     = colors.HexColor("#1F2937")   # Dark slate (body)
LIGHT_BG  = colors.HexColor("#F8FAFC")  # Off-white
BORDER    = colors.HexColor("#E2E8F0")   # Light grey

def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # ── Custom paragraph styles ───────────────────────────────────────────────
    title_s = ParagraphStyle("title_s", fontName="Helvetica-Bold", fontSize=20,
                              textColor=PRIMARY, leading=26, spaceAfter=2)
    sub_s   = ParagraphStyle("sub_s",   fontName="Helvetica",      fontSize=9,
                              textColor=colors.HexColor("#64748B"), leading=13, spaceAfter=10)
    h2_s    = ParagraphStyle("h2_s",    fontName="Helvetica-Bold", fontSize=12,
                              textColor=PRIMARY, leading=16, spaceBefore=10, spaceAfter=4)
    h3_s    = ParagraphStyle("h3_s",    fontName="Helvetica-Bold", fontSize=9.5,
                              textColor=ACCENT,  leading=13, spaceBefore=4,  spaceAfter=2)
    body_s  = ParagraphStyle("body_s",  fontName="Helvetica",      fontSize=8.8,
                              textColor=SLATE,   leading=13)
    code_s  = ParagraphStyle("code_s",  fontName="Courier",        fontSize=8,
                              textColor=colors.HexColor("#374151"), leading=12,
                              backColor=colors.HexColor("#F1F5F9"), borderPadding=4)
    why_s   = ParagraphStyle("why_s",   fontName="Helvetica-Oblique", fontSize=8.8,
                              textColor=AMBER,   leading=13)

    def row(label, content, label_color=TEAL):
        """Render a two-column bullet row inside a table."""
        lp = Paragraph(f"<b><font color='#{label_color.hexval()[2:]}'>▸ {label}</font></b>", body_s)
        rp = Paragraph(content, body_s)
        t  = Table([[lp, rp]], colWidths=[110, 418])
        t.setStyle(TableStyle([
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",  (0,0), (-1,-1), 3),
            ("BOTTOMPADDING",(0,0),(-1,-1), 3),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING",(0,0), (-1,-1), 0),
        ]))
        return t

    def section_header(num, title):
        bg = colors.HexColor("#EFF6FF")
        data = [[Paragraph(f"<b>{num}. {title}</b>", h2_s)]]
        t = Table(data, colWidths=[532])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), bg),
            ("BOX",          (0,0),(-1,-1), 0.5, BORDER),
            ("TOPPADDING",   (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ]))
        return t

    def bullet_block(items):
        """items = list of (label, detail, why)"""
        rows = []
        for label, detail, why in items:
            rows.append([
                Paragraph(f"<b>•  {label}</b>", h3_s),
                Paragraph(""),
            ])
            rows.append([
                Paragraph(f"<font color='#374151'>{detail}</font>", body_s),
                Paragraph(""),
            ])
            if why:
                rows.append([
                    Paragraph(f"<i>⚡ Why: {why}</i>", why_s),
                    Paragraph(""),
                ])
            rows.append([Paragraph(" ", body_s), Paragraph("")])  # spacer

        t = Table(rows, colWidths=[510, 22])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), LIGHT_BG),
            ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
            ("TOPPADDING",    (0,0),(-1,-1), 2),
            ("BOTTOMPADDING", (0,0),(-1,-1), 2),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ]))
        return t

    # ── Build story ───────────────────────────────────────────────────────────
    story = []

    story.append(Paragraph("📋  Project Changelog — Document Chat RAG", title_s))
    story.append(Paragraph(
        "Prepared on: 08 October 2026  •  Project: document-chat-rag  •  Repo: github.com/madhan-4413/projects",
        sub_s
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceBefore=0, spaceAfter=12))

    # ── Overview table ────────────────────────────────────────────────────────
    story.append(Paragraph("Session Overview", h2_s))
    ov_data = [
        [Paragraph("<b>Area</b>", body_s),      Paragraph("<b>Summary</b>", body_s)],
        [Paragraph("Project Cleanup",  body_s), Paragraph("Removed irrelevant files, sample PDFs, thumbnails, and empty folders.", body_s)],
        [Paragraph("Documentation",   body_s),  Paragraph("Rewrote README.md from scratch; added SETUP.md for Windows/Gemini setup.", body_s)],
        [Paragraph("AI Integration",  body_s),  Paragraph("Replaced local Ollama/Llama 3.2 LLM with Google Gemini 2.5 Flash via API.", body_s)],
        [Paragraph("Security",        body_s),  Paragraph("Created .env for API key storage; added .gitignore to prevent secret leakage.", body_s)],
        [Paragraph("RAG Logic Fix",   body_s),  Paragraph("Added smart query router: full-doc summarization vs. chunk-based Q&A.", body_s)],
        [Paragraph("GitHub Sync",     body_s),  Paragraph("Staged, committed, and pushed all changes to madhan-4413/projects on GitHub.", body_s)],
        [Paragraph("PDF Report",      body_s),  Paragraph("Generated AI_Feature_Suggestions_Roadmap.pdf with 5 categories and roadmap table.", body_s)],
    ]
    ov_t = Table(ov_data, colWidths=[130, 402])
    ov_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  colors.HexColor("#EFF6FF")),
        ("TEXTCOLOR",     (0,0),(-1,0),  PRIMARY),
        ("BACKGROUND",    (0,1),(-1,-1), LIGHT_BG),
        ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ]))
    story.append(ov_t)
    story.append(Spacer(1, 10))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 1 — AI Feature Suggestions PDF
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("1", "AI_Feature_Suggestions_Roadmap.pdf — Generated"))
    story.append(bullet_block([
        (
            "File Created",
            "AI_Feature_Suggestions_Roadmap.pdf (inside document-chat-rag/)",
            "User asked for all AI feature suggestions to be compiled into a shareable PDF document."
        ),
        (
            "Content: 5 Feature Categories",
            "1) Document Intelligence & Multi-Format Ingestion — multi-format support, OCR/Vision parsing, "
            "table extraction, multi-document indexing. "
            "2) Advanced Retrieval (Advanced RAG) — hybrid BM25+dense search, reranking, HyDE query transformation, "
            "persistent vector DB. "
            "3) Citations, Verification & Explainability — page-level source citations, PDF highlighting, hallucination guardrails. "
            "4) Automated Document Actions — one-click summaries, auto-generated starter questions, quiz/flashcard generator, "
            "chat export to PDF/Word. "
            "5) Multi-Agent & Conversational Capabilities — agentic tool calling (web/code), dynamic model switcher, voice I/O.",
            "User needed all ideas in one organised document for reference and planning."
        ),
        (
            "Implementation Roadmap Table",
            "Phase 1 (Quick Wins), Phase 2 (Core RAG Upgrade), Phase 3 (Advanced AI) — with impact/effort ratings.",
            "Provides a clear execution path so the user knows which features to implement first."
        ),
        (
            "Script Cleaned Up",
            "generate_suggestions_pdf.py was deleted after the PDF was generated.",
            "Temporary helper script — removed to keep the project folder clean."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 2 — Project Folder Cleanup
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("2", "Project Folder Cleanup — Irrelevant Files Removed"))
    story.append(bullet_block([
        (
            "docs/dspy.pdf — Deleted",
            "A 460 KB sample PDF completely unrelated to this project (DSPy library documentation).",
            "Not referenced anywhere in code; cluttered the project; confused new contributors."
        ),
        (
            "resources/thumbnail.png — Deleted",
            "A 291 KB external demo thumbnail image sourced from the original template repo.",
            "Referenced only in README via a GitHub CDN URL — not a local asset. Removed to keep repo lean."
        ),
        (
            "docs/ and resources/ folders — Deleted",
            "Both directories became empty after removing their only files.",
            "Empty directories add noise to the project structure with no purpose."
        ),
        (
            "generate_suggestions_pdf.py — Deleted",
            "Temporary Python script used only to generate the AI features PDF.",
            "One-time tool; no longer needed after the PDF was produced."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 3 — README.md Rewrite
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("3", "README.md — Complete Rewrite"))
    story.append(bullet_block([
        (
            "Title & Description Updated",
            "New title: '📄 Document Chat RAG (Retrieval-Augmented Generation)' with a clear one-line project description.",
            "The original README was the template's README — not specific to this user's project."
        ),
        (
            "Key Features Section Added",
            "6 bullet points: Local & Private execution, BGE embeddings, Real-time streaming, "
            "Interactive PDF Preview, Context-Aware QA Prompting, One-Click Session Reset.",
            "Users need a quick at-a-glance understanding of what the app does without reading the code."
        ),
        (
            "Architecture & Pipeline Diagram Added",
            "Mermaid flowchart showing: PDF Upload → SimpleDirectoryReader → BGE Embeddings → "
            "VectorStoreIndex → Streaming Query Engine → Gemini → Chat UI.",
            "Visual architecture helps developers and collaborators understand the RAG pipeline instantly."
        ),
        (
            "Tech Stack Section Added",
            "Ollama (replaced by Gemini), LlamaIndex, BAAI/bge-large-en-v1.5, Streamlit, Python 3.11+.",
            "Clearly documents all tools and frameworks used for reproducibility."
        ),
        (
            "Step-by-Step Getting Started Guide",
            "3 steps: Install Ollama / configure Gemini API → pip install -r requirements.txt → streamlit run app.py.",
            "Previously missing — users had no clear onboarding path."
        ),
        (
            "Project Structure Tree Added",
            "ASCII tree of all files with inline comments explaining each file's role.",
            "Helps new contributors navigate the codebase quickly."
        ),
        (
            "AI Features Roadmap Section",
            "Links to AI_Feature_Suggestions_Roadmap.pdf with Phase 1/2/3 summaries.",
            "Connects the feature planning document to the README for easy discovery."
        ),
        (
            "Author & License Section",
            "Madan Sai Jogi — GitHub @madhan-4413, LinkedIn profile, MIT License.",
            "Professional README standard; also adds personal branding to the project."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 4 — .env + .gitignore + .env.example
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("4", ".env / .gitignore / .env.example — Security & Secret Management"))
    story.append(bullet_block([
        (
            ".env File Created",
            "Stores: GOOGLE_API_KEY and GEMINI_API_KEY with the user's Google Gemini API key.",
            "Hard-coding API keys directly in source code is a critical security anti-pattern. "
            "Centralising secrets in .env enables easy rotation without touching code."
        ),
        (
            ".gitignore Created",
            "Rules added: .env / .env.* / *.env (secrets), __pycache__/ (Python cache), "
            "venv/ / env/ / .venv/ (virtual envs), .streamlit/ (Streamlit config), .DS_Store / Thumbs.db (OS junk).",
            "Without .gitignore the API key would be pushed to GitHub and publicly exposed — "
            "a serious security risk. The .gitignore prevents this permanently."
        ),
        (
            ".env.example Created",
            "Template file showing: GOOGLE_API_KEY=your_google_gemini_api_key_here",
            "Allows collaborators to know which environment variables are required "
            "without exposing the actual secret values."
        ),
        (
            "python-dotenv Added",
            "Added load_dotenv() call at the top of app.py; added python-dotenv to requirements.txt.",
            "Automatically loads .env variables into os.environ so the app reads them securely at runtime."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 5 — LLM Switch: Ollama → Google Gemini
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("5", "app.py — LLM Switched from Ollama (Llama 3.2) to Google Gemini 2.5 Flash"))
    story.append(bullet_block([
        (
            "Old LLM Removed",
            "Removed: from llama_index.llms.ollama import Ollama and Ollama(model='llama3.2', request_timeout=120.0)",
            "Ollama requires a locally running server and ~2 GB model download — heavy setup for end users."
        ),
        (
            "New LLM Added",
            "Added: from llama_index.llms.gemini import Gemini and "
            "Gemini(model='models/gemini-2.5-flash', api_key=...) loaded from .env via os.getenv().",
            "Google Gemini is cloud-based, requires no local installation, and is significantly "
            "more powerful — especially for long-context summarization tasks."
        ),
        (
            "load_llm() Function Updated",
            "Now reads GOOGLE_API_KEY / GEMINI_API_KEY from environment; "
            "shows a clear st.error() message if the key is missing instead of crashing silently.",
            "Improves user experience by giving actionable error messages when misconfigured."
        ),
        (
            "Settings.llm Updated",
            "Settings.llm = llm (Gemini) now set globally before creating the VectorStoreIndex query engine.",
            "Ensures all LlamaIndex retrieval and synthesis operations use Gemini consistently."
        ),
        (
            "Header Text Updated",
            "Changed: 'Chat with Docs using Llama-3.2' → '💬 single-model RAG'.",
            "User requested the title to reflect the new model-agnostic branding."
        ),
        (
            "Page Title Updated",
            "st.set_page_config(page_title='single-model RAG') — appears in browser tab.",
            "User modified this directly; kept in sync with the main header."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 6 — Full PDF Summarization Fix
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("6", "app.py — Full PDF Summarization Fix (Smart Query Router)"))
    story.append(bullet_block([
        (
            "Root Problem Identified",
            "RAG retrieves only the top 2-3 most similar text chunks to the query. "
            "When a user asked 'summarize this PDF', Gemini only saw 2-3 pages of context "
            "and responded 'I don't know!' because the full document was never passed to it.",
            "Standard RAG architecture limitation — chunk retrieval is not suitable for whole-document tasks."
        ),
        (
            "doc_full_text Session Store Added",
            "st.session_state.doc_full_text[file_key] now stores the full concatenated text "
            "of all document pages at index time using: '\\n\\n'.join([doc.get_content() for doc in docs])",
            "Enables the full document text to be retrieved on demand for any summary request "
            "without re-loading or re-parsing the PDF."
        ),
        (
            "is_summary_request() Detector Added",
            "Detects 20+ summary-related keywords: 'summary', 'summarize', 'summarise', 'overview', "
            "'gist', 'brief', 'key points', 'main points', 'key takeaways', 'highlights', "
            "'explain the pdf', 'what is this document', 'entire pdf', 'whole document', etc.",
            "Allows automatic routing without requiring the user to use a special command or button."
        ),
        (
            "summarize_full_document() Function Added",
            "Uses google.generativeai directly (bypassing LlamaIndex RAG) to send the ENTIRE document "
            "text to models/gemini-2.5-flash with a structured prompt requesting: "
            "📌 Main topic, 🔑 Key concepts, 📊 Data/findings, 💡 Key takeaways.",
            "Gemini 2.5 Flash supports a 1M token context window — large enough to read entire textbooks. "
            "Bypassing RAG chunks ensures no information is lost."
        ),
        (
            "Smart Query Router Added",
            "if is_summary_request(prompt): → summarize_full_document() via full text. "
            "else: → RAG streaming query engine for specific Q&A.",
            "Best of both worlds: accurate whole-document summaries AND precise chunk-based Q&A — "
            "automatically selected based on what the user asks."
        ),
        (
            "Loading Indicator Added",
            "Shows '🔍 Reading the entire document and generating summary...' while Gemini processes.",
            "Full-document summarization takes 3-10 seconds — the spinner prevents the user "
            "from thinking the app has frozen."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 7 — requirements.txt & SETUP.md Updates
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("7", "requirements.txt & SETUP.md — Updated for Gemini Integration"))
    story.append(bullet_block([
        (
            "requirements.txt — New Packages Added",
            "llama-index-llms-gemini>=0.6.0, google-generativeai>=0.8.0, python-dotenv>=1.0.0. "
            "Also retained: streamlit, llama-index-core, llama-index-embeddings-huggingface, "
            "llama-index-readers-file, torch, transformers, sentence-transformers.",
            "New LLM and security dependencies must be declared so that pip install -r requirements.txt "
            "installs everything needed in a fresh environment."
        ),
        (
            "SETUP.md — Fully Rewritten for Gemini",
            "Step 1: Get Google API key from aistudio.google.com. "
            "Step 2: Create .env file with GOOGLE_API_KEY=... "
            "Step 3: pip install -r requirements.txt. "
            "Step 4: streamlit run app.py. "
            "Troubleshooting table: missing key, slow first run, ModuleNotFoundError.",
            "Old SETUP.md still referenced Ollama and Linux commands — completely wrong "
            "for the new Gemini-based stack on Windows."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # CHANGE 8 — GitHub Pushes
    # ════════════════════════════════════════════════════════════════════════════
    story.append(section_header("8", "GitHub — All Changes Pushed to madhan-4413/projects"))
    story.append(bullet_block([
        (
            "Push 1 — Initial Project Files",
            "Commit: 'Add document-chat-rag project with clean setup and AI features roadmap PDF'. "
            "Files: app.py, requirements.txt, README.md, SETUP.md, AI_Feature_Suggestions_Roadmap.pdf, "
            "main_self_hosted_vectorDB.ipynb, rag_demo.ipynb.",
            "First push of the cleaned project to the remote repository."
        ),
        (
            "Push 2 — README Rewrite",
            "Commit: 'Update README.md with comprehensive project documentation, architecture, and tech stack'.",
            "README was completely rewritten and needed to be synced to GitHub."
        ),
        (
            "Push 3 — Gemini Integration + Security",
            "Commit: 'Switch LLM from local Ollama to Google Gemini with secure .env configuration'. "
            "Files changed: app.py, requirements.txt, SETUP.md, .gitignore (new).",
            "Major code changes needed to be versioned and backed up on GitHub."
        ),
        (
            "Push 4 — .env.example Template",
            "Commit: 'Add .env.example template'. "
            "Added .env.example so collaborators know which API key variables are required.",
            "Best practice for open-source projects — never commit real secrets, always commit a template."
        ),
        (
            "Authentication Method Used",
            "Personal Access Token (PAT) with 'repo' scope provided by the user. "
            "Used as: git push https://madhan-4413:<TOKEN>@github.com/madhan-4413/projects.git main",
            "GitHub no longer accepts password authentication for Git operations over HTTPS. "
            "PAT is the recommended alternative."
        ),
        (
            "Rebase Used (Not Merge)",
            "git fetch + git rebase FETCH_HEAD used to resolve push rejections "
            "when the remote had commits not present locally.",
            "Rebase keeps a cleaner, linear commit history compared to merge commits."
        ),
    ]))
    story.append(Spacer(1, 8))

    # ── Summary table ─────────────────────────────────────────────────────────
    story.append(Paragraph("Files Changed — Complete Reference", h2_s))
    files_data = [
        [Paragraph("<b>File</b>", body_s), Paragraph("<b>Action</b>", body_s), Paragraph("<b>Reason</b>", body_s)],
        [Paragraph("app.py", body_s),                         Paragraph("Modified", body_s), Paragraph("Gemini LLM, .env loading, full-doc summarization router", body_s)],
        [Paragraph("requirements.txt", body_s),               Paragraph("Modified", body_s), Paragraph("Added gemini, dotenv, google-generativeai packages", body_s)],
        [Paragraph("README.md", body_s),                      Paragraph("Rewritten", body_s),Paragraph("Complete rewrite with architecture, tech stack, roadmap", body_s)],
        [Paragraph("SETUP.md", body_s),                       Paragraph("Rewritten", body_s),Paragraph("Updated for Gemini API key setup instead of Ollama", body_s)],
        [Paragraph(".env", body_s),                           Paragraph("Created",  body_s), Paragraph("Stores GOOGLE_API_KEY securely outside source code", body_s)],
        [Paragraph(".env.example", body_s),                   Paragraph("Created",  body_s), Paragraph("Public template showing required env variable names", body_s)],
        [Paragraph(".gitignore", body_s),                     Paragraph("Created",  body_s), Paragraph("Prevents .env, __pycache__, venv from being committed", body_s)],
        [Paragraph("AI_Feature_Suggestions_Roadmap.pdf",body_s),Paragraph("Created",body_s),Paragraph("PDF report of all recommended AI features and roadmap", body_s)],
        [Paragraph("docs/dspy.pdf", body_s),                  Paragraph("Deleted",  body_s), Paragraph("Irrelevant sample PDF — not part of this project", body_s)],
        [Paragraph("resources/thumbnail.png", body_s),        Paragraph("Deleted",  body_s), Paragraph("External demo image from template — not needed locally", body_s)],
        [Paragraph("docs/ & resources/ (dirs)", body_s),      Paragraph("Deleted",  body_s), Paragraph("Empty directories removed after file cleanup", body_s)],
        [Paragraph("generate_suggestions_pdf.py", body_s),    Paragraph("Deleted",  body_s), Paragraph("Temporary script — removed after PDF was generated", body_s)],
    ]
    ft = Table(files_data, colWidths=[160, 65, 307])
    ft.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), colors.HexColor("#EFF6FF")),
        ("TEXTCOLOR",     (0,0),(-1,0), PRIMARY),
        ("BACKGROUND",    (0,1),(-1,-1), LIGHT_BG),
        ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [LIGHT_BG, colors.white]),
    ]))
    story.append(ft)

    doc.build(story)
    print(f"SUCCESS: {OUTPUT} successfully generated.")

if __name__ == "__main__":
    build()
