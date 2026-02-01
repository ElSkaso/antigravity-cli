# templates.py
# Die DNA des Grand-Architect Frameworks

FILES = {
    "MISSION.md": """# 🎯 Mission
> **The Why.**
> What is the ultimate goal? What problem are we solving?

## Core Objective
* [ ] Define the primary goal here.

## Non-Goals
* [ ] What are we NOT doing?
""",

    "SPEC_PRODUCT.md": """# 📦 Product Specification
> **The What.**
> Features, User Stories, UX flow.

## User Persona
* **Who:** ...

## Core Features (MVP)
1. Feature A
2. Feature B
""",

    "SPEC_TECH.md": """# ⚙️ Technical Specification
> **The How.**
> Architecture, Stack, Data Models.

## Stack
* Python / Typer
* Git

## Data Model
* ...
""",

    "PROGRESS.md": """# 🚧 Progress & Changelog
> **The When.**
> Current status and history.

## Status
* **Phase:** Initialization
* **Current Task:** Setup Project Structure

## Roadmap
* [ ] Phase 1: MVP
* [ ] Phase 2: Refinement

## Changelog
* **Init:** Project created via Antigravity CLI.
""",

    "todo.md": """# ✅ Todo List
> Tactical, small steps.

* [ ] Initial Commit
""",
    
    ".gitignore": """# Standard Python Gitignore
__pycache__/
*.py[cod]
venv/
.env
.DS_Store
.vscode/
"""
}

# Optional: Standard Requirements
REQUIREMENTS = """typer
rich
"""