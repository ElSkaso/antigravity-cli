import os
import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# --- KONFIGURATION & SETUP ---

# Wir laden .env trotzdem für den API Key (der gehört zum Tool, nicht zum Projekt)
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Standard-Settings
MODEL_NAME = "gemini-pro-latest" 
FILES = ["MISSION.md", "SPEC_PRODUCT.md", "SPEC_TECH.md", "PROGRESS.md", "TODO.md", "BRAINSTORM.md", "CONTEXT_AI.md"]

# Globale Variable für den Projektpfad (wird im Main-Block gesetzt)
PROJECT_ROOT = "."
AG_DIR = "ag"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if not API_KEY:
    print("⚠️ WARNUNG: Kein GOOGLE_API_KEY gefunden.")

genai.configure(api_key=API_KEY)

# --- MODELS ---
class FileUpdate(BaseModel):
    content: str

class GenerateRequest(BaseModel):
    file_name: str
    current_content: str
    instruction: str

# --- HELPER FUNCTIONS ---

def get_target_path(filename: str) -> str:
    """Konstruiert den vollen Pfad ins Zielprojekt/ag/"""
    return os.path.join(PROJECT_ROOT, AG_DIR, filename)

def ensure_ag_dir():
    """Stellt sicher, dass der ag/ Ordner existiert"""
    target_dir = os.path.join(PROJECT_ROOT, AG_DIR)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"📁 Ordner erstellt: {target_dir}")

def get_project_context(exclude_file: str):
    context = ""
    for filename in FILES:
        if filename != exclude_file:
            path = get_target_path(filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    context += f"\n--- {filename} ---\n{f.read()}\n"
    return context

# --- ENDPOINTS ---

@app.get("/config")
def get_config():
    # Wir geben auch den Pfad zurück, damit man im UI sieht, wo man arbeitet
    return {
        "model": MODEL_NAME,
        "project_root": os.path.abspath(PROJECT_ROOT)
    }

@app.get("/files/{file_name}")
def read_file(file_name: str):
    file_path = get_target_path(file_name)
    if not os.path.exists(file_path):
        return {"content": ""}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/{file_name}")
def save_file(file_name: str, update: FileUpdate):
    ensure_ag_dir() # Sicherstellen, dass der Ordner da ist, bevor wir schreiben
    file_path = get_target_path(file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(update.content)
    return {"status": "success", "path": file_path}

@app.post("/generate")
def generate_content(req: GenerateRequest):
    model = genai.GenerativeModel(MODEL_NAME)
    project_context = get_project_context(req.file_name)
    
    prompt = f"""
    Du bist der Antigravity Architect.
    
    PROJEKT KONTEXT (Read-Only):
    {project_context}
    
    TARGET DATEI ({req.file_name}):
    {req.current_content}
    
    ANWEISUNG:
    {req.instruction}
    
    Antworte NUR mit dem Inhalt der Markdown-Datei.
    """
    
    try:
        response = model.generate_content(prompt)
        return {"generated": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- CLI ENTRY POINT ---

if __name__ == "__main__":
    # Hier parsen wir die Argumente, BEVOR Uvicorn startet
    parser = argparse.ArgumentParser(description="Startet den Antigravity Server für ein Projekt.")
    parser.add_argument("path", nargs="?", default=".", help="Pfad zum Root-Ordner des Zielprojekts")
    
    args = parser.parse_args()
    
    # Pfad setzen und validieren
    PROJECT_ROOT = args.path
    if not os.path.isdir(PROJECT_ROOT):
        print(f"❌ Fehler: Der Pfad '{PROJECT_ROOT}' existiert nicht.")
        exit(1)
        
    print(f"🚀 Antigravity zielt auf: {os.path.abspath(PROJECT_ROOT)}")
    print(f"📂 Erwarte AG-Ordner in: {os.path.join(PROJECT_ROOT, AG_DIR)}")
    
    # Server starten
    uvicorn.run(app, host="127.0.0.1", port=8000)