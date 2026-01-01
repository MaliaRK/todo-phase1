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
        Parse the 'add' command to extract title, description, priority, and tags
        Expected format: "add <title> - <description> -p <priority> -t <tag1>,<tag2>"
        """
        if not command_args.strip():
            raise ValueError("Add command requires a title")

        title = ""
        description = None
        priority = "Medium"  # Default priority
        tags = []

        # Process the command args to extract options
        # First, check if priority is specified
        priority_part = None
        if ' -p ' in command_args:
            parts = command_args.split(' -p ', 1)
            command_args = parts[0]  # The main part without priority
            priority_part = parts[1]  # The part after -p

        # Then check if tags are specified in the original command
        tags_part = None
        if ' -t ' in command_args:
            main_parts = command_args.split(' -t ', 1)
            command_args = main_parts[0]  # The main part without tags
        elif ' -t ' in priority_part or (priority_part and ' -t ' in priority_part):
            # Tags specified after priority
            priority_parts = priority_part.split(' -t ', 1)
            priority_part = priority_parts[0]
            tags_part = priority_parts[1]

        # Extract title and description from the main command part
        if ' - ' in command_args:
            title, description = command_args.split(' - ', 1)
            title = title.strip()
            description = description.strip()
        else:
            title = command_args.strip()

        # Process priority if specified
        if priority_part:
            priority = priority_part.strip()
            # Check if tags are specified after priority
            if ' -t ' in priority_part:
                priority_parts = priority_part.split(' -t ', 1)
                priority = priority_parts[0].strip()
                tags_part = priority_parts[1]

        # Process tags if specified
        if tags_part:
            tags = [tag.strip() for tag in tags_part.split(',') if tag.strip()]

        # Validate priority
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be one of: High, Medium, Low")

        return title, description, priority, tags

    def execute_add_command(self, command_args: str) -> str:
        """
        Execute the 'add' command with user feedback
        """
        try:
            title, description, priority, tags = self.parse_add_command(command_args)
            task = self.task_service.add_task(title, description, priority, tags)
            return f"Task added successfully with ID {task.id}: {task.title}\nPriority: {task.priority}, Tags: {', '.join(task.tags) if task.tags else 'None'}"
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
            for task in tasks:
                formatted_task = self.task_service.format_task_display(task)
                result.append(formatted_task)
                result.append("")  # Add blank line between tasks
            return "\n".join(result).strip()
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
        Expected format: "update <id> <new_title> - <new_description> -p <new_priority> -t <new_tags>"
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

            # Process the content part to extract title, description, priority, and tags
            title = None
            description = None
            priority = None
            tags = None

            # Check if priority or tags are specified
            if ' -p ' in content_part or ' -t ' in content_part:
                # Extract title and description from the main part
                main_part = content_part
                if ' -p ' in content_part:
                    main_part, rest = content_part.split(' -p ', 1)
                    priority = rest.split(' ')[0]  # Get the priority value
                    # Check if tags follow after priority
                    if ' -t ' in rest:
                        priority = rest.split(' -t ')[0].strip()
                        tags_part = rest.split(' -t ')[1]
                        tags = [tag.strip() for tag in tags_part.split(',') if tag.strip()]
                elif ' -t ' in content_part:
                    main_part, tags_part = content_part.split(' -t ', 1)
                    tags = [tag.strip() for tag in tags_part.split(',') if tag.strip()]

                # Now extract title and description from main_part
                if ' - ' in main_part:
                    title, description = main_part.split(' - ', 1)
                    title = title.strip()
                    description = description.strip()
                else:
                    title = main_part.strip()
            else:
                # No priority or tags specified, handle as before
                if ' - ' in content_part:
                    title, description = content_part.split(' - ', 1)
                    title = title.strip()
                    description = description.strip()
                else:
                    title = content_part.strip()

            # Validate priority if provided
            if priority and priority not in ["High", "Medium", "Low"]:
                return f"Error: Priority must be one of: High, Medium, Low"

            task = self.task_service.update_task(task_id, title, description, priority, tags)
            return f"Task {task_id} updated successfully"
        except ValueError:
            return "Error: Invalid task ID or command format. Use: update <id> <title> - <description> -p <priority> -t <tags>"
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

    def execute_search_command(self, keyword: str) -> str:
        """
        Execute the 'search' command to search tasks by keyword
        """
        try:
            if not keyword.strip():
                return "Error: Search command requires a keyword to search for"

            keyword = keyword.strip()
            tasks = self.task_service.search_tasks(keyword)

            if not tasks:
                return f"No tasks found matching '{keyword}'."

            result = []
            result.append(f"Search results for '{keyword}':")
            result.append("")
            for task in tasks:
                formatted_task = self.task_service.format_task_display(task)
                result.append(formatted_task)
                result.append("")  # Add blank line between tasks
            return "\n".join(result).strip()
        except Exception as e:
            return f"Error searching tasks: {str(e)}"

    def execute_filter_command(self, filter_args: str) -> str:
        """
        Execute the 'filter' command to filter tasks by status, priority, or tag
        Expected format: "filter status:<completed|incomplete>" or "filter priority:<High|Medium|Low>" or "filter tag:<tag_name>"
        """
        try:
            if not filter_args.strip():
                return "Error: Filter command requires filter criteria. Use: filter status:<value> or filter priority:<value> or filter tag:<value>"

            filter_args = filter_args.strip().lower()

            if filter_args.startswith('status:'):
                status_value = filter_args[7:]  # Remove 'status:' prefix
                if status_value in ['completed', 'done', 'true']:
                    tasks = self.task_service.filter_by_status(True)
                elif status_value in ['incomplete', 'todo', 'false']:
                    tasks = self.task_service.filter_by_status(False)
                else:
                    return "Error: Status must be one of: completed, incomplete"
            elif filter_args.startswith('priority:'):
                priority_value = filter_args[9:]  # Remove 'priority:' prefix
                priority_value = priority_value.capitalize()  # Capitalize to match expected values
                if priority_value not in ["High", "Medium", "Low"]:
                    return "Error: Priority must be one of: High, Medium, Low"
                tasks = self.task_service.filter_by_priority(priority_value)
            elif filter_args.startswith('tag:'):
                tag_value = filter_args[4:]  # Remove 'tag:' prefix
                tasks = self.task_service.filter_by_tag(tag_value)
            else:
                return "Error: Invalid filter format. Use: filter status:<value> or filter priority:<value> or filter tag:<value>"

            if not tasks:
                return "No tasks found matching the filter criteria."

            result = []
            result.append(f"Filter results for {filter_args}:")
            result.append("")
            for task in tasks:
                formatted_task = self.task_service.format_task_display(task)
                result.append(formatted_task)
                result.append("")  # Add blank line between tasks
            return "\n".join(result).strip()
        except Exception as e:
            return f"Error filtering tasks: {str(e)}"

    def execute_sort_command(self, sort_args: str) -> str:
        """
        Execute the 'sort' command to sort tasks by priority, alphabetically, or by creation order
        Expected format: "sort priority" or "sort alpha" or "sort creation"
        """
        try:
            if not sort_args.strip():
                return "Error: Sort command requires a sort method. Use: sort priority, sort alpha, or sort creation"

            sort_args = sort_args.strip().lower()
            all_tasks = self.task_service.list_tasks()

            if sort_args in ['priority', 'by priority', 'p']:
                sorted_tasks = self.task_service.sort_by_priority(all_tasks)
            elif sort_args in ['alpha', 'alphabetical', 'a']:
                sorted_tasks = self.task_service.sort_alphabetically(all_tasks)
            elif sort_args in ['creation', 'id', 'c']:
                sorted_tasks = self.task_service.sort_by_creation(all_tasks)
            else:
                return "Error: Sort method must be one of: priority, alpha, creation"

            if not sorted_tasks:
                return "No tasks to sort."

            result = []
            result.append(f"Tasks sorted by {sort_args}:")
            result.append("")
            for task in sorted_tasks:
                formatted_task = self.task_service.format_task_display(task)
                result.append(formatted_task)
                result.append("")  # Add blank line between tasks
            return "\n".join(result).strip()
        except Exception as e:
            return f"Error sorting tasks: {str(e)}"

    def execute_help_command(self) -> str:
        """
        Execute the 'help' command to display available commands
        """
        help_text = """
Available commands:
  add <title> - <description> -p <priority> -t <tags>    : Add a new task
  list                         : List all tasks
  search <keyword>             : Search tasks by keyword
  filter <criteria>            : Filter tasks (status:, priority:, tag:)
  sort <method>                : Sort tasks (priority, alpha, creation)
  complete <task_id>           : Mark task as complete
  incomplete <task_id>         : Mark task as incomplete
  update <task_id> <title> - <description> -p <priority> -t <tags> : Update a task
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