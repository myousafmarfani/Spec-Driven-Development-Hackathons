# Data Model: Todo Application - Phase I

**Feature**: Todo Application - Phase I
**Date**: 2026-02-08

## Task Entity

### Properties
- **id**: int (unique, auto-generated)
- **title**: str (required, 1-200 characters)
- **description**: str (optional, max 1000 characters)
- **completed**: bool (default: False)
- **created_at**: datetime (auto-generated timestamp)

### Validations
- Title must be between 1-200 characters
- Description, if provided, must not exceed 1000 characters
- ID must be unique across all tasks
- completed field must be boolean
- created_at must be a valid timestamp

### State Transitions
- New task: completed=False (default)
- Toggle operation: completed=!completed (toggles current state)

## Relationships
- No relationships with other entities; self-contained entity

## Business Rules
- Task must have a unique ID upon creation
- Task status defaults to incomplete when created
- All tasks must have a title between 1-200 characters
- Task descriptions are optional but limited to 1000 characters if provided