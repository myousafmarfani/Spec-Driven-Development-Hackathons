# Phase I - Python Console Todo App

## Project Overview
In-memory todo application built using Spec-Driven Development.

## Spec-Kit Structure
- speckit.constitution - Project principles and standards
- speckit.specify - What to build (requirements)
- speckit.plan - How to build (architecture)
- speckit.tasks - Atomic work units

## Tech Stack
- Python 3.13+
- UV for package management
- In-memory storage (no database)
- Standard library only

## Development Workflow
1. Always read relevant spec before implementing
2. Reference task IDs in all code
3. Follow constitution principles
4. Implement only what tasks authorize

## Running the App
```bash
uv run python main.py
```

## Project Structure
See @speckit.plan for complete structure