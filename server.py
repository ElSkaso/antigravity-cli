# server.py
# The Brain of Antigravity Studio

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Konfiguration laden
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-1.5-pro"

app = FastAPI(title="Antigravity API")


# CORS erlauben (damit React später zugreifen darf)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Setup
if API_KEY:
    genai.configure(api_key=API_KEY)

# Datenmodelle
class FileUpdate(BaseModel):
    content: str

class GenerateRequest(BaseModel):
    file_name: str
    current_content: str
    instruction: str

# --- ENDPOINTS ---

@app.get("/ping")
def ping():
    # Jetzt verrät der Ping sogar, welches Gehirn wir nutzen!
    return {
        "status": "online", 
        "model": MODEL_NAME,
        "api_key_set": bool(API_KEY) # Zeigt True/False, ohne den Key zu verraten
    }

@app.get("/files/{filename}")
def read_file(filename: str):
    """Liest eine Markdown-Datei aus dem aktuellen Verzeichnis."""
    file_path = Path(filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return {"content": file_path.read_text(encoding="utf-8")}

@app.post("/files/{filename}")
def save_file(filename: str, update: FileUpdate):
    """Speichert Inhalt in eine Datei."""
    file_path = Path(filename)
    file_path.write_text(update.content, encoding="utf-8")
    return {"status": "saved", "file": filename}

@app.post("/generate")
def generate_content(req: GenerateRequest):
    """Der Kern: Ruft Gemini auf."""
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key missing in .env")

    model = genai.GenerativeModel(MODEL_NAME)

    # Der Grand Architect System Prompt
    system_prompt = (
        "Du bist ein Senior Software Architect (Grand Architect Level). "
        "Deine Aufgabe ist es, professionelle technische Dokumentationen zu schreiben. "
        "Antworte NUR mit dem Inhalt der Markdown-Datei. Kein 'Hier ist dein Text'. "
        "Halte dich strikt an technische Fakten. Sei präzise. Nutze Listen."
    )

    full_prompt = (
        f"{system_prompt}\n"
        f"Datei: {req.file_name}\n"
        f"Aktueller Inhalt/Kontext:\n{req.current_content}\n"
        f"User Anweisung: {req.instruction}"
    )

    try:
        response = model.generate_content(full_prompt)
        return {"generated": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))