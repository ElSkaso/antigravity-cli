# Product Specification (User Experience)

> **OWNER:** UX Visionary Mode
> **GOAL:** A CLI that feels like magic.

## 1. User Personas
* **The Developer (You):** Wants to code, hates administrative tasks. Needs instant feedback.

## 2. The Commands (User Stories)

### Story 1: "Checking Status"
* **Command:** `python main.py status`
* **Behavior:** Reads `PROGRESS.md` and displays current phase/task in a pretty ASCII box.

### Story 2: "Starting a Task"
* **Command:** `python main.py start "Fix login bug"`
* **Behavior:** Updates `PROGRESS.md` (Current Task), creates git branch (optional), prints success msg.

### Story 3: "Finishing a Task"
* **Command:** `python main.py finish`
* **Behavior:** Prompts for result, moves task to "Completed", commits to git automatically.

## 3. Design Guidelines
* **Color Coding:** Green (Success), Yellow (Working), Red (Error).
* **Speed:** Execution < 500ms.
