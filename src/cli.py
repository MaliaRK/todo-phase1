"""
Command-line interface for the Todo Application CLI
"""
from typing import Optional
from .services import TaskService
from .models import Task


class CLI:
    """
    Command-line interface and input parsing
    """
    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    def parse_add_command(self, command_args: str) -> tuple:
        """
        Parse the 'add' command to extract title and description
        Expected format: "add <title> - <description>"
        """
        if not command_args.strip():
            raise ValueError("Add command requires a title")

        # Check if the command contains a description separator
        if ' - ' in command_args:
            title, description = command_args.split(' - ', 1)
            title = title.strip()
            description = description.strip()
        else:
            title = command_args.strip()
            description = None

        return title, description

    def execute_add_command(self, command_args: str) -> str:
        """
        Execute the 'add' command with user feedback
        """
        try:
            title, description = self.parse_add_command(command_args)
            task = self.task_service.add_task(title, description)
            return f"Task added successfully with ID {task.id}: {task.title}"
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error adding task: {str(e)}"

    def execute_list_command(self) -> str:
        """
        Execute the 'list' command to display all tasks
        """
        try:
            tasks = self.task_service.list_tasks()
            if not tasks:
                return "No tasks found."

            result = []
            result.append("ID | Status    | Title")
            result.append("---|-----------|------")
            for task in tasks:
                status = "Complete" if task.completed else "Incomplete"
                title = task.title
                result.append(f"{task.id:2} | {status:9} | {title}")
            return "\n".join(result)
        except Exception as e:
            return f"Error listing tasks: {str(e)}"

    def execute_complete_command(self, command_args: str) -> str:
        """
        Execute the 'complete' command to mark a task as complete
        """
        try:
            if not command_args.strip():
                return "Error: Complete command requires a task ID"

            task_id = int(command_args.strip())
            task = self.task_service.toggle_task_completion(task_id)
            return f"Task {task_id} marked as complete"
        except ValueError:
            return "Error: Invalid task ID. Please provide a valid number."
        except Exception as e:
            return f"Error completing task: {str(e)}"

    def execute_incomplete_command(self, command_args: str) -> str:
        """
        Execute the 'incomplete' command to mark a task as incomplete
        """
        try:
            if not command_args.strip():
                return "Error: Incomplete command requires a task ID"

            task_id = int(command_args.strip())
            task = self.task_service.toggle_task_completion(task_id)
            return f"Task {task_id} marked as incomplete"
        except ValueError:
            return "Error: Invalid task ID. Please provide a valid number."
        except Exception as e:
            return f"Error marking task as incomplete: {str(e)}"

    def execute_update_command(self, command_args: str) -> str:
        """
        Execute the 'update' command to update a task
        Expected format: "update <id> <new_title> - <new_description>"
        """
        try:
            if not command_args.strip():
                return "Error: Update command requires a task ID and new content"

            # Split by first space to separate task ID from the rest
            parts = command_args.split(' ', 1)
            if len(parts) < 2:
                return "Error: Update command requires a task ID and new content"

            task_id_str, content_part = parts
            task_id = int(task_id_str)

            # Check if the content part contains a description separator
            if ' - ' in content_part:
                title, description = content_part.split(' - ', 1)
                title = title.strip()
                description = description.strip()
            else:
                title = content_part.strip()
                description = None

            task = self.task_service.update_task(task_id, title, description)
            return f"Task {task_id} updated successfully"
        except ValueError:
            return "Error: Invalid task ID or command format. Use: update <id> <title> - <description>"
        except Exception as e:
            return f"Error updating task: {str(e)}"

    def execute_delete_command(self, command_args: str) -> str:
        """
        Execute the 'delete' command to delete a task
        """
        try:
            if not command_args.strip():
                return "Error: Delete command requires a task ID"

            task_id = int(command_args.strip())
            success = self.task_service.delete_task(task_id)
            if success:
                return f"Task {task_id} deleted successfully"
            else:
                return f"Error: Task with ID {task_id} not found"
        except ValueError:
            return "Error: Invalid task ID. Please provide a valid number."
        except Exception as e:
            return f"Error deleting task: {str(e)}"

    def execute_help_command(self) -> str:
        """
        Execute the 'help' command to display available commands
        """
        help_text = """
Available commands:
  add <title> - <description>    : Add a new task
  list                         : List all tasks
  complete <task_id>           : Mark task as complete
  incomplete <task_id>         : Mark task as incomplete
  update <task_id> <title> - <description> : Update a task
  delete <task_id>             : Delete a task
  help                         : Show this help message
  exit or quit                 : Exit the application
        """.strip()
        return help_text

    def parse_command(self, user_input: str) -> tuple:
        """
        Parse user input to extract command and arguments
        """
        user_input = user_input.strip()
        if not user_input:
            return "invalid", ""

        parts = user_input.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        return command, args