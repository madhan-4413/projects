# Windows Setup Guide — Document-Chat-RAG (Google Gemini)

## Step 1: Configure Google Gemini API Key

1. Get your API key from **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2. Create or open the `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   *(Note: The `.env` file is already added to `.gitignore` to prevent leaking secrets to GitHub).*

---

## Step 2: Install Python Dependencies

Open PowerShell and navigate to the project directory:
```powershell
cd D:\projects\document-chat-rag
pip install -r requirements.txt
```

---

## Step 3: Run the Streamlit Application

```powershell
cd D:\projects\document-chat-rag
streamlit run app.py
```

The application will open automatically in your browser at **`http://localhost:8501`**.

---

## Step 4: Using the App

1. In the **sidebar**, click **"Browse files"** and upload a PDF document.
2. Wait for the **"Ready to Chat!"** notification (embedding model downloads automatically on first run).
3. Type your question in the chat input at the bottom to receive real-time answers synthesized by **Google Gemini**.
4. Click **"Clear ↺"** at any time to reset conversation history and cache.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `GOOGLE_API_KEY not found in .env` | Verify that `.env` exists in `document-chat-rag/` with your valid key. |
| Slow embedding (first run) | The `bge-large-en-v1.5` model (~1.3GB) downloads only on first launch. |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` to install missing packages. |
