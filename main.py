
import os
import pdfplumber
import openai
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()  # Loads GROQ_API_KEY from .env

openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = os.getenv("GROQ_API_KEY")

app = FastAPI(title="Rental Agreement Analyzer")

@app.get("/", response_class=HTMLResponse)
async def form():
    return '''
    <html>
    <head><title>Rental Agreement Analyzer</title></head>
    <body style="font-family: Arial, sans-serif;">
      <h2>Rental Agreement Analyzer</h2>
      <form action="/analyze" enctype="multipart/form-data" method="post">
        <input name="file" type="file" accept="application/pdf" required>
        <button type="submit">Analyze</button>
      </form>
    </body>
    </html>
    '''

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):
    # save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # extract text from PDF
    extracted_text = ""
    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
    os.remove(temp_path)

    # call Groq (Mixtral) API
    response = openai.ChatCompletion.create(
        model="mixtral-8x22b",
        messages=[
            {"role": "system", "content": "You are a legal assistant. Provide a concise analysis of the following rental agreement."},
            {"role": "user", "content": extracted_text}
        ],
        temperature=0.25,
        max_tokens=1000
    )

    analysis = response.choices[0].message["content"].replace("\n", "<br>")

    return f'''
    <html>
    <head><title>Analysis Result</title></head>
    <body style="font-family: Arial, sans-serif;">
      <h2>Analysis Result</h2>
      <div>{analysis}</div>
      <hr>
      <a href="/">Analyze another document</a>
    </body>
    </html>
    '''
