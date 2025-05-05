
# Rental Agreement Analyzer (MVP)

Simple FastAPI service that allows users to upload a rental agreement PDF and get an AI-generated analysis.

## Setup locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_key"
uvicorn main:app --reload
```

## Deploy on Render

1. Fork this repo to GitHub.
2. Sign in to [Render](https://render.com) and choose "New Web Service".
3. Connect your GitHub repo and accept defaults.
4. Add an environment variable `GROQ_API_KEY` with your key from https://console.groq.com.
5. Deploy! Render will build and run the service on a free URL like https://rental-agreement-analyzer.onrender.com
