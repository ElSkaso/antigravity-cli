# templates.py
# The Antigravity DNA - Minimal, Compatible & Focused.

FILES = {
    "MISSION.md": """# 🎯 Mission
> **The Why.**
> What is the ultimate goal? What problem are we solving?

## Core Objective
* [ ] Define the primary goal here (One sentence).

## Non-Goals
* [ ] What are we NOT doing? (Scope defense).
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

    "TODO.md": """# ✅ Todo List
> Tactical, small steps.

* [ ] Initial Commit (`ag finish`)
* [ ] Fill out MISSION.md
""",

    "BRAINSTORM.md": """# 🧠 Brainstorming
> Unstructured ideas and notes.

* ...
""",

    "CONTEXT_AI.md": """# 🤖 AI Context
> Meta-Information for LLMs (Copy/Paste this).

## Project Identity
* **Name:** {name}
* **Goal:** See MISSION.md
* **Stack:** Python, Typer, Markdown-based State.

## Workflow rules
1. Update `PROGRESS.md` on every major step.
2. Keep code simple.
"""
}

REQUIREMENTS = """typer
rich
"""