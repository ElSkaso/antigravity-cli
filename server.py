from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import glob

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfiguration
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-pro-latest" # gen ai model
FILES_DIR = "." # current directory
# These files should serve as context
CONTEXT_FILES = ["MISSION.md", "SPEC_PRODUCT.md", "SPEC_TECH.md", "PROGRESS.md", "TODO.md"]

if not API_KEY:
    raise ValueError("No API Key found!")

genai.configure(api_key=API_KEY)

class FileUpdate(BaseModel):
    content: str

class GenerateRequest(BaseModel):
    file_name: str
    current_content: str
    instruction: str

def get_project_context(exclude_file: str):
    """Liest alle anderen Markdown-Dateien, um Kontext zu geben."""
    context = ""
    for filename in CONTEXT_FILES:
        if filename != exclude_file and os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                context += f"\n--- INHALT VON {filename} ---\n"
                context += f.read()
                context += "\n--- ENDE ---\n"
    return context
# In server.py

@app.get("/config")
def get_config():
    return {"model": MODEL_NAME}
    
@app.get("/files/{file_name}")
def read_file(file_name: str):
    if not os.path.exists(file_name):
        # Falls Datei nicht existiert, leere zurückgeben (oder erstellen)
        return {"content": ""} 
    with open(file_name, "r", encoding="utf-8") as f:
        return {"content": f.read()}

@app.post("/files/{file_name}")
def save_file(file_name: str, update: FileUpdate):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(update.content)
    return {"status": "success"}

@app.post("/generate")
def generate_content(req: GenerateRequest):
    model = genai.GenerativeModel(MODEL_NAME)
    
    # 1. Wir holen den Kontext aller anderen Dateien
    project_context = get_project_context(req.file_name)
    
    # 2. Wir bauen den ultimativen Prompt
    prompt = f"""
    Du bist ein erfahrener Software-Architekt (Antigravity CLI).
    
    PROJEKT KONTEXT (Hintergrundwissen):
    {project_context}
    
    AKTUELLER FOKUS (Diese Datei bearbeitest du):
    Dateiname: {req.file_name}
    Inhalt:
    {req.current_content}
    
    ANWEISUNG DES USERS:
    {req.instruction}
    
    AUFGABE:
    Antworte NUR mit dem neuen Inhalt für die Datei '{req.file_name}'.
    Kein "Hier ist der Code", kein Markdown-Block um alles herum (außer es gehört in die Datei).
    Behalte den bestehenden Stil bei.
    """
    
    response = model.generate_content(prompt)
    return {"generated": response.text}