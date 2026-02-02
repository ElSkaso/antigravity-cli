import os
from typing import List, Optional
try:
    from . import templates # Wenn als Modul importiert
except ImportError:
    import templates # Fallback

# Konstanten
AG_DIR = "gaf_definitions"
FILES = ["MISSION.md", "SPEC_PRODUCT.md", "SPEC_TECH.md", "PROGRESS.md", "TODO.md", "BRAINSTORM.md", "CONTEXT_AI.md"]

# State (Root Path)
_project_root = "."

def set_root(path: str):
    """Setzt den Root-Pfad für das Zielprojekt."""
    global _project_root
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pfad existiert nicht: {path}")
    _project_root = path
    print(f"🔧 Root gesetzt auf: {os.path.abspath(_project_root)}")

def get_root() -> str:
    return _project_root

def get_ag_path() -> str:
    """Gibt den vollen Pfad zum gaf_definitions Ordner zurück."""
    return os.path.join(_project_root, AG_DIR)

def get_file_path(filename: str) -> str:
    """Konstruiert den vollen Pfad zu einer Datei im gaf_definitions Ordner."""
    return os.path.join(get_ag_path(), filename)

def ensure_ag_dir():
    """Lazy Creation: Erstellt den gaf_definitions Ordner nur, wenn nötig."""
    target_dir = get_ag_path()
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"📁 Lazy Creation: Ordner erstellt: {target_dir}")
        # Optional: Initiale Dateien aus templates.py erstellen?
        # User sagte: "Er nutzt templates.py, um zu wissen, was der Standardinhalt einer neuen Datei ist."
        # Wenn wir den Ordner erstellen, sollten wir ihn vielleicht auch befüllen?
        # Im ursprünglichen Code war das nicht so (nur save_file hat ensure aufgerufen).
        # Wir belassen es bei "Folder creation", das Befüllen passiert beim Schreiben oder Init.

def read_file(filename: str) -> str:
    """Liest den Inhalt einer Datei."""
    path = get_file_path(filename)
    if not os.path.exists(path):
        return "" # Oder Default aus Template? Im alten Code war es "".
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_file(filename: str, content: str) -> str:
    """Schreibt Inhalt in Datei. Erstellt Ordner falls nötig."""
    ensure_ag_dir()
    path = get_file_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def get_project_context(exclude_file: Optional[str] = None) -> str:
    """Sammelt alle Markdown Dateien als Kontext."""
    context = ""
    for filename in FILES:
        if filename != exclude_file:
            content = read_file(filename)
            if content:
                context += f"\n--- {filename} ---\n{content}\n"
    return context

def list_files() -> List[str]:
    return FILES
