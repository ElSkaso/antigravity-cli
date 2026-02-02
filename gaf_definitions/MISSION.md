# Mission & Philosophy

## 1. The Vision
*   **Problem:** Manual maintenance of context files like `PROGRESS.md` leads to significant overhead, which hinders the acceptance and up-to-dateness of project documentation.
*   **Solution:** Provision of a command-line tool for automated project status management and dynamic documentation updates.
*   **Guiding Principle:** "Context as Code." Project documentation is generated and maintained as an integral side effect of operational activities.

### Technical Key Features
*   **Markdown-based Persistence:** Utilizing existing Markdown files as the primary data storage medium to ensure transparency and reduce system complexity.
*   **Seamless Git Integration:** Tight coupling with the Git version control system to synchronize project status and emulate native Git commands.
*   **Robust Data Integrity:** Implementation of protective mechanisms against data loss and corruption, especially in case of file parser errors, through transaction-like file processing and warnings.

## 2. Strategic Goals
*   **Zero-Friction Context:** Updating the project status must be faster than writing a commit message.
*   **Single Source of Truth:** `PROGRESS.md` is always in sync with Git.
*   **MVP Scope:** Support `start`, `finish`, and `status` commands within 24 hours.

## 3. The "Antigravity" Principles
*   **Radical Simplicity:** No database. The Markdown files *are* the database.
*   **Invisibility:** The tool should feel like a native git extension.
*   **Fail Safe:** If file parsing fails, do not destroy data. Abort and warn.