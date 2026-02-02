# 🚀 Antigravity Studio

> **Context as Code.**
> The ultimate goal is to create an orchestration manager that allows you to delegate software projects to AI agents.

**Antigravity Studio** is a "Sidecar" application that runs alongside your actual software project. It uses **Google Gemini (`gemini-pro-latest`)** to act as your AI Architect, helping you draft Missions, Specs, and Tech definitions while keeping you in full control via a visual Diff-View.

Instead of polluting your project with tool-specific configs, Antigravity acts as a cleanly separated "Manager" that injects structure only where needed.

## ✨ Features

* **🛰️ Sidecar Architecture:** The tool lives outside your target project. It manages documentation and code injection without forcing its own dependencies on your codebase.
* **🧠 AI Architect:** Built-in integration with `gemini-pro-latest` to generate and refine architecture documents based on your prompts.
* **⚡ Hot-Plug:** Connect to any project on your disk simply by passing the path (e.g., `python backend/server.py ../my-project`).
* **📂 Lazy Structure:** Automatically creates the `gaf_definitions/` folder structure in your target project only when you confirm a change.

## 📦 Installation

The Studio consists of a Python Backend (Logic & AI) and a React Frontend (UI).

### 1. Backend Setup (Python)

```bash
# Clone the repo
git clone [https://github.com/YOUR_USERNAME/antigravity-studio.git](https://github.com/YOUR_USERNAME/antigravity-studio.git)
cd antigravity-studio

# Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Dependencies
pip install fastapi uvicorn google-generativeai python-dotenv
```

### 2. Frontend Setup (Node.js)

```bash
cd gui
npm install
```

### 3. Configuration
Create a `.env` file in the root folder of the studio:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 🕹️ Usage

Since this is a client-server application, you generally need two terminal windows.

**Terminal 1: The Backend (Brain)**
Point the server to the project you want to manage.
```bash
# Syntax: python backend/server.py [PATH_TO_TARGET_PROJECT]
source venv/bin/activate
python backend/server.py ../my-plant-app
```

**Terminal 2: The Frontend (Interface)**
```bash
cd gui
npm run dev
```

**Open Studio:**
Go to [http://localhost:5173](http://localhost:5173) in your browser.

## 🏗️ The Framework Structure
Antigravity manages the following "Grand-Architect" files within an `gaf_definitions/` folder in your target project:

* `MISSION.md`: The Strategic Vision (The Why).
* `SPEC_PRODUCT.md`: The Features & User Stories (The What).
* `SPEC_TECH.md`: The Architecture & Data Structure (The How).
* `PROGRESS.md`: The Current State & Changelog (The When).

***
Built with **FastAPI**, **React**, and **Google Gemini**.O