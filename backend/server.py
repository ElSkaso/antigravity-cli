import os
import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Modules
from . import roles
from . import ai_engine
from . import fs_manager

# Init AI Engine
if not ai_engine.init_ai():
    print("⚠️  AI Engine konnte nicht initialisiert werden (API Key fehlt).")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class FileUpdate(BaseModel):
    content: str

class GenerateRequest(BaseModel):
    file_name: str
    current_content: str
    instruction: str

# --- ENDPOINTS ---

@app.get("/config")
def get_config():
    # Wir geben auch den Pfad zurück, damit man im UI sieht, wo man arbeitet
    return {
        "model": ai_engine.MODEL_NAME,
        "project_root": os.path.abspath(fs_manager.get_root())
    }

@app.get("/files/{file_name}")
def read_file(file_name: str):
    try:
        content = fs_manager.read_file(file_name)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/{file_name}")
def save_file(file_name: str, update: FileUpdate):
    try:
        path = fs_manager.save_file(file_name, update.content)
        return {"status": "success", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def generate_content(req: GenerateRequest):
    # 1. Rolle bestimmen
    role_key = roles.determine_role_for_file(req.file_name) # Assuming logic moved to roles or staying here?
    # Wait, roles logic was determined in server.py before. 
    # User provided snippet puts determine_role_for_file in server.py.
    # But now server.py should be lean. The logic essentially belongs to "roles" or "server".
    # I kept "determine_role_for_file" in server.py in previous turn.
    # But cleaner is to move it to roles.py? 
    # For now, I will keep helper in server.py OR move it to roles.py if I can edit roles.py.
    # User said "Use this code as inspiration: server.py... determine_role_for_file".
    # So it was in server.py. I will define it right here again or keep it if I didn't delete it?
    # I am replacing the whole file, so I need to include it or import it.
    # roles.py was created by USER. I can't edit it easily without tool call?
    # I can edit roles.py.
    # Let's put logic here for now to be safe, or check if roles.py has it.
    # Viewing roles.py earlier showed only definitions.
    
    # Let's re-implement determine_role_for_file here or use a helper.
    # Better: Put it in server.py for now as orchestration logic.
    
    current_role = determine_role_for_file(req.file_name)
    system_prompt = roles.get_role_prompt(current_role)
    
    # 2. Context holen
    project_context = fs_manager.get_project_context(exclude_file=req.file_name)
    
    # 3. Prompt bauen
    # Diese Logik könnte auch in AI Engine, aber AI Engine soll "dumm" sein.
    # Also bauen wir den User-Prompt hier.
    
    user_prompt = f"""
    PROJEKT KONTEXT (Read-Only):
    {project_context}
    
    TARGET DATEI ({req.file_name}):
    {req.current_content}
    
    ANWEISUNG:
    {req.instruction}
    
    Antworte NUR mit dem Inhalt der Markdown-Datei.
    """
    
    try:
        response_text = ai_engine.generate(system_prompt, user_prompt)
        return {"generated": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- CLI ENTRY POINT ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Startet den Antigravity Server.")
    parser.add_argument("path", nargs="?", default=".", help="Pfad zum Root-Ordner des Zielprojekts")
    args = parser.parse_args()
    
    # Root im FS Manager setzen
    try:
        fs_manager.set_root(args.path)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        exit(1)
        
    print(f"🚀 Antigravity Server gestartet.")
    uvicorn.run(app, host="127.0.0.1", port=8000)