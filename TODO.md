# Development Task List

## Phase 1: MVP Core
- [ ] **Project Setup:**
    - [ ] Initialize `main.py` with `typer` for CLI command handling.
    - [ ] Create `core/manager.py` to encapsulate file parsing and writing logic.
- [ ] **`status` Command:**
    - [ ] Implement function to read `PROGRESS.md`.
    - [ ] Implement Regex-based parser to extract "Current Task".
    - [ ] Display the extracted status using a `rich.Panel`.
- [ ] **`start` Command:**
    - [ ] Implement `start <task_name>` command in `typer`.
    - [ ] Implement atomic file write logic: read all lines, replace the "Current Task" line in memory, and write the entire file back.
    - [ ] Add basic error handling to prevent data loss on parse failure.
    - [ ] Stage `PROGRESS.md` using `subprocess.run(["git", "add", "PROGRESS.md"])`.
- [ ] **`finish` Command:**
    - [ ] Implement `finish <commit_message>` command in `typer`.
    - [ ] Update "Current Task" to a completed/default state.
    - [ ] Prepend a new entry to the "Changelog" section.
    - [ ] Commit the changes using `subprocess.run(["git", "commit", ...])`.

## Phase 2: UI Polish
- [ ] **User Feedback:**
    - [ ] Implement a consistent color-coding scheme for success (green), warning (yellow), and error (red) messages.
    - [ ] Refine all command outputs to be clear, concise, and actionable.
- [ ] **Interactive Elements:**
    - [ ] Add interactive prompts for commands requiring confirmation (e.g., `finish` without a message).
    - [ ] Enhance `status` output with more `rich` components for better visual structure.
- [ ] **CLI Usability:**
    - [ ] Add help text and documentation for all commands and options using `typer`.
    - [ ] Ensure all non-AI commands execute under the 500ms performance target.

## Phase 3: AI Advanced Features
- [ ] **Backend Setup:**
    - [ ] Set up a basic FastAPI server to handle AI API calls.
    - [ ] Implement secure management for AI API keys (e.g., via environment variables).
- [ ] **AI Command Implementation:**
    - [ ] Implement `antigravity create "<prompt>"` to generate a new file.
    - [ ] Implement `antigravity ai expand --file <file> --section <section>` for content expansion.
    - [ ] Implement `antigravity ai summarize <file>` for document summarization.
    - [ ] Implement `antigravity ai refine <file>` for grammar and tone correction.
- [ ] **Advanced Git Integration:**
    - [ ] Implement `antigravity save "<commit_message>"` for a streamlined save-and-commit workflow.
- [ ] **Web UI (Stretch Goal):**
    - [ ] Initialize Vite + React frontend project.
    - [ ] Connect the web UI to the local FastAPI backend.