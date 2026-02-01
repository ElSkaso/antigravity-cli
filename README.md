# 🚀 Antigravity CLI

> **Context as Code.**
> Stop manually updating your documentation. Let your CLI do it while you work.

The **Antigravity CLI** is a Python-based tool designed to eliminate the friction between coding and reporting. It manages your project's status (`PROGRESS.md`) and your version control (`git`) with single commands.

## ✨ Features

* **⚡ Frictionless Workflow:** Update status and commit code in one go.
* **📄 Markdown as Database:** No SQLite, no JSON sidecars. The `PROGRESS.md` is the Single Source of Truth.
* **🧠 Auto-Context:** Keeps your AI agents (and your team) always in sync with the latest project status.
* **🛡️ Git Integration:** Automatically stages, commits, and timestamps your progress.
* **📊 History Export:** Generates clean Markdown tables of your changelog (`ag log --export`).

## 📦 Installation

```Bash
# Clone the repo
git clone [https://github.com/YOUR_USERNAME/antigravity-cli.git](https://github.com/YOUR_USERNAME/antigravity-cli.git)
cd antigravity-cli

# Setup venv & install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create Alias (optional but recommended)
echo "alias ag='$(pwd)/venv/bin/python $(pwd)/main.py'" >> ~/.zshrc
source ~/.zshrc
```


## 🕹️ Usage
**1. Start a Task**
Stop thinking about administrative overhead. Just work.

```Bash
ag start "Implement new login logic"
```
Updates `PROGRESS.md` "Current Task" and sets the mental context.


**2. Check Status**
See where you are at a glance.

```Bash
ag status
Displays a rich terminal panel with Phase and Task.
```

**3. Finish & Commit**
The magic moment. Archives the task and pushes to git.

```Bash
ag finish
Moves task to history, timestamps it, and runs git commit -m "Finish: ...".
```

**4. View History**
See what you accomplished.

```Bash
ag log          # Pretty table in terminal
ag log --export # Generates HISTORY.md for reporting
```

## 🏗️ The Antigravity Framework Structure
This tool is built to manage the Antigravity File Structure:

- `MISSION.md`: The Why.

- `SPEC_PRODUCT.md`: The What.

- `SPEC_TECH.md`: The How.

- `PROGRESS.md`: The When (Managed by this CLI).

***
Built with [Typer](https://typer.tiangolo.com/) & [Rich](https://rich.readthedocs.io/en/stable/).