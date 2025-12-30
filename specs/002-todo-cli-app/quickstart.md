# Quickstart: Todo Application CLI

## Setup
1. Ensure Python 3.13+ is installed
2. Install UV package manager
3. Create virtual environment and install dependencies
4. Run the application with `python main.py`

## Usage
- `add <title> - <description>` - Add a new task
- `list` - Display all tasks
- `complete <task_id>` - Mark task as complete
- `incomplete <task_id>` - Mark task as incomplete
- `update <task_id> <new_title> - <new_description>` - Update task
- `delete <task_id>` - Delete task
- `help` - Show available commands
- `exit` or `quit` - Exit the application

## Example Workflow
1. Add a task: `add Buy groceries - Get milk and bread`
2. View tasks: `list`
3. Mark complete: `complete 1`
4. Update task: `update 1 Buy weekly groceries - Get all needed items`
5. Delete task: `delete 1`