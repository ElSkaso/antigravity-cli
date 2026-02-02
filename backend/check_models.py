# check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Kein API Key in .env gefunden!")
else:
    genai.configure(api_key=api_key)
    print(f"✅ Key gefunden. Frage Google nach verfügbaren Modellen...\n")
    
    try:
        for m in genai.list_models():
            # Wir wollen nur Modelle, die Text generieren können
            if 'generateContent' in m.supported_generation_methods:
                print(f"👉 {m.name}")
    except Exception as e:
        print(f"❌ Fehler beim Abrufen: {e}")