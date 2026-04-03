"""CLI interface for the Todo Application."""

from typing import Optional
from src.managers.task_manager import TaskManager


class CLIInterface:
    """Command-line interface for the todo application."""

    def __init__(self):
        """Initialize the CLI interface with a task manager."""
        self.manager = TaskManager()

    def run(self):
        """Start the main application loop."""
        print("Welcome to the Todo Application!")
        print("Type 'help' for a list of commands.")

        while True:
            try:
                command = input("\nEnter command: ").strip().lower()

                if command == "quit" or command == "exit":
                    print("Goodbye!")
                    break
                elif command == "help":
                    self.display_help()
                elif command == "add":
                    self.handle_add_task()
                elif command == "list" or command == "view":
                    self.handle_list_tasks()
                elif command == "update":
                    self.handle_update_task()
                elif command == "delete":
                    self.handle_delete_task()
                elif command == "complete" or command == "toggle":
                    self.handle_toggle_task()
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

    def display_help(self):
        """Display available commands."""
        print("\nAvailable commands:")
        print("  add      - Add a new task")
        print("  list     - View all tasks")
        print("  update   - Update an existing task")
        print("  delete   - Delete a task")
        print("  complete - Mark a task as complete/incomplete")
        print("  help     - Show this help message")
        print("  quit     - Exit the application")

    def handle_add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")

        title = input("Enter task title (1-200 characters): ").strip()
        if not title:
            print("Error: Title is required")
            return

        description = input("Enter task description (optional, max 1000 characters): ").strip()

        result = self.manager.create_task(title, description)

        if result["success"]:
            print(f"✓ {result['message']}")
            task = result["task"]
            if task:
                status = "✓" if task["completed"] else "○"
                print(f"  [{status}] {task['id']}: {task['title']}")
        else:
            print(f"✗ {result['message']}")

    def handle_list_tasks(self):
        """Handle listing all tasks."""
        print("\n--- Task List ---")

        result = self.manager.list_tasks()

        if result["success"]:
            tasks = result["tasks"]
            if not tasks:
                print("No tasks found.")
            else:
                print(f"You have {len(tasks)} task(s):\n")
                for task in tasks:
                    status = "✓" if task["completed"] else "○"
                    print(f"  [{status}] {task['id']}: {task['title']}")
                    if task["description"]:
                        print(f"      Description: {task['description']}")
                    print(f"      Created: {task['created_at']}")
                    print()
        else:
            print(f"✗ {result['message']}")

    def handle_update_task(self):
        """Handle updating a task."""
        print("\n--- Update Task ---")

        try:
            task_id_str = input("Enter task ID to update: ").strip()
            if not task_id_str:
                print("Error: Task ID is required")
                return

            task_id = int(task_id_str)
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if the task exists first
        existing_result = self.manager.storage.storage.get_by_id(task_id)
        if not existing_result:
            print(f"Error: Task with ID {task_id} does not exist")
            return

        print(f"Updating task {task_id}: {existing_result.title}")

        title_input = input(f"Enter new title (current: '{existing_result.title}', press Enter to keep current): ").strip()
        desc_input = input(f"Enter new description (current: '{existing_result.description}', press Enter to keep current): ").strip()

        # Prepare update values
        new_title = title_input if title_input else None
        new_description = desc_input if desc_input else None

        # Only update if changes were provided
        if new_title is not None or new_description is not None:
            result = self.manager.update_task(task_id, new_title, new_description)

            if result["success"]:
                print(f"✓ {result['message']}")
                task = result["task"]
                if task:
                    status = "✓" if task["completed"] else "○"
                    print(f"  [{status}] {task['id']}: {task['title']}")
            else:
                print(f"✗ {result['message']}")
        else:
            print("No changes made to the task.")

    def handle_delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")

        try:
            task_id_str = input("Enter task ID to delete: ").strip()
            if not task_id_str:
                print("Error: Task ID is required")
                return

            task_id = int(task_id_str)
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        result = self.manager.delete_task(task_id)

        if result["success"]:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ {result['message']}")

    def handle_toggle_task(self):
        """Handle toggling task completion status."""
        print("\n--- Toggle Task Completion ---")

        try:
            task_id_str = input("Enter task ID to toggle: ").strip()
            if not task_id_str:
                print("Error: Task ID is required")
                return

            task_id = int(task_id_str)
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        result = self.manager.toggle_complete(task_id)

        if result["success"]:
            print(f"✓ {result['message']}")
            task = result["task"]
            if task:
                status = "✓" if task["completed"] else "○"
                print(f"  [{status}] {task['id']}: {task['title']}")
        else:
            print(f"✗ {result['message']}")


def main():
    """Main entry point for the CLI interface."""
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()