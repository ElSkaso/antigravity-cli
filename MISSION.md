# Mission & Philosophy

## 1. The Vision
* **Core Problem:** Maintaining manual context files (`PROGRESS.md`) creates friction. Friction leads to abandonment.
* **Solution:** A CLI tool that manages the project state automatically.
* **Mantra:** "Context as Code." The documentation updates itself as a side-effect of working.

## 2. Strategic Goals
* **Zero-Friction Context:** Updating the project status must be faster than writing a commit message.
* **Single Source of Truth:** `PROGRESS.md` is always in sync with Git.
* **MVP Scope:** Support `start`, `finish`, and `status` commands within 24 hours.

## 3. The "Antigravity" Principles
* **Radical Simplicity:** No database. The Markdown files *are* the database.
* **Invisibility:** The tool should feel like a native git extension.
* **Fail Safe:** If file parsing fails, do not destroy data. Abort and warn.
