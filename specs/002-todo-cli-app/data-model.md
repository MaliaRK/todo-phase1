# Data Model: Todo Application CLI

## Task Entity

### Fields
- **id**: Integer, auto-incrementing, required, unique identifier
- **title**: String, required, task title or subject
- **description**: String, optional, detailed task description
- **completed**: Boolean, required, completion status (default: false)

### Validation Rules
- id: Must be a positive integer, auto-generated and unique
- title: Must be non-empty string, maximum 200 characters
- description: Optional string, maximum 1000 characters
- completed: Must be boolean value, defaults to False

### State Transitions
- completed: Can transition from False to True (incomplete → complete)
- completed: Can transition from True to False (complete → incomplete)

## Task Collection

### Structure
- **tasks**: Dictionary mapping task ID to Task object
- **next_id**: Integer tracking the next available ID for auto-increment

### Operations
- Add task: Insert task with auto-generated ID
- Get task: Retrieve task by ID
- Update task: Modify task fields by ID
- Delete task: Remove task by ID
- List tasks: Return all tasks in collection