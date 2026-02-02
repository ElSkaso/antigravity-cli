import os
import google.generativeai as genai
from dotenv import load_dotenv

def init_ai():
    """Lädt API Key und konfiguriert Gemini."""
    load_dotenv() # Versucht .env zu laden (lokal oder root)
    # Fallback: Root .env explizit suchen, falls CWD nicht root ist
    if not os.getenv("GOOGLE_API_KEY") and os.path.exists("../.env"):
        load_dotenv("../.env")
        
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ WARNUNG: Kein GOOGLE_API_KEY gefunden.")
        return False
    
    genai.configure(api_key=api_key)
    return True

MODEL_NAME = "gemini-pro-latest"

def generate(system_instruction: str, user_prompt: str) -> str:
    """Sendet Prompt an Gemini und gibt Antwort zurück."""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # Wir kombinieren System Prompt und User Prompt hier,
        # da gemini-pro-latest "system_instruction" Parameter hat, aber
        # strukturierter Prompt oft besser funktioniert.
        # Fallback: Alles in den Prompt, wenn das Modell keine System-Instructions unterstützt.
        
        full_prompt = f"{system_instruction}\n\n{user_prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # Hier könnte man Logging einbauen
        raise e
