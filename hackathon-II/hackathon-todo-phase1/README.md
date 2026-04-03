# Hackathon II - Phase I: Todo Console App

## Overview
Command-line todo application with in-memory storage, built using Spec-Driven Development.

## Features (Basic Level)
- ✅ Add Task (title + description)
- ✅ View All Tasks
- ✅ Update Task
- ✅ Delete Task
- ✅ Mark as Complete/Incomplete

## Setup Instructions

### Prerequisites
- Python 3.13+
- UV package manager

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd hackathon-todo-phase1

# Install dependencies
uv sync

# Run application
uv run python main.py
```

## Usage
After running the application, you will see a command prompt. Type 'help' to see available commands:

- `add` - Add a new task with title and optional description
- `list` or `view` - View all tasks with their status
- `update` - Update an existing task's title or description
- `delete` - Delete a task by ID
- `complete` or `toggle` - Mark a task as complete/incomplete
- `help` - Show available commands
- `quit` or `exit` - Exit the application

Example workflow:
1. Type 'add' to create a new task
2. Enter the task title (1-200 characters)
3. Optionally enter a description (max 1000 characters)
4. Use 'list' to view all your tasks
5. Use other commands as needed

## Spec-Driven Development
This project follows SDD methodology:
- See /specs for all specifications
- See CLAUDE.md for Claude Code instructions
- All code maps to tasks in speckit.tasks

## Author
Muhammad Yousaf

## Hackathon
GIAIC Hackathon II - Phase I