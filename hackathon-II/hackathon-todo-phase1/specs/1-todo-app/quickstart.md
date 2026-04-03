# Quickstart Guide: Todo Application - Phase I

**Feature**: Todo Application - Phase I
**Date**: 2026-02-08

## Getting Started

This guide explains how to run and use the todo application with its core functionality.

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional, for dependency management)

## Running the Application

1. Clone or download the repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   python main.py
   ```

## Using the Application

Once launched, the application presents a menu-driven interface:

1. **Add Task**: Creates a new task with title and optional description
   - Prompts for task title (1-200 characters)
   - Optionally prompts for description (up to 1000 characters)
   - Automatically assigns a unique ID and sets status to incomplete

2. **View Tasks**: Displays all tasks with their details
   - Shows ID, title, description, and completion status
   - Lists all tasks in the current session

3. **Update Task**: Modifies an existing task's title or description
   - Requires the task ID to update
   - Allows changing title or description following the same validation rules

4. **Delete Task**: Removes a task by ID
   - Prompts for task ID to delete
   - Validates that the task exists before deletion

5. **Toggle Task Status**: Marks a task as complete/incomplete
   - Prompts for task ID
   - Switches the completion status from current state

## Exiting

Press the appropriate menu option or use Ctrl+C to exit the application.
Note: All tasks are stored in memory and will be lost when the application closes.