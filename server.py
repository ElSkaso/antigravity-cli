# server.py
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

# --- KONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Hier ändern wir das Modell zentral
MODEL_NAME = "gemini-2.5-flash" 

app = FastAPI(title="Antigravity API")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Setup
if API_KEY:
    genai.configure(api_key=API_KEY)

# Datenmodelle (Pydantic)
class FileUpdate(BaseModel):
    content: str

class GenerateRequest(BaseModel):
    file_name: str
    current_content: str
    instruction: str

# --- ENDPOINTS ---

@app.get("/ping")
def ping():
    return {
        "status": "online", 
        "model": MODEL_NAME,
        "api_key_set": bool(API_KEY)
    }

@app.get("/files/{filename}")
def read_file(filename: str):
    file_path = Path(filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return {"content": file_path.read_text(encoding="utf-8")}

@app.post("/files/{filename}")
def save_file(filename: str, update: FileUpdate):
    file_path = Path(filename)
    file_path.write_text(update.content, encoding="utf-8")
    return {"status": "saved", "file": filename}

@app.post("/generate")
def generate_content(req: GenerateRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key missing in .env")

    model = genai.GenerativeModel(MODEL_NAME)

    system_prompt = (
        "Du bist ein Senior Software Architect. "
        "Antworte NUR mit dem Inhalt der Markdown-Datei. "
        "Kein 'Hier ist dein Text'. Sei präzise."
    )

    full_prompt = (
        f"{system_prompt}\n"
        f"Datei: {req.file_name}\n"
        f"Kontext:\n{req.current_content}\n"
        f"Anweisung: {req.instruction}"
    )

    try:
        response = model.generate_content(full_prompt)
        return {"generated": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))