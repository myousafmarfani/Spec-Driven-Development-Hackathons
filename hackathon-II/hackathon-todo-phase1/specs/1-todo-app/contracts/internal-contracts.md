# API Contracts: Todo Application - Phase I

**Feature**: Todo Application - Phase I
**Date**: 2026-02-08

## Internal Method Contracts

### Task Class
- `__init__(self, title: str, description: str = "") -> Task`: Creates a new task with validation
- `to_dict(self) -> dict`: Returns task data as dictionary
- `__str__(self) -> str`: Returns string representation of task

### TaskStorage Class
- `add(self, task: Task) -> int`: Adds task and returns assigned ID
- `get_by_id(self, task_id: int) -> Optional[Task]`: Returns task by ID or None
- `get_all(self) -> List[Task]`: Returns all tasks
- `update(self, task_id: int, title: str = None, description: str = None) -> bool`: Updates task, returns success
- `delete(self, task_id: int) -> bool`: Deletes task by ID, returns success

### TaskManager Class
- `create_task(self, title: str, description: str = "") -> dict`: Creates task with validation, returns result
- `list_tasks(self) -> List[dict]`: Returns all tasks as dictionaries
- `update_task(self, task_id: int, title: str = None, description: str = None) -> dict`: Updates task, returns result
- `delete_task(self, task_id: int) -> dict`: Deletes task, returns result
- `toggle_complete(self, task_id: int) -> dict`: Toggles task completion status, returns result

### CLI Interface
- `run(self) -> None`: Starts the main application loop
- `display_menu(self) -> None`: Shows the main menu options
- `handle_add_task(self) -> None`: Handles adding a new task
- `handle_list_tasks(self) -> None`: Handles displaying all tasks
- `handle_update_task(self) -> None`: Handles updating a task
- `handle_delete_task(self) -> None`: Handles deleting a task
- `handle_toggle_task(self) -> None`: Handles toggling task status