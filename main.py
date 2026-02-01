import typer
import re
import subprocess
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Setup
app = typer.Typer(no_args_is_help=True)
console = Console()
PROGRESS_FILE = Path("PROGRESS.md")

def get_content():
    if not PROGRESS_FILE.exists():
        console.print("[bold red]❌ Error:[/bold red] PROGRESS.md not found.")
        raise typer.Exit(code=1)
    return PROGRESS_FILE.read_text(encoding="utf-8")

def parse_progress(content):
    phase_match = re.search(r"\* \*\*Phase:\*\* (.*)", content)
    task_match = re.search(r"\* \*\*Current Task:\*\* (.*)", content)
    phase = phase_match.group(1).strip() if phase_match else "Unknown"
    task = task_match.group(1).strip() if task_match else "Unknown"
    return phase, task

# --- COMMAND 1: STATUS ---
@app.command()
def status():
    """Zeigt den aktuellen Status an."""
    content = get_content()
    phase, task = parse_progress(content)

    status_content = Text()
    status_content.append("\n📍 Current Phase:\n", style="bold white")
    status_content.append(f"   {phase}\n", style="yellow")
    status_content.append("\n🔨 Current Task:\n", style="bold white")
    status_content.append(f"   {task}\n", style="cyan")

    console.print(Panel(
        status_content, 
        title="[bold green]Antigravity System Status[/bold green]",
        expand=False,
        border_style="green"
    ))

# --- COMMAND 2: START ---
@app.command()
def start(task_name: str):
    """Startet Task: Updated Markdown."""
    content = get_content()
    pattern = r"(\* \*\*Current Task:\*\* )(.*)"
    
    if not re.search(pattern, content):
        console.print("[bold red]❌ Error:[/bold red] 'Current Task' line missing.")
        raise typer.Exit(code=1)

    new_content = re.sub(pattern, f"\\1{task_name}", content)
    PROGRESS_FILE.write_text(new_content, encoding="utf-8")

    console.print(f"[bold green]🚀 Started Task:[/bold green] {task_name}")

# --- COMMAND 3: FINISH (The Magic) ---
@app.command()
def finish():
    """
    Beendet Task -> Loggt in Markdown -> Git Commit.
    """
    content = get_content()
    
    # 1. Aktuellen Task finden
    task_match = re.search(r"\* \*\*Current Task:\*\* (.*)", content)
    current_task = task_match.group(1).strip() if task_match else "Unknown"

    if current_task in ["Unknown", "Waiting for input", ""]:
        console.print("[yellow]⚠️  No active task to finish.[/yellow]")
        raise typer.Exit()

    # 2. Markdown Updaten
    # A. Task zurücksetzen
    new_content = re.sub(r"(\* \*\*Current Task:\*\* )(.*)", r"\1Waiting for input", content)
    
    # B. Ins Changelog schreiben
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"\n* **{timestamp}:** {current_task} (Completed)"
    
    # Wir hängen es einfach an das Ende der 'Changelog' Sektion (simpler Regex Hook)
    if "## Changelog" in new_content:
        new_content = new_content.replace("## Changelog", f"## Changelog{log_entry}")
    else:
        new_content += log_entry # Fallback

    PROGRESS_FILE.write_text(new_content, encoding="utf-8")
    console.print(f"[dim]📝 Logged to PROGRESS.md[/dim]")

    # 3. Git Automatisierung
    try:
        console.print("[bold blue]💾 Committing to Git...[/bold blue]")
        # Git Add
        subprocess.run(["git", "add", "."], check=True)
        # Git Commit mit Task Name
        commit_msg = f"Finish: {current_task}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        console.print(f"[bold green]✅ Success![/bold green] Task archived and committed.")
        
    except subprocess.CalledProcessError:
        console.print("[bold red]❌ Git Error:[/bold red] Did you run 'git init'?")
    except FileNotFoundError:
        console.print("[bold red]❌ Error:[/bold red] Git is not installed or not in PATH.")

if __name__ == "__main__":
    app()