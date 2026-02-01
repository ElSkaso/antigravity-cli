# Technical Specification

> **INPUT:** `SPEC_PRODUCT.md`
> **CONSTRAINTS:** `STACK_DECISIONS.md`

## 1. Architecture Overview
* **Pattern:** Command Controller (Typer) -> Logic Layer -> File I/O.
* **Entry Point:** `main.py`
* **Core Logic:** `core/manager.py` (Handles parsing).

## 2. Data Persistence (The Markdown DB)
* **Read Strategy:** Read `PROGRESS.md` line by line.
* **Parse Strategy:** Use Regex to identify `## Current Status` and `* **Current Task:**`.
* **Write Strategy:** Replace specific lines in memory and write back the full file atomically.

## 3. Implementation Details
* **CLI Library:** `typer`
* **UI Library:** `rich` (Console, Panel)
* **Git Integration:** Use `subprocess.run(["git", ...])`. Do not use huge git libraries.
