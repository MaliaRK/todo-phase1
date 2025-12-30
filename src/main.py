"""
Main application entry point for the Todo Application CLI
"""
from src.storage import InMemoryStorage
from src.services import TaskService
from src.cli import CLI


def main():
    """
    Application entry point and command loop
    """
    print("Welcome to the Todo Application CLI!")
    print("Type 'help' for available commands or 'exit' to quit.")

    # Initialize the application components
    storage = InMemoryStorage()
    task_service = TaskService(storage)
    cli = CLI(task_service)

    while True:
        try:
            user_input = input("\ntodo> ").strip()

            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if user_input.lower() == 'help':
                result = cli.execute_help_command()
                print(result)
                continue

            # Parse the command
            command, args = cli.parse_command(user_input)

            # Execute the appropriate command
            if command == 'add':
                result = cli.execute_add_command(args)
                print(result)
            elif command == 'list':
                result = cli.execute_list_command()
                print(result)
            elif command == 'complete':
                result = cli.execute_complete_command(args)
                print(result)
            elif command == 'incomplete':
                result = cli.execute_incomplete_command(args)
                print(result)
            elif command == 'update':
                result = cli.execute_update_command(args)
                print(result)
            elif command == 'delete':
                result = cli.execute_delete_command(args)
                print(result)
            elif command == 'help':
                result = cli.execute_help_command()
                print(result)
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")

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