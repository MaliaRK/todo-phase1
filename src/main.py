"""
Main application entry point for the Todo Application CLI
"""
from src.storage import InMemoryStorage
from src.services import TaskService
from src.cli import CLI


def main():
    """
    Application entry point and command loop with menu-driven interface
    """
    print("--- Todo Application ---")
    print("\nWelcome to the Todo Application CLI!")
    print("Select an option from the menu below:")

    # Initialize the application components
    storage = InMemoryStorage()
    task_service = TaskService(storage)
    cli = CLI(task_service)

    while True:
        try:
            print("\n--- Todo Application ---")
            print("\n1. Add Task")
            print("2. View All Tasks")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Mark Task Complete")
            print("6. Mark Task Incomplete")
            print("7. Search Tasks")
            print("8. Filter Tasks")
            print("9. Sort Tasks")
            print("10. Exit")
            print("\nEnter your choice (1-10):")

            user_input = input().strip()

            if user_input == '10' or user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            # Execute the appropriate menu option
            if user_input == '1':
                task_title = input("Enter task title: ")
                task_description = input("Enter task description (optional, press Enter to skip): ")
                if not task_description.strip():
                    task_description = None
                priority_input = input("Select priority (High/Medium/Low) [default: Medium]: ").strip()
                if not priority_input:
                    priority_input = "Medium"

                tags_input = input("Enter tags (comma-separated, optional, press Enter to skip): ").strip()
                tags = []
                if tags_input:
                    tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

                # Use CLI to execute the add command with the inputs
                command_args = f"{task_title}"
                if task_description:
                    command_args += f" - {task_description}"
                if priority_input:
                    command_args += f" -p {priority_input}"
                if tags:
                    command_args += f" -t {','.join(tags)}"

                result = cli.execute_add_command(command_args)
                print(result)
            elif user_input == '2':
                result = cli.execute_list_command()
                print(result)
            elif user_input == '3':
                task_id = input("Enter task ID to update: ")
                task_title = input("Enter new task title (or press Enter to keep current): ")
                task_description = input("Enter new task description (or press Enter to keep current): ")

                update_args = f"{task_id} "
                if task_title.strip():
                    update_args += f"{task_title}"
                    if task_description.strip():
                        update_args += f" - {task_description}"
                elif task_description.strip():
                    update_args += f"  - {task_description}"
                else:
                    update_args = task_id  # Just ID if no updates

                # Check if priority or tags are to be updated
                priority_update = input("Enter new priority (High/Medium/Low) or press Enter to keep current: ").strip()
                if priority_update:
                    update_args += f" -p {priority_update}"

                tags_update = input("Enter new tags (comma-separated) or press Enter to keep current: ").strip()
                if tags_update:
                    update_args += f" -t {tags_update}"

                result = cli.execute_update_command(update_args)
                print(result)
            elif user_input == '4':
                task_id = input("Enter task ID to delete: ")
                result = cli.execute_delete_command(task_id)
                print(result)
            elif user_input == '5':
                task_id = input("Enter task ID to mark complete: ")
                result = cli.execute_complete_command(task_id)
                print(result)
            elif user_input == '6':
                task_id = input("Enter task ID to mark incomplete: ")
                result = cli.execute_incomplete_command(task_id)
                print(result)
            elif user_input == '7':
                keyword = input("Enter search keyword: ")
                result = cli.execute_search_command(keyword)
                print(result)
            elif user_input == '8':
                print("Filter options:")
                print("1. By status (completed/incomplete)")
                print("2. By priority (High/Medium/Low)")
                print("3. By tag")
                filter_choice = input("Select filter type (1-3): ").strip()

                if filter_choice == '1':
                    status = input("Enter status (completed/incomplete): ").strip().lower()
                    filter_args = f"status:{status}"
                elif filter_choice == '2':
                    priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()
                    filter_args = f"priority:{priority}"
                elif filter_choice == '3':
                    tag = input("Enter tag name: ").strip()
                    filter_args = f"tag:{tag}"
                else:
                    print("Invalid filter choice")
                    continue

                result = cli.execute_filter_command(filter_args)
                print(result)
            elif user_input == '9':
                print("Sort options:")
                print("1. By priority")
                print("2. Alphabetically")
                print("3. By creation order")
                sort_choice = input("Select sort method (1-3): ").strip()

                if sort_choice == '1':
                    sort_args = "priority"
                elif sort_choice == '2':
                    sort_args = "alpha"
                elif sort_choice == '3':
                    sort_args = "creation"
                else:
                    print("Invalid sort choice")
                    continue

                result = cli.execute_sort_command(sort_args)
                print(result)
            else:
                print(f"Invalid menu choice: {user_input}. Please enter a number between 1-10.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()