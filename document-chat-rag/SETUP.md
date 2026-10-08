# Windows Setup Guide — Document-Chat-RAG

## Step 1: Install Ollama

1. Go to **https://ollama.com/download/windows**
2. Download and run the **OllamaSetup.exe** installer
3. After installation, open a new PowerShell window and verify:
   ```powershell
   ollama --version
   ```

## Step 2: Pull the Llama 3.2 Model

Open PowerShell and run:
```powershell
ollama pull llama3.2
```
> ⏳ This downloads ~2GB. Wait until it says "success".

Verify the model is ready:
```powershell
ollama list
```

## Step 3: Start Ollama Server (if not auto-started)

```powershell
ollama serve
```
> Ollama usually auto-starts as a background service after install. If `ollama list` works, the server is already running.

## Step 4: Install Python Dependencies

```powershell
cd D:\projects\RAG\document-chat-rag
pip install -r requirements.txt
```

## Step 5: Run the App

```powershell
cd D:\projects\RAG\document-chat-rag
streamlit run app.py
```

The app will open at **http://localhost:8501**

## Step 6: Using the App

1. In the **sidebar**, click **"Browse files"** and upload a PDF
2. Wait for **"Ready to Chat!"** message (indexing may take 20–60 seconds)
3. Type your question in the chat box at the bottom
4. Use **"Clear ↺"** to reset the conversation

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ollama` not recognized | Restart PowerShell after installing Ollama |
| `Connection refused` on query | Run `ollama serve` in a separate terminal |
| Slow embedding (first run) | BGE model (~1.3GB) downloads on first use — wait |
| `ModuleNotFoundError` | Re-run `pip install -r requirements.txt` |
