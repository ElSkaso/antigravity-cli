# Technical Stack & Constraints

## 1. Core Stack
* **Language:** Python 3.9+
* **CLI Framework:** `Typer` (Standard for modern Python CLIs).
* **Output:** `Rich` (For tables/colors).

## 2. Constraints
* **No Database:** Do NOT introduce SQLite/JSON sidecars. The Markdown is the Source of Truth.
* **No Heavy Git Libs:** Use `subprocess` for git commands.
* **Dependencies:** Keep `requirements.txt` tiny.

## 3. Non-Goals
* A GUI interface.
* Multi-user support (Git handles conflicts).
