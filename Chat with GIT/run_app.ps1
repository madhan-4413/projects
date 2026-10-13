$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
Write-Host "Starting Chat with GitHub (Google Gemini RAG)..." -ForegroundColor Cyan
streamlit run app.py
