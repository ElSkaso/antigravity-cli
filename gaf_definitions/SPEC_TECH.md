# Technical Specification

## 1. Architecture Patterns
* **Sidecar Pattern:** The tool runs independently alongside the target project.
* **Client-Server:** Python FastAPI Backend + React Frontend.

## 2. Tech Stack
* **Backend:** Python 3.10+, FastAPI, Uvicorn.
* **Frontend:** React, Vite, TailwindCSS.
* **AI:** Google Gemini Pro via `google-generativeai`.

## 3. Data Model
* **Format:** Pure Markdown (`.md`).
* **Storage:** Local Filesystem (No Database).

## 4. Constraints & Decisions (ehemals stack_decisions)
> Diese Regeln sind unverhandelbar für den AI-Architekten.

* **[DECISION-001] No Database:**
    * *Constraint:* Wir nutzen keine SQL/NoSQL Datenbank.
    * *Reasoning:* Das Tool muss "portable" sein und darf keine versteckten State-Files haben. Alles muss für den User in Textform lesbar sein.
    
* **[DECISION-002] Python Standard Lib first:**
    * *Constraint:* Vermeide externe Dependencies wenn möglich.
    * *Reasoning:* Einfache Installation für neue User.

* **[DECISION-003] No Eldrazi References:**
    * *Constraint:* Keine Magic: The Gathering Referenzen im Code oder UI.
    * *Reasoning:* User Preference (Streng!).